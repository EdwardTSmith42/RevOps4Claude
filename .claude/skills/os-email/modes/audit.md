# Mode: audit

Read-only inspection of the user's inbox + recent archive to understand what's actually there. Produces a structured report that drives the rest of the skill: pre-fills `setup`, suggests filter candidates, surfaces emerging label needs, identifies mixed-use vendors empirically.

This is the front door. It runs **before** any account-mutating action. The user can run `audit` at any time without changing inbox state — no labels are applied, no archives, no filters.

## Why this exists

A buyer with thousands of unread messages doesn't know what's in their inbox. Asking them "what are your top 5 noisiest senders?" up front gets a foggy guess. Looking at the actual inbox produces grounded answers in seconds. Audit is also the wow moment — connect Gmail, see the shape of your inbox in 30 seconds.

## Inputs

- Account (from MCP)
- `--depth quick|full` — `quick` samples 200 messages (default), `full` samples 500
- `--window <days>` — how far back to sample (default 30 days inbox + 30 days archive)

## Procedure

### 1. Sample messages

Pull two parallel samples via the mapped message-search tool:

- **Inbox sample** — `in:inbox newer_than:<window>d`, capped at depth.
- **Archive sample** — `-in:inbox newer_than:<window>d`, capped at depth/2.

The archive sample reveals what the user already triages out. Senders heavy in archive but rare in inbox tell us the user has implicit rules already.

Fetch full content via the mapped batch content fetch.

### 2. Cluster

Cluster the sample along these axes:

- **By sender** — top senders by volume (inbox vs archive), with proposed classification per sender.
- **By content shape** — what the message looks like (newsletter, receipt, human reply, automated notification, calendar artifact, support ask, etc.). Use `triage-philosophy.md` and `classification-rules.md` to classify.
- **By future-action label** — projected `action-required` / `needs-reply` / `needs-support` / `vendor-admin` / `receipts` / `newsletter` / `meetings` distribution.
- **By mixed-use signal** — senders showing 2+ distinct content shapes (e.g., Stripe sends receipts AND security alerts). Auto-flagged as never-sender-only-filter.

### 3. Surface patterns

Generate findings in plain language:

- **Inbox shape** — one-line percentage distribution across the 7 triage labels (plus an "other" residual), computed from the projected classification of the sample.
- **Top filter candidates** — senders with 5+ messages all classified the same way, none mixed-use. Listed with sample subject lines.
- **Mixed-use vendors detected** — listed with the distinct content types observed.
- **Emerging label candidates** — patterns that don't fit the universal 7 labels. For each candidate, surface a short question that names the observed cluster (count, what the senders have in common) and proposes a candidate label or asks whether to fold it into an existing one. Common shapes worth watching for: collaboration-tool noise (Slack-class, Linear-class), named-client mail for consultants, student/member questions on a course platform, internal-team correspondence. Surface these as questions, not commitments. The user decides during `setup`.
- **Implicit rules** — patterns visible in archive but not inbox. Surface them as observations the user can convert to filters: name the sender, name what they already do with it (archive everything), and ask whether to formalize.
- **Threads needing reply** — count of threads where the user hasn't replied to the most recent inbound message older than 3 days.

### 4. Inbox-shape narrative

Write a 3–5 sentence narrative describing the inbox to the user. Plain language, not stats. The narrative should give the user a felt sense of what their inbox actually is: what dominates the volume, what they care about that's threaded through, what they're already triaging implicitly, and which mixed-use vendors will need narrower filtering rather than sender-only blocks. Concrete to *their* inbox — name actual senders and patterns observed in the sample, not generic categories.

This narrative is the wow moment. It's what the buyer remembers.

### 5. Write the audit artifact

Save the audit to `os-inputs/email-accounts/<account>.audit.md`. Include:

- Audit timestamp + depth + window
- Inbox shape distribution
- Top 20 senders with proposed classification + mixed-use flag
- Filter candidates (sender + sample subjects + proposed label)
- Mixed-use vendors detected
- Emerging label candidates (as questions for the user)
- Inbox-shape narrative
- Suggested next step (`setup` if no profile exists; `setup --refresh` if profile exists but stale; `filter-design --from-audit` if profile exists and is current)

This artifact is consumed by `setup` and `filter-design`. Re-running `audit` overwrites it. Past audits aren't preserved by default — the inbox state at the time is the only audit that matters.

### 6. Present to user

Show the user:

- The narrative (always)
- The inbox-shape distribution (always)
- Top 5 filter candidates with one-click confirm (offered, not committed)
- Emerging label candidates (asked, not assumed)
- Suggested next step

Do not apply anything. The user runs `setup` next (or skips to `first-sweep --dry-run` for a deeper preview).

## Output

- `os-inputs/email-accounts/<account>.audit.md` written
- Inline narrative shown to user
- Suggested next mode

## Approval gates

None — this mode is read-only. The audit artifact is a write to the user's workspace, not to Gmail.

## Performance notes

- `quick` depth (200 messages) runs in well under a minute and is sufficient for the wow moment + driving setup.
- `full` depth (500 messages) is for buyers who want a thorough first audit; recommend it once the wow moment has happened and the user is invested.
- Use the batch content fetch rather than per-message fetches where the connector offers one.
- Cluster client-side rather than via Gmail search — the search API isn't built for this.
