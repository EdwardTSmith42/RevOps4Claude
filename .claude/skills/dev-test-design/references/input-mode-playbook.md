# Input Mode Playbook

Use this reference to choose the right starting questions and default proof boundary for the incoming work shape.

## `diff`

Start with:
- what behavior actually changed?
- which branch or path inside the diff is riskiest?
- what is the smallest observable boundary that would prove this change?

Default proof order:
1. direct behavior check
2. contract or property proof if the change has obvious laws
3. differential proof when old-vs-new comparison is practical

Standard disconfirming check:
- same input on baseline vs candidate should differ only where the intended behavior changed

Escalate when:
- the diff mixes unrelated behavior slices
- the changed path is transition-heavy or retry-heavy
- the public contract is unstable or ambiguous

## `bug_report`

Start with:
- what is the smallest failing boundary?
- can we prove the failure on main or the prior implementation?
- what adjacent behavior could be silently regressed by the fix?

Default proof order:
1. fail-first or baseline repro
2. smallest fixing proof at the true boundary
3. one adjacent regression fence

Standard disconfirming check:
- prove the original bug still fails under materially similar inputs before trusting the fix

Escalate when:
- root cause is still unclear
- the bug is timing-sensitive or sequence-dependent
- reproduction requires extra local signal or temporary instrumentation

## `feature_plan`

Start with:
- what is the thinnest acceptance slice?
- what nearby behavior is most likely to regress?
- which proof shape would let us change the implementation later without rewriting the tests?

Default proof order:
1. thin acceptance proof
2. one regression fence
3. contract or property proof when the feature adds a reusable boundary or law

Standard disconfirming check:
- define one input or path that should not change, and prove it stays unchanged

Escalate when:
- the feature crosses UI, API, and workflow boundaries
- the acceptance slice is still ambiguous
- the implementation requires model/eval or stateful workflow proof
