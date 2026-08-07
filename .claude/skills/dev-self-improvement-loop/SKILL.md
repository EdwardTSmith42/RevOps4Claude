---
name: dev-self-improvement-loop
description: >-
  Master self-improvement and process-learning orchestrator for turning concrete
  engineering friction, tool failures, user corrections, and repeat patterns
  into better skills, SOPs, references, wrappers, and follow-up work. Triggers
  when the user says "run the self-improvement loop", "let's capture what we
  learned", "this should become a rule", "turn this into a skill update", or
  after an insightful or frustrating moment when the real task is improving how
  we operate, not just solving the immediate code issue. Also invokable from
  inside other skills (e.g., `dev-review` cluster, `dev-investigate`) as a
  delegate-pattern after surfacing a durable pattern. Do NOT trigger for vague
  "we learned a lot" reflections without a concrete change target. Do NOT
  trigger as a substitute for actually solving the immediate engineering
  problem.
version: 0.1.0
display_name: Self-Improvement Loop
tagline: 'Turn friction, corrections, and patterns into better skills and SOPs.'
category: Planning
packs:
  - dev-pack
icon: 'phosphor:ChartLineUp'
when_to_use: >-
  Master self-improvement and process-learning orchestrator. Use after an
  insightful or frustrating moment when the real task is *improving how we
  operate*, not just solving the immediate code issue.


  Also invokable from inside other skills (e.g., `dev-review` cluster,
  `dev-investigate`) as a delegate-pattern after surfacing a durable pattern.
---

# Self-Improvement Loop

## Purpose

Use this loop when the question is not only "what happened?" but "what should we change in our internal system so this goes better next time?"

Capture learnings and optimizations and be willing to make small tweaks to continuously improve how we operate. This is a meta-skill — it does not replace normal domain work. It improves the experts, skills, references, SOPs, wrappers, templates, and follow-up habits around that work.

## When to use

Use this loop especially after:
- **User corrections** (the user told us we did something wrong)
- **Repeated tool or wrapper failures**
- **Investigations that went too broad or too narrow**
- **Proof / test runs that exposed missing evals or weak validation**
- **Successful patterns that clearly deserve to become repeatable**
- **Incidents where similar failures may exist in adjacent surfaces**
- **Moments where the code or architecture led us astray from its actual intention**
- **Times where we had to rewrite or retry commands**

Triggered by the user manually, OR invokable from inside other skills as a delegate-pattern when a durable pattern surfaces.

## Default outputs

- **Trigger and evidence** — what surfaced this
- **Failure or success pattern** — what's the durable learning
- **What should change now** — the proposed system change
- **Change target** — which existing artifact to update (or new one to create, only as last resort)
- **Immediate patch or doc update** — the actual change applied
- **Follow-up todo or investigation** — what's left, captured via `dev-scope-deferral` if appropriate
- **Validation plan** — how we confirm the improvement helps
- `No durable lesson` when appropriate

## Workflow

### 1. Classify the trigger

- `user correction`
- `tool or wrapper failure`
- `scope miss`
- `proof gap`
- `repeat code pattern`
- `successful pattern worth formalizing`
- `adjacent risk worth follow-up`

### 2. Gather the smallest evidence set

Just enough to explain the lesson:
- Commands, logs, traces, test results.
- Diffs or review findings.
- Task artifacts such as a repo-local `tasks/todo.md` and `tasks/lessons.md`, or your cross-project lessons file (if you keep one).
- Execution receipts when they exist.
- Relevant skill docs, references, templates, or wrappers.

### 3. Decide whether the lesson is durable

- **One-off confusion is not enough** unless severity is high.
- **Repeated friction across runs or tools is strong evidence.**

If the evidence is weak, **say `no durable lesson` and stop.** Don't capture noise.

### 4. Choose the smallest correct change target (in this order)

1. **Existing `SKILL.md`** (most preferred — improve what exists)
2. **Existing reference / template**
3. **Existing SOP or lessons file** (repo-local `tasks/lessons.md`, or your cross-project lessons file if you keep one)
4. **Existing wrapper / script**
5. **Local package install or update**
6. **Follow-up todo or investigation** (via `dev-scope-deferral` skill)
7. **Only then: a new specialist skill** (last resort)

This is the **change-target hierarchy.** Forcing "improve what exists" before "create new" is anti-skill-explosion discipline.

### 5. Produce one concise improvement brief

A short prose brief, not a sprawling doc. Cover:
- What the trigger was + evidence.
- The pattern (failure or success).
- The proposed system change.
- Which target (per the hierarchy above).
- Risk / scope of the change.
- Validation plan.

### 6. Apply the smallest clear update now

If the change is **obvious AND low-risk**, apply it now (e.g., update an existing SKILL.md negative trigger; add one bullet to a reference doc; tighten one rule).

If higher risk OR pattern may exist elsewhere OR change requires a decision: **ask the user** instead of silently broadening scope.

### 7. Validate the improvement

- **Structural validation** for docs/skills (frontmatter valid; cross-references resolve; live-reload picks up).
- **Smoke use** of the updated skill or wrapper (run it on a representative input).
- **Targeted proof** if a script or guard changed.

## What good improvement looks like

- Turns a concrete failure or standout success into a reusable rule, guard, or tool change.
- Updates the system that produced the error, not only the narrative about it.
- Preserves counterexamples, edge cases, and failure signatures.
- Makes it so we don't have to cycle as many times to find the correct approach next time.
- Documents gotchas and other learnings.
- Updates documentation, skills, scripts, and other assets.
- Creates explicit next steps with owners and landing zones.
- Distinguishes `verified`, `heuristic`, `unknown`, and `no durable lesson`.

## What bad improvement looks like

- Vague "we learned a lot" summaries.
- Blame without a system change.
- Documentation churn with no behavior change.
- **Immediate invention of a new skill** when an existing one should be tightened.
- Giant follow-up lists with no scope or owner.
- Treating one anecdote as a universal law without checking repeatability.

## Storage and landing zones

Prefer updating an **existing landing zone** over creating a new one:

- **Durable repo-local guardrails** → `<repo>/tasks/lessons.md` (when repo-specific)
- **Durable cross-project lessons** → your cross-project lessons file or auto-memory system, if you keep one
- **Active local follow-ups** → `<repo>/tasks/todo.md`
- **Private reusable SOP** → your personal SOP collection
- **Domain-specific doctrine / reference / template** → the owning skill's `references/` or `templates/` directory
- **Process verification or orchestration history** → workspace-local `execution-receipts/` (when applicable)

**Do not create a competing memory log for the same type of learning.** Anti-fragmentation rule.

## Subagent guidance

Use subagents when the evidence spans multiple domains:
- One lane inspects wrapper / tool behavior.
- One lane inspects current expert docs and SOPs.
- One lane checks whether the same issue likely exists elsewhere.

Split by **disjoint risk surface**, not arbitrary file chunks (per `scope-adapter.md` from `dev-review` cluster — same principle).

## Hard rules

- **Prefer system or tooling changes over "humans should remember better."**
- **Keep code follow-up separate from process follow-up.**
- **Default to one durable lesson and one next step**, not a brainstorm dump.
- **If the evidence is weak, say `no durable lesson` and stop.**
- **If the same issue may exist elsewhere, record a bounded follow-up rather than expanding the current task without consent.**
- **Improvement loops should reduce future friction, not create new ceremony.**

## Cross-skill invocations

This skill is invokable from inside other skills as a delegate-pattern when a durable pattern surfaces:
- From `dev-review` cluster modes (after a checkpoint or ship-gate exposes a recurring weakness).
- From `dev-investigate` modes (after a war-story-derived pattern surfaces).
- From `dev-fresh-eyes` (after a recurring critique pattern emerges).

## Design Rationale

- **"Prefer system or tooling changes over 'humans should remember better'"** — the core principle. Don't write rules that depend on memory.
- **The change-target hierarchy** (existing SKILL → reference → SOP → wrapper → install → follow-up → only then new) — anti-skill-explosion rule. Forces "improve what exists" before "create new."
- **"If the evidence is weak, say `no durable lesson` and stop"** — explicit anti-overcapture rule.
- **"Default to one durable lesson and one next step, not a brainstorm dump"** — bounded output rule.
- **"Distinguish `verified` / `heuristic` / `unknown` / `no durable lesson`"** — epistemic discipline.
- **"Improvement loops should reduce future friction, not create new ceremony"** — meta-rule about the meta-skill.
- **"Do not create a competing memory log for the same type of learning"** — anti-fragmentation across landing zones.

## Related skills

- `dev-scope-deferral` — invoke for follow-up todos surfaced during the loop.
- `consolidate-memory` (if installed) — sometimes used together when memory entries reflect a process-learning pattern.
- `dev-review` cluster — invokes this skill as a delegate-pattern from its modes (e.g., after `manifesto-review` reveals a recurring pattern worth formalizing).
- `dev-investigate` — invokes this skill after surfacing war-story-derived patterns.

