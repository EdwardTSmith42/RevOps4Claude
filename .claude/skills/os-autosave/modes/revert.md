---
mode: revert
parent: os-autosave
---

# os-autosave / revert — return to a previous state

## What this mode does

Returns the workspace to a previous state. Three target types: last commit, point in time (N hours ago / specific timestamp), or named snapshot/commit.

This is the user's "save from heartache" payoff. Whatever happened — os-tune made a change they don't want, they accidentally edited a file, a manual mess accumulated over a week — revert returns them to a known-good state.

## When this fires

User-initiated only. os-tune never auto-reverts.

Common phrasing shapes (intent, not script):

- Undo the last save → revert to most recent commit (parent of HEAD)
- "Go back N hours/days" or "to <date>" → revert to a point in time
- "Go back to before [event]" → revert to an os-tune snapshot tag or a commit-message match
- "Revert this skill to its last good state" → revert a specific file or folder, not the whole workspace

## Inputs

- **Target.** Which state to revert to. Resolved from user phrasing:
  - "last commit" → previous commit hash
  - relative time ("N hours/days ago") → commit at-or-before that time
  - "before [event]" → matching snapshot tag (os-tune snapshots) or commit-message search
  - absolute date → commit on or before that date
- **Scope.** Whole workspace (default) or specific files
- **Confirmation level.** Always confirm before applying; the level of detail in the diff shown can be configured

## Edge cases

**Auto-save isn't on yet** (no local version control). There's nothing to revert to — say so plainly in the user's words (no raw git output, no "repo not initialized"), and offer to turn auto-save on (`setup` Part A) so future work is protected. Same pattern as `commit`.

## What `revert` does

1. **Resolve the target.** Find the commit hash that matches the user's described state. If ambiguous, surface options.
2. **Compute the diff.** What's about to change between current and target?
3. **Surface the diff in plain language.** Name what's about to change (file counts, what was added/modified/removed) and offer the user the choice between seeing the full diff or proceeding.
4. **Confirm before applying.** User says yes; revert proceeds. User says no or modifies; revert iterates or stops.
5. **Save current state first.** Before reverting, run `commit` on any pending changes with a "Pre-revert state" message naming the reason. Even when the revert is intentional, the current state is preserved as a commit so the user can come back if they change their mind.
6. **Apply the revert.** Default to `git revert` (which adds a new commit undoing the target — preserves history). Use `git reset --hard` only when the user explicitly says they want to throw away the in-between work.
7. **Sync to the online backup if one exists.** Push the result up only if the user has the optional backup on; otherwise the local undo is complete.
8. **Surface the result.** Confirm what was undone in plain language, and remind the user their previous state is saved as a restore point they can come back to.

## Operating principles

- **Never lose unsaved work.** Always commit pending changes before reverting. The "save before destroy" rule.
- **Always confirm.** Revert is the most destructive operation os-autosave offers. Even if the user's intent is clear, the diff surfaces and a confirmation is required.
- **Plain language.** The user sees everyday undo vocabulary, never the git verbs (reset, checkout). The diff is described in plain English with concrete file counts and the target's plain-language name.
- **Preserve history.** Default to `git revert` over `git reset`. Only use reset when the user explicitly says they want to throw away in-between work.
- **Surface the audit trail in inbox.** Every revert logs an entry to `os-inputs/_os-inbox.md` with `[type: audit]` tag and full context so os-tune can flag patterns (e.g., user reverts the same skill 3 times = something deeper is wrong with that skill).

## Edge cases

**Target is ambiguous.** Multiple commits match the user's description. Revert surfaces options ranked by likely match, each labeled with the commit's plain-language message and timestamp so the user can pick.

**Conflicts during revert.** Rare in v1 (single-machine usage) but possible if the user has a non-fast-forward history. Surface clearly; route to manual resolution help. v1 doesn't auto-resolve.

**Reverting would discard an os-tune change the user explicitly accepted.** Surface a warning that names what they confirmed earlier and ask for explicit reconfirmation before proceeding.

**Reverting a file rather than the whole workspace.** Supported. Compute file-level diff, confirm, apply. Same principles.

**The target is in the future (timestamp ahead of HEAD).** Surface the inconsistency politely and ask whether they meant an earlier date.

## What revert never does

- Force-push without explicit user confirmation
- Discard pending changes without committing them first
- Revert without showing the diff
- Apply silently — every revert produces a session-output line confirming what changed

## See also

- `commit` — what gets reverted
- `snapshot` — os-tune's targeted snapshots, often the destination of *"go back to before [os-tune change]"*
- `status` — see current state and recent history before reverting
- `setup` — run if revert says the repo isn't ready
