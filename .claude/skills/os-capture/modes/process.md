# Mode: process

Classify open inbox entries and route them to their destinations. Dry-run by default. Applies on confirmation.

## Inputs

- `--depth quick|full` — `quick` processes the 50 most recent entries (default), `full` processes everything open
- `--dry-run` — explicit dry-run only, no apply prompt
- `--auto-trivial` — opt-in to auto-applying trivial-tier classifications without per-batch confirmation. Off by default; user can enable in `os-inputs/_os-setup-philosophy.md` when it exists.

## Procedure

1. **Audit pass.** Run the same classification logic as `audit` mode — read inbox, skip metadata, project destinations and confidence tiers per `references/classification-rules.md`. Build the routing plan.

2. **Group by tier.**
   - **Trivial-tier batch** — high-confidence classifications across all destinations. Single combined dry-run preview.
   - **Moderate-tier individual** — uncertain classifications, one-at-a-time decisions.
   - **Promotion candidates** — `[type: correction]` entries with proposed targets. Always individual, regardless of tier.

3. **Process trivial-tier batch.**
   - Show the user the full batch as a single dry-run: count by destination, list per destination with item text and proposed action.
   - Wait for confirmation. The user can override individual items before approving the batch.
   - On approval, apply each item:
     - User Tracker / System Worklog → invoke `os-tracker/add` with the appropriate parameters
     - Knowledge → append to or create `os-knowledge/<topic>.md`
     - Trash → no destination write; mark inbox entry only
   - For each routed item, append `[status: resolved]` and `*Routed to: <destination>*` to the inbox entry.

4. **Process moderate-tier individually.**
   - For each item, show the user: the entry, the proposed destination + one alternative, the reasoning.
   - User picks proposed, picks alternative, supplies a different destination, defers (`[status: deferred]`), or asks to skip.
   - Apply per the user's choice.

5. **Process promotion candidates individually.**
   - For each correction entry, follow the heuristic in `references/promotion-paths.md` to propose one target with a confidence read.
   - Show the user: the correction, the proposed target, the confidence, optionally one alternative if confidence is medium-or-lower.
   - User confirms, redirects, or defers.
   - On confirmation, write the lesson to the target. Append `*Promoted to: <target-path>*` to the inbox entry. Set `[status: resolved]`.

6. **Final report.** Show what was routed where:
   - Counts by destination
   - Items the user deferred (`[status: deferred]`)
   - Any errors or surprises
   - Suggested next moves (e.g., a note about deferred items worth re-processing soon, or a flag that a promotion to AGENTS.md may want a fresh-eyes review before the change goes live)

## Output

- Updated `os-inputs/_os-inbox.md` with `[status: resolved]` and routing/promotion trails on processed entries
- New or updated entries in `os-tracker/<context>.md` files (via `os-tracker/add`)
- New or updated entries in `os-knowledge/<topic>.md` files
- New or updated content in `AGENTS.md`, skill `references/`, or SOPs (per promotion)
- A processing report shown to the user inline

## Approval gates

- **Trivial-tier batch** — single confirm covers the whole batch, with override-before-confirm for individual items.
- **Moderate-tier** — per-item ask.
- **Promotion** — per-item ask, regardless of tier.
- **Auto-trivial mode** — when explicitly opted in via `_os-setup-philosophy.md`, the trivial batch applies without confirmation, but writes an audit entry to `os-inputs/_os-inbox.md` as `[type: audit] [skill: capture] [tier: trivial]` summarizing what was routed.

## Error handling

- **Tracker file doesn't exist** — `os-tracker/add` auto-creates per the contract. No special handling here.
- **Knowledge topic ambiguity** — when the destination topic isn't obvious, the entry escalates to moderate-tier and asks.
- **Promotion target ambiguity** — when the heuristic can't propose with high confidence, surface the ambiguity and offer all three targets.
- **Partial failure** — if a routing operation fails mid-batch, log the failure to inbox.md as `[type: audit] [skill: capture] [status: open]`, continue with remaining items, surface the failure in the final report.

## os-tune integration

When invoked from os-tune's `close-out` mode at session-end, `process` runs automatically with one offered confirmation that names the count of unprocessed inbox items and asks whether to process them now (accept / skip / decline). If the user accepts, `process` runs as normal. If skip or decline, no-op. The session-end pairing is configurable; the user can opt out via `_os-setup-philosophy.md`.
