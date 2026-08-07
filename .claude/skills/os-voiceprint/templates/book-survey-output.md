# Template — Book Survey Output

The output shape for `from-book` stage 2. Combines the survey report (what the manuscript looks like at the voice-landscape level) with the proposed capture plan (what to extract and why). The user reviews and approves before stage 3 runs.

## Format

```
## Survey: <book title or descriptor>

[Short report — 200-400 words covering the five survey questions]

### POV characters
[Which POVs appear and which chapters belong to each. Distinctiveness assessment: are the voices similar enough that a master alone suffices, or different enough that overlays help?]

### Scene types and treatments
[What scene types appear and which are distinctively handled. Action, dialogue, interior, descriptive, exposition, comic relief — name the ones worth flagging.]

### Register variations
[Any broader variations: genre hybrids, time-period shifts, format breaks, tonal arcs.]

### Structural anomalies
[Frame narratives, found-document insertions, epistolary sections — anything that stands apart from the dominant voice.]

### Dominant voice
[Brief description of the master voice the master voiceprint will need to capture.]

## Proposed capture plan

Based on the survey, here's what I'd recommend extracting:

1. **Master voiceprint** — `<filename>.md`, scope: `<scope>`. Captures the dominant voice across the manuscript.
2. **<Per-POV / genre-overlay layers, if any>** — `<filename>.md`, scope: `<scope>`. [What this overlay captures and why it warrants its own voiceprint.]
3. **<Style samples, if any>** — `<author>/<pattern>.md`, pattern: `<pattern>`. [What this sample demonstrates and why it warrants its own file.]

[Continue listing layers, with rationale per layer]

### Layers I considered but recommend skipping

[Any layers that could exist but probably aren't worth the extraction time, with brief reasons. The frame narrator with limited page count, the genre-overlay that's actually consistent enough to fold into master, etc.]

## Confirm

Approve as proposed, adjust specific layers, add layers I didn't suggest, or simplify to master-only?
```

## Worked example

```
## Survey: Nova Cayce — Book One (urban fantasy)

This is a 312-page urban fantasy with three close-third POV characters: protagonist Nova (chapters 1-4, 7-9, 12-15 — about 60% of the book), antagonist Harvard (chapters 5-6, 10-11), and a brief frame narrator (prologue, epilogue). Nova's interior is distinctive — noir-inflected, paratactic, sensory. Harvard's interior is sparser, more observational. The frame narrator's voice differs from both and is distinct enough to flag, though the limited page count (8 pages total across prologue and epilogue) probably doesn't warrant a full voiceprint.

Scene types include extended action sequences (notably the rooftop chase in chapter 2 and the warehouse confrontation in chapter 14), dialogue-heavy investigation scenes (chapters 7-8 where Nova and Alec interview informants), and a recurring flashback motif (Nova's childhood — chapters 3, 9, 14). The action sequences in particular have a distinctive paratactic-rhythm treatment worth capturing. The interior-flashback treatment is also distinctive.

The overall register is dark urban fantasy with noir signatures — tactile, grime-textured, period-appropriate slang ("doughboys," "chromed up," "*maricòn*"), italicized interior thought mid-action, comma-spliced run-ons in interior voice.

### POV characters
Three POVs. Nova and Harvard are voice-distinct enough to warrant overlays. The frame narrator's brief footprint doesn't justify a full voiceprint.

### Scene types and treatments
Action, dialogue, interior reflection (especially flashback), descriptive (atmospheric noir setting). Action and interior-reflection are most distinctive.

### Register variations
None significant beyond the POV variation. The book is consistently urban-fantasy noir throughout.

### Structural anomalies
Frame narrative (prologue + epilogue from a different narrator). Worth flagging in survey notes but not capturing as a full layer.

### Dominant voice
Noir-inflected close-third in past tense, with sensory-tactile texture and paratactic interior runs. The master voiceprint captures this.

## Proposed capture plan

Based on the survey, here's what I'd recommend extracting:

1. **Master voiceprint** — `pen-name-x.md`, scope: `fiction-urban-fantasy`. Captures the dominant noir close-third voice across the manuscript.

2. **Per-POV overlay (Nova)** — `pen-name-x-protagonist-nova.md`, scope: `fiction-pov-nova`. Nova's interior is the most voice-distinctive thread in the book — noir-inflected, paratactic, sensory. Drafting Nova chapters benefits from the overlay alongside the master.

3. **Per-POV overlay (Harvard)** — `pen-name-x-antagonist-harvard.md`, scope: `fiction-pov-harvard`. Harvard's observational distance is distinct enough to warrant an overlay — a flat, watchful register that contrasts with Nova's close-third density.

4. **Style sample (action)** — `pen-name-x/action-scene.md`, pattern: `action-scene`. The rooftop chase from chapter 2 — 312 words. Demonstrates the paratactic rhythm Nova carries through fight choreography.

5. **Style sample (interior reflection / flashback)** — `pen-name-x/interior-reflection.md`, pattern: `interior-reflection`. The Yoofie flashback from chapter 3 — 400 words. Demonstrates how Nova's interior shifts into childhood-memory register.

### Layers I considered but recommend skipping

- Frame-narrator voiceprint: only 8 pages of source, too thin to extract a useful artifact. The voice is noted in survey but skipped in the plan.
- Dialogue style sample: the dialogue is well-handled but not so distinctive that a sample would teach drafting more than the master + per-POV overlays already do.
- Genre overlay (`fiction-urban-fantasy-noir`): the noir treatment is fully captured in the master voiceprint, no separate overlay needed.

## Confirm

Approve as proposed, adjust specific layers, add layers I didn't suggest (e.g., a dialogue sample if you disagree with my call), or simplify to master-only?
```

## After confirmation

Once the user approves the plan, stage 3 runs the extractions one layer at a time. Each layer's output is presented before stage 4 saves through library. The user can stop, redo, or skip any individual layer mid-flow.

## Output discipline

The survey report is concise — 200-400 words for the prose section. It does not produce voiceprint content (that's stage 3's job). It does not exhaustively analyze the manuscript (that defeats the survey's purpose).

The capture plan is structured as a numbered list with one-line rationale per layer. Each layer has a proposed filename, frontmatter highlights (scope, pattern), and brief justification. The "layers I considered but recommend skipping" section is short — three or four bullets — and exists so the user can see what was considered without having to ask.

The closing "Confirm" line is the user-interaction seam. The mode does not extract anything until the user responds.
