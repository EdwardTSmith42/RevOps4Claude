# V3 Origination, EasyAPISummary, and the Offer Engine

How credit decisions and financing offers work for enterprise EasyAPI providers (LaserAway parent 16681, Milan parent 28551, and similar). Learned building the LaserAway/Milan approval-rate and Credit-Limit-Enforcement SSRS reports (2026-06).

## Server / data source

- The `ProductionCopy` MCP connection is server **AG2-Prod-SQL-Az**, database **HFDprod** (the production OLTP). This is a different server/DB name than `hfdsqlfinance` / `HFDProd_Finance`, which is a copy that also carries `EasyAPISummary`, `Applications`, `Providers`.
- SSRS reaches AG2/HFDprod via the shared data source **`/Data Sources/ProdAG2ProductionRealTimeReadOnly`** (`Initial Catalog=HFDProd`, stored creds, id `660f22ea-9689-4cb5-8023-7c037f738633`). Real-time read replica, fast.
- **HFDprod is compatibility level 130**: no `STRING_AGG`, no `TRIM`. Use `STUFF(... FOR XML PATH(''))` for string aggregation, `LTRIM(RTRIM())` for trim. (JSON functions `OPENJSON`/`JSON_VALUE` work at 130.)

## V3 gotcha: declines/approvals are NOT in dbo.Applications

In Origination V3 (the EasyAPI flow), an application does not write to `HFDprod.dbo.Applications` until it is **signed** (status `CONF`). For LaserAway/Milan, `Applications` is ~100% `CONF`. Every credit decision (approve/decline/pending/ineligible) lives in **`HFDprod.dbo.EasyAPISummary`** (EAS). So approval rate, decline reasons, and unsigned amounts all come from EAS plus the offer tables below, never from `Applications` alone.

## EasyAPISummary (decision log)

- **`AccountId`** (GUID, nvarchar) = the Application Unique Key, stable per application. `ApplicationId` (hex) and `SessionId` change per attempt; do not use them as the app key.
- Many rows per `AccountId` (re-submits and program-tier attempts). To get the application of record, dedupe by `AccountId` taking the latest row (`MAX(Id)`); use `MIN(SubmittedOn)` per `AccountId` as the application created date.
- `Disposition`: Approved / Declined / Pending Approval / Ineligible.
- `CreditGrade` (A-E), `RiskScore`, `RiskModel` (e.g. BankLoan, OffersAdjustment), **`ScorebreakModel` = the risk pipeline / look** (e.g. "LaserAway 2nd Look"), `ProgramCode`, `Region`, `FinancialInstrument`, `SubmittedOn` (UTC), `ProviderId` (nvarchar; join `Providers` via `TRY_CAST(ProviderId AS INT)`). No dollar amounts on EAS.
- `CriticalMessage` = JSON array of decline reasons, e.g. `[{"ErrorCode":"D02","Description":"...","Meta":null}]`. Only Declined/Ineligible rows have one; Approved/Pending do not. Codes seen: D01 age, **D02 thin/no credit file**, D03 bankruptcy, D05 delinquent on existing loan, D07 insufficient credit, D08 identity, **D09 = Loan Stacking** (Decline; message "Active loan count (X) meets or exceeds limit (Y) for credit grade Z"; D/E grades, max 1 active loan; live for LaserAway V3), **E36 = Credit Limit Enforcement** (Ineligible disposition; "Maximum credit limit has been reached"; Meta `{"availableCredit":...}`; checks the requested amount against the grade-specific aggregate credit cap, runs after loan stacking), E17 no credit bureau report, P01/P02 existing-loan late/delinquent (Meta "Triggered applications: <ids>").

**Do not confuse D09 with Credit Limit Enforcement.** Per Confluence (RO/3868590082 "Loan Stacking, Credit Limit Enforcement & Friendly Fraud Detection Process"; IT/2551185409 "Risk Engine"; IT/4225499142 "Risk Event Documentation" - "when CLE returns AvailableCredit the policy emits E36 instead of D02"): **D09 = loan stacking** (the >=1-active-loan count check, Decline), **E36 = the actual Credit Limit Enforcement code** (Ineligible, emitted by policy `EnsureCreditLimitNotReachedWithHFD`). CLE is live for ~20 Easy Apply/API providers but **V3-pending**, so E36 reads 0 for LaserAway/Milan (V3) while D09 fires (loan stacking is live for LaserAway V3). Dispositions in EAS: Decline = D-codes (D01-D09), Pend = P-codes (P01-P04), **Ineligible = E-codes** (E01-E09, E17, E36).
- Exclude test rows with `ISNULL(IsTest,0)=0`.
- On the hfdsqlfinance copy EAS is indexed `NCI_SubmittedOn` and on `AccountId`. EAS is large; always bound by `SubmittedOn`. The `mssql` MCP connector times out on multi-month EAS aggregations; validate against `ProductionCopy` (AG2 is fast).

## Approval rate (matches the Tableau "HFD" datasource)

Definition (per the Tableau workbook): `COUNTD(Approved Application Unique Key) / COUNTD(Submitted Application Unique Key)`, where Submitted statuses = `DOC,APR,CONF,DCN,PND,CIF,CRW` and Approved = `APR,CONF,DOC`.

Reconstruct on production from EAS: per `AccountId`, take the latest row's `Disposition` and map Approved to approved+submitted, Declined and 'Pending Approval' to submitted-only, Ineligible to excluded. This tracks the Tableau number without touching `Applications`. A program-code funnel groups this by `ProgramCode`; the signed/contract count for the same program comes from `Applications` (status `CONF`), and funded count/$ from `SAOPurchaseHistory` origination - combine the EAS aggregate and the Applications aggregate with a `FULL OUTER JOIN` on `ProgramCode` (a program can have submissions but no signs in a window, or vice versa).

## Timezones: EAS is UTC, Applications is Pacific (the warehouse mixes them)

Verified 2026-06-22 on AG2-Prod-SQL-Az (`SYSDATETIME()` = `SYSUTCDATETIME()` minus 7h, i.e. the server runs **Pacific**):

- **EAS datetime columns are UTC** - `SubmittedOn`, `SessionStartedOn`, `ApplicationSubmittedOn` (all within seconds of each other, all match `SYSUTCDATETIME()`).
- **`HFDprod.dbo.Applications.CreatedOn` / `ActivatedOn` are PACIFIC** (server-local; `MAX(CreatedOn)` matched `SYSDATETIME()`, not UTC). So a report touching both EAS and Applications mixes timezones and must convert one side.
- **Display a UTC column in Pacific:** `CAST(col AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific Standard Time' AS datetime2(0))` (the Windows zone id handles PST/PDT; `AT TIME ZONE` works at compat 130).
- **Filter a UTC column by a Pacific-local date param and keep the index seek** - convert the *param boundary* to UTC, not the column:
  ```sql
  WHERE eas.SubmittedOn >= CAST(CAST(@StartDate AS datetime2) AT TIME ZONE 'Pacific Standard Time' AT TIME ZONE 'UTC' AS datetime2)
    AND eas.SubmittedOn <  CAST(CAST(DATEADD(DAY,1,@EndDate) AS datetime2) AT TIME ZONE 'Pacific Standard Time' AT TIME ZONE 'UTC' AS datetime2)
  ```
  Wrapping the column in `AT TIME ZONE` makes the predicate non-SARGable on a 400k-rows/month table. Applications-side date filters need no conversion - they are already Pacific.

## EAS raw decision-detail columns and PII handling

For a decision-level / launch-monitoring detail report, EAS carries these display columns (beyond the decision fields above): `FirstName`, `LastName`, `NationalId`, `NationalIdLastFour`, `OFACResult` ('clear' or a hit) plus `OFACScore`, `CreditScore` (nvarchar) and `FICO` (nvarchar) and `CreditScoreType`, `SessionStartedOn` (UTC). Apply the `pci-pii-guard` skill:

- **`EAS.NationalId` is RAW national-id / SSN data** (9 chars, ~81k distinct, no masking - verified, NOT a hash). Never display it raw. Hash for display: `CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', LTRIM(RTRIM(NationalId))), 2)` - one-way, consistent per person (good for spotting repeat applicants / loan stacking). This SHA-256 does **not** match the canonical analytic `DimPerson.PersonHashedNationalId` (uppercase MD5); if you need to join consumer-side, hash to that MD5 convention instead.
- **`FirstName` / `LastName` are raw PII.** The existing "LaserAway Milan Approval Detail" report masks the patient to initial + last: `LEFT(ISNULL(LTRIM(FirstName),''),1) + '. ' + ISNULL(LastName,'')`. Follow that precedent.
- **`CriticalMessage` components for a non-tech display:** `JSON_VALUE(CriticalMessage,'$[0].ErrorCode')`, `'$[0].Description'`, `'$[0].Meta'`, each guarded by `ISJSON(CriticalMessage)=1`. Multi-element arrays are ~0% (7 rows since 2026-06 across all programs), so reading `$[0]` covers it.
- **Volume:** ~400k raw EAS rows/month across all programs. A raw-detail section must be `TOP`-capped (e.g. `TOP 3000 ... ORDER BY SubmittedOn DESC`) and used scoped by program/provider; unfiltered it is unusable.

## Program code for a funnel: use Applications.ProgramCode, not the origination row

For a program-code funnel/summary on the signed side, group and filter by **`Applications.ProgramCode`** (set at application time), not by the `SAOPurchaseHistory` origination row's `ProgCode`. The origination row exists only **after funding**, so sourcing program code from it silently drops every approved-but-unfunded application and caps the report at the last funded date. (Verified: a launch-monitoring report sourced program code from origination and missed 16 of 298 `CUS-ASPEN2ND-DNT-PRM-1.1` apps, stopping at 6/17 instead of current.) `a.ProgramCode` equals the origination `ProgCode` for 99.97% of funded loans, so switching the source does not move funded numbers. The full three-section report (EAS conversion funnel by program code, activated detail by created date/status, EAS raw history; all Pacific-time, PII-masked) was built 2026-06 as `/Testing/Matt/LaunchMonitoring - Applications`.

## FinanceOffer.dbo.OfferHistory (requested + offered amounts, including unsigned apps)

- `ApplicationId` (nvarchar 128) **= EAS.AccountId**. Indexed `IX_OfferHistory_ApplicationId` (INCLUDEs Request, Response, CreateDateUTC), so `OUTER APPLY (SELECT TOP 1 ... WHERE ApplicationId = @k ORDER BY CreateDateUTC DESC)` is a fast seek. Do not scan or `ORDER BY CreateDateUTC` unfiltered; the table is huge and that times out.
- Many rows per app (re-quotes); take the latest by `CreateDateUTC`.
- **`Request`** (JSON object): `$.ServiceCost` = the requested treatment amount (matches signed `Applications.TotalCost`). Also `$.ProgramCode`, `$.Region`, `$.FinancialInstrument`.
- **`Response`** (JSON array of offer options; empty `[]` when no offers were generated). Each element: `$.MaxFinanceAmount` = the assigned credit limit, `$.MinFinanceAmount` / `$.MinTreatmentAmount` = provider floor, `$.DefaultFinanceAmount`, `$.ServiceCost`, `$.ProgramCode`, `$.TermMonths`, `$.InterestRate`, `$.Name`, `$.Id`. Use `JSON_VALUE(Response,'$[0].MaxFinanceAmount')` for the limit (consistent across elements).
- Coverage: roughly 100% of approved apps and ~73% of declines have an OfferHistory request (the rest declined before an offer was requested).
- This is the source for requested/limit amounts on **unsigned** apps. Over-limit ("asked for more than the limit") = `ServiceCost > Response[0].MaxFinanceAmount`, measurable for all apps that received an offer, not just signed.

## FinanceOffer.dbo.ProviderConfigs (the offer catalog) and why an app gets no offers

- One row per provider: `ProviderId`, `Document` (nvarchar(max) JSON, ~160-220 KB). `Document.$.Offers` is an array (e.g. 141 offers for one provider).
- Each offer element fields: `Active` (true/false), `ArchivedDateUTC` (non-null means archived/dead), `ProgramCode`, **`Condition`** (eligibility expression string, e.g. `$.CreditGrade = 'A' AND ($.Request.ProgramCode = $.ProgramCode OR $.Request.Section = $.ProgramCode)`), `Criteria` (human summary, often null), `MinFinanceAmount` / `MaxFinanceAmount` (eligible amount range), `MinTreatmentAmount` / `MaxTreatmentAmount`, `TermMonths`, `InterestRate`, `DownPaymentAmount`, `AdvanceRate`, `Name` (e.g. `CUS-LA1ST-PRM-01_A_Grade_18P`), `ProviderFees`.
- An offer is eligible when: `Active = 'true'` AND `ArchivedDateUTC IS NULL` AND its `ProgramCode` matches the app's `ProgramCode` AND the `Condition` credit grade matches the app's `CreditGrade` AND the requested amount is within `[MinFinanceAmount, MaxFinanceAmount]`.
- Extract the grade from `Condition`: it is the text between `CreditGrade = '` and the next quote. Parse with `SUBSTRING(cond, CHARINDEX('CreditGrade = ''', cond)+15, CHARINDEX('''', cond, CHARINDEX('CreditGrade = ''', cond)+15) - (CHARINDEX('CreditGrade = ''', cond)+15))`.
- The LaserAway "waterfall" (provider 16753 example, live offers, grade -> max finance): 1st look `CUS-LA1ST-PRM-01` = A,B up to 15k/12k; 2nd look `CUS-LA2ND-PRM-05`/`4.2` = A,B,C up to 5k; 3rd look `CUS-LA3RD-06` = A,B,C,D,E up to 2,401; `CUS-LA3RD-PRM-07` = C,D up to 2,700; 4th look `CUS-LA4TH-PRM-01` = D,E up to 2,401. A grade-E applicant evaluated under 1st look matches no offer; even in 3rd/4th look the cap is $2,401.

## No-offer reason logic (config-driven decline detection)

For an app with no offer (`OfferHistory.Response = '[]'`), classify against the provider's active offers aggregated per `(ProgramCode, grade)` with min/max amount:

1. No OfferHistory request -> "Declined before an offer was requested".
2. No active offers for the app's `ProgramCode` -> "No active offers configured for program X" (a config gap).
3. App's `CreditGrade` is not among the grades offered in that program -> "Grade {G} not offered in {program} (offers {grades}); grade {G} offered in {other programs} (max ${max})". This is the dominant case (about 88% at provider 16753) and reveals grade/program routing gaps.
4. Requested `ServiceCost` is above the grade max (or below the min) for that program -> "Requested ${X} exceeds grade {G} max ${max}".
5. Otherwise the offer config would allow it, so the decline is a genuine credit decision.

This is the basis for spotting **D02 declines caused by bad configuration**: a thin-file D02 whose grade also has no offer in the program it was routed to (case 3) or whose program has no active offers (case 2) is a config/routing candidate, distinct from a genuine thin-credit decline. The deployed detail report renders this string per no-offer app; the `prog_grade` / `prog_grades` / `grade_progs` CTE pattern (with `STUFF ... FOR XML PATH` for the grade/program lists at compat 130) is the reusable building block.

## Dead-end tables (checked; do NOT use for current V3 amounts)

- `Underwriting.dbo.UnderwritingLog`: defunct, all rows from 2021 (legacy "Enova").
- `HFDprod.dbo.v3application`: defunct 2021-22 pilot, amounts NULL.
- `HFDprod.dbo.ApplicationUnderwriter`: no amount column.
- `HFDprod.dbo.PreApplications`: current and has `FinanceAmount`, but it is the legacy V2 prequal flow and does not overlap V3 EasyAPI applications (no key join, and zero match by SSN+provider+time).
