# Template — Voiceprint File

The full file format for voiceprints saved through os-library/save. Used by all voiceprint modes (from-sample, from-book per layer, import, update). The file lives at `os-inputs/voiceprints/<filename>.md`.

## File structure

```
---
type: voiceprint
author: <name>
default: yes | no
scope: <scope>
genre: <optional>
source: <provenance>
created: <YYYY-MM-DD>
notes: <freeform>
---

# Analysis

[Technical linguistic breakdown — dimension scores, custom dimensions, grounded justifications. The working layer for human audit.]

# Voiceprint

## {Nickname}

[The portable artifact — 150-300 word prose portrait written in the source voice. Source-clean. What downstream skills load.]
```

## Frontmatter

Required: `type`, `author`. Strongly recommended: `default`, `scope`, `created`. Optional: `genre`, `source`, `notes`. Full schema in `../../os-library/references/voiceprint-schema.md`.

## Body sections

The file body has two top-level sections separated by `# Analysis` and `# Voiceprint` headers.

The **Analysis** section is the working layer. It contains the technical breakdown produced by the from-sample two-pass procedure: standard dimensions scored 1-10 with brief grounded justifications, plus 1-2 custom dimensions capturing what makes this voice distinctive. The Analysis can cite short lexical evidence and reference source content for grounding. Downstream skills (drafting, editing, fiction-edit) should NOT consume this section — it's too source-specific and contains audit content not portable across uses.

The **Voiceprint** section is the portable artifact. It opens with a `## {Nickname}` header capturing the voice's essence in a short descriptive phrase. The body is a 150-300 word prose portrait *written in the voice it describes* — terse for terse voices, lyrical for lyrical voices, etc. The portrait must demonstrate at least three of the idiosyncrasies named in the Analysis (not just name them). The portrait must pass the era-tells self-check (no LLM-cadence patterns, no source-leak). This section is what downstream skills load as voice context.

## Source-cleanliness rules

The Voiceprint section must be source-clean:
- No quoted source text
- No source-specific lexemes (no characteristic words from the source as illustration — describe the lexical choice instead)
- No source topics or scenes (no kettle, no Paris awning if those appear in the source — describe the pattern, or invent stand-ins clearly not from the source)
- Concrete writing is fine when the concreteness is invented. Source-drawn concreteness is not

The Analysis section is allowed to cite source content for grounding (it's the audit layer), but the cited content stays inside the Analysis section and never bleeds into the Voiceprint portrait.

## Worked example

Filename: `pen-name-x-protagonist-nova.md`

```yaml
---
type: voiceprint
author: pen-name-x
default: no
scope: fiction-pov-nova
genre: urban fantasy
source: "Pen Name X — Book One, chapters belonging to Nova POV (1-4, 7-9, 12-15), ~28k words sampled"
created: 2026-04-25
notes: "Per-POV overlay on the master voiceprint pen-name-x.md. Captures Nova's distinctive close-third interior — noir-inflected, paratactic, sensory. Loaded alongside the master, not instead of it."
---

# Analysis

## Lexical (8/10)
[Specific observed features about word choice, with grounded examples from the source. Technical terms like "Anglo-Saxon vocabulary preference," "noir-period slang frequency," etc.]

## Syntactic (9/10)
[Sentence structure observations. Paratactic patterns, run-on tolerance in interior, etc.]

[continues through standard dimensions plus 1-2 custom dimensions]

# Voiceprint

## The Reluctant Tactician

[The 150-300 word prose portrait, written in the noir-inflected close-third interior voice it describes. Source-clean — no kettles, no specific named cases. Demonstrates the paratactic rhythm, the sensory grounding, the interior-monologue voice.]
```

## Output discipline

The full file is written through os-library/save, which handles filename generation per convention and frontmatter validation. The voiceprint mode produces the body content and proposed frontmatter values. Library/save does the persistence.

The file is composed once. The Analysis section is preserved in the file but not consumed by downstream skills (the contract is documented in the SKILL.md and library reference docs). When drafting or editing loads the voiceprint, they parse to the `# Voiceprint` section and use that body as voice context.
