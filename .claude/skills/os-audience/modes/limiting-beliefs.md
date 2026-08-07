# Mode: limiting-beliefs

## Purpose

Produce a full belief-based marketing asset set for a specific offer: an NLP deconstruction of the prospect's psychological landscape, 10 direct-response sales bullets, and four tables of limiting beliefs (Big Domino / Vehicle / Internal / External) with counter-frameworks that dislodge each belief.

This is downstream research — it feeds webinars, VSLs, lead magnets, email launches, landing-page copy, ad copy. It's raw material for a drafter, not finished copy.

## Triggers

Phrases like: *"map limiting beliefs"*, *"what's blocking my customer from buying"*, *"identify objections"*, *"dismantle buyer psychology"*, *"build belief-shifting content"*, *"what are my audience's beliefs about X"*, *"what limiting beliefs does my avatar have"*.

Also triggers when another skill (VSL writing, landing page, webinar script) needs belief input.

## Inputs

See `references/audience-input-context.md`. This mode specifically benefits from:
- An avatar already produced by `modes/avatar` — grounds the belief work in a named person
- Existing customer language (objections heard on sales calls, churn reasons, community complaints)
- The offer's core mechanism

Without at least a described offer and a named segment, ask for these before producing output.

## Run

Three steps, in order. Order matters: each step feeds the next.

**Step 1 — Deconstruction of Psychological Triggers.** Run the 20-field NLP excavation in `references/nlp-psychological-triggers.md`. Fill every field with specific, grounded content. Thin fields weaken everything downstream.

The branding fields (*Brand The Mistaken Belief*, *Brand The Primary Cause*, *Brand The Primary Solution*) are critical — name each dynamic in 2–4 words so it becomes argumentable. *"The Productivity Trap"* is easier to work with than *"that thing where you feel busy but aren't making progress."*

**Step 2 — 10 Sales Bullets (NLP).** Synthesize the deconstruction into 10 emotionally charged bullets with strict formatting:

- Start with a verb ending in "s" (*Uncovers*, *Delivers*, *Shows*, *Unlocks*, *Crushes*)
- ≤18 words per bullet
- End with a variant of *so you can / that lets you / that empowers you to / that allows you to* plus a concrete real-world benefit
- Visceral, direct-response language — conversational and thought-provoking

Don't paraphrase the formatting rules. The cadence is the craft. Relaxing it degrades output.

**Step 3 — Limiting Beliefs tables.** Return four tables, one per belief category, with columns: **Belief** / **Deeper Belief** / **Counter-Framework** / **Strategy**.

- **Big Domino:** exactly 2 beliefs, each large enough to anchor a 90-minute webinar. Core worldview shifts, not micro-objections.
- **Vehicle:** 5 or more (up to 10–20 when specificity serves) — skepticism about the method/system/process.
- **Internal:** 5 or more — self-doubt, perceived inadequacy.
- **External:** 5 or more — time, money, support, economy, environment.

For each belief:
- **Belief** — the exact surface belief, phrased as the prospect would think it
- **Deeper Belief** — the belief-behind-the-belief (not a restatement). See `references/buyer-psychology-beliefs.md`.
- **Counter-Framework** — the name/structure of the dislodge model. Must *dislodge* (reframe, replace), not *counter* (argue against).
- **Strategy** — the *what* and *why*. Reveal the strategy, withhold the tactics (reveal-and-restraint — see `references/buyer-psychology-beliefs.md`).

All cells filled. No fluff, no disclaimers, no commentary between tables.

See `templates/limiting-beliefs-output.md` for the canonical output shape.

## Output

Per `templates/limiting-beliefs-output.md`. Three sections in order: Deconstruction, Sales Bullets, Limiting Beliefs tables.

After the output, include a brief cross-mode suggestion block. Examples:
- "You might also benefit from `avatar` if you haven't profiled this audience yet — the belief work is sharper when anchored in a specific named person."
- "Consider `core-transformation` to articulate the FROM/TO shift your offer produces — the Big Domino beliefs often map directly to that transformation."

## Design Rationale

All six rationale items below are stated explicitly in the source prompt's preamble — the original author surfaced the design thinking clearly.

- **Deconstruction precedes bullets and belief tables** — forces the psychological research up front, grounded in the specific offer, before compressing into marketing artifacts. Tables written without the deconstruction regress to generic objections.
- **Three sections, not one** — the deconstruction is raw material, the bullets are the atomic content unit, the tables are the belief-shifting strategy. Each serves a different downstream use. Combining them loses separation of concerns.
- **Frameworks dislodge, not counter** — stated verbatim by source: *"Frameworks must dislodge the belief, not just counter it — reframe or replace with something more empowering."* A counter argues. A dislodge reframes. See `references/buyer-psychology-beliefs.md`.
- **Belief-behind-the-belief** — stated by source: *"Go beyond surface-level beliefs to investigate the belief-behind-the-belief."* Surface beliefs are proxies for the deeper beliefs the prospect won't state. Countering the surface just migrates the resistance.
- **Reveal-and-restraint** — stated by source: *"Give away the strategy (what/why) to build demand, withhold tactics (how) to preserve the value of paid offers."* Both an operational rule and a content-strategy one.
- **Two Big Domino beliefs, not one and not ten** — stated by source: *"overarching themes large enough to structure a 90-minute webinar around."* The 2-count comes from webinar-scope rationale — more than 2 and they're not big enough.

- **5+ floor for Vehicle / Internal / External, with the ceiling flexible** — 5 is the coverage minimum; 10 to 20 is valid and often better when specificity serves the downstream copywriting work. The discipline: aim for 5 at minimum, expand when the audience or the offer surfaces enough material to justify the additional rigor.

## References

- `references/buyer-psychology-beliefs.md` — primary consumer, four categories, belief-behind, dislodge, reveal-and-restraint
- `references/nlp-psychological-triggers.md` — the 20-field deconstruction
- `references/audience-input-context.md` — input expectations
- `references/audience-insight-influences.md` — named experts (Brunson's Big Domino, etc.) cited briefly when relevant

## Templates

- `templates/limiting-beliefs-output.md`
