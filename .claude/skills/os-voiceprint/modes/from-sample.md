---
name: os-voiceprint/from-sample
description: Produce a voiceprint from sample writing — a single piece, a multi-piece corpus, or transcript content. Two-pass procedure: technical Analysis with dimension scores, then a 150-300 word Voiceprint portrait written in the source voice. Output is one file conforming to the library voiceprint schema, saved through os-library/save. Triggers on "analyze my voice," "create a voiceprint from these emails," "extract style from this article." Do NOT trigger for book-length manuscripts (use `from-book` for layered extraction) or for ingesting an existing voiceprint (use `import`).
---

# Mode — From Sample

Produce a voiceprint from sample writing. The classic voiceprint extraction — a piece of writing in, a portable voice artifact out. This mode preserves the v0.3 procedure (Analysis + Voiceprint two-section output) and adds library integration so the result lands in `os-inputs/voiceprints/` with proper frontmatter.

## When to use

The user has writing to analyze and wants a voiceprint. Source is one piece (a single article, a single post) or a multi-piece corpus (several emails, a set of newsletter issues, a collection of social posts). Total source length is typically 500-5000 words. Multi-piece corpora produce stronger voiceprints because cross-sample patterns surface only when the analyst can compare across pieces.

The mode handles self-voiceprints (the user's own writing), pen-name voiceprints (the user's other writing identity), and external-author voiceprints (an admired writer the user wants to emulate selectively).

## Inputs

- **Required:** A block of writing from the target writer. Ideally 500+ words. More if the writing varies across contexts.
- **Strongly preferred:** Multiple samples from varied contexts (emails, posts, talks, articles). Cross-sample patterns — recurring setup phrases, signature sign-offs, story-to-point arcs — surface only when the analyst can compare across pieces. Single-sample voiceprints miss these.
- **Optional:** Stated context about where the writing appears (social posts, emails, articles, book chapters). This biases the figurative-language constraint and informs the `scope` frontmatter value.
- **Optional:** Stated `author` if not the user (a pen name, an external author).
- **Optional:** Stated `default` preference (yes / no) for self-voiceprints.

## Run — the two-pass procedure

The procedure runs in two passes, preserved from v0.3 because the structure forces linguistic thinking before voice synthesis.

### Pass 1 — Analysis

Produce a technical linguistic analysis. Use scientific language, shorthand, and terminology that only linguists, writing specialists, and AIs would recognize. This is the working layer, not the polished output. Cover the voiceprint dimensions defined in `../references/voiceprint-definition.md`. For each dimension give a score out of 10 and a brief justification grounded in specific features of the input text.

Include one or two *custom dimensions* the model identifies as important for this specific writer — patterns that don't fit the standard taxonomy but matter for emulating this voice. The open slots exist to capture idiosyncrasy the checklist would miss.

The Analysis may cite short lexical evidence (characteristic words, idiomatic phrases, punctuation habits) to ground scores. Source topics or scenes may be referenced as structural evidence when needed. The Analysis is the human-audit layer, not the portable artifact.

### Pass 2 — Voiceprint portrait

Now produce the voiceprint itself as a **prose portrait written in the style it is describing**. Not a dimension-by-dimension list. Not a rubric in voice. A short piece of writing — roughly 150-300 words — that describes the voice while sounding like the voice.

The prose portrait must *demonstrate* at least three of the specific idiosyncrasies named in the Analysis, not just name them. If the Analysis says the writer uses lowercase openings and self-nicknaming sign-offs, the portrait should show such moves in action. Naming without demonstrating is the failure mode this pass was designed to prevent.

Give the voiceprint a nickname at the top that captures its essence in a short descriptive phrase.

Before finalizing the portrait, run the era-tells self-check in `../references/era-tells-self-check.md`. Most LLM-generated voice writing leaks recognizable patterns — descending aphoristic codas, contrast-clause strings, generic "Here's the thing:" openers — even when rhythm and register are otherwise correct. The self-check catches these before output. Rewrite any flagged line using a move the source actually makes. Don't ship the portrait until it passes.

The portrait must also be source-clean. No quoted source text. No source-specific lexemes (no characteristic words from the source as illustration — describe the lexical choice instead). No source topics or scenes. Concrete writing is fine when the concreteness is invented. Source-drawn concreteness is not. See `../references/voiceprint-definition.md` for the full source-cleanliness rules.

## Compose the file with frontmatter

After the two passes produce the Analysis and the Voiceprint portrait, compose the full file in the library voiceprint format. The file structure runs from frontmatter through Analysis through Voiceprint:

```
---
type: voiceprint
author: <name>
default: yes | no
scope: <scope>
genre: <optional>
source: <provenance — what was sampled>
created: <YYYY-MM-DD>
notes: <freeform — calibration notes, what the voiceprint captures vs. what's intentionally excluded>
---

# Analysis

[Pass 1 output — dimension scores, custom dimensions, grounded justifications]

# Voiceprint

## {Nickname}

[Pass 2 output — the 150-300 word prose portrait, source-clean, demonstrating idiosyncrasies]
```

Frontmatter values come from a mix of inferred-from-source and user-supplied:
- `author` — defaults to `name` from `os-inputs/_os-user-profile.md` if the user didn't name an author. If they named one (a pen name, an external author), use that.
- `default` — for self-voiceprints, ask the user if not specified. For non-self voiceprints, default to no.
- `scope` — infer from the source content type (a multi-email corpus is `customer-email`, a transcript collection is `longform`, social posts are `social-media`). Ask if uncertain.
- `genre` — supply for fiction sources. Skip for non-fiction.
- `source` — describe the corpus briefly ("9 emails from Q4 newsletter sequence," "transcript of keynote talk + 3 LinkedIn posts").
- `created` — today's date.
- `notes` — capture any calibration notes from the Analysis that the user should know about (e.g., "voiceprint excludes the formal book intro which has different POV"). Keep brief.

## Save through library

Once the file is composed, invoke the os-library/save flow to persist it. The save procedure is documented in `../../os-library/modes/save.md`. The mode:

1. Determines the target path: `os-inputs/voiceprints/<filename>.md`
2. Generates the filename per convention: `<author>-<scope>.md` for scope-specific voiceprints, `<author>.md` for the user's general-scope default
3. Validates the frontmatter against the schema in `../../os-library/references/voiceprint-schema.md`
4. Writes the file
5. Confirms with the file path and any validation warnings

If the user is invoking from-sample inside a drafting session and may not want to persist (one-off voiceprint for one-off use), the save step is optional. Ask before persisting.

## Output

The file written to `os-inputs/voiceprints/<filename>.md`, with confirmation of the path and the frontmatter values. If the user wanted to see the Analysis and Voiceprint portrait inline (typical for first review), surface them in the response so the user can verify before they're consumed by downstream skills.

## Output discipline

The Voiceprint portrait is the portable artifact. It must:
- Match the style being described (a terse voice gets a terse portrait, a lush voice gets a lush portrait)
- Demonstrate the idiosyncrasies named in the Analysis, not just list them
- Pass the era-tells self-check (no LLM-cadence patterns, no source-leak)
- Stay within 150-300 words
- Open with a nickname header capturing the voice's essence

The Analysis is the working layer. It must:
- Cover the standard dimensions plus 1-2 custom dimensions
- Score each dimension with a number out of 10
- Ground each score in observed features of the input
- Cite short lexical evidence where useful (this is the audit-trail layer)

Source-cleanliness applies to the Voiceprint portrait, not the Analysis. The Analysis can reference source content for grounding. The Voiceprint cannot.

## Cross-mode suggestions

After saving a voiceprint, common follow-ups depend on the user's larger flow. If the user is mid-drafting, mention that drafting can now load the new voiceprint via os-library/find. If the user produced multiple voiceprints in sequence (one per scope), point at os-library/list to see the full collection. If the user is building a pen-name corpus and the source was a book chapter, consider running `from-book` instead for the full layered extraction.

## Design rationale

The two-pass procedure separates linguistic thinking from voice synthesis. Pass 1 forces the model to observe specific features. Pass 2 synthesizes those features into a portrait that demonstrates them. Without the separation, voiceprints regress to vague pattern-matching that doesn't reproduce the voice.

The Voiceprint portrait is written in its own style as both a quality check and a demonstration. A voiceprint that describes a terse voice in lush academic prose is evidence the model hasn't internalized the voice. Matching the style proves the analysis worked.

The two-section file (Analysis preserved + Voiceprint portrait) preserves the audit trail. Downstream skills consume only the Voiceprint section, but the Analysis remains in the file for human review when the voiceprint surprises someone.

Library integration closes a loop earlier versions left open. Raw-text output the user filed by hand produced drift; writing through os-library/save with validated frontmatter from the start prevents the "great voiceprint, but where did it go" failure mode.
