# gh CLI troubleshooting

Common failure modes the setup wizard catches, with the user-facing messaging and the resolution path.

## gh not installed

**Symptom:** `gh --version` returns "command not found."

**Wizard surfaces:** *"GitHub's command-line tool isn't installed yet. We need it to set up your private repo. On Mac, the easiest path is Homebrew — run `brew install gh` in your terminal. If you don't have Homebrew, here's the official download: https://cli.github.com. Come back here once it's installed."*

**Resolution:** Wizard waits for user to confirm install, then re-runs `gh --version` to verify.

## Homebrew not installed (Mac path)

**Symptom:** User reports `brew: command not found.`

**Wizard surfaces:** *"Looks like you don't have Homebrew either. You have two paths: install Homebrew first (https://brew.sh), then `brew install gh`. Or skip Homebrew entirely and use the direct download (https://cli.github.com). Either works."*

**Resolution:** User picks a path. Wizard waits for `gh --version` to succeed.

## gh installed but not authenticated

**Symptom:** `gh auth status` reports not logged in.

**Wizard surfaces:** *"gh is installed but you haven't signed in to GitHub yet. I'll start the auth flow — it'll open your browser, GitHub will ask you to authorize gh, and then you'll come back here."*

**Resolution:** Wizard runs `gh auth login` interactively. After completion, re-checks status.

## Auth flow stalled or browser blocked

**Symptom:** `gh auth login` started but never completed, or browser blocked.

**Wizard surfaces:** *"The browser auth didn't complete. Want to retry, or use a personal access token instead? (Token path is more steps but works without browser.)"*

**Resolution:** User picks. Browser retry or PAT-based flow with explicit instructions.

## MFA / two-factor required mid-flow

**Symptom:** GitHub prompts for 2FA code; user has it but flow times out.

**Wizard surfaces:** *"GitHub is asking for your 2FA code. Approve the auth in your browser when prompted, then come back."*

**Resolution:** Wizard waits longer than the default timeout for the auth handshake.

## Repo name collision

**Symptom:** `gh repo create` fails because the name is taken.

**Wizard surfaces:** *"Looks like '<name>' is already a repo on your account. Want to use a different name, or use the existing one?"*

**Resolution:** User picks. New name or existing-repo path. Wizard suggests a variant (e.g., adding the year) if user wants to stay close to the original.

## Permission error pushing

**Symptom:** Initial push fails with permission error.

**Wizard surfaces:** *"Push failed with a permission error. Most common cause: the gh auth doesn't include the right scopes. Want me to re-run auth with the right scopes?"*

**Resolution:** Wizard runs `gh auth refresh -s repo` and retries push.

## Network failures

**Symptom:** Any gh command times out.

**Wizard surfaces:** *"Looks like a network issue. Want to retry, skip this step (we can finish setup offline and push later), or stop?"*

**Resolution:** User picks. Skip path commits locally; push later when connected.

## Existing repo, divergent state

**Symptom:** User has an existing repo set up; remote and local diverge.

**Wizard surfaces:** *"Your local workspace and the remote repo have different content. Want to: pull the remote (replacing local), force-push local (replacing remote), or stop and review manually?"*

**Resolution:** User picks. Wizard does NOT default to either destructive option — explicit confirmation required.

## Unknown failure

**Symptom:** Anything not above.

**Wizard surfaces:** *"Hit an issue I don't recognize: <error text>. Want to retry, skip this step, or get help?"* Logs the failure to `os-inputs/_os-inbox.md` with `[type: audit] [skill: os-autosave]` so reflect can surface patterns of unknown failures.

**Resolution:** User picks. Failure log helps us learn the failure modes that show up in the field.
