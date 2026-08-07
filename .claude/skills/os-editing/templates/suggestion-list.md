# Template — Suggestion List

The shared output format for `modes/suggest-edits` across all lenses. Preserved verbatim from CE 101 sources because the formatting is part of why these outputs scan well: bolded labels, location reference, terse issue + suggestion lines, easy to skim across many entries.

## Format (per suggestion)

Output suggestions as a numbered list. Each entry follows this exact structure:

```
### N - {very short title or description of the issue/suggestion}
__Location__: {line number, paragraph number, or quoted span}
__Issue__: {short description of what is there and what is missing or could be improved — use **bolding** to highlight the specific words/phrases at issue}
__Suggestion__: {concise one-line explanation of the edit, including the suggested replacement text, written in the writer's own voice/style. If a rewrite is suggested, match the original structure, punctuation, and line-break patterns.}
```

Continue numbering sequentially: `### 1 -`, `### 2 -`, `### 3 -`, etc.

When multiple suggestions apply to the same passage, synthesize into a single unified entry. If multiple lenses produced the suggestions, name the lenses in the synthesis label:

```
### N - {synthesized title} (combining {lens-1} + {lens-2})
__Location__: {line / paragraph / passage}
__Issue__: {synthesized issue description with **bolded** terms}
__Suggestion__: {unified suggestion in the writer's voice}
```

If a single lens produced multiple overlapping suggestions on one passage, drop the lens-name parenthetical and just synthesize: `### N - {synthesized title}`.

## Required formatting rules

- `__Location__:`, `__Issue__:`, `__Suggestion__:` use markdown bold (double-underscore style around the label keyword, with the colon outside — visually anchors the labels regardless of renderer, and some renderers also italicize, both are fine)
- The `__Issue__` line **always** contains **bolding** on the specific words or phrases the suggestion addresses. This is non-optional — without bolding, the issue line dilutes into prose
- No intro or conclusion text. The output begins with `### 1 - ...` and ends with the last numbered entry
- If there are no issues to flag, say so explicitly with one sentence ("No issues to flag — this passage scans clean")
- If there are multiple issues across the draft, no need to summarize — the numbered list is the report

## Voice match

Suggested rewrites must match the writer's voice — sentence rhythm, register, vocabulary, syntactic quirks, idiosyncratic punctuation. If the writer uses fragments, the rewrite can use fragments. If the writer never uses semicolons, the rewrite shouldn't introduce them. A suggestion that doesn't match voice is worse than no suggestion.

## What NOT to include

- Don't include passages that have no issue. The suggestion list is actionable items only.
- Don't include praise ("This paragraph is great!"). The mode produces edits, not encouragement.
- Don't include preamble ("Here are my suggestions for your draft..."). Begin with `### 1 -`.
- Don't include conclusion ("Hope these help! Let me know if you have questions."). End with the last entry.

## Example

```
### 1 - Vague claim about results
__Location__: paragraph 2, sentence 1
__Issue__: "Many businesses see results" — **vague**, readers won't trust it. The number is the piece that would make the claim credible, and it's missing.
__Suggestion__: Replace with a specific claim if you have data: "Most B2B SaaS companies see a 14-22% lift after the rollout." If no data, drop the claim entirely.

### 2 - Passive voice flattens the close
__Location__: final paragraph, sentence 3
__Issue__: "Mistakes were made and lessons were learned" — **passive**, distancing, weakens the takeaway.
__Suggestion__: "I made mistakes. I learned what I needed to."
```

