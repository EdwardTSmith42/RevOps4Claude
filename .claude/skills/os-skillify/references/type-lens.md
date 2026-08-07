# Reference: Type Lens

> **Malleability note:** This framework is canonical for the type-lens distinctions. Specific question lists, stress-tests, and house-style sections per type are adaptable — refine based on what produces strong skills in practice. The orthogonal-axes principle (type is a lens, not a mode-peer) is non-negotiable.

The type lens is a parameter that layers across all `os-skillify` sub-modes. It adjusts:

- Interview questions (see `interview-the-need.md` for the question bank).
- Stress-test patterns (what to probe for during `enhance` / `consolidate`).
- House-style sections emitted in the resulting `SKILL.md`.
- Consolidation rubric weighting (see `consolidation-rubric.md`).
- Counterpart choice for `dual-lane` (in rare cases — default counterpart works for all types).

It does **not** change which sub-mode runs. `from-prompt` is still `from-prompt`; the lens just shapes how the workflow asks questions and what it emits.

## The three types

### `creative`

**Focus:** variety, voice, anti-collapse mechanisms, subjective quality.

**Failure mode:** *feels like AI wrote it.* The model's training-mean output is recognizable; preventing it is the craft.

**Examples:** fiction-writing skills (writer, story-architect, scene-planner, concept-developer), persona skills, content-generation skills, marketing-copy skills, narrative-design skills.

**What the lens emphasizes:**

- *Anti-pattern-collapse mechanisms* — wildcards, destabilizers, randomness, deliberate friction. The mechanisms that prevent the model from defaulting to genre-mean.
- *Voice and persona* — who is the agent being when it operates? Whose voice does it carry? What's the discipline that protects voice?
- *Per-beat / per-instance judgment* — creative skills often require judgment per output (what's fixed vs free to vary in story-architect; pen-fit in concept-developer). The lens surfaces these judgment points.
- *Working Voice section* — how the agent talks to the user matters. Conversational discipline, push-back norms, pacing.
- *Failure-mode-as-headline* — name the *feels like AI wrote it* failure at the top so the agent fights it deliberately.

**House-style sections typically emitted:**

- Default failure mode to fight
- Working Voice
- Worked example (illustrative, not template)
- Pen-name / persona considerations
- Anti-collapse mechanisms

### `technical`

**Focus:** precision, invariants, edge-case coverage, objective verifiability.

**Failure mode:** *breaks in production.* The output is wrong in a way that can be measured.

**Examples:** code-generation skills, deployment skills, validation skills, schema skills, data-migration skills, infrastructure skills, testing skills.

**What the lens emphasizes:**

- *Invariants* — what must hold across all invocations? What can never be true after this skill runs?
- *Edge cases* — empty inputs, null cases, race conditions, retries, timeouts, partial failures.
- *Disconfirming checks* — for medium / high-risk operations, what's the explicit check that would prove the skill failed?
- *Boundaries* — what does this skill not touch? What systems / files / state are out of bounds?
- *Verifiable outputs* — outputs that can be checked against a specification, not judged subjectively.

**House-style sections typically emitted:**

- Invariants
- Edge cases handled
- Boundaries (what this skill does NOT do)
- Verification / disconfirming-check procedure
- Failure-mode taxonomy
- Test fixtures or example inputs

### `hybrid`

**Focus:** situational — the skill has both creative and technical aspects, and different sections want different lenses.

**Examples:** PR-description skills (narrative + structured), documentation skills (clear-prose + correctness), infrastructure-narrative skills (technical content + voice), creative-tool-wrapper skills (taste + reliability).

**What the lens does:**

- Asks both pools of questions during interview, with the agent (and user) picking which apply.
- Allows section-by-section type assignment: *"inputs and outputs are technical; working voice and tone are creative."*
- Consolidation rubric applies weightings per section, not uniformly across the skill.

**Risk:** hybrid can become *apply both checklists wholesale*, which produces bloat. The discipline is *situational mixed*, not *both at once*.

## How the lens shapes each sub-mode

| Sub-mode | Creative adaptation | Technical adaptation | Hybrid adaptation |
| --- | --- | --- | --- |
| `from-prompt` | Phase 2 rationale probes anti-collapse + persona + craft discipline; Phase 4 build emits Working Voice, failure-mode-as-headline | Phase 2 probes invariants + edge cases + boundaries; Phase 4 emits Invariants, Verification | Section-by-section assignment; user picks |
| `from-content` | Craft-preservation tilts toward voice-protective and judgment-surfacing extraction | Craft-preservation tilts toward invariant and edge-case extraction | Both, per content section |
| `microtool-from-content` | 7-section anatomy emphasizes the persona / voice / craft sections | 7-section anatomy emphasizes the invariant / boundary sections | Both, with explicit per-section assignment |
| `microtool-from-job` | Clarification interview probes the anti-collapse / persona / craft target | Clarification interview probes the invariant / boundary target | Both pools available |
| `enhance` | "Stronger" = more voice-protective, more anti-collapse, more disciplined craft; cluster-coherence weighted toward voice / persona | "Stronger" = more precise, more deterministic, better edge-case coverage; cluster-coherence weighted toward invariant / contract | Both, per section |
| `dual-lane` | Divergent-strengths brief weights procedural-rigor vs voice-and-failure-mode; counterpart = `skill-creator` | Divergent-strengths brief weights tightness vs robustness; counterpart = `skill-creator` (or technical-focused alternative) | Both, with section-by-section weighting |
| `consolidate` | Rubric weights voice + working-voice section + anti-collapse mechanisms + failure-mode framing | Rubric weights invariants + edge cases + test coverage + procedural rigor | Per-section weighting |
| `interview` | Anti-collapse / voice / craft questions | Invariant / edge-case / boundary questions | Both pools available, pick per question |

## When type is unclear or inferred

- *Inferred from input:* file types (`.py`, `.ts`, `.sql` → technical; `.md`, `.txt` → likely creative or hybrid), framing in user's request (*"write" / "draft" / "compose"* → creative; *"validate" / "check" / "deploy"* → technical), existing skill stubs (look at sibling skills in same directory).
- *When unclear:* ask once. *"Is this skill creative-leaning, technical-leaning, or hybrid?"*
- *Asking is cheap.* Don't infer wrong silently. Inferring wrong then producing a brief / draft tuned to the wrong type wastes more time than the one question saves.

## Where this framework could be wrong

- *The line between types isn't always clean.* A PR-description skill has narrative quality (creative) but factual correctness (technical). Treat hybrid as the answer rather than forcing creative or technical.
- *If a type-specific operation diverges enough in steps (not just content), it should split into its own sub-mode.* Reserve that right. Right now the lens model works because the operations are stable; if `enhance creative` and `enhance technical` end up wanting different process steps (not just different content), they're really different sub-modes.
- *There may eventually be more than three types.* Process / orchestrator skills might be a real fourth type with different optimization targets. Don't add without need.

## Used by

- All sub-modes of `os-skillify` — pass `--type` parameter through; downstream references (interview-the-need, consolidation-rubric, divergent-strengths-templates) branch on it.
- The parent `SKILL.md` dispatcher — surfaces a single type-question at intake when the input doesn't make the type obvious.

## See also

- `interview-the-need.md` — type-lens-aware question bank
- `consolidation-rubric.md` — type-lens-aware weighting for `consolidate` mode
- `divergent-strengths-templates.md` — type-lens-aware divergent-strengths instructions for `dual-lane` mode
- `../../_shared/references/creative-criteria.md` — adjacent reference for creative-domain quality criteria
