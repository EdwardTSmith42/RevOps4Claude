---
name: dev-plan
description: >-
  Plan code work via three modes — `scope` (thin slices, milestones, non-goals),
  `architecture` (boundaries, invariants, blast radius, migration), or `prd`
  (formal MVP PRD with RED→GREEN→VERIFY execution). Triggers on "plan this
  feature", "scope this work", "architecture question on X", "draft a PRD for",
  "what's the smallest valuable slice". Do NOT trigger for second-pass critique
  of an existing plan (use `dev-fresh-eyes`). Do NOT trigger for in-flight bug
  investigation (use `dev-investigate`).
version: 0.1.0
category: Planning
display_name: Plan
tagline: 'Plan code work — scope slices, architecture, or formal PRD.'
packs:
  - dev-pack
icon: 'phosphor:MapTrifold'
when_to_use: >-
  Reach for this when you're about to build something real and want the plan before the code —
  slicing the work into milestones, pinning down the architecture and its blast radius, or
  writing a full MVP spec.

  Three modes — `scope` (thin slices, milestones, non-goals), `architecture`
  (boundaries, invariants, blast radius, migration), `prd` (formal MVP PRD with
  RED → GREEN → VERIFY execution).
modes:
  - name: scope
    job: 'Thin slices, milestones, non-goals.'
  - name: architecture
    job: 'Boundaries, invariants, blast radius, migration.'
  - name: prd
    job: Formal MVP PRD with RED → GREEN → VERIFY execution.
---

# dev-plan

## Purpose

Plan code work before writing it. Three planning angles — pick the one that matches the actual question:

- **`scope`** — what to build, in what order, what to defer. Thin-slice / milestone / non-goals discipline.
- **`architecture`** — system shape, boundaries, invariants, blast radius, migration strategy.
- **`prd`** — formal MVP-scoped PRD with existing-pattern inventory, overlap scan, and RED→GREEN→VERIFY execution gate.

The three angles are complementary. A single planning session often touches all three: scope first to bound the work, architecture if structural risk is real, PRD when the work needs a formal write-up + execution discipline.

## Mode selection

| Question | Mode |
|---|---|
| "What's the smallest slice that matters?" | `scope` |
| "What can we defer? What's a `now / later / unknown yet`?" | `scope` |
| "Where should the boundary be?" / "Where do I put the seam?" | `architecture` |
| "What invariants should this preserve?" / "What's the blast radius?" | `architecture` |
| "I'm starting non-trivial implementation; need a PRD" | `prd` |
| "Need RED→GREEN→VERIFY execution discipline" | `prd` |
| "Has anyone touched this in an open PR?" | `prd` (it includes overlap scanning) |

If the user asks something cross-cutting ("plan this feature, including architecture and PRD"), run `scope` first to bound the work, then route to `architecture` and/or `prd` as the bound surfaces structural and execution risk.

## Run

1. **Pick the mode** using the table above. If ambiguous, ask the user briefly which angle matters most.
2. **Read the mode file** in `modes/<mode>.md` and execute its workflow.
3. **End at the mode's defined output** — don't expand into an adjacent mode without user direction.

Each mode produces a different durable output:
- `scope` → a markdown plan with thin-slice scope, non-goals, milestone order, risks/proof, open questions
- `architecture` → a markdown design with problem frame, invariants, boundary proposal, blast radius, rollout
- `prd` → a markdown PRD file at the agreed path (default `.local/dev-plan/prd/<slug>.md`) with existing-pattern inventory, MVP scope, failing-tests-first, minimal implementation plan

## Hard rules (cluster-level — apply across modes)

- **Always name non-goals explicitly.** A plan that can't say what's intentionally *out* of scope is still too broad.
- **Sequence proof / verification early**, not as an afterthought. The plan should connect what's being built to how it's being proven.
- **Smallest valuable move** before bigger structural moves. Prefer a thin slice that ships and reviews cleanly over a "do everything" phase.
- **Prefer existing patterns** over inventing new structure unless there's a real reason. (Cross-references: `dev-fresh-eyes`'s build-vs-buy order applies here too.)
- **Don't do false precision in estimates** when the real uncertainty is structural — name the structural unknowns instead.
- **If a human revises the plan with explicit constraints**, fold them into the active plan / checklist before more design work. Never plan against a stale draft.

## Hand-offs to adjacent skills

- **`dev-fresh-eyes`** — once a plan or architecture proposal exists, run a skeptical second pass before implementation.
- **`dev-PR`** — when the plan converges into a real branch and PR, the brief carries planning rationale forward.
- **`dev-branch-memory`** — capture decision-trail memory during execution; the architecture and PRD modes especially benefit from `dev-branch-memory capture` calls when key trade-offs get made.
- **`dev-scope-deferral`** — for items the plan explicitly defers, capture them as deferred-investigation notes so they don't get lost.

## Distinct from adjacent skills

- **`dev-fresh-eyes`** critiques an *existing* plan; dev-plan *produces* one. They pair: dev-plan emits, dev-fresh-eyes pressure-tests.
- **`dev-investigate`** investigates bugs (something already broken); dev-plan plans new work or refactors.
- **`dev-review checkpoint`** reviews milestone state mid-execution; dev-plan establishes the milestone shape before execution.

## Design Rationale

- **Three modes preserve three distinct planning angles.** Folding them into one mode would lose the discipline that comes from picking *which angle* matters now — sequencing, structure, or formal write-up.
- **Mode selection as a routing question, not a workflow phase** — different planning sessions need different angles. Forcing every session through scope→architecture→prd in lockstep adds friction when only one angle is in play.
- **Cluster-level hard rules apply across modes** — non-goals, smallest-move, proof-early are shared discipline. Lifting them to the SKILL.md top-level surfaces them at routing time rather than duplicating across modes.
- **PRD mode is `prd`, not `mvp-prd`**. The MVP framing is implicit in the discipline (in-scope / out-of-scope / minimal implementation) — naming it `mvp-prd` adds redundancy without clarity.
- **Negative triggers in description** disambiguate from `dev-fresh-eyes` (critique-side) and `dev-investigate` (bug-side).

## References

- `references/scope-shaping.md` — `scope` mode: now/later/unknown-yet rule, smallest-outcome heuristics
- `references/plan-review-loop.md` — `scope` mode: when plan-review lanes materially sharpen the plan
- `references/architecture-question-types.md` — `architecture` mode: question taxonomy (boundary / decomposition / integration / migration / contract risk / system cleanup)
- `references/change-design-heuristics.md` — `architecture` mode: narrowest-move heuristics, invariant guidance
- `references/prd-rubric.md` — `prd` mode: section quality bar, ship/no-ship checks

## Templates

- `templates/prd-template.md` — `prd` mode: PRD skeleton with MVP gates (problem, pattern inventory, overlap scan, MVP scope, failure modes, RED tests, GREEN implementation, VERIFY)

## First-time setup

The `prd` mode's overlap-scan step shells out to GitHub's `gh` CLI (`gh pr list`, `gh pr view`). Install `gh` and authenticate (`gh auth login`) before first use, or adapt the overlap-scan step to your forge's equivalent (e.g., `glab` for GitLab). Skills assume a GitHub-style PR workflow; if your team uses a different tracker for branch overlap, swap the command and keep the discipline.

(This note can be deleted from your local copy of the skill once `gh` is installed and working.)
