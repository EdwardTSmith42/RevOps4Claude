# Shared review rubric — categories every slice reviewer carries

Malleability note: the category list is canonical as a floor, not a ceiling —
campaigns add addenda when new defect classes emerge (that mechanism is part of
the methodology). The per-category framing below is adaptable to the stack.

Each reviewer evaluates its slice against all categories, plus slice-specific
focus questions from the orchestrator.

- **Correctness & contract fidelity** — does the code do what its own comments,
  types, and API docs claim? Wire types vs runtime shapes; controller status
  codes vs framework behavior.
- **Contract drift** — generated artifacts vs source of truth; client types vs
  server responses; prompt text vs what tools/validators actually accept
  (prompt-contract drift is its own sub-class for AI-facing surfaces).
- **Seam & boundary behavior** — what happens at the joints: session filters,
  middleware, scope expansion, serialization layers. Unit-tested config can be
  dead at runtime; test through the real entry path.
- **Failure-window hygiene** — create-then-link windows, partial writes,
  compensation on failure, what a retry does (does it accumulate orphans or
  converge?).
- **Concurrency & state ordering** — optimistic-concurrency tokens, claim
  semantics, stale-claim recovery, last-write-wins exposures.
- **Schema evolution safety** — what happens to persisted data when the
  canonical schema moves; forward-compat posture; version stamps on cached
  artifacts.
- **DB ownership & migration hygiene** — tables/columns on the right object
  boundary; migration reversibility; backfill precision (timestamp truncation
  vs equality guards).
- **Workload realism** — behavior at realistic scale: large payloads, many-item
  documents, render latency, pagination. Performance-sensitive slices carry at
  least one workload-realistic check.
- **Dead code & least surprise** — config nothing reads, files nothing imports,
  names that promise behavior the code doesn't have. Dead config misdirects
  the next reader; that is a real defect.
- **Test trust** — can each test fail? Does it model the live boundary shape or
  a normalized convenience shape? Are mocks easier than reality?
- **Security-adjacent contract checks** — cross-tenant probes returning 404 vs
  403, scope checks before byte access, validator/render policy mirrors.
  (Frame findings as functional-contract findings, not as a security audit.)
- **Docs & operational truth** — README claims vs behavior, deploy notes vs
  pipelines, alarms that consume the healthchecks they reference.
