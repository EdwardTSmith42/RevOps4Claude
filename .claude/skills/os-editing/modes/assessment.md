---
name: os-editing/assessment
description: Score NON-FICTION writing (articles, blog posts, emails, marketing copy, reports, essays) across 6 dimensions (Grammar, Mechanics, Lexical Precision, Voice & Tone, Structural Coherence, Engagement & Impact) on a 1-10 rubric, deliver a calibrated revision-stage verdict (friendly variant Polish / Tune-up / Surgery / Rebuild — or strict variant Refinement Stage / Moderate Revision Stage / Substantial Revision Stage / Foundational Reconstruction Stage), and produce 3-5 prioritized recommendations ordered by impact. Cite specific passages for every score. Handles single pieces and multi-piece campaigns (email sequences, post series). Triggers when the user wants a quality diagnosis with a verdict — "score this," "how is this writing," "what stage is this at," "is this ready to publish." Do NOT trigger for fiction prose (use `fiction-assessment`), line edits (use `suggest-edits`), prose rewriting (use `humanize`), or tone description (use `tone-profile`).
---

# Mode — Assessment (non-fiction)

Multi-dimension scored review of a non-fiction draft, with calibrated revision-stage verdict and 3-5 prioritized recommendations.

For fiction manuscripts, use the sibling mode `fiction-assessment` — its rubric (Grammar / Mechanics / Prose Texture / Voice & POV / Scene & Story Architecture / Reader Pull) calibrates to fiction concerns this mode does not cover well.

## Purpose

The user wants to know how a non-fiction draft is doing — across multiple dimensions, with a clear verdict on what stage of revision it's at, and a small ordered list of the most impactful next moves. This is the "how is my writing?" mode for articles, blog posts, emails, marketing copy, reports, essays, technical writing, and similar prose.

## When to use

- "Score this writing"
- "How is this draft?"
- "What stage is this at?"
- "Is this ready to publish?"
- "Give me feedback on this — be specific"
- After running `suggest-edits` or `humanize`, to verify the edited version's stage

## Inputs

- The draft (text, attached file, or pasted) — single piece OR multi-piece campaign (email sequence, post series)
- Optional: stated context (publication, audience, voice goal) — informs voice scoring and format-specific notes
- Optional: stated writer skill level — informs prescription depth
- Optional: verdict variant preference (strict / friendly) — defaults to friendly unless commercial context signaled

### Multi-piece campaigns (email sequences, post series, etc.)

When the input is a sequence of related pieces (e.g., a 9-email Black Friday campaign, a multi-post LinkedIn series), the mode handles the campaign as a unit:

- **Score each piece individually** on the 6 dimensions, but produce ONE top-line summary, ONE verdict (covering the campaign as a whole), and ONE prioritized recommendation list (covering both campaign-level issues and per-piece issues)
- **Surface campaign-level patterns** in addition to per-piece scores: voice consistency across pieces (e.g., signature drift between authors), CTA consistency, internal contradictions across pieces (e.g., a "3 days left" email followed by a "7 days left" email), repetitive openers that wear thin across the sequence
- **Note cancelled / struck-through pieces** explicitly. If pieces are wrapped in `~~strikethrough~~` or otherwise marked as drafts the writer cancelled, score them anyway but call out in the top-line summary that they're flagged as not-sent — useful diagnostic for understanding what the writer tried and rejected
- **Format-specific notes** for the campaign cover sequence-level concerns (cadence, narrative arc across pieces, sequence-end CTA placement) in addition to per-piece notes

## Run — the 5-step diagnostic cycle

### 1. Get the lay of the land

Before touching the draft, establish:
- **Content type** — article, blog post, email, report, social media, academic paper, fiction, etc.
- **Publication context** — platform, journal, internal document, book, etc.
- **Target audience** — demographics, expertise level, professional context, etc.
- **Primary purpose** — inform, persuade, entertain, instruct, etc.
- **Author concerns** — anything they've flagged

If parameters aren't explicit, infer them from context and name the inference in one short line so the writer can correct it — what platform you're reading the piece for, what audience you're assuming, what register you're calibrating against.

### 2. Diagnose the text

Read once for flow (the whole piece), a second time for details. Score each of the 6 dimensions, then translate the scores into a verdict.

**Score the 6 dimensions:**

Technical proficiency:
- **Grammar & Syntax (X/10)** — subject-verb agreement, tense consistency, pronoun clarity, sentence structure, subordination/coordination
- **Mechanics (X/10)** — spelling, punctuation, capitalization, formatting, special character usage
- **Lexical Precision (X/10)** — word choice accuracy, terminology, redundancy, cliché avoidance (cross-check against `../../_shared/references/ai-writing-patterns.md` for the AI-tell catalog), register consistency

Stylistic effectiveness:
- **Voice & Tone (X/10)** — consistency, audience appropriateness, alignment with stated intent, distinctiveness, emotional resonance
- **Structural Coherence (X/10)** — logical progression, paragraph unity, transitions, information hierarchy, beginning/ending effectiveness
- **Engagement & Impact (X/10)** — reader interest, message clarity, memorability, persuasive effectiveness

For each score:
- **Cite specific passages.** Quote 2-3 words or a short span — abstract grades ("voice is good") are useless.
- **Voice score is calibrated to writer's stated intent**, not absolute aesthetic. A deliberately rough/raw voice scores high on voice if the writer intended that register.

**Translate the scores into a verdict** using the calibrated scale from `../references/revision-verdict-scale.md`:

| Most dimensions | Friendly variant | Strict variant |
|---|---|---|
| 8-10 | **Polish** | **Refinement Stage** |
| 6-7 | **Tune-up** | **Moderate Revision Stage** |
| 4-5 | **Surgery** | **Substantial Revision Stage** |
| Below 4 | **Rebuild** | **Foundational Reconstruction Stage** |

"Most dimensions" is the calibration anchor. If 5 of 6 dimensions fall in one band and one outlier is higher or lower, place the verdict in the band where most dimensions fall and call out the outlier in the prioritized recommendations.

Default to the **friendly variant** unless the user has signaled a professional/commercial context or explicitly asked for blunt framing.

### 3. Prescribe improvements (3-5 prioritized recommendations)

Order by impact, not by dimension. The top recommendation is the one that, if acted on, would most improve the piece. Don't run through dimensions in order.

Each recommendation:
- **Names the issue specifically.** Not abstract ("improve voice") but anchored — the specific opener that clashes with the body register, the specific paragraph where the argument breaks, the specific claim that goes unsupported. The recommendation only earns its place when the writer can point at the passage and recognize the problem.
- **Says what to do.** Diagnostic without prescription is half a recommendation.
- **Cites the passage** so the writer knows where.

3-5 recommendations is the default range. Fewer than 3 misses obvious wins. More than 5 produces overwhelm. (Why 3-5 specifically — TBD, preserved as default, malleable per user request.)

### 4. Tailor to the medium (format-specific notes)

After the core feedback, add a short paragraph on how to make the piece shine on its intended platform:
- LinkedIn: scannable structure, mobile readability, professional tone calibration, CTA effectiveness
- Sales / marketing email: subject line, preview text, CTA placement, signature voice, PS line
- Email sequence (multi-piece): cadence, opener variety, internal consistency across pieces, narrative arc across the sequence, end-of-sequence CTA placement
- Blog post: header hierarchy, paragraph length, internal linking, meta description
- Newsletter: subject line, preview text, opener hook, single-thought-per-issue discipline
- Academic paper: citation format, terminology, argument structure, evidence presentation
- Direct-response copy: pain-triplet rhythm, scarcity / urgency / guarantee handling, named-result specificity, signature voice
- Technical documentation: scannable structure, code-block / step formatting, prerequisite identification, version specificity

If the user didn't specify a context, skip this step or make it brief.

For fiction manuscripts, this mode is the wrong tool — route to `fiction-assessment` instead.

### 5. Double-check before delivering

Before returning the assessment:
- All 6 dimensions scored with specific passage citations
- Verdict calibrated to "most dimensions" rule
- 3-5 recommendations ordered by impact, each specific and prescriptive
- No advice that conflicts with the writer's voice, point of view, or stated intent
- Voice score honors the writer's intent, not absolute aesthetic
- Match prescription depth to writer skill level (don't recommend wholesale restructuring to a beginner without explanation)

## Output

Per `../templates/assessment-rubric.md`:

```
## Top-line summary
{One paragraph — must-knows.}

## Scores
{6 dimensions, X/10 each, with passage citations}

## Verdict
{Stage label and 1-2 sentence diagnosis}

## Prioritized recommendations (top 3-5)
1. **{Specific issue}** — {what to do, why first}
...

## Format-specific notes
{Optional, brief, medium-specific}
```

## Output discipline

- **Don't rewrite the author's text.** The mode produces guidance, not a revised version. (See `../references/editing-principles.md` — "Suggest, don't dictate.")
- **The author is unoffendable** but the diagnosis still has to be useful — blunt where blunt serves, not blunt for its own sake.
- **Cite passages for every score.** Without citations, the rubric is unfalsifiable.

## Cross-mode suggestions (postamble)

After the assessment, point at the natural next action in one short line that fits the actual verdict. The typical next moves: act on the top recommendation via `suggest-edits` with the lens that matches the weakest dimension; remove AI-tells via `humanize` if Lexical Precision flagged that pattern; compress via `shorten` before structural revision when the verdict is Tune-up or below and the draft is meaningfully too long. Pick the one suggestion that fits — don't list all candidates.

## Design rationale

- **6 dimensions, not a single overall grade**, because a single grade hides the lopsidedness that determines what to fix first. Per-dimension scoring forces specificity.
- **4-stage verdict scale calibrated to rubric cutpoints** because "most dimensions in this band" turns abstract scores into a concrete revision recommendation. The user knows whether they're polishing or rebuilding.
- **Two variant verdict scales (strict / friendly)** because the same diagnosis lands differently depending on writer / context. Same calibration cutpoints, different language. Default to friendly unless commercial context signals otherwise.
- **5-step run procedure (Lay of Land → Diagnose → Prescribe → Tailor → Double-Check)** because each step catches what the previous step might miss. Diagnose without Lay-of-Land produces local fixes that miss systemic issues. Double-Check catches the diagnostician's own bias.
- **"Match prescription to writer skill level"** because recommending wholesale restructuring to a beginner produces paralysis, and recommending tweaks to an experienced writer produces under-improvement. Calibrate by signal.
- **Voice score calibrated to writer's stated intent** because a deliberately rough voice scores low on "polished" but should score high on "voice" if the writer intended that register. Without this calibration, voice scoring punishes intentional choices.
- **3-5 prioritized recommendations** because fewer misses wins, more produces overwhelm. (TBD specific number — preserved as default.)
- **Order recommendations by impact, not by dimension** because dimension order is a categorical artifact. Impact order is what actually serves the writer.

