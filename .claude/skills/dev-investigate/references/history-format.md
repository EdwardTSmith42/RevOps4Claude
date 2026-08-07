# Duck Hunt history doc format

Schema for the cross-session history doc that prevents Duck Hunt from repeating itself.

## File location

`<notes-root>/duck-hunt/<repo-slug>/<branch-slug>/history.md` — `<notes-root>` is your harness's notes/state directory (Claude Code default: `~/.claude/notes/`).

- `<repo-slug>` = lowercased + hyphenated repo name (e.g., `my-app` for `My-App`).
- `<branch-slug>` = lowercased + slash-replaced branch name (e.g., `feature--auth-fix` for `feature/auth-fix`).

One file per repo+branch combo. Append-only. Survives sessions, worktrees, machine restarts.

## File template

```markdown
# Duck Hunt history — <repo> / <branch>

**Created:** <ISO timestamp>
**Last updated:** <ISO timestamp>
**Diff base:** origin/develop (or as detected)
**Total cycles run:** <count>
**Total FIX_NOW commits:** <count>

## Active session (if running)

- **Pass state:** idle | running
- **Pass started at:** <ts>
- **Lock expires at:** <ts>
- **Consecutive empty passes:** <count>
- **Stop conditions:** <session timeout> / <empty-pass threshold>

## Cold zones (don't re-hunt soon)

Areas / methods covered with no findings within the freshness window (default 7 days):

- `<file-or-area>` — covered by `<method>` on `<date>` — no findings — freshness expires `<date+7d>`
- ...

## Hot zones (have credible suspicions)

Areas where past cycles surfaced suspicions that were `unclear` or `confirmed` but not yet terminal:

- `<file-or-area>` — last cycle: `<date>` — note: `<one-line>` — next method to try: `<method>`
- ...

## Pending hunt queue

Slices / files queued for upcoming cycles (FIFO):

- [ ] `<slice>` — added `<date>` — reason: `<one-line>`
- ...

## Per-cycle log (most recent first)

### Cycle <N> — <ISO ts>

- **Trigger:** scheduled | manual | immediate
- **Slice:** `<file-or-area>`
- **Methods used:** `<method>` (and others if fanout)
- **Subagents fanout:** `<async-state>` / `<contract-drift>` / `<cache-swr>` (or `single-method` if no fanout)
- **Findings classification:** `<n>` confirmed / `<n>` likely / `<n>` unclear / `<n>` dismissed
- **Triage outcomes:**
  - **FIX_NOW:** `<n>` — commits: `<sha1>`, `<sha2>`
  - **HUMAN_DECISION:** `<n>` — see notes: `<list>`
  - **DEFER:** `<n>` — scope-deferral notes: `<paths>`
  - **DISMISSED:** `<n>`
- **Challenger lane invoked:** `<tool>` (or `none`)
- **Validation commands:** `<commands>` — pass/fail
- **Empty pass:** yes | no
- **Notes:** `<one-line plain-language summary>`

### Cycle <N-1> — ...

(Append per cycle. Most recent first.)

## Branch advancement events

When the branch HEAD moves past a previously-hunted commit:

- `<date>` — HEAD advanced from `<old-sha>` to `<new-sha>`. Commits added: `<list>`. Marked as un-hunted, prioritized for next cycle.

## Stop record (when loop ends)

- **Stopped at:** <ISO ts>
- **Reason:** session expired | empty-pass threshold | manual stop
- **Total cycles:** <count>
- **Total FIX_NOW landed:** <count>
- **Final summary:** <one-line>
```

## Read protocol (each cycle, before picking a method)

1. Open the history doc (create from template if absent).
2. Update `Last updated` timestamp.
3. Read the **Cold zones** list — don't re-hunt those (within freshness window).
4. Read the **Hot zones** list — these are priority candidates for revisiting with a different method.
5. Read the **Pending hunt queue** — pull the next item if applicable.
6. Read the most recent cycle entry — what method was last used, on what slice. Rotate methods.

## Write protocol (each cycle, after work completes)

1. Append a new cycle entry under "Per-cycle log."
2. Update `Cold zones` if the cycle covered an area with no findings.
3. Update `Hot zones` if findings surfaced.
4. Update `Pending hunt queue` (mark items done, add follow-ups).
5. Update top-level metadata (`Total cycles run`, `Total FIX_NOW commits`, `Last updated`).
6. If empty pass, increment `Consecutive empty passes`. If non-empty, reset to 0.

## Branch-advancement protocol

At the start of each cycle, check whether the branch HEAD has moved since the last cycle entry. If yes:

1. Add a "Branch advancement event" entry.
2. List newly-added commits.
3. Mark those commits as un-hunted (priority candidates).

## Cross-session integration

For richer context across multiple Duck Hunt sessions (especially when prior cycles weren't canonicalized in this doc):

If your harness exposes a session-transcript search capability (e.g. a session-management MCP), search prior transcripts for `"duck-hunt <repo-slug> <branch-slug>"` over roughly the last 30 days. If it doesn't, skip — this doc is the canonical record.

Surface relevant findings from prior sessions that may not be in this history.md (e.g., findings only logged to a session transcript that wasn't summarized into history). Use sparingly — the canonical record is history.md; transcript search is the safety net.

## Freshness window

**Default: 7 days.** A method-on-area entry in `Cold zones` expires after 7 days. After expiry, the area is fair game for re-hunting (the codebase may have changed; the method may be tuned differently).

Tunable by editing the `Stop conditions` section's `freshness-days: 7` field (when present).

## Schema versioning

This is v0.1. Future updates may add fields. Cycles should fail gracefully on unknown fields.

## Used by

- `dev-duck-hunt` SKILL.md (read at activation; bootstrap if absent).
- `dev-investigate recurring-hunt` mode (read pre-cycle; append post-cycle).
