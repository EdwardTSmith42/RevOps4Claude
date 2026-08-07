# PR body skeleton

Reviewer-facing narrative first, deterministic support sections second. AI-authored sections from the brief replace these placeholders verbatim — these are scaffolding, not target text.

```markdown
## Summary

<bug-fix: lead with User-Facing Bug Fixes bullets in plain language from user-experience perspective>
<feature/infra: lead with outcome + code-shape decision; then 1-3 supporting points>

---

## Big Picture

<before / after explanation with clickable file links>

## File By File

<curated, grouped, human-oriented; each entry says what the file proves or why it matters; not a dump of every file>

- [<short-label>](<file-link>): <what this file does for the change>
- [<short-label>](<file-link>): <what contract this owns>

## How It Works

1. <ordered step in mechanism>
2. <state ownership / error path / lifecycle>
3. <integration boundaries>

## Patterns Kept vs Changed

**Kept:**
- <familiar architecture / contracts / utilities preserved>

**Changed:**
- <responsibility moved / tightened / made explicit>

## One Important Mental Model

<one framing idea that makes the diff easier to read>

---

## Changed Files

<deterministic list with clickable links — supports the narrative; not the main artifact>

## Critical Files

<files that own contracts or invariants; reviewer must understand these>

## Tests

<what each test proves; only mention tests that prove a specific edge or invariant>

## Blast Radius

<what this could affect; what's verified vs. trusted>

## Contracts

<API / data shape / behavioral contracts touched by this PR>

## Verification

<what proof exists: tests pass, scenario tested in browser, regression added, etc.>
```

## Section ordering rationale

- **Summary first** — readers skim it. Lead with impact (bugs) or outcome (features), not metadata.
- **Reviewer-facing narrative second** (`Big Picture`, `File By File`, `How It Works`, `Patterns Kept vs Changed`, `One Important Mental Model`) — this is the prose that actually orients the reviewer.
- **Deterministic support sections last** (`Changed Files`, `Critical Files`, `Tests`, `Blast Radius`, `Contracts`, `Verification`) — they support the narrative, they don't replace it.

## File-link format

- For an existing PR: links target `pull/<number>/files#diff-<sha>` so reviewers land in the correct PR diff context.
- For a new PR: do a second post-create body refresh after `gh pr create` returns the PR number, so the final body uses real `Files changed` anchors.
- Labels should be the file basename or shortest unique suffix (`AiProvider/index.tsx`, not the full repo path).

## Backwards-compatibility sections

Keep these only when older briefs already use them:
- `## Existing Code Reused`
- `## New Code / Added`

For new briefs, prefer the curated `## File By File` and `## Patterns Kept vs Changed` shape.
