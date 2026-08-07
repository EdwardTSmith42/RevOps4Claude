# Latent-bug signals — high-value catalog

The hard-won pattern catalog for hunting hidden bugs. War-story-derived; ships without per-pattern incident origins (origin notes were intentionally omitted).

## Signals to scan for

- Missing `await`, detached callbacks, swallowed async failures, or lifecycle work that resolves too early.

- Process-local dedup, retries without idempotency, replay after timeout, or duplicate side effects after reconnect.

- Polling that never settles, stale-threshold mismatches, unbounded loops, or N+1 fetches.

- SWR `mutate` misuse, missing rollback, direct cache writes in the wrong layer, or stale fan-out after writes.

- Contract drift between server types, generated clients, schema validators, prompts, flows, and UI consumers.

- When a branch makes hidden or internal work into real persisted records, audit direct-by-id auth and ownership boundaries, not just list filtering or UI visibility rules.

- Check binding invariants on shared runners and adapters: thread/message, session/project, trigger/workflow, file/project, and similar pairings should be proved explicitly rather than assumed from separate lookups.

- Tests that are green but shallow: obvious surviving mutants, state-machine gaps, or assertions that miss the real invariant.

- UI flows that work in isolation but fail at route, project, thread, tab, or notification handoff boundaries.

## How to use

When running `latent-hunt` mode:

1. Build the risk map first (changed files + immediate consumers).
2. **Then** scan for these signals across the risk map, not the whole repo.
3. For each signal that matches, classify the suspicion (`confirmed` / `likely` / `unclear` / `dismissed`) with file evidence.
4. Rank by severity (see `severity-rubric.md`) and triage to terminal states (see `triage-rubric.md`).

## Why these specifically

These are war-story-derived patterns — each one points at a real category of incident from past investigations. The catalog is intentionally specific (e.g., "thread/message, session/project, trigger/workflow, file/project") because specific pairings remind the agent to check the *exact* thing rather than abstract principles. Specific examples beat generic best practices. Adapt the pairings to your own domain — the pattern is "binding invariants on shared runners," and the examples illustrate what specificity looks like.

## Used by

- `latent-hunt` mode — the highest-leverage single asset.
- `recurring-hunt` mode — used during method rotation (especially the `risk-map and diff-cluster scan` method).

## Malleability note

**Canonical:** the patterns themselves. Each pattern is the result of an actual incident root-cause; rewording them risks losing the specificity that makes them trigger right.

**Adaptable:** the specific domain pairings (thread/message, etc.) — replace with your own codebase's invariant pairings. The *concept* of "binding invariants on shared runners" generalizes; the pairings are examples.

