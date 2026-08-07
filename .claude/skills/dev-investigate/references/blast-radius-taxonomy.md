# Blast-radius taxonomy

Manual-reasoning taxonomy for mapping the likely downstream impact of a code change. Used by `latent-hunt` and `recurring-hunt` as their portable scope strategy. The taxonomy stands on its own when a repository-specific dependency scanner is unavailable.

## The three risk buckets

- **Likely-now risks** — impact that almost certainly manifests if the change ships. Direct consumers of changed functions, code paths exercised by the affected flow, components that will rerender / requery.
- **Possible-watch risks** — adjacent surfaces that *might* be affected. Worth tracking but not blocking. Often resolves to "no impact" after a closer look.
- **Unknown-needs-simulation risks** — surfaces where reasoning alone can't determine impact. Name the experiment that would resolve the unknown (logging, scenario test, observability harness).

The **unknown-needs-simulation** bucket is the differentiator. Most risk taxonomies stop at known/unknown; this one names the experiment that resolves the unknown rather than letting it linger.

## Subsystem clusters

When mapping blast radius, group risks by **subsystem**, not flat list. A change affecting `imports → admin UI` and `imports → exports` belongs in two clusters; clustering surfaces the cross-system shape.

Common subsystem clusters to adapt to your codebase:
- **client/UI** — hooks, components, view-level state
- **server/API** — routes, services, persistence
- **flows / workflows** — orchestration definitions and triggers
- **pipelines** — extraction, transformation, ingestion
- **generated SDK / mocks** — generated client code, schema validators
- **agent prompts / tool schemas** — when applicable

Cluster names are codebase-specific; the *grouping discipline* (don't flat-list, group by subsystem) is what matters.

## Authority-weighted priorities

Not all surfaces weigh equally. Prioritize:

1. **Authority surfaces** — entry points, shared state owners, mutation owners. These propagate widely; a bug here cascades.
2. **High-traffic surfaces** — code paths exercised by many users / flows / requests.
3. **Generated-contract surfaces** — server types, generated clients, schema validators. Drift here reaches every downstream consumer silently.
4. **Authentication / ownership boundaries** — direct-by-id auth, ownership predicates. Bugs here are security risks.

Surfaces low on this list (rarely-traveled paths, dev-only code, deprecated branches) get less attention.

## Where to look

When mapping the blast radius around a changed file or symbol:

- **Immediate consumers** — files that directly import / call the changed code.
- **Boundaries** — type / schema / contract definitions affected by the change.
- **State owners** — components / services / flows that own state the change touches.
- **Retries** — retry / replay code that would re-execute affected paths.
- **Caches** — cache layers (SWR, in-memory, generated SDK) that hold affected data.
- **Async callbacks** — promise handlers, event listeners, webhook handlers.
- **Generated-contract surfaces** — anything regenerated from the changed source.

These are the same surfaces named in `latent-bug-signals.md` (the high-value catalog) — the overlap is intentional.

## Stance

- Lightweight, static-analysis-first.
- Does not claim certainty.
- Marks uncertainty as **simulation/logging follow-up** — name the experiment, don't just label "unknown."

## Used by

- `latent-hunt` mode — Step 2 (Build a risk map BEFORE deep review).
- `recurring-hunt` mode — Scope Strategy (when shared seam uncertainty surfaces).

## Malleability note

**Canonical:** the three risk buckets and the unknown-needs-simulation discipline. Collapsing buckets or dropping the "name the experiment" requirement loses what makes the taxonomy useful.

**Adaptable:** subsystem cluster names and the specific surfaces to look for — these are codebase-specific. Update as the architecture evolves.
