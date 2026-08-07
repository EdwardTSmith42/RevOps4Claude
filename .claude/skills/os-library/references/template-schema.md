# Template Schema

Templates are proven structural shapes for specific output formats — landing page architectures, welcome-email sequences, hook formulas, VSL outlines. They live in `os-inputs/templates/` as flat files (no nesting) because templates are typically format-keyed, not author-keyed.

A template captures structure, not content. The point of a template is to encode "how this format works" so the writing skill can produce a new piece in the same shape with new content. Templates are agnostic to voice and author — voice comes from the voiceprint, content comes from the brief, structure comes from the template.

## Frontmatter schema

```yaml
---
type: template
format: <format value>
proven: yes | no | with-context
notes: <freeform — what context this works in, any caveats>
---
```

Required: `type`, `format`. Strongly recommended: `proven`, `notes`. Optional: a `source` field if the template was derived from a specific successful piece.

## Field guidance

**`type`** is always `template` for files in this directory.

**`format`** is the output format the template produces. Starter values include `landing-page`, `welcome-email`, `hook-formula`, `email-sequence`, `vsl-outline`, `case-study`, `lead-magnet`, `nurture-email`, `sales-letter`, `newsletter-issue`, `social-post`, and similar. Format values are descriptive labels — a user developing new structural patterns can add new formats freely. The point is findability when drafting needs a structural shape for a specific job.

**`proven`** marks whether the template has been validated by use. Three values: `yes` for templates that produced strong results in real campaigns or pieces, `no` for untested templates the user is experimenting with, and `with-context` for templates that worked in specific contexts but may not transfer (a B2B SaaS landing-page template that doesn't fit a creator-class audience, for example). Matching prefers `proven: yes`, but loads `no` and `with-context` templates when no proven option exists.

**`notes`** is freeform and especially important for templates. Common uses: what context the template works in (campaign type, audience temperature, revenue or response signal when known), what to keep vs. what to swap (which structural moves are universal versus vertical-specific), and known failure modes (which traffic types or audience profiles the template should NOT be used for, with the reason).

A `source` field can identify where the template was derived from — typically the URL of a successful piece or the filename of a saved-out variant. Optional but useful for templates that came from analyzing real wins.

## The template body

The body of the file is the actual structural shape. Format depends on what the template encodes — a hook formula might be a one-paragraph prose description with placeholders, a landing page might be a section-by-section outline with each section's job described, an email sequence might be N email summaries with cadence notes between them.

The template body should be specific enough that drafting can produce a new piece by following it, but abstract enough that the new piece doesn't read as a clone of the source. The template encodes structure ("section 3 establishes the obstacle the reader has tried before, section 4 names why those approaches failed") not content ("section 3 says claims drag on for months").

A useful test: if the user removed the source content from a successful piece, what would remain that's transferable? That's the template.

## Worked example

A filename like `<format>-<descriptor>.md` (where the descriptor disambiguates among multiple templates for the same format) might carry frontmatter shaped like this:

```yaml
---
type: template
format: landing-page
proven: with-context
notes: "<which campaigns this worked on, what audience temperature it assumes, which sections to swap for different audiences, known anti-patterns>"
---

# <Format descriptor as the document title>

## Section 1 — <what this section does for the reader>
A 2-3 sentence description of the section's job. Effect-described placeholder language ("a single-sentence promise that makes the outcome concrete and quantified, paired with a de-risking line") rather than verbatim sample text — the template is structural, not copy.

## Section 2 — <next section's job>
[Continued template body — section-by-section outline describing the job each section does. Roughly 600-1200 words total for a long-form template.]
```

## When this template gets loaded

The matching discipline ranks templates by `format` plus `proven` against the job context. A template loads when the user is producing output matching its format AND the job context aligns with the template's notes (audience temperature, vertical, offer shape).

If the job context contradicts the template's notes (cold traffic against a warm-traffic template, for example), the template still loads but with lower confidence and a flag noting the context mismatch. The user sees the flag and decides whether to use the template anyway, modify it, or look for a different one.

## Adding new templates

The user can save templates two ways. The first is to invoke `os-library/save` with a template body and frontmatter values. The second is to use a future writing mode that extracts a template from a successful piece — produces a `with-context` template by default that the user can promote to `proven: yes` after re-use validates it.

Templates accumulate slowly. A user typically has a small library of 5-15 templates that get re-used heavily, plus experimental templates that get tested and either promoted or archived. The `proven` field is the curation hinge — templates that don't earn `proven: yes` over time are candidates for cleanup during validation sweeps.

## Repairing template frontmatter

If a template has missing frontmatter, `os-library/repair` reads the body and infers what it can. The body usually announces its format in the heading or first line. The `proven` field defaults to `no` if the user hasn't marked it. Repair surfaces this and asks whether to upgrade. Notes are the hardest field to infer — repair often asks the user to add notes after the fact when they're missing, since the context-of-success information is human knowledge.

## What templates are not

A template is not a draft. The writing skill doesn't fill in templates word-for-word — it uses templates as structural guides while producing fresh content calibrated to voice and brief. A template that reads as a fill-in-the-blank form is too rigid — drafting will produce mechanical-feeling output. A template that reads as a structural outline (section by section, what each section does, what each transition handles) is the right shape.

A template is also not a prompt. Templates are loaded as references during drafting, not invoked as their own skill. The writing skill is the producer. The template informs the structure.
