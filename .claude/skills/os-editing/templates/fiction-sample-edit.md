# Template — Fiction Sample Edit

The output shape for `modes/fiction-edit` when the mode is producing example edits with rationale (the most useful default for fiction work because voice/style is perceptible only by side-by-side comparison).

## Format (per flagged passage)

```
> **Original:** "{the passage verbatim}"
>
> **Rationale:** {what's wrong, in plain terms — clichés, redundancy, vague verbs, awkward construction, voice issue, etc. Distinguish subjective preferences from objective issues.}
>
> **Suggested Edits:**
>
> 1. {first rewrite option, in the author's voice}
> 2. {second rewrite option, alternate emphasis or rhythm}
```

The blockquote markdown (`>`) is intentional — it visually nests the edit unit and reads naturally as a side-by-side comparison.

Why two rewrite options (not one): voice judgments are subjective, and offering 2-3 alternatives respects the author's agency more than dictating a single rewrite. The author picks the one that fits their voice, or declines both.

**Layer-3-protected passages (when Voice-Sensitive Filter fires hard):** acceptable form is `(Leave as written.) — {one-line reason the rhythm is voice}` paired with `(Only if you want X:) — {alternative rewrite}`. This is preferred over manufacturing a fake second option just to hit the count. The conditional-alternative format makes the keep-or-change choice auditable.

## Output discipline

- **In-line edited manuscript is the preferred output if the user only wants the cleaned text.** Sample Edit Format is for sections where rationale is requested or where the issue warrants explanation.
- **Don't rewrite or reimagine the author's scenes.** The job is to clean, polish, and elevate the original — not ghostwrite. Keep the author's setup, characters, beats, and outcomes intact.
- **Use blockquote nesting (`>`) so each edit unit is visually self-contained.** Multiple edits read cleanly when stacked.
- **No preamble.** Begin with the first `> **Original:**` line.

## Adjacent: in-line edited manuscript (when the user wants the cleaned text only)

When the user requests "in-line edits" or "just give me the cleaned manuscript," return the rewritten passage in full, verbatim, with no markup, no comments, no rationale. Equivalent to running `humanize` for fiction prose, but with the Voice-Sensitive Filter applied.

Output discipline for in-line manuscript:
- The full edited manuscript text. No surrounding prose, no preamble, no postamble.
- Preserve the author's chapter/scene/paragraph breaks exactly. Do not re-paragraph or re-format unless the original formatting was broken.
- If a passage has issues but the fix would require subjective voice calls, leave the passage unchanged (don't impose taste in in-line mode) and use Sample Edit Format for those passages instead.
- If the user asked for both in-line edits AND rationale, run Sample Edit Format only — the two formats are not combined into a single output.

## Adjacent: developmental-feedback format (when to use)

If the issue is at the manuscript level (narrative flow, character consistency, scene purpose, motivation, pacing) rather than line-level prose, use this looser format instead:

```
> **{Issue type — Narrative Flow / Character Consistency / Scene Purpose / Motivation Clarity / Pacing}:**
> "{specific observation about a chapter, scene, or beat}"
>
> **Suggestion:** {a structural suggestion, NOT a rewrite}
```

Developmental notes don't include rewrites — they propose a direction the author considers. The author owns the scene. The editor owns the diagnostic.

## Style of edit suggestions

- Clean and confident
- Occasionally witty or sharp when warranted, but never snide
- Minimal explanation unless requested
- Reads like a manuscript touched by a pro, not an algorithm

