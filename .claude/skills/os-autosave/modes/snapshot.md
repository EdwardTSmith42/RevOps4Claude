---
mode: snapshot
parent: os-autosave
---

# os-autosave / snapshot — pre-change tagged commit (os-tune only)

## What this mode does

Creates a tagged commit before os-tune applies a moderate or large change, so revert can target THIS specific change later — not just "last commit" or "yesterday's state."

This mode is called by os-tune only. The user doesn't invoke it directly.

## When this fires

os-tune's `refine` and `extend` modes call `snapshot` before applying any change classified as moderate or large per `os-tune/references/approval-tiers.md`. Trivial-tier changes commit only after applying — those don't need pre-snapshot navigation since they're reversible without targeted-snapshot tags.

## What `snapshot` does

1. **Verify pending changes are clean.** If there are uncommitted changes, run `commit` first to capture them under their own message. Then proceed.
2. **Create the snapshot commit** with a tagged message in the form `Snapshot: pre-<os-tune-mode> on <skill-name> — <one-line summary of incoming change>`. The summary describes what's about to happen in plain language, not what just happened. See `references/commit-message-format.md` for exact shape.
3. **Tag the commit** with a snapshot label so revert can find it: `snapshot/<YYYYMMDD-HHMM>-<skill>-<mode>`. Tags are searchable later.
4. **Sync to the online backup if one exists.** If the user has the optional backup on, push the snapshot up too; if not, the local snapshot is complete on its own.
5. **Return** the commit hash + tag to os-tune, which os-tune can reference if the user later asks to revert *this specific change*.

## Operating principles

- **Snapshots are paired with their change.** Every snapshot has a description of what's about to happen, so revert can describe the change in plain language naming the os-tune mode, the skill touched, and when.
- **os-tune-only invocation.** The user doesn't call snapshot directly. If a user wants a manual save point, they use `commit` with a custom message.
- **Snapshots don't replace the regular commit.** After os-tune's change applies successfully, a regular commit fires too (per `commit` mode). The snapshot is the BEFORE state; the post-change commit is the AFTER state. Both exist.
- **Snapshots accumulate but stay manageable.** Snapshot tags are visible in revert mode's history. Old snapshots aren't auto-pruned in v1 — let real usage tell us if pruning is needed.

## See also

- `commit` — the regular commit os-tune fires after a change
- `revert` — uses snapshot tags as targets
- `os-tune/references/approval-tiers.md` — defines which changes warrant a snapshot
