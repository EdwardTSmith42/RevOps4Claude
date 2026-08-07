# Mode: dmo (Desires, Motivators, Obstacles)

## Purpose

Produce a four-section audience analysis focused on the motivational architecture: what the prospect desires, what internally and externally drives those desires, and what obstacles block them — specifically the obstacles at each temporal stage (before the offer, during engagement, after fulfillment).

The distinguishing craft move is the Before/During/After obstacle framing. Most obstacle analysis flattens pain into a single list. The temporal split reveals post-purchase risks (maintenance problems, success-contingent problems, identity problems) that flat analysis misses.

## Triggers

Phrases like: *"identify desires, motivators, and obstacles"*, *"DMO analysis"*, *"what drives and blocks my customer"*, *"map my audience's motivations and blockers"*, *"what obstacles will my customer hit"*. Also useful when the user wants a motivational deep-dive without the full avatar portrait.

## Inputs

See `references/audience-input-context.md`. DMO benefits from:
- An avatar already produced by `modes/avatar` (ideal — gives the mode a named person to work against)
- The offer and its fulfillment mechanism — DMO needs to understand *what the prospect experiences inside the offer* to map During-stage obstacles
- Business model / pricing — the Before-stage obstacles differ for a $97 product vs. a $10K offer

## Run

Four sections in order.

**Section 1 — Core Desires & Motivators.** Identify:
- Primary desires (tangible payoffs — financial, status, transformation, security, ease, pleasure)
- Hidden emotional triggers and identity factors (subconscious material the prospect wouldn't name publicly)
- How the prospect defines success and an ideal outcome (first-person — their definition, not yours)

**Section 2 — Dream Outcomes via Hormozi's Value Equation.** See `references/psychographic-frameworks.md` for the Value Equation. Cover:
- The ultimate transformation (life or business after the goal is achieved)
- Aspirational goals — what they daydream about but don't verbalize (often slightly embarrassing or "too big" to say out loud)
- **External drivers** (circumstantial / visible-to-others reasons they want this)
- **Internal drivers** (identity / self-concept reasons)

Both external and internal drivers required — any durable desire has both. Missing either layer produces thin articulation.

**Section 3 — Obstacles & Pain Points (Before / During / After).** The distinguishing move.

- **Before — What's stopping them now.** Knowledge gaps, time constraints, self-doubt, skepticism, resource limits, priors. The standard obstacle list.
- **Before — The precipitating moment.** What happened last week, last quarter, or at 3 AM that made them start searching for a solution. Specific triggering event.
- **During — Inside the offer.** Execution friction (overwhelm, perfectionism, technical hurdles), relational friction (accountability, asking for help), belief friction (*"what if I'm the exception who can't do this"*).
- **After — Secondary obstacles post-fulfillment.** Maintenance problems (skill requires ongoing effort). Success-contingent problems (new problems the solution creates — "now I have to hire someone"). Identity problems (they don't know who they are without the original pain).

The After stage is the most commonly missed. Include it — it's where churn, referral gaps, and upsell opportunities live.

**Section 4 — Market Frictions & Psychological Roadblocks.**
- Why they hesitate or delay (the friction pattern)
- Common objections in voice — stated, then what's underneath
- Beliefs and industry misconceptions blocking action
- External factors (competition, economic trends, peer influence, cultural context)

See `templates/dmo-output.md` for the canonical shape.

## Output

Per `templates/dmo-output.md`. Four sections in order, each section fully populated.

After output, brief cross-mode suggestion block. Examples:
- "The Internal-driver material often surfaces Big Domino beliefs — run `limiting-beliefs` to dismantle them formally."
- "For the full psychographic portrait this DMO was built against, run `avatar` if you haven't."
- "To turn the Dream Outcome into a nameable FROM/TO shift, run `core-transformation`."

## Design Rationale

- **Before / During / After obstacle framing** — pain has a temporal arc, not a single point. The temporal split is the mode's main craft move. [elicited from source structure]
- **Internal + External drivers, both required** — any durable desire has both a circumstantial root (what others will see, what it buys) and an identity root (who it makes them). Analyses that only surface one layer produce brittle marketing input. [elicited]
- **Hormozi's Value Equation as the Dream Outcome spine** — makes the dream-outcome articulation structured across four variables (Dream × Likelihood / Time × Effort) rather than just "what they want." Every offer move touches these four levers. [stated in source]
- **Aspirational goals they don't verbalize** — the strongest motivations are often the ones the prospect is embarrassed to state. Surfacing these is the mode's psychographic depth check. [elicited]
- **Precipitating moment (Before)** — the trigger event that moved the prospect from passive to active searching is high-leverage marketing material. Standard obstacle lists miss this. [elicited]
- **After-stage obstacles are non-optional** — the mode specifically enforces After-stage coverage because most analysis skips it. Post-fulfillment material feeds churn prevention, referral enablement, and upsell design. [elicited]

## References

- `references/psychographic-frameworks.md` — Hormozi's Value Equation, Behavior → Belief → Identity Driver
- `references/buyer-psychology-beliefs.md` — Section 4 (Market Frictions & Psychological Roadblocks) overlaps with the four-category belief taxonomy
- `references/audience-input-context.md` — input expectations
- `references/audience-insight-influences.md` — Hormozi cited here, others referenced briefly when relevant

## Templates

- `templates/dmo-output.md`
