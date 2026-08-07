# Non-ship gate

> Sibling gate: `dev-review`'s `close-out-gate.md` covers *ship-readiness* for a change; this file covers *bug-fix closure*. Shared skeleton by convention, different conditions by design — improvements to the shared shape propagate both ways.

The close-out conditions that block declaring a bug fix complete. Used by `pr-interrogate` (Quality Gates) and `triage-and-fix` (closeout).

## The five conditions

Do not close (or declare a fix complete) if any of these are true:

1. **Missing same-input differential proof.** Without `base fail / candidate pass` on the same payload, the fix isn't proven. (See `differential-proof.md`.)

2. **Unresolved critical assumptions remain.** Assumptions that must be true for the fix to work — feature flag state, route actually used in production, sample representativeness, backend behavior unchanged — must be either verified or named as confidence-reducing factors.

3. **Missing rootness classification.** Fix must be classified as `ROOT` / `PARTIAL_ROOT` / `SYMPTOM` per `rootness-classification.md`. "It works" without rootness is incomplete.

4. **High/critical risk missing code+test+runtime triplet evidence.** For high-risk changes, the proof must include all three:
   - **Code** — the change itself, reviewed and understood.
   - **Test** — at least one targeted test (or harness/scenario when test isn't feasible).
   - **Runtime** — observed behavior in a real (dev/staging/prod) environment, even briefly.
   
   Two-out-of-three (code + test, no runtime; or code + runtime, no test) leaves one of the most common failure modes unguarded.

5. **Required harness decisions unresolved.** When the fix needed temporary observability or a specific harness, decisions about whether to keep / remove / promote that instrumentation must be settled before close.

## Quality gates from `pr-interrogate`

The `pr-interrogate` mode adds:

- Exact failure signature captured.
- Exact scenario replayed on both refs.
- At least one user-visible flow walkthrough explained.
- Side-effect scan includes unchanged sibling call sites.
- Any data/observability gaps explicit.

## When close is denied

When a non-ship condition fires:

- State the specific condition.
- Name what would resolve it (the next verification step or the missing artifact).
- Report a conditional verdict (`NO-SHIP` for `pr-interrogate`; "needs further proof" for `triage-and-fix`).
- Do not silently weaken the standard.

## Used by

- `pr-interrogate` mode — Quality Gates step (10 of 10).
- `triage-and-fix` mode — closeout discipline.
- `recurring-hunt` mode — Fix Flow step 6 (commit only after green proof) and step 7 (challenger validation) implicitly enforce items 1-2.

## Malleability note

**Canonical:** the five conditions. Loosening any of them is what causes "fix shipped, bug came back" outcomes.

**Adaptable:** how strictly the high-risk triplet rule applies — for low-risk changes, code + test (without runtime) may be sufficient. Use risk level as the calibration.

