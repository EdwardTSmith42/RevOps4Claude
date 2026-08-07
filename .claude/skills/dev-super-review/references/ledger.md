# Findings ledger format

Malleability note: the status vocabulary and Decision-line shape are canonical
(commits and code comments reference them); section ordering and prose style
are adaptable.

One markdown file, the campaign's system of record. Header states the ID
convention and the dedup rule ("when a later slice finds the same root issue,
update Also-seen-in and append evidence instead of creating a duplicate").

## Status vocabulary (fixed)

`open` · `needs-decision` · `accepted-risk` · `deferred` · `fixed` ·
`duplicate-of <ID>`

## Entry shape

```markdown
### <PROJECT>-REV-NNN - <one-line title in plain language>

Status: <status>
Severity: P1 | P2 | P3
Primary slice: <slice name>
Category: <rubric category>

Files:
- <repo-relative paths>

Problem:
<plain-language description; quote evidence verbatim with file:line or
commit hashes when the finding rests on archaeology>

Recommended fix:
<the smallest correct shape; name alternatives only when the choice is real>

Decision: <human> <date> — <what was decided, the why, accepted trade-offs,
implementing commit hash>
```

## Ledger rules

- IDs are stable and never reused; gates and side-quests mint new IDs even
  late in the campaign.
- An entry flips to `fixed` only with a Decision line naming the human, the
  date, and the commit.
- `needs-decision` entries carry a recommendation — the human ratifies or
  overrides; they should never have to do the investigation themselves.
- Slice trust notes (a short per-slice verdict section) live at the bottom of
  the ledger so the release owner can read confidence by area.
- Counts quoted anywhere else (PR descriptions, readiness docs) must be
  re-derived from the ledger at every checkpoint — stale counts are the first
  sign of record drift.
