# Mode: design

The narrower lane: turn one diff, bug report, or feature plan into **one minimal verification design** that is credible, diagnostic, and hard to game.

This mode runs after the problem is framed and before proof is implemented. Use after `strategy` mode has picked the proof shape, or directly when the strategy is obvious.

## Default outputs

Produce in this order:
- `Input frame`
- `Behavior claim`
- `Primary risk`
- `Smallest proof boundary`
- `Primary proof mode`
- `Oracle or pass/fail rule`
- `Disconfirming check`
- `Minimal artifacts`
- `What not to test`
- `Done signal`

## Workflow

### 1. Classify the request

- `input_kind`: `diff | bug_report | feature_plan`
- `work_type`, `risk_level`, `surface`

### 2. Reduce the request to one behavior claim

The skill's value is in the verb. Not "test the new auth flow" — "verify that an unauthenticated request to `/api/admin` returns 401 with no body, even when the legacy `X-Internal-Token` header is present."

### 3. Choose the narrowest proof boundary

The smallest unit that *proves* the claim. Most plans test too much surface.

### 4. Pick one primary proof mode

See `strategy` mode's mode list. One primary; supporting modes only for named blind spots.

### 5. Define the minimum convincing proof

- **Invariant(s)** the change must preserve
- **Oracle** or pass/fail rule — what determines success?
- **One disconfirming check** — what would catch the fix being wrong?
- **Exact artifact(s)** — file paths, test names
- **Explicit `What not to test`** — bound the scope

### 6. Route to execution skills only after the plan is coherent

If the plan can't name disconfirming evidence, it's incomplete. Don't start writing tests yet.

### 7. Stop when the main risk is closed

Don't broaden into suite design for the whole module. That's a separate pass.

## Input-specific guidance

### `diff`

- Read behavior change, name the riskiest changed branch.
- Prefer one direct check that crosses the changed branch.
- Avoid testing through layers of indirection that hide the change.

### `bug_report`

- Isolate the smallest failing boundary.
- Prefer **fail-first or before/after differential proof** when practical — test fails before the fix, passes after.
- A green test on a fixed bug without before/after evidence is weaker proof than the differential.

### `feature_plan`

- Define the **thinnest acceptance slice** plus **one regression fence**.
- Don't build a scenario matrix. One thin slice + one fence beats six "comprehensive" tests that all pass for the wrong reasons.

## Templates and references

- `templates/proof-plan.md` — fill-in-the-blank shape for the output
- `references/input-mode-playbook.md` — diff vs bug-report vs feature-plan playbooks
- `references/minimal-proof-rubric.md` — what counts as minimal-but-credible

## Hand-offs

- After this mode produces a plan → execute via the project's test runner.
- For medium+ risk → `invariants` mode in addition.
- For pressure-testing the resulting tests → `dev-investigate mutation-scout`.
- For trust assessment after tests run → `coverage` mode.

## Guardrails

- Don't default to generic TDD advice.
- **Require one primary proof artifact first.** Add a second only for a named blind spot.
- **Large diffs must be split into behavior slices.** Never produce one vague proof plan for unrelated changes.
- **Bug plans should include fail-first or same-input baseline proof when practical.**
- **Feature plans should prove a thin acceptance slice plus one adjacent regression fence**, not a scenario matrix.
- **Prefer production boundary shape over convenience mocks** or helper-heavy tests.
- **Use browser/E2E proof only when browser/session/wiring is the actual risk.**
- **If root cause is still unclear, choose temporary observability before permanent test expansion.**
- **If the plan cannot name disconfirming evidence, it is incomplete.**
