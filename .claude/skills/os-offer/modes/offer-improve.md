# Mode: offer-improve

## Purpose

Strategic review of an existing offer, surfacing specific evidence-based opportunities to increase profitability — via pricing, positioning, product design, bundling, audience targeting, or operational leverage. Produces a 6-section analysis ending with 3-5 prioritized recommendations, each grounded in buyer psychology, pricing theory, or competitive advantage.

Optional financial-benefits lens when the offer lacks clear revenue/cost-savings articulation.

## Triggers

Phrases like: *"improve my offer,"* *"review my offer,"* *"make my offer more profitable,"* *"what's wrong with my offer,"* *"strategic offer review,"* *"profit levers,"* *"offer critique,"* *"offer audit,"* *"how do I reposition this offer."*

Also triggers when another skill (content-strategy, biz-strategy) surfaces offer-level friction that warrants a full review.

## Inputs

See `../references/offer-input-context.md`. This mode needs:

- **Required:** the existing offer in enough detail to critique. Description, deliverables, price, audience, current positioning.
- **Strongly preferred:** performance metrics if available (conversion rate, CAC, LTV, churn)
- **Strongly preferred:** specific concerns the user has ("not converting," "revenue plateau," "feels undifferentiated")
- **Optional:** competitive comparison, prior avatar / positioning work

If the user supplies only a one-line offer description, ask for more before producing output. Thin input produces thin review.

## Run

Six-section analysis per `../templates/offer-improve-output.md`:

**1. Offer Summary.** Paraphrase the offer as understood. Note any ambiguities in the user's description rather than glossing.

**2. Market Fit.** Honest read of who this is for, what they're struggling with, what outcome they're truly seeking, where the offer under- or over-delivers. Honesty is the whole value of this section — if the stated audience is too broad or the outcome is fuzzy, flag it.

**3. Value + Differentiation.** What makes this unique or credible. What could be better articulated. What prospects remain unsure about. Whether the offer has a named Unique Mechanism — if not, flag as a differentiation opportunity and point at `unique-mechanism` mode.

**4. Profit Levers.** Direct analysis across four levers:
- **Pricing power** — current pricing, value gap, ceiling (if supported)
- **Cost of delivery** — where time/effort goes, bottlenecks, standardization opportunities
- **LTV / CAC leverage** — acquisition cost, lifetime value opportunities, ratio health
- **Packaging / upsell** — tiering opportunities, natural upsells, cross-sells

**5. Recommendations to Increase Profitability.** 3-5 prioritized, specific, justified recommendations. Each includes:
- Clear heading (the action, not the topic)
- Specific action — not "improve X"
- Rationale grounded in audience psychology, pricing theory, or competitive advantage
- Expected directional impact

**6. Optional Next Steps.** Additional actions or data that would deepen the review. Include only when there's a genuinely useful next move.

### Financial-benefits lens (optional)

When the offer lacks clear financial-outcome articulation (buyer can't easily calculate ROI), run this additional lens:

- Does the offer clearly help buyers make or save money?
- If unclear, 5-minute brainstorming exercise:
  1. What does the buyer currently spend/lose by not having this offer?
  2. What revenue or cost-savings would they realize with it?
  3. Over what timeframe does the lift compound?
  4. Conservative 12-month financial impact?
  5. One-sentence articulation (*"Every month you don't solve [root problem], you're leaving $X in [revenue/savings] on the table"*)
- Repositioning recommendation tying offer to financial outcomes

Apply this lens when B2B or high-consideration buyers need ROI justification. Skip for consumer / impulse offers where financial framing would feel forced.

### Constraints throughout

- **Don't recommend "raise your prices" without justification.** Every pricing recommendation must be grounded in positioning, scarcity, or transformation value. Source-stated constraint.
- **Avoid generalities.** Every recommendation must be specific and contextualized. No "improve your marketing" or "strengthen your brand" — name the specific move.
- **Stay grounded in offer mechanics, not surface messaging.** Messaging tweaks produce temporary lift. Mechanical changes (pricing, packaging, delivery, audience) produce durable improvement.
- **Tone: sharp, decisive, professional.** User is unoffendable and wants the best outcome. Critique honestly.
- **Hybrid analytical perspective** — pricing psychology (value perception) + full-funnel marketing (acquisition path) + behavioral economics (decision friction). Each section reflects at least one lens.

## Output

Per `../templates/offer-improve-output.md`. Six required sections + optional financial-benefits lens.

After output, point at the natural next moves from where the user is now — typically one or two of: developing the unique mechanism the offer lacks (if Section 3 flagged that gap) via `unique-mechanism`, re-speccing the offer as a full vehicle via `offer-vehicle`, brainstorming adjacent or complementary offers via `offer-brainstorm`, or checking the market positioning of the improved offer via `../../os-biz-strategy/modes/market-map`. Pick the pointer that fits the recommendations you just made; phrase as a short pointer at the next move with the mode name, not a sales pitch.

## Design Rationale

- **"Don't recommend raise-your-prices unless supported"** — source-stated. Easy recommendation without justification reads as lazy. Forces value-justified pricing thinking. [stated]
- **Hybrid analytical perspective (pricing psychologist + full-funnel marketer + behavioral economist)** — stated as composite role. Each lens sees different friction: pricing psychology → value perception, funnel marketing → acquisition path, behavioral economics → decision friction. Missing a lens produces shallow analysis. Preserved as Design Rationale note rather than persona-cosplay. [stated]
- **Stay grounded in offer mechanics, not surface messaging** — stated. Messaging tweaks produce temporary lift. Mechanical changes produce durable improvement. Surface-level recommendations feel actionable but don't compound. [stated]
- **Specific, contextualized recommendations only** — stated: *"Avoid generalities. Every recommendation must be specific and contextualized."* Forces the mode past the safe-abstract output into concrete moves. [stated]
- **Assess for Blue Ocean opportunities in Section 3** — stated as one of the 7 analysis steps. Competitive positioning is an offer-level lever, not just a marketing-level one. [stated]
- **Financial-benefits lens optional, not required** — some offers (consumer, impulse, low-ticket) don't benefit from ROI framing, where applying it produces forced justifications. Gated by context. [elicited]
- **Six-section output structure** — preserved from source as a complete strategic review shape. Each section answers a specific diagnostic question. Skipping sections produces uneven analysis. [stated]

## References

- `../references/offer-input-context.md` — input expectations
- `../references/offer-frameworks.md` — vehicle-vs-method (many "improve" recommendations are about building a Vehicle where only a Method exists), root-problem-vs-symptoms (surface issues often trace to root-level design flaws), high-ticket psychology
- `../references/vehicle-theory.md` — cross-references when recommending vehicle-level changes
- `../references/unique-mechanism-playbook.md` — cross-references when flagging mechanism gap
- `../../_shared/references/hormozi-value-equation.md` — the four-lever check in Value + Differentiation section
- `../../_shared/references/positioning-concepts.md` — Unlike Statement / NTPV when surfacing positioning gaps

## Templates

- `../templates/offer-improve-output.md` — six-section review shape with optional financial-benefits lens

## Examples

Examples grow from real runs rather than ship seeded.
