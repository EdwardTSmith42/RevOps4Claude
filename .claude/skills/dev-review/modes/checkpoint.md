# Mode: checkpoint

Part of the `dev-review` skill. Selected when the user wants a milestone checkpoint loop — phrasings like "Run the milestone review," "Smoke + regression sweep," "Decompose this monolithic file safely," "Coding-milestone checkpoint."

## Job

Repeatable coding-milestone checkpoint: local progress commit → smoke gate 1 → regression review → monolith sweep + decompose safely → cleanup audit → smoke gate 2. Keeps progress traceable and prevents regressions between coding steps.

## Scope adaptation

`checkpoint` works at commit / branch-slice / PR scope. Default is current branch against `origin/develop`. Per `../references/scope-adapter.md`: large changes may warrant sub-agent fanout for the regression-review step (especially when monolith sweep produces many candidates).

## Run

### 1. Classify scope and risk

- Set `work_type` (`bug | polish | feature`) and `risk_level` (`low | medium | high`) up front.
- Capture base branch for comparison (default `origin/develop`).

### 2. Create a local progress commit

```bash
git status --short
git add -A   # OR stage explicit files for tighter commits
git commit -m "chore(progress): checkpoint <scope>"
git rev-parse --short HEAD  # record hash
```

(Conventional commit format preferred. Keep the commit local unless the user asks to push.)

### 3. Run smoke test gate 1

- Detect the smoke command for this repo:
  - Check `package.json` scripts for `smoke`, `test:smoke`, `e2e:smoke`.
  - Check `Makefile` for smoke targets.
  - Check `scripts/smoke.sh` or similar conventions.
  - Fall back to: smallest meaningful end-to-end check (build + boot + key request).
- If smoke fails, **stop and fix before continuing.** Don't proceed past gate 1.

### 4. Run regression review of the milestone commit

See `../references/regression-review-checklist.md`. Inspect commit and diff surface:

```bash
git show --stat --name-only HEAD
git diff --stat <base-ref>...HEAD
```

Review for:
- **Logic regressions:** changed conditions, default values, null handling, error paths.
- **Data-shape drift:** renamed fields, schema mismatches, optional vs required values.
- **Concurrency/timing:** async fan-out, retries, timeout handling, race-prone shared state.
- **Error handling:** swallowed exceptions, broad catches, missing failure signals.
- **Duplicate/stale code:** copied logic, dead branches, commented-out old code.

Run scoped lint/type checks where available. Run targeted tests for changed modules.

Findings bar:
- Flag `P0/P1` for behavior regressions and data-loss risks.
- Flag `P2` for maintainability issues that are likely future bugs.
- Flag `P3` for cleanup opportunities.

**Stop the loop and fix forward when smoke fails or `P0/P1` findings remain.** Continue to monolith decomposition only after high-severity findings are resolved or explicitly deferred.

### 5. Run monolith sweep and decompose safely

See `../references/decomposition-playbook.md`.

- **Find oversized files** (touched in current milestone range):
  ```bash
  git diff --name-only <base>...HEAD | xargs -I{} sh -c 'lines=$(wc -l < "{}"); [ $lines -gt 500 ] && echo "$lines {}"' | sort -rn
  ```
  Suggested line thresholds: TypeScript/JavaScript 500 / Python/Ruby 400 / Go/Rust/Swift 500 / Java/Kotlin 600 / C/C++ 700.
- **Pick low/medium-blast candidates first.** Defer high-blast files unless the user explicitly approves.
- **Test-first guardrail:**
  1. Identify invariants that must stay true.
  2. Add/extend tests that fail if behavior wiring breaks.
  3. Run those tests before refactor to capture baseline.
  4. Add one focused integration test lane at the real boundary (DB-heavy code: live Postgres URL).
- **Split strategy:** extract pure helpers first → isolated state/transport adapters → keep public API shape unchanged while splitting internals → update imports incrementally.

### 6. Run post-decomposition cleanup audit

After extracted modules are green:

- Search for and remove transitional scaffolding:
  - **Pass-through barrels** with no independent runtime behavior.
  - **Compatibility facades** that only preserve old file layout.
  - **Monolith-style stdlib/network re-exports** in leaf modules.
  - **Shim-only tests** that lock in transitional structure.
- Search for and harden temporary easy mocks back to live boundary shape:
  - **DB row fixtures** using normalized or derived fields the real repository does not return.
  - **Direct FastAPI route tests** that rely on `Query(...)` marker defaults instead of explicit values.
- **Rebuild or revalidate generated assets** if they embed old import/query patterns.
- **Remove obsolete files/patterns** once the split is verified.
- **Re-run targeted tests** after cleanup edits before the final smoke gate.
- If any wrapper must remain, document the exact reason, remaining consumers, and cleanup trigger.

### 7. Run smoke test gate 2

- Re-run the same smoke command used in gate 1.
- Run targeted tests for decomposed modules.
- Confirm no regressions before declaring milestone complete.

Both gates (1 and 2) are required: gate 1 anchors what was working; gate 2 confirms no regression after milestone work.

## Output

See `../templates/checkpoint-report.md`. Required structure:

- `Milestone Commit`: hash + message + scope
- `Smoke Test 1`: command + pass/fail + key output
- `Regression Findings`: severity-ranked findings with file/line evidence
- `Monolith Sweep`: oversized-file list + decomposition decisions
- `Cleanup Audit`: obsolete shims/patterns removed, intentionally retained wrappers, deferred cleanup
- `Tests Added/Updated`: what was added and why
- `Smoke Test 2`: command + pass/fail + delta vs gate 1
- `Residual Risk / Deferred Follow-ups`: explicitly list any deferrals (invoke `dev-scope-deferral` for valid follow-ups)

## Constraints

- **Keep the progress commit local** unless the user asks to push.
- **Do not merge from this workflow.**
- **Do not decompose high-blast files without explicit user approval.**
- **Prefer minimal scoped edits over architecture churn.**
- **Two smoke gates are required.** "Smoke passed" is ambiguous without before-AND-after.

## Mode-specific references

- `../references/regression-review-checklist.md` (required for step 4)
- `../references/decomposition-playbook.md` (required for steps 5-6)
- `../references/scope-adapter.md` (fanout for large monolith candidates)
- `../templates/checkpoint-report.md`

## Design Rationale

Mode-specific notes:

- **Two smoke gates (before AND after)** — gate 1 anchors what was working before milestone work; gate 2 confirms no regression after decomp/cleanup. Without both, "smoke passed" is ambiguous.
- **"Add tests that protect current wiring and behavior BEFORE decomposing"** — tests-first-for-refactor. Same principle as differential-proof's "capture proof harness before changing code."
- **"Harden temporary easy mocks back to the live boundary shape"** — anti-mock-rot rule. Aligns with the user's mock-hardening preference in their operating principles (`AGENTS.md`).
- **DB row fixtures using normalized/derived fields the real repo doesn't return** — specific war-story pattern. Lift verbatim.
- **Direct FastAPI route tests using `Query(...)` marker defaults** — specific war-story. Lift verbatim.
- **"Pick low/medium-blast candidates first"** — graduated risk discipline.

