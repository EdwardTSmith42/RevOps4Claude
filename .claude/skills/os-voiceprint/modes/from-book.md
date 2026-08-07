---
name: os-voiceprint/from-book
description: Produce a layered voiceprint from a book-length manuscript — survey the book's voice landscape (POVs, scene types, register shifts), recommend a capture plan, then extract a master voiceprint plus optional per-POV voiceprint overlays plus optional curated style samples. Output is multiple files (one or more voiceprints plus zero or more style samples), each saved through os-library/save with proper frontmatter. Triggers on "extract voiceprint from this book," "create voiceprint for my pen name's book," "analyze this manuscript's voice." Do NOT trigger for short samples (use `from-sample`) or for ingesting an existing voiceprint (use `import`).
---

# Mode — From Book

Layered voiceprint extraction for book-length sources. A book is a different beast from a paragraph — multiple POVs, scene types, register variations across chapters, narrator-vs-character voice distinctions. A flat voiceprint loses these. This mode surveys the manuscript first, recommends what to capture, then extracts each layer the user approves.

The output is typically multiple files: one master voiceprint capturing the dominant voice, optional per-POV voiceprints for distinct character narrators, optional style samples for specific patterns the user wants emulated separately (action scenes, dialogue rhythm, interior reflection).

## When to use

The user has a book-length manuscript and wants a voiceprint or voiceprint family. Sources include the user's own books (memoir, business book), pen-name fiction, external authors whose voice the user wants to emulate.

The mode handles books that are 40+ pages with multiple chapters. Shorter samples (single chapters, fragments) are better served by `from-sample`. If the user supplies something on the border, ask whether to treat it as one piece (from-sample) or as a multi-chapter sample worth surveying (from-book).

## Inputs

- **Required:** A book-length manuscript or a substantial chapter set. Could be a file path, a pasted long-form text, or a directory of chapter files. Total content typically 30k-120k+ words.
- **Optional:** Stated `author` (the writer's name — the user's, a pen name, or an external author). If the user is the author and the work is a self-publication, use the user's name. For pen names and external authors, ask explicitly.
- **Optional:** Stated `genre` (literary fiction, urban fantasy, romance, thriller, memoir, business). Helpful for the survey since genre affects what kind of voice variations are normal.
- **Optional:** Specific intent — "I just want a master voiceprint, skip the overlays" / "I want per-character voiceprints, the POVs are very distinct" / "I want style samples for action scenes specifically."
- **Optional:** Time budget. Book-length surveys are slower than from-sample runs. The mode can scale: a quick scan + master voiceprint only, or a full survey + multiple layers.

## Run — the four-stage procedure

The mode runs through four stages with user interaction at the seam between stages two and three. Stages 1-2 produce a survey and a capture plan. Stage 3 runs the extractions. Stage 4 saves the layered output.

### Stage 1 — Survey the book's voice landscape

Read or sample-scan the manuscript to identify the voice landscape. The survey method is documented fully in `../references/book-survey-method.md`. Briefly: scan chapter starts and ends, sample mid-chapter passages, identify POV characters and tense shifts, note register variations across scene types (action vs. dialogue vs. interior vs. descriptive vs. exposition), spot any deliberate register breaks (a chapter from a different narrator, a found-document insertion, an epistolary section).

Produce a survey report covering: how many POV characters appear and which chapters belong to which, what scene types appear and how distinct their treatment is, what register variations exist across chapters, any structural voice anomalies worth flagging.

The survey is fast — chapter-level, not line-level. The goal is to map the landscape, not analyze every passage. Detailed analysis happens in stage 3 only on the layers the user selects.

### Stage 2 — Recommend a capture plan

Based on the survey, recommend what to capture. The default plan covers most cases:

- **Always:** A master voiceprint capturing the dominant voice (the one that runs across most chapters, scene types, and POVs)
- **If POVs are distinct:** Per-POV voiceprint overlays for characters whose narrative voice differs meaningfully from the master. A book in close-third with three POV characters where each has distinctive interior voice gets three overlays. A book where POVs are similar in register gets none.
- **If scene types are distinctive:** Curated style samples for specific patterns the user wants emulated separately. A noir thriller with extended action scenes might get an `action-scene` style sample. A literary novel with extended interior reflection might get an `interior-reflection` sample.
- **If genre or register splits exist:** Possibly a genre-overlay voiceprint (e.g., a literary-thriller hybrid might get a `master` voiceprint plus a `thriller-pacing` overlay).

Present the plan with rationale per layer. Let the user adjust: keep all, drop overlays, add custom layers ("I want a style sample for the dream-sequence scenes specifically"), simplify to master-only.

The survey report and the proposed capture plan together form stage 2's output. The user reviews and approves before stage 3 begins. See `../templates/book-survey-output.md` for the format.

### Stage 3 — Extract each approved layer

For each layer the user approved, run extraction:

**Master voiceprint:** Sample broadly across the manuscript (3-5k words drawn from chapter beginnings, middles, and ends, representative across POVs and scene types if applicable). Run the from-sample two-pass procedure on the sampled content. The output is a master voiceprint with `scope: fiction-<genre>` (or another scope value if the book isn't fiction).

**Per-POV voiceprint:** Sample 1.5-2k words from chapters belonging to that POV character, focused on passages where the POV's distinctive voice is clearest (interior reflection, characteristic dialogue, signature observations). Run the from-sample procedure on the sampled content. The output is a voiceprint with `scope: fiction-pov-<character>` (or similar). Notes field captures what makes this POV distinct from the master.

**Style sample:** Identify a representative 200-500 word passage demonstrating the pattern. The style sample is NOT a voiceprint — it's a verbatim passage with frontmatter (per the style-sample schema in `../../os-library/references/style-sample-schema.md`). The mode extracts the passage, drafts the frontmatter (author, pattern, source, length, notes), and saves through library.

**Genre-overlay voiceprint:** Only if the user requested one. Sample passages where the overlay's distinctive register is clearest. Produce a voiceprint with a scope value naming the overlay (e.g., `fiction-thriller-pacing` for a thriller-pacing overlay layered on a literary master).

Each extraction runs the era-tells self-check before output, just like from-sample. Each artifact must pass the source-cleanliness gate (no quoted source text, no source-specific lexemes, no source topics in the portrait — invented-concrete is fine).

### Stage 4 — Compose layered output and save

Compose the full layered output: the master voiceprint file, any per-POV voiceprint files, any style sample files. Each conforms to its respective frontmatter schema.

Save the stage-2-approved layers via os-library/save without re-asking — the user already approved the capture plan in stage 2, and asking again interrupts more than it protects. The mode invokes os-library/save for each approved layer with validated frontmatter, writes to the right location, and surfaces the saved paths in the final summary.

Two exceptions warrant a confirmation seam at stage 4. First, when a layer's first extraction came back weak or off-target (the era-tells self-check flagged issues, the source-cleanliness gate caught leakage, the per-POV portrait drifted from the survey's stated character voice) — the mode pauses to surface the issue and asks whether to retry that layer, drop it, or save anyway. Second, when a filename collision occurs at save time (a voiceprint already exists at the target path) — the mode asks before overwriting, per the standard os-library/save collision-handling pattern.

The user-profile is referenced for the `author` value when the manuscript is the user's own work. For pen names and external authors, the author value is what the user supplied at input.

## Output

Multiple files written to `os-inputs/voiceprints/` and (optionally) `os-inputs/style-samples/<author>/`. The mode produces a final summary listing every file written, with a brief note on what each layer captures. The user has both the artifacts and a map of how they relate.

Example layered output for a pen-name urban fantasy book:

```
Saved layered voiceprint for pen-name-x:

os-inputs/voiceprints/pen-name-x.md
  Master voiceprint, scope: fiction-urban-fantasy. Captures the dominant voice across the book.

os-inputs/voiceprints/pen-name-x-protagonist-nova.md
  Per-POV overlay for protagonist Nova. Distinctive close-third interior, noir-inflected.

os-inputs/voiceprints/pen-name-x-antagonist-harvard.md
  Per-POV overlay for Harvard. Sparse, observational, more matter-of-fact.

os-inputs/style-samples/pen-name-x/action-scene.md
  Style sample, pattern: action-scene. The rooftop-chase passage.

os-inputs/style-samples/pen-name-x/interior-reflection.md
  Style sample, pattern: interior-reflection. The Yoofie-flashback passage.
```

When the user later invokes drafting for a chapter in this voice, the matcher loads pen-name-x.md as master, optionally pen-name-x-protagonist-nova.md as overlay, and the relevant style samples as few-shot exemplars.

## Output discipline

Every produced voiceprint must pass the era-tells self-check and the source-cleanliness gate. The Voiceprint portrait section is what downstream skills consume. The Analysis section is the audit layer.

Style samples are verbatim passages from the source, NOT voiceprints. The style sample's body is the actual prose, untouched. Frontmatter captures the metadata (author, pattern, source, length, notes).

The mode does not silently overwrite existing voiceprints. If a voiceprint for the same author exists at the target path, the mode asks whether to overwrite (regenerating an updated voiceprint) or save under a different filename.

## Cross-mode suggestions

After a from-book run, the user typically has the layered voiceprint family they need. Useful follow-ups: drafting can now load the master and overlays via os-library/find when producing chapters in this voice. If the user wants to add more style samples beyond what the survey identified, manual curation via os-library/save is the path. If the master voiceprint feels off after first use in drafting, regenerating with adjusted survey notes is fast.

## Design rationale

The survey-then-plan structure exists because flat extraction loses register and POV variation. A user with a multi-POV urban fantasy book gets a worse voiceprint from a single broad sample than from a master plus per-POV overlays. The survey identifies what's worth capturing. The user decides what's worth the extraction time.

User interaction at the stage-2 seam is deliberate. Different users want different layers. Some want master-only and ignore overlays. Some want a complete family. Asking before extraction respects user time and prevents producing layers the user won't use.

Per-POV voiceprints are scoped specifically (e.g., `scope: fiction-pov-nova`) so the matcher can load them as overlays alongside the master rather than competing with the master at find time. The drafting matcher's job is then to load master + relevant overlay + style samples for the scene type, all keyed to the same author.

Style samples extracted during from-book live alongside voiceprints because they answer different questions. The voiceprint teaches the *what* and *why* abstractly. The style sample shows the *how* concretely. Drafting often loads both for fiction work — the voiceprint as voice context, the samples as few-shot exemplars for specific scene types.

The mode deliberately does not produce per-chapter voiceprints. Chapter-level granularity is too narrow for portable artifacts. POV granularity is the smallest unit that produces useful overlays.
