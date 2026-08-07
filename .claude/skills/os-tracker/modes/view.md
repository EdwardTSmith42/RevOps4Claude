# Mode: view

Read the current state of one or more tracker contexts. Read-only.

## Inputs

- `context` (optional) — context slug, `all`, or `user` (default). When omitted: `user`.
- `section` (optional) — filter to one section.
- `since` (optional) — ISO timestamp. Show only items added/updated since this time.

## Procedure

1. Resolve context(s):
   - If `all`: read every `os-tracker/<slug>.md` file
   - If a specific slug: read `os-tracker/<slug>.md`. If file doesn't exist, surface the absence and offer to auto-create on next `add`.
   - Default `user`: read `os-tracker/user.md`. If absent, auto-create with empty schema (per the auto-create-on-first-use principle), then return the empty state.

2. Render the relevant content:
   - Without a `section` filter, return the full file
   - With a `section` filter, return only that section
   - With `since`, filter items by their last-modified marker (the watermark + per-item timestamps if the schema is extended later)

3. When `context: user` is used (the default), surface a hint that `system` exists and can be viewed with `view --context system`. Don't auto-show system.

## Output

Markdown matching the section schema, scoped to the requested context and filters. The user gets back exactly what's in the file (preserving custom sections they've added).

## Approval gates

None — read-only.
