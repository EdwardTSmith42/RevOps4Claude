---
name: dev-stale-worktree-curator
description: >-
  Audit git worktrees older than a chosen age, classify which are safe to remove
  / need a push first / contain only discardable churn. Operate safest-first;
  pause on ambiguous cases. Use when disk space is tight, Docker cannot start
  because of storage pressure, or you want a repeatable workflow for preserving
  important local work before removing stale worktrees. Good fit for a weekly
  cron. Do NOT trigger for clean-up of the current single worktree (use
  `dev-clean-up`). Do NOT trigger for arbitrary file deletion outside the
  worktree audit context.
version: 0.2.0
source-prompts:
  - stale-worktree-curator.md
display_name: Stale Worktree Curator
tagline: Audit aging worktrees — safe to remove vs needs-push vs discardable.
category: Planning
packs: [dev-pack]
icon: 'phosphor:Tree'
when_to_use: >-
  Audit git worktrees older than a chosen age. Classifies which are safe to
  remove, which need a push first, which contain only discardable churn.
  Operates safest-first; pauses on ambiguous cases.

  Use when disk space is tight, Docker won't start because of storage pressure,
  or you want a repeatable workflow before removing stale worktrees. Good fit
  for a weekly cron.
---

# Stale Worktree Curator

## Purpose

Review old git worktrees without losing important work. Produce a stale-worktree report first, then work safest-first: remove clean remote-backed trees, push recoverable local commits, discard low-value generated churn only when the branch is already backed by remote, and stop for human judgment on ambiguous cases.

Designed for periodic (e.g., weekly cron) sweeps when disk pressure or general worktree hygiene calls for it.

## Workflow

### 1. Audit stale worktrees

```bash
# List all worktrees with metadata
git worktree list --porcelain

# For each worktree, determine age (modified time of the worktree directory)
find <worktree-path> -maxdepth 0 -mtime +7  # >7 days old

# For each, gather:
# - branch / detached state
# - upstream tracking
# - dirty status
# - ahead/behind counts vs upstream
git -C <worktree-path> status --short
git -C <worktree-path> rev-parse --abbrev-ref HEAD
git -C <worktree-path> rev-parse --abbrev-ref @{u} 2>/dev/null
git -C <worktree-path> rev-list --left-right --count @...@{u} 2>/dev/null
```

Optionally estimate disk usage: `du -sh <worktree-path>`.

### 2. Identify protected worktrees (live agent sessions + Docker bind mounts)

Before removing anything, identify worktrees referenced by **live agent sessions** and treat them as protected. If you run multiple long-lived agent sessions across worktrees (Claude Code, Codex, Cursor, etc.), check whichever directory your harness writes session metadata to and extract the recent `cwd` values:

```bash
# Example: Claude Code stores session metadata under ~/.claude/projects/
ls ~/.claude/projects/
# Extract cwd from each session file; any worktree path matching = in-use
```

Adapt the path to your harness, or skip the step if you don't run concurrent agent sessions across worktrees.

Any matching worktree path should be **treated as in-use unless the user explicitly says otherwise.** Open sessions often mean the user intends to come back.

Then identify worktrees that **Docker containers bind-mount from** — these are BLOCKED, never auto-removable. A container's data can live *inside* a worktree (e.g., a compose project started from that worktree bind-mounting a data directory as its database volume); pruning the worktree deletes live database files out from under the container:

```bash
# Every container (live AND stopped) — stopped containers still own their data
docker ps -a --format '{{.ID}}'

# For each, check bind-mount Sources against every candidate worktree path
docker inspect <id> --format '{{json .Mounts}}' | \
  python3 -c "import json,sys; print('\n'.join(m['Source'] for m in json.load(sys.stdin) if m['Type']=='bind'))"
```

If any Source falls under a candidate worktree path, classify that worktree `blocked_docker_bind`. If the Docker daemon is not running, treat Docker-backed status as **unknown** — check heuristically for container-data directories (a `docker/data/`-style path is the common shape) and pause rather than assume safe.

### 3. Classify each stale worktree into an action bucket

- **`remove_safe`** — clean, remote-backed, and not ahead of upstream. Safe to remove now.
- **`remove_keep_local_branch`** — clean branch whose committed work is preserved by the local branch ref, even if it has no upstream or is ahead/diverged. Worktree removable; branch ref preserves the work.
- **`discard_generated_then_remove`** — dirty only because of known generated churn, with no unique local commits that would be lost. Discard churn → remove.
- **`discard_generated_then_remove_keep_local_branch`** — dirty only because of known generated churn, but committed work preserved by local branch ref. Same as above + keep branch ref.
- **`push_then_remove`** — local commits look recoverable and should be pushed before cleanup. Push → then remove.
- **`needs_review`** — detached, no upstream, divergent, or dirty in substantive files. **Pause and ask the user.**
- **`blocked_docker_bind`** — a container (live or stopped) bind-mounts from inside this worktree. **Never auto-remove.** Surface it to the user with the owning containers named, and suggest either relocating the compose project to the canonical checkout or tearing the containers down first.
- **`prune_metadata`** — Git still has stale worktree metadata for a missing path. Just `git worktree prune`.

### 4. Operate in this order (safest-first)

1. Clear `prune_metadata` items.
2. Remove `remove_safe`.
3. Inspect `discard_generated_then_remove`.
4. Inspect `remove_keep_local_branch` and `discard_generated_then_remove_keep_local_branch`.
5. Push `push_then_remove`.
6. **Pause on `needs_review`.**

### 5. Re-check disk pressure after each batch

After each batch, re-check free disk and **stop once pressure is relieved.** Do not keep deleting old worktrees just because the workflow can.

```bash
df -h .
```

### 6. (Optional) Docker janitor for additional pressure

If Docker storage is the main pressure source after worktree cleanup:

```bash
# Report mode (dry-run) first
docker images --format json | <classifier>

# Apply only after reviewing:
# Remove only stale unused local/custom images and dangling images.
# Keep warm base + active compose images.
# Do NOT auto-prune Docker volumes or build cache (those should stay opt-in).
```

## Generated churn allowlist

The principle: only paths that are deterministically regenerated from committed source count as churn. A path qualifies if rebuilding from a clean checkout reproduces it byte-for-byte (or close enough that the diff has no review value). Anything else — even if it *looks* generated — is review-required.

Common churn paths in JS/TS repos that usually qualify:

- Build output directories (`dist/`, `build/`, `coverage/`, `.turbo/`, `.next/`, similar framework caches)
- Dependency directories (`node_modules/`)
- Compiler artifacts (`*.tsbuildinfo`)
- Generated API client / SDK / OpenAPI files written from a single source spec (e.g., a generated routes file, a generated `swagger.json`, a generated SDK package source tree)
- Editor / tooling scratch directories the repo doesn't track meaningfully

Per-repo additions go alongside these — the allowlist is **intentionally conservative** and adapted per project. Add a path only after confirming a clean rebuild reproduces it, and never add migrations, lockfiles, prompt files, or anything else where a stray dirty file could represent real intent.

## Review commands

Inspect a worktree before taking action:

```bash
git -C /path/to/worktree status --short
git -C /path/to/worktree diff --stat
git -C /path/to/worktree log --oneline --decorate -n 5
```

Review local-only commits before pushing:

```bash
git -C /path/to/worktree log --oneline --decorate <upstream_branch>..HEAD
```

Push a recoverable branch:

```bash
git -C /path/to/worktree push -u origin <branch_name>
```

Remove a safe worktree and prune stale metadata:

```bash
git -C /absolute/path/to/repo worktree remove /path/to/worktree
git -C /absolute/path/to/repo worktree prune
```

## When to stop and ask

Stop and ask the user when any of these are true:

- The worktree is detached and not obviously disposable.
- The branch has no upstream and the local commits are not trivial.
- The branch diverged from upstream.
- Dirty files include substantive source, docs, prompts, migrations, or configs.
- The cleanup choice depends on product judgment rather than repo hygiene.

## Hard rules

- **Never use `git worktree remove --force`** unless the worktree is already backed up or the user explicitly accepts the risk.
- **Never assume detached work is disposable.** A detached worktree with unique commits is a review case, not a cleanup case.
- **Treat generated churn as a narrow allowlist, not a vibe.** If even one dirty file falls outside the allowlist, the worktree is not auto-discardable.
- **Do not auto-discard migrations, published flow artifacts, prompt files, or lockfiles** just because they were generated once. Review them.
- **If a branch has no upstream or is ahead/diverged from upstream, preserve it first** by pushing it or creating a local backup branch/tag before considering removal.
- **A clean or committed-only branch can still be removed safely if keeping the local branch ref is acceptable.** Removing the worktree does not delete the branch or its commits.
- **Treat any worktree path referenced by a live agent session as protected by default.**
- **Never remove a worktree that any Docker container (live or stopped) bind-mounts from.** Check `docker ps -a` + `docker inspect .Mounts` before classifying anything safe-to-remove; if the daemon is down, a container-data directory in the worktree means pause, not proceed.
- **A worktree carrying more than a trivial amount of container data (rule of thumb: a data directory over ~10MB) is pause-and-ask, never auto-prune** — even when git state looks clean. Database files are invisible to git status.
- **Prefer `git worktree remove <path>` over raw filesystem deletion.** Use `git worktree prune` afterward to clean stale metadata.
- **For Docker cleanup, default to a dry run first.**
- **Keep warm base images and active compose images.** The Docker janitor is intentionally scoped to stale local/custom images and dangling images, not general cache pruning.
- **Do not auto-prune Docker volumes or build cache** as part of routine cleanup.

## Design Rationale

Why this skill is structured the way it is:

- **The 8-state action bucket vocabulary is the highest-leverage content.** The distinctions (`remove_safe` vs `remove_keep_local_branch` vs `discard_generated_then_remove`) capture real safety-relevant differences that flat "safe to remove" classification would miss.
- **Safest-first ordering** — clear metadata first; remove safest items; inspect ambiguous; push recoverable; pause on review-required. Reduces blast radius if a misclassification occurs partway through.
- **"Treat generated churn as a narrow allowlist, not a vibe"** — anti-vibe rule. The allowlist is explicit and conservative.
- **"Live agent-session worktrees protected by default"** — anti-deletion-of-active-work rule: never propose removing a worktree an active session (any harness) is working in.
- **"A clean or committed-only branch can still be removed safely if keeping the local branch ref is acceptable"** — specific safety distinction (worktree removal ≠ branch deletion).
- **Docker janitor narrowly scoped** — to stale local/custom images and dangling images. Volumes and build cache stay opt-in because they're more likely to hide useful local state.
- **The Docker bind-mount block exists because of a real data-loss incident (2026-06-10):** a prune removed a worktree while a compose project bind-mounted its data directory as Postgres data dirs. The live local databases were deleted out from under the running containers and were unrecoverable after the next reboot (crash-loop on a corrupted lock file). Git-state checks can never catch this — DB data dirs are gitignored, so the worktree looked clean.

## First-time setup

This skill assumes:

- **git** with worktree support (any modern version).
- Standard POSIX shell tooling (`find`, `du`, `df`).
- For the live-session protection step: a known location where your agent harness writes per-session metadata that includes a `cwd`. The example uses Claude Code's `~/.claude/projects/`; adapt the path to your harness (Codex, Cursor, etc.) or skip the step if you don't run multiple long-lived agent sessions across worktrees.
- For the optional Docker janitor: a working `docker` CLI.

No persistent configuration. The generated-churn allowlist is per-repo and lives in this file; tune it for the project you're sweeping after confirming each path rebuilds cleanly.

## Related skills

- `dev-clean-up` — for cleanup of the *current single worktree* (churn / runtime-only / full-reset). Distinct skill.
