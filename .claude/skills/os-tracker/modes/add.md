# Mode: add

Add a new item to a tracker context. Dry-run by default.

## Inputs

Per the contract in `references/contract.md`:

- `context` (required) — slug. Auto-create file if absent.
- `section` (required) — one of `next`, `actions`, `open-questions`, `bugs`, `needs`, `ideas`, `backlog`.
- `area` (optional) — for `actions` or `open-questions`, the sub-area name.
- `text` (required) — item text.
- `source` (optional) — wikilink to source.
- `tags` (optional) — inline metadata tags.

## Procedure

1. Resolve the context file. If it doesn't exist, create with empty schema from `templates/context.md`. Log creation as `[type: audit] [skill: os-tracker]` in `os-inputs/_os-inbox.md`.

2. Build the item line:
   - For checklist sections (`next`, `actions`, `open-questions`, `bugs`, `needs`, `backlog`): `- [ ] <text> — <source-wikilink> [tag: value] [tag: value]`
   - For `ideas` (prose section): paragraph or bullet without `- [ ]`

3. Locate the insertion point:
   - For `next`: append to the `## Next (≤5)` section. If the section already has 5 items, surface the cap and propose demoting the oldest item to its area-actions section as part of the same operation.
   - For `actions` / `open-questions` with `area`: locate or create `## <Area> — actions` (or `— open questions`).
   - For `bugs`, `needs`, `ideas`, `backlog`: append to the existing single section.

4. Update the source map:
   - If `source` is provided and not already in `## Source map`, append the wikilink there.

5. Update the watermark to the current time.

6. **Dry-run.** Show the proposed file diff (added section if any, inserted item, source-map update, watermark update). Wait for confirmation.

7. On confirmation, write.

## Output

Confirmation of the inserted item's location: context, section, area (if any), line number. Caller can use this for follow-up `update` operations.

## Approval gates

- Standard dry-run + confirmation before write.
- The `Next` cap (5) triggers a sub-decision: confirm both the new add AND the demotion of the displaced item.
