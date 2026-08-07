---
name: os-editing/shorten
description: Compress a draft 5-20% while preserving voice, argument, and specifics. Cut filler / hedges / qualifiers first, restructure last, preserve proper nouns, numbers, named examples. Output is the shortened version + word-count delta + 2-3 line summary of what was cut. Triggers when the user wants a draft tightened, compressed, condensed, or shortened — but wants the substance to survive. Do NOT trigger when the user wants AI-tells removed (use `humanize`), structural recommendations (use `assessment`), or sentence-level edits (use `suggest-edits`).
---

# Mode — Shorten

Compress a draft 5-20% while preserving voice, argument, and specifics. Output is the transformed text, not a suggestion list.

## Purpose

The user wants the draft tighter — more time-to-value for the reader, less filler — but they want the substance, voice, and structure to survive. They do NOT want a wholesale rewrite or restructure (those are different jobs and require explicit user direction).

## When to use

- "Tighten this up"
- "Cut this down"
- "Shorten this by [X]%"
- "Make this more time-to-value"
- "Trim the fat"
- After `assessment` flagged Engagement & Impact at "Tune-up" or below for length-driven reasons
- After `humanize`, if the cleaned version is still too long for its slot. Run in that order — humanize has no length target and may return something longer, so compressing first wastes the work

## Inputs

- The draft (text, attached file, or pasted)
- Optional: target reduction (default range 5-20%, default target 10-15%)
- Optional: stated voice goal or context

## Run — the 8-step process

### 1. Initial assessment

Read the entire content twice. First pass for the main argument, key points, tone, and overall structure. Second pass for line-level detail. Don't make cuts yet — understand the piece first.

### 2. Redundancy analysis

Identify repeated concepts, phrases, or ideas that appear in multiple forms throughout the text. Mark instances where the same point is made unnecessarily. (Cross-reference: `../references/edit-lenses.md` redundancy lens, especially the 4 cases of repetition.)

### 3. Verbose pattern recognition

Locate wordy constructions:
- Unnecessary qualifiers ("very," "quite," "rather," "actually," "basically," "really")
- Redundant adjective stacks
- Phrases that could be expressed more concisely (see redundancy lens phrase-reduction list — *"in spite of the fact that"* → *"although"*, *"during the course of"* → *"during"*, etc.)

### 4. Structural evaluation

Examine sentence structure for:
- Adjacent ideas that could be combined into a single sentence
- Filler transitions that can be cut without losing flow
- Complex constructions that simplify cleanly

### 5. Precision enhancement

Replace vague or general terms with more specific alternatives **when doing so reduces word count or maintains the same word count with better meaning**. (Don't add words for specificity — that's a different mode. Here, specificity-as-compression: a single named noun replacing a 5-word abstraction.)

### 6. Flow preservation

Ensure cuts maintain logical progression and don't create awkward transitions or gaps in reasoning. After cuts, re-read for flow.

### 7. Voice consistency check

Verify edits preserve the original author's tone, style, and personality. Specifically:
- **If the writer hedges as a stylistic choice**, don't mass-cut hedges. Flag them as candidates but preserve voice-calibrated hedging.
- **Preserve proper nouns**, numbers, named examples — these are usually the concrete substance carrying the meaning. Cutting them produces blander writing.
- **Preserve sentence variety and rhythm.** A shortened version that's all short sentences is worse than a slightly longer version with rhythmic variety.

### 8. Final review

Read the revised content aloud (mentally) to ensure it flows naturally and maintains the intended impact.

## Cut ordering — filler first, restructure last

The order matters. Voice survives this order. Voice doesn't survive arbitrary order:

1. **Filler words first.** "Just," "really," "very," "actually," "basically." These are voice-neutral.
2. **Redundant phrases next.** "Absolutely essential" → "essential", "in spite of the fact that" → "although." Still voice-neutral.
3. **Hedges and qualifiers third.** "Could be," "might," "may." Calibrate to voice — if the writer hedges stylistically, leave most hedges alone.
4. **Adjacent-idea consolidation fourth.** Two sentences making the same point → one sentence. This starts touching voice.
5. **Sentence restructuring last.** Most voice-touching. Only restructure when the cut is high-leverage.

## Constraints

- **Preserve original meaning and intent of all key points without exception.**
- **Maintain the author's distinctive voice, tone, and writing style throughout.**
- **Avoid changing specialized terminology, proper nouns, or technical language** that serves specific purposes.
- **Do not eliminate supporting evidence, examples, or details** crucial to the argument.
- **Keep sentence variety and rhythm** that contributes to readability.
- **Resist the urge to rewrite extensively.** Strategic cuts and minor refinements, not wholesale restructuring.
- **Default range: 5-20% reduction.** If the user requests >20%, name the trade-off plainly: past 20%, voice and structure usually need rewriting rather than editing, and the result will read as a different piece rather than a tighter version of the same one. Offer to take it to whichever band the user confirms after hearing the trade-off.

## Output

```
{The shortened content in full, maintaining the original formatting and structure.}

---

**Compression summary:**
- Original word count: {N}
- Shortened word count: {N}
- Reduction: {X}%
- Primary cuts: {2-3 sentence summary of what was cut — filler / qualifiers / redundant phrases / consolidated paragraphs / etc.}
- Voice preserved: {when the writer flagged a voice intent — hedging style, fragment use, etc. — name the patterns that were kept verbatim, so the calibration is auditable. Skip this line if no voice intent was flagged.}
```

## Output discipline

- **Output the full shortened content first.** The user pastes it into their draft.
- **Compression summary at the end** — short, concrete, names what was cut.
- **No preamble.** Begin with the shortened content's first line.
- **Preserve original formatting** (headers, lists, bolding, links) unless the user asked for format changes.

## Cross-mode suggestions (NOT a postamble)

Like `humanize`, `shorten`'s primary output is pasteable transformed text — the user copies the shortened content (and optionally the compression summary) back into their draft. Cross-mode pointers don't belong inside that delivery; they live in the hub layer surrounding it.

If a hub-layer follow-up is useful after the shortened text is delivered, the typical next steps include `humanize` when the compressed version still reads machine-flavored (though the cleaner order is humanize first, then shorten), `tone-profile` on both versions when the writer wants to verify the tone survived the cut, and naming structural rewriting (rather than editing) when the user is pushing for deeper compression than 20% covers. These belong in a separate message after the shortened delivery is complete — never embedded as a footer inside the output the user will paste.

## Design rationale

- **5-20% default range** because narrow enough that voice survives, wide enough that the edit is meaningfully tighter. More aggressive cuts (40%+) require structural rewriting that breaks the "preserve voice" guarantee.
- **Cut filler first, restructure last** because filler (just / really / very / actually) is voice-neutral. Restructuring is voice-touching. Ordering protects voice.
- **Preserve specifics (proper nouns, numbers, named examples)** because these are usually the concrete substance carrying the meaning. Cutting them produces blander writing in the name of brevity.
- **Hedge cutting calibrated to author intent** rather than indiscriminate, because if the author hedges stylistically, mass-cutting changes voice. The mode flags hedges as candidates but does not mass-cut them.
- **Refuse-with-explanation past 20%** because the user often doesn't realize that aggressive compression IS rewriting. Naming the line lets the user choose with full information.
- **Compression summary at the end** rather than as a preamble because the user wants the shortened content first. The meta-information is secondary.

