---
mode: refine
parent: os-tune
description: >-
  Sub-mode of `os-tune`. Fold a tweak, output edit, or piece of feedback into an existing skill's defaults. Minimum-viable-edit; preserves the skill's craft; updates the smallest part of the skill that accomplishes the change. Routes to `voiceprint` if the feedback is voice/tone calibration rather than skill behavior. Triggers on "fold this into the email skill," "update this skill so it does X by default," "this isn't quite right — fix the skill," "always include a P.S.," "refine this skill."
---

# os-tune / refine — fold feedback or output tweaks back into a skill

## What this mode does

Updates an existing skill's definition based on feedback from how it was actually used. The user ran a skill, got an output, tweaked the output, and wants the skill itself to produce that improved output going forward.

This is the self-improvement loop. Without it, skills stay frozen at their initial design — the user re-tweaks the same way every time. With it, the skill gets better the more it's used. It's what makes os-tune "the loop."

## When this fires

Two paths.

**Inline after running a skill (most common):** The user invoked a skill, the skill produced output, the user edited the output. os-tune notices (via `os-inputs/_os-inbox.md` capture, recent-session context, or explicit invocation) and asks: *"Want me to update the skill so this is the default?"* The user says yes; refine runs.

**Direct invocation:** The user said *"refine the email skill — when it generates client check-ins it should always include a P.S. with the next meeting reminder"* or *"the daily assist mode is too long; trim it to three lines."* Target named, behavior change stated.

Don't fire when:

- The user explicitly said the tweak was a one-off (*"just for this case, not as a default"*)
- The "feedback" contradicts the skill's purpose (route to the os-skillify handoff for a new skill, or `extend` for a new mode)
- The feedback is voice/tone calibration that belongs in the user's voiceprint, not in the skill (route to `voiceprint`)

## Inputs

- **Target skill path.** Named explicitly, or resolved from recent-session context.
- **The output the user got.** Either the literal output, or pointer to the inbox entry capturing it.
- **The tweak / edit / direction.** What the user changed, or what they want the skill to produce next time.
- **Optional rationale.** *Why* the user wants this change — surfaces whether the right place is the skill, the voiceprint, or a brief.

## What `refine` does

1. **Loads the target skill's full file structure.** SKILL.md + relevant mode file(s) + relevant references. os-tune reads everything that could be touched before deciding.

2. **Identifies which file the change belongs in:**
   - **Output formatting tweak** (e.g., "always include a P.S.") → mode file
   - **Operating-principle tweak** (e.g., "always run dry-run first") → SKILL.md or principles reference
   - **Voice / tone tweak** (e.g., "make it warmer") → may belong in the user's voiceprint, not the skill — route to `voiceprint` if so
   - **New behavior** (not a tweak) → route to `extend` (mode) or the os-skillify handoff (skill) and surface the route

3. **Designs the precise edit.** Minimum viable edit — the smallest change that accomplishes the user's intent. Don't refactor while you're in there.

4. **Surfaces the diff with rationale.** Names which file and section are changing, the diff itself, and a one-line reasoning that connects the user's stated intent to the specific edit — so the user can sanity-check the inference before approving.

5. **After approval, applies the edit safely.** For moderate or large changes, invoke `os-autosave snapshot` first with a short pre-change name (e.g., `pre-tone-default-on-email-skill`) so the change has a clean revert target. Apply the edit. Invoke `os-autosave commit` with a os-tune-generated message in the form `os-tune refine: <skill> — <one-line summary>`. Run a sanity check (skill still parses, still routes correctly, no broken references). If the sanity check fails, revert to the snapshot.

## Operating principles

- **Minimum viable edit.** The smallest change that accomplishes the user's intent. Don't refactor while you're in there. If the change exposes a deeper issue, surface it as a separate `refine` candidate rather than expanding scope.
- **Preserve craft.** Don't lose the existing skill's voice, structure, or operating principles when integrating a tweak. The user's existing skill embodies their craft; refine is additive, not replacing.
- **Surface the route.** If the tweak doesn't belong in the skill, say so before applying — naming where it does belong (voiceprint, brief, convention file) and asking the user to confirm the redirect rather than silently misapplying.
- **Writes follow `../../_shared/references/skill-update-protocol.md`.** Show before write, sanity-check after, customization respect for modify operations. Mode-specific concerns layer on top.
- **Capture corrections in inbox; track active work in system tracker.** When `refine` fires inline, the *correction* (the tweak pattern that should generalize) gets logged to `os-inputs/_os-inbox.md` as `[type: correction]` per `AGENTS.md`'s convention. The *active refinement task* (e.g., "updating email-skill client-checkin mode to add P.S. default") gets written to `os-tracker/system.md` via `os-tracker/add` so it's visible as work-in-progress. The two are complementary, not redundant — see `os-inputs/_os-inbox-conventions.md` for the full model. Inbox entries earn promotion to durable references via `reflect`; system-tracker tasks are marked done when the refinement applies.
- **Inherit Personal OS context.** Voiceprint and conventions still load — refine generates new prose for the modified skill section, and that prose needs voice calibration.
- **Apply the skill-prompting principles to every edit.** Load `../../_shared/references/skill-prompting-principles.md` before designing the diff — every principle there applies to revisions just as it applies to first writes, and refines drift toward the model's defaults if the lens isn't loaded. Especially worth re-checking on writing-domain and judgment-domain skills, where a "tighten this up" tweak can quietly turn prose into bullets.
- **Recognize self-extension triggers.** Load `../../_shared/references/self-extending-skills.md` and watch for tweak requests that are really self-extension asks in disguise — "the writing skill should handle VSL too," "the editing skill needs a new lens for X," "voiceprint should support author-scope Y." When the target skill is additive and doesn't yet carry the three-beat self-extending pattern, the right move is often to add that pattern rather than (or in addition to) implementing the specific tweak — because the pattern handles every future ask in the same family. Surface the alternative path to the user before applying.

## Edge cases

**The tweak fights the skill's stated purpose.** If the user wants behavior that contradicts the skill's purpose section, `refine` surfaces the conflict: *"The skill's purpose says X; the tweak would push it toward Y. Update the purpose too, or leave the skill and route to a different mode/skill?"*

**The tweak applies across multiple modes.** If the change should affect more than one mode in the skill, `refine` updates them together with the diffs surfaced as a batch. The user approves the batch.

**The tweak is repeated feedback the user has given before.** If the inbox or session context shows the user has surfaced this same tweak before but it didn't get persisted, `refine` calls it out: *"You've raised this before — the previous tweak didn't get folded in. Want to fix that pattern too?"*

**The tweak is voiceprint material disguised as a skill tweak.** Many "make it warmer / less formal / more conversational" asks are voiceprint calibrations. `refine` surfaces the route to `voiceprint` and asks the user to confirm. Folding voice changes into individual skills is the failure mode that makes a portfolio of skills slowly drift in voice.

## See also

- the os-skillify handoff — when the feedback is actually a new skill, not a tweak
- `extend` — when the feedback is actually a new mode
- `voiceprint` — when the feedback is voice/tone calibration that belongs in the voiceprint, not in the skill
- `../references/figure-it-out-routing.md` — how routing decides among make/extend/refine
- `../references/inheritance-protocol.md` — what context loads before refining
- `../../_shared/references/skill-prompting-principles.md` — the principles applied to every refine edit
- `../../_shared/references/self-extending-skills.md` — recognize tweak requests that are really self-extension asks; offer the cleaner path
- `os-library/repair` — for fixing frontmatter issues exposed during refine
