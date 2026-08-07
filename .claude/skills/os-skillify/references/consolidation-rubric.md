# Reference: Consolidation Rubric

> **Malleability note:** The weighting tables are starting points based on observed `dual-lane` runs. The principle — consolidate per element with explicit weighting by type-lens — is canonical. Specific element-to-lane mappings are adaptable as the project's house style evolves.

For use in `consolidate` mode (and the auto-final phase of `dual-lane`). Provides the rubric for merging two skill drafts into one consolidated `SKILL.md` with explicit rationale.

## Phase 1 — Read both drafts in full

Catalog:

- Structural elements present in each (frontmatter, sections, examples, tables, code blocks).
- Voice and framing differences.
- Vocabulary differences (same concept, different names).
- Coverage differences (what each contains that the other doesn't).
- Substantive disagreements (places where the drafts contradict).

Output a brief diff summary used to drive consolidation choices.

### Settled house style → expect one lane as natural backbone

In a project where the house style has stabilized across many skills, expect one lane to consistently produce the **consolidation backbone** with the other lane providing additive structure. (Observed in practice: agent-directed-voice lanes tend to win backbone duty once a project's house style favors that register; vocabulary-and-procedure lanes contribute taxonomies, decision tables, and pseudocode as targeted additions.)

That's a feature, not a failure of divergence. The brief's *divergent-strengths* instructions should still push the lanes toward different optimization targets — that's what makes the additive contributions sharp. But once the backbone-lane pattern is clear, consolidation can lean into it: use the backbone lane's draft as the base file, layer in the other lane's specific contributions, document the choice in the rationale. Faster to consolidate, equally honest about what each lane produced.

When the backbone-lane pattern is *not* clear — both lanes equally complete, neither obviously the foundation — that's a real divergence and consolidation should pick per element rather than by lane.

## Phase 2 — Apply the rubric (type-lens-aware)

### Default weightings (type-agnostic)

When one lane is `os-skillify` and the other is `skill-creator`, these elements typically come from the named lane:

| Element | Typically take from | Reason |
| --- | --- | --- |
| Opening + voice | `skill-creator` (agent-directed "you are the X") | Reads better for a skill an agent has to internalize |
| Default failure modes section | `skill-creator` (failure-mode-as-headline) | Surfacing failures up-front improves discipline |
| Frontmatter description | Merge (`skill-creator`'s positive triggers + `os-skillify`'s negative triggers) | Description discipline benefits from both |
| Mode list / process structure | Pick the cleaner of the two; often `skill-creator` | First-class modes read better than appendices |
| Vocabulary taxonomies (dispositions, statuses, classifications) | `os-skillify` | Typically more rigorous |
| Pseudocode | `os-skillify` | Sharpens operations |
| Diagnostic vocabulary | `os-skillify` | Procedural-clarity strength |
| Worked example | `os-skillify` (more detailed) | Mark as illustrative, not template |
| Disconfirming checks | `os-skillify` | When present, valuable |
| Working Voice section | `skill-creator` | Conversational discipline |
| Per-file / per-section guidance | `os-skillify` (when present) | Procedural-clarity strength |
| Design Rationale | `os-skillify` | Typically deeper |
| Source / discarded notes | `os-skillify` | Provenance discipline |

### Creative-type weighting adjustments

When the type lens is creative, *additionally* favor:

- Voice-protection mechanisms — from whichever lane has them more developed.
- Persona / pen-name considerations — from whichever lane treats them more deliberately.
- Anti-collapse mechanisms — both lanes' coverage gets preserved; never drop.
- "Default failure mode to fight" framing — `skill-creator` typically wins this.
- Per-output judgment surfaces — from whichever lane makes them more explicit.
- Worked examples — keep one, ensure it's clearly illustrative-not-template (per project house style).

### Technical-type weighting adjustments

When the type lens is technical, *additionally* favor:

- Invariants section — from whichever lane has them more rigorous.
- Edge-case enumeration — both lanes' coverage gets preserved.
- Disconfirming-check procedure — `os-skillify` typically wins this.
- Test fixtures — from whichever lane provides them.
- Boundary statements — both lanes' boundaries get unioned.
- Failure-mode taxonomy — `os-skillify` typically wins this.

### Hybrid-type weighting

Apply both creative and technical adjustments per section. Identify which sections are creative-flavored (voice, persona, judgment surfaces) and which are technical-flavored (inputs, outputs, invariants), and weight accordingly.

## Phase 3 — Resolve substantive disagreements

If the two drafts disagree on substance (not just framing), pick deliberately:

1. *Check against the brief's hard constraints.* Usually one draft is brief-consistent and the other isn't. Pick the brief-consistent one and discard the other.
2. *If both are brief-consistent but they disagree on craft:* pick on craft grounds, with reasoning surfaced in the rationale (*"Lane A says load destabilizers; Lane B says don't. Brief says skill is not a prose mutator; destabilizers are for prose mutators only. Taking Lane B's position."*).
3. *If you can't pick confidently:* mark the cell as TBD in the consolidated draft and surface to the user. Don't silently choose.

**Never silently average or split-the-difference on substantive disagreements.** Pick or punt; don't soften.

## Phase 4 — Compose the consolidated draft

Write the consolidated `SKILL.md` to the destination path. Follow project house style if a sibling skill exists at the destination (mirror its section ordering, vocabulary, link conventions).

Length should match the more comprehensive of the two drafts — the goal is to capture the best of both, not produce a shorter average. If both drafts came in significantly over the brief's length target, the consolidation can trim back to target by dropping the elements with the weakest justification (usually redundant examples or over-explained rationale).

## Phase 5 — Consolidation rationale (mandatory)

Emit a consolidation rationale. Options:

- *Inline:* appendix section in the consolidated `SKILL.md` (typically `## Source` or `## Consolidated from`). Names what came from each lane. Works well when rationale is short.
- *Sidecar:* separate `experiments/<skill-slug>/CONSOLIDATION.md` if the destination skill should stay clean of consolidation noise.

Rationale minimum content:

- What each lane contributed (short bulleted summary).
- What was discarded from each lane (with reasoning).
- Where the lanes disagreed and which way the consolidation went (with reasoning).
- Any TBDs left for the user.

## Phase 6 — Decision log

Per `os-skillify` craft, emit a decision-log entry covering the consolidate run. Include input draft paths, destination path, and a pointer to the consolidation rationale.

## Common consolidation failure modes

- **Bloated consolidation** — keeping everything from both drafts produces a skill longer and worse than either. *Fix:* pick per element; don't aggregate. The rubric weighting forces a choice per element.
- **Voice patchwork** — switching between "you are the X" framing and procedural framing mid-skill reads jarringly. *Fix:* pick one voice and apply throughout. The opening voice usually determines the rest.
- **Vocabulary collision** — both drafts have a disposition taxonomy with overlapping but slightly different labels. *Fix:* never use both vocabularies in the same skill. Pick the cleaner one and document why.
- **Lost rationale** — consolidating into the final `SKILL.md` but forgetting the rationale means future readers can't trace why choices were made. *Fix:* the rationale is mandatory. Phase 5 isn't optional.
- **Silent averaging** — picking "somewhere in the middle" on substantive disagreement without explicit reasoning. *Fix:* pick or punt explicitly. Soft averages hide bad decisions.
- **Brief drift** — consolidated draft drifts from the brief's hard constraints because neither lane was checked against the brief explicitly. *Fix:* the brief is the correctness floor; verify the consolidated draft against it before declaring done.

## See also

- `type-lens.md` — full type framework
- `divergent-strengths-templates.md` — what the two lanes were optimizing for
- `disposition-vocabulary.md` — canonical labels (apply to consolidation decisions as needed)
- `../modes/consolidate.md` — the mode that uses this rubric
- `../modes/dual-lane.md` — the mode that auto-invokes consolidate
