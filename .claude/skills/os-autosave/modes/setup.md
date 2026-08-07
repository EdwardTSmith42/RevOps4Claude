---
mode: setup
parent: os-autosave
---

# os-autosave / setup — turn on the safety net

## What this mode does

Turns on auto-save for the workspace. Two parts, and the split is the whole point:

- **Part A — local restore points (the default, always).** Quietly switches on local undo so every change from here is reversible. No account, no network, no terminal, no git words. It's all most people ever need. (Not run at install — guided-setup parks auto-save on the Getting Started list; this mode runs when the user takes that offer.)
- **Part B — an off-machine backup (optional, opt-in).** For users who want a copy stored safely online in case the whole machine dies. Needs a free GitHub account. Offered, never assumed — and never run unless the user asks.

Designed for non-coders: assumes nothing about git, GitHub, or the terminal.

## When this fires

- *"Turn on auto-save"* / *"Turn on version control"* → Part A (and *offer* Part B at the end)
- *"Back up my workspace online"* / *"I want a cloud copy"* → Part B directly (run Part A first if it isn't on yet)
- User-initiated for Part B — os-autosave never sets up an online backup on its own

---

## Part A — Local restore points (the default)

Do this quietly and warmly. The user should come away knowing *"auto-save is on; I can undo anything by asking"* — not learning what git is.

1. **Check what's there.** Is the workspace already under local version control? Is there already a backup connected? (Read-only checks; don't narrate them.)
2. **Turn on local undo.** Initialize local version control if it isn't already. Don't say "git init" — just do it.
3. **Make sure the right things are ignored.** Use the workspace's shipped `.gitignore` if one's present (os-guided-setup ships one); otherwise generate it from `references/gitignore-defaults.md`. This keeps secrets, OS junk, and machine-local files out of saves. No need to walk the user through the list unless they ask.
4. **Save the first restore point.** Capture the current workspace as the baseline.
5. **Confirm in plain language, once.** Something in the spirit of: *"Auto-save is on — I'll quietly keep restore points as we work, so you can undo anything just by asking."* Then it runs silently going forward; no save-by-save narration.

That's the whole default. Local, silent, done. No GitHub, no push, no account.

**Then mention the backup as a future option — lightly, once.** *"Later, if you want, I can also keep a backup copy of all this stored safely online, in case your computer ever dies. Totally optional — just say the word."* Don't push it; don't run it now unless they ask.

---

## Part B — Online backup (optional, opt-in only)

Run this **only when the user wants a cloud copy.** This is where GitHub comes in. Frame it the whole way through as *"keeping a safe copy online,"* not as a git/GitHub tutorial. Explain each step in a sentence — what's about to happen and why — and keep moving; offer the deeper "why" only if they're curious.

### B1 — See what's already in place

Quietly check whether the GitHub command-line tool is installed and signed in, and whether a backup is already connected. Report in plain language only what matters — e.g. *"Looks like you're not signed in to GitHub yet — I'll walk you through it."*

### B2 — Get the GitHub tool ready (if needed)

If the GitHub CLI (`gh`) isn't installed, help them get it: detect the platform (Mac first), and on Mac propose `brew install gh` (or point at the official download if Homebrew isn't there). Surface copy-paste-ready instructions; ask them to run the install and confirm. Don't run the install for them — that's a boundary they should cross on purpose.

### B3 — Sign in to GitHub

Run `gh auth login` interactively. Before it launches, tell them plainly: a browser will open, GitHub will ask them to approve, and they'll come back here when done. Verify with `gh auth status`; if it fails, name the likely cause (no internet, wrong account, two-factor) and walk through it.

### B4 — Create the private backup

Suggest a name from `os-inputs/_os-user-profile.md` (often a `personal-os-<handle>` shape); let them accept or edit. **Always private** — there's no public option. Create it (`gh repo create <name> --private --confirm`). If the name's taken, offer variants; if they'd rather use a repo they already have, switch to that and verify access.

### B5 — Send the first backup up

Connect the workspace to the new repo and push the current state. Surface a one-line plain result: *"Done — a private backup is now saved online (X files). I'll keep it updated automatically."*

### B6 — Quick check

Confirm nothing's left unsaved and the backup is reachable. Close with a plain one-liner and the repo link for their records.

---

## Save preferences

Whatever got set up, record it to `os-inputs/_os-setup-philosophy.md`:

- Whether the online backup is on, and the repo URL if so
- Save cadence preference (default: every os-tune apply + session boundaries)
- Default undo behavior

These get read by `commit`, `revert`, `status`, and os-tune.

## Offer the recurring background schedule (optional)

At the end, offer to hand off to `os-guided-setup`'s recurring-automation step, which can schedule os-autosave and os-tune to run together on a low-friction cadence (often a morning routine), using the harness's **native** scheduler. For someone who's never set up a scheduled task, introduce the idea in a sentence. Opt-in, never assumed.

## Failure modes (graceful)

Mostly relevant to Part B. Catch the cases in `references/gh-cli-troubleshooting.md`. Each failure surfaces, in plain language: what went wrong, the likely cause, the next step, and a "skip this for now" option — because the online backup is optional, almost no failure here is terminal. Part A (local restore points) should already be working regardless, so the user is never left unprotected while sorting out a backup hiccup.

## Operating principles

- **Local-first.** Part A always runs and stands on its own. Part B is a bonus the user chooses.
- **No terminal commands the user has to remember.** Every git/gh command runs inside the wizard; the user makes choices, not commands.
- **Plain language throughout.** No git/GitHub jargon in user-facing text — "restore point," "online backup," not "commit," "push," "remote."
- **Show before you do** — for anything that changes their machine or account. Trivial read-only checks don't need narration (or confirmation).
- **Save partial progress.** If setup quits mid-flow, what finished stays done; re-running picks up where it left off.
- **Privacy non-negotiable for the backup.** If created, the repo is always private.

## See also

- `references/gitignore-defaults.md` — what gets excluded and why (used if the workspace has no shipped `.gitignore`)
- `references/gh-cli-troubleshooting.md` — backup-path failure modes and recipes
- `commit` — what runs after setup, every time
- `revert` — the safety-net mode setup makes possible
- `os-guided-setup` — parks auto-save at install (Getting Started list); both parts run here when the user opts in
