# Reference: Divergent-Strengths Templates

> **Malleability note:** These template snippets are starting points. Refine per project as you observe which divergence prompts produce the strongest contrasts in practice. The principle — instruct each lane to optimize for different strengths so consolidation has real choices to make — is canonical; the exact wording is adaptable.

For use in `dual-lane` mode. Append the appropriate divergent-strengths instructions to each lane's invocation prompt.

The goal is to *force divergence* so consolidation has real choices. Convergence between two lanes optimizing for the same things wastes subagent budget. Divergence produces material for consolidation.

## Standard template (works for most skills, type-agnostic)

**Lane A (`os-skillify`, generative drafting):**

> *Optimize for procedural clarity and vocabulary discipline. Explicit definitions, diagnostic vocabulary, pseudocode where it sharpens an operation, structured tables for taxonomies, Design Rationale + Source sections. The discipline that makes the skill mechanically runnable by a future agent.*

**Lane B (`anthropic-skills:skill-creator`):**

> *Optimize for principled flexibility and agent-directed voice. "You are the X" framing, failure-mode-as-headline, Working Voice section that talks to the future agent in second person, principles-over-checklists where judgment matters. The voice and framing that makes the skill feel like collaboration rather than spec-fulfillment.*

## Creative-type template

For skills where voice / persona / variety / anti-collapse matters.

**Lane A:**

> *Optimize for craft discipline and vocabulary precision. Per-decision-point vocabulary (disposition taxonomies, classification labels). Explicit treatment of the anti-collapse mechanism — how does this skill prevent training-mean output? Pseudocode for selection / randomization where applicable. Design Rationale section that names the creative decisions the skill turns on.*

**Lane B:**

> *Optimize for voice protection and craft flexibility. "You are the X" framing throughout. Failure-mode-as-headline naming the specific "feels like AI wrote it" failure for this skill. Working Voice section showing how the agent talks to the user (push-back norms, pacing, framing of trade-offs). Per-output judgment guidance written as principles, not checklists.*

## Technical-type template

For skills where invariants / edge-cases / verifiability matters.

**Lane A:**

> *Optimize for invariant rigor and edge-case taxonomy. Explicit Invariants section. Edge-case enumeration. Pseudocode for the operation. Disconfirming-check procedure. Failure-mode taxonomy with disposition vocabulary. Test-fixture examples.*

**Lane B:**

> *Optimize for principled boundary discipline and operating posture. "You are the X" framing. Failure-mode-as-headline naming the specific production-breaking failure. Working Voice section showing how the agent surfaces risk and confidence. Principles for when to abstain vs proceed.*

## Hybrid-type template

For skills with mixed creative and technical aspects.

**Lane A:**

> *Optimize for clarity at the interfaces. For creative sections (voice, persona, judgment), use principles-over-checklists. For technical sections (inputs, outputs, invariants), use vocabulary-discipline and structured-table form. Be explicit about which sections are which type and why.*

**Lane B:**

> *Optimize for agent-directed voice throughout, with the failure-mode framing adapted per section: "feels like AI wrote it" for creative parts, "breaks in production" for technical parts. Working Voice section that addresses both registers. Worked example showing the same operation with both creative-judgment and technical-precision visible.*

## How to adapt

- **Per-skill tuning.** As you observe which divergences produce the strongest consolidations for a specific project, refine the templates for that project. Save the project-tuned versions alongside the project's brief template.
- **Per-counterpart tuning.** If using a counterpart other than `skill-creator`, adjust Lane B's instructions to play to that counterpart's actual strengths.
- **Add lessons-from-prior-runs.** If a prior dual-lane run on a sibling skill revealed something like *"Lane A always over-specifies the worked example,"* append a constraint: *"Worked example should be illustrative-only, not template-shaped — under 30 lines."* Carry lessons forward.

## What divergence is *not*

- **Not divergent topics.** Both lanes work from the same brief on the same skill. They diverge in *how they emphasize* the brief's content, not in *what they cover*.
- **Not divergent quality.** Both lanes produce complete runnable skills. Neither is "draft" and the other "final." Both are first-class.
- **Not divergent constraints.** The brief's hard constraints bind both lanes equally. Divergence is in style, not in scope.

## Common failure: weak divergence

If consolidation reveals that both lanes produced nearly identical drafts, the divergent-strengths instructions were too weak. Strengthen for the next run:

- Make the contrast sharper (procedural-rigor vs principled-flexibility is sharper than *"be more explicit"* vs *"be less explicit"*).
- Add concrete deliverables that differ (e.g., Lane A must include pseudocode for at least one operation; Lane B must open with a failure-mode-as-headline section).
- Reference specific recent skills to anchor on (*"Lane A: model on the procedural-clarity style of [sibling skill]; Lane B: model on the agent-directed voice of [other sibling skill]"*).

## See also

- `type-lens.md` — what each type means
- `consolidation-rubric.md` — how the consolidate mode weights what each lane contributed
- `interview-the-need.md` — question bank that produces briefs the lanes operate on
- `../modes/dual-lane.md` — the mode that uses these templates
