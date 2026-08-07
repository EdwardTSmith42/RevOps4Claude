# Voiceprint Definition

A voiceprint is a digital writing-style fingerprint. It describes *how* a writer writes — lexical choices, syntactic habits, structural patterns, idiosyncrasies. It does not describe *what* the writer writes about (no topics, no samples, no thematic suggestions).

A voiceprint captures tone, register, style, and attitude. It may factor in use of creativity, humor, and figurative language. It always includes one or two dimensions that the analyst identifies as important for this specific writer — patterns not covered by the standard taxonomy.

The purpose of a voiceprint is to guide future AIs in emulating the writer's style reliably. A good voiceprint is portable — another AI should be able to read it and produce writing that feels like the source without having seen the source.

## One writer, many voiceprints — and what actually unifies them

A person doesn't have one voice. They have one *self* that comes out differently in every room. The same writer is punchy on social, warmer in a note to a coworker, sustained and patient in a long essay, and clipped in a Slack reply. Each of those is a real, distinct voice — so a writer usually ends up with several voiceprints, one per context, and that is correct, not redundant. Voice work is additive: a new context earns a new voiceprint captured from that context's own samples, not a tweaked copy of an existing one.

These sibling voiceprints can — and often should — differ sharply, sometimes to the point of contradiction. A move that's banned in one can be natural in another: a writer who would never use an exclamation point in a customer email might use them freely on social. Which beliefs surface, how much the reader is assumed to already know (a follower who knows the writer vs. a stranger arriving from search), how formal, how warm, whether signature concepts show up at all — all of it shifts by room. Two of a person's voiceprints can flatly disagree on the surface and both be right. The skill should never try to force consistency across them by flattening one toward another.

So if it isn't shared rules or shared content, what makes them recognizably the *same person*? The **deep fingerprint** — the idiosyncratic constructions, the rhythm (burstiness), and the characteristic moves of thought, how the writer's mind gets from one idea to the next. That layer barely bends by channel. The sentences get shorter on social, but the *shape of the move* underneath stays continuous. That continuity is the through-line; everything above it is free to vary.

It helps to hold three layers when capturing or comparing voiceprints:

1. **Content and stance** — what's said, which beliefs surface, the topics, the signature concepts. Most channel-bound of all, and often *not voiceprint material* — it lives in the writer's head or in other documents, not in the style fingerprint. A voiceprint that smuggles in topics or pet concepts will make downstream drafts sound like the writer is lecturing in rooms where they wouldn't.
2. **Surface mechanics** — sentence length, formality, punctuation habits, white space, the exclamation-point question. Channel-bound. This is the outfit for the room, and it's the layer that *must be observed from real samples* rather than inferred, because it's too subtle to specify in the abstract.
3. **Deep fingerprint** — idiosyncrasy, rhythm/burstiness, surprise (perplexity), and the one or two custom dimensions that capture how this specific mind moves. The invariant. This is the "same person" thread, and it maps to the Idiosyncrasy, Burstiness, and Perplexity dimensions plus the custom slots below.

The practical upshot for capture: build each context's voiceprint from that context's own samples, but sanity-check that its deep fingerprint feels continuous with the writer's other voiceprints. If a new voiceprint reads like a *different person* rather than the same person in a different room, something went wrong in the capture — not in the writer. And when a writer's voice genuinely evolves, the change has to be sorted by layer: a shift in surface mechanics for one channel is a room-change (touch only that voiceprint); a shift in the deep fingerprint is a person-change (every sibling is now a candidate for review). The `update` mode exists for exactly this judgment.

## Dimensions to evaluate

Each dimension gets a rating out of 10 and a short grounded justification.

### Lexical Range

Vocabulary breadth, specificity, and ornamentation. Does the writer use plain language with precise word choice, or a wide vocabulary with varied registers, or highly technical jargon?

### Syntactic Complexity

Sentence structure patterns. Do sentences run short and declarative, long and compound, a mix? How much subordination and embedding? How strictly does the writer follow standard grammar vs. stylized fragments?

### Format & Cadence

Paragraph shape, line breaks, list usage, visual rhythm. Is the writing modular and scannable, or dense prose? How does the writer use white space, em dashes, colons, other punctuation for pacing?

### Idiosyncrasy

Signature moves that appear consistently and distinguish this voice. Recurring constructions, pet phrases, punctuation habits, opening/closing patterns. This is often where the voiceprint earns its keep.

### Tone

Emotional register of the writing. Warm, clinical, assertive, conversational, caustic, earnest. How consistent is the tone across the sample?

### Register

Formality level. Academic, professional-casual, casual, slangy. How does the writer handle technical content — do they code-switch or stay at one register throughout?

### Figurative Language

Use of metaphor, simile, analogy, vivid imagery. Be cautious with high scores — most writers produce articles, emails, and short-form social posts where heavy figurative language becomes purple prose. Reserve scores above 6 for genuine fiction/poetic writers. High-score voiceprints will bias downstream AI output toward ornamented writing, and for most clients this degrades rather than improves future output.

### Perplexity

Predictability vs. surprise in word choice and sentence flow. Highly formulaic writing scores low. Writing that keeps subverting expectations scores high. Formulaic isn't bad — reliable structures are often the point.

### Burstiness

Variation in sentence length and rhythm. Writing that alternates between punchy short sentences and flowing longer ones scores high. Uniform sentence lengths score low.

### Custom dimensions (1–2)

The dimensions above are the standard set. Every voiceprint should also include one or two dimensions that the analyst identifies as distinctive for this specific writer. Examples from prior voiceprints: *Editorial Compression*, *Strategic Vulnerability*, *Argumentative Forward-Motion*. These capture patterns the standard taxonomy misses.

## What a voiceprint must not include

The rules below apply with different strictness to the two sections of the output.

### Voiceprint section (the portable artifact consumed by downstream skills) — strict

- **No writing samples from the source** — no quoted sentences or phrases pulled from the input.
- **No source-specific lexemes** — if the source writer uses *blammo*, *oooft*, or any other characteristic word, describe the lexical choice abstractly ("punchy slang, idiosyncratic interjections") rather than reproducing the word. The portrait is training input for downstream writing skills, and a specific source word in the portrait will propagate as a generation cue.
- **No source topics, objects, or scenes** — if the source discusses a kettle, a Paris awning, or a workshop morning, the portrait cannot name any of those. Describe the pattern ("opens with a concrete everyday scene") or invent stand-ins clearly not from the source ("a doorknob, a bus stop") as illustration.
- **No topic or thematic suggestions** — no "this voice is built for X" or "works best when writing about Y."
- **No content ideas or recommendations** about what the writer should write next.
- **No commentary on writing quality** unless quality itself is a distinctive feature.

### Analysis section (the analyst's working layer, for human review) — looser

- **May cite short lexical evidence to ground scores** — characteristic words, idiomatic phrases, punctuation habits. Prefer the shortest evidence that grounds the rating.
- **Avoid quoting full source sentences** when a shorter marker would serve. If a full sentence is genuinely necessary to show a structural pattern, cite it — but default to the minimum.
- **Source topics and scenes may be referenced** when needed to explain a structural observation (e.g., "opens with a personal scene — walking Paris, writing on a kettle") — but this is reference evidence, not voiceprint content.

Analysis is intended for a human to audit whether the voiceprint is honest. Downstream drafting, editing, and repurposing skills should consume ONLY the Voiceprint section, because it is the only section whose source-cleanliness is guaranteed.

A voiceprint is pure style description, usable as portable input to other skills.
