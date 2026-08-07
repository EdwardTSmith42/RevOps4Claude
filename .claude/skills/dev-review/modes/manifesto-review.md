# Mode: manifesto-review

Part of the `dev-review` skill. Selected when the user wants a manifesto-guided review for legibility / navigability / trust — phrasings like "Run a manifesto review," "Make this codebase easier to navigate," "Review for collaboration legibility," "Pressure-test against the agentic coding practices."

## Job

Review a code area against the Agentic Coding Practices manifesto. Reconstruct the trust layer, identify a small set of changes that reduce ambiguity (rather than stylistic churn), surface 3-5 high-signal recommendations with rationale, implement only the approved subset.

## Scope adaptation

Per `../references/scope-adapter.md`, `manifesto-review` works at any scope:
- **File / files / directory:** review the named area.
- **Branch / commit / PR:** review the changed surface (use `git diff --stat` to identify scope).
- **Existing slice (no diff):** valid — review code that is risky, old, or confusing even without a fresh diff.

This mode is review-first. Implementation only happens on the approved subset; never auto-implements without explicit user approval.

## Run

### 1. Reconstruct the trust layer

Figure out the minimum map someone needs to work safely in the slice. See `../references/agentic-coding-manifesto.md` for the full rubric.

- What is canonical vs derived vs legacy?
- Which files or services own the behavior?
- How is the code supposed to be run and verified?
- Which contracts or invariants already exist?
- Which known gaps are already documented, and which are only implied?

Prefer reading boundaries over internals first: entry points, exported types, serializers, schemas, docs, tests, CLI surfaces, integration seams.

### 2. Look for manifesto-aligned improvement opportunities

Bias toward improvements that **reduce ambiguity rather than stylistic churn.** Good targets:

- Missing or stale source-of-truth cues
- Implicit state or policy hidden in scattered conditionals
- Unnamed data shapes that should be a type, enum, state, policy, or error class
- Boundary code lacking one clarifying contract comment
- Critical interfaces without a focused contract test
- Docs or generated artifacts that look authoritative but are stale, duplicate, or unowned
- Missing honest gap tracking around known limitations, rollout constraints, or deferred behavior

**Avoid broad rewrites unless the user asks for them.** Prefer the smallest change that improves navigation, ownership, or verification confidence.

### 3. Produce a short recommendation set

**Recommend at most 3-5 improvements in the first pass.** For each one, state:

- What to change.
- Why it reduces uncertainty.
- Which manifesto idea it supports (tie back to `../references/agentic-coding-manifesto.md`).
- Scope and risk.
- Whether it should be implemented now or deferred.

**If the code is already clear enough, say that plainly and explain why no change is worth the churn.**

Tie each recommendation back to the manifesto in a sentence, not a slogan.

### 4. Wait for approval before implementation

Do not implement immediately unless the user explicitly asked for changes in the same request. When approval is required, ask for it after presenting the recommendation set.

If the user approves some but not all items, implement only the approved subset.

### 5. Implementation rules (when approved)

- Keep changes tightly scoped to the reviewed slice.
- Prefer existing patterns over new abstractions.
- Favor named contracts, ownership cues, boundary comments, and focused tests over sweeping reorganization.
- Update stale docs or generated artifacts only when they are part of the changed truth surface.
- **Do not inflate the change with unrelated cleanup.**

Good implementation examples:

- Extracting an implicit status string union into a named type.
- Adding one authoritative subsystem note that points to the real entry points and verification path.
- Replacing repeated raw object-shape assumptions with a shared helper or contract.
- Adding one focused contract test around a prompt/tool/API/config boundary.
- Recording a known limitation explicitly where future readers will hit it.

### 6. Verification

Match proof to risk:

- **Review-only requests:** cite concrete file evidence for each recommendation.
- **Small code changes:** run targeted tests or typechecks for the touched surface.
- **Contract or boundary changes:** add or run focused contract tests where practical.

In the closeout, separate:
- Implemented improvements
- Deferred improvements (invoke `dev-scope-deferral` for each)
- Remaining uncertainty or gaps

## Output

See `../templates/manifesto-review-output.md`. Use plain language; keep first pass easy to scan:

1. **Scope reviewed**
2. **Findings and proposed improvements** (3-5 max)
3. **Approval checkpoint or implementation summary**
4. **Verification**

## Mode-specific references

- `../references/agentic-coding-manifesto.md` (the rubric itself)
- `../references/scope-adapter.md` (scope decisions for any-size review)
- `../templates/manifesto-review-output.md`

Cross-mode use:
- `brief` mode at large scope cross-loads `agentic-coding-manifesto.md` for documentation/readability evaluation criteria. Two-skill threshold met inside cluster.

## Design Rationale

Mode-specific notes:

- **"Improvements that reduce ambiguity rather than stylistic churn"** — explicit anti-bikeshed rule. The manifesto's core principle.
- **"3-5 improvements max in the first pass"** — bounded count (similar to mutation-scout's 3-8). Prevents brainstorm-list output.
- **"If the code is already clear enough, say that plainly"** — explicit-affirmation move (same pattern as fresh-eyes). Prevents critique-for-critique's-sake.
- **"Tie each recommendation back to the manifesto in a sentence, not a slogan"** — anti-slogan rule. Forces concrete grounding.
- **Wait-for-approval discipline** — review-first, implementation-only-on-approved-subset. Prevents the LLM-failure-mode of "I'll just go ahead and refactor while I'm here."
- **"Prefer reading boundaries over internals first"** — entry-points-and-contracts-first reading order. Same principle as the Agentic manifesto's "Put comments at boundaries and contracts, not on obvious lines of code."

