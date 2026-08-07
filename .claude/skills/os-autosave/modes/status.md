---
mode: status
parent: os-autosave
---

# os-autosave / status — show pending and recent state

## What this mode does

Read-only. Shows the user what's currently pending, the last commit, and recent history. No mutations.

Used both by the user (asking what's pending or what os-tune most recently changed) and by os-tune as part of its inheritance — knowing the workspace's git state informs os-tune's behavior. Before applying a moderate-tier change, os-tune checks status to verify the workspace is clean and committed.

## When this fires

- User: any phrasing that asks "what's currently unsaved or recently changed?"
- os-tune: pre-flight check before invoking `commit` or `snapshot`

## What `status` returns

Three blocks, in plain language:

**Pending changes.** Files modified, added, or deleted since the last commit, summarized with counts plus the most relevant file names (don't dump the full path list when it's long).

**Last commit.** Hash, message, timestamp — phrased as a single readable sentence with relative time.

**Recent history.** Last N commits (default 10) with message and timestamp. Filter to show only os-tune-triggered, manual, or snapshots if the user asks for a specific subset.

## Edge cases

**Auto-save isn't on yet** (no local version control). Don't let the raw error surface — say plainly, in the user's words, that auto-save hasn't been turned on so there's no history to show yet, and offer to turn it on (`setup` Part A). Same pattern as `commit`.

## Operating principles

- **Read-only.** Never modifies. Safe to call freely.
- **Plain language.** Translates `git status` and `git log` output into user-facing English.
- **Filterable.** User can ask for specific subsets — os-tune changes, manual changes, snapshots.

## See also

- `commit` — apply pending changes
- `revert` — undo recent changes
- `setup` — run if the repo isn't initialized
