---
name: hfd-database
description: "Use this skill when working with HFD (Healthcare Finance Direct) SQL Server databases or any DBUp-* migration repository. Trigger when: writing or modifying SQL migration scripts for Analytics/Finance/HFDProd/FinanceOffer databases, creating or altering stored procedures/views/tables/functions, converting Tableau calculated fields to SQL, working with provider data or provider hierarchy, building ETL MERGE procedures, querying Analytics data warehouse or Finance source tables, or preparing PRs for any DBUp-* repo. Also trigger when the user mentions DimProvider, FactApplication, FactContract, HybridApplicationPerformance, HybridHurdlePerformance, MergeProviderData, HFDProd, Netpurchases, or any dw/ro/dbo schema objects. Even if the user just says 'add a column' or 'update the proc' or 'fix this SQL' in the context of any HFD repo, use this skill."
---

# HFD Database Skill

Guide for working with Healthcare Finance Direct's SQL Server databases and the DBUp-* migration repositories.

**Critical:** All database changes must comply with the [HFD Data Standards Rule Book](references/data-standards.md). Read that file before making any new or modified object. The key rules are summarized below but the full reference covers naming, data types, constraints, indexes, programmability, and style.

## Data Standards Quick Reference

See `references/data-standards.md` for the full rule book. Most common rules:

- **PascalCase** object names, `Id` not `ID`
- **Views:** `VW_` prefix
- **Stored procs:** `usp_<Entity><Action>` prefix
- **Indexes:** `IX_<Table>_<Columns>`, `UIX_` for unique
- **Constraints:** explicitly named `PK_`, `FK_`, `UQ_`, `CHK_`, `DF_`
- **`NVARCHAR` only** - `VARCHAR` is banned
- **`DATETIME2(3)` only** - `DATETIME` is banned
- **`DECIMAL(19,4)`** for money, **`DECIMAL(19,8)`** for rates/percentages
- **UDFs (scalar AND table-valued) are discouraged** - use views instead
- **Indexes must use compression** (ROW or PAGE) by default
- **Physical deletes prohibited** without CTO approval - use `ArchivedOnUtc DATETIME2(3) NULL`
- **`ON DELETE CASCADE` not allowed**
- **UPPERCASE SQL keywords, leading commas, schema-qualified names, idempotent scripts**
- **Required in procs:** `SET NOCOUNT ON; SET XACT_ABORT ON;`
- **Audit columns** on all transactional tables: `CreatedOnUtc`, `UpdatedOnUtc`, `CreatedBy`, `UpdatedBy`

## Database Environment

| Database | Server | Purpose |
|----------|--------|---------|
| **Analytics** | hfdsqlfinance.office.local | Data warehouse, reporting views, DimProvider, FactApplication |
| **Finance** | hfdsqlfinance.office.local | Operational finance data, SAO/hybrid/hurdle logic, HybridApplicationPerformance, HybridHurdlePerformance |
| **Finance_Archive** | hfdsqlfinance.office.local | Archived historical data (e.g., SAOHybridHistory20240318) |
| **HFDProd_Finance** | hfdsqlfinance.office.local | Production source tables (Providers, Applications, Netpurchases) |
| **FinanceOffer** | hfdsqlfinance.office.local | Provider offer configurations with JSON |
| **ReportServer** | hfdsqlreport.office.local | SSRS catalog (use the `ssrs` skill) |

- **Engine:** SQL Server 2022, Analytics at compatibility level 130 (SQL Server 2016 mode)
- **Disallowed on compat 130:** `STRING_AGG` (use `STUFF...FOR XML PATH`), `TRIM` (use `LTRIM(RTRIM(...))`), `TRANSLATE`, graph tables
- **Always use `WITH (NOLOCK)`** on every table/view reference in read queries

### MCP Connector Notes

The project has two MCP connections to `hfdsqlfinance`:

- **`mssql`** - First connection. Returns "-1" for empty result sets AND for timed-out queries (a `-1` on a `COUNT(*)`, which always returns a row, means the query timed out -- not zero rows; bound or split it). Suppresses error details. **In practice this is the reliable connector for `hfdsqlfinance` -- prefer it.** `ProductionCopy` also works.
- **`mssql2`** - Second connection. Historically preferred (column headers, "(N rows affected)", better error surfacing), but it can fail outright with `[28000] Login failed. The login is from an untrusted domain and cannot be used with Integrated authentication`. No MSSQLSvc SPN is registered for the service account on `hfdsqlfinance`/`hfdsqlreport`, so its integrated-auth path breaks. When `mssql2` throws that, switch to `mssql` or `ProductionCopy`. (See memory `reference_ssrs_sql_connectors`.)

**Gotchas:**
- Both connections default to the Analytics database context. Cross-database metadata queries are unreliable: `Finance.sys.objects` scans and even `OBJECT_DEFINITION(OBJECT_ID('Finance.dbo.X'))` can return 0 rows / NULL for objects that exist (verified 2026-06: OBJECT_DEFINITION returned NULL for a view that does exist). `OBJECT_ID()` itself DOES resolve cross-database reliably, so the dependable column-metadata pattern is a single statement: `SELECT c.name, TYPE_NAME(c.user_type_id) AS Typ, c.max_length, c.is_nullable FROM Finance.sys.columns c WITH (NOLOCK) WHERE c.object_id = OBJECT_ID('Finance.dbo.SAODisputeList')`. For a view or proc body, read `<Db>.sys.sql_modules` the same way (filter by `OBJECT_ID(...)`) or query from inside the target database.
- Complex queries against large views (`HybridApplicationPerformance`, `fSAOHybridAccounts()`) often time out silently. Filter to a single provider for testing.
- Temp tables do NOT persist between MCP tool calls. Use variable tables (`DECLARE @t TABLE`) or single-batch queries instead.
- Prefer ONE statement per call. A multi-statement batch returns only the FIRST statement's result and silently drops a later SELECT: `SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED; SELECT ...`, `USE Db; ...; SELECT ...`, and a SELECT after an INSERT/UPDATE all come back as `Rows affected: -1` with no rows. (Parse and column-name errors still surface because the whole batch is parsed, which can make it look like the SELECT ran.) So satisfy the NOLOCK rule with inline `WITH (NOLOCK)` on every table and view (including `sys.columns`, `sys.partitions`) rather than a leading `SET` statement. For exact row counts on big tables use `SELECT SUM(rows) FROM <Db>.sys.partitions WITH (NOLOCK) WHERE object_id = OBJECT_ID('<Db>.dbo.<Table>') AND index_id IN (0,1)` instead of `COUNT(*)`.

## Schema Layout (Analytics)

| Schema | Purpose | Examples |
|--------|---------|---------|
| `dw` | Data warehouse dimensions, facts, ETL procs | DimProvider, DimPerson, DimAddress, FactApplication, FactContract |
| `ro` | Read-only reporting views (Align, Tableau) | vAlignProviders, vAlignTableauContracts |
| `dbo` | General reporting views (Hatch Bank, funds) | VW_Hatch_Application_File, VW_SubmittedFunds |

## Star Schema Design

**Dimension tables:** DimProvider, DimPerson, DimAddress, DimOffer, DimFactorCodes, DimSectionFast
**Fact tables:** FactApplication, FactContract, FactOffer

### Person-Level (Consumer) Analytics: dw.DimPerson and repeat-loan queries

Learned 2026-06-10 building the Repeat and Subsequent Loans workbook; every rule below was verified against production counts.

- **Join keys:** `FactContract.ContractApplicantKey = DimPerson.PersonUniqueKey` and `FactApplication.ApplicationApplicantKey = DimPerson.PersonUniqueKey`. Contracts join applications via `ContractApplicationKey = ApplicationUniqueKey`.
- **Consumer dedupe key is `DimPerson.PersonHashedNationalId`** (uppercase MD5, `varchar(32)`). Never select raw person PII (DimPerson also carries name/DOB/mobile/email); the hash is the analytic identity.
- **MANDATORY exclusions for any person-level metric** (else one fake "person" absorbs hundreds of thousands of loans):
  - `PersonHashedNationalId IS NULL`
  - `'D41D8CD98F00B204E9800998ECF8427E'` = MD5 of the EMPTY STRING, **253,945 contracts** (2026-06)
  - `'002B4F0279296AA9DFF6DC4FC493E638'` (2,353), `'4C93008615C2D041E33EBAC605D14B5B'` (1,211), `'6C3E226B4D4795D518AB341B0824EC29'` (280)
  - rule form: also drop any hash with `> 50` contracts (next legitimate max is ~38; auto-catches future dummies). Impact example: all-HFD "subsequent loans" = 306,122 / $565M raw but 49,212 / $101.8M after exclusion.
- **Applicants vs borrowers:** ~2.33M distinct hashed ids exist via FactApplication but only ~696K have any FactContract (70% applied, never signed). A consumer metric must state which population it uses; joining FROM FactContract scopes to borrowers naturally.
- **Repeat/subsequent-loan SQL pattern:** sequence per person with `MIN(ContractCreated) OVER (PARTITION BY PersonHashedNationalId)`; subsequent = `ContractCreated > first`; second-loan date = `MIN(CASE WHEN ContractCreated > first THEN ContractCreated END)` so identical-timestamp ties yield NULL (matches the Tableau LOD semantics). Reference numbers (all statuses, dummy-excluded, full history 2026-06): all HFD 695,875 consumers / 5.59% repeat / $2,068 avg subsequent / 7.11 months to 2nd; Aspen parents (15559+14286) 112,919 / 2.30% / $1,859 / 9.05 months.
- **The published Tableau dataset `v.HfdV3` is NOT the warehouse:** rolling 3-year contract window (~725K contracts vs 1.76M all-time) at FactApplication grain. Verification SQL for anything built on it needs `ContractCreated >= DATEADD(YEAR, -3, GETDATE())`, and duration metrics are right-censored by the window (Aspen months-to-2nd: 8.2 in-window vs 9.05 lifetime). See the `tableau-twb` skill lessons 70-74 and memory `reference_vhfdv3_extract_window`.

### Provider-Level (Sales/AM) Analytics: V3 ro views, territory fields, loyalty tier

Learned 2026-06-10 building the AM Business Review workbook on the V3 layer; counts verified against production.

- **The `ro.VW_HfdV3*` view family has exactly 5 members** (the SQL feed behind the published v.HfdV3 source): `VW_HfdV3DimAddress`, `VW_HfdV3DimPerson`, `VW_HfdV3FactApplication`, `VW_HfdV3FactContract`, `VW_HfdV3FactSAOPurchase`. There is NO V3 provider or partner dim view; provider attributes come straight from `dw.DimProvider` (self-join `ProviderParentKey = ProviderUniqueKey` for the parent row). Fact-to-provider keys: `ContractProviderKey` / `ApplicationProviderKey` = `DimProvider.ProviderUniqueKey` (varchar both sides).
- **Loyalty tier lives in `dbo.vw_ProviderHealthScorecard.ProgramTier`** (Foundation 11,547 / Preferred 274 / Elite 201 as of 2026-06), join on `ProviderId = DimProvider.ProviderUniqueKey`, verified exactly 1 row per provider (12,022 = distinct). DimProvider has no tier column. Do not confuse with the Sales Territory Performance workbook's "Service Tier" calc, which is a volume banding on prior-month contract value (Elite >= 60K, Premier >= 23K, Preferred >= 12K, Core >= 4.5K, else Basic) and not the loyalty program. `ro.vProviderUtilizationTrend` (provider x MonthStart grain) also carries a historical `LoyaltyTier` plus `UtilizationStatus`/`PrevMonthTreatment` if a premade monthly trend is enough.
- **AM territory fields:** `DimProvider.ProviderParentAccountGroup` segments the book (Area Managers, Enterprise Management, Special Markets, Excluded Accounts, Area Managers Invalid Address Information, NULL). `ProviderParentAccountGroupDetail` is the per-AM territory in the form `Area Managers - <Territory>` (Desert Frontier, Great Lakes, West, ...); strip the prefix for display, map NULL to Unassigned. Aspen Dental sits under Excluded Accounts, so rollups defaulted to the Area Managers group exclude it by design.
- **Parent rows transact:** ~40 contracts / ~$133K per month (0.06% of volume) land on `ProviderIsParent = 1` rows. A location-only roster (`ProviderIsParent = 0`) drops that volume; state the exclusion when totals must reconcile.
- **Sales-reporting conventions** (copied from the Sales Territory Performance workbook; flag them as conventions when reusing): exclude `ProviderStatus IN ('CAN','PDACT','TST')`; decode `ProviderFundingType` 10000 = Cash Over Time, 10001 = Cash Up Front, 10002 = Hybrid Financing; leadership YTD views filter to Cash Up Front + Hybrid Financing; parent 'Dolce Medical Spa Parent' is hard-excluded; Utilization % = COUNTD(providers with an application) / COUNTD(providers in scope).
- **Provider-month grid pattern** for utilization and active-account metrics in one Custom SQL: cross join a month spine (distinct `DATEFROMPARTS(YEAR(ContractCreated), MONTH(ContractCreated), 1)` from FactContract) with the DimProvider roster, left join per-month contract and application aggregates, keep `MonthStart >=` the provider's activation month. Zero-activity provider-months stay as rows, which is what makes COUNTD-based utilization and active-account denominators computable in Tableau. Wrap-tested shape at `C:\Users\esmith\temp\am_review_custom_sql.sql` (270,646 rows / 18,228 providers for Jan 2025 - Jun 2026).

## Key Source Tables (HFDProd_Finance)

Read `references/provider-hierarchy.md` for detailed column lists and ID mappings when working with provider classification logic.

### dbo.Providers

Core provider table. Key columns:

- `ProviderId` (PK), `ProviderName`, `PracticeName`
- `ParentProvider` (FK to parent's ProviderId), `IsParentProvider` (bit)
- `FundingType`: 10000 = Cash Over Time, 10001 = Cash Up Front, 10002 = Hybrid Financing, NULL = treat as Area Managers
- `State`, `Zip` (used for territory assignment)
- `IsTest` (bit), `ProviderStatus` ('TST' = test)

### dbo.ProviderRelationsReps

Rep assignments. Key columns:

- `ProviderId` (FK), `FirstName`, `LastName`
- Used for rep-based territory/dynamic filter logic

### FinanceOffer.dbo.ProviderConfigs

Provider offer configurations with JSON documents. Key columns:

- `ProviderId` (FK), `Document` (nvarchar(max) JSON)
- Document contains `$.Offers` array, each offer may have `$.ProviderFees` nested JSON array
- Avg document size ~160KB, ~19K rows. Known fee types: originationFee, servicingFee
- Use `CROSS APPLY OPENJSON(c.Document, '$.Offers') WITH (...)` for typed extraction
- For small nested arrays like ProviderFees (max 2 items), `JSON_VALUE` with hardcoded indices (`$[0]`, `$[1]`) outperforms a second `CROSS APPLY OPENJSON`

### Filtering Test Providers

Always exclude test providers in reporting views: `WHERE IsTest != 1 AND ProviderStatus != 'TST'`

### Finance.dbo Funding Sources (SAO purchase + hybrid)

Provider funding (money actually sent to the provider) lives in two `Finance.dbo` tables, both keyed by `HFDID` (= `HFDProd_Finance.dbo.Applications.autoid`):

- **`SAOPurchaseHistory`** - funded loan transactions. Key cols: `OfficeID` (provider), `ParentOfficeID`, `HFDID`, `type` (`Origination` = new funded loan; `Sale`/`Adjustment`/`Cancellation` = later ledger activity), `p_saoprice` (amount funded to provider), `p_MDRAmount`/`P_MDRRate` (merchant discount amount/rate), `Downpayment` (due) and `DownPmtPaid` (collected), `MatrixGrade` (credit grade), `FinancialInstrument` (`RIC` or `BankLoan`), `FundDate`, `RoutingLast4`/`BankLast4` (the provider's own deposit account, constant-ish per provider). Funding-sent / deposit-date logic: RIC -> `DATEADD(DAY,1,FundDate)`, BankLoan -> `FundDate`, Hybrid -> `PaidtoProvDate`. **Deposits are split by financial instrument**, so a deposit/batch is uniquely (provider, settlement date, instrument) -- the batch id must encode date AND instrument, e.g. `CONVERT(char(8), <settlement date>, 112) + '-RIC'` (or `-BankLoan` / `-Hybrid`). Put the date first so the id sorts chronologically. A per-deposit total is therefore `{ FIXED [ProviderId], [BatchId] : SUM([FundedAmount]) }`, not keyed on date alone.
- **`SAOHybridHistory`** - hybrid-financing payouts. Key cols: `ProviderID`, `HFDID`, `amttoprov` (amount funded; filter `amttoprov > 0`), `PaidtoProvDate`, `RoutingLast4`/`BankLast4`. Join `Providers` on `ProviderID` and `Applications` on `autoid = HFDID` for names/grades.
- **`HFDProd_Finance.dbo.Applications`** - `autoid` = HFDID. `status`: `EXP` expired, `APR` approved, `DCN` declined, `CONF` confirmed/signed. `DownPayment` (due) vs `AmountCollected` (collected; `0` on unfunded CONF apps, since collection happens at/after funding). "Funded" = `autoid IN (SELECT hfdid FROM SAOPurchaseHistory WHERE type='Origination')`.

Volumes (all providers, 2026-05): SAOPurchaseHistory ~756K, SAOHybridHistory (amttoprov>0) ~381K, Applications ~3.5M, Originations ~592K. Size Tableau extracts and scope filters accordingly; unfiltered joins across these time out on the MCP connectors.

### Disputes and Chargebacks (consumer-side)

Three sources, reconciled on one key: **`HFDID` = `LedgerDetail.ProcedureID` = the HubSpot dispute ticket "Account #"** (the loan / account id). Verified 2026-06-16 building the ACI (Affordable Care, parent provider 15742) disputes-and-chargebacks report.

- **`Finance.dbo.SAODisputeList`** - account-level dispute and chargeback rollup (history back to 2022, ~10.8K rows), one row per `HFDID`. Every row is a dispute (`IsDispute = 'Yes'`); the chargeback subset has `IsChargeBack = 'Yes'`. Flag values are `'Yes'` or empty string, NOT `Y`/`N`. Useful cols: `CountChargeBacks`, `ChargeBackTotal`, `ChargeBackDown`, `IsDownChargeBack`, `First/LastChargeBackDate`, `PaymentStatus`, `DetailStatus`/`DetailStatusDate`. Provider keys: `OfficeID` (location), `ParentOfficeID` (parent, can be stale, see `reference_netpurchases_parent_stale`), `ProviderID`. Never SELECT the PII columns: `FirstName`, `LastName`, `PatientID`, `Email1`, `DecisionMaker`, `DecisionmakerEmail`. Scope a parent via `ParentOfficeID = <parent>`, but for accuracy prefer `OfficeID IN (<current child set from dw.DimProvider>)`; for ACI the ParentOfficeID gap was only 3 of 1,218 accounts, but it is real.
- **`HFDProd_Finance.dbo.vS3_Disputes`** - lean view giving a clean **`DisputeDate`** per `HFDID` (plus `ProviderID`, `PaymentStatus`, `ActivatedOn`, and PII `Email`/`PrimaryPhone`). Use it for the dispute date; use `SAODisputeList.FirstChargeBackDate` for the chargeback date. `HFDProd_Finance.dbo.vReporting_BNKDisputeFollowUp` is the bank-dispute follow-up worklist.
- **`HFDProd_Finance.dbo.LedgerDetail`** (~50.7M rows) - transaction-level consumer ledger. **Join on `ProcedureID` (the loan), NOT `autoid` (the ledger-row PK).** Joining on `autoid` returns coincidental one-row collisions that look like real matches. Chargebacks are rows where **`AccountingCode = 'STOP'`**. Fee codes seen: **7300** = recurring card payment (the payment that gets stopped), **7107** = card-payment chargeback reversal and repost, **103 / 7103** = NSF fee assess / reverse; `AccountingCode = 'HOLD'` is applied to reposted late/NSF fees. STOP posts in reversing +/- pairs, so **net the dollars (especially `PrincipalAmount`); do not count rows**. Principal added back = chargeback lost (HFD eats the payment, consumer still owes); credit added back = chargeback won. `Voided` and `Comment` help interpret rows. The `IX_ProcedureID_FeeCode` index makes ProcedureID-scoped scans fast.
- **Chargeback resolution (won / lost / pending):** STOP `Amount` always nets to ~0 (re-presentment +/- pairs), so it cannot classify the outcome. Use `SAODisputeList.PaymentStatus` as the resolution driver (validated against the ledger 2026-06): `TCOL` = lost / charged off (PrincipalBalance 0, a `FeeCode 501` `HOLD` principal write-off); `ACT` / `PIF` = won / recovered (still on the books and paying); `PCOL` / `LATE` / `DEL` = pending (in collections / delinquent). Chargebacks post as STOP on both `FeeCode 7107` (down payment) and `7300` (recurring); `FeeCode 300` is the principal add-back.
- **Provider financial impact:** most providers are **non-recourse**, so a consumer chargeback is HFD's loss, not a debit to the practice. `Finance.dbo.ProviderRecourse` has one row per provider (`ProviderID`, `RecourseDate`, `Recourse` where `'1'` = on recourse; only ~19 providers are). Actual provider clawbacks post to `Finance.dbo.SAOPurchaseHistory` as `type IN ('Adjustment','Cancellation')` with negative `p_saoprice`; attribute dispute-driven ones by `HFDID` and timing. Confirm the "provider impact" definition with the requester before reporting.
- **HubSpot:** consumer disputes arrive by form into the **Disputes pipeline `26466881`** (~32.8K tickets, ~24K since 2025; the pipeline also holds general billing inquiries, ~71% are `BILLING_ISSUE`, ~98% Closed). Ticket-level id properties are essentially empty (`hfdid` 0 filled, `provider_id` 4, `application_id` 2) and the account number is only in the free-text subject. The reliable join is on the associated CONSUMER contact: **`contact.application_id` = `HFDID` = `Applications.autoid`** (filled on ~33K contacts; ~24.6K dispute tickets, about 75%, link to such a contact). Reconcile ticket -> `contact.application_id` -> `HFDID` -> provider via a cross-object query (`SELECT ... FROM TICKET WHERE hs_pipeline='26466881' AND CONTACT.application_id ...`). Provider/practice STAFF contacts instead carry `contact.provider_id` / `parent_provider_id` (these are NOT the consumer keys). Chargebacks are bank-initiated and do NOT create a HubSpot ticket (sampled 0 of 5), so HubSpot disputes and ledger STOP chargebacks are largely disjoint populations: UNION them, do not join. See the `hubspot-tickets` skill.
- **Confluence:** "Chargeback Automation Phase I" (page 3928981506) lists the chargeback event/reason codes (C783-C875, the C884 letter, the `CHBK` account status) and the STOP-on-payment trigger; "Refunds and Chargebacks" (page 3228106778) explains the principal/interest ledger mechanics.

### Finance.dbo Hybrid Objects (PBI 22266)

- **`HybridApplicationPerformance`** (view) - Application-level hybrid data with hurdle calculations. Replaced `SAOHybridBaseData()` TVF. Uses `ProviderID` (renamed from `OfficeID`).
- **`HybridHurdlePerformance`** (view) - Cohort-level hurdle metrics. Replaced `fSAOHybridHurdleSSRS()` and `fSAOHybridHurdleSSRS_HurdleDate()` TVFs. Grain is `HurdleGroup + HybridGroup` where `HurdleGroup = monthly vintage + parent provider`.
- **`fSAOHybridTransactionsSSRS()`** (TVF, banned per standards but still used) - Historical transactions for SSRS reports. Has a window function with `HurdleGroup` in ORDER BY that causes the 8007-byte RANGE frame error for long HurdleGroup values.

### Optimizing reports that read the v2 hybrid views

`fSAOHybridDataTape()`, `HybridApplicationPerformance` (HAP), and `HybridHurdlePerformance` (HHP) all look fast in isolation but are crippling when joined to other large tables in a single statement. Predicates on `ProviderID` / `ParentProviderID` from the outer query cannot push through the views' internal CTEs and window functions, so the planner materializes the entire upstream graph before filtering.

Pattern that recovered a never-returning report (974s -> 3.7s for a 658-row scope):

1. **Pre-filter HFDIDs to a small temp table FIRST** using `Finance.dbo.SAODailyDataTape` (carries `parentprovider`, `ProviderID`, indexed on `ReportEnd`) inner-joined to `fSAOHybridAccounts()`. This is the only place where the provider filter can use indexes.
2. **Materialize HAP scoped to those HFDIDs** before joining to anything else. Even a `WHERE hap.ParentProviderID = X` direct on HAP returns in ms, but hash-joining unmaterialized HAP to other large tables blows up.
3. **Bypass HHP entirely** when querying for a specific scope. Rebuild it locally from `#HAP` plus a tightly scoped scan of `SAOHybridHistory`. The HHP view's `RunningTotals` CTE runs `SUM() OVER (PARTITION BY HurdleGroup ORDER BY ...)` over the entire 600k+ row history; nothing pushes the filter through.
4. **Bypass `fSAOHybridDataTape()` and `fSAOHybridTransactionsSSRS()`** for the same reason. Rebuild the pmt aggregation directly. The original UNION ALL has three branches: `Finance_Archive.dbo.SAOHybridHistory20240318` (PaidtoProvDate <= '20240317'), `Finance.dbo.SAOHybridHistory` (PaidtoProvDate > '20240317'), and `fSAOOriginationData` (Adjustment / Origination / Cancellation rows where SAOAdvRate = 0.30 — only `Adjustment` survives the pmt filter and contributes only to TotalPaidToProv via SAOPrice).
5. **Pre-aggregate `LedgerDetail` fees** scoped to the HFDIDs (uses `IX_ProcedureID_FeeCode`).

A worked example lives at `C:\Users\esmith\temp\hybrid_query_optimized.sql` (parent provider 20348 went from never-returning to 3.7s for 658 rows).

### SSRS string parameters and `NOT IN (NULL)`

SSRS report parameters with `DataType = String` arrive as `NULL` when the user leaves the prompt blank. The expression `dt.providerid NOT IN (@StringParam)` evaluates to UNKNOWN for every row when `@StringParam` is NULL and silently filters out the entire result set. The catalog query for `Hybrid Funding Datatape - Monthly - Beta` had this trap on `@ProviderExclusions` -- after running the upstream graph for 10+ minutes, it returned 0 rows.

Fix pattern:

```sql
DECLARE @ProvExcl INT = TRY_CAST(NULLIF(@ProviderExclusions, '') AS INT);
...
WHERE ( @ProvExcl IS NULL OR dt.ProviderID <> @ProvExcl )
```

Use the same NULLIF + TRY_CAST shim for any optional `@ProviderID` / `@ParentProviderID` parameter the report passes as a string.

### Precision: don't cast FLOAT to DECIMAL when matching report output

`HFDProd_Finance.dbo.Providers.CostCC` is `FLOAT(53)`; the retention fee columns are `DECIMAL(12,4)`. The pre-existing reporting math (`a.MonthlyPmt * (p.CostCC / 100)`) flows through SQL Server's FLOAT promotion rules and keeps full FLOAT precision. Casting the percentages to `DECIMAL(19,8)` to "tidy them up" loses sub-cent precision and produces row-level mismatches against the original report. Either keep the raw expression (no cast) or use `FLOAT` explicitly.

## V3 Origination, EasyAPISummary & the Offer Engine

Enterprise EasyAPI providers (LaserAway parent 16681, Milan parent 28551, and similar) run on Origination V3. Full detail in `references/v3-origination-offers.md`. Key facts:

- `ProductionCopy` MCP = server **AG2-Prod-SQL-Az**, database **HFDprod** (production OLTP). SSRS reaches it via shared data source `/Data Sources/ProdAG2ProductionRealTimeReadOnly`. **HFDprod is compatibility level 130** (no `STRING_AGG`; use `STUFF(... FOR XML PATH(''))`).
- In V3 an application does not reach `dbo.Applications` until it is **signed** (`CONF`). All approve/decline/pending decisions live in **`HFDprod.dbo.EasyAPISummary`** (EAS), keyed by `AccountId` (the Application Unique Key); dedupe by `AccountId` taking the latest row (`MAX(Id)`). Approval rate, decline/ineligible reasons (`CriticalMessage` JSON: D02 thin file, D08 identity, **D09 loan stacking** (not credit limit), **E36 Credit Limit Enforcement** "Maximum credit limit has been reached" - Ineligible disposition, V3-pending so 0 for LaserAway/Milan), `CreditGrade`, and the risk pipeline (`ScorebreakModel`) all come from EAS. `Applications` holds only signed deals for these providers.
- Requested and offered dollar amounts, including for **unsigned** apps, come from **`FinanceOffer.dbo.OfferHistory`** (`ApplicationId = EAS.AccountId`, latest by `CreateDateUTC`; indexed, so use a `TOP 1` `OUTER APPLY`): `Request` JSON `$.ServiceCost` = requested amount, `Response[0].MaxFinanceAmount` = assigned limit. `Response = '[]'` means no offers were generated.
- Whether an app could get an offer is governed by **`FinanceOffer.dbo.ProviderConfigs`** (`Document.$.Offers` array; each offer has `Active`, `ArchivedDateUTC`, `ProgramCode`, a `Condition` grade expression, and `MinFinanceAmount`/`MaxFinanceAmount`). Reconstructing offer eligibility explains no-offer declines (grade not offered in the evaluated program, requested amount out of range, or no active offers) and is the path to flag D02 declines caused by bad configuration.
- **Timezones, PII, and program-code funnels (raw decision detail):** EAS datetime columns (`SubmittedOn`, `SessionStartedOn`, `ApplicationSubmittedOn`) are **UTC**, but `HFDprod.dbo.Applications.CreatedOn`/`ActivatedOn` are **Pacific** (the AG2 server runs Pacific) - a report over both mixes timezones and must convert one side (`... AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific Standard Time'`; convert the date-param boundary, not the column, to stay SARGable). `EAS.NationalId` is **raw SSN** (hash it, never display raw); `FirstName`/`LastName` are raw PII (mask to initial + last per the existing approval-detail report). For a program-code funnel/summary, source program code from **`Applications.ProgramCode`**, never the post-funding `SAOPurchaseHistory` origination `ProgCode` (which silently drops approved-but-unfunded apps and caps the report at the last funded date). Full patterns in `references/v3-origination-offers.md`.

## JSON Query Performance

- `OPENJSON WITH` (typed columns) is faster than multiple `JSON_VALUE` calls on the same large document
- For small nested arrays with known max size, `JSON_VALUE` with hardcoded indices avoids a second `CROSS APPLY OPENJSON`. Use `OUTER APPLY` with `MAX(CASE WHEN...)` as an alternative pivot approach
- `LIKE`/`CHARINDEX` pre-filters on large nvarchar(max) JSON columns are slower than just parsing the JSON directly
- Compatibility level 130 lacks native JSON optimization. Level 150+ enables it. Compat level is set per-database: `ALTER DATABASE [DbName] SET COMPATIBILITY_LEVEL = 160;` (no restart needed)
- For recurring queries against large JSON columns, consider materializing the data into relational tables via ETL rather than parsing at query time

## ETL MERGE Pattern

All ETL stored procedures follow this pattern. Read `references/etl-patterns.md` for templates.

1. **Source query** builds the incoming dataset with all computed columns
2. **BINARY_CHECKSUM** generates a row hash for change detection
3. **MERGE** matches on business key (e.g., `ProviderUniqueKey`)
4. **WHEN MATCHED** only updates if row hash differs: `isnull(tgt.RowHash, '') <> isnull(src.RowHash, -1)`
5. **WHEN NOT MATCHED** inserts new rows

### CROSS APPLY (VALUES (...)) Pattern

When a MERGE source query needs multiple intermediate classification values that feed into several output columns, use `CROSS APPLY (VALUES (...)) alias(col1, col2, ...)` to compute them once and reference by alias. This avoids duplicating complex CASE expressions.

## DBUp Migration Framework

HFD has separate DBUp repos per database. Pick the right one for the target:

| Repo | Database | GUID |
|------|----------|------|
| **DBUp-Analytics** | Analytics | `466c6e10-44c8-4767-a538-c0264d9a85f0` |
| **DBUp-Finance** | Finance | `79793e55-f391-4409-a246-55c2a405511b` |
| **DBUp-FinanceOffer** | FinanceOffer | `531a679e-e477-41b8-b829-df0783b8c558` |
| **DBUp-HFDProd** | HFDProd_Finance | `7aa20993-266a-466b-94a8-60b6c826b2f9` |
| **DBUp-BaseRepo** | (shared infrastructure) | `62147c3d-1d6d-41d7-ae3b-2feb7327932a` |
| **DBUp-FeatureFlag** | FeatureFlag | `7a8cc2dc-b594-498f-b3b5-aa546233ada6` |
| **DBUp-Payment** | Payment | `5280bcdd-3f04-48af-83c8-d1fceba0c6c5` |
| **DBUp-Underwriting** | Underwriting | `27ddbdbc-c24e-4d99-a856-30274993c6a6` |
| **DBUp-Wallet** | Wallet | `c853f0c4-a30c-430e-aeb9-18e6b8c40a16` |
| **DBUp-Workflow** | Workflow | `e0c2c020-33d0-43ab-bcda-85345cdbbf6f` |
| **DBUp-OriginationV3** | OriginationV3 | `f9241138-5863-4562-930b-36c357eea747` |
| **DBUp-V3Postgres** | V3 Postgres | `6111ebfe-7053-47d8-9e55-20d261d65d6f` |

Local clones live at `C:\Users\esmith\PycharmProjects\DBUp-<Name>`. The hybrid/hurdle/SAO finance objects live in **DBUp-Finance**, not DBUp-Analytics. Always verify the target database before creating a PR.

### File Naming Convention & Execution Order

```
YYYYMMDD-N-DescriptiveName-TicketNumber.sql
```

- `YYYYMMDD`: date of creation
- `N`: sequence number **within that date** (see the ordering rule below)
- `DescriptiveName`: matches the database object name when possible
- `TicketNumber`: Azure DevOps work item ID

**Execution order — read this BEFORE numbering a multi-object PR.** DBUp itself does not sort or discover these scripts. The pipeline template `HFD/PipelineTemplates` → `Deploy/dbup-deploy.yml` does: it globs every `*.sql` **recursively across all folders**, sorts by a **numeric, folder-agnostic** key, and runs `dbuputility.dll` **once per file**:

```powershell
$orderedFiles = $matchingSqlFiles | Sort-Object {
    $parts = $_.BaseName.Split('-'); ([int]$parts[0] * 10000 + [int]$parts[1]) }   # date*10000 + N
foreach ($file in $orderedFiles) { <copy 1 file to temp folder>; dotnet $dll dbuputil --folder $temp }
```

So the only thing controlling order is `N` (the 2nd hyphen token). **THE RULE:**

> Within a given date, `N` must be a **globally UNIQUE integer, ascending in dependency order, ACROSS ALL FOLDERS** — tables / stg / indexes / dims first, then procs, then views.

- **Number across folders, NEVER per-folder.** `Table/…-1-…`, `Stored Procedures/…-1-…`, and `Views/…-1-…` all produce the *same* key; `Sort-Object` is not stable and the key ignores the folder, so the tie breaks arbitrarily and a view can run before its table. This broke DBUp-Analytics build 66884 on 2026-07-09 (`Invalid object name 'dw.FactSeoGscDaily'` — a `-1-` view ran before its `-4-` fact). A multi-object PR must therefore renumber into one global sequence (e.g. tables `01-10`, procs `11-13`, views `14-18`).
- **Views hard-fail out of order; procs don't.** `CREATE VIEW` validates referenced objects at create time; `CREATE OR ALTER PROCEDURE` has **deferred name resolution**, so an out-of-order proc silently survives while an out-of-order view fails the deploy.
- **Zero-padding is cosmetic** (`[int]'01' == [int]'1'`); uniqueness + ascending dependency order of `N` is what matters. A single-object-per-date PR satisfies this trivially. A same-date follow-up/hotfix must use `N` values ABOVE any already used for that date, or it ties.
- **Deploys are NOT atomic.** Each script is its own `dbuputility` process/transaction; the loop `exit 1`s on the first failure, so scripts before it stay committed and journaled in `dbo.SchemaVersions` (keyed on the bare filename). Recover by fixing + re-running — idempotency guards + the journal skip already-applied scripts. Renaming an already-applied script makes DBUp re-run it, so check `SELECT ScriptName FROM dbo.SchemaVersions WITH (NOLOCK) WHERE ScriptName LIKE '%<ticket>%'` before renumbering.

### Directory Structure

| Folder | Contents |
|--------|----------|
| `Table/` | ALTER TABLE with idempotency guards |
| `Stored Procedures/` | CREATE OR ALTER PROCEDURE |
| `Views/` | ALTER VIEW or DROP/CREATE |
| `Functions/` | User-defined functions (new UDFs discouraged by standards, but existing ones are modified here) |

Folders are **organizational only** — they do NOT affect execution order (the pipeline flattens all folders and orders by the `N` in the filename). A view in `Views/` will run before a table in `Table/` if its `N` is lower.

### Idempotency Guards

Scripts run once, but always guard DDL for safety:

```sql
-- Adding a column
IF COL_LENGTH('dw.DimProvider', 'NewColumn') IS NULL
    ALTER TABLE dw.DimProvider ADD NewColumn NVARCHAR(64) NULL;

-- Adding a table
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'NewTable' AND schema_id = SCHEMA_ID('dw'))
    CREATE TABLE dw.NewTable (...);

-- Dropping an object
IF OBJECT_ID('dbo.OldFunction', 'IF') IS NOT NULL
    DROP FUNCTION dbo.OldFunction;
```

## Tableau-to-SQL Conversion

Tableau workbook-level calculated fields cannot be extracted via REST API. They must be read from the Tableau UI or workbook XML.

When converting:

- Preserve **first-match-wins priority** order from Tableau CASE/IF logic
- Use **provider IDs** (not names) in SQL CASE WHEN clauses
- Add **inline comments** with the provider/practice name for readability
- The `CROSS APPLY (VALUES (...))` pattern works well for computing intermediate classification groups
- **Custom SQL in a Tableau data source cannot start with a `WITH`/CTE.** Tableau wraps Custom SQL as a derived table (`SELECT ... FROM (<your sql>) Custom_SQL_Query`), and SQL Server rejects a CTE at the start of a parenthesized subquery (`Incorrect syntax near the keyword 'WITH'`). Rewrite CTEs as derived tables or inline subqueries, or move the logic to the connection's Initial SQL building a `#temp` table. Test it the way Tableau runs it: `SELECT TOP 10 * FROM (<custom sql>) q` -- a clean run as a top-level statement in SSMS/MCP does NOT prove it works in Tableau. (See the `tableau-twb` skill.)

Example:

```sql
CROSS APPLY (
    VALUES (
        /* BaseGroup */
        CASE
            WHEN P.ParentProvider IN (15559 /* ABC Corp */, 14286 /* XYZ Inc */) THEN 'Category A'
            WHEN P.FundingType = 10000 THEN 'Category B'
            ELSE 'Category C'
        END,
        /* DetailGroup */
        CASE
            WHEN P.State IN ('NY','NJ','CT') THEN 'Northeast'
            WHEN P.State IN ('CA','OR','WA') THEN 'West'
            ELSE 'Unknown Region'
        END
    )
) AG(BaseGroup, DetailGroup)
```

## Requesting a production update from Data Engineering

For one-off production data changes that are NOT DBUp migrations (for example a provider reassignment, or a single-row data correction), hand Data Engineering a self-contained, validated script rather than running it yourself. Canonical example of how to phrase the request in Teams: https://teams.microsoft.com/l/message/19:aab0cb996d54427cb517c6473607fd73@thread.v2/1780370618865?context=%7B%22contextType%22%3A%22chat%22%7D

Include in the request:

- The SQL itself: a single guarded `UPDATE` (a `WHERE` that re-confirms the source state, e.g. `AND RelationsRep = <oldrep>`) or a transaction-wrapped block with BEFORE/AFTER snapshots. Hard-code the affected IDs. Do not leave a runtime join the app server cannot resolve (e.g. a cross-database join to `Analytics.dw.*`, which does not exist on the HFDProd app server).
- What it changes and why, the expected row count, and the linked ticket.
- Confirmation it was validated read-only against the production mirror (the `ProductionCopy` MCP connection / HFDprod).

See the `hfd-account-reassignment` skill for the reassignment-specific script template.

## PR Workflow

### Work item type

When creating a new Azure DevOps work item for a DB change, **always create a Product Backlog Item (PBI), not a Task**. PBIs are the unit the team plans against and the PR title convention (`PBI-[id]-...`) assumes a PBI. Child tasks under a PBI are fine for sub-work, but the top-level work item that the PR ties to should be a PBI.

### Branch naming

```
PBI-[ticket number]-[short-description]
```

### Two-commit strategy (mandatory)

1. **First commit:** Create the new migration file with the **current production code** (`SELECT OBJECT_DEFINITION(OBJECT_ID('schema.ObjectName'))`) and commit. This applies to every proc/view/function change, even if an older version exists in the repo. The commit message should say "Baseline commit before refactoring" or similar.
2. **Second commit:** Apply changes to that same file and commit. Reviewers see the exact diff, and rollback is straightforward.

This is non-negotiable. Without the baseline commit, the diff in the PR is just "new file" and reviewers can't see what actually changed.

### PR requirements

- Link to Azure DevOps work item
- Title: `PBI-[ticket number] - [Brief description]`
- Description sections: Summary, Problem, Solution, Testing Performed, Impact, Known Limitations / Post-Release Actions
- Include a verification section explaining how the change was tested (via SELECT, via isolated test query, against a sample provider, etc.)

### Compliance checklist before submitting

Before opening a PR for any new or modified database object, verify:

- [ ] Object follows naming conventions (`VW_`, `usp_`, `IX_`, etc.)
- [ ] All `NVARCHAR` (no `VARCHAR`)
- [ ] All `DATETIME2(3)` (no `DATETIME`)
- [ ] `DECIMAL(19,4)` for money, `DECIMAL(19,8)` for rates
- [ ] Named constraints (`PK_`, `FK_`, `UQ_`, `CHK_`, `DF_`)
- [ ] All indexes use compression
- [ ] UPPERCASE SQL keywords, leading commas, schema-qualified object references
- [ ] Script is idempotent
- [ ] Procedures include `SET NOCOUNT ON; SET XACT_ABORT ON;`
- [ ] New transactional tables have audit columns
- [ ] No `VARCHAR`, `DATETIME`, `MONEY`, scalar UDFs, physical deletes, `ON DELETE CASCADE`
- [ ] Baseline commit included current production code before changes

### Creating PRs via Azure DevOps MCP

Use `mcp__ado__repo_create_pull_request` with:

- `repositoryId`: the repo GUID from the table above
- `sourceRefName`: `refs/heads/PBI-XXXXX-description`
- `targetRefName`: `refs/heads/main`
- `workItems`: the ticket number as string

### Announcing a PR in Teams (the DBUp chat webhook)

When Ed asks to "post the PR" / announce it to the team, the target is the **DBUp chat**, reached via a Power Automate incoming webhook. Do NOT use the WeeklyOperationsSLAs reports webhook (that flow posts to the SLA/Department reports channel; its URL lives in the `run_*.bat` files under `C:\Scripts\WeeklyOperationsSLAs` on revops-server).

- **Canonical example + URL source:** `C:\Scripts\TeamsNotices\post_dbup_pr_notice.ps1` on revops-server (readable over WinRM: `Invoke-Command -ComputerName revops-server { ... }`; RPC is blocked, WinRM works). The URL is also captured at `C:\Scripts\CompanyAssociation\dbup_webhook_url.txt` (server) and `C:\Users\esmith\temp\assoc_matcher_final\dbup_webhook_url.txt` (local). Never echo the URL into chat or logs.
- **Payload:** `{"type":"message","attachments":[{"contentType":"application/vnd.microsoft.card.adaptive","content":{<AdaptiveCard v1.4>}}]}` with a single `TextBlock` (`wrap: true`) carrying the whole message as markdown. POST with `Content-Type: application/json; charset=utf-8`; HTTP 202 (sometimes 200) = success.
- **Voice/content:** first person from Ed ("Hi team - I've put up **PR #NNNN**..."), what the PR adds, testing status, a `[View PR #NNNN in Azure DevOps](url)` link, "Thanks!". No AI/Claude attribution ever.
- **Timing:** Ed usually wants these to land ~7:00 AM PT; schedule a one-time task rather than posting off-hours.
- **Reviewer convention (both DBUp-* and RevOps PRs):** add the standard reviewer set (see memory `reference_dbup_finance_reviewers`) via `repo_update_pull_request_reviewers`. Review requirements are BRANCH POLICY (auto-complete waits for them): DBUp PRs need **one data engineer + one analyst**; **RevOps needs one data engineer + two analysts**. Setting auto-complete right after opening the PR is therefore safe and is Ed's normal pattern. Don't describe reviews as optional in announcements or PR text.

### Key IDs

- **HFD Project:** `1a9ee84b-890e-4a44-aec8-8eb32c852551`

## Commit and PR Content Rules

- NO `Co-Authored-By` trailers or Anthropic/Claude references in commit messages
- NO references to CLAUDE.md, .claude/, or docs/superpowers/ in git commits (these are gitignored)
- Commit messages should focus on **why**, not just what
- When editing an existing function/view/proc in DBUp, always commit the **original production code first** as the baseline, then commit the changes on top

## Shell Gotchas (Windows)

- PowerShell here-strings (`@'...'@`) fail when SQL contains single quotes (e.g., `O'Connor`). Use Write/Edit tools instead of shell commands for SQL file creation
- Bash heredocs can be interrupted. For large SQL files, prefer the Write tool or Agent tool
- Git commit messages with special characters (backticks, dollar signs) need careful quoting. Prefer HEREDOCs with single quotes

## Incident Root-Causing: Verify Execution Before Naming a Culprit

When root-causing "which process inserted/changed X", distinguish proved facts from pattern-matching. State unverified links as "consistent with", never "was". Verification sources that work at HFD:

- **Query Store on Finance** (READ_WRITE, per-database permission works even when `sys.dm_exec_procedure_stats` is denied): per-proc execution counts and time windows via `sys.query_store_query` (filter `q.object_id = OBJECT_ID('dbo.ProcName')`) joined to `query_store_plan` -> `query_store_runtime_stats` -> `query_store_runtime_stats_interval`. Ad-hoc statements have `object_id = 0`, but capture mode AUTO may skip cheap one-off statements, so absence of an ad-hoc entry is weak evidence.
- **DbUp journal** (`dbo.SchemaVersions`): exactly when each migration applied. A broken CI trigger flushes the whole pending queue in one run when fixed, applying files in sort-key order within minutes of each other.
- **Tool-specific audit tables**: FinOps manual adds log to `finance.dbo.SAOPurchase_AddLog` (`@AddedBy`, `@Reason`). Check these before concluding "manual insert".

Traps learned from the 9683617 incident (8/2026):
- **SAOPurchaseHistory `Id` adjacency cannot fingerprint the inserting proc.** History Ids are assigned at the move-to-history step, which re-orders rows (ascending OfficeID, types interleaved). Populate-time clustering is destroyed.
- **Eligibility copy-drift is the standing failure mode.** Multiple objects re-implement SAOOriginations' WHERE inline: `SAOOriginationsMissed` (feeds the daily SAOPopPurchaseOriginations catch-up sweep), `SAOPop_Purchase2/3`, `SAOPopPurchaseOriginationsByProvider_Batch(_v2)`, `SAOPopPurchaseOneOrig_Clear`, `SAOPopPurchaseOneAdjAlt`, `SAOPopRepurchase`. Any gate added to SAOOriginations MUST be replicated into these copies (KEEP IN SYNC markers exist) or a held loan becomes a "missed" loan to the sweeper and funds anyway.

## Related Skills

- **`ssrs`** - For SSRS reports on `hfdsqlreport.office.local`. Use when searching for or modifying reports that reference database objects you're changing
- **`tableau-twb`** - For building or modifying Tableau workbooks over these databases (Custom SQL or the published v.HfdV3 source). Carries the GUID field map for v.HfdV3, the generated-dashboard recipe, and the number-format tokens.
- **`twb-selftest`** - **MANDATORY gate before delivering ANY generated or modified .twb/.twbx**: static lint, then the Tableau Desktop open smoke test (Desktop is the only authoritative validator; static checks alone shipped two broken files in one day). If a database task ends in a workbook handoff, run it.

## Reference Files

- `references/data-standards.md` - **Full HFD Data Standards Rule Book** (mandatory for all new code)
- `references/provider-hierarchy.md` - Provider table column details and parent/child logic
- `references/etl-patterns.md` - MERGE procedure templates and row hash patterns
- `references/v3-origination-offers.md` - **V3 EasyAPI origination**: EasyAPISummary decisions, approval-rate reconstruction, OfferHistory requested/offered amounts, ProviderConfigs offer eligibility, and the no-offer / bad-config reason logic

## Disallowed in Output

Em-dashes, exclamation points, metaphors, analogies, purple prose. See CLAUDE.md for the full disallowed list.
