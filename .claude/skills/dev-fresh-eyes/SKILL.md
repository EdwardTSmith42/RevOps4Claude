---
name: dev-fresh-eyes
description: >-
  Take a second skeptical pass over an existing plan, proposed approach, PRD, or
  implementation outline. Use when the user says "fresh eyes," "re-review with
  fresh eyes," or asks for a second pass to find gaps, inconsistencies,
  mistakes, missed opportunities, reusable existing patterns, over-engineering,
  under-engineering, over-complication, or custom work that should instead reuse
  an existing package or internal solution. Do NOT trigger for original drafting
  from scratch (use the relevant authoring skill). Do NOT trigger for code
  review of a bug-fix PR — use `dev-investigate pr-interrogate` instead.
version: 0.1.0
display_name: Fresh Eyes
tagline: 'A skeptical second pass on an existing plan, PRD, or implementation outline.'
category: Troubleshooting
packs:
  - dev-pack
icon: 'phosphor:Eye'
when_to_use: >-
  Use when a plan / PRD / proposal / implementation outline already exists and
  you want it pressure-tested for gaps, sizing, reuse opportunities, or
  build-vs-buy decisions. Inspects adjacent reality before critiquing —
  repo-grounded, not abstract best-practice advice.
---

# Fresh Eyes

## Purpose

Challenge a plan after an initial draft already exists. Keep what is sound, tighten what is weak, and surface the clearest better path without restarting from zero. Use to find gaps, inconsistencies, mistakes, missed opportunities, reusable existing patterns, over-engineering, under-engineering, over-complication, or custom work that should instead reuse an existing package or internal solution.

This skill is intentionally cross-cutting: invoked from inside other skills (e.g., `dev-investigate recurring-hunt` Fix Flow step 2 calls fresh-eyes on the chosen plan) and directly by the user when reviewing PRDs, implementation outlines, refactor plans, branch strategies, or architectural proposals.

## When to use

- The user says "fresh eyes" or asks for a second pass on an existing draft.
- A plan / PRD / proposal / implementation outline already exists and the user wants to pressure-test it for gaps, sizing, reuse opportunities, or build-vs-buy decisions.
- During autonomous fix loops (e.g., `dev-investigate recurring-hunt`), as a discipline before implementing — pressure-test scope and reuse before writing code.

Do NOT trigger for:
- Original drafting from scratch (no draft to critique).
- Code review of a bug-fix PR — that's `dev-investigate pr-interrogate`'s job (with reproduction evidence and rootness classification).
- Generic "is this code good" reviews — use `dev-review` for those.

## Run

1. **Restate the plan briefly:**
   - objective
   - main approach
   - explicit scope

2. **Inspect adjacent reality before critiquing:**
   - Search the repo for similar features, helpers, components, flows, abstractions, or dependencies.
   - Note existing patterns worth piggybacking on.
   - **This step is load-bearing.** Critiquing in the abstract without checking what already exists is the single most common failure mode of "fresh eyes" reviews.

3. **Run a skeptical second pass across these lenses:**
   - **gaps:** missing steps, missing edge cases, weak proof, rollout blind spots
   - **inconsistencies:** conflicts between goals, scope, architecture, sequencing, or constraints
   - **mistakes:** broken assumptions, wrong boundaries, fragile dependencies, or incorrect technical reasoning
   - **opportunities:** simpler paths, cleaner reuse, better sequencing, or smaller slices
   - **sizing:** over-engineered, under-engineered, or needlessly complicated areas
   - **build-vs-buy:** places where existing repo code or a stable package should replace custom implementation

4. **Recommend the right correction set:**
   - Keep what is already right.
   - **On live production work,** prefer the minimum change that materially improves correctness, simplicity, or leverage.
   - **On pre-production work,** explicitly ask whether a broader canonical redesign, cleanup, or replacement is fundamentally better than a small patch.
   - If the old path is no longer meant to survive, prefer one happy path over hybrid compatibility.

5. **If the plan is already solid, say so explicitly and keep feedback short.**

If repo or code context is missing, state that pattern-reuse and package guidance is provisional rather than pretending it is confirmed.

## Build-vs-Buy order

When evaluating custom work, prefer this order unless context argues otherwise:

1. **Reuse an existing repo pattern, helper, component, flow, or utility.**
2. **Use a stable package** for commodity problems when it reduces maintenance and matches team norms.
3. **Write custom code** only when the behavior is product-specific, existing options are a poor fit, or dependency cost is not justified.

## Pre-Production Expansion Rule

When reviewing features that are not live in production yet — prototypes, pre-release surfaces, internal alphas, anything where the cost of a wider redesign is still cheap:

- **Do not anchor on the smallest patch by default.**
- **Explicitly assess whether this is the right moment** to improve the overall design, remove obsolete seams, or replace a weak pattern entirely.
- **Prefer one canonical implementation with strong tests** over hybrid compatibility that leaves legacy paths alive.
- **Accept fail-fast breakage during development** when it exposes remaining wrong assumptions before launch.
- **If a broader change is better, say so plainly** and explain why the extra scope buys down future maintenance.

## What to look for

- Reinventing a pattern that already exists nearby
- Introducing abstractions before they earn their keep
- Solving today's problem with tomorrow's architecture
- A plan that is too thin for the real risk or blast radius
- Steps that are out of order or missing prerequisite work
- Tests or proof that do not actually cover the risky behavior
- New dependencies that do not buy enough, or missing dependencies where custom code is wasteful
- Extra files, layers, or indirection that can collapse into a smaller change
- Compatibility shims that protect an old path which should instead be deleted before launch
- A "safe" hybrid plan that leaves two happy paths to maintain when one should become canonical

## Output

The output is typically pasted into a PR comment, planning doc, or design thread — keep it self-contained markdown the user can copy without editing. Prefer concise headings:

```markdown
## What Holds Up

## Gaps and Inconsistencies

## Reuse and Existing Patterns

## Simplify / Right-Size

## Package vs Custom

## Recommended Adjustments

## Open Questions
```

Keep each section short. If the plan is already solid, say so explicitly under "What Holds Up" and skip the rest.

## Guardrails

- Do not rewrite the entire plan unless the current shape is fundamentally wrong.
- Do not recommend a new package when the standard library or existing repo utilities are already sufficient.
- Do not recommend custom code just because it feels faster; account for maintenance and team familiarity.
- Prefer the smallest correct change that matches existing patterns for live production work; for pre-production work, prefer the best canonical shape when the broader move is clearly better.
- Do not preserve hybrid compatibility for pre-production code unless there is an explicit requirement to carry the old path.
- Stay concrete: tie critiques to the actual plan and nearby code, not generic best practices.
- **Do not implement during this review unless the user explicitly asks.**

## Design Rationale

Why this skill is structured the way it is:

- **"Inspect adjacent reality before critiquing" is the step that makes this skill work.** Most LLM "fresh eyes" passes critique in the abstract; this one requires repo grounding first. Without it, recommendations become generic best-practice advice that misses repo-specific context.
- **Live-production vs. pre-production split.** The right correction set depends on stage. Live production wants minimum change for material correctness; pre-production should consider canonical redesign over backward-compatible patches.
- **"If the plan is already solid, say so explicitly and keep feedback short"** — prevents critique-for-critique's-sake. The explicit affirmation move counters the LLM tendency to manufacture critiques even when nothing is wrong.
- **Standalone skill, not a mode of `dev-investigate`.** Fresh-eyes applies broadly: PRDs, implementation outlines, refactor plans, branch strategies, architectural proposals, fix plans. Folding it into `dev-investigate` would either duplicate it across sibling skills or cement it as bug-specific when it isn't.
- **Parallel subagents are fair game.** When fresh-eyes wants disjoint surfaces audited in parallel (e.g., one agent on test coverage, one on dependency review), spawning subagents is appropriate — no special permission gate.

## Relationship to os-fresh-eyes

`os-fresh-eyes` (personal-os pack) is this skill's domain-general sibling — the same skeptical stance (**global, subtractive, adversarial, grounded** — the inversion of a first pass's local/additive/agreeable/confident default) applied to plans, ideas, strategy, writing, and workspace conventions instead of code. For non-code artifacts, use it if installed; if it isn't, the stance still applies — this skill's moves generalize further than their dev framing.

The two skills are deliberately self-contained (a buyer may own either pack alone) and share significant language by design. This skill's native tactics map onto the sibling's core lenses: adjacent-code search → *adjacent estate*; the pre-production expansion rule → *commitment gradient*; proof discipline and the failing-test-first pattern → *grounding*. The mapping is what keeps the two coherent without a hard dependency.

> **Propagation note:** improvements to this skill's shared core (the stance, the lens craft, the "if it's solid, say so" discipline) should be propagated to `os-fresh-eyes` when relevant, and vice versa. The duplication is deliberate; drift between the copies is not.

## Related skills

- `os-fresh-eyes` (personal-os pack) — the domain-general sibling for non-code artifacts; see *Relationship* above.
- `dev-investigate` modes (especially `triage-and-fix` and `recurring-hunt`) invoke fresh-eyes in their workflow when a fix plan needs a skeptical second pass.
- `dev-scope-deferral` — when fresh-eyes recommends deferring part of the plan to a follow-up, invoke `dev-scope-deferral` to capture it as a deferred-investigation note.
