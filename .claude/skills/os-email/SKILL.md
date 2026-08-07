---
name: os-email
version: 0.1.0
description: >-
  Triage Gmail inboxes via a 7-label future-action taxonomy (action-required,
  needs-reply, needs-support, vendor-admin, receipts, newsletter, meetings) —
  each label is a handle for a downstream workflow that may not exist yet
  (support handler, reply drafter, meetings workflow), so labels stay broad
  until those workflows ship. Personal OS's v1 starter pillar; operates on any
  connected Google Workspace account. Six modes: audit, setup, first-sweep,
  incremental, filter-design, docs-comments. Triggers on "audit my inbox," "set
  up email triage," "triage my inbox," "do an inbox sweep," "design a Gmail
  filter," "what should I label this email." Do NOT trigger for outbound email
  composition (use `os-writing` mode `email`).
display_name: Email
tagline: Triage Gmail with a 7-label taxonomy that earns its splits.
category: Planning
packs:
  - personal-os
icon: 'phosphor:Envelope'
when_to_use: >-
  Personal OS's v1 starter pillar. Operates on any connected Google Workspace
  account. The 7-label taxonomy (action-required, needs-reply, needs-support,
  vendor-admin, receipts, newsletter, meetings) stays broad on purpose — each
  label is a *handle for a downstream workflow*, not a final destination.
  Workflows like reply-drafter and support-handler will graduate from these
  labels later.


  Start with `audit` to see what's in your inbox, then `setup` for per-account
  profiles, then `first-sweep` for the historical mass, then `incremental` for
  the daily pass. `filter-design` and `docs-comments` are specialized lanes.
modes:
  - name: audit
    job: Read-only audit of inbox state across labels.
  - name: setup
    job: Configure per-account triage profile.
  - name: first-sweep
    job: First triage pass over the historical inbox.
  - name: incremental
    job: Daily triage pass.
  - name: filter-design
    job: Design Gmail filters from observed patterns.
  - name: docs-comments
    job: Triage Google Docs comment notifications.
---

# Email — keep the inbox usable, set up for AI handoff over time

## Purpose

Aggressively move low-action mail out of the inbox while preserving anything that may require attention, a reply, or future operational lookup. Default posture: archive by default, preserve action-risk and human-reply mail. Every touched message gets at least one triage label and is then either archived or intentionally kept visible.

The skill is built around a mental model — read `references/triage-philosophy.md` first. The short version: **labels denote future actions, not content types**. The label answers "what happens next?" — `needs-support` because a support workflow eventually handles it, `needs-reply` because a reply is composed (today by the human, eventually by an AI drafting workflow). Labels start broad. Sub-classifications (refund, cancellation) are added only when downstream skills exist to consume them.

The skill is account-agnostic. The taxonomy and classification rules are universal; per-account knobs (sender filters, account-specific rules, account-specific labels) live in `os-inputs/email-accounts/<account>.md`, written by `setup` after grounded findings from `audit`.

## When to use

The user wants insight into or action on their inbox. Common triggers: "audit my inbox," "show me what's in there," "triage my inbox," "do a sweep," "set up triage on this account," "design a filter for sender X."

If the user is composing outbound mail, route to `os-writing` (mode `email`). Reply drafting is a separate, higher-stakes capability — see `references/reply-drafting-roadmap.md` — and is not in this skill's v1 scope.

## Modes (v0.1)

| Mode | Job | Output |
|---|---|---|
| `audit` | Read-only sampling of inbox + recent archive — the front door | Inbox-shape narrative + audit artifact in `os-inputs/email-accounts/<account>.audit.md` |
| `setup` | Confirm audit findings, create labels with approval, write per-account profile | Created labels + `os-inputs/email-accounts/<account>.md` |
| `first-sweep` | Process N unprocessed messages, propose label+archive, batch-confirm, apply | Triage report + applied actions + sweep log |
| `incremental` | Catch-up against the unprocessed query, bounded by last-sweep watermark | Same shape, smaller batches |
| `filter-design` | Propose Gmail filters from observed patterns | Filter spec + creation with approval |
| `docs-comments` | Sub-method for `comments-noreply@docs.google.com` notifications | Per-doc classification |

### Self-determining when not specified

- *"Show me what's in my inbox" / "audit my inbox" / "what's in there"* → `audit`
- *"Set up triage on this account"* → `setup` (run `audit` first if no audit artifact exists)
- *"Triage my inbox" / "do a sweep" / "process my unread"* → `first-sweep` if no profile exists, otherwise `incremental`
- *"Design a filter for sender X"* → `filter-design`
- *"What about this Google Docs comment from Z"* → `docs-comments`

## Recommended user flow

```
audit                                ← wow moment, ~30 seconds, read-only
   ↓
setup (uses audit findings)          ← interview becomes confirmation
   ↓
first-sweep --dry-run                ← second wow moment, still read-only
   ↓
first-sweep                          ← apply
   ↓
incremental + filter-design (ongoing)
```

The audit step earns its place: without it, setup asks questions the user can't answer accurately, and the buyer doesn't see grounded value until step 4.

## Deferred to future versions

| Mode / capability | Phase | What it does |
|---|---|---|
| `draft-replies` | v0.2+ | Drafts replies for `needs-reply` and `needs-support` labels into Gmail drafts; never sends. Phase 1 of the reply-drafting roadmap. |
| `revert <sweep-id>` | v0.2 | Reverts a sweep using the JSONL sweep log. |
| `meetings` workflow | v0.2 | Designed handling of post-meeting transcripts, summaries, action items. Currently labeled `meetings` and kept visible. |
| `digest` | v0.3 | Periodic digest of archived `newsletter` mail. |
| Cross-account learning | v0.3 | When the user has multiple accounts, sender patterns confirmed on one suggest filters on another. |

## Inputs

- **Account.** Read from whatever email connector is wired (any Gmail/mail MCP). The skill never asks the user for an email address. Tool names vary by connector — modes name capabilities, and `setup` records the capability-to-tool mapping per `../_shared/references/cross-harness-adaptation.md` (Connectors vary too).
- **Per-account profile.** `os-inputs/email-accounts/<account>.md` — written by `setup`, read by every mode that mutates state.
- **Audit artifact.** `os-inputs/email-accounts/<account>.audit.md` — written by `audit`, read by `setup` and `filter-design`.
- **User principles.** `AGENTS.md` — operating principles loaded into agent context for runtime judgment.
- **Voiceprint.** Reserved for `draft-replies`; loaded via the `library` skill's matching convention.

## Hard guardrails

The skill enforces these regardless of user instruction:

1. No deletion.
2. No auto-unsubscribe.
3. No auto-reply or auto-cancel.
4. No sender-only filters for mixed-use vendors.
5. Account-mutating actions require explicit per-action approval (label creation, batch archive, filter creation are all dry-run by default).
6. No personal data in the skill — sender lists, account-specific senders, identified humans live in profile artifacts only.
7. **No pre-creation of labels for workflows that don't exist yet.** Refund handling, cancellation routing, billing-dispute escalation all stay under `needs-support` until a support-handler skill ships.

See `references/guardrails.md` for the full list and rationale.

## The unprocessed query

All sweep modes use this Gmail search to find untriaged inbox mail:

```
in:inbox -label:newsletter -label:receipts -label:action-required -label:needs-reply -label:needs-support -label:vendor-admin -label:meetings
```

Messages already carrying any triage label are skipped on subsequent sweeps.

## Self-extending behavior

The 7-label taxonomy is deliberately frozen as the universal core, but the surfaces *around* it are additive — new account-specific labels for the user's business shape, new sub-methods like `docs-comments` for platform notification types that don't classify well from the email body alone, new account profiles as the user connects additional Google Workspace accounts. When a sweep or audit surfaces a clear pattern that doesn't fit the existing 7 labels and doesn't fold cleanly into an account-specific label already in the profile, do three things: name the gap explicitly (what the cluster looks like, why it doesn't fit), offer two paths (fold into the closest existing label with a per-account rule, or surface a candidate account-specific label that the user can adopt during `setup --refresh`), and on the second path update the per-account profile via `setup --refresh` rather than inventing a label silently. The universal 7 stay broad and stable; growth happens in the per-account profile and in new sub-method references when a platform's notifications need their own classification logic.

## References

- `references/triage-philosophy.md` — the foundational mental model. Read first.
- `references/label-taxonomy.md` — the 7 labels and what each captures
- `references/classification-rules.md` — the 7 numbered rules for assigning labels
- `references/guardrails.md` — non-negotiables
- `references/docs-comments.md` — Drive comment sub-method
- `references/reply-drafting-roadmap.md` — phased plan for the future drafting capability
- `templates/account-profile.md` — per-account profile starting shape

