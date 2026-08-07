# Mode: audit

Read-only inspection of `os-inputs/_os-inbox.md`. Projects what `process` would do without doing it.

This is the front door for users new to the skill, and the safe re-orientation move when the inbox feels noisy and the user wants to see what's there before acting.

## Inputs

- `--depth quick|full` — `quick` reads the most recent 50 entries (default), `full` reads everything

## Procedure

1. **Read the inbox.** Parse `os-inputs/_os-inbox.md` into entries by `## YYYY-MM-DD — title` headers. Capture body text, tags, status, and any `*Routed to:*` / `*Promoted to:*` trailing lines.

2. **Filter to processable entries.** Apply the skip rules from `references/classification-rules.md` rule 0: drop `[type: audit|lesson|reject]`, drop `[status: resolved|deferred]`, drop tag-only metadata.

3. **Project classification per entry.** Apply rules 1–5 to each remaining entry. Capture:
   - Proposed destination (Promotion / User Tracker / System Worklog / Knowledge / Trash)
   - Proposed section / area / target file as appropriate
   - Confidence tier (trivial / moderate)
   - Reasoning (one sentence)

4. **Aggregate and narrate.** Build the report:
   - **Counts** — open items, by destination, by confidence tier
   - **Inbox shape narrative** — 2-4 sentences in plain language describing what's accumulated, broken down by destination class (how many corrections, how many user-tracker items, how many system-worklog items, how many likely-trash) with whatever shape patterns are evident (e.g. clustering around a topic, recurring themes). The point is to give the user a felt sense of what's in there before they decide whether to process.
   - **Highlights** — anything striking. Repeat captures (same idea logged twice), aging entries (open for 14+ days), corrections that recommend overlapping changes.
   - **Suggested next move** — `process` if the user wants to act, or a more specific clean-up suggestion when one tier or destination dominates the open set and processing it alone would clear most of the noise.

5. **Surface, don't act.** No writes. No mutations. The audit is a read.

## Reachability sweep

The audit's second job (per SKILL.md): report files unreachable from the workspace map.

1. Read `_os-map.md` — the indexed surfaces and their index files.
2. Walk the workspace's data dirs (`os-inputs/`, `os-knowledge/`, `os-outputs/`, `os-tracker/`, workspace root `.md` files — not `skills/`, which SKILL_INDEX covers). For each file, it's reachable if its directory is indexed in the map OR something reachable links to it (markdown link or `[[wikilink]]`).
3. The inbox is the sanctioned orphanage — never flag it or its entries.
4. Report orphans as a short list with a one-line guess at each file's nature. REPORT ONLY — attaching an orphan is a routing decision for `process` or the user, never an auto-fix (per the hard guardrail).

## Output

A markdown report with the four sections above (Counts, Inbox shape narrative, Highlights, Suggested next move). The report is shown to the user inline.

Optional artifact: write the audit to `os-inputs/_audits/inbox-<timestamp>.md` if the user wants a record. Default off — `audit` is usually a transient view, not a saved record.

## Approval gates

None — read-only.

## Performance notes

- A `quick` audit (50 entries) runs in seconds and covers the active inbox window for most users.
- `full` reads everything, including aged resolved entries. Useful for `reflect`-adjacent queries but slower. Recommend `quick` by default.
