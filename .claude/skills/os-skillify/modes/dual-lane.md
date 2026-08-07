---
name: dual-lane
description: >-
  Sub-mode of `os-skillify`. Spawn this skill + a different-lineage skill-drafter (default `anthropic-skills:skill-creator`) in parallel from one brief; auto-consolidate the two drafts. The divergence is real because the lanes come from different design philosophies — os-skillify enhances-from-prior-art with Personal OS inheritance; skill-creator builds-from-spec. Briefing each lane to optimize for different strengths sharpens the divergence. Five phases: Brief prep → Divergent-strengths instructions → Parallel spawn → Auto-consolidate → Decision log. Earns its extra subagent cost when the target skill is foundational, multi-mode, voice-load-bearing, first-of-a-kind, or high-stakes. Triggers on "run dual-lane on this," "parallel-draft this skill with skill-creator," "two-lane this skill." Do NOT trigger for leaf skills, mechanical transforms, well-modeled siblings, or low-stakes utilities (single-lane is sufficient).
---

# Sub-mode — Skillify dual-lane

Spawn two different-lineage skill-drafters in parallel from one brief, then consolidate. The mode's value comes from *forcing real divergence* — two lanes optimizing for different strengths produce material the consolidation has to genuinely choose between. Two lanes optimizing for the same things converge and waste subagent budget.

This mode orchestrates; it doesn't merge. The actual merge happens in `consolidate` mode, auto-invoked as the final phase unless `--stop-after-drafts` is set.

## When to use

This mode earns its extra cost when the target skill is:

- **Foundational** — referenced or invoked by multiple other skills.
- **Multi-mode / multi-input** — 3+ modes, multiple input shapes, judgment-heavy decision points.
- **Voice-load-bearing** — carries persona / voice / craft-judgment (creative skills especially).
- **First-of-a-kind** — no obvious sibling skill to model on; broad design space.
- **High-stakes** — a flaw propagates expensively into downstream work.

When in doubt, ask the user. The signal is roughly: *"if this skill ships subtly wrong, how many places will I feel that later?"* High → dual-lane. Low → single-lane is sufficient.

Single-lane is sufficient for leaf skills, mechanical transforms, well-modeled siblings, and low-stakes utilities. The mode itself can suggest *"this looks like a dual-lane candidate"* during brief intake based on these signals.

## Preconditions

The parent dispatcher's two gates apply (inheritance protocol + map-before-make). The inheritance protocol's outputs become part of both lanes' context — both lanes see the same voice, conventions, library, recent feedback — so they diverge in *how they emphasize the brief*, not in *what they know about the user*.

Writes follow `../../_shared/references/skill-update-protocol.md`. Both lane drafts and the consolidated result go through show-before-write.

## Inputs

1. **A brief artifact** — markdown file both lanes read. If no brief exists, route to `interview` mode first. The brief carries most of the work; this mode's quality is bounded above by brief quality.
2. **Counterpart selection** — default `anthropic-skills:skill-creator`. The name matters less than the *lineage*: what this needs is a skill-builder from a different tradition than skillify's, so the two drafts diverge in useful ways. On a harness without that specific skill, use its stock skill-builder (whatever it's called there) and tune Lane B's brief to that tool's actual strengths rather than to the ones listed below. May also be overridden if a better-fitting counterpart exists for the type lens.
3. **Type-lens parameter** — `creative`, `technical`, or `hybrid`. Adapts the divergent-strengths instructions and the consolidation rubric. See `../references/type-lens.md`.
4. **Output paths** — where each lane writes its draft. Convention: `experiments/<skill-slug>/skillify-lane.md` and `experiments/<skill-slug>/skill-creator-lane.md` (or counterpart name).

## Workflow

### Phase 1 — Brief preparation

If a brief artifact doesn't exist, route to `interview` mode to build one. Otherwise verify the brief covers:

- Project context + authoritative reading order
- Target skill purpose + existing stub (if any)
- Source material pointers
- Hard constraints
- Required capabilities + outputs
- Test fixture (if applicable)
- Form & style expectations
- Output paths for each lane

A thorough brief is non-negotiable. Thin briefs produce two thin drafts and a thin consolidation.

### Phase 2 — Divergent-strengths instructions

Append divergent-strengths instructions to each lane's invocation prompt. See `../references/divergent-strengths-templates.md` for type-lens-specific templates.

Standard divergence (works for most skills):

- **Lane A (os-skillify, `enhance`-flavored drafting):** *optimize for procedural clarity and vocabulary discipline — explicit definitions, diagnostic vocabulary, pseudocode where it sharpens an operation, Design Rationale + Source sections.*
- **Lane B (skill-creator):** *optimize for principled flexibility and agent-directed voice — "you are the X" framing, failure-mode-as-headline, Working Voice section.*

If type-lens is `creative`, emphasize anti-collapse mechanisms and persona/voice considerations. If `technical`, emphasize invariants and edge-case coverage. If `hybrid`, give each lane discretion to apply both where appropriate.

### Phase 3 — Parallel spawn

**Spawn both lanes as background subagents** (default — `run_in_background: true`). Foreground time during the wait is freed for useful work: writing the brief for the next wave, consolidating a prior wave's drafts, mining DESIGN_DECISIONS for new addenda. Background spawning is preferred whenever there's other work; foreground parallel works too but blocks the main agent thread.

Each lane:

- Reads the brief
- Invokes its respective skill (os-skillify or skill-creator)
- Drives end-to-end to a written `SKILL.md` draft at its assigned output path
- Returns a short self-summary (under 300 words): what differs from any prior stub, judgment calls made, concerns

Both lanes run in parallel; you wait for both to return before Phase 4.

**Lane retry pattern.** API failures happen (~1 in 20 subagent calls in observed practice — sockets close, providers hiccup). If a lane returns with an API error before producing its draft, **retry that lane rather than abandoning** — relaunch the same prompt as a new background subagent. The brief is unchanged; the failure is transient. Don't degrade to single-lane consolidation unless a retry also fails.

**Lessons from prior runs.** If prior `dual-lane` runs exist in this project (check `experiments/` or wherever drafts are archived), mine them for two things before launching:

1. Which lane tends to provide the consolidation backbone in this project's house style — so divergent-strengths instructions can lean into the *productive* contrast rather than restating defaults.
2. Recurring length issues, schema choices, or vocabulary that future briefs should pre-resolve.

Append these as a *Lessons from prior runs* section in the brief — both lanes pick them up.

### Phase 4 — Auto-consolidate (or pause for human review)

By default, when both lanes return, auto-invoke `consolidate` mode with both drafts as input.

If `--stop-after-drafts` is set, return both drafts to the user without consolidating. Use when human review of the two drafts is desired before merging.

### Phase 5 — Decision log

Standard `os-skillify` decision log for the dual-lane run as a whole:

- What the brief asked for
- What each lane produced (paths + brief summaries)
- What the consolidation kept from each lane (decided by `consolidate` mode and surfaced in its rationale)
- What was discarded with reasoning
- Any TBDs surfaced

Per project house style, the dual-lane entry may also append to a project-level DESIGN_DECISIONS log if one exists.

## Output

- Two lane drafts at the assigned paths
- A consolidated `SKILL.md` at the final destination (typically `skills/<skill-slug>/SKILL.md` or wherever the brief specified)
- A decision-log entry covering the dual-lane run
- A consolidation rationale (produced by the auto-invoked `consolidate` mode)

## Operating principles

- **Brief quality bounds output quality.** If the brief is thin, the consolidated draft will be thin too. Don't shortcut Phase 1.
- **Don't run two skillify lanes.** The divergence value comes from different lineages. Running skillify-twice converges and wastes subagent budget.
- **Don't pre-rank the lanes.** Both are first-class inputs to consolidation. The brief instructs each to optimize for different strengths *so consolidation has real choices to make* — not so one lane is "primary" and the other "secondary."
- **Background spawning is preferred** for parallel subagent execution. Foreground parallel works too but blocks the main thread.
- **Consolidation is its own mode.** This mode's responsibility is orchestration (brief → spawn → wait). The merge happens in `consolidate`.

## Failure modes to watch for

- **Lane convergence** — both lanes produce nearly identical drafts. *Cause:* brief didn't differentiate them, or divergent-strengths instructions were too weak. *Fix:* strengthen instructions in `../references/divergent-strengths-templates.md`; this run's consolidation is faster but produces less learning.
- **One lane fails or stalls** — counterpart timed out or returned an unusable draft. *Fix:* surface explicitly; consolidate from the surviving lane with a note that single-lane was used; consider running the counterpart again separately.
- **Brief inadequate** — both lanes asking the same clarifying questions or making the same wrong assumptions. *Fix:* this is a Phase 1 failure; route back to `interview` mode to strengthen the brief, then retry.

## See also

- `SKILL.md` — parent dispatcher
- `../references/divergent-strengths-templates.md` — divergence prompts for the two lanes
- `../references/consolidation-rubric.md` — how `consolidate` mode merges
- `../references/type-lens.md` — type framework that shapes divergent-strengths instructions
- `modes/consolidate.md` — the auto-final step
- `modes/interview.md` — brief-builder when source is thin
- `../../_shared/references/skill-update-protocol.md` — write discipline both lanes operate under

## Source provenance

Origin: real-world experience drafting the Autowriter Fiction skill stack. Running os-skillify + skill-creator in parallel from a thorough brief produced markedly stronger first-draft skills than either lane alone. The retry pattern, background-spawning default, and lessons-from-prior-runs section emerged from operating the pattern across several waves.
