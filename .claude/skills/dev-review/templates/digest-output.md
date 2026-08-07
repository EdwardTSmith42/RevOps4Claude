# Digest output template

Output structure for `digest` mode. Lives at `.local/check-digest/<YYYY-MM-DD>/`.

## Files produced

```
.local/check-digest/<YYYY-MM-DD>/
├── index.md              # ranked queue (this template, top half)
├── details/
│   └── pr-<num>.md       # per-PR brief (this template, bottom half)
├── report.json           # structured artifact (JSON shape below)
└── pm-summary.md         # optional, --pm-view (PM-friendly)
```

## index.md (ranked queue)

```markdown
# Open PR Ship-Readiness Digest — <YYYY-MM-DD>

**Repo:** <owner>/<repo>
**Filter:** author=<author>, state=open, limit=<N>
**Total PRs:** <count>

## Ranked Queue

| Rank | PR | Title | Severity | Fix Risk | Testability | Ship Today? | Detail |
|---|---|---|---|---|---|---|---|
| 1 | [#<num>](<url>) | <title> | S<n> | low/med/high | manual-friendly/mixed/script-heavy | ✅ Yes / ⚠ With conditions / ❌ No | [→](details/pr-<num>.md) |
| 2 | ... | ... | ... | ... | ... | ... | ... |

## Top ship candidates (ready today)
- [#<num>](<url>) — <one-sentence outcome>
- ...

## Top blocked items
- [#<num>](<url>) — <one-sentence blocker>
- ...

## Open notes
- Error-reporting signal availability: <full / partial / none — when no IDs/signatures in PR text>
- Risk scoring: heuristic, conservative; treat as triage input, not human-sign-off replacement
```

## details/pr-<num>.md (per-PR brief)

```markdown
# PR #<num>: <title>

**URL:** <github url>
**Author:** <username>
**Branch:** <head> → <base>
**Status:** <draft / open / changes requested / approved>
**Days open:** <n>

## What it does
<Plain-language one-sentence description.>

## Bug / support signals
- Support system: <link or "none referenced">
- Feedback tracker: <link or "none referenced">
- Project tracker: <link or "none referenced">
- GitHub issue: <link or "none referenced">
- Reporter quotes: <"verbatim phrase from PR description or comments" or "none">

## Error-reporting impact (if available)
- Issue ID: <id or "no error-reporting signal in PR text">
- Event count (last 24h): <n>
- First-seen: <ts>
- Last-seen: <ts>
- Affected Users: <count if confirmed; otherwise "unknown (not tracked)">

## Files touched
- Total: <n> files / +<additions> -<deletions>
- Dangerous file flags: <lockfile / migration / schema / contract / generated artifact / deploy config — list, or "none">

## Testability
**<manual-friendly / mixed / script-heavy>**

<Reasoning: e.g., "UI-heavy change, manual smoke covers it" / "backend logic with existing tests, script-driven" / "mixed — has both">

## Severity + fix-risk
- **Severity:** S<n> — <one-sentence reason>
- **Fix risk:** <low / medium / high> — <one-sentence reason>

## Unresolved comments
- <count> review threads unresolved
- <count> external-reviewer comments unresolved
- Notable: <highest-priority unresolved comment summary, or "none">

## Ship recommendation
**<Ready today: yes / no / with conditions>**

<Reasoning: what's blocking, what would unblock, or "ready to merge as-is">
```

## report.json (structured)

```json
{
  "generated_at": "<UTC timestamp>",
  "repo": "<owner>/<repo>",
  "filter": {
    "author": "<author>",
    "state": "open",
    "limit": <N>
  },
  "total_prs": <count>,
  "prs": [
    {
      "number": <num>,
      "title": "<title>",
      "url": "<url>",
      "author": "<user>",
      "branch": "<head>",
      "base": "<base>",
      "rank": 1,
      "ship_recommendation": "ready_today | with_conditions | blocked",
      "severity": "S0 | S1 | S2 | S3",
      "fix_risk": "low | medium | high",
      "testability": "manual-friendly | mixed | script-heavy",
      "files_touched": <n>,
      "additions": <n>,
      "deletions": <n>,
      "dangerous_files": ["<file>", ...],
      "unresolved_review_threads": <n>,
      "unresolved_reviewer_comments": <n>,
      "error_reporting_impact": {
        "issue_id": "<id or null>",
        "event_count_24h": <n or null>,
        "first_seen": "<ts or null>",
        "last_seen": "<ts or null>",
        "attributed_users": <n or null>,
        "tracking_confirmed": <bool>
      },
      "bug_signals": {
        "support_system": "<link or null>",
        "feedback_tracker": "<link or null>",
        "project_tracker": "<link or null>",
        "github_issue": "<link or null>"
      },
      "days_open": <n>
    }
  ]
}
```

## pm-summary.md (optional, --pm-view)

```markdown
# PR Status Snapshot — <YYYY-MM-DD>

## Top <N> ship candidates

### #<num>: <title>
- **What:** <one-sentence outcome>
- **Impact:** <one-sentence user/business impact>
- **Ship status:** Ready today / Ready with conditions / Blocked
- **Unblock action:** <if not ready, what's needed to flip it>

### #<num>: <title>
...

## Active blockers (notable)
- #<num>: <title> — <blocker reason> — <unblock action>
- ...
```

## Notes

- Avoid technical jargon in `pm-summary.md` — reference `details/pr-<num>.md` for technical detail.
- `userCount` from most error-reporting tools is `attributed users` by default, not affected users.
- Risk scoring is heuristic and intentionally conservative.

## Used by

- `digest` mode of `dev-review`.
