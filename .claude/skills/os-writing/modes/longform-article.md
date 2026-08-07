---
name: os-writing/longform-article
description: Draft a longform article — Substack post, blog article, newsletter issue, education content, SEO-targeted piece, or other extended written piece. Produces the full article from hook through close, calibrated to publication context and audience. Triggers on "draft a Substack post about X," "write a blog article on Y," "produce a longform piece on Z." Do NOT trigger when the user wants a landing page (use `landing-page`), a single email (use `email`), or a sequence of pieces (use `email-sequence`).
---

# Mode — Longform Article

Full longform-article writing. Produces extended written pieces — Substack posts, blog articles, education content, SEO-targeted pieces, op-eds, essays. Calibrated to publication context, audience, and through-line.

The mode handles the article shape conventions: a strong hook opening, a clear through-line developing one core argument or story, body sections that earn their place, a close that lands a takeaway. Hook anatomy lives in `../references/hook-anatomy.md`. Format-specific anatomy is anchored in `../references/writing-principles.md` and customized per publication.

## When to use

The user is producing a longform written piece. Common triggers: "draft a Substack post on marketing operations," "write the blog article about Y," "produce a longform piece on Z for the newsletter," "draft an essay about W."

If the user is producing a landing page, `landing-page` is the right mode (different structure entirely — landing pages are conversion artifacts, articles are reading artifacts). If the user is producing a single email or a sequence, the email modes apply. If the user wants only a hook or section, use `hooks` for the opener and this mode with section-targeted revision for sections.

## Inputs

The mode loads references via the library convention (`../references/library-loading.md`):

**Required:** What the article is about. The argument, story, or insight the piece carries. Either inline or via the brief / source material.

**Required (or asked):** Publication context. Substack post, blog post on a personal site, guest post on a publication, SEO-targeted article, newsletter issue, op-ed, essay. Different contexts have different conventions for length, voice register, structural expectations, and SEO concerns.

**Required (or asked):** Target length. Substack posts often run 800-2,500 words. Blog posts vary 600-3,000+. Education content and longform essays run longer (2,000-5,000+). SEO-targeted pieces calibrate to keyword competition. The brief specifies. If missing, the mode asks.

**Required (or asked):** Audience. Who's reading. What they already know about the topic. What they'd find generic vs. fresh. The audience profile shapes voice, depth of explanation, and what counts as the through-line.

**Loaded from library:** Voiceprint at `longform` scope (or scope matching the publication context). Style samples for the relevant patterns (a `personal-anecdote-opener` sample, a `tactical-insight-section` sample, etc.). Template if a proven longform template exists for the publication. Brief from `os-inputs/briefs/current/`.

**Optional:** Source material. Research, transcripts, customer quotes, prior writing the article draws on. Inline or linked.

**Optional:** SEO targets. For SEO-targeted articles, the user may supply target keywords, competitor analysis, or specific search-intent signals. The mode honors these without letting SEO override voice.

## Run

The procedure runs through six stages.

**Stage 1: Read the brief and source material.** What's being argued or explored. What evidence and examples support it. What audience-specific framing applies. The mode reads the available material before producing — articles produced without grounding in the brief read as generic.

**Stage 2: Load references.** Apply the library-loading convention. Surface what's loaded. If the publication context implies a specific voiceprint scope, the mode loads it (a Substack post loads the longform voiceprint, while a guest blog post in a more formal register loads a different scope if one exists).

**Stage 3: Plan the through-line.** A longform article carries one core argument, story, or insight from hook to close. The mode identifies the through-line from the brief and source material before producing. If the brief contains multiple potentially-distinct through-lines, the mode surfaces the choice — *"This brief has two strong angles: 'marketing ops as P&L line' and '8 years of misunderstanding the function.' I'd lead with the first and weave the second through. Confirm or pick differently?"*

**Stage 4: Plan the section structure.** Articles vary structurally but most longform pieces have a recognizable shape: hook / opener (sets up the through-line), context (situates the reader), development (the substance — argument, story, or insight unfolding), pivot (often where the article turns from setup to payoff), payoff (the through-line landing), close (takeaway, action, or final reflection). The mode adapts this skeleton to the specific piece. For an essay-shaped piece, the development is one extended argument. For a tactical piece, the development is a sequence of insights or steps. For a personal-narrative piece, the development is a story arc.

**Stage 5: Produce the article.** Hook follows `../references/hook-anatomy.md`, calibrated to longform article length (3-5 sentences, story or specific-result openers often work best for longform). Body develops the through-line section by section — each section earning its place by advancing the through-line. Sections that don't earn their place get compressed or cut. Close lands the takeaway or calls the reader to a specific action.

The mode produces in the writer's voice from start to finish. Longform articles are where voice fidelity is most visible — readers spend 5-15 minutes inside the piece and notice voice drift. A piece that opens in voice but drifts to AI-generic by paragraph 4 fails the voice test even if the substance is good.

**Stage 6: Production review.** After producing, the mode briefly reviews the article for through-line clarity (does the piece carry one argument from hook to close?), section pacing (does each section earn its place?), voice consistency (does the voice hold across the piece?), and length-vs-substance match (is the length warranted by what's being said?).

## Output

The full article, with publication-appropriate formatting:

```
## Article: <title or working title>

**References loaded:**
- Voiceprint: <name>
- Brief: <brief filename>
- Style samples: <list>
- Template: <name or "none — structured per longform conventions">
- Publication context: <Substack / blog / etc.>
- Target length: <X words>

---

# [Article title]

[Hook / opener — 3-5 sentences setting up the through-line]

[Body sections, each labeled if appropriate for the publication context, each developing the through-line]

[Close — landing the takeaway or action]

---

**Production notes:**
- Word count: <actual>
- Through-line: <one-sentence summary>
- Sections that felt thin (if any): <list>
- Sections that ran long (if any): <list>
- Any context-fit concerns: <if applicable>
```

The article body itself is publication-format-appropriate. Substack uses subheadings to break up sections. Blog posts often use H2s and H3s. Newsletters often skip sub-headings and use prose-density variation as the structural cue. The mode calibrates per publication context.

## Output discipline

Strong hook from word one. Through-line established in the opener and carried through. Each section earning its place. Close landing the takeaway or action. Voice consistent across the whole piece.

The mode does not pad to hit a target length. If the substance is 1,200 words and the brief asked for 2,000, the mode flags the gap rather than producing 800 words of filler. Padding produces articles readers notice as padded.

The mode does not bury the lead. A longform article that gets to the actual point in paragraph 5 has lost most readers by then. The opener establishes the through-line. The body develops it. The close lands it.

The mode honors voice fidelity across length. Longform is where voice drift surfaces most visibly. The mode notes any sections where voice felt difficult to hold and flags them in production notes.

## Iteration

Longform articles benefit from iteration more than shorter formats. The mode supports the iteration patterns from `../references/iteration-discipline.md`:

**Prior-output-plus-direction:** "Tighten the opening section by 30%," "swap paragraph 4 for something more specific," "add a counter-argument before the close." The mode produces a revised version that preserves the unaffected sections.

**Section-targeted revision:** "Rewrite the close — make it more pointed," "swap the hook for a story-opener," "rework the payoff section — the current version doesn't land the through-line." The mode produces a replacement for the named section while preserving the rest.

**Batch-then-pick for the opener specifically:** "Give me 3 alternative openers for this article." The mode produces variants spanning hook shapes. The user picks. The chosen opener lands in the next iteration.

For longform, iteration is normal — first pass establishes shape, second pass tightens, third pass sharpens specific moments. Three or four rounds are common for the strongest pieces.

## Cross-mode suggestions

After a longform article, the natural next steps depend on what the user needs. Before publishing, `os-editing/assessment` gives a score and verdict. For a focused critique through a specific lens (specificity, takeaway, what-why-how, developmental), `os-editing/suggest-edits` with the relevant lens surfaces actionable edits. For length compression, `os-editing/shorten` removes 5–20% while preserving voice. For AI-tell cleanup the production missed, `os-editing/humanize`. For a check of the tonal register, `os-editing/tone-profile`.

Pick the one or two that fit; don't recite the full list.
