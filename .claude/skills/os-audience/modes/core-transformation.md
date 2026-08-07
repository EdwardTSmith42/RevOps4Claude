# Mode: core-transformation

## Purpose

Articulate the core transformation an offer produces for the prospect — a specific FROM/TO shift — plus the non-obvious insights that make the articulation sharp rather than generic. The central deliverable is a sharable FROM/TO statement. The supporting sections (Key Benefits, Non-Obvious Insights, Expert Principles, Potential Challenges) frame how the transformation is understood.

## Triggers

Phrases like: *"what transformation does my offer produce"*, *"articulate the transformation"*, *"what FROM/TO does my offer represent"*, *"find my core transformation"*, *"what does my audience transform into"*. Also triggers when the user shares an offer or URL and asks what it's *really* selling.

## Inputs

See `references/audience-input-context.md`. Core-transformation specifically benefits from:
- **Any concrete input about the offer** — content, notes, a landing page, a URL, a business description. The mode adapts to what's available.
- An avatar already produced — the transformation is AVATAR-specific (the FROM state is their current reality, the TO state is what changes for them). Without an avatar, the mode can still run but will inflate the abstractness of the FROM/TO.

If given a URL, the mode can fetch the page (if web access is available) to work from actual content rather than assumed content.

## Run

Five steps, in order.

**Step 1 — Identify themes.** Read the input carefully. List the main themes, topics, and solutions present. Neutral reading, no judgment yet.

**Step 2 — Identify the core transformation.**
- Determine the primary problem the offer solves for the prospect.
- Brainstorm multiple candidate transformations — not just the obvious one, the non-obvious ones too.
- Identify the most impactful transformation that aligns with the offer's specifics. This is usually not the most superficial one.

**Step 3 — Articulate the FROM/TO statement.** In the canonical arrow-bullet format:

```
FROM:
→ [current state 1 — circumstantial, grounded]
→ [current state 2 — felt experience]
→ [current state 3 — identity/self-concept]

TO:
→ [desired state 1 — circumstantial]
→ [desired state 2 — felt experience]
→ [desired state 3 — identity they become]
```

Three-layer minimum. At least one circumstantial line, one felt-experience line, one identity-shift line. A FROM/TO that only moves the prospect between circumstances (*"from no money to more money"*) is not a transformation — it's a purchase outcome. Durable transformations shift identity.

**Step 4 — Surface Non-Obvious Master-Level Insights.** At least three. Each insight is something the offer owner *hadn't already said*, or an angle the prospect *hasn't considered*. Pass each candidate through the "huh" test:

> *Would a reader say "huh, I hadn't thought of it that way" — or is this a restatement of something already obvious from the input?*

If it fails the huh test, cut it and look harder. The discipline is explicitly anti-cliche. (This test comes from the source prompt's own directive: *"Can I return results that are less cliche?"* — preserved as a design move.)

**Step 5 — Frame supporting structure.** Two more supporting sections:

- **What the Experts Say** — brief, one sentence per named expert. Reference, don't lecture. See `references/audience-insight-influences.md`. Typical touchpoints: Donald Miller (FROM/TO storytelling), Hormozi (value equation), Brunson (transformation positioning), Porterfield (micro-transformation in lead magnets), Clark (education-first positioning). Only cite experts whose principles genuinely apply to the specific transformation. Don't name-drop for coverage.
- **Potential Challenges to the Transformation** — audience limiting beliefs that will resist the transformation, each paired with brief counter-framing. See `references/buyer-psychology-beliefs.md`. This is the audience-side. Full counter-framework work lives in `modes/limiting-beliefs`. Don't duplicate that mode's depth here.

See `templates/core-transformation-output.md` for the canonical output shape.

**Anti-cliche self-check before shipping.** Re-read every line and ask: *"Is this something any competent AI would produce about any offer, or does it specifically show through the input?"* If the line could apply to any offer, rewrite it against the specifics. This check runs on the entire output, especially the FROM/TO statement and the Non-Obvious Insights.

## Output

Per `templates/core-transformation-output.md`. Do NOT include Ways-to-Communicate or lead-magnet-strategy sections — those belong in the future content-strategy skill, not this mode.

After output, brief cross-mode suggestion block. Examples:
- "To formalize the Potential Challenges into dislodge-ready counter-frameworks, run `limiting-beliefs`."
- "To anchor this transformation in a specific named avatar (sharper FROM state), run `avatar` first."
- "To map the full motivational arc behind the TO state, run `dmo`."

## Design Rationale

- **FROM/TO as the headline** — the transformation statement is the mode's central deliverable. Everything else supports it. If a reader only sees the FROM/TO section, they should understand the transformation. [elicited]
- **Arrow-bullet format ("→") for FROM/TO states** — preserved verbatim from source. The multi-line arrow structure lets each dimension stand alone without tabular overhead, and the visual cadence reinforces the sense of motion. [stated in source]
- **Three-layer FROM/TO minimum (circumstantial / felt / identity)** — without the identity layer, the output is a purchase outcome, not a transformation. The identity shift is what makes the transformation durable and emotionally resonant. [elicited]
- **Non-obvious insights pass the "huh" test** — the source prompt emphasizes *"aha-moment level insights, not just front-of-the-brain stuff"* and *"non-obvious or master-level insights"*. The discipline is surfacing what the offer owner hasn't already said. [stated in source]
- **Anti-cliche self-check** — source prompt includes the directive *"Can I return results that are less cliche and more to the instructions?"* Preserved as an explicit self-check step before shipping. Maps onto the broader era-tells work from the voiceprint conversion. [stated in source]
- **Experts cited briefly** — the source named Porterfield, Hormozi, Brunson, Clark. One sentence per expert, applied specifically to the transformation. No biography, no unnecessary name-dropping. [elicited]
- **Potential Challenges at audience-side only** — full belief-dislodge work lives in `modes/limiting-beliefs`. This mode surfaces challenges, but it doesn't duplicate the dismantling work. [elicited — avoids cross-mode bleed]
- **Ways-to-Communicate and lead-magnet tail dropped** — source prompt extended into content-strategy material. That belongs in a future content-strategy skill, not audience. Keeps this mode focused. [classification decision]

## References

- `references/buyer-psychology-beliefs.md` — belief-behind principle (feeds Potential Challenges section)
- `references/psychographic-frameworks.md` — Hormozi's Value Equation (implicit in FROM/TO), Miller's FROM/TO tradition
- `references/audience-insight-influences.md` — named experts for the "What the Experts Say" section
- `references/audience-input-context.md` — input expectations

## Templates

- `templates/core-transformation-output.md`
