# Differential proof

The "base fail / candidate pass" discipline for proving a bug fix actually fixes the bug. Used by `pr-interrogate` and `triage-and-fix` modes.

## The four-item bar

Never declare a fix valid without before/after proof. Minimum bar:

1. **Repro on base branch** (`main` or PR base) **fails with the expected signature.**
2. **Same payload/steps on candidate branch passes.**
3. **Evidence artifacts are linked or path-referenced.**
4. **Root-cause chain is explicit** from source of bad state to observed failure.

If any item is missing, the verdict must be conditional or `NO-SHIP`.

## The hash-matching discipline

When running the same scenario on base and candidate refs, **use the same test payload hash or scenario hash** between runs. Without explicit hash matching, "we ran the same test" silently becomes "we ran a similar test" — and similar tests don't constitute differential proof.

Where a true hash isn't available, lock and document the inputs explicitly:
- Payload / fixture file path or contents.
- Test command (verbatim).
- Environment (when relevant).
- Random seed (when randomness is involved).

## Pass/fail matrix

Required artifact for differential proof:

| Ref | Result | Log tail (or path) |
|---|---|---|
| `base` (origin/main or PR base) | fail with expected signature | path/to/log |
| `candidate` (PR head) | pass | path/to/log |

## When differential proof isn't possible

Some bugs can't be reproduced deterministically (race conditions, timing-sensitive failures, rare state combinations). For these:

- **Capture the proof harness or scenario before changing code.** Even if the harness can't reliably reproduce the failure, having the harness lets later runs verify the fix.
- **Document the non-determinism explicitly** in the verdict. Confidence drops accordingly.
- **Consider an invariant gate or local observability loop** as the proof — see `lane-selector.md` for proof-style alternatives.

## Used by

- `pr-interrogate` mode — defines the evidence standard.
- `triage-and-fix` mode — proof-shape selection.
- `recurring-hunt` mode's Fix Flow — when fixing in-loop, prefer test-driven (proof first).

## Malleability note

**Canonical:** the four-item bar (base fail / candidate pass / artifacts / root-cause chain). Skipping any item makes the proof not differential.

**Adaptable:** the form the proof takes — automated test, manual scenario, harness, observability snapshot. The four items must be true; how they're produced is flexible.

