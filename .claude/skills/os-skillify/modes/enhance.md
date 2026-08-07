---
name: enhance
description: >-
  Sub-mode of `os-skillify`. Audit, consolidate, idiom-modernize, and improve **already-existing** skills (their `SKILL.md`, modes, references, templates). Operates over live files — destructive — with explicit snapshot + per-change verification + user-confirmation gates. Six phases: Survey → Detect signals → Surface decisions → Apply changes → Verify → Log. Triggers on "audit my skill library," "review my existing skills," "consolidate these skills," "find redundancy across these skills," "modernize these Codex-era patterns," "add modes to the X skill," "split the X skill — it's doing two things." Do NOT trigger for converting a legacy prompt (use sibling `from-prompt`), for tweaking a single skill's behavior (use `os-tune/refine`), or for adding one mode to a single skill (use `os-tune/extend`).
---

# Sub-mode — Skillify enhance

Operates over **already-existing** skills. Where `from-prompt` and the content sub-modes generate new artifacts, `enhance` audits and improves what's already shipped — surfacing redundancy, missing structural elements (negative triggers, Design Rationale, examples), drift from current Personal OS idioms, and consolidation opportunities across siblings.

This mode is destructive: it modifies live files. The workflow is built around that fact — snapshot before changes, order changes by reversibility, verify per change, log lineage.

## When to use

- The user wants to audit one skill, a cluster, or the whole library.
- The user wants to consolidate siblings sharing vocabulary / references / job-shape into a category skill.
- The user wants to split a skill doing two distinct jobs.
- The user wants to modernize Codex-era patterns (custom heartbeats → `/loop`, sandboxed subagent restrictions dropped, hard-coded paths adapted, case-system mirroring removed).
- The user wants to fill in missing structural elements across a set of skills.

Don't trigger for single-skill tweaks (route to `os-tune/refine`) or adding one new mode to one skill (route to `os-tune/extend`). `enhance` is the cross-skill audit-and-improve surface.

## Preconditions

The two gates of the parent dispatcher apply (inheritance protocol + map-before-make), with the map-before-make check adapted: for `enhance`, the question isn't *does this overlap with an existing skill?* (everything is an existing skill); it's *does this consolidation/split decision affect skills outside the surveyed set?* If so, surface for explicit user confirmation before applying.

Writes follow `../../_shared/references/skill-update-protocol.md`. Plus the mode-specific concerns below — especially the snapshot-before-changes discipline and per-change verification, since `enhance` operates over live files and a bad consolidation cascades.

## Workflow

Run **Setup** first to establish scope. Then phases 1–6.

### Setup — scope + goals + snapshot

Before scanning anything, confirm with the user (use `AskUserQuestion` if not given upfront):

1. **Target skills** — absolute paths to the `SKILL.md` files under review. Can be one skill, a category-skill cluster, or an arbitrary related set.
2. **Workspace for WIP artifacts** — where audits, decision logs, and snapshots live during the run. Default: project-relative `experiments/enhance-<YYYY-MM-DD>-<short-slug>/`.
3. **Goals — what's being optimized for.** Multi-select via `AskUserQuestion`:
   - *Cohesion* — find redundancy across siblings; consolidate where the two-skill threshold has fired.
   - *Idiom alignment* — modernize legacy patterns (Codex-era heartbeats, sandbox-era subagent restrictions, hard-coded paths, case-system mirroring).
   - *Cluster split* — surface skills doing two distinct jobs that should split.
   - *Mode addition* — add new modes to an existing category skill.
   - *Structural completeness* — fill missing negative triggers, Design Rationale sections, examples, `source-prompts:` frontmatter.
   - *Specific user-named goal* — e.g., *"make the investigate cluster's mode-routing clearer."*
4. **Type lens** *(optional)* — `creative` / `technical` / `hybrid`. Shapes what "stronger" means during decisions. For creative skills, stronger = more voice-protective, more anti-collapse, more craft-disciplined. For technical, stronger = more precise, better edge-case coverage, sharper invariants. See `../references/type-lens.md`.
5. **Snapshot.** Take a snapshot of the target skills' current state into `<workspace>/snapshots/`. Use `os-autosave snapshot pre-enhance-<short-slug>` so the rollback path is plain-language revertable.

### Phase 1 — Survey

For each target skill, read `SKILL.md` + every mode + every reference + every template. Build a per-skill profile:

- *Job statement* (one sentence)
- *Inputs* (what does it expect?)
- *Run shape* (numbered steps? mode router? single workflow?)
- *References loaded* (full list of `references/*.md` paths, including `_shared/` references)
- *Templates* (full list)
- *Cross-skill references* (does it invoke other skills? which?)
- *Legacy artifacts* (paths to `~/.codex/...`? subagent restrictions? custom heartbeats? Codex script invocations? case-system mirroring?)

Write each profile to `<workspace>/audits/<skill-name>-profile.md`.

For multi-skill audits, produce `<workspace>/audits/_overlap-matrix.md` showing pairwise vocabulary / reference / job overlap.

### Phase 2 — Detect signals

Scan profiles + overlap matrix for the patterns documented in `../references/cluster-coherence-signals.md`. Bin findings by signal type:

- *Consolidation candidates* — shared vocabulary, shared references loaded from different paths, job-shape overlap. Two-skill threshold met → promote to shared.
- *Split candidates* — single skills doing two distinct jobs (different reference sets per mode, different output shapes, different invocation patterns).
- *Drift candidates* — Codex-era patterns with idiomatic Claude Code / Personal OS replacements:
  - Custom RRULE / heartbeat scheduling → delegate to `/loop`
  - Sandbox-era subagent restrictions → drop the restriction, keep the substantive guidance
  - Codex case-system mirroring (`lanes.json` / `hypotheses.jsonl`) → drop file-mirroring, keep concepts
  - Hard-coded `~/.codex/...` paths → portable equivalents or env-driven
  - Codex skill cross-references that don't exist in the current library → adapt or mark inert
- *Structural gaps* — skills missing:
  - Negative triggers in description
  - Design Rationale section
  - `source-prompts:` frontmatter for traceability
  - Examples (note: empty `examples/` is sometimes correct per `../../_shared/references/example-rules.md` — flag, don't auto-fill)
- *Promotion candidates* — references duplicated across skills that haven't been promoted to `_shared/` yet.

Write findings to `<workspace>/audits/_findings.md`.

### Phase 3 — Surface decisions

For each finding, decide the action — using the disposition vocabulary in `../references/disposition-vocabulary.md` (subset relevant to `enhance`: `CONSOLIDATE`, `SPLIT`, `ADAPT`, `AUGMENT`, `DEFER`, `NO-OP`).

**Always use `AskUserQuestion` for borderline calls.** Worth asking about:

- *Should this look-alike pair actually consolidate, or are they intentionally distinct?* (Same vocabulary used for different reasons is real — `NO-OP` with note is sometimes right.)
- *Should this meta-skill stay standalone or become a mode?*
- *Should the legacy idiom get full adaptation now, or stay as-is until the user actively encounters it?*
- *Should this skill split (it does two jobs) or stay bundled (the two jobs are tightly coupled)?*

For non-borderline applies (e.g., adding a missing negative trigger; promoting a reference duplicated across 3+ skills), apply directly with a decision-log entry.

### Phase 4 — Apply changes

**Order by reversibility.** Misfires get caught before they cascade.

1. *Promotion / consolidation* (creates new shared references; doesn't delete content yet) — apply first.
2. *Augmentation* (adds missing structural elements) — apply second.
3. *Adaptation* (replaces legacy patterns) — apply third with explicit per-change confirmation since these change behavior.
4. *Split* (creates new files, then removes content from existing) — apply last, with explicit per-skill confirmation.

For each destructive change, follow the skill-update-protocol's show-before-write discipline. Per-change verification (read the modified file end-to-end) catches regressions before they cascade. Record the change in the decision log immediately, not in a batched final pass.

If a change misfires (regression detected, craft lost, description garbled), revert from the snapshot via `os-autosave revert pre-enhance-<short-slug>`.

### Phase 5 — Verify

For each modified skill:

- *Craft preserved* — does the skill still do its original job? Walk through the modified Run section against the original.
- *Rationale holds* — does the Design Rationale still describe the essential moves, or did consolidation accidentally drop a rationale entry?
- *Cross-references resolve* — for skills loading shared references, do all paths still resolve?
- *No orphaned content* — did consolidation leave stale text behind (e.g., a mode body still mentioning a reference that got promoted away)?
- *Live-reload sanity* — skill still appears correctly in the available-skills list with negative triggers preserved.

For multi-skill runs, write `<workspace>/decision-log/_VERIFICATION-BATCH-<YYYY-MM-DD>.md` covering all modified skills.

### Phase 6 — Log

For each modified skill, write or update a decision-log entry at `<workspace>/decision-log/<skill-name>.md` per `../templates/decision-log-entry.template`. Record:

- *Date enhanced*
- *Goals* (from Setup)
- *Changes applied* per-change (what changed, why, lineage)
- *References promoted / created*
- *Adaptations applied* (idiom changes with rationale — also belong in the affected skill's Design Rationale)
- *Splits performed* (sources that became multiple destinations)
- *Deferrals* (findings flagged but not applied; reasoning + unblocking conditions)
- *Verification* (cross-reference to batch file or inline notes)

If the skill was previously created via `from-prompt`, append the enhancement record to its existing decision log rather than creating a new file. Lineage matters: the decision log shows the skill's full trajectory across sub-mode runs.

## Operating principles

- **Writes follow `_shared/references/skill-update-protocol.md`.** Plus the snapshot-before-changes discipline below.
- **Snapshot before changes.** Skills aren't always in a clean git state when an enhance run starts; the os-autosave snapshot is the rollback path.
- **Order changes by reversibility.** Promotion (least destructive) first; split (most destructive) last.
- **Per-change verification.** Batched verification at the end loses the ability to attribute regressions.
- **Always confirm borderline calls.** Consolidation decisions over live skills affect routing and behavior the user already depends on. Cost of asking is low; cost of mis-consolidating is high.
- **Document idiom adaptations explicitly** in Design Rationale of the affected skill (e.g., *"Cadence values were Codex-tuned defaults; adapted to `/loop` semantics on 2026-04-26"*). Future maintainers should read why a change happened, not just see that it did.
- **Lossless by default.** Findings tagged `NO-OP` still get a decision-log entry — so future audits don't re-surface the same look-alike pair without context.

## Status updates to the user

Surface at four checkpoints:

1. *End of Phase 2 detect* — findings list with proposed dispositions, before any changes.
2. *End of Phase 4 apply* — what changed, what was deferred.
3. *End of Phase 5 verify* — verification results.
4. *End of Phase 6 logs* — final summary, recommended next steps.

## Cross-mode interactions

- *`from-prompt` → `enhance`*: a conversion run produces sources marked `DEFER`; when their dependencies later become available, run `from-prompt` on the deferred sources, then `enhance` on the cluster to integrate them cleanly.
- *`enhance` → `from-prompt`*: an `enhance` run might surface a missing skill (*"the cluster needs a 'comms' standalone but it doesn't exist yet"*). Use `from-prompt` (with the existing-related-skills as a destination plan) to land the missing skill, then re-run `enhance` to consolidate.
- *`enhance` → `consolidate`*: when two of the surveyed skills genuinely warrant a merge into one but the merge is complex enough to want two-lane drafting first, hand off to `dual-lane` from inside `enhance`.

## See also

- `SKILL.md` — parent dispatcher and gate logic
- Sibling sub-modes: `from-prompt`, `from-content`, `microtool-from-content`, `microtool-from-job`, `dual-lane`, `consolidate`, `interview`
- `../references/cluster-coherence-signals.md` — Phase 2 signal patterns
- `../references/disposition-vocabulary.md` — Phase 3 decision labels
- `../references/prompt-based-vs-tool-wrapper.md` — Phase 1 skill-type assessment, Phase 3 deferral revisiting
- `../references/type-lens.md` — how the type parameter shapes what "stronger" means
- `../../_shared/references/skill-update-protocol.md` — write discipline this mode operates under
- `../../_shared/references/example-rules.md` — assessment for empty `examples/` directories during Phase 2
- `../../_shared/references/scaffolding-patterns.md` — three-question assessment when surveying suspected scaffolding
- `../templates/decision-log-entry.template` — Phase 6 entry template

## Source provenance

Distilled from cross-library audit work the user has been doing manually before this mode existed (the v0.1 bug-investigation pilot was the catalyst — 14 sources, multiple consolidations and splits, all run by hand). The workflow shape, disposition vocabulary, and cluster-coherence signals are encoded here so future audit passes run faster than the pilot did.
