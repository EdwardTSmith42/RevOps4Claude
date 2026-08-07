---
mode: reflect
parent: os-tune
description: >-
  Sub-mode of `os-tune`. Surface longer-cadence patterns from accumulated logs (skill-usage.log, inbox task-audit lines, system tracker). Proposes refines (heavy-tweaked skills), makes (recurring tasks without a skill yet), extends (related new behavior), or deprecates (unused skills). Inline proactive prompting is the immediate sibling consumer; reflect is the weekly/monthly partner. Triggers on "what patterns have I been hitting," "reflect on the last month," "run a weekly review," "what should I be doing differently."
---

# os-tune / reflect — surface longer-cadence patterns

## What this mode does

Reads accumulated `os-inputs/_os-inbox.md` entries plus skill-usage logs and surfaces the strongest patterns. Proposes consolidations, new skills, refinements, or deprecations based on what's actually been happening across many sessions.

If `close-out` is the end-of-day ritual, `reflect` is the end-of-week or end-of-month one. Same mechanism, longer window. The two complement: close-out captures fine-grained signal session by session; reflect identifies which signal has compounded into a real pattern worth acting on.

Reflect also has an inline-and-immediate sibling: **proactive prompting** (per `_shared/references/proactive-prompting.md`). Both consume the same logs (skill-usage.log + inbox task-audit lines). Proactive prompting fires AT the moment of work when the current request matches a recurring pattern; reflect runs at longer cadences and surfaces multi-pattern reports. Patterns deferred during proactive prompting may surface in reflect's next run as the instance count grows; permanently-rejected patterns surface in neither.

## When this fires

**User-initiated:** *"What patterns have I been hitting?"* / *"Reflect on the last month"* / *"Run a weekly review."* The most common path.

**Schedule-prompted:** A scheduled reminder fires (per `os-inputs/_os-setup-philosophy.md` user-configurable cadence — typical is weekly Monday morning or monthly first-of-month). Claude offers to run reflect, naming how long it's been since the last one. User accepts, defers, or skips.

**Threshold-triggered:** When inbox.md crosses a configurable size threshold (e.g., 25+ unprocessed entries) or skill-usage logs show a pattern has fired more than N times unaddressed, os-tune surfaces a short *reflect candidate* — naming the pattern, its instance count since the last reflect, and offering to address it now.

## Inputs

- **`os-inputs/_os-inbox.md`** — accumulated session lessons, corrections, captures, and audit lines since the last reflect run. Task-audit lines (`[type: audit] [skill: none] [task: <slug>]`) carry the cross-session signal for non-skill repetitive work; their verbatim `Request:` field is the source-of-truth for clustering similar tasks across sessions.
- **`os-tracker/system.md`** — ongoing Personal OS system work; long-running unresolved threads are themselves a pattern signal (something the system has been chipping at without finishing).
- **`os-memory/`** — the distilled memories, and the primary input. Each carries a `kind`, a `summary`, and for recurring-request memories the user's own phrasing. Clustering these is what surfaces make-skill candidates. Produced by `distill`; see `../references/memory-format.md`.
- **`os-memory/_ledger.md`** — what's already been acted on or declined. Read this *first*: a pattern with a ledger line is settled, and re-proposing it is how a system that notices becomes a system that pesters.
- **The harness's skill-invocation log** — a mechanical record of which skills ran, written by the harness rather than by an agent (on Claude Code, a `PostToolUse` hook appending to `~/.claude/skill-usage.jsonl`). Drives frequency and refine-candidate detection. `../scripts/skill_usage_report.py` reads this log and resolves modes against each skill's declared list — use it rather than parsing here. If no such log exists, work from memories alone — they carry the stronger signal anyway — and mention once, in a line, that turning on invocation logging would sharpen the next run. See `../references/usage-logging-setup.md`. One mention; if they decline, that's answered.
- **Last reflect's output** — what was promoted, deferred, or rejected last time (avoids re-proposing rejected patterns)
- **`os-inputs/_os-setup-philosophy.md`** — user preferences for what reflect should focus on or skip
- **Optional time window** — *"reflect on this week"* vs *"this month"* vs *"since last reflect"*

## What `reflect` does

1. **Aggregates signal across the time window.** Counts: how often each skill ran, how often each kind of tweak appeared, how often each lesson type was logged. Builds a frequency picture.

2. **Identifies strong patterns.** A pattern is strong when:
   - The same lesson appears 3+ times in inbox without resolution
   - The same skill-output tweak appears 3+ times across sessions (skill-usage.log signal: high tweak-count on the same skill+mode)
   - A new repeat-prompt pattern emerges — 3+ task-audit lines (`[type: audit] [skill: none]`) across sessions with similar verbatim `Request:` strings. The AI's `[task: <slug>]` tag is a hint, not authority; cluster by Request similarity even when the slugs differ. Make-skill candidate.
   - A skill is heavily used and consistently tweaked (refine candidate — combines skill-usage.log frequency with high tweak count)
   - A skill is rarely used and may be a deprecate candidate
   - Cross-channel pattern: heavy use of an existing skill PLUS frequent ad-hoc work that overlaps in scope (extend candidate — the existing skill's purpose may want broadening)

3. **Proposes actions per pattern.** Each pattern surfaces with a recommended route:
   - **Refine** existing skill (most common — accumulated tweaks that should be defaults)
   - **Make** new skill (recurring task that doesn't have a skill yet)
   - **Extend** existing skill (related new behavior emerging from use)
   - **Promote** an inbox lesson to a durable reference or principle
   - **Deprecate** (routes to `os-skillify enhance` — audit/retire) a skill that hasn't been used in N weeks
   - **Consolidate** (routes to `os-skillify consolidate`) two skills that have converged in purpose

4. **Surfaces the top 1–3 patterns to the user.** Don't overwhelm. The strongest signals first. User picks which to act on; the rest stay in inbox for next reflect.

5. **Routes accepted patterns to the appropriate mode.** A "refine" pattern triggers `refine`; a "make" pattern triggers the os-skillify handoff with the accumulated context as input. The user confirms each routing and the action runs.

6. **Marks processed inbox entries.** Lessons that fed an action get tagged as resolved (or archived to `os-inputs/_os-session-log.md` if the user prefers a short inbox (never deleted — archival is relocation, per os-capture's guardrail)). Lessons that were considered but rejected get tagged so they don't resurface in the next reflect.

## Operating principles

- **Strongest signals only.** Better to surface 1 strong pattern than 10 weak ones. The user's time is the constraint; reflect's job is signal-to-noise, not exhaustive coverage.
- **Trace the source.** Every pattern surfaced shows what's behind it: which sessions, which inbox entries, which skill-usage logs. The user can interrogate before approving.
- **Don't re-propose rejected patterns.** If the user rejected a pattern last reflect, don't surface it again unless the underlying signal has materially changed.
- **Configurable cadence.** Some users want weekly reflects, others monthly, others only on threshold trigger. `_os-setup-philosophy.md` carries the preference.
- **Audit trail to inbox.** Reflect's output (what was surfaced, what was acted on, what was rejected) writes to inbox.md as its own meta-entry, so future reflects can see the history.
- **Watch for skill-prompting-principle drift.** Beyond usage-frequency signals, reflect also passes the existing skill library through the lens of `../../_shared/references/skill-prompting-principles.md` as one of its pattern detectors. A writing-domain skill that's mostly bullets, a judgment-domain skill that's mostly hard rules, a template full of verbatim sample text — these are principle-violation patterns that surface as `refine` candidates even when usage metrics look healthy. Especially worth running after the principles themselves have been added or revised (skills built before the principles existed are the highest-leverage target).
- **Watch for frozen-additive skills.** Load `../../_shared/references/self-extending-skills.md` and pass the library through its lens too. A skill the user invokes often, with a tweak history that frequently surfaces requests in the family "the skill should also handle X" — and that doesn't currently carry the three-beat self-extending pattern — is an additive skill that's frozen. Surface as a refine candidate. The fix isn't to add each requested capability one at a time; it's to add the self-extending pattern so the skill can grow with future asks in the same family.

## What reflect doesn't do

- Doesn't act unilaterally — every pattern requires user confirmation before running
- Doesn't replace `close-out` (different time window, different signal density)
- Doesn't surface every pattern it sees — filters aggressively for the strongest

## Edge cases

**Inbox is empty.** No reflect needed. os-tune surfaces a short *nothing accumulated* line and exits cleanly.

**All patterns are weak.** Reflect names the strongest signal it saw, notes it's still below threshold, and proposes no action — a normal outcome during quiet periods.

**Massive backlog.** If reflect hasn't run in months and the inbox is huge, os-tune surfaces the entry count and offers a choice: start with the strongest few patterns, or run a full sweep.

**Pattern surfaces a deeper structural issue.** Sometimes the right action isn't make/extend/refine but a workspace-wide change (`AGENTS.md` update, new convention, etc.). Reflect flags these as *"surface to the user — not a os-tune-mode action"* and writes them to inbox for the user to handle directly.

## See also

- `close-out` — the end-of-session partner that feeds inbox.md
- the os-skillify handoff, `extend`, `refine` — the modes reflect routes to when a pattern is acted on
- `references/inheritance-protocol.md` — inbox + skill-usage logs are core inheritance sources
- `../../_shared/references/skill-prompting-principles.md` — the lens reflect applies when scanning the library for principle-violation patterns
- `../../_shared/references/self-extending-skills.md` — the lens reflect applies when scanning for frozen-additive-skill patterns
- `AGENTS.md` — the workspace conventions reflect operates inside
