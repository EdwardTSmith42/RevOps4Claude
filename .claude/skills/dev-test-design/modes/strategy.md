# Mode: strategy

The top-level proof router. Answer: **"What is the right way to prove this change?"**

This mode is for the broader question, not the narrow design. It picks the *shape* of proof; `design` mode turns that shape into a concrete plan.

## When to use

- The work is broad enough that the shape isn't obvious.
- The user wants stronger tests, coverage assessment, legacy test cleanup, or better logging-for-proof.
- There's a question of whether existing tests are weak, stale, duplicated, flaky, or misaligned.
- The proof needs to compose multiple lanes (e.g., one property test + one differential proof + one observability harness).

## Default outputs

Produce some or all:
- `Risk and proof shape`
- `What to test`
- `What not to test`
- `Primary strategy`
- `Supporting skills and tools`
- `Minimal implementation plan`
- `Coverage and trust assessment`
- `Follow-up cleanup or tooling ideas`

For broad requests, start with a short testing plan before any implementation.

## Workflow

### 1. Classify the change

- `work_type`: `bug | polish | feature | refactor | migration | investigation`
- `risk_level`: `low | medium | high`
- `surface`: `ui | api | workflow | schema | prompt | parser | model-eval | infra | mixed`

### 2. Choose one boundary or behavior slice first

- Don't start with "review all of <module>" or "improve testing everywhere."
- Name **one** boundary, **one** risky behavior, **one** proof question. Other slices get their own pass.

### 3. Inspect the current proof surface

- Existing tests
- Nearby logging/harnesses
- CI or build guards
- Drift or no-op runners

### 4. Choose the primary proof mode

| Mode | Use when |
|---|---|
| **`hermetic behavior`** | Pure function, deterministic transformation, no environment dependence |
| **`property`** | Range of inputs / invariant that must hold; finds edge cases TDD misses |
| **`stateful`** | State machine, sequence of operations, transition correctness |
| **`contract`** | API/RPC/event boundary; format + version + compatibility |
| **`differential`** | Bug fix (before-fix fails / after-fix passes) or refactor (old vs new produce same output) |
| **`eval/rubric`** | LLM output, prompt change, generation quality |
| **`browser smoke`** | Browser/session/wiring risk is the *actual* risk |
| **`temporary observability`** | Root cause unclear; instrument before testing |

Pick **one** primary mode. Supporting modes can be added but only for named blind spots.

### 5. Define the proof plan

- Invariant(s) the change must preserve
- Disconfirming check(s) — what would fail if the fix is wrong
- Exact artifact(s) to produce
- Trust-state target (`verified` / `useful but heuristic` / `incomplete` / `stale or misleading`)

### 6. Implement only after the plan is coherent

If you can't name disconfirming evidence, the plan is incomplete. Don't start writing tests yet.

### 7. Assess trust after the run

After tests run, classify the result:
- `verified` — proof exercises the actual failure mechanism, fail-first or strong differential
- `useful but heuristic` — adequate for risk level but doesn't prove the seam directly
- `incomplete` — known gaps in the plan
- `stale or misleading` — tests pass but for the wrong reasons; need replacement

### 8. Capture follow-up improvements out of scope

If the plan surfaces work that's valid but expands the current change, invoke `dev-scope-deferral`.

## Hand-offs

- After `strategy` picks a shape → invoke `design` mode to author the minimal plan.
- For medium+ risk → also invoke `invariants` mode.
- After tests exist and you want to assess trust → `coverage` mode.

## Guardrails

- Don't default to generic TDD advice.
- Don't recommend "more tests" without naming what behavior they protect.
- Don't choose browser/E2E as primary unless wiring/session/auth is the actual risk.
- Don't broaden into whole-suite design when the trigger was one specific change.
- If evidence is incomplete, return `unknown` plus the next validation step — don't pretend certainty.
