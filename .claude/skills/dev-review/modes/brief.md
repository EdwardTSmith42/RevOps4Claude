# Mode: brief

Part of the `dev-review` skill. Selected when the user wants to produce or sync a change-context brief — phrasings like "Build me a context brief for this change," "Document this change," "Summarize what I've been working on." **Everything PR-shaped is `dev-PR`'s territory, not this mode's**: "write the PR body," "open a PR," the pre-open checklist, and PR creation all route to `dev-PR`, which owns the brief-to-PR-body pipeline end to end. This mode covers briefs that are *not* destined for a PR — milestone documentation, reviewer context for an unmerged change, a memory artifact for future sessions.

## Job

Produce a high-fidelity change-context brief that adapts across a wide range of scopes:
- **Small bug-fix commit** → technical-what + user-story-affected (lightweight)
- **Medium change** → reviewer-facing narrative (Big Picture / How It Works / Patterns Kept vs Changed / Reviewer Guide)
- **Large change** → all of the above + architectural decisions + design decisions + manifesto-criteria evaluation (documentation, readability, trust layer)

For PR-scope work, hand the brief to `dev-PR` — it renders the PR body and opens the PR. This mode may still (optionally) sync briefs to the `tasks/todo.md` repo-local backlog.

## Scope-adaptive profiles

The brief authoring shape depends on the change type AND scope. Three profiles:

### Profile A: Small bug-fix commit

For a single commit or tight commit-range that fixes a specific bug. The brief is tightly coupled to the technicals on what was happening + the user story being affected.

**Required sections:**
- **Bug summary** (one sentence: what was broken, who was affected)
- **Root cause** (technical: where the bug originated, why it happened)
- **User story affected** (in the user's voice: what the user experienced)
- **Fix shape** (what changed, why this shape over alternatives)
- **Verification** (how this fix was proven)
- **Plain-Language Fix** (one or two sentences explaining the fix for someone new to the codebase)

Skip: Big Picture / File By File / Architectural narrative (overkill for a small fix).

### Profile B: Medium change

For a feature, refactor, or fix that touches multiple files but doesn't reshape architecture. Standard reviewer-facing narrative.

**Required sections (the "good PR body shape" from pr-context-brief):**
- `## Summary` — what changed and why (lead with user-facing outcome for bug fixes; lead with feature outcome for features)
- `## Big Picture` — the change framed as a story
- `## How It Works` — the mechanics, clearly enough that a reviewer can trace the chain
- `## Patterns Kept vs Changed` — what stayed the same in risky areas, what changed intentionally and why
- `## Reviewer Guide` — where to start; few files that carry the story; what each file proves
- `## File By File` — curated, grouped, human-oriented (doesn't need to cover every file on larger changes)
- `## Verification` — what proves the change works
- `## Plain-Language Fix` (for bug fixes) — required even at this scope
- `## Affected Users` — `unknown (not tracked)` unless attribution is confirmed (cross-reference `../../dev-investigate/references/user-attribution-rule.md`)

### Profile C: Large change

For substantial features, multi-file refactors, architectural shifts, migration work. Adds to Profile B:

- `## Big Picture` extended with **architectural decisions** (what design was chosen and why)
- **Design decisions** section (state model, error path strategy, canonical utilities used, scope-focused boundaries)
- **One Important Mental Model** (the conceptual change a reviewer needs to hold in their head)
- **Risk / Blast Radius** section (medium/high-risk only)
- **Rollout / Rollback** section (medium/high-risk only)
- **Monitoring** section (what signals will tell us if this regresses)
- **Open Questions** section (acknowledged but not yet resolved)
- **Cross-load `agentic-coding-manifesto.md` rubric** for documentation/readability/trust-layer evaluation. Surface findings if the change introduces ambiguity that the manifesto would flag.

Per the user's articulation: "anything sufficiently large should also be evaluated against criteria like we have in our manifesto re: documentation, readability, etc."

## Run

### 1. Detect scope and pick profile

- Inspect: branch name, commit count in scope, diff size (`git diff --stat <base>...HEAD`), files touched, risk markers (lockfiles, schemas, contract files, generated artifacts).
- Pick profile A / B / C based on:
  - **A:** single commit OR explicitly a small bug fix; <5 files touched; <100 lines changed.
  - **B:** medium change; 5-20 files touched; 100-500 lines changed; OR feature work that doesn't reshape architecture.
  - **C:** >20 files touched OR >500 lines changed OR architectural shift OR migration work.
- These thresholds are heuristics, not hard rules — surface profile choice to the user if borderline.

### 2. Initialize or update the brief

Brief location: `<repo>/docs/change-briefs/open/<branch-slug>.md` (repo-local convention from pr-context-brief).

If brief doesn't exist: create with the profile-appropriate sections.
If brief exists: preserve authored explainer sections on rerun (don't wipe content the user wrote).

For PR-scope work, also link to `<repo>/tasks/todo.md` (repo-local backlog).

### 3. Author the brief content

Per `../references/brief-authoring-standard.md` (the ~30-rule discipline lifted from pr-context-brief):

- **Plain-language first, technical second.** Lead with what the user / business / reviewer cares about; raw IDs and signatures secondary.
- **AI-authored reviewer guidance is the main artifact.** Don't reverse-generate from filenames; tell the story.
- **Concrete bug context evidence required for bug fixes:** Evidence/Error Data (error-reporting system / log / API snippets with links) OR Verbatim Signals (quoted user/customer/internal statements).
- **File labels:** prefer basename or shortest unique suffix (`<ComponentName>/index.tsx`), not full repo path.
- **`## Reviewer Guide` tells the reviewer where to start.** Few files that carry the story; what each file proves; group supporting files when broad.
- **`## File By File` is curated, grouped, human-oriented.** Doesn't need to cover every file on large PRs.
- **`## Patterns Kept vs Changed` explains preserved boundaries and intentional changes in plain English.** No link dumps.
- **For error-reporting-derived impact:** never `0 affected users` without confirmed tracking; default `Affected Users: unknown (not tracked)`.
- **Validation rejects boilerplate / placeholder content** — no "this branch needs a brief," no TODO placeholders in required sections.
- **Brief stays local by default.** Don't emit `Context brief` line into the GitHub PR body unless intentionally committed.

For Profile C (large changes), additionally apply manifesto criteria from `../references/agentic-coding-manifesto.md`:
- Does the change clarify or obscure source-of-truth?
- Does it introduce or reduce implicit state / scattered policy / unnamed shapes?
- Does it preserve or improve testable contracts at boundaries?
- Does it leave honest gap tracking for any deferred work?

### 4. (PR scope) Build the PR body

Generated PR body shape:

```markdown
## Summary
<lead with user-facing bug fixes (bullets) for bug-fix PRs; lead with feature outcome for feature PRs>

## Big Picture
<the change framed as a story>

## How It Works
<the mechanics>

## Reviewer Guide
<where to start; few files that carry the story>

## File By File
<curated, grouped>

## Patterns Kept vs Changed
<plain English on preserved + intentional changes>

## Verification
<what proves it works>

## Changed Files
<deterministic list>

## Critical Files
<deterministic flag>

## Tests
<deterministic test summary>

## Blast Radius
<medium/high-risk only>

## Contracts
<deterministic contract impact>
```

Use clickable links for touched files: `pull/<num>/files#diff-<sha>` if open PR exists; deterministic fallback otherwise.

### 5. (PR scope) Pre-open checklist gate

If the work turns out to be PR-bound, stop here and hand off to `dev-PR` — its pre-open checklist (`../../dev-PR/references/cycle-checklist.md`) is the canonical gate:

- Confirm state model
- Confirm error path simple
- Confirm canonical utilities (no new abstractions where existing ones work)
- Confirm scope focused
- Confirm non-self audit (re-read the diff as if you didn't write it)
- Confirm out-loud checklist (each item answered, not skipped)
- Confirm lockfiles required (default no lockfiles in PR; explicit confirm if changed)

Block opening the PR until all confirmations are explicit.

### 6. Refuse protected branches

`init-brief` and `create-pr` refuse protected branches (`develop`, `main`, etc.) unless explicit override. Safety rule.

## Hard rules

- **Skip enforcement when open PR author isn't current `gh` user.** Don't mutate non-personal PRs.
- **Briefs must include `Plain-Language Fix`** for bug fixes, written for someone new to the codebase.
- **Briefs must include concrete bug context evidence** (Evidence/Error Data OR Verbatim Signals) for bug fixes.
- **No `0 affected users`** without confirmed tracking.
- **Default no lockfiles** in PR; explicit confirm if changed.
- **Validation blocks meta/boilerplate placeholders.**

## Mode-specific references

- `../references/brief-authoring-standard.md` (the core standard — ~30 rules)
- `../../dev-PR/references/cycle-checklist.md` (canonical pre-open gate, owned by dev-PR)
- `../references/scope-adapter.md` (scope detection for profile choice)
- `../references/agentic-coding-manifesto.md` (cross-loaded for Profile C large-change evaluation)
- `../templates/change-brief.md` (the brief structure)
- `../../dev-PR/templates/pr-body.md` (the PR body shape, owned by dev-PR)

Cross-cluster:
- `../../dev-investigate/references/user-attribution-rule.md` (Affected Users wording)
- `../../dev-investigate/references/output-format-contract.md` (plain-language-first / file paths / URLs)

## Output

Three artifacts depending on scope:

1. **Brief at `<repo>/docs/change-briefs/open/<branch-slug>.md`** — always.
2. **Hand-off to dev-PR** (when the work is PR-bound) — the brief is the input; dev-PR renders and opens.
3. **`tasks/todo.md` linkage** (when applicable) — adds or updates a line linking to the brief.

## Design Rationale

Mode-specific notes:

- **Three profiles (small / medium / large) instead of one-size-fits-all** — the brief should adapt across a wide range. Bug fix documentation is tightly coupled to the technicals of what was happening and the user story it affected. Larger code changes need to account for architectural decisions, design decisions, and other big-picture elements.
- **Manifesto cross-load for Profile C** — anything sufficiently large should also be evaluated against the manifesto's documentation/readability/trust-layer criteria. The manifesto reference becomes a Profile-C-only requirement; smaller changes don't need full manifesto evaluation.
- **AI-authored reviewer guidance is the main artifact** — pure-deterministic PR bodies become noise. The narrative is what reviewers actually use; the deterministic sections are support.
- **Brief stays local by default** — privacy / iteration. Only the PR body ships to GitHub; the brief stays in `docs/change-briefs/open/` for the author and AI agents.
- **Plain-Language Fix is mandatory for bug fixes** — written for someone new to the codebase. Anti-jargon discipline.
- **Pre-open checklist with out-loud confirmations** — the out-loud part forces the agent to actually verify each item rather than rubber-stamp. Same principle as investigate's "explicitly note contradictory evidence."
- **Don't emit `Context brief` line into GitHub PR body unless committed** — the brief is private context; don't link to a local file path from a public PR body.

