# Triage philosophy

The mental model the skill operates from. Read this before any other reference. When a runtime decision is ambiguous, return to these principles.

## Principle 1 — Labels denote future actions, not content types

A label answers "what happens next?" not "what kind of email is this?"

- `action-required` → a human takes a specific action by a deadline.
- `needs-reply` → a reply is composed (today by the human, eventually by an AI drafting workflow).
- `needs-support` → a customer-support workflow handles it (today by the human, eventually by a support-handler skill).
- `vendor-admin` → filed for retention; no further action.
- `receipts` → filed for bookkeeping (eventually consumed by an accounting workflow).
- `newsletter` → filed for read-later or a future digest workflow.
- `meetings` → handed off to a meetings-lifecycle workflow.

Each label is the entry point to a downstream workflow. If the workflow doesn't exist yet, the label is a placeholder and the human handles the action. When the workflow ships, it activates against the existing label without taxonomy churn.

## Principle 2 — Start broad. Narrow only when a downstream skill earns it.

The opening taxonomy is deliberately small. Don't pre-create labels for workflows that don't exist.

- A refund request is `needs-support` today, not `refund-request`. There's no refund-handler skill yet.
- A cancellation request is `needs-support` today, not `cancellation`.
- A billing dispute is `needs-support` today, not `billing-dispute`.

When a `support-handler` skill ships and it learns to handle refunds, the message can carry both labels — `needs-support` + `support:refund` — so the support skill can route. But the broad bucket comes first; narrow sub-labels are added when there's something to route to.

The cost of premature narrowing is taxonomy bloat the user has to maintain forever. The cost of starting broad is occasional manual sub-classification — recoverable.

## Principle 3 — Multi-label is encouraged when actions compose

A message can carry more than one label. The labels combine; they don't compete.

- A receipt that flags a price change → `receipts` + `action-required`.
- A meeting transcript with an explicit ask → `meetings` + `needs-reply`.
- A customer email that's both a refund request and a billing question → `needs-support` (broad) and, when sub-skills exist, `support:refund` + `support:billing`.

## Principle 4 — Action labels beat filing labels on conflict

When in doubt, surface. The default actions encode urgency:

- `action-required` and `needs-reply` and `needs-support` → keep visible.
- `vendor-admin`, `receipts`, `newsletter`, `meetings` (most) → archive.

A message that could be either a receipt or an action-required item gets `action-required` and stays visible. False-positive cost (one extra glance) is much lower than false-negative cost (missed deadline, lost customer).

## Principle 5 — No pre-creation of labels for work we can't do yet

If there's no skill, SOP, or human-defined process behind a proposed label, don't create the label. Use the broadest existing bucket instead.

This applies to:
- Sub-classifications (refund, cancellation, billing) — wait for the support handler.
- Routing labels (`route:to-team`, `route:to-cpa`) — wait for the routing skill.
- Project labels — wait for explicit user direction.

The exception: the user's per-account profile may add account-specific labels (e.g., `clients` for a consultant who genuinely separates client mail) when the user articulates a real downstream action. The agent surfaces these candidates from the audit; the user confirms.

## Principle 6 — One source of truth for shared components

The user's voiceprint, identity, principles, and per-account profile are loaded from canonical locations and never duplicated inside the skill:

- Identity → `os-inputs/_os-user-profile.md`
- Voiceprint(s) → `os-inputs/voiceprints/` (matched via the `library` skill)
- Per-account profile → `os-inputs/email-accounts/<account>.md`
- User principles → `AGENTS.md`

When reply drafting ships, it reads voiceprint and account profile from these sources. When new triage rules are added, they layer onto the universal rules without overwriting them.

## Principle 7 — Calibrated handoff to AI replies

Drafting replies is a separate, higher-stakes activity. The skill is built so reply drafting can plug in over time without restructuring triage:

1. Triage labels stay stable. `needs-reply` and `needs-support` are where drafting hooks in.
2. Drafting starts on low-risk categories (calendar confirmations, simple acknowledgments) with human review of every draft.
3. Voiceprint + situational templates accumulate during the human-in-the-loop phase.
4. Categories graduate to less oversight as confidence is earned.
5. Compound workflows (e.g., issue refund via Stripe inside `needs-support`) come last.

See `reply-drafting-roadmap.md` for the phased rollout. The key implication for triage: keep `needs-reply` and `needs-support` clean and well-classified, because they're the inputs to that future workflow.

## What this means for the agent at runtime

When the agent is classifying a message:

1. Ask "what's the next action?" first. The label follows.
2. If multiple actions apply, multi-label.
3. If the next action is unclear, prefer the visibility-preserving label.
4. Don't invent a new label unless the user has articulated a downstream workflow for it.
5. Surface emerging patterns to the user during sweeps so they can decide whether new sub-labels are earned.
