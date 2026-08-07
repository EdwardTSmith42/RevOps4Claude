# Defect families

The taxonomy of bug categories used to choose the right hunt lane and proof strategy. Used by `latent-hunt` and `mutation-scout` modes.

## The seven families

- **`async/state`** — promise/await mistakes, detached callbacks, lifecycle resolution timing, swallowed async failures, missing `await`.
- **`retry/idempotency`** — retries without idempotency, replay after timeout, duplicate side effects after reconnect, process-local dedup that doesn't survive restart.
- **`cache/SWR`** — SWR `mutate` misuse, missing rollback, direct cache writes in the wrong layer, stale fan-out after writes, stale-threshold mismatches.
- **`performance`** — polling that never settles, unbounded loops, N+1 fetches, performance cliffs at scale boundaries.
- **`contract/schema`** — drift between server types, generated clients, schema validators, prompt schemas, flow definitions, and UI consumers.
- **`proof weakness`** — tests that are green but shallow: surviving mutants, state-machine gaps, assertions that miss the real invariant. (Hand-off to `mutation-scout` mode.)
- **`UI sequence or handoff`** — UI flows that work in isolation but fail at route, project, thread, tab, or notification handoff boundaries.

## Per-family hunt lanes

Each family has a preferred hunt lane:

| Family | Preferred lane | Why |
|---|---|---|
| async/state | static reasoning + runtime | sequence and lifecycle need both code reading and live observation |
| retry/idempotency | static reasoning + runtime | needs replay scenarios |
| cache/SWR | static reasoning + tool lane | SWR-specific patterns benefit from targeted analyzers |
| performance | tool lane (perf tooling) + runtime | profile actual workloads |
| contract/schema | tool lane (schema diffing) + static | contract drift surfaces in cross-boundary diffs |
| proof weakness | proof lane (`mutation-scout` mode) | mutation thinking is the right tool |
| UI sequence/handoff | runtime + browser validation | needs live UI reproduction |

## Mutation-scout change-shape mapping

The `mutation-scout` mode's change-shape categories overlap with these families:

- `branch/boundary` ↔ partial overlap with `async/state`, `UI handoff`
- `mapping/contract` ↔ `contract/schema`
- `error/retry` ↔ `retry/idempotency`
- `async/state` ↔ `async/state`
- `normalization/defaulting` ↔ partial overlap with `contract/schema`

## Used by

- `latent-hunt` mode — defect-family classification step (3 of 7).
- `mutation-scout` mode — change-shape classification (mapped to families).

## Malleability note

**Canonical:** the family vocabulary itself (these seven labels). Adding new families requires user check-in; renaming creates drift.

**Adaptable:** the per-family hunt-lane preference is a guideline, not a rule — sometimes a contract/schema bug benefits from runtime testing, sometimes a UI bug surfaces statically.

