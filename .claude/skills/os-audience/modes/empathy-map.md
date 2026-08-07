# Mode: empathy-map

## Purpose

Produce a classic 8-field empathy map for a specific audience-moment. Compact output, narrower than `modes/avatar`. Empathy maps profile *moments*, not life arcs — how the prospect experiences a specific context, scene, or decision point.

## Triggers

Phrases like: *"build an empathy map"*, *"what does my customer think and feel"*, *"empathy map for X audience"*, *"what's my audience's internal experience"*. Also triggers when the user wants a quick zoom rather than a full avatar.

## Inputs

See `references/audience-input-context.md`. Empathy maps specifically require:
- **Required:** An audience segment (same requirements as avatar)
- **Required:** A specific context or moment — *"a coach on Sunday night preparing Monday's sessions,"* not *"a coach in general"*. Empathy maps without a context collapse into avatar-lite. Ask for the moment before producing output.

## Run

One pass, eight fields.

**The 8 categories** (from the classic empathy-map framework):
- **Thinks** — internal thoughts in this moment
- **Feels** — named emotions (specific, not "bad" or "frustrated")
- **Says** — what they'd say out loud (often filtered, defensive, or performative)
- **Does** — observable behavior
- **Sees** — what's in their visual environment (feeds, people, interfaces)
- **Hears** — voices, media, messages they're taking in
- **Pains** — frustrations and blockers felt in this moment
- **Goals** — short-term immediate goals (not life-level)

Grounding rules:
- Every field gets specific content. *"Frustrated"* is a category. *"Quietly ashamed of the course outline sitting untouched for three weeks"* is content.
- Distinguish **Says** from **Thinks.** If they're the same, you're missing the filter. What prospects say publicly is performance-adjusted. What they think is closer to the truth. The gap between the two is where the craft lives.
- **Sees** and **Hears** are environmental, not internal — the signal-noise the prospect is swimming in (social feeds, overheard comments, advisor voices, ambient media).
- **Pains** and **Goals** are moment-bound. Life-level material goes in `modes/avatar`.

See `templates/empathy-map-output.md` for the canonical format (numbered list with bold category words, table variant available).

## Output

Per `templates/empathy-map-output.md`. Default: numbered list, bold category words. Table variant on request.

After output, include a brief cross-mode suggestion block. Examples:
- "For a full psychographic portrait (not just this moment), run `avatar`."
- "To surface what's blocking this prospect from acting, run `limiting-beliefs`."

## Design Rationale

- **Moment-bound, not life-bound** — empathy maps without a specific context collapse toward avatar territory and lose their distinctive value. The ask for a moment is a coverage move.
- **Says vs Thinks separation** — the filter-gap is the main psychographic insight this format offers. If the two fields converge, the output is thin.
- **Specific named emotions** — generic emotion words ("frustrated," "overwhelmed") kill the utility. Named, situation-specific emotions unlock downstream content work.
- **Environmental Sees/Hears** — not what the prospect perceives internally, but the noise/signal environment they're navigating. This often surfaces competitive context or peer-influence material that avatar analysis misses.
- **Short output, light touch** — the mode is deliberately compact. Not every audience question needs a full avatar. Empathy map is the quick-zoom version. Avatar is the deep portrait.

## References

- `references/audience-input-context.md` — input expectations

No references to `buyer-psychology-beliefs.md` or `psychographic-frameworks.md` for this mode — it stays at the moment-level and doesn't reach into belief or framework territory. Those concerns belong to other modes.

## Templates

- `templates/empathy-map-output.md`
