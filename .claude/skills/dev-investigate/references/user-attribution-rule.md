# User attribution rule

The discipline for reporting user-impact numbers when user attribution may not be tracked. Avoids the "0 affected users" lie.

## The rule

- **Default wording when attribution is unknown/unreliable: `Affected Users: unknown (not tracked)`.**
- Do NOT state `0 affected users` unless user attribution is explicitly known to be tracked for that issue family.
- When showing a raw `userCount` from an error-monitoring system, label it as `attributed users` unless tracking is explicitly confirmed.
- Only state a confident user-count when you've verified attribution tracking is reliable for the queried issue family.

## Why this works

Saying "0 affected users" when tracking is absent is misleading — the bug may affect many users we just don't see. The "unknown (not tracked)" wording preserves the epistemic honesty: we don't know, here's why, and here's what would let us know.

## When to apply

- Error-monitoring queries (any time `userCount` is reported).
- Impact estimation in PR-interrogation verdicts.
- Bug-fix PR descriptions and task-tracker summaries.
- Cross-system updates — any bug-comms workflow you maintain must enforce this in posted content.

## Filtering discipline for error-monitoring data

Two hard-won rules when narrowing error-monitoring queries:

- **Don't filter by internal issue ID alone.** Some monitoring tools group events into "issues" by an internal hash that occasionally combines unrelated events from different code paths. Filtering by issue ID alone can suppress real production events that share an internal group with dev noise. Scope filtering to environment + signature/message instead.

- **Treat dev-only / staging-only signatures as suspect until proved real.** Visual-regression tests, staging smoke tests, and CI runners produce a lot of error traffic that doesn't reflect production behavior. Mark such families as likely dev noise; only escalate as regression when the signature spreads across independent sessions or reaches production.

## Used by

- `evidence` mode — when error lane reports `userCount`.
- `pr-interrogate` mode — for impact estimation step.
- Any cross-system bug-comms workflow you maintain — for cross-system update content.

## Malleability note

**Canonical:** the "unknown (not tracked)" default and the "never claim 0 without confirmed tracking" rule. The epistemic-honesty floor is non-negotiable.

**Adaptable:** the specific filtering heuristics — adapt to the patterns your team's error-monitoring tool produces.

