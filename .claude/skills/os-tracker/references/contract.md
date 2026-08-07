# Tracker contract

Other skills (Capture, os-tune, Email's draft-replies when it ships) invoke Tracker's modes to add or update items. They don't edit `os-tracker/<context>.md` files directly. Centralizes section-schema discipline.

## `os-tracker/add`

Creates a new item in a tracker context.

**Inputs:**
- `context` (required) — the context slug (e.g., `user`, `system`, or a project/client slug the user has added). If the file doesn't exist, auto-create with empty schema.
- `section` (required) — one of: `next`, `actions`, `open-questions`, `bugs`, `needs`, `ideas`, `backlog`. Maps to the corresponding `## …` section.
- `area` (optional) — sub-grouping within `actions` or `open-questions` (e.g., a domain like "Email" or "Marketing", or a project name). When provided, the item lands in `## <area> — actions` (or `— open questions`); if that sub-section doesn't exist, it's created.
- `text` (required) — the item text. Plain prose, no leading `- [ ]` marker (the skill adds the right prefix per section).
- `source` (optional) — wikilink to originating file or note (e.g., `os-inputs/_os-inbox.md` or `[[Master Tracker — Personal]]`). Appended to the item as ` — <wikilink>` and added to the `## Source map` section if not already present.
- `tags` (optional) — array of inline tags (`deadline: 2026-05-10`, `blocked-by: customer-feedback`, etc.). Rendered as `[tag: value]` after the text.

**Behavior:**
- Dry-run by default; show the proposed insertion before applying.
- Update the watermark on write.
- If `section: next` would exceed the 5-item cap, propose demoting the oldest `Next` item to its area-actions section as part of the same operation.

**Returns:** the inserted item's location (context, section, line) for downstream reference.

## `os-tracker/update`

Modifies an existing item.

**Inputs:**
- `context` (required) — the context slug.
- `match` (required) — item identifier. Either a text match (skill finds by substring) or a stored item ID from a prior `add` / `view` call.
- `action` (required) — one of:
  - `done` — mark complete (`- [ ]` → `- [x]`), append `[done: <today>]`, optionally move to backlog after N days (configurable in `_os-setup-philosophy.md`; default: leave in place)
  - `edit` — replace item text; requires `new_text` parameter
  - `move` — change the section/area; requires `to_section` and optional `to_area` parameters
  - `delete` — remove the item; requires explicit confirmation regardless of dry-run mode

**Behavior:**
- Dry-run by default; show the proposed change before applying.
- For `delete`, always require confirmation (overrides any "auto-approve trivial" config).
- Update the watermark on write.

**Returns:** confirmation of the change applied.

## `os-tracker/view`

Reads tracker state.

**Inputs:**
- `context` (required) — context slug, or `all` for all contexts, or `user` for the user-visible default. Default when called without args: `user` only.
- `section` (optional) — filter to one section.
- `since` (optional) — ISO timestamp. Returns only items added/updated since this time. Useful for os-tune's inheritance scan.

**Behavior:**
- Read-only. No writes, no watermark update.

**Returns:** the relevant tracker content as structured data (context, section, items with metadata) or rendered markdown depending on the caller.

## Conventions for skills writing through Tracker

- **Capture** writes via `add`. When routing inbox items to a tracker, `source` should be `os-inputs/_os-inbox.md` and the item text should preserve the original capture's intent. After write, append `[status: resolved]` and `*Routed to: os-tracker/<context>.md — <section>*` to the inbox entry.
- **os-tune** reads via `view --context system` for inheritance (knowing what's in flight). When os-tune's modes complete a piece of work, they can write via `update` with `done` action.
- **Other skills** ship without direct Tracker integration unless they have a clear use case. Earns-its-place.

## Errors and fallbacks

- If a context file doesn't exist on `add`, auto-create with empty schema, log the creation as `[type: audit] [skill: os-tracker]` to inbox.md.
- If a `match` finds zero items on `update`, surface the zero-match condition rather than silently no-op'ing.
- If a `match` finds multiple items on `update`, surface the matches and ask which one (per pace-the-human principle — don't act on ambiguous matches).
