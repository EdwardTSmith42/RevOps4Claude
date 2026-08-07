---
name: os-voiceprint
version: 0.1.0
description: >-
  Produce voiceprints — portable artifacts capturing how a writer writes
  (lexical, syntactic, rhythmic, idiosyncratic features) so future AI output can
  emulate the style. Four modes: `from-sample` turns writing or transcripts into
  one voiceprint; `from-book` maps a manuscript into a master voiceprint,
  per-POV overlays, and curated style samples; `import` brings existing
  voiceprint text into the library with proper frontmatter; `update` refreshes a
  changed voice and judges whether the shift warrants reviewing sibling
  voiceprints. All modes save through `os-library`. Triggers on "analyze my
  voice," "create a voiceprint," "extract style from this book," "import an old
  voiceprint," "update my voiceprint, my writing has changed," or when another
  skill needs missing voice context. Do NOT trigger for line-editing prose (use
  `os-editing`) or finding existing voiceprints (use `os-library/find`).
display_name: Voiceprint
tagline: Capture how a writer writes — so AI can sound like them.
category: Writing
packs:
  - personal-os
icon: 'phosphor:Microphone'
when_to_use: >
  Reach for this any time you want a writer's voice in writable form. Most
  people start with `from-sample` on their own writing — that one voiceprint
  becomes voice context for every drafting and editing skill that comes after.
  Use `from-book` when you have a full manuscript and want layered output
  (master voice plus per-POV overlays plus curated style samples). Use `import`
  to bring an existing voiceprint file into your library with proper
  frontmatter. Use `update` when your voice in a context has genuinely shifted
  and the saved voiceprint no longer sounds like you — it refreshes that one and
  tells you whether your other voiceprints need a look too.


  A good voiceprint pays for itself the first time `writing` produces something
  that sounds *unmistakably you* instead of competent-and-bland.
modes:
  - name: from-sample
    job: >-
      Produce a voiceprint from one or more writing samples — the most common
      path.
  - name: from-book
    job: >-
      Layered voiceprint from a book-length manuscript — master voice plus
      per-POV overlays plus curated style samples.
  - name: import
    job: >-
      Bring an existing voiceprint file into the library with proper
      frontmatter.
  - name: update
    job: >-
      Refresh an existing voiceprint from new samples, then judge whether the
      change is a room-change or a person-change that warrants revisiting
      sibling voiceprints.
---

# Voiceprint — voice capture for downstream skills

## Purpose

A voiceprint is a portable artifact that captures *how* a writer writes, not *what* they write about. Drafting and other producer skills load voiceprints as voice context so generated output sounds like the writer. The voiceprint skill produces these artifacts from various source shapes — a paragraph of sample writing, a multi-piece corpus, a full book, or a previously-produced voiceprint that needs ingestion into the new library convention.

The skill underpins voice fidelity across the rest of the skill pack. Writing modes find voiceprints via the os-library/find convention. Editing modes can score voice against a stated voiceprint. Without good voiceprints in `os-inputs/voiceprints/`, downstream skills fall back to generic register and the user notices.

## When to use

A user has sample writing and wants a portable style profile. The user has a book-length manuscript (their own, a pen name's, an external author's) and wants a layered voiceprint that captures the master voice plus relevant overlays. The user has an existing voiceprint produced before the library existed and wants to bring it into the library with proper frontmatter. Another skill needs a voiceprint and none is on file — voiceprint produces one on the fly, and the user can choose whether to persist via os-library/save.

## Modes

| Mode | Input | Output |
|---|---|---|
| `from-sample` | Sample writing (one piece or a multi-piece corpus, 500+ words preferred) | One voiceprint file (frontmatter + Analysis + Voiceprint portrait) |
| `from-book` | Book-length manuscript or large chapter set | Layered output: one master voiceprint, optional per-POV voiceprints, optional curated style samples |
| `import` | Existing voiceprint text (from a v0.3 run, an external file, pasted content) | One voiceprint file with proper library frontmatter |
| `update` | An existing voiceprint plus new samples (or a described shift) from the same context | The refreshed voiceprint, a layer-sorted diff, and a room-change vs. person-change verdict with sibling review flags |

### Self-determining when not specified

If the input is a single piece or a small multi-piece corpus, route to `from-sample`. If the input is a book-length manuscript (40+ pages, multiple chapters, multiple POVs or scene types), route to `from-book`. If the input is an existing voiceprint the user wants to file, route to `import`. If the user points at a voiceprint that already exists and says their voice has changed or supplies fresh samples meant to *replace* the basis of an existing voiceprint, route to `update` — the tell is that a voiceprint for this context is already on file and the goal is to refresh it, not add a new one.

When the size or shape is ambiguous, ask before proceeding. A 30-page manuscript fragment is on the from-sample/from-book border. A multi-chapter sample with one POV throughout is from-sample. A multi-chapter sample with POV shifts is from-book.

## Inputs across all modes

Every voiceprint mode produces output that conforms to the library voiceprint schema (see `../os-library/references/voiceprint-schema.md`). The frontmatter values come from a mix of inferred-from-source and user-supplied, depending on mode:

- `author` — the user's name (from `os-inputs/_os-user-profile.md`) for self-voiceprints, or supplied by the user for pen names and external authors
- `default` — usually no for non-self voiceprints. The user picks for self-voiceprints
- `scope` — inferred from the source's content type (a book is `fiction-<genre>`, a customer-email corpus is `customer-email`). The user can override
- `genre` — supplied for fiction
- `source` — inferred from what was sampled (chapter count, file path, corpus description)
- `created` — today's date
- `notes` — produced by the mode where calibration notes are surfaced. The user can edit before save

The mode produces the artifact and proposes frontmatter. The user reviews and approves. Library/save persists with validated frontmatter.

## Library integration

All voiceprint modes write through `../os-library/modes/save.md` rather than emitting raw text the user has to file manually. The chain looks like this. The mode produces the voiceprint content and proposed frontmatter. The mode invokes the os-library/save flow (or follows the save procedure inline, depending on Cowork architecture). Library/save writes the file to `os-inputs/voiceprints/<filename>.md` with validated frontmatter, generates the filename per the convention, and confirms success.

When voiceprint is invoked from inside another skill's run (drafting needs a voiceprint and none exists, asks the user for sample text), the chain is the same with one addition: after the voiceprint is produced, the mode asks whether to save it for future use or use it once and discard. On-the-fly creation supports both paths.

See `references/library-integration.md` for the full integration pattern.

## Operating principles

These hold across all modes.

**One writer has many voiceprints, unified by fingerprint — not by content or rules.** A person is one self expressed differently in every room: punchy on social, warm to a coworker, sustained in an essay. Each context earns its own voiceprint, captured from that context's own samples, and siblings can differ to the point of contradiction (an exclamation point banned in one is natural in another). Do not flatten them toward each other. What makes them the same person is the *deep fingerprint* — idiosyncrasy, rhythm, characteristic moves of thought — not shared topics, beliefs, or never-do rules, which all flex by channel. Hold three layers when capturing or comparing: content/stance (most channel-bound, often not voiceprint material), surface mechanics (channel-bound, must be observed not inferred), and deep fingerprint (the invariant). Full treatment in `references/voiceprint-definition.md`.

**The voiceprint is for downstream consumption, not human reading.** A writing skill loads the # Voiceprint section as voice context. The portrait must be source-clean (no quoted source text, no source-specific lexemes, no source topics) so it teaches portable style rather than source content. The Analysis section is the analyst's working layer, useful for human audit but not loaded by downstream skills.

**Demonstrate, don't just name.** The Voiceprint portrait must show the moves it describes. A portrait that says "the writer opens in lowercase" without itself opening in lowercase hasn't internalized the voice. The era-tells self-check (`references/era-tells-self-check.md`) catches the common failure modes.

**Match the style being described.** A voiceprint of a terse voice should be terse. A voiceprint of a lush voice should be lush. The closer the portrait reads to the source style, the more faithfully downstream skills will reproduce it.

**Source-clean the portrait.** No verbatim source quotes, no source-specific nouns or scenes, no source topics. Concrete writing is fine when the concreteness is invented (not drawn from the source). The era-tells self-check screens for source-leak before output.

**Capture idiosyncrasy.** Every writer has quirks that don't fit standard taxonomies. The custom-dimension slots in the Analysis exist for this. Without them, voiceprints regress to a checklist and lose what makes the voice distinctive.

## Output discipline

Every mode produces a file that conforms to the library voiceprint frontmatter schema. The body has two sections: `# Analysis` (working layer, technical breakdown, dimension scores with grounded justifications) and `# Voiceprint` (portable portrait, prose written in the source voice, source-clean, 150-300 words for from-sample). Downstream skills load only the # Voiceprint section as voice context. They do not consume the # Analysis section.

For `from-book`, the output is multiple files — typically one master voiceprint, zero to N per-POV voiceprints, zero to N style samples. Each file conforms to its respective schema (voiceprint-schema for the voiceprints, style-sample-schema for the samples).

For `import`, the output is one voiceprint file. The existing voiceprint text becomes the body, and the user supplies the frontmatter values.

## Cross-mode chain pattern

The common chain runs from-book → multiple from-sample-equivalent extractions → os-library/save for each layer. The user sees a survey of the manuscript, approves a capture plan, and the mode runs the extractions one at a time with confirmation before saving each.

Another common chain: drafting needs a voiceprint, finds none in the library, asks the user for sample text. Drafting chains into os-voiceprint/from-sample with the supplied text. Voiceprint produces the portrait. The user decides whether to save it via os-library/save for future use or discard it after this run.

## Design rationale

The skill is a four-mode router because the three input shapes — sample writing, book-length manuscripts, existing voiceprints — have genuinely different procedures. Sample writing wants direct two-pass extraction. Book-length sources want a survey-then-capture-plan flow because flat extraction loses register and POV variation. Existing voiceprints just need form-filling for the new library frontmatter. Forcing all three into one mode would either over-engineer the simple case (sample writing) or under-serve the complex case (books).

The library integration is foundational rather than optional because voiceprints are the longest-lived inputs in the system. A voiceprint produced once gets loaded by writing modes hundreds of times. Persisting through os-library/save with proper frontmatter from the start prevents the "great voiceprint, but where did it go" failure mode.

The two-section file structure (Analysis + Voiceprint) preserves the audit trail. Without Analysis preserved, the voiceprint is unfalsifiable — a downstream consumer can't tell whether the portrait was honestly grounded in observed features or hallucinated from generic patterns. With Analysis preserved (but excluded from downstream consumption via documented contract), the human reviewer can audit the work without polluting the drafting context.

The era-tells self-check is the highest-leverage quality gate — the final pass in every mode that produces a portrait.

## References

- `references/voiceprint-definition.md` — dimensions to evaluate, what a voiceprint is and is not, figurative-language caution
- `references/era-tells-self-check.md` — LLM era-tell patterns to screen out before output
- `references/library-integration.md` — how voiceprint writes to os-library/save with proper frontmatter
- `references/book-survey-method.md` — chapter-level survey procedure for from-book mode

## Templates

- `templates/voiceprint-output.md` — output shape for a voiceprint file (frontmatter + Analysis + Voiceprint sections)
- `templates/voiceprint-file.md` — full file format with frontmatter at top
- `templates/book-survey-output.md` — survey-and-plan shape for from-book mode
- `templates/style-sample-from-book.md` — style sample shape for from-book extractions

## Related skills

- `os-library` — voiceprint outputs are saved through os-library/save and found via os-library/find. Voiceprint is the primary producer. Library is the storage and discovery layer.
- `os-editing/fiction-edit`, `os-editing/fiction-assessment` — load voiceprints when scoring or editing for voice fidelity
- `os-writing` — the largest consumer. Loads voiceprints via os-library/find for every drafting run

## Self-extending behavior

Voice work is additive — every new *context* (a pen name, a new register, a fresh genre, an admired external author) is a new voiceprint, not a revision to an existing one. That additivity is about *coverage*, and it sits alongside a separate move for *evolution*: when the voice in a context the user already has on file genuinely shifts, that's not a new voiceprint, it's an `update` to the existing one (which then judges whether siblings need a look). Keep the two distinct — new room, new voiceprint; same room that changed, update. When the user surfaces a writing context that doesn't have a voiceprint yet, offer the two natural paths: produce one now from sample writing they can supply (route to `from-sample`), or, if the source is a book-length manuscript, run the layered survey-and-extract flow (route to `from-book`). When the user already has voiceprint text from another tool or an older version, route to `import` rather than re-producing from scratch. When a saved voiceprint no longer sounds like the user, route to `update`. The skill is greedy about coverage because downstream voice fidelity compounds with library breadth.
