---
mode: distill
parent: os-tune
description: >-
  Sub-mode of `os-tune`. Turn archived agent threads into durable memories under `os-memory/` before the harness deletes them. Reads the user's own turns — not the assistant's, not tool output — and writes one small memory per thing worth remembering. The input side of `reflect`: memories are what reflect clusters across weeks. Normally reached through `os-weekly-tuneup`, but runs standalone on "distill my recent threads", "catch my OS up on the last few weeks", "turn my history into memories".
---

# os-tune / distill — turn archived threads into memory

## Why this exists

Personal OS used to ask the AI to log its own work as it went. It never happened — not once in months — because a silent, judgment-heavy chore at the least salient moment of a session is a chore that gets skipped. The fix isn't more discipline. It's to stop asking, and instead read what the harness already recorded perfectly.

The catch is that harnesses delete transcripts on a rolling window. So this mode is a race: capture the durable part before the source expires. That's why `os-weekly-tuneup` runs it first and why it's the one step worth doing even when the user has no time for the rest.

## What gets read

Only the user's own turns. Not the assistant's replies, not tool results, not harness-injected text.

That narrowness is the point. What someone asked for, in their own words, repeated across weeks, is the signal that reveals a missing skill. The assistant's replies are the machine describing itself; clustering those surfaces the AI's habits dressed up as the user's.

The script handles the filtering, and it filters more than it looks like it should — subagent transcripts especially, whose "user" turns are prompts the assistant wrote to itself and which routinely outnumber real ones.

```bash
python3 <skill-dir>/scripts/distill_threads.py scan
python3 <skill-dir>/scripts/distill_threads.py extract --limit 5
python3 <skill-dir>/scripts/distill_threads.py mark --thread <id> --memories <n>
```

`scan` reports what's pending and how close the oldest is to expiry. `extract` returns batches of threads with the user's turns. `mark` records a thread as done so it's never reprocessed — that idempotency is what keeps a weekly run cheap.

Exit code 3 from either means nothing is pending. Say so and stop; don't manufacture work.

## The run

1. **Scan.** If nothing is pending, say so and stop. If the oldest pending thread is near the retention edge, mention it — that's the one fact that changes urgency.
2. **Extract a batch.** Default five threads. Larger batches cost more per run and gain nothing; the state file means an interrupted run resumes cleanly.
3. **Read each thread's turns and decide what's worth remembering.** Most threads produce zero or one memory. Some produce three. Many produce none at all, and that's the normal case, not a failure.
4. **Write the memories** to `os-memory/`, following `references/memory-format.md`.
5. **Mark each thread** with how many memories it produced, then continue to the next batch or stop.

## What earns a memory

Write a memory when a thread contains something that will still matter in a month:

- A request shape that keeps recurring — the strongest signal there is, and the one that becomes a skill
- A correction or preference stated plainly enough to generalize
- A decision with reasoning that isn't recoverable from the artifacts it produced
- A tool, service, or workflow the user worked out how to drive, where the re-discovery cost is real

Don't write a memory for: work that's fully visible in what it produced, one-off questions, conversation, or anything you'd be paraphrasing rather than preserving.

**A thread with nothing durable in it is the common case.** Marking it done with zero memories is the correct outcome and costs nothing. Filler memories are worse than no memories — they dilute the clustering that `reflect` depends on, and a store full of "the user asked about a file" teaches nothing.

## Style

Keep each memory small and plain. Lead with the thing itself, not the circumstances around it.

Quote the user's own phrasing when the phrasing is the signal — for recurring-request memories it usually is, because that verbatim wording is what lets `reflect` recognize the same ask wearing different words next month. Paraphrase everything else.

Record which project a memory came from. It's how a memory gets found and removed later if a working relationship ends.

## Guardrails

- **No secrets, credentials, or customer data** in a memory. The source thread may contain them; the memory must not.
- **Never write to the transcripts.** This mode reads its source and writes only to `os-memory/`.
- **Client work is in scope by default** — that's where repetition concentrates and where the value is. Exclusions are the user's explicit call, set during `os-weekly-tuneup/setup` and honored by the script.
- **Don't infer beyond the turns.** A memory records what the user said and did, not a theory about what they meant.

## Related

- `os-weekly-tuneup` — the scheduled pass that normally invokes this
- `os-tune/reflect` — the consumer; clusters these memories into proposals
- `references/memory-format.md` — the memory file contract
- `dev-branch-memory` — the same idea scoped to one branch, and where this format came from
