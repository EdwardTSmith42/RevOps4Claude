# Promotion paths

For `[type: correction]` entries, where should the lesson durably live? Capture proposes one target with a confidence read. The user confirms or redirects.

## Three targets

- **`AGENTS.md`** (workspace root) — cross-cutting operating principles. The correction shapes how the system works *across* skills.
- **A skill's `references/<topic>.md`** — skill-specific patterns. The correction applies to one skill's behavior.
- **An SOP or dedicated doc** — procedures, step-by-step workflows. The correction names a sequence the user does the same way each time, or a multi-step rule that's bigger than a reference but doesn't need its own skill.

## Heuristic

Apply in order:

### 1. Does the correction name a principle that applies across multiple skills?

If yes → **AGENTS.md**. The correction is durable cross-cutting guidance.

Signals:
- The correction is about voice, register, or interaction style
- The correction is about how the user thinks, makes decisions, or wants AI to behave generally
- The correction would apply equally well in 3+ skills if it came up

Example shapes:
- A vocabulary or phrasing preference the user wants honored anywhere the AI speaks for them — voice, applies anywhere
- An interaction principle about when to push back or defer to the user — cross-cutting
- A taxonomy or design heuristic that should govern multiple skills' behavior — cross-cutting

### 2. Does the correction name a behavior of one specific skill?

If yes → **the skill's `references/<topic>.md`**. The correction is skill-specific calibration.

Signals:
- The correction is about how a particular skill should classify, format, or route
- The correction is about a default the skill should adopt
- The correction names the skill (or one is unambiguous from context)

Example shapes:
- A correction about how one skill should present its output → that skill's relevant reference (or a new one)
- A correction about a default behavior the user wants a specific skill to adopt → that skill's operating-principles section or a dedicated reference
- A correction about how a particular skill should classify or auto-handle something → that skill's classification or schema reference

### 3. Does the correction name a multi-step procedure?

If yes → **an SOP or dedicated doc**. The correction is a workflow the user does the same way each time, bigger than a reference, smaller than a skill.

Signals:
- The correction has steps in a specific order
- The correction would be invoked as "follow my <X> SOP" rather than as a passing rule
- The procedure is durable but doesn't justify a full skill (no triggers, no modes)

Example shapes:
- A pre-flight checklist the user runs before a particular kind of release → `sops/<name>-checklist.md`
- A periodic review ritual the user does on a fixed cadence → `sops/<cadence>-review.md`

### 4. None of the above — surface the ambiguity

If the correction doesn't fit cleanly into any of the three targets, surface the ambiguity rather than forcing a target. Two paths:

- Ask the user where it should go, with the three target descriptions surfaced
- Defer the entry (`[status: deferred]`) until a clearer pattern emerges from related corrections

## Confidence

For each correction entry, assign a confidence:

- **High** — one target fires cleanly, no ambiguity
- **Medium** — one target is most likely but one other is plausible. Surface both with a recommendation.
- **Low** — the correction could go in 2-3 places equally well. Surface the ambiguity, ask, or defer.

## Promotion mechanics

When the user confirms a target:

1. **Write the lesson** to the chosen target — append to AGENTS.md, append to a skill ref, create or append to an SOP. Use the user's voice; preserve verbatim quotes where the correction was specific.
2. **Mark the inbox entry promoted** — append `*Promoted to: <target-path>*` italic line below the entry. Set `[status: resolved]`.
3. **Update related artifacts** — if the promotion changes a default or convention referenced elsewhere, surface those references for review (don't auto-edit; a single principle change can ripple).

When the user redirects:

- Apply their chosen target instead.
- Note the redirect for future heuristic calibration (a recurring redirect pattern is a signal the heuristic should evolve).
