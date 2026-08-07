# Label taxonomy

Seven labels. Every triaged message gets at least one. The label answers "what happens next?" — see `triage-philosophy.md` for the mental model.

| Label | Future action | Default action |
|---|---|---|
| `action-required` | Human takes a specific action by a deadline | Keep visible |
| `needs-reply` | A reply is composed (human today, AI-drafted later) | Keep visible |
| `needs-support` | Customer-support workflow handles it (human today, support-handler skill later) | Keep visible |
| `vendor-admin` | Filed for retention, no further action | Archive |
| `receipts` | Filed for bookkeeping (future accounting workflow) | Archive |
| `newsletter` | Filed for read-later or future digest workflow | Archive |
| `meetings` | Meetings-lifecycle workflow (transcripts → action items, etc.) | Mixed (see below) |

## When to use each

**`action-required`** — explicit action, deadline, migration, account risk, billing issue, security issue, model/API retirement, deprecation, breaking change. The user (a human) needs to do something specific.

**`needs-reply`** — a real person or business asks for a response that isn't customer support. Partnership pitches the user finds interesting, scheduling, feedback requests, decisions awaited, replies to the user's own outbound, collaboration threads.

**`needs-support`** — a customer or member asks for help: cancellation, refund, billing question, access issue, membership change, support ticket. Today the user handles these; eventually a support-handler skill activates against this label and may add sub-labels (`support:refund`, `support:billing`) when those sub-skills exist.

**`vendor-admin`** — account, compliance, policy, sub-processor, vendor cancellation, or operational notice with no immediate action. Archived but retained for retrieval.

**`receipts`** — payment, purchase, refund, cancellation confirmation, invoice, statement. Archived for bookkeeping.

**`newsletter`** — newsletters, creator content, podcasts, read-later learning material, low-action editorial mail, vendor product marketing.

**`meetings`** — calendar lifecycle: invites, reminders, prep, transcripts, summaries, recordings, action items.

## Multi-label

A message can carry more than one. The labels compose:

- A receipt that flags a price change → `receipts` + `action-required`.
- A meeting transcript with an explicit ask → `meetings` + `needs-reply`.
- A customer email that's a billing dispute escalating → `needs-support` + `action-required`.

Default-action precedence: any message with `action-required`, `needs-reply`, or `needs-support` is kept visible regardless of other labels.

## Meeting nuance

- Pre-meeting reminders/prep for past meetings → `meetings`, archive.
- Post-meeting transcripts/recordings/summaries/action items → `meetings`, **keep visible** until the meetings workflow is designed.

## What's deliberately NOT a label (yet)

- **No sub-classifications** like `refund-request`, `cancellation`, `billing-dispute`. These roll up into `needs-support` until the support-handler skill ships and earns the split. See `triage-philosophy.md` Principle 2.
- **No product-specific risk labels** (e.g. `stripe-billing`). Use `action-required` and let the message body carry specifics.
- **No sender labels** (e.g. `from-clickup`). Sender-based archiving belongs in Gmail filter rules.
- **No priority labels** (`p0`, `urgent`). Default actions encode urgency.

## Account-specific labels

The user's per-account profile may add labels when the user articulates a real downstream action:

- `clients` — a consultant who genuinely separates client mail and routes it to a client-thread workflow.
- `from-team` — a corporate user separating internal collaboration mail.
- `students` — a course teacher separating student-support mail (could also be `needs-support`).

These come from observed inbox patterns surfaced during `audit` and confirmed during `setup`. The agent never invents account-specific labels without user confirmation.
