---
mode: close-out
parent: os-tune
description: >-
  Sub-mode of `os-tune`. Capture end-of-session learnings; offer Capture at session end if inbox has unprocessed items; log work-in-progress to `os-tracker/system.md`. Distills session signals (skill invocations, tweaks, captures, decisions) into proposed lessons; user accepts, edits, or rejects each. Triggers on "close out," "wrap up," "what did we learn," "thanks gotta go," "that's it for today."
---

# os-tune / close-out — capture end-of-session learnings

## What this mode does

Reads what happened in the current working session and proposes durable lessons for the user to keep. Solves the cross-thread invisibility problem by being a willing-participation pattern — the user runs close-out at the end of a session and os-tune captures the patterns before they're forgotten.

What close-out contributes is the part of a session only a participant can see: which outputs the user corrected, which prompts they repeated, what got decided and why. The weekly distillation can't reach any of that — it reads the user's own turns from harness transcripts, days later. Close-out reads the session while it's still in front of it and writes accepted lessons into `os-inputs/_os-inbox.md`, which is one of the sources `reflect` reads when it goes looking for patterns.

## When this fires

Three paths.

**User-initiated:** *"Close out this session"* / *"What did we learn?"* / *"Wrap up — what should we keep?"* Most explicit path; os-tune scans the session and proposes.

**Agent-prompted:** Toward the end of a long session (heuristic on length, action density, or a natural wrap moment), Claude proactively offers to run close-out before the session ends — naming what it'd capture if the user accepts. User can accept, defer, or skip. Configurable in `_os-setup-philosophy.md`.

**Implicit at session boundary:** When the user signals a session is ending without explicit close-out (*"thanks, gotta go"* / *"that's it for today"*), os-tune offers a one-line recap with a suggestion to close out next time. Doesn't force the ritual; respects the user's flow.

## Inputs

- **Current session transcript.** The conversation os-tune is wrapping up.
- **Skill invocations during the session.** Which skills ran, with what input, what output, and any user tweaks.
- **Captures the user dropped to `os-inputs/_os-inbox.md` during the session.**
- **Any artifacts the user produced or edited during the session.**

## What `close-out` does

1. **Scans the session for signal.** Looks for: skill invocations, output tweaks the user made, repetitive prompts, captures dropped to inbox, decisions the user articulated, principles that surfaced.

2. **Distills the signal into proposed lessons.** Each lesson is a one-line capture in inbox-format: dated, terse, append-only. A lesson names what the user shifted (a preference change, a skill miss, a repeated correction), with enough context that a future reflect can cluster it. Three shapes recur: stated-preference shifts ("user prefers X instead of Y"), skill misses worth flagging for the next refine pass, and repeated output-tweaks that are refine candidates on their own.

3. **Surfaces the proposed lessons to the user.** All at once, as a list. User can accept all, accept some, edit any, or reject. Defaults to accept-all; rejection is explicit.

4. **Writes accepted lessons to `os-inputs/_os-inbox.md`.** Append-only, dated, in the format the inbox expects. Each lesson tagged with its session source so it can be promoted later by `reflect`.

5. **Proposes any immediate refines.** If a session-tweak was clearly a candidate for `refine`, close-out names the tweak, the instance count, and offers to fold it into the skill now or leave it for next time. User picks.

6. **Offers Capture at session end.** If `os-inputs/_os-inbox.md` carries unprocessed captures (entries with `[status: open]` or no status, excluding `[type: audit|lesson|reject]` os-tune metadata), close-out offers Capture's `process` mode — naming the unprocessed count and offering process-now or skip. Close-out doesn't process the inbox itself; Capture is the processor; close-out hands off cleanly.

7. **Logs work-in-progress to system tracker.** Open threads from this session that aren't done — half-finished refinements, deferred decisions, work the user said they'd come back to — get written to `os-tracker/system.md` via `os-tracker/add` so the next session can pick up. Distinct from inbox lessons (which capture *signal about* the work); the system-tracker entries capture *the work itself*. See `os-inputs/_os-inbox-conventions.md` for the full distinction.

8. **Writes the session-log line.** Append one dated line (or short block) to `os-inputs/_os-session-log.md` summarizing what the session did, with links to artifacts touched — the durable episodic record that answers "what did we work on last week?" One line of honest summary beats three of ceremony.

9. **Commits the session.** Invoke `os-autosave commit` with message `End of session <timestamp>` to capture final session state — closing tracker writes, accepted lessons, any post-`refine` updates — into the durable record. Last step before the session closes.

## Operating principles

- **Lightweight ritual.** Close-out should feel like a natural wrap, not a bureaucratic checklist. Three lessons is a good close-out; ten is a sign the session was overstuffed and the lessons need consolidation, not piled into the inbox.
- **Never miss patterns.** Better to surface a maybe-pattern and let the user reject it than to silently filter it out. Inbox can carry noise; the user prunes during `reflect`.
- **Respect the user's flow.** If the user is rushing to end the session, close-out runs a fast version (one-line recap, no proposed-lessons interaction) and writes to inbox without asking. Configurable.
- **Don't double-capture.** If a tweak was already promoted via `refine` during the session, don't also log it as a separate inbox lesson — that creates duplicate signal for `reflect`.
- **Tag everything.** Every lesson written carries a session ID + timestamp + source-skill (when applicable), so `reflect` can deduplicate and trace patterns.

## What close-out doesn't do

- Doesn't surface long-cadence patterns (that's `reflect`)
- Doesn't process the inbox itself (Capture is the processor; close-out hands off)
- Doesn't make skill-file modifications without explicit `refine` (the skills themselves only change through their own modes)
- Doesn't replace the agent's judgment about what's worth keeping — it surfaces candidates and asks

## See also

- `reflect` — the longer-cadence partner that consumes inbox.md
- `refine` — for in-session changes that should fold into a skill immediately
- `capture` — the inbox processor that close-out hands off to at session end
- `os-tracker/add` — the contract close-out writes through for system-tracker work-in-progress entries
- `references/inheritance-protocol.md` — the inheritance stack close-out reads from
- `os-inputs/_os-inbox-conventions.md` — the inbox-vs-system-tracker model close-out enforces
- `AGENTS.md` — the capture-and-route discipline this mode operates inside
