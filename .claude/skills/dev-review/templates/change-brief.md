# Change brief template

The per-branch context brief structure used by `brief` mode. Lives at `<repo>/docs/change-briefs/open/<branch-slug>.md` (PR scope) or appropriate path for non-PR scopes.

## Profile-aware structure

The brief structure adapts based on profile (per `brief` mode body):
- **Profile A** (small bug-fix commit): minimal sections.
- **Profile B** (medium change): standard reviewer-facing sections.
- **Profile C** (large change): + architectural / design / manifesto sections.

## Profile A (small bug-fix commit)

```markdown
# Brief — <branch slug or commit subject>

**Scope:** Single commit / small bug fix
**Date:** <YYYY-MM-DD>

## Bug summary
<One sentence.>

## Root cause
<Technical: where the bug originated, why it happened.>

## User story affected
<In the user's voice.>

## Evidence
- <link to error-reporting system / log / API snippet>
OR
> <verbatim signal: quoted user/customer/internal statement>

## Fix shape
<What changed, why this shape over alternatives.>

## Verification
<How proven.>

## Plain-Language Fix
<One or two sentences for someone new to the codebase.>

## Affected Users
<count if confirmed; otherwise "unknown (not tracked)">
```

## Profile B (medium change)

```markdown
# Brief — <branch-slug>

**Scope:** Medium change (5-20 files / 100-500 lines)
**Branch:** <name>
**Base:** <baseline ref>
**Date:** <YYYY-MM-DD>

## Why
<Why this work is needed now.>

## Bug / Feature
<What problem this addresses or what outcome users should expect.>

## Evidence / Verbatim Signals
- <evidence link or quoted signal>

## Plain-Language Fix (for bug fixes)
<One or two sentences for someone new to the codebase.>

## Reviewer Summary
<For someone who wants to trust this change quickly.>

## Reviewer Guide
- <file basename>: <what this file proves; why it matters>
- ...
- (Group supporting files when broad.)

## Big Picture
<The change as a story.>

## How It Works
<The mechanics, clearly enough that a reviewer can trace the chain.>

## Patterns Kept vs Changed
**Kept:**
- ...

**Changed:**
- ...

## File Notes
- <path>: <why this file matters to the review>
- ...

## Verification
<What proves it works.>

## Affected Users
<count if confirmed; otherwise "unknown (not tracked)">
```

## Profile C (large change)

Add to Profile B sections:

```markdown
## Big Picture (extended for large change)
<Includes architectural decisions: what design was chosen and why.>

## Why This Shape
<Design decisions: state model, error path strategy, canonical utilities used, scope-focused boundaries.>

## Mental Model
<The conceptual change a reviewer needs to hold in their head.>

## Risk / Blast Radius
<What this change affects; level of risk.>

## Rollout / Rollback
<How to deploy + roll back.>

## Monitoring
<What signals will tell us if this regresses.>

## Open Questions
<Acknowledged but not yet resolved.>

## Manifesto Evaluation
<Cross-load `references/agentic-coding-manifesto.md`. Does this change:
- Clarify or obscure source-of-truth?
- Introduce or reduce implicit state / scattered policy / unnamed shapes?
- Preserve or improve testable contracts at boundaries?
- Leave honest gap tracking for any deferred work?
Surface findings if the change introduces ambiguity that the manifesto would flag.>
```

## Backwards-compatibility sections (older briefs only)

```markdown
## Existing Code Reused
<For older briefs only; don't add to new briefs.>

## New Code / Added
<For older briefs only.>
```

## Notes

- Brief stays local; do not emit `Context brief` line into the GitHub PR body unless the brief is intentionally committed.
- Authored explainer sections are preserved on rerun.
- Validation rejects boilerplate placeholders.

## Used by

- `brief` mode of `dev-review`.
