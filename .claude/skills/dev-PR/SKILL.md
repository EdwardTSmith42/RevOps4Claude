---
name: dev-PR
description: >-
  Author a per-branch PR context brief, compose the PR body, and open or update
  the PR — with reviewer-oriented sections (Big Picture, How It Works, Patterns
  Kept vs Changed) prioritized over generic file-list narration. Assumes a
  GitHub workflow (`gh` CLI). Triggers on "draft the PR body", "open a PR for
  this branch", "build a brief for this change", "PR-prep for this branch". Do
  NOT trigger for PR review (use `dev-review`). Do NOT trigger for bug-fix PR
  interrogation (use `dev-investigate pr-interrogate`).
version: 0.1.0
category: Coding
display_name: PR Author
tagline: 'Compose PR bodies that lead with the why, not the file list.'
packs:
  - dev-pack
icon: 'phosphor:GitPullRequest'
when_to_use: >-
  Reach for this when you've finished a branch and need to open or update a PR.
  Authors a per-branch context brief, then composes the PR body —
  reviewer-oriented sections (Big Picture, How It Works, Patterns Kept vs
  Changed) prioritized over generic file-list narration. The discipline that
  makes reviewers say 'I get it' on the first scroll.
---

# dev-PR

## Purpose

Help a reviewer trust your change quickly. Author a branch-scoped brief, then compose a PR body that explains **what changed, why this shape, which patterns stayed the same, which changed on purpose, where to start reading, and what proof matters** — in that order, in plain language.

The PR body is reviewer orientation, not a changelog. The branch brief is the source artifact; the PR body is its public render.

## When to use

- Preparing a PR ("write the PR body for this branch", "draft the PR description").
- Updating an existing PR body after fixes land ("refresh the PR body").
- Authoring the branch-scoped brief that the PR body is built from ("build a brief for this change").
- Pre-open gating before clicking Create ("run the pre-open checklist").

## First-time setup

This skill assumes a GitHub-based workflow. Before first use:

- Install the GitHub CLI (`gh`) — see https://cli.github.com/.
- Authenticate: `gh auth login` (browser flow is easiest).
- Confirm the active account matches the repo owner where you'll be opening PRs (`gh auth status`).

The skill writes branch briefs to a repo-local convention (`docs/change-briefs/open/<branch-slug>.md` by default). If your repo uses a different location for change documentation, surface and adapt the path on first run.

Other tool integrations (project tracker, support system, bug-comms channels) are out of scope here — those belong in sibling skills you wire up separately.

After this section has been read once, you can remove it from the in-repo copy of the skill.

## Workflow

### 1. Confirm the surface

```bash
git branch --show-current
git status --short
gh pr list --head "$(git branch --show-current)" --json number,title,author --jq '.[]'
```

Refuse to proceed on protected branches (`main`, `develop`, `master`, `release/*`) unless the user explicitly overrides. PRs from other authors: do not mutate the body unless the user explicitly asks; this skill is for personal PR prep.

### 2. Author or refresh the branch brief

Brief lives at `docs/change-briefs/open/<branch-slug>.md` (repo-local convention; adapt path if the target repo uses a different one — surface the path before writing).

**If a `dev-branch-memory` dream artifact exists** for this branch (default path: `<repo>/.local/branch-memory/<repo-key>/<branch-slug>/dream/reviewer-brief-input.md`), prefer it as the source for the reviewer-facing brief sections — that artifact is purpose-built for PR-time consolidation and likely has more rationale captured than a fresh authoring pass would surface. If you don't use `dev-branch-memory`, skip this step.

**Graceful degradation when no brief exists and the user doesn't want to author one:** read `git diff` and `git log` directly, draft the PR body from those, and *recommend* authoring a brief if the change is medium/high-risk (lockfile changes, schema migrations, public API changes, multi-file refactors).

If the brief exists, **preserve authored explainer sections on rerun**. Reviewer-facing prose is the artifact that matters most; never overwrite it with deterministic fallback text.

The brief should include — populate with real evidence, not placeholders:

- **Why now** — the trigger (Sentry issue, customer report, internal incident, deadline)
- **Bug / problem** — what's broken or missing
- **Outcome** — what users / reviewers should expect
- **Evidence / Error Data** — Sentry/log/API snippets with links, OR
- **Verbatim Signals** — quoted user/customer/internal statements
- **Plain-Language Fix** — written for someone new to the codebase
- **Scope** — minimal low-risk scope (or explicit risk classification + risk/blast-radius/rollout/rollback sections for medium/high-risk branches)

Bug-fix PRs additionally need:
- **User-Facing Bug Fixes** — one or more plain-language bullets describing each regression/fix from the user-experience perspective (these become the lead bullets in `## Summary`).

For Sentry impact lines: **never write `0 affected users` unless attribution tracking is explicitly confirmed.** Use `Affected Users: unknown (not tracked)` when attribution is unknown.

See `templates/branch-brief.md` for the section structure.

### 3. Compose the PR body

Read `references/reviewer-writing.md` before drafting reviewer-facing sections. The shape is:

```markdown
## Summary
<bug-fix: lead with User-Facing Bug Fixes bullets; feature/infra: lead with outcome + code-shape decision>

## Big Picture
<before/after system or flow explanation, with file links>

## File By File
<curated, grouped, human-oriented; each entry says what the file proves or why it matters>

## How It Works
<ordered mechanism: state ownership, error path, lifecycle>

## Patterns Kept vs Changed
<Kept: familiar architecture, contracts, utilities. Changed: responsibilities moved or tightened.>

## One Important Mental Model
<one framing idea that makes the diff easier to read>

## Changed Files / Critical Files / Tests / Blast Radius / Contracts / Verification
<deterministic reviewer-support sections; these come second and support the narrative>
```

The reviewer-facing narrative sections (`Big Picture`, `File By File`, `How It Works`, `Patterns Kept vs Changed`, `One Important Mental Model`) are the **main artifact** — write them yourself. The deterministic sections are safety-net support.

For file labels, use the file basename or shortest unique suffix (`AiProvider/index.tsx`, not the full repo path).

For `## Reviewer Guide` (when included): tell the reviewer where to start. Order with `Start with`, `Then check`, `Then confirm`. Group supporting files instead of listing every path.

See `templates/pr-body.md` for the section skeleton and `references/reviewer-writing.md` for the writing rules.

### 4. Pre-open checklist (gate)

**The agent answers every item itself, out loud, with concrete evidence** — do not rubber-stamp the list, and do not ask the user to confirm items. "Out loud" means the agent states each answer and the evidence behind it as part of its work; the answered checklist lands in the PR body as a record. An item the agent genuinely cannot verify is stated as unverified — never greened on optimism — and only *that* gets surfaced to the user. Do not proceed to step 5 until every item is answered (or explicitly flagged unverified with reasoning).

- **State model**: data shape and ownership boundaries verified
- **Error path simple**: failure modes considered; no swallowed errors
- **Canonical utilities**: reused existing helpers vs. reinventing
- **Scope focused**: nothing unrelated bundled in
- **Non-self audit**: a reviewer who didn't write this could understand it from the brief
- **Out-loud checklist done**: this list itself
- **Lockfiles**: default is **no lockfiles** in the PR. Detect with:
  ```bash
  git diff --name-only --diff-filter=AM "origin/$BASE" | grep -E '(yarn|package|uv|Cargo|poetry|Pipfile)\.lock'
  ```
  If lockfiles are present, determine from the branch's own history whether the dependency change is intentional (a commit that adds/upgrades a dependency on purpose) or churn. Only when intent genuinely can't be determined from the work itself does the question go to the user.

Block PR creation if any item is unanswered. See `references/cycle-checklist.md` for the begin / during / pre-open lifecycle.

### 5. Write body to disk

Write the composed PR body to `/tmp/pr-body-<branch-slug>.md`. No approval stop here — the agent proceeds directly to opening the PR. The user reviews on GitHub itself, where review belongs; edits and reactions are flagged there, not in chat. The agent pauses for the user in exactly two situations: it genuinely cannot describe the PR (missing context it can't recover), or it has an idea for materially improving the PR body that's worth a quick take. Otherwise: open it, hand over the link.

**Relevance rule for the body:** the PR body describes the change as it exists, not the journey that produced it. Process events that left no mark on the final diff — aborted actions, corrected mistakes, tooling detours, dead-end approaches — don't belong, however memorable they were in the session. The test: would a reviewer reading only the final diff need this sentence to evaluate the change? Anything that would embarrass the author without informing the reviewer is doubly disqualified.

### 6. Create / update the PR

```bash
# New PR (use --draft if work is still in progress)
gh pr create --title "<conventional-commit-style title>" --base develop --body "$(cat /tmp/pr-body-<branch>.md)"
gh pr create --title "..." --base develop --draft --body "$(cat /tmp/pr-body-<branch>.md)"

# Update existing PR body
gh pr edit <number> --body "$(cat /tmp/pr-body-<branch>.md)"
```

After creating a new PR: read the PR back via `gh pr view <number>`, refresh the body once more so file links resolve to `pull/<number>/files#diff-...` anchors instead of weaker fallbacks, and hand the user the PR link — that's the deliverable.

### 7. Hand off to adjacent skills as appropriate

These hand-offs happen *after* the PR body is written and the PR exists. Do not embed pointers to them inside the PR body itself — the body is a pasteable artifact for reviewers, not a workflow log.

- For larger / risky PRs: consider `dev-review checkpoint` before opening, to surface gaps the brief missed.
- For non-blocking issues surfaced during the pre-open checklist: capture via `dev-scope-deferral`.
- For bug-fix PRs that need coordinated status updates posted out to a project tracker, support system, or team channel: hand off to whatever bug-comms skill or playbook you've wired up for that.

## Hard rules

- **AI-authored sections > deterministic fallbacks.** The reviewer-orientation craft is what makes the body useful; template-stitching from filenames is the safety net, not the target quality bar.
- **Never paraphrase preserved authored sections** when refreshing a brief. Reauthoring destroys craft.
- **Plain-language first, IDs second.** Lead with what changed and impact; reference IDs go in parentheses or trailing.
- **Bug-fix PRs lead `## Summary` with user-facing fix bullets**, not bookkeeping.
- **Feature PRs lead `## Summary` with the outcome and code-shape decision**, not metadata.
- **`Affected Users: unknown (not tracked)`** when attribution is untracked. Never `0 affected users` unless explicitly confirmed.
- **Refuse protected branches** (`main`, `develop`, `release/*`) — a hard stop the agent enforces itself: don't open, say why. The user can override by explicit instruction; the agent never asks permission to proceed as a workaround.
- **Do not mutate non-personal PRs** (other authors) without explicit user request.
- **Brief is local by default.** Don't emit a `Context brief` line into the GitHub PR body unless the brief itself is intentionally committed to the repo.
- **Lockfile discipline.** Default is no lockfiles in PR. If they're changed, verify from the branch's own work that the dependency change is intentional; escalate only when intent can't be determined.

## Design Rationale

- **Reviewer orientation > changelog.** A PR body's job is to help a reviewer trust the change quickly — what changed, why this shape, what patterns stayed the same, where to start reading. Filename-driven changelog narration fails at all of these.
- **Brief as source artifact, PR body as render.** The brief is where reviewer-facing thinking happens. The PR body is its public projection. Authoring once and rendering twice prevents the brief and PR body from drifting.
- **AI-authored sections preferred over deterministic fallbacks** because reviewer orientation requires judgment, not template-filling. Deterministic text is a safety net — useful when the AI flow fails — not the target quality bar.
- **Preserve authored sections on brief rerun** because reauthoring is destructive of craft. The init step should be additive: refresh diff stats and metadata, leave reviewer-facing prose alone.
- **`unknown (not tracked)` over `0 affected users`** because "0" implies no impact when really we don't know. The phrasing prevents accidental confidence.
- **Bug-fix PRs lead with user-facing bullets** because reviewers (and stakeholders skimming the PR list) need impact before mechanism. Hiding the user-facing change inside paragraphs violates the orientation rule.
- **Pre-open checklist as out-loud self-answers** because checklist items rubber-stamp themselves when implicit. The agent saying each answer out loud — with evidence, into the PR body — forces real verification. The human is not the verification mechanism; evidence is. The user's review happens on GitHub, where it belongs.
- **Refuse protected branches** because PR-prep against `main` / `develop` is almost always a workflow mistake. The block is recoverable; the unintended PR isn't.
- **Lockfile discipline** because lockfile churn is the most common form of accidental scope expansion. Default no, opt in with explicit intent.

## Distinct from adjacent skills

- **`dev-review`** — reviews and fixes (ship-gate, checkpoint, manifesto-review, smoke-qa, etc.). Everything PR-shaped — the brief, the body, the checklist, opening and updating the PR — belongs to dev-PR, and only dev-PR. dev-review's `brief` mode covers non-PR change briefs and cites this skill's checklist rather than carrying its own copy.
- **`dev-investigate pr-interrogate`** — verifies whether a bug-fix PR is *actually* a root-cause fix (rootness classification + differential proof). dev-PR doesn't assess fix quality; it composes the body.
- **`dev-branch-memory`** — captures decision-trail memory for the branch's implementation work. dev-PR's brief is reviewer-facing; branch-memory is implementer-facing. The brief can pull from `dev-branch-memory dream` output near PR time.
- **Anything that posts outside GitHub** — project-tracker updates, support-system notes, team-channel announcements — is a downstream hand-off, not part of this skill. dev-PR's surface is GitHub only.

## References

- `references/reviewer-writing.md` — writing rules for the reviewer-facing sections (read this before drafting)
- `references/cycle-checklist.md` — begin / during / pre-open lifecycle gates with out-loud confirmation flags

## Templates

- `templates/branch-brief.md` — section structure for the per-branch brief
- `templates/pr-body.md` — PR body skeleton (reviewer-facing narrative + deterministic support sections)

