# HFD Data Conventions for SSRS Queries

Field codes, filter conventions, and table semantics used when writing SQL inside HFD SSRS reports. Most of these are non-obvious and have specific traps that cause silent wrong answers or zero-row results.

## PaymentStatus codes (applications.PaymentStatus)

The `applications.PaymentStatus` column stores 3-5 character CODES. Long descriptive names (`Transferred to Provider`, `Late`, etc.) appear in display/UI layers but NOT in the source column. Filtering by the long name returns 0 rows. Known codes:

| Code | Meaning |
|------|---------|
| `ACT` | Active (current) |
| `LATE` | Late (1-30 days past due) |
| `DEL` | Delinquent (30+ days past due) |
| `PCOL` | Pending Collections |
| `TCOL` | Transferred to Collections |
| `TPROV` | Transferred to Provider |
| `PIF` | Paid In Full |
| `CHG` | Charged Off |
| `CAN` | Cancelled |

Filtering example:
```sql
WHERE a.PaymentStatus IN ('TPROV', 'TCOL')
-- NOT: WHERE a.PaymentStatus IN ('Transferred to Provider', 'Transferred to Collections')
```

The existing SSRS reports translate codes to long names in the SELECT for display:
```sql
CASE
    WHEN a.PaymentStatus = 'LATE'  THEN 'Late'
    WHEN a.PaymentStatus = 'DEL'   THEN 'Delinquent'
    WHEN a.PaymentStatus = 'PCOL'  THEN 'Pending Collections'
    WHEN a.PaymentStatus = 'TCOL'  THEN 'Transferred to Collections'
    WHEN a.PaymentStatus = 'TPROV' THEN 'Transferred to Provider'
END AS 'Payment Status'
```

## Status history for as-of-date queries

`HFDProd_Finance.dbo.ApplicationPaymentStatusHistory` records every transition with a timestamp. Columns:

| Column | Type |
|--------|------|
| `ApplicationPaymentStatusHistoryID` | uniqueidentifier |
| `ApplicationId` | int (= `applications.AutoID`) |
| `OldStatus` | varchar |
| `NewStatus` | varchar |
| `CreatedDate` | datetime |
| `CreatedBy` | varchar |

To resolve "PaymentStatus as of @EndDate" for a loan: take the row with the latest `CreatedDate <= @EndDate` per `ApplicationId`, return `NewStatus`. Pattern in `skill.md`'s "Reproducibility" section.

A similar table `ApplicationStatusHistory` tracks the underlying `applications.status` field (not the payment status). `ApplicationDetailStatusHistory` exists for detail-level changes.

## Ledger fee codes (ledgerdetail.FeeCode)

The `HFDProd_Finance.dbo.ledgerdetail` table holds every accounting entry. Filter by `FeeCode` to isolate types of activity:

| FeeCode | Meaning | Sign convention |
|--------:|---------|----------------|
| `501` | Write-off (charge-off) | Amount stored as positive |
| `7300` | Payment principal | Amount stored NEGATIVE (credit to receivables); multiply by -1 to get positive collected |
| `7500` | Payment interest | Same as 7300 - stored negative |

Standard payment-collection aggregation:
```sql
SELECT ld.ProcedureID AS HFDID,
       SUM(ld.Amount) * -1 AS AmountCollected
FROM HFDProd_Finance.dbo.ledgerdetail ld WITH (NOLOCK)
WHERE ld.FeeCode IN (7300, 7500)
  AND (ld.voided = 0 OR ld.voided IS NULL)
  AND ld.AccountingCode NOT IN ('STOP', 'RFND')
  AND CAST(ld.TransactionDate AS DATE) < @EndDate
GROUP BY ld.ProcedureID
```

### AccountingCode filter values to exclude

The `AccountingCode` column on `ledgerdetail` qualifies entries that should be excluded from financial rollups:

- **`STOP`** - servicing-stop entries. ALWAYS exclude from any payment/writeoff aggregation. Every existing HFD report does.
- **`RFND`** - refund correction entries. Exclude when calculating net payments collected. The deliverable reconciliation files (provider-side) exclude these; the existing `Smile Doctors ReWork Reconciliation` SSRS report does NOT. If you need to reconcile to a provider's downloadable Excel, add `RFND` to the exclusion list. One loan with three duplicate payment bookings plus two refund corrections can swing a reconciliation by hundreds of dollars in either direction depending on whether RFND is included.

Standard exclusion clause for reconciliation reports:
```sql
AND ld.AccountingCode NOT IN ('STOP', 'RFND')
```

## SAOPurchaseHistory (provider funding data)

`HFDProd_Finance.dbo.SAOPurchaseHistory` records each SAO purchase event (and adjustments/refunds). Key columns for reconciliation:

| Column | Meaning |
|--------|---------|
| `HFDID` | Loan ID (= `applications.AutoID`) |
| `ProgCode` | Program code (e.g., `CUS-SMILEDOCS-INV-INS-03`) |
| `SAOPrice` | HFD-side purchase price (what HFD recorded paying for the receivable) |
| `P_SAOPrice` | Provider-side funding amount (what was actually funded to the provider) |
| `SAOAdvRate` / `P_SAOAdvRate` | HFD-side / provider-side advance rate |
| `MDRAmount` / `P_MDRAmount` | Merchant discount rate amounts (HFD-side / provider-side) |
| `CurrentRecord` | bit - 1 = current snapshot, 0 = historical/superseded |
| `SoldToPartner` | SPV name |
| `SoldToDate` | Date the loan was sold to the SPV |

**SAOPrice vs P_SAOPrice trap.** Choose deliberately based on whose reconciliation you're matching:
- HFD-internal: usually `SAOPrice`
- Provider reconciliation (e.g., Smile Docs disputing an invoice): `P_SAOPrice`. The provider-side deliverable spreadsheets always use `P_SAOPrice`.

These can differ by 5-10% per loan. Mismatching them creates discrepancies that look like rounding but aren't.

**Multi-record handling.** Many loans have multiple rows in `SAOPurchaseHistory` (original purchase + adjustment rows). For reconciliation totals:

```sql
-- Net funded amount per loan, INCLUDING historical and current records,
-- matching the provider's SUMIFS pattern:
SELECT sph.HFDID, SUM(sph.P_SAOPrice) AS Net_Funded
FROM HFDProd_Finance.dbo.SAOPurchaseHistory sph WITH (NOLOCK)
WHERE sph.ProgCode = 'CUS-SMILEDOCS-INV-INS-03'
GROUP BY sph.HFDID
```

Do NOT use `MAX(SAOPrice)` (returns just one record's value) and do NOT add `WHERE CurrentRecord = 1` if you're matching a provider deliverable - their SUMIFS includes all rows, current and historical. Adjustment pairs like `(+$181.96, -$181.96)` correctly net to $0 with SUM.

## AmortizationSched (term derivation)

`HFDProd_Finance.dbo.AmortizationSched` holds the per-loan payment schedule. Use this NOT `applications.NumberOfPayments` to determine a loan's term.

**Why not `applications.NumberOfPayments`:**
- Updates on loan modifications - shows remaining/modified payments, not original
- Reset to 0 on full payoff
- Counts raw payments, not months (biweekly with 78 payments is a 36-month loan, not 78)

**Canonical "original term in calendar months":**
```sql
LoanTermSpan AS (
    SELECT ams.ProcedureID AS HFDID,
           DATEDIFF(MONTH, MIN(ams.EventDate), MAX(ams.EventDate)) + 1 AS SpanMonths
    FROM HFDProd_Finance.dbo.AmortizationSched ams WITH (NOLOCK)
    WHERE ams.Event = 'Payment'
      AND ams.Payment > 6
    GROUP BY ams.ProcedureID
)
```

**The `Payment > 6` filter** is copied from the `OwnershipDataTapePopulate` stored proc on the Finance server. It excludes ~0.5% of rows that are tiny adjustment entries (e.g., $0.07 final-payment rounding, $0 placeholders for skip-payment months, sub-dollar interest-only residuals). Without it, those outlier rows can extend `MAX(EventDate)` and inflate the calculated term by a month or two. The `$6` threshold is pragmatic, not principled - real Smile Docs / HFD monthly payments are $30+, so any row above $6 is a real installment. Match this filter unless you have a reason to diverge.

`ams.Event` values include `Payment`, `Loan`, and others. Filter to `Payment` to isolate scheduled installments.

## MCP connector reliability

When running ad-hoc validation queries against the Finance DB:

- **`mcp__mssql2__execute_sql`** - newer, returns column headers, surfaces errors better. **Default choice.**
- **`mcp__mssql__execute_sql`** - older, returns `-1` rows-affected for empty/timed-out result sets. Use as a fallback when `mssql2` returns unexpected `0 rows affected` on a query you know should return data (a known `mssql2` quirk on multi-statement batches with leading `DECLARE`).
- **`mcp__SSRSReportServer__execute_sql`** - the only connector that reaches `ReportServer.dbo.Catalog` on `hfdsqlreport`. Use for catalog searches.

If `mssql2` returns `0 rows affected` for a query that should have rows: replace `DECLARE @X DATE = '...'` parameter blocks with inline literal date strings and retry. `mssql2` sometimes suppresses the result set when a multi-statement batch starts with `DECLARE`.

## Cross-database object reference

Common qualified-name patterns:

| Object | Fully qualified |
|--------|-----------------|
| Loan / application | `HFDProd_Finance.dbo.applications` |
| Provider | `HFDProd_Finance.dbo.providers` |
| Ledger entries | `HFDProd_Finance.dbo.ledgerdetail` |
| SAO purchase/adjustment | `HFDProd_Finance.dbo.SAOPurchaseHistory` |
| Amortization schedule | `HFDProd_Finance.dbo.AmortizationSched` |
| Payment status history | `HFDProd_Finance.dbo.ApplicationPaymentStatusHistory` |
| Netpurchases snapshot | `finance.dbo.netpurchases` |
| Ownership data tape (canonical loan attributes) | `Analytics.dw.vw_ownershipdatatape` |

The `finance.dbo.netpurchases` table is the standard point-in-time snapshot for "what was this loan's state as of `@reportend`?" - filter `WHERE np.reportend = @EndDate` with strict equality. Multiple reportend dates exist concurrently (rolling monthly snapshots).

## Stop-loss / true-up calculation context

For the Smile Docs ReWork reconciliation (and similar stop-loss programs), the per-loan stop-loss-owed formula is:

```
StopLossAmount  = P_SAOPrice * (1 - StopLossPct)
StopLossOwed    = StopLossAmount - AmountCollected
```

Where:
- `StopLossPct` looks up by `(Term, MatrixGrade)` from a contract-specific thresholds table
- Negative `StopLossOwed` values are kept in the sum (collected exceeded stop-loss-adjusted exposure)
- Loans without a matched threshold (off-bucket terms) contribute $0

This is the per-loan methodology that matches provider-side reconciliations. The alternative cohort-level methodology (sum write-offs per vintage, compare to `CohortFinance * StopLossPct`) is also defensible per contract language but produces different numbers.
