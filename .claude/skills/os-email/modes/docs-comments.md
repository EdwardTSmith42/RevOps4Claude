# Mode: docs-comments

Sub-method for `comments-noreply@docs.google.com` notifications. Inspect the actual document when needed and classify accordingly.

This mode is invoked by `first-sweep` and `incremental` when they encounter Docs comment notifications, and can be invoked directly when the user asks "what about that Google Docs comment from X."

## Inputs

- One or more Docs comment notification messages
- Per-account profile (for collaborator/domain whitelist)

## Procedure

Follow `references/docs-comments.md` end to end. The reference is the source of truth; this mode is the executor.

### Drive inspection

Use the Google Workspace MCP:

- `list_document_comments` for Docs
- `list_presentation_comments` for Slides
- `list_spreadsheet_comments` for Sheets

Prioritize unresolved comments. Match comment authors against the user's per-account profile to identify business-adjacent collaborators.

### Bulk grouping

When multiple notifications arrive for the same document within a sweep, inspect the document once and apply labels to the whole group.

### Output

- Per-message classification: `needs-reply` (kept visible) or appropriate archival label
- Reasoning per message
- Any new collaborator patterns worth adding to the per-account profile
