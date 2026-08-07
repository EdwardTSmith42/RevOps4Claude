# Mode: scope

Part of `dev-plan`. Selected when the question is "what should we build, in what order, and how small can we keep it?"

## Job

Reduce a broad ask into a thin slice with explicit non-goals, milestone order, and proof expectations connected to the work.

## Default outputs

- `Problem statement` — the real ask in plain language
- `Thin-slice scope` — the smallest valuable slice
- `Non-goals` — what's intentionally *not* in scope
- `Milestone order` — sequencing keyed to risk and verification
- `Risks and proof needs` — what could break, what proof catches it
- `Open questions` — unresolved decisions

## Run

1. **Classify the planning need:**
   - `feature`
   - `refactor`
   - `bug plan`
   - `investigation`
   - `prd` (if formal write-up needed → route to `prd` mode after this)

2. **Name the smallest valuable slice.** Apply `references/scope-shaping.md`'s `now / later / unknown yet` split.

3. **Separate goals, non-goals, and deferred follow-ups explicitly.** A plan that can't name what's intentionally *out* of scope is still too broad.

4. **Sequence milestones around risk and verification.** Sequence so each milestone:
   - Reduces a real risk
   - Has clear proof of done
   - Can be reviewed and shipped cleanly on its own

5. **Route through review lanes only if the plan is worth sharpening.** See `references/plan-review-loop.md` — don't add a review lane if the plan is already clear and small.

6. **Return the plan** in the default-outputs shape above.

## When to escalate

- → `architecture` mode if the slice surfaces a structural question (where's the boundary? what invariant?)
- → `prd` mode if the work warrants a formal write-up + RED→GREEN→VERIFY execution
- → `dev-fresh-eyes` for a skeptical second pass on the proposed slice

## Guardrails

- Don't let scope expand into a giant PRD when one milestone or slice would do.
- Don't sequence proof / verification *after* implementation — bake it into the milestone order from the start.
- Don't do false precision in estimates when the real uncertainty is structural; name the structural unknowns instead.
- Prefer a thin milestone that ships cleanly over a broad "do everything" phase.
- When the user revises with explicit product constraints, fold corrections into the active plan before more design work. Never plan against a stale draft.
