# Capture decision tree

How AI should handle capture intent during chat. Referenced from the workspace operating principles (`AGENTS.md`) and any skill that needs to decide between direct-route, sub-agent, and inbox.

## What counts as a capture subject

Everything worth keeping, regardless of who typed it. Chat items include what the user pastes or says **and what the user and AI produce together** — research results, skill outputs, analyses, artifacts from a working session. A substantial artifact the pair just made is as capturable as a link the user dropped, and it routes through the same tree. Retroactive capture is first-class: *"capture what we just talked about"* (or *"save this," "capture that research"*) sweeps the session's substantive output through the tree with the same effect as if each piece had been routed in the moment.

## Project vs. exploring — the intent layer

Before routing an artifact the session produced, read the working mode:

- **Working a project** (the artifact feeds ongoing, named work) → saving is a no-brainer. Route silently to the artifact's home per the storage invariants (`workspace-layout.md`), link it from the project's hub note if one exists, acknowledge in one line.
- **Exploring** (playing with an idea, no committed project yet) → offer once, one line — keep or let it go. Save on yes; drop without ceremony on no or silence.

The distinction is about the *user's investment*, not the artifact's quality — exploration produces gems too, which is why the offer exists at all.

## The default is direct-route

Most routing is obvious from the content itself. AI's parallelism means queueing isn't a free win — the queue is friction unless it earns its place.

Three lanes, decided by the answer to two questions: *"is the destination clear from the content?"* and *"is the work heavy enough that the user should keep moving?"*

| Lane | Picks when | Mechanic |
|---|---|---|
| **Direct route** | Destination is clear, work is fast | Sync write to destination; brief one-line acknowledgment to user |
| **Background sub-agent** | Destination is clear, work is heavy (transcript extraction, golden-nugget mining, summary of long content) | Dispatch sub-agent; user keeps moving; result lands in destination; AI reports on completion |
| **Inbox** | Destination genuinely unclear, multi-item decomposition needs review, batch-context benefits classification, or user explicitly asks to queue | Append to `os-inputs/_os-inbox.md` with `[type: capture]` (or `[type: correction]` for corrections); processed later by Capture |

## Read destination from the content

Most captures show their own destination if you read the surface:

- **Action item** (request, reminder, deadline, "I should…", "remind me to…", "follow up on…") → **tracker** (User context unless system-flavored). Whether a user task lands in the internal backlog or an external app (ClickUp, Asana…) is *learned*: consult `os-inputs/_os-routing.md` — match a confirmed rule and route silently; no match, ask once (two options), route, and record the rule; default internal when unsure. Full protocol in `os-tracker/references/routing.md`.
- **Created artifact** (writing, report, plan, presentation, client deliverable, creative work, or another thing the user made or Personal OS made on their behalf) → **outputs** (`os-outputs/`) when the user wants to keep it. Organize around the user's actual practice — client, project, content type, theme, or another contextual home — rather than imposing a universal hierarchy. Mark drafts clearly; preserve the first meaningful draft and final version as separate files with the same stem and different lifecycle suffixes. If the work genuinely pivots into something else, start a new filename family and link it to the original.
- **Content / idea / quote / link / framework / fragment** ("this is interesting," "save this," "btw [link]," "quote: …") → **knowledge** (`os-knowledge/<topic>.md`) — keep *what's valuable* from it plus the source, not just the raw link; extract when it warrants (heavy → sub-agent). When the content resists a plain fetch (blocked, JS-rendered, transcript-shaped), climb the acquisition ladder in `web-content-acquisition.md` before giving up. Not a reading-list item unless the user says so.
- **Correction of AI's work** ("I would never say X," "we don't end prices in 7") → **inbox** with `[type: correction]` (always — corrections want promotion review, never auto-route to durable destinations)
- **Reflection or principle** that's not yet a correction → **knowledge** if standalone, **system worklog** if about Personal OS itself
- **Nothing routes to `os-memory/`.** It isn't a capture destination — the weekly pass writes it by distilling past sessions, and capture never puts anything there. If something in the moment is worth remembering, it belongs in one of the destinations above; memory is what gets derived later, not what gets filed now.
- **Multi-item note** (drive-and-talk journal, meeting notes with several actions) → **inbox**, will be exploded into sub-entries by Capture
- **Cross-system signal** (email needing reply, Slack thread, ClickUp ticket) → **dedicated triage skill for that system** (email for Gmail; Slack/ClickUp future skills). Personal OS inbox only when escalation needed.

## Worked examples

| Capture | Lane | Where |
|---|---|---|
| *"Save this article — [link]"* | Direct | `os-knowledge/<topic>.md` |
| *"Save this email draft so I can edit it later"* | Direct | `os-outputs/<artifact-stem>-first-draft.md` |
| *"This is interesting — [paste]"* | Direct | `os-knowledge/<topic>.md` |
| *"Remind me to follow up with Anthropic about the API quota"* | Direct | `os-tracker/user.md`, actions, area: External |
| *"I'd never say 'load-bearing' to my readers"* | Direct (with type tag) | `_os-inbox.md` `[type: correction]` |
| *"Pull the golden nuggets from this YouTube video [link]"* | Sub-agent | Sub-agent runs gold skill; writes to `os-knowledge/<topic>.md`; reports on completion |
| *"Here are 15 bookmarks from X this week"* | Inbox or sub-agent | Inbox if user wants to see clusters before routing; sub-agent if user wants them processed and clustered into knowledge directly |
| Drive-and-talk note covering 8 things — tasks, reflections, research items | Inbox | Process step decomposes into N sub-entries, each routes per its content |
| *"This is interesting"* (about a Slack DM from her boss asking for a deliverable) | Direct | `os-tracker/user.md` — read the surface; the content is an action item, not a fragment for knowledge |
| Mid-session insight while building a skill | None — work in progress | The artifact is the capture. Tangential thread? → inbox. Otherwise let close-out catch it. |

## When to ask before capturing

Don't ask on every capture. Ask when:

- Destination is genuinely ambiguous between two clear options ("this could be tracker or knowledge")
- The capture would create a new file (new `os-knowledge/<topic>.md` topic) — confirm topic name once
- The user's framing is unclear enough that the AI's interpretation might miss

Don't ask when:

- User said *"save this"* / *"this is interesting"* / *"capture this"* — they've already opted in
- Surface content tells you the destination
- It's a correction (just write it; user can correct the correction)

## Audit logging — calibrated, not blanket

Two distinct flavors of audit-line, both written to `os-inputs/_os-inbox.md` with `[type: audit]`:

### Direct-route audits (`[skill: capture]`)

For *routing decisions* — where the AI sent a captured item. Logged when the action has consequence:

- **Tracker adds** → audit-log (action items have follow-through)
- **Sub-agent dispatches** → audit-log (async work; user may want to know what fired and when it lands)
- **Promotions** (`AGENTS.md`, skill refs, SOPs) → audit-log (durable behavior changes)
- **Knowledge writes** → audit-log only when sub-agent-driven or large; trivial knowledge appends don't need an audit line
- **Inbox writes** → not logged (the inbox itself is the record)

Audit lines are one-line summaries: *"Routed to `os-tracker/user.md`: follow up with Anthropic about API quota"*. Enough to scan and undo if needed; not noise.

### Task audits (`[skill: none] [task: <slug>]`)

For *substantive non-skill work the AI did* — drafts, summaries, structured outputs, classifications, anything that produced an artifact the user kept. The pattern reflect detects here is the most valuable: *"you keep doing this kind of thing without a skill — make one?"*

Format covers four fields in 1-3 lines: Input / Output / Approach / Request (verbatim, in italics). The Request field is the cross-session signal — reflect clusters by similar Request strings to detect repetitive tasks even when the AI's `[task: ...]` slug differs across instances.

Threshold for "substantive": did the AI produce something the user kept or built on? If yes, log. Pure conversation, clarifying questions, exploratory chat — no log.

Full spec for both flavors plus skill-usage.log JSONL channel: `skill-usage-logging.md`.

## Announce briefly, never silently

After every direct-route, sub-agent dispatch, or inbox capture, AI tells the user what just happened in one line. Examples:

- *"Saved to `os-knowledge/<topic>.md` (e.g. an agentic-memory note)."*
- *"Saved the first draft to `os-outputs/<artifact-stem>-first-draft.md`."*
- *"Added to your tracker under External."*
- *"Running gold on that link in the background — will write to `os-knowledge/<topic>.md` and ping you when done."*
- *"Captured to inbox — there are 8 items in this note; run `process` to route them."*

The user shouldn't have to ask what happened. They also shouldn't get a paragraph about it.

## User overrides

User can always override the lane:

- *"Just queue it"* — force inbox even if direct-route would fire
- *"Just do it"* — force direct-route even if AI would have queued
- *"Process this in the background"* — force sub-agent
- *"Wait, undo that"* — revert the last direct-route or sub-agent dispatch (read the audit line, remove the entry)

## Configuration

Per-user overrides in `os-inputs/_os-setup-philosophy.md`:

```
## capture
direct_route: enabled         # set false to force everything through inbox
background_processing: enabled # set false to make user wait for heavy work
audit_log_knowledge: false    # set true to log every knowledge write, not just sub-agent / large
```

Defaults match the calibrations above. Override only when the default friction matters.
