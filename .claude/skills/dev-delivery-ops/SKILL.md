---
name: dev-delivery-ops
description: >-
  Coach the unified delivery loop — BIG PLAN → Fresh Eyes → Slice; for each
  slice Slice Plan → Fresh Eyes → Human Decisions → Code → Review/Debug → Now
  What → Fresh Eyes → Self-Improvement Loop → Commit → Project Checkpoint. Use
  as a coach skill that keeps work in the loop, classifies each piece of work
  as `bug | polish | feature` with a `risk_level`, scales verification depth to
  risk, and points at the right `dev-*` skill at each beat. Triggers on "let's
  start a new project", "kick off the delivery loop", "what should we do next
  on this work", "set up the delivery process for this", "use the unified
  delivery process". Do NOT trigger for actually implementing code (use the
  relevant `dev-*` skill — `dev-plan` / `dev-investigate` / `dev-PR` / etc.).
  Do NOT trigger for one-off bug investigation (use
  `dev-investigate triage-and-fix`). Do NOT trigger as a substitute for picking
  the right specific skill — this skill points at the others, it doesn't
  replace them.
version: 0.1.0
category: Planning
display_name: Delivery Ops
tagline: Coach the unified delivery loop — BIG PLAN → Slice → Verify.
packs:
  - dev-pack
icon: 'phosphor:Path'
when_to_use: >-
  Asserts the unified delivery loop: BIG PLAN → Fresh Eyes → Slice; for each
  slice Slice Plan → Fresh Eyes → Human Decisions → Code → Review/Debug → Now
  What → Fresh Eyes → Self-Improvement Loop → Commit → Project Checkpoint.
  Coach skill — points at the right specific skill at each beat; doesn't
  replace them.
---

# dev-delivery-ops

## Purpose

Coach skill. Doesn't do code; **asserts the loop** that keeps work moving through the right beats with the right skills. The articulated workflow:

```
BIG PLAN → Fresh Eyes → Slice
  For each Slice:
    Slice Plan → Fresh Eyes → Human Decisions → Code It →
    Review/Debug → Now What? → Fresh Eyes →
    Self-Improvement Loop → Commit → Project Checkpoint
  Loop to next slice, until BIG PLAN is finished
  Check analytics, senior review
  Open PR → PR-remediation loop
```

This skill makes sure that loop actually runs — that fresh-eyes happens twice per slice (once at plan time, once after coding), that the now-what beat doesn't get skipped, that the self-improvement loop happens before commit, that the project checkpoint happens after.

## When to use

- Starting a new feature, refactor, or non-trivial change.
- Mid-flight when the work is drifting and you want to reorient on the loop.
- Setting up delivery process for a new project (work-type profiles, gate rules, case shape).
- When the question is "what beat are we in, and what's next?"

## How this skill works

It is **a router and a coach**, not a workflow runner. Output is short:

1. **Where are we in the loop?** Name the current beat.
2. **What should the current beat produce?** Be concrete.
3. **Which skill owns this beat?** Point at it.
4. **What's the risk-scaled verification expectation for this slice?**
5. **What's the next beat after this one?** Look one ahead, not five.

The user (or another agent) does the actual work via the named skill. This skill checks back in at beat transitions.

## Work-type classification

Every piece of work classifies as exactly one of:

| Work type | Default proof shape | Owner skills |
|---|---|---|
| **`bug`** | Differential proof (fail-first or before/after) | `dev-investigate` (lane selection inside) → `dev-test-design design` (proof plan) → `dev-PR` |
| **`polish`** | Non-regression OR differential, scaled to risk | `dev-plan scope` (if non-trivial) → `dev-test-design coverage` → `dev-PR` |
| **`feature`** | Acceptance proof + assumption ledger + staged verification | `dev-plan` (any mode) → `dev-fresh-eyes` → `dev-test-design strategy` → ... → `dev-PR` |

Classify early and explicitly. Mixed work gets split.

## Risk classification

| Risk | Verification expectation | Examples |
|---|---|---|
| **`low`** | Acceptance or non-regression check; one disconfirming check optional | UI copy, config tweaks, doc updates |
| **`medium`** | Direct test + disconfirming check + invariant proof if state/contract changes | Most feature work, refactors that touch one boundary |
| **`high`** | Direct test + disconfirming check + invariants (functional + at least one of perf/operational/safety) + temporary observability if needed | Auth changes, data migrations, public API contract changes, billing |

`dev-test-design invariants` mode is required for medium+ risk.

## The loop, beat by beat

### Beat 1 — BIG PLAN

For non-trivial work only (3+ slices, multi-week, architectural shifts).

- **Owner:** `dev-plan` (`scope` for milestones; `architecture` for system shape; `prd` for formal write-up)
- **Output:** sliced plan with explicit non-goals and rough sequence
- **Skip when:** single-slice work, simple polish, one-shot bug fix

### Beat 2 — Fresh Eyes on BIG PLAN

- **Owner:** `dev-fresh-eyes`
- **Output:** gaps / inconsistencies / reuse-and-existing-patterns / simplifications / recommendations
- **Skip when:** the plan is genuinely small and the surface is well-understood

### Beat 3 — Slice (split big plan into slices)

If BIG PLAN exists, name the next slice and confirm scope. Output: which slice, what's in scope, what's deferred.

### For each slice — beats 4 through 13

#### Beat 4 — Slice Plan

- **Owner:** `dev-plan scope` (lighter weight than BIG PLAN); for bug-shaped slices use `dev-now-what` (figure out the fix shape) or `dev-investigate triage-and-fix`
- **Proof design:** the "with what proof" half of the output is `dev-test-design`'s job — `strategy` to pick the proof shape, `invariants` (required at medium+ risk per the risk table) to pin what must stay true. Slice plans without a proof plan aren't done.
- **Output:** what this slice does, why, in what order, with what proof

#### Beat 5 — Fresh Eyes on Slice Plan

- **Owner:** `dev-fresh-eyes`
- **Output:** Tier 1 (must-fix) findings before coding starts

#### Beat 6 — Human Decisions

Beats 4 and 5 surface decisions that need human input. Capture them; surface them; wait for the user.

#### Beat 7 — Code It

The user (or sub-agent) writes the code. This skill steps back.

#### Beat 8 — Review / Debug

- **Owner:** `dev-review` (any mode appropriate to scope) for code review; `dev-investigate` for bugs found during this beat
- **Output:** review findings classified into FIX_NOW / HUMAN_DECISION / DEFER / DISMISSED

#### Beat 9 — Now What?

- **Owner:** `dev-now-what`
- **Trigger:** review surfaced something. The question is no longer "did we ship the slice?" but "given what review found, what's the right shape for the next move?"
- **Output:** symptom-vs-root assessment, existing-seams scan, minimum-viable-change recommendation, deferred follow-ups

#### Beat 10 — Fresh Eyes on Next Move

If "Now What?" produced a non-trivial pivot, fresh-eyes the new shape before implementing.

#### Beat 11 — Self-Improvement Loop

- **Owner:** `dev-self-improvement-loop`
- **Trigger:** anything in this slice was friction-y, surprising, a correction, or a pattern. Capture it before it evaporates.
- **Output:** updated skill / SOP / agent rules file / memory entry

#### Beat 12 — Commit

- **Owner:** the user. Default discipline: do not commit until behavior is tested and verified.
- **Verification gate:** scaled to `risk_level` per the work-type profile. No commit before invariants pass.

#### Beat 13 — Project Checkpoint

- **Owner:** `dev-checkpoint`
- **Commit seam:** when beat 13 runs right after a beat-12 commit, dev-checkpoint's own commit step is already satisfied — it reorients only. Its commit step exists for the case where checkpoint is the *first* gate reached with verified-but-uncommitted work. One commit, whichever beat gets there first.
- **Trigger:** end of slice, especially if multiple slices are bundling into one milestone
- **Output:** what's done / partial / pending / deferred + skill-usage signal

### After all slices — beats 14 through 16

#### Beat 14 — Analytics & senior review

User-driven gate (analytics check, senior/staff engineer review, stakeholder sign-off — whatever your team's pre-PR escalation looks like). This skill names that the gate exists and pauses.

#### Beat 15 — Open PR

- **Owner:** `dev-PR`
- **Verification:** brief artifact + reviewer-orientation sections

#### Beat 16 — PR remediation loop

- **Owner:** your reviewer-agent lane (an independent reviewer tool, or a fresh-context subagent)
- **Trigger:** PR opened, async reviewer assigned

## Cross-cutting reminders this skill enforces

- **Verification gates the commit.** Don't commit until proof matches risk.
- **Two fresh-eyes passes per slice.** Once at plan time, once after review/debug if the "now what" produced a new shape.
- **Self-improvement before commit.** Captures durable patterns before context evaporates.
- **Project checkpoint after each slice.** Keeps state honest.

## Output shape

When invoked, return a short status note covering: the current beat (and what just finished), the concrete deliverable this beat produces, the `dev-*` skill (and mode) that owns it, the risk-scaled verification expectation for this slice, the immediately-next beat, and any notes that matter (gates not yet passed, outstanding human decisions). Look one beat ahead, not five.

## Hard rules

- **Don't replace specific skills.** This skill points at others. If the user invokes this for a code change, the answer is "use `dev-plan`" or "use `dev-investigate`," not "I'll do it here."
- **Don't skip fresh-eyes beats.** If the user wants to skip, name the trade-off; don't silently drop them.
- **Don't merge polish + bug + feature into one slice.** Classify and split.
- **Verification scales to risk, not to "we did some tests."** Risk-appropriate disconfirming checks are required at medium+.

## First-time setup

This skill assumes the rest of the `dev-*` pack is installed — every beat hands off to a named sibling (`dev-plan`, `dev-fresh-eyes`, `dev-investigate`, `dev-review`, `dev-test-design`, `dev-now-what`, `dev-self-improvement-loop`, `dev-checkpoint`, `dev-PR`). Install the `dev-pack` as a unit rather than skill-by-skill; a coach with no skills to coach is not useful.

If your stack uses a different async-reviewer agent than Devin (CodeRabbit, Greptile, in-house bot), substitute it at Beat 16 — the loop shape is what matters, not the specific tool. (This note can be deleted from your local copy of the skill once read.)
