# Market Frameworks — Strategic Reference

Domain reference for strategic market analysis. Loaded primarily by `market-map` and `blue-ocean` modes. Canon frameworks from direct-response / conversion psychology tradition (Schwartz, Brunson) and strategic consulting tradition (Kim, Mauborgne, Osterwalder).

## Schwartz's 5 Stages of Market Sophistication

Eugene Schwartz (*Breakthrough Advertising*, 1966). Each market moves through sophistication stages over time as competitors enter. Messaging that targets the wrong stage fails — claiming novelty in a saturated category looks naïve. Claiming differentiation in a nascent category confuses the audience.

| Stage | Description | Messaging implication |
|---|---|---|
| **1 — No Competition (New Market)** | Audience unaware the solution category exists | Educate and introduce the category, name the solution space |
| **2 — One Clear Leader** | One dominant solution, first-mover advantage | Audience hasn't seen competitors — position as the obvious answer |
| **3 — Expanding Market (Competitive, Not Saturated)** | Multiple competing offers exist | Differentiate through features or unique mechanisms |
| **4 — Red Ocean (Highly Competitive, Commoditized)** | Market aware of all solutions | Strong brand, unique positioning, or emotional storytelling to stand out |
| **5 — Saturation & Skepticism** | Overwhelm and distrust | Radical differentiation or category-reframing — old claims don't land |

A market's stage is a function of when you're showing up, not of the category's inherent newness. Even well-established categories can have niche sub-markets at Stage 1 or 2.

## Audience Awareness — 5 Stages

Canonical content lives at `_shared/references/schwartz-awareness-ladder.md` — Schwartz/Brunson canon, shared with `os-audience` for the same purpose. The shared reference covers the five stages, messaging implications, and malleability notes.

When to use in biz-strategy modes:
- `modes/market-map` — dedicated "Audience Awareness Level" section works through all five stages explicitly as analytical discipline.
- `modes/positioning` — calibrates Elevator Pitch tone and Value Articulation Story to the dominant awareness stage.

Sits alongside two orthogonal readings in this skill — **Market Sophistication** (category maturity, above) and **Market Temperature** (readiness-to-buy, below). The three frameworks triangulate different market variables.

## Brunson's Market Temperature — Hot / Warm / Cold

Russell Brunson (*DotCom Secrets*, *Expert Secrets*). A situational-readiness cut that complements the awareness ladder. Awareness asks *what do they know?* Temperature asks *how ready are they to buy right now?*

| Temperature | State | Messaging implication |
|---|---|---|
| **Cold** | New to your offer, don't know you | Heavy education, content marketing, trust-building |
| **Warm** | Familiar with concept, interacted with similar offers, not committed | Strong differentiation, clear messaging, proof |
| **Hot** | Actively looking for a solution, close to buying | Urgency, risk-reversal (time-limited bonuses, guarantees) |

The three frameworks (Sophistication, Awareness, Temperature) triangulate different market variables:
- **Sophistication** = how crowded is the category?
- **Awareness** = how much does the buyer know?
- **Temperature** = how ready is the buyer *now*?

Different readings produce different messaging recommendations. Analyzing all three is the primary craft move of `market-map`.

## Blue Ocean Strategy — Kim & Mauborgne Toolkit

W. Chan Kim and Renée Mauborgne (*Blue Ocean Strategy*, INSEAD, BOGN). Strategic frameworks for creating uncontested market space rather than competing in crowded ones.

### Strategy Canvas

A visualization comparing the value curves of you vs. competitors across the factors the industry competes on. Highlights where your offering differs from the competitive convergence pattern.

**Output:** two or more value curves plotted across shared factors. Divergence from the industry norm is the strategic signal.

### ERRC Grid

Four value-innovation levers used in combination:

| Action | Question | Effect |
|---|---|---|
| **Eliminate** | Which factors the industry takes for granted should be eliminated? | Cost reduction |
| **Reduce** | Which factors should be reduced well below the industry standard? | Cost reduction |
| **Raise** | Which factors should be raised well above the industry standard? | Value elevation |
| **Create** | Which factors should be created that the industry has never offered? | New value |

Eliminate/Reduce drive cost down. Raise/Create drive differentiation up. Both together produce a "blue ocean" — differentiation *and* low cost simultaneously.

### Six Paths Framework

Six directions to look for uncontested market space:

1. Look across **alternative industries** (not just competitors in the same industry)
2. Look across **strategic groups** within the industry
3. Look across the **chain of buyers** (user ≠ purchaser ≠ influencer)
4. Look across **complementary products and services**
5. Look across the **functional-emotional orientation** (if industry competes functionally, emotional appeal opens space, and vice versa)
6. Look across **time** (where is the trend heading? act ahead of it)

Each path surfaces different latent demand.

### Three Tiers of Noncustomers

Customers you don't currently serve, sorted by distance from your market:

- **First tier — "Soon-to-be" noncustomers**: use your offering minimally, will defect to alternatives
- **Second tier — "Refusing" noncustomers**: aware of your industry, actively reject it
- **Third tier — "Unexplored" noncustomers**: in different markets, never considered your industry

The biggest blue oceans often live in the third tier — audiences no competitor is currently serving.

### Buyer Utility Map + Blue Ocean Idea Index

Utility Map: tests whether an idea delivers value across six stages of the buyer experience (purchase, delivery, use, supplements, maintenance, disposal) on six utility levers (productivity, simplicity, convenience, risk, fun/image, environmental friendliness). Finds the blocks in the current market.

Idea Index: tests new ideas against four criteria — utility, price, cost, adoption hurdles.

### Price Corridor of the Mass

Pricing method aimed at mass capture rather than niche premium. Three steps: identify the price corridor of the mass (what substitutes and alternatives charge), specify the level within the corridor, set the level within the corridor that achieves your profitability goals.

### Adoption Hurdles Map

Four barriers to strategic execution: **organizational** (internal politics), **resource** (budget, staffing), **motivational** (team buy-in), **political** (stakeholder resistance). Address each explicitly before rollout.

### Tipping Point Leadership + Fair Process

Execution frameworks. Tipping Point Leadership focuses on leverage points (the 20% of actions producing 80% of change). Fair Process engages stakeholders through Engagement, Explanation, and Expectation clarity.

## Strategic Overlays — Adversarial Quality Checks

Not divergent brainstorming. Adversarial pressure-tests applied to proposed strategies to detect fragility before it's real.

### Inverse Thinking

Flip every assumption. For each load-bearing claim, ask: *what if the opposite were true?* Reveals which claims actually have evidence vs. which are inherited assumptions.

### Skeptical Investor Review

Role-play a hard-nosed VC reading the strategy. What would they question? Where would they press on unit economics, market size, defensibility, team risk? Anything the strategy can't defend at this level isn't ready.

### Forced Trade-offs

Blue Ocean rhetoric often implies you can have everything (cost down AND differentiation up). Real strategy requires trade-offs. For each proposed move, name what you're explicitly *not* doing and why. Unexamined trade-offs are where strategies quietly break.

Overlays run *against* a proposed strategy, not in parallel. Apply them after the primary analysis.

## Used by

- `modes/market-map` — primary consumer of Sophistication + Awareness + Temperature + Competitive/Positioning
- `modes/blue-ocean` — primary consumer of Kim/Mauborgne toolkit + Strategic Overlays
- `modes/positioning` — may reference Awareness and Temperature when calibrating positioning
- `modes/models-method` — less direct, may reference Schwartz/Brunson when the model being built needs to target a specific awareness stage

## Canonical references

- Schwartz, *Breakthrough Advertising* (1966) — Sophistication ladder
- Brunson, *DotCom Secrets* / *Expert Secrets* — Market Temperature
- Kim & Mauborgne, *Blue Ocean Strategy* (INSEAD / BOGN) — full toolkit and overlays
