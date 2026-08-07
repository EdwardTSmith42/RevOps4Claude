# Output format contract

The cluster-wide output formatting rules. Reflects the user's `AGENTS.md` preferences. Used by every mode that produces user-facing output.

## The contract

### Plain language first, technical detail second

Lead with what the user/business cares about:
- ✅ "Estimate line items disappear after extraction completes for some users."
- ❌ "ImportPipeline.normalizePayload returns null when key prefix doesn't match `org_*` regex pattern."

The plain-language description anchors the reader; technical detail follows for those who need it.

### Lead with plain-language descriptors first; raw IDs secondary

When referencing tasks, PRs, conversations:
- ✅ "Update on the duplicate-charge bug ([TASK-123](https://your-tracker/task/123))"
- ❌ "Update on TASK-123"

Plain language first (what is this?), IDs in parentheses (the lookup hook).

### Plain file paths for local artifacts; clickable URLs only for web resources

- **Local artifacts** in chat / handoff output: plain file paths.
  - ✅ `/tmp/investigations/2026-04-26/report.md`
  - ❌ `[report.md](file:///tmp/investigations/2026-04-26/report.md)` (broken in non-local contexts; can leak paths)

- **Web resources** (task-tracker entries, PRs, error-monitoring issues, support conversations): clickable links with descriptive text.
  - ✅ `[apps#33297](https://github.com/org/repo/pull/33297)`
  - ❌ Bare PR number `apps#33297` without link
  - ❌ Just the URL without descriptive text

This rule applies to PR descriptions and task-tracker posts especially: do NOT link to a local file path outside of local chat — paths are user-system-specific and won't open for anyone else.

### User-attribution wording

See `user-attribution-rule.md`. Default: `Affected Users: unknown (not tracked)` unless tracking is explicitly confirmed.

### Confidence stated explicitly

Hypotheses carry confidence (`low` / `medium` / `high` per `status-vocabulary.md`). Don't claim 100% certainty. Use `abstain` when evidence is genuinely incomplete.

### What this cannot be — explicitly

Per `atomic-hypothesis-method.md`, the "what this cannot be" bucket is part of the standard output. It forces explicit assumption statement and lets future investigators avoid re-walking dead-ends.

### Avoid generic AI tells

- No leading "I'd be happy to help with…"
- No closing "Let me know if you have any questions!"
- No emoji unless explicitly requested.
- No "Here's a comprehensive breakdown of…" framing.
- Direct, factual, lead-with-substance.

## Used by

Every mode of `dev-investigate`. Every standalone skill spawned from this cluster (`dev-fresh-eyes`, `dev-scope-deferral`, and any cross-system bug-comms workflow you maintain that consumes investigation output).

## Malleability note

**Canonical:** the rules above. They reflect the user's `AGENTS.md` preferences and are non-negotiable.

**Adaptable:** the rendering specifics (e.g., bullet vs. table vs. headed sections). The format adapts to context; the rules apply uniformly.

