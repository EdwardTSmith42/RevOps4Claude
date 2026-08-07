---
name: hfd-sao-adjustments
description: >
  Safely build, validate, and hand off SAO purchase adjustments against HFD Finance
  loans (Finance.dbo.saopurchase / saopurchasehistory). Use this WHENEVER someone wants to
  zero out a loan, load or post an Adjustment/Cancellation row, claw back or reverse a funding,
  correct a payment split, re-enable a zeroed loan to re-originate when the partner's split comes
  back (flip its origination to an adjustment), remediate a mis-funded provider, or fix a
  CoFi/NVision (or any partner) loan that funded when it should not have — even if they only say "make an adjustment,"
  "adjust this loan," "reverse this," "flip the type," or just name an HFDID. Also trigger for reviewing an
  adjustment script before it runs. This is production money and mostly irreversible, so the
  skill encodes the safe pattern learned the hard way: right table, mirror an existing template,
  zero-out math that accounts for prior adjustments, correct dates, transaction + rollback gate,
  PII-safe construction, and — critically — who can actually execute it. Do NOT hand-write an
  ad-hoc INSERT for these; use this skill.
---

# HFD SAO Adjustments — build them safely

Posting an SAO adjustment moves real money on a live financial ledger, and most of it can't be
cleanly undone. A wrong table, a stale date, a re-run, or a mis-mirrored column has caused real
incidents here. Your job is almost never to "just run an INSERT" — it's to **build a faithful,
validated adjustment and route it to someone who can execute it**, because the read connectors
you have usually can't (and shouldn't) write to these tables.

Pair this with the **`hfd-database`** skill (connectors, `WITH (NOLOCK)`, the `mssql` MCP
gotchas) and the memories `project_nvision_cofi_zeroout`, `reference_hfd_partner_mapping`, and
`reference_provider_funding_pause`. A worked example lives at
`C:\Users\esmith\temp\nvision_9542790_zeroout.sql`.

## The two tables (this trips everyone up)

- **`Finance.dbo.saopurchase`** — the *operational/interim* table. This is the **entry point**:
  FinOps loads new adjustments here, and they flow into history on the next cycle. It is
  **transient — it gets cleared/reloaded each SAO run**, so a row you insert must be picked up
  before the next clear. Same column schema as history.
- **`Finance.dbo.saopurchasehistory`** — the *permanent* ledger. Adjustments **end up here**
  (the funding process copies them over and stamps `FundDate` on propagation), but you do not
  normally insert here directly — doing so bypasses the operational process and was the original
  mistake in the NVision remediation.

**Rule of thumb:** target **`saopurchase`** (the way FinOps entered every past adjustment); let
it flow to history naturally. If someone insists on history, confirm why first.

## Who can actually run it (check this early)

The MCP SQL login (`ReportUser` on HFDSQLFinance) is effectively read-only on these tables:
`HAS_PERMS_BY_NAME(...,'INSERT')` returns **0** for both `saopurchase` and `saopurchasehistory`.
So you generally **cannot execute the insert yourself** — build and validate it, then hand it to
**FinOps** (their process owns `saopurchase`) or to someone whose SSMS login has write access.
Don't burn a turn trying to INSERT through the MCP; verify perms with
`HAS_PERMS_BY_NAME('Finance.dbo.saopurchase','OBJECT','INSERT')` and plan the hand-off.

## The safe workflow

### 1. Scope and verify the loan(s)
- Confirm the exact HFDID(s). If the request is "all the X loans," resolve the set from data,
  not names. For partner/CoFi scope, identify via `HFDProd_Finance.dbo.PartnerProviders`
  (`PartnerId` — CoFi = 172), **not** `SoldToPartner` (that column is the SPV the loan was sold
  to, e.g. `CH SPV Reign Rock`, not the partner). See `reference_hfd_partner_mapping`.
- Pull the loan's **current net paid** across *all* existing rows:
  ```sql
  SELECT HFDID, SUM(CASE WHEN Type='Origination' THEN 1 ELSE 0 END) AS Orig,
         SUM(CASE WHEN Type='Adjustment' THEN 1 ELSE 0 END) AS Adj,
         CAST(SUM(P_SAOPrice) AS DECIMAL(19,2)) AS NetPaid
  FROM Finance.dbo.saopurchasehistory WITH (NOLOCK) WHERE HFDID = @hfdid GROUP BY HFDID;
  ```
  Prior partial adjustments are common — you must zero the **remaining** net, not the original.

### 2. Pull a real template — never invent the row shape
Find a recent adjustment for the **same ProgCode / program** and mirror it exactly:
```sql
SELECT TOP 1 * FROM Finance.dbo.saopurchasehistory WITH (NOLOCK)
WHERE Type='Adjustment' AND ProgCode = @progcode ORDER BY Id DESC;
```
The column conventions (money split, which fields are zeroed vs copied) matter and quietly
change per program. Copying a live example is far safer than reconstructing from memory.

### 3. Compute the amounts (zero-out math)
To bring a loan to **$0 paid**, the adjustment's money columns = **negative of the current net**
of each column (summed across every existing row for that HFDID). This nets to zero even when
prior adjustments exist. The columns move together on the advance/MDR split:

| Column | Value |
|---|---|
| `Type` | `'Adjustment'` |
| `TotalCost`, `AdjustmentAmount` | `-(net TotalCost)`  (the gross) |
| `SAOPrice`, `P_SAOPrice` | `-(net SAOPrice)` = gross × `SAOAdvRate` (e.g. 0.96) |
| `MDRAmount`, `P_MDRAmount` | `-(net MDRAmount)` = gross × `MDRRate` (e.g. 0.04) |
| `FinancedAmount` | **unchanged** (copy the original) |
| downpayment fields, `MonthlyPmt` | `0` |
| rates (`SAOAdvRate`,`MDRRate`,`P_*Rate`,`BaseAdvRate`) | copy from origination |
| `Id` | **IDENTITY — never insert it** |

`SAOPrice + MDRAmount = TotalCost` on every leg — a good arithmetic self-check. For a partial
adjustment (not a full zero-out), the same shape applies with the partial gross.

### 4. Dates — the subtle ones
- **`AdjustmentDate`** = the accounting/load date. Confirm the intended period with FinOps
  rather than assuming; `CAST(GETDATE() AS date)` is a reasonable default.
- **`SoldToDate`** = the **next sale cycle**, i.e. `AdjustmentDate + 1` — **NOT** the
  origination's `SoldToDate` (which is in the past). This is how the reversal gets picked up by
  the upcoming SPV sale run. Copying the origination's stale `SoldToDate` back-dates the sale and
  it won't be processed. (Past pattern: `AdjustmentDate 6/25 → SoldToDate 6/26`.)
- **`FundDate`** = `NULL` on entry into `saopurchase`; the funding process sets it on
  propagation. `SoldToPartner` = copy the origination's SPV.

### 5. Build the row with INSERT … SELECT from the origination
Select from the loan's **origination row** and negate the money columns. This copies the
descriptive and PII columns (`PatientID`, `FirstName`, `LastName`, `BankLast4`, `Routinglast4`)
**server-side** so they never surface in the script text or your context — a clean PII posture.
Only override `Type`, the money columns, and the dates. Wrap it so it's reviewable:

```sql
USE Finance; SET NOCOUNT ON; SET XACT_ABORT ON;

-- BEFORE: current state (expect NetPaid = the amount you're reversing)
SELECT HFDID, CAST(SUM(P_SAOPrice) AS DECIMAL(19,2)) AS NetPaid
FROM Finance.dbo.saopurchasehistory WITH (NOLOCK) WHERE HFDID = @hfdid GROUP BY HFDID;

BEGIN TRAN;

INSERT INTO Finance.dbo.saopurchase ( /* explicit column list, excluding Id */ )
SELECT 'Adjustment', o.ParentOfficeID, /* …descriptive cols copied… */
     , -o.TotalCost                 -- TotalCost
     , 0, 0, 0, 0                   -- downpayment fields
     , o.FinancedAmount             -- unchanged
     , -o.TotalCost                 -- AdjustmentAmount
     , CAST(GETDATE() AS date)      -- AdjustmentDate  (confirm the period)
     , /* interestrate, NumberOfPayments */ , 0 /*MonthlyPmt*/
     , -o.SAOPrice, o.SAOAdvRate, -o.MDRAmount, o.MDRRate
     , o.SoldToPartner
     , CAST(DATEADD(DAY,1,CAST(GETDATE() AS date)) AS date)  -- SoldToDate = next cycle
     , /* MatrixGrade, DoctorID */ , 1 /*CurrentRecord*/
     , NULL                         -- FundDate (set on processing)
     , /* … */ , -o.P_SAOPrice, o.P_MDRRate, -o.P_MDRAmount, /* … */
FROM Finance.dbo.saopurchasehistory o WITH (NOLOCK)
WHERE o.HFDID = @hfdid AND o.Type = 'Origination';

PRINT CONCAT('Rows inserted: ', @@ROWCOUNT, '  (expected 1 per loan)');

-- AFTER: net across history + interim should equal the target (0.00 for a zero-out)
SELECT CAST(SUM(P_SAOPrice) AS DECIMAL(19,2)) AS NetPaid
FROM ( SELECT P_SAOPrice FROM Finance.dbo.saopurchasehistory WITH (NOLOCK) WHERE HFDID=@hfdid
       UNION ALL
       SELECT P_SAOPrice FROM Finance.dbo.saopurchase        WITH (NOLOCK) WHERE HFDID=@hfdid ) x;

ROLLBACK TRAN;   -- <<< change to COMMIT only after both result sets look right
```

**The transaction defaults to `ROLLBACK`.** The person running it reviews the before/after, then
flips to `COMMIT`. Keep validation SELECTs to non-PII columns (HFDID, amounts, office) per the
`pci-pii-guard` skill.

### 6. Hand off
State plainly that the MCP login can't execute it, and route the script to FinOps (or a
write-capable SSMS login). Offer to draft the one-line note to FinOps. Record the remediation in
the relevant project memory / incident notes.

## Gotchas that have actually bitten us

- **Self-zeroing on re-run.** A script that computes `-(current net)` is **not** idempotent —
  after the first run nets the loan to $0, re-running posts a **$0.00** no-op row (a duplicate).
  Running one 4× created 20 stray rows once. Post exactly **one** row per loan; don't loop it.
- **Wrong table.** Direct `saopurchasehistory` inserts bypass the FinOps process and had to be
  cleaned up. Target `saopurchase` unless told otherwise.
- **Stale `SoldToDate`.** Copying the origination's `SoldToDate` back-dates the SPV sale; use
  next-cycle (`+1`).
- **PII.** Never SELECT/display `FirstName`/`LastName`/`PatientID`/`BankLast4`/`Routinglast4` in
  validation output; INSERT…SELECT keeps them server-side.
- **`mssql` MCP quirks** (see `hfd-database`): single statement per call, no leading `WITH`,
  `-1` means timeout/empty. Cross-DB `OBJECT_DEFINITION` can return NULL — don't conclude an
  object is empty from that.

## Re-enabling re-origination after a split (flip origination → adjustment)

Sometimes the plan is that a zeroed loan should **re-originate later** — e.g. a CoFi/partner loan
you zeroed now that should fund at the correct split once the partner finally sends it. You'll hit
a wall: `SAOOriginations` permanently excludes any HFDID that already has an origination row, and a
split arriving only opens the partner gate — it does **not** clear this exclusion:

```sql
AND a.HFDID NOT IN (SELECT HFDID FROM finance.dbo.saopurchasehistory WHERE type='origination')
AND a.HFDID NOT IN (SELECT HFDID FROM finance.dbo.saopurchase        WHERE type='origination')
```

So nothing re-originates on its own.

**Fix (data-only, no code change):** flip the loan's single `'Origination'` row to `'Adjustment'`.
That drops it from the exclusion set; **amounts are untouched so net paid is unchanged** (the
flipped +row and the existing zero-out −row both sit under 'Adjustment' and cancel); and once the
split lands the loan re-originates the correct legs.

```sql
UPDATE h SET h.Type = 'Adjustment'
FROM Finance.dbo.saopurchasehistory h JOIN @Loans l ON l.HFDID = h.HFDID
WHERE h.Type = 'Origination' AND h.OfficeID = @office;   -- expect exactly N rows
```

Same rig as any ledger write: transaction + `ROLLBACK` default, before/after SELECTs, and
**assert `@@ROWCOUNT = expected` (auto-rollback if it isn't)**. FinOps / a write login runs it —
`ReportUser` can't UPDATE these tables either.

**Know before you flip:**
- **Safe to run before the split.** After the flip the loan is eligible but the partner gate still
  *holds* it (no `'Purchase'` row in `Analytics.dw.CofiFundingRequests` yet), so it won't
  re-originate that night — no double-pay.
- **Necessary but not sufficient.** Re-origination only fires when a `'Purchase'` split actually
  lands in `CofiFundingRequests`. If that ingestion isn't running (it has sat empty), flipping
  alone does nothing — the split feed has to be fixed too.
- **Cosmetic:** the flipped row is an `'Adjustment'` with `AdjustmentDate = NULL` /
  `AdjustmentAmount = 0` (the dollars stay in `P_SAOPrice`), and the loan drops out of origination
  reports (net $0). Stamp `AdjustmentDate` / `AdjustmentAmount` if adjustment reporting keys on them.
- **Alternative:** if you'd rather *not* re-originate, post the split as a `'purchase'` / Sale when
  it arrives and leave the originations intact (cleaner audit trail). Pick per how the split is
  meant to pay — confirm with FinOps.

Worked example: `C:\Users\esmith\temp\nvision_flip_origination_to_adjustment.sql`.

## A funding pause is the reliable belt-and-suspenders

If the goal is to *prevent* funding (not reverse it), a provider **funding pause**
(`FinOpsPauseProviderFunding_XML`, see `reference_provider_funding_pause`) blocks every path and
is executable by `ReportUser`. Consider it when a code/data control is still stabilizing.
