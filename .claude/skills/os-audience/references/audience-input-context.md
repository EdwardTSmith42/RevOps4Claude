# Audience — Input Context

The common inputs all modes in `audience` expect. When the user invokes a mode, the mode should have (or ask for) these inputs before producing output.

## Required input

- **The offer or business.** What the product/service is, what it does, who it's for at a high level, what the core mechanism is. Enough detail that specific psychographic fields can be populated concretely — not "a coaching business" but "a 1:1 coaching offer for solopreneur coaches scaling past $10K/month who want to productize without losing client results."

## Strongly preferred input

- **The audience segment.** A specific sub-group within the broader "who it's for" — a named niche, role, or life-stage. "Coaches" is too broad. "Solopreneur coaches stuck at $10K/month MRR for 18+ months" is actionable.
- **Existing research or customer language.** Reviews, testimonials, objections heard on sales calls, onboarding surveys, churn reasons, community posts. Grounds every mode in actual prospect voice rather than inferred voice. Modes will flag when outputs are running on inference rather than grounded research.

## Optional input (mode-dependent)

- **Business model / pricing tier.** Informs Hormozi Value Equation mapping in `dmo` and `core-transformation`.
- **Prior avatar or audience profile.** If the user has already run `modes/avatar`, other modes can consume that output as input rather than re-researching from scratch. This is the primary chaining pattern — avatar first, then zoom modes against it.
- **Competitive context.** Which other offers the audience considers, and what they've tried before. Sharpens `modes/avatar` Market Context section.
- **Awareness stage estimate.** Where the prospect sits on Schwartz's 5-stage ladder (see `psychographic-frameworks.md`). Useful for all modes but especially `modes/dmo` and future content-strategy work.

## How to ask for missing input

If the user invokes a mode without enough input, ask briefly and specifically. Do not ask for a wall of questions. Ask for the one piece of information that blocks the output most severely. Prefer:

> "I can run the avatar mode, but I need a tighter audience segment first. You mentioned coaches — which coaches specifically? (Life coaches scaling past $10K? Business coaches under $100K? Something else?) Once I know who we're profiling, I can produce the avatar."

Over:

> "Please answer the following 12 questions about your business, audience, pricing, competitors, customer language, prior research..."

The latter is friction. The former respects that the user is probably starting from a specific moment of need and can surface additional context as requested.

## Grounding check — applied by every mode

Every mode should ask itself, before shipping output:

1. **Is every field populated with specific, grounded content?** Thin fields signal thin research.
2. **Is the output traceable to input?** If the user asks "where did X come from?", the answer should be "from your input about Y" or "from the research you pasted."
3. **If input was inferred (not given), is that flagged?** When a mode guesses an audience attribute, the guess should be marked as such — so the user can correct.

## Used by

All `audience` modes.
