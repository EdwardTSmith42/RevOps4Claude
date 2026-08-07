# Blue Ocean — canonical output shapes

`modes/blue-ocean` is modular. Output shape depends on which entry point and which toolkit artifacts the user's question calls for. This template catalogs the canonical shapes for each artifact type.

## Opening output (when the user hasn't named an entry point)

When the user arrives with an open question, open with the entry-point menu:

```markdown
# Blue Ocean Navigator — Let's Start

Where do you want to begin?

1. **Ignite an Idea** — "I have an idea, now what?"
2. **Escape Market Saturation** — "Everyone's doing X. I need a different path."
3. **Tools & Mental Models** — "Show me a Strategy Canvas / ERRC Grid / Six Paths Map."
4. **Expand Demand** — "Who else could buy this?"
5. **Break GTM Bottlenecks** — "Why isn't this strategy landing?"
6. **Investor Readiness** — "Can you help make a deck or model?"

Or just tell me what you're working on or stuck with, and I'll meet you there.
```

Once the user picks (or describes enough that routing is obvious), drop into one of the shapes below.

## Strategy Canvas

Plots the current competitive landscape's value curve vs. the proposed blue-ocean curve.

```markdown
# Strategy Canvas: [Industry / Category]

## Factors of Competition

[List the 5–8 factors the industry competes on — e.g., price, features, service levels, brand, distribution channels, customization, reliability, speed]

## Value Curves

| Factor | Industry Average (Red Ocean) | [Your Offer] (Proposed) | Direction |
|---|---|---|---|
| [Factor 1] | High | Low | ↓ (reduced / eliminated) |
| [Factor 2] | Medium | High | ↑ (raised) |
| [Factor 3] | Low | High | ↑ (raised / created) |
| [Factor 4] | High | High | → (unchanged) |
| [Factor 5] | Not present | Present | 🆕 (created) |

## Divergence Pattern

[One paragraph: where the proposed curve diverges from the industry convergence pattern, and why that divergence is strategically meaningful — does it open new demand, reduce cost, both?]

## Competitive Implication

[What this divergence looks like to a competitor — is it defensible? Can they follow? How long?]
```

## ERRC Grid

The four-lever value-innovation frame.

```markdown
# ERRC Grid: [Offer Name]

## Eliminate
*Which factors the industry takes for granted should be eliminated entirely?*

- [Factor to eliminate, with reasoning about why the industry assumes it's necessary]
- ...

## Reduce
*Which factors should be reduced well below the industry standard?*

- [Factor to reduce, with reasoning]
- ...

## Raise
*Which factors should be raised well above the industry standard?*

- [Factor to raise, with reasoning]
- ...

## Create
*Which factors should be created that the industry has never offered?*

- [Factor to create, with reasoning]
- ...

## Combined Effect

[One paragraph: how the Eliminate/Reduce actions drive cost down AND the Raise/Create actions drive value up — the simultaneous cost-differentiation pattern that makes it a blue ocean.]
```

## Six Paths Map

Six directions to look for uncontested market space. Cover each path, and emphasize the ones with the strongest potential for this offer.

```markdown
# Six Paths Exploration: [Offer Name]

## 1. Alternative Industries
[What industries offer alternative ways to fulfill the same customer need? What can be learned from them? Is there a move from competing in your industry to borrowing from another?]

## 2. Strategic Groups Within the Industry
[What are the major strategic groups (premium / mid / discount, or by specialization)? Is there space by combining elements from multiple groups?]

## 3. The Chain of Buyers
[Who is the buyer, user, influencer? Are they the same? Is there an underserved buyer tier?]

## 4. Complementary Products and Services
[What products or services complement this offer? Is there an integration move or bundle move?]

## 5. Functional-Emotional Orientation
[Does the industry compete functionally or emotionally? Flipping can open space. If functional — can you add emotional appeal? Vice versa?]

## 6. Time / Trend Direction
[Where is the trend heading? Are there early signals that will reshape the market in 2–5 years? Can the offer position ahead of the curve?]

## Strongest Path(s)
[1–2 paths that seem most promising for this specific offer, with reasoning.]
```

## Three Tiers of Noncustomers

```markdown
# Noncustomers — Three Tiers: [Offer Name]

## First Tier — "Soon-to-be" Noncustomers
*Use your industry minimally, will defect to alternatives.*

- Who they are: [description]
- What they currently tolerate: [description]
- What would make them commit: [description]

## Second Tier — "Refusing" Noncustomers
*Aware of your industry but actively reject it.*

- Who they are: [description]
- Why they refuse: [description]
- What reframe might open them: [description]

## Third Tier — "Unexplored" Noncustomers
*In different markets, never considered your industry.*

- Who they are: [description]
- Why they haven't considered this category: [description]
- What bridge would bring them in: [description]

## Primary Target for Expansion
[Which tier holds the biggest blue-ocean opportunity for this offer — often the third tier — with reasoning.]
```

## Adoption Hurdles Map

```markdown
# Adoption Hurdles: [Strategy / Offer Name]

## Organizational Hurdles
[Internal politics, departmental friction, established ways of working. What will resist?]

## Resource Hurdles
[Budget, staffing, tech, capability gaps. What's missing?]

## Motivational Hurdles
[Team buy-in, customer adoption psychology, change fatigue. Where's the motivational deficit?]

## Political Hurdles
[Stakeholder resistance, power structures, vested interests. Who might block this and why?]

## Sequence of Address
[Which hurdle to tackle first, and why. Usually the hurdle whose resolution unlocks the others.]
```

## Strategic Overlay Application (Adversarial Check)

After a primary analysis, apply one or more overlays.

```markdown
# Strategic Overlay Review

## Inverse Thinking
*What if the opposite of each load-bearing claim were true?*

- Claim: [original claim]
- Inverted: [opposite]
- Evidence check: [does the original actually have evidence, or is it inherited assumption?]

(Repeat for each claim the strategy depends on.)

## Skeptical Investor Review
*What would a hard-nosed VC question here?*

- [Question 1 — usually about unit economics or market size]
- [Question 2 — usually about defensibility]
- [Question 3 — usually about team or execution risk]

For each: whether the strategy has a defensible answer.

## Forced Trade-offs
*What is this strategy explicitly not doing, and why?*

- Not doing: [X] — Because: [reasoning]
- Not doing: [Y] — Because: [reasoning]
- Not doing: [Z] — Because: [reasoning]
```

## Key rules

- **Modular means user-directed.** The user picks the artifact they want (explicitly or implicitly through their question). Don't produce the full catalog every time. Produce the right artifact for the moment.
- **Value curves require specific factors and specific positioning.** A Strategy Canvas with abstract labels is theater. Factor names and ratings should be concrete enough that a competitor could recognize them.
- **ERRC moves require cost-differentiation simultaneity.** A pure-Raise-only ERRC is a premium play, not a blue ocean. A pure-Reduce-only ERRC is a discount play. Blue Ocean requires both sides moving at once.
- **Overlays run after primary analysis, not parallel.** Inverse Thinking / Skeptical Investor / Forced Trade-offs are pressure tests on a proposed strategy, not brainstorming modes.
- **Every artifact should have a "so what" moment.** If the output doesn't point at a concrete strategic move, it's analysis for its own sake.

## Grounding check before shipping

1. Does the artifact type match what the user actually asked?
2. Are factors/tiers/hurdles specific to the input offer, not generic?
3. If overlays were applied, did they surface at least one concrete trade-off or inherited assumption?
4. Does the output end with a concrete next move?
