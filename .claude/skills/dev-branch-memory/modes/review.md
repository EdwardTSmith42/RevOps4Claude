# Review Mode

Review mode inspects branch memory quality without changing implementation code.

## Review Checks

- Does every significant decision have a memory note?
- Are memory states accurate (`active`, `superseded`, `deferred`, etc.)?
- Are source references present when durable instructions shaped decisions?
- Are private sources kept out of PR-safe outputs?
- Are provisional notes resolved or explicitly carried as uncertainty?
- Are deferred follow-ups concrete enough to act on later?
- Does reviewer context explain what the diff alone cannot?

## Output Shape

Use this shape:

```markdown
## Branch Memory Health

## Missing Context

## Contradictions / Superseded Notes

## Source Trace Gaps

## PR-Safety Issues

## Recommended Fixes
```

Do not create or edit memories in review mode unless the user explicitly asks.
