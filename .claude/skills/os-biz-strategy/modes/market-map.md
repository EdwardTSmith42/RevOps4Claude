# Mode: market-map

## Purpose

Produce a market mapping for a specific offer and audience: Sophistication level (Schwartz), Awareness level (Schwartz/Brunson), Market Temperature (Brunson Hot/Warm/Cold), plus competitive analysis with counter-positioning recommendations and a final positioning hook. The output is input for landing-page copy, VSL framing, ad messaging, and positioning decisions.

## Triggers

Phrases like: *"map my market,"* *"market mapping analysis,"* *"where does my offer fit in the market,"* *"sophistication and awareness analysis,"* *"competitive positioning analysis,"* *"how do I position against my competitors,"* *"analyze the market for this offer."*

Also triggers when another mode or skill needs a market reading as input (e.g., an offer skill working out counter-positioning).

## Inputs

See `references/market-input-context.md`. This mode specifically needs:

- **Required:** The offer (what, who for, core mechanism, price)
- **Strongly preferred:** An avatar or tight audience segment (ideally from `os-audience/avatar`). Market reading without an avatar is cruder.
- **Strongly preferred:** Some competitive context — who else is in this space, what they claim
- **Optional:** Prior positioning attempts, customer language

If no avatar and no competitive context, ask for at least one before producing output.

## Run

Four analytical sections in order, then recommendations and a hook.

**Step 1 — Market Sophistication Level.** Work through Schwartz's 5 levels (No Competition → One Clear Leader → Expanding → Red Ocean → Saturation & Skepticism). For each level, state whether it applies and why not. Converge on a specific level or between-two-levels reading with grounded reasoning. See `references/market-frameworks.md`.

**Step 2 — Audience Awareness Level.** Work through the 5 stages (Unaware → Problem Aware → Solution Aware → Product Aware → Most Aware). Converge on the audience's current position with grounded reasoning. Different prospects in the same audience may sit at different stages — identify the dominant stage.

**Step 3 — Market Temperature.** Cold / Warm / Hot. Ask how ready is this audience to buy *right now*, independent of how aware they are. A Solution-Aware audience can be Cold (knows solutions exist but not actively looking), Warm (actively comparing), or Hot (ready to commit).

**Step 4 — Competitive & Positioning Analysis.** Five sub-questions:
- Who are the biggest competitors? (Name them, or name the categories of competitor — agency, freelancer, in-house hire, DIY, etc.)
- What messaging patterns dominate? (The common claims the audience has heard many times)
- How can this offer counter-position? (Name the unique mechanism, construct an Unlike Statement)
- What gaps in the market can this offer win?
- What pricing models dominate, and how can this offer use perceived value pricing?

**Step 5 — Strategic Recommendations.** 3–5 concrete next moves the user should take based on the market reading. Actions, not principles. *"Run a 60-day pilot with 2 performance-linked milestones"* is a recommendation. *"Build trust"* is a platitude.

**Step 6 — Final Positioning Hook.** A single sentence positioning hook that captures the unique mechanism + audience desire + differentiator from common alternatives. Sharable as a standalone headline.

See `templates/market-map-output.md` for the canonical output shape.

## Output

Per `templates/market-map-output.md`. Always work through all stages explicitly — rejected levels with reasoning are part of the output's value. Never collapse to a conclusion without showing the reasoning.

After output, include a brief cross-mode suggestion block — separate from the artifact so it doesn't contaminate copy/paste. Pick the one or two adjacent modes that would most sharpen what just shipped, and describe the *effect* the user would get rather than reciting a fixed line. Common next moves from a market-map output: turning the unique mechanism into a visual framework (`models-method`), formalizing the positioning into an Elevator Pitch / NTPV blueprint (`positioning`), or pressure-testing the read and exploring noncustomer expansion (`blue-ocean`).

## Design Rationale

- **Three-framework triangulation (Sophistication + Awareness + Temperature)** — each surfaces a different market variable. Sophistication = how crowded. Awareness = how much they know. Temperature = how ready now. Analyzing all three produces sharper messaging recommendations than analyzing one.
- **Work through all levels/stages explicitly, not just the conclusion** — the reasoning that rejects a level is part of the output's value. Collapsing to a conclusion without the reasoning produces vibes-based analysis that degrades the output's defensibility.
- **Competitive positioning follows the framework analysis** — can't counter-position before knowing where you are on the three frameworks. Ordering matters.
- **Unique mechanism has a name, and the name follows naming discipline** — 2–4 words, specific, claim-worthy, avoid over-the-top modifiers (the "quantum-" / "neuro-" / "hyper-" register that signals hype rather than mechanism). See `references/positioning-concepts.md` on Unlike Statement pattern.
- **Output includes Strategic Recommendations, not just analysis** — the framework reading compiles to concrete next moves the user can take. Without the recommendation layer, the mode produces theater.
- **Final Positioning Hook is sharable standalone** — someone reading only that hook should understand the offer's unique angle. Forces the mode to actually land on a concrete positioning position.

## References

- `references/market-frameworks.md` — primary consumer (Sophistication, Awareness, Temperature, and Strategic Overlays if user wants pressure-testing)
- `references/positioning-concepts.md` — Unlike Statement pattern, NTPV (when mentioning vehicle names)
- `references/biz-strategy-influences.md` — Schwartz, Brunson, Hormozi cited briefly when relevant
- `references/market-input-context.md` — input expectations

## Templates

- `templates/market-map-output.md`

## Examples

- `examples/legacy-fractional-cmo-market-map.md` — shape-demonstration example (Fractional CMO offer for a stalled-growth founder avatar). Useful for seeing what cumulative depth looks like across all four sections at once; the template carries the structural teaching.

