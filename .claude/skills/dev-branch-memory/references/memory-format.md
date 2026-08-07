# Branch Memory Format

Branch memory files are Obsidian-friendly markdown files with YAML frontmatter.

## Directory Layout

```text
branch.md
manifest.json
memories/YYYY-MM-DDTHHMMSSZ-<kind>-<slug>.md
dream/final-branch-memory.md
dream/reviewer-brief-input.md
dream/deferred-followups.md
```

## Memory Frontmatter

Required fields:

```yaml
---
type: branch-memory
repo: repo-key
branch: branch-name
thread_id: unknown
created_at: 2026-04-28T17:45:00Z
updated_at: 2026-04-28T17:45:00Z
status: active
memory_kind: architecture-decision
confidence: provisional
summary: "One-line summary"
tags: []
related_files: []
source_refs: []
supersedes: []
---
```

Allowed `status` values:

- `active`: still relevant to current branch direction
- `superseded`: useful historical context, but no longer the chosen path
- `final`: reconciled into final branch memory
- `deferred`: valid follow-up intentionally outside current branch
- `promoted`: proposed or moved into a durable memory/SOP surface

Allowed `confidence` values:

- `unknown`: context is worth preserving, but evidence is incomplete or not yet inspected
- `provisional`: planned or directionally chosen, but not yet implemented or exercised
- `supported`: implemented and supported by code/tests/review evidence, with some acceptance/runtime proof still open
- `verified`: the specific decision has direct proof, not just a passing build or unrelated test suite
- `reversed`: explicitly undone or proved wrong, retained for historical context

Suggested `memory_kind` values:

- `architecture-decision`
- `refactor`
- `contract`
- `source-of-truth`
- `risk`
- `verification`
- `temporary-instrumentation`
- `deferred-followup`
- `pattern-preserved`
- `pattern-changed`
- `reviewer-context`

## Body Sections

Use only sections that carry signal. Start with a plain-language `TL;DR: ...` before the first heading. Prefer this order:

```markdown
TL;DR: One sentence explaining the decision and why it matters.

# Memory

## Current Decision

## Decision Arc

## Human Input That Moved It

## Why It Came Up

## What Changed In Code

## Options Considered

## Routes Not Taken

## Existing Patterns Preserved

## Patterns Changed

## Risk / Invariant

## Evidence So Far

## Source Trace

## Open Questions

## Reviewer Relevance
```

`Risk / Invariant` is expected for `contract`, `source-of-truth`, `risk`, and other safety-sensitive memory kinds. It should say what future changes must preserve or avoid.

`Decision Arc`, `Human Input That Moved It`, `Options Considered`, and `Routes Not Taken` are expected when a memory captures planning, architecture, source-of-truth, tool-contract, or UX decisions reached through discussion. These sections should explain the path to the decision in reviewer-readable language. They should not paste long transcript excerpts or expose hidden internal reasoning.

## Branch Index

`branch.md` is a human-readable branch index. Keep it short and do not duplicate the full deterministic inventory from `manifest.json`. It should make it obvious that branch memories exist and highlight only the most useful current context.

```markdown
# Branch Memory: <branch>

## Purpose

## Current State

## Important Memories

- Latest/highest-signal memory summary, if useful
- Another high-signal memory summary, if useful

## Dream Outputs

## Open Questions
```

The deterministic source of file inventory is `manifest.json`, not `branch.md`. Updating `branch.md` after capture is optional, but if memories exist it should not imply the branch has no memory.
