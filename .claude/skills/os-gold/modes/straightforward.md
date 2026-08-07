# Mode: straightforward

Part of the `gold` skill. The default mode. Selected when the user wants a clean, quotable list of insights from a source — fast, usable, no analytical preamble.

## Job

Produce a list of golden nuggets from the source content. Each nugget stands alone, each is as punchy as the source allows, and the list is deduplicated. No summary, no editorializing, no overthinking — just the gold.

## Run

1. **Read the source slowly.** Scan not just for facts but for resonance: what sparks emotion, reveals perspective, or reframes thinking?
2. **Mark candidates.** Highlight every line, phrase, or section that contains a self-contained idea, insight, or framing.
3. **Refine each candidate.** Sharpen for clarity, punch, and stand-alone value. Rewrite if needed. Be open to quoting verbatim when the author's original words already capture the idea best.
4. **Derive implicit insights.** For ideas the source demonstrates or implies but never states directly, make the unstated wisdom explicit. These often become the most valuable nuggets.
5. **Organize.** Thematic subheadings if they help, otherwise a flat list. Err toward listing rather than over-structuring.
6. **Apply the stand-alone test** to every nugget before output. If it doesn't work without the source, either rewrite or drop it. See `../../_shared/references/what-is-a-golden-nugget.md`.

## Output

Strict shape. See `templates/straightforward-nugget-list.md`.

- Brief title at top
- Optional thematic subheadings if the nuggets cluster naturally
- Each nugget: **bold single-line articulation** followed by **2–5 bullet points** explaining / exploring / expanding
- No intro, no outro — just the list

## Design Rationale

- **Precision *and* quantity** — stated in source: "Don't skimp out and miss on the best stuff. Capture it all." The common failure is over-filtering. The rule corrects toward inclusion. [stated in source]
- **Stand-alone test is non-negotiable** — without it, nuggets collapse back into source-dependent paraphrase. [stated in source]
- **Rewriting OK when it sharpens** — not required, but allowed. The goal is quotability, not fidelity to exact source words. When the author's phrasing already hits, preserve it. [stated in source]
- **Implicit nuggets count** — some of the best insights in any source are never stated directly. Allowing derived nuggets expands extraction beyond "what was written." [stated in source]
- **Bold line + 2–5 bullets** — the bold line is the shareable insight (screenshot-able, tweetable). The bullets are the expansion that helps the reader remember why it mattered. Two artifacts at different densities serving different moments of use. [inferred from source output spec]

