# Disciplined bug arc

The 6-step skeleton for full root-cause bug work. It is the compact checklist used by `evidence` and `pr-interrogate`; investigations that need a fully structured case route through `dev-delivery-ops`.

## The six steps

1. **Initialize the bug case.** Capture: bug statement, work_type (always `bug` for this arc), risk-level, time bounds, environment scope, investigation constraints.

2. **Collect evidence and map the failure chain.** Follow the four evidence lanes (`evidence-lanes.md`) and build the failure chain in code (`pr-interrogate` mode's step 2). Outputs: lane status matrix, chain-as-executable-logic.

3. **Validate atomic hypotheses.** Apply `atomic-hypothesis-method.md` — disconfirming-first. Outputs: four-bucket result (Observed facts / Hypotheses with confidence / Ruled out / Unknowns).

4. **Implement and verify with differential proof.** Per `differential-proof.md` — base fail / candidate pass on same payload. Outputs: pass/fail matrix, log artifacts.

5. **Run blast-radius and regression checks.** Use `blast-radius-taxonomy.md` for likely-now / possible-watch / unknown-needs-simulation. Confirm sibling call sites haven't regressed.

6. **Close with rootness + resolution classification.** Apply `rootness-classification.md` — ROOT / PARTIAL_ROOT / SYMPTOM. Apply `non-ship-gate.md` to confirm close conditions are met. If close is denied, route to a follow-up (often via `dev-scope-deferral`).

## When to use this arc as a checklist

- High-risk or high-impact bugs where structured discipline matters.
- Bugs that need a developer handoff package (use with `evidence` mode).
- PRs being interrogated for ship-readiness (use with `pr-interrogate` mode — step 6 maps to the verdict).

For low-risk bugs (typo fix, simple regression with obvious repro), the arc is overkill — `triage-and-fix` mode picks the smallest credible repro boundary.

## Code+test+runtime triplet

For high-risk steps, the proof should include all three:

- **Code** — the change itself, reviewed and understood.
- **Test** — at least one targeted test (or harness when test isn't feasible).
- **Runtime** — observed behavior in dev/staging/prod, even briefly.

Two-out-of-three leaves common failure modes unguarded. See `non-ship-gate.md`.

## Used by

- `evidence` mode — soft gate at the close of a full investigation.
- `pr-interrogate` mode — the step-6 close (rootness + non-ship-gate).
- `triage-and-fix` mode — when the fix lane is `structured bug-ops case`, this arc shapes the workflow.

## Malleability note

**Canonical:** the six steps and their sequencing. Each step's output gates the next; reordering breaks the verification chain.

**Adaptable:** how heavily each step is run depends on risk. Low-risk bugs may compress steps 1+2 into a one-paragraph statement and skip step 5. High-risk bugs run every step explicitly.
