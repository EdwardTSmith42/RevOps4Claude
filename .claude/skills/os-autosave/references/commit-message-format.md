# Commit message format

Standard formats for os-autosave commits. The format matters because revert mode navigates by these messages — meaningful messages make targeted revert possible.

## os-tune-triggered commits

Format: `os-tune <mode>: <skill> — <one-line summary>`

Examples:

- `os-tune refine: email skill — added P.S. default to client check-in mode`
- `os-tune extend: tracker skill — added "weekly review" mode`
- `os-tune make: new skill "transcript-cleanup" — generated from session pattern`

The summary is one line. If the change touched multiple files, the summary describes the *intent* of the change, not the file list.

## os-tune snapshots (pre-change)

Format: `Snapshot: pre-<mode> on <skill> — <incoming-change-summary>`

Tagged with: `snapshot/<YYYYMMDD-HHMM>-<skill>-<mode>`

Examples:

- `Snapshot: pre-refine on email skill — adding P.S. default to client check-ins`
- Tag: `snapshot/20260504-1423-email-refine`

The pre-change message describes what's about to happen, not what just happened.

## Session-start commits (manual edits caught)

Format: `Manual edits since last session — <N> files`

Examples:

- `Manual edits since last session — 2 files`
- `Manual edits since last session — 5 files (mostly .DS_Store cleanup, 2 real changes)`

The summary line gives a quick characterization. If the changes are unusually large, surface a warning before committing.

## Session-end commits

Format: `End of session <timestamp>`

Examples:

- `End of session 2026-05-04T16:42`

Simple. Marks the session boundary.

## User-initiated manual commits

Format: `Manual save — <user message or 'workspace state'>`

Examples:

- `Manual save — about to try a risky refactor`
- `Manual save — workspace state` (default when no user message)

User message is preserved verbatim. The "Manual save" prefix makes manual commits scannable in `git log`.

## Initial commit (from setup wizard)

Format: `Initial commit — Personal OS workspace`

Just one — runs once during setup.

## Pre-revert preserve commits

Format: `Pre-revert state: <reason>`

Examples:

- `Pre-revert state: about to revert to before os-tune refined email skill`
- `Pre-revert state: about to go back to yesterday's state`

These run automatically before any revert, preserving current state in case the user changes their mind.

## Why these formats

- **Scannable.** Reading `git log` or recent history surfaces what happened at a glance.
- **Targetable for revert.** *"Revert to before os-tune refined email skill"* maps directly to a snapshot tag or a commit message search.
- **Differentiable.** Manual commits, os-tune commits, session boundaries, and snapshots are all visually distinct.
- **Stable for tooling.** Future v0.2 features (UI history viewer, branch management) can parse these formats predictably.

