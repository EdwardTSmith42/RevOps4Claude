# Mode: avatar

## Purpose

Produce a full psychographic avatar — a portrait of a specific audience member's psychology that downstream content, offer, and landing-page skills can consume. The output is a *person* (named, grounded, vivid), not a demographic segment label.

## Triggers

Phrases like: *"profile my avatar"*, *"build a customer persona"*, *"who's my ideal customer"*, *"give me a psychographic profile"*, *"map my target audience"*, *"analyze my audience segment"*. Also triggers when another mode or skill calls for avatar input.

## Inputs

See `references/audience-input-context.md` for common input expectations. Avatar mode particularly benefits from:
- A tight audience segment (not "coaches" but "solopreneur coaches stuck at $10K/month MRR")
- Existing customer language (reviews, objection handling, sales-call notes)
- The offer and its core mechanism

Without a tight segment, ask for one before producing output.

## Run

Work through the avatar as a three-layer psychographic analysis, then compose the output.

**Mental model: Behavior → Belief → Identity Driver** (see `references/psychographic-frameworks.md`). Every observed behavior traces to a belief, which anchors in an identity driver. The work is tracing that arc for each of the avatar's dimensions — daily life, dream outcomes, fears, values.

**Step 1 — Name and role.** Give the avatar an alliterative first name paired with a descriptive title that captures their emotional identity, not their job — *<First-Name> the <Descriptive-Title-That-Names-Their-Predicament>*. A demographic label (*"The Life Coach Segment"*) doesn't work; an emotional-identity descriptor (something like *"the Overworked Practitioner Trapped by Her Own Success"*) does. The alliteration makes the avatar memorable; the descriptive title fixes the psychographic frame so downstream copy targets the predicament rather than the demographic.

**Step 2 — Surface layer (what they show).** Fill the Profile fields (age, role, goals they admit publicly) and write the opening narrative — a 3–5 sentence scene of their day. Specific and grounded. The test: does the scene name particular times, particular actions, particular tensions? A line that opens with the time on the clock and ends with the exact moment of stuck-ness beats "they're busy and overwhelmed." Generic produces generic copy downstream.

**Step 3 — Gap layer (what they want vs. have).** Fill the Current Reality vs. Desired State table. Six aspects minimum — daily schedule, income model, impact, market position, business model, identity. For each, find the *Hidden Truth* — the tension or fear the prospect wouldn't readily articulate themselves. The Hidden Truth column is where the avatar earns its keep.

**Step 4 — Unfiltered layer (what they won't say).** The Silent Struggles section. What they won't say publicly, and what keeps them awake at night. The "What Keeps Them Awake" first-person quote is the analyst's synthesis of what the prospect would say if they were being honest — not a real quote from the input. Specific, raw, identity-inflected.

**Step 5 — Aspirational layer (Dream Outcomes).** Three sub-categories: Emotional Rewards (specific named feelings), Lifestyle Aspirations (concrete markers — "location independence," "Fridays with kids"), and Identity Upgrades (who they become — "person who built something sustainable," "recognized thought leader"). Each category requires its own list.

**Step 6 — Fear layer (Psychological Landscape).** Three-layer fears table (Surface Concern → Underlying Fear → Deep-Seated Barrier). Each layer is distinctly deeper. The root is identity-level, not circumstantial. See `references/buyer-psychology-beliefs.md` on the belief-behind-the-belief excavation. Then list Hidden Desires — what they want but don't name, often because the desire feels embarrassing or "too much."

**Step 7 — Context layer (Market + Values).** Market Context & External Pressures (what they're swimming in — industry shifts, competitive pressure, cultural expectations). Values in Conflict table (each core value paired with the current reality that compromises it and the emotional dissonance produced).

**Step 8 — Closing.** A 1–2 sentence line summarizing the internal arc from friction to freedom. In the avatar's emotional register, not a marketing wrap-up.

See `templates/avatar-output.md` for the canonical output shape.

## Output

Per `templates/avatar-output.md`. Always include every section. Thin sections indicate thin input (ask for more context rather than padding).

After the avatar, include a brief cross-mode suggestion block — one to three other audience modes that would sharpen what you just produced, named by what they'd reveal that the current output didn't. The shape is a pointer in the user's direction of what they might want next: `limiting-beliefs` if the next move is figuring out what's blocking the buy, `core-transformation` if it's articulating the FROM/TO shift, `dmo` if it's mapping the before/during/after obstacle arc, `empathy-map` if it's zooming on a specific moment. Pick what fits the avatar that just landed and the work the user is heading toward; don't recite the full list.

## Design Rationale

- **Alliterative persona name** — makes the avatar memorable and nameable. An avatar no one remembers to use isn't useful. Default to alliterative unless a non-alliterative name serves the voice better.
- **Emotional Identity Role, not job title** — the role captures where the prospect is stuck, not what they do for work. Changes the downstream work that references the avatar (copy, offers) from demographic targeting to psychographic targeting.
- **Hidden Truth column in the gap table** — the Current vs. Desired gap is observable. The *why they haven't closed it* is not. That's the column that makes the avatar useful for marketing.
- **"Silent Struggles: What They Won't Tell Anyone"** — public statements are filtered. Forcing the analyst past the filter is the main craft move that distinguishes a psychographic avatar from a demographic profile.
- **Three-layer fears excavation** — the source prompts varied on column names (Surface / Underlying / Deep-Seated vs. Surface / Deeper / Root) but consistently enforced three layers. Identity-level fears are the durable ones. Counter-framing the surface only moves the resistance.
- **Dream Outcomes split into Emotional / Lifestyle / Identity** — prevents the Dream Outcomes section from collapsing into generic "more money, more time." Each sub-category forces a different kind of articulation.
- **Grounded specificity over generality, enforced via the input expectation** — a tight segment produces a vivid avatar. A loose segment produces cliché. The mode refuses to proceed without enough input.
- **Cross-mode suggestion block at the end** — this is a category-skill property, not a single-skill one. The user may not know what else the skill can do. Surfacing 1–3 relevant follow-up modes turns one mode's output into a navigable surface.

## References

- `references/buyer-psychology-beliefs.md` — belief-behind excavation (feeds the three-layer fears table)
- `references/psychographic-frameworks.md` — Behavior → Belief → Identity Driver arc
- `references/audience-insight-influences.md` — domain experts to reference briefly when relevant
- `references/audience-input-context.md` — input expectations

## Templates

- `templates/avatar-output.md`
