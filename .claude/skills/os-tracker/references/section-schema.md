# Section schema

Every Tracker context file uses this section structure in this order. Empty sections drop.

## Header

```
<Context Title>
Last refresh: YYYY-MM-DDTHH:MM
```

The first line is the title verbatim — no leading `#`. (This convention keeps the file compatible with note tools, like Bear, that render line 1 as the note title.) The watermark is set on every write.

## Sections

### `## Next (≤5)`

The handful of items the user is actually working on next. Strict cap of 5. Items pulled from areas the user has flagged as in-focus, or items marked time-sensitive. When `Next` would exceed 5, the lowest-priority item demotes to its area-actions section before the new item is added.

Format: checklist items.

### `## <Area> — actions`

Concrete, named work-items grouped by area. Each area gets its own `## <Area> — actions` section. Areas are user-defined or detected from item content. Each item ends with ` — [[Source Note Title]]` or ` — [[file/path.md]]` wikilink when there's an originating source.

Format: checklist items, optionally with sub-tasks for decomposed work.

### `## <Area> — open questions / decisions`

Items that read as questions or design choices ("Decide:", "Should we…?", "Why does…?"). Tracked as `- [ ]` so they're visible and check-offable; kept separate from actions so the user can mass-prune without touching real work.

Format: checklist items.

### `## Bugs / time-sensitive`

Cross-area bugs and calendar-bound items. One section across all areas — the urgency is the grouping principle, not the area.

Format: checklist items, optionally with `[deadline: YYYY-MM-DD]` tag.

### `## Needs / blockers`

Items waiting on someone or something else. Each entry names the blocker.

Format: checklist items, with the blocker named in the text or as `[blocked-by: <person/thing>]`.

### `## Ideas / parking lot`

Prose, **not** checklist. Exploration, single-word concepts, "what if…" musings. Doesn't count as open work. Don't drop these — the user wants them preserved. Resist the urge to convert them to action items unless the user explicitly asks.

Format: prose paragraphs or bullet points (without checkboxes).

### `## Backlog`

Stale tasks. Items that aged out of `Next` and area-actions but the user hasn't archived. **Never** auto-archive without user consent. Keep them visible here so the user can revisit.

Format: checklist items.

### `## Source map`

Wikilinks to source notes that have contributed items to this tracker. Auto-maintained by `add` when a `source` argument is provided. Lets the user trace back from a tracker item to where it came from.

Format: bulleted wikilinks, one per source note.

## Tags within items

Items can carry inline tags for metadata:

- `[deadline: YYYY-MM-DD]` — when the item is due
- `[blocked-by: <person/thing>]` — what's blocking progress
- `[priority: high]` — explicit priority bump (rare; default ordering is by section + position)
- `[done: YYYY-MM-DD]` — set on completion before move-to-bottom or archive

Tags are optional. The skill never requires them.

## Custom sections

Users opt into complexity by adding sections. Skill-supported additions documented in this file as they earn their place. Until then, custom sections are user-managed — the skill preserves them on read but doesn't reorganize them.

Examples a user might add (none in v0.1 default):

- `## Watching` — items the user is monitoring but not actively working on
- `## Waiting` — items in someone else's court for a known duration
- `## <Project> — videos / batches` — project-specific batch series

When a user repeatedly asks to add the same custom section across contexts, that's signal os-tune's `refine` could fold it into the default schema. Earns-its-place applies.
