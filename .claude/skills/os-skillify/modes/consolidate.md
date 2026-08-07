---
name: consolidate
description: >-
  Sub-mode of `os-skillify`. Merge two existing skill drafts into a single `SKILL.md` with consolidation rationale. Runs standalone (the user has two drafts from anywhere) or as the auto-final step of `dual-lane`. Six phases: Read both drafts → Apply consolidation rubric (type-lens-aware) → Resolve substantive disagreements → Compose consolidated draft → Emit rationale → Decision log. Substantive disagreements are pick-or-punt — never silently averaged. Triggers on "merge these two skill drafts," "consolidate <draft-a> and <draft-b>," "produce a consolidated skill from these two." Do NOT trigger for editing a single draft (use `os-tune/refine` or `enhance`), or for generating a fresh skill from scratch (use a generative sub-mode).
---

# Sub-mode — Skillify consolidate

Merge two existing skill drafts into one consolidated `SKILL.md` with a written rationale. The rationale is mandatory — future readers should be able to trace why every consolidation choice was made.

The mode runs standalone (the user supplies two drafts) or as the auto-final step of `dual-lane` (after parallel-spawn returns both lane drafts).

## When to use

- **Standalone:** *merge these two skill drafts*, *consolidate `skillify-lane.md` and `skill-creator-lane.md`*. The user has two drafts (from a prior `dual-lane` run, manual experiments, any source) and wants a merged result.
- **Auto-invoked:** end of `dual-lane` mode unless `--stop-after-drafts` was set.

Don't trigger for editing a single draft (route to `os-tune/refine` or `enhance`). Don't trigger for generating a fresh draft from raw inputs (route to a generative sub-mode like `from-prompt`, `from-content`, `microtool-from-content`, `microtool-from-job`).

## Preconditions

The parent dispatcher's two gates apply (inheritance protocol + map-before-make). Inheritance loads the same Personal OS context (voice, conventions, library) that bounds the consolidation choices; map-before-make confirms the consolidated skill genuinely needs to exist (vs. folding into an existing skill).

Writes follow `../../_shared/references/skill-update-protocol.md`. The consolidated draft is shown to the user before persistence; the rationale is shown alongside.

## Inputs

1. **Two draft paths** — `draft_a` and `draft_b`. Either order.
2. **Destination path** — where the consolidated `SKILL.md` should land. Conventionally `skills/<skill-slug>/SKILL.md`.
3. **Type-lens parameter** *(optional)* — `creative`, `technical`, `hybrid`. If absent, inherit from the drafts or ask once. Adjusts the consolidation rubric (see `../references/consolidation-rubric.md`).
4. **Original brief** *(optional but strongly recommended)* — the brief both drafts were built from. The brief's hard constraints, required capabilities, and required outputs become the consolidation's correctness floor.

## Workflow

### Phase 1 — Read both drafts in full

Read both drafts end-to-end. Catalog:

- *Structural elements present* in each (frontmatter, sections, examples, tables, code blocks)
- *Voice and framing differences* — does one open with "you are the X" while the other is procedural? Does one front-load failure modes while the other buries them?
- *Vocabulary differences* — same concept, different names? (e.g., one calls it `Bound / Partial / Open`; the other `Resolved / Pending / Open`)
- *Coverage differences* — what does each contain that the other doesn't?
- *Substantive disagreements* — places where the drafts contradict each other (e.g., one says load destabilizers; the other says don't)

Output a brief diff summary you'll use for consolidation choices.

### Phase 2 — Apply consolidation rubric (type-lens-aware)

Per `../references/consolidation-rubric.md`, weight each draft's strengths by type:

- *Creative type* — voice + working-voice section + anti-collapse mechanisms + failure-mode framing + persona-fit considerations
- *Technical type* — invariants + edge-case coverage + procedural rigor + diagnostic vocabulary + pseudocode where it sharpens
- *Hybrid type* — both, selectively per section

The rubric has element-by-element guidance for the common case where one lane is `os-skillify` (procedural-clarity, vocabulary-discipline) and the other is `skill-creator` (agent-directed voice, failure-mode-as-headline). Adapt as the drafts warrant — the rubric is a starting point, not a script.

### Phase 3 — Resolve substantive disagreements

If the drafts disagree on substance (not just framing), pick deliberately, with reasoning:

1. *Check against the brief's hard constraints.* Usually one draft is brief-consistent and the other isn't. Pick the brief-consistent one; discard the other.
2. *If both are brief-consistent but they disagree on craft:* pick on craft grounds, with reasoning surfaced in the rationale (*"Lane A says load destabilizers; Lane B says don't. Brief says skill is not a prose mutator; destabilizers are for prose mutators only. Taking Lane B's position."*).
3. *If you can't pick confidently:* mark the cell as TBD in the consolidated draft and surface to the user. Don't silently choose.

**Never silently average or split-the-difference on substantive disagreements.** Pick or punt; don't soften.

### Phase 4 — Compose the consolidated draft

Write the consolidated `SKILL.md` to the destination path. Follow project house style if a sibling skill exists at the destination (mirror its section ordering, vocabulary, link conventions).

Length should match the more comprehensive of the two drafts — the goal is to capture the best of both, not produce a shorter average. If both drafts came in significantly over the brief's length target, consolidation can trim back to target by dropping the elements with the weakest justification (usually redundant examples or over-explained rationale).

### Phase 5 — Consolidation rationale (mandatory)

Emit a consolidation rationale. Two options:

- *Inline:* appendix section in the consolidated `SKILL.md` (typically `## Source` or `## Consolidated from`). Names what came from each lane. This is the house style for many projects and works well when the rationale is short.
- *Sidecar:* separate `experiments/<skill-slug>/CONSOLIDATION.md` if the destination skill should stay clean of consolidation noise.

Rationale minimum content:

- What each lane contributed (short bulleted summary)
- What was discarded from each lane (with reasoning)
- Where the lanes disagreed and which way the consolidation went (with reasoning)
- Any TBDs left for the user

### Phase 6 — Decision log

Standard `os-skillify` decision-log entry covering the consolidate run. Include input draft paths, destination path, and a pointer to the consolidation rationale.

## Operating principles

- **Both lanes are first-class inputs.** Don't pre-rank. The rubric weights different strengths but both drafts contribute.
- **Substantive disagreements are pick-or-punt.** Never average or split.
- **House style wins ties.** If both drafts are equally strong on a given element but the project has a sibling skill establishing a convention, follow the convention.
- **The brief is the correctness floor.** Anything in the brief's hard constraints that's missing from the consolidated draft is a bug.
- **Don't quietly drop content.** Anything from either lane that doesn't make the consolidation gets a decision-log entry. Lossless by default applies here too.

## Failure modes to watch for

- **Bloated consolidation** — keeping everything from both drafts produces a 2x-length skill worse than either. *Fix:* pick per element; don't aggregate.
- **Voice patchwork** — switching between "you are the X" framing and procedural framing mid-skill reads jarringly. *Fix:* pick one voice and apply throughout.
- **Vocabulary collision** — both drafts have disposition taxonomies with overlapping but slightly different labels. *Fix:* never use both vocabularies in the same skill. Pick the cleaner one and document why.
- **Lost rationale** — consolidating without writing the rationale means future readers can't trace why choices were made. *Fix:* the rationale is mandatory. Phase 5 isn't optional.
- **Silent averaging** — picking "somewhere in the middle" on substantive disagreement without explicit reasoning. *Fix:* pick or punt explicitly. Soft averages hide bad decisions.
- **Brief drift** — consolidated draft drifts from the brief's hard constraints because neither lane was checked against the brief explicitly. *Fix:* the brief is the correctness floor; verify the consolidated draft against it before declaring done.

## See also

- `SKILL.md` — parent dispatcher
- `../references/consolidation-rubric.md` — full rubric with type-lens weightings
- `../references/type-lens.md` — type framework
- `../references/divergent-strengths-templates.md` — what the two lanes were optimizing for (when called from `dual-lane`)
- `../references/disposition-vocabulary.md` — canonical labels (apply to consolidation decisions as needed)
- `modes/dual-lane.md` — the mode that auto-invokes this one
- `../../_shared/references/skill-update-protocol.md` — write discipline

## Source provenance

Pattern emerged from the Autowriter Fiction work. Initial dual-lane drafts produced markedly stronger results than either lane alone — but only when consolidation was treated as a distinct craft rather than a "pick the better draft" shortcut. Encoding the rubric, the pick-or-punt rule, and the mandatory-rationale step is what made the pattern repeatable.
