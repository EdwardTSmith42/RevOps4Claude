# Agentic Coding Practices

**Codebase Legibility Brief**

A codebase becomes easier for both humans and AI when it reduces ambiguity faster than it adds features.

## Fundamental truths

1. The main bottleneck is usually not coding speed. It is uncertainty about where truth lives, how the system works, and how to verify changes safely.
2. More comments do not automatically help. Clear boundaries, stable naming, explicit ownership, and testable contracts help more. That said, a well-placed comment can make a huge difference.
3. A repo is only truly understandable if someone can answer quickly: what is canonical, how do I run it, how do I verify it, what can break, and what is still incomplete.
4. Machine-readable surfaces beat prose when automation matters. Typed outputs, schemas, registries, event envelopes, and contract tests reduce guessing.
5. Honest gap tracking is a feature. A known limitation written down clearly is safer than implied completeness.

## Core practices

1. Keep one canonical "start here" entry point with current setup, run, verification, and source-of-truth links.
2. Declare which files, services, configs, or generated artifacts are authoritative, and which are legacy, derived, or reference-only.
3. Use the same subsystem doc shape everywhere: purpose, entry points, dependencies, invariants, failure modes, and minimal verification.
4. Encode important concepts as named types, states, policies, and failure classes instead of leaving them implicit in scattered conditionals.
5. Put comments at boundaries and contracts, not on obvious lines of code.
6. Turn critical interfaces into contract tests: APIs, events, prompts, tools, config precedence, migrations, and CLI output.
7. Generate lightweight indexes or registries for large surfaces so people and agents can navigate before reading the deepest code.
8. Treat documentation freshness like test freshness: stale links, stale paths, and stale instructions are real defects.

## Apply this anywhere

For a new repo, start with the doc map, source-of-truth statement, subsystem template, health check, and contract-test habit.

For an existing repo, do not add more docs first. First fix stale navigation, outdated paths, missing ownership, and unclear verification. Once the trust layer is reliable, the rest compounds.

## Used by

- `manifesto-review` mode of `dev-review` (primary — the rubric this mode reviews against)
- `brief` mode of `dev-review` at Profile C (large change) — cross-loaded for documentation/readability evaluation criteria

## Malleability note

**Canonical:** the principles above. They reflect the user's design philosophy for codebases that humans + AI can both work in.

**Adaptable:** the implementation patterns (where contract tests live, what doc shape looks like, etc.) — these adapt per repo. The principles don't.

