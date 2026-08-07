---
name: os-library
version: 0.1.0
description: >-
  Manage the user's reference inputs — voiceprints, style samples, templates,
  and briefs that downstream skills (os-writing, the fiction-oriented editing modes, os-voiceprint,
  others) load when they produce work. Five user-facing modes (list, find,
  save, repair, validate) plus a documented matching convention other skills
  follow internally. Triggers when the user wants to see what reference
  material they have ("what voiceprints do I have," "show me my templates"),
  find the best match for a job context, save a new input artifact with proper
  frontmatter, repair a file with broken frontmatter, or validate the whole
  inputs collection. Do NOT trigger for producing voiceprints from source
  material (use `os-voiceprint`), drafting new content (use `os-writing`), or
  skill conversion (use `os-skillify`).
display_name: Library
tagline: 'Voiceprints, samples, templates, briefs — matched at the right moment.'
category: Planning
packs:
  - personal-os
icon: 'phosphor:Books'
when_to_use: >-
  Library is what makes downstream skills *find the right reference
  automatically*. Drafting needs a voiceprint? Library matches one. Editing
  needs a style sample? Library finds it. You don't have to remember what you
  have or where it lives.


  Reach for this directly when you want to see what reference material you've
  built up, find the best match for a job, save a new input artifact, repair
  broken frontmatter, or validate the whole inputs collection.
modes:
  - name: list
    job: Show what reference material you have.
  - name: find
    job: Match the best reference for a given job context.
  - name: save
    job: Save a new input artifact with proper frontmatter.
  - name: repair
    job: Fix a file with broken frontmatter.
  - name: validate
    job: Validate the entire inputs collection.
---

# Library — reference input management

## Purpose

The library skill is shared infrastructure for the user's reference inputs. It defines the filesystem convention and the matching discipline that downstream skills (`os-writing`, fiction-oriented writing modes (in `os-editing`), `os-voiceprint`, others) follow when they produce work. The user invokes library directly to inspect, find, save, repair, or validate inputs. Other skills follow the matching convention from inside their own modes when they need to load references for a job.

The four input types the library manages:

- **Voiceprints** — portable artifacts capturing a writer's voice, scoped by domain or format (general, social-media, customer-email, longform, fiction-noir, etc.)
- **Style samples** — curated passages (200-500 words) demonstrating specific writing patterns the user wants emulated (action scenes, dialogue, rhythmic patterns, hook openers, etc.)
- **Templates** — proven structural shapes for specific output formats (landing pages, welcome sequences, hook formulas, etc.)
- **Briefs** — project-level context for ongoing work, with current and archive subdirectories so accumulated briefs don't crowd the active set

The library does not produce these artifacts. Producers live in other skills — `os-voiceprint` produces voiceprints, future writing modes may extract templates from sample work, the user curates style samples manually. The library stores, finds, repairs, and validates them.

## When to use

Direct user invocations include asking what voiceprints, templates, or style samples are on file, finding the best reference match for a stated job ("what voiceprint should I use for a customer email?"), saving a new artifact with proper frontmatter after an external skill produces it, repairing a file whose frontmatter is incomplete or malformed, and validating the inputs collection periodically to surface drift before it accumulates.

Indirect use happens when other skills follow the matching convention from inside their own runs. A writing mode that needs a voiceprint reads `references/matching-discipline.md`, scans `os-inputs/voiceprints/` with soft search, and ranks candidates by the same logic the library skill uses. The library is the source of truth for that logic.

## First-time setup

The library expects a one-time profile file at `os-inputs/_os-user-profile.md` with the user's name (used as the implied author when matching voiceprints without an explicit author signal). If the file is missing, `os-library/find` and any consumer skill following matching-discipline will fall back to less reliable inference. Create the file once with the user's name; the file is auto-loaded thereafter and the setup step does not need to repeat. Most subdirectories under `os-inputs/` autocreate on first save. The first-time-setup instruction here can be deleted from the buyer's local skill copy once the profile is in place.

## Modes

| Mode | Job | Output shape |
|---|---|---|
| `list` | Show available inputs filtered by type and optional tags | A scannable list grouped by type, with key frontmatter fields per entry |
| `find` | Soft fuzzy match for a job context, return ranked candidates plus repair flags | A small ranked list (top 1-3 per type) with confidence and any frontmatter issues |
| `save` | Write a new input with proper frontmatter, validate the schema | Confirmation of the saved file path and any schema warnings |
| `repair` | Fix incomplete or malformed frontmatter on a specific file, with user confirmation | The repaired file plus a diff of what changed |
| `validate` | Sweep all inputs and produce a repair worklist | A grouped list of files needing attention, ordered by severity |

### Self-determining when not specified

If the user names a mode, run it. Otherwise infer from the verb in the request. Inspection requests ("what do I have?" / "show me my templates") route to `list`. Match-for-job requests ("what should I use for X?" / "find me a voiceprint that fits Y") route to `find`. Persist-this requests ("save this voiceprint" / "add a new template") route to `save`. Targeted-fix requests ("fix the frontmatter on file Z") route to `repair`. Sweep requests ("check my inputs" / "what needs cleanup") route to `validate`.

When a downstream skill (`os-writing`, fiction-oriented writing modes (in `os-editing`), `os-voiceprint`) needs a reference and `find` returns no clean match, the calling skill follows the graceful-degradation convention documented in `references/matching-discipline.md` rather than failing.

## Inputs directory layout

The user's reference material lives at the workspace root, not inside the skill pack:

```
os-inputs/
├── _os-inputs-conventions.md   # overview pointing at this skill
├── _os-user-profile.md         # name + user-level config (one-time setup)
├── voiceprints/
│   ├── README.md
│   └── <author>-<scope>.md
├── style-samples/
│   ├── README.md
│   └── <author>/<pattern>.md
├── templates/
│   ├── README.md
│   └── <format>-<descriptor>.md
└── briefs/
    ├── README.md
    ├── current/
    └── archive/
```

Each subdirectory carries a README.md explaining its type's schema with worked examples. The `_os-user-profile.md` file is set up once at first use and holds the user's name (used as the default author when matching voiceprints).

The four type schemas are documented in:
- `references/voiceprint-schema.md`
- `references/style-sample-schema.md`
- `references/template-schema.md`
- `references/brief-schema.md`

Plus `references/matching-discipline.md` covers the soft-search convention, scoring rules, graceful degradation, and on-the-fly creation chains. Other skills load this reference when they need to find inputs from inside their own modes.

## Operating principles

The library follows three principles that prevent it from getting in the user's way.

**Bookkeeping never blocks the work.** A user who wants to find a voiceprint shouldn't have to clean up frontmatter first. `find` works on whatever's available, surfaces issues as flags rather than failures, and offers `repair` as a follow-up. Validation is a separate, voluntary sweep.

**Soft search, not strict matching.** `find` uses fuzzy tag-and-keyword scoring with sensible fallbacks. A query for "Mat's voice" matches `mat-mulholland` (substring), `mat-customer-email` (prefix), and any voiceprint where notes mention "Mat" (content fallback). Strict equality matching is the wrong default at curation scale — users misremember exact filenames, and the library should be forgiving.

**Convention over enforcement.** The four type schemas are the canonical shape, but malformed files don't get rejected. They show up in `find` results with a "frontmatter incomplete" flag. The repair flow proposes corrections, and the user confirms. The schema enforces itself through use, not gatekeeping.

## Cross-skill API

When other skills (`os-writing`, fiction-oriented writing modes (in `os-editing`), `os-voiceprint`, etc.) need to load references from `os-inputs/`, they follow the convention from `references/matching-discipline.md` rather than calling library modes directly. The pattern looks like this:

1. Read `os-library/references/matching-discipline.md` to understand the scoring rules and graceful degradation patterns
2. Read `os-library/references/<type>-schema.md` for the relevant input type to know which fields to score against
3. Scan `os-inputs/<type>/` for matching candidates, applying the soft-search logic
4. If no clean match is found, surface the situation to the user with the three explicit options (proceed without, supply sample for on-the-fly creation, point at related reference)
5. If on-the-fly creation is chosen, chain into the relevant producer (typically `os-voiceprint` for voiceprints) and then call `os-library/save` to persist if the user wants to keep it

The library skill itself isn't invoked from inside other skills' runs. It's the documentation and convention layer. The producer skills (`os-voiceprint`, writing modes) implement the discovery and matching inline, following the convention.

## Self-extending behavior

The set of reference types the user accumulates keeps growing as their craft surface area grows. The library starts with four types (voiceprints, style samples, templates, briefs); the user may surface a need for new shapes over time (e.g., a "scene-beat exemplar" type for fiction that doesn't fit style-sample, or a "campaign-postmortem" type that doesn't fit brief). When a save or find surfaces a clear shape that isn't well-served by any of the four types, do three things: name the gap explicitly, offer two paths (shoehorn it into the closest existing type with notes, or extend the library with a new type), and on the second path hand off to `os-tune`'s `extend` to add a new schema reference and route handling. Don't silently invent new types — the library's value is in the convention being shared across consumer skills, and new types need to land in the convention deliberately.

## Design rationale

The library exists as its own skill rather than as documentation under skillify or as a pure convention because user invocability matters. The user wants to ask "what do I have" and "find me the right reference," which is naturally a skill surface. Documentation-only conventions don't have invocation modes. Skillify is about converting prompts into skills, a different job entirely.

Five modes rather than fewer because the operations don't compose well. List and find have different output shapes. Save and repair have different write semantics. Validate sweeps the corpus rather than acting on a single file. Each mode does one thing well.

Soft search rather than strict matching because users misremember filenames and accumulate inputs faster than they curate frontmatter. Strict matching would block work behind bookkeeping. The repair flow exists because the right answer to drift is to surface it and offer a fix, not to enforce on every read.

Per-type schemas rather than one bloated schema because fiction and business inputs share almost no fields beyond `type` and `notes`. Empty fields are cognitive overhead. Tight schemas keep each input file focused on what its type actually needs.

The user-profile file rather than implicit user identity because the user's name is the default for matching voiceprints, and silent assumptions about identity would produce confusing fallback behavior. One small file at first use establishes the convention transparently.

## Related skills

- `os-voiceprint` — produces voiceprint artifacts. `os-library/save` persists them with proper frontmatter. `os-library/find` ranks them when other skills need a voice reference.
- `os-writing` — the largest consumer of `os-library/find`. Writing modes load voiceprints, style samples, and templates per job context.
- fiction-oriented writing modes (in `os-editing`) — uses style samples and voiceprints calibrated to specific authors and pen names.
- `os-skillify` — for skill creation, prompt conversion, and adding new library reference types when the four starter types aren't enough. Library doesn't invoke `os-skillify` during normal runs; the self-extending hand-off above is the exception.
