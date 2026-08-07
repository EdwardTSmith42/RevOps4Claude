---
name: os-library/save
description: Write a new input file (voiceprint, style sample, template, or brief) to the right os-inputs/ subdirectory with proper frontmatter. Validates the schema and warns about issues without blocking the save. Triggers on "save this voiceprint," "add a new template," "create a brief for X," and on chains from other skills (voiceprint produces a voiceprint, then save persists it). Do NOT trigger when the user wants to find existing inputs (use `find`), inspect the collection (use `list`), or fix a file with broken frontmatter (use `repair`).
---

# Mode — Save

Write a new input artifact to `os-inputs/` with proper frontmatter. Used directly by the user when adding a new template or brief, and chained from other skills (`os-voiceprint`, writing modes) when they produce an artifact the user wants to keep.

Save validates the schema before writing — required fields present, enum values within the starter list (or freeform values flagged for review). Validation issues produce warnings, not failures. The save still happens. The user sees the warnings and can repair later.

## When to use

Typical user invocations save a voiceprint as the default for a scope, add a new template the user wants to keep, or create a brief for a named project.

Chained invocations: `os-voiceprint` produces a portrait, then `os-library/save` persists it. A writing mode extracts a template from a successful piece, then `os-library/save` stores it with `proven: with-context` until use validates it.

## Inputs

- The artifact content (the body of the file — voiceprint portrait, style sample passage, template structure, or brief notes)
- The frontmatter values (type, plus type-specific required fields)
- Optional: a suggested filename (the mode generates one if not supplied)

## Run

The procedure runs through five steps.

**Step 1: Determine the type and target subdirectory.** From the supplied frontmatter, identify the type. Set the target path: voiceprints land in `os-inputs/voiceprints/<filename>.md`, style samples land in `os-inputs/style-samples/<author>/<pattern>.md`, templates land in `os-inputs/templates/<filename>.md`, briefs land in `os-inputs/briefs/current/<filename>.md` by default. Produced work — anything a skill made rather than material it will later consume — lands in `os-outputs/<filename>.md`; the distinction is whether a future run reads it back as input.

For briefs specifically, the target subdirectory is determined by the `status` field. Briefs with `status: active` or `status: done` land in `current/`. Briefs with `status: archived` land in `archive/` — this handles the case where the user is back-filling notes for finished work (a campaign that already shipped, a book that was released months ago) and wants the brief filed in the archive directly rather than created in current and moved manually. Subsequent moves between current and archive remain manual. Status is the routing signal at save time only.

**Step 2: Validate the frontmatter.** Check required fields per type (see the schema references). Check enum values where applicable — `default: yes | no`, `proven: yes | no | with-context`, `status: active | done | archived`. Freeform values (a new scope, a new pattern) are accepted but flagged in the warning summary. Missing optional fields are noted but not flagged.

**Step 3: Generate the filename if not supplied.** Use a deterministic naming pattern per type. Voiceprints: `<author>-<scope>.md` (or `<author>.md` if scope is general and default is yes). Style samples: `<pattern>.md` inside the `<author>/` folder. Templates: `<format>-<descriptor>.md` (the descriptor disambiguates among multiple templates for the same format). Briefs: `<project>.md`. If the generated filename collides with an existing file, ask the user before overwriting.

**Step 4: Write the file.** Compose the frontmatter block followed by the body content. Use exact YAML formatting (no extra whitespace, no quoting where unnecessary). The body content goes immediately after the closing `---` of the frontmatter, separated by a single blank line.

**Step 5: Confirm and surface warnings.** Tell the user where the file was saved (full path), summarize the frontmatter values, and list any validation warnings with severity. Save does not abort on warnings — it persists the file and trusts the user to address issues at their own pace.

## Output

A confirmation summary with the saved path, the frontmatter as written, and any warnings. Brief and scannable — the user wants to know it succeeded and what issues, if any, came up.

The shape, in skeleton:

```
Saved: <full path>

Frontmatter written:
- <field>: <value>
- [...]

[Warnings block, only if present]
Warnings:
- <field> issue — <one-line description with severity hint>
```

A clean save ends with a one-line "ready to use" confirmation. A save with warnings lists each warning with a brief description and a hint about whether action is recommended now (`repair` it) or whenever convenient.

## Output discipline

Save's output is functional. Confirm what was written and where, surface any issues plainly, and stop. No preamble framing the save, no unnecessary postamble suggesting next steps unless the warnings warrant action ("repair this file" if a warning is severe enough).

## Filename collision handling

If the generated filename already exists at the target path, save does not overwrite silently. The mode surfaces the collision with three options: rename the new file (suggesting a disambiguator), overwrite the existing file (with confirmation), or abort the save. The default is to ask rather than guess — collision usually means the user is updating an existing artifact, but sometimes means a name conflict the user didn't anticipate.

For voiceprints specifically: if the user is regenerating a voiceprint with the same author and scope, overwriting is usually the right answer. Save proposes overwrite as the default and asks for confirmation.

## Chained saves from other skills

When `os-voiceprint` produces a portrait and chains into save, the typical flow looks like this. The producer's output includes the portrait body plus suggested frontmatter values (author from the source, scope from context, source from the corpus identifier). Save receives both, validates the schema, generates the filename per the convention, writes the file, and returns the confirmation. The user is asked once — at the end of the producer run — whether to keep the artifact.

For on-the-fly creation during a drafting session, the chain is similar but the save step is optional. Drafting can use a temporary voiceprint without persisting it. Save only happens if the user confirms keeping it for future use.

## Cross-mode suggestions

After a save, mention adjacent operations only when warranted. If the save produced warnings worth addressing, point at `repair`. If the user just saved a new voiceprint and is mid-drafting flow, mention that drafting can now load the new voiceprint via find. Otherwise no postamble — the save is the result.
