# Era-Tells Self-Check

Before outputting the Voiceprint prose portrait, scan it for era-specific AI patterns. These patterns make the voice section read as LLM-generated rather than voice-matched, even when sentence rhythm and register are otherwise correct. They leak past rhythm-based checks because they *sound* voice-y while actually being generic.

## Patterns to flag

**Descending-length aphoristic codas.** Three or four phrases of decreasing length used as a closing flourish — *"Punchy. Parable. Point made. Door open."* A 2022–2023 LLM tell. Especially suspicious when alliterative.

**Contrast-clause strings.** *"Not X. Y."* / *"Not just X — Y."* / *"It's not X, it's Y."* deployed as a rhythm device, often in succession. Recognizable LinkedIn-sage cadence.

**Aphoristic wrap-up sentences.** *"That's the whole move."* / *"That's the shape."* / *"That's how you win."* Final-line punch-delivers that try to earn weight through confidence alone. A default-model tic.

**Triplet fragments as generic rhythm.** *"Scene. Lesson. CTA."* kind of thing, imported as a stylish device rather than because the source writer builds in triplets. If the source doesn't use triplets, don't add them.

**Pull-quote framing.** Short declaratives set up with extra white space around them so they read as quotable one-liners. Makes the portrait feel like a carousel slide rather than a writer's prose.

**Generic sage openers.** *"Here's the thing:"* / *"The truth is:"* / *"Here's what most people miss:"* — unless the source writer demonstrably uses them, in which position, at which frequency.

**Self-praise framing.** *"The voice that sells."* / *"A system that works."* — glossy claims about what the voice *does*, substituted for description of how the voice *reads*.

**Parallel-construction runs.** Three or four sentences in a row with the same grammatical shape (*"It does X. It does Y. It does Z."*) — unless the source writer's rhythm genuinely runs in parallels.

## The nuance

Any of these patterns can be legitimate if the source voice genuinely uses them. A writer who alliterates their sign-offs can have an alliterative coda in their portrait. A writer who builds in triplets can have triplets. A writer who opens with *"Here's the truth:"* can have that in their portrait.

A blanket ban would neuter legitimate voice-matching. The working rule:

**Use a pattern only if the source voice demonstrably uses it, and use it the way the source uses it. Don't import generic LLM-stylish moves because they sound voice-y.**

For each pattern that appears in the draft Voiceprint portrait, verify against the source:

1. Does the source writer use this pattern?
2. Does the source use it in this position (opener, closer, pivot)?
3. Would omitting it reduce voice fidelity, or would omitting it strip an LLM tell?

If the pattern survives all three checks, keep it. Otherwise, rewrite the line using a move the source actually makes.

## Source-leak check (runs alongside era-tells check)

Source-leak is a second class of failure. Era-tells import *generic LLM cadence*. Source-leaks import *source-specific content* (lexemes, scenes, topics) into what is supposed to be a portable style artifact. Both must be screened out before output.

For each specific noun, concrete reference, or verbatim phrasing in the draft portrait, ask: *does this appear in the source?* If yes, it's a source-leak. Rewrite as abstract pattern-description, or swap for an invented stand-in that clearly isn't source content.

Source-leak types to watch:

- **Specific source lexemes** — e.g., quoting the writer's characteristic words (*"Mofo. Blammo. Shit."*) as illustration of lexical choices. Fix: describe the vocabulary abstractly ("punchy slang, profanity used as rhythm, idiosyncratic interjections").
- **Specific source scenes or objects** — e.g., naming *a kettle, a Paris awning* when those appear in the source. Fix: describe the pattern ("opens with a concrete everyday scene") or invent stand-ins clearly not in the source ("a traffic light, a waiting room, a coat hook").
- **Specific source setup phrases** — e.g., reproducing *"Here's the truth:"* as an illustrative opener when the source uses that phrase. Fix: describe the pattern ("opens with a one-line setup phrase that telegraphs the turn") without reproducing the exact phrasing.
- **Reader-name echoes** — e.g., the source opens *"Hey Firsty Lastname,"* and the portrait opens *"Hey reader,"*. Borderline — the lowercase convention is a style move, and "reader" isn't source content. Acceptable if it's genuinely demonstrating the move. Not acceptable if it's just reproducing the source's opening frame. Use judgment.

Source-leaks are subtle because they *feel* voice-y and concrete. They are actually training residue that reduces the voiceprint's portability — a downstream writing skill will pick up "kettle" as a content cue and generate about kettles, which is the opposite of what the skill is for.

## Invented concreteness is encouraged

Concrete writing is still encouraged in the portrait — it's source-drawn concreteness that's prohibited. If the source uses concrete metaphors, the portrait should too, but with invented examples. Rule of thumb: could this specific noun or scene plausibly have come from someone else's writing entirely? If yes, it's fine as illustration. If no — if it's a signature object of the source — rewrite.

## Run the check

After drafting the Voiceprint portrait, read it against BOTH lists (era-tells and source-leak). For each flagged pattern present in the draft, apply the verification questions. Rewrite anything that fails.

This check goes before output, not after. A voiceprint that ships with leaked era-tells will train downstream writing skills on LLM cadence. A voiceprint that ships with source-leaks will train downstream writing skills on source-specific content cues. Both are failures the skill is designed to prevent.
