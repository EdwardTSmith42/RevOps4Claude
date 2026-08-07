---
name: os-content-template
version: 0.1.0
description: >-
  Deconstruct a successful piece of short-form content (a LinkedIn post, tweet
  thread, Instagram caption, essay opener) into a reusable, generalized template
  with slot variables, and optionally produce a ghostwriter-style interview
  guide to elicit the raw material for filling the template with someone else's
  story. Triggers when the user pastes a post and says "make this into a
  template," "turn this post into a framework," "reverse-engineer this into
  something I can reuse," "what's the structure of this?" or asks for an
  interview guide to capture a client's content. Two modes — `extract-template`
  (default, the deconstruction) and `interview-guide` (the elicitation
  instrument). Often used in sequence. Do NOT trigger for writing a single piece
  of content — this is for making content patterns reusable.
display_name: Content Template
tagline: Reverse-engineer good content into reusable templates.
category: Research
packs:
  - creator-pack
icon: 'phosphor:BracketsCurly'
when_to_use: >-
  When you find a piece of short-form content that *works* (a LinkedIn post,
  tweet thread, Instagram caption, essay opener) and want to capture its
  structure for reuse, this is the skill.


  `extract-template` deconstructs the post into a reusable framework with slot
  variables. `interview-guide` produces a ghostwriter-style elicitation
  instrument for filling that template with someone else's story. Often used in
  sequence.
modes:
  - name: extract-template
    job: Deconstruct a post into a reusable template with slot variables.
  - name: interview-guide
    job: Ghostwriter-style elicitation instrument for the template.
---

# Content → Template — extract reusable templates from finished pieces

## Purpose

Take a piece of content that works — a post, thread, short essay, hook, or any short-form writing that has a clear rhetorical structure — and convert it into a generalized, plug-and-play template that other creators can use to produce their own version without plagiarism. Optionally, produce a ghostwriter-style interview guide that elicits the raw material (the credentials, the results, the tension, the body of work) needed to fill the template for a specific client.

The skill serves ghostwriters, content strategists, and creators who want to reproduce effective content forms without copying specific content.

## When to use

- The user has a specific post, thread, or short-form piece and wants the structure abstracted so it can be reused
- A ghostwriter is preparing to interview a client and needs a conversational guide anchored to a specific content pattern
- Content strategy work: building a library of reusable templates from high-performing posts

Do **not** use for:
- Writing a fresh piece of content (use `os-writing`, or `os-content-mining/format-remix` for fresh idea generation)
- Summarizing a post (use a summarizer)

## Inputs

- **Required for `extract-template` mode:** The source content (a post, thread, short essay, copy block). If long-form, the relevant section.
- **Required for `interview-guide` mode:** Either an extracted template (output from `extract-template`) or the original source content. The interview guide builds off the template's slot structure.
- **Optional:** Target use-case (LinkedIn, X, email, landing page) — influences the tone of the interview questions but not the template shape.

## Run

Mode-selection routing:

- User pastes content and asks to templatize, reverse-engineer, or "make reusable" → **`extract-template`** (see `modes/extract-template.md`)
- User has a template and asks for interview questions, a ghostwriter guide, or "how do I get this from my client" → **`interview-guide`** (see `modes/interview-guide.md`)
- User asks for both → run `extract-template` first, then `interview-guide` off the resulting template

Shared across modes: use generalized abstractions that transcend the original industry/niche. Preserve rhetorical power — short sentences stay short, contrast-clause structures stay, and the punch doesn't get abstracted out.

## Output

Mode-specific. See:
- `modes/extract-template.md` for template extraction output
- `modes/interview-guide.md` for interview-guide output

## Design Rationale

Why this skill is structured the way it is:

- **Two modes split at the natural seam** — pattern recognition (extracting structure) and empathic questioning (eliciting raw material) are different jobs with different cognitive postures. Forcing them into one output produces muddy work in both.
- **Generalized beyond the original niche** — a template that only works for one industry isn't a template; it's just that one post again. The craft is abstracting far enough that the structure transfers, without abstracting so far that the rhetorical punch evaporates.
- **`[ALL CAPS]` slot variables** — visually distinct from prose, impossible to confuse with template body, trivial to find-and-replace when a creator fills it in.
- **Rhetorical power preserved through abstraction** — abstraction commonly flattens punch. Keep short sentences short, contrast structures intact, sentence-rhythm parallel; replace only the specifics. A template that loses the rhythm of its source has lost the thing that made the source work.
- **Interview guide is conversational, not a questionnaire** — formal questioning shuts down the vulnerability the guide needs to surface. Casual register invites honesty, and honesty is the raw material the template needs.
- **Cold read first, label slots last** — the extraction process orders the moves so abstraction happens after structure is understood. Labeling slots before seeing the spine produces wrong-level variables (too specific, or specific to the wrong thing).

## Modes

- `modes/extract-template.md` — the deconstruction (default when user pastes a post)
- `modes/interview-guide.md` — the ghostwriter-interview instrument (run after extract-template, or standalone)

## Examples

- `examples/im-not-a-template-and-interview.md` — a worked example combining both modes, from a "I'm not a ___, but I ___" post pattern. Grounded in real human-authored content, demonstrates both the template abstraction and the interview guide voice.

## Saving extracted templates

Extracted templates are exactly the artifact type the library manages: offer to persist keepers via `os-library/save` to `os-inputs/templates/` (per the library's template schema), so `os-writing` and siblings can load them by the matching discipline. One-line offer after extraction; no ceremony.

## Where outputs go

Outputs persist per the workspace storage methodology — see `../_shared/references/workspace-layout.md` (Knowledge system invariants): when the work belongs to an ongoing project, save silently to `os-outputs/` with dated frontmatter and a link trail; when the user is exploring, offer once. No skill-specific save scheme.

## Related skills

- `os-content-mining` (`format-remix`) — after templatizing one post, a quick remix pass can generate more post ideas that would fill the same template.
- `os-voiceprint` — before running `interview-guide`, loading a voiceprint helps the interview questions sound like the interviewer's natural register rather than a generic warm voice.

## When the skill meets a shape it doesn't yet handle

This skill is additive — every new content surface (LinkedIn carousel, email opener, landing-page section, YouTube hook, podcast intro) is a candidate for its own template family with its own conventions, and a creator's working library of templates grows alongside their practice. When a user pastes something whose shape doesn't fit cleanly into the existing six-step extraction (a multi-modal post, a structured carousel, something where the "spine" lives in a non-obvious place), surface the gap honestly rather than forcing the wrong abstraction.

Then offer two paths. First: extract what you can this time, run the result as a one-off, and the user keeps the output without ceremony. Second: treat the example as a seed for a new sub-mode or a new entry in their template library — hand off to the skill-creation flow if the extraction needs a different process, or to the library-save flow if the result is itself a template worth keeping for reuse. Choose based on whether the user signals this is a recurring need or a curiosity. When the signal is ambiguous, ask — the cost of asking is small; the cost of saving clutter or losing wanted capability is larger.
