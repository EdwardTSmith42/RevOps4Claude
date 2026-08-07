---
name: dev-clean-up
description: >-
  Explicit cleanup workflows in three modes — (1) `churn` cleanup that removes
  generated/out-of-scope diff noise while keeping the current branch/worktree
  intact, (2) `runtime-only` shutdown for the current worktree, or (3)
  `full-reset` back to a clean detached checkout at a base ref like
  `origin/main`. Triggers on "clean up churn", "remove generated files from
  the diff", "drop swagger/sdk noise", "shut down this worktree", "stop the
  local env here", "clean up this worktree", "bring me back to main for the
  next project", "reset this lane for the next project". Choose the mode from
  the exact phrasing — do NOT treat generic cleanup language as automatic full
  reset. Do NOT trigger for stale-worktree audits across many worktrees (use
  `dev-stale-worktree-curator`). Do NOT trigger for bug-fix cleanup (those are
  part of `dev-investigate` or `dev-review checkpoint`).
version: 0.1.0
display_name: Clean Up
tagline: 'Cleanup workflows — churn, runtime-only shutdown, full-reset.'
category: Planning
packs:
  - dev-pack
icon: 'phosphor:Eraser'
when_to_use: >-
  Reach for this when a workspace needs tidying — clearing generated noise out of a diff,
  shutting down a worktree's local environment, or resetting a lane back to a clean base for
  the next project.

  Three modes — `churn` (remove generated/out-of-scope diff noise while keeping
  the current branch/worktree intact), `runtime-only` (shutdown for the current
  worktree), `full-reset` (back to a clean detached checkout at a base ref).
  Choose by exact phrasing — generic 'cleanup' language doesn't auto-trigger
  full-reset.
modes:
  - name: churn
    job: >-
      Remove generated / out-of-scope diff noise while keeping the worktree
      intact.
  - name: runtime-only
    job: Shutdown for the current worktree only.
  - name: full-reset
    job: Back to a clean detached checkout at a base ref.
---

# Clean Up

## Purpose

Three explicit cleanup modes for the current worktree, picked from the user's exact phrasing. Manually triggered when the user knows it's time to clean up — not invoked by automation.

## First-time setup

This skill assumes:

- A `git` working tree (worktrees encouraged but not required).
- A known base ref to reset against (commonly `origin/main` or `origin/develop` — confirm with the user the first time `full-reset` is invoked, then carry the choice forward in conversation).
- Local dev servers / runtimes startable and stoppable from the worktree (the skill identifies and stops the ones it can prove ownership of).

If the project uses a custom local-runtime tool (e.g., a wrapper that knows which worktree owns which shared services), name it in the per-context profile so the agent runs `<tool> status` during inspection instead of guessing from PIDs. Without that, `runtime-only` falls back to inspecting `package.json` scripts and targeted PID kills.

## Mode mapping (phrase-driven)

- **`clean up churn`** / `drop generated files from this diff` / `remove swagger/sdk noise` / `keep this branch` → mode `churn`
- **`shut down this worktree`** / `stop the local env here` / `leave the branch alone but stop the runtime` → mode `runtime-only`
- **`clean up this worktree`** / `bring me back to main` / `reset this lane for the next project` → mode `full-reset`

If the user says only `clean up` and the intended scope is unclear, **inspect first and restate the mode you are taking before executing.**

## Workflow

### 1. Inspect before mutating

```bash
git status --short --branch
git rev-parse --show-toplevel
git ls-files --others --exclude-standard --directory --no-empty-directory
```

If the project has a local-runtime ownership tool configured (see First-time setup), also run its status command to learn which services this worktree owns.

If untracked directories will be deleted by the chosen mode, **inspect them before executing cleanup.** Treat repo-local tool state such as `.factory/`, `.local/`, agent-scratch dirs, etc. as something to classify, not blind trash:

```bash
ls -la .factory  # or other untracked dirs
find .factory -maxdepth 2 -print | head -n 50
```

Classify each untracked workspace folder:
- **Disposable** temp/cache/log/runtime state → safe to delete.
- **Durable tool state** that belongs in a global home → move it there first if appropriate.
- **Locally useful scratch state** that should survive cleanup → preserve and exclude from this pass.

When you move or delete untracked folders, **explain briefly why.**

### 2. Confirm mode

Restate the mode before executing. If ambiguous, ask the user.

### 3. Execute the chosen mode

#### `churn` — remove generated/out-of-scope diff noise; keep branch

Identify generated files in the current diff (typical patterns: `swagger.json`, generated SDK / mock files, lockfiles when not intentionally changed, build artifacts, generated type files).

```bash
# For tracked-but-modified generated files:
git checkout -- <generated-files>

# For untracked generated files:
rm <untracked-generated-files>  # only after inspecting

# Then verify:
git status --short
```

Goal: targeted generated/out-of-scope files clean; current branch unchanged.

#### `runtime-only` — stop repo-local runtime; keep branch

Stop development servers / processes owned by this worktree. **Never use broad port-kill or repo-wide kill patterns** in a project with shared backend services — kill cascades to other worktrees. Inspect ownership first.

When a local-runtime ownership tool is configured: ask it which services this worktree owns, then stop only those.

Otherwise: identify dev/server PIDs from `package.json` scripts (or the equivalent in the project's stack), confirm they belong to this worktree, kill targeted PIDs.

**If the current worktree owns shared services that other worktrees depend on, stop and surface that clearly instead of killing them.** Shared-service handoff is a human or separate-lane decision.

Goal: app client/server ports not owned by the cleaned worktree; current branch unchanged.

#### `full-reset` — discard local state; clean detached checkout at base

**Requires explicit user authorization.** Only run when the user has clearly asked to discard local changes.

```bash
# Confirm baseline (e.g. origin/main or origin/develop — see First-time setup)
git fetch origin --prune

# Verify worktree state is acceptable to discard
git status --short

# Discard local changes + reset to detached HEAD at the base ref
git checkout --detach origin/<base>
git clean -fdx  # remove untracked files (be CAREFUL — re-inspect first)
```

Goal: working tree clean, `HEAD` detached at `origin/<base>`.

### 4. Verify

```bash
git status --short --branch
```

For `full-reset`, also verify:
```bash
git symbolic-ref --short -q HEAD || echo detached
git rev-list --left-right --count origin/<base>...HEAD
```

For `runtime-only` or `full-reset` when a local-runtime ownership tool is configured, also re-run its status command to confirm the expected services stopped.

Expected results:
- **`churn`:** targeted generated/out-of-scope files clean; current branch unchanged.
- **`runtime-only`:** runtime owned by this worktree stopped; current branch unchanged.
- **`full-reset`:** working tree clean; `HEAD` detached at `origin/<base>`.
- **Shared services:** untouched unless the user explicitly chose a different path outside this skill.

## Hard rules

- **Treat requests like `clean up churn` as authorization only for churn cleanup,** not runtime shutdown or branch reset.
- **Treat requests like `clean up this worktree` / `reset me for the next project` / `bring me back to main` as authorization to discard local worktree state.**
- **Do not use `full-reset` for churn cleanup.**
- **If the user has not clearly asked to discard local changes, do not run `git clean -fdx` or `git checkout --detach`.**
- **Before any cleanup that will remove untracked directories, inspect the directories first** and decide whether they are disposable, should be folded into a global tool home, or should be preserved locally.
- **If you delete or move untracked workspace folders, include a short rationale in your response.**
- **In projects with shared backend services, never use broad port-kill or repo-wide kill patterns.** Let inspection-first discipline determine ownership.
- **If the current worktree owns shared services that other worktrees depend on, stop and surface that clearly instead of killing them.**
- **`runtime-only` and `churn` should preserve the current branch.**

## Design Rationale

Why this skill is structured the way it is:

- **Phrase-driven mode selection** — the user's exact phrasing maps to one of three intentional modes. "Clean up churn" ≠ "clean up worktree." Ambiguous phrasing forces inspection + restatement before executing. This anti-overreach discipline is hard-won; cleanup operations are irreversible enough that one wrong mode call can erase hours of work.
- **Inspect before you mutate, always** — untracked workspace folders often hold durable tool state (agent scratch dirs, local config, in-progress notes) that shouldn't be blindly deleted. The classification step (disposable / durable / scratch) prevents data loss.
- **Shared-service ownership rule** — in multi-worktree setups where one worktree runs a backend service the others depend on, stopping that runtime cascades. Surface the ownership conflict; don't kill silently.
- **`full-reset` requires explicit authorization** — discarding local state is irreversible. The phrasing trigger ("bring me back to main", "reset this lane") is the explicit ask; without it, default to non-destructive modes.
- **Manually triggered, not automated** — the user invokes when they're ready. No automation should call this skill.

## Related skills

- `dev-stale-worktree-curator` — for periodic (e.g., weekly) sweeps across many worktrees. Distinct skill, distinct trigger pattern.
- `dev-review checkpoint` — milestone cleanup loops integrate cleanup discipline (post-decomposition cleanup audit) but happen mid-development; this skill is specifically for "I'm done now."
