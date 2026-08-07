# Mode: triage-and-fix

Part of the `dev-investigate` skill. Selected when the user wants one expert to choose the right investigation, proof, and fix workflow rather than manually selecting among bug, incident, observability, and validation tools — phrasings like "investigate, fix, and prove this bug correctly" or "what's the right way to handle this regression."

## Job

Pick the right investigation lane, name the root-cause hypothesis before implementing, scale proof depth to risk, and stop short of escalating into full incident process when a small direct repro is enough.

## Run

1. **Classify the bug:**
   - `regression | incident | support report | local repro | unknown`
2. **Choose the smallest credible repro boundary first.**
3. **Decide the primary lane:**
   - direct repro and fix
   - structured bug ops case
   - support/incident bundle
   - temporary observability
4. **Name the root-cause hypothesis before implementing.**
5. **Choose the fix shape:**
   - root fix
   - partial root fix
   - symptom containment with explicit follow-up
6. **Choose the proof:**
   - targeted test
   - differential proof (base fail / candidate pass — see `references/differential-proof.md`)
   - invariant gate
   - local/dev observability loop

### Optional escalation

Escalate only when the bug case needs additional evidence or a more formal lane:

- use a broader risk-scaled bug workflow when the case needs a fuller system of record than a simple direct fix
- use a structured investigation lane (`evidence` mode) for high-ambiguity or high-impact incidents
- use support, error-monitoring, or other external evidence lanes when the local repro is weak and outside evidence should shape the investigation
- use temporary observability or harness work when root cause is sequence-dependent, timing-sensitive, or otherwise opaque
- use before/after proof or ship/no-ship review lanes (`pr-interrogate` mode) when the fix needs stronger release evidence than a local repro alone
- use a proof-design lane when verification strategy is the real blocker
- when an adjacent valid improvement surfaces but expands blast radius beyond the current fix, invoke the `dev-scope-deferral` skill rather than bloating this fix

See `references/lane-selector.md` for the full lane menu.

### Guardrails

- Prefer root-cause fixes over symptom-only patches.
- Do not broaden into full incident process when a small direct repro is enough.
- Do not claim full root-cause closure if the fix only guards one symptom path.
- If evidence is incomplete, say `unknown` instead of forcing certainty.
- Remove or review process-driven instrumentation before closeout.

## Mode-specific references

- `../references/lane-selector.md` (escalation menu)
- `../references/rootness-classification.md` (ROOT / PARTIAL_ROOT / SYMPTOM — informs fix-shape choice)
- `../references/differential-proof.md` (proof options)
- `../references/non-ship-gate.md` (close-out conditions)
- `../references/output-format-contract.md` (plain language first, raw IDs secondary)

## Output

Soft template — adapt to context:

- `Bug frame` — one-sentence restatement of the bug
- `Smallest repro boundary` — what does and doesn't reproduce
- `Primary investigation lane` — what was chosen and why
- `Fix shape` — root / partial root / symptom containment
- `Proof plan` — what verifies the fix and how
- `Open risks and follow-ups` — what isn't yet addressed (invoke `dev-scope-deferral` for valid deferrable items)

## Design Rationale

Mode-specific notes (cluster-level rationale lives in the parent SKILL.md):

- **The 6-step picker (classify → repro boundary → primary lane → root-cause hypothesis → fix shape → proof) works because each step's output gates the next** — you can't choose the fix shape before naming the root-cause hypothesis; you can't choose the proof before knowing the fix shape. Reordering or skipping breaks the verification chain.
- **"Push toward root cause over symptom-only fixes" appears as both goal and guardrail** — redundancy is reinforcement, not waste. Symptom containment is sometimes the right answer; the doubled mention prevents drifting to it as the default.
- **"Do not broaden into full incident process when a small direct repro is enough"** — process bloat steals attention from the actual fix. The "smallest credible repro boundary" guideline prevents the picker from automatically choosing the heaviest lane.
- **"If evidence is incomplete, say `unknown` instead of forcing certainty"** — when this mode escalates to the user for a decision, abstaining keeps the option open for follow-up; forcing certainty propagates as ground truth and corrupts downstream choices.
