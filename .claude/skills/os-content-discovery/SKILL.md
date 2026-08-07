---
name: os-content-discovery
version: 0.1.0
description: >-
  Find content topics and ideas worth writing about. Two workflows: the EIB
  chain (`extract` audience+driver from existing content → `topics` from an
  audience statement → `subtopics` from a topic → `drivers` for FFGAs of a
  subtopic), and `explore` (kernel idea → multi-section thinking essay for
  testing or developing). Produces portable content artifacts consumed by
  drafting and editing. Triggers on "what should I write about," "give me
  topic ideas for my audience," "extract the audience for this post," "expand
  this topic into subtopics," "give me FFGAs for this subtopic," "unpack this
  idea," "what's interesting about this thought." Do NOT trigger for the
  conversational interview workflow (use `os-content-interview`), drafting prose
  (use `os-writing`), audience profiling (use `os-audience`), or template
  extraction (use `os-content-template`).
display_name: Content Discovery
tagline: Find what's worth writing about — EIB (Extract → Ideate → Brief) chain or kernel-idea exploration.
category: Writing
packs:
  - creator-pack
icon: 'phosphor:MagnifyingGlass'
when_to_use: >-
  Reach for this when the question is *what should I write about* and you have
  structured input — an audience statement, a topic, a subtopic, or a piece of
  existing content to reverse-engineer from. Two workflows:

  - The **EIB (Extract → Ideate → Brief) chain**: `extract` audience+driver from existing content →
  `topics` from an audience statement → `subtopics` from a topic → `drivers` for
  FFGAs of a subtopic. End-to-end content discovery from any starting point.

  - `explore` — kernel idea → multi-section thinking essay for testing or
  developing.

  Produces portable artifacts consumed by drafting and editing.
modes:
  - name: extract
    job: Pull audience + driver from existing content.
  - name: topics
    job: Generate topic ideas from an audience statement.
  - name: subtopics
    job: Expand a topic into subtopics.
  - name: drivers
    job: >-
      Generate FFGAs (frustrations / fears / goals / aspirations) for a
      subtopic.
  - name: explore
    job: Kernel idea → multi-section thinking essay.
---

# Content Discovery — find what to write about

## Purpose

Content discovery is the upstream step before drafting. The **EIB (Extract → Ideate → Brief) chain** (Engaging Internet Brain) is a structured reverse-engineering ladder that produces topics, subtopics, and emotional drivers from an audience statement. **Explore** develops a kernel idea into a multi-section thinking essay. Both answer *what should I write about?* with structured input.

For the conversational sibling — the interview-shaped flow where the user wants to be asked questions and talk through their ideas — use the standalone `os-content-interview` skill. That's a different scale of thing (persona-led, charisma-first, podcast-mined follow-up patterns) and lives in its own surface.

This skill operates upstream of `os-writing`. The typical chain runs: identify the audience and emotional driver (`extract` here, or `os-audience` for a deeper profile) → expand into topics and subtopics (EIB (Extract → Ideate → Brief) chain) → write a brief covering one subtopic (`os-library/save`) → draft prose (`os-writing`).

## When to use

Direct triggers are any time the user asks what to write about, asks for topic ideas, asks to expand a topic, asks what an audience is feeling, asks who a post is for, asks for FFGAs on a subtopic, or asks to unpack an idea.

Indirect triggers include any moment the user has an audience but no concrete subjects to draft about, or existing content but no formal sense of who it speaks to.

If the user wants a conversational interview to surface content ideas, route to `os-content-interview`. If the user already has a topic and just wants to draft, route to `os-writing` directly. If the user wants a deep audience profile (psychographics, jobs-to-be-done, objections), route to `os-audience`. Content discovery operates at the lighter, more generative end — fast topic ideation, not deep profiling.

## Modes (v0.1)

| Mode | Job | Output shape |
|---|---|---|
| `extract` | Reverse-engineer AUDIENCE / SUBJECT / EMOTIONAL DRIVER from a piece of existing content | Three-line structured output |
| `topics` | Generate 5 pillar topics from an audience statement | Numbered list of topic titles |
| `subtopics` | Expand a topic into 5 specific subtopic angles for a given audience | Numbered list of subtopic descriptions |
| `drivers` | Produce 8 FFGAs (2 fears, 2 frustrations, 2 goals, 2 aspirations) for a subtopic and audience | List of 8 first-person emotional statements |
| `explore` | Develop a kernel idea into a rich multi-section thinking essay surfacing why the idea is interesting, what problem it solves, the deeper philosophy, objections, and ripple effects | Substantive exploratory essay (typically 600-2000 words) for use as a thinking artifact |

Extracting voice and post-structure from a sample piece (the legacy EIB Step 4) is satisfied today by chaining to `os-voiceprint/from-sample` (for the voice layer) and `os-content-template` (for the structural pattern). Run both when the user wants both layers to reuse on future work.

### Self-determining when not specified

If the user names a mode, run it. Otherwise infer from what the user has and what they're asking for:

- A piece of existing content plus a question about who it speaks to or why it works → `extract`.
- An audience statement, or any "who" definition, plus a request for what to write about → `topics`.
- A pillar topic plus an audience, looking for specific angles → `subtopics`.
- A specific subtopic plus an audience, looking for what the audience actually feels → `drivers`.
- A kernel idea (a sentence, a tweet, a bullet list, a half-formed thought) the user wants to think with rather than draft from → `explore`.
- A request for the conversational, one-question-at-a-time content-finding flow → route out to `os-content-interview` (separate skill).

When the user supplies multiple inputs that imply chained EIB work — say, an audience and a topic, with an ask for subtopics plus FFGAs — run the chain in sequence: `subtopics` first, then `drivers` on each, surface the full ladder at the end.

## The EIB (Extract → Ideate → Brief) chain

The four EIB modes (extract, topics, subtopics, drivers) compose into a chained ladder that can be run end-to-end or at any single step:

```
[existing content] → extract → AUDIENCE / SUBJECT / DRIVER
                                       ↓
                                       AUDIENCE → topics → 5 PILLAR TOPICS
                                                              ↓
                                                              one TOPIC + AUDIENCE → subtopics → 5 SUBTOPICS
                                                                                                       ↓
                                                                                                       one SUBTOPIC + AUDIENCE → drivers → 8 FFGAs
```

Each step takes the previous step's output as input. The user can enter the chain at any rung — start from existing content (`extract`), an audience statement (`topics`), a topic (`subtopics`), or a subtopic (`drivers`). The chain stops when the user has what they need.

The chain is documented in detail at `references/eib-chain.md`. Modes reference each other (e.g., `topics` notes that subtopic expansion is the next step) but never call each other directly — the user invokes each mode in sequence.

## Content-strategy stance

Across all EIB modes, output favors actionable, engaging, scroll-stopping topics over comprehensive coverage. The bias toward business-relevant subjects (productivity, mindset, frameworks, money-making, competitive edge) and away from ethics / sustainability / inclusiveness / data-driven decision-making is documented in `references/content-strategy-stance.md`.

This is a content-strategy bias, not a values judgment. The skill's job is to surface topics that work for online business audiences — content people will actually read and share. When users explicitly want ethics or sustainability content (some audiences do), the modes adjust. The default skews commercial.

## Integration with other skills

Content discovery composes with several adjacent skills:

- **`os-content-interview`** is the conversational sibling. Where this skill takes structured input (audience, topic, content), `os-content-interview` pulls content ideas out through podcast-host-style dialogue. Different surface, same upstream goal.
- **`os-audience`** is the deeper sibling. Where `extract` produces a one-line audience statement from one piece of content, `os-audience` builds full psychographic profiles, jobs-to-be-done analyses, and objection maps. Use `extract` when you want fast input to the EIB (Extract → Ideate → Brief) chain, `os-audience` when you need a profile to inform offer design or campaign strategy.
- **`os-writing`** consumes content-discovery output. After running the EIB (Extract → Ideate → Brief) chain to identify a subtopic + audience + emotional driver, draft prose against that brief.
- **`os-voiceprint/from-sample`** + **`os-content-template`** together satisfy the legacy EIB Step 4 (voice + structural pattern from a sample piece). Run them on a sample if you want both layers to reuse.
- **`os-offer`** consumes audience and emotional-driver work. EIB output feeds offer messaging.

## First-time setup

Content discovery works cold — none of the modes require setup before they run. They get sharper when the upstream library has the right inputs in it:

- A populated user profile at `os-inputs/_os-user-profile.md` lets the modes default to the user's own audience and domain when the user asks for *topics for me* without naming an audience. Set up via `os-capture`.
- A `os-audience` profile of the user's primary audience (or a key client's) gives the EIB (Extract → Ideate → Brief) chain richer context than a one-line audience statement does. Saved profiles live under the library.
- Briefs saved via `os-library/save` after an EIB run let drafting work load the audience + subtopic + FFGAs without re-running the chain.

None of these are blockers. The skill graceful-degrades when they're absent.

## Library integration

EIB modes don't load library references by default — they're upstream of voiceprint and brief work. The user profile at `os-inputs/_os-user-profile.md` is referenced when the user asks for topics framed at *their* audience without naming one explicitly; the mode loads the profile to understand the user's domain and audience focus before generating.

If EIB output should persist as a brief (because the user wants to draft from this subtopic later), the mode suggests `os-library/save` to write a brief covering the subtopic + audience + emotional driver. Saving is opt-in.

## Operating principles

The skill follows three principles consistent with the rest of the skill pack.

**Output mirrors output format.** EIB modes produce structured output (audience statements, lists, FFGAs) — the modes themselves are written with restraint, not in heavy prose.

**Bias toward specific over generic.** Topics, subtopics, and FFGAs all benefit from specificity. The modes prefer concrete pain-points over abstract themes, named feelings over generalized states. Surface-level patterns produce surface-level content.

## Cross-mode suggestions

After running a mode, useful follow-ups depend on what the user has and where they want to go:

- After `extract`: run `topics` for the surfaced audience, or `os-audience` for a deeper profile.
- After `topics`: pick a topic and run `subtopics` on it.
- After `subtopics`: pick a subtopic and run `drivers` for its FFGAs.
- After `drivers`: write a brief covering the subtopic + driver, save to library, then draft.
- After `explore`: route to `os-writing` to turn the developed idea into finished prose, or to `os-content-mining` (`format-remix`) to reshape into multiple format variants.
- For conversational content surfacing rather than EIB structure, route to the standalone `os-content-interview` skill.

## Related skills

- `os-content-interview` — conversational sibling for the interview-shaped content-finding flow
- `os-audience` — deeper audience profiling for offer and campaign work
- `os-writing` — produces prose from EIB output (briefs, voiceprints, source material)
- `os-voiceprint` — captures voice from sample work
- `os-content-template` — extracts reusable templates from finished pieces
- `os-offer` — uses audience and emotional-driver work for offer messaging


## References

- `references/audience-statement-format.md` — the shape of an audience statement (the artifact `extract` produces and `topics` consumes).
