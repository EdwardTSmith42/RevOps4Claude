# Shared References

Reference documents that are loaded by more than one skill. When a reference is only used by a single skill, it lives inside that skill's own `references/` folder. When a reference is genuinely cross-cutting — multiple skills consult the same knowledge for the same reason — it moves here.

## When to promote a reference to `_shared/`

Promote when both conditions are true:

1. Two or more skills load (or should load) the same reference document.
2. They load it for the same reason — the reference is serving the same purpose in each context, not just incidentally touching similar content.

Example promotion triggers:
- The `voiceprint-definition.md` reference lives inside the `os-voiceprint/` skill today. If the `os-editing/` skill adds a voice-matching mode that also loads it, promote.
- The copy-editing checklist that ends up inside `os-editing/references/` might be loaded by a `content-review/` skill later — promote when that happens.

## When to leave a reference inside a skill

Leave it where it is when only one skill loads it, or when two skills load similar content but for different purposes. Premature promotion creates coupling without benefit.

## Naming

Same rules as per-skill references (see `naming-conventions.md`):
- lowercase, hyphen-separated
- noun-phrase
- `.md` extension

## Updating cross-references

When a reference moves here from a skill folder, update the loading skill(s) to point to the new path. The skill's `references/` section in SKILL.md should list the shared reference explicitly so the dependency is visible.

## Current contents

- `content-format-taxonomy.md` — the content-format lens for short-form delivery modes; its own malleability note treats the *kind* of cut as canonical and the exact count as adaptable, so read the file for the current set. Loaded by content-mining (idea + atomize rungs) and gold. Promoted 2026-04-23 during the conversion of the former content-repurposing skill (merged into content-mining 2026-08-01).
- `creative-criteria.md` — the quality filter for ideas that travel; the criteria capture the main pathways (novelty, wonder, clarity, connection, utility) and the file treats the exact set as adaptable, so read it for the current list. Loaded by content-mining (idea + atomize rungs) and gold. Promoted 2026-04-23 during the conversion of the former content-repurposing skill (merged into content-mining 2026-08-01).
- `schwartz-awareness-ladder.md` — Schwartz's five stages of audience awareness (Unaware, Problem Aware, Solution Aware, Product Aware, Most Aware) with messaging implications. Loaded by audience and biz-strategy. Promoted during the 2026-04-24 consolidation pass.
- `hormozi-value-equation.md` — Hormozi's four-lever value equation (Dream Outcome × Perceived Likelihood / Time Delay × Effort & Sacrifice). Loaded by audience (modes/dmo, modes/core-transformation) and offer (modes/offer-brainstorm, modes/offer-vehicle, modes/offer-improve). Promoted during the offer build (2026-04-24).
- `positioning-concepts.md` — USP, NTPV (Niche/Transformation/Promise/Vehicle), Unlike Statement, Elevator Pitch structure, Value Articulation Story 7-beat format, Zone of Genius vs. Competence, silent observation protocol. Loaded by biz-strategy (modes/positioning) and offer (modes/offer-vehicle, modes/unique-mechanism, templates/problem-promise-paragraph). Promoted during the offer build (2026-04-24).
- `skill-prompting-principles.md` — the canonical principles for writing skills that frontier models follow well. The list grows as new failure modes get named, so consumers point at it rather than restating it. Loaded by os-skillify (SKILL.md, all four sub-modes, all three templates) and os-tune (refine, extend, and listed in inheritance-protocol). Promoted at creation on 2026-05-24 because the protocol applies to every skill-authoring or skill-editing operation in the workspace.
- `self-extending-skills.md` — the additive-vs-complete heuristic and the three-beat self-extending pattern (surface the gap, offer two paths, hand off cleanly). Loaded by os-skillify (SKILL.md, all four sub-modes, SKILL.md.template), os-tune (refine, extend, reflect, inheritance-protocol), the audit-lens, and additive skills that point at the principle (os-writing and likely more os-* during their audit). Promoted at creation on 2026-05-24 during the os-writing audit because additive skills across the workspace need the disposition, and meta-skills need to bake it in when building new ones.
- `what-is-a-golden-nugget.md` — definition, four-test quality bar (stand-alone, specific, transferable, non-obvious), and failure modes for the kind of high-value insight Personal OS extracts from source content. Loaded by os-gold (all three modes) and os-content-mining (Step 2 quality filter). Promoted during the os-* audit (2026-05-24) when the two-skill threshold was met. Cross-referenced from `creative-criteria.md`.

Each shared reference carries a malleability note clarifying what can vary per skill and what is canonical. **Read that note before restating a reference's contents anywhere.** Where it pins a list — external canon like Schwartz's stages or Hormozi's levers, or a set this workspace has marked canonical — naming the members inline is fine and carries real meaning. Where it treats the set as adaptable, point at the file instead: an enumeration reads as complete and goes stale silently the moment the reference grows.
