---
name: os-autosave
version: 0.1.0
description: >-
  The workspace safety net for Personal OS. Quietly keeps local restore points so
  any AI-driven or manual change can be undone — the user never types or sees a git
  command. Default is local-only (zero accounts, zero friction); an off-machine
  backup to a private GitHub repo is an optional add-on the user can turn on later.
  Pairs with os-tune's tiered approval — snapshots before moderate/large changes so a
  revert can target a specific os-tune operation. Five modes: `setup` (turn on local
  restore points; optional online backup), `commit` (save a restore point), `snapshot`
  (named save point), `revert` (restore to a point / N hours ago / a named save point),
  `status` (what's unsaved). Triggers on "set up auto-save," "turn on version control,"
  "save where I am," "undo to yesterday," "go back to before os-tune changed the email
  skill," "what's unsaved," "back up my workspace online."
display_name: Auto-Save
tagline: Quietly keeps restore points so you can always go back.
category: Planning
packs:
  - personal-os
icon: 'phosphor:FloppyDisk'
when_to_use: >-
  The safety net for Personal OS. It quietly saves restore points as you work, so
  you can undo anything just by asking — no git, no terminal, no jargon. Local by
  default; an online backup is optional.


  Reach for this to turn on auto-save for a workspace, save a named point you can
  return to, undo back to yesterday / a specific os-tune change / a named point, or
  add an off-machine backup. Status mode tells you what's unsaved.
modes:
  - name: setup
    job: First-time setup — turn on local restore points (silent). Offers an optional off-machine backup (private GitHub repo) for users who want one.
  - name: commit
    job: Save a restore point now (local; pushes to the backup too, if one's set up).
  - name: snapshot
    job: Named save point you can return to later.
  - name: revert
    job: 'Restore to a point, N hours ago, or a named save point.'
  - name: status
    job: What's currently unsaved.
---

# os-autosave — the safety net for Personal OS

## Purpose

os-autosave is the workspace's undo system, packaged for people who never want to think about version control. It runs git underneath, but the user never types a git command and never sees git words. What it does:

- Quietly keeps **local restore points** as work happens — AI-triggered, at session boundaries, and at the next session open if the user edited something offline.
- Lets the user **undo to any earlier state** when something goes sideways, in plain English.
- Shows **what's currently unsaved** when asked.
- Optionally keeps an **off-machine backup** (a private GitHub repo) for users who want a copy stored safely online — opt-in, never required.

The default is local-only on purpose. Restore points on the machine give the full undo safety net with **zero accounts and zero friction** — exactly what you want during a first install. The online backup is a separate, later choice for people who want protection against the whole machine dying; it costs a free GitHub account and a minute of setup, so it's offered, not assumed.

It's the protective layer that lets os-tune be bold. os-tune can apply trivial changes on its own (per `os-tune/references/approval-tiers.md`) because os-autosave captures a restore point first — if it goes wrong, undo is one sentence. It's also protection against the user's own manual edits: open a skill file outside the app and break something, and os-autosave catches it on the next session open and offers to roll it back.

## When to use

Common triggers:

- *"Turn on auto-save"* / *"Turn on version control"* → `setup`
- *"Save where I am"* / *"Make a restore point"* → `commit`
- *"Undo to yesterday"* / *"Go back to before [X]"* → `revert`
- *"What's unsaved?"* / *"What's changed?"* → `status`
- *"Back up my workspace online"* / *"I want a cloud copy"* → `setup`'s optional backup step
- (Internal) os-tune calls `snapshot` before moderate/large changes
- (Internal) os-tune calls `commit` after any successful apply
- (Internal) Session-start runs `commit` if there are pending manual edits since last session

## Modes (v0.2)

| Mode | Job | Who calls it |
|---|---|---|
| `setup` | Turn on local restore points (silent, no accounts). Optionally add an off-machine backup later. | User |
| `commit` | Save a restore point. Pushes to the backup too, if one exists. | User, os-tune, session-end hook |
| `snapshot` | A named restore point before os-tune applies a moderate/large change | os-tune only |
| `revert` | Return the workspace to an earlier state | User |
| `status` | Show what's unsaved, the last restore point, recent history | User, os-tune (for inheritance) |

## How it relates to install (os-guided-setup)

Auto-save is deliberately **parked at install, not switched on**. The first session is engineered for immediate momentum — there's nothing to lose in the first ten minutes, setup chores are no fun, and some users don't even have the accounts that the online layer would ask about. So os-guided-setup leaves auto-save as a passive item on the pre-seeded Getting Started list, where it gets offered gently in the days after install (and sometimes as one of the closing two-door options). When the user says yes, `setup` runs Part A — local restore points need no account and no network, so every user gets the undo safety net regardless. The **off-machine backup stays a second, strictly opt-in layer** for users who have (or want) GitHub. Local-first everywhere, remote strictly opt-in, nothing mandatory at install.

## Inheritance from Personal OS

os-autosave doesn't have rich inheritance like os-tune, but it reads:

1. **Identity.** `os-inputs/_os-user-profile.md` — drives the default backup-repo name suggestion *if* the user opts into the online backup.
2. **Philosophy.** `os-inputs/_os-setup-philosophy.md` — user preferences for save cadence, message style, default undo behavior.
3. **Workspace files and `.gitignore`** — scopes what gets saved vs ignored. Uses the workspace's shipped `.gitignore` if present; otherwise generates one from `references/gitignore-defaults.md`.

## os-tune integration

os-tune calls os-autosave at three moments:

- **Before any os-tune apply that's moderate or large tier** — `snapshot` runs, creating a named restore point for the upcoming change. If the apply goes wrong, this is the target to roll back to.
- **After any successful os-tune apply** — `commit` runs with an os-tune-generated message naming the mode, the skill, and the intent.
- **At session end** — `commit` runs, capturing final session state.

os-tune's mode files (`os-tune/modes/refine.md`, `extend.md`, `close-out.md`) include the calls. The wiring is one-line invocations, not architectural coupling — os-autosave exposes operations; os-tune calls them at the right moments.

## Scheduled background runs (paired with os-tune)

os-autosave and os-tune are paired in os-guided-setup's recurring-automation step: the user can opt into a scheduled sweep that runs both at a low-friction cadence (often a morning routine), so restore points and pattern detection happen without anyone having to think about them. The scheduling lives in os-guided-setup (on the harness's native scheduler); what os-autosave contributes is operations that are safe to call repeatedly with nothing to do (idempotent — see `commit`).

## Operating principles

- **Local-first, remote opt-in.** Default protection is local restore points — no account, no network, no friction. The off-machine backup is a deliberate, later, opt-in choice; never a precondition for being protected.
- **Plain language, never git language.** The user sees everyday words for saving and undoing — "restore point," "undo," "back up online" — never "commit," "push," "init," "HEAD," "detached," "rebase." Git terms that leak through errors get rewritten before they reach the user.
- **Surface, don't surprise.** Every save shows, in one plain line, what was captured. Every undo shows what's about to change before it happens — even when os-tune is the caller.
- **Never lose unsaved work.** Before any operation that could discard changes (undo, branch swap), os-autosave saves or sets aside pending changes and shows what's about to be affected.
- **Privacy by default for the backup.** If the user does opt into the online backup, the repo is always private — no public option.
- **No terminal required, ever.** After setup the user never types a git command; everything works through plain requests.

## What os-autosave never does

- Doesn't turn on the online backup without the user asking for it
- Doesn't create public repos
- Doesn't include secrets in saves (the `.gitignore` catches them; if something slips through, status warns before the next save)
- Doesn't push to a backup that exists without saving locally first
- Doesn't undo without confirmation, even when called by os-tune
- Doesn't rewrite history (no rebase, no force-push) — append-only

## Related skills

- `os-tune` — primary integration point. Calls os-autosave at three AI-triggered moments.
- `os-guided-setup` — leaves auto-save parked at install rather than switching it on; defers both turning it on and the online backup to this skill.
- `os-library` — shipped skills carry `version` tags; os-autosave commits when they change but doesn't manage the tag.
- All other skills — os-autosave captures their files in restore points without needing to know about them.
