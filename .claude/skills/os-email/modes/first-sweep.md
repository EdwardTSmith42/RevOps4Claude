# Mode: first-sweep

The wow-moment guided run. Process N unprocessed messages, propose label+archive per message, batch-confirm, apply.

## Inputs

- Account (from MCP)
- Per-account profile (`os-inputs/email-accounts/<account>.md`) — required; if missing, route to `setup` first
- `--limit N` — how many messages to process this sweep (default 50)
- `--dry-run` — propose classifications without applying

## Procedure

### 1. Load context

- Read the per-account profile.
- Read `references/label-taxonomy.md`, `references/classification-rules.md`, `references/guardrails.md`.
- Verify the 7 triage labels exist on the account (mapped list-labels tool). If any are missing, route to `setup`.

### 2. Fetch unprocessed messages

Use the mapped message-search tool with:

```
in:inbox -label:newsletter -label:receipts -label:action-required -label:needs-reply -label:needs-support -label:vendor-admin -label:meetings
```

Limit to N. Fetch full content via the mapped batch content fetch (or per-message fetch if the connector has no batch call — note the slowdown).

### 3. Classify each message

For each message, apply the classification rules in order. Capture:

- Proposed label(s)
- Proposed action (keep visible / archive)
- Confidence (high / medium / low)
- Reasoning (one sentence — which rule fired and why)

For Google Docs comment notifications, route to the `docs-comments` sub-method.

For ambiguous messages (low confidence), default to keep-visible with `action-required` or `needs-reply` and flag for user review.

### 4. Group and present

Group the proposed actions:

- **Keep visible** (action-required, needs-reply, post-meeting artifacts)
- **Archive** (vendor-admin, receipts, newsletter, past-meeting reminders)
- **Needs user judgment** (low confidence)

Present the report to the user. Show counts and samples per group. Show the full list for "needs user judgment."

### 5. Batch confirm (approval gate)

Ask the user to approve in batches:

- Approve "keep visible" group as-is? (Usually yes — these only add labels, no archives.)
- Approve "archive" group as-is? (The bigger commitment — applies labels AND removes from inbox.)
- For "needs user judgment," walk one-by-one or skip.

User can override individual proposals before approving the group.

### 6. Apply (skip if --dry-run)

Use the mapped batch label-modify tool to apply labels and remove `INBOX` where archiving. Group operations by destination label for efficiency.

### 7. Update watermark, sweep log, and report

- Update the per-account profile's `last_sweep` timestamp.
- Append observed sender patterns worth converting to filters (these feed `filter-design`).
- Append a sweep log entry to `os-inputs/email-accounts/<account>.sweeps/<timestamp>.jsonl` — one line per processed message with `{message_id, applied_labels, archived, confidence, rule_fired}`. Enables a future `revert <sweep-id>` mode and gives the user an audit trail.
- Generate a final report:
  - Total processed
  - Counts by label
  - Sender patterns observed (3+ messages from same sender within sweep)
  - Suggested next action (run `filter-design`, run `incremental` again, done)

## Approval gates

- Before applying labels: batch confirmation, archive group separate from keep-visible group.
- Individual override: any proposal can be overridden before the batch is approved.
- Dry-run: no approval needed; the report is the deliverable.

## Performance notes

- Batch label modifications via the mapped batch tool rather than one-at-a-time.
- For sweeps over 100 messages, paginate the Gmail search rather than asking for everything at once.
