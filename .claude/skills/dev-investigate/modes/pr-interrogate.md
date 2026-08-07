# Mode: pr-interrogate

Part of the `dev-investigate` skill. Selected when the user wants an evidence-based answer to "Does this PR actually fix the bug?", "Root-cause fix or symptom patch?", "How do we reproduce and prove it?", "What assumptions and side effects remain?", or "Is this safe to deploy now?" — phrasings like "interrogate this PR," "is this a real fix," or providing a PR URL with a bug context.

This is a reliability gate, not a style review.

## Job

Reconstruct the root cause, reproduce the bug on the PR's base branch, prove or disprove on the candidate, classify the fix as ROOT / PARTIAL_ROOT / SYMPTOM, quantify production impact, and issue a transparent GO / GO WITH FOLLOW-UPS / NO-SHIP verdict with evidence.

## Run

### Inputs to collect

1. PR URL and base branch.
2. The concrete bug statement in plain language.
3. Reproduction steps from support/user reports if available.
4. Production evidence source(s) — typically an error-monitoring system, plus optional admin/DB access.
5. A known failing example (trace ID, temp ID, request payload, timestamp window).

If any are missing, proceed with best available evidence but call out the missing inputs as confidence limits.

### Evidence standard

Never declare a fix valid without before/after proof.

Minimum bar (see `../references/differential-proof.md`):

1. Repro on base branch (`main` or PR base) fails with the expected signature.
2. Same payload/steps on candidate branch passes.
3. Evidence artifacts are linked or path-referenced.
4. Root-cause chain is explicit from source of bad state to observed failure.

If any item is missing, verdict must be conditional or `NO-SHIP`.

### Workflow

1. **PR and scope intake.**
   - Pull PR metadata, diff, changed files, comments, and linked incidents.
   - Translate vague titles into a plain-language issue statement.
   - **Lock scope:** the exact bug being validated, not all possible bugs.
   - Output: "We are validating X, not Y." Candidate ref and base ref pinned by commit SHA.

2. **Build the failure chain.**
   - Map the chain in code: where bad input originates → enters shared app state → which calls/mutations consume it → where server/runtime fails.
   - Use before/after line references.
   - **The chain should read as executable logic, not narrative.** Narrative is unverifiable; executable logic can be checked against the code line-by-line.

3. **Correlate with production signals.**
   - Use **production-only queries first.** (Production has more data, denser signal. Dev/staging may have untested code throwing errors for unrelated reasons that contaminate the signature.)
   - Pull concrete events that match the signature: timestamps, transactions/endpoints, trace IDs.
   - Confirm the event pattern matches the code-level chain.
   - Apply the user-attribution rule: see `../references/user-attribution-rule.md`. Default wording: `Affected Users: unknown (not tracked)` unless tracking is explicitly confirmed.

4. **Reproduce on base branch.**
   - Test or scenario file.
   - Command used.
   - Log showing failure signature.

5. **Prove on candidate branch.**
   - **Same test payload hash or scenario hash** between base and candidate runs. ("We ran the same test" silently becomes "we ran a similar test" without explicit hash matching.)
   - Pass/fail matrix: `base` fails, `candidate` passes.
   - Log tail proving expected behavior.

6. **Root-cause vs. symptom classification.** See `../references/rootness-classification.md`.

7. **Assumptions and confidence limits.**
   - List assumptions that must be true for the conclusion to hold (feature flag state, route actually used in production, event sample representative, backend validation behavior unchanged).
   - If an assumption is weak or unverified, lower confidence and call it out.

8. **Side-effect and regression scan.**
   - Behavior changes in shared hooks (error handling, retries, null semantics).
   - Inconsistent handling across similar modules.
   - UX drift (silent failure, false success toast, stale loading states).
   - History/navigation issues (back button, query param churn).
   - Contract drift (types, transformer output shape, tool payload assumptions).
   - **Search broadly for sibling call sites, not just changed files.** The most common verification failure mode is only re-testing changed files; sibling call sites are where regressions hide.

9. **Impact estimation (when an error-monitoring system is the data source).**
   - Define numerator and denominator explicitly.
   - Use same environment, time window, and dataset.
   - State what the percent means and what it does not mean.
   - Caveat if the exact product metric is unobservable from monitoring tags.
   - **Never infer exact product-level incidence when instrumentation cannot support it.**

10. **Verdict and ship recommendation.** Use `../templates/pr-interrogation-verdict.md`.

### Quality gates

Do not conclude until all are true:

1. Exact failure signature captured.
2. Exact scenario replayed on both refs.
3. At least one user-visible flow walkthrough is explained.
4. Side-effect scan includes unchanged sibling call sites.
5. Any data/observability gaps are explicit.

See `../references/non-ship-gate.md` for cluster-shared close-out conditions.

### Command playbook (adapt as needed)

```bash
# Fetch PR refs and inspect changed files
git fetch origin pull/<PR_NUMBER>/head:pr-<PR_NUMBER>
git diff --name-status origin/main...pr-<PR_NUMBER>

# Inspect specific before/after files
git diff --unified=8 origin/main...pr-<PR_NUMBER> -- <path>
git show origin/main:<path> | nl -ba | sed -n 'start,endp'
git show pr-<PR_NUMBER>:<path> | nl -ba | sed -n 'start,endp'

# Run targeted tests for changed behavior (adapt the runner to your stack)
<test-runner> <test-path-1> <test-path-2>
```

## Mode-specific references

- `../references/atomic-hypothesis-method.md`
- `../references/differential-proof.md` (required — the evidence standard)
- `../references/rootness-classification.md` (required — ROOT/PARTIAL/SYMPTOM)
- `../references/user-attribution-rule.md`
- `../references/non-ship-gate.md`
- `../references/output-format-contract.md`
- `../templates/pr-interrogation-verdict.md`

## Output

Strict template: `../templates/pr-interrogation-verdict.md`. The 7-item reporting structure:

1. What problem this PR claims to solve.
2. Before vs. after logic chain (with code references).
3. Reproduction evidence (`base` fail, `candidate` pass).
4. Production correlation evidence (events, traces, dates, links).
5. Assumptions required.
6. Potential side effects/regression risks.
7. Verdict (`GO` / `GO WITH FOLLOW-UPS` / `NO-SHIP`) + Classification (`ROOT` / `PARTIAL ROOT` / `SYMPTOM`) + Confidence (`High` / `Medium` / `Low`).

When the verdict is `GO WITH FOLLOW-UPS`, invoke the `dev-scope-deferral` skill to capture the follow-ups as a deferred-investigation note rather than embedding follow-up details in the verdict.

## Design Rationale

Mode-specific notes:

- **"Lock scope: exact bug, not all possible bugs"** — PR interrogations that drift to "all possible issues" never reach a verdict. The explicit lock is a failure-mode fence.
- **"Production-only queries first"** — production has more data (denser signal); dev/staging can throw errors from untested code that contaminate the signature.
- **"Chain should read as executable logic, not narrative"** — narrative is unverifiable; executable logic can be checked against the code line-by-line.
- **"Same test payload hash or scenario hash"** — explicit anti-drift discipline. Without this, "we ran the same test" silently becomes "we ran a similar test."
- **"Search broadly for sibling call sites, not just changed files"** — the most common verification failure mode is only re-testing changed files. Naming the failure mode prevents it.
- **The triple-axis verdict (Verdict × Classification × Confidence)** — preserves nuance that GO/NO-SHIP collapses lose: a `GO` with `SYMPTOM` / `Medium` confidence tells the reviewer "this fixes the immediate report but leaves work, and we know we don't fully know."
- **"Never infer exact product-level incidence when instrumentation cannot support it"** — strong anti-hallucination guard for impact estimation. The denominator/numerator/dataset discipline is harder to fake than a confident "X% of users."
