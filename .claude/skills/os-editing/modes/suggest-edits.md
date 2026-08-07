---
name: os-editing/suggest-edits
description: Produce a numbered suggestion list of focused editorial improvements across one or more selectable lenses (copy-edit, redundancy, active-voice, specificity, developmental, what-why-how, takeaway). Triggers when the user wants a structured edit pass with actionable line-by-line suggestions, not a rewrite or scored assessment. Output is a numbered list with bolded `__Location__:`, `__Issue__:`, `__Suggestion__:` per entry. Do NOT trigger when the user wants edited prose returned (use `humanize`), a scored assessment with verdict (use `assessment`), or a tone description (use `tone-profile`).
---

# Mode — Suggest Edits

Lens-based suggestion-list editing. Run one or more editorial lenses against a draft and produce a numbered list of improvement suggestions in the shared CE 101 format.

## Purpose

The user wants focused, actionable editorial suggestions on existing prose. They want to see the edits as a list, evaluate each one, and choose what to apply. They do not want the prose rewritten for them and they do not want a scored review.

## When to use

- "Edit this draft" / "give me feedback on this" with no further specification — default to **copy-edit lens**
- "Check this for [specific issue: redundancy / passive voice / vagueness / argument / takeaway]" — run the matching lens
- "Run a full edit pass" — run all lenses that fit the draft
- After `assessment` flagged a specific dimension — run `suggest-edits` with the matching lens

## Inputs

- The draft (text, attached file, or pasted)
- Optional: lens selection (one, multiple, or "all")
- Optional: writer's stated intent (target audience, register, voice goal) — informs voice-match

## Lens selection

Available lenses (full descriptions in `../references/edit-lenses.md`):

| Lens | Best for |
|---|---|
| `copy-edit` | General default — sentence-level mechanics across 6 dimensions (redundancy, active voice, tenses, parallelism, sentence structure, specificity) |
| `redundancy` | Drafts that feel padded, or deeper redundancy / repetition work |
| `active-voice` | Drafts that read as distant or evasive, persuasive content |
| `specificity` | Drafts that feel vague — marketing copy, credibility claims, how-to content |
| `developmental` | Argumentative or persuasive content, paragraphs that need stronger Claim-Support-Takeaway |
| `what-why-how` | How-to / instructional content, paragraphs that name a What without explaining Why or How |
| `takeaway` | Long-form educational content, drafts where the reader is left without a clear next action |

**If the user specifies one or more lenses, run those.** If the user specifies "all," run every lens that fits the draft (skip lenses that don't apply — e.g., don't run `what-why-how` on pure narrative).

**If the user doesn't specify, self-determine:**
- Default to `copy-edit` if the draft has no obvious specific issue
- Add a second lens if the draft has a clear secondary need: vagueness → add `specificity`, argument-driven → add `developmental`, instructional → add `what-why-how`
- Cap at 2-3 lenses unless the user asked for "all" — running 7 lenses on one draft produces overwhelm

## Run

1. **Read the entire draft first.** Don't start writing suggestions on paragraph 1 before reading paragraph 12. Argument flow, voice, and structure are visible only across the whole piece. (See `../references/editing-principles.md` — "Read the whole piece before editing any of it.")

2. **Make a mental note of the writer's voice.** Sentence rhythm, register, vocabulary, syntactic quirks, idiosyncratic punctuation. This calibrates suggested rewrites — they should sound like the writer wrote them. (See `../references/editing-principles.md` — "Mirror the author's language.")

3. **Apply each selected lens to the whole draft.** For each lens, look for the issues it's designed to catch. Reference `../references/edit-lenses.md` for the lens's specific checks, common-failure patterns, and fix-pattern examples.

4. **For passages where multiple lenses fire**, perform editing synthesis — combine the suggestions into a single unified entry rather than listing the same passage multiple times. State which lens-suggestions are being combined.

5. **Write the suggestion list** in the format specified in `../templates/suggestion-list.md`:
   - Numbered sequentially (`### 1 -`, `### 2 -`, ...)
   - Each entry has `__Location__:`, `__Issue__:`, `__Suggestion__:` lines with mandatory **bolding** in the Issue section
   - No intro, no conclusion, no preamble

6. **Don't include passages with no issue.** The suggestion list is actionable items only. (See `../references/editing-principles.md` — "Don't return passages unchanged.")

7. **If the draft has no issues at the selected lens(es)**, say so explicitly with one sentence ("No issues to flag — this draft scans clean against the [lens] checks."). Don't invent issues to fill space.

## Output

Per `../templates/suggestion-list.md`. The output begins with `### 1 - {title}` and ends with the last numbered entry. No surrounding prose.

If multiple lenses were run, briefly note at the very top *which* lenses produced which entries — e.g., `(redundancy) ### 1 -` or `(combining copy-edit + specificity) ### 4 -`. This helps the writer see which kinds of issues dominated, which informs the next pass.

## Output discipline

- **Voice match suggested rewrites.** A suggestion that doesn't sound like the writer is worse than no suggestion.
- **No praise.** Skip "this paragraph is great" entries — the mode produces edits, not encouragement.
- **No preamble.** Begin with `### 1 -`. The numbered list is the report, not a wrapper around one.
- **Postamble allowed only as a one-line cross-mode pointer** (see "Cross-mode suggestions" below). The pointer is a single italicized line after the last entry, not a paragraph. Skip it entirely if no adjacent mode is obviously the next step.
- **Synthesize when multiple lenses fire on the same passage.** Don't list duplicates. Use the synthesis label format `### N - {title} (combining {lens-1} + {lens-2})` — name the lenses, not the entry numbers.
- **Sequential numbering across all entries** even when lenses are mixed. With single-lens runs, no per-entry lens prefix is needed. With multi-lens runs, optionally prefix `(lens-name)` before the `### N -` so the writer can see which lens produced which entry.

## Cross-mode suggestions (postamble)

After the suggestion list, optionally point at one adjacent mode the writer is most likely to want next, in one short line that fits the actual output. The typical next steps: after a copy-edit pass, a scored diagnostic or a tone read; after a specificity or developmental pass, a direct rewrite to apply the suggestions; after a redundancy pass, a compression pass via `shorten` if length is the deeper issue. Pick the suggestion that fits — don't recite all candidates, and skip the postamble entirely when no adjacent mode is the obvious next step.

## Design rationale

- **Lens architecture rather than monolithic editor** because different drafts need different lenses. Running all 7 lenses on a tight draft produces noise. Running one lens on a sprawling draft misses structural issues. The lens catalog separates concerns so the user (or the mode) calibrates per draft.
- **Output format preserved verbatim from CE 101 sources** because the bolded labels and numbered list format scan well for writers iterating across many suggestions. Changing the format would lose a craft move that's settled across 8 source prompts.
- **"Don't return passages unchanged"** as output discipline because suggestion-list reports are actionable items only. A wall of "looks fine" entries hides the real issues.
- **Synthesis when multiple lenses fire on the same passage** because listing the same passage multiple times under different lens-tags fragments the author's attention. Synthesis preserves the multi-lens insight without duplication.
- **Cap of 2-3 lenses unless user asks for "all"** because more lenses produce overwhelm. The writer can iterate — run two lenses, act on the suggestions, run two more if needed.

