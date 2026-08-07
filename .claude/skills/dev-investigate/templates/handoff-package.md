# Investigation handoff package

Strict-ish output template for `evidence` mode of `dev-investigate`. Produces a developer-ready handoff with timeline, hypotheses, lane status, PR-overlap verdict, and next-checks guidance.

Render as a markdown document. Sections in this order:

```markdown
# Investigation: <plain-language bug summary>

## Incident context and user impact

- **What's broken:** <one-sentence symptom + user impact>
- **Reported by:** <support conversation / user / detection source>
- **Time bounds:** <UTC window>
- **Environment scope:** <production / staging / development / multi-env>
- **Affected Users:** <count if attribution confirmed; otherwise "unknown (not tracked)">

## Evidence index

Plain file paths for local artifacts; clickable links for web resources.

- Support: <links + file paths>
- Runtime: <links + file paths>
- Error (error-monitoring): <links>
- Replay: <site/recording IDs + screenshot paths>

## Timeline correlation

UTC-aligned events across systems:

| Timestamp (UTC) | Lane | Event |
|---|---|---|
| <ts> | <support/runtime/error/replay> | <event> |
| ... | ... | ... |

## Hypothesis matrix

| Hypothesis | Confidence | Status | Supporting evidence |
|---|---|---|---|
| <hypothesis> | <low/medium/high> | <proposed/in_test/confirmed/partially_confirmed/rejected/abstain> | <link/path> |

## What this cannot be

- <ruled out scenario> — because <specific clue>
- <ruled out scenario> — because <specific clue>

## Unknowns

- <unknown>
- Next verification step: <executable check>

## Lane status matrix

| Lane | Status | Blocker (if blocked) | Fallback attempted |
|---|---|---|---|
| Support | complete/partial/blocked/pending | ... | ... |
| Runtime | ... | ... | ... |
| Error | ... | ... | ... |
| Replay | ... | ... | ... |

## PR/develop overlap verdict

- **Overlap:** none / partial / exact
- **Existing PRs/merges checked:** <links>
- **Decision:** new isolated PR / amend existing thread / trim scope to net-new

## Next developer checks

(Source-area guidance, not implementation. Don't prescribe code unless explicitly asked.)

- <area to investigate>
- <next experiment>

## Non-reproduced or failed-attempt notes

- <attempt> — <why it didn't confirm>
- <attempt> — <why it didn't confirm>
```

## Notes

- **Plain language first; raw IDs in parentheses.**
- **Plain file paths for local artifacts; clickable URLs only for web resources.**
- **Default attribution wording: "unknown (not tracked)" unless confirmed.**
- **Confidence stated explicitly per hypothesis.**

## Used by

- `evidence` mode of `dev-investigate`.
