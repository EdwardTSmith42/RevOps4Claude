# Mode: architecture

Part of `dev-plan`. Selected when the work is fundamentally about system shape, boundaries, or risk — not just sequencing.

## Job

Frame the real architecture question, identify constraints/invariants/blast radius, and propose the narrowest viable structural change. Connect the design to proof and rollout strategy.

## Default outputs

- `Problem frame` — the real architecture question in plain language
- `Architecture question type` — see `references/architecture-question-types.md`
- `Invariants and constraints` — what must remain true; what bounds the design
- `Boundary or seam proposal` — the narrowest structural move that solves the problem
- `Blast radius and migration risk` — what gets touched, what could regress, what's hard to roll back
- `Verification or rollout needs` — proof, rollout staging, monitoring

## Run

1. **Classify the question** using `references/architecture-question-types.md`:
   - `boundary`
   - `decomposition`
   - `integration`
   - `migration`
   - `contract risk`
   - `system cleanup`

2. **Name the current shape and the real pain point.** What's actually broken / friction-inducing about today's structure? Be specific — "the boundary between X and Y is fuzzy" beats "the architecture is messy."

3. **Identify invariants, constraints, and non-goals.**
   - Invariants: what behavioral / data guarantees must remain true after the change.
   - Constraints: deadlines, contracts, team familiarity, dependency cost.
   - Non-goals: structural cleanup the change should *not* absorb.

4. **Choose the narrowest architectural move that could solve the problem.** Apply `references/change-design-heuristics.md`. Default to seams over rewrites; default to staying within current boundaries unless there's a real reason.

5. **Size blast radius and rollout risk.** Who depends on this surface? What's the migration path? What's the rollback?

6. **Connect the design to proof, migration, and handoff.** Architecture advice without proof and rollout implications is incomplete.

## When to escalate

- → `scope` mode if the structural move needs to be sequenced into thin slices
- → `prd` mode if the architecture decision warrants a formal PRD with execution discipline
- → `dev-fresh-eyes` for a skeptical second pass on the proposed boundary / seam
- → `dev-investigate latent-hunt` if the architecture question is "what could break that we're not seeing yet"

## Guardrails

- **Don't default to a rewrite when a narrower seam exists.** Most architecture questions are answered by moving a boundary, not redrawing the system.
- **Name non-goals explicitly** so architecture work doesn't accidentally absorb adjacent cleanup.
- **Preserve team readability and continuity** unless a stronger reason exists. Familiarity is real maintenance value.
- **Treat unresolved contract ambiguity as a no-ship risk** on release-critical surfaces.
- **Architecture advice should include proof + rollout implications**, not just structure.
