# RevOps4Claude — Skills for Claude Cloud Routines

This repository mirrors the Personal OS skill library so **Claude cloud routines**
(scheduled cloud agents) can use them. A cloud routine auto-discovers skills
committed under `.claude/skills/` when it clones this repo at run start.

- **Source of truth:** the local Personal OS vault at `C:\Users\esmith\personal-os\skills`.
  Edit skills there, not here.
- **Sync:** a daily Windows Scheduled Task ("RevOps4Claude Skill Sync Daily")
  re-copies the vault's skills into `.claude/skills/` and pushes any changes each morning.
- **Do not hand-edit `.claude/skills/`** — it is overwritten on the next sync.

Excluded from the mirror: local report backups, stray zips, and caches.