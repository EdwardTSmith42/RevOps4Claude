# Mode: coverage

Diff-aware trust assessment. Answer: **"Do we trust the proof on what changed?"**

This mode runs after a diff exists and tests exist (your tests, someone else's tests, or a mix). It maps changed code to behaviors and contracts, inventories direct and indirect proof, flags misleading tests, and recommends the smallest next proof.

This is **not** whole-repo coverage ratcheting. Diff-aware only.

## When to use

- The user asks about changed-code coverage, trust, or "is this enough proof?"
- Tests exist but their value is unclear.
- A release-ready / ship-gate decision needs a diff-aware trust summary.
- Pressure-testing existing tests before declaring something done.

## Default outputs

- `Changed surface map` — what behaviors / contracts changed
- `Trust verdict by changed behavior` — per-behavior verdict from the rubric
- `Production-executed but unproved path` — code that runs in prod but has no proof
- `Highest-risk unproved path` — the priority next proof
- `Misleading proof to ignore` — tests that pass for the wrong reasons
- `Smallest next proof` — the cheapest move that meaningfully improves trust
- `Why to trust this` — the summary statement

## Workflow

### 1. Classify

`work_type`, `risk_level`, `surface` — same as `strategy` mode.

### 2. Read the diff as behavior

Don't read the diff as files. Read it as:
- **Ingress guards** — auth, validation, rate limits
- **State mutation** — writes, transitions
- **Read paths** — query patterns
- **Side effects** — emits, notifications, external calls
- **Fallbacks** — error handling, retries
- **Contracts** — API shapes, event schemas

### 3. Inventory proof tied to the changed surface

For each changed behavior, find:
- Direct tests (file:test name)
- Indirect tests (E2E that crosses this behavior incidentally)
- CI / build guards
- Production observability (logs, metrics, alerts)

### 4. Grade trust per behavior

Use the rubric (`references/trust-rubric.md`):

| Verdict | When |
|---|---|
| **`verified`** | Direct test exercises the behavior, includes disconfirming check or fail-first proof |
| **`adequate`** | Test crosses the behavior with reasonable assertions, risk-appropriate |
| **`heuristic`** | Tests exist but exercise neighboring behavior or assert weakly |
| **`unknown`** | Behavior not covered by visible tests; needs investigation |
| **`misleading`** | Tests pass for the wrong reasons (snapshot-only on a stateful change, mock-heavy on a contract change, no-op suite, etc.) |
| **`quarantined`** | Tests exist but are skipped, flaky, or stale |

### 5. Name the smallest missing proof

Of the `unknown` and `misleading` paths, identify:
- Which is **highest risk**?
- What's the **smallest move** that changes its verdict to `verified` or `adequate`?

Don't recommend "more tests." Recommend the *one* test (or one rewrite) that moves the riskiest unproved behavior up the rubric.

### 6. Route to adjacent skills

- **`dev-investigate mutation-scout`** — pressure-test the existing tests with mutations to confirm they actually catch realistic mistakes.
- **`design` mode** — design the smallest next proof.
- **`dev-scope-deferral`** — for `unknown`/`misleading` paths that are real but out of scope for the current change.

## Use this mode when

- The user asks about changed-code coverage, trust, or "is this enough proof?"
- Tests exist but their value is unclear.
- A release-ready answer needs a diff-aware trust summary.
- After CI shows green and you want to know if green actually means anything.

## Do NOT use this mode for

- Choosing the overall test strategy from scratch — use `strategy` mode.
- Whole-repo coverage ratcheting — this skill is diff-aware, not codebase-wide.
- Treating line coverage percentage as the result.
- Padding test counts to look better.

## Hard rules

- **Never report a single coverage score without naming the changed behaviors it hides.**
- **Never count broad E2E or browser smoke as strong proof unless it demonstrably crosses the changed branch or contract.**
- **Skipped, flaky, stale, or no-op suites are trust failures, not partial credit.**
- **Snapshot-only or mock-heavy tests do not count as strong proof for stateful, async, or contract changes.**
- **For medium/high-risk diffs, require at least one disconfirming check or fail-first proof.**
- **Prefer deleting or relabeling misleading tests over padding counts.**
- **Treat production-executed but unproved changed behavior as a higher priority than easy percentage wins.**

## Templates and references

- `references/trust-rubric.md` — the full verdict rubric with examples per category

## Hand-offs

- For pressure-testing the existing tests after this assessment → `dev-investigate mutation-scout`.
- For designing the smallest next proof → `design` mode.
- For shipping decisions reading this output → `dev-review ship-gate`.
- For PR body that needs this trust summary → `dev-PR`.
