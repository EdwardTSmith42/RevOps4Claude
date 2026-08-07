# Disposition vocabulary

The canonical labels for what happens to a source (in `from-prompt` and content-driven sub-modes) or a finding (in `enhance` mode). Pick from this fixed list — the discipline of choosing forces clarity. Aliases like *validated* / *completed* / *done* cause cross-run drift; use the canonical labels.

## Canonical dispositions

### `SHIP NOW`

The source converts directly to a destination with minimal adaptation. Used when:

- The source is already well-shaped for the target format.
- No script / MCP / runtime dependencies require adaptation.
- The craft moves preserve cleanly.

Used in `from-prompt` (and content-driven sub-modes) for sources that port faithfully. Most prompt-based skills (per `prompt-based-vs-tool-wrapper.md`) end up here.

### `ADAPT`

The source converts but with documented changes — typically idiom adaptation from one runtime to another. Used when:

- Legacy patterns need current idioms (custom heartbeats → `/loop`, sandbox-era subagent restrictions dropped, hard-coded `~/.codex/...` paths → relative or env-driven).
- The runtime model differs but the craft transfers (e.g., RRULE-based heartbeats are Codex-specific; `/loop` is Claude-native; the *intent* of *run every 30 minutes with stop conditions* is preserved).
- The user's stance has shifted (e.g., subagent restriction was Codex sandbox-era; user prefers subagents in Claude Code).

The decision log records the adaptation with rationale. Adaptations should appear in the converted skill's Design Rationale section.

### `MERGE`

The source merges with one or more sibling sources into a single destination. Used in cluster conversions when:

- Multiple sources share heavy reference load and job-shape overlap.
- They become modes of one category skill rather than separate skills.
- The "shared load" heuristic fires (per `../../_shared/references/skill-vs-mode-vs-reference.md`).

Each merged source gets a thin stub decision-log entry pointing at the consolidated entry.

### `SPLIT`

The source splits into two or more destinations. Used when:

- The source does two distinct jobs that have different reference loads, output shapes, or invocation patterns.
- Forcing them into one skill would either bloat the prompt or distort routing.
- The split is *across* the source's content (different parts go different places), not duplication.

Each destination gets its own decision-log entry; the source's stub describes the split rationale.

### `DEFER`

The source is **out of scope for the current run** but still valuable. The decision log captures:

- What the source does.
- Why it's deferred (depends on a Codex script not yet ported; depends on an MCP not yet available; the user wants to revisit after a different cluster lands).
- What would unblock conversion (*"when the Sentry MCP integration is ready"* / *"when DeliveryOps is converted"*).

The original source remains untouched at its source path. No work is performed in the current run beyond the decision-log entry.

### `DEFER + SALVAGE`

Hybrid disposition for sources whose **orchestration role can't be preserved** (e.g., Codex bash wrapper has no Claude Code equivalent yet) **but whose embedded craft IS transferable** (e.g., epistemic rules, taxonomies, vocabulary, output formats).

Used in `from-prompt` mode when:

- The source is primarily a tool wrapper (script invocation glue, MCP integration, runtime auth flows).
- The script / MCP isn't ported yet, so the orchestration role can't ship.
- BUT the source contains valuable rules (user-attribution rules, noise filters, war-story-derived patterns, output-format contracts) that should not vanish.

The salvage step extracts the transferable rules into shared references in the cluster being built (e.g., `dev-investigate/references/user-attribution-rule.md`). The orchestration role waits for a separate run when the dependency is available.

The decision log records:

- What was deferred (and why).
- What was salvaged (with destinations).
- What would unblock the deferred orchestration role.

This pattern came up for **6 of 14 sources** in the v0.1 bug-investigation pilot. Expect it to be common for clusters with tool-wrapper-heavy ratios.

### `ARCHIVE`

The source is preserved as historical record but does NOT convert. Used when:

- The source is genuinely obsolete (the job it does isn't needed anymore).
- A newer pattern subsumes it.
- The user wants the artifact preserved without active conversion.

The decision log explains why it's archived. The original source remains untouched.

### `BONUS ONLY`

Used in product-context conversions (e.g., user-facing copy / marketing content): the source becomes promotional / supplementary content rather than a working skill. Rare in skill conversion; documented for vocabulary completeness.

### `BACKEND ONLY`

Used in product-context conversions: the source becomes backend-only logic (no user-facing surface). Rare in skill conversion; documented for vocabulary completeness.

## `enhance` mode dispositions

When operating over existing skills (not converting from legacy prompts), `enhance` mode adds these:

### `CONSOLIDATE`

Two or more existing skills (or references) merge or promote to a shared location. Used when:

- The two-skill threshold has fired (same content loaded by 2+ skills for the same reason).
- Sibling skills with shared vocabulary and reference load should become modes of a category skill.
- Duplicated reference content should promote to `_shared/references/`.

### `AUGMENT`

An existing skill gains missing structural elements without changing its core behavior. Used for:

- Adding negative triggers to descriptions.
- Adding Design Rationale sections.
- Adding `source-prompts:` frontmatter for traceability.
- Filling in missing examples (per `../../_shared/references/example-rules.md` — only when 5–10 strong exemplars are available).

### `NO-OP`

Finding noted in the audit but no action warranted. Used when:

- A look-alike pair turns out to be intentionally distinct (different defining nuances).
- Drift from a Codex-era pattern is acceptable for the user's workflow.
- Promoting the reference would create more drift than it prevents.

The decision log records the finding and the no-op rationale, so future audits don't re-surface it without context.

## Anti-patterns / aliases to avoid

Do not use these — they cause drift:

- ❌ `validated` (use `confirmed` for hypotheses, `pass` for invariants)
- ❌ `completed` (means different things to different readers)
- ❌ `done`, `finished`, `closed` — none specific
- ❌ `partial` (use `partially_confirmed` for hypotheses, `partial` only for lane status)
- ❌ `TODO` or `later` as a disposition — use `DEFER` with explicit unblocking conditions

## How to pick

When unsure between dispositions:

- **`SHIP NOW` vs `ADAPT`:** Are you changing the source's runtime assumptions or just translating format? Format-only → `SHIP NOW`. Runtime / idiom changes → `ADAPT`.
- **`MERGE` vs `SPLIT`:** Does the source share reference load with siblings? Yes → `MERGE` candidate. Does it do two distinct jobs internally? Yes → `SPLIT` candidate. (Both can be true: split a source AND merge each half with different siblings.)
- **`DEFER` vs `DEFER + SALVAGE`:** Does the source contain transferable rules (vocabulary, taxonomies, output contracts) that other skills want to load? Yes → `SALVAGE` the rules now, defer the orchestration. No → straight `DEFER`.
- **`ARCHIVE` vs `DEFER`:** Will the work resume? `DEFER` if yes, `ARCHIVE` if no.

## Used by

- `from-prompt` mode — Phase 3 (Plan destination).
- `from-content`, `microtool-from-content`, `microtool-from-job` — destination / disposition decisions.
- `enhance` mode — Phase 3 (Surface decisions).
- `consolidate` mode — when consolidation decisions need labels.
- Decision-log templates throughout.

## Source

Vocabulary expanded from the original Cowork-flavored skillify (`SHIP NOW / ADAPT / MERGE / ARCHIVE / BONUS ONLY / BACKEND ONLY`) based on patterns surfaced in the v0.1 bug-investigation pilot. The pilot added `DEFER / DEFER + SALVAGE / SPLIT / CONSOLIDATE / AUGMENT / NO-OP` formally.
