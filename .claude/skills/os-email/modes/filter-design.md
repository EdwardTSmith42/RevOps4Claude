# Mode: filter-design

Propose new Gmail filters from observed patterns. Never sender-only for mixed-use vendors. The user reviews and approves; the skill creates the filter via the mapped filter-management tool only after approval. (If the wired connector can't create filters — some can't — say so and offer the filter spec for the user to add in Gmail's own settings instead.)

## Inputs

- Account (from MCP)
- Per-account profile — required
- Either:
  - `--sender <email>` — design a filter for a specific sender, **or**
  - `--from-sweep` — propose filters for senders observed during recent sweeps

## Procedure

### 1. Identify candidate

If `--sender`, use that. If `--from-sweep`, query the per-account profile's recent observations for senders with 3+ same-label messages.

### 2. Mixed-use vendor check

Cross-reference the candidate against:

- The mixed-use vendor list in `references/guardrails.md`
- The user's profile-flagged mixed-use vendors

If the candidate matches, **do not** propose a sender-only filter. Instead, propose narrower options:

- Subject pattern + sender (e.g. `from:noreply@stripe.com subject:(invoice OR receipt)`)
- List-Id + sender
- Full label-only without archive (so the user can see filtered mail in a label view but it stays in inbox)

### 3. Sample recent mail

Pull the last 10–20 messages from the candidate sender. Verify they're all the same triage class. If they're not (e.g. some receipts, some security alerts), refuse the sender-only filter and propose a narrower variant.

### 4. Propose the filter spec

Show the user:

- **Match criteria** (from, subject, list-id, has-the-words)
- **Action** (apply label, skip inbox, mark read, never spam)
- **Sample of recent matches** so they can sanity-check
- **What this filter would NOT have caught** (cases the criteria miss)
- **Risk callout** if any sample looks ambiguous

### 5. Approval gate

Wait for explicit approval. The user can edit any field before approving.

### 6. Create the filter

Create via the mapped filter-management tool. Confirm creation with the returned filter ID. Append the filter to the per-account profile's "Active sender filters" section.

### 7. Backfill (optional)

Offer to run the filter retroactively over the last N days of mail. Use the same approval flow as `first-sweep` for the backfill batch.

## Approval gates

- Filter spec: explicit approval before creation.
- Backfill: separate approval, batch-style.
- Mixed-use vendor: refuse sender-only outright; never present that as an option.

## What the skill never proposes

- Sender-only filters for mixed-use vendors (per `guardrails.md`).
- Filters that delete instead of archive.
- Filters that auto-mark spam.
- Filters that auto-hide future security alerts.
