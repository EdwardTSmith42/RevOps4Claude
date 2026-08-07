---
name: cofi-nvision
description: >
  Reference for the CoFi/NVision funding integration — data ingestion, SAO function split,
  funding gates, transaction types, and troubleshooting. Use this skill whenever working on
  CoFi-related code, debugging CoFi ingestion issues, modifying SAOOriginations/SAOAdjustments/
  SAOCancellations, investigating CoFi provider funding, touching SAOPurchaseHistory for CoFi
  providers, or when the user mentions CoFi, NVision, provider 37204, PartnerProviders 172,
  CofiFundingRequests, or the CoFi nightly file. Also use when working with the vSAOPurchaseHistorySummary
  view or any of the ~170 downstream objects that join on SAOPurchaseHistory.
---

# CoFi / NVision Funding Integration

CoFi (PartnerId 172) is a funding partner that co-funds applications with NVision. For CoFi-involved
applications, the payment is split between NVision (original provider) and CoFi (provider ID 37204),
going to two separate bank accounts.

> **IMPORTANT — model change (July 2026, PR #10621):** The original design split the ORIGINATION
> into two SAOPurchaseHistory rows (NVision + CoFi 37204 legs). That was rolled back due to
> downstream impact (~300 objects join on SAOPurchaseHistory assuming one origination per HFDID).
> The current model: SAO functions produce ONE row per event with FULL amounts; the **payment**
> is split downstream instead (targeted 8/14/2026). The funding gates and Void hold REMAIN —
> CoFi providers are still held until their split data arrives in CofiFundingRequests.
> Sections below describing two-row splits, CROSS APPLY, split_pct math, and OfficeID 37204 legs
> document the RETIRED design — kept for history/PR archaeology, do not re-implement.

## Architecture Overview

```
CoFi SFTP server (sftp.gohfd.com:/Cofi/)
    |
    v  (nightly CSV: hfd_daily_export_YYYYMMDD.csv)
Python ingestion pipeline (revops-server, C:\Scripts\CoFi\)
    |
    v  (staging -> sproc -> target)
Analytics.dw.CofiFundingRequests
    |
    v  (LEFT JOIN from Finance functions)
SAOOriginations / SAOAdjustments / SAOCancellations
    |
    v  (SAOPopPurchase inserts results)
finance.dbo.SAOPurchaseHistory (2 rows per CoFi HFDID)
    |
    v  (collapses back to 1 row)
finance.dbo.vSAOPurchaseHistorySummary (for downstream consumers)
```

## Key Tables and Objects

| Object | Database | Purpose |
|--------|----------|---------|
| `dw.CofiFundingRequests` | Analytics | Target table for ingested CoFi file data |
| `dw.stgCofiFundingRequests` | Analytics | NVARCHAR staging table, truncated after each load |
| `dw.stgCofiFundingRequests_Rejected` | Analytics | Rejected rows with RejectReason |
| `dw.usp_CofiFundingRequestsLoadFromStage` | Analytics | CTE-based ETL: validate, reject, dedup, load |
| `dbo.IngestionAudit` | Analytics | Pipeline audit trail (SUCCESS/FAILED/SKIPPED) |
| `dbo.SAOOriginations()` | Finance | Origination function with CoFi split + funding gate |
| `dbo.SAOAdjustments()` | Finance | Adjustment function with CoFi split + funding gate |
| `dbo.SAOCancellations()` | Finance | Cancellation function with CoFi split + funding gate |
| `dbo.SAOPurchaseHistory` | Finance | Historical purchase records (2 rows per CoFi HFDID) |
| `dbo.SAOPurchase` | Finance | Interim queue table (SAOPopPurchase inserts here) |
| `dbo.vSAOPurchaseHistorySummary` | Finance | View collapsing split rows back to 1 per event |
| `dbo.PartnerProviders` | HFDProd_Finance | Links providers to CoFi (PartnerId=172) |
| `dbo.Partners` | HFDProd_Finance | CoFi = PartnerId 172, PartnerName 'CoFi' |

## CoFi Providers

CoFi-linked providers are determined dynamically from `HFDProd_Finance.dbo.PartnerProviders WHERE PartnerId = 172 AND IsActive = 1`.

As of July 2026, these include:
- 35708, 35737 — CoFi integration accounts
- 37204 — **Cofi Integrated Holder** (the CoFi destination office for split rows)
- 37601 — NVision Eye Centers - Parent
- 37602, 37603, 37604, 37605 — NVision Management subsidiaries

Bank info for funding is on `HFDProd_Finance.dbo.ProviderBillingAccounts` — use **Bank2** columns.

## The CoFi Nightly File

### Vendor Contract
- **Delivery**: Daily via SFTP, 03:00-04:00 UTC
- **File naming**: `hfd_daily_export_YYYYMMDD.csv`
- **Encoding**: UTF-8, LF line endings, RFC 4180 quoting
- **Idempotent**: re-sent files for the same date contain the same data

### Schema (7 columns, strict order)
| Column | Type | Description |
|--------|------|-------------|
| `transaction_date` | String (MM-DD-YYYY) | Business date |
| `hfd_loan_id` | Integer/String | Maps to HFDID |
| `hfd_provider_id` | Integer | HFD provider ID |
| `cofi_invoice` | String | CoFi invoice number |
| `transaction_type` | String | Purchase, Refund, Partial Refund, Void |
| `nvision_amount` | Integer | NVision's share in **cents** |
| `cofi_amount` | Integer | CoFi's share in **cents** |

### Target Table Column Names (PascalCase after sproc)
`TransactionDate`, `HfdLoanId`, `HfdProviderId`, `CofiInvoice`, `TransactionType`, `NvisionAmount`, `CofiAmount`

## Transaction Type Mapping

| File TransactionType | SAO Function | What it means |
|---------------------|--------------|---------------|
| **Purchase** | SAOOriginations | Fund the split — standard origination |
| **Partial Refund** | SAOAdjustments | Partial balance reduction |
| **Refund** | SAOCancellations | Full cancellation, negative amounts |
| **Void** | EXCLUDED | Don't fund — takes priority over Purchase |

Each function joins to CofiFundingRequests filtering on its respective TransactionType.

## The Split Math

**The file amounts are TotalCost splits, NOT P_SAOPrice (purchase price) splits.**

This was a critical discovery — the amounts represent how much each funder pays toward the provider's
total cost. P_SAOPrice, SAOPrice, and MDR are calculated from the split TotalCost using existing rates.

```
-- Split ratio from the file
NVision_pct = NvisionAmount / NULLIF(NvisionAmount + CofiAmount, 0)
CoFi_pct    = CofiAmount    / NULLIF(NvisionAmount + CofiAmount, 0)

-- TotalCost per leg (from file, via split_pct * original TotalCost)
NVision TotalCost = NvisionAmount / 100    (cents to dollars)
CoFi    TotalCost = CofiAmount / 100

-- All other values derived from split TotalCost using EXISTING rates:
P_SAOPrice = split_TotalCost * P_SAOAdvRate
SAOPrice   = P_SAOPrice + (split_TotalCost * HFDAddFeeRate)
MDRAmount  = split_TotalCost - SAOPrice    (the 4% discount)
HFDAddFee  = split_TotalCost * HFDAddFeeRate

-- RATES are identical on both legs (application-level, NOT split):
SAOAdvRate, P_SAOAdvRate, MDRRate, P_MDRRate, HFDAddFeeRate, ReserveRate
```

**Common mistake**: If MDR = 0, the file amounts are being treated as P_SAOPrice instead of TotalCost.
Check that `split_P_SAOPrice` is NOT being set directly from the file — the CROSS APPLY should only
produce `split_pct` and `split_OfficeID`, not a dollar amount.

## Funding Gates

All three SAO functions have a funding gate that holds CoFi-linked providers until the appropriate
split data arrives in CofiFundingRequests:

```sql
-- Pattern (in WHERE clause):
AND NOT (
    -- Provider IS linked to CoFi
    EXISTS (
        SELECT 1 FROM HFDProd_Finance.dbo.PartnerProviders cp WITH (NOLOCK)
        WHERE cp.ProviderId = a.ProviderID AND cp.PartnerId = 172 AND cp.IsActive = 1
    )
    -- BUT split data has NOT arrived yet
    AND NOT EXISTS (
        SELECT 1 FROM Analytics.dw.CofiFundingRequests cofi_gate WITH (NOLOCK)
        WHERE TRY_CAST(cofi_gate.HfdLoanId AS INT) = a.HFDID
        AND cofi_gate.TransactionType = '<type>'  -- Purchase / Partial Refund / Refund
    )
)
```

| Function | Gate checks for | Effect |
|----------|----------------|--------|
| SAOOriginations | `Purchase` | Holds origination until Purchase split exists |
| SAOAdjustments | `Partial Refund` | Holds adjustment until Partial Refund split exists |
| SAOCancellations | `Refund` | Holds cancellation until Refund split exists |

**Void priority** (SAOOriginations only): If a Void record exists for an HFDID, it's excluded
from originations entirely, even if a Purchase also exists.

**Gate column gotcha**: The cancellation gate must use `a.providerid` (from @Applications), NOT
`la.hfdid` (which is the loan ID). Using the wrong column makes the gate a silent no-op.

## CROSS APPLY Split Pattern

Each function uses CROSS APPLY with a VALUES clause to produce two rows per CoFi HFDID:

```sql
CROSS APPLY (
    VALUES
        ('NVision',
         CASE WHEN cofi.HfdLoanId IS NOT NULL
              THEN CAST(cofi.NvisionAmount AS DECIMAL(18,6))
                   / NULLIF(CAST((cofi.NvisionAmount + cofi.CofiAmount) AS DECIMAL(18,6)), 0)
              ELSE 1.0 END,
         a.ProviderID),
        ('CoFi',
         CASE WHEN cofi.HfdLoanId IS NOT NULL
              THEN CAST(cofi.CofiAmount AS DECIMAL(18,6))
                   / NULLIF(CAST((cofi.NvisionAmount + cofi.CofiAmount) AS DECIMAL(18,6)), 0)
              ELSE NULL END,
         CASE WHEN cofi.HfdLoanId IS NOT NULL THEN 37204 ELSE NULL END)
) AS split(split_leg, split_pct, split_OfficeID)
```

- Non-CoFi apps: NVision row gets `split_pct = 1.0` (no change), CoFi row gets `NULL` (filtered out)
- CoFi apps: two rows with proportional split_pct values
- `WHERE split.split_pct IS NOT NULL AND split.split_pct <> 0` filters out phantom and zero-value rows

### CofiFundingRequests Dedup

The JOIN to CofiFundingRequests uses dedup subqueries:
- **SAOOriginations**: `ROW_NUMBER() OVER (PARTITION BY HfdLoanId ORDER BY ID DESC)` — latest Purchase
- **SAOAdjustments**: `SUM(NvisionAmount), SUM(CofiAmount) GROUP BY HfdLoanId` — aggregates all Partial Refunds
- **SAOCancellations**: `SUM(...)` — aggregates all Refunds

### Join Safety for Downstream

After CoFi split, SAOPurchaseHistory has TWO origination rows per CoFi HFDID. Functions that join
to it must filter `OfficeID <> 37204` to get the NVision row for rates:

- `SAOAdjustments`: `fsaooriginationdata() ph ... AND ph.OfficeID <> 37204`
- `SAOAdjustments`: `phfo` subquery also filters `OfficeID <> 37204`
- `SAOCancellations`: `@SAO_Origination` and `@SAO_FinancialOwner` both filter `OfficeID <> 37204`

## Summarized View: vSAOPurchaseHistorySummary

Collapses NVision + CoFi rows back to one row per event for ~170 downstream objects.

**Grouping key**: `(HFDID, Type, AdjustmentDate, SoldToDate)`

| Treatment | Columns |
|-----------|---------|
| **SUM** | TotalCost, SAOPrice, MDRAmount, P_SAOPrice, P_MDRAmount, HFDAddFee, ReserveAmount, AdjustmentAmount, DownPayment, DownPmtPAID, NetDwnPmtOwed |
| **MAX** (identical on both legs) | All rates, non-financial columns |
| **Conditional MAX** (NVision row only) | ParentOfficeID, ProviderName, OfficeID, PracticeName, CompanyID, DoctorID, ProgCode, SoldToPartner |
| **CAST wrapper** | IsPromo, CurrentRecord (`CAST(MAX(CAST(... AS TINYINT)) AS BIT)` — MAX on bit is invalid) |

## Ingestion Pipeline

**Location**: `\\revops-server\c$\Scripts\CoFi\`
**Schedule**: Daily via Task Scheduler (`CofiFundingRequests_DailyRun`), 6:00 AM local
**Config**: `.env` file (not committed; `.env.example` is the template)

### Flow
1. Try network share (`\\PRPTBI01\Cofi`) — currently inaccessible
2. Fall back to SFTP (`sftp.gohfd.com:/Cofi/`)
3. Catch-up window: LOOKBACK_DAYS=10 (yesterday back 10 days)
4. For each file in window: skip if already SUCCESS in IngestionAudit
5. Read CSV, map columns, clean values
6. Load to staging, execute sproc, mark SUCCESS/FAILED
7. Send Teams notification (CofiNotifications channel)

### Known Issues

**Empty files**: CoFi has historically sent header-only files (102 bytes). The pipeline processes
them as SUCCESS with RowCount=0. When CoFi later updates the file with real data, the pipeline
skips it (already SUCCESS). Fix: delete the IngestionAudit row and re-trigger.

**Resend handling**: The pipeline uses filename-based idempotency. A corrected re-send for the
same date will be silently skipped. Manual intervention required: delete the SUCCESS audit row.

**Teams webhook**: The webhook URL in `.env` must match the CofiNotifications channel in Power
Automate. The webhook for Tableau Health Monitoring is a different workflow ID — don't mix them up.

**9 files skipped notification**: Normal behavior with LOOKBACK_DAYS=10. Each day, 9 prior days
are already SUCCESS'd and get skipped. Only yesterday's file gets processed.

## Troubleshooting

### CoFi file has data but RowCount=0
1. Check IngestionAudit — was the file processed before data was added?
2. If STATUS=SUCCESS with RowCount=0, delete the audit row and re-trigger
3. Verify the file on SFTP actually has data: `check_sftp_file.py` or `U:\Cofi\` mapped drive

### MDR = 0 on CoFi originations
The file amounts are being treated as P_SAOPrice instead of TotalCost. Check that:
- `split_P_SAOPrice` does NOT exist in the CROSS APPLY
- Dollar CASE expressions end with `* split.split_pct` (not a direct file amount)
- The original rate-based formulas calculate from `a.TotalCost` (split by `* split_pct`)

### Provider not appearing in SAOOriginations
Check in order:
1. `fProviders()` returns the provider? (`WHERE status <> 'TST'`)
2. `fApplicationsNotSDC()` returns the HFDID?
3. Funding gate: is the provider CoFi-linked AND no Purchase data in CofiFundingRequests?
4. Void exclusion: is there a Void record for this HFDID?
5. Funding pause: `SAOProviderFundingPause WHERE isActive=1`?
6. Already processed: `HFDID IN SAOPurchaseHistory WHERE type='origination'`?

### Kerberos double-hop on revops-server
`Invoke-Command -ComputerName revops-server` with SQL Trusted_Connection fails (ANONYMOUS LOGON).
Use scheduled tasks (run locally as esmith) or RDP to run scripts that need SQL access.

## PRs and PBI

- **PBI**: 22602
- **RevOps PR #9471**: Python ingestion pipeline + .env.example
- **DBUp-Analytics PR #9470**: Staging, rejected, sproc, index, CreatedAt fix
- **DBUp-Finance PR #9496**: Initial CoFi split + summarized view
- **DBUp-Finance PR #10347**: Funding gate
- **DBUp-Finance PR #10407**: Transaction type mapping + Void priority + TotalCost fix
- **DBUp-Finance PR #10621**: ROLLBACK of the two-row split (gates + Void kept) — payment split moves downstream, launch 8/14/2026

## DBUp Migration Naming

CoFi migrations follow the standard `YYYYMMDD-N-ObjectName-PBI.sql` pattern.
DbUp journals by filename — editing an already-deployed script is a **silent no-op**.
Always create a NEW dated migration file for changes to deployed functions.
