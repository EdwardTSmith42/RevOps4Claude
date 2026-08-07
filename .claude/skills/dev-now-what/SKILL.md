---
name: dev-now-what
description: >-
  Pressure-test bugs, review findings, and "what now?" requests to identify the
  real problem, distinguish symptoms from upstream causes, scan for shared
  helpers or duplicated logic that should be unified, and return the smallest
  correct implementation plan with proof. Triggers on "now what?", "what's the
  right way to handle this?", "we have these findings — what's the plan?", "this
  review surfaced X — figure out the fix shape", "figure out a plan for this."
  Do NOT trigger for greenfield design or feature scoping (use `dev-plan`). Do
  NOT trigger when there's already a confirmed root-cause hypothesis and the
  work is bug-shaped (use `dev-investigate triage-and-fix`). Do NOT trigger for
  skeptical critique of an existing plan (use `dev-fresh-eyes`).
version: 0.1.0
category: Troubleshooting
display_name: Now What?
tagline: Pressure-test findings into the smallest correct fix shape.
packs:
  - dev-pack
icon: 'phosphor:FlowArrow'
when_to_use: >-
  After a bug surface or review surface, use this to identify the *real* problem
  — distinguish symptoms from upstream causes, scan for shared helpers or
  duplicated logic that should be unified, and return the smallest correct
  implementation plan with proof.
---

# dev-now-what

## Purpose

Use this when the question isn't "write code right now" but "what is the real problem, what should we fix, and how should we shape the work?" — the bridge between findings and a plan.

This skill triggers on a particular state of ambiguity: review findings just landed, an incident report needs translation, a half-formed sense of "something is broken" needs to become a concrete fix shape. It is neither pure bug investigation (no confirmed reproduction yet) nor pure planning (no confirmed scope yet). It's the deliberate beat between them.

## Five operating defaults

These are the principles, not the workflow. The workflow adapts; these stay constant.

1. **Findings are hypotheses, not truth.** A review comment, a Sentry signal, a customer report, a failing test — all of them describe *something*. Whether they describe the *real* problem is the open question.
2. **Upstream / root-cause checks come before downstream patch plans.** Don't plan the fix at the symptom site until you've checked one or two layers upstream for shared helpers, contracts, state transitions, retry rules, cache rules, identity handoffs.
3. **One seam over bespoke copies.** If multiple code paths serve the same purpose, prefer unifying through one shared seam over patching three places independently.
4. **Keep the shipped fix narrow** unless the broader root cause is what actually makes the bug recur. Don't expand scope to feel thorough; expand only when narrow scope doesn't actually solve the recurring problem.
5. **Pre-production canonical bias.** For features and prototypes that are not live yet, prefer the best canonical solution over a minimal compatibility patch when the broader move is clearly better. Hybrid compatibility on pre-production code preserves wrong assumptions; fail-fast breakage during development surfaces them.

## Default output

Return a plan with these sections:

```markdown
## Problem Statement

## Symptom vs Root Cause

## Existing Seams and Reuse Opportunities

## Minimum Viable Change

## Verification

## Deferred Follow-ups
```

For pre-production work, **`Minimum Viable Change` means the smallest correct canonical design**, not automatically the smallest diff.

## Workflow

### 1. Restate the issue in plain language

- Who is affected?
- What concrete behavior is broken?
- What evidence triggered the question — bug report, review finding, test failure, runtime signal, customer report?

### 2. Treat each finding as provisional

For each finding or hypothesis surfaced so far:
- What exact failure does it describe?
- What must be true for that finding to be the *real* problem?
- Could it instead be a symptom of an upstream helper, contract, state transition, cache rule, retry rule, or identity handoff?

### 3. Run an upstream-first scan

- Check the nearest shared helper, boundary, or contract before planning a local patch.
- Check whether the same behavior exists at sibling call sites or sibling components.
- If two findings point into the same seam, plan them together before deciding on separate fixes.

### 4. Run a reuse and unification scan

This is the step that distinguishes this skill from generic bug triage.

Look for:
- Duplicated logic that serves the same purpose.
- One-off header construction, token retrieval, routing, state clearing, error classification that should be centralized.
- Helpers doing two jobs at once. Common smells:
  - `best-effort` plus `required` behavior in one helper
  - one-time event capture plus long-lived state synchronization
  - eager initialization plus lazy refresh
- Same UI surface implemented twice in different files because they "felt different."

Prefer unification only when the **semantics are actually the same**. If similar code should stay separate, name the reason explicitly. Don't force DRY when the two flows are superficially similar but semantically different.

### 5. Classify the issue shape

Use one of:
- **`root`** — fixing this seam should eliminate the observed bug *and* its close siblings
- **`symptom`** — this fixes the reported break, but the real cause is upstream
- **`adjacent`** — valid improvement or similar weakness, but not required to resolve the active problem

### 6. Choose the smallest correct fix scope

- **Expand to the root seam** when it is still low-risk and meaningfully reduces recurrence.
- **Stay narrow** when the root cause would require broader state-machine or architecture churn that isn't needed for the active incident.
- **For pre-production surfaces** (not yet live) — explicitly ask whether a broader cleanup or redesign is the better canonical answer. Don't preserve hybrid compatibility unless a real requirement says the old path must survive. Prefer deleting obsolete paths, writing strong tests, letting incorrect assumptions fail now over carrying thousands of lines of legacy maintenance forward.
- **If you stay narrow**, preserve the stronger follow-up explicitly — invoke `dev-scope-deferral` rather than hand-waving it away.

### 7. Define invariants before finalizing the plan

- What must remain true after the change?
- For medium+ risk work, include at least one **disconfirming check** — something that would fail if the fix didn't actually solve the problem.
- Prefer proof tied to the actual seam, not only UI-level acceptance.

### 8. Build the plan around proof

- Name the files or helpers to change.
- Name the tests or scenario proofs that confirm the root cause is actually fixed.
- Call out observability or replay checks only when they materially sharpen confidence.

### 9. Self-review pass on the plan

Before returning:
- Did the plan mistake a symptom for the cause?
- Did it miss a shared helper or sibling path?
- Did it over-generalize into refactor work that isn't required?
- Does the proof exercise the *real* failure mechanism, or just the aftermath?

Revise before delivering.

## What to check (a checklist)

- shared helpers, wrappers, interceptors, hook utilities
- duplicate code paths with the same purpose
- helpers whose contract changes depending on caller mode
- one-time lifecycle helpers also being used as state-sync helpers
- client/server contract seams
- retry, timing, stale-state, cache invalidation behavior
- logout/login/bootstrap handoffs
- "works in one surface, broken in another" drift
- whether tests prove the seam or only the aftermath

## Decision rules

- Prefer one helper for one purpose.
- If callers need different semantics, keep one shared core and thin mode-specific wrappers.
- Prefer explicit data flow over clever indirection.
- Don't force DRY when two flows are semantically different.
- If the root fix is materially riskier than the symptom fix, say so and split the work intentionally.
- For pre-production, optimize for the clean future happy path over temporary dual-path safety.
- Prefer fail-fast tests over silent compatibility shims for legacy code that should be removed before launch.
- If evidence is incomplete, return `unknown` plus the next validation step — don't pretend certainty.

## Hand-offs to adjacent skills

- **`dev-investigate triage-and-fix`** — once a confirmed root-cause hypothesis exists and the work is bug-shaped (reproduction + lane selection + proof). `dev-now-what` ends where the fix shape is decided; `dev-investigate` carries the implementation through.
- **`dev-investigate evidence`** — when the ambiguity is severe enough that you need full evidence-first investigation (support reports, logs, runtime traces) before any fix-shape decision.
- **`dev-fresh-eyes`** — once the plan exists, run skeptical critique before implementation.
- **`dev-plan scope` / `dev-plan architecture`** — when scope expands beyond one focused fix into milestone-level sequencing or system-shape decisions.
- **`dev-scope-deferral`** — for the `Deferred Follow-ups` section. Don't hand-wave deferred work; capture it.

## Hard rules

- **Don't jump from one review finding straight to one code edit.** That's the failure mode this skill exists to prevent.
- **Don't propose parallel bespoke fixes when one seam should own the behavior.**
- **Don't turn "same purpose" into a refactor excuse.** Unify only where behavior and ownership align.
- **Don't default to a minimal patch on pre-production surfaces** if that preserves a known-wrong architecture or leaves legacy code as an unofficial second happy path.
- **Don't skip explicit non-goals.**
- **Don't call a plan done until the proof strategy matches the risk.**

## Design Rationale

- **Distinct from `dev-investigate` and `dev-plan`.** dev-investigate assumes there's a confirmed bug to triage; dev-plan assumes you know what you're building. dev-now-what occupies the deliberate beat between findings and a plan, where the work shape is itself the open question.
- **Reuse / unification scan is the distinctive step.** Generic bug triage doesn't include it. This skill's value-add is making that scan a default, not an afterthought.
- **Output structure mirrors the workflow.** Six sections, in the order the workflow produces them. Stakeholders can read just `Symptom vs Root Cause` and `Minimum Viable Change` to get the call without the supporting work.
- **Pre-production canonical bias is encoded** because the most expensive bugs to fix come from compatibility shims preserved during prototyping that get cemented at launch. Better to break fail-fast during dev.

## Distinct from adjacent skills

- **`dev-investigate`** — bug-shaped lane selection + investigation + proof. Different central question: *how do we prove and fix this bug?*
- **`dev-plan`** — feature/scope shaping. Different central question: *what should we build?*
- **`dev-fresh-eyes`** — critique of an existing plan/draft. Different central question: *what's wrong with this plan?* The boundary in one line: now-what *forms* the plan; fresh-eyes *attacks* the plan. Consecutive beats in the delivery loop, not competitors.

> **Propagation note:** four of this skill's moves — root/symptom/adjacent classification, the disconfirming check, the `unknown` verdict, and the self-review pass — also live in `os-fresh-eyes` (personal-os pack) as domain-general craft. Both copies are kept deliberately (packs are self-contained); improvements to these moves in either skill should be propagated to the other when relevant.
