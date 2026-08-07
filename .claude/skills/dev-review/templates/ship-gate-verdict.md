# Ship-gate verdict template

Strict template for `ship-gate` mode output. Use this exact structure.

```markdown
## Scope Selection
- Scope: <commit | commit_range | branch_slice | branch | pr> @ <ref or PR number>
- Baseline: <baseline ref>
- Pinned commit SHAs: <head> ... <base>

## PR-Diff Risk Questions

**Q1 unintended consequences:** <answer + changed-file evidence, OR "not applicable: <reason>">

**Q2 perf/memory/race:** <answer + changed-file evidence, OR "not applicable: <reason>">

**Q3 overengineering judgment:** <answer + rationale grounded in diff size/complexity>

**Q4 park-or-revert decision:** Ship now / Park with investigation (via `dev-scope-deferral`) / Revert risky slice + reason

## Worst-Case Failure Modes
- [Severity] Mode, trigger, blast radius, evidence

## Crash/Deploy Risk List
- [Blocking | Non-blocking] Risk, affected runtime, evidence, mitigation

## Missing Test Coverage Map
- Changed behavior area → missing unit/integration/e2e coverage
- Edge cases not covered (race, null, stale data, retries, timeout)

## Findings (severity-ranked)

### S0 (Blockers)
- File:line — Trigger condition — User/system impact — Why diff introduces or fails to prevent

### S1 (High)
- ...

### S2 (Medium)
- ...

### S3 (Low)
- ...

## PARK / REVERT Decisions
- PARK: <issue> — <reason> — captured via scope-deferral skill at <note path>
- REVERT: <slice> — <reason — can't be hardened in scope>

## Ship/No-Ship Gates
- [PASS/FAIL] No `Blocking` crash/deploy risks remain
- [PASS/FAIL] No unresolved high-severity review thread ignored without rationale
- [PASS/FAIL] Every fixed blocker has a real failing test that now passes
- [PASS/FAIL] Rollback path is clear for deploy-facing changes
- [PASS/FAIL] All four PR-diff risk questions answered with changed-file evidence
- [PASS/FAIL] Any PARK or REVERT call is explicit and justified

## Final Verdict
**SHIP** | **SHIP WITH CONDITIONS** | **NO-SHIP**

(For NO-SHIP) Minimum fixes required to flip NO-SHIP → SHIP:
- ...

(For SHIP WITH CONDITIONS) Conditions:
- ...
```

## Notes

- Default user-attribution wording for error-reporting-derived impact: `Affected Users: unknown (not tracked)` unless tracking is confirmed.
- Plain file paths for local artifacts; clickable URLs for web resources.

## Used by

- `ship-gate` mode of `dev-review`.
