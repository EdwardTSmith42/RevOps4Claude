# Lane selector

The escalation menu — which investigation/proof/fix lane to pick based on what the bug needs. Used by `triage-and-fix`, `latent-hunt`, and `recurring-hunt` modes.

## Investigation lanes

- **Direct repro and fix** — the smallest credible repro is enough; no formal case needed.
- **Structured bug-ops case** — risk-scaled workflow with stage gates. Use `dev-delivery-ops` for the full case workflow; the compact disciplined arc also lives in `disciplined-bug-arc.md`.
- **Support/incident bundle** — when external evidence (support transcripts, replay) should shape the investigation.
- **Temporary observability** — when root cause is sequence-dependent, timing-sensitive, or otherwise opaque to static reasoning.
- **Full evidence investigation** (`evidence` mode) — high-impact, hard-to-reproduce, multi-system bugs that need a developer handoff package.

## Hunt lanes (for `latent-hunt`)

- **Static reasoning lane** — for suspicious control flow and ownership seams. Read code carefully; reason about state.
- **Tool lane** — for repo analyzers, lint/type checks, search scripts, perf tooling, custom audits.
- **Proof lane** — for mutation-style fault ideas and test weakness. Invoke `mutation-scout` mode when proof quality is the gap.
- **Runtime lane** — for sequence, retry, stale-state, or handoff validation.
- **Challenger lane** — when an independent second pass buys new signal. Spawn a fresh-context subagent with a disjoint risk surface where the harness supports it, route to a separate coding tool / model if you've wired one up, or do a separate sequential pass with an explicitly different focus.

## Proof lanes (for `triage-and-fix`)

- **Targeted test** — adds a failing test that the fix makes pass.
- **Differential proof** — base fail / candidate pass with same payload (see `differential-proof.md`).
- **Invariant gate** — the fix establishes an invariant that would be broken by the bug pattern; gate enforces it.
- **Local/dev observability loop** — when reproducibility is too hard for a unit test, capture the proof harness or observability snapshot before changing code.

## Decision heuristics

- **Prefer the smallest credible repro boundary.** Don't escalate to `evidence` mode for a 5-minute fix.
- **Don't broaden into full incident process when a small direct repro is enough.** Process bloat steals attention.
- **Match proof depth to risk.** A typo fix doesn't need differential proof; a race-condition fix probably does.
- **If evidence is incomplete, abstain over forced certainty.** Run more lanes or surface to user; don't claim a verdict you can't support.

## Used by

- `triage-and-fix` mode — supplies the escalation menu.
- `latent-hunt` mode — hunt-lane selection.
- `recurring-hunt` mode — method rotation pulls from this and `hunt-method-menu.md`.

## Malleability note

**Canonical:** the lane categories (investigation / hunt / proof) and their distinct purposes. Mixing categories ("use the runtime lane to fix the test") muddles the choice.

**Adaptable:** which specific lanes are available depends on what tooling exists. Use `dev-delivery-ops` when the investigation needs a structured case; use the lighter evidence lanes when it does not.
