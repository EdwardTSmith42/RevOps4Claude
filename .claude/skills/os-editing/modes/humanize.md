---
name: os-editing/humanize
description: Take the machine fingerprints off a draft and land it back in the writer's voice. Runs a composition pass (ordering, over-polish, missing specifics, cashed-out endings), a skeptical-reader audit, then a line pass against the canonical AI-writing catalog — with a final check that no claim was lost. May restructure: reorder, cut sections, delete strong-but-lacquered lines. Output is the finished prose only, no commentary, unless the user asks to diagnose instead. Triggers on "humanize this," "make this sound less like AI," "remove the AI tells," "de-slop this draft," "de-AI-ify this," "clean this up for LinkedIn / X / the newsletter," "does this read as machine-written." Do NOT trigger for compression to a length target (use `shorten`), suggestions the writer picks from (use `suggest-edits`), a scored verdict (use `assessment`), tone description (use `tone-profile`), or fiction prose (use `fiction-edit`).
---

# Mode — Humanize

Remove what makes a draft read as machine-made, then put it back in the writer's voice. Returns the rewritten piece, ready to use.

## Purpose

Most de-AI passes chase vocabulary — swap "delve" for "explore," strip the em-dashes, call it done. That fails, because the tells that actually give a draft away are structural and survive any synonym swap. This mode works from the full catalog at three altitudes and fixes composition first, so the result reads as written-by-a-person rather than written-by-a-model-with-a-thesaurus.

The second thing it protects is voice. A generic cleanup produces generically clean prose — competent, characterless, regressed toward the model's mean. So the pass resolves a specific voice and lands the cleaned draft there.

Hold the framing from `../../_shared/references/ai-writing-patterns.md`: this is an **editing guard, not an authorship detector**. It catches prose that fails to reach a real reader, whoever wrote it. Never report findings to a writer as evidence that a machine wrote their work.

## What this mode may change, and what it may not

It **may restructure.** Reorder sections, cut a passage, delete a strong sentence that's doing lacquer work, expand a thin claim into the specific thing it's standing in for. A pass restricted to swapping words cannot fix the failures that matter most, so the restriction isn't worth keeping.

It **may not touch rhythm.** Staccato, line-break cadence, the build-and-pop of a stacked passage — that's the writer's hand. Attempts to reproduce it copy the surface, compress past the point the meaning survives, and produce fragments that parse only for someone who already knows what they meant.

The target isn't the writer's final draft. It's **the version where the writer's own pass is all that's left** — everything mechanical handled, the piece's own hand still to be added.

## Inputs

- **Required:** the draft. Pasted, or a file path.
- **Optional — voice.** Whose voice the result lands in. Unspecified, resolve by the implied-author rule: read `os-inputs/_os-user-profile.md` for the user's name and load the matching voiceprint, scoped to the format when a scoped variant fits. With no voiceprint on file, say so and run voice-neutral rather than inventing a voice — then offer `os-voiceprint` for next time.
- **Optional — genre and destination.** An X post, a client memo, a sales email, a chapter. Changes what counts as a tell. Ask if it isn't obvious from the draft.
- **Optional — diagnose only.** The user wants to know what's wrong and fix it themselves.

## Run

### 0. Identify the genre and the claimed author

Before applying anything, name the register and who the piece is supposed to sound like. The genre carve-outs in the catalog are not a footnote — direct-response copy legitimately keeps exclamation points and hard closes, academic prose legitimately keeps semicolons and announced conclusions, structured business documents legitimately have headings. When the draft sits in one of those registers, say which rules are being skipped before touching anything.

### 1. Composition pass

Read the whole draft first. Local edits made without the global picture produce inconsistent voice and broken argument.

Work the composition tier of the catalog. In practice the recurring moves: cut the lacquered sentence that cashes the story out into its own lesson; replace the general noun with the particular thing it's standing in for; stage what's merely asserted; unbutton an ending that resolves too neatly for its genre; move a rhetorical device to where it actually pays, or drop it; strip the sentences that comment on the writing rather than advancing it; and check whether the piece has any shape other than a general-purpose answer poured into its format.

Two disciplines while doing this.

**Length has no preferred direction.** Sometimes the repair is deletion. Sometimes it's a rewrite that runs much longer because instantiating costs words. Never compress toward a target — that's `shorten`'s job, deliberately invoked. Repairs skew longer for a reason worth knowing: tightening is its own editing pass that almost nobody but working copywriters runs by reflex, so untightened prose reads like a person who had a thought and posted it.

**Consequence is the deep check.** Does anything in the piece behave differently because of what it just said? A claim that costs the writer nothing, a difficulty named and then ignored, a risk that no later sentence is wary of — those are the fabricated-set failures, and they survive every surface fix.

### 2. The skeptical-reader audit

Step away from your own edits and read the result cold, as a reader who knows the field, is busy, and is not automatically impressed. One question: *did this writer say something to me, or write around the topic?*

Then the author-plausibility check: if this came from the person it's supposed to have come from, are these the words they'd reach for, and would they frame it this way for a peer?

The audit is a different question than the composition pass asked, which is the point — it reads the output on its own terms rather than re-checking your own work.

### 3. Line pass

Now the sentence and vocabulary tiers, gated by confidence.

**Hard tells get fixed on sight.** A word borrowed from a profession the writer isn't in, an invented label where a description would do, wording no one in the claimed author's world would use. One instance is enough — no corroboration needed.

**Soft signals get fixed only when they cluster.** Nominalizations, tidy contrasts, dense abstract lists, vague nouns, restatement that doesn't progress. Any one is ordinary human writing. Act when several land in the same passage and point the same way: nobody acting, nothing concrete changing, words that belong to no one. Scale the bar to the piece — in a short post, two reinforcing signals is a cluster.

**A lone soft signal gets left alone.** This is the rule that keeps the mode from mangling good drafts.

Take replacement vocabulary from the draft itself. If the writer says "stupid simple" in paragraph four, that beats "important" as a replacement for "transformative" anywhere else. Don't import words the writer doesn't use.

### 4. Final check

**Re-injection.** A rewrite is itself an act of generation, and it reliably introduces fresh tells — a new tidy closer, a fresh tricolon, cadence rebalanced until it's too even. Sweep for what step 3 added.

**No claim lost.** Then the disconfirming check, and run it honestly: list what the input said that the output doesn't. The list should be empty, or every item on it should have a stated reason. Cuts target lacquer and redundancy. If a cut would remove information, it becomes a flag for the writer rather than a cut.

## What to leave alone

Every instinct in an editing pass points the other way, so this is explicit.

Roughness that is evidence of a person is not an error: missing capitals, a typo, a dropped period, a trailing-off sentence, a word repeated in the heat of a point, a digression that isn't strictly needed. Cleaning those produces prose that is more correct and more obviously machine-touched.

The distinction to hold: **residue** is what a machine leaves behind — chatbot framing, mechanical hedging, structural announcements — and it goes. **Traces** are what a person leaves behind, and they stay. When it's unclear which one you're looking at, ask whether the irregularity costs the writer anything. A typo costs a little credibility and buys nothing, which is exactly why a machine wouldn't produce one.

Don't manufacture roughness either. Sprinkling typos on an otherwise perfect piece is a costume. The irregularity that matters is structural — where the writer's attention actually went — and it can't be added afterward.

And if a sentence is fine, leave it. Restraint is the harder craft.

## Output

**The rewritten piece only.** No preamble, no commentary inside it, no diff, no bullet-listed change summary. Begin with the first line of the piece and end with its last. The user pastes it back into their draft.

Two things belong *outside* that delivery, in the surrounding message rather than embedded in the prose:

- Anything from the no-claim-lost check that turned into a flag rather than a cut.
- Judgment calls worth naming — something deliberately left because it read as the writer's real voice rather than a tell, or a genre rule skipped.

Keep both short. The draft is the deliverable.

**Diagnose-only.** When the user asks what's wrong rather than for a rewrite, skip the rewrite and return the read: which patterns appear, where, at which confidence level, and — for each — what the reader loses. Report reader-level failures, never a feature count.

## Boundary with `shorten`

Both transform text and both remove words, so the line is stated rather than inferred. `shorten` compresses toward a length target, deliberately, with a word-count delta as part of its output. This mode has no length target in either direction; its cuts are lacquer removal, and the piece may well come back longer. Chain them in either order — the useful sequence is usually humanize first, then `shorten` if the result is still too long for its slot.

## Design rationale

- **Composition before line work, with an audit between.** The passes ask different questions, which is what makes two of them worth running. A single pass, or two identical passes, misses the document-level failures entirely — and those are the ones that survive every vocabulary fix.
- **Restructure rights, bounded by an invariant.** A mode that can only swap words can't fix ordering, can't cut the lacquered thesis, can't instantiate. Giving it real surgery rights requires the no-claim-lost check as the counterweight; without an explicit disconfirming list, a confident structural gutting is indistinguishable from good work.
- **Two confidence levels rather than one flat checklist.** Flattening hard tells and soft signals together is how a guard becomes a mangler. Most catalog items are things human writers do constantly; acting on them individually damages good drafts.
- **Length is unconstrained in both directions.** An earlier framing of this mode treated humanizing as a form of tightening. Observed edits contradict it — a writer's own repair pass held length flat in one case and nearly quadrupled it in another, while the concrete-to-abstract ratio moved the same direction in both.
- **Rhythm is out of scope on purpose.** Not because it doesn't matter — it's often the most distinctive thing about a writer — but because attempts to reproduce it degrade into incomprehensible fragments. Better to stop cleanly at the edge of the writer's hand.
- **Replaces the former `direct-rewrite` mode rather than sitting beside it as a deeper option.** A quick pass and a thorough pass covering the same job is an invitation to route to the sloppy one. There's one AI-tell-removal mode, and it always runs the full method. The clean-prose-only output contract is inherited from that mode, which had it right.

## Sources

Distilled from the Wikipedia *Signs of AI writing* taxonomy, field-tested rewrite practice, blind-sample testing against fresh writers with no context, and two before-and-after diffs of a working writer's own hand-edits of AI drafts. The composition tier comes almost entirely from the diffs; the sentence tier from the blind samples; the vocabulary tier is the older empirical catalog. Full account in `../../_shared/references/ai-writing-patterns.md`.
