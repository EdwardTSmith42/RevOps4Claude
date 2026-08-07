# Classification rules

Read `triage-philosophy.md` first — these rules implement those principles. The label always answers "what happens next?" not "what kind of email is this?"

Apply rules in order; the first matching rule wins. When multiple rules apply, prefer the one that keeps the message visible.

## 1. Customer/member support requests get `needs-support`

Use `needs-support` when a customer, member, student, or paying user asks for help. This is the broad bucket for any support-flavored ask, regardless of sub-type.

- Cancellation requests, refund requests, billing questions, access issues, membership changes, support tickets, "your product broke for me," "how do I do X."
- Including automated notifications whose underlying event is a customer message (e.g., a platform DM notification of a customer ask).
- The user handles these today. When a support-handler skill ships, it activates against this label and may add sub-labels for the categories it can handle.
- Do not automate cancellation or refund handling at triage time. Triage and preserve context only.

## 2. Direct human or business requests get `needs-reply`

Use `needs-reply` for non-support human asks where the user owes a response.

- Real-person requests for partnership, feedback, scheduling, a decision, or continuing an active conversation.
- Replies to the user's own outbound where the human came back with substance.
- Cold collaboration or paid-partnership pitches: keep visible as `needs-reply` when strategically interesting; archive obvious mass outreach as `newsletter`.
- Academic/editorial group threads: `needs-reply` when title or latest message implies pending revision/manuscript action.
- Google Docs comment notifications: inspect the doc; see `docs-comments.md`.

## 3. Action-risk platform/vendor notices get `action-required`

Use `action-required` for platform, vendor, infrastructure, billing, security, legal, tax, or compliance notices that require the user (a human) to do something specific.

Signals: `action required`, `retirement`, `sunset`, `deprecated`, `breaking change`, `migration`, `billing failed`, `security`, `suspension`, `API change`, `model`, `quota`, `terms`, `account access`, payment-failure, hold-on-account.

- Model/context-window retirement notices, API deprecations: never auto-archive.
- Plausible legal, tax, insurance, payroll, or compliance-risk notices: keep visible even when copy is salesy.
- Service-continuity notices: keep visible when access, billing, verification, deployment, or production integrations may stop working.

## 4. Vendor/admin notices without immediate action get `vendor-admin`

- Sub-processor changes → `vendor-admin` unless they include an explicit action or deadline.
- Product/admin updates that explicitly state no pricing, configuration, or action changes → `vendor-admin`.
- Old low-balance alerts and old sign-in/security-code notifications → `vendor-admin` once confirmed stale or expected.
  - **Never** create a standing rule that hides future security alerts by default.
- Old test emails, verification-code emails, resolved/duplicate incident artifacts → `vendor-admin` after retention.

## 5. Receipt-shaped retention mail gets `receipts`

- Payment, purchase, refund confirmation, invoice, statement, successful-payment notifications.
- Cancellation confirmations: `receipts` (matches retention reason).
- A receipt that also flags an action (price change, plan migration) gets `receipts` + `action-required`.

## 6. Editorial / promotional volume gets `newsletter`

- Newsletters, creator content, podcasts, read-later learning material, low-action editorial mail.
- Vendor/product marketing, launch announcements (when the sender is recurring low-action).
- Prefer sender-based Gmail filters once a sender is confirmed low-action.
- **Never** sender-only archive filters for mixed-use vendors. See `guardrails.md`.
- Do not unsubscribe automatically.
- Keep archived newsletters available for future digest workflows.

## 7. Calendar lifecycle gets `meetings`

- Pre-meeting automation (generic prep emails) → take no automatic action unless the user confirms a sender-specific rule.
- Old calendar invites and event reminders for past meetings → `meetings`, archive.
- Post-meeting transcripts, recordings, summaries, action items → `meetings`, **keep visible** until the meetings workflow is designed.
- A transcript with an explicit ask → `meetings` + `needs-reply`.

## Per-account overrides

The user's `os-inputs/email-accounts/<account>.md` profile may add account-specific rules — for example, a recurring sender the user always wants surfaced as `action-required`, or a platform DM channel whose underlying event is a customer ask that should route to `needs-support`. Account-specific rules layer on top; they don't replace.

Account-specific labels (e.g., `clients`, `from-team`) are also defined in the profile and applied alongside the universal seven.

## When in doubt

Keep visible. False-positive cost is one extra glance; false-negative cost can be a missed deadline or lost customer. Use `action-required` or `needs-reply` and surface during the sweep report so the user can downgrade if appropriate.
