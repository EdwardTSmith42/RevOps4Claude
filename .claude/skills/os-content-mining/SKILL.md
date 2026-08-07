---
name: os-content-mining
version: 0.2.1
description: >-
  Turn one source — post, article, transcript, podcast, interview, workshop,
  insight, or notes — into derived content at the depth the moment calls for.
  Four modes form a depth ladder. `format-remix`: six novel ideas across
  delivery formats, never summaries — "repurpose this," "spin this into posts,"
  "turn this into a week of content." `multi-layer-extract`: surface / truth /
  bias / consequence / narrative analysis with ideas per layer — "go deep on
  this," "break this down." `atomize`: the full content-ecosystem kit — nuggets,
  questions, frameworks, sound bites, angles, expansion paths — "mine this talk
  for everything," "turn this into a content system," "one source, many pieces."
  `sop`: extract standalone step-by-step documents — "extract the SOP," "turn
  this into a procedure I can follow." Do NOT trigger for stand-alone nugget
  extraction (use `os-gold`), finished copy (use `os-writing`), or summarization
  — this skill rejects summary at every depth.
display_name: Content Mining
tagline: 'One source in — quick ideas, deep angles, a full content kit, or SOPs out.'
category: Research
packs:
  - creator-pack
icon: 'phosphor:Atom'
when_to_use: >-
  Reach for this whenever you have a source — anything from a one-liner insight
  to a two-hour transcript — and want content *derived from* it. Pick the rung
  that matches the moment: `format-remix` for six fast post ideas,
  `multi-layer-extract` for layered analysis of a dense piece, `atomize` for
  the full content-ecosystem kit, `sop` for the how-to as a runnable document.
modes:
  - name: format-remix
    job: >-
      Quick ideation — six novel content ideas, one per delivery format, from
      any source.
  - name: multi-layer-extract
    job: >-
      Five-layer analytical extraction with content ideas per layer, for dense
      sources.
  - name: atomize
    job: End-to-end content-ecosystem map from a single rich source.
  - name: sop
    job: >-
      Extract the working procedures from a source as standalone,
      self-contained SOP documents saved to os-knowledge/.
---

# Content Mining

## Purpose

Turn a source — as small as a one-liner insight, as large as a workshop transcript — into derived content, at whatever depth the moment calls for. Sometimes that's six quick post ideas. Sometimes it's a layered analytical extraction. Sometimes it's the full content ecosystem: golden nuggets worth saving, questions the source answers (directly and indirectly), named frameworks, quotable sound bites, clustered content angles, and expansion paths showing how each primitive could ladder across formats. And sometimes what you want out of a source isn't content at all — it's the *procedure*, kept as a runnable document.

One skill covers all four because the job is the same at every depth — derive, never summarize, and stay grounded in what the source actually says — and only the investment differs.

The bias of the skill: *strategist first, editor second, creator last.* Clarity and leverage beat volume and creativity.

## The depth ladder — how much do you want out of the source?

One source can yield several different things, and the right rung depends on which one you're after. The full picture, including the neighbors:

| You want... | Use |
| --- | --- |
| The best stand-alone insights — quotable, save-worthy ideas | `os-gold` |
| A fast set of post ideas — six novel angles, one per format | this skill, `format-remix` |
| Layered analysis of a dense source, with ideas per layer | this skill, `multi-layer-extract` |
| A full content kit — nuggets, questions, angles, expansion paths | this skill, `atomize` |
| The how-to — a procedure you can follow, as a standalone document | this skill, `sop` |
| A working AI skill built from the material | `os-skillify` (`from-content`, or `from-prompt` when starting from an SOP) |

Routing when the user doesn't name a mode: "repurpose this" / "give me ideas from this" → `format-remix`. "Go deep" / "break this down" on a dense source → `multi-layer-extract`. "Mine this for everything" / "turn this into a content system" → `atomize`. "Pull the how-to out" → `sop`. When the ask is ambiguous between a quick pass and a full run, ask — the depth rungs cost very different amounts of the user's attention, and picking the wrong one wastes either the source or the user's time.

These chain naturally: remix a source today, come back and atomize it when it proves out, keep an SOP from it, and later hand that SOP to `os-skillify` when the procedure earns automation.

**A deliberate overlap, on the record:** `atomize` extracts golden nuggets and sound bites inline — work that `os-gold` also owns as a standalone skill. This is by design, not drift. Golden Nuggets is a branded idea from the creator's courses, and people who learned it there rightly expect it as its own skill; meanwhile a mining kit would be incomplete without a nugget section. So both exist, `atomize` may hand off to gold for the deeper passes (see the run notes below), and neither is a candidate for merging into the other. Reciprocal note in `os-gold`.

## When to use

- User has a post, transcript, article, insight, or notes and wants new angles or post ideas derived from it (`format-remix`)
- A good tweet or short insight the user wants expanded into multiple format variants (`format-remix`)
- A dense source the user wants analyzed layer by layer, with ideas surfaced from each layer (`multi-layer-extract`)
- User has a single rich source (podcast episode, keynote, interview, long essay, workshop) and wants a full content atomization kit (`atomize`)
- Weekly or monthly content production from one flagship input
- Building a compounding content system from existing expertise (previous interviews, past talks, archived essays)
- The source teaches a repeatable procedure the user wants captured as a runnable document (`sop`)

Do **not** use for:
- Stand-alone insights list without idea expansion — use `os-gold`
- Drafting finished copy from an idea — use `os-writing`; every rung here produces concepts and kits, not final prose
- Summarization — this skill explicitly rejects summary at every depth

## Inputs

- **Required:** The source. Any length — the quick rungs work on a one-liner; `atomize` earns its keep on rich inputs.
- **Optional:** Mode. Inferred from the ask when unnamed (see the routing rule above).
- **Optional:** Audience context (industry, role, platform) — biases angle generation toward resonance points.
- **Optional:** The source's relationship to the writer and its intended role in the new work. Distinguish the writer's own material from an external source, then infer whether the source is the subject, supporting evidence, or a catalyst for new thinking. See `../_shared/references/source-to-content-transformation.md`.
- **Optional:** Depth preference — within `atomize`, the user may request a lighter pass (steps 1–6 only, extraction without expansion).

## First-time setup

The skill works on any rich source you hand it. It gets sharper when a few things are in place:

- A voiceprint (via `os-voiceprint`) so suggested angles and sound-bite phrasings lean toward how you actually sound — otherwise angle suggestions skew generic.
- An audience profile (via `os-audience`) so cluster generation tilts toward what your readers care about rather than what the source happens to emphasize.
- The companion content skills installed (`os-gold` for stand-alone nugget extraction, `os-content-template` for templatizing winning angles) so hand-offs after mining have somewhere clean to land.

None of these are hard requirements — mining will run without them and degrade gracefully. Remove or supersede this section once you've decided which companions you actually use.

## Run

Each mode has its own run, in its own file:

- `modes/format-remix.md` — the quick rung: six novel ideas, one per delivery format.
- `modes/multi-layer-extract.md` — the analytical rung: layered extraction, with angles and ideas per layer.
- `modes/atomize.md` — the deep rung: the nine-step extraction-and-expansion run producing the six-section content kit.
- `modes/sop.md` — the procedure rung: standalone SOP documents from the source's how-to.

### Craft shared by the idea rungs (`format-remix`, `multi-layer-extract`)

- **Push beyond the obvious.** Challenge assumptions, reveal hidden truths, offer a strikingly fresh take on something people think they already understand.
- **Transform rather than anonymize.** When the source is a catalyst, extract the portable idea and develop it through the writer's worldview, audience, experience, business, tensions, or adjacent beliefs. Deleting the speaker's name while paraphrasing the same point is not new content.
- **Keep traceability without creating reader dependence.** Every idea should have an honest intellectual path back to the source, while a catalyst-based concept should make complete sense to someone who never encountered it.
- **Respect source ownership.** The writer's own notes, interviews, and prior work can supply their language and lived experience. External material can stimulate new thinking without automatically making the eventual concept about the external source. Apply `../_shared/references/source-to-content-transformation.md`.
- **Deduplicate.** If two ideas restate the same underlying insight in different formats, keep the stronger one.
- **Every idea is draft-ready, not a draft.** Sharp enough to spark engagement, directional enough that a writer could draft it in an hour.
- **Write for a busy, skeptical reader bombarded by bland content.** Short, sharp sentences. No jargon. No fluff. No abstract waffle. Casual-professional voice: approachable yet credible. Direct, passionate, persuasive. Storytelling or personal framing OK if it clarifies, but stay focused on reader takeaway. Avoid stating the obvious — surprise the reader or give them something to chew on. Each idea tight but rich with implication: the kind of title that immediately sparks interest or demands a click.
- **No preamble, no outro.** Return only the ideas themselves, each labeled with its format (or, in `multi-layer-extract`, its source layer).

## Design Rationale

Why this skill is structured the way it is:

- **End-to-end (extraction + expansion) in one pass (`atomize`)** — the deep rung exists because users want a full content map, not two separate workflows chained together. Chaining nugget extraction into a separate ideation pass misses the synthesis that happens when extraction and expansion inform each other. The nine-step sequence builds that synthesis. [inferred from source]
- **Nine steps in this specific order** — extraction (1–6) before expansion (7–8) prevents hallucinated angles that don't trace to source. QC last (9) catches generic ideas that slipped through. Inverting the order produces output that looks substantive but isn't grounded. [stated in source spirit, order implicit]
- **"Avoid generic content ideas. Every angle should be grounded in something actually present in the source"** — a hard constraint. Calibration against the model's tendency to produce on-topic but source-unmoored ideas. [stated in source]
- **Strategist first, editor second, creator last** — a priority bias, not a hard routing sequence. The phrase captures the skill's depth-over-volume posture: when choosing between more ideas and better-aimed ideas, aim wins. Don't treat this as a per-decision order of operations. [elicited — clarified 2026-04]
- **Name frameworks descriptively, not creatively** — reusability requires findability. "The Viper Method" dies the moment the reader can't remember what a Viper is. "Objection-Preemption Sequence" survives because it describes itself. [inferred from source]
- **"Implied, demonstrated, or answered indirectly" insights count** — most frameworks in real-world sources are never stated as frameworks. The skill must identify them from pattern across examples. Without this, extraction misses most of the gold. [stated in source]
- **Content primitives as the pivot between extraction and expansion** — Step 6 ("abstract to content primitives") is the hinge that lets a specific insight from the source become a portable asset usable across channels. Without this abstraction, angles stay too story-specific to travel. [stated in source]
- **Angle clusters (education / persuasion / authority / narrative / tactical)** — five clusters cover the main jobs-to-be-done of content. Forcing angles into clusters ensures variety in intent, not just variety in format. Reference-grade but malleable — see `references/angle-cluster-taxonomy.md`. [elicited 2026-04]
- **Follow the source's strengths; never populate to fill.** Mining is strengths-based, the StrengthsFinder logic applied to content: investing in a source's dense areas produces exceptional material, while shoring up its weak areas only ever drags them to average — and fabricates on the way. Empty and sparse sections are legitimate outputs that tell the truth about the source. This replaced an earlier populate-evenly rule that pressured exactly the wrong behavior. [elicited 2026-07-19]
- **One skill, four depths — merged from `os-content-repurposing` 2026-08-01.** The two skills shared the same job-shape (source in, derived content out), loaded the same shared references for the same reasons (format taxonomy, creative criteria), and differed only in how much depth the user wanted. Two names for one depth axis made routing a memory test; one skill with a depth ladder makes it a question the routing table answers. The former repurposing craft is preserved intact in its two mode files. [elicited 2026-08-01, consolidation review]
- **Six content formats, not a free-for-all (`format-remix`)** — forcing one idea per format produces breadth across delivery modes the model wouldn't naturally explore. Without the format constraint, output defaults to the model's favorite shape (usually listicles). Reference-grade but malleable — see `../_shared/references/content-format-taxonomy.md`. [elicited]
- **Creative criteria as a quality filter (idea rungs)** — every idea must embody at least one of counter-intuitive / awe-inspiring / elegantly simple / relatable / actionable. Without this, ideas default to bland. [stated in source]
- **Multi-layer forces one insight per layer, even speculative** — prevents skipping layers when the source "looks shallow." The safeguard catches the case where the model collapses four layers into one because it can't find material in three of them. [stated in source]

## References

- `../_shared/references/content-format-taxonomy.md` — the six delivery formats; used by `format-remix` (one idea per format) and `atomize` (expansion paths)
- `../_shared/references/creative-criteria.md` — quality bar for ideas, nuggets, and sound bites; all rungs
- `../_shared/references/source-to-content-transformation.md` — decides whether a source remains the subject, acts as evidence, or disappears into writer-owned thinking; all idea-generating rungs
- `references/angle-cluster-taxonomy.md` — the five angle clusters (education / persuasion / authority / narrative / tactical); `atomize` only
- `references/multi-layer-analysis-framework.md` — canonical for the analytical layers and their count; `multi-layer-extract` only
- `../_shared/references/what-is-a-golden-nugget.md` — cross-loaded when applying nugget quality criteria in `atomize` Step 2
- `../_shared/references/sop-completeness.md` — the runnable / partial / named-only grades; `sop` mode only

## Modes

- `modes/format-remix.md` — quick ideation: six ideas, one per format
- `modes/multi-layer-extract.md` — five-layer deep extraction with ideas per layer
- `modes/atomize.md` — the nine-step content-kit run
- `modes/sop.md` — extract working procedures as standalone SOP documents

## Templates

- `templates/content-mining-output.md` — canonical six-section output shape (`atomize`)
- `templates/sop-output.md` — the single-file SOP shape (`sop`)

(`format-remix` and `multi-layer-extract` carry their output shapes inline in their mode files — idea lists don't need a separate template.)

## Where outputs go

Outputs persist per the workspace storage methodology — see `../_shared/references/workspace-layout.md` (Knowledge system invariants). `sop` lands its documents in `os-knowledge/` by design; `atomize` kits are usually worth saving the same way. The idea rungs produce lighter artifacts — when the work belongs to an ongoing project, save silently to the broadest existing home with dated frontmatter; when the user is exploring, offer once. No skill-specific save scheme.

## Getting the source text

When the source is a URL rather than pasted text — a video, a podcast page, a blocked article — acquire it per `../_shared/references/web-content-acquisition.md` (fetch → browser → user's session → ask, with the transcript SOP for YouTube). Verify completeness before mining; a teaser page mined confidently produces confident nonsense.

## Related skills

- `os-gold` — when the user wants the stand-alone insights themselves, not ideas derived from them
- `os-content-template` — after content-mining produces strong angles, templatize the winners for reuse
- `os-writing` — drafts finished prose from any idea or angle this skill produces
- `os-skillify` — downstream of `sop` mode: `from-prompt` turns a saved SOP into a working skill when the procedure earns automation

## When the source asks for something this skill doesn't currently produce

Mining methods accumulate. A new kind of source (a Q&A AMA archive, a sales-call recording, a structured research interview) or a new kind of extraction lens (regret moments, before/after pivots, decision-rule excavations) won't always fit cleanly into the current nine-step shape. When that happens:

- **Name the gap.** Say plainly that the current nine steps don't carry this extraction lens or this source shape, rather than forcing the request through the closest existing step and producing a wrong-shape output.
- **Offer two paths.** Either: set the new capability up for next time — the user supplies a sample of the kind of source or a sketch of the new extraction lens, and the skill hands off to `os-tune`'s `extend` (for a new mode) or `os-library` (for a new shared reference or template). Or: run once without setup, using the closest existing steps with the source as substance, no artifact saved.
- **Hand off cleanly when setup is chosen.** This skill doesn't try to be the skill-builder or the library — it surfaces the gap, frames the choice, and hands the examples to the right downstream flow.

Lean greedy when the signal points at recurring need (an ongoing publication, a regular source type, a lens the user wants on every run); lean restrained on one-offs. Ask when the signal is ambiguous. Full discipline in `../_shared/references/self-extending-skills.md`.
