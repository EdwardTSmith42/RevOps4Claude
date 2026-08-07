# Smoke-QA report template

Output shape for `smoke-qa` mode. Lives at `.local/check-smoke-qa/<timestamp>/report.md` (sandbox-safe path; not committed).

```markdown
# Smoke QA Report — <branch / scope>

**Date:** <UTC timestamp>
**Scope:** <branch / commit / PR>
**Baseline:** <ref>
**Base URL:** <http://localhost:3000 / https://staging.example.com / etc.>

## Routes inferred
<Routes likely affected by the diff, derived from changed file paths + routing config parsing.>

- <route 1>
- <route 2>
- ...

## Routes visited
<Routes actually visited by browser-use.>

## Per-route evidence

### <route 1>
- **Final URL** (post-redirect): <url>
- **HTTP status** (if available): <200/4xx/5xx>
- **Page title:** <title>
- **Body text preview:** <first ~500 chars>
- **Interactive elements snapshot:** <buttons / links / inputs visible>
- **Screenshot:** `<screenshot path>`
- **Errors / friction signals:** <console errors / blank pages / timeouts / rage-click candidates>

### <route 2>
...

## Summary
- **Passed** (loaded, no errors): <count>
- **Errored** (4xx/5xx/JS errors/blank): <count>
- **Blocked** (auth required / didn't load): <count>
- **Inferred but not visited** (skipped due to time/scope): <count>

## Follow-ups
- <route or issue> — <reason it needs manual verification or follow-up>
- (Captured via `dev-scope-deferral` skill if any need deferred work.)

## Notes
- Route inference is heuristic; false positives and negatives are possible.
- This is smoke/regression-oriented, not a replacement for E2E.
- `browser-use` doesn't expose rich console/network logs — this report focuses on route coverage, redirect detection, screenshots, and empty-page signals.
```

## Used by

- `smoke-qa` mode of `dev-review`.
