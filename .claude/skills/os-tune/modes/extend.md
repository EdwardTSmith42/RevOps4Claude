---
mode: extend
parent: os-tune
description: >-
  Sub-mode of `os-tune`. Add a new mode to an existing skill rather than creating a new skill that duplicates intent. Updates the parent SKILL.md mode index plus creates the new mode file (one Modify + one Create write). Mirrors existing skill's frontmatter style, structure, length register; doesn't break existing modes. Triggers on "extend my email skill to handle X," "add a mode to tracker for Y," "this skill needs a new mode for Z."
---

# os-tune / extend — add a mode to an existing skill

## What this mode does

Adds a new mode to an existing skill rather than creating a new skill that duplicates intent.

This is the map-before-make payoff. When the user's ask is coherent with a skill they already have, extending is cleaner than making a new skill that overlaps. The new behavior joins the existing skill as a mode; the skill grows while staying coherent.

## When this fires

Two paths.

**From routing (most common):** The user said *"figure it out"* (or an equivalent) with a need. os-tune's routing scanned the skills inventory per `../references/figure-it-out-routing.md`, found a high-confidence match, and surfaced *"this sounds like another mode of your email skill, not a new skill — extend it?"* The user confirmed.

**From direct invocation:** The user explicitly said *"add a mode to my email skill that does X"* or *"extend the tracker skill to handle Y."* The target is named; routing is bypassed.

Don't fire when:

- The new behavior contradicts the existing skill's purpose (route to the os-skillify handoff, often with a note that two skills coexist cleanly)
- The new behavior is large enough to be its own skill (route to the os-skillify handoff)
- The user explicitly said *"new skill"* (respect the override)

## Inputs

- **Target skill path.** Resolved from the user's named skill or the routing decision.
- **New behavior description.** The ask in the user's words — what should the new mode do?
- **Optional source material.** Examples, content, or prior outputs that fuel the new mode's design.

## What `extend` does

1. **Reads the target skill's `SKILL.md`** to understand scope, mode boundaries, and operating principles.
2. **Reads existing modes** in the target's `modes/` directory for shape consistency (frontmatter style, structure, length register).
3. **Designs the new mode** following the existing shape — same structure, same principles, same length.
4. **Updates the SKILL.md mode index** (the table or routing logic listing the skill's modes) to include the new mode.
5. **Surfaces the diff** to the user before persisting:
   - The proposed new mode file (full content)
   - The proposed SKILL.md update (diff against current)
6. **After approval, persists both files safely.** Invoke `os-autosave snapshot` first with a name like `pre-extend-<skill>-with-<new-mode>` — adding a new mode is a moderate-tier change and warrants a snapshot. Persist both files. Invoke `os-autosave commit` with message `os-tune extend: <skill> — added <new-mode> mode`. Run a sanity check (skill still parses; new mode reachable from SKILL.md's self-determining routing). If the sanity check fails, revert to the snapshot.

## Operating principles

- **Mirror the existing shape.** New modes follow the conventions of the skill they join — frontmatter style, mode-section structure, principles section format. A new mode that reads as written by a different author breaks the skill's coherence.
- **Don't break existing modes.** The new mode can't override or contradict the operating principles of its host skill. If the new behavior conflicts with an existing principle, surface the conflict and let the user resolve before adding.
- **Update the index.** SKILL.md's mode table or routing logic must reflect the new mode. A new mode that isn't indexed won't be discovered.
- **Writes follow `../../_shared/references/skill-update-protocol.md`.** Two files change in this mode (the new mode is Create; SKILL.md's mode-index update is Modify). Both diffs surface in the same batch — extend's defining write-discipline detail. Sanity checks include "new mode reachable from SKILL.md's self-determining routing."
- **Inherit Personal OS context.** Voiceprint and conventions still load (per `../references/inheritance-protocol.md`) even though we're not generating a full skill — the mode body still has prose that needs voice calibration.
- **Apply the skill-prompting principles to the new mode.** Load `../../_shared/references/skill-prompting-principles.md` before designing the mode body — the file is canonical and current; don't work from a remembered list. Mirroring the existing skill's shape and applying the principles point the same direction in most cases; where they conflict (the host skill predates the principles and is bullet-heavy in a prose domain), surface the conflict to the user rather than silently choosing one.
- **Use extend as a moment to consider whether the host skill should gain self-extending behavior.** Load `../../_shared/references/self-extending-skills.md`. If the host skill is additive and doesn't currently carry the three-beat self-extending pattern, the extend pass is a natural moment to ask whether to add the pattern alongside the new mode — a recurring pattern of "add mode X to skill Y" is itself a signal that the skill is additive and would benefit from being greedy about future extension. Surface the option to the user; don't add the pattern silently, and don't add it to skills the additive-vs-complete heuristic identifies as complete.
- **Track work-in-progress in system tracker.** When extend starts, log the active extension task to `os-tracker/system.md` via `os-tracker/add` (e.g., *"extending email-skill with reschedule-confirmation mode"*). The entry stays open until the extension applies; close-out marks it done. Lets the next session pick up if the work doesn't complete this one. Mirrors `refine`'s pattern. See `os-inputs/_os-inbox-conventions.md` for the inbox-vs-system-tracker model.

## Edge cases

**The new mode would duplicate an existing one.** If the new ask is essentially equivalent to a mode the skill already has, `extend` says so and routes to `refine` (the user might mean "tweak the existing mode") or asks if they really want a duplicate.

**The new mode crosses skill boundaries.** If the new behavior would touch logic that lives in another skill, `extend` flags the cross-skill dependency and asks how to handle it (extend both? extract into a third skill? keep as-is and reference?).

**The host skill is canonical.** If the target skill is a shipped Personal OS skill (listed in `.os-manifest.json`), `extend` notes: your customizations are safe — updates detect them by hash and will never overwrite them silently — but consider whether the addition is personal (extend in place) or something any user would want (worth suggesting upstream). Skills not in the manifest are entirely the user's; extend freely.

## See also

- the os-skillify handoff — when the ask is really a new skill
- `refine` — when the ask is really feedback on the existing modes
- `../references/figure-it-out-routing.md` — how routing decides between make/extend/refine
- `../references/inheritance-protocol.md` — what context loads before extension
- `../../_shared/references/skill-prompting-principles.md` — the principles the new mode should follow
- `../../_shared/references/self-extending-skills.md` — consider whether the host skill should gain self-extending behavior as part of the extend pass
- `os-library/repair` — for fixing frontmatter or schema issues that come up while extending
