# SOP completeness — can you actually hand this procedure to someone?

A shared judgment reference for any skill that writes or evaluates SOPs. Used by `os-content-mining/sop` when deciding what a source can honestly support, and by `os-skillify/from-prompt` when judging an SOP it's been handed as conversion input.

The question this reference answers: **is there enough here that a person who wasn't in the room could do the thing?** Not "does it sound complete" — sources are often confident in exact proportion to how little they specify.

## The three grades

### Runnable

The source gives you the steps, their order, and enough of the reasoning that a stranger could execute without going back to ask. Small gaps are fine — a missing time-box, an unstated default — as long as a reasonable fill exists and gets marked where it's made.

**The test:** walk the procedure mentally as someone with no context. Every time you have to invent something, count it. A handful of small, markable inventions: still runnable. An invented *step*: it isn't.

### Partial

The shape is real — you can see what the procedure is and roughly how it goes — but whole steps or decision points are missing, and filling them means guessing at the author's method rather than supplying a routine default. A partial procedure can still be extracted, but the SOP must say plainly which parts are reconstruction, and the coverage section carries the honest bill.

**The tell:** the source explains *why* the procedure works better than it explains *how to do it*. Persuasion-shaped sources (podcasts, keynotes, sales-adjacent teaching) sit here constantly — the mechanism gets ten minutes, the mechanics get one.

### Named-only

The source tells you the procedure exists, maybe tells you it's great, and never shows you inside it. Nothing to extract. The only honest output is a sentence: this is named in the source and not explained there.

**Respect the source's own admission.** When an author says "I can't explain this properly in this format" — believe them. That sentence is data, not modesty.

## Why the grades matter

The failure this reference exists to prevent: a named-only or partial procedure, written up with confident headers and clean numbered steps, is **indistinguishable from a runnable one** until someone follows it and hits the invented parts. The grade, assigned before extraction and shown to the user, is what keeps that document from getting written.

## Worked example

From a real run (Taki Moore, Kickoff Sessions #291 — a 64-minute podcast):

- **Runnable:** the six-week focus cycle — steps, order, the card fields, the scoring axes, all stated. Extracted with three small marked fills (session length, what happens to hard-but-high-impact ideas, the fallback when no constraint is nameable).
- **Runnable:** the event structure — the speaker was literally walking through a diagram of it.
- **Partial:** sell-by-chat — the episode's headline topic, and yet no scripts, no sequences, no qualification logic. Enough to describe, not enough to run.
- **Named-only:** the "magic model" — the speaker's own words: *"it's very hard to explain in a podcast in six minutes."* Named in the extraction's coverage notes; no SOP attempted.

The lesson in the example: the headline topic graded *partial* and a side tangent graded *runnable*. What a source advertises and what it actually teaches are independent — grade what's on the page.
