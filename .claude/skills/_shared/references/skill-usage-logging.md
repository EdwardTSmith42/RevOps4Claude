# Skill usage logging

Cross-cutting behavior: os-tune can only notice your patterns if the system is observable to itself. Two channels do that, with different writers — one the harness writes mechanically, one the AI writes by hand.

## Why this exists

os-tune's marketing promise — *"os-tune notices your patterns"* — depends on the system being observable to itself. Without behavioral data, os-tune only sees what the user explicitly captures to inbox. With data, os-tune can detect:

- *"You ran X 14 times last month"* → a skill worth a closer look
- *"You asked the AI to draft client follow-up emails 5 times across sessions, similar phrasing each time"* → make-skill candidate

The first signal lives in the harness's invocation log. The second lives in inbox audit lines. Both feed os-tune's `reflect` mode and proactive prompting.

## Channel 1 — the harness's invocation log

**Written by the harness, not by the AI.** This is the important thing about it. An earlier design asked the AI to append a line at the end of every run; across months of real use it produced nothing, because a silent bookkeeping chore at the least salient moment of a session is a chore that gets skipped. The fix was to stop asking and read what the harness already records perfectly.

Opt-in, off until the user wires it. Setup lives in `skills/os-tune/references/usage-logging-setup.md`; on Claude Code it's a `PostToolUse` hook. Default location `~/.claude/skill-usage.jsonl`, overridable with `OS_SKILL_USAGE_LOG`.

### Format

```jsonl
{"ts":"2026-05-03T15:42:10Z","skill":"os-email","args_preview":"sweep my inbox","cwd":"/path/to/workspace","tool_use_id":"toolu_abc123"}
```

### Fields

- `ts` — ISO timestamp (UTC)
- `skill` — the invoked skill's name
- `args_preview` — the opening of the request, truncated; short requests are captured whole
- `cwd` — the working directory the invocation ran in
- `tool_use_id` — the harness's identifier for the call

Read it with `skills/os-tune/scripts/skill_usage_report.py` rather than parsing it inline — it resolves modes against each skill's declared mode list, which the raw log doesn't carry.

### What this channel can and can't tell you

It answers *which skills ran, how often, and where* — frequency and staleness. It does not record a mode, an outcome, or whether the user tweaked the result, so signals that need those come from Channel 2, from `os-memory/`, or from asking. Claims about tweak counts don't have a data source here; don't write instructions that assume one.

### The legacy workspace log

`os-inputs/_os-skill-usage.log` was Channel 1's original home under the AI-writes-it design. **Nothing writes it now.** Readers fall back to it when it's populated — an install that accumulated entries under the old design keeps its history — but a fresh workspace's copy stays empty, and that's expected rather than a fault.

## Channel 2 — inbox audit lines for non-skill substantive work

Lower-frequency, human-readable signal for substantive AI actions that *aren't* a skill invocation. Written to `os-inputs/_os-inbox.md` as `[type: audit]` entries. The pattern reflect detects here is the most valuable: *"this kind of work isn't a skill yet, but you keep doing it."*

### When to write an audit line

When the AI does substantive ad-hoc work that produces an artifact — drafts, summaries, structured outputs, plans, classifications, deliberate reasoning that ended in something the user kept. Pure conversation doesn't log; substantive work does.

The threshold is the AI's judgment call: *"did this just produce something the user kept or built on?"* If yes, log. If the exchange was clarifying, exploring, or chatting, don't log.

### Format

Standard inbox entry (newest at top), with the audit tag block and a 1-3 line body covering four fields. Compact:

```
## 2026-05-03 — drafted client follow-up email to Anthropic
[type: audit] [skill: none] [task: client-email] [session: sess-abc]

Input: bullet notes from yesterday's call with Anthropic re API quota. Output: 4-paragraph conversational email asking for a follow-up call. Approach: applied the user's default voiceprint, softened tone on the "frustrated" passage. Request: *"draft a follow-up email to Anthropic about the API quota — make it conversational and ask for a call"*
```

### Fields in the body

Four fields, each a short clause. The body packs into 1-3 lines:

- **Input** — what the AI worked from (notes, content, a question, blank page)
- **Output** — what the AI produced (1-line characterization, no full content)
- **Approach** — distinctive moves the AI made (voiceprint applied, framework used, structure chosen)
- **Request** — the user's verbatim instruction phrasing in italics. *This field is the cross-session signal* — reflect compares Request strings across sessions to cluster similar tasks regardless of the AI's task-tag

### Tags

- `[type: audit]` — always
- `[skill: none]` — explicit signal this wasn't a skill invocation
- `[task: <slug>]` — AI's best-effort task-type guess (free-form). Examples: `client-email`, `meeting-notes`, `decision-memo`, `code-review`, `weekly-recap`, `customer-reply`. Hint, not authority.
- `[session: <id>]` — session identifier for grouping

### Why two channels not one

- **Volume.** Skills run often; inbox shouldn't drown in skill-X-ran lines.
- **Format.** Skill-usage.log is machine-data; inbox is human-readable mixed signal.
- **Privacy.** Separate opt-outs (some users want skill metrics but not behavioral records of ad-hoc work, or vice versa).
- **Reuse.** Reflect already reads inbox; no new wiring for non-skill signal.

## How reflect cross-references both channels

Reflect reads BOTH the log and the inbox during pattern surfacing. The clustering logic:

- **Skill-frequency patterns** come from skill-usage.log: *"ran X 14 times, 6 tweaks of the same shape"* → refine candidate.
- **Make-skill candidates** come from inbox audit lines: cluster by `[task: <slug>]` first, then verify by similarity of `Request:` verbatim strings. *"3+ audit lines with similar Request strings, regardless of `[task: ...]` tag"* → make-skill candidate.
- **Cross-channel patterns** can surface too: heavy use of an existing skill PLUS frequent ad-hoc work that overlaps in scope might suggest extending the skill.

The verbatim Request field is the source of truth for clustering. The AI's task-tag is a hint; if reflect sees similar Request strings tagged `client-email` and `customer-checkin`, it clusters them anyway and surfaces *"these look like the same task with different names — what do you actually call this?"*

## Auto-log discipline

Auto-log by default. No asking. Per `AGENTS.md`, asking is reserved for actions with consequences (skill creation, mutations). Logging is consequence-free record-keeping — just do it.

The AI announces direct-routes briefly (per the capture-decision-tree), but the audit-line write itself is silent. The user sees the announcement, not the log entry.

## Privacy — three levels in `_os-setup-philosophy.md`

```yaml
logging:
  log_substantive_non_skill: true   # whether the AI writes inbox audit lines
```

That setting governs **Channel 2 only** — it's the one the AI performs, so it's the one a preference can switch off. Setting it false keeps the harness log (if wired) and stops the audit lines; os-tune loses make-skill candidate detection and keeps frequency detection.

**Channel 1 is not governed from this file.** It's a harness hook the user installs deliberately and removes the same way — see `skills/os-tune/references/usage-logging-setup.md` for what it records and how to turn it off or delete what it collected. A preference file can't switch off something running inside the harness, and pretending otherwise would be the worst kind of privacy claim.

## Rotation

Both channels rotate when they cross thresholds, to keep the active files scannable:

- **The harness log** — rotation is the harness's business, not the workspace's. If it grows past comfort, the user trims or rotates it where it lives.
- **inbox.md** — audit lines with `[status: resolved]` older than 90 days move to `os-inputs/_inbox-archive/<year>.md` per the existing inbox aging convention. Audit lines without status stay until manually resolved.

Rotation operations are deferred infrastructure — the spec is here, the actual rotate runs as its own operation when log size matters. Until then, the files just grow; reflect reads them all.

## What this convention does NOT replace

- The capture-decision-tree's existing `[type: audit]` lines for direct-routes. Those continue logging *routing decisions* (where things went). The new task-audit lines log *substantive work done*. Both coexist with the same `[type: audit]` tag — they're distinguished by `[skill: ...]`. Direct-route audits carry `[skill: capture]`; task audits carry `[skill: none]` plus `[task: <slug>]`.
- The inbox's role as a holding pen for corrections, captures, and lessons. Task-audit lines are a fourth use, additive.
- os-tune's inheritance protocol. The log channels become operational sources where they were previously deferred infrastructure.

## See also

- `os-inputs/_os-inbox-conventions.md` — inbox tag taxonomy, including the `[type: audit]` and `[skill: ...]` tags
- `os-inputs/_os-setup-philosophy.md` — privacy and logging configuration
- `skills/_shared/references/capture-decision-tree.md` — the related direct-route audit-line convention
- `skills/os-tune/modes/reflect.md` — the primary consumer of both channels
- `skills/os-tune/references/inheritance-protocol.md` — sources #7 (inbox) and #10 (skill-usage logs)
