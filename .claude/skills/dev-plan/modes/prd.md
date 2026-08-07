# Mode: prd

Part of `dev-plan`. Selected when starting non-trivial implementation, triaging regressions, or preparing a draft plan that needs formal write-up + RED→GREEN→VERIFY execution discipline.

## Job

Produce a low-risk MVP-scoped PRD before coding, then enforce a reliable RED → GREEN → VERIFY loop.

## Default storage

Three options — pick based on the project context:

1. **Local-only (default)** — `<repo>/.local/dev-plan/prd/<branch-slug>.md`. Gitignored. Use for personal planning that shouldn't travel with the branch.
2. **Branch-traveling draft** — `<repo>/tasks/prd/<branch-slug>.md`. Travels with the branch for collaboration; clean up before final push.
3. **Tracked task** — when the repo uses an external task system, land the PRD there as a trackable task. Pair with `dev-branch-memory` for capturing decision-trail memory during execution.

If the repo uses an external task system, prefer option 3 unless the user explicitly says local-only.

## Run

### 1. Generate the PRD skeleton

Use `templates/prd-template.md` as the structure. Fill in:
- Title, type (`bugfix` | `feature` | `refactor`), branch, base branch
- File path the PRD will live at

### 2. Existing pattern inventory (required before proposing changes)

Search the repo for similar code, tests, helpers, components. Cite exact files in the PRD's "Existing Pattern Inventory" section.

```bash
rg "<targetFunctionOrConcept>" -n
rg --files | rg "<feature-or-module>"
```

The PRD does not move past this section until the inventory is real (concrete file paths, not "TBD").

### 3. Open-PR overlap scan

Detect overlap with active branches before writing implementation steps:

```bash
gh pr list --base "$(git rev-parse --abbrev-ref HEAD@{upstream} 2>/dev/null | sed 's|origin/||' || echo develop)" --state open --json number,title,headRefName,files \
  --jq '.[] | "\(.number) \(.headRefName): \(.title)"'

# For file-level overlap on a specific PR:
gh pr view <number> --json files --jq '.files[].path' | sort > /tmp/pr-<num>-files.txt
git diff --name-only "origin/${BASE}" | sort > /tmp/branch-files.txt
comm -12 /tmp/pr-<num>-files.txt /tmp/branch-files.txt
```

If overlap exists:
- Don't duplicate fixes across active branches
- Branch from the correct feature branch if work is stacked
- Log mitigation in the PRD's "Branch/PR Overlap Check" section

### 4. MVP scope — narrow and explicit

In-scope and out-of-scope lists are both required. Apply `references/prd-rubric.md` for section quality bar.

### 5. Failing tests first (RED)

Add tests with real edge cases (race / null / stale / timing / retry) before implementation. The tests must fail meaningfully — not just exist.

### 6. Minimal implementation (GREEN)

Implement the smallest fix that makes tests pass. Don't expand scope mid-implementation.

### 7. Verify

Run targeted suites and nearby regressions. Capture proof in the PRD's "Verification" section.

### 8. Finalize PRD hygiene

- Keep PRD docs in the final PR only when needed for audit / collaboration.
- Otherwise, if you used `tasks/prd/` storage, remove draft PRD files before final push.

## When to escalate

- → `dev-fresh-eyes` before starting RED tests, to pressure-test scope and existing-pattern reuse
- → `dev-PR` once GREEN is achieved and a real PR is ready
- → your team's cross-system update flow for regression PRDs (tracker comment, support-system note, release notes) so the people watching the regression know the fix is in motion
- → `dev-scope-deferral` for items the PRD explicitly defers (capture them so they don't get lost)

## Required rules

1. Inventory existing code/test patterns before proposing changes.
2. Keep MVP narrow and explicit (in-scope + out-of-scope).
3. Run overlap scan against open PRs and list collisions by file path.
4. Write failing tests before implementation.
5. Use low-risk, non-architectural changes unless the user asks otherwise.
6. Log expansion ideas separately from MVP tasks (use `dev-scope-deferral`).
7. If comments repeat policy conflicts across PRs, pause and request human decisions before more edits.
8. When the user revises concrete product constraints, update the PRD and implementation checklist before coding so execution doesn't follow a stale draft.
