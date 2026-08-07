---
name: os-library/validate
description: Sweep the entire os-inputs/ directory and produce a repair worklist of files with frontmatter issues, ordered by severity. Triggers on "check my inputs," "sweep for issues," "what files need repair," or as a periodic maintenance pass. Do NOT trigger when the user wants to fix a specific file (use `repair`), find inputs for a job (use `find`), or inspect the collection (use `list`).
---

# Mode — Validate

Sweep across all of `os-inputs/` and produce a worklist of files that need attention. Validate identifies issues without fixing them — repair is the action mode. Validate gives the user the inventory of what needs work and how severe each issue is.

This mode is voluntary maintenance. The library is forgiving by design — find works on whatever's available, list shows everything including drift, save persists with warnings rather than failing. Validate is the periodic sweep that lets the user catch up on bookkeeping at their own pace, when convenient.

## When to use

Direct user invocations: "check my inputs," "sweep for issues," "what needs repair," "validate my library."

Periodic maintenance: a user accumulating inputs over weeks should run validate occasionally to keep drift in check. A user noticing find returning more repair flags than expected should run validate to see the full picture.

## Inputs

- Optional: a type filter to validate only one input type (`voiceprints`, `style-samples`, `templates`, `briefs`)
- Optional: a severity threshold (`severe-only` shows just the must-fix items, `all` shows everything including missing optional fields)

If no filters are supplied, validate sweeps everything and reports all severities.

## Run

The procedure runs through five steps.

**Step 1: Scan all inputs subdirectories.** Walk `os-inputs/voiceprints/`, `os-inputs/style-samples/<author>/`, `os-inputs/templates/`, and `os-inputs/briefs/current/` plus `os-inputs/briefs/archive/`. Skip `README.md` files — they ship as directory documentation, not library entries, and flagging them would report a broken library on every fresh install. Read each remaining file's frontmatter and identify which schema applies based on directory placement.

**Step 2: Check each file against its schema.** For every file, validate against the relevant `references/<type>-schema.md`. Issues fall into three severity tiers.

Severe: missing required fields (a voiceprint without `type` or `author`, a brief without `project`). These can break matching or cause inferred-default behavior the user didn't intend.

Moderate: malformed *closed-enum* values (a `default: maybe` instead of yes/no, a `proven: true` instead of yes/no/with-context, a `status: complete` instead of active/done/archived). These are real schema violations because the field's value space is fixed.

Mild: missing optional but recommended fields (no `created` date on a voiceprint, no `notes` on a template), and unknown values on *open-enum* fields (`scope`, `pattern`, `format`). The open-enum fields explicitly support freeform values via the `<other>` slot — a `scope: q4-launch-campaign` is not malformed, it's an extension of the taxonomy. Flag these for awareness so the user can confirm whether the freeform value is intentional, but do not treat them as errors.

**Step 3: Group results by severity and type.** A severe issue on a voiceprint is more important than a mild issue on a template. Group the worklist so the user can act on severe issues first. Within each severity tier, order by type (voiceprints first since they're loaded most), then alphabetically within type.

**Step 4: Surface auto-detect-able issues that aren't strict schema violations.** Two examples: a voiceprint file with no body content (frontmatter is fine but the actual portrait is missing or empty), and a brief with `status: active` that's older than 6 months (likely should have moved to archive). These aren't required by the schema but are worth surfacing as "consider checking this."

**Step 5: Produce the worklist.** A grouped list, severity-ordered, with file path and one-line description of the issue per entry. The user can work through it via repair (one file at a time) or pick targeted fixes.

## Output

A structured worklist organized by severity, then by type within severity. Use prose framing for the section intros. Entries are list-shaped enumerations — bullets are appropriate.

The shape, in skeleton:

```
## Validate sweep — <N> files checked, <M> issues found

### Severe (<N> files, fix first)

These have missing required fields. Find may rank them low or skip them entirely until repaired.

- <path> — <missing/malformed required field>
- [...]

### Moderate (<N> files)

Malformed closed-enum values. Find ranks them but with reduced confidence.

- <path> — <field>: <bad value> (should be <enum values>)
- [...]

### Mild (<N> files)

Missing optional but recommended fields, or unfamiliar open-enum values worth confirming.

- <path> — missing <field> (<one-line rationale for why it'd help>)
- [...]

### Other observations (<N> files)

- <path> — <non-schema concern: empty body, stale status, etc.>
```

Each entry is one line: file path, then the issue in a short clause. When the sweep finds nothing, the output is a single line stating the count and "no issues found." Don't pad.

## Output discipline

The worklist's value is in being scannable and actionable. The user should be able to look at the worklist and decide what to fix in 30 seconds. Severity ordering is the most important property — a wall of mild issues with severe ones buried in the middle is the failure mode.

If the worklist is long (more than ~20 entries), provide a summary count at the top and show severe and moderate fully, with mild collapsed to a count and a hint to filter (`severe-only` or `--severity moderate`).

## When to run validate

Validate is voluntary, not required. Reasonable cadences include weekly during heavy curation periods, monthly during light use, or whenever find starts surfacing more repair flags than usual. The library does not enforce a schedule.

A user who never runs validate isn't doing anything wrong — find and list will keep working, surfacing repair flags inline as needed. Validate just gives the inventory view, which is more efficient when the user wants to clean up several files at once.

## After validate

The natural follow-up is repair — work through the severe issues first, then moderate, defer mild as time permits. Repair handles one file at a time with confirmation per file, so the user controls the pace.

If the worklist surfaces a recurring issue (multiple voiceprints missing `created`, several templates missing `notes`), the user can address them in batch via repair-in-sequence. The library doesn't bulk-repair without per-file confirmation, so "batch" still means working through the list one at a time, just quickly.

## Cross-mode suggestions

After a sweep, the obvious next step is repair. Mention it briefly with a count of severe and moderate issues to address. If the worklist is empty, no postamble — the sweep is the result.
