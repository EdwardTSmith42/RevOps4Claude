# Offer — Input Context

Common inputs all modes in `offer` expect, plus per-mode specifics. When the user invokes a mode, the mode should have (or ask for) these inputs before producing output.

## Required input (all modes)

- **The offer, business, or offer concept.** For `modes/offer-improve`, this is an existing offer to critique. For `modes/offer-vehicle`, `modes/unique-mechanism`, and `modes/offer-brainstorm`, this is either an existing offer to develop or a business description from which to generate one.

## Strongly preferred (mode-dependent)

### `offer-brainstorm` specifically

- **The avatar / audience profile.** Ideally from `../../os-audience/modes/avatar`. Without an avatar, offers are generic — every brainstormed offer must connect to specific avatar desires, obstacles, and identity factors. Ask for an avatar (or a detailed audience description) before producing output.
- **Any pricing / business model constraint.** If the user wants only high-ticket ($3K+) or low-ticket (<$500) options, bias brainstorming accordingly. Without this, default to a range.

### `offer-vehicle` specifically

- **The avatar / audience profile.** Same reasoning as brainstorm — vehicles need a specific Before-State to anchor Movement Mechanics. Ideally from `../../os-audience/modes/avatar`. Ask for avatar if absent.
- **The core service or capability.** What the business actually does. The vehicle is constructed *around* this capability — the vehicle isn't the capability itself.
- **Optional:** competitive context (what similar vehicles look like), prior pricing, any existing mechanism name or concept.

### `unique-mechanism` specifically

- **The offer or service the mechanism will differentiate.** The mode excavates the mechanism from the existing delivery. Without a delivery to excavate, output is speculative.
- **Some description of how you currently deliver results.** Micro-steps the user follows. If absent, the mode conducts a series of elicitation questions to surface the observable journey. See `unique-mechanism-playbook.md` Section 3 (Excavating and formalizing).
- **Market sophistication estimate.** Informs Promise-Exposure Spectrum calibration. If not provided, the mode asks.
- **Proof material.** Case studies, data, quantitative outcomes. If absent, the mode uses `[INFO NEEDED]` and `[CASE STUDY NEEDED]` placeholders per source convention.

### `offer-improve` specifically

- **The existing offer in enough detail to critique.** Description, deliverables, price, audience, current positioning. If the user supplies only a headline, ask for more.
- **Optional:** performance metrics (conversion rate, CAC, LTV), specific concerns the user has, competitive comparison.

## Optional input (all modes)

- **Prior avatar or market map.** Chained workflow assumes upstream audience + market work. If the user has run `os-audience` and `os-biz-strategy` first, the outputs feed offer directly.
- **Competitive landscape.** Who else serves this audience with adjacent offers.
- **Voice or positioning preferences.** Pulled from prior `os-audience` or `os-biz-strategy/modes/positioning` runs if available.
- **Pricing tier or business model preferences.** Subscription vs. one-time, high-touch vs. self-study, cohort vs. evergreen.

## How to ask for missing input

Ask for the single piece of information that blocks the output most severely. Don't batch-request a questionnaire. Match the model used in `audience` and `biz-strategy`:

Prefer:
> *"I can produce a vehicle spec, but I need a tighter sense of the avatar first. You mentioned 'coaches' — which coaches? (Life coaches at $50K? Business coaches scaling past $10K/mo? Executive coaches at Fortune 500?) A tight avatar grounds the FROM-state — without it the vehicle drifts generic."*

Over:
> *"Please answer the following 15 questions about your business, audience, pricing, competitors, positioning, mechanism..."*

## Grounding checks — applied by every mode

Before shipping output:

1. **Is every field populated with specific, grounded content?** Generic offers signal generic input. Push back or ask for more context rather than generating fluff.
2. **Is the output traceable to input?** If the user asks *"where did this come from?"*, the answer should point at specific input they provided.
3. **If input was inferred (not given), is that flagged?** Use `[INFO NEEDED]` or `[ASSUMED: ...]` when inventing detail rather than burying speculation in plausible-sounding output.
4. **Does the output honor all stated constraints?** Price-ends-in-0/5/9, no "ethical" / "authentic" words, no over-the-top mechanism names, no raise-your-prices recommendation without justification.

## Cross-mode chaining

Offer-design's natural upstream:

1. `../os-audience/modes/avatar` → produces avatar
2. `../os-audience/modes/limiting-beliefs` → produces belief map (for `unique-mechanism`'s Enemy Takedown step)
3. `../os-biz-strategy/modes/market-map` → reads sophistication / awareness / temperature
4. `../os-biz-strategy/modes/positioning` → articulates positioning blueprint
5. `os-offer/modes/*` → construct the offer using upstream context

Offer-design's natural downstream:

- `os-content-discovery` → consumes PPP, unique mechanism, and vehicle spec when surfacing content angles around the offer.
- `os-writing` → primary consumer for finished assets (VSL, landing page, email, longform) built on the completed offer vehicle + unique mechanism.

When the user invokes an offer mode without upstream input, the mode should surface the gap and suggest running the upstream mode first.

## Used by

All `offer` modes.

