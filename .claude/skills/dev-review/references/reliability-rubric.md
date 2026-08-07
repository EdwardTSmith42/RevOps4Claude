# Reliability rubric

Severity scale, failure-mode prompts, crash/deploy checklist, coverage map, test-first fix loop, ship-gate heuristic, and PARK/REVERT rule for `ship-gate` mode (and used by other modes for consistent severity language).

## Baseline rule

- Compare branch diff against `origin/develop` by default.
- If the PR base is another branch (PR-to-PR), compare against `origin/<baseRefName>`.
- Still fetch and attempt to merge latest `origin/develop` before remediation work.
- If conflicts appear during merge, **stop and ask the user how to proceed.**

## PR-diff scope contract

- **Evaluate only changed files and the immediate call-sites needed to prove impact.**
- Do not expand into unrelated legacy debt during release-readiness.
- If a concern is real but outside changed behavior, mark it `PARKED (OUT OF SCOPE)`.

## Severity scale

- **`S0` Blocker** — Ship-stopping risk. Likely crash, boot failure, data corruption, or security impact.
- **`S1` High** — Major reliability regression with realistic trigger and high user impact.
- **`S2` Medium** — Recoverable defect or edge-case failure with bounded blast radius.
- **`S3` Low** — Minor inconsistency or maintainability risk, usually non-blocking.

## Failure-mode prompts

For each changed behavior, ask:

1. What is the worst runtime outcome if this assumption is wrong?
2. Can this path throw or deadlock under null/empty/timeout/race conditions?
3. Can stale/out-of-order events regress state?
4. Can this break deploy/startup, migrations, or environment boot?
5. Is there a silent data-loss or data-corruption mode?

## Crash/deploy risk checklist

- Null or undefined dereference in new paths.
- Changed env var names, required config, or strict parsing.
- Docker/build context mismatch (copied paths, target stage, startup command).
- Startup assumptions that differ between local/dev/prod.
- Migration ordering or backward compatibility break.

## Coverage map checklist

Map each risk area to missing tests:

- **Unit coverage** for core branching logic and edge conditions.
- **Integration coverage** for service boundaries and API contracts.
- **E2E coverage** for user-visible reliability regressions.
- **Regression tests** for each previously failing scenario.

## Test-first fix loop

For each blocking issue:

1. Write a realistic failing test that reproduces the observed defect.
2. Run only that test first and capture proof it fails.
3. Implement minimal robust fix.
4. Re-run the same test and confirm pass.
5. Run nearby regression tests to protect adjacent behavior.

**Never skip the failing-test proof step.** Don't write placeholder tests.

## Ship gate heuristic

- Return **`NO-SHIP`** when any `S0` exists OR unresolved `S1` lacks mitigation.
- Return **`SHIP WITH CONDITIONS`** when only `S2/S3` remain with explicit follow-ups (each follow-up should be captured via `dev-scope-deferral` skill).
- Return **`SHIP`** when no unresolved blocker/high risk remains and coverage is adequate for changed behavior.

## User-impact wording

For error-reporting-derived impact lines: cross-reference `../../dev-investigate/references/user-attribution-rule.md`.
- Default `Affected Users: unknown (not tracked)` unless attribution is explicitly confirmed.
- When showing raw `userCount`, label as `attributed users` unless tracking confirmed.

## PARK vs REVERT rule

- **`PARK`** — keep PR scope; defer non-critical or out-of-scope risks to a follow-up investigation. Invoke `dev-scope-deferral` skill to capture the deferred item.
- **`REVERT`** — remove changed code when risk is high and cannot be safely mitigated in current scope.

PARK and REVERT are explicit decisions; never silently leave a finding unaddressed.

## Used by

- `ship-gate` mode (severity classification + failure-mode prompts + ship gate heuristic)
- `checkpoint` mode (for severity language during regression review)
- `digest` mode (per-PR severity classification)
- `manifesto-review` mode (when recommendations need severity-anchored prioritization)

## Malleability note

**Canonical:** the four-level severity scale (S0/S1/S2/S3) and the ship gate heuristic. These map to ship/no-ship decisions and shouldn't drift across modes.

**Adaptable:** the failure-mode prompts and crash/deploy checklist — these are starting points. New patterns surfaced through real-use should be added (or surfaced via `dev-self-improvement-loop` skill).

