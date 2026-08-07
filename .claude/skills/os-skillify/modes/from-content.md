---
name: from-content
description: Sub-mode of `skillify`. Designs a full Cowork-native skill that operationalizes a body of knowledge supplied as content (article, transcript, book chapter, lecture notes, video summary). Produces SKILL.md plus 1-N modes plus references following os-tune's pack conventions. Mode count flows from what the content actually contains — single-mode if the content captures one tight job, multi-mode if it covers a domain with multiple jobs. Mirrors source frameworks, terminology, and step-counts. Lifts verbatim phrases that add fidelity. Triggers on "build me a skill from this transcript," "design a skill that operationalizes this article," "make this content into a skill," "create an assistant that helps me apply this knowledge." Do NOT trigger when the user wants a focused single-purpose tool (use sibling `microtool-from-content`), when converting an existing prompt (use sibling `from-prompt`), or when the input is a need rather than content (use sibling `microtool-from-job`).
---

# Mode — Skill from content

Design a full Cowork-native skill from a body of knowledge supplied as content. The output is a complete skill structure (SKILL.md plus 1-N mode files plus 0-N reference files) following skillify conventions. Mode count flows from what the content actually contains.

## When to use

The user has substantial content (article, transcript, book chapter, lecture notes, video summary) and wants a Cowork-native skill that operationalizes the knowledge for downstream use — by themselves, their team, or anyone else who installs the skill.

If the user wants a focused single-purpose tool from the same content (rather than a multi-mode skill), route to sibling `microtool-from-content`. If the user has a working prompt to convert, route to sibling `from-prompt`. If the user has no content but does have a job-to-be-done, route to sibling `microtool-from-job`.

## Preconditions

Two gates apply before this sub-mode runs, per the parent `skillify` dispatcher:

1. **Inheritance protocol** — loads Personal OS context (identity, voiceprint, org rules, conventions, skills inventory, brief, inbox, setup philosophy, system tracker, capture decision tree) per `../../os-tune/references/inheritance-protocol.md`. The produced skill inherits voice and convention compliance.
2. **Map-before-make check** — runs the routing logic per `../../os-tune/references/figure-it-out-routing.md` to surface whether the request is actually a candidate for `extend` or `refine` against an existing skill. The user can override and force generation.

Before writing any produced files, also load `../../_shared/references/skill-prompting-principles.md` and apply its principles to every artifact. For content-derived skills this matters acutely: the source content is usually prose for human consumption, so the produced skill should be written that way too, and shouldn't get flattened into bullets and verbatim sample phrasings during conversion.

Also load `../../_shared/references/self-extending-skills.md` and assess whether the skill being built is additive or complete. Content-derived skills lean additive more often than not — long-form content typically encodes a domain where the user's needs keep producing new shapes — but the heuristic still applies per skill. When additive, the produced skill carries the three-beat self-extending section; when complete, omit it.

See `SKILL.md` for the gate logic and how the dispatcher routes among sibling sub-modes.

## Inputs

- **Required:** Content to operationalize. Could be a transcript, article, book chapter, podcast episode, lecture notes, video summary, or any long-form material that captures a body of knowledge. Length typically 1000-50000 words.
- **Optional:** Stated audience for the skill — *"this is for me"*, *"for my coaching clients"*, *"for public release in the skill pack."* Calibrates the skill's tone and assumed context.
- **Optional:** Stated scope — *"keep it tight, just the core moves"* vs. *"comprehensive, every angle the content covers."*
- **Optional:** Examples of related skills already in the pack the user wants the new skill to compose with or borrow from.
- **Optional:** Voiceprint via `os-library/find` if the source content is in the user's voice and the skill should preserve that.

## Run — six-phase procedure

The mode runs through a procedure adapted from skillify's 6-phase workflow (classify → surface rationale → plan destination → build → verify → log), calibrated for content-as-input rather than prompt-as-input. The mode adds an explicit read phase at the start because content input requires a digest step that prompt input doesn't.

### Phase 1 — Read the content

Read the supplied content fully. Identify:

- **Named frameworks.** Specific frameworks the content introduces or relies on (e.g., "the 3-pillar framework," "the Hormozi value equation," "the 5-day learning architecture").
- **Terminology.** Specific words the source uses repeatedly that carry weight — signature language, neologisms, branded terms.
- **Step-counts.** Where the content uses a numbered structure (3 pillars, 9 accelerators, 5 days, 7 sections), capture the count exactly.
- **Verbatim phrases.** Uniquely memorable lines or paragraphs that drive home concepts and would lose force if paraphrased.
- **Promised outcomes.** What the content claims its readers will be able to do after applying it.
- **Worked examples.** Specific cases the content walks through that demonstrate the moves in action.

Surface this analysis briefly to the user before designing — it confirms the mode read the content correctly and lets the user catch missed signals.

### Phase 2 — Classify

Based on the content, decide:

**Single-mode skill or multi-mode skill?**

- **Single-mode** when the content captures one tight job with a clear input → output transformation (e.g., "given a lecture transcript, produce notes in the Cornell format").
- **Multi-mode** when the content covers a domain with multiple distinct jobs (e.g., a book chapter on copywriting that covers headlines, body copy, and CTAs as three separable jobs).

**If multi-mode, what's the mode list?** Each mode should be a distinct job with its own input → output. Mode names short and descriptive. Typical multi-mode skills land at 3-5 modes — ranges outside that should have specific reasons.

**Does the skill warrant references?** References are appropriate when:
- A craft pattern is shared across multiple modes
- A canonical structure is referenced by multiple modes
- A framework needs depth that would bloat individual mode files
Otherwise, fold the relevant material into mode files directly.

**What's the skill's place in the pack?** Does it belong as a standalone, or could its content be a mode added to an existing category skill (drafting, content-discovery, etc.)? When in doubt, prefer adding a mode to an existing skill rather than proliferating skills. Surface the recommendation to the user.

Surface the classification (single vs. multi, mode list, references list, standalone vs. fold-in) to the user for approval before drafting.

### Phase 3 — Design

For each mode the user approves, design:

- **Frontmatter.** Name + description with explicit triggers and negative triggers ("Do NOT trigger for...").
- **When to use.** Common triggers and where to route instead.
- **Inputs.** Required and optional, with scoping notes.
- **Run procedure.** The mode's actual workflow — phases, decision points, craft moves. Lift verbatim phrasing from source content where it sharpens.
- **Constraints.** Hard rules and soft preferences. Mirror source step-counts and source framework structure.
- **Output shape.** What the mode produces and in what format.
- **Cross-mode suggestions.** Where the user typically goes after this mode runs.
- **Source provenance.** What craft preserves from source content, what's new design.

For each reference, design the canonical content that supports the modes that consume it.

### Phase 4 — Build

Writes follow `../../_shared/references/skill-update-protocol.md` — show all proposed files as a batch, confirm, write, sanity-check each. Wrap the writes in auto-save: invoke `os-autosave snapshot` with a name like `pre-skillify-<skill-name>` before persisting, then `os-autosave commit` with message `os-tune skillify: <skill-name> — created from content` after a successful sanity check. If sanity check fails, revert to the snapshot.

Plus skillify conventions:

- No semicolons in body prose (em dashes, periods, or commas instead)
- Restrained bullet use — bullets for genuinely listy material, prose for connective tissue and reasoning
- Frontmatter compliant on every SKILL.md and mode file
- Cross-references that resolve (every path mentioned in a file exists on disk)
- Library integration where appropriate (matching-discipline reference, voiceprint loading patterns)

Each mode file should mirror the source's framework structure where applicable. If the source uses "3 pillars," the mode references 3 pillars. If the source uses "9 accelerators," 9 accelerators.

### Phase 5 — Verify

Surface the produced skill to the user. The user reviews the SKILL.md, the mode files, and the references. Common adjustments:

- Mode boundaries (split / merge / rename modes)
- Constraint tightening or loosening
- Output format adjustments
- Source-craft preservation (lift more verbatim phrases or paraphrase more)
- Cross-skill integration (which existing pack skills the new skill composes with)

Iterate until the skill feels right.

### Phase 6 — Log

Produce a per-source decision log entry at `<workspace>/decision-log/<Source Name>.md` documenting:

- What was built and where
- Why the mode shape (single vs. multi) was chosen
- What craft preserves from source
- What's new design
- Open questions for v0.2 / real-use follow-up

If the skill is multi-mode, also produce or update a category-skill log entry.

## Output

A complete skill at `/skills/<name>/` with:

```
<skill-name>/
├── SKILL.md
├── modes/
│   ├── <mode-1>.md
│   ├── <mode-2>.md
│   └── ...
└── references/  (optional)
    ├── <ref-1>.md
    └── ...
```

Plus the per-source decision log entry.

## Craft preservation from content

The mode applies the patterns documented in `../references/craft-preservation-from-content.md`. The key moves:

- **Mirror frameworks.** If the source has named frameworks, the skill references them by name and uses their structure.
- **Lift verbatim phrases.** Uniquely memorable lines transfer verbatim into mode files (typically into examples, into success-quality descriptions, or into output templates).
- **Mirror step-counts.** Exact count preservation. No rounding for symmetry.
- **Stay inside the source.** Don't add frameworks or moves the source doesn't have. Inference about what's implied is fine — invention is not.
- **Capture terminology.** Source-specific words that carry weight survive into the produced skill's vocabulary.

## Constraints

**Single-mode minimum, no fewer.** Even thin content produces at least one mode. If the content is so thin no mode emerges, route to `microtool-from-content` or `microtool-from-job` instead.

**Mode count tracks content actually present.** Don't pad to hit a target mode count. If the content captures 2 distinct jobs, the skill has 2 modes.

**Verify before logging.** Always run the verify phase with the user before producing the decision log entry. Logged work that the user later wants to revise creates documentation drift.

**Library integration is opt-in.** Add library integration patterns where they help (voice-fidelity-sensitive skills should load voiceprints — project-scoped skills should load briefs). Don't bolt library integration onto every mode reflexively.

**v0.4 conventions throughout.** No semicolons. Restrained bullets. Frontmatter compliant. Paths resolve. Negative triggers in descriptions.

## Cross-mode suggestions

After `from-content`, useful follow-ups:

- Run the new skill on a real input to battletest it. Iterate based on signal.
- If the skill's classification surfaced fold-in candidates ("this should be a mode in `writing`"), use `extend` to add a mode to the existing skill instead.
- If you produced a skill but realize you also need adjacent micro-tools, run sibling `microtool-from-content` or `microtool-from-job` for those.

