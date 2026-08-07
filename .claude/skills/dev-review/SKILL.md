---
name: dev-review
description: >-
  Review and assess code changes at any scope — commit, branch slice, PR, or
  portfolio of open changes. Picks the right lane (ship-gate verdict, milestone
  checkpoint, manifesto review, change-context brief, runtime smoke QA, or
  open-PR digest) for the situation. Triggers on "check this commit/branch/PR",
  "ship-readiness check", "milestone check", "manifesto review", "build me a
  brief for this change", "smoke-test this branch", "rank our open PRs". Adapts
  to scope size with sub-agent fanout for large changes (full diff summary +
  assigned slice in detail per subagent). Do NOT trigger for bug investigation
  (use `dev-investigate`), bug-fix PR interrogation (use `dev-investigate
  pr-interrogate`), or greenfield design questions (use `dev-fresh-eyes`). Do
  NOT trigger for cleanup/worktree hygiene (use `dev-clean-up` or
  `dev-stale-worktree-curator`).
version: 0.1.0
category: Troubleshooting
source-prompts:
  - review-expert.md
  - gh-pr-reliability-gate.md
  - milestone-review-loop.md
  - agentic-manifesto-review.md
  - pr-context-brief.md
  - branch-smoke-qa.md
  - open-pr-ship-readiness-digest.md
display_name: Code Review
tagline: 'Review changes at any scope — commit, branch, PR, portfolio.'
packs:
  - dev-pack
icon: 'phosphor:ChecksquareOffset'
when_to_use: >-
  Picks the right lane (ship-gate verdict, milestone checkpoint, manifesto
  review, change-context brief, runtime smoke QA, or open-PR digest) for the
  situation. Adapts to scope size with sub-agent fanout for large changes.
modes:
  - name: ship-gate
    job: Ship-readiness verdict on a change.
  - name: checkpoint
    job: Milestone smoke + regression sweep.
  - name: manifesto-review
    job: Review against the agentic-coding manifesto criteria.
  - name: brief
    job: Change-context brief for non-PR work (PR-bound briefs hand off to dev-PR).
  - name: smoke-qa
    job: Runtime smoke QA of a branch.
  - name: digest
    job: Ranked digest of open PRs.
---

# Check

## Purpose

One entry point for assessing code changes at any scope (commit / branch slice / PR / portfolio). The skill picks the right lane based on the user's intent and the scope of the change, then delegates to one of six modes. Underneath, modes share a common vocabulary for severity rubrics, ship-no-ship verdicts, sub-agent fanout, and output formatting — so reports compose cleanly across lanes.

## When to use

Pick a mode based on what the user is asking for:

- **`ship-gate`** — "Does this change ship safely?" / "Pre-release reliability check" / "Run the ship gate." Compare-to-base reliability triage with explicit verdict (SHIP / SHIP WITH CONDITIONS / NO-SHIP). Works on PR scope by default; broaden to commit-range / branch-slice via the scope-adapter.
- **`checkpoint`** — "Milestone checkpoint" / "Smoke + regression sweep" / "Decompose this monolithic file safely." Local progress commit + smoke gate 1 + regression review + monolith sweep + cleanup audit + smoke gate 2.
- **`manifesto-review`** — "Manifesto-guided review" / "Make this codebase easier to navigate" / "Review for legibility and trust layer." Review against the Agentic Coding Practices manifesto; surface 3-5 high-signal improvements.
- **`brief`** — "Build me a context brief for this change" / "Document this change for reviewers." Scope-adaptive: small bug-fix commit (technical-what + user-story-affected) → medium change (reviewer-facing narrative) → large change (+ architectural decisions + design decisions + manifesto-criteria evaluation).
- **`smoke-qa`** — "Smoke-test this branch" / "QA the changed routes" / "Run the diff-aware UI smoke." Diff-aware route inference + browser-use validation.
- **`digest`** — "Rank our open PRs" / "Daily ship-readiness digest" / "Which PRs are ready to ship today?" Portfolio-scoped ranked queue across many open changes.

If the user's request is unclear or fits multiple modes, ask one targeted question rather than guessing.

## Picker logic (the review-expert classification)

When the user asks for "review" without naming a specific mode, classify:

1. **Target scope:** `file | files | commit | commit_range | pr | branch | existing_slice`
2. **Review goal:** `correctness | ship-readiness | regression-risk | cleanup | existing-code audit | legibility`
3. **Map to mode:**
   - `pr` + `ship-readiness` → `ship-gate`
   - `commit | commit_range` + `regression-risk | cleanup` → `checkpoint`
   - any scope + `legibility | navigation | trust-layer` → `manifesto-review`
   - any scope + `documentation` or "write me a brief" → `brief`
   - `branch` + `runtime-validation | UI` → `smoke-qa`
   - portfolio + "rank ship-readiness" → `digest`
4. **Choose the narrowest scope that can answer the question.** Broad review is a warning surface, not the default proof surface.
5. **Add supporting lanes only when they close a named blind spot.** See `references/lane-selector.md`.
6. **Return findings first, then validation/trust, then next step.**

## Inputs

Mode-dependent. Common across modes:

- **Scope identifier** — commit hash / branch name / PR URL or number / commit range / file or directory path / "current branch."
- **Optional review goal** — when invoked without explicit goal, the picker logic infers from scope and phrasing.
- **Optional invocation flags** — e.g., explicit fanout request, manifesto rubric scope, brief authoring level.

## Run

1. **Mode selection.** Map the user's request to one mode using the When-to-use guide and picker logic above.
2. **Apply scope adapter** — see `references/scope-adapter.md`. Decide whether the change fits direct review or warrants sub-agent fanout (full diff summary + assigned slice in detail per subagent, with parent reconciliation).
3. **Load shared references** that apply across modes:
   - `references/scope-adapter.md` — every mode except `digest`.
   - `references/lane-selector.md` — supporting-lane decisions.
   - cross-cluster reference at `../dev-investigate/references/output-format-contract.md`.
   - Plus mode-specific references (each mode names what it loads).
4. **Run the mode.** Mode files in `modes/` contain the run logic. Preserve craft moves verbatim.
5. **Compose with siblings.** When the work surfaces:
   - Adjacent improvements to defer → invoke `dev-scope-deferral` skill.
   - A durable lesson worth capturing → invoke `dev-self-improvement-loop` skill.
   - A "where are we now?" reorient need → invoke `dev-checkpoint` skill.
   - Cross-system updates to post → hand off to your bug-comms workflow (if you maintain one) when the change is bug-related; otherwise post the update yourself, one message per destination.

## Output

Each mode produces its own output shape; common across modes:

- **Plain language first, technical detail second.** Lead with what the user/business cares about; raw IDs and signatures secondary.
- **Confidence stated explicitly.** Findings carry severity (S0/S1/S2/S3 from `references/reliability-rubric.md`) and confidence.
- **No claim of 100% certainty.** Always include "what this cannot be" (ruled out by evidence) and "what remains unknown."
- **Plain file paths for local artifacts;** clickable URLs only for web resources (PRs, issues in your project tracker or error-reporting system).
- **Affected Users wording**: cross-reference `../dev-investigate/references/user-attribution-rule.md` — default `unknown (not tracked)` unless attribution is explicitly confirmed.
- **PARK / REVERT classifications** for findings out-of-scope or unmitigatable in the current change.

## Design Rationale

Why this skill is structured the way it is:

- **One category skill, six modes** — the legacy source prompts cross-referenced each other heavily and shared vocabulary (severity rubrics, ship-no-ship verdicts, scope discipline). One unified entry point removes coordination overhead while keeping mode boundaries crisp.
- **Variable-scope by design.** The user's central design ask: not PR-only, but adaptive to commit / branch slice / PR / portfolio. `references/scope-adapter.md` codifies the heuristics; every per-change mode loads it.
- **Sub-agent fanout when surface is large.** The chosen architecture: hybrid — each subagent gets a full diff summary + their assigned slice in detail. Better cross-cutting awareness than slice-only fanout; lighter than full-diff-per-subagent.
- **Picker logic in SKILL.md, not a separate `triage` mode.** review-expert's classification + lane-picker logic lives at the category level. The mode files focus on heavyweight workflows; the lightweight "what review do I need?" path resolves at the router level.
- **The 4 mandatory PR-diff risk questions stay mandatory.** Always all 4 (the discipline is forcing the enumeration). Even when a question doesn't apply, the answer is "not applicable + reason." See `references/diff-risk-questions.md`.
- **`brief` mode is scope-adaptive across a wide range** (by design): small bug-fix commit (technical what + user story) → medium change (full reviewer-facing narrative) → large change (+ architectural + design decisions + manifesto-criteria evaluation). Different profiles within one mode.
- **The Agentic Coding Practices manifesto is a shared reference**, used both by `manifesto-review` mode (primary consumer) AND by `brief` mode at large scope (cross-load for documentation/readability evaluation). Two-skill threshold met inside the cluster.
- **Cross-cluster references** — `user-attribution-rule.md`, `output-format-contract.md`, `pr-overlap-check.md` live in the `dev-investigate` cluster and are cited from `dev-review` modes by absolute path. Standalone format constraint; future enhancement could promote to a higher-level shared location.
- **PARK / REVERT vocabulary** for ship-gate findings — distinct from FIX_NOW / DEFER. PARK = real but not-required-to-ship-this-PR (defer to follow-up). REVERT = unsafe and can't be hardened in scope.

## References

Shared across modes:

- `references/scope-adapter.md` — variable-scope handling + sub-agent fanout heuristics
- `references/lane-selector.md` — supporting-lane menu (when to add static reasoning / tool / proof / runtime / challenger)
- `references/reliability-rubric.md` — severity scale (S0/S1/S2/S3), failure-mode prompts, crash/deploy checklist, ship-gate heuristic
- `references/diff-risk-questions.md` — the 4 mandatory PR-diff risk questions
- `references/ship-no-ship-vocabulary.md` — SHIP / SHIP WITH CONDITIONS / NO-SHIP / PARK / REVERT
- `references/agentic-coding-manifesto.md` — the manifesto rubric (legibility / trust layer / contract tests / honest gap tracking)
- `references/brief-authoring-standard.md` — ~30 rules for change-context briefs and reviewer-facing PR bodies
- Pre-open gate: cited from `../dev-PR/references/cycle-checklist.md` (dev-PR owns everything PR-shaped)
- `references/decomposition-playbook.md` — monolith decomposition test-first guardrail
- `references/regression-review-checklist.md` — milestone regression review pass

Cross-cluster (cited via sibling-skill path from `dev-investigate`):

- `../dev-investigate/references/output-format-contract.md` — plain-language-first / file-path / URL rules
- `../dev-investigate/references/user-attribution-rule.md` — Affected Users wording + error-reporting rules
- `../dev-investigate/references/pr-overlap-check.md` — overlap with open PRs / mainline merges before opening new fix
- `../dev-investigate/references/severity-rubric.md` — P0–P3 (cluster-shared severity language; reliability-rubric.md is more specific to PR-diff)

## Templates

- `templates/ship-gate-verdict.md` — ship-gate output structure (used by `ship-gate` mode)
- `templates/checkpoint-report.md` — milestone checkpoint output (used by `checkpoint` mode)
- `templates/manifesto-review-output.md` — manifesto review output (used by `manifesto-review` mode)
- PR body shape: `../dev-PR/templates/pr-body.md` (dev-PR owns it; brief mode hands PR-bound work there)
- `templates/change-brief.md` — per-branch context brief structure (used by `brief` mode)
- `templates/smoke-qa-report.md` — smoke QA output (used by `smoke-qa` mode)
- `templates/digest-output.md` — portfolio digest index + per-PR brief shape (used by `digest` mode)

## Examples

`examples/` is empty for v0.1. Per skillify's example-rules, single examples mis-train the skill more than missing examples do — populate from real Phase 5 verification runs once 5+ strong exemplars are available.

## Related skills

- `dev-investigate` — bug-investigation cluster. Use `dev-investigate pr-interrogate` for bug-fix PR verdicts (rootness classification + differential proof); use `dev-review ship-gate` for general PR reliability triage. They overlap on overlap-check; both cite the shared `pr-overlap-check.md` reference.
- `dev-fresh-eyes` — invoke when a checkpoint reveals a plan-shape concern, or when a `manifesto-review` recommendation deserves a skeptical pre-implementation pass.
- `dev-scope-deferral` — invoke from any check mode when adjacent improvements surface (PARK items in ship-gate; deferred decomposition in checkpoint; etc.).
- `dev-self-improvement-loop` — invoke after a check run that surfaces a durable pattern worth formalizing.
- `dev-checkpoint` — sometimes invoked alongside `dev-review checkpoint` when the user wants both verification AND state reorientation.
- `dev-clean-up` — invoke when the post-check finding includes "and clean up the churn." Distinct skill, distinct trigger.
- `browser-use` — invoked by `check smoke-qa` for the actual browser ops.
- If you maintain a separate cross-system bug-comms workflow, `ship-gate` / `brief` will hand off to it for bug-related changes that need posting across task tracker / chat / support system.

An independent reviewer can be invoked as a challenger lane from `ship-gate` and `checkpoint` — a fresh-context subagent, or a separate coding tool / model if you've wired one up. The lane stays the contract; the reviewer is the implementation.

## First-time setup

This skill assumes a GitHub-hosted repo and the `gh` CLI for PR-scoped operations (`ship-gate`, `digest`, `brief` at PR scope, `pre-open-checklist`):

- Install: `brew install gh` (or platform equivalent).
- Authenticate: `gh auth login` and confirm `gh auth status` succeeds.

The `smoke-qa` mode delegates to the `browser-use` skill — install it separately if you plan to run that mode.

Modes that link out to a project tracker, support system, or error-reporting tool (digest, brief, ship-gate impact lines) describe them in abstract terms; adapt the link patterns to whatever your team uses.
