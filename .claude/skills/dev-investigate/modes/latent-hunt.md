# Mode: latent-hunt

Part of the `dev-investigate` skill. Selected when the user wants a separate hidden-bug hunt rather than a normal review — phrasings like "hunt for hidden bugs in this branch / PR / code slice," "find race conditions / stale state / mutation survivors / contract drift," or "ranked latent risks for this code surface."

## Job

Map suspicious seams before reading everything; choose the smallest high-yield hunt lanes; combine code reasoning, targeted tools, and proof-gap triage; return ranked risks with evidence and confidence; avoid defaulting into broad fixes or generic PR review.

## Run

1. **Define the hunt target.**
   - `branch | pr | commit_range | file_cluster | existing_slice`
   - Name the question in plain language: hidden regressions, stale state, race risk, performance cliffs, etc.

2. **Build a risk map BEFORE deep review.**
   - Start with changed files when a diff exists.
   - Expand only to immediate consumers, boundaries, state owners, retries, caches, async callbacks, and generated-contract surfaces.
   - **Prefer a blast-radius sketch over whole-repo reading.** See `../references/blast-radius-taxonomy.md` for the manual-reasoning taxonomy (likely-now / possible-watch / unknown-needs-simulation; subsystem clusters; authority-weighted priorities).

3. **Classify the likely defect families.** See `../references/defect-families.md`:
   - `async/state`
   - `retry/idempotency`
   - `cache/SWR`
   - `performance`
   - `contract/schema`
   - `proof weakness`
   - `UI sequence or handoff`

4. **Choose the narrowest useful hunt lanes.** See `../references/lane-selector.md`:
   - **Static reasoning lane** for suspicious control flow and ownership seams.
   - **Tool lane** for repo analyzers, lint/type checks, search scripts, perf tooling, or custom audits.
   - **Proof lane** for mutation-style fault ideas and test weakness — invoke the `mutation-scout` mode of this skill when the gap is proof-quality rather than inspection.
   - **Runtime lane** for sequence, retry, stale-state, or handoff validation.
   - **Challenger lane** only when an independent second pass buys new signal.

5. **Run the hunt.**
   - Prefer small, evidence-rich commands and scoped tests.
   - Favor realistic bug patterns over style cleanup.
   - Record whether each suspicion is `confirmed` / `likely` / `unclear` / `dismissed`.

6. **Rank what matters.** See `../references/severity-rubric.md`:
   - `P0/P1`: correctness, data loss, authorization, duplicate side effects, broken handoffs.
   - `P2`: latent reliability or stale-state risks likely to produce bugs later.
   - `P3`: cleanup or maintainability issues only if they plausibly hide defects.

7. **Decide the next move.**
   - Fix immediately only when low-risk and user intent allows.
   - Otherwise recommend the smallest next proof surface or human decision.
   - For valid follow-up work surfaced during the hunt: **invoke the `dev-scope-deferral` skill** rather than embedding TODO-style notes in this output.

### High-value signals — load this catalog before scanning

See `../references/latent-bug-signals.md` for the 10-signal high-value catalog (verbatim from the source). Highlights:

- Missing `await`, detached callbacks, swallowed async failures, lifecycle work that resolves too early.
- Process-local dedup, retries without idempotency, replay after timeout, duplicate side effects after reconnect.
- Polling that never settles, stale-threshold mismatches, unbounded loops, N+1 fetches.
- SWR `mutate` misuse, missing rollback, direct cache writes in the wrong layer, stale fan-out after writes.
- Contract drift between server types, generated clients, schema validators, prompts, flows, and UI consumers.
- When a branch makes hidden or internal work into real persisted records, audit direct-by-id auth and ownership boundaries, not just list filtering or UI visibility rules.
- Check binding invariants on shared runners and adapters: thread/message, session/project, trigger/workflow, file/project, and similar pairings should be proved explicitly rather than assumed from separate lookups.
- Tests that are green but shallow: obvious surviving mutants, state-machine gaps, or assertions that miss the real invariant.
- UI flows that work in isolation but fail at route, project, thread, tab, or notification handoff boundaries.

### Subagent guidance

When subagent fan-out helps:
- Split by **disjoint risk surface, not arbitrary file chunks.**
- Examples: one lane for SWR/cache, one for async/retry, one for performance or contract drift.
- Give each lane a **concrete question** and **clear ownership.**
- Do not ask multiple agents to re-review the same exact surface.

## Mode-specific references

- `../references/defect-families.md`
- `../references/latent-bug-signals.md` (the high-value catalog)
- `../references/severity-rubric.md`
- `../references/triage-rubric.md`
- `../references/lane-selector.md`
- `../references/hunt-method-menu.md`
- `../references/blast-radius-taxonomy.md`
- `../references/output-format-contract.md`

## Output

Soft template:

- `Hunt scope`
- `Risk map`
- `Chosen lanes`
- `Findings` (with file evidence and confidence per finding)
- `Unproved suspicions`
- `Recommended next step`

Triage every finding to a terminal state (`FIX_NOW` / `HUMAN_DECISION` / `DEFER` / `DISMISSED` per `../references/triage-rubric.md`). For `DEFER` items, invoke the `dev-scope-deferral` skill.

## Guardrails

- This is not the default skill for normal review.
- Do not turn every hunt into a whole-repo audit.
- Do not confuse broad suspicion with confirmed bugs; label uncertainty explicitly.
- Do not chase style, decomposition, or cleanup unless it plausibly hides a defect.
- Do not recommend heavyweight tools or whole-repo mutation runs unless the expected insight is clearly worth it.
- Do not default to fixing issues during the hunt unless the user asked for fixes or the fix is obvious and low-risk.

## Design Rationale

Mode-specific notes:

- **"Map suspicious seams before reading everything"** + **"prefer a blast-radius sketch over whole-repo reading"** — explicit anti-pattern guard against the "read everything first" failure mode that LLMs gravitate toward. The risk-map step (2) precedes the deep-review step (5) deliberately.
- **Defect-family classification → narrowest hunt lanes** works because typed risk lets you pick the right tool: async/state needs runtime; contract drift needs schema diffing; proof weakness needs mutation thinking. Untyped risk → exhaustive review.
- **The high-value-signals catalog is the highest-leverage single asset** — these are war-story-derived patterns. Origin notes are intentionally omitted; the patterns stand on their own.
- **"Tests that are green but shallow"** is the entry point that bridges to the `mutation-scout` mode — when latent-hunt finds shallow tests, mutation-scout is the next mode.
- **Subagents are first-class** — the substantive guidance ("split by disjoint risk surface, not arbitrary file chunks") is real craft and stays.
