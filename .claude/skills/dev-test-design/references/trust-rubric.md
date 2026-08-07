# Trust Rubric

Use the shared trust-state vocabulary so coverage audits can be compared with other proof artifacts.

## Trust States

- `verified`
  - direct, behavior-aligned proof likely to catch a realistic regression
- `adequate`
  - not perfect, but good enough for the current risk
- `heuristic`
  - useful signal, not enough to stand alone
- `unknown`
  - cannot confidently connect proof to changed behavior
- `misleading`
  - green but should not materially increase confidence
- `quarantined`
  - known value exists, but the artifact is not trusted in the main path

## Downgrade Triggers

- suite is skipped, flaky, stale, or no-op
- proof only touches neighbors, not the changed branch
- test is implementation-coupled and misses the real contract
- snapshot or mock-heavy proof stands in for stateful/contract risk

## Coverage Questions

- which changed behavior is actually proved?
- what is the highest-risk unproved path?
- which current tests should be ignored or relabeled?
- what is the smallest next proof that would materially increase trust?

## Output Template

- changed behavior
- current proof
- trust state
- gap or downgrade reason
- smallest next proof
