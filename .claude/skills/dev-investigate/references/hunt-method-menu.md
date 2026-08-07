# Hunt method menu

The lane menu used during method rotation in `recurring-hunt` and `latent-hunt`. Different methods produce different signal; rotating lanes prevents the loop from grinding the same review pattern.

## High-value methods

- **Risk-map and diff-cluster scan** — pull from `latent-bug-scout`'s discipline: changed files + immediate consumers, clustered by feature/dir/state owner. Use `blast-radius-taxonomy.md` for the manual-reasoning shape.

- **Blast-radius seam scan** — when shared seam uncertainty is high. Map nearby consumers and boundaries before expanding scope.

- **Static suspicious-pattern review** — read code carefully for the patterns in `latent-bug-signals.md`: missing await, detached callbacks, swallowed async failures, retries without idempotency, SWR mutate misuse, contract drift.

- **Targeted proof-gap and test weakness review** — `mutation-scout` mode territory. When the gap is whether tests would catch a realistic mistake, run mutation-scout instead of more code reading.

- **Async / retry / stale-state / contract checks** — focused checks for the corresponding defect families.

- **Runtime smoke or browser validation** — when behavior change is the question. Use `browser-use` skill or Chrome MCP for UI flows.

- **Library or file-format docs review** — when packages, framework contracts, or file-format details are unstable or unclear. Internet research is allowed; prefer official docs and primary sources.

## Adjacent lanes that depend on configured tooling

- **Independent-reviewer challenger pass** — a second pair of eyes without the fixing agent's tunnel vision. Spawn a fresh-context subagent, or route to a separate reviewer CLI / model if one's wired up.

- **Error-monitoring sweep** — query for new dev-only or prod issues in the error-monitoring system. Use the relevant MCP directly when no wrapper skill is configured.

- **Session-replay walk** — UI-handoff debugging via session replay. Use browser-use or the relevant MCP when no replay-specific wrapper skill is configured.

## Method rotation rules

- **Use varied lanes, not one repeated review pattern.** If the last method was used recently and another promising method exists, rotate.

- **If the same slice still has credible suspicion, revisit it with a different method.** Don't rotate slices when the suspicion is unresolved; rotate methods.

- **Skip lanes that need sign-in, UI approval, or any other user interaction.** Record that they were blocked. Continue with available lanes.

- **For slow lanes (challenger reviews, browser tests), prefer one tool-appropriate long wait over short polling.** Ten to fifteen minutes is acceptable when the tool is known to take that long.

## Subagent fan-out (when useful)

When subagent fan-out helps the hunt:
- **Split by disjoint risk surface, not arbitrary file chunks.**
- One lane for SWR/cache, one for async/retry, one for performance or contract drift — disjoint surfaces.
- Give each lane a **concrete question** and **clear ownership.**
- Don't ask multiple agents to re-review the same exact surface.

## Used by

- `recurring-hunt` mode — method rotation.
- `latent-hunt` mode — hunt-lane selection (overlaps with `lane-selector.md`).

## Malleability note

**Canonical:** the rotation principle (vary lanes; rotate methods over slices when suspicion is unresolved) and the disjoint-risk-surface fan-out rule.

**Adaptable:** which specific methods are in the menu — depends on what tooling is configured (challenger CLIs, error-monitoring MCPs, replay tools).

