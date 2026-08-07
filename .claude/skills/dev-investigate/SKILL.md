---
name: dev-investigate
description: >-
  Investigate, prove, fix, and verify bugs across the full lifecycle. Picks the
  right lane (direct fix vs full evidence investigation vs latent-bug hunt vs
  mutation pressure-test vs PR fix interrogation vs recurring autonomous loop)
  for the situation. Triggers on "investigate this bug", "is this PR actually a
  fix", "hunt for hidden bugs", "pressure-test these tests". Do NOT trigger for
  greenfield design questions, code review without a bug, or PR
  comment-and-approve workflows — use `dev-fresh-eyes` for design critique and
  `dev-review` for general PR review. Do NOT trigger for "turn on Duck Hunt" or
  recurring autonomous bug-hunt activation — use `dev-duck-hunt` (the thin
  wrapper that owns scheduling + history); the per-cycle workflow lives in this
  skill's `recurring-hunt` mode.
version: 0.1.0
category: Troubleshooting
display_name: Investigate
tagline: 'Investigate, prove, fix, and verify bugs across the full lifecycle.'
packs:
  - dev-pack
icon: 'phosphor:MagnifyingGlassPlus'
when_to_use: >-
  Reach for this when something's broken, suspicious, or just not behaving the way
  it should, and you want it genuinely understood and fixed — not patched on a
  guess. It sizes the work to the situation on its own: a quick direct fix when
  the cause is obvious, a full evidence-backed investigation when it isn't, a hunt
  for bugs that haven't bitten yet, a pressure-test of whether your tests would
  even catch the regression, or a check on whether a PR truly fixes what it
  claims.


  The throughline is proof — you come away knowing *why* it happened and that it's
  actually resolved.
modes:
  - name: triage-and-fix
    job: Direct lane for a confirmed, reproducible bug — fix shape, implementation, proof.
  - name: evidence
    job: Evidence-first investigation when cause is unknown — reports, logs, traces before any fix.
  - name: latent-hunt
    job: Hunt for bugs that haven't bitten yet in a scoped surface.
  - name: mutation-scout
    job: Pressure-test whether existing tests would catch a planted regression.
  - name: pr-interrogate
    job: Verify a bug-fix PR is actually a root-cause fix (rootness + differential proof).
  - name: recurring-hunt
    job: One cycle of the recurring autonomous hunt (bootstrapped by dev-duck-hunt).
---

# Investigate

## Purpose

One entry point for investigating, proving, fixing, and verifying bugs. The skill chooses the right lane based on the user's intent and the available evidence — direct fix vs. full evidence investigation vs. latent-bug hunt vs. mutation pressure-test vs. PR-fix interrogation vs. recurring autonomous loop. Underneath, six modes share a vocabulary of atomic hypotheses, evidence lanes, lane status, rootness classification, severity rubric, and triage rubric — so output is consistent across lanes and reports compose cleanly.

## When to use

Pick a mode based on what the user is asking for:

- **`triage-and-fix`** — "investigate, fix, and prove this bug correctly" — the orchestrator that picks the smallest credible repro boundary, names the root-cause hypothesis before implementing, scales proof depth to risk.
- **`evidence`** — "run a full evidence investigation across support / runtime / error / replay; produce a developer handoff package" — for high-impact, hard-to-reproduce, or cross-system bugs.
- **`latent-hunt`** — "hunt for hidden bugs in this branch / PR / code slice" — proactive sweep for race conditions, stale state, retries, mutation survivors, contract drift; ranked risks with evidence.
- **`mutation-scout`** — "pressure-test whether the diff would catch realistic mistakes" — diff-scoped mutation thinking; 3-8 realistic mutants; identifies shallow tests.
- **`pr-interrogate`** — "does this bug-fix PR actually fix the bug?" — reproduce on base, prove on candidate, classify ROOT/PARTIAL_ROOT/SYMPTOM, issue GO / GO WITH FOLLOW-UPS / NO-SHIP verdict.
- **`recurring-hunt`** — "turn on Duck Hunt" / recurring autonomous bug sweep with stop conditions — fixes obvious low-risk issues in-loop; logs locally; delegates scheduling to the harness's recurring-task primitive.

If the user's intent is unclear, ask one targeted question rather than guessing the mode.

## Inputs

Mode-dependent. Each mode declares its own input expectations. The category-level inputs are:

- A bug statement, PR URL, branch name, or scoped code slice — whatever ties the investigation to something concrete.
- Available evidence sources (error-monitoring issues, task-tracker entries, support transcripts, session replay URLs, commit SHAs).
- Investigation constraints (read-only vs. permitted writes; whether posting back to your task-tracker or support system is in scope).

## First-time setup

This skill assumes a GitHub-shaped workflow and the `gh` CLI for PR inspection (used in `pr-interrogate` mode). Install `gh` and authenticate (`gh auth login`) before invoking that mode against real PRs.

Several modes can integrate with adjacent systems when configured: an error-monitoring system (Sentry MCP or equivalent) for the error lane, a task-tracker for backlog coordination, a support system for incident context, and a session-replay tool for the replay lane. These are *optional* — each mode degrades gracefully to direct evidence collection if the integration isn't present. Where the workflow value depends on cross-system posting (one update each to task tracker, team chat, support system, with identity and per-destination rendering rules), keep that craft separate from investigation — your own cross-system bug-comms workflow handles it, configured once per your stack rather than per invocation.

Remove or supersede this section after your environment is set up.

## Run

1. **Mode selection.** Map the user's request to one mode using the "When to use" guide. If the request fits two modes (e.g., "evidence + posting" → `evidence` followed by a handoff to your cross-system bug-comms workflow), name the chain explicitly before starting.
2. **Load shared references** that apply across modes:
   - `references/atomic-hypothesis-method.md` (every mode that produces hypotheses)
   - `references/output-format-contract.md` (every mode that produces user-facing output)
   - Plus mode-specific references (each mode names what it loads).
3. **Run the mode.** Mode files in `modes/` contain the run logic. Preserve craft moves verbatim from those files.
4. **Compose with siblings.** When a mode uncovers cross-cutting work — adjacent issues to defer (`dev-scope-deferral`), follow-up plans to pressure-test (`dev-fresh-eyes`), or cross-system updates to post (your bug-comms workflow, if you maintain one) — invoke the sibling rather than embedding that craft inside the mode body.

## Output

Each mode produces its own output shape. Common across modes:

- **Plain language first, technical detail second.** Lead with what the user/business cares about; raw IDs and signatures secondary.
- **Confidence stated explicitly.** Hypotheses carry low/medium/high confidence; abstain over forced certainty when evidence is incomplete.
- **No claim of 100% certainty.** Always include "what this cannot be" (ruled out by evidence) and "what remains unknown."
- **Plain file paths for local artifacts;** clickable URLs only for web resources (PRs, task-tracker entries, error-monitoring issues, support conversations).
- **"Affected Users: unknown (not tracked)"** by default unless attribution tracking is explicitly confirmed.

See `references/output-format-contract.md` for the full contract.

## Design Rationale

Why this skill is structured the way it is:

- **One category skill, six modes** — the underlying disciplines (evidence investigation, latent hunting, mutation pressure-testing, PR interrogation, recurring autonomous hunts, root-cause triage) cross-reference each other heavily in practice. One unified entry point with shared vocabulary removes the cross-skill coordination overhead while keeping mode boundaries crisp.
- **Modes share a unified vocabulary.** Atomic hypotheses, ROOT/PARTIAL/SYMPTOM, the unified triage rubric (FIX_NOW/HUMAN_DECISION/DEFER/DISMISSED), lane status, severity — these recur across modes with high consistency in the source prompts. Promoting them to shared references prevents drift and keeps reports composable across lanes.
- **Cross-cutting craft lives in standalone skills, not modes.** `dev-scope-deferral` and `dev-fresh-eyes` are invoked from inside investigate modes when needed, and cross-system bug posting (if you maintain a separate workflow for it) stays out of these modes too. This keeps modes focused — they don't redefine cross-system posting or pre-prod expansion rules — and lets the standalone craft serve other category skills as the library grows.
- **Tool-specific lanes are not modes.** Session replay, error-monitoring queries, independent-reviewer challenger passes — these are tool-wrappers, not investigation strategies. Modes reference them as "the replay lane" / "the error lane" / "the challenger lane" without embedding the tool integration. When a tool-specific wrapper skill is available, the modes call out to it; otherwise the relevant MCP / CLI / browser tooling is invoked directly.
- **Recurring-hunt delegates scheduling to the harness's recurring-task primitive.** Embedding scheduling in the mode would duplicate and conflict with whatever the harness already offers (Claude Code: `/loop`; elsewhere: cron, scheduled-tasks servers). The mode focuses on per-cycle behavior (target slice, method rotation, fix flow) and lets the scheduler handle when to wake.
- **The shared `output-format-contract.md` reference encodes the workspace's output preferences** (plain language first, raw IDs secondary, no "0 affected users" without confirmed tracking). This way preferences live in one place and propagate to every output.
- **No subagent restriction.** Modes parallelize via subagents where the harness supports them, when independent work splits cleanly, following latent-hunt's substantive guidance (single-agent harnesses: run the lanes sequentially): split by disjoint risk surface (not arbitrary file chunks); concrete question + clear ownership per lane; don't ask multiple agents to re-review the same surface.

## References

Cluster-shared references (loaded across modes):

- `references/atomic-hypothesis-method.md` — observed facts / hypotheses with confidence / ruled out / unknowns; disconfirming-first; "what this cannot be"
- `references/evidence-lanes.md` — Support / Runtime / Error / Replay lane vocabulary
- `references/lane-status-vocabulary.md` — complete / partial / blocked + blocker reason + fallback attempted
- `references/user-attribution-rule.md` — "unknown (not tracked)" default; user-count labeling rules for error-monitoring data
- `references/differential-proof.md` — base fail / candidate pass; same payload hash; 4-item bar
- `references/rootness-classification.md` — ROOT / PARTIAL_ROOT / SYMPTOM with criteria
- `references/pr-overlap-check.md` — exact / partial / no overlap rules; optional context-brief convention
- `references/lane-selector.md` — escalation / lane menu (static reasoning / tool / proof / runtime / challenger)
- `references/defect-families.md` — async/state, retry/idempotency, cache/SWR, perf, contract/schema, proof weakness, UI handoff
- `references/latent-bug-signals.md` — high-value catalog of latent-bug patterns
- `references/severity-rubric.md` — P0 / P1 / P2 / P3 with criteria
- `references/triage-rubric.md` — FIX_NOW / HUMAN_DECISION / DEFER / DISMISSED (unified, terminal-states-only)
- `references/status-vocabulary.md` — hypothesis / invariant / lane status terms (no aliases)
- `references/non-ship-gate.md` — five close-out conditions; code+test+runtime triplet
- `references/output-format-contract.md` — plain file paths; web URLs only; plain-language-first; raw-IDs-secondary
- `references/blast-radius-taxonomy.md` — likely-now / possible-watch / unknown-needs-simulation; subsystem clusters; authority-weighted priorities
- `references/hunt-method-menu.md` — lanes for recurring/latent hunts (risk-map, blast-radius, static, proof-gap, async/retry/contract, runtime smoke, browser, library docs)
- `references/disciplined-bug-arc.md` — six-step skeleton (case init → evidence → atomic hypotheses → implement+verify with differential proof → blast-radius+regression → close with rootness)

## Templates

- `templates/handoff-package.md` — full evidence-investigation handoff (used by `evidence` mode)
- `templates/pr-interrogation-verdict.md` — GO / GO WITH FOLLOW-UPS / NO-SHIP × ROOT / PARTIAL / SYMPTOM × Confidence (used by `pr-interrogate` mode)
- `templates/recurring-hunt-session-log.md` — Duck-Hunt-style session log structure (used by `recurring-hunt` mode)

## Examples

`examples/` is empty for v0.1. Single examples tend to mis-train the skill more than missing examples do — populate from real verification runs once several strong exemplars are available.

## Related skills

- `dev-fresh-eyes` — invoked from `recurring-hunt`'s Fix Flow and from `triage-and-fix` when a fix plan needs a skeptical second pass.
- `dev-scope-deferral` — invoked from any mode when adjacent valid follow-up work surfaces. Writes a deferred-investigation note under the configured notes directory.
- Your cross-system bug-comms workflow (if you maintain one) — invoked from `evidence` mode when investigation findings need to be posted across systems (task-tracker, team chat, support-system internal note) in one coordinated pass. Keeping that posting craft separate from investigation is intentional; this skill produces the findings, the comms workflow consumes them.
- Your harness's recurring-task primitive — `recurring-hunt` delegates scheduling to it. On Claude Code the typical invocation is `/loop 30m /dev-investigate recurring-hunt`; on other harnesses use cron / a scheduled-tasks MCP / manual re-invocation.

Tool-specific lanes call out to MCP / CLI tooling directly when no wrapper skill is present: session-replay via browser-use or Chrome MCP, error-monitoring via the relevant MCP (Sentry is the assumed default), independent-reviewer challenger lanes via a fresh-context subagent (or a separate coding tool if one's wired up). Manual blast-radius reasoning lives in `references/blast-radius-taxonomy.md`.
