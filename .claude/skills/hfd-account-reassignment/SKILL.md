---
name: hfd-account-reassignment
description: Use when reassigning provider accounts from one HFD relationship rep to another - rep leaving, territory swap, mis-assigned accounts, or any mass UPDATE of HFDProd.dbo.Providers.RelationsRep. Triggers on "reassign accounts", "move accounts", "update area manager", "mis-assigned providers", "wrong rep", "fix territory", or any mention of AutoRepID, ProviderRelationsReps, or dw.TerritoryAssignment.
---

# HFD Provider Account Reassignment

## Overview

Rep ownership of an HFD provider lives in `HFDProd.dbo.Providers.RelationsRep` (an INT FK to `HFDProd.dbo.ProviderRelationsReps.AutoRepID`). The geographic territory each provider belongs to is derived from `Analytics.dw.TerritoryAssignment` (zip-first, state-fallback). Reassigning accounts means producing a deterministic, auditable UPDATE script that data engineering runs against production.

**REQUIRED BACKGROUND:** The `hfd-database` skill covers connection guidance (prefer `mssql2`), the production DB name (`HFDProd`, not `HFDProd_Finance`), and the mandatory `WITH (NOLOCK)` rule.

## When to use

- A rep is leaving and their book needs to be redistributed by territory.
- A rep is swapping territories with someone else.
- A handful of providers are on the wrong rep (zip is wrong, state is wrong, or the rep was assigned manually).
- Any time you're about to write `UPDATE HFDProd.dbo.Providers SET RelationsRep = ...`.

Do NOT use for one-off ownership flips of `SalesRep1`/`SalesRep2`/`FinancialOwner` that aren't about geography - those columns follow different ownership rules.

## Right-sizing the output

Match the deliverable to the size of the change. The user usually wants the smallest thing that works:

| Number of providers | Deliverable |
|---|---|
| 1-3 | Just identify the correct rep(s) and tell the user. They will update manually in the admin UI. Do NOT generate a script. At most, offer a one-line UPDATE in the chat for them to paste if useful. |
| 4-25 | One short SQL block in the chat (BEGIN TRAN + UPDATE + verify + COMMIT/ROLLBACK). No standalone file unless asked. |
| 25+ or "a rep is leaving" | Full standalone .sql file with BEFORE/AFTER snapshots, VALUES driver, transaction wrap, validation queries. Hand off to data engineering. |

Default to the smaller option when in doubt. Generating a 400-row script for a 2-row change wastes everyone's time. Ask before producing a file if the user hasn't explicitly requested one.

## Key tables

| Table | Use |
|---|---|
| `HFDProd.dbo.ProviderRelationsReps` | Rep lookup. Columns: `AutoRepID`, `FirstName`, `LastName`, `Disabled`. Find a rep by name here. |
| `HFDProd.dbo.Providers` | Source of truth. The `RelationsRep` column is what you're updating. Also has `State`, `Zip` used to derive territory. |
| `Analytics.dw.TerritoryAssignment` | Grain: one row per `MatchValue` (`MatchType` is `'Zip'` or `'State'`) -> `Territory` name. 6,624 zip rows + 48 state rows. Use Zip first, fall back to State. |
| `Analytics.dw.ProviderAccountAssignment` | Enterprise/special-markets override. Check whether any target providers have entries (e.g. `AssignmentGroup='Excluded'` or `'SpecialMarkets'`); these may need separate handling. |

## Territory -> dominant rep (current as of 2026-05)

Re-derive whenever doing a real reassignment - new reps and turnover change the picture. The query is in the workflow below.

| Territory | AutoRepID | Rep |
|---|---|---|
| Desert Frontier | 20047 | Melissa Adams |
| Georgia Alabama | 20045 | Kathleen Phillips |
| Great Lakes | 20041 | Brian Quasebarth |
| Gulf Coast | 20049 | Dalton Gatewood |
| Mid Atlantic | 20042 | Maura Monti |
| North California | 20050 | CJ Marine |
| Northeast | 20043 | Pat Troy |
| South California | 20052 | Alayna Austin |
| South Central | 20044 | Gregg Givens |
| South Florida | 20029 | Gabriela Chacin |
| South Texas | 20046 | Jeremy Anderson |
| Southeast | 20025 | Scott Winslow |
| West | 20052 | Alayna Austin |

States with NO state-fallback row (zip-only): **CA, TX, FL.** A provider stamped `State='CA'` with a NULL or out-of-CA zip will not map.

## Workflow

1. **Resolve the source rep** to an `AutoRepID`. Use `WHERE FirstName LIKE '...' OR LastName LIKE '...'` against `ProviderRelationsReps`.
2. **Pull the source book** with `IsActive`, `Status`, `IsParentProvider`, `State`, `Zip` so you can sanity-check size and composition.
3. **Re-derive the territory -> dominant-rep mapping** (do not trust the cached table above for a real change):

   ```sql
   SELECT rc.Territory, rc.RelationsRep AS AutoRepID,
          prr.FirstName, prr.LastName, rc.Cnt AS CurrentAcctCnt
   FROM (
       SELECT m.Territory, m.RelationsRep, COUNT(*) AS Cnt,
              ROW_NUMBER() OVER (PARTITION BY m.Territory ORDER BY COUNT(*) DESC) AS rn
       FROM (
           SELECT ap.RelationsRep,
                  COALESCE(z.Territory, s.Territory) AS Territory
           FROM (
               SELECT p.RelationsRep, p.State,
                      LEFT(LTRIM(RTRIM(ISNULL(p.Zip,''))),5) AS Zip5
               FROM HFDProd.dbo.Providers p WITH(NOLOCK)
               WHERE p.RelationsRep IS NOT NULL
                 AND p.RelationsRep <> @SourceRepId
                 AND p.IsActive = 1
                 AND p.Status = 'CUR'
           ) ap
           LEFT JOIN Analytics.dw.TerritoryAssignment z WITH(NOLOCK)
                  ON z.MatchType='Zip'   AND z.MatchValue = ap.Zip5
           LEFT JOIN Analytics.dw.TerritoryAssignment s WITH(NOLOCK)
                  ON s.MatchType='State' AND s.MatchValue = ap.State
       ) m
       WHERE m.Territory IS NOT NULL
       GROUP BY m.Territory, m.RelationsRep
   ) rc
   JOIN HFDProd.dbo.ProviderRelationsReps prr WITH(NOLOCK) ON prr.AutoRepID = rc.RelationsRep
   WHERE rc.rn = 1
   ORDER BY rc.Territory;
   ```

4. **Compute the per-provider new rep** with zip-first, state-fallback. Embed the territory -> rep mapping as `(VALUES ...)` so the join stays in one self-contained query.
5. **Bucket the source book**: mapped vs unmapped. Investigate every unmapped row - they fall into three categories (next section).
6. **Generate the final UPDATE script** as a hard-coded `(ProviderID, NewRep)` VALUES list. Do not leave the live join against `TerritoryAssignment` in the production script; data engineering should be able to read every assignment.
7. **Validate** against `ProductionCopy` (read-only mirror of HFDProd) before handing off.

## Data quality categories for unmapped rows

When the zip/state join produces NULL, the row almost always falls into one of three buckets. Investigate before assuming "manual decision":

| Category | Symptom | Fix |
|---|---|---|
| A. Placeholder shells | NULL or blank Zip, generic name ("OrthoFi Placeholder", "RH Place Holder", "Petland OBS", "Test"). | Leave on source rep, NULL out, or assign by hand. Real practices are not in this bucket. |
| B. Wrong State | Valid Zip in another state, but `State` column is something else (typically the source rep's home state). | Use the zip's real state for the state-fallback. Add the row to the VALUES list with the rep for that territory. |
| C. CA/TX/FL zip typo | `State` matches but Zip is not in `TerritoryAssignment`. Compare to a sibling practice or look up the practice name - usually one digit off (e.g., 91655 vs 91355 Valencia, 92852 vs 92584 Menifee). | Treat as if the corrected zip applies; add to VALUES list. Optionally file a data-quality fix separately. |

**Sister-practice cross-check** is the cheapest way to confirm Category B/C: pull every record sharing the same `ParentProvider` or name pattern and compare states/reps. If 117 of 118 records say NV, the lone MS one is wrong.

## Production-ready script template

```sql
USE HFDProd;
GO

SET NOCOUNT ON;
SET XACT_ABORT ON;
BEGIN TRAN;

-- BEFORE snapshot
SELECT 'BEFORE' AS Phase, RelationsRep, COUNT(*) AS Cnt
FROM HFDProd.dbo.Providers WITH (NOLOCK)
WHERE RelationsRep = @SourceRepId
GROUP BY RelationsRep;

-- Driver
;WITH NewAssignment(ProviderID, NewRep) AS (
    SELECT * FROM (VALUES
        -- grouped by destination rep, with comments
        (12345, 20050),
        (12346, 20052)
        -- ...
    ) v(ProviderID, NewRep)
)
UPDATE p
   SET p.RelationsRep = na.NewRep
  FROM HFDProd.dbo.Providers p
  JOIN NewAssignment na ON na.ProviderID = p.ProviderID
 WHERE p.RelationsRep = @SourceRepId;

PRINT CONCAT('Rows reassigned: ', @@ROWCOUNT);

-- AFTER snapshot
SELECT 'AFTER' AS Phase, RelationsRep, COUNT(*) AS Cnt
FROM HFDProd.dbo.Providers WITH (NOLOCK)
WHERE RelationsRep = @SourceRepId
GROUP BY RelationsRep;

-- COMMIT TRAN;   -- uncomment after verifying counts
-- ROLLBACK TRAN;
```

Keep the script readable for DE: group VALUES rows by destination rep, comment each block with the territory and rep name, and document any zip/state corrections inline so the audit trail lives in the script.

## Validation (run against ProductionCopy before handoff)

```sql
-- 1. All driver ProviderIDs exist AND currently belong to the source rep
SELECT COUNT(*) AS MatchingAndOwnedBySource
FROM HFDProd.dbo.Providers p WITH(NOLOCK)
JOIN (VALUES (12345),(12346) /* full list */) v(ProviderID) ON v.ProviderID = p.ProviderID
WHERE p.RelationsRep = @SourceRepId;
-- Expect: count = number of rows in VALUES

-- 2. Nothing on the source rep is unaccounted for
SELECT COUNT(*) AS UnaccountedFor
FROM HFDProd.dbo.Providers p WITH(NOLOCK)
WHERE p.RelationsRep = @SourceRepId
  AND p.ProviderID NOT IN ( /* every ProviderID in the driver + intentionally-left list */ );
-- Expect: 0, OR the count of intentionally-skipped placeholders
```

## Common mistakes

- **Using `HFDProd_Finance` in the production script.** That's the linked DB name on `hfdsqlfinance.office.local`. The production DB on the actual app server is `HFDProd`. Always write `HFDProd.dbo.Providers` in the script.
- **Trusting `State` over `Zip`.** Across HFD, State='CA' is the literal default for newly-created provider records. Zip is more reliable for territory derivation; verify both when they disagree.
- **Forgetting CA/TX/FL have no state fallback.** A blank or out-of-state zip on a CA/TX/FL-stamped record will not map. Don't treat the resulting NULL as "no territory" - investigate.
- **Leaving the territory join in the production script.** Data engineering should see the exact (ProviderID, NewRep) pairs, not a query that re-derives them at runtime against a table that could change.
- **Skipping the `ProviderAccountAssignment` check.** Enterprise/SpecialMarkets overrides for a provider may mean the rep change has no downstream effect on reporting. Worth flagging when present.
- **Forgetting `WITH (NOLOCK)`** on every reference in read queries (mandatory per user preferences).
- **Pre-validating on `mssql2` only.** Always run the final SELECT validation on the `ProductionCopy` MCP connection because that's the actual HFDProd schema/data the script will run against.

## Related skills

- **`hfd-database`** - MCP connection guidance, naming, NOLOCK rules, DBUp repo layout. Required background.
- **`ssrs`** - Reassignments do not affect SSRS catalog, but reports filtered by rep may need a refresh after the cutover.
