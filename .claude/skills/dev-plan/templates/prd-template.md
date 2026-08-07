# PRD: {{TITLE}}

## Metadata

- PRD ID: `{{PRD_ID}}`
- Date: `{{DATE}}`
- Type: `{{TYPE}}` (`bugfix` | `feature` | `refactor`)
- Branch: `{{BRANCH}}`
- Base branch: `{{BASE_BRANCH}}`
- Storage: `local` (gitignored at `.local/dev-plan/prd/`) | `draft` (lives at `tasks/prd/`, removed before final push)
- File path: `{{PLAN_PATH}}`

## 1. Problem Statement

- What user/system problem are we solving?
- What concrete symptom proves this matters now?

## 2. Existing Pattern Inventory

> Required before proposing changes. List actual files, not "TBD".

- Existing files/patterns to mirror:
  - `path/to/example`: why this is the preferred pattern
  - `path/to/example`: what should be reused
- Existing tests to mirror:
  - `path/to/test`: pattern to copy

## 3. Branch/PR Overlap Check

Run:
```bash
gh pr list --base "{{BASE_BRANCH}}" --state open --json number,title,headRefName --jq '.[] | "\(.number) \(.headRefName): \(.title)"'
```

For file-level overlap on a specific PR:
```bash
gh pr view <number> --json files --jq '.files[].path' | sort > /tmp/pr-<num>-files.txt
git diff --name-only "origin/{{BASE_BRANCH}}" | sort > /tmp/branch-files.txt
comm -12 /tmp/pr-<num>-files.txt /tmp/branch-files.txt
```

Result summary:
- [ ] No overlap with open PR branches
- [ ] Overlap found and mitigated (list PR numbers and file paths below)
  - PR #...: files: ..., mitigation: ...

## 4. MVP Scope

- **In scope:**
  1.
  2.
- **Out of scope:**
  1.
  2.

## 5. Worst-Case Failure Modes

1. Trigger:
   - Impact:
   - Mitigation:
2. Trigger:
   - Impact:
   - Mitigation:

## 6. Failing Tests First (RED)

> Add tests *before* implementation. Tests must fail meaningfully — not just exist.

- [ ] Test: `<path/to/test>` — covers `<edge case>`
- [ ] Test: `<path/to/test>` — covers `<edge case>`

## 7. Minimal Implementation Plan (GREEN)

> Smallest fix that makes the failing tests pass. Don't expand scope mid-implementation.

- Step 1:
- Step 2:
- Step 3:

## 8. Verification (VERIFY)

- [ ] Targeted test suite passes
- [ ] Nearby regression checks pass
- [ ] Manual scenario verified (if applicable)
- [ ] Proof captured: `<artifact / log / screenshot path>`

## 9. Open Questions

- (...)

## 10. Deferred / Follow-up

> Items intentionally not in this PRD. Capture via `dev-scope-deferral` if they need durable tracking.

- (...)
