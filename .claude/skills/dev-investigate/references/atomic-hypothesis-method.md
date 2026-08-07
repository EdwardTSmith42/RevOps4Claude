# Atomic hypothesis method

The disciplined practice of building hypotheses one assumption at a time, validating each independently, and reporting findings as separate buckets of facts / hypotheses / ruled-out / unknowns.

## The four buckets

Every investigation maintains an **assumptions ledger** with four buckets, populated as evidence accumulates:

- **Observed facts** — direct evidence only. Things you can point to in logs, traces, screenshots, or code.
- **Hypotheses** — possible explanations. Each carries a confidence rating: `low` / `medium` / `high`.
- **Ruled out** — scenarios contradicted by specific evidence. Always include the *clue* that rules them out.
- **Unknowns** — what still cannot be verified. Surface these explicitly rather than letting them stay implicit.

## Core moves

1. **Build atomic hypotheses, not one giant theory.** Decompose the problem into the smallest assumptions that can be independently tested.
2. **Define disconfirming checks before collecting evidence.** What evidence would *rule out* this hypothesis? Write that down first; collecting only confirming evidence is confirmation bias.
3. **Validate one assumption at a time.** Don't try to confirm three hypotheses with one observation; observations that fit multiple stories are weak evidence.
4. **Explicitly note contradictory evidence and weaken/retire hypotheses accordingly.** The *retire* move is what separates honest investigation from confirmation bias.
5. **Include "What this cannot be"** in the output, populated from the *Ruled out* bucket. This forces explicit assumptions and lets future investigators avoid re-walking dead-ends.
6. **Don't skip to root-cause certainty when evidence is incomplete.** Abstain over forced certainty; record unknowns and define the verification step that would resolve them.

## Confidence calibration

- **High confidence:** Multiple independent lines of evidence support the hypothesis; disconfirming checks have been run and failed to disprove.
- **Medium confidence:** Some evidence supports the hypothesis; one or more assumptions are unverified.
- **Low confidence:** Plausible but unverified; surfaced for completeness, not yet a candidate for action.

When evidence is genuinely incomplete, mark hypotheses as `abstain` rather than forcing a confidence label.

## Why this works

- **Atomic hypotheses can be independently disconfirmed;** one giant theory only fails as a whole and doesn't tell you which piece was wrong.
- **Disconfirming-first narrows the search faster** than confirming-first, which leads to confirmation bias.
- **"What this cannot be" forces the AI to state explicit assumptions** and quickly rule out areas that seem related but cannot be — based on a specific clue. Plus, writing down hypotheses, assumptions, and rule-outs is itself useful for future passes.

## Output format

When this method shapes a report, render it as four labeled sections in this order:

```
## Observed facts
- ...

## Hypotheses
- [confidence: high|medium|low] ...
- [confidence: ...] ...

## What this cannot be
- ... (because of <specific clue>)

## Unknowns
- ...
- Next verification step: ...
```

## Used by

- `evidence` mode of `dev-investigate` — core dependency
- `pr-interrogate` mode of `dev-investigate` — used for assumptions and confidence limits
- `recurring-hunt` mode of `dev-investigate` — Local Investigation Mode
- Any cross-system bug-comms workflow you maintain — consumes the four-bucket output for cross-system updates

## Malleability note

**Canonical:** the four-bucket vocabulary (Observed facts / Hypotheses with confidence / Ruled out / Unknowns) and the disconfirming-first discipline. Renaming buckets or collapsing them creates incompatibility across modes.

**Adaptable:** the rendering format (collapsing into prose vs. bullet sections), the confidence-rating granularity (low/med/high vs. richer scales), the placement in a larger report. Different modes may surface different subsets in their final output, but internally the method should run with all four.

