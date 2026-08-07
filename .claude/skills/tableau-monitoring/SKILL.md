---
name: tableau-monitoring
description: >
  Institutional knowledge for HFD's Tableau infrastructure — the HFDV3 metric monitor system,
  virtual connection limitations, the architecture redesign to published datasources, and
  lessons learned. Use this skill whenever working on Tableau extract refreshes, virtual
  connections, Bridge health issues, the HFDV3 monitor Python codebase, datasource performance
  tuning, or planning changes to HFD's Tableau data architecture. Also use when someone asks
  about why we moved away from virtual connections, what the monitor does, how the 3-year
  rolling window works, or anything related to HFDV3Base, Bridge timeouts, or extract failures.
  Trigger even on casual references like "the monitor is failing" or "refresh is slow."
---

# HFD Tableau Monitoring & Architecture

This skill captures the full context of HFD's Tableau monitoring system and the architectural
decisions behind it. It exists so future sessions can pick up where we left off without
re-discovering things the hard way.

## What This Covers

1. **The HFDV3 Metric Monitor** — a Python system that validates Tableau data against SQL Server
2. **Virtual connection limitations** — why we're killing them
3. **The architecture redesign** — published datasources with 3-year rolling windows
4. **What we tried and what failed** — so you don't repeat the experiments
5. **The FactOffer problem** — why it's separate and what we decided

For detailed schemas, row counts, SQL queries, and the monitor codebase structure, read
`references/technical-details.md`.

---

## The HFDV3 Metric Monitor

### What It Does

The monitor is a Python system (`hfdv3_monitor/`) that runs on the revops server and:

1. Queries Ed's Tableau published datasource for `SUM(ContractValue)` (treatment volume)
2. Queries SQL Server directly for the same metric with a 3-year rolling window
3. Compares the two values — if they differ by more than 1%, something is wrong
4. Sends Teams notifications on mismatch, staleness, or recovery
5. Monitors Tableau Bridge health and can auto-restart on cache corruption
6. Writes a health CSV for trend tracking

### Codebase Structure

```
hfdv3_monitor/
├── monitor.py          — Main orchestrator, entry point
├── config.yaml         — All metric pairs, thresholds, server settings
├── tableau_client.py   — Tableau REST API client with retry/circuit-breaker
├── sql_client.py       — Direct SQL Server client (pyodbc, Windows Auth)
├── comparisons.py      — Metric comparison engine (supports Tableau + SQL sources)
├── notifier.py         — Teams webhook notifications
├── health.py           — Health report CSV writer
├── bridge_health.py    — Bridge server health checks
├── bridge_remediation.py — Cache-issue detection + auto-restart
└── requirements.txt    — requests, pyyaml, pyodbc
```

### Source Types

The comparison engine supports two source types:

- **`source_type: "tableau"`** — Queries a Tableau published datasource via VizQL Data Service.
  Uses `datasource_luid`, `measure_field`, `aggregation`, and `filters`.
- **`source_type: "sql"`** — Queries SQL Server directly via pyodbc. Uses a raw SQL `query`
  string. Connects with Windows Auth (Trusted_Connection) using existing server credentials.

The current config compares Tableau (source A) against SQL Server (source B) as the source of
truth. This replaced an earlier design that compared two Tableau datasources, which failed
constantly (see "What Failed" below).

### Key Config Values

- **Tableau site:** `healthcarefinancedirect` on `10az.online.tableau.com`
- **SQL Server:** `PRPTBI01`, database `Analytics`, Windows Auth
- **Ed's datasource LUID:** `9cffc20f-2e85-475e-a24d-2687cc566ace`
- **Threshold:** 1% mismatch tolerance
- **Freshness:** stale after 48 hours, drift alert after 24 hours

---

## Virtual Connection Limitations (Why We're Killing Them)

The HFDV3Base virtual connection (`4ab51096-dda8-4c67-bd23-75815bd25d92`) was the central
datasource for all HFD Tableau analytics. We discovered it has fundamental limitations that
published datasources don't:

### Incremental Refresh Is Append-Only

Virtual connection incremental refresh uses `WHERE column > last_max_value` and appends the
results. It never updates existing rows. There is no upsert, no replace-last-rows, no subrange
refresh. We tested this with `sdr_leads` (11,910 rows) using both `hs_lastmodifieddate` and
`sync_updated_at` — 567 modified rows were never picked up because no new rows were inserted.

Published datasources (since Tableau 2024.1-2024.2) support:
- **Replace last N rows** — refresh recent data without full extract
- **Subrange refresh** — refresh a specific date range
- **Extract filters** — permanently exclude old data
- **API-triggered refresh** — REST API call on demand

None of these are available on virtual connections.

### Hard 2-Hour Timeout

Virtual connection extract refresh has a non-configurable 2-hour timeout. With 55M+ rows across
14 tables, the HFDV3Base extract regularly bumped against this, causing failures with "Malformed
response from Tableau Data Server" or "Operation cancelled" errors.

### No REST API Trigger

There is no REST API endpoint to trigger a virtual connection extract refresh. This is an open
feature request from Tableau. You can only trigger it from the UI or on a schedule.

### No Extract Filters

Virtual connections don't support extract filters, so you can't permanently exclude old data
from the extract. Every refresh processes all rows.

### The Decision

Ed's conclusion: *"I think we can just kill virtual connections then, they are adding more
limitations vs. value."* Published datasources support all the same web authoring features —
the only difference is that editing the data model (joins/tables) requires Desktop, but
calculated fields and web edit work identically.

---

## The Architecture Redesign

### Old Model

One virtual connection (HFDV3Base) with 14 tables, 55M+ rows total, 2-hour extract timeout,
append-only incremental refresh. The monitor compared two Tableau datasources against each
other.

### New Model

**Core Published Datasource (~12.6M rows):**

| Table | Strategy | Rows |
|-------|----------|------|
| FactApplication | Custom SQL, 3yr rolling | 3.7M |
| FactContract | Custom SQL, 3yr rolling | 722K |
| DimPerson | Filtered via FactApplication join | 3.7M |
| DimAddress | Filtered via DimPerson→FactApplication | 3.7M |
| DimProvider | Direct table | 28K |
| DimDate | Direct table | ~11K |
| FactSAOPurchase | Direct table | 768K |

The rolling window uses `WHERE ApplicationCreatedOn >= DATEADD(YEAR, -3, GETDATE())` — no
manual date maintenance needed.

**Separate FactOffer Published Datasource (~22M rows):**

FactOffer has ~22M rows (avg 7 offers per application, up to 3,246 max). Date filtering barely
helps (3% reduction). The pricing team needs individual offer rows for drill-through conversion
analysis, so aggregation doesn't work. This gets its own datasource with less frequent refresh.

**The Monitor** now compares Tableau against SQL Server directly, bypassing virtual connections
entirely.

### What's Excluded

- **DimOfferFast** — Different granularity, known issues. Ed explicitly said not to use it.
- **sdr_leads** — Different use case (HubSpot data), only 11,910 rows
- **DimOffer** — Not needed without FactOffer in the core datasource

### Calculated Fields to Migrate

The virtual connection has **167 calculated fields**:
- 87 on DimProvider (LOD calcs for provider metrics, pacing, growth rates)
- 39 date/period calcs (parameter-driven period comparisons)
- 5 parameters (p_View Level, p_Metric View, p_Custom Start/End Date, p_Analysis Period)
- Various others across tables

These need to be recreated in the new published datasource(s). The test plan is to download
the Enterprise Origination Scorecard workbook, replace the datasource, and see which calcs
break — that tells us exactly which ones this workbook needs.

For the full calculated field inventory, read `references/technical-details.md`.

---

## What We Tried and What Failed

### 1. Incremental Refresh on sdr_leads (FAILED)

**What:** Test incremental refresh on the small sdr_leads table before applying to larger ones.

**What happened:**
- First tried `hs_lastmodifieddate` — field exists in SQL but wasn't mapped in the virtual
  connection. Even though the UI showed it in the dropdown, it couldn't update extract data.
- Switched to `sync_updated_at` — mapped and configured, row counts matched (11,910), but
  567 modified rows weren't picked up.

**Why it failed:** Virtual connection incremental refresh is append-only. Since no new rows
were inserted (only existing rows updated), there was nothing to append.

**Lesson:** Don't waste time configuring vconn incremental refresh for tables that get updates
to existing rows. It only works for truly append-only data (new rows with increasing timestamps).

### 2. Tableau Prep Builder (ABANDONED)

**What:** Evaluate Prep Builder as an alternative for ETL with incremental updates.

**What happened:**
- Prep Builder can read from SQL Server via Bridge (since 2025.1)
- But it cannot write back to SQL via Bridge, and cannot output to virtual connections
- Prep incremental refresh is also append-only (same limitation)
- Prep flow timeout is 4+ hours (configurable) vs 2h for vconns — more headroom but same core limitation
- A test Prep flow failed with "Invalid Query Fatal Error(1,1): invalid document structure" —
  traced to "Unknown SessionID" in Bridge logs (session pooling conflict with concurrent vconn
  extract operations)

**Why we abandoned it:** Doesn't solve the fundamental problem. Same append-only limitation,
and the session pooling conflicts with Bridge make it unreliable alongside active vconn extracts.

### 3. Monitor Comparing Two Tableau Datasources (FAILED CONSTANTLY)

**What:** The original monitor design compared Ed's Treatment Volume datasource against the
v.HfdV3 published datasource (backed by the virtual connection).

**Why it failed:** Two problems:
1. The source_b filter used `ContractStatus = 'CUR'` but that value doesn't exist in the data.
   Active contracts use status `'ACT'`. So the VizQL query returned zero/null every time.
2. Even with correct filters, the vconn extract was frequently stale or failed (2h timeout),
   so source_b data was unreliable.

This created a vicious cycle: mismatch detected → refresh triggered → refresh times out →
next run detects mismatch again → repeat forever.

**Fix:** Replaced source_b with a direct SQL Server query using Trusted_Connection. No more
dependency on the virtual connection for monitoring.

### 4. LUID ac64f376-9140-40f8-a81c-77482417a47a (NOT FOUND)

Ed provided this LUID thinking it was for the sdr_leads table. The Tableau API couldn't find
it as any content type. It was likely a table-level LUID internal to the virtual connection
editor. Clicking "refresh" on it in the UI triggered all 14 tables to refresh, not just one.

**Lesson:** Virtual connection table-level LUIDs are internal and not addressable via the
REST API. You can only refresh the entire virtual connection, not individual tables within it.

### 5. Bridge Cache Corruption (RECURRING)

The Bridge worker on PRPTBI01 periodically develops CacheInvariant/siteLuid cache corruption.
Symptoms: extract refreshes run 2-4x longer, then fail with "Malformed response from Tableau
Data Server" or "Operation cancelled" (2h timeout).

**Fix:** The monitor includes `bridge_remediation.py` which:
1. Scans Bridge worker logs for CacheInvariant warnings
2. Detects long-running jobs (>60 min)
3. Auto-restarts the Bridge Windows service when corruption is detected
4. Has a 2-hour cooldown between restarts

The Bridge service name is `Tableau Bridge worker(esmith@OFFICE)`.

---

## FactOffer: The Decision

FactOffer has 22.6M rows with only 10 columns. Each application generates an average of 7
offers (max 3,246). Key fields: OfferRequestProgramCode, OfferRequestRegion,
OfferRequestCreditGrade, OfferIssuedDate, OfferApplicationUniqueKey.

**Can we aggregate it?** We analyzed this: monthly aggregation by program code + region +
credit grade compresses to ~114K rows (99.5% reduction). But Ed confirmed the pricing team
"drills into all the offers that show sometimes and looks at conversion at each step." They
need row-level data.

**Decision:** Separate published datasource for FactOffer. The core datasource stays fast at
~12M rows, and pricing gets their own extract that can refresh on a different schedule.

**For the Enterprise Origination Scorecard specifically:** The Patient Conversion Funnel uses
aggregated counts (applications → offers → contracts), not individual rows. The Promo views
use `ContractPromoCode` from FactContract, not `OfferRequestProgramCode` from FactOffer. So
this scorecard may work entirely without FactOffer.

---

## Enterprise Origination Scorecard Test

The test workbook for validating the datasource migration:

- **Workbook LUID:** `ca75c2ed-edf8-4d88-9c3e-5c7906095688`
- **Project:** Customer Success
- **Owner:** Edward Smith
- **Views:** 6 (3 Business Review, 3 Promos)

**Test plan:**
1. Create published datasource in Desktop with custom SQL queries
2. Publish as "Enterprise Origination - Extract Test"
3. Download scorecard workbook, replace datasource
4. Identify which vconn calculated fields are missing
5. Recreate needed calcs, compare results
6. Measure refresh time (target: under 30 minutes)

The full SQL queries and join model are in `references/technical-details.md`.

---

## Quick Reference: Status Values

These tripped us up once — documenting for posterity:

| Field | Valid Values |
|-------|-------------|
| ContractStatus | ACT, PIF, TCOL, CAN, PCOL, LATE, DEL, TPROV, BNK, DEC |
| ContractDetailStatus | CAN1, ARGM, CAN3, CAN2, DISP, BNA, CHBK, PCAN, NRE, BNN, BAN, etc. |
| ApplicationStatus | (check SQL — not enumerated yet) |
| ApplicationDisposition | (check SQL — not enumerated yet) |

There is no `'CUR'` status anywhere. Active contracts = `'ACT'`.
