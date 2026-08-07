---
name: os-writing/landing-page
description: Draft a landing page — sales page, opt-in page, product page, or event registration page. Produces the full page from hero through close, calibrated to page type and audience traffic temperature (cold / warm). Triggers on "draft the landing page," "write the sales page for X," "create an opt-in page for the lead magnet." Do NOT trigger when the user wants only a hook / headline (use `hooks`), or only specific sections without the full page (use this mode with section-targeted revision).
---

# Mode — Landing Page

Full landing-page writing. Produces the complete page from hero to close, calibrated to page type (sales / opt-in / product / event), audience traffic temperature (cold / warm), and brief. Section-by-section anatomy and calibrations live in `../references/landing-page-anatomy.md`.

## When to use

The user is producing a landing page. Common triggers: "draft the long-form sales page for the upcoming launch," "write the opt-in page for the lead magnet," "create the product page for X," "draft the event registration page for the webinar."

If the user wants only a headline or section, this mode handles it via section-targeted revision (see Iteration below). For sequences of related pages (a launch funnel with multiple pages), the user produces each page through this mode separately, with the brief tying them together.

## Inputs

The mode loads references via the library convention (`../references/library-loading.md`):

**Required:** What's being offered. The product, service, lead magnet, or event being promoted. Either inline detail or via the brief.

**Required (or asked):** Page type. Long-form sales (warm traffic), short sales (cold traffic), opt-in (lead magnet), product (e-commerce), webinar registration, etc. Different types use different sections from `../references/landing-page-anatomy.md`. If unclear, the mode asks.

**Required (or asked):** Audience traffic temperature. Cold (audience meeting the writer for the first time), warm (audience knows the writer / has seen prior content), hot (audience is ready to buy and just needs the page). Temperature shapes section emphasis and length.

**Required (or asked):** Audience profile. Who's reading. What they already know about the offer space. What objections they typically have. What competitors they've considered. The audience profile lives in the brief. If missing, the mode asks before producing.

**Loaded from library:** Voiceprint matching the format. Style samples for the relevant patterns — a direct-response landing page benefits from a rhythm-shaped sample for the problem-and-promise sections; a fiction-adjacent style sample (dialogue, scene-building) would be loaded for other formats and skipped here. Template if a proven landing-page template exists for the type. Brief from `os-inputs/briefs/current/`.

**Optional:** Specific section requests. The user can specify "make the social proof section especially developed," "skip objection-handling — we don't have time," "include a video-embed placeholder in the hero." When supplied, the mode honors them.

**Required:** Offer specifics — price, what's included, deadlines, scarcity, guarantees, bonuses. The brief should carry these. If not, the mode asks. Producing a landing page with vague offer specifics produces a vague page.

## Run

The procedure runs through five stages.

**Stage 1: Read the brief and confirm the contract.** What's being offered. To whom. At what price. By when. With what scarcity / urgency / guarantees. The mode confirms each element before producing.

**Stage 2: Load references and select section structure.** Apply the library-loading convention. With references loaded, the mode selects which sections from `landing-page-anatomy.md` apply for this page type and traffic temperature. Long-form warm-traffic sales typically uses all eight sections. Short cold-traffic sales usually compresses to hero, problem, promise, offer, close. Opt-in pages run even leaner: hero, promise, offer, close. The mode surfaces the section plan to the user before producing — naming which sections are in the plan and what each will do — and asks for confirmation or adjustment. The plan checkpoint matters because reshaping a 3,000-word page after production is expensive; getting the section plan right costs one round-trip.

**Stage 3: Produce the page section by section.** With the section plan approved, produce each section in turn following the per-section conventions from `landing-page-anatomy.md`:
- Hero: specific headline, sub-headline, single CTA above the fold
- Problem: pain named in the audience's language, often pain-triplet structured
- Promise: outcome-stated transformation
- Mechanism: 200-400 words explaining how the thing actually works
- Social proof: specific named cases, quoted dollar amounts, real outcomes
- Offer: full specifics, value stack calibrated to actual value
- Objection handling: common objections named and resolved
- Close: restated promise, final CTA, last impression

Each section honors the voiceprint and the audience profile. Sections that don't earn their place per the anatomy reference get compressed or skipped — padded sections produce conversion friction.

**Stage 4: Apply pacing.** Long-form pages need pacing as much as length. Paragraph length runs 1-3 sentences typically. Single-sentence paragraphs work for emphasis. Subheadings break up sections. Bullet points handle genuine enumerations (offer specifics, mechanism steps) but don't substitute for prose argument. CTAs appear at multiple points across the page so readers who decide at any point don't have to scroll.

**Stage 5: Produce the page.** Deliver the full page in the structure called for. Include placeholder markers where specifics need to come from elsewhere — pricing the brief didn't supply, a named testimonial the writer referenced but didn't include, a screenshot the page calls for. The placeholder is explicit (`[INSERT PRICING]`, `[INSERT NAMED-TESTIMONIAL]`) so the user can see exactly what's still needed before publishing.

## Output

The full landing page, structured by section. Section headers are visible (`## Section 1 — Hero` etc.) so the user can read the page top-to-bottom or jump to a specific section. The reference-loaded note opens. The page follows.

```
## Landing page: <campaign / project name>

**References loaded:**
- Voiceprint: <name>
- Brief: <brief filename>
- Style samples: <list>
- Template: <name or "none — followed direct-response convention">
- Page type: <type>
- Traffic: <temperature>

---

## Section 1 — Hero

[Headline]

[Sub-headline]

[CTA]

## Section 2 — Problem
[etc., through all sections in the plan]

---

## Production notes

[Any sections that felt thin and might benefit from additional brief detail. Any placeholders for content the user needs to supply. Any flagged context-fit concerns.]
```

## Output discipline

The page delivers as a unit. Each section labeled, each section earning its place. Prose density matches landing-page conventions — paragraphs short, line breaks frequent, scannable.

No preamble before the page. The reference-loaded note is brief and scannable. Production notes appear at the end so the user has visibility into thin sections, missing specifics, and context-fit observations.

The mode never produces a section without substance to fill it. If the brief is missing the social-proof specifics, the social-proof section is shorter or holds placeholder markers — the mode doesn't fabricate testimonials. Same for offer specifics, deadline dates, mechanism details: real or placeholder, never fabricated.

The mode honors page-type length conventions. Long-form sales pages run 2,000-5,000 words. Short cold sales pages run 600-1,500 words. Opt-in pages run 200-600 words. Pages outside these ranges are flagged in production notes ("This page came in at 800 words for a long-form warm-traffic page — either expand the social-proof and objection-handling sections, or accept the shorter form").

## Iteration

Long-form pages especially benefit from iteration. The mode supports the iteration patterns from `../references/iteration-discipline.md`:

**Section-targeted revision:** "Rewrite the close to add deadline urgency," "rework the social proof section to include the new case study," "make the hero headline more specific." The mode produces a replacement for the named section while preserving the rest.

**Prior-output-plus-direction at page level:** "Tighten the whole page by 20%," "make the tone less direct-response and more advisory," "add an objection-handling section if it isn't there." The mode revises while preserving structure.

**Batch-then-pick for hero or close specifically:** "Give me 3 alternative hero headlines," "draft 2 different closes." The mode produces variants for the named section. The user picks.

## Cross-mode suggestions

After a landing page, the natural next steps depend on the launch state. Before publishing, `os-editing/assessment` returns a score and verdict — useful as a pre-launch quality gate. If the page came in long, `os-editing/shorten` compresses 5–20% while preserving voice. If the production didn't fully catch AI-tells, `os-editing/humanize` with the direct-response carve-outs (which keep `!` and pain-triplet rhythm) does the cleanup. If the page is part of a launch funnel, switch to `email-sequence` to produce the campaign that drives traffic to it.

Pick the suggestion that fits where the user actually is; don't recite all four.
