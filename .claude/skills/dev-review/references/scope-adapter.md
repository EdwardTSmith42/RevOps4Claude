# Scope adapter

The cluster-wide design for variable-scope review (commit / branch slice / PR / portfolio) with sub-agent fanout when surface is too large to reason about together. The user's central design ask for the `dev-review` cluster.

## Variable scope

`dev-review` modes are **not PR-only.** They adapt to the natural unit the user wants reviewed:

| Scope | Detection | Baseline | Use cases |
|---|---|---|---|
| **single commit** | Single SHA referenced; `git show <SHA>` | `<SHA>~1` (or rebase base if mid-rebase) | "Check this commit" |
| **commit range** | Range referenced (`<base>..<head>` or last N commits) | The named base | "Review the last 5 commits" |
| **branch slice** | A subset of files in a branch | `origin/develop` (default) or named base | "Review only the auth-related changes in this branch" |
| **branch** | Full branch | `origin/develop` (default) | "Check this branch" |
| **PR** | PR number / URL provided | PR base ref (`origin/develop` if base is develop; otherwise `origin/<baseRefName>`) | "Check this PR" |
| **portfolio** | Multiple open PRs (digest territory) | N/A — each PR has its own base | "Rank our open PRs" |
| **existing slice** | No diff; review code that's risky / old / confusing | N/A | "Manifesto-review the auth module" |

Detection heuristics: if user names a SHA → commit; range syntax → range; named subset → slice; "this branch" → branch; PR number/URL → PR; "all open PRs" / "today's queue" → portfolio.

When scope is ambiguous, ask one targeted question rather than guessing.

## Sub-agent fanout

When the changed surface is large (>1 disjoint risk surface AND surface is too large to reason about together — soft heuristic), fan out to sub-agents.

### When to fan out (soft heuristic — agent uses judgment)

The fanout question is: *"Can I reason about this entire change in one pass without losing context, or are there independent areas that benefit from focused review?"*

Soft signals favoring fanout:
- Multiple distinct subsystems touched (frontend + backend + infra; or feature A + feature B).
- Cross-cutting concerns (auth + data layer + UI).
- Diff exceeds what fits in working context comfortably (varies by model).
- Different reviewing skills needed for different areas (e.g., frontend UX vs backend reliability).

Soft signals AGAINST fanout (review serially):
- Tight, focused change (single feature, single file, small commit).
- Tight cross-cutting integration where you need full context simultaneously.
- Small enough that the overhead of fanout exceeds the focused-context benefit.

**The user articulated this preference: heuristic-driven, not hard threshold.** The agent uses judgment per change.

### Fanout architecture (hybrid: full diff summary + assigned slice in detail)

When fanout fires, each subagent gets:

1. **Full diff summary** (concise): high-level overview of the entire change so the subagent has cross-cutting awareness.
2. **Assigned slice in detail**: the specific area this subagent is reviewing (full files, line-level diff, related call-sites).

Subagent reviews their assigned slice with cross-cutting awareness from the summary. Reports findings in standard shape. Parent reconciles findings across all subagents.

### Disjoint risk surfaces

Subagent assignments should split by **disjoint risk surface** — not arbitrary file chunks:

- ✅ "Frontend changes" / "Backend changes" / "Infra changes" — distinct subsystems
- ✅ "Auth changes" / "Data layer changes" / "UI changes" — by concern
- ✅ "Migration changes" / "Application code changes" — by lifecycle phase
- ❌ "Files 1-10" / "Files 11-20" — arbitrary chunking loses context

If a "slice" can't be cleanly named, the cut is wrong. Re-cut.

### Reconciliation

After all subagents return, the parent agent:

1. **De-duplicates findings** — same issue surfaced by multiple subagents collapses to one entry.
2. **Surfaces conflicts** — if two subagents disagree on severity or recommendation, flag explicitly.
3. **Aggregates evidence** — multiple subagents pointing at the same area = stronger signal.
4. **Prioritizes for the final report** — uses cluster's severity rubric (`reliability-rubric.md`) for ranking.
5. **Produces unified output** — the consumer reads ONE report, not N subagent transcripts.

Cross-cutting issues that span multiple subagent slices (e.g., contract drift between frontend and backend) deserve special attention during reconciliation; they're often what fanout is trying to catch.

## Per-mode scope handling

Different modes interact with scope differently:

- **`ship-gate`** — naturally PR-shaped; adapts cleanly to commit / range / branch via the table above. Fanout fires when many subsystems touched.
- **`checkpoint`** — typically commit / branch-slice scoped (milestone work in progress). Fanout fires when the milestone work touches many files (especially during monolith-sweep step).
- **`manifesto-review`** — any-scope including existing-slice (no diff). Fanout per subsystem when reviewing a large area.
- **`brief`** — scope determines profile (small / medium / large) per the brief mode body. Fanout for large changes when distinct subsystems need different brief sections.
- **`smoke-qa`** — branch-scoped by nature. Fanout per route cluster (auth vs unauth, by feature) when many routes affected.
- **`digest`** — portfolio-scoped; uses its own per-PR fanout (each subagent reviews one PR; parent ranks).

## Used by

- Every mode of `dev-review` except (partly) `digest` (which has its own portfolio fanout pattern).

## Malleability note

**Canonical:** the variable-scope coverage (any unit a user wants reviewed) and the hybrid fanout architecture (full diff summary + assigned slice). These are the user's articulated design.

**Adaptable:** the soft heuristics for when to fan out — these will refine with real-use signal. The "disjoint risk surface" principle is canonical; the specific axes (subsystem / concern / lifecycle / etc.) are examples that adapt per change.

