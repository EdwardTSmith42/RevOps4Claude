# Reply drafting roadmap

Drafting replies is a separate, higher-stakes capability that hangs off the triage skill. This document maps the phased rollout so triage v1 sets up clean hooks for it.

## Why phased

Drafting replies is high-stakes for three reasons:

1. **Reputation.** A bad reply goes out under the user's name.
2. **Irreversibility.** Send is a one-way action. Mis-tone, factual errors, or misread intent cost trust.
3. **Context dependency.** A correct reply often requires context the email alone doesn't carry — past threads, project state, customer history, current commitments.

The right rollout earns trust on narrow, well-understood categories before expanding scope. The skill ships with an explicit phase model so the user (and the agent) know which phase a given category is in.

## The phases

### Phase 0 — Triage only (current scope)

- AI labels and archives.
- Humans reply.
- Triage labels (`needs-reply`, `needs-support`) make reply queues findable.

### Phase 1 — Drafts for review

- AI drafts replies and saves them as Gmail drafts.
- Every draft requires human review and explicit send.
- Start narrow: calendar confirmations, simple acknowledgments, FAQ-style support answers, "got your message, will look at it tomorrow"-class replies.
- Each draft includes confidence + the rationale for what it's saying.
- The human's edits feed back into voiceprint and pattern templates.

### Phase 2 — Calibrated drafting

- Voiceprint + situational templates dialed in from Phase 1 feedback.
- AI drafts a wider range of categories.
- Human approves with light edits or one-click send.
- Per-category confidence threshold: "send without me reading line-by-line for these categories I've reviewed N times and signed off on."

### Phase 3 — Send autonomy for narrow categories

- AI sends specific approved categories (e.g., calendar reschedules, common acknowledgments) without per-message human review.
- Human spot-checks a daily digest of sent mail.
- Categories revoked if any send produces a complaint or correction.

### Phase 4 — Compound workflows

- AI handles multi-turn back-and-forth that requires actions in other systems (issue refund via Stripe, schedule via calendar, update CRM).
- Each compound workflow is its own skill that hangs off `needs-support` (or another action label) with its own approval gates and rollback plan.

## What v1 sets up for this

Triage v1 (this skill) is Phase 0. It doesn't draft replies. But it deliberately:

- Keeps `needs-reply` and `needs-support` as clean, action-oriented labels — the input queues for drafting.
- Stores user voice and identity in canonical locations (`os-inputs/voiceprints/`, `os-inputs/_os-user-profile.md`) the future writing skill will read.
- Documents the per-account profile as the place where reply preferences (signature, tone overrides per account, escalation rules) accumulate.
- Reserves the deferred mode `draft-replies` in `SKILL.md` so the integration point is named even before it ships.

## Heuristics for picking Phase 1 categories

When the writing skill ships, start with categories that meet all of:

1. **Bounded response.** A finite set of correct answers (yes/no/reschedule, link to FAQ, "received, thanks").
2. **Low blast radius.** A wrong reply is easily corrected and doesn't lose money or trust.
3. **Repeated.** The user has handled this category enough times that voice and approach are stable.
4. **Recoverable.** A bad draft caught in review costs nothing; a sent reply can be followed up with a correction.

Bad starting categories: anything novel, anything customer-facing about money, anything with legal implications, anything where the answer depends on facts the AI may not have.

## Where drafting plugs in

The writing skill (when it exists) reads:

- The Gmail message (subject, body, thread history)
- The user's voiceprint via `library` skill matching
- The per-account profile from `os-inputs/email-accounts/<account>.md`
- User principles from `AGENTS.md`
- A category-specific template from `os-inputs/templates/` if one exists

It writes a Gmail draft. It does not send. Send is always a human action in Phase 1, an approved-category-only AI action in Phase 3+.
