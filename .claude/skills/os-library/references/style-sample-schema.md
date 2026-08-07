# Style Sample Schema

Style samples are curated 200-500 word passages that demonstrate a specific writing pattern the user wants emulated. They live in `os-inputs/style-samples/<author>/<pattern>.md`, nested one folder deep by author because a single author typically has multiple patterns worth saving.

A style sample is the user's curated excerpt, not an automatically extracted artifact. The user reads through their own work or an admired author's work, picks 200-500 words that exemplify one specific move, and saves it. Library helps find the right sample for a given job.

## Frontmatter schema

```yaml
---
type: style-sample
author: <name>
pattern: <pattern value>
genre: <optional>
source: <provenance — book title + chapter, post URL, etc.>
length: <approximate word count>
notes: <freeform — when this move works, what it teaches>
---
```

Required: `type`, `author`, `pattern`. Strongly recommended: `source`, `length`. Optional: `genre`, `notes`.

## Field guidance

**`type`** is always `style-sample` for files in this directory.

**`author`** matches the same convention as voiceprints — lowercase, hyphenated. The user's own samples use the user's name. Pen-name samples use the pen name. External author samples use the external author's name. The author field is required because style samples are author-specific by nature. A generic "good action scene" without an author tag isn't useful for voice-fidelity work.

**`pattern`** is the specific writing move the sample demonstrates. Starter values include `action-scene`, `dialogue`, `interior-reflection`, `descriptive-passage`, `exposition`, `hook-opener`, `cliff-hanger`, `scene-transition`, `tension-build`, `comic-relief`, and similar named moves. Pattern values are descriptive labels, not enum-bound — a user developing a new vocabulary for their craft can add new patterns freely. When in doubt, use an existing pattern value. The point is findability across the user's collection, which means consistency over precision.

**`genre`** is optional and applies mainly to fiction samples. Examples: `urban fantasy`, `literary fiction`, `noir`. A pattern can read differently across genres (a noir action scene differs from a literary one) — marking genre helps disambiguate.

**`source`** identifies where the passage came from with enough specificity to recover it later — typically a title, chapter or section, and a short locator describing the scene or beat (or, for external authors, a published-work citation with chapter and page). Provenance helps the user remember why this sample was worth saving.

**`length`** is the approximate word count of the sample. Useful for quick scanning when picking which sample to load (a 200-word fragment trains differently than a 500-word scene).

**`notes`** is freeform. Common uses: what the sample teaches (the specific move worth imitating), when to load it (which job contexts fit, which don't), and what to imitate vs. what's source-specific (so the producer doesn't carry over vocabulary or worldbuilding that won't transfer).

## The style sample body

The body of the file is the actual sample — the verbatim passage from the source. No commentary, no markdown decoration, no explanation. Just the prose, set in a single block. The downstream skill loads the verbatim text as a few-shot example showing the pattern in action.

If the sample needs context (a paragraph before it, a paragraph after it), include those briefly with light markup so the model sees the pattern in its natural surrounding without confusion about what's being demonstrated.

## Worked example

A style-sample filename under `<author>/<pattern>.md` (for example, an author folder containing one file per saved pattern) might carry frontmatter shaped like this:

```yaml
---
type: style-sample
author: <author-handle>
pattern: action-scene
genre: <genre tag>
source: "<title — section — short locator>"
length: 312 words
notes: "<what the sample teaches, what transfers, what doesn't>"
---

[Verbatim passage of approximately the stated length, ending at the end of a natural scene beat. No editorial commentary, no markdown headers inside the passage, no explanation. Just the prose, exactly as it appears in the source.]
```

## When this style sample gets loaded

The matching discipline ranks style samples by `author` plus `pattern` against the job context. A sample loads when the user is producing output matching its pattern AND the author signal matches (the user named the author, the brief is for that author's work, the genre signal aligns).

A style sample is loaded as a few-shot exemplar — the downstream skill sees the verbatim passage as an example of how the pattern should land in this author's voice. Multiple style samples can load together if the job spans multiple patterns (a scene that pivots from action into dialogue, for example, would benefit from both `action-scene` and `dialogue` samples for the same author).

## Curating new style samples

To add a style sample, the user picks a 200-500 word passage from their work or a reference author's work, copies it verbatim into a new file at `os-inputs/style-samples/<author>/<pattern>.md`, fills in the frontmatter, and saves. Library/save validates the schema. The user can also chain through `os-library/save` directly with the passage and frontmatter values, which writes the file in the right place.

A useful curation discipline: when reading work the user wants to learn from, save samples actively rather than passively. The user decides this passage demonstrates this pattern, and gives it a clear name. Patterns chosen by the user are more useful than patterns inferred by an automated process — the curation choice is itself signal.

## Repairing style sample frontmatter

If a sample has missing frontmatter, `os-library/repair` reads the body and infers what it can: the file path tells the type, the parent directory tells the author, and the body content gives genre and pattern signals. The pattern field is the hardest to infer — repair will often surface options ("this looks like an action-scene or possibly a tension-build — which?") and let the user pick.
