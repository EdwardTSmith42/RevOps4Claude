# PR interrogation verdict

Strict template for `pr-interrogate` mode of `dev-investigate`. Renders the triple-axis verdict (Verdict × Classification × Confidence) plus the 7-item reporting structure.

```markdown
# PR Interrogation: <PR title and number>

**PR:** [<title>](<url>)
**Base ref:** `<commit SHA>` (origin/<branch>)
**Candidate ref:** `<commit SHA>` (PR head)

## 1. What problem this PR claims to solve

<Plain-language statement of the bug being validated. "We are validating X, not Y." — explicit scope lock.>

## 2. Before vs. after logic chain

(Executable logic, not narrative. With code references.)

**Base branch (failing path):**

1. <step> — `<file>:<line>`
2. <step> — `<file>:<line>`
3. ...

**Candidate branch (fixed path):**

1. <step> — `<file>:<line>`
2. <step> — `<file>:<line>`
3. ...

## 3. Reproduction evidence

| Ref | Result | Test/scenario | Log path |
|---|---|---|---|
| `base` | fail with expected signature | `<test path / scenario hash>` | `<log path>` |
| `candidate` | pass | `<same test path / scenario hash>` | `<log path>` |

**Same payload hash:** `<hash or explicit lock — payload contents / fixture path / command verbatim / random seed>`

## 4. Production correlation evidence

- **Error-monitoring events matching signature:** [<count>] [<link>]
- **Time window:** <UTC range>
- **Sample trace IDs:** <list>
- **Affected Users:** <count if confirmed; otherwise "unknown (not tracked)">
- **Endpoints/transactions:** <list>

## 5. Assumptions required

For this conclusion to hold, these must be true:

- <assumption> — verified / unverified
- <assumption> — verified / unverified

(Lower confidence and call out for unverified assumptions.)

## 6. Potential side effects / regression risks

- **Behavior changes in shared hooks:** <findings>
- **Inconsistent handling across similar modules:** <findings>
- **UX drift:** <findings (silent failure / false success / stale loading)>
- **History/navigation:** <findings>
- **Contract drift:** <findings>
- **Sibling call sites scanned:** <list — broader than just changed files>

## 7. Verdict

- **Verdict:** `GO` / `GO WITH FOLLOW-UPS` / `NO-SHIP`
- **Classification:** `ROOT` / `PARTIAL ROOT` / `SYMPTOM`
- **Confidence:** `High` / `Medium` / `Low`
- **Reason for confidence level:** <one or two sentences>

### Blocking risks (for NO-SHIP) or required follow-ups (for GO WITH FOLLOW-UPS)

- <item>

For `GO WITH FOLLOW-UPS`, invoke the `dev-scope-deferral` skill to capture each follow-up as a deferred-investigation note.

### Why to trust this conclusion

Objective evidence artifacts:

- <artifact path/link>
- <artifact path/link>

## Quality gate check

Confirm all five conditions are met before declaring complete (see `references/non-ship-gate.md`):

- [ ] Same-input differential proof
- [ ] Critical assumptions verified or named
- [ ] Rootness classification stated
- [ ] (High/critical risk only) Code+test+runtime triplet evidence
- [ ] Required harness decisions resolved
```

## Notes

- **Lock scope** at the top — "We are validating X, not Y."
- **Chain is executable logic, not narrative** — with code references.
- **Same payload/scenario hash** between base and candidate runs.
- **Search broadly for sibling call sites, not just changed files.**
- **Never infer exact product-level incidence when instrumentation cannot support it.**

## Used by

- `pr-interrogate` mode of `dev-investigate`.
