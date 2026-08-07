# Ship / no-ship vocabulary

Canonical verdict labels for `ship-gate` and disposition labels for findings. Pick from this fixed list — the discipline of choosing forces clarity.

## Verdict labels (the final decision for a ship-gate run)

- **`SHIP`** — no unresolved blocker/high risk; coverage adequate for changed behavior; ready to merge.
- **`SHIP WITH CONDITIONS`** — only `S2/S3` findings remain with explicit follow-ups; each follow-up captured via `dev-scope-deferral` skill. The conditions are the follow-ups, named explicitly.
- **`NO-SHIP`** — any `S0` exists OR unresolved `S1` lacks mitigation. Minimum fixes required to flip NO-SHIP to SHIP must be listed.

## Finding disposition labels

For each finding produced during analysis:

- **`Blocking`** — must fix before ship. Drives the SHIP / NO-SHIP verdict.
- **`Non-blocking`** — safe with follow-up issue. Counts toward "SHIP WITH CONDITIONS" if any are present.
- **`PARK`** — real concern but **not introduced or touched by this change**. Out of scope for this ship; defer to a separate investigation. Invoke `dev-scope-deferral` skill to capture.
- **`REVERT`** — unacceptably high risk; **cannot be safely hardened in current scope**. The risky slice should be removed from the change.

PARK and REVERT are explicit decisions; never silently leave a finding unaddressed.

## How verdicts compose with dispositions

| Findings | Verdict |
|---|---|
| Any `Blocking` (S0 or unresolved S1) | NO-SHIP |
| All `Blocking` resolved + remaining `Non-blocking` | SHIP WITH CONDITIONS |
| All `Blocking` resolved + no remaining `Non-blocking` | SHIP |
| Any `REVERT` decision | NO-SHIP for the reverted slice; remaining SHIP/SHIP WITH CONDITIONS for the rest |
| Any `PARK` decision | doesn't change verdict (parks are out of scope) but each PARK item gets a `dev-scope-deferral` note |

## When to use each

- **PARK vs Non-blocking:** Non-blocking = real issue introduced by this change but not severe enough to block. PARK = real issue NOT introduced by this change; surfaced during review but out of scope.
- **REVERT vs Blocking:** Blocking = must fix before ship. REVERT = can't be fixed in current scope; remove the risky slice instead.

## Used by

- `ship-gate` mode (primary consumer — verdict + finding dispositions)
- `digest` mode (uses `ready today: yes/no` shorthand mapping to SHIP / SHIP WITH CONDITIONS / NO-SHIP)
- Any check mode that produces a ship-readiness assessment

## Malleability note

**Canonical:** the four finding dispositions (Blocking / Non-blocking / PARK / REVERT) and the three verdicts (SHIP / SHIP WITH CONDITIONS / NO-SHIP). Adding states or aliasing labels causes drift.

**Adaptable:** the *threshold* for what counts as `S0` / `S1` / `S2` / `S3` (see `reliability-rubric.md`); the verdict logic stays fixed.

