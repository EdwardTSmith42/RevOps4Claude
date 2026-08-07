# Mode: mutation-scout

Part of the `dev-investigate` skill. Selected when the user wants to pressure-test whether a PR diff would catch realistic mistakes — phrasings like "are these tests actually catching anything," "pressure-test the diff," "mutation-scout this PR," or "if the changed code were wrong, would current proof notice."

The core question is: **if the changed code were wrong in a realistic way, would current proof notice?**

## Job

Diff-scoped mutation and fault-injection thinking. Pressure-test a diff, not a repository. Identify likely surviving mutants and the smallest stronger proof.

## Run

1. **Scope to changed hunks plus immediate guards, consumers, and boundaries.**

2. **Classify the change shape:**
   - `branch/boundary`
   - `mapping/contract`
   - `error/retry`
   - `async/state`
   - `normalization/defaulting`

3. **Inspect nearby tests and proof artifacts.**

4. **Generate roughly 3–8 realistic mutants or injected faults.** The principle is bounded count, not the specific bounds — fewer leaves the test gap unclear; more drowns the signal in noise.

5. **Judge whether current proof likely `kills`, `misses`, or leaves them `unclear`.**

6. **Name shallow-test patterns and the smallest stronger proof.**

7. **Stop once the weakness pattern is clear and actionable.** Don't grind through 20 mutants when 3 already showed the gap.

## Mode-specific references

- `../references/defect-families.md` (the change-shape categories overlap with defect-families)
- `../references/triage-rubric.md` (for the "Stop or defer note" output: HUMAN_DECISION / DEFER)
- `../references/output-format-contract.md`

## Output

Soft template — produce some or all of:

- `Changed-code mutation surface`
- `Top mutant or fault ideas` (3–8 realistic ones)
- `Shallow-test signals`
- `Likely surviving mutants`
- `Minimal strengthening plan`
- `Stop or defer note` — when the weakness pattern needs broader work, invoke the `dev-scope-deferral` skill rather than embedding follow-up TODOs

## Guardrails

- Do not recommend whole-repo mutation runs by default.
- Do not chase mutation score.
- **Prefer realistic developer mistakes and runtime faults over synthetic noise.** The realistic qualifier prevents the LLM-failure-mode of generating off-by-one and null-check mutants in code that already handles them.
- Prefer manual or local fault injection when tool setup would cost more than the insight.
- Focus on changed code and immediate risk edges only.
- **Prefer one stronger property or contract test over many weak examples.**

## Design Rationale

Mode-specific notes:

- **"If the changed code were wrong in a realistic way, would current proof notice?"** is the framing question — the entire mode collapses to this one sentence. Keep verbatim.
- **The 3–8 mutant range is an undefended default** — the principle (bounded count) is what carries; the specific bounds are flexible. Phrased softly as "roughly 3–8."
- **"Realistic developer mistakes over synthetic noise"** — without the realistic qualifier, mutation thinking generates trivial null-checks and off-by-ones in code that already handles them. The qualifier is what keeps the mutants useful.
- **"Stop once the weakness pattern is clear and actionable"** — explicit stop criterion prevents grinding through 20 mutants when 3 already showed the gap.
- **"Prefer one stronger property or contract test over many weak examples"** — same heuristic appears in `latent-hunt`. Cluster-shared craft.
