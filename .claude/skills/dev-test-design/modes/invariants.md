# Mode: invariants

Define and enforce **functional / performance / operational / minimality / safety invariants** to prevent plausible-but-wrong or plausible-but-slow AI implementations.

This mode addresses repeated AI-coding failure modes:
- Plausible but semantically wrong behavior (tests pass for the wrong reasons)
- Correct behavior with hidden efficiency regressions
- Over-built solutions that satisfy prompts but miss the actual job

## When to use

- Medium+ risk work where correctness alone isn't enough — performance, ops behavior, scope minimality also matter.
- Any change where "looks right and tests pass" is *not* sufficient evidence.
- After `strategy` and `design` modes if invariants weren't already explicit.

## Workflow

### 1. Identify invariant categories that apply

| Category | Asks |
|---|---|
| **functional** | Does this preserve correct behavior across the input space? |
| **performance** | Does this stay within latency / throughput / memory budget? |
| **operational** | Does this preserve observability, idempotence, replayability? |
| **minimality** | Is the change *small enough* — no incidental surface expansion? |
| **safety** | Does this preserve safety/security/access invariants? |

For medium+ risk, prefer at least **two orthogonal categories**. Functional alone usually isn't enough.

### 2. Author each invariant

Each invariant has:
- **Statement** — what must remain true (one sentence, declarative)
- **Metric** — what's measured to check it
- **Target** — the threshold or expected value
- **Disconfirming check** — exactly what would fail if the invariant is violated
- **Critical?** — yes/no. Critical invariants block close.

Example (performance):
```
Statement: p95 latency stays within agreed budget
Metric: p95 latency on /api/threads/list under representative concurrency
Target: <= baseline + 10%
Disconfirming check: run benchmark at concurrency=20, capture p95, compare against pre-change baseline
Critical: yes
```

### 3. Record observed results

For each invariant, after the proof runs:
- `pass` — invariant verified
- `fail` — invariant violated; fix is wrong or incomplete
- `abstain` — couldn't verify; **abstain requires a reason**

### 4. Run the gate

Don't close the work until:
- All critical invariants are `pass`
- No silent abstains
- No `fail` records left unaddressed

### 5. Capture follow-ups

If a non-critical invariant is `abstain` and the verification work would be valuable later, invoke `dev-scope-deferral`.

## Invariant categories — typical patterns

See `references/invariant-contract.md` for the full pattern catalog. Brief overview:

- **functional** — output equality / behavior equivalence on N input cases; before/after differential
- **performance** — latency budgets / throughput floors / memory ceilings; benchmark at representative load
- **operational** — log fields preserved / metric cardinality bounded / replay determinism / idempotence on retry
- **minimality** — file count delta / public surface delta / dependency delta / config option count
- **safety** — auth boundary preserved / data classification respected / permission scope unchanged

## Recording invariants

The prompt-driven workflow above is sufficient for most work: write invariants directly into the proof plan, track results in the PR body, the change brief, or verification notes. If your team runs a structured case-file or DeliveryOps process, the same fields (statement / metric / target / disconfirming check / critical / status) can be lifted into whatever schema that process uses.

## Hard rules

- **Don't `abstain` silently.** Every abstain requires a reason in writing.
- **Critical work doesn't close with critical invariants abstained.**
- **Prefer at least two orthogonal categories for medium+ risk.**
- **Invariants tied to actual behavior, not phrased as wishes.** "Should be fast" isn't an invariant; "p95 <= 200ms at 20 concurrent users" is.
- **Disconfirming checks are mandatory.** "How would I notice this invariant was violated?" must have a concrete answer.

## Hand-offs

- `design` mode supplies the proof plan that invariants attach to.
- `coverage` mode reads invariant pass/fail when assessing trust on a diff.
- `dev-investigate triage-and-fix` consumes invariant verdicts when classifying root vs. symptom fixes.

## References

- `references/invariant-contract.md` — full invariant pattern catalog with examples
