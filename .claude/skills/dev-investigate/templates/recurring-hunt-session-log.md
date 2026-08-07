# Recurring-hunt session log

Strict template for `recurring-hunt` mode of `dev-investigate`. Tracks the per-cycle state of an autonomous bug-hunt loop.

```markdown
# Recurring Hunt: <branch> @ <repo-slug>

**Session start:** <UTC timestamp>
**Session stop time:** <UTC timestamp = start + 12h default>
**Empty-pass threshold:** 5 (default; tunable)
**Target scope:** <feature / dir / route / "current branch diff against origin/develop">
**Diff base:** <`origin/<branch>` / `origin/main` / merge-base>

## Session state

- **Pass state:** `idle` | `running`
- **Pass trigger:** `immediate` | `scheduled` | `manual`
- **Pass started at:** <UTC timestamp>
- **Lock expires at:** <UTC timestamp = pass-start + 60min default>
- **Last reviewed commit:** <SHA>
- **Last updated:** <UTC timestamp>
- **Consecutive empty passes:** 0
- **Loop primitive:** `/loop 30m /dev-investigate recurring-hunt` (or as configured)

## Initial hunt queue

- <slice / file cluster / area>
- <slice / file cluster / area>

## Pass history

### Pass 1 — <UTC timestamp>

- **Slice:** <chosen target>
- **Method:** <hunt method from menu>
- **Findings:**
  - <finding> — `confirmed` / `likely` / `unclear` / `dismissed`
- **Triage:**
  - <finding> → `FIX_NOW` / `HUMAN_DECISION` / `DEFER` / `DISMISSED`
- **Fixes landed:**
  - <plain-language summary> — commit `<SHA>`
  - Files staged: <list>
  - Generated churn included: <none / explicit list>
  - Validation commands: <list>
  - Residual risk: <note>
- **Deferred items:**
  - <item> → invoked `dev-scope-deferral`, note at `<notes-root>/investigations/<date>-<slug>.md`
- **Local investigations:**
  - <item> — see investigation block below
- **Pass result:** <new findings produced / empty pass>
- **Lock released at:** <UTC>

### Pass 2 — ...

## Local investigations (in-session)

### <slug>

- **Hypothesis:** <statement> [confidence]
- **Observed facts:** <list>
- **What this cannot be:** <list — because of specific clues>
- **Unknowns:** <list>
- **Next verification step:** <executable>

## Stop state

- **Reason:** `time_elapsed` | `5_empty_passes` | `manual_stop` | `still_active`
- **Closeout summary:** <plain-language>
- **Heartbeat / loop:** deleted at <UTC> | still active

## Notes

- **Logs are private and local. Do not commit.**
- **Generated SDKs, swagger.json, sdk.msw.ts, lockfiles excluded by default.**
- **Sandbox-safe path:** if the canonical session log path is read-only, use a workspace-safe shadow path (e.g. `.local/recurring-hunt/`).
- **Never use `git add -A` / `git commit -a` for fixes from this loop.**
```

## Used by

- `recurring-hunt` mode of `dev-investigate`.
