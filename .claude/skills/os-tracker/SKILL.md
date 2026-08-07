---
name: os-tracker
version: 0.1.0
description: >-
  Maintain task backlogs as plain-markdown files with a section schema. Two
  default contexts — `user` for visible backlog, `system` for Personal OS
  work-in-progress; users add more contexts as they earn a split (project,
  client, etc.). Pluggable storage adapters (Bear / Notes / Obsidian) defer to
  v0.2. Other skills
  (Capture, os-tune) write through this skill's contract rather than editing files
  directly. Four modes: view, add, update, setup (connect an external task system
  like ClickUp/Asana and prime learned task routing). Triggers on "show my
  tracker," "what am I working on," "add to tracker," "track this," "mark done,"
  "what's next," "help me use ClickUp," "connect Asana," "where should my tasks go."
display_name: Tracker
tagline: Plain-markdown backlogs that other skills write through.
category: Planning
packs:
  - personal-os
icon: 'phosphor:ListChecks'
when_to_use: >-
  Reach for this any time you want to see, add to, or update a task list.
  Tracker is the contract layer — Capture and os-tune don't touch the files
  directly, they call through Tracker. That keeps your backlogs consistent no
  matter which skill is writing.


  Two contexts ship by default: `user` for your visible backlog, `system` for
  Personal OS system work. Add more (per-project, per-client) when you have
  a real reason to split.
modes:
  - name: view
    job: Show the current state of a tracker context.
  - name: add
    job: Add a task with proper section placement.
  - name: update
    job: 'Mark done, move sections, edit existing tasks.'
  - name: setup
    job: >-
  - name: tidy
    job: Review a context for items that are done, stale, or drifted, and propose what to do about each. Proposes only; never writes unconfirmed.
      Connect an outside task app and prime where tasks get routed — learned over
      time, not configured up front.
---

# Tracker — task backlogs in plain markdown, with structure

## Purpose

Hold the user's actionable backlog and the system's work-in-progress in a small set of files with one consistent shape. Default to simple. Let the user opt into complexity.

The skill owns the section schema, the watermark protocol, and the contract that other skills (Capture, os-tune) write through. Storage is pluggable — markdown at `os-tracker/<context>.md` is the v0.1 default; external adapters (Bear / Apple Notes / Obsidian) defer to v0.2 when there's user demand.

## When to use

- *"Show my tracker"* / *"what am I working on"* → `view`
- *"Add this to my tracker"* / *"track this"* / *"new task: …"* → `add`
- *"Mark X done"* / *"X is finished"* / *"move Y to backlog"* → `update`
- *"Help me use ClickUp"* / *"connect Asana"* / *"where should my tasks go"* → `setup`

If the user is processing inbox items, route to Capture — that skill writes through Tracker. If the user is wrapping a session and capturing learnings, route to os-tune's `close-out`.

## Modes (v0.1)

| Mode | Job | Output |
|---|---|---|
| `view` | Read the current state of one or more contexts | The tracker file content, optionally filtered by section |
| `add` | Add a new item to a context, section, optional area sub-section | Updated tracker file, dry-run shown first |
| `update` | Modify an existing item — mark done, edit text, move section, add wikilink | Updated tracker file, dry-run shown first |
| `setup` | Connect an external task system and prime task routing (learned, not pre-stated) | The routing ledger at `os-inputs/_os-routing.md`, dry-run shown first |

## Contexts

A context is one tracker file. v0.1 ships two by default, auto-created on first invocation if absent:

- **`os-tracker/user.md`** — the user's personal/work backlog. Visible. The thing the user reads.
- **`os-tracker/system.md`** — Personal OS system work. Things the system is tracking that the user doesn't need to see most of the time (skill refinements in flight, ongoing routing work, deferred items the system noticed). Hidden from the user's daily view but available on demand.

Users add more contexts when they earn a split — a separate project, a consulting client, a co-founder context. Each new context is a new file with the same schema. The convention is filename = context slug. No registration step; the file's existence is the registration.

## Task routing — internal vs. external

A task can live in the user's internal backlog (`os-tracker/user.md`) or in an outside task
app they already use (ClickUp, Asana, Linear, Todoist…). Which one is **learned over time**,
not configured from a table up front: the first time a kind of task comes up where the
destination isn't settled, the system asks once, routes it, and records the decision. The
questions taper off as the ledger fills in.

The `setup` mode primes this — it connects the external system (when one's wired) and sets
the safe default (internal-only; nothing leaves the machine until a rule sends it out). The
live state lives in the user's ledger at `os-inputs/_os-routing.md`. Capture and any
direct-route during chat consult that ledger on every task. The full model and the
consult-and-ask protocol are in `references/routing.md`.

## Section schema

Every context file has the same sections in the same order. Sections are optional — empty sections drop. See `references/section-schema.md` for the full schema.

Quick reference:

```
<Context Title>
Last refresh: YYYY-MM-DDTHH:MM

## Next (≤5)

## <Area> — actions

## <Area> — open questions / decisions

## Bugs / time-sensitive

## Needs / blockers

## Ideas / parking lot

## Backlog

## Source map
```

`Next (≤5)` is the user's focus list — strict cap of 5. `Backlog` never auto-archives. `Ideas / parking lot` is prose, not checklist — it preserves "what if…" musings without counting as open work.

## Watermark

Each context carries a watermark line just below the title (`Last refresh: <iso-timestamp>`). When a refresh-style operation runs (relevant once an external-source adapter ships), the watermark bounds the source-note scan. v0.1 markdown adapter doesn't refresh from external sources; the watermark is set on every write so future adapters can use it.

## Contract for other skills

Capture, os-tune, and any skill that creates tasks should invoke Tracker's modes rather than editing files directly. This centralizes section-schema discipline.

The contract:

- `os-tracker/add` accepts: `context`, `section`, optional `area` (sub-grouping within an `<Area> — actions` section), `text`, optional `source` (wikilink to the originating file/note).
- `os-tracker/update` accepts: `context`, `match` (item identifier — text match or item ID), `action` (one of: `done`, `edit`, `move`, `delete`).
- `os-tracker/view` accepts: `context` (or `all`), optional `section` filter, optional `since` timestamp.

See `references/contract.md` for the full contract.

## Operating principles

- **Default to simple. Let the user opt into complexity.** Two contexts pre-created. Sections opinionated. The user can add more contexts, can rename sections, can add custom sections — but only if they ask. The skill never invents.
- **Dry-run before write.** Per the workspace mutation discipline (see `AGENTS.md`). Add and update show the proposed change before applying.
- **Source notes are read-only.** When `add` includes a `source` wikilink, the source note is referenced, not modified.
- **`Backlog` never auto-archives.** Stale items stay visible until the user explicitly archives.
- **Auto-create on first use.** If `os-tracker/user.md` or `os-tracker/system.md` don't exist when a mode first runs, create them with empty section scaffolds (`templates/context.md`). The user reconciles later if they prefer different file locations or names.
- **Skills ship empty.** No personal data inline. Per `AGENTS.md`.
- **System context is hidden by default.** `view` defaults to `context: user`. `view --context system` or `view all` shows system. os-tune reads system as inheritance; the user reads it on demand.
- **The label must stand on its own.** The markdown method has no structured due-date or assignee fields, so the task *text* carries them. Fold the deadline, the who, and the what into the label: "Text Kyle by Tue about the budget," not "Text Kyle." A task you can't act on from its text alone is incomplete — capture the relevant info at write time rather than losing it.
- **Reminders aren't passive tasks.** If an item is time-triggered ("remind me tomorrow / at 3 / next week"), don't silently file it and let the user assume it'll reach them. Either schedule it on the harness's native scheduler so it actually fires, or say plainly that you can't actively ping them — it'll surface on tomorrow's Daily Brief *if* their machine is awake and the brief runs — and offer to set the brief up if it isn't. Never imply a reminder will reach someone when it's just sitting in markdown.

## Adapters (v0.2+)

Markdown is the v0.1 substrate. Future adapters wrap external systems while exposing the same contract:

- **Bear adapter** — wraps a Bear-notes integration that implements the same section schema, watermark, and source-map. Becomes a second adapter, not the canonical one.
- **Apple Notes** — defer until user demand.
- **Obsidian** — defer; Obsidian can read/write the markdown adapter natively if the user points it at `os-tracker/`, so a dedicated adapter may never be needed.

Adapter choice goes in `os-inputs/_os-setup-philosophy.md` when it exists; default markdown until then.

## References

- `references/section-schema.md` — full section schema with examples
- `references/contract.md` — write contract for other skills
- `references/routing.md` — internal-vs-external task routing: the model + the learned consult-and-ask protocol
- `templates/context.md` — empty context starter
