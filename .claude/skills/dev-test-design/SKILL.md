---
name: dev-test-design
description: >-
  Design the smallest correct proof for a change — choose a testing strategy,
  turn it into one minimal verification plan, pin down disconfirming-check
  invariants, and assess whether coverage on what changed earns trust. Four
  modes — `strategy` (what's the right way to prove this?), `design` (turn one
  diff/bug/feature into one minimal proof plan), `invariants` (define + enforce
  functional/perf/operational/minimality invariants), `coverage` (diff-aware
  trust assessment). Triggers on "what's the right way to prove this", "design
  tests for this change", "are these tests catching anything", "is this enough
  proof", "define invariants for this work", "trust assessment on the changed
  code". Do NOT trigger for actually running tests (use the project's test
  runner). Do NOT trigger for bug investigation (use `dev-investigate`). Do NOT
  trigger for whole-repo coverage ratcheting — this skill is diff-aware, not
  codebase-wide.
version: 0.1.0
category: Troubleshooting
display_name: Test Design
tagline: Design the smallest correct proof for a change.
packs:
  - dev-pack
icon: 'phosphor:TestTube'
when_to_use: >-
  Reach for this when the question is *how do we actually prove this works* — choosing a
  testing strategy, turning a change into a minimal proof plan, pinning down invariants, or
  judging whether your coverage earns trust.

  Four modes — `strategy` (master orchestrator: what's the right way to prove
  this?), `design` (turn one diff/bug/feature plan into one minimal proof plan),
  `invariants` (define + enforce functional/perf/operational/minimality
  invariants with disconfirming checks), `coverage` (diff-aware trust
  assessment: do we trust the proof on what changed?).
modes:
  - name: strategy
    job: What's the right way to prove this change?
  - name: design
    job: Turn one diff / bug / feature plan into one minimal proof plan.
  - name: invariants
    job: Define + enforce invariants with disconfirming checks.
  - name: coverage
    job: 'Diff-aware trust assessment: do we trust the proof on what changed?'
---

# dev-test-design

## Purpose

The dev-* cluster has lots of skills that *use* tests (dev-investigate, dev-review, dev-PR), but none that **design** them. This is that skill. The job: pick the right proof shape, turn it into the smallest plan that actually buys confidence, and assess whether existing tests trust-justify the change.

The cluster's testing methodology lives here, principle-first.

## Operating principles (apply to all modes)

These are the core ideas. The workflow adapts to the situation; these stay constant.

- **The smallest proof that actually buys confidence.** Generic TDD advice produces busywork. Explicit proof design produces trust.
- **Disconfirming checks for medium+ risk work.** A test that can't fail when the bug is present is theater. Every medium+ risk plan includes at least one check that fails if the fix didn't actually solve the problem.
- **Production boundary shape over convenience mocks.** When testing DB-backed adapters or HTTP routes, model the live boundary. Mock-heavy tests pass for the wrong reasons.
- **Trust by behavior, not by line-count.** Coverage percentage hides which behaviors are actually defended. Always name the behaviors a number describes.
- **Misleading tests are a trust failure, not partial credit.** Skipped, flaky, stale, snapshot-only, or no-op tests get classified honestly — `quarantined` or `misleading`, not "we have coverage."
- **If root cause isn't clear, prefer temporary observability before permanent test expansion.** Don't write a hardened test to defend behavior you don't yet understand.
- **Production-executed-but-unproved beats easy-percentage-wins.** Ranks the smallest next proof by what changed code is actually running in prod without coverage, not by how much you can add to the score.
- **For bug fixes, fail-first or before/after differential proof when practical.** A green test on a fixed bug is weaker than a test that was red before the fix and green after.
- **Pre-production canonical bias.** For not-yet-launched features, prefer one canonical test pattern over hybrid compatibility tests that preserve dual happy paths.

## Modes

Four modes. Pick by the question being asked.

| Mode | Question being asked | When to use |
|---|---|---|
| `strategy` | "What's the right way to prove this?" | Top-level routing. Bug, polish, feature, refactor, migration — pick the proof shape before designing. |
| `design` | "What's the minimal proof plan for this specific diff/bug/feature?" | After the strategy is clear, narrow into one verification plan. |
| `invariants` | "What must remain true after this change, and how do we prove it?" | Medium+ risk work. Functional / performance / operational / minimality / safety invariants with disconfirming checks. |
| `coverage` | "Do we trust the proof on what changed?" | After tests exist (yours or someone else's). Diff-aware trust mapping. |

Modes can be chained: `strategy` → `design` → `invariants`. Or used individually. Default modes order in a typical workflow:

- New feature/refactor → `strategy` then `design` (and `invariants` for medium+ risk)
- PR review / shipping decision → `coverage`
- Pressure-testing existing tests → `coverage` followed by handoff to `dev-investigate mutation-scout`

See:
- `modes/strategy.md` — testing-expert content (top-level proof routing)
- `modes/design.md` — test-design-architect content (one diff → one minimal plan)
- `modes/invariants.md` — invariant-proof-gate content (define + enforce invariants)
- `modes/coverage.md` — productive-coverage content (diff-aware trust assessment)

## Cross-skill handoffs

- **`dev-investigate triage-and-fix`** — when a bug investigation needs a proof shape decided.
- **`dev-investigate mutation-scout`** — pressure-test whether existing tests catch realistic mistakes (the natural follow-on to `coverage` mode).
- **`dev-fresh-eyes`** — for skeptical critique of a proof plan before implementation.
- **`dev-PR`** — pulls in coverage/trust verdicts when authoring the PR body.
- **`dev-review checkpoint` / `dev-review ship-gate`** — consume `coverage` output to gate ship readiness.
- **`dev-scope-deferral`** — when this skill surfaces test gaps that are real but out-of-scope for the current change.

## Hard rules

- **Never default to generic TDD advice.** "Write tests" is not a plan; "write a fail-first test for behavior X with oracle Y" is.
- **Never count snapshot-only or mock-heavy tests as strong proof for stateful, async, or contract changes.**
- **Never report a coverage score without naming what behaviors it hides.**
- **Skipped, flaky, stale, no-op tests are `misleading` or `quarantined`** — not "partial credit."
- **For medium+ risk diffs, require at least one disconfirming check.** No exceptions.
- **Browser / E2E proof only counts when the test demonstrably crosses the changed branch or contract.**
- **Don't test what is too cheap to break.** Explicit `What not to test` is part of every plan.

## Distinct from adjacent skills

- **`dev-investigate`** investigates and fixes bugs; it consumes proof plans from this skill but doesn't design them.
- **`dev-investigate mutation-scout`** pressure-tests existing tests via mutation. dev-test-design designs them in the first place.
- **`dev-review`** reviews changes and uses coverage output but doesn't author the proof plan.
- **`dev-fresh-eyes`** critiques plans (including test plans) but doesn't author them from scratch.

## Templates

- `templates/proof-plan.md` — the minimal proof plan shape (Behavior claim / Primary risk / Smallest proof boundary / Primary mode / Oracle / Disconfirming check / Minimal artifacts / What not to test / Done signal)

## References

- `references/input-mode-playbook.md` — diff vs bug-report vs feature-plan input shapes
- `references/minimal-proof-rubric.md` — what counts as minimal-but-credible
- `references/trust-rubric.md` — verdict scale (verified / adequate / heuristic / unknown / misleading / quarantined) with examples
- `references/invariant-contract.md` — invariant categories (functional / performance / operational / minimality / safety) and disconfirming-check shape
