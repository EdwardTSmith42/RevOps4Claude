# EIB Chain — How the modes compose

The four EIB modes (`extract`, `topics`, `subtopics`, `drivers`) form a chained ladder where each step's output feeds the next. The chain is the canonical reverse-engineering workflow for moving from existing content (or a clean audience statement) to a fully-articulated content brief.

## The chain

```
[existing content]
        ↓
     extract  →  AUDIENCE / SUBJECT / EMOTIONAL DRIVER
                              ↓
                              AUDIENCE
                                   ↓
                               topics  →  5 PILLAR TOPICS
                                                ↓
                                             one TOPIC + AUDIENCE
                                                       ↓
                                                  subtopics  →  5 SUBTOPICS
                                                                       ↓
                                                                    one SUBTOPIC + AUDIENCE
                                                                              ↓
                                                                          drivers  →  8 FFGAs
```

The chain runs top-to-bottom but the user can enter at any rung depending on what input they have:

- Starting from existing content (a tweet, post, email): `extract` → `topics` → `subtopics` → `drivers`
- Starting from an audience statement: `topics` → `subtopics` → `drivers`
- Starting from a pillar topic: `subtopics` → `drivers`
- Starting from a subtopic: `drivers` directly

The chain stops when the user has what they need. Some users want pillar topics for a content calendar and stop at `topics`. Some want emotional resonance for a single piece and run only `drivers`.

## Why chain at all

Each step narrows abstraction:

- `extract` outputs an **audience** — a population definition.
- `topics` outputs **pillar topics** — broad themes that audience cares about.
- `subtopics` outputs **specific subjects** — what individual content pieces would address.
- `drivers` outputs **emotional resonance** — how the audience actually feels about that subject.

A draft written against a subtopic alone produces decent content. A draft written against a subtopic *plus* the FFGA layer produces content with emotional resonance. The chain exists because each rung adds usable signal that the next rung depends on.

## Running the chain end-to-end

When a user supplies enough input to run multiple steps at once (e.g., *"here's an audience and a pillar topic, give me subtopics with FFGAs"*), the mode runs the chain in sequence:

1. Run `subtopics` on the topic + audience → 5 subtopics
2. For each subtopic, run `drivers` on the subtopic + audience → 8 FFGAs
3. Surface the full ladder at the end — pillar topic, 5 subtopics, 40 FFGAs (8 × 5)

The user can then pick which subtopic to draft against without having to re-invoke each mode separately.

If the user supplies an audience plus a content sample (no topics yet), the chain runs:

1. `extract` on the sample → confirm or refine the audience
2. `topics` on the audience → 5 pillar topics
3. Surface to user, ask which pillar to expand
4. `subtopics` on the chosen pillar → 5 subtopics
5. Surface to user, ask which subtopic to deepen (or run `drivers` on all 5)
6. `drivers` per subtopic → FFGAs

The mode pauses at each user-decision point rather than auto-running through the entire ladder. Pillar topics in particular are a meaningful choice — running drivers on all 25 subtopics across 5 pillars produces 200 FFGAs, which is rarely useful.

## Persisting EIB output

If the user wants to draft against an EIB result later, the natural persistence path is to write a brief covering the audience + subtopic + FFGAs and save via `os-library/save`. The brief schema is documented at `../../os-library/references/brief-schema.md`.

Briefs persist project-level work — the EIB output is project-relevant for any drafting work in that subtopic for that audience. When the user starts a new project on a different audience or subtopic, the brief reflects the new EIB run, not the old one.

## When the chain breaks

Two failure modes to watch for:

**Audience drift between steps.** If the audience statement supplied to `topics` is broader than the audience that emerged from `extract`, the topics will be vague. Tighten the audience before running `topics` rather than letting drift compound.

**Topic abstraction mismatch.** If a pillar topic is too narrow (already at subtopic granularity), `subtopics` will produce overlapping or strained output. If it's too broad (entire industry rather than a pillar), subtopics will be generic. The mode can flag this and ask the user to adjust the topic before expanding.

