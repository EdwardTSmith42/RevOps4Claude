# Mode: update

Modify an existing tracker item — mark done, edit, move, delete. Dry-run by default; delete always requires explicit confirmation.

## Inputs

Per the contract in `references/contract.md`:

- `context` (required) — slug.
- `match` (required) — text substring or stored item ID.
- `action` (required) — one of `done`, `edit`, `move`, `delete`.
- `new_text` (required for `edit`).
- `to_section` (required for `move`); `to_area` (optional for `move`).

## Procedure

1. Resolve the context file. If absent, surface the absence and stop.

2. Find the matching item:
   - Substring match against item text
   - If zero matches: surface the zero-match, stop
   - If multiple matches: surface all matches with their sections and ask which one (don't proceed on ambiguity)
   - If one match: proceed

3. Apply the action:
   - **`done`**: change `- [ ]` to `- [x]`. Append `[done: <today>]`. Per default config, leave the item in place; if `_os-setup-philosophy.md` opts into auto-archive-on-done with a delay, the item moves to backlog after N days (handled by a separate sweep, not this mode).
   - **`edit`**: replace item text with `new_text`. Preserve checkbox state, source wikilink, and tags unless `new_text` includes new versions.
   - **`move`**: relocate item to `to_section` (and `to_area` if provided). When moving to/from `next`, respect the 5-item cap.
   - **`delete`**: remove the item line entirely.

4. Update the watermark.

5. **Dry-run.** Show the proposed file diff. Wait for confirmation.

6. **`delete` requires explicit confirmation regardless of dry-run mode.** Even if the user has opted into auto-approve-trivial, `delete` always asks.

7. On confirmation, write.

## Output

Confirmation of the change applied: action, item description, before/after location.

## Approval gates

- Standard dry-run + confirmation for `done`, `edit`, `move`.
- Always-ask for `delete`, regardless of any auto-approve config.
- Multi-match ambiguity always asks the user to disambiguate.
