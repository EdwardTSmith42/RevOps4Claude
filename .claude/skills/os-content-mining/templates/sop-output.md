# Template: sop-output

The single-file shape for an extracted SOP. One document, complete in itself: a reader should be able to run the procedure without the source open, and audit the extraction without asking what came from where.

Two sections are **always present**, even when empty: the provenance block and "What this doesn't cover." An empty coverage section is a claim — *the source explains this fully* — not an omission. That's deliberate: it makes a lazy extraction visible, because a lazy one either fills the section honestly or makes a checkable false claim.

```markdown
---
name: SOP — [what the procedure does, in plain words]
description: [one line: the job this procedure does, and where it came from]
tags: [sop, ...]
---

# SOP — [Name]

[Provenance block — always present: the source, a link, how to re-acquire it,
and the date extracted. If this SOP was part of a mining run, link the mining
kit too.]

## What this is

[Two or three plain sentences. What the procedure produces, and the idea
underneath it — why the person who invented it says it works. If the source
has a memorable line that captures it, quote it here.]

## When to run it

[The real-life situations that call for this, written so a reader recognizes
their own moment in the list — not abstract preconditions.]

## What you need

[Materials, prior artifacts, time. If the source didn't say how long it takes
and you estimated, mark the estimate `[filled in]`.]

## The steps

[The procedure itself, in order. Keep the source's own step count and names —
if they call it three phases, it's three phases here. For each step: what you
do, and where it helps, why the step exists. Anywhere you supplied something
the source left open — a default, an ordering, a threshold — mark it
`[filled in]` at the point of use.]

## Why it works

[The mechanism, briefly. What breaks if you skip the counterintuitive step.
This is what lets someone adapt the procedure instead of following it blind.]

## What this doesn't cover — always present

[Everything the source names but never explains, and every part of the
procedure this file couldn't specify. If genuinely nothing is missing, say
so explicitly: the section stays, as the claim of full coverage.]
```

## Rules

- **Self-contained or it isn't done.** No step may require the source, or a second file, to execute.
- **Every gap-fill is marked where it sits.** `[filled in]` at the point of use, not collected in a footnote.
- **Keep the source's own names and counts.** Renaming their framework or rounding their step count breaks the link back to the source.
- **Plain language.** These files are read by people mid-task and by AI building skills from them. Explain simply; keep jargon only when it's the source's own load-bearing term — and then define it once.
- **Pasteable.** The document is the deliverable. Meta-commentary about the extraction goes in chat, never inside the file.
