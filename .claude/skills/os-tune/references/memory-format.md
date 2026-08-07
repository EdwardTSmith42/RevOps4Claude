# Memory format

One memory, one file, under `os-memory/`. Written by `os-tune/distill`, read by `os-tune/reflect`, indexed by nothing — the directory is the index. The ledger beside them (`_ledger.md`) is written by `os-weekly-tuneup`, which owns the sequence that produces its entries.

**Malleability note.** The frontmatter fields below are canonical: `reflect` clusters on them, so renaming or dropping one breaks pattern detection. Everything about the body is adaptable — length, headings, how much of the user's phrasing you keep. Adapt the prose freely; leave the keys alone.

## Filename

```
os-memory/<YYYY-MM-DD>-<short-slug>.md
```

Date first so the directory sorts chronologically. Slug short enough to scan, specific enough to tell two memories apart at a glance.

## Frontmatter

```yaml
---
kind: recurring-request | preference | decision | tool-knowledge
summary: <one line, plain language, what this memory is>
project: <project the source thread came from>
thread_id: <source thread>
created: <YYYY-MM-DD>
status: active | acted-on | rejected | superseded
tags: [<free-form>]
---
```

Seven fields, and each one earns its place:

- **`kind`** — the four shapes worth distinguishing, because each has a different downstream action. A `recurring-request` becomes a skill. A `preference` becomes a line in a profile or a principles file. A `decision` is context that stops the same ground being re-litigated. `tool-knowledge` is the one whose re-discovery cost is obvious and immediate. If a memory doesn't fit one of these, that's usually a sign it isn't durable enough to keep.
- **`summary`** — what `reflect` scans first. Write it so a human skimming forty of these can tell in one line whether this one matters.
- **`project`** — provenance, and the mechanism for removing a client's memories if that relationship ends.
- **`thread_id`** — traceability back to the source while the source still exists.
- **`status`** — how the ledger and the memory stay in sync. `active` until something happens; `acted-on` once a change ships; `rejected` when the user declined, which is a decision worth keeping so it isn't re-proposed; `superseded` when a later memory replaces it.
- **`tags`** — free-form, no taxonomy. A tag that never gets used to find anything costs nothing; a taxonomy invented before there's a consumer costs a lot.

## Body

Short. A few sentences to a few short paragraphs. Lead with the thing itself rather than the circumstances that produced it.

For a `recurring-request`, quote the user's actual phrasing — two or three examples of how they asked, verbatim. That wording *is* the signal: it's what lets `reflect` recognize the same request next month when it arrives dressed in different words. Paraphrase everything else.

For a `decision`, say what was chosen and what it was chosen over. The rejected alternative is usually the part that isn't recoverable from anything else.

## What not to put in

- Secrets, credentials, tokens, or customer data. The source thread may contain them; the memory must not.
- Long transcript excerpts. Quote a line, not an exchange.
- The assistant's reasoning. Memories record what the user asked and what was decided, not the machine's account of itself.
- Anything already obvious from the artifacts the work produced. If reading the file tells you, the memory is redundant.

## Status transitions

`reflect` proposes; the user disposes; the ledger records. When a proposal is accepted and something ships, the driving memories move to `acted-on` and a ledger line goes into `os-memory/_ledger.md`. When the user declines, they move to `rejected` — permanently, because re-proposing a rejected pattern every week is how a system that notices becomes a system that pesters.

A memory is never deleted to reflect a change of mind. Supersede it and let the trail stand.
