# Inheritance protocol — how os-tune reads Personal OS context before generating

os-tune's value over a stock skill-builder — `skill-creator` in Claude and Codex, and most harnesses ship an equivalent under some other name — is that skills made (or modified) inside Personal OS inherit context the OS already has. A skill made anywhere else — a fresh Claude tab, a new GPT, default tooling — starts from a blank slate. This document describes what os-tune loads, in what order, and how it shapes generated/modified skills.

## What os-tune reads before any mode runs

When generation (via os-skillify), `extend`, `refine`, `close-out`, or `reflect` runs, os-tune loads — in this order:

1. **Identity.** `os-inputs/_os-user-profile.md` — the user's name, role, primary work types. Drives the implied-author rule for voiceprint matching (see `os-library/references/matching-discipline.md`).

2. **Voiceprint.** Per the matching-discipline convention, os-tune loads the user's default voiceprint matching the scope of the skill being generated/touched. If the skill produces prose, the voiceprint loads. If the skill is purely structural (e.g., a routing skill with no prose output), voiceprint may not apply — os-tune notes this and proceeds.

3. **Conventions.** `AGENTS.md` — operating principles. New or modified skills must comply: one source of truth, dry-run by default, ship no personal data inside skills, plain language first, capture-and-route discipline (per `skills/_shared/references/capture-decision-tree.md`), etc. The capture decision tree is principle-level inheritance — when a os-tune mode itself captures content (e.g., during `refine`'s inline-after-running path), it applies the same lane-picking logic.

4. **Org rules** (when present). `os-inputs/<org>-rules.md` — per-org operating rules layered onto voiceprint. Voice and positioning constraints, audience-aware copy rules, business-specific conventions (e.g., pricing rules for a consulting practice). Optional — skills work without org rules. When present, generated copy and recommendations comply.

5. **Skills inventory.** Scans `skills/` for existing skill names, descriptions, and mode lists. Used by:
   - generation (os-skillify) — to run the map-before-make check (is the request really a new skill?)
   - `extend` — to choose the target skill
   - `refine` — to identify the skill being refined

6. **Brief.** If a brief in `os-inputs/briefs/current/` matches the project context (per matching-discipline's brief-matching rules), os-tune loads it. Briefs scope the skill to project-specific framing.

7. **Inbox.** `os-inputs/_os-inbox.md` — recent corrections, captures, audit lines, lessons. os-tune scans for items related to the current ask, especially relevant for `refine` (the inline-after-running path) and `reflect` (the longer-cadence pattern surfacer). See `os-inputs/_os-inbox-conventions.md` for the full read/write model and the inbox-vs-system-tracker distinction.

8. **Setup philosophy.** `os-inputs/_os-setup-philosophy.md` — user preferences for tier thresholds, cadence opt-ins, override defaults, adapter choices. Optional — defaults apply when absent. Configurable per user; os-tune respects the overrides without re-asking.

9. **Tracker (system context).** `os-tracker/system.md` — ongoing Personal OS system work, pending followups, active refinements in flight. os-tune reads this to know *intent* — what the system is currently working on. Distinct from inbox: tracker = intent (the work itself); inbox = signal about the work (corrections, lessons, captures). Used by:
   - `refine` and `extend` — to avoid restarting a refinement that's already in flight
   - `reflect` — to detect repeating unresolved work-in-progress as patterns worth elevating
   - generation (os-skillify) — to spot when a stated need overlaps with active work

10. **Skill-prompting principles.** `skills/_shared/references/skill-prompting-principles.md` — the canonical principles every produced or modified skill should follow. Load the file rather than working from a remembered list; it grows as new failure modes get named. Loaded for any meta-skill operation that writes to a skill file: generation (os-skillify)/`skillify` sub-modes, `extend`, `refine`. Without this load, edits tend to regress toward bullet-and-rule defaults that hurt prose-domain and judgment-domain skills.

11. **Self-extending skills disposition.** `skills/_shared/references/self-extending-skills.md` — the additive-vs-complete heuristic and the three-beat self-extending pattern. Loaded by generation (os-skillify)/`skillify` (to decide whether the produced skill carries self-extending behavior), by `extend` (because adding a mode is a moment to ask whether the host skill should gain the disposition if it doesn't have it), by `refine` (because a tweak request shaped as "this skill should also handle X" is a self-extension trigger), and by `reflect` (which flags heavily-used additive skills missing the disposition as refine candidates). Without this load, additive skills stay frozen at their initial capability list and lose the quality that makes them grow alongside the user's practice.

12. **Skill-usage signals (two channels).** Cross-session pattern detection runs on two complementary records:
    - The harness invocation log (optional, user-wired) — one line per skill invocation: timestamp, skill, the opening of the request, working directory. Drives frequency detection. It carries no outcome or tweak count, so "tweaked the same way" is not a signal this source can provide.
    - `os-inputs/_os-inbox.md` task-audit lines (`[type: audit] [skill: none] [task: <slug>]`) — one entry per substantive non-skill action the AI did, with Input / Output / Approach / Request (verbatim) body fields. The verbatim Request string is the cross-session signal — reflect clusters by Request similarity to detect *"you keep asking for this kind of thing — make a skill?"* The AI's task-slug is a hint; the verbatim is the truth.
    
    Privacy configurable per `os-inputs/_os-setup-philosophy.md` (`full | minimal | disabled`). Full spec: `skills/_shared/references/skill-usage-logging.md`.

## How inheritance shapes output

The loaded context flows into generated/modified skills in specific ways.

**Voice.** Generated prose — skill descriptions, mode body content, examples — calibrates to the user's voiceprint. Skills don't sound like a generic assistant. They sound like the user.

**Conventions.** Generated frontmatter, file paths, and structural patterns follow `AGENTS.md`. os-tune won't generate a skill that violates the principles — if the user asks for something that conflicts (e.g., embed a sender filter list inline), os-tune surfaces the conflict and proposes the convention-compliant alternative (per-context profile file).

**Org rules.** When org rules are loaded, generated copy respects them — voice constraints, jargon avoidance, pricing rules, audience-framing rules. If a generated artifact would violate org rules, os-tune surfaces the conflict and proposes the compliant alternative.

**No duplication.** The map-before-make check prevents new skills that overlap existing ones. Existing skills' descriptions are read so os-tune knows what's already covered. Routing surfaces *"this sounds like another mode of your X skill"* when applicable.

**No personal data.** Per `AGENTS.md`'s "ship no personal data inside skills," generated skills never inline user-specific names, account IDs, or filter lists. Those go into per-context profile files (`os-inputs/email-accounts/<account>.md`, etc.). os-tune knows this and won't bake personal data into a skill body.

**Dry-run before write.** Every file write proposal is surfaced as a diff before persisting. Inheritance from `AGENTS.md`'s mutation discipline. The user sees what will change before it changes.

**Project-scoped framing.** When a brief loads, generated skill content stays inside the brief's scope. A skill made under the "client onboarding" brief doesn't accidentally bleed into "newsletter ops" framing.

**Recent feedback.** Inbox items inform the skill body — if the user has captured *"client check-in emails should always include a P.S."* in inbox.md, a new email-related skill (or refine pass on an existing one) reflects that.

**Awareness of work in flight.** When the system tracker shows active work that overlaps with the current ask, os-tune surfaces the overlap rather than proceeding cold. *"Refine on email-skill is already in flight from a prior session — pick up where it left off?"*

## Graceful degradation

If a context source is missing, os-tune surfaces the gap and asks. Same pattern as `os-library/references/matching-discipline.md`:

- **No voiceprint?** Generated prose will sound generic. Ask whether to proceed (accept lower fidelity), supply a sample (chain into `os-voiceprint/from-sample`), or skip.
- **No org rules?** os-tune proceeds without the org-specific layer. Common — many users won't have org rules.
- **No skills inventory?** os-tune can't run map-before-make. Surface and ask whether to proceed without the check (rare — the inventory should exist, even if small).
- **No `AGENTS.md`?** os-tune generates with default conventions and flags the gap. (Also rare — `AGENTS.md` is part of the workspace template.)
- **No brief that matches?** Briefs are usually optional. os-tune proceeds without; offers to write a quick inline brief if the user wants project framing.
- **No inbox?** os-tune proceeds. Inbox is provisional and may be empty.
- **No `_os-setup-philosophy.md`?** Defaults apply. Common until a user overrides something.
- **No system tracker context?** Auto-create on first write per the Tracker contract. Reads return empty until populated.
- **No skill-usage.log?** Refine-candidate detection (skill-frequency-based) degrades; inbox task-audit lines still feed make-skill candidate detection. os-tune surfaces the partial gap when refine candidates would otherwise have surfaced.
- **No inbox task-audit lines?** Make-skill candidate detection degrades; skill-usage.log still feeds refine-candidate detection. Common when `_os-setup-philosophy.md` has `logging.level: minimal`.
- **Both channels disabled (`logging.level: disabled`)?** Reflect and proactive prompting can still operate on inbox corrections/captures/lessons but lose all behavioral pattern detection. os-tune surfaces this clearly so the user can re-enable if they later want pattern surfacing.

Silent approximation is never the answer. The user always sees what's missing.

## Why this protocol matters for the brand

os-tune's promise — *"a skill made inside Personal OS is fundamentally different from a skill made anywhere else"* — depends on this protocol working. Without inheritance, os-tune is a wrapper around the stock skill-builder and the integration moat collapses. The protocol *is* the moat.

Concretely: someone who buys Personal OS and runs os-tune on day one gets skills that:

- Sound like them (voice)
- Respect their org's voice and business rules (org rules)
- Save to the right place (conventions)
- Reference what they already have (inventory awareness)
- Don't duplicate (map-before-make)
- Don't carry personal data into shipped skills (`AGENTS.md` compliance)
- Reflect their recent corrections (inbox.md awareness)
- Know what's in flight (system tracker awareness)

Someone running the stock skill-builder in a fresh chat gets none of these. Same prompt, different artifact. That difference is what the buyer is paying for.

## Inheritance vs override

The user can override any of these defaults in any mode invocation:

- *"Use a non-default voiceprint"* → loads the named voiceprint instead of the user's default
- *"Don't load the brief"* → skips brief loading even if one matches
- *"Skip the inbox"* → doesn't surface recent inbox items as influences
- *"Make this without the conventions"* → produces a skill outside `AGENTS.md` compliance (rare, but supported with a flag)
- *"Don't apply org rules"* → bypass org-rule checks for one run

Overrides are noted in the output's audit trail so the user can see what didn't load. Default is to inherit.

## When inheritance can be partial

For some generation (os-skillify) and `extend` runs, only a subset of the inheritance stack matters. A purely structural skill (no prose, no user-facing copy) may not need a voiceprint or org rules. A one-off tool the user wants to throw away may not need brief alignment. os-tune is allowed to skip parts of the stack when they're irrelevant — but it surfaces what it skipped and why, so the user can correct if the inference was wrong.

The default is full-stack inheritance. Skipping is the exception.

## See also

- `os-library/references/matching-discipline.md` — the reference-loading convention this protocol extends
- `AGENTS.md` — the workspace conventions inheritance enforces
- `skills/_shared/references/capture-decision-tree.md` — the behavioral inheritance applied during capture-related os-tune work
- `skills/_shared/references/skill-prompting-principles.md` — the skill-prompting principles applied during any meta-skill write
- `skills/_shared/references/self-extending-skills.md` — the additive-vs-complete disposition consulted during  extend / refine / reflect
- `os-inputs/_os-inbox-conventions.md` — the inbox / system-tracker write model
- `skills/os-tracker/references/contract.md` — how os-tune modes write through to Tracker
- `references/figure-it-out-routing.md` — how the inheritance feeds the routing decision
