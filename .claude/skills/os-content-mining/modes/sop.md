# Mode: sop

Part of the `os-content-mining` skill. Selected when the user wants to pull a *working procedure* out of a source — not ideas to write about, but steps to follow.

## Job

Turn the how-to knowledge buried in a source into one or more SOP files: single, self-contained documents that each hold a complete workflow — the steps, the reasoning behind them, and an honest account of what the source didn't explain. An SOP is both a thing to keep (it lives in your knowledge folder and you can follow it directly) and raw material for later (a skill can be built from it — `os-skillify/from-prompt` accepts an SOP as input).

The difference from the default mining run, in one line: the default run extracts what a source *says* so you can create content from it. This mode extracts what a source *teaches you to do* so you can do it.

## Run

### 1. Read the source and survey the candidates

Read the whole source. List every procedure it carries — every place where someone explains a repeatable way of doing something. For each candidate, give a one-line completeness read using the three grades in `../../_shared/references/sop-completeness.md`:

- **Runnable** — the source gives you enough to actually follow the procedure.
- **Partial** — the shape is there but real steps are missing; extracting it means filling gaps, and every fill must be marked.
- **Named-only** — the source mentions the procedure, maybe sells it, but never explains it. Not extractable. Say so and move on — a named-only procedure written up confidently is a summary wearing a checklist's clothes.

Show the survey to the user before extracting anything. It's short, and it's where the honest conversation about the source happens.

### 2. Ask: one document or several?

Sources often carry more than one procedure. Ask the user how they want them packaged. The default worth suggesting: separate files when the procedures stand on their own (each gets found, followed, and possibly promoted to a skill independently), one combined file when they're stages of a single larger workflow that nobody would run separately.

### 3. Extract each SOP to the single-file shape

Use `../templates/sop-output.md`. Everything about the procedure goes in the one file — a reader should never need the source open beside it, and never need a second file to run it.

While writing, hold the mining skill's standing rule: follow the source's strengths, never pad. Where the source is rich, go deep. Where it's thin, the SOP says it's thin.

### 4. Mark every gap you filled

When the source leaves a step unspecified and the procedure needs one — a time-box, an ordering, a default — you may supply it, but the supplied piece gets marked `[filled in]` right where it appears. And anything the source names but never explains goes in the closing "what this doesn't cover" section.

This is the step that makes the file trustworthy. A confident document with no gap marks and no coverage notes looks exactly like a careful extraction until someone checks it against the source. The marks are what let a reader — or a future skill-builder — audit the SOP without re-reading the source.

### 5. Save to the knowledge folder

SOPs land in `os-knowledge/`, named `sop-<what-it-does>.md`, with the standard lightweight frontmatter. They're knowledge files on purpose: readable, followable, citable — and available later as fodder for `os-skillify` if the procedure earns automation.

## Output

One file per SOP (or one combined file, per the user's choice in step 2), each following `../templates/sop-output.md`. Plus the survey from step 1, delivered in chat — including the candidates that *didn't* make the cut and why.

## Related

- `../../_shared/references/sop-completeness.md` — the three grades, with worked examples
- `../templates/sop-output.md` — the single-file shape
- `os-skillify/from-prompt` — where an SOP goes when it's time to become a skill
