# Lane selector

The supporting-lane menu — which review/validation lanes to add when the chosen mode has a named blind spot. Loaded by the `dev-review` SKILL.md router and by individual modes when escalation is needed.

## The lanes

- **Static reasoning** — read the code carefully, reason about state. Cheapest. Use for control-flow / ownership / contract analysis where a careful read can answer the question.
- **Tool lane** — repo analyzers, lint / type / build checks, search scripts, perf tooling. Use when a tool can mechanically catch what reasoning would miss.
- **Targeted tests / proof** — unit tests, contract tests, integration tests for the changed surface. Use when behavior verification is the gap.
- **Runtime / observability** — actually run the change, observe behavior. Use for sequence / timing / handoff issues that static reasoning can't catch.
- **Challenger lane** — independent reviewer. A fresh-context sub-agent fanout, or a separate coding tool / model if you've wired one up. Use when blind spots from a single reviewer are the concern.
- **PR / reliability gate** — heavyweight `ship-gate` mode workflow. Use when ship-readiness is the question.
- **Milestone cleanup** — `checkpoint` mode workflow. Use when the change is a milestone needing regression review + decomp + cleanup audit.

## The rule

**Choose only the rungs that close a real blind spot.**

If the review question is narrow, do not run the full gauntlet. Most reviews need 1-2 lanes; running all of them is expensive and dilutes signal.

## Common ladder (fastest to slowest)

When uncertain, climb the ladder until you have enough signal:

1. Local reasoning and code reading
2. Targeted tests or type/lint/build checks
3. One or more challenger lanes
4. PR or reliability gate
5. Milestone cleanup if the slice is large or recently decomposed

Stop at the rung where the answer becomes clear.

## Escalation triggers (when to add a lane)

- **Add tool lane** when reasoning surfaces something a tool can verify cheaply (e.g., contract drift suspected → run the schema diff tool).
- **Add proof lane** when "I think this works" needs to become "this provably works" (e.g., race condition concern → add a targeted timing test).
- **Add runtime lane** when behavior depends on real environments (DB sequence drift, API timing, browser interaction).
- **Add challenger lane** when an independent perspective would catch what the primary reviewer might miss (especially for async/state-heavy changes).
- **Add ship-gate lane** when the question is "is this safe to deploy" rather than "is this code good."
- **Add milestone-cleanup lane** when the work touches many files OR recently decomposed code OR introduces transitional scaffolding.

## Anti-patterns

- ❌ **Default to broad review.** "Branch-wide review" is a warning surface (when something feels off), not the default proof surface.
- ❌ **Run every lane to be thorough.** Lanes have cost; uncalibrated lane addition burns inference and dilutes signal.
- ❌ **Skip lanes the question requires.** If "is this safe to deploy" is the question, skipping the ship-gate lane is malpractice.

## Used by

- `dev-review` SKILL.md router (picker logic)
- `ship-gate` mode (for "should I add a challenger lane?" decisions)
- `checkpoint` mode (for "should I add a runtime lane after smoke?")
- `manifesto-review` mode (for "should I add proof lane for a contract change recommendation?")

## Malleability note

**Canonical:** the lane categories (static / tool / proof / runtime / challenger / ship-gate / milestone-cleanup). These map to distinct kinds of evidence each lane produces.

**Adaptable:** the specific tools per lane — the menu of sibling tool-wrapper skills evolves; treat the lane as the contract, the tools as the implementation.

