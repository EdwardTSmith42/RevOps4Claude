---
name: os-capture
version: 0.1.0
description: >-
  The inbox processor for Personal OS — classifies open items in
  `os-inputs/_os-inbox.md` and routes to User Tracker, System Worklog, Knowledge,
  Trash, or Promotion (corrections to AGENTS.md / skill refs / SOPs). Pairs with
  os-tune's `close-out` at session end. Two modes: audit, process. Triggers on
  "process my inbox," "audit the inbox," "clear the inbox," "route my captures."
  Do NOT trigger for skill creation/refinement (use os-skillify) or direct task
  entry (use `os-tracker/add`).
display_name: Capture
tagline: 'Process your inbox into action, knowledge, or trash.'
category: Planning
packs:
  - personal-os
icon: 'phosphor:TrayArrowDown'
when_to_use: >-
  Reach for this when the little things have piled up — corrections you tossed off
  mid-chat, links you meant to file, half-formed ideas, loose to-dos — and you
  want them sorted instead of sitting in a heap. Capture reads through everything
  waiting in your inbox and puts each item where it belongs: a task you'll
  actually see, a note in your knowledge base, the trash, or a change to how your
  system behaves.


  Run `audit` to see what it would do, then `process` to clear the lot. A
  satisfying way to reach inbox zero without doing the filing yourself.
modes:
  - name: audit
    job: Read-only review of inbox items and proposed routing.
  - name: process
    job: Apply routing decisions and clear the inbox.
---

# Capture — process the inbox into the right destinations

## Purpose

The inbox is a holding pen — corrections, captures, audit trail. Capture is the processor that clears it. Each open item lands in one of five destinations:

- **User Tracker** (`os-tracker/user.md` via `os-tracker/add`) — actionable items the user wants visible
- **System Worklog** (`os-tracker/system.md` via `os-tracker/add`) — Personal OS system work, hidden from the user's daily view but available on demand
- **Knowledge** (`os-knowledge/<topic>.md`) — durable concepts, frameworks, learnings worth keeping
- **Trash** — explicit drop. The inbox entry stays in place, marked `*Routed to: trash*`, kept as historical record per the inbox conventions.
- **Promotion** — `[type: correction]` entries that earn promotion to `AGENTS.md`, a skill's `references/`, or an SOP. Capture surfaces these with a proposed target and confidence read; the user confirms or redirects. Never auto-routes.

## When to use

- *"Process my inbox"* / *"clear the inbox"* / *"route my captures"* → `process`
- *"What's in my inbox?"* / *"audit the inbox"* / *"show me what's there"* → `audit`

If the user is creating or refining a skill, route to os-skillify. If they're directly adding a task without going through the inbox, route to Tracker's `add`.

## Modes (v0.1)

| Mode | Job | Output |
|---|---|---|
| `audit` | Read-only inspection — counts open items, projects classification, surfaces ambiguous entries; also runs the reachability sweep (files unreachable from `_os-map.md`, reported not fixed) | Inbox-state narrative + audit report + orphan report, no mutations |
| `process` | Classify, dry-run routing plan, apply on confirmation; archives aged resolved/audit entries to the session log | Routed entries marked in inbox, items added to Tracker / Knowledge, aged entries archived |

## Recommended flow

```
audit                          ← read-only, see what's there
   ↓
process --dry-run              ← see the routing plan
   ↓
process                        ← apply
```

Or just `process` — it dry-runs by default before applying.

## Inbox tag respect

Per `os-inputs/_os-inbox-conventions.md`:

- **Skip** entries with `[type: audit|lesson|reject]` — system metadata (os-tune / os-skillify audit trail), not user items.
- **Skip** entries with `[status: resolved|deferred]` — already handled.
- **Process** entries with `[status: open]` or no status tag.
- **Treat `[type: correction]` differently** — these go to the Promotion path, not Tracker / Knowledge / Trash.
- **Process tag-less entries** as user items (the most common case for human-written entries).

When marking an entry processed, append `[status: resolved]` and an italic `*Routed to: <destination>*` line below the entry body. Don't delete or rewrite the entry.

## Classification confidence

Borrows os-tune's `[tier: trivial|moderate|large]` vocabulary. Two practical tiers in v0.1; the third earns its place when needed:

- **Trivial** — high-confidence classifications. Clear noise, obvious task, unambiguous knowledge entry. Batched into a single dry-run preview the user approves wholesale.
- **Moderate** — uncertain. Ask one-at-a-time with a proposal + one alternative. The user picks or redirects.
- (**Large** — held for future. If a class of ambiguity keeps requiring context-heavy decisions, that's the trigger to add a third tier with explicit deferral.)

The disposition is *act when confident, ask when uncertain, learn from corrections.* The early-life skill leans on the user more — early asks calibrate the heuristics — and graduates classes of items to auto-routing as patterns stabilize. Every redirect is calibration data for what the system mis-classified. *How* the system captures is itself something it learns to do automatically over time. (The exact tuning protocol for this graduation is an open question, listed under Open questions below.)

Default behavior: trivial batches together; moderate asks individually. The user can opt into "ask everything" or "auto-approve trivial silently" via `os-inputs/_os-setup-philosophy.md` when it exists.

## Cadence

- **Manual** — primary invocation. The user runs `process` when they want.
- **Session-end** — os-tune's `close-out` mode offers Capture when there are unprocessed inbox items at session end. The user confirms or skips.
- **Scheduled / background** — held as an open design question (listed under Open questions below). Directional preference: pair Capture's inbox processing with os-autosave and os-tune as a scheduled or morning-routine background sweep — frequent enough to be useful, infrequent enough to stay out of the way, dispatched to a sub-agent so the user isn't blocked. Not committed; v0.1 stays manual + session-end.

## Hard guardrails

- **Dry-run before any write.** Per workspace mutation discipline.
- **Never auto-route corrections.** `[type: correction]` always surfaces with a proposed promotion target; the user confirms.
- **Never delete inbox entries — archive them.** Routed entries stay in place with `[status: resolved]` and the routing trail. At the end of a `process` run, entries resolved before the current session (and `[type: audit]` lines older than the session) move to `os-inputs/_os-session-log.md` as dated one-liners with their routing trail intact. The inbox stays a short queue; the session log stays the durable episodic record ("what did we work on last week" is answered there, not by scrolling the inbox). Nothing is ever discarded — archival is relocation, not deletion.
- **The reachability sweep reports, never fixes.** `audit` lists files unreachable from `_os-map.md` (per the knowledge-system invariants in `_shared/references/workspace-layout.md`); attaching an orphan is a routing decision for `process` or the user, not an auto-fix.
- **Never overwrite the system audit trail.** Skip `[type: audit|lesson|reject]` entries — these are mechanical logs other skills wrote for their own purposes.
- **Write to Tracker through the contract.** Capture never edits `os-tracker/*.md` directly. Always goes through `os-tracker/add`.

## References

- `references/classification-rules.md` — how to decide which destination an entry routes to
- `references/promotion-paths.md` — for `[type: correction]` entries, how to propose AGENTS.md / skill ref / SOP destinations

## Open questions (v0.2 candidates)

- **Knowledge structure.** Currently flat at `os-knowledge/<topic>.md`. Sub-organization (by domain, by source skill, etc.) earns its place when the directory grows enough to make scanning hard.
- **Aging-out / archive.** Resolved entries older than ~90 days could move to `os-inputs/_inbox-archive/<year>.md` to keep the active inbox scannable. `reflect` could read both. Defer until inbox volume warrants.
- **Cross-context routing.** When an item could be either User or System Tracker (e.g., a follow-up with an external vendor that's both a personal action and something the system is tracking), v0.1 asks. If the ambiguity recurs, a heuristic earns its place.
