---
name: dev-branch-memory
description: >-
  Capture, review, and consolidate branch-scoped implementation memory across
  agent threads. Use when the user wants periodic/heartbeat memory for
  architectural decisions, refactors, source-traceable process choices, reviewer
  context, or PR-time "dream" consolidation for a branch.
version: 0.1.0
display_name: Branch Memory
tagline: 'Capture, review, consolidate branch-scoped memory across threads.'
category: Planning
packs:
  - dev-pack
icon: 'phosphor:GitBranch'
when_to_use: >-
  Use for periodic / heartbeat memory on a branch — architectural decisions,
  refactors, source-traceable process choices, reviewer context, or PR-time
  'dream' consolidation. Lets multiple agent threads working on the same branch
  hand off without losing state.
modes:
  - name: capture
    job: Append decision-trail entries during branch work.
  - name: dream
    job: PR-time consolidation of the branch's memory.
  - name: review
    job: Read back the branch memory for reviewer or handoff context.
---

# Branch Memory

## Overview

Use this skill to preserve the decision layer of branch work: why a change took this shape, what alternatives were considered, which existing patterns were kept or changed, what evidence moved the plan, and what a future reviewer cannot recover from the diff alone.

A strong branch memory should read like a concise decision trail, not a dry technical manual. It should make the human reasoning visible: what the user cared about, what the agent proposed, what was rejected or narrowed, and why the final path won. This matters because future reviewers and agents are most likely to repeat the tempting routes that are absent from the diff.

This is branch-local memory, not a transcript archive and not permanent SOP promotion. Capture evolving notes during implementation, then dream them into reviewer-ready branch context near PR time.

## Modes

- `capture`: write one concise memory note from the current thread or heartbeat.
- `dream`: consolidate branch notes into final branch memory and PR-brief input.
- `review`: inspect existing branch memory for gaps, contradictions, missing source refs, or weak reviewer context.
- `promote`: propose durable SOP, lesson, or architecture-memory updates after branch closeout. Do not auto-promote.

V1 focuses on `capture` and `dream`. Use `review` opportunistically before PR, and treat `promote` as proposal-only.

## First-time setup

The bundled Python scripts under `scripts/` are invoked with `python3 <skill-dir>/scripts/<name>.py`, where `<skill-dir>` is wherever this skill is installed on your machine (for example, `~/.claude/skills/dev-branch-memory/` on Claude Code; substitute your harness's skills directory). Resolve the path once at the start of any branch-memory work so subsequent calls in the same session can reuse it. The scripts read `--repo "$PWD"` for git context and are otherwise cwd-agnostic.

## Storage

Resolve the branch memory directory with:

```bash
python3 <skill-dir>/scripts/resolve_branch_memory_dir.py --repo "$PWD" --mkdir
```

Default storage is workspace-local:

```text
<repo>/.local/branch-memory/<repo-key>/<branch-slug>/
```

Set `BRANCH_MEMORY_HOME` to use a shared local/private root across worktrees. In automation or heartbeats, prefer a writable workspace path if the private path is unavailable.

Expected layout:

```text
branch.md
manifest.json
memories/
dream/
```

## Where memories live — the user's call

The storage location is a user decision, made once per repo and remembered. On first use in a repo, suggest a smart default and get a confirm before writing anything:

- **Default suggestion:** the resolver's repo-local root (`<repo>/.local/branch-memory/`) — branch-named subfolders, typically untracked (offer to add `.local/` to the repo's gitignore if it isn't).
- **Tracked-in-repo alternative:** some teams keep memories in version control as shared context — a folder like `<repo>/work-process/<branch-name>/` committed alongside the code. Set `BRANCH_MEMORY_HOME` to any base path to get this; the resolver honors it.
- Record the choice in the repo's memory manifest so future sessions don't re-ask.

Tracked vs untracked is a real trade-off (shared reviewer context vs repo noise) — name it in one sentence when asking; don't decide it silently.

## Capture Workflow

1. Resolve the branch directory and inspect existing `manifest.json`, `branch.md`, and recent `memories/*.md`.
2. Before writing, decompose the current thread/checkpoint into distinct decision clusters. If the thread is long, if memory has not been captured for several meaningful decisions, or if the previous memory was recent but covered a different decision lane, write multiple focused memories instead of one broad note. Prefer one memory per distinct source-of-truth, contract, refactor, risk, verification, or deferred-followup decision.
3. Reconstruct the decision arc for each cluster before drafting:
   - the user concern or product pressure that made the question matter
   - the agent proposal or initial path
   - alternatives, tempting shortcuts, or routes not taken
   - the user correction or agreement that moved the plan
   - the final decision and the reviewer-facing rationale
4. Decide whether there is new branch memory worth capturing. Capture only material decisions or context:
   - refactor or architecture decisions
   - source-of-truth, contract, or boundary choices
   - pattern kept vs changed
   - alternatives rejected because they added prompt/tool complexity, duplicated paths, weakened source-of-truth clarity, or hid important user intent
   - evidence that changed the approach
   - temporary instrumentation and keep/discard decision context
   - verification/risk decisions
   - deferred but valid follow-up context
5. Do not restate durable instructions as new memory. Do cite durable sources when they shaped the decision.
6. Write timestamped notes with `write_memory.py`, then validate each new file.

Style requirements for each memory:
- Start the body with `TL;DR: ...` in plain language.
- Prefer human-impact summaries over implementation-mechanism summaries, especially in `summary`.
- Keep technical detail precise, but explain why it matters before diving into file mechanics.
- Include the conversational rationale when it materially shaped the outcome. Paraphrase the user's concern and the agent's proposal in plain language; avoid quoting long transcript excerpts.
- Include `Options Considered` or `Routes Not Taken` when a tempting alternative was rejected. Explain why it was rejected so future reviewers do not rediscover the same bad path.
- For `contract`, `source-of-truth`, `risk`, and safety-related memories, include a `Risk / Invariant` section that says what future changes must not break.
- Separate shipped behavior from deferred behavior explicitly when both appear in the same decision lane.
- Use source refs as traceability, not as a substitute for plain-language explanation.
- Do not include hidden internal chain-of-thought. Capture observable reasoning from the conversation, evidence, code inspection, tests, and explicit user/agent decisions.

```bash
python3 <skill-dir>/scripts/write_memory.py \
  --repo "$PWD" \
  --kind architecture-decision \
  --summary "Kept transformer output stable while moving validation upstream" \
  --status active \
  --confidence provisional \
  --tag flow-server \
  --source-ref "AGENTS.md :: verify before done shaped proof plan" \
  --related-file packages/flows/src/example.ts \
  --body-file /tmp/branch-memory-body.md
```

Session attribution: the script auto-detects a session/thread id from `CODEX_THREAD_ID` or `CLAUDE_SESSION_ID` when either is exported. On harnesses that export neither, pass `--thread-id` explicitly — otherwise memories record `thread_id: unknown` and lose the source-traceability the review/dream modes depend on.

If there is no meaningful new decision, say so and do not create filler memory.

## Parallel Review Guidance

For long, high-context branches, subagents may review independent decision lanes before capture. Only use this when it improves quality or coverage, and give each agent a fork of the thread context plus a bounded lane such as "analytics source-of-truth decisions" or "AdminJS navigation decisions." The parent agent remains responsible for reconciling overlap, preventing duplicate memories, and ensuring final notes do not contradict each other.

## Confidence Guidance

- Use `verified` only when the specific memory decision has direct proof, not merely because the branch compiled.
- Use `supported` when implementation and tests support the decision but acceptance/browser/runtime proof remains.
- Use `provisional` for plans, architecture direction, or decisions not yet exercised.
- Use `unknown` when preserving context despite incomplete evidence.
- Use `reversed` only for a decision that was explicitly undone or proved wrong.

## Dream Workflow

1. Resolve the branch directory.
2. Read `manifest.json`, `branch.md`, all `memories/*.md`, current `git status`, and current `git diff --stat`.
3. Reconcile notes into:
   - `dream/final-branch-memory.md`: complete local/private branch story.
   - `dream/reviewer-brief-input.md`: sanitized PR-safe input for your PR-brief workflow (e.g., `dev-PR` if installed, or any equivalent PR-authoring skill or playbook you've wired up).
4. Preserve useful superseded decisions when they explain why the final diff looks the way it does.
5. Separate deferred follow-ups from shipped behavior.
6. Update `manifest.json` after writing dream artifacts.

Read `modes/dream.md` before doing the consolidation.

## Source Traceability

Branch memory should cite sources that materially shaped decisions:

- user instruction or correction
- compact paraphrase of the user/agent conversation that changed the route
- `AGENTS.md`
- private SOP path
- skill path
- codebase precedent
- failing/passing test
- runtime log or scenario evidence
- PR/review/comment link

Use source refs to trace both good and flawed decisions. Cite the source and summarize how it shaped the local decision; do not copy whole policy sections.

Read `references/source-traceability.md` for the source-ref format.

## Guardrails

- Keep branch memory private/local by default.
- Do not include secrets, tokens, customer private data, or long transcript excerpts.
- Do not store private local file paths in `reviewer-brief-input.md`; sanitize them for PR use.
- Do not promote branch memory into SOPs, `AGENTS.md`, or architecture memory without explicit user approval.
- Do not use branch memory as the active branch registry.
- Do not create notes for routine edits visible from the diff.
- Mark uncertain decisions as `confidence: provisional` or `unknown`; do not overstate evidence.

## References

- Format: `references/memory-format.md`
- Capture mode: `modes/capture.md`
- Dream mode: `modes/dream.md`
- Review mode: `modes/review.md`
- Source tracing: `references/source-traceability.md`

## Scripts

- `scripts/resolve_branch_memory_dir.py`: resolve repo, branch, slug, and memory directory.
- `scripts/write_memory.py`: create a timestamped memory note and update the manifest.
- `scripts/update_manifest.py`: rebuild manifest from files on disk.
- `scripts/validate_memory.py`: validate frontmatter and expected branch-memory fields.
