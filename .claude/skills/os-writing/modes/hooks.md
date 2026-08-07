---
name: os-writing/hooks
description: Generate hooks — single openers or batteries of variants for one piece. Hooks are the openers that buy the reader's next 30 seconds. Output is one hook (when the user wants targeted production) or a numbered list of variants (when the user wants options). Triggers on "draft a hook," "write 5 hook options," "give me an opener for X." Do NOT trigger when the user wants the full piece (use the appropriate format mode — `email`, `email-sequence`, `landing-page`, `longform-article`).
---

# Mode — Hooks

Produce hook openers. The mode handles single-hook production (one targeted hook for a known piece) and hook-battery production (multiple variants for a piece in development). Hook anatomy and shape conventions live in `../references/hook-anatomy.md`.

## When to use

The user wants an opener and isn't ready to produce the whole piece yet. Common triggers: "I need a hook for this Substack post," "give me 5 subject lines to choose from," "draft an opener for the Black Friday landing page," "what's the strongest hook for this argument."

If the user wants the full piece (article, email, landing page) with a hook included, the format-specific mode is the right call — those modes handle hook production as part of the broader piece. `hooks` is for hook-only production, often as a sketching step before committing to the full piece.

## Inputs

The mode loads references via the library convention (`../references/library-loading.md`), with hook-specific calibration:

**Required:** What the piece is about. The hook needs the substance to hook *to*. The user supplies a paragraph of context, a topic, a draft of the body, or a brief — whatever's available.

**Required (or asked):** What format the hook is for. Subject line, social post opener, newsletter opener, landing-page headline, longform article opener, video opener — different formats have different length and tone calibrations. If the format isn't clear, the mode asks before producing.

**Loaded from library:** Voiceprint matching the user's scope for the format. Hook-specific style samples if any exist — these live under `os-inputs/style-samples/<author-slug>/` and are most useful when they show how a specific writer opens a piece in the relevant shape. Brief if the project has one.

**Optional:** A specific hook shape the user wants ("give me a curiosity-gap hook," "I need a stakes-raise opener"). When supplied, the mode produces in that shape. When not, the mode picks the shape that fits the substance and brief.

**Optional:** Quantity. Default is 1 hook for targeted production, 3-5 hooks for battery production. The user can ask for more.

## Run

The procedure runs through four steps.

**Step 1: Load the substance.** Read the user's input — the piece's topic, body, brief, or context. Identify what the hook needs to set up: the specific outcome promised, the question the body answers, the surprise the body delivers, the case the body argues for.

**Step 2: Identify the format and load references.** Confirm the format (subject line, post opener, headline, etc.). Apply the library-loading convention to find the voiceprint, style samples, and template if any apply. The voiceprint loads at the scope matching the format (a customer-email voiceprint for a subject line, a longform voiceprint for an article opener, etc.).

**Step 3: Produce hook(s).** For targeted single-hook production, produce one hook in the shape that fits substance and brief. For battery production, produce 3-5 variants spanning different shapes — curiosity gap, pattern interrupt, stakes raise, specific result, provocative claim, story opener, question-to-reader. The variants must be genuinely different in approach, not minor word-swaps within one shape.

Honor format length conventions from `../references/hook-anatomy.md`: subject lines stay 3-7 words, landing-page headlines stay under 15 words, longform openers run 3-5 sentences, and so on.

Honor voice fidelity. Each hook reads in the writer's voice from word one. A hook that sounds polished-corporate when the voiceprint is plainspoken-direct fails the voice test before the body even loads.

**Step 4: Brief notes per variant.** When producing a battery, briefly name what makes each variant distinct ("variant 1: curiosity-gap setup, variant 2: stakes raise, variant 3: specific result lead"). The user picks based on these notes plus the hook itself.

## Output

For single-hook production: one hook delivered with a brief note on the shape and what it sets up. Format-appropriate length.

For battery production: a numbered list of variants. Each variant numbered, each with a brief shape-note, no hook longer than format conventions allow. The user picks. A follow-up invocation refines the picked one if needed.

The shape of a battery output, demonstrated on an illustrative topic (the variants below show how *shape* differs across hook types for the same underlying piece; the topic itself is just a vehicle for the demonstration):

```
## Hook battery — for the [piece]

1. **Curiosity-gap opener.** [A line that opens a loop the reader needs to close — names a question, a contradiction, or a missing piece without revealing the answer.] [Shape note: what it sets up, why the reader keeps reading.]

2. **Specific-result lead.** [A line built around a concrete number, named outcome, or quantified contrast — the reader keeps reading because the specificity signals substance.] [Shape note.]

3. **Pattern-interrupt opener.** [A line that inverts the genre's expected take — the reader keeps reading because the disagreement is unfamiliar.] [Shape note.]

4. **Story opener.** [A line that drops the reader into a specific moment — concrete time, concrete person, concrete situation — the reader keeps reading because the scene is in motion.] [Shape note.]
```

Variants must be genuinely different in approach. Word-swaps within a single shape don't count as variants — those are revisions of the same hook.

## Output discipline

No preamble before the hook(s). For batteries, begin with a brief context line (one sentence naming the piece the hooks are for) and proceed to the numbered variants. The hooks themselves are the output. Commentary is minimal.

The mode never produces a hook in a shape that doesn't fit the substance. If the brief calls for a stakes-raise hook but the body doesn't support stakes-raising, the mode flags the mismatch rather than producing a hollow stakes-raise.

The mode never produces a hook in a voiceprint-incongruent shape. A polished landing-page hook on a casual newsletter voiceprint mismatches — the mode uses the casual voice even when the format is landing-page (calibrating shape, not voice).

## Cross-mode suggestions

After a hook battery, the user usually picks one. The natural next step is to drop the chosen hook into the full piece via the format-specific mode (`email`, `landing-page`, `longform-article`) and keep producing. If the user wants to refine the picked hook further before dropping it in, invoke this mode again with prior output and revision direction. If none of the battery variants quite land, ask for additional shapes — the default cap of five is a default, not a ceiling.

Pick the suggestion that fits what just happened; don't recite all three.
