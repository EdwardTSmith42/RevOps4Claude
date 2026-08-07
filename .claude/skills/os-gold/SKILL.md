---
name: os-gold
version: 0.1.1
description: >-
  Extract the highest-value, memorable, stand-alone insights ("golden nuggets")
  from a body of source content — an article, essay, transcript, podcast, book
  chapter, or conversation. Nuggets are sticky, quotable, stand-alone ideas a
  reader could highlight, tweet, write on a sticky note, or return to. Triggers
  when the user pastes content and asks to "find the gold," "pull out the best
  insights," "extract what's interesting," "give me the golden nuggets," "mine
  this for ideas," or "what's worth saving from this?" Three modes —
  `straightforward` (clean quotable list), `deep-exploration` (three-engine
  analytical dive), and `video-transcript` (T.A.K.I. method for video). Do NOT
  trigger for summarization — this skill intentionally rejects summary in favor
  of discrete, stand-alone insights.
display_name: Golden Nuggets
tagline: 'Extract memorable, stand-alone insights — never summaries.'
category: Research
packs:
  - creator-pack
icon: 'phosphor:Sparkle'
when_to_use: >-
  Reach for this when you want sticky, quotable, *stand-alone* ideas from a
  piece of content — things a reader could highlight, tweet, write on a sticky
  note, or come back to. The skill intentionally rejects summary.


  Use `straightforward` for a clean quotable list, `deep-exploration` for a
  three-engine analytical dive, or `video-transcript` for the T.A.K.I. method on
  video content.
modes:
  - name: straightforward
    job: Clean quotable list of golden nuggets.
  - name: deep-exploration
    job: Three-engine analytical dive into the source.
  - name: video-transcript
    job: T.A.K.I. method extraction tuned to video transcripts.
---

# Gold — extract the highest-value insights from any source

## Purpose

Extract the ideas from a source that would survive the source. A golden nugget is a high-value insight — explicit or implicit — that stands on its own without needing the original context, and that a reader could realistically save, share, return to, or use to reframe their thinking. The skill prefers *resonance* over *comprehensiveness*: missing a weak insight is fine. Missing the line that changes how someone thinks about the topic is not.

Three modes cover the range of depth users actually want:
- **`straightforward`** — clean quotable list of nuggets with light expansion. Default for most uses.
- **`deep-exploration`** — three-engine analytical dive (recursive questions, analytical skeleton, authorial cognition tracing) followed by a nugget list. For when the source is dense or the user wants thinking-partner work, not just extraction.
- **`video-transcript`** — T.A.K.I. method (Timestamp / Assumptions / Keywords / Incongruence) plus three layers of gold and the S.T.O.R.Y. stickiness filter. For video transcripts where speaker energy, tics, and unplanned moments matter.

## When to use

- The user wants to mine an article, essay, book chapter, podcast, or interview for insights — not summarize it
- Building a personal insight library / swipe file from recent reading
- Preparing quotable material for social posts, newsletters, or reference
- Analyzing a video transcript specifically (use `video-transcript` mode)
- Doing deep exploratory work on a dense source (use `deep-exploration` mode)

Do **not** use for:
- TL;DR summaries (anti-pattern: this skill rejects summary)
- Extracting frameworks from a rich source (use `os-content-mining` — extraction *and* expansion) or generating content ideas from a short one (use `os-content-mining/format-remix`)

## Inputs

- **Required:** The source content as text (or a transcript if using `video-transcript` mode).
- **Optional:** Mode selection. Default: `straightforward`. Override to `deep-exploration` for dense sources, or to `video-transcript` for video.
- **Optional:** Audience / use-case hint (e.g., "for LinkedIn posts" or "for personal notes") — biases selection toward the audience's resonance points.

## Run

Mode-selection routing:

- Default → **`straightforward`** mode. The user pastes content and wants the best ideas out, quickly.
- Source is a video transcript OR the user mentions video, YouTube, podcast, talk → **`video-transcript`** mode.
- The user asks to "explore," "dig deep," "analyze thoroughly," or the source is dense conceptual material → **`deep-exploration`** mode.

Across all modes, the defining quality of a golden nugget is:
- **Stand-alone.** Assume the reader has not seen the source. The nugget must work on its own.
- **Sticky.** A reader would highlight it, quote it, or write it on a sticky note.
- **Not a summary.** A summary paraphrases. A nugget isolates something discrete that carries weight.
- **Implicit OR explicit.** Some nuggets are quoted verbatim. Others are derived from context, examples, or patterns.
- **Deduplicated.** If two candidate nuggets say the same thing in different words, keep the sharper one.

See `../_shared/references/what-is-a-golden-nugget.md` for the full definition, quality criteria, and failure modes.

## Output

Mode-specific. See:
- `modes/straightforward.md`
- `modes/deep-exploration.md`
- `modes/video-transcript.md`

Shared across modes: no preamble. No postamble. The deliverable is the extracted material itself. Emojis and em-dashes avoided (per source style rules).

## Design Rationale

Why this skill is structured the way it is:

- **Three modes, not one** — the three source prompts represent three genuinely different extractive jobs. Straightforward is a fast swipe-file pass. Deep-exploration is analytical partnership. Video-transcript uses signals (energy shifts, incongruence) that only exist in spoken content. Folding them into one mode produces the wrong depth for each use. [inferred from source ensemble]
- **Stand-alone quality test is the load-bearing constraint** — without it, nuggets collapse back into paraphrase. "Would this still work if the reader had never seen the source?" is the question that separates a nugget from a summary. [stated in source]
- **Precision AND quantity** — stated in source: "Precision and selection matter, but so does quantity. Don't skimp out and miss on the best stuff." The anti-stinginess rule calibrates against the common failure mode of over-filtering and missing the gems that *are* there. [stated in source]
- **Implicit nuggets count** — some of the best insights in a source are never stated directly. They're demonstrated through examples, stories, or contrast. Allowing derived nuggets expands the extraction beyond verbatim lines. [stated in source]
- **No summary, ever** — the mode-switching trigger-language explicitly rejects summarization. This matters because models default to summary when asked for "key points." Stating the anti-summary stance up front keeps the skill honest. [stated in source]
- **Deep-exploration uses three insight engines** — Recursive Questions probe the content's logic, Analytical Skeleton exposes its structure, Authorial Cognition reveals the mind that produced it. The engine set is canonical in that reference, not here — its malleability note treats the kind of triangulation as the fixed part and the exact three as adaptable. Orthogonal axes cover depth that any single lens would miss. Reference-grade but malleable (see `references/insight-engines.md`). [elicited 2026-04]
- **T.A.K.I. for video specifically** — video has signals text doesn't (energy shifts, timing, incongruence between tone and claim). The four letters are the four signals that carry extra information in the spoken form. Reference-grade but malleable. [elicited 2026-04]

## References

- `../_shared/references/what-is-a-golden-nugget.md` — definition, quality criteria, failure modes. Shared across modes.
- `references/insight-engines.md` — the insight engines used by `deep-exploration` mode; canonical for which they are and how many.
- `references/story-filter.md` — the S.T.O.R.Y. stickiness framework (Simplify / Tell / Own / Relate / Yield). Used by `video-transcript` mode, may be useful to other writing skills.

## Templates

- `templates/straightforward-nugget-list.md` — strict output shape for `straightforward` mode.

## Modes

- `modes/straightforward.md` — clean quotable list. Default.
- `modes/deep-exploration.md` — three-engine analytical dive followed by nugget list.
- `modes/video-transcript.md` — T.A.K.I. + 3 layers + S.T.O.R.Y. for video content.

## Getting the source text

When the source is a URL rather than pasted text — a video, a podcast page, a blocked article — acquire it per `../_shared/references/web-content-acquisition.md` (fetch → browser → user's session → ask, with the transcript SOP for YouTube). Verify completeness before mining; a teaser page mined confidently produces confident nonsense.

## Where outputs go

Outputs persist per the workspace storage methodology — see `../_shared/references/workspace-layout.md` (Knowledge system invariants): when the work belongs to an ongoing project, save silently to `os-outputs/` with dated frontmatter and a link trail; when the user is exploring, offer once. No skill-specific save scheme.

## Related skills

- `os-content-mining` (`format-remix`) — run *after* to turn nuggets into content ideas across formats. The nuggets are portable intellectual seeds: when the user wants ideas for their own work, hand them over as catalysts for new, self-sufficient concepts rather than assuming the eventual content should discuss the original source. Explicit requests for commentary or attribution keep the source visible. See `../_shared/references/source-to-content-transformation.md`.
- `os-content-mining` — if the user wants extraction *and* a content map in one pass, prefer content-mining over chaining.

**A deliberate overlap, on the record:** `os-content-mining`'s `atomize` mode extracts nuggets and sound bites inline — the same work this skill owns. That duplication is a decision, not drift: Golden Nuggets is a branded idea from the creator's courses and stays its own installable skill, while a mining kit would be incomplete without a nugget section. Mining may hand off to this skill for the deeper passes (`deep-exploration` for dense conceptual sources, `video-transcript` for spoken ones). Neither skill is a candidate for merging into the other. Reciprocal note in `os-content-mining`.

## First-time setup

The skill works on any pasted source out of the box. It gets sharper when a couple of companions are in place:

- An audience profile (via `os-audience`) so nugget selection tilts toward what resonates with your readers, not just what's structurally interesting in the source.
- `os-content-mining` installed for the natural next step after extraction (turn the strongest nuggets into content ideas across formats via `format-remix`).

Neither is a hard requirement — the skill runs without them. Remove or supersede this section once you've decided which companions you actually use.

## When the source asks for something this skill doesn't currently produce

Gold-finding methods accumulate. A new kind of source (a research-paper appendix, a strategy memo, a long Slack thread) or a new kind of extraction lens (regret moments, taboo claims, decision-rule excavations) may not fit cleanly into the three current modes. When that happens:

- **Name the gap.** Say plainly that none of the three modes carry this lens or this source shape, rather than forcing the request into the closest existing mode and producing a wrong-shape output.
- **Offer two paths.** Either: set the new capability up for next time — the user supplies a sample of the source or a sketch of the new lens, and the skill hands off to `os-tune`'s `extend` (for a new mode) or `os-library` (for a new shared reference). Or: run once without setup, using the closest existing mode with the source as substance, no artifact saved.
- **Hand off cleanly when setup is chosen.** This skill surfaces the gap and frames the choice; it doesn't try to be the skill-builder or the library itself.

Lean greedy when the signal points at recurring need (an ongoing publication, a regular source type, a lens the user wants on every run); lean restrained on one-offs. Ask when ambiguous. Full discipline in `../_shared/references/self-extending-skills.md`.
