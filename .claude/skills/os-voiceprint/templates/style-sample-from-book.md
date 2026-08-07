# Template — Style Sample from Book

The output shape for style samples extracted by `os-voiceprint/from-book` stage 3. Used when the from-book mode identifies a passage worth saving as a curated style sample — typically an action scene, dialogue beat, interior reflection, or other pattern the user wants emulated separately from the master voiceprint.

The template wraps a verbatim source passage in the library style-sample frontmatter so os-library/save can persist it correctly. The body content is the actual passage from the source book — no commentary, no analysis, no rewrite. The frontmatter carries the metadata downstream skills need to find and load the sample.

## File structure

```
---
type: style-sample
author: <name>
pattern: action-scene | dialogue | interior-reflection | descriptive-passage | exposition | hook-opener | <other>
genre: <optional, for fiction>
source: <provenance — book title + chapter, page range>
length: <approximate word count>
notes: <freeform — when this move works, what it teaches>
---

[The verbatim source passage — 200-500 words. No editorial commentary, no markdown headers within the passage itself. Just the prose.]
```

## Field guidance

**`type`** is always `style-sample` for files in this directory.

**`author`** matches the pen name, real name, or other-author identifier the user supplied at the start of the from-book run. Lowercase with hyphens.

**`pattern`** names the specific writing move the sample demonstrates. From-book stage 1 (the survey) typically identifies which patterns are distinctive enough to warrant samples. Common values surfaced by from-book: `action-scene`, `dialogue`, `interior-reflection`, `descriptive-passage`, `exposition`, `comic-relief`. The pattern values are descriptive labels, not enum-bound.

**`genre`** applies to fiction sources. Set to the manuscript's genre when known.

**`source`** describes where the passage came from. From-book typically generates this as `"<book title> — <chapter or section reference>"`. Specific page or paragraph references help when the user later wants to verify the sample against the source.

**`length`** is the approximate word count of the passage. Useful for quick scanning when picking which sample to load (a 200-word fragment trains differently than a 500-word scene).

**`notes`** is freeform. From-book stage 3 typically generates notes from the survey context — what the survey identified about how this pattern reads in this manuscript, which scene types or moments the pattern covers, any caveats about transferability.

## The passage body

The body of the file is the verbatim source passage. From-book extracts the passage from the manuscript without modification. The passage runs 200-500 words for a typical sample.

If the passage benefits from a paragraph of context before or after it (a setup line that makes the passage's job clearer when loaded as a few-shot exemplar), include the context inline with the passage rather than as separate framing. The downstream skill that loads the sample sees the prose as it reads, with whatever context the user curated alongside.

No editorial commentary inside the body. No markdown headers within the passage (the file's frontmatter and the optional context-paragraph are the only structural elements). The point is preserving the source prose intact so downstream skills load it as a faithful exemplar.

## Worked example

Filename produced by from-book: `os-inputs/style-samples/pen-name-x/action-scene.md`

```yaml
---
type: style-sample
author: pen-name-x
pattern: action-scene
genre: urban fantasy
source: "Pen Name X — Book One, ch. 5, the rooftop chase"
length: 312 words
notes: "From-book stage 3 identified this passage as the cleanest example of the manuscript's action treatment. The rhythm shift between Nova's interior monologue and externalized action is the move worth emulating. Voice protected — don't smooth the run-ons. Pairs with pen-name-x-protagonist-nova voiceprint."
---

The wind carried the smell of ozone across the rooftop, sharp enough to make Nova's eyes water. Her fingers found the seam in the wall — three inches wide, six feet up, exactly where Maccay said it would be — and she pushed.

[Verbatim passage continues for 312 words, ending at the natural scene beat.]
```

## How from-book uses this template

In stage 3 of `from-book`, the mode:

1. Identifies passages from the manuscript that match patterns flagged in the stage-2 capture plan
2. Extracts each passage verbatim
3. Drafts the frontmatter (author from the project, pattern from the survey, source from the manuscript reference, length by counting, notes synthesized from survey observations)
4. Composes the file using this template
5. Calls os-library/save to persist with proper frontmatter

The user sees the proposed frontmatter and passage before save and can adjust before the file is written.

## When to add a style sample manually vs. via from-book

From-book produces style samples as part of a layered extraction from a book-length source. The samples are derivative of the survey — they capture patterns the survey flagged.

When the user wants to add a style sample outside the from-book flow (a passage from a book they didn't run from-book on, a passage from their own writing they want curated), the manual path is to invoke `os-library/save` directly with the passage and frontmatter values. The os-library/save flow uses the same style-sample schema documented in `../../os-library/references/style-sample-schema.md`.
