# The 4 mandatory PR-diff risk questions

The 4 questions that the `ship-gate` mode (and any check mode running ship-readiness analysis) must answer for every change. **Always all 4 — the discipline is forcing the enumeration.** When a question doesn't apply, the answer is "not applicable + reason" — never silently skipped.

## The questions

All 4 are always answered:

### Q1. What are the unintended consequences of these changes that could break all sorts of stuff?

The agent enumerates failure modes — what could go wrong that wasn't the intent of the change? Look for:
- Side effects on shared state
- Behavior changes in shared hooks (error handling, retries, null semantics)
- Inconsistent handling across similar modules
- Contract drift (types, transformer output shape, tool payload assumptions)
- UX drift (silent failure, false success toast, stale loading states)

Answer with diff evidence: file paths + line references. Not "I worry that..." — "<file>:<line> introduces X which could cause Y in <other file>:<line>."

### Q2. Are there any performance issues, memory leaks, race conditions, or other issues of that nature?

Specifically look for:
- Performance: N+1 queries, unbounded loops, missing indexes, inefficient algorithms.
- Memory leaks: unsubscribed event listeners, retained references, growing caches without eviction.
- Race conditions: async/await mistakes, shared mutable state, retry-without-idempotency, stale-state writes.
- Other: deadlocks, unbounded recursion, synchronization issues.

Answer with diff evidence. If none apply, say "No perf/memory/race concerns because <specific reason from the diff>."

### Q3. Is this PR overengineered? Are we making bad choices? Or are these common issues that just need a fine touch?

Judgment call grounded in diff size and complexity:
- Is the change scoped to the actual problem, or did it grow?
- Did the change introduce new abstractions that aren't yet earning their keep?
- Did it solve today's problem with tomorrow's architecture?
- Did it use existing repo patterns or reinvent them nearby?

Answer with rationale grounded in diff size/complexity. Not vibe — concrete: "The diff introduces 3 new abstractions for one new feature. Two of them have one consumer; the third has zero consumers outside the PR. Likely overengineered."

### Q4. Should we park any aspect of this (use scope-deferral) or revert back to original code in order to make it safer to ship?

Triage decision per finding:
- **Ship now** — safe enough as-is.
- **Park with investigation** — real concern but not required to ship; invoke `dev-scope-deferral` skill to capture as deferred-investigation note. Out of scope for this ship.
- **Revert risky slice** — unsafe and can't be hardened in current scope; remove or back out the risky change.

Answer must be explicit per finding (or per cluster of related findings). State the reason for each decision.

## Why all 4 are mandatory

**The discipline is forcing the enumeration.**

Without the mandatory framing, the agent skims and skips questions that "don't seem to apply." With the mandatory framing, the agent has to write down "Q2 not applicable: this is a string-formatting change with no async surface, so no perf/memory/race risk." That sentence is *cheap* to write but valuable as evidence: it proves the agent considered Q2, not just that Q2 felt irrelevant.

Even when the answer is "not applicable," the *reason* is captured. Future investigators can re-evaluate if context changes.

## Format

For ship-gate output, present the 4 questions as a section:

```markdown
## PR-Diff Risk Questions

**Q1 unintended consequences:** <answer + changed-file evidence, or "not applicable: <reason>">

**Q2 perf/memory/race:** <answer + changed-file evidence, or "not applicable: <reason>">

**Q3 overengineering judgment:** <answer + rationale grounded in diff size/complexity>

**Q4 park-or-revert decision:** Ship now / Park with investigation (via `dev-scope-deferral` skill) / Revert risky slice + reason
```

## Used by

- `ship-gate` mode — these 4 are mandatory for every ship-gate run

Could also be useful in `checkpoint` mode for the regression review step, though `checkpoint`'s focus is more on regression/decomp/cleanup than ship-readiness. Cross-load only if the user requests "run the ship questions on this checkpoint."

## Malleability note

**Canonical:** all 4 questions are always answered (no skipping). The wording is preserved verbatim (these are exactly the questions from the source).

**Adaptable:** the *order* of questions — the source has them in this order; the order helps the agent build context (consequences first, then specific risk types, then judgment, then triage). Don't reorder without reason.

