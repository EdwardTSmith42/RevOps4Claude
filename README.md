# RevOps4Claude — Skills + Voice for Claude Cloud Routines

This repository mirrors the Personal OS setup so **Claude cloud routines**
(scheduled cloud agents) can use it. A cloud routine clones this repo at run
start and auto-discovers what's here.

## What's synced (daily, ~7:10 AM PT)
- **`.claude/skills/`** — the full Personal OS skill library. Routines auto-discover these.
- **`os-inputs/voiceprints/`** — the operator's voiceprints, so routines can draft in his voice.
- **`os-inputs/_os-user-profile.md`** — drives the implied-author rule ("write as me" -> the default voiceprint).

## Source of truth
Everything here is a mirror of the local Personal OS vault at
`C:\Users\esmith\personal-os`. **Edit there, not here** — this repo is
overwritten on the next sync. Sync script: `personal-os\bin\cloud-skill-sync-daily.ps1`
(Windows Scheduled Task "RevOps4Claude Skill Sync Daily").

Excluded from the mirror: local report backups, stray zips, caches, and the rest
of `os-inputs/` (inbox, logs, preferences) that routines don't need.