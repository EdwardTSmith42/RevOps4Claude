# Deferred-investigation note template

Strict structure for the deferred-investigation note. Lives at your workspace's deferred-investigation path (e.g., `os-inputs/_os-deferred-investigations/<date>-<slug>.md`).

```markdown
# <Plain-language title of the deferred improvement>

**Date:** <YYYY-MM-DD>
**Source context:** <what was being worked on when this surfaced — PR title, branch, investigation slug, or "fresh-eyes review of <plan>">
**Current scope:** <what ships now>

## Problem statement

<What's the underlying issue or improvement opportunity? Concrete, specific.>

## Remaining fragility

<After the current change ships, what's still fragile? What conditions still produce buggy or suboptimal behavior?>

## Proposed design

<How would the deferred work be done? Sketch the approach, not the full implementation. One or two paragraphs.>

## Risks

<What could go wrong with the deferred work itself? Blast radius, review risk, timing pressure, dependency cost.>

## Non-goals

<What's explicitly out of scope for the deferred work? (Helps a future investigator avoid scope creep.)>

## Executable verification idea

<The specific check, test, scenario, or experiment that would prove the deferred work succeeded. Executable means: someone can run it and get a yes/no answer. Not "we should make sure this works" — that's a wish, not verification.>

## Cross-references

- **Repo backlog pointer:** <path / line in tasks/todo.md or equivalent, if added>
- **Related artifacts:** <links / paths>
```

## How to use

1. Fill every section. Empty sections are fine to skip if explicitly N/A; "TBD" sections suggest the deferral isn't ready to defer.
2. The **Executable verification idea** is the highest-leverage section. If you can't articulate the verification, the deferred work isn't concrete enough to defer — keep investigating until it is.
3. Cross-link from the relevant skills' outputs (investigate handoff package, fresh-eyes recommendations) to this note path.

## Used by

- `dev-scope-deferral` standalone skill.
