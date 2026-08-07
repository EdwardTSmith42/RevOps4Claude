# Monolith decomposition playbook

Used by `checkpoint` mode (steps 5-6) when oversized files surface during the milestone sweep.

## When to use

When the monolith sweep produces oversized files in the changed surface, AND the user has approved decomposition (high-blast files require explicit approval).

## Candidate selection

1. **Prefer files touched in the current milestone range** (`git diff --name-only <base>...HEAD`).
2. **Defer high-blast files** unless the user explicitly approves.
3. **Prioritize files with clear seams:**
   - Mixed concerns (UI + data + transport in one file)
   - Repeated utility logic that can move to helper modules
   - Large conditional blocks that map cleanly to submodules

## Test-first guardrail

Before splitting a file:

1. **Identify invariants** that must stay true.
2. **Add/extend tests** that fail if behavior wiring breaks.
3. **Run those tests before refactor** to capture baseline.
4. **Add one focused integration test lane** at the real boundary (for DB-heavy code: live Postgres URL) to catch schema/runtime realities that mocks miss.

## Split strategy

1. **Extract pure helpers first** (no side effects).
2. **Extract isolated state/transport adapters next.**
3. **Keep public API shape unchanged** while splitting internals.
4. **Update imports incrementally** and keep commits scoped.

## Post-split cleanup audit

After the extracted modules are green, **explicitly audit and remove transitional scaffolding**:

1. Search for **pass-through barrels** and **compatibility facades** that only preserve old file layout.
2. **Delete wrappers that have no independent runtime behavior.**
3. Replace **monolith-root stdlib/network re-exports** with direct imports in leaf modules.
4. **Rewrite shim-specific tests** so they assert real module behavior/importability rather than preserving a temporary shim forever.
5. **Harden temporary easy mocks back to the live boundary shape:**
   - DB or repository fixtures should match actual query output, not normalized convenience rows.
   - Direct FastAPI route tests should pass behavior-relevant `Query(...)` defaults explicitly.
6. **Rebuild or revalidate generated assets** if they embed old import/query patterns.
7. **If any wrapper must remain, document the exact reason, remaining consumers, and cleanup trigger.**

## Verification after split

1. Re-run targeted tests for extracted modules.
2. Re-run smoke tests for end-to-end wiring.
3. Re-run the monolith sweep and confirm candidate count drops or rationale for deferral is documented.
4. **Re-run key target tests in isolated-process mode** (single file) as well as grouped mode to expose import-order/circular dependency issues.
5. **For integration lanes against long-lived local DBs**, guard for sequence drift and high-row-density list queries so tests stay deterministic.
6. **Re-run the same targeted tests after cleanup deletions**, not just after the initial extraction.
7. **Re-run any tests that were temporarily simplified during extraction** after replacing those mocks with live boundary shapes.

## Exit criteria

Do not consider decomposition complete until all of the following are true:

1. The extracted modules and their real call sites are green.
2. Obsolete pass-through barrels and no-behavior compatibility facades are deleted or explicitly deferred.
3. No new code is being taught to import unrelated helpers through the old monolith module.
4. Any intentionally retained wrapper has a documented reason and a future cleanup trigger.

## Suggested line thresholds

- TypeScript / JavaScript: 500
- Python / Ruby: 400
- Go / Rust / Swift: 500
- Java / Kotlin: 600
- C / C++ headers and sources: 700

These are starting heuristics; adjust per repo conventions. The principle is: a file that's "too big to reason about as one unit" deserves a sweep regardless of exact line count.

## Used by

- `checkpoint` mode of `dev-review` (steps 5-6 — monolith sweep + post-decomposition cleanup audit)

## Malleability note

**Canonical:** the test-first guardrail (add tests before splitting; capture baseline) and the post-split cleanup audit's anti-mock-rot rules (DB row fixtures matching real query output; FastAPI `Query(...)` defaults passed explicitly). These are war-story-derived patterns.

**Adaptable:** the line thresholds — they're starting heuristics. Repo conventions can override.

