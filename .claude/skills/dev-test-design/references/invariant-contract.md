# Invariant Contract

## Categories
- `functional`: primary behavior correctness.
- `performance`: latency/throughput/resource budgets on realistic scenarios.
- `operational`: diagnosability and runtime evidence quality.
- `minimality`: avoids unnecessary scope/dependency/surface expansion.
- `safety`: explicit guardrail constraints.

## Required Fields Per Invariant
- `invariant_id`
- `category`
- `critical`
- `statement`
- `disconfirming_checks[]`
- `status` (`proposed|pass|fail|abstain`)
- `abstain_reason` (required when status=`abstain`)
- `evidence_refs[]`

## Gate Expectations
- At least one passing `functional` invariant before `IMPLEMENT_VERIFY` exit.
- No critical `proposed` invariants at `BLAST_RADIUS_REGRESSION`/`CLOSEOUT`.
- Medium/high/critical should have passing invariants in at least two categories.
- High/critical should include at least one passing non-functional invariant.

## Practical Rule
Invariants are not a second test suite; they are a compact list of what must remain true to avoid plausible-but-wrong outcomes.
