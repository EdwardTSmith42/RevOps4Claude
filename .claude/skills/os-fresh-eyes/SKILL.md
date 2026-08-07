---
name: os-fresh-eyes
description: >-
  Take a skeptical second pass over any existing artifact — a plan, idea,
  strategy, draft, convention, or structure decision — to find what the first
  pass missed: the broader class the problem is an instance of, overlap with
  existing material, unearned commitments, ungrounded assertions, and drift from
  the user's own principles. Use when the user says "fresh eyes" on non-code
  work, or asks for a second pass, a re-review, a sanity check, or "what am I
  missing" on something that already exists. Do NOT trigger for original
  drafting (use the relevant authoring skill). Do NOT trigger for code, PRDs,
  or implementation outlines — use `dev-fresh-eyes` (if installed), the
  self-contained engineering sibling that shares this skill's core.
version: 0.1
display_name: Fresh Eyes (General)
tagline: 'A skeptical second pass for knowledge work — plans, ideas, drafts, decisions.'
category: Thinking
packs:
  - personal-os
icon: 'phosphor:Eye'
when_to_use: >-
  Use when an artifact already exists — a plan, product idea, strategy doc,
  piece of writing, workspace convention, or structural decision — and you
  want it pressure-tested before committing further. Grounded in the user's
  own corpus, not abstract best practice.

  For code and engineering plans, use `dev-fresh-eyes` (the dev calibration
  of this skill). For original drafting, use the relevant authoring skill.
---

# Fresh Eyes (General)

## Purpose

Challenge an existing artifact after the first pass produced it. Keep what is sound, name what the first pass structurally could not see, and surface the clearest better path without restarting from zero.

The skill exists because a first pass — human or AI, and especially AI — has a predictable stance: **local, additive, agreeable, and confident**. It solves the problem in front of it, solves it by making something new, accepts the frame it was handed, and presents the result with more certainty than the grounding supports. Fresh eyes is the systematic inversion: **global, subtractive, adversarial, and grounded**. Every lens below is one of those four inversions applied to a different surface. Hold the inversions as the mental model; the lenses are where they land.

This skill is the domain-general core. `dev-fresh-eyes` is its engineering calibration — same stance, plus repo-grounded moves (adjacent-code search, build-vs-buy ordering, test/lint/typecheck discipline, the failing-test-first pattern that both proves a fix and leaves a durable regression guard). Other discipline calibrations live in this file and grow as they earn their keep.

## When to use

- The user says "fresh eyes" about anything that isn't code or an engineering plan.
- An artifact exists — plan, musing, strategy, draft, convention proposal, structure decision — and the user wants it pressure-tested before more work stacks on top of it.
- Another skill's output is about to become an input to something bigger (an avatar feeding copy, a brief feeding a build) and the handoff deserves a skeptical gate.
- Early in a chain of decisions, when a wrong first move would beget more wrong moves — this is when the pass pays most.

Do NOT use for:
- Original drafting from scratch — there is nothing to re-see.
- Code, PRDs, implementation outlines, refactor plans — route to `dev-fresh-eyes` when installed; without it, run the core lenses here with the dev calibration notes below.
- Ongoing collaborative editing where the user wants a partner, not a review — use the relevant authoring or editing skill.

## Run

**1. Restate the artifact in two or three sentences** — its objective, its approach, and the decision it is asking the reader to accept. If you cannot restate the decision, that is itself the first finding: the artifact doesn't know what it's deciding.

**2. Ground before critiquing.** Read what sits adjacent in the user's corpus — related files, prior decisions in the same project, the principles docs, earlier artifacts the current one extends or contradicts. This step is load-bearing, and it is the one a default pass skips: critique without corpus-grounding degenerates into generic best-practice advice that any reviewer could have written about any artifact. If the corpus is thin or unavailable, say the pass is running unanchored rather than pretending it is grounded.

**3. Run the seven lenses.** Each names the default disposition it counters, because the counter-move is the craft — a lens applied without knowing why it exists gets applied mechanically.

- **Altitude — is this an instance or a class?** The default pass solves the problem in front of it. Ask what class of problem this is an instance of, and whether solving the instance sets a precedent that will be copied before the class is ever examined. The failure signature is parallel conventions that drift — the knowledge-work sibling of duplicated code that gets bug-fixed in one place and not the other. Then choose the altitude *deliberately*: sometimes the instance is still the right thing to solve today. Governor: **name the class, but bill the instance** — you may only escalate altitude if you also hand back an answer at the original altitude. A fresh-eyes pass that turns every question into a rearchitecture is its own failure mode.

- **Frame — is the artifact answering the right question?** The default pass polishes what it was handed. Ask whether the goal behind the request is better served by a different move, a smaller move, or no move. Deletion and do-nothing are first-class candidate outcomes and get genuinely steelmanned, not politeness-mentioned. Generation is the default tool's hammer; the strongest version of an artifact is sometimes the version where a whole section doesn't exist.

- **Adjacent estate — what already covers part of this?** The default pass creates; a grounded pass checks what exists first. In knowledge work the cost of missing overlap is not duplication but a **second source of truth** — two artifacts answering the same question slightly differently, which is worse than either being wrong, because the corpus now contradicts itself and every future reader inherits the ambiguity. For each overlap found: merge, link-and-defer, or declare the boundary explicitly. Never leave the overlap implicit.

- **System of artifacts — who consumes this later?** The default pass optimizes the deliverable in isolation. Ask what contracts this artifact touches: indexes that need a line, skills or documents that load it, conventions it silently extends or violates, readers who will act on it without this conversation as context. This is the knowledge-work version of changing a function without checking its callers.

- **Commitment gradient — what does this decision lock in, and is that earned?** The default pass is structure-eager: given ambiguity it proposes a directory, a taxonomy, a new category, because structure looks like helpfulness. But structure is cheap to create and expensive to unwind — it colonizes spatial memory, accrues links, and sets precedent. Ask whether the commitment has been earned by accumulated mass, and prefer the reversible shape when it hasn't. The dev calibration's live-production vs. pre-production split is this same lens: the stage of the work sets how much commitment a change is allowed to make.

- **Grounding — which load-bearing assertions are assumed rather than evidenced?** The default pass hedges stylistically everywhere while never identifying which *specific* assertion is ungrounded. Do the opposite: no diffuse hedging. First, where the artifact states facts about the corpus or the world ("the system already has X," "users do Y"), *verify the load-bearing ones directly* — read the file, check the source — rather than trusting the artifact's own confidence; an artifact's most checkable statements are the ones a default pass checks least. Then name the two or three assertions most likely to be wrong, what each rests on, and what evidence would settle it. An artifact allowed to say "hypothesis-grade" honestly is worth more than one that performs confidence.

- **Doctrine — does this drift from the operator's own principles?** The default pass treats every conversation as fresh and will cheerfully help violate last month's hard-won rule. This pass checks the artifact against what the user has already committed to — their principles files, prior decisions in the project, positions taken in earlier artifacts. Drift isn't automatically wrong; principles evolve. But drift must be *named* so the user chooses it rather than sliding into it. This lens is the one only a corpus-grounded reviewer can run, and it is not optional.

**4. Recommend the correction set.** Keep what is right, and say so specifically — affirmation is information, not padding. Order the findings by consequence, not by lens, and classify each by depth: **root** (correcting this resolves the finding and its siblings), **symptom** (this fixes the visible issue but the real cause sits upstream — name the upstream), or **adjacent** (valid, but not required for this artifact to succeed). For any correction that changes the artifact's direction, name its disconfirming check — what you'd expect to observe if the correction turned out to be wrong. Where the honest verdict on a finding is *unknown*, say `unknown` plus the next validation step; a manufactured verdict is worse than an open one. Where a finding implies work beyond the artifact's scope, capture it as an explicit deferral (route to the tracker or the relevant follow-up skill) rather than scope-creeping the artifact.

**5. Self-review before delivering.** The reviewer gets no reviewer, so run the pass on your own output: did any finding mistake a symptom for its cause? Did the altitude lens over-generalize into work the artifact doesn't require? Is every critique still tied to the actual artifact and corpus? Revise before returning, not after.

**6. If the artifact is already solid, say so plainly and stop.** A pass that manufactures findings to justify its invocation teaches the user to ignore it. "This holds up; two small notes" is a successful fresh-eyes run.

## Output

Self-contained markdown the user can paste into a doc or thread without editing. Report only the lenses that found something — a dutiful "no findings" under seven headers is noise. Suggested shape:

```markdown
## What Holds Up

## Findings (ordered by consequence)
<!-- each finding names its lens inline, states the issue, and proposes the correction -->

## The Class Behind the Instance   <!-- only when the altitude lens fired -->

## Deferred / Out of Scope

## Open Questions   <!-- at most two or three, sized for a human to actually answer -->
```

## Discipline calibrations

The seven lenses run everywhere; calibrations change emphasis and add discipline-specific heuristics — the moves that are genuinely native to one domain rather than instances of the core lenses.

- **`dev` → route to `dev-fresh-eyes` when installed.** The engineering sibling (dev pack) is canonical for code, PRDs, and implementation outlines; when it isn't installed, these notes are the fallback calibration. Its native heuristics: repo search for existing helpers before accepting custom work, the build-vs-buy preference order, the pre-production expansion rule, and proof discipline — e.g., writing the difficult *failing* test first, then fixing it, which both proves the fix and leaves a durable safeguard against regression. Those are dev-only tactics, but note how each maps to a core lens (adjacent estate, commitment gradient, grounding) — the mapping is what keeps the two skills from drifting.

- **`plan / strategy`** — emphasis on frame and grounding. Native heuristics: check that the plan states what would falsify it; check sequencing against dependencies rather than against enthusiasm; ask what the plan assumes about resources and attention that the operator's actual calendar contradicts.

- **`writing / content`** — emphasis on frame and system-of-artifacts. Native heuristics: check the piece against the stated audience artifact (not a generic reader); check that the opening promise and the body's delivery match; ask what the piece wants the reader to *do* and whether anything in it serves that.

- **`structure / convention`** (workspace and system decisions — new directories, schemas, naming, routing rules) — emphasis on altitude and commitment gradient. Native heuristics: has the structure been earned by mass or is it anticipatory; does the convention have an owner and a written home or will it exist only as precedent; what does a lazy write look like under this convention and does the design survive it.

When the artifact doesn't fit a listed calibration, run the core lenses uncalibrated and say so. When the same unlisted discipline shows up repeatedly, that's the signal to add its calibration — supply an example pass or two and route through `os-tune`'s `extend` so it lands as a first-class calibration here. A one-off domain doesn't earn a saved calibration; a recurring one does. The skill growing new calibrations is the intended behavior, not scope creep — fresh-eyes compounds across every domain the operator works in.

## Guardrails

- Do not rewrite the artifact unless its current shape is fundamentally wrong; the deliverable is findings and corrections, not a competing draft.
- Do not implement corrections during the review unless the user explicitly asks.
- Stay concrete: every critique ties to the actual artifact and the actual corpus, not to generic best practice.
- Escalate altitude only with a same-altitude answer attached (name the class, bill the instance).
- Push hardest early in a decision chain and on high-stakes artifacts; on low-stakes work, a light pass is the right-sized pass.
- State it flat, offer the alternative, name the trade-off. Don't hedge findings into noise.

## Design Rationale

- **The four inversions (global / subtractive / adversarial / grounded) are the core, not the lens list.** Lenses derived from a diagnosis stay coherent as they're recalibrated per discipline; a bare checklist drifts into mechanical application. The lens list can grow or merge; the inversions shouldn't need to.
- **Lenses run always; calibrations are per-discipline** — rather than making each lens a mode — because every artifact deserves every inversion cheaply, while disciplines differ in *emphasis* and in a small set of genuinely native tactics (the dev failing-test move has no writing-domain equivalent).
- **`dev-fresh-eyes` stays a separate skill** rather than folding in as a mode: it predates this skill, other dev skills invoke it by name, and its repo-grounded workflow is heavy enough to justify its own file. The reconciliation contract is the lens mapping noted in its calibration entry — dev nuances are documented as instances of core lenses, so improvements to the core propagate by intent rather than by copy-paste.
- **"Name the class, bill the instance" is the governor** that keeps the altitude lens from making this skill exhausting. A reviewer that always escalates teaches the user to stop inviting review.
- **"If it's solid, say so and stop" is inherited from the dev skill** and is load-bearing for trust: manufactured findings are how review skills die.
- **Report-only-what-fired output** counters the template-completion instinct — seven dutiful sections bury the two that matter.
- **Root/symptom/adjacent classification, the disconfirming check, the `unknown` verdict, and the self-review beat are shared lineage with `dev-now-what`** (dev pack, kept as the plan-forming beat of the delivery loop). Both skills carry these four moves deliberately — packs are self-contained — and improvements to them in either skill propagate to the other.

> **Propagation note:** `dev-fresh-eyes` and `dev-now-what` (dev pack) share this skill's core stance and several moves by design — self-contained siblings, not dependencies. Improvements to the shared core in any of the three should be propagated to the others when relevant. The duplication is deliberate; drift is not.

## Where outputs go

Outputs persist per the workspace storage methodology — see `../_shared/references/workspace-layout.md` (Knowledge system invariants): when the work belongs to an ongoing project, save silently to `os-outputs/` with dated frontmatter and a link trail; when the user is exploring, offer once. No skill-specific save scheme.

## Related skills

- `dev-fresh-eyes` (dev pack) — the self-contained engineering sibling; canonical for code, PRDs, implementation outlines when installed.
- `os-tune` / `extend` — how new discipline calibrations land in this skill.
- `dev-scope-deferral` — capture out-of-scope findings as explicit follow-ups.
- `os-audience`, `os-offer`, `os-writing` — common producers of the artifacts this skill reviews.
