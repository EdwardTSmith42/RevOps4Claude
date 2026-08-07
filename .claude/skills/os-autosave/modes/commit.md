---
mode: commit
parent: os-autosave
---

# os-autosave / commit — save a restore point

## What this mode does

Saves a restore point — a local save of the current workspace state. If the user has turned on the optional online backup, it also sends the save up there. Called manually by the user (in plain language — "save where I am"), or automatically by os-tune and the session lifecycle.

Saves carry formatted messages (per `references/commit-message-format.md`) so `revert` can navigate them meaningfully later. The user never sees the message format or the word "commit" — to them it's a restore point.

## When this fires

Two paths.

**Manual:** any user phrasing that means "save this state" — commit, save, snapshot-it. Optional message.

**Automatic — three moments:**

1. **After os-tune applies a successful change** — `refine` or `extend` calls commit with operation context
2. **At session end** as a side-effect, capturing final state (message marks the session boundary with a timestamp)
3. **Immediately after `setup` completes** (initial commit)

## Inputs

- **Optional message** — when called manually or by os-tune, an explicit message overrides the default-generated one
- **Optional scope** — restrict the commit to specific files (rare; default is everything)
- **Calling context** — who's calling (user / os-tune / session lifecycle), affects message format and audit trail

## What `commit` does

1. **Run `git status`** to see what's pending. If nothing, surface a plain "nothing to commit" line and exit cleanly.
2. **Stage all changes** respecting `.gitignore` (`git add -A`).
3. **Generate the commit message** per `references/commit-message-format.md` if no explicit message was supplied. Format varies by caller — os-tune-triggered, session-start, session-end, user manual, initial — see the format reference for exact shapes.
4. **Save the restore point** (commit) with the message.
5. **Sync to the online backup — only if one's set up.** If the user turned on the optional backup, push there. If there's no backup configured, stop here: local-only is the complete, expected state, *not* an error or a missing step.
6. **Surface the result** in plain language: a one-line "saved a restore point" with the file count — and, if a backup exists, that it synced online too. Never the raw commit message or git output.

## Operating principles

- **Local save first, backup second.** The restore point is always saved locally first; the online sync (if any) comes after. Never sync without saving locally.
- **No backup is a normal state, not a failure.** If no online backup is configured, a save is local-only and complete. Don't warn, don't nag, don't route to setup.
- **Idempotent.** Saving when nothing's changed is a quiet no-op, not an error.
- **Backup-sync errors fall back to local.** If the online sync fails (network, auth), the local restore point still stands; surface the sync hiccup in plain language with a low-key retry option. The user never loses work over a connectivity issue.
- **Surface unusual changes.** If the commit includes files that look like secrets (matching common secret-leak patterns), surface a warning before committing. User can confirm or abort.
- **Audit trail in inbox.** os-tune-triggered commits log a corresponding `[type: audit]` entry in `os-inputs/_os-inbox.md` so the user can see os-tune's activity in one place. Session-boundary commits don't log to inbox (too noisy).

## Edge cases

**Auto-save isn't on yet** (no local version control). Surface plainly — in the user's words, not "the repo isn't initialized" — and offer to turn auto-save on (`setup` Part A).

**There's a merge conflict from elsewhere.** Surface in plain language and route to `revert` or to manual conflict resolution. v1 doesn't try to resolve conflicts automatically.

**The online backup sync fails repeatedly** (only possible if a backup is set up). Surface it in plain language, keep saving restore points locally, and suggest re-running `setup`'s backup step if the GitHub sign-in seems to have expired.

**The commit would include something that looks sensitive.** Surface and confirm. The `.gitignore` should prevent most of these but human-pasted secrets in arbitrary files happen.

## See also

- `setup` — runs first, makes commit possible
- `snapshot` — os-tune's pre-change variant of commit (different message format, tagged)
- `revert` — undoes a commit (or a series)
- `status` — see what would be committed without committing
- `references/commit-message-format.md` — full format spec
