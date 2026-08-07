# Mode: tidy

Review a tracker context for items that have gone stale, quietly finished, or drifted past relevance — and propose what to do about each. Read-and-propose; never writes without confirmation.

Normally reached through `os-weekly-tuneup`, but useful any time a list has grown faster than it's been worked.

## Inputs

- `context` (optional) — context slug, `all`, or `user` (default). When omitted: `user`.
- `since` (optional) — ISO timestamp. Restrict to items untouched since then. When omitted, use the last tidy recorded in the context, else 30 days.
- `evidence` (optional) — recent work to check items against. When `os-weekly-tuneup` invokes this, it passes the memories distilled earlier in the same run; a thing you did last Tuesday is the best evidence that a todo about it is finished.

## Procedure

1. **Read the context** per `view`. If it doesn't exist, say so and stop — nothing to tidy.

2. **Sort every open item into one of four buckets.** Most items land in `leave` and that's fine; a tidy that proposes changing half the list is usually wrong about the list.

   - **`done`** — evidence shows this happened. Cite the evidence.
   - **`stale`** — untouched past the window, still plausibly wanted.
   - **`drifted`** — the thing it describes has moved on: the feature shipped differently, the decision was made another way, the reason it existed is gone.
   - **`leave`** — active, recent, or deliberately parked. No action.

3. **Propose one action per non-`leave` item**, and say why in a few words:
   - `done` → close it
   - `stale` → keep, defer with a new date, or drop
   - `drifted` → rewrite to what it actually means now, or drop

4. **Present the whole set at once, grouped by bucket, newest first.** Not one prompt per item — a twelve-question interrogation is how a tidy becomes something the user avoids. Let them accept all, accept by bucket, or pick individually.

5. **Apply only what was confirmed**, via `update`. Record the tidy date in the context so the next run has a window to work from.

## Judgment

**Closing something the user still wanted is the expensive mistake.** Leaving a stale item costs a line of clutter; closing a live one loses work. When an item is ambiguous, propose `leave` and move on — the next tidy will see it again with more evidence.

**A long-lived unfinished item is a signal, not a failure.** Something that has survived several tidies untouched is usually telling you either that it matters more than its position suggests, or that it was never really a task. Say that out loud once rather than proposing to drop it a fourth time.

**Don't propose rewrites for tidiness alone.** Rewrite a `drifted` item when its current wording would mislead the person who reads it next. Otherwise leave the words alone.

## Guardrails

- **Never delete or close without explicit confirmation.** This mode runs inside a recurring pass; a scheduled ritual that quietly closes items is how people stop trusting their own list.
- **Evidence beats inference.** "Untouched for 30 days" is not evidence something is done — only that nobody wrote it down. Mark `done` only with something concrete behind it.
- **One tidy per context per run.** Don't loop.
- **Say when there's nothing to do.** A clean list is a good outcome and worth one sentence, not a manufactured list of suggestions.

## Output

A short summary line, then the grouped proposals:

```
<n> items reviewed · <n> look done · <n> stale · <n> drifted · <n> left alone
```

Then each non-`leave` bucket with its items and one-line reasons. If every item lands in `leave`, say so and stop.
