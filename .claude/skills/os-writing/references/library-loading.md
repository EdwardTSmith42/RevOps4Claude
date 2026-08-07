# Library Loading (writing-side)

How writing modes load references from `os-inputs/` per the library matching convention. This is the consumer-side companion to library's `os-library/references/matching-discipline.md`. Where the matching-discipline reference defines the contract, this reference applies it specifically to writing jobs.

## What writing loads

Every writing job typically loads up to four reference types:

A **voiceprint** for voice fidelity. Writing writes within the voice this voiceprint captures. By default, the user's scope-specific voiceprint matching the requested output format (a customer-email voiceprint for an email mode invocation, a longform voiceprint for an article). Falls back to the user's general default voiceprint if no scope-specific match exists. Falls back to the graceful-degradation flow if no user voiceprint exists at all. Voiceprint loading is foundational — a draft without voice fidelity is a draft that reads as AI-produced.

**Style samples** as few-shot exemplars. Optional but high-leverage when the job has a specific pattern (an action scene, dialogue rhythm, pain-triplet structure, hook formula). The mode loads samples matching the relevant author and pattern. Multiple samples can load together when the piece spans multiple patterns. Style samples teach the *how* concretely. The voiceprint teaches the *what* and *why* abstractly. They complement.

A **template** as a structural guide. Optional. When a proven template exists for the requested format (`landing-page-long-form.md`, `welcome-email-7-day.md`), it shapes the output structure. Templates inform shape, not content. The mode follows the section-by-section job each section does, producing fresh content that fits the structure.

A **brief** for project context. Either supplied inline by the user or loaded from `os-inputs/briefs/current/` when the user names the project. The brief carries audience profile, goal, constraints, source material pointers, and notes on which references the user already curated for this project. Briefs are usually project-scoped, not piece-scoped — one brief covers many drafted pieces in the same project.

## How the loading sequence runs

The matching-discipline doc defines the soft-search procedure abstractly. Writing applies it in a specific sequence per job.

**Step 1: Parse the job context.** What's being produced (output format)? Who's the target voice (the user, a pen name, an external author, or unspecified)? What genre or register signals appear in the request? Which references did the user explicitly name?

**Step 2: Resolve explicit references first.** If the user named specific references — a particular author's voiceprint, a specific template, a saved brief — load those directly. No matching needed for explicit names.

**Step 3: Find the brief.** If the user named a project, exact-match against `os-inputs/briefs/current/` and load. If the user didn't name a project but is producing something a brief might cover, list active briefs matching the requested target format. **Per the matching-discipline contract, never silently choose among active briefs** — even when exactly one matches, surface the candidate to the user and confirm before loading. The surface names the matched brief and asks whether to use it for this run, since a silent auto-load against the wrong brief is a worse failure mode than the round-trip of confirming. If multiple match, ask which to use. If none match, ask whether to write a quick brief inline before producing.

**Step 4: Find the voiceprint.** Apply the implied-author rule from the matching discipline — when no author is named, use `name` from `os-inputs/_os-user-profile.md`. Score voiceprints using the three-layer model. Top match becomes the loaded voiceprint. If confidence is low or candidates are close, ask the user to confirm before proceeding.

**Step 5: Find style samples.** Score against author and pattern. Style samples are optional, so finding none is acceptable — the mode produces the piece without few-shot exemplars and notes their absence. When samples do exist for the relevant author and pattern, load up to 2-3 (more becomes overwhelming as few-shot context).

**Step 6: Find a template.** Score against format and `proven`. Templates are optional. When a `proven: yes` template exists, prefer it. When a `proven: with-context` template matches, load it but flag the context-fit (the brief's situation may or may not align with the template's success-context).

**Step 7: Note what was loaded.** Before producing, the mode briefly names the references in play — voiceprint slug, brief slug, any style samples and templates that matched, and explicit notes for any that didn't (no style samples found, no proven template for this format, will produce structurally per genre convention). The note is the audit trail; it doesn't recite a fixed format.

## When a reference type is missing

The matching discipline names three options when no clean match exists for a needed reference type: proceed without, supply sample text for on-the-fly creation, point at a related reference as substitute. Writing applies them per type.

For **missing voiceprint**: don't proceed without. Writing always asks here — voice-generic prose is the failure mode the mode is built to prevent. The on-the-fly creation chain runs into `os-voiceprint/from-sample` with sample text the user supplies. After production, the mode asks whether to save the temporary voiceprint via `os-library/save` for future use.

For **missing style samples**: proceed without is fine. Style samples are nice-to-have, not essential. The mode produces the piece without few-shot exemplars and notes the absence. The user can curate samples later if outputs feel underdeveloped on a specific pattern.

For **missing template**: proceed without is fine. Writing can produce structurally-sound prose without a saved template by following genre conventions documented in `references/<format>-anatomy.md`. The mode notes the absence. The user can extract a template from a successful piece later if outputs would benefit from a reusable shape.

For **missing brief**: ask the user to supply one inline. A writing job without a brief is producing without a contract — high risk of producing the wrong piece.

## Loading order matters for context

When multiple references load, the mode reads them in a specific order so the context window isn't crowded by lower-priority material:

1. **Brief first** — sets the contract for what's being made
2. **Voiceprint second** — establishes the voice the rest of the production must honor
3. **Templates third** — shapes the structural approach
4. **Style samples fourth** — provide concrete few-shot patterns where applicable
5. **Source material last** — the substantive content the piece draws from

If context is tight (a long manuscript section being drafted, multiple reference loads competing), the mode prioritizes brief and voiceprint above all else. Style samples and templates can be cited rather than fully loaded if they would otherwise crowd out the source material.

## Citing references in output

After producing, the mode names the references in play so the user has visibility. The shape:

```
**References loaded:**
- Voiceprint: <slug used>
- Brief: <brief slug, if loaded>
- Style samples: <author>/<pattern> (with a note on which section it informed, if relevant)
- Template: <name, or "none — followed genre convention from <anatomy-reference>">

**Source material consumed:**
- <where the substantive content came from — inline supply, saved file, link from the brief>

[The drafted piece follows]
```

The block names what shaped the work; it doesn't recite a fixed template. Fields that don't apply are omitted rather than left empty. This makes iteration easier — the user knows what informed the work and can adjust references before re-running.

## When the user overrides

Sometimes the user wants a non-default reference loaded — writing in another author's voice for a specific piece, using a long-form template even when the piece would normally be short, loading a brief from another project for cross-pollination. The user knows what they're doing; the mode honors the override and notes the substitution in the references-loaded section so the user can spot if the override produced unintended results.
