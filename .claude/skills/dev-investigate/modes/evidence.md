# Mode: evidence

Part of the `dev-investigate` skill. Selected when the user wants a full evidence-first bug investigation across support reports, logs, runtime traces, replay data, and PR/backlog state — phrasings like "run a full evidence investigation," "produce a developer handoff package," or directly providing a bug report, support conversation, or task-tracker message for triage.

## Job

Run repeatable, comprehensive bug investigations that prioritize reproducibility and high-confidence hypotheses over quick patch guesses. Produce a developer-ready handoff package with timeline, hypotheses, lane status, PR-overlap verdict, and next-checks guidance.

## Run

1. **Scope and hypothesis framing.**
   - Restate bug in one sentence: user symptom + impact.
   - Build atomic hypotheses (assumption-by-assumption), not one giant theory. See `../references/atomic-hypothesis-method.md`.
   - Define disconfirming checks before collecting evidence.

2. **Evidence collection lanes.** See `../references/evidence-lanes.md` for the full taxonomy.
   - **Support lane:** pull exact transcript snippets and key user actions.
   - **Runtime lane:** collect server/app/tool-call logs in bounded time windows.
   - **Error lane:** correlate error-monitoring issues/events with concrete timestamps and entities. Call the relevant error-monitoring MCP directly (Sentry is the assumed default); if a wrapper skill is configured, invoke it instead.
   - **Replay lane:** when a session-replay tool is in play, prefer extracting the action timeline as text over long video playback — text is reasonable-over-able, video isn't. Use browser-use or Chrome MCP directly when no replay-specific wrapper skill is configured.
   - For each lane, record status as `complete`, `partial`, or `blocked`, with the blocker reason and fallback attempted. See `../references/lane-status-vocabulary.md`.

3. **Reproduction and contradiction checks.**
   - Attempt reproduction from the evidence sequence.
   - Record what reproduces and what fails to reproduce.
   - Explicitly note contradictory evidence and weaken/retire hypotheses accordingly.

4. **Overlap check (already-fixed risk).**
   - Check open PRs for direct or adjacent fixes.
   - Check recent `develop`/`main` merges for candidate remediations.
   - State whether incident appears already addressed, partially addressed, or still unaddressed. See `../references/pr-overlap-check.md`.

5. **Backlog coordination** — if the user has authorized cross-system updates:
   - Deduplicate in the primary bug list before creating new work.
   - If existing task exists, add evidence-rich update.
   - If no task exists, create a new task and attach artifacts.
   - **Hand off to your cross-system bug-comms workflow** to handle the actual posting across systems (task-tracker, team chat, support-system internal note) with the strict cross-system rules — one update per destination, configured agent identity, never message customers directly through their support thread. Don't embed posting logic in this mode. If you don't maintain a separate workflow for this, do the posting yourself after the investigation closes — but keep the rules above intact.

6. **Handoff package assembly.** Build a developer-ready package using `../templates/handoff-package.md`.
   - Include symptom-vs-broader-source analysis and confidence per hypothesis.
   - Do not prescribe exact code changes unless explicitly asked.

### Inputs to capture first

- User report(s): support conversation IDs, screenshots, timestamps, user/org/project identifiers.
- Time bounds: explicit UTC window around incident reports.
- Environment scope: production / staging / development.
- Investigation constraints: read-only vs. permitted writes (e.g., task-tracker comments/tasks, support-system notes).

### Effectiveness heuristics

High-signal investigations include:
- Exact UTC cross-system timeline joins.
- Symptom-vs-broader-source analysis (what could the symptom be hiding?).
- PR/develop overlap checks.
- Explicit confidence per hypothesis.
- Marked-blocked lanes with momentum maintained via fallback evidence in other lanes.

Avoid weak handoffs that omit confidence, omit blockers, or skip overlap checks.

### Hard rules

- Never claim 100% certainty. Report findings, hypotheses, confidence, and unknowns.
- Include "What this cannot be" based on evidence (per `../references/atomic-hypothesis-method.md`).
- Default user-attribution wording: `Affected Users: unknown (not tracked)` unless tracking is explicitly confirmed. See `../references/user-attribution-rule.md`.
- For local artifacts in chat/handoff output, use plain file paths. For web resources (PRs, task-tracker entries, error-monitoring issues, support conversations), use clickable links. See `../references/output-format-contract.md`.

## Mode-specific references

- `../references/atomic-hypothesis-method.md` (every hypothesis goes through this method)
- `../references/evidence-lanes.md` (Support / Runtime / Error / Replay vocabulary)
- `../references/lane-status-vocabulary.md`
- `../references/user-attribution-rule.md`
- `../references/pr-overlap-check.md`
- `../references/output-format-contract.md`
- `../references/status-vocabulary.md` (status term consistency)
- `../templates/handoff-package.md`

## Output

Strict-ish: see `../templates/handoff-package.md`. Required sections:

- Incident context and user impact
- Evidence index (plain file paths for local artifacts; web URLs for external systems)
- Timeline correlation across systems
- Hypothesis matrix (supported / refuted / unknown + confidence)
- Lane status matrix (support / runtime / error / replay + blockers + fallback attempted)
- PR/develop overlap verdict
- Next developer checks (source-area guidance, not implementation)
- Non-reproduced or failed-attempt notes

If posting to operational systems (task-tracker / chat / support-system), a separate **cross-system bug-comms workflow** handles the update; this mode produces the investigation findings that workflow consumes.

## Design Rationale

Mode-specific notes:

- **Atomic hypotheses, not one giant theory** — each assumption can be independently disconfirmed; one giant theory only fails as a whole and doesn't tell you which piece was wrong. (See shared rationale in `../references/atomic-hypothesis-method.md`.)
- **"Define disconfirming checks before collecting evidence"** — confirming-first leads to confirmation bias; disconfirming-first narrows the search faster.
- **Lane status mandates "fallback attempted"** — without it, lanes get silently abandoned without trying alternatives. The mandate forces explicit retry.
- **"Avoid weak handoffs that omit confidence, omit blockers, or skip overlap checks"** — names the three specific failure modes by which handoffs degrade. Quality bar.
- **Posting orchestration deliberately lives outside this mode** — the cross-system update craft (one-update-per-destination, plain-language renderings per system, identity rules, never-message-customer) is substantial enough that bundling it inside `evidence` would make this mode too dense to maintain. Keep it as its own workflow so each piece stays focused.
