# Mode: offer-brainstorm

## Purpose

Generate offer options given an avatar (os-audience output) + offer context. Two patterns: **breadth** (10-category catalog of ~40 named offer ideas) and **depth** (Hormozi-style 3 fully-fleshed offers using the Value Equation + obstacles-as-solutions formula + 5 delivery vehicles + sub-offers + scarcity/urgency/guarantee enhancements). Breadth is default. Depth is requested or chained as follow-up after the user picks from breadth.

Deliverable feeds downstream work — market-mapping, offer-vehicle construction, unique-mechanism excavation.

## Triggers

Phrases like: *"brainstorm offers for my audience,"* *"give me offer ideas,"* *"what could I sell to [segment],"* *"generate offer options,"* *"Hormozi offer,"* *"100M offer,"* *"what offers should I build."*

Also triggers when another skill (content-strategy, biz-strategy) needs an offer catalog as input.

## Inputs

See `../references/offer-input-context.md`. This mode benefits most from:
- An avatar or tight audience segment (ideally from `../../os-audience/modes/avatar`)
- Some offer direction or business context (what you already sell, or the domain you're in)
- Optional: pricing tier / business model preferences (high-ticket vs. low-ticket, subscription vs. one-time)

Without an avatar, ask for one — offers are generic without a specific audience.

## Run

### Pattern selection

- **Default — Breadth pattern.** User pastes audience + offer context. Produce the 10-category catalog per `../templates/offer-brainstorm-output.md` (breadth shape).
- **Depth pattern.** User explicitly asks for "Hormozi-style," or "deep on a few offers," or chains in after picking from the breadth catalog. Produce 3 offers + 5 delivery vehicles + sub-offers per `../templates/offer-brainstorm-output.md` (depth shape).
- **Sequential chain.** User asks for both: run breadth first, then depth on selected candidates from the breadth output.

### Breadth pattern run logic

1. **Empathy step (from Hormozi's interview pattern, adapted):** briefly write from the avatar's perspective — 3-5 sentences covering disruption they see, competition they face, dream outcomes they want, obstacles just before/after attaining dream outcomes. Anchors the catalog in the avatar.

2. **Generate the 10-category catalog.** Each category gets multiple named offers. Aim for roughly:
   - DIY / Self-Study: 3-5 offers (signature courses + mini-courses/workshops)
   - Done-With-You / Group Implementation: 3-4 offers (bootcamps + cohorts)
   - Memberships & Continuity: 3-4 offers (ongoing support + accountability pods)
   - High-Level Masterminds & Retreats: 3-4 offers (premium MM + retreats)
   - Done-For-You / White-Label: 3-4 offers (tech/funnel + branding/curriculum)
   - Coaching & Consulting: 3-4 offers (1:1 advisory + ongoing retainers)
   - Licensing & Certification: 2-3 offers
   - Specialized Tools & Resource Bundles: 3-4 offers (templates/swipe + software bundles)
   - Hybrid Offers: 2-3 combined offers
   - Alternative / Non-Obvious: 3-4 offers (creative, non-traditional)

3. **Name every offer.** Credible, concrete, no over-the-top names. Quoted with brief description + 1-2 bullet features.

4. **Filter against Hormozi's four offer-worthy criteria** (massive pain + purchasing power + easy to target + growing market). Any offer that fails the filter is dropped — and listed in the output's Filtered Out section with a one-line reason, so the filter's work is visible and the user gets a chance to react to the cuts. Don't quietly replace a cut offer just to preserve the count. See `../references/offer-frameworks.md`.

5. **Close with Key Takeaways** — 4 observations (pricing range, niche segmentation, stacking opportunities, notable patterns).

6. **Chain hint:** close with pointer to `../../os-biz-strategy/modes/market-map` to read sophistication / awareness / temperature for selected offers.

### Depth pattern run logic (Hormozi-style)

1. **Empathy step** (same as breadth).

2. **Generate 3 best offers** using obstacle-as-solution formula verbatim:

   > *"[AWESOME UNIQUE FRAMEWORK OR PRODUCT NAME]: How to [YAY] without [BOO] even if you [GREATEST OBSTACLE]."*

   Each offer grounded in Hormozi's Value Equation: Dream Outcome × Perceived Likelihood / Time Delay × Effort. See `../../_shared/references/hormozi-value-equation.md`.

3. **Generate 5 delivery vehicles**, each phrased as its own offer (different *ways* the transformation gets delivered — live cohort / self-paced / DFY / hybrid / etc.).

4. **Expand with sub-offers**: for each main offer, 3-5 sub-offers accomplishing important steps of the transformation per the Value Equation.

5. **Enhance with scarcity / urgency / guarantees:**
   - **Scarcity:** limited supply of seats, slots, bonuses, or "never available again"
   - **Urgency:** rolling cohorts, seasonal urgency, ticking clock
   - **Guarantee:** risk-reversal structured as *"If you do not get X result in Y time period, we will Z"* — with a named guarantee (*"The 90-Day Profit Lock Guarantee"*)

### Interactive pause pattern

In the original Hormozi source, the prompt paused between major steps and asked *"Shall I continue to the next step?"* The ChatGPT-era UX assumption adapts to agent context as: produce Step 1 output, then briefly ask if the user wants to proceed to Step 2 rather than dumping all three steps in one response. Preserves the iterative-approval intent.

Apply this pause-between-steps pattern primarily in the depth pattern (where each step's output is substantial), and skip it in breadth pattern (breadth is a single catalog).

## Output

Per `../templates/offer-brainstorm-output.md`. Select shape based on requested pattern (breadth default, depth on request).

After output, point at the natural next moves from where the user is now — typically one to three of: mapping the market for one of these offers (sophistication / awareness / temperature) via `../../os-biz-strategy/modes/market-map`, fleshing out a chosen offer into a full vehicle spec via `offer-vehicle`, or developing the unique mechanism behind a chosen offer via `unique-mechanism`. Pick the pointers that fit the catalog you just produced; phrase each as a short pointer at the next move with the mode name, not a sales pitch.

## Design Rationale

- **Breadth and depth as two patterns, one mode** — the source prompts represent two different brainstorming jobs (catalog vs. deep 3). One mode with two patterns keeps the surface simple. User picks based on where they are in the process. [elicited from source ensemble]
- **Obstacle-as-solution formula** — *"How to [YAY] without [BOO] even if you [GREATEST OBSTACLE]"* preserves Hormozi's specific structural move. The formula forces the offer to address the most-painful obstacle head-on rather than merely advertising the outcome. [stated in source]
- **10-category breadth discipline** — defaults to comprehensive coverage rather than whatever 3-4 offers feel obvious. Forces non-obvious categories (Licensing, Alternatives). [stated as *"comprehensive AND have variety, obvious and non-obvious"*]
- **Hormozi's four offer-worthy criteria as filter** — massive pain + purchasing power + easy to target + growing market. Screens offers that won't scale or convert. [stated]
- **Named offers in quotes** — forces specificity. *"6-Figure Coach Blueprint"* is evaluable as a first-class artifact. *"A coaching program for coaches"* isn't. [elicited from source pattern]
- **Chain to market-map** — stated in source closing: *"Once you've found an offer or offers you'd like to pursue, your next step is to Map Your Market."* Brainstorm → pick → market-map → refine is the natural workflow. [stated]
- **Empathy step before generation** — write from the avatar's perspective before brainstorming. Grounds the offers in the specific audience rather than the analyst's assumption of what offers should be. [stated in Hormozi source]
- **Interactive pause-between-steps adapted for agent context** — the ChatGPT-era UX literal pause is less important than the intent (user should approve before the mode generates more output). Adapted rather than preserved literally. [scaffolding assessment]

## References

- `../references/offer-input-context.md` — input expectations
- `../references/offer-frameworks.md` — Hormozi's four offer-worthy criteria, vehicle-vs-method distinction (Name candidates use vehicle-framing)
- `../references/offer-design-influences.md` — Hormozi, Kennedy, Brunson cited when invoking tradition
- `../../_shared/references/hormozi-value-equation.md` — primary canonical reference for depth pattern
- `../../_shared/references/creative-criteria.md` — quality filter for offer ideas

## Templates

- `../templates/offer-brainstorm-output.md` — both breadth and depth shapes

## Examples

- `../examples/solopreneur-coach-offers.md` — breadth pattern (legacy-flagged seed)
- `../examples/fractional-cmo-offers.md` — breadth pattern (legacy-flagged seed)

Depth-pattern examples grow from real runs rather than ship seeded.
