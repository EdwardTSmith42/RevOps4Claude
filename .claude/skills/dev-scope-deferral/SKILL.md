---
name: dev-scope-deferral
description: >-
  Capture a valid follow-up improvement uncovered during current work without
  bloating the current PR or task. Writes a deferred-investigation note with the
  problem statement, remaining fragility, proposed design, risks, non-goals, and
  an executable verification idea. Invoked directly by the user ("defer this,"
  "save this for later"), and as a delegate-pattern from inside other skills
  (`dev-investigate` modes, `dev-fresh-eyes`) when they uncover work that's
  valid but expands blast radius / review risk / timing beyond the current
  scope. Do NOT trigger to dodge required safety changes. Do NOT trigger for
  vague future ideas — only for concrete, valid follow-up work uncovered during
  current scope.
version: 0.1.0
display_name: Scope Deferral
tagline: Capture valid follow-up improvements without bloating the current PR.
category: Planning
packs:
  - dev-pack
icon: 'phosphor:Bookmark'
when_to_use: >-
  Use when current work uncovers a valid follow-up that would expand blast
  radius, review risk, or timing if rolled into the current PR. Writes a
  deferred-investigation note with problem statement, fragility, proposed
  design, risks, non-goals, and an executable verification idea.


  Invoked directly ('defer this,' 'save this for later'), and as a
  delegate-pattern from inside other skills when they uncover work that's valid
  but out-of-scope. Don't use it to dodge required safety changes.
---

# Scope Deferral

## Purpose

Preserve the stronger follow-up cleanly without bloating the current change. **The right engineering answer is sometimes bigger than the right PR.** This skill captures the bigger answer as a deferred-investigation note so it isn't lost while keeping the current change focused.

This skill exists at two levels:
1. **Direct invocation by the user** — "defer this," "save this for later," "scope-deferral on this."
2. **Delegate-pattern from inside other skills** — when `dev-investigate` modes, `dev-fresh-eyes`, or other workflows uncover follow-up work, they invoke this skill rather than embedding TODO-style notes in their primary outputs.

## When to use

- A current change is safe and useful on its own AND a follow-up adds real value but expands blast radius / review risk / timing.
- During investigation (any `dev-investigate` mode), an adjacent issue surfaces that's valid but out of scope.
- During `dev-fresh-eyes` review, a recommended adjustment is right but should be its own pass.
- During mutation-scout, the strengthening plan is broader than this PR.

Do NOT use to:
- Dodge a change required for safety.
- Capture vague TODO-only investigation notes.

## Inputs

- The current work context (what's being shipped now).
- The deferred improvement (what surfaced that's worth doing later).
- Repo / branch context (so the backlog pointer can be added to the right place).

## Run

1. **Confirm the split is justified:**
   - The current PR/fix is safe and useful on its own.
   - The follow-up adds real value but expands blast radius, review risk, or timing.
   - Both criteria must hold. If either fails, this isn't the right skill — fold the work into the current scope or drop it.

2. **Write the scope split in plain language.** A one-paragraph statement of what ships now, what doesn't, and why.

3. **Create or update a deferred-investigation note** under your workspace's deferred-investigation directory (e.g., `os-inputs/_os-deferred-investigations/<date>-<slug>.md`, or wherever your workspace keeps long-lived investigation notes). Use `templates/deferral-note.md` for the structure.
   - Filename: `<YYYY-MM-DD>-<short-kebab-slug>.md`.
   - Create the directory if it doesn't exist.

4. **Record the follow-up** with:
   - Problem statement
   - Remaining fragility
   - Proposed design
   - Risks
   - Non-goals
   - **Executable verification idea** (the *executable* qualifier is what separates a useful deferred note from a wish)

5. **Add or update the repo-local backlog pointer**, usually in `tasks/todo.md` or your project's equivalent backlog file. Keep the pointer concise: link / path to the deferred-investigation note + one-sentence summary.

6. **If the deferral reflects a durable preference, route the lesson to where durable preferences live for you** — a cross-project lessons store for guidance you want everywhere, or the project's agent-instructions file (e.g., `AGENTS.md`, `CLAUDE.md`, or equivalent) for project-specific guidance. Don't let one-off deferrals sprawl into a pattern of unaddressed follow-ups.

## Output

Three artifacts, in order:

1. **Deferred-investigation note** at your workspace's deferred-investigation path (full structure per `templates/deferral-note.md`).
2. **Repo-local backlog pointer** (line added to `tasks/todo.md` or equivalent, if applicable).
3. **Inline summary to user** — what's deferred, where the note lives, and how the current scope reads as a result.

```markdown
## Scope deferred

**Why scope stays narrow:** <one paragraph>
**Deferred improvement:** <plain-language summary>
**Note path:** `<path to the deferred-investigation note>`
**Backlog pointer:** <path or omit if not applicable>
**Ship-now decision:** what ships, what doesn't
**Verification hook for later:** <executable check>
```

## Guardrails

- **Do not use this skill to dodge a change that is required for safety.** If the deferred work is required, ship it now.
- **Do not create vague TODO-only investigation notes.** Concrete > breadth.
- **Keep the current PR / scope explanation explicit:** what ships now, what does not, and why.
- **Prefer one concrete deferred note over a brainstorm list.** A list of three rough ideas is worse than one well-articulated deferral.

## Design Rationale

Why this skill is structured the way it is:

- **Two-criteria split-justification ("safe and useful on its own" AND "follow-up has cost reason")** prevents using this skill to defer required safety work. Both criteria must hold.
- **"Executable verification idea" requirement** — the *executable* qualifier separates a useful deferred note from a wish. A vague "we should do this someday" doesn't ship; an executable check (a test scenario, a logging probe, a reproduction harness) does.
- **Notes live in the workspace's deferred-investigation directory** — a stable, greppable home that persists across projects so deferrals don't get lost in scratch files or buried in chat transcripts.
- **Standalone skill + delegate-pattern** — invokable directly by the user AND as a delegate from other skills. Promoting deferral to a named skill that other skills explicitly call out to makes the dependency visible, rather than embedding ad-hoc TODO-style notes in unrelated outputs.
- **Repo-local backlog pointer + private note** — the note has the depth (problem statement, design, risks, verification); the pointer is the discoverability hook (someone reading `tasks/todo.md` finds the deferred work).
- **Lesson-routing step** — if the deferral reflects a durable preference, route the lesson to wherever your durable preferences live (cross-project lessons store, or your project's agent-instructions file) to prevent the pattern from becoming a sink for unaddressed follow-ups. The note captures the case; the lesson capture prevents it from happening again.

## Related skills

- `dev-investigate` modes — invoke this skill when adjacent valid work surfaces during investigation.
- `dev-fresh-eyes` — invokes this skill when a recommended adjustment should be its own pass.
- Your harness's spawn-a-side-task affordance (if available) — some agent harnesses can spin a deferred item into its own background session. Complementary to this skill: write the durable note here for the record, and optionally spawn a side-task when the user wants to start the deferred work soon.

## Templates

- `templates/deferral-note.md` — the structure for the deferred-investigation note.
