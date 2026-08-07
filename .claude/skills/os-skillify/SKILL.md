---
name: os-skillify
version: 0.1.0
description: >-
  Generate, audit, or consolidate skills and microtools. Eight sub-modes on two axes — four generative routed by input shape (`from-prompt`, `from-content`, `microtool-from-content`, `microtool-from-job`) and four operational over existing material (`enhance`, `dual-lane`, `consolidate`, `interview`). Optional `--type creative|technical|hybrid` lens layers across all sub-modes. Two gates fire first: inheritance protocol (loads Personal OS voice + conventions + library awareness) and map-before-make (avoids duplicating skills that exist). Triggers on "skillify this," "make me a skill from X," "convert this prompt," "design a tool that does Y," "audit my skill library," "consolidate these skills," "dual-lane this," "interview me for a brief," "merge these two drafts." Do NOT trigger when adding a mode (use `os-tune`'s `extend`), tweaking a skill (use `refine`), or capturing lessons (use `close-out`).
display_name: Skillify
tagline: 'Generate, audit, or consolidate skills and microtools — with Personal OS inheritance baked in.'
category: Meta
packs:
  - personal-os
icon: 'phosphor:MagicWand'
when_to_use: >-
  Skillify is the generative and curatorial surface of Personal OS — the verb
  that turns a prompt, a piece of content, or a stated need into a working
  skill or microtool, and the surface that audits, splits, consolidates, and
  re-shapes existing skills as the library matures.


  Reach for this when you want to make a new skill from a prompt, an article,
  a transcript, or a stated need; or when you want to audit, consolidate, or
  improve existing skills; or when you want two parallel drafts merged into
  one stronger result. os-tune calls this skill from its `figure it out`
  router when the routing decision lands on "make" or "audit / consolidate"
  rather than `extend` / `refine`.
modes:
  - name: from-prompt
    job: Convert an existing prompt, SOP, or GPT persona into a skill (6-phase preservation workflow).
  - name: from-content
    job: Build a multi-mode Cowork-native skill from long-form content (broad scope).
  - name: microtool-from-content
    job: Build a focused single-mode skill or copy-pasteable prompt from long-form content (narrow scope).
  - name: microtool-from-job
    job: Build a focused tool from a stated need / pain / concept (no source content).
  - name: enhance
    job: Audit, consolidate, idiom-modernize, and improve already-existing skills (cross-skill scope).
  - name: dual-lane
    job: Spawn this skill + a different-lineage skill-drafter in parallel from one brief; auto-consolidate.
  - name: consolidate
    job: Merge two existing skill drafts into a single skill with consolidation rationale.
  - name: interview
    job: Build a skill brief conversationally when source material is thin.
type_lens:
  parameter: '--type creative|technical|hybrid'
  default: ask once when input doesn't make type obvious
  shapes: interview questions, stress-tests, consolidation rubric, divergent-strengths instructions, house-style sections emitted
---

# Skillify — generate, audit, or consolidate skills and microtools

## Purpose

Skillify is the generative and curatorial side of os-tune. It produces new skills and microtools from raw content, from a stated need, or from an existing prompt — and it audits, consolidates, splits, and re-shapes existing skills as the library matures. Output can be a Cowork-native skill or a copy-pasteable code-fenced prompt depending on portability needs.

The skill's value over a stock skill-builder — `skill-creator` in Claude and Codex, and most harnesses ship an equivalent under some other name — is the two gates. A skill made or modified through skillify inherits Personal OS context — voice (from voiceprint), conventions (from `AGENTS.md` / `CLAUDE.md`), org rules (when present), existing-skill awareness (from inventory scan), and recent feedback (from inbox + system tracker). A skill made anywhere else starts from a blank slate. The integration moat lives in those gates working.

## When to use

The eight sub-modes route on two axes: **input shape** for generative work, and **operation over existing material** for curatorial work.

**Generative sub-modes (input-shape routing):**

- *"Skillify this prompt"* / *"convert this prompt"* / *"turn this SOP into a skill"* → `from-prompt`
- *"Build a skill from this transcript"* / *"design a skill that operationalizes this article"* / *"make this content into a skill"* → `from-content`
- *"Make a focused tool from this content"* / *"give me a copy-pasteable prompt that does X based on this article"* → `microtool-from-content`
- *"Design a tool that does X"* / *"I have this pain point — what tool would help"* / *"make me a micro-tool for [job]"* → `microtool-from-job`

**Operational sub-modes (existing-material routing):**

- *"Audit my skill library"* / *"consolidate these skills"* / *"find redundancy across these skills"* / *"modernize these Codex-era patterns"* / *"split the X skill — it's doing two things"* → `enhance`
- *"Run dual-lane on this"* / *"parallel-draft this skill with skill-creator"* / *"two-lane this skill"* — for foundational, multi-mode, voice-critical, first-of-a-kind, or high-stakes skills → `dual-lane`
- *"Merge these two skill drafts"* / *"consolidate `draft-a.md` and `draft-b.md`"* — or auto-invoked at the end of a `dual-lane` run → `consolidate`
- *"Interview me for a skill brief"* / *"help me figure out what this skill should do"* / *"build me a brief before drafting"* — or auto-invoked when other sub-modes detect insufficient input → `interview`

Don't fire for:

- Adding a mode to an existing skill — route to `os-tune`'s `extend`.
- Tweaking how an existing skill behaves — route to `refine`.
- Wrapping a session and capturing lessons — route to `close-out`.
- Storing reference inputs — route to `os-library/save`.

## Sub-modes

| Sub-mode | Input / Trigger | Output |
| --- | --- | --- |
| `from-prompt` | Existing prompt, SOP, or GPT persona with craft worth preserving | Full skill structure or fold-in to existing skill, via 6-phase classification → rationale → destination → build → verify → log workflow |
| `from-content` | Long-form content (article, transcript, book chapter, lecture notes) — substantial enough to fuel a multi-mode skill | Full Cowork-native skill (`SKILL.md` + 1-N modes + references) |
| `microtool-from-content` | Same content types, narrower scope — captures one tight job from the source | Single-mode Cowork skill OR copy-pasteable prompt with the canonical 7-section anatomy |
| `microtool-from-job` | Stated need (pain point, concept name, job-to-be-done) — no source content | Single-mode skill OR copy-pasteable prompt; clarification interview runs first if the need is thin |
| `enhance` | One or more already-existing skills | Modified live skills (consolidate / split / adapt / augment); decision log per skill; verification + snapshot discipline |
| `dual-lane` | A brief artifact + skill-slug | Two parallel lane drafts at `experiments/<slug>/`; auto-consolidated `SKILL.md` at the destination |
| `consolidate` | Two skill drafts + destination | Single consolidated `SKILL.md` with mandatory consolidation rationale (inline or sidecar) |
| `interview` | Anything from a vague request to a partial idea to an existing stub | Brief artifact at `experiments/<slug>/BRIEF.md` (or wherever specified); type-lens-aware question pool |

## Routing logic — picking the sub-mode

The dispatcher reads the input shape and the user's intent:

- **An existing prompt / SOP / GPT persona supplied** → `from-prompt`.
- **Long-form content supplied + scope is broad** (covers a domain with multiple jobs) → `from-content`.
- **Long-form content supplied + scope is focused** (one tight job) → `microtool-from-content`.
- **No content supplied, only a need / pain / concept** → `microtool-from-job` (which runs its own narrow clarification interview when the need is too thin to design from).
- **One or more existing skills + intent to audit / consolidate / split / modernize** → `enhance`.
- **Foundational / multi-mode / voice-critical / high-stakes skill + intent to draft with parallel divergent lanes** → `dual-lane`.
- **Two existing drafts + intent to merge** → `consolidate` (also auto-invoked at the end of `dual-lane`).
- **Vague request or insufficient input + intent to think through what the skill should be** → `interview` (also auto-invoked when other sub-modes detect insufficient input).
- **Ambiguous between sub-modes** — surface the options with one-line rationale and ask the user to pick. Don't guess on the input shape.

The user can short-circuit by naming the sub-mode explicitly (*"run from-content on this"*); routing is bypassed. The graceful-degradation rule still applies — if the named sub-mode doesn't fit the input, surface the mismatch rather than silently approximating.

When the user's request mixes sub-modes (*"interview me, then dual-lane this"* or *"convert this prompt AND consolidate it with the existing X skill"*), name the chain. Common chains:

- `interview` → `dual-lane` → (auto) `consolidate` — most thorough path for foundational skills.
- `interview` → `from-prompt` — when the user has a legacy prompt but the conversion needs a brief first.
- `from-prompt` → `enhance` — convert a new source, then run an enhance pass over the cluster it joins.
- `enhance` → `from-prompt` — audit reveals a missing sibling skill; convert the source, then re-run enhance.

## Type lens — `--type creative|technical|hybrid`

A parameter that layers on top of any sub-mode. Adjusts what questions get asked, what stress-tests get applied, what house-style sections get emitted, and how consolidation weights elements.

- **`creative`** — variety / voice / anti-collapse focus. Subjective quality. Failure mode: *feels like AI wrote it.* Examples: fiction skills, persona skills, content-generation skills.
- **`technical`** — precision / invariants / edge-case focus. Objective verifiability. Failure mode: *breaks in production.* Examples: code-generation skills, deployment skills, validation skills, schema skills.
- **`hybrid`** — situational mixed. The user picks question-by-question or section-by-section which lens applies where. Examples: PR-description skills, documentation skills, infrastructure-narrative skills.

If `--type` is unspecified, skillify infers from input (source files, intended use, target file types) or asks once during setup. *Asking is cheap.* Don't infer wrong silently.

**Modes and types are orthogonal axes.** The sub-mode describes *what skillify does*; the type lens describes *how the sub-mode adapts*. The lens doesn't replace a sub-mode — it shapes the questions asked during the workflow and the sections emitted in the resulting `SKILL.md`.

Full framework at `references/type-lens.md`.

## The two gates

Both gates fire before any sub-mode procedure executes. Inline in the dispatcher; sub-modes assume gates have passed.

### Gate 1 — Inheritance protocol

Loads Personal OS context per `../os-tune/references/inheritance-protocol.md` — the protocol file is the sole canonical enumeration of sources; in brief they cover: identity, voiceprint, conventions (`CLAUDE.md` / `AGENTS.md` + capture-decision-tree), org rules (when present), skills inventory, brief, inbox, setup philosophy, system tracker, skill-prompting principles, skill-usage logs (two channels — `_os-skill-usage.log` JSONL + inbox task-audit lines).

The produced or modified skill inherits voice (from voiceprint), convention compliance (from `CLAUDE.md` / `AGENTS.md`), and existing-skill awareness (from inventory). Without this gate, skillify would produce skills that are voice-generic and convention-blind — same problem as the stock skill-builder.

For curatorial sub-modes (`enhance`, `consolidate`), the inheritance protocol bounds what "stronger" means during decisions — the voiceprint and convention scan inform whether a proposed consolidation respects established patterns.

Graceful degradation per the protocol: missing sources surface to the user; nothing silently approximates.

### Gate 2 — Map-before-make check

Runs the routing logic per `../os-tune/references/figure-it-out-routing.md` to surface whether the request is actually a candidate for `extend` or `refine` against an existing skill. Even when the user invoked skillify directly, the check fires. If a strong match against an existing skill surfaces, the dispatcher hands off to `extend` (for new behavior coherent with an existing skill) or `refine` (for feedback that's really a tweak) and asks the user to confirm.

For `enhance` mode, the check is adapted: the question isn't *does this overlap with an existing skill?* (everything is an existing skill); it's *does this consolidation / split decision affect skills outside the surveyed set?* If so, surface explicitly before applying.

The user can override and force generation or modification, but the check fires either way. Without this gate, skillify would happily duplicate skills that already exist or modify skills outside the scope the user intended.

## Operating principles

- **Both gates always fire.** No fast path for "obvious" operations. The two gates are what make skillify different from generic tooling.
- **No fast path for "obvious" prompt conversions either.** The `from-prompt` sub-mode runs all 6 phases regardless of how simple the source looks. Speed comes from practice, not skipping steps. Hidden craft hides in chunks that look routine.
- **Writes follow `_shared/references/skill-update-protocol.md`.** Show-before-write, sanity checks per file, batched confirmation for multi-file operations. Curatorial sub-modes add snapshot-before-changes discipline on top.
- **Lossless by default.** Every conversion produces a decision-log entry. Every consolidation logs what was kept from each lane and what was discarded. Every `enhance` finding gets a log entry, even `NO-OP` ones. Nothing silently vanishes.
- **Preserve craft, not surface phrasing.** When a chunk is classified as a craft move (uniquely-effective phrasing, sequence, or directive), its exact wording is part of what makes it work. Don't paraphrase craft.
- **Mirror named frameworks and step-counts.** If the source has named frameworks, the produced skill references them by name and uses their structure. If the source uses 3 pillars, the skill has 3 pillars (not 5 for symmetry).
- **Stay inside the source.** Don't add frameworks the source doesn't have. Inference about what's implied is fine; invention is not.
- **Substantive disagreements are pick-or-punt, never softened.** When two drafts disagree on substance during `consolidate`, pick deliberately (with reasoning surfaced in the rationale) or mark as TBD. Never silently average.
- **Negative triggers in frontmatter descriptions.** Generated skill descriptions end with explicit *"Do NOT trigger for X"* phrasing when confusion with adjacent skills is likely. Negative triggers affect routing directly.
- **Produced skills follow the skill-prompting principles.** Canonical reference at `../_shared/references/skill-prompting-principles.md` — load it, don't recall it. See the section below; this is a real requirement, not a stylistic preference.
- **Produced skills carry self-extending behavior when the skill is additive.** Skills serving a domain where the user's needs keep producing new shapes get the three-beat self-extension pattern (surface the gap, offer two paths, hand off cleanly); skills that perform one stable job once well do not. The additive-vs-complete heuristic and the full pattern live in `../_shared/references/self-extending-skills.md`. Assess additive-vs-complete during Phase 3 destination planning (in `from-prompt`); include or omit the section accordingly in the build phase.
- **TBD rationale can ship.** If a rationale item can't be resolved before v0.1 ships, name it explicitly as TBD rather than fabricating one. Honest beats tidy.
- **Shared references promote at the two-skill threshold.** Two skills loading the same reference for the same reason is enough to promote to `_shared/references/`. Waiting for a third risks duplication and drift.
- **Skills ship empty.** Per `AGENTS.md`, generated skills carry no user-specific data inline. Per-context profiles populate at runtime.
- **Generated skills reference the storage methodology, never invent their own.** Any produced skill whose runs yield substantial artifacts gets one line: outputs persist per the knowledge-system invariants (`_shared/references/workspace-layout.md`), with the project-vs-exploring read (capture decision tree) deciding silent-save vs offer. No per-skill save schemes.
- **No silent approximation.** When inheritance sources are missing, surface the gap. When the input shape doesn't fit the chosen sub-mode, surface the mismatch.
- **Dual-lane is for foundational skills, not all skills.** Two subagent runs + consolidation costs real budget. Use it when the skill is foundational, complex, or carries real weight for taste / judgment. Leaf skills and simple utilities run single-lane. The mode itself can suggest *"this looks like a dual-lane candidate"* based on brief signals.
- **Brief quality bounds output quality.** The single highest-leverage point in the skillify workflow is the brief. When the input is thin, route through `interview` before drafting starts. Brief-building is itself craft.

## How the produced skill should be written

Every generated or modified skill follows the prompting principles in `../_shared/references/skill-prompting-principles.md`. Load that file before producing any artifact — it's the canonical list, it grows as new failure modes get named, and it carries the before/after pairs that make each one usable. This section deliberately doesn't restate it: a summary here would go stale the moment the reference gains a principle, and a stale summary is worse than a pointer because it reads as complete.

What the principles collectively protect against is one thing: a frontier model's defaults. Left alone, a produced skill drifts toward bullets where prose belongs, rules where the craft is a judgment call, verbatim sample text the next model will copy word for word, compression that reads fine to a machine and opaque to the human maintaining it, and absolute phrasing that suppresses moves the author never thought to allow. Every principle in the reference names one of those and gives the counter-move. Templates carry the same patterns forward by example.

## Output formats (microtool sub-modes)

Two output formats supported across the microtool sub-modes:

**Cowork-native skill** — full skill structure with `SKILL.md` + frontmatter + mode files + references. Lives at `skills/<name>/`. Iterates via `refine` / `extend`. Best when the tool will be used inside Cowork, integrates with library, expects iteration.

**Copy-pasteable code-fenced prompt** — single markdown code fence containing the canonical 7-section anatomy. No frontmatter, no skill structure. Drop into any LLM. Best when the tool will be used outside Cowork, shared with non-Cowork users, used as a one-shot in another LLM, or included in documentation.

The full tradeoff is in `references/output-format-tradeoffs.md`. The microtool sub-modes ask which format the user wants if not specified.

For `from-content`, the output is always a Cowork-native skill — the format only branches on how many modes the skill has.

## Tool-wrapper skills — bank the tool knowledge a session just earned

When a session has just earned external-tool knowledge the hard way — docs fetched, auth untangled, an MCP's real tool names discovered, a working invocation finally landed — offer to bank it as a small wrapper skill (or extend the existing wrapper for that tool). This is an instant offer, exempt from the usual repeated-pattern threshold: the re-discovery cost is obvious the first time, and the knowledge evaporates at session end if uncaptured. Generation routes through the normal sub-modes (`microtool-from-job` usually); the contents standard — working subset only, proven auth, credential pointers never secrets, the user's permission ledger, last-verified dates, and the self-update line every wrapper carries — is in `references/tool-wrapper-skills.md`. Load it before generating any wrapper.

## When the requested generation or operation shape isn't yet a sub-mode

The eight sub-modes cover the input shapes and operations the current design anticipates. When a user surfaces a request that doesn't cleanly fit — a new input shape (audio recording, a feedback log, a chat transcript with mixed intent), a hybrid that wants two sub-modes worth of behavior, or an output shape the current modes don't produce — surface that the request sits outside the existing routing rather than forcing it through the closest mismatch.

Offer two paths. First, set up for next time: route the meta-request through skillify itself (this skill generates skills, including new versions of itself or new sibling sub-modes) or through `extend` on this skill so the new sub-mode lands as part of the regular run. Second, produce once without setup: handle the current request inline using whichever sub-mode is closest, with the gaps named explicitly so the user can decide whether to iterate.

When the same off-pattern request shows up two or three times across sessions, that's the moment to actually extend rather than keep handling inline. The reason this matters: skillify's value comes from the gates inheriting Personal OS context, and an off-pattern request handled inline doesn't accumulate into a sub-mode the next user benefits from. Treating skillify as additive — and meaning it — is how the generation surface keeps pace with what people actually want to make. Full principle at `../_shared/references/self-extending-skills.md`.

## Design Rationale — what changed in v0.2

This skill was substantially expanded in v0.2 to integrate cross-system learnings from operating skillify outside Personal OS (running it in Claude Code's standalone skills tree, drafting the Autowriter Fiction stack, observing real consolidations between os-skillify and `skill-creator`):

- **Modes and types as orthogonal axes**, not entangled. The operation (`from-prompt` / `from-content` / `microtool-from-content` / `microtool-from-job` / `enhance` / `dual-lane` / `consolidate` / `interview`) describes *what skillify does*. The type lens (`creative` / `technical` / `hybrid`) describes *how the operation adapts*. They blend rather than conflict because type is a lens applied across operations, not a peer to operations. If in practice a type-specific operation diverges enough in *steps* (not just content within steps), it should split into its own sub-mode — reserve that right.
- **Curatorial sub-modes (`enhance`, `dual-lane`, `consolidate`) live alongside generative sub-modes**, not in a separate skill. They share the two gates, the disposition vocabulary, the skill-prompting principles, and the skill-update-protocol. Splitting them into a sibling skill would duplicate the gate logic.
- **`dual-lane` names the counterpart explicitly** (default: `anthropic-skills:skill-creator`) rather than just *"run twice."* The divergence is real because the two skills come from different lineages. Running skillify-twice would converge.
- **`consolidate` is a distinct sub-mode**, not buried inside `dual-lane`, because it has standalone value (user has two drafts from anywhere, wants merged) and because separating it lets `dual-lane` optionally stop short for human-in-the-loop review.
- **`interview` is a top-level sub-mode** because brief quality is the single highest-leverage point. Building the brief is itself craft, not setup overhead. The interview output is a first-class artifact (the brief) that downstream sub-modes consume. The narrower clarification used inside `microtool-from-job` shares craft with `interview` and shares a single reference (`interview-the-need.md`) but operates at a tighter scope.
- **Divergent-strengths instructions are first-class**, encoded in `references/divergent-strengths-templates.md`. Telling each lane *"optimize for X"* sharpens consolidation choices. Two lanes told the same thing converge and produce no real comparison.
- **Type-lens default to "ask once"** rather than "always require" or "always infer." Inferring wrong silently is worse than asking; requiring is friction. Asking once is the right middle.
- **Hybrid type means "user picks question-by-question"** rather than "apply both checklists wholesale." Wholesale-both produces bloat. Situational-mixed produces what the skill actually needs.

All v0.1 craft preserved. Classification, rationale extraction, naming conventions, disposition vocabulary, the four input-shape sub-modes, the two gates — all canonical. v0.2 adds; it doesn't replace.

## See also

- `../os-tune/modes/extend.md` — when the ask is really a new mode of an existing skill
- `refine` — when the ask is really feedback on an existing skill
- `os-library/save` — for persisting copy-pasteable prompts as templates
- `../os-tune/references/inheritance-protocol.md` — what context loads before generating
- `../os-tune/references/figure-it-out-routing.md` — the routing logic the map-before-make check applies

**Sub-mode references (in this skill's `references/` dir):**

- `references/classification-taxonomy.md` — used by `from-prompt` Phase 1
- `references/rationale-extraction.md` — used by `from-prompt` Phase 2
- `references/craft-preservation-from-content.md` — used by content-driven sub-modes
- `references/microtool-anatomy.md` — the 7-section structure used by microtool sub-modes
- `references/output-format-tradeoffs.md` — Cowork-native vs copy-pasteable choice
- `references/interview-the-need.md` — question bank covering microtool-clarification (scope A) and full-brief building (scope B); used by `microtool-from-job` and `interview`
- `references/type-lens.md` — creative / technical / hybrid framework
- `references/divergent-strengths-templates.md` — type-lens-aware divergent-strengths instructions for `dual-lane`
- `references/consolidation-rubric.md` — type-lens-aware element weighting for `consolidate`
- `references/cluster-coherence-signals.md` — patterns used by `enhance` Phase 2 and `from-prompt` cluster decisions
- `references/disposition-vocabulary.md` — canonical labels for sources, findings, and consolidation decisions
- `references/prompt-based-vs-tool-wrapper.md` — early-triage pattern for `from-prompt` and `enhance`
- `references/tool-wrapper-skills.md` — contents standard for external-tool wrapper skills (load before generating any wrapper)

**Shared references (load from `_shared/references/`):**

- `../_shared/references/skill-update-protocol.md` — write discipline for all sub-modes
- `../_shared/references/skill-prompting-principles.md` — the principles every produced skill follows
- `../_shared/references/self-extending-skills.md` — when produced skills should include the self-extending three-beat pattern (additive) vs leave it out (complete)
- `../_shared/references/example-rules.md` — example selection rules for produced skills
- `../_shared/references/scaffolding-patterns.md` — how to assess scaffolding in source prompts
- `../_shared/references/skill-vs-mode-vs-reference.md` — destination decision tree
- `../_shared/references/naming-conventions.md` — naming rules for produced files
- `../_shared/references/frontmatter-format.md` — Cowork-validator frontmatter rules

**Templates (in this skill's `templates/` dir):**

- `templates/SKILL.md.template` — scaffold for a new skill's `SKILL.md`
- `templates/mode.md.template` — scaffold for a mode inside a category skill
- `templates/reference.md.template` — scaffold for a reference doc
- `templates/decision-log-entry.template` — decision-log entry
