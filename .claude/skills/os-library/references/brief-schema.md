# Brief Schema

Briefs are project-level context for ongoing work — the audience, the goal, the constraints, the source material, the references chosen. They live in `os-inputs/briefs/` split across `current/` (active projects) and `archive/` (finished projects, kept for context and learning).

A brief is the user's working notes for a specific output project. Writing modes load the active brief at the start of a run so the producer knows what's being made and why. After the project ships, the brief moves to archive — useful later when the user wants to understand what worked or build similar pieces from a known-good context.

## Frontmatter schema

```yaml
---
type: brief
project: <name>
target: <output-format being produced>
status: active | done | archived
notes: <freeform>
---
```

Required: `type`, `project`. Strongly recommended: `target`, `status`. Optional: `notes`, plus user-added fields as needed (see below).

## Field guidance

**`type`** is always `brief` for files in this directory.

**`project`** is a short name for the project. Use lowercase with hyphens (e.g., a campaign-name-plus-year, a book-title-and-volume, a newsletter-arc-and-quarter). Project names should be specific enough to disambiguate when the user has multiple projects of the same type in flight at once.

**`target`** is the format being produced. Single-target briefs use a single value: `landing-page`, `email-sequence`, `vsl`, `book-chapter`. Multi-target briefs (a campaign producing landing page plus email sequence plus VSL) can use a list value or describe the targets in `notes` — pick whichever feels natural for the project.

**`status`** is `active` while the project is in progress, `done` after launch, `archived` after the user no longer needs ready access. The split between `briefs/current/` and `briefs/archive/` reflects this: `active` and `done` typically live in current (with `done` being recent finished work), `archived` lives in archive. Movement between directories is manual — `os-library/save` doesn't auto-relocate based on status changes.

**`notes`** is freeform. Common uses: top-level summary of the project goal, audience profile for this specific project, constraints (deadline, word count, hard rules from the client), references chosen for this project (which voiceprint, which templates, which style samples), what's been produced so far, what's left, what's been learned in iteration.

A brief can carry user-added fields beyond the required ones. A campaign brief might add commerce-shaped fields (revenue target, cohort, co-author). A fiction brief might add structural fields (POV, chapter, act). Library does not enforce a closed set — the brief is the user's working notes, and the schema is a starting structure.

## The brief body

The body of a brief is the user's working notes for the project, organized however the user prefers. Common sections include:

The audience — who's being addressed, what they already know, what they don't, what they want to do as a result of the piece. A short paragraph or a few bullet points (genuinely list-shaped enumeration is fine here).

The goal — what the piece needs to accomplish, the metric of success if there is one, the action the reader should take.

The references — which voiceprint, which templates, which style samples are loaded for this project. Listing them explicitly in the brief means writing modes don't have to re-discover them per run.

The constraints — deadlines, word counts, hard rules (things to avoid mentioning, things that must be included, forbidden phrasings).

The source material — links to research, transcripts, prior wins, customer quotes, anything the producer should reference. Inline or linked.

The work log — what's been produced, what's been revised, what's left. Updated as the project progresses.

## Worked example

A filename under `current/<project>.md` for an active email-sequence brief might carry frontmatter and body shaped like this:

```yaml
---
type: brief
project: <project-slug>
target: email-sequence
status: active
notes: "<one-paragraph summary: what the project is, scope and shape, key dates>"
---

# <Project Name> — brief

## Audience
Who's being addressed (role, situation, pain), what they already know, what they want as a result of the piece. Specific enough that the producer can write to a real reader rather than a generic one.

## Goal
What this project needs to accomplish, the metric of success if there is one, the action the reader should take.

## References loaded
- Voiceprint: <which voiceprint(s) by author/scope, and which pieces use which>
- Templates: <which structural templates, or note that one will be extracted post-launch>
- Style samples: <which patterns and authors, with what they're loaded for>

## Constraints
- Hard deadlines and counts (number of pieces, sent on dates, word ceiling)
- Voice shift notes when more than one signer or POV is in play
- Required framings or recurring lines across the project
- Things to avoid mentioning (related campaigns, internal-only context)

## Work log
- <Piece identifier> — status (drafted, scheduled, sent), notes
- [...]
```

## When briefs get loaded

Writing modes load the active brief when the user names the project ("draft email 5 of the prove-it-black-friday sequence") or when the brief is in `briefs/current/` and is the only active brief matching the requested `target` format. A user with multiple active briefs of the same target should name the project explicitly.

The matching for briefs is usually exact (project name) — fuzzy matching on briefs would be risky given that briefs hold project-specific context the wrong project shouldn't poison. If find returns multiple `status: active` briefs and the user hasn't named one, the calling skill asks which to use rather than silently picking.

## Moving briefs to archive

When a project ships and the user no longer needs the brief in active rotation, move the file from `briefs/current/` to `briefs/archive/` and update `status:` to `archived`. This is a manual move — library does not auto-relocate. The current/archive split matters because the user can have many archived briefs (campaigns accumulate), and find should not have to scan all of them when the user is working on something current.

Archived briefs are useful for two things: building new briefs from the shape of a successful one, and looking up "what did we say in the X campaign" when the question comes up later. A `os-library/find` against archive briefs requires explicitly asking ("look in archive for any briefs matching Y") to avoid surfacing old context where it doesn't apply.

## Repairing brief frontmatter

If a brief has missing frontmatter, `os-library/repair` reads the body and infers what it can. The project name is usually in the title or filename. The target is usually in the body's "what we're producing" section. Status defaults to `active` if not specified — repair flags the assumption and lets the user adjust. Notes are the hardest to infer. Repair will often leave them blank rather than fabricate.

## What briefs are not

A brief is not a draft. The brief is the working notes that inform the draft. The draft is produced separately by writing modes loading the brief as context.

A brief is not a template. A template is the structural shape of a format. A brief is the project-specific context for one particular project. A landing-page template can be loaded by many briefs targeting landing pages.

A brief is not a checklist. The work log section is closer to a journal than a task list — what's been done, what's been learned. Granular task tracking belongs in whatever the user uses for project management, not in the brief.
