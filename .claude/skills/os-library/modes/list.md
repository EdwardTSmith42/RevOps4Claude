---
name: os-library/list
description: Show the user what reference inputs they have on file, optionally filtered by type and tags. Triggers on "what voiceprints do I have," "show me my templates," "list my style samples," "what briefs are active." Do NOT trigger when the user wants the best match for a specific job (use `find`), is saving a new input (use `save`), or is sweeping for issues (use `validate`).
---

# Mode — List

Show the user what reference inputs they have on file. The simplest mode in the library skill — no scoring, no graceful degradation, just inspection.

## When to use

Direct user invocations include "what voiceprints do I have," "show me my templates," "list my active briefs," "what style samples do I have for pen-name-x," and similar inspection requests.

The mode is also useful as a discovery step before a more specific operation. A user thinking through a drafting project might list voiceprints to remember what's available, then invoke find for the specific job.

## Inputs

- Optional: a type filter (`voiceprints`, `style-samples`, `templates`, `briefs`, or `all`) — defaults to `all`
- Optional: tag filters on frontmatter fields (e.g., a specific author, a specific format, `status: active`)

If no filter is supplied, list everything grouped by type.

## Run

The procedure has three steps.

First, scan the filtered subdirectories of `os-inputs/`. Skip `README.md` files — every library directory ships with one as documentation; they're not library entries and carry no frontmatter by design. For voiceprints and templates, scan the directory directly. For style samples, scan one folder deep (samples are nested by author). For briefs, scan `current/` by default and `archive/` only if the user asked for archived briefs.

Second, read each file's frontmatter and produce a one-line summary per entry. The summary surfaces the key fields per type: voiceprint shows `author`, `scope`, `default`, `created`. Style sample shows `author`, `pattern`, `genre`. Template shows `format`, `proven`. Brief shows `project`, `target`, `status`.

Third, group results by type and present them. Within each type, order by recency (newest first) for voiceprints and briefs, by author then pattern for style samples, and by `proven: yes` then format for templates.

Files with missing or malformed frontmatter still appear in the list, with a `[needs repair]` flag. Do not skip them silently — the user should see what they have, including drift.

## Output

A grouped list, one section per type. Within each section, a flat list of entries with one line per entry showing the key fields. Use prose framing for the section intros where useful, but the entries themselves are list-shaped enumerations and stay bulleted.

The shape, in skeleton:

```
## Voiceprints (<N> files)

- <filename> — <key field>: <value>, <key field>: <value>, created: <date> [needs repair: <issue>]
- [...]

## Style samples (<N> files)
- <author>/<pattern>.md — pattern: <value>, genre: <value>, length: <approx words>

## Templates (<N> files)
- [...]

## Briefs — current (<N> active)
- [...]
```

Each entry surfaces the key frontmatter fields for that type — voiceprint shows author/scope/default/created, style sample shows pattern/genre/length, template shows format/proven, brief shows project/target/status. Files with frontmatter issues carry a `[needs repair: <one-line description>]` flag at the end of the line.

If the user passed a specific type filter, show only that section. If a tag filter narrowed results to zero, say so explicitly (e.g., that no templates with the requested format are on file) rather than returning an empty list with no context.

## Output discipline

The list output is informational. No preamble framing the result, no postamble suggesting next steps unless the user is clearly mid-workflow. Begin with the first section heading, end with the last entry.

If the corpus is large enough that listing everything would overwhelm (rare at v0.1, but possible later), default to a summary count per type with a hint to filter by author, scope, or format.

## Cross-mode suggestions

After listing, briefly mention adjacent modes if the user looks like they're about to need one. After listing voiceprints, mention `find` if the user seems to be deciding which to use. After listing files with `[needs repair]` flags, mention `repair` or `validate` as cleanup options. Skip the postamble if the user just wants the list.
