# Mode: incremental

Daily/weekly catch-up against the unprocessed query. Same shape as `first-sweep` but tuned for ongoing maintenance rather than first-touch.

## Inputs

- Account (from MCP)
- Per-account profile — required
- `--since <duration>` — only process messages newer than this (default: since `last_sweep` watermark)
- `--limit N` — default 25
- `--dry-run`

## Differences from first-sweep

- Smaller default batch (25 vs 50).
- Bounded by the per-account `last_sweep` watermark — doesn't re-touch already-processed mail.
- Trusts the user's existing filters more — fewer "needs user judgment" surfacing because account patterns are known.
- Surfaces filter-design candidates more aggressively (any sender with 3+ unfiltered messages this sweep is a candidate).
- Shorter approval flow — when confidence is high across the board, the user can opt in to "auto-approve high-confidence archives, walk me through the rest."

## Procedure

Same as `first-sweep`, with the watermark applied:

```
in:inbox -label:newsletter -label:receipts -label:action-required -label:needs-reply -label:needs-support -label:vendor-admin -label:meetings after:<watermark>
```

Update watermark on completion.

## When to suggest filter-design

If the same sender appears 3+ times in one incremental sweep, all classified the same way, all low-action — surface a brief offer to the user that names the sender, the count and timeframe, and the consistent label, and asks whether to design a filter. Keep it short enough that the answer is obvious.
