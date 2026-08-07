# Checkpoint report template

Strict template for `checkpoint` mode output.

```markdown
# Milestone Checkpoint Report — <branch / scope>

## Milestone Commit
- Hash: <sha>
- Message: <conventional commit message>
- Scope: <work_type> / <risk_level>

## Smoke Test 1
- Command: <command>
- Result: PASS | FAIL
- Key output: <relevant excerpt>

## Regression Findings (severity-ranked)

### P0/P1 (behavior regressions, data-loss risks)
- File:line — Finding — Evidence

### P2 (likely future bugs)
- ...

### P3 (cleanup opportunities — only if plausibly hide defects)
- ...

## Monolith Sweep
- Oversized files in changed surface:
  - <file>:<lines>
  - ...
- Decomposition decisions:
  - <file>: <decompose now / defer / no-op> — <reason>

## Cleanup Audit
- Obsolete shims/patterns removed:
  - ...
- Intentionally retained wrappers (with reason + cleanup trigger):
  - ...
- Deferred cleanup (via `dev-scope-deferral`):
  - ...

## Tests Added/Updated
- <file>: <what was added and why>
- ...

## Smoke Test 2
- Command: <command>
- Result: PASS | FAIL
- Delta vs gate 1: <unchanged | improved | regression>

## Residual Risk / Deferred Follow-ups
- <item> — <reason for deferral> — captured via scope-deferral at <note path>
- ...
```

## Notes

- Both smoke gates (1 and 2) are required.
- If smoke fails or P0/P1 findings remain, stop the loop and fix forward.
- Don't decompose high-blast files without explicit user approval.

## Used by

- `checkpoint` mode of `dev-review`.
