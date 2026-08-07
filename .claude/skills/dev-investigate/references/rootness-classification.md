# Rootness classification

The canonical taxonomy for classifying a bug fix as ROOT / PARTIAL ROOT / SYMPTOM. Used by `pr-interrogate` and `triage-and-fix` modes.

## The three classifications

### ROOT

A `ROOT` fix:

1. **Blocks bad state at ingress** and before high-impact mutations.
2. **Prevents downstream cascades** without relying on luck or timing.
3. **Preserves valid paths** and user-visible behavior (no collateral damage).

### PARTIAL ROOT

A `PARTIAL ROOT` fix addresses the root cause for the reported scenario but leaves adjacent paths exposed. Common patterns:

- Catches the bad state at one ingress but not all known ingress points.
- Prevents the cascade in the dominant flow but not edge-case flows.
- Adds a guard that the team knows is incomplete pending a follow-up.

When a fix is `PARTIAL ROOT`, it MUST come with:
- A named follow-up (use the `dev-scope-deferral` skill to capture).
- Explicit naming of the unaddressed paths.
- Confidence reduction in the verdict.

### SYMPTOM

A `SYMPTOM` fix indicators:

1. **Only catches one endpoint** while the same bad state can still flow elsewhere.
2. **Depends on a single UI path** while alternate paths remain unguarded.
3. **Hides errors** without preventing invalid operations.

`SYMPTOM` fixes are sometimes the right answer (e.g., shipping a containment patch under deadline pressure with a follow-up planned). They are NOT the same as a `ROOT` fix and should never be reported as one.

## How to classify

When interrogating a fix, ask in order:

1. **Does the fix block bad state at the source, or at a downstream consumer?**
   - At the source → likely ROOT or PARTIAL ROOT.
   - At a downstream consumer → likely SYMPTOM.

2. **If bad state could still arrive via a different path, would the fix catch it?**
   - Yes → ROOT.
   - No, only the tested path is guarded → SYMPTOM or PARTIAL ROOT depending on how many paths exist.

3. **Does the fix rely on luck, timing, or a specific UI flow being used?**
   - Yes → SYMPTOM (the guard isn't structural).

4. **Does the fix preserve all valid paths and user-visible behavior?**
   - Yes → strengthens ROOT classification.
   - No → reduces confidence; potential collateral damage.

## Used by

- `pr-interrogate` mode — verdict step (Verdict × Classification × Confidence).
- `triage-and-fix` mode — fix-shape selection (root fix vs. partial root fix vs. symptom containment).
- `non-ship-gate.md` — closing without rootness classification is a non-ship condition.

## Malleability note

**Canonical:** the three-state classification (ROOT / PARTIAL ROOT / SYMPTOM) and the criteria above. Renaming or collapsing creates incompatibility across modes.

**Adaptable:** how the classification is rendered in different contexts. PR-interrogate verdicts use it as one axis of the triple-axis verdict (Verdict × Classification × Confidence); root-cause case systems use it as a stage-gate condition.

