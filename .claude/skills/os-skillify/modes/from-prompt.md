---
name: from-prompt
description: >-
  Sub-mode of `skillify`. Converts a legacy prompt, SOP, or GPT persona into a Cowork-native skill, a mode within an existing skill, a shared reference doc, or a template — without losing the craft that made the original work. Six-phase workflow: classify → surface rationale → plan destination → build → verify → log. Preserves three things the original author spent years refining — the craft (specific moves that shape output quality), the rationale (why those moves work), and the judgment (heuristics that keep outputs sharp under edge cases). Triggers on "convert this prompt to a skill," "skillify this prompt," "turn this SOP into a skill," "import this legacy prompt," "decide where this prompt's knowledge belongs in the library." Do NOT trigger when generating from raw content (use sibling `from-content`), from a need (use sibling `microtool-from-job`), or for a focused tool from content (use sibling `microtool-from-content`).
---

# Sub-mode — Skillify from prompt

Convert a hand-crafted prompt into a Cowork-native skill while preserving the craft, rationale, and judgment baked into the original. Scaffolding (the patches and incantations added to coax older models) is mostly noise on frontier models, but some of what *looks* like scaffolding hides real craft. This mode assesses rather than auto-drops.

Handles full conversion end to end: classification, rationale extraction, destination planning, file creation, verification, and decision logging.

## When to use

- The user wants to convert one or more legacy prompts into skills
- The user wants to decide whether a prompt should become its own skill, a mode of an existing skill, a shared reference, or a template
- The user wants to audit a converted skill against its original

## Preconditions

Two gates apply before this sub-mode runs, per the parent `skillify` dispatcher:

1. **Inheritance protocol** — loads Personal OS context per `../../os-tune/references/inheritance-protocol.md`. The produced skill inherits voice and convention compliance.
2. **Map-before-make check** — runs the routing logic per `../../os-tune/references/figure-it-out-routing.md`. If the source prompt's content overlaps with an existing skill, the dispatcher offers `extend`/`refine` as alternatives before the conversion proceeds.

Additionally, before Phase 4 (Build) writes anything, load `../../_shared/references/skill-prompting-principles.md` and apply its principles to every file produced. This is what keeps converted skills from regressing toward bullets-and-rules defaults — especially when the source prompt is for a writing-domain or judgment-domain job.

Also load `../../_shared/references/self-extending-skills.md` during Phase 3 (destination planning) and assess whether the skill being built is additive (its value grows as the user's library, mode list, or coverage accumulates) or complete (one well-defined job done once well). When the source prompt encodes an additive skill — a writing producer, an editing tool, a voice-capture skill, an audience analyzer, anything where new shapes will keep arriving — Phase 4 builds the produced skill with the three-beat self-extending section. When the source prompt encodes a complete skill, the section is omitted; adding self-extension language to a complete skill is over-engineering. The reference carries the heuristic and the canonical three-beat pattern.

When the source is an SOP, also load `../../_shared/references/sop-completeness.md` and grade it (runnable / partial / named-only) before converting — a partial or named-only SOP converts into a skill that performs confidence the source can't back, so surface the grade and let the user decide whether to fill the gaps first.

See `SKILL.md` for the gate logic.

## Six-phase workflow

Run the phases in order. Each phase produces an artifact before the next phase starts.

### Phase 1 — Classify

Read the source prompt end to end. Tag every chunk into one of six categories (see `../references/classification-taxonomy.md` for the full taxonomy and examples):

1. **Trigger / framing** — what job it does, who it serves, when it applies
2. **Craft moves** — specific phrasings, sequences, or directives that shape output quality (preserve verbatim)
3. **Domain knowledge** — definitions, taxonomies, checklists, criteria (extract to references)
4. **Output shape** — strict format requirements, section order, field structures (extract to templates)
5. **Examples** — canonical sample outputs (disposition per `../../_shared/references/example-rules.md`)
6. **Scaffolding candidate** — tip bribes, persona cosplay, performance-coaxing, step-numbering, XML ritual wrappers. Apply the assessment procedure in `../../_shared/references/scaffolding-patterns.md` before deciding disposition. Some chunks that look like scaffolding carry real craft.

**Produce the classification table as an explicit intermediate artifact.** Write it to a WIP location (`source/extracted-skills/<source-name>-classification.md`) before moving to Phase 2. This creates a checkpoint — a misclassification can be caught before it propagates through the rest of the workflow.

### Phase 2 — Surface the rationale

This is the phase that makes converted skills trustworthy under edge cases. For every chunk tagged as a **craft move** or **judgment heuristic**, ask: *why does this work?*

- If the rationale is stated in the source (even as an aside), lift it verbatim into the rationale notes.
- If the rationale is implicit, ask the user to articulate it before continuing. Don't guess. Tacit craft is the most valuable thing being preserved.
- Record each rationale as a one-liner: *"[move]* works because *[reason]*."

These rationale notes become the "Design Rationale" section in the converted skill's SKILL.md.

See `../references/rationale-extraction.md` for prompting patterns and examples.

### Phase 3 — Plan destination

Decide what the source becomes. Four options:

- **New standalone skill** — a distinct job with no close siblings in the existing library
- **Mode within an existing or new category skill** — shares reference material with siblings
- **Shared reference doc only** — pure domain knowledge, no job logic
- **Template only** — a stable output shape referenced by existing skills

Apply the "shared load" heuristic: if two prompts would load the same reference doc for the same reason, they belong as modes of one skill, not as separate skills. Full decision tree in `../../_shared/references/skill-vs-mode-vs-reference.md`.

Also assess whether the skill warrants companion agents. The test: does the skill involve two or more independent analytical passes — workstreams that don't need to wait on each other's output? If yes, plan one agent per parallel workstream. Typical candidates are category skills with multiple modes that could run concurrently. If agents are warranted, name them in the plan alongside the skill files.

Produce a plan: destination path, files to create, references to reuse, modes to group, and agents to build (if any).

### Phase 4 — Build

Writes follow `../../_shared/references/skill-update-protocol.md` — show all proposed files as a batch (Create mode for new skills; Modify mode if folding into existing skills), confirm, write, sanity-check each. Sanity checks include frontmatter validity and cross-reference resolution per the protocol.

Wrap the writes in auto-save: invoke `os-autosave snapshot` with a name like `pre-skillify-<skill-name>` before persisting, then `os-autosave commit` with message `os-tune skillify: <skill-name> — created from prompt` after a successful sanity check. If sanity check fails, revert to the snapshot.

Create the files directly at the canonical location `skills/<skill-name>/`, following the templates in `../templates/`. For each converted skill, produce:

- `SKILL.md` — trigger, run logic, **Design Rationale** section, pointers to references and templates. Frontmatter description ends with "Do NOT trigger for X" if confusion with adjacent skills is likely.
- `references/*.md` — extracted domain knowledge. Shared references live at `skills/_shared/references/<file>.md` and are referenced via relative paths.
- `modes/*.md` — for category skills with multiple modes.
- `templates/*.md` — strict output shapes (loaded only in strict mode).
- `examples/*.md` — per `../../_shared/references/example-rules.md`. Prefer 5–10 strong examples or none. Avoid single cringe-prone exemplars. Legacy examples ship with the `legacy-` prefix and frontmatter documenting concerns and replacement priority.
- `agents/*.md` — one file per companion agent, if Phase 3 called for them. Each agent file carries YAML frontmatter (`name`, `description` with `<example>` blocks) and a system prompt in the markdown body.

Naming and path conventions follow `../../_shared/references/naming-conventions.md`. Frontmatter follows `../../_shared/references/frontmatter-format.md` (Cowork-validator-compliant `description: >-` block-folded scalar, descriptions under 1024 chars). Shared-reference promotion follows the two-skill threshold.

### Phase 5 — Verify

Run the converted skill against a representative input — real content the original prompt was designed for. Compare output to what the original prompt produces. Four checks:

- **Craft preserved** — does the output show the same distinctive moves?
- **Rationale holds** — if the user asks for a variation, does the Design Rationale give the agent enough judgment to adapt without breaking the thing?
- **Example quality** — do the included examples still read as strong exemplars, or are they AI-dated / weak? Apply `../../_shared/references/example-rules.md` criteria. Replace, drop, or flag as needed.
- **No silent loss** — is there anything in the source that doesn't appear somewhere in the conversion (skill / reference / template / example) or in the decision log?

Produce a verification note: the test input used, the output produced, the comparison. This goes into the decision log under "Verification." A conversion is not complete until all four checks have been run and recorded.

**For multi-skill batches** (when a classification pass produced several related skills at once), write a batch verification file at `<workspace>/decision-log/_VERIFICATION-BATCH-<YYYY-MM-DD>.md`. The batch file records structural verification for all skills in the batch, per-skill craft-preservation test plans, expected-failure-mode list, and cross-skill notes.

Expected-failure-mode catalog worth watching for during craft-preservation tests:

- **Over-scaffolding removal** — a dropped craft move that was actually doing work. Identified when converted output is noticeably blander than original.
- **Mode-routing ambiguity** — inputs the skill can't clearly route. Mode criteria need sharpening.
- **Example gap** — a mode with zero examples producing uneven output across runs.
- **Rationale hole** — asking the skill for a variation and watching it break. Suggests the Design Rationale isn't teaching the right adaptation.

### Phase 6 — Log

Write a decision-log entry at `<workspace>/decision-log/` following `../templates/decision-log-entry.template`. Entries record: source path, destination path(s), disposition (SHIP NOW / ADAPT / MERGE / ARCHIVE / BONUS ONLY / BACKEND ONLY), classification table, rationale notes captured, what was dropped and why (including scaffolding assessment outcomes), example decisions, verification notes.

Two patterns:

- **Standalone skill** (one source → one skill) — one decision-log file, named after the source prompt. Full entry per the template.
- **Category skill** (multiple sources → one skill with modes) — one consolidated decision-log file named after the skill (e.g., `audience (category skill).md`) covering all sources and design decisions, plus one thin stub file per source that points at the consolidated entry. Preserves "one entry per source filename" discoverability while avoiding content duplication.

The log is the lossless-by-default guarantee. Every source prompt produces an entry (or stub) before conversion is considered complete.

## Operating principles

- **No fast path for "obvious" conversions.** Every prompt runs the full six-phase workflow. Prompts that look like simple ports often hide the most interesting craft. Speed comes from practice, not skipping steps.
- **Lossless by default.** Every source prompt produces a decision-log entry. Nothing silently vanishes.
- **Preserve wording on craft moves.** When a chunk is classified as a craft move, its exact phrasing is part of what makes it work.
- **Assess scaffolding — don't auto-drop.** Apply the three-question assessment in `../../_shared/references/scaffolding-patterns.md` to every scaffolding candidate before dropping. Hidden craft hides inside scaffolding more than anywhere else.
- **Examples are high-leverage and high-risk.** A bad example mis-trains the skill more than a missing example does.
- **Negative triggers in frontmatter descriptions.** Every generated skill's description ends with "Do NOT trigger for X" phrasing when confusion with adjacent skills is likely.
- **Frontmatter must survive Cowork's validator.** Follow `../../_shared/references/frontmatter-format.md` for the canonical description-routing and YAML rules; do not restate or narrow them from memory here.
- **Malleability notes on shared references.** References promoted to `_shared/` carry a "Malleability note" section clarifying what's canonical and what's adaptable. Prevents references from becoming sacred.
- **TBD rationale can ship.** If a rationale item can't be resolved before v0.1 ships, name it explicitly as TBD rather than silently omitting or fabricating.
- **Shared references promote at the two-skill threshold.** Two skills loading the same reference for the same reason is enough to promote.
- **Apply the skill-prompting principles to every produced artifact.** Load the canonical reference at `../../_shared/references/skill-prompting-principles.md` rather than working from memory. The principles especially change how Phase 4 builds skills for writing, judgment, and human-consumption outputs.

## Cross-mode suggestions

After `from-prompt`:

- Run the produced skill on real input to verify craft preservation. Iterate via `refine` if tweaks surface.
- If Phase 3 surfaced fold-in candidates ("this should be a mode in `writing`"), run `extend` with the new mode design.
- If the conversion produced a category skill with multiple sources still to convert, batch them as a multi-source run and produce a consolidated decision-log entry.

## See also

- `SKILL.md` — parent dispatcher and gate logic
- Sibling sub-modes: `from-content`, `microtool-from-content`, `microtool-from-job`
- `../references/classification-taxonomy.md` — Phase 1 taxonomy
- `../references/rationale-extraction.md` — Phase 2 prompting patterns
- `../../_shared/references/scaffolding-patterns.md` — three-question scaffolding assessment
- `../../_shared/references/skill-prompting-principles.md` — the principles every produced skill follows
- `../../_shared/references/self-extending-skills.md` — additive-vs-complete heuristic and the three-beat self-extending pattern
- `../../_shared/references/example-rules.md` — example selection criteria
- `../../_shared/references/skill-vs-mode-vs-reference.md` — Phase 3 destination decision tree
- `../../_shared/references/naming-conventions.md` — naming rules
- `../../_shared/references/frontmatter-format.md` — Cowork-validator frontmatter rules
- `../templates/decision-log-entry.template` — Phase 6 entry template
- `../templates/SKILL.md.template`, `mode.md.template`, `reference.md.template` — file scaffolds
