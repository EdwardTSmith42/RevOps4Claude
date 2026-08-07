# PR overlap check

The discipline of checking open PRs and recent develop/main merges for already-in-progress fixes before opening a new fix branch. Prevents duplicate work and silent merge conflicts.

## The check

Before creating any fix branch or PR for a bug:

1. **List open PRs** in the relevant repo. Shortlist by area / keywords matching the bug signature.
2. **Inspect each shortlisted PR's** `.md` context brief and changed files.
3. **Check recent merges to `develop`** (or `main`, depending on the workflow) for candidate remediations that already shipped.

## Decision rule

- **Exact overlap** (a PR is fixing the same issue): **do not open a new PR.** Add notes to the existing thread/PR.
- **Partial overlap** (a PR is fixing some of this, missing some): **trim scope to net-new low-risk deltas only.** Don't ship duplicative lines.
- **No overlap** (no PR addresses this): **proceed with isolated fix PR.**

State explicitly which case applies in the investigation findings.

## Per-team PR conventions

If your team has a PR-brief convention (a `.md` context brief committed alongside the diff, a required `WHY NOW` section in the summary, etc.), apply it on new PRs surfaced through this check. The `dev-PR` skill, when configured for your team's conventions, handles the brief-authoring side.

## Practical commands

Assumes GitHub via the `gh` CLI; adapt to your forge if different.

```bash
# List open PRs
gh pr list --repo <org>/<repo> --state open --limit 50 \
  --json number,title,url,headRefName,baseRefName,updatedAt

# Inspect a candidate
gh pr view <PR_NUMBER> --repo <org>/<repo> \
  --json files,body,title,url,headRefName,baseRefName
```

## Used by

- `evidence` mode — step 4 (overlap check before backlog coordination).
- `recurring-hunt` mode — before any FIX_NOW PR (the mode usually doesn't open PRs but the principle applies when fixes get promoted).
- `pr-interrogate` mode — incidentally, when interrogating whether a similar fix is already in flight.
- Any cross-system bug-comms workflow you maintain — when posting updates that include "fix in progress" status, the overlap check informs whether to point at a new task or an existing one.

## Malleability note

**Canonical:** the three-state decision rule (exact / partial / no overlap → existing thread / trim scope / new PR).

**Adaptable:** the specific commands (forge-dependent), the repo structure, and any per-team PR-brief convention. Different orgs have different brief locations or different merge-target branches.

