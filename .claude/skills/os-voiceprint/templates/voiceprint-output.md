# Voiceprint — canonical output shape

Use this shape as the default output. Flexible mode can deviate for quick voice sketches or specific dimension deep-dives, but the default output follows this structure.

## Shape

```markdown
# Analysis

## <Voiceprint nickname — short descriptive phrase capturing the essence>

**<Dimension>**: N/10 — <brief justification grounded in specific features of the input text>
**<Dimension>**: N/10 — <justification>
... (continue through all standard dimensions from references/voiceprint-definition.md)
**<Custom dimension 1>**: N/10 — <justification>
**<Custom dimension 2>**: N/10 — <justification>

# Voiceprint

## <Voiceprint nickname, same as Analysis>

<A 150–300-word prose portrait of the voice, written in the voice. No dimension headers. No ratings. No rubric structure. Continuous prose (or the voice's native paragraph structure) that describes how the voice reads while demonstrating at least three of the specific idiosyncrasies named in Analysis.

Adapt every surface move — sentence length, rhythm, register, punctuation habits, paragraph shape, openings, closings — to match the source. The portrait should read as something the target writer could plausibly have written about their own voice.>
```

## Key rules for the Voiceprint section

- **Prose portrait, not a dimension list.** No `**Lexical Range — 7/10**` headers. No section-by-section structure. The Voiceprint is a single piece of writing in the source voice.
- **Demonstrate at least three idiosyncrasies.** If Analysis names lowercase openings, self-nicknaming sign-offs, and setup phrases ("Here's the truth"), the portrait should actually perform three such moves, not just describe them.
- **Adapt all surface moves** — sentence structure, rhythm, register, punctuation, paragraph shape, openings, closings. The voice should be inhabited, not gestured at.
- **No ratings in this section.** Scores live in Analysis. The portrait is pure prose.
- **No source content in the portrait.** Three sub-rules, all strict:
  - **No quoted source text.** No sentences or phrases pulled from the input. Describe the writer's moves, don't reproduce them.
  - **No source-specific lexemes.** If the writer uses *blammo*, *oooft*, *mofo*, or any other characteristic word, describe the lexical choice ("punchy slang, idiosyncratic interjections") without reproducing the word. These words are generation cues — putting them in the portable artifact propagates them to downstream skills.
  - **No source topics, objects, or scenes.** If the source writes about kettles, Paris, or workshop mornings, the portrait cannot name any of those. Describe the pattern ("opens with a concrete everyday scene") or use invented stand-ins clearly not from the source ("a traffic light, a doorknob, a bus stop"). Concrete writing is still fine — source-drawn concreteness is the only thing forbidden.
- **No topic or content suggestions.** Pure style description only.
- **Run the era-tells self-check before finalizing** (see `references/era-tells-self-check.md`). Screens for both LLM-pattern leakage (aphoristic codas, contrast-clause strings, pull-quote framing) and source-leak (specific source lexemes, topics, or scenes reproduced in the portrait).

## Length guide

- **Short portrait:** ~150 words. Dense, voice-matched prose. Preferred for compact or terse voices.
- **Standard portrait:** ~200–250 words. The default for most voices.
- **Expansive portrait:** up to ~300 words. Reserved for voices with wide range a shorter portrait can't represent.

Longer than 300 words risks losing the voice-match to length pressure. Shorter than 150 risks missing the idiosyncrasies.
