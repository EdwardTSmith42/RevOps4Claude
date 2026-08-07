---
account: <email@example.com>
created: <YYYY-MM-DD>
last_sweep: null
account_type: <creator | consultant | founder | employee | mixed>
---

# Email profile — <email@example.com>

This profile captures account-specific customizations only. Universal rules live in the skill's references and are loaded at runtime.

## Account context

- Purpose:
- Replier(s): (just user / user + team / shared)
- Posture: archive by default, preserve action-risk and human-reply mail

## Account-specific labels

Beyond the universal 7. Each entry: label name → when to apply → downstream action.

- (none yet)

## Account-specific starting rules

Layered on top of `references/classification-rules.md`. The first matching rule still wins; account-specific rules add to the set.

- (none yet)

## Customer/member-facing patterns

Patterns that route to `needs-support`. Senders, subject patterns, or platform notifications whose underlying event is a customer ask.

- (none yet)

## Mixed-use vendors flagged for this account

In addition to the universal mixed-use list in `references/guardrails.md`. Sender-only filters are not allowed for any vendor on this list.

- (none yet)

## Active sender filters

Filters created by `filter-design` that apply to this account. Each entry: sender pattern → label → archive y/n.

- (none yet)

## Observed sender patterns (filter candidates)

Senders seen 3+ times during sweeps that haven't been promoted to a filter yet. Reviewed in `filter-design`.

- (none yet)

## Reply-drafting preferences

Reserved for when the writing skill ships. Captures per-account voice override, signature, escalation rules.

- Default voiceprint: (use library default unless overridden)
- Signature override: (none)
- Escalation rules: (none)

## Open questions

Account-specific things the user hasn't decided yet.

- (none yet)
