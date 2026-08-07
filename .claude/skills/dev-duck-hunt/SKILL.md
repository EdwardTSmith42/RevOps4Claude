---
name: dev-duck-hunt
description: >-
  Recurring autonomous bug hunt for a branch / feature / scoped code surface.
  Runs one hunt cycle immediately, then schedules recurring passes via the
  harness's recurring-task primitive until stop conditions hit (default 12-hour window, 5 consecutive
  empty passes, or user says stop), tracking what's been tried so it doesn't
  repeat itself. A thin wrapper around `dev-investigate recurring-hunt` (the
  per-cycle workflow lives there); this skill bootstraps scope, history, and
  scheduling. Triggers on "turn on Duck Hunt", "start the duck hunt loop", "Duck
  Hunt this branch", "begin the recurring bug sweep", "Duck Hunt for the next 12
  hours". Do NOT trigger for one-pass code review (use `dev-review` or
  `dev-investigate latent-hunt`) or for investigation of a specific reported bug
  (use `dev-investigate evidence`).
version: 0.1.0
category: Troubleshooting
source-prompts:
  - duck-hunt.md
display_name: Duck Hunt
tagline: Recurring autonomous bug hunt — runs until it stops finding things.
packs:
  - dev-pack
icon: 'phosphor:Crosshair'
when_to_use: >-
  Run one hunt cycle immediately, then schedule recurring passes via your
  harness's recurring-task primitive until stop conditions hit (default 12-hour window OR 5 consecutive empty
  passes OR you say stop). Tracks what's been tried across sessions in a
  persistent history doc so it doesn't repeat itself. Sub-agent fanout per cycle
  covers multiple defect families in parallel.


  Thin wrapper around `dev-investigate recurring-hunt`; this skill bootstraps
  scope + history + scheduling.
---

# Duck Hunt

## Purpose

A recurring autonomous bug-hunt workflow. One-shot bootstrap that:

1. **Detects target scope** (branch / feature / explicit slice).
2. **Loads cross-session history** from the configured notes path (Claude Code default: `~/.claude/notes/duck-hunt/<repo>/<branch>/history.md`) so this run doesn't re-try methods already tried + cold.
3. **Sets up `/loop` scheduling** with sensible defaults (30-min cycles, 12-hour stop, 5-empty-pass auto-stop — all tunable).
4. **Runs the first cycle immediately** so the user sees signal before walking away.
5. **Delegates per-cycle work** to `dev-investigate recurring-hunt` (the per-cycle workflow lives there — single source of truth).

Each cycle uses sub-agent fanout (2-3 disjoint defect families in parallel) and routes FIX_NOW fixes through an independent second-opinion pass before they commit — a fresh-context subagent by default, or a separate coding tool if you've wired one up. Keep it light for routine passes; go deeper for severe FIX_NOW.

## First-time setup

This skill assumes a few things about your environment:

- **A `/loop` slash command** (or equivalent recurring-task primitive in your harness) that can schedule a slash command on an interval. The default invocation here is `/loop 30m /dev-investigate recurring-hunt`. If your harness uses a different scheduling primitive (cron, launchd, `ScheduleWakeup`, an MCP scheduled-tasks server), substitute it in step 4 of Run and in the `Stop conditions` section.
- **Write access to a notes directory** for the persistent history doc — Claude Code's default is `~/.claude/notes/duck-hunt/`; on other harnesses, substitute your harness's notes/state directory. The directory is created on first run. (The `~/.claude/notes/...` paths elsewhere in this skill all use the Claude Code default.)
- **`dev-investigate`, `dev-fresh-eyes`, and `dev-scope-deferral` installed** — this skill delegates to all three.

Remove or supersede this section once your harness's loop primitive is wired and the history-doc directory exists.

## When to use

- "Turn on Duck Hunt" / "start the duck hunt loop" / "Duck Hunt this branch."
- "Begin the recurring bug sweep" / "autonomous low-risk fix loop" / "megabranch hardening in chunks."
- "Run Duck Hunt overnight" / "Duck Hunt for the next 12 hours."

Do NOT use for:
- **One-pass code review** → `dev-review` or `dev-investigate latent-hunt`.
- **Bug investigation** triggered by a specific report → `dev-investigate evidence`.
- **Ship-readiness check** on a single PR → `dev-review ship-gate`.

## Run (activation, first cycle only)

### 1. Detect target scope

- If the user names a feature / directory / route / subsystem, use that.
- Otherwise default to the **current branch diff against `origin/develop`**.
- Fallbacks: tracked branch, `origin/main`, merge-base-backed diff.
- Capture: `repo`, `branch`, `base-ref`, optional `slice` (subdirectory or explicit file list).

### 2. Bootstrap the history doc

Path: `~/.claude/notes/duck-hunt/<repo-slug>/<branch-slug>/history.md`

- If the file doesn't exist, create it from `../dev-investigate/references/history-format.md` schema.
- If it exists, **read it** before scheduling — surface a one-line summary to the user: "Resuming Duck Hunt on `<branch>`. Prior runs: <N>. Cold zones: <list>. Pending suspicions: <list>."

For richer cross-session context (when prior session transcripts may have non-canonicalized findings): if your harness exposes a session-transcript search capability (e.g. a session-management MCP), search prior transcripts for "duck-hunt" + repo/branch slugs. If it doesn't, skip — history.md is the canonical record and the loop works fine without this.

### 3. Check for an existing active session

If another Duck Hunt is already active for the same repo+branch (recent `Pass state: running` in the history doc with a non-stale lock), reuse it rather than starting a parallel hunt.

### 4. Set up `/loop` scheduling

Recommend the user invoke (or invoke directly via your harness's skill-invocation mechanism):

```
/loop 30m /dev-investigate recurring-hunt
```

The mode body in `dev-investigate recurring-hunt` handles per-cycle behavior (lock + claim + classify + triage + execute + release).

### 5. Run one cycle immediately

Don't wait for the first scheduled wake-up. Invoke `dev-investigate recurring-hunt` once **inline** so the user sees signal in the current session.

## Stop conditions (delegated to /loop + per-cycle self-check)

- **Session expired** — default 12 hours from start (configurable via the history doc).
- **Five consecutive empty passes** — default; tunable.
- **User says stop** — manual stop; closeout via `recurring-hunt` mode.

When stop conditions hit, the loop is cancelled. **Do not keep emitting wake-ups** for an expired session.

## Cross-session repeat-avoidance

The history doc at `~/.claude/notes/duck-hunt/<repo>/<branch>/history.md` is the canonical anti-repeat record. Each cycle:

- **Reads the doc before picking a method** — skip methods already tried + still cold within the freshness window (default: 7 days).
- **Appends to the doc after each pass** — methods used, slice covered, findings classification, terminal triage states.
- **Maintains "cold zones" and "hot zones"** lists for fast lookups.
- **Flags branch advancement** — when the branch HEAD moves past a previously-hunted commit, mark new commits as un-hunted and prioritize them.

See `../dev-investigate/references/history-format.md` for the schema.

## Sub-agent fanout per cycle

Each cycle picks **one target slice**. On that slice, by default it spawns **2-3 disjoint subagents** covering different defect families in parallel (no subagent support in your harness? run the same defect-family lenses as sequential passes over the slice):

- One on async / state / timing.
- One on contract drift / schema mismatch / data shape.
- One on cache / SWR / stale state.

Or, when slice is small enough that fanout overhead exceeds benefit, fall back to single-method-per-cycle.

The per-cycle workflow in `dev-investigate recurring-hunt` includes this fanout step. Parent reconciles findings into one classified list before triaging.

## Auto-challenger — an independent second-opinion pass

Each FIX_NOW commit auto-routes through an independent second pass before it lands:

- **By default**, spawn a fresh-context subagent with the diff + recent commit and a disjoint review focus — it catches the tunnel-vision mistakes the fixing agent can't see in itself.
- **If you've wired up a separate coding tool** (another CLI or model), route to it instead for genuine cross-model divergence.
- **No second agent available in your harness** — re-review the diff yourself in a fresh pass with a deliberately different focus before landing it.
- **Low-risk fixes** can skip the challenger entirely if `--no-challenger` is set.

The challenger reads the diff + recent commit; reports findings; the mode reconciles and decides whether to proceed or down-classify.

## Hard rules (carry-forward from `dev-investigate recurring-hunt`)

- **Never open or merge pull requests.**
- **Never sweep unrelated user work into a Duck Hunt commit.** No `git add -A`. No `git commit -a`.
- **If a fix can't be cleanly isolated, downgrade** to `HUMAN_DECISION` or `DEFER`.
- **Generated artifacts excluded by default** (swagger.json, sdk.msw.ts, lockfiles).
- **Anti-zombie**: when the loop hits its empty-pass threshold or session timeout, kill the loop. Don't keep emitting "session expired" wake-ups.
- **All logs private and local** — never sync to a project-tracker, support-system, or team-chat surface without explicit user request.
- **Never make UI/UX changes, risky behavior changes, or architecture changes** in this loop. Defer them via `dev-scope-deferral`.

## Design Rationale

- **Thin wrapper, single source of truth.** The per-cycle workflow stays in `dev-investigate recurring-hunt`. This skill exists for the cleaner trigger surface ("turn on Duck Hunt") + activation bootstrap. Avoids duplication.
- **Cross-session history doc** addresses the central anti-repeat concern: a recurring loop that re-tries the same methods on the same areas wastes cycles and erodes trust. The history doc persists across runs, sessions, worktrees, and machine restarts, so each cycle starts from the cumulative record rather than a blank slate.
- **Sub-agent fanout per cycle.** Different defect families (async/state, contract drift, cache/SWR) are genuinely parallelizable. Covering 2-3 in one cycle compresses wall-clock time versus covering them across sequential cycles. Single-method fallback when slice is too small to amortize the fanout overhead.
- **Auto-challenger — an independent second pass.** Each FIX_NOW fix gets a second opinion before it commits: a fresh-context subagent by default, or a separate coding tool if you've wired one up. Catches the tunnel-vision mistakes the fixing agent can't see in itself.
- **`/loop` is the assumed cadence primitive.** Other primitives (`ScheduleWakeup`, `CronCreate`, MCP scheduled-tasks servers, native cron/launchd) are viable substitutes — the skill's behavior doesn't depend on `/loop` specifically, only on *something* that can wake it on an interval.

## References

- `../dev-investigate/references/history-format.md` — schema for the cross-session history doc.

## Related skills

- **`dev-investigate recurring-hunt`** — per-cycle workflow (lock, classify, triage, fix, release). Single source of truth for the per-cycle craft.
- **`/loop`** — cadence delegation. Default `30m`; tunable.
- **`dev-fresh-eyes`** — invoked in Fix Flow step 2 (plan pressure-test).
- **`dev-scope-deferral`** — invoked for `DEFER` items (writes deferred-investigation note).
- **Your bug-comms workflow** (if you have one for posting bug status to a tracker / chat / support-system) — explicitly **not** invoked from this loop. Duck Hunt runs as Local Investigation Mode; cross-system status posting stays a separate, deliberate human-initiated step.
- **Session-transcript search** (whatever capability your harness offers, if any) — optional cross-session richer context when prior sessions have content not yet canonicalized in history.md.
