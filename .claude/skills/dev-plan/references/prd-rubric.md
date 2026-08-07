# MVP PRD Rubric

Use this rubric while filling `../templates/prd-template.md`.

## A. Scope Quality

- MVP scope is explicit and small.
- Out-of-scope list is real and non-empty.
- No architecture changes unless required and approved.

Fail if:
- "In scope" includes broad rewrites, refactors, or multi-system changes without hard need.

## B. Existing Pattern Quality

- At least two concrete existing code references are listed.
- At least one existing test reference is listed.
- Plan copies established patterns instead of inventing new ones.

Fail if:
- The plan introduces new patterns while equivalent internal patterns already exist.

## C. Overlap Quality

- Open PR overlap scan is run and recorded.
- Any overlap lists PR numbers and affected files.
- Mitigation is chosen (rebase/stack/cherry-pick/skip).

Fail if:
- There are file overlaps and no mitigation plan.

## D. Test-First Quality

- New failing tests are named before implementation.
- RED proof commands are listed.
- Tests include hard cases (race, stale state, null/undefined, timeout, retry, ordering).

Fail if:
- Tests are added only after implementation.
- Tests are trivially easy and miss real failure conditions.

## E. Verification Quality

- New tests fail before code change and pass after change.
- Nearby regression tests are run.
- Runtime/manual verification is logged when needed.

Fail if:
- No fail->pass evidence exists for added tests.

## F. Escalation Rule

Escalate to human review and pause code changes when:
- review threads repeatedly rehash the same policy conflict across PRs
- multiple "fixes" to one file keep reintroducing equivalent regressions
- behavior choice is product/policy driven, not purely technical

When escalating, include:
- conflicting options
- user impact of each option
- recommended default and reason
