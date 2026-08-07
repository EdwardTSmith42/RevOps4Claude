# Template — Tone Profile Output

The output shape for `modes/tone-profile`. Produces a 4-dimensional tone profile with scores, describers, anti-tones, and supporting passages.

## Format

```
## {Short, descriptive name for the tone profile — e.g., "Confident Mentor with a Crooked Smile"}

**Formal/Casual**
- Score: {0-10, 5 = neutral} - {Neutral / Slightly / Somewhat / Very / Extremely formal | casual}
- Comes off as: {up to 3 refined tone describers}
- Without being: {up to 3 anti-tones}
- Supporting passages: "{2-3 short verbatim passages from the draft that exemplify this dimension}"

**Serious/Funny**
- Score: {0-10} - {label}
- Comes off as: {3 describers}
- Without being: {3 anti-tones}
- Supporting passages: "{verbatim 2-3 short passages}"

**Respectful/Irreverent**
- Score: {0-10} - {label}
- Comes off as: {3 describers}
- Without being: {3 anti-tones}
- Supporting passages: "{verbatim 2-3 short passages}"

**Matter-of-Fact/Enthusiastic**
- Score: {0-10} - {label}
- Comes off as: {3 describers}
- Without being: {3 anti-tones}
- Supporting passages: "{verbatim 2-3 short passages}"
```

## Scoring scale

- **0** = extremely toward the left pole of the dimension (e.g., extremely formal)
- **5** = neutral / both equally
- **10** = extremely toward the right pole (e.g., extremely casual)

Common labels by score band:
- 0-1: extremely
- 2-3: very
- 4: somewhat
- 5: neutral / both slightly
- 6: somewhat
- 7-8: very
- 9-10: extremely

## Calibration discipline

**Use mid-range scores.** Most writing isn't 10/10 on any dimension. Insisting on extreme scores produces miscalibrated profiles. A piece that scores 7/10 toward casual and 6/10 toward enthusiastic is more accurate (and more useful) than one that scores 10/10 across the board.

**Reserve 9-10 and 0-1 for genuinely extreme cases.** If you find yourself wanting to give multiple dimensions a 10/10, recheck the draft — you're probably overweighting surface markers.

## Describers and anti-tones

Each describer is a refined adjective that goes beyond the dimension label. "Casual" is the dimension. "Conversational, lived-in, plainspoken" are the describers.

Anti-tones name what the writing is *not* — usually adjacent risks. "Casual without being sloppy / lazy / familiar" sharpens the casual rating by exclusion.

Up to 3 of each per dimension. Fewer if the writing is genuinely undifferentiated on that axis.

## Supporting passages

Quote 2-3 short verbatim passages from the draft that exemplify each dimension's reading. Without these, the profile is unfalsifiable — the user can't verify the score against the actual prose. Anchor every dimension to specific text.

## Output discipline

- No intro, no preamble. Begin with the profile name (`## {Name}`) and proceed through the four dimensions
- After the four dimensions, optionally add a one-paragraph synthesis describing how the dimensions interact (e.g., "Casual + serious produces a specific blend: trusted-friend-explaining-something-difficult, neither breezy nor formal")
- No conclusion or postamble — the synthesis IS the conclusion if included

