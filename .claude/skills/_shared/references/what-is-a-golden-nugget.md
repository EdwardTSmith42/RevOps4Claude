# What Is a Golden Nugget

The canonical definition, quality criteria, and failure modes for the kind of high-value insight Personal OS skills extract from source content. Loaded by the os-gold skill (all three modes) and the os-content-mining skill (Step 2 quality filter); promoted to `_shared/` during the os-* batch audit when the two-skill threshold was met.

## Definition

A **golden nugget** is a high-value insight, memorable statement, or thought-provoking concept — large or subtle — that is worth pondering, sharing, or saving.

Golden nuggets are not summaries. They are stand-alone intellectual gems.

A nugget can be:
- A verbatim quote from the source whose phrasing carries the insight
- A near-verbatim quote, lightly sharpened for stand-alone use
- An implicit idea inferred from examples, stories, or structure — made explicit by the extractor

## Quality criteria

Each retained nugget should meet at least several of these:

- **Stand-alone.** A reader unfamiliar with the source can understand and be moved by it without context.
- **Sticky.** A reader would highlight it, write it on a sticky note, or quote it to someone else.
- **Evokes "aha" or resonance.** Triggers emotion, reframes thinking, or captures a framework worth remembering.
- **Human value.** Carries value along at least one of: emotional, intellectual, financial, spiritual, practical.
- **Not a summary.** A summary paraphrases the whole. A nugget isolates something discrete.
- **Distinct.** Not a variation or restatement of another nugget in the list.

## Failure modes to avoid

- **Context-dependent statements.** A line that only makes sense if you've read the source is not a nugget. Drop it or derive the stand-alone version.
- **Editorializing or critique.** The extractor's job is to surface, not to comment. Observations go to the user. Opinions don't.
- **Duplication.** If two candidates express the same core idea, keep the sharper one.
- **Over-filtering.** The opposite of over-filtering is under-extracting. Don't skimp on good material out of a false sense of restraint — quantity AND precision both matter.

## The stand-alone test

For each candidate, ask: *If a reader saw this nugget alone — no source, no context, no setup — would it still do useful work?*

- "The three-step process for onboarding" → **fails** (requires knowing what three steps, what onboarding)
- "Most onboarding fails because the user never sees the win before the effort" → **passes** (stands alone, reframes, actionable)

## Types of nuggets

Useful categories (not an exhaustive taxonomy — just enough to help the extractor recognize what they're seeing):

- **Reframes** — "It's not X, it's Y" insights that invert a default
- **Principles** — compact rules that apply beyond the original context
- **Definitions** — crisp articulations that replace fuzzy concepts
- **Observations** — patterns the author names that the reader hadn't noticed
- **Heuristics** — rules of thumb with specified conditions
- **Metaphors** — comparisons that make an abstract concept graspable
- **Contrarian claims** — positions that run against the default and earn their contrarianism
- **"Missed gold"** — insights the source makes implicitly via example or contrast, never stated directly

## Criteria from adjacent frameworks

Creative criteria that overlap heavily with nugget-ness (see `../../_shared/references/creative-criteria.md`):
- Counter-intuitive
- Awe-inspiring
- Elegantly simple
- Relatable
- Actionable

A nugget that also hits one or more of these tends to travel farther.

## Used by

- `os-gold/modes/straightforward.md` — direct quality bar
- `os-gold/modes/deep-exploration.md` — applied in the final "Golden Nugget Extraction" section
- `os-gold/modes/video-transcript.md` — layered with T.A.K.I. signal detection
- `os-content-mining/SKILL.md` — Step 2 quality filter when extracting nuggets as part of the content ecosystem map

## Malleability note

Canonical: the four-test quality bar (stand-alone, specific, transferable, non-obvious) and the failure modes that disqualify a candidate nugget. These name the defining concepts; consumers that diverge from them are no longer extracting nuggets in the same sense.

Adaptable: how the four tests are applied per source format and per output destination. os-gold's `deep-exploration` weights non-obvious heavily because the mode's job is surfacing what the source didn't state; os-content-mining's Step 2 weights transferable heavily because the downstream work is repurposing the nugget into other content surfaces. Both are correct calibrations of the same underlying quality bar.

