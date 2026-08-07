# Mode: recurring-hunt

Part of the `dev-investigate` skill. Selected when the user wants a recurring autonomous bug-hunt loop on a branch / feature / scoped code surface — phrasings like "turn on Duck Hunt," "recurring bug sweep on this branch," "megabranch hardening in chunks," or "autonomous low-risk fix loop."

**Two invocation paths:**
- **Via `dev-duck-hunt` skill (recommended for first activation):** invoking `dev-duck-hunt` bootstraps scope detection + history doc + recurring scheduling, then delegates per-cycle work here.
- **Direct:** schedule this mode via your harness's recurring-task primitive (Claude Code: `/loop 30m /dev-investigate recurring-hunt`; elsewhere: cron, a scheduled-tasks MCP, or manual re-invocation each cycle) — when activation has already happened (or for explicit cadence pinning).

The mode body covers per-cycle behavior; the harness's recurring-task primitive handles cadence and stop conditions.

## Cross-session history (the mechanism behind repeat-avoidance)

Each cycle reads + writes a persistent history doc at the path the `dev-duck-hunt` install configures (typically under `~/.claude/notes/duck-hunt/<repo-slug>/<branch-slug>/history.md`). The schema is owned by this skill's `references/history-format.md` (dev-duck-hunt, the bootstrap wrapper, cites it). The history doc is the canonical anti-repeat record across sessions, worktrees, and machine restarts.

**Pre-cycle (before picking a method):**
1. Open history doc (create from template if absent).
2. Read **Cold zones** (recent methods × areas with no findings) — skip these within freshness window (default 7 days).
3. Read **Hot zones** (areas with `unclear` / `confirmed` suspicions) — priority for revisit with a different method.
4. Read **Pending hunt queue** — pull next item if applicable.
5. Read most recent cycle entry — what method was last used, on what slice.
6. **Branch advancement check:** if HEAD moved past previously-hunted commits, mark new commits as un-hunted (priority candidates).

For richer cross-session context (when prior sessions have content not yet canonicalized in history.md), optionally search prior session transcripts for `"duck-hunt <repo> <branch>"` — if your harness exposes such a capability; otherwise skip, history.md is canonical.

**Post-cycle (before releasing the lock):**
1. Append a new "Cycle <N>" entry to the per-cycle log section.
2. Update Cold zones (areas covered with no findings).
3. Update Hot zones (areas with new suspicions).
4. Update Pending hunt queue (mark items done, add follow-ups).
5. Update top-level metadata (totals, Last updated).
6. Increment `Consecutive empty passes` if no FIX_NOW / HUMAN_DECISION / DEFER produced; reset to 0 otherwise.

## Job

Run one bug-hunt cycle: reopen session log, claim the lock, refresh branch state, choose a target slice and method, run narrow evidence-rich hunt methods, classify suspicions, triage to terminal states, fix obvious low-risk bugs in-loop, and update the session log before releasing the lock.

## Run

### Activation (first cycle only — when user turns on the loop)

1. **Determine the target surface.**
   - If the user names a feature, directory, route, or subsystem, use that.
   - Otherwise default to the current branch diff against `origin/develop` when available.
   - If `origin/develop` is unavailable, use the narrowest sensible base such as the tracked branch, `origin/main`, or a merge-base-backed diff.

2. **Check for an existing active session for the same repo and branch.** Reuse it instead of creating a duplicate.

3. **Create or update the session log** using `../templates/recurring-hunt-session-log.md`.
   - If the canonical private path is read-only, create the writable session log under a workspace-safe path (e.g. `.local/recurring-hunt/...` or `/tmp/recurring-hunt/...`); never fail the cycle on path issues.
   - Record: start time, stop time defaults, target scope, diff base, session-lock defaults, initial hunt queue.

4. **Run one cycle immediately.** Don't wait for the first scheduled wake-up.

5. **Schedule via the harness's recurring-task primitive.** On Claude Code, recommend `/loop 30m /dev-investigate recurring-hunt` (or their preferred cadence); elsewhere, cron / a scheduled-tasks MCP / manual re-invocation each cycle. The mode does not embed its own scheduling.

### Stop conditions

These come from the scheduler, but the mode also self-checks at the start of each cycle:
- Session expired (default: 12 hours after start).
- Five consecutive empty passes (default; tunable).
- User said stop.

When any stop condition is reached, **the cycle ends and the loop should be cancelled.** Do not keep emitting wake-ups to report that the session is already finished.

### Per-cycle behavior

Each cycle runs this sequence:

1. **Reopen the writable session log.**
2. **Claim the session lock before doing more work.**
   - If `Pass state` is already `running` and `Lock expires at` is still in the future: record `skipped_active_lock` and end the cycle without changing the empty-pass counter.
   - If the lock is stale: record `stale_lock_reclaimed`, then continue.
   - Claim by setting: `Pass state: running`, `Pass trigger: immediate|scheduled|manual`, `Pass started at`, `Lock expires at` (default 60 min lock).
   - Refresh `Lock expires at` and `Last updated` before browser work, long-running validation, or challenger-review steps. **Use a tool-appropriate long wait for slow reviewers instead of repeated short polling** (10–15 minutes is acceptable when the tool is known to take that long).

3. **Refresh branch state:** current commit, diff summary, pending hunt queue, recent methods used.

4. **Choose one target slice.**
   - Pick from Hot zones / Pending queue / branch-advancement priority commits in the history doc.
   - Otherwise default to the next slice in scope (small diff: whole; medium: cluster; large megabranch: one cluster per pass).

5. **Pick methods + decide single-method-vs-fanout.**

   **Default: sub-agent fanout (2-3 disjoint defect families in parallel).** This compresses coverage per wall-clock minute. Spawn subagents for different defect-family lenses on the same slice:

   - One on **async / state / timing** (race conditions, missing await, retry / idempotency, lifecycle ordering).
   - One on **contract drift / schema mismatch / data shape** (server-types vs generated clients, prompt vs flow vs UI).
   - One on **cache / SWR / stale state** (mutate misuse, missing rollback, stale fan-out after writes).
   - Optionally a fourth lane (perf / proof-weakness / UI handoff) when slice complexity warrants.

   **Fall back to single-method-per-cycle when:**
   - Slice is small (<5 files / <100 lines) — fanout overhead exceeds benefit.
   - User explicitly requests single-method (`--no-fanout` flag in invocation).
   - Lane requires UI sign-in / approval (run sequentially instead).
   - The harness has no subagent support — run the same defect-family lenses as sequential passes over the slice; the lenses are the contract, parallelism is just the speed.

   **Rotate methods across cycles** — don't repeat the same method on the same slice in consecutive cycles unless suspicion is new (per Cold zones logic above).

   See `../references/hunt-method-menu.md` for the method catalog. **Prefer small, evidence-rich commands and scoped tests over whole-repo audits.**

6. **Reconcile fanout findings.** When subagents return:
   - De-duplicate findings across lanes (same issue surfaced by multiple subagents).
   - Surface conflicts explicitly (lanes disagree on severity / recommendation).
   - Aggregate evidence — multiple lanes flagging the same area = stronger signal.
   - Produce one classified list before triage.

7. **Classify each suspicion:** `confirmed` / `likely` / `unclear` / `dismissed`.

8. **Triage every credible issue** to one of: `FIX_NOW` / `HUMAN_DECISION` / `DEFER` / `DISMISSED`. See `../references/triage-rubric.md`. **Investigate until you can confidently land on one of these four terminal states.** "INVESTIGATE_LOCAL" is the in-progress signal that you're still investigating; it is not itself a terminal triage state.

9. **Execute the matching path** (Fix Flow, Local Investigation, Defer, or Dismiss — see below).

10. **Update the history doc** with the cycle entry per the Post-cycle protocol above (Cold zones / Hot zones / Pending queue / cycle log entry / metadata).

11. **Release the session lock in a finally-style closeout:** set `Pass state: idle`, clear or rewrite the lock fields, update `Last reviewed commit` and `Last updated`.

### Scope strategy

Choose slices small enough to reason about and validate manually:
- Small diff: review the whole changed slice directly.
- Medium diff: cluster by feature, directory, state owner, or shared helper boundary.
- Large megabranch: pick one related cluster per pass.
- Shared seam uncertainty: use the blast-radius taxonomy (see `../references/blast-radius-taxonomy.md`) to map nearby consumers and boundaries before expanding scope.

Expand only to the nearest meaningful seam, not to the whole repo.

### Fix Flow (for `FIX_NOW` items)

1. Plan the smallest correct seam and proof plan. (When a planning skill is available, invoke it; otherwise reason inline.)
2. **Run `dev-fresh-eyes`** on that plan to pressure-test scope, reuse, and whether pre-production work should take a broader canonical shape.
3. Implement the chosen fix in a test-driven style. Prefer writing or tightening a failing targeted test first when practical. If the bug is difficult to pin with a test first, capture the proof harness or scenario before changing code.
4. Run targeted validation: tests, lint or type checks when relevant, smoke checks, browser validation when UI/handoff behavior changed.
5. **Inspect worktree and stage only the recurring-hunt fix.**
   - Run `git status --short` before staging.
   - **Never use `git add -A`, `git commit -a`, or any whole-worktree staging shortcut.**
   - Stage only the files that belong to the current fix.
   - Recheck with `git diff --cached --stat` and `git diff --cached` before committing.
   - Remove unrelated user edits, generated artifacts, and lockfile churn from the index unless they are required for the fix and explicitly justified in the session log.
   - **If the fix cannot be isolated cleanly from unrelated local work, do not leave it floating as an uncommitted success. Downgrade the item to `HUMAN_DECISION` or `DEFER`.**
6. Commit only after the proof is green. Verified isolated fixes should not be left uncommitted unless isolation is impossible or the user explicitly says not to commit yet.
   - Prefer one small commit per bug or tightly related fix cluster.
   - Use conventional commit format.
   - Avoid generated artifact churn unless the fix truly requires it; if so, explain why in the session log.
   - **Treat generated SDKs, Swagger/OpenAPI outputs, and lockfiles as excluded by default** unless the source change genuinely requires them.
7. **Auto-route an independent second-opinion pass** (default behavior, not optional):
   - Spawn a fresh-context subagent with the diff + severity hint and a disjoint review focus — a second pair of eyes without the fixing agent's tunnel vision.
   - **If you've wired up a separate coding tool** (another CLI or model), route to it instead for cross-model divergence.
   - **No second agent available in your harness** — re-review the diff yourself in a fresh pass with a deliberately different focus (read it as a skeptical reviewer, not the author) before committing.
   - **High-severity FIX_NOW** → run more than one independent pass (different focuses or tools).
   - Override: `--no-challenger` skips this step entirely (rare; document in cycle entry).
   - Reconcile challenger findings — apply additional FIX_NOW items if any; don't blindly accept reviewer patches.
8. Record in the history doc cycle entry: plain-language bug summary, chosen seam, commit hash, staged files, generated churn intentionally included or explicitly excluded, validation commands, residual risk, **challenger lane invoked + reconciled findings**.

### Local Investigation (for items that can't be safely fixed this pass)

Stay local-only:
- Collect evidence.
- Write hypotheses with confidence (use `../references/atomic-hypothesis-method.md`).
- Note what the bug cannot be.
- Record unknowns.
- List the next best verification step.

Save in the active writable session file. **Do not sync task-tracker, support-system, chat, or any other external system unless the user explicitly asks** — cross-system posting is its own craft (handled by a separate bug-comms workflow if you maintain one), not this mode's job.

### Defer flow

Invoke the `dev-scope-deferral` skill for any `DEFER` item. The skill writes a deferred-investigation note under the configured notes directory, records the executable verification idea, and updates the repo-local backlog pointer if applicable.

### Method rotation

Use varied lanes, not one repeated review pattern. See `../references/hunt-method-menu.md`. When package behavior, framework contracts, or file-format details are unstable or unclear, internet research is allowed; prefer official docs and primary sources.

If a lane requires sign-in, UI approval, or any other user interaction, skip it and record that it was blocked.

## Mode-specific references

- `../references/triage-rubric.md` (required — terminal triage states)
- `../references/severity-rubric.md`
- `../references/hunt-method-menu.md`
- `../references/blast-radius-taxonomy.md`
- `../references/lane-selector.md`
- `../references/atomic-hypothesis-method.md` (for Local Investigation)
- `../references/output-format-contract.md`
- `../templates/recurring-hunt-session-log.md` (per-session log structure)
- `../references/history-format.md` (required — cross-session history doc schema; owned here, cited by the dev-duck-hunt wrapper)

Cross-skill invocations:
- `dev-fresh-eyes` (Fix Flow step 2 — plan pressure-test).
- `dev-scope-deferral` (DEFER items).
- The harness's recurring-task primitive (scheduling; Claude Code: `/loop`).
- An independent second-opinion pass (Fix Flow step 7 — a fresh-context subagent, or a separate coding tool if wired up).
- Session-transcript search, where the harness offers one (optional, for richer cross-session context when prior sessions weren't canonicalized in history.md).

## Output

Per-cycle output to the session log:

- `Session path` (writable + canonical)
- `Hunt scope`
- `This-pass slice and method`
- `Findings and triage` (with classifications + terminal triage states)
- `Fixes landed with commits and proof`
- `Deferred or investigated items` (link to scope-deferral notes when written)
- `Stop state and next wake-up`

## Guardrails

- Never open or merge pull requests.
- Never perform actions that require user interaction or permission to complete.
- Never keep a recurring-hunt loop alive after the session expired or hit its terminal empty-pass threshold.
- Never treat generated-file churn as acceptable by default.
- Never fail a pass only because the canonical private log is not writable; use a workspace-safe shadow log instead.
- Never leave an isolated, verified `FIX_NOW` patch uncommitted between passes unless the user explicitly asked to hold commits or the fix could not be isolated safely.
- Never sweep unrelated user work into a recurring-hunt commit.
- Never use repo-wide staging shortcuts for recurring-hunt commits.
- Do not make UI/UX changes, risky behavior changes, or architecture changes in this mode; defer them via `dev-scope-deferral`.
- Do not use this mode as an excuse for broad cleanup or refactor work.
- Do not preserve stale hybrid compatibility just to make a fix feel safer; if the correct fix is broader and low-risk in pre-production code, make that explicit in the plan first (cross-reference: fresh-eyes' Pre-Production Expansion Rule).
- Keep all logs private and local.

## Design Rationale

Mode-specific notes:

- **Scheduling belongs to the harness, not the mode** — Claude Code uses `/loop`; other harnesses have their own recurring-task primitive. Embedding scheduling inside the mode would duplicate and conflict with it. The mode focuses on per-cycle behavior; the harness handles cadence.
- **Cadence values (30 min / 12 h / 5 empty passes)** are undefended starting defaults. Expected to need re-tuning under `/loop` semantics, prompt-cache TTL behavior, and `ScheduleWakeup` range.
- **Cross-session history doc** replaces a per-session log with a persistent record under `~/.claude/notes/duck-hunt/<repo>/<branch>/history.md`. Addresses the central concern: "track what has been tried before so the loop doesn't repeat itself." Survives sessions, worktrees, machine restarts.
- **Sub-agent fanout per cycle** — 2–3 disjoint defect families covered in parallel compresses coverage per wall-clock minute vs single-method-per-cycle.
- **Auto-challenger — an independent second pass** — a fresh-context subagent by default, or a separate coding tool if you've wired one up; run more than one pass for high-severity fixes.
- **The lock + claim + finally-release pattern** prevents two passes from corrupting the session file simultaneously. Operational concurrency discipline.
- **"Expired sessions are terminal, not recyclable. Do not keep the loop alive just to report 'session expired.'"** — anti-zombie discipline. Hard-won.
- **"Never use `git add -A` / `git commit -a`"** — the autonomous-fix loop must isolate each fix from unrelated local work or risk sweeping in user edits. Explicit anti-pattern fence.
- **"If the fix cannot be isolated cleanly... downgrade to `HUMAN_DECISION` or `DEFER`"** — the explicit downgrade rule prevents stale uncommitted fixes between passes.
- **Generated-artifact exclusion default** — generated churn produces noise that masks real changes; the source change either implies generated changes (intentional, justified in session log) or doesn't (accidental, excluded).
- **Cross-skill invocations** — `dev-fresh-eyes` for plan pressure-testing, `dev-scope-deferral` for deferral, and an independent second-opinion pass (subagent or separate tool) for the challenger step. No cross-system posting workflow is invoked from this mode — Local Investigation Mode is local-only by design.
- **The triage rubric is unified at the cluster level** (FIX_NOW / HUMAN_DECISION / DEFER / DISMISSED) — a legacy "RISKY" label collapses to either HUMAN_DECISION (risk needs a human call) or DEFER (real but should be follow-up). The "RISKY" label was hiding which decision was actually needed; splitting forces the disambiguation.
