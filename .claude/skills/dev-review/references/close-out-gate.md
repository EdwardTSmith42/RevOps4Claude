# Close-out gate

The 6-item ship gate for `ship-gate` mode (and used by other modes for close-out validation). Aligned with investigate cluster's `non-ship-gate.md` but specifically for ship-readiness rather than bug-fix root-cause closure.

## The 6 conditions

Do not declare ship-ready (or close out a `ship-gate` run) if any of these are true:

### 1. Any `Blocking` crash/deploy risks remain

`S0` (ship-stopping) or unmitigated `S1` (high-severity) findings classified as `Blocking` per `ship-no-ship-vocabulary.md`. If any remain, the verdict is NO-SHIP.

### 2. Any unresolved high-severity review thread is ignored without explicit rationale

If a reviewer (human or autonomous review agents via challenger lanes) raised a high-severity concern that hasn't been addressed, ignoring it requires explicit rationale. "We disagree because <reason>" is acceptable; silent skip is not.

### 3. Every fixed blocker has a real failing test that now passes

Per `reliability-rubric.md`'s test-first fix loop:
- Failing test was written first.
- Test was confirmed to fail before fix.
- Fix was implemented.
- Test now passes.
- Nearby regression tests run.

If any blocker fix lacks failing-then-passing proof, this gate fails.

### 4. Rollback path is clear for deploy-facing changes

For changes that affect deploy (env vars, migrations, infrastructure config, breaking API changes):
- Rollback procedure is documented (often in the brief's "Rollout / Rollback" section).
- Rollback was considered in the design (the change can be reversed without manual recovery).

If deploy-facing AND rollback path is unclear, this gate fails.

### 5. All four PR-diff risk questions are answered with changed-file evidence

Per `diff-risk-questions.md`: all 4 mandatory questions are answered with diff evidence (file paths + line references). Even when a question doesn't apply, the answer is "not applicable + reason" — not silently skipped.

### 6. Any `PARK` or `REVERT` call is explicit and justified

If findings include PARK or REVERT decisions:
- PARK items are captured via `dev-scope-deferral` skill (with executable verification idea).
- REVERT items have explicit rationale ("can't be hardened in scope because <reason>").
- Neither is silently left in limbo.

## When close is denied

When a gate condition fires:

- State the specific condition.
- Name what would resolve it (next verification step or missing artifact).
- Report a conditional verdict (`NO-SHIP` or "needs further proof").
- Do not silently weaken the standard.

## Used by

- `ship-gate` mode (the final gate before verdict)
- `checkpoint` mode (closing the milestone — not all items apply, but #1 / #5 / #6 carry over)

## Malleability note

**Canonical:** the 6 conditions. Loosening any of them is what causes "shipped, then immediate hotfix needed" outcomes.

**Adaptable:** the specifics of "deploy-facing" change detection — repo-by-repo conventions vary (some use `infra/` directories, some use `migrations/`, some have explicit deploy configs). The principle (rollback path clear for deploy-facing changes) is canonical; what counts as "deploy-facing" adapts.

