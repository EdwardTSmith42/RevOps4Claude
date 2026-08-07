# Dream Mode

Dream mode consolidates branch memory notes into final reviewer-ready context near PR time.

## Inputs

Read:

- `manifest.json`
- `branch.md`
- all `memories/*.md`
- current `git status --short`
- current `git diff --stat`
- existing PR/change brief if the repo already uses one

Do not read raw transcripts by default. Branch memory is the curated input.

## Reconciliation Rules

- Merge duplicate notes into one final narrative.
- Preserve superseded decisions when they explain the final shape.
- Mark unresolved uncertainty instead of pretending the branch is cleaner than it is.
- Keep deferred follow-ups separate from shipped behavior.
- Cite durable sources that shaped decisions, but do not copy private SOP content into PR-safe outputs.
- Convert relative dates to absolute dates.
- Prefer concise reviewer context over chronological exhaustiveness.

## Outputs

Write:

```text
dream/final-branch-memory.md
dream/reviewer-brief-input.md
dream/deferred-followups.md
```

`final-branch-memory.md` is local/private. It can mention private source paths.

`reviewer-brief-input.md` must be PR-safe. Do not include private local file paths, private SOP text, secrets, or private customer data. It should be suitable as source material for your PR-brief workflow (e.g., `dev-PR` if installed), not necessarily pasted verbatim.

`deferred-followups.md` records valid improvements outside the current PR scope. If the repo has a backlog process, include the recommended backlog pointer text separately.

## Final Branch Memory Shape

```markdown
# Final Branch Memory

## Branch Outcome

## Key Decisions

## Why This Shape

## Patterns Preserved

## Patterns Changed

## Superseded Approaches

## Source Trace

## Verification Evidence

## Residual Risk

## Deferred Follow-ups
```

## Reviewer Brief Input Shape

```markdown
# Reviewer Brief Input

## Reviewer Summary

## Why This Shape

## Patterns Preserved

## Patterns Changed

## Files / Areas To Review First

## Verification

## Residual Risk
```

After writing dream outputs, run:

```bash
python3 <skill-dir>/scripts/update_manifest.py --repo "$PWD"
```
