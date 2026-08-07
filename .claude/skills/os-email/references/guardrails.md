# Guardrails

Non-negotiable rules the skill enforces regardless of user instruction. If a user explicitly asks for something on this list, surface the guardrail, explain why, and offer the safe alternative.

## Never

- **Delete mail during triage.** Even when the user says "just delete the spam." Archive instead — Gmail retains everything and the user can always purge later.
- **Unsubscribe automatically.** Unsubscribing is a user-visible action that can confirm the address to spammers and can lose access to mail the user actually wants. Surface candidates; the user clicks unsubscribe.
- **Auto-reply.** Even templated. Even a brief acknowledgment. Reply mail goes through `os-writing`, not triage.
- **Auto-cancel memberships, subscriptions, or payments** in response to inbox content. Customer/member cancellation requests get labeled `needs-support` and kept visible.
- **Pre-create labels for workflows that don't exist yet.** No `refund-request`, no `cancellation`, no `billing-dispute` — those are `needs-support` until a support-handler skill ships. See `triage-philosophy.md` Principle 5.
- **Apply sender-only archive filters to mixed-use vendors.** Google, Stripe, PayPal, banks, payroll providers (Gusto), insurance, cloud (AWS/GCP/Azure), infrastructure (Cloudflare), and core business platforms send mixed mail — receipts AND security AND billing AND newsletters. Filtering by sender alone hides mail that needs to be seen.
- **Create a standing rule that hides future security alerts.** Old security codes can be archived case by case. A filter that auto-hides them is a foot-gun.
- **Ship personal data in the skill.** Sender filter lists, account-specific senders, identified humans, mixed-use vendors specific to the user's business — these live in `os-inputs/email-accounts/<account>.md` only.

## Always

- **Dry-run by default for account-mutating actions.** Creating labels, applying filters, batch-archiving — show the user what will happen before it happens. Confirm step is required.
- **Per-action approval.** Even after a confirm step, large batches are processed with a final "OK to apply to all N?" pause. The user can opt in to silent application via their account profile.
- **Preserve action-risk mail when in doubt.** If a message is ambiguous, label it `action-required` or `needs-reply` and keep visible. Better a small false-positive cost than a missed migration deadline.
- **Inspect mixed-use senders message-by-message.** When the user asks "should I filter Google?" the answer is "Google sends receipts, security alerts, Drive shares, Calendar invites, and Workspace billing — no, but here are three narrower patterns we can filter."
- **Log every applied action.** The user gets a triage report at the end of every sweep: what was labeled, what was archived, what was skipped and why.
- **Watermark the per-account profile.** After every sweep, update the profile's `last_sweep` timestamp and any new sender patterns observed.

## Mixed-use vendor reference list

Treat these as never-sender-only-filter by default. The user's profile may extend this list.

- Google (Workspace, Drive, Docs, Calendar, Pay, Ads)
- Stripe, PayPal, Square
- Banks (Chase, BoA, Wells Fargo, etc.)
- Payroll (Gusto, ADP, Rippling)
- Insurance (any)
- Cloud (AWS, GCP, Azure, Cloudflare, Vercel, Netlify)
- Core dev infrastructure (GitHub, GitLab, Sentry, Datadog)
- Core business SaaS the user has confirmed sends mixed mail (no-code builders, email/newsletter platforms, automation, databases, AI providers, etc. — captured per-account in the user's profile, not hard-coded here)
