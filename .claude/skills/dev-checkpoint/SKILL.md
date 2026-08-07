---
name: dev-checkpoint
description: >-
  Commit current verified work, then reorient on project state by summarizing
  what is completed, partially completed, and still pending; checking for missed
  items, side quests, and architecture/pattern gaps; and recommending the next
  steps. Use when the user asks for a "checkpoint", "milestone reorientation",
  "where are we?", "what's done vs pending?", or asks to commit and then discuss
  the project status. Do NOT trigger for milestone smoke + regression sweeps
  (use `dev-review checkpoint`). Do NOT trigger for ship-readiness verdicts (use
  `dev-review ship-gate`). This skill complements those modes; user can invoke
  both when both are needed.
version: 0.1.0
display_name: Project Checkpoint
tagline: 'Commit + reorient on project state — what''s done, partial, pending.'
category: Planning
packs:
  - dev-pack
icon: 'phosphor:Flag'
when_to_use: >-
  Reach for this when you ask 'where are we?' or 'what's done vs pending?' or
  want to commit current verified work and then discuss project status. Surfaces
  missed items, side quests, and architecture/pattern gaps; recommends next
  steps.
---

# Project Reorientation Checkpoint

## Purpose

Run when the user wants a **reliable progress checkpoint** — not just a code diff summary. The job: commit verified work, then take a wider-lens reading of project state by reconstructing what's done / partially done / pending / deferred, checking for missed items and side quests, and recommending next steps.

Manually triggered. Common phrasings: "checkpoint," "where are we?," "what's done vs pending?," "let's reorient," "milestone reorient."

## Workflow

### 1. Confirm checkpoint surface

Show current branch and worktree state:
```bash
git branch --show-current
git status --short
```

Gather most-relevant source-of-truth artifacts for the current branch:
- the repo-local backlog or task list if your project keeps one (e.g., `tasks/todo.md`)
- relevant brief / spec / change-doc files if they exist (e.g., a per-branch brief under wherever your project keeps in-flight design notes)
- recent commit history: `git log --oneline -8`

**If the branch has drifted from the plan, prefer the current code plus task artifacts over stale prose.**

### 2. Gate the commit on verification

**Don't commit blindly.** Check whether verification evidence exists for the changed surface:
- Reuse existing fresh verification evidence when it is adequate.
- If verification is missing or stale for the changed surface, **run the smallest meaningful checks first.**
- If verification is incomplete, say so plainly and either:
  - **Stop before commit**, OR
  - Make a scoped user-approved progress commit only if the user explicitly wants that despite the gap.

### 3. Commit the checkpoint when appropriate

Stage only the work that belongs in the milestone:
```bash
git add <specific files>   # -A only after confirming the diff carries no unrelated churn
```

Commit with a conventional message describing the actual checkpoint scope:
```bash
git commit -m "chore(progress): checkpoint <plain-language scope>"
```

Record the commit hash and subject:
```bash
git rev-parse --short HEAD
git log -1 --oneline
```

If generated files are present, decide whether they are authoritative derived artifacts for this change OR avoidable churn. **State that decision explicitly in the checkpoint report.**

### 4. Reconstruct project state from evidence

Compare the intended plan against the actual branch contents.

Classify work into:
- **Completed** — concrete items truly done on the branch
- **Partially completed** — exists but with important gaps
- **Pending** — remaining work
- **Intentionally deferred** — explicit deferrals (cross-reference any `dev-scope-deferral` notes)

Look for common ways progress gets lost:
- **Bug-fix side quests** that changed scope.
- **Docs / specs / todos** that no longer match reality.
- **Architecture or contract implications** not captured in the task list.
- **Generated artifacts or cleanup items** that may have been skipped.
- **Tests or verification gaps** that make "done" weaker than it sounds.

### 5. Take a wider-lens architecture pass

Review the changed subsystem boundaries, not just file diffs. Call out:
- **Canonical truth location** — what's authoritative now?
- **Duplicated logic or contract drift**
- **Dead code or transitional seams**
- **Concurrency / state ordering risks**
- **Policy / config values that should be explicit**

**Keep this pragmatic.** Prefer a few high-signal observations over a broad audit.

### 6. Skill usage signal (system-level health, optional)

**Skip this step entirely if skill-usage logging isn't running.** Two sources may exist and they're complementary, not competing. A harness hook (on Claude Code, `PostToolUse` on the Skill tool → `~/.claude/skill-usage.jsonl`) can't be forgotten and spans every project, but records only the skill and raw args. A workspace log an agent appends to carries more — mode, context, outcome — but depends on that habit holding, which it does in an actively-tended workspace and doesn't in one where attention has moved on. Prefer whichever is populated; pass `--log` to choose. Say plainly if neither exists.

Treat it as **forward-looking signal, not a basis for trimming.** A skill recently added or recently ported across harnesses shows as "idle in last N days" even when it's healthy; the signal is for noticing trigger-gaps and anomalies, not for deletion calls.

```bash
python3 <skills-dir>/os-tune/scripts/skill_usage_report.py --days 30
```

The script lives in `os-tune` (which always ships with Personal OS, so it's there whenever this skill is). It finds the log and skills directory on its own (override with `--log` / `--skills-dir`), and prints most-used skills, which modes fired, modes defined but never fired, and idle skills. `--format json` if you want to post-process.

**On mode resolution — read the caveat before trusting the mode lines.** The log records the skill and the free-form args; harnesses don't record a mode, because mode is a Personal OS convention that lives inside that prose. The script resolves it by matching each skill's *declared* modes against the args, which means:

- A mode only registers as fired when the invocation actually named it. Routing that happened conversationally — the user described a need and the skill picked a mode — looks the same as no mode at all. Those land under *invoked without naming a mode*.
- So **"never fired" means "never named," not "dead."** It's a trigger-wording signal, and a strong one, but never a deletion verdict on its own.
- Skills that declare no modes are single-mode by design and are excluded from the never-fired list rather than counted as missing data.

**Reading the mode-level signals:**
- A skill with high invocation count but only one mode firing → other modes have a trigger-gap problem worth investigating.
- A mode listed in "defined but never fired" → either dead, or its trigger conditions never match how requests get framed in practice.
- Both signals are watch-items, not delete-candidates. Recent additions and recent ports skew the same way idle-because-unused entries do.

Report shape (under "## Skill Usage" section in the output):

- **Top 5 used skills (last 30d):** count + name. One-liner observation if anything jumps out.
- **Idle skills (last 30d):** the list, with an explicit caveat line that idle-on-this-surface doesn't mean unused overall (recent additions and cross-harness ports look the same as truly dead skills here).
- **Anything that looks anomalous:** a skill invoked dozens of times this week vs. its baseline, etc. Worth one sentence if visible.

**Hard rule:** never recommend deleting a skill based on this report alone. The data is observational, not decision-ready.

### 7. Recommend the next slice

Suggest the next steps in priority order. Separate:
- **Must-do before ship**
- **Worthwhile follow-up improvements** (capture via `dev-scope-deferral` skill)
- **Explicitly deferred larger work**

**Prefer small shippable slices over a vague long list.**

## Output

Return the checkpoint in this shape:

```markdown
# Checkpoint — <branch / scope>

## Checkpoint Commit
<hash, subject, and whether the work was committed or intentionally left uncommitted>

## Where We Are
<2-4 sentence plain-language status of the project>

## Completed
- <concrete items that are truly done on the branch>

## Partially Completed
- <items that exist but still have important gaps>

## Pending / Deferred
- <remaining work, with explicit deferrals called out>

## Architecture / Pattern Notes
<the most important wide-lens observations — keep pragmatic, few high-signal items>

## Verification
<what proof exists and what is still missing>

## Skill Usage (last 30d, observational — omit if harness has no skill-usage log)
<top 5 most-invoked skills + mode-level breakdown (skill:mode counts) + idle skills + modes-defined-but-never-fired. Frame everything as watch-items with an explicit caveat that recent additions / cross-harness ports look the same as truly dead skills here. Never a delete-candidate.>

## Next Steps
<prioritized recommendations: must-do before ship / worthwhile follow-ups / explicitly deferred>
```

## Hard rules

- **Keep the report plain-language first; IDs and internal names second.**
- **Do not open or merge a PR from this workflow** unless the user asks.
- **Do not let a checkpoint report imply ship-readiness if verification is weak.**
- **If the branch contains unrelated churn, name it explicitly** rather than burying it.
- **If a task list is stale, say so and anchor the checkpoint to code plus the most current evidence.**
- **Skill-usage signal is observational, not action-driving.** Idle skills are watch-items, not delete-candidates — recent additions and cross-harness ports show up the same way truly dead skills do.

## Design Rationale

- **Verification gates the commit** — don't commit blindly. Aligns with non-ship-gate principles. If verification is incomplete, abstain over forced commit.
- **"Bug-fix side quests that changed scope"** — names a common-progress-loss mode explicitly.
- **"Wider-lens architecture pass"** — encourages stepping back from file diffs to subsystem boundaries.
- **"Pragmatic — few high-signal observations over broad audit"** — anti-broad-audit fence.
- **"Small shippable slices over vague long list"** — anti-brainstorm-list rule.
- **"If task list is stale, say so and anchor to code plus most current evidence"** — anti-stale-anchor rule. Trust code over stale plans.
- **Distinct from `dev-review checkpoint` mode** — `dev-review checkpoint` is the milestone-review-loop (smoke + regression + monolith + cleanup). This skill is the state-reorientation summary. They overlap conceptually but produce different outputs; user can invoke both in sequence when both are needed.

## Related skills

- `dev-review checkpoint` — milestone-review-loop (smoke + regression + monolith + cleanup). Complementary; user can invoke both.
- `dev-fresh-eyes` — for skeptical second pass on the recommended next slice.
- `dev-scope-deferral` — invoke for any deferrable follow-ups uncovered.
