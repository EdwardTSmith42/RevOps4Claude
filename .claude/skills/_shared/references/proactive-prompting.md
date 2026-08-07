# Proactive prompting

Cross-cutting AI behavior: when the user is doing substantive work that matches a recurring pattern, surface a brief offer to systematize. Inline-and-immediate, not session-start. Triggered by the work itself.

## Why this exists

The skill-usage signals (the harness invocation log, when wired, + inbox task-audit lines) record what the user keeps doing. Without proactive prompting, that data sits dormant unless the user remembers to ask. Proactive prompting is the consumer that turns logged behavior into useful nudges *at the moment they're useful* — when the user is doing the thing for the Nth time and would benefit from being freed from re-typing it.

The discipline is restraint. One offer per recurring pattern. Easily ignored. Always low-stakes ask. The magic is the AI catching the moment a pattern earns systematization without the user having to think about it.

## When it fires

When the AI is about to do (or has just done) substantive work for the user, AND that work matches a recurring pattern in the logs.

**Conditions for firing:**

1. The user's current request triggers substantive AI work (drafts, summaries, structured outputs, classifications — anything that would land as a task-audit line in the inbox).
2. Recent logs show **3+ similar instances** within the last **14 days** (configurable).
3. The pattern is NOT in `os-inputs/_os-proactive-prompts-rejected.md` within its rejection window.
4. `os-inputs/_os-setup-philosophy.md` has `proactive_prompting.enabled: true` (or absent — default is on).

**One exception to the threshold — tool knowledge just earned.** When the session has just worked out how to drive an external tool (fetched a CLI's docs, discovered an MCP's real tool names, untangled auth, landed a working invocation), offer to bank it as a tool-wrapper skill *immediately* — no 3-instance wait. The re-discovery cost is obvious on the first encounter, and the knowledge evaporates at session end if uncaptured. Pattern and contents spec: `skills/os-skillify/references/tool-wrapper-skills.md`. The other skip conditions below still apply (hurry, one-off framing, one offer per session).

**Conditions to skip even when matching:**

- First or second instance of a pattern (threshold is 3+, not 2+ — avoids false-positive offers on early coincidences).
- The user's framing suggests a hurry (*"quick one"*, *"just real fast"*) or an explicit one-off (*"this is a one-time thing"*). Don't interrupt momentum.
- The work was just dispatched to a sub-agent — wait until the sub-agent reports back, then decide.
- The current session has already surfaced a proactive prompt that the user deferred or rejected. One offer per session, max.

## How matching works

The matching layer reads two signals:

1. **The harness invocation log** (when the user wired it — `skills/os-tune/references/usage-logging-setup.md`) — for skill-frequency patterns. *"User invoked os-email 14 times this month"* → not a make-skill candidate (the skill exists), but a skill worth revisiting. Absent the hook, this signal simply isn't available; work from the audit lines.

2. **Inbox task-audit lines** (`[type: audit] [skill: none] [task: <slug>]`) — for non-skill patterns. The make-skill candidate signal lives here.

For task-audit matching, the **verbatim Request string is the source of truth** (per the cross-session verbatim-signal principle). The AI's `[task: <slug>]` is a hint, not authority — cluster by Request similarity even when slugs differ. Two entries tagged `client-email` and `customer-checkin` with similar verbatim Request strings are the same pattern.

Practical matching heuristic for v0.1: the AI reads the last ~40 task-audit entries plus the current request. If 3+ entries (including the current one if it'll log) have similar Request strings (substring overlap, paraphrase similarity, same task scope), the pattern qualifies.

## Surface format

Always do the work first. Then surface the offer at a natural break point in the response. One line, casual, low-stakes:

> *"Done. Btw, this is the 4th similar follow-up email this week — same shape each time. Want to make a skill so you don't have to keep asking?"*

> *"Drafted. I notice you've structured 5 meeting notes the same way since last Tuesday. Make this a skill?"*

> *"Routed. You've added 6 'follow up with X' tracker items in the past 10 days. Want a skill that drafts the follow-up email and tracks the followup together?"*

The offer's three components:
- **Concrete count + window:** *"4th similar email this week"* — fact, drawn from log, verifiable.
- **One-line characterization of the pattern:** *"same shape each time"* — what's repeating.
- **Low-stakes ask:** *"Want to make a skill?"* — never *"you should"* or *"this needs to be."*

Avoid:
- Generic phrasing (*"I noticed a pattern"*) — be specific.
- Pushy framing (*"you really should systematize this"*) — never.
- Multiple offers in one response (one pattern at a time).
- Offering before the work is done (interrupts momentum).

## User responses

Four shapes:

**Accept** — *"yes"* / *"make it"* / *"do it"*
→ AI invokes the appropriate `skillify` mode (typically `os-skillify/microtool-from-job` for emerging task patterns, occasionally `os-skillify/from-content` if the pattern surfaced from content work). The accepted pattern signature is logged so the AI knows the skill exists for future runs.

**Defer** — *"not now"* / *"later"* / *"remind me next week"*
→ Add the pattern to `os-inputs/_os-proactive-prompts-rejected.md` with a 14-day window (configurable). The pattern doesn't resurface for that window even if it keeps occurring.

**Reject** — *"not interesting"* / *"don't ask again"* / *"I prefer to do this manually"*
→ Add to `os-inputs/_os-proactive-prompts-rejected.md` with `permanent` window. Never resurfaces.

**Ignore** — user says nothing about the offer and proceeds with their own agenda.
→ No state change. The offer doesn't resurface this session, but can fire again next session if the pattern remains.

## Rejection state — `os-inputs/_os-proactive-prompts-rejected.md`

Format: per-pattern entries with timestamp, window, and verbatim signature for matching.

```
## task: client-email
Rejected 2026-05-03, window 14d. Verbatim signature: *"draft a follow-up email to Anthropic"*

## task: meeting-summary
Rejected 2026-05-04, permanent. Verbatim signature: *"summarize this meeting note"*. Reason: prefer to keep manual.
```

The AI checks this file before surfacing any offer. Pattern signature matching uses the same verbatim similarity logic as the detection layer. After the rejection window expires, the entry's window date is in the past — the pattern can fire again. Permanent rejections never expire.

User can edit this file directly to remove rejections (or undo a "permanent" by changing the window).

## Privacy and disable

Configurable in `os-inputs/_os-setup-philosophy.md`:

```yaml
## proactive_prompting
enabled: true                      # surface skill-candidate offers when patterns detected at moment of work
threshold_count: 3                 # how many matching instances qualify a pattern
threshold_days: 14                 # how recent the matches must be
respect_rejection_days: 14         # default rejection window when user defers
```

Default `enabled: true`. The first time it fires for a user, the AI adds a one-line first-fire notice:

> *"(I'm watching for repeated patterns and will surface skill-candidate offers when I notice them — once per pattern. Disable in `os-inputs/_os-setup-philosophy.md` if not useful.)"*

This shows up only once. Subsequent offers don't repeat the meta-explanation.

For users who want zero behavioral pattern detection, setting `proactive_prompting.enabled: false` (or `logging.level: disabled` for the broader opt-out) silences the feature entirely.

## How this differs from `reflect`

Reflect is the longer-cadence sibling consumer of the same logs. Proactive prompting is **inline and immediate**; reflect is **batched and reflective**. Both feed off the same data:

| Feature | Trigger | Cadence | Surface |
|---|---|---|---|
| Proactive prompting | Current work matches pattern | Per substantive action | One-liner offer in the AI's response |
| Reflect | User invokes (or scheduled) | Weekly / monthly / threshold-based | Multi-pattern report with proposed routes |

A pattern surfaced by proactive prompting that the user defers might still appear in reflect's next run as a stronger pattern (more instances accumulated). A pattern rejected permanently won't appear in either.

## What this does NOT do

- **Doesn't fire at session start.** That's a v0.2 candidate. The trigger problem (when is "session start" really a session start?) is harder than the inline trigger; defer until inline is shipping and we have user-feedback data.
- **Doesn't ask 25 follow-up questions.** One offer, one line. Per pace-the-human.
- **Doesn't volunteer mid-work.** The offer comes AFTER the AI does the requested work, not before.
- **Doesn't replace explicit invocation.** *"Hey os-tune, anything notable?"* still works as a manual escape valve and triggers a broader scan.

## Sketched algorithm (for the AI implementing this)

1. User makes a substantive request.
2. AI does the requested work (drafts, summarizes, classifies, etc.).
3. While doing the work or just after, AI scans:
   - Last ~40 inbox task-audit entries
   - Recent skill-usage.log entries
   - `os-inputs/_os-proactive-prompts-rejected.md`
4. AI checks: does the current work match a recurring pattern? (Verbatim Request similarity to 3+ recent entries, not currently rejected, threshold met.)
5. If yes, AI adds a one-liner offer at a natural break in the response.
6. If user accepts, AI routes to appropriate skillify sub-mode. If user defers/rejects, AI updates rejection state. If user ignores, no state change.
7. Either way, the work is logged as a task-audit entry per usual capture-decision-tree behavior — including the fact that an offer was surfaced (in the entry's audit notes).

## See also

- `skills/_shared/references/skill-usage-logging.md` — the producer side; what feeds proactive prompting
- `skills/_shared/references/capture-decision-tree.md` — how substantive work gets logged in the first place
- `skills/os-tune/modes/reflect.md` — the longer-cadence sibling consumer
- `skills/os-skillify/SKILL.md` — the destination when user accepts an offer
- `AGENTS.md` — the sub-principle that triggers this behavior
