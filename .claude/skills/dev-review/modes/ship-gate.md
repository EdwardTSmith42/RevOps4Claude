# Mode: ship-gate

Part of the `dev-review` skill. Selected when the user wants pre-release reliability triage with an explicit ship-or-no-ship verdict — phrasings like "Run the ship gate," "Pre-release reliability check," "Does this PR ship safely?", "Should I ship this?"

## Job

Compare a change against the correct baseline, sync with latest base, run focused reliability analysis, answer the 4 mandatory PR-diff risk questions, classify findings by severity (S0/S1/S2/S3) and disposition (Blocking / Non-blocking / PARK / REVERT), and issue a ship verdict (SHIP / SHIP WITH CONDITIONS / NO-SHIP).

## Scope adaptation

Per cluster design (`../references/scope-adapter.md`), `ship-gate` adapts beyond PR-only:

- **PR scope (default):** compare against PR base (`origin/develop` if base is develop; otherwise `origin/<baseRefName>` for PR-to-PR).
- **Branch scope:** compare current branch against `origin/develop` (or user-named base).
- **Commit-range scope:** compare commit range (e.g., last 5 commits) against the branch base.
- **Single-commit scope:** compare HEAD against HEAD~1 (or against the rebase base if mid-rebase).

When the changed surface is large (>1 disjoint risk surface AND the surface is too large to reason about together — soft heuristic), apply sub-agent fanout per `scope-adapter.md`: each subagent gets a full diff summary + their assigned slice in detail; parent reconciles findings.

## Run

### 1. Confirm scope and baseline

```bash
# For PR scope:
TARGET=331  # PR number
gh pr view "$TARGET" --json number,title,url,baseRefName,headRefName,updatedAt,files,comments,reviews
BASE_REF="$(gh pr view "$TARGET" --json baseRefName --jq .baseRefName)"
BASELINE="origin/$BASE_REF"

# For branch / commit scope:
# Use git rev-parse / git log / git diff to identify scope explicitly.
```

State the scope and baseline up front: "Validating <scope> against <baseline>, commit SHAs pinned: <head>...<base>."

### 2. Sync with latest base, handle conflicts explicitly

```bash
git fetch origin --prune
if [ "$(git rev-list --count HEAD..origin/develop)" -gt 0 ]; then
  git merge --no-edit origin/develop || true
fi
```

**If conflicts exist, stop and ask the user how to proceed.** List conflicting files. Don't auto-resolve.

### 3. Analyze diffs and nearby source context

```bash
gh pr diff <num>
gh pr diff <num> --name-only
git diff <baseline>...HEAD
git show <commit>
rg <pattern> <changed-files>
```

For non-PR scope, use `git log --oneline <baseline>..HEAD` and `git diff <baseline>...HEAD` directly.

### 4. Answer the 4 mandatory PR-diff risk questions

**All 4 are always answered.** When a question doesn't apply, the answer is "not applicable + reason." See `../references/diff-risk-questions.md`.

1. What are the unintended consequences of these changes that could break all sorts of stuff?
2. Are there any performance issues, memory leaks, race conditions, or other issues of that nature?
3. Is this PR overengineered? Are we making bad choices? Or are these common issues that just need a fine touch?
4. Should we park any aspect of this (use scope-deferral) or revert back to original code in order to make it safer to ship?

### 5. Classify findings by severity and disposition

Severity (per `../references/reliability-rubric.md`):
- **S0 Blocker** — ship-stopping. Likely crash, boot failure, data corruption, security impact.
- **S1 High** — major reliability regression with realistic trigger and high user impact.
- **S2 Medium** — recoverable defect or edge-case failure with bounded blast radius.
- **S3 Low** — minor inconsistency or maintainability risk; usually non-blocking.

Disposition (per `../references/ship-no-ship-vocabulary.md`):
- **Blocking** — must fix before ship.
- **Non-blocking** — safe with follow-up issue.
- **PARK** — real concern but not introduced/touched by this change; out of scope.
- **REVERT** — unacceptably high risk; cannot be safely hardened in-scope.

For each finding, include: file path + line reference, trigger condition, user/system impact, why the diff introduces or fails to prevent the risk.

### 6. Apply two-phase discipline

- **Phase A: read-only analysis** — surface all findings before any code change.
- **Phase B: test-first remediation** — for each blocking issue:
  1. Write a realistic failing test that reproduces the bug.
  2. Run the test and confirm it fails before code changes.
  3. Implement the smallest robust fix.
  4. Re-run the test and confirm it passes.
  5. Run nearby regression tests.

**Never skip the failing-test proof step.** Don't write placeholder tests.

### 7. Re-evaluate ship gate after fixes

Apply the close-out gate (`../references/close-out-gate.md`):
1. No `Blocking` crash/deploy risks remain.
2. No unresolved high-severity review thread is ignored without explicit rationale.
3. Every fixed blocker has a real failing test that now passes.
4. Rollback path is clear for deploy-facing changes.
5. All four PR-diff risk questions are answered with changed-file evidence.
6. Any `PARK` or `REVERT` call is explicit and justified.

### 8. Produce verdict

Use `../templates/ship-gate-verdict.md`. Verdict options (per `../references/ship-no-ship-vocabulary.md`):
- **SHIP** — no unresolved blocker/high risk; coverage adequate.
- **SHIP WITH CONDITIONS** — only S2/S3 remain with explicit follow-ups (invoke `dev-scope-deferral` for each).
- **NO-SHIP** — any S0 exists or unresolved S1 lacks mitigation.

For PARK items, invoke `dev-scope-deferral` skill to capture each as a deferred-investigation note (don't bloat the verdict with follow-up details).

## Hard rules

- **Base conclusions on diff evidence and direct call-site impact only.** Don't expand into unrelated legacy debt during release-readiness.
- **Do not claim runtime proof you did not execute.**
- **Do not write placeholder tests.** Tests must represent real failure conditions and meaningful assertions.
- **Always prove failing-then-passing for new remediation tests.**
- **If conflicts appear during develop sync, ask user before continuing.**
- **Answer all four mandatory PR-diff risk questions before final verdict.**
- **For PARK or REVERT calls:** explicit rationale required.
- **User-attribution wording:** when reporting user counts derived from your error-reporting system, default `Affected Users: unknown (not tracked)` unless attribution is confirmed (cross-reference `../../dev-investigate/references/user-attribution-rule.md`).

## Mode-specific references

- `../references/diff-risk-questions.md` (required — the 4 mandatory questions)
- `../references/reliability-rubric.md` (severity + failure-mode prompts + crash/deploy + coverage map + ship-gate heuristic)
- `../references/ship-no-ship-vocabulary.md` (verdict + PARK/REVERT)
- `../references/scope-adapter.md` (variable scope + fanout)
- `../references/close-out-gate.md` (6-item gate)
- `../templates/ship-gate-verdict.md`

Cross-cluster:
- `../../dev-investigate/references/user-attribution-rule.md` (Affected Users wording)
- `../../dev-investigate/references/pr-overlap-check.md` (overlap with open PRs / recent merges)

## Output

See `../templates/ship-gate-verdict.md`. Required sections:

- PR/scope selection + baseline
- PR-Diff Risk Questions (all 4 with diff evidence)
- Worst-Case Failure Modes
- Crash/Deploy Risk List
- Missing Test Coverage Map
- Ship/No-Ship Gates
- Final verdict + minimum fixes for NO-SHIP→SHIP

## Design Rationale

Mode-specific notes:

- **All 4 PR-diff risk questions are mandatory** — the discipline is forcing the enumeration. Even when a question doesn't apply, the agent says so explicitly with reason. 
- **Two-phase: read-only then test-first remediation** — read-only first prevents "I'll just fix this real quick" drift that contaminates the analysis.
- **"Only analyze changed code paths plus immediate call-sites needed to prove impact"** — scope discipline; matches investigate's "expand only to" pattern.
- **PARK / REVERT vocabulary** is distinct from FIX_NOW / DEFER (used in `dev-investigate` triage). PARK = real concern, out-of-scope-for-this-ship; REVERT = unsafe, can't be hardened. Sharper than just "defer" because it captures the unship-this-slice option.
- **"Never skip the failing-test proof step"** — anti-placeholder-test rule.
- **Ship gate heuristic codified** in `reliability-rubric.md`: NO-SHIP if any S0 or unresolved S1; SHIP WITH CONDITIONS if only S2/S3 with follow-ups; SHIP if no unresolved blocker/high.

