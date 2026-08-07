# Capture Mode

Capture mode writes one or more concise memory notes when branch decisions would be hard for a reviewer or future agent to reconstruct from the diff.

## Capture Triggers

Capture when one of these changed since the last memory:

- a refactor boundary moved
- an architectural decision was made or reversed
- a contract/schema/prompt/tool boundary changed
- an existing pattern was intentionally preserved
- an existing pattern was intentionally changed
- a tempting route was rejected and future reviewers would benefit from knowing why
- a user correction changed the shape, language, or decision criteria of the plan
- a proof strategy changed because evidence contradicted a plan
- temporary instrumentation was used and taught something
- scope was narrowed and a valid follow-up was deferred
- a durable instruction source materially shaped the branch decision

Do not capture routine edits, command output, lint/test pass noise, or obvious implementation details.

## Capture Steps

1. Resolve the branch directory:

```bash
python3 <skill-dir>/scripts/resolve_branch_memory_dir.py --repo "$PWD" --mkdir
```

2. Read the existing branch memory surface:

```bash
sed -n '1,220p' <branch-memory-dir>/manifest.json
sed -n '1,220p' <branch-memory-dir>/branch.md
ls <branch-memory-dir>/memories
```

3. Decide whether new signal exists. If not, report no capture.
4. Decompose new signal into focused decision clusters before drafting. A long thread or checkpoint may deserve several memories, but each memory should have one primary decision lane.
5. For each cluster, reconstruct the decision arc before writing:
   - What did the user care about or push back on?
   - What did the agent propose or initially assume?
   - What alternatives, shortcuts, or duplicate paths were considered?
   - Which route was rejected, and why would it be tempting later?
   - What final decision did the human/agent conversation converge on?
6. Draft each body in a separate `/tmp/branch-memory-*.md` file.
7. Write each memory with `write_memory.py`.
8. Run `validate_memory.py` on each new file.

## Multi-Memory Guidance

Write multiple memories when the current context contains independent decisions that future readers would search for separately. Good split points include:

- source-of-truth or canonical data ownership decisions
- API, schema, route, or event contract decisions
- UI/navigation or product-surface pattern changes
- verification/risk decisions that changed implementation scope
- deferred follow-ups with clear owner context

Do not split only because many files changed. If the decision is one coherent boundary choice, one memory is better.

If memory has been written recently, compare against recent summaries first. Add a new memory only when the new decision lane is different or when later evidence materially changes the prior note.

## Subagent Review Guidance

For long threads, subagents may inspect separate decision lanes and propose memory candidates if your harness supports forking them with the full thread context; on single-agent harnesses, review the lanes sequentially yourself. Keep each assignment bounded, for example "review analytics decisions for branch-memory capture." The parent agent must reconcile duplicates, resolve contradictions, and write or validate the final memories.

## Capture Body Guidance

Lead with the decision and impact. Keep the note short enough to be reviewed later. Start every memory body with a one-sentence `TL;DR: ...` before the first heading.

Prefer these stable sections when they carry signal:

- `Current Decision`: what changed or what policy this branch chose.
- `Decision Arc`: how the conversation moved from initial framing to final choice.
- `Human Input That Moved It`: the user's concern, correction, or agreement that materially shaped the decision.
- `Why It Came Up`: the product, review, bug, or architecture pressure that caused the decision.
- `What Changed In Code`: short map of the main implementation surfaces, not a file-by-file changelog.
- `Options Considered`: plausible choices discussed or implied by the plan.
- `Routes Not Taken`: rejected paths and why they should stay rejected unless new evidence appears.
- `Risk / Invariant`: required for contract, source-of-truth, risk, and safety memories; name what future changes must not break.
- `Evidence So Far`: proof that directly supports this decision.
- `Source Trace`: concrete refs that shaped the decision.
- `Open Questions`: unresolved or deferred work.
- `Reviewer Relevance`: how a reviewer should interpret the diff.

Use headings consistently enough that both humans and future agents can skim many memories quickly. Omit sections that add no signal.

Good memory:

- "TL;DR: We kept the public transformer output shape stable and moved validation upstream because client consumption already depends on the old shape. The tempting route was to normalize the response in-place, but the user called out that downstream consumers already rely on the current shape, so this branch protects the public contract and moves validation earlier."

Weak memory:

- "Edited three files and ran tests."
- "The tool now has a better API."

## Heartbeat Guidance

Heartbeat captures should be selective. It is better to write no note than to create a low-signal note that later obscures the real branch decisions.

Heartbeat prompt shape:

```text
Use $branch-memory capture mode. Review the current thread and current branch. If non-trivial refactor, architecture, contract, source-traceability, risk, verification, or deferred-followup decisions have emerged since the last memory, decompose them into focused decision clusters and write one or more concise branch memories. Do not duplicate existing memories. Use verified only for decisions with direct proof; prefer supported/provisional/unknown when evidence is incomplete.
```
