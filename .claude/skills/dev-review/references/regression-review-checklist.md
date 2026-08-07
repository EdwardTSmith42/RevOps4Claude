# Regression review checklist

Used by `checkpoint` mode (step 4) to inspect the milestone progress commit for behavior regressions and other risks.

## When to use

After creating the milestone progress commit. Before continuing to monolith decomposition.

## 1. Scope and baseline

- Capture commit hash: `git rev-parse --short HEAD`
- Capture range against base branch: `git diff --stat origin/develop...HEAD`
- Build review surface: `git show --stat --name-only HEAD` and `git diff <base>...HEAD`

## 2. Behavior-risk review (manual)

For each changed file, evaluate:

- **Logic regressions** — changed conditions, default values, null handling, error paths.
- **Data-shape drift** — renamed fields, schema mismatches, optional vs required values.
- **Concurrency / timing** — async fan-out, retries, timeout handling, race-prone shared state.
- **Error handling** — swallowed exceptions, broad catches, missing failure signals.
- **Duplicate / stale code** — copied logic, dead branches, commented-out old code.

## 3. Fast static checks

- Run scoped lint/type checks where available.
- Run targeted tests for changed modules.
- If `jscpd` is available, run duplication check on changed files.

## 4. Findings bar

- **`P0/P1`** — behavior regressions and data-loss risks. Stop the loop and fix forward.
- **`P2`** — maintainability issues that are likely future bugs. Note for follow-up.
- **`P3`** — cleanup opportunities. Note only if they plausibly hide defects.

## 5. Gate decision

- **Stop the loop and fix forward** when smoke fails or `P0/P1` findings remain.
- **Continue to monolith decomposition** only after high-severity findings are resolved or explicitly deferred (via `dev-scope-deferral`).

## Used by

- `checkpoint` mode of `dev-review` (step 4 — regression review of milestone commit)

## Malleability note

**Canonical:** the 5 review categories (logic / data-shape / concurrency-timing / error handling / duplicate-stale) and the gate decision (stop on smoke fail or P0/P1).

**Adaptable:** the specific tools (jscpd, lint, type) — repo-specific. Any tool that surfaces the same risks substitutes cleanly.

