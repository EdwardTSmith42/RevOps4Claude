# Brief authoring standard

The discipline for change-context briefs and reviewer-facing PR bodies. Used by `brief` mode and (cross-load) by `digest` mode for per-PR brief shape.

## Core principles

- **Plain language first, technical detail second.** Lead with what the user / business / reviewer cares about; raw IDs and signatures secondary.
- **AI-authored reviewer guidance is the main artifact.** Don't reverse-generate from filenames; tell the story. The script (or your harness's deterministic fallback) stitches it together — it does not invent the whole story from filenames.
- **Write for a reviewer who wants to trust the change quickly.** Explain what patterns stayed the same in risky areas. Explain what changed intentionally and why. Use file notes to point reviewers to real entry points, not every file in the diff.

## Required sections (PR scope)

Generated PR body shape, in order:

1. **`## Summary`** first. Lead with user-facing bug fixes (bullets) for bug-fix PRs; lead with feature outcome for feature PRs.
2. **Reviewer-facing narrative sections:**
   - `## Big Picture` — the change framed as a story
   - `## File By File` — curated, grouped, human-oriented (doesn't need to cover every file on large PRs)
   - `## How It Works` — the mechanics
   - `## Patterns Kept vs Changed` — preserved boundaries and intentional changes in plain English (no link dumps)
   - `## One Important Mental Model` — the conceptual change a reviewer needs to hold in their head
3. **Deterministic reviewer support sections:**
   - `## Changed Files`
   - `## Critical Files`
   - `## Tests`
   - `## Blast Radius`
   - `## Contracts`
   - `## Verification`

For higher-fidelity briefs, author these directly (the body builder will prefer them over generic fallbacks):

- `## Reviewer Summary`
- `## Reviewer Guide` — where to start; few files that carry the story; what each file proves; group supporting files when the diff is broad
- `## Big Picture`
- `## Why This Shape`
- `## How It Works`
- `## Patterns Preserved`
- `## Patterns Changed`
- `## Verification`
- `## Mental Model`
- `## File Notes` — bullets like `- <path>/<file>.ts: explain why this file matters to the review`

## Required content

- **Briefs must include `Plain-Language Fix`** for bug fixes, written for someone new to the codebase.
- **Briefs must include concrete bug context evidence** via at least one of:
  - `Evidence / Error Data` — error-reporting system / log / API snippets with links
  - `Verbatim Signals` — quoted user / customer / internal statements
- **Bug-fix PRs** should include one or more `--fix-bullet` entries so the PR summary opens with plain-language user-facing bullets describing each regression/fix.
- **Feature PRs** should start `## Summary` with a human explanation of the outcome and code shape, not bookkeeping bullets.
- **Bug-fix PRs with `User-Facing Bug Fixes`** should still start `## Summary` with those bullets first, written in plain language from the user-experience perspective.
- **Medium/high-risk branches** add extra brief and PR-body sections: `## Risk / Blast Radius`, `## Rollout / Rollback`, `## Monitoring`, `## Open Questions`.

## Format rules

- **Clickable GitHub links for touched files**: `pull/<number>/files#diff-...`. For new PR creation, regenerate links post-create using actual file diffs.
- **File labels:** prefer file basename or shortest unique suffix (`<ComponentName>/index.tsx`), not full repo path.
- **`## Reviewer Guide` should tell the reviewer where to start.** Prefer the few files that carry the story of the change. Tell the reviewer what each file proves or why it matters. When a diff is broad, mention supporting files as a group instead of listing every path.
- **`## File By File`:** curated, grouped, human-oriented. Doesn't need to cover every file on large PRs.
- **`## Patterns Kept vs Changed`:** explain preserved boundaries and intentional changes in plain English. Do not dump long link lists or restate file paths when the architecture can be explained more clearly with bullets.

## User-attribution wording

For error-reporting-derived impact lines: cross-reference `../../dev-investigate/references/user-attribution-rule.md`.
- **Never** write `0 affected users` unless attribution tracking is explicitly confirmed.
- If attribution is unknown/unreliable, use `Affected Users: unknown (not tracked)` and optionally provide `attributed users` as a separate metric.

## Brief location and lifecycle

- **Brief files live at** `<repo>/docs/change-briefs/open/<branch-slug>.md`.
- **Brief files are branch-scoped context/explainer docs**, not the canonical list of active branches. (Cross-branch state lives in a separate registry the user maintains — e.g., a notes file or repo-specific equivalent.)
- If the user asks to "track" / "park" / "resume" / otherwise manage a branch in active branches, update the branch registry directly; do not overload the brief for that job.
- **`tasks/todo.md`** is auto-created if missing and linked to the brief.
- **Detail profile** is computed from real diff stats and touched risk markers (auto by default).
- **Authored explainer sections are preserved on rerun** — reviewer-oriented writing does not get wiped out when the brief is regenerated.
- **Brief stays local by default.** Do not emit a `Context brief` line into the GitHub PR body unless the brief itself is intentionally committed and reviewable on GitHub.

## Backwards compatibility

- Keep `## Existing Code Reused` and `## New Code / Added` only for backwards compatibility when older briefs already use them. Don't add to new briefs.

## Validation rules

- **Validation blocks meta/boilerplate content** (e.g., "this branch needs a brief") and TODO placeholders in required sections.
- **`init-brief` and `create-pr` refuse protected branches** (`develop`, `main`, etc.) unless `--allow-protected-branch` is explicitly passed.
- **PR creation belongs to `dev-PR`** — its pre-open checklist (`../../dev-PR/references/cycle-checklist.md`) is the required gate; blocks opening a PR until out-loud confirmation flags are provided. See `pre-open-checklist.md`.

## Lockfile discipline

- **Default:** no lockfiles in PR (`yarn.lock`, `uv.lock`, etc.).
- **If lockfiles are changed:** pre-open requires explicit `--confirm-lockfiles-required` confirmation.

## PR-author scoping

- **If an open PR on the branch is authored by someone else, enforcement is skipped by default** (`--only-my-prs` default true). Don't mutate non-personal PRs.

## Used by

- `brief` mode of `dev-review` (primary consumer)
- `digest` mode of `dev-review` (cross-loads for per-PR brief shape)

## Malleability note

**Canonical:** the section ordering (Summary first, reviewer-facing narrative, then deterministic reviewer support); the user-attribution rule; the lockfile discipline; the protected-branch refusal; the brief-stays-local default; the requirements for bug-fix briefs (`Plain-Language Fix` + concrete evidence).

**Adaptable:** the specific sub-sections to author for higher fidelity (Reviewer Summary / Reviewer Guide / Big Picture / etc.) — these are options, not requirements. The sub-section names can also vary per repo convention as long as the principle (curated, reviewer-oriented, AI-authored narrative) holds.

