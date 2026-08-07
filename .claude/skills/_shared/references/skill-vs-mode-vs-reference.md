# Skill vs. Mode vs. Reference — decision tree

After classifying a prompt's chunks, decide what the source becomes. Four options:

1. **New standalone skill** — a distinct job, probably no close siblings yet
2. **Mode within a category skill** — shares reference material with related prompts
3. **Shared reference doc only** — pure domain knowledge, no job logic of its own
4. **Template only** — a stable output shape that existing skills can reference

## Decision questions (in order)

### Q1 — Is there job logic at all?

If the source is a pure definition, checklist, or taxonomy with no run logic (no "do this, then that, return X"), it's a **reference doc**. If it's a widely-applicable domain concept, extract to `skills/_shared/references/<topic>.md` (shared by multiple skills). If it's a skill-internal domain concept, extract to `skills/<skill-name>/references/<topic>.md`. Stop.

Examples: a standalone "Here are the six content formats" explainer; a glossary; a scoring rubric with no accompanying task.

If there is job logic, continue.

### Q2 — Is there an existing category skill this job belongs to?

Scan the existing skill library. Does a skill already exist in the same category (editing, offer design, content planning, etc.)?

- **Yes, and this prompt is one of several siblings that share reference material** → **mode** within the existing category skill.
- **Yes, but this prompt has nothing in common with the siblings except the category label** → **standalone skill**. (Category is not enough of a shared-load signal.)
- **No** → continue to Q3.

### Q3 — Does this prompt have close siblings among the unconverted prompts?

Look at the other unconverted prompts in the library. Are there 2+ prompts that would use the same references as this one?

- **Yes, 3+ close siblings** → create a new **category skill** with modes. This source becomes the first mode.
- **Yes, 1–2 close siblings** → judgment call. Lean toward a category skill if the siblings are likely to multiply; lean toward standalone skills that later get merged if unsure.
- **No** → **standalone skill**.

### Q4 — Is the output shape stable and reusable?

Independent of Q1–Q3, ask whether the output shape is:
- **Specific to this skill only** → keep as `templates/` inside the skill
- **Reusable across skills** (e.g., a report shape used by multiple analyzers) → extract to a shared templates library

## The "shared load" heuristic

The strongest signal for "mode, not standalone skill" is: *would this skill and its candidate sibling load the same reference doc for the same reason?*

Example: Copy Editor Bot, Redundancy Checker, Active Voice Helper, and Tone Scale Finder would all load the same copy-editing checklist. That's strong shared load → they're modes of one `editing` skill.

Counter-example: Offer Brainstormer and Landing Page Writer both fall under "marketing" but they'd load completely different references (offer frameworks vs. copywriting structures). Weak shared load → separate skills.

## Category skills — structure

A category skill with modes looks like:

```
skills/os-editing/
  SKILL.md                   # category-level trigger, mode routing
  references/
    copy-editing-checklist.md
    voice-matching.md
    writer-style-preservation.md
  modes/
    copy-edit.md
    developmental.md
    argument-amplify.md
    redundancy-check.md
    tone-scale.md
    takeaway-extract.md
    time-to-value.md
    de-ai-ify.md
  templates/
    issue-suggestion-report.md
    takeaway-list.md
  examples/
    copy-edit-example.md
    developmental-example.md
```

SKILL.md at the category level:
- Triggers on the category concept ("edit this," "improve my writing")
- Selects a mode based on user intent (copy edits vs. structural changes vs. argument strengthening)
- Loads shared references that apply to all modes
- Delegates run instructions to the selected mode file

Each mode file contains:
- The specific craft moves from the original prompt
- Mode-specific directives
- Which templates to use for strict mode
- Which examples to draw on

## When to split an existing category skill

If a category skill accumulates modes whose references diverge significantly, split. Example: if `editing` grew to include "edit this code" modes alongside "edit this prose" modes, the references diverge enough that two category skills (`prose-editing`, `code-editing`) are better than one.

Heuristic: a category skill with a single shared reference that all modes use is healthy. A category skill where different modes use disjoint reference sets is a merge that should be split.

## When to promote a mode to a standalone skill

If a mode grows enough reference material or craft complexity that it starts to dominate the category skill, promote it. Signs: the mode file becomes longer than SKILL.md; the mode starts using references none of the other modes touch; users ask for the mode's output by the mode's name, not the category name.

## When to demote a standalone skill to a reference

If a "skill" turns out to be mostly definitions with thin run logic, demote. The run logic gets folded into whichever skill references the knowledge, and the definitions live as a reference.

## Shared-reference promotion — when and how

A reference lives inside the skill that needs it (`skills/<skill-name>/references/<topic>.md`) until a second skill starts loading it *for the same reason*. At that moment, promote to `skills/_shared/references/<topic>.md`.

### Promotion threshold

**Two skills loading for the same reason is enough.** Waiting for a third skill to reach for the same content risks silent duplication and reference drift — the two copies diverge as each skill's needs evolve independently.

Same-reason is the part that does the work. Two skills that happen to mention "Schwartz awareness" incidentally but use it for different purposes (e.g., one for categorizing prospects, one for analyzing a writer's target audience in a writing-style context) do not pass the same-reason test.

### How to promote

1. Write the canonical version at `_shared/references/<topic>.md`. Consolidate from both skill-internal versions where possible; prefer the clearer phrasing.
2. Add a **malleability note** to the shared reference describing what's canonical (the shape of the framework) and what's adaptable (skill-specific calibration). Malleability notes prevent the reference from becoming sacred and let skills diverge with a documented reason when needed.
3. Update the original skill-internal references to cross-reference the shared version rather than duplicating content. Each skill's reference may include skill-specific usage notes ("When to use in this skill's modes: ...") below the cross-reference.
4. Update the `_shared/references/README.md` to list the new promoted reference.
5. Note the promotion in both skills' decision logs (or in the verification batch file for the current skillify run).

### Path conventions for shared references

Skills load shared references via relative paths:

- From `skills/<skill-name>/SKILL.md` → `../../_shared/references/<file>.md` (up 2 levels: skill, skills)
- From `skills/<skill-name>/references/*.md` or `skills/<skill-name>/modes/*.md` → `../../_shared/references/<file>.md` (up 3 levels)
- From one skill to another skill's artifact: `../<other-skill>/modes/<mode>.md` (from SKILL.md) or `../../<other-skill>/...` (from nested files)

Cross-skill references to other skills' modes/references should be rare — usually a sign that the shared content should promote to `_shared/` instead.

## Path conventions summary

The canonical workspace tree lives in `naming-conventions.md` and isn't restated here — one tree, one place to correct when the layout moves.

The two rules this file depends on: skills live at `skills/<skill-name>/`, and shared references live at `skills/_shared/references/`. Nothing belongs outside those two trees.
