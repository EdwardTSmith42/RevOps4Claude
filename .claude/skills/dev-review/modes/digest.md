# Mode: digest

Part of the `dev-review` skill. Selected when the user wants a portfolio-scoped ranked queue across multiple open changes — phrasings like "Rank our open PRs," "Daily ship-readiness digest," "Which PRs are ready to ship today?", "PM-friendly summary of what we have in flight."

## Job

Build a ship-readiness digest across all (or filtered) open PRs in a repo. For each PR, produce a brief with: unresolved review-thread + external-reviewer comment counts, files touched + add/del + dangerous-file flag, testability classification, severity + fix-risk, ship-readiness recommendation. Output an index board (ranked) + per-PR briefs + JSON artifact + (optional) PM-friendly summary.

## Scope adaptation

Unlike the per-change modes, `digest` is intentionally portfolio-scoped (across many open PRs). It doesn't apply per-change sub-agent fanout heuristics from `scope-adapter.md` directly. Instead, it has its own fanout pattern:

- **For large queues (>10 open PRs):** fan out by PR — one subagent per PR for the per-PR brief; parent reconciles into the index board.
- **For small queues (≤10 PRs):** review serially in a single agent.

Per the user's design ask: should adapt to any number of open PRs.

## Run

### 1. Identify scope

- **Default:** `--repo` from current `git rev-parse --show-toplevel`'s remote, `--author @me`, `--limit 30`.
- **Filter flags:** `--repo`, `--author`, `--state open`, `--limit N`, `--label`, etc.
- **Output paths:** `.local/check-digest/<YYYY-MM-DD>/index.md`, `.local/check-digest/<YYYY-MM-DD>/details/pr-<num>.md`, `.local/check-digest/<YYYY-MM-DD>/report.json`, `.local/check-digest/<YYYY-MM-DD>/pm-summary.md` (when requested).

### 2. List open PRs

```bash
gh pr list \
  --repo <owner>/<repo> \
  --state open \
  --author @me \
  --limit 30 \
  --json number,title,url,headRefName,baseRefName,updatedAt,createdAt,additions,deletions,changedFiles,labels,reviews,reviewDecision,mergeable,mergeStateStatus
```

### 3. For each PR (sub-agent fanout for large queues), gather and score

Per-PR data shape (preserve verbatim from source):

- **Files touched / additions / deletions / dangerous-file flag** — flag dangerous files (lockfiles, schemas, migrations, contract files, generated artifacts, deploy configs).
- **Unresolved review-thread count + unresolved external-reviewer comment count** (human reviewers, autonomous review agents, anything posting threaded comments) — `gh api repos/<owner>/<repo>/pulls/<num>/comments` for line-level; track unresolved threads explicitly.
- **Testability classification** — `manual-friendly` / `mixed` / `script-heavy`. Heuristic: changes to UI/routes → manual-friendly; pure backend logic with existing tests → script-heavy; in between → mixed.
- **Bug/support signal extraction** — pattern-match in PR description + comments for links to your support system, feedback tracker, project tracker, and GitHub issues; plus reporter-quote phrasing ("user reported," "customer hit," "saw error in production"). Configure the specific link patterns per your stack.
- **Error-reporting impact when available** — if PR text references issue IDs from your error-reporting system, query it for event count, first-seen, last-seen. Apply user-attribution rule: never `0 affected users` without confirmed tracking.
- **Severity + fix-risk classification** — heuristic. Risk scoring is intentionally conservative (default to higher risk when uncertain).
- **Ship-readiness recommendation** — `ready today: yes / no / ready with conditions`.

### 4. Produce the index board (ranked)

Sort by ship-priority signals:
- Unresolved external-reviewer comment count (descending — more pressure → higher rank)
- Error-reporting impact (descending if available)
- Severity (descending)
- Days open (descending — older PRs that should ship)

Cap the board at the top N (default 30; tunable).

### 5. Produce per-PR briefs

For each PR, write `.local/check-digest/<date>/details/pr-<number>.md` with:
- Title + URL
- Status snapshot (review state, merge state, days open)
- Bug/support signal links (support system / feedback tracker / project tracker / GitHub issue, per your stack)
- Error-reporting impact (if available; user-attribution rule applies)
- Files touched + dangerous-file flags
- Testability + severity + fix-risk
- Unresolved comment summary
- Ship recommendation + reasoning

### 6. (Optional) PM-friendly summary

If `--pm-view`, produce `pm-summary.md` focused on:
- Top N ship candidates (default top 5)
- Per-candidate: one-sentence what + impact + ship-readiness
- Unblock actions (what's needed to flip each from "not ready" to "ready")

Avoid technical jargon in PM summary; reference the per-PR briefs for technical detail.

### 7. Produce JSON artifact

Write `.local/check-digest/<date>/report.json` with structured data for downstream tooling:

```json
{
  "generated_at": "<UTC timestamp>",
  "repo": "<owner>/<repo>",
  "filter": { ... },
  "prs": [
    {
      "number": 425,
      "title": "...",
      "url": "...",
      "rank": 1,
      "ship_recommendation": "ready_today",
      "severity": "S1",
      "fix_risk": "low",
      "testability": "manual-friendly",
      "files_touched": 12,
      "additions": 234,
      "deletions": 45,
      "dangerous_files": [],
      "unresolved_review_threads": 0,
      "unresolved_external_reviewer_comments": 0,
      "error_reporting_impact": null,
      "bug_signals": [...]
    },
    ...
  ]
}
```

## Hard rules

- **Keep API calls low-impact:** one bounded snapshot per run. Don't fan out to per-PR detail calls beyond what's needed.
- **`userCount` from most error-reporting tools is `attributed users` by default, not affected users.** Apply user-attribution rule.
- **Risk scoring is heuristic and intentionally conservative.** Don't over-claim ship-readiness.
- **This is triage input, not a replacement for human sign-off on high-risk changes.** Always.
- **For sandboxed/worktree automation:** prefer `.local/...` or `/tmp/...` paths if the canonical workspace path isn't writable.

## Mode-specific references

- `../templates/digest-output.md` (index + per-PR brief + JSON shapes)

Cross-cluster:
- `../../dev-investigate/references/user-attribution-rule.md` (Affected Users wording for error-reporting-linked impact)

Cross-skill:
- If your error-reporting system has an MCP server or CLI, invoke it directly for impact queries. The user-attribution rule applies regardless of tool.

## Output

See `../templates/digest-output.md`. Files produced:
- `index.md` — ranked queue board
- `details/pr-<num>.md` — per-PR briefs
- `report.json` — structured artifact
- `pm-summary.md` (optional)

## Design Rationale

Mode-specific notes:

- **Portfolio-scoped, distinct from per-change modes.** `ship-gate` evaluates one change deeply; `digest` evaluates many changes broadly. Different shape, different output.
- **Sub-agent fanout per PR** for large queues — keeps individual PR analysis focused while the parent agent reconciles into the index board.
- **Prompt-driven scoring** rather than a deterministic builder script. Trades systematic risk scoring for adaptability and zero install footprint; revisit if drift across runs becomes a problem.
- **Testability trichotomy** (`manual-friendly` / `mixed` / `script-heavy`) — useful for ranking what's reviewable today vs needs more proof work.
- **`ready today: yes/no`** — binary recommendation simpler than full ship-gate verdict; right shape for a ranked queue.
- **"Triage input, not a replacement for human sign-off"** — explicit non-replacement framing.
- **Risk scoring conservative** — preserve the conservative bias from the source.
- **Output paths to `.local/` not `<workspace>/logs/`** — sandbox-safety; not committed.

