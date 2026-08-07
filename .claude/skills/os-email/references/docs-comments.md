# Google Docs comment sub-method

For `comments-noreply@docs.google.com` notifications, the email subject and body alone are usually not enough to classify. Inspect the actual document when needed.

**Precondition.** Drive scope must be authorized on the connected Google Workspace MCP. If only Gmail scope is available, fall back to subject-line classification and surface the limitation to the user.

## Procedure

1. **Extract** the document title and URL from the email.
2. **Inspect** the actual Drive comments via the Google Workspace MCP (`list_document_comments` / `list_presentation_comments` / `list_spreadsheet_comments`) when the email content is ambiguous.
3. **Prioritize** unresolved comments over resolved comments.
4. **Classify as `needs-reply`** when:
   - The user owns or is clearly responsible for the document, **and**
   - A named person asks for a concrete edit, reply, copy, decision, or review.
5. **Before labeling `needs-reply`, screen for outreach/sales-attention tactics:**
   - Comment text points attention at a CTA, landing page, offer, or marketing copy without clear relationship to active work.
   - The commenter appears to be using the doc comment mainly to surface themselves in the inbox.
   - The request is vague, performative, or unrelated to a known project.
6. **Archive** unresolved Docs comments when they appear to be sales/outreach attention tactics rather than real work.
7. **Do not archive** unresolved human asks just because the sender is an automated Google notification.
8. **Resolved comments** can usually be archived unless the resolution reveals a still-open follow-up.

## When the document is shared, not owned

The user's per-account profile may flag certain collaborators or domains as business-adjacent. Comments from those collaborators on shared documents stay visible as `needs-reply` when the comment implies active work, even if the user doesn't own the doc.

## Bulk handling

When a sweep encounters multiple Docs comment notifications for the same document, group them. Inspect the document once, classify all related notifications together, and apply labels in one batch.
