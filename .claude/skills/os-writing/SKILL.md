---
name: os-writing
version: 0.1.0
description: >-
  Produce new prose from briefs, voiceprints, and references — the producer side
  of the writing workflow. Five modes: hooks for openers and hook batteries,
  email for single-piece emails, email-sequence for multi-piece campaigns,
  landing-page for sales and opt-in pages, longform-article for Substack and
  SEO articles. Loads voiceprints, style samples, templates, and briefs via the
  library matching convention so output sounds like the writer, not the model.
  Iteration is supported and expected — modes accept prior output plus revision
  direction. Triggers when the user wants to produce new prose ("draft a hook,"
  "write an email for X," "draft the landing page for Y campaign," "write a
  Substack post about Z"). Do NOT trigger for editing existing prose (use
  os-editing), tone analysis (use os-editing/tone-profile), or producing
  voiceprints from samples (use os-voiceprint).
display_name: Writing
tagline: >-
  Produce new prose in a writer's voice — hooks, emails, landing pages,
  articles.
category: Writing
packs:
  - creator-pack
icon: 'phosphor:PenNib'
when_to_use: >-
  The producer side of the writing workflow. Loads voiceprints, style samples,
  templates, and briefs via the library matching convention so output sounds
  like the writer, not like a model.

  Iteration is supported and expected — every mode accepts prior output plus revision
  direction. Reach for this when you want to *produce* prose.
modes:
  - name: hooks
    job: Openers and hook batteries.
  - name: email
    job: Single-piece email.
  - name: email-sequence
    job: Multi-piece email campaign.
  - name: landing-page
    job: Sales / opt-in landing page.
  - name: longform-article
    job: Substack and SEO articles.
---

# Writing — produce new prose from briefs, voice, and references

## Purpose

Writing is the producer side of the writing workflow. The user supplies a brief (what to make, for whom, why), writing loads relevant references via the library convention (voiceprint for voice fidelity, style samples as few-shot exemplars, templates for structural shape, briefs for project context), and produces new prose calibrated to all of them.

This skill operates downstream of audience, biz-strategy, offer, and voiceprint, and upstream of editing. The chain typically runs: research the audience and offer (audience, biz-strategy, offer) → produce a voice (voiceprint) → write the brief → draft new prose (writing) → edit and refine (editing) → publish.

Writing is iterative by nature. A first pass is rarely the final piece. The modes are built to accept prior output plus revision direction so the user can iterate within the same mode as the piece develops.

## When to use

The user wants to produce new prose. Common triggers: "draft a hook," "write an email," "draft the landing page," "write a Substack post," "I need 5 hooks for a post about X," "draft email 3 of the welcome sequence." If the user is editing existing prose, route to editing instead. If the user is brainstorming concepts or doing audience research, route to the appropriate insight skill.

## Modes

| Mode | Job | Output shape |
|---|---|---|
| `hooks` | Generate openers — single hook or a battery of variants for one piece | One hook or a numbered list of hook candidates |
| `email` | Single-piece email writing — subject line, body, optional PS | Full email with subject and body |
| `email-sequence` | Multi-piece email campaigns — welcome sequences, nurture flows, sales sequences | Sequence of emails with cadence notes |
| `landing-page` | Sales pages, opt-in pages, product pages — full-page copy | Complete landing page from hero to close |
| `longform-article` | Substack posts, blog articles, SEO-targeted pieces | Full article with intro, body, conclusion |

### Self-determining when not specified

If the user names a mode, run it. Otherwise infer from the request:

- *"Draft a hook," "I need an opener," "write 5 hooks"* → `hooks`
- *"Write an email," "draft the PS line"* → `email` (single piece)
- *"Draft the welcome sequence," "I need 7 emails for X campaign"* → `email-sequence`
- *"Draft the landing page," "write the sales page"* → `landing-page`
- *"Write a Substack post," "draft an article about X"* → `longform-article`

When the format is ambiguous ("draft something for the launch"), ask before producing. Writing consumes the most user time per output, so wrong-format work is expensive.

## When the requested format isn't yet a mode

The current modes cover the bulk of common writing work but won't cover every format a writer might produce — a VSL, an ad-copy variant, an internal format unique to the user's practice, a one-off they don't expect to repeat. When the user asks for something the existing modes don't fit, writing surfaces the gap explicitly and offers two paths rather than forcing the request into a wrong-shape mode or declining.

The first path is *set the format up as a new mode for next time*. The user supplies one or more examples — a piece they've written before in this format, a piece from another writer whose shape they want to mirror, a rough sketch with notes about what the final should look like. Writing hands off to `os-tune` with the examples and the user's framing as input; its `extend` mode produces the new mode file inside the skill, and from then on the format is a first-class mode. The next request in this format runs the same shape without re-supplying examples.

The second path is *produce it once, no setup*. The user just wants to see what the skill can do with the materials at hand. Writing produces the piece using the closest existing mode as a structural starting point and the supplied source material as the substance. No new mode gets saved; the output is the only artifact.

Writing is greedy about extension when the signal points at recurring need — a request that mentions weekly use, a publication context the user keeps producing for, a format their work routinely calls for. A one-off doesn't earn a saved mode. When the signal is ambiguous, the mode asks. The same disposition applies to templates: when a request would benefit from a saved template the library doesn't yet have, writing offers to extract one via `os-library/save` after the piece is produced, so the next run can load it as a structural reference.

The why: a skill that stays frozen at its initial mode list shrinks the user's ambitions to what the skill already supports. A skill that extends in response to use grows alongside the writer's practice. Self-extension is what makes the skill an investment, not just a tool. The canonical principle and its application across the workspace lives in `../_shared/references/self-extending-skills.md`.

## Inputs across all modes

Every writing mode accepts the same shape of inputs and uses them to produce calibrated output. The user supplies any combination — the mode loads the rest from the library where possible.

**The brief.** What's being made and why. Either a `os-library/find` lookup against `os-inputs/briefs/current/` if the user named a project, or a quick inline brief if no saved brief exists. The mode can chain into a "write a quick brief" flow if neither is available.

**The voice.** A voiceprint loaded via `os-library/find`. By default, the mode uses the user's scope-specific voiceprint matching the requested output format, falling back to the user's general default voiceprint. The user can override by naming a different author's voiceprint (loading the corresponding `<author-slug>.md` from `os-inputs/voiceprints/`). If no voiceprint matches, the mode follows the graceful-degradation pattern documented in `../os-library/references/matching-discipline.md`.

**Style samples.** Optional but high-leverage. Style samples live under `os-inputs/style-samples/<author-slug>/<pattern-name>.md` — one file per pattern per author. The mode loads any samples that match the author and the kind of move the piece needs (a rhythm sample for direct-response copy, a scene-opener sample for fiction-adjacent work, a personal-anecdote sample for newsletters). Samples function as few-shot exemplars and are most valuable when they show *the* specific move the piece is trying to make.

**Templates.** Optional. If a proven template exists for the requested format (e.g., `landing-page-long-form.md`, `welcome-email-7-day.md`), the mode loads it as a structural guide. Templates inform shape, not content.

**Source material.** What the piece is *about* — research notes, a transcript, a customer interview, a topic outline, a piece of inspiration content. This is the substantive input the prose draws from. Distinct from the brief (which is meta-context) and from references (voice, style, structure).

**Prior output and revision direction (for iteration).** When the user is iterating, supply the prior version of the piece plus a description of what to change. The mode treats prior output as context to refine, not replace.

## Library loading convention

Writing modes follow the matching-discipline documented in `../os-library/references/matching-discipline.md` rather than calling os-library/find as RPC. The pattern, summarized:

The mode parses the brief and explicit references the user named. The mode scans `os-inputs/voiceprints/`, `os-inputs/style-samples/`, `os-inputs/templates/`, `os-inputs/briefs/` per the soft-search rules, applying the implied-author rule (use `name` from `_os-user-profile.md` when no author is named). The mode ranks candidates by the per-type scoring rules and surfaces top matches. When no clean match exists for a needed reference type, the mode follows the graceful-degradation pattern: surface the gap, offer the user three options (proceed without, supply sample for on-the-fly creation, point at related reference). The mode never silently approximates.

`references/library-loading.md` covers the writing-specific application of this convention.

## Iteration discipline

Writing is iterative. The same mode is invoked multiple times per piece as the work develops — initial draft, revision 1 with new direction, revision 2 incorporating editor feedback, polish pass. The modes support iteration through three patterns documented in `references/iteration-discipline.md`:

The first pattern is **prior-output-plus-direction**. The user supplies the previous version of the piece plus a one-line direction ("tighten the opening," "make the third paragraph more specific," "add a stronger CTA"). The mode treats prior output as the starting state and revises in the direction supplied.

The second pattern is **batch-then-pick**. The user asks for multiple variants of the same piece (3 hook options, 5 subject lines, 2 alternative landing-page openers). The mode produces variants in parallel, the user picks the one that lands, and a follow-up invocation refines that one specifically.

The third pattern is **section-targeted revision**. Long-form pieces (landing pages, longform articles, sequences) often need revision on a specific section without disturbing the rest. The user names the section ("rewrite the close," "revise email 4"), and the mode produces a replacement for just that section while preserving the surrounding work.

Whether iteration materially improves output is something to measure in real use — the modes are built to support it but don't enforce a specific number of passes.

## Operating principles

These hold across all writing modes. Full content in `references/writing-principles.md`.

**Voice fidelity is the constraint that doesn't bend.** A draft that's structurally sound but voice-generic reads as AI-produced and underperforms. Writing always loads a voiceprint (the user's, by default, scope-matched to the output format) and writes within that voice. If no voiceprint exists, writing surfaces the gap rather than producing voice-generic prose.

**Specificity over generality.** Vague prose is the most common writing failure. Specific numbers, named cases, concrete outcomes, exact constraints — every writing mode prioritizes these. The four-questions test (why read it, what learn, how help, why trust) anchors specificity work.

**The brief is the contract.** What's promised in the brief is what gets produced. If the brief is unclear or ambiguous, writing asks rather than guessing. Producing the wrong piece because the brief was vague is wasted work for everyone.

**Audience grounding.** Prose calibrates to who's reading. Writing honors the audience profile from the brief (or asks for one when none exists) and writes for that specific reader, not for an abstract "reader."

**Anti-AI-language calibrated to genre.** The catalog at `../_shared/references/ai-writing-patterns.md` is the editing skill's reference for AI-tells. Writing honors it during production rather than relying on editing to clean up after. Direct-response copy keeps `!` and pain-triplet rhythm. Fiction stays out of scope (that's a future fiction skill). Online-prose default is the typical calibration for blog posts, newsletters, and marketing copy.

**Iteration is normal.** A first pass is the starting point, not the final piece. Modes are designed to accept prior output and revision direction. The user iterates as the piece develops. Writing doesn't pretend one-shot work is enough.

## Cross-mode chain pattern

A common chain runs through several modes per piece. For a Substack post: `os-library/find` to surface relevant references → `longform-article` for the full draft → `os-editing/assessment` to score the result → `os-editing/suggest-edits` with the matching lens to act on top recommendations → `os-editing/humanize` for the final AI-tell pass.

For an email sequence: `os-library/find` to identify references and the brief → `email-sequence` to produce the sequence → `os-editing/assessment` on the sequence as a campaign → `os-editing/suggest-edits` per email as needed → `os-editing/shorten` if any email is bloated.

For a landing page: same pattern, with the structural depth of `landing-page` requiring more iteration cycles. Often runs `landing-page` once for the full draft, then targets section-by-section revision via the section-targeted iteration pattern.

## Output discipline

Each mode produces structured prose appropriate to its format. The output begins with the first line of the piece itself — for emails, the subject line; for articles, the headline; for hooks, the hook. No preamble framing what's about to be produced, because preamble dilutes the thing being produced and trains the reader to skip past the model's preface to find the actual work. End with the last line of the piece, not a sign-off from the model.

Briefs and voiceprints the mode used in production are noted in a short reference-loaded block at the start of the response, separate from the prose itself. The point is auditability — the user can see what shaped the work without the meta-context bleeding into the prose. When the mode produces multiple variants (hook batteries, subject-line variants), each is numbered. When the mode iterates on prior output, the response includes a brief note of what changed.

## Cross-mode suggestion postamble

After completing a writing mode, briefly mention the adjacent mode the user is most likely to need next, framed as a natural continuation rather than a sales pitch. The shape of these suggestions depends on what the user just produced:

After `hooks`, the natural next step is to drop the chosen hook into the full piece — either `longform-article` or `landing-page` depending on format.

After `email` or `email-sequence`, the typical next step is review — `os-editing/assessment` to score the result, or `os-editing/shorten` if the piece feels bloated.

After `landing-page`, suggest the pre-launch quality pass via `os-editing/assessment`, and the compression pass via `os-editing/shorten` if length is a concern.

After `longform-article`, name the iteration pattern — invoking this mode again with prior output and revision direction targets specific sections without re-doing the whole article.

These postambles describe the *next likely step*; they're not scripts to recite. The mode picks the suggestion that fits what just happened and phrases it in voice with the rest of the work.

## First-time setup

Writing is a consumer skill — its value depends on what's in the library. Before producing prose, the buyer needs at minimum a voiceprint matching the kind of writing they do. The graceful-degradation flow handles the no-voiceprint case by surfacing the gap and offering to chain into voiceprint creation, but the experience is meaningfully better when a voiceprint is already in place. Recommended setup order: install `os-voiceprint` and create at least one voiceprint matching your primary writing register; install `os-library` if you want the discovery layer to work across briefs, style samples, and templates; populate `os-inputs/briefs/current/` with any active project briefs you'll be writing against. None of these are hard requirements — the skill will surface what's missing and offer paths forward — but the first run is smoother with them in place.

## Design rationale

The skill is one trigger-routed hub rather than separate skills per format because writing jobs share substrate: voiceprint loading, brief consumption, style-sample exemplars, anti-AI calibration, iteration patterns. Splitting into one skill per format would duplicate the substrate logic and force the user to remember which skill handles which format. One writing hub with mode routing keeps the substrate centralized and the surface area small.

The modes cover the bulk of likely day-to-day writing work — hooks, emails, sequences, landing pages, articles — and ship with the architectural foundations strong rather than every mode-specific depth maxed out. Building specialized depth speculatively before real use produces skills bloated with unused craft. Mode depth grows in response to actual use.

The library convention is followed inline rather than via skill-to-skill RPC. The matching-discipline reference is the canonical contract — writing modes implement it within their own runs rather than calling out to another skill, because the cross-surface architecture doesn't reliably support inter-skill RPC.

Iteration support is structural rather than enforced. The modes accept prior output plus revision direction but don't dictate how many iterations to run. Real iteration patterns surface as the user works with the modes; the skill is built to support patterns without prescribing them.

The voiceprint load is foundational rather than optional. Without voice fidelity, writing produces generic AI-flavored prose the writer will recognize and dislike. The library convention's graceful-degradation flow handles the no-voiceprint case (surface the gap, offer creation on the fly), but the mode never silently produces voice-generic output. The skill is built around protecting voice fidelity.

## Where outputs go

Outputs persist per the workspace storage methodology — see `../_shared/references/workspace-layout.md` (Knowledge system invariants): when the work belongs to an ongoing project, save silently to `os-outputs/` with dated frontmatter and a link trail; when the user is exploring, offer once. No skill-specific save scheme.

## Related skills

- `os-library` — the storage and discovery layer. Writing follows the matching-discipline convention to load voiceprints, style samples, templates, and briefs.
- `os-voiceprint` — produces voiceprints. Writing is the largest consumer. If no voiceprint exists for a job, writing can chain into `os-voiceprint/from-sample` for on-the-fly creation.
- `os-editing` — the consumer of writing output. The chain runs writing → editing for review and refinement.
- `os-audience`, `os-biz-strategy`, `os-offer` — produce briefs and references that writing consumes upstream.
- `os-content-mining`, `os-gold`, `os-content-template` — adjacent content-side skills that may produce briefs or source material writing works on.
