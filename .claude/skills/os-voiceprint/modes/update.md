---
name: os-voiceprint/update
description: Refresh an existing voiceprint when the writer's voice in that context has genuinely evolved, then sort the change by layer and judge whether it's a room-change (touch only this voiceprint) or a person-change (the deep fingerprint moved, so sibling voiceprints become candidates for review). Triggers on "update my voiceprint, my writing has changed," "my voice has shifted, refresh this," "the saved voiceprint doesn't sound like me anymore." Do NOT trigger for a brand-new context that has no voiceprint yet (use `from-sample`), for filing externally-produced voiceprint text (use `import`), or for fixing malformed frontmatter (use `os-library/repair`).
---

# Mode — Update

Refresh a voiceprint that already exists, because the voice it captured has moved. The job is two things at once: produce an honest current voiceprint for this context, and decide what the change *means* for the writer's other voiceprints. A voice shift that's confined to one room touches one file. A shift in how the writer's mind actually moves touches the whole family.

This mode exists because of how voice is structured (see `../references/voiceprint-definition.md`). A writer has many voiceprints, one per context, and they can differ to the point of contradiction. What unifies them is the *deep fingerprint*, not shared content or rules. So when a voice evolves, the only question that matters is *which layer moved* — and that question can't be answered by re-running extraction blind, which is why updating is its own mode rather than just "run from-sample again."

## When to use

The user already has a voiceprint on file for a context and one of these is true: they say their writing in that context has changed, they supply fresh samples meant to *replace* the basis of the existing voiceprint, or a drafting session keeps fighting the saved voiceprint because it no longer sounds like them. The tell that separates this from `from-sample` is that a voiceprint for this context already exists and the goal is to refresh it, not to cover a new room.

If the context is genuinely new (no voiceprint yet), that's `from-sample`. If the user wants to file voiceprint text produced elsewhere, that's `import`. If the file is fine but its frontmatter drifted, that's `os-library/repair`.

## Inputs

- **Required:** The target voiceprint to update — by name, or located via `os-library/find` from the context the user describes.
- **Required (one of):** Fresh sample writing from the *same context* (ideally 500+ words, multiple pieces preferred — the same bar as `from-sample`), **or** a described shift the user can articulate well enough to evaluate (weaker; prefer samples whenever they exist, because surface mechanics have to be observed, not inferred).
- **Optional:** The user's own read on whether this feels like a whole-self change or just-this-channel. Useful as a prior, but the mode forms its own verdict from the layer diff and reconciles with the user's.

## Run

### Step 1 — Load the existing voiceprint

Read the target file, both sections. The `# Analysis` section (dimension scores, custom dimensions, grounded justifications) is the baseline you'll diff against. The `# Voiceprint` portrait is what downstream skills currently load. Note the `created` date and the `source` — they tell you how old the basis is.

### Step 2 — Re-extract from the new samples

Run the same two-pass procedure as `from-sample` against the fresh samples: a technical `# Analysis` with dimension scores, then a 150-300 word `# Voiceprint` portrait written in the voice, passing the era-tells self-check and source-cleanliness rules. This produces the *candidate* updated voiceprint. Don't save it yet — the verdict in the next steps may change what gets saved and where.

### Step 3 — Diff old vs. new, sorted by layer

This is the heart of the mode. Compare the baseline Analysis to the candidate Analysis and sort every meaningful change into one of the three layers from `../references/voiceprint-definition.md`:

- **Content and stance** — which beliefs surface, topics, signature concepts. Changes here are expected and channel-bound; they rarely mean anything for siblings. (And often they shouldn't be in the voiceprint at all — flag if the old one was carrying content it shouldn't.)
- **Surface mechanics** — sentence length, formality, punctuation, white space, the exclamation-point question (Format & Cadence, Register, Tone). Changes here are usually *room-level*: the writer dresses differently for this room now.
- **Deep fingerprint** — idiosyncrasy, rhythm/burstiness, surprise/perplexity, and the custom dimensions. Changes here are *person-level*: how the mind moves has shifted, and that doesn't stay in one room.

Be explicit and specific: name which dimensions moved, by how much, and with what evidence. A vague "the voice feels different" is not a diff.

### Step 4 — Render the verdict: room-change or person-change

From the layer diff, classify:

- **Room-change** — the movement is in content and/or surface mechanics only; the deep fingerprint is stable. The writer sounds like the same person, dressed differently for this room. Siblings are untouched.
- **Person-change** — the deep fingerprint itself moved (rhythm, idiosyncratic constructions, characteristic thought-moves). The same shift is likely present across every context, so every sibling voiceprint is now a candidate for review.

When the evidence is mixed, say so and reconcile with the user's own read rather than forcing a binary. Err toward room-change when only one or two surface dimensions moved and the fingerprint dimensions held — most voice evolution is room-level, and over-calling person-change creates needless churn across the library.

### Step 5 — Surface the siblings (person-change only)

If the verdict is person-change, find the writer's other voiceprints by reusing `os-library/list` filtered to `type: voiceprints` and the target's `author`. Present each sibling as a *candidate for review*, and for each one name the specific deep-fingerprint shift to check for in that context. This is information for the user, not a queue the mode drains on its own.

### Step 6 — Save, and never silently propagate

Save the updated target voiceprint through `os-library/save`, overwriting the same `<author>-<scope>.md` file, bumping `created` to today, and noting the update in `source` or `notes` (what changed, and the room-vs-person verdict).

For siblings, the rule is firm: **never auto-rewrite a sibling.** Voice is too subtle to propagate a change by inference — a deep-fingerprint shift shows up *differently* in each room, and the only faithful way to capture it is from that room's own fresh samples. So for each sibling the user wants to bring current, run a separate `update` pass on it with its own samples and its own approval. Propose; don't propagate.

## Output

- The refreshed target voiceprint (shown inline for review before it's consumed downstream), saved through `os-library/save`.
- The layer-sorted diff — what moved, in which layer, with evidence.
- The verdict (room-change or person-change) with its reasoning.
- For a person-change: the list of sibling voiceprints flagged for review, each with the specific shift to check for, and the explicit note that none were modified.

## Output discipline

Lead with the verdict and the diff, not the new portrait — the judgment is the value this mode adds over a blind re-run. Keep the diff specific (named dimensions, real evidence). Never present a sibling as "updated" — siblings are only ever *flagged*. State plainly when siblings were left untouched and why.

## Design rationale

Updating is a distinct mode, not "re-run from-sample," because the value is the *judgment about scope*, not the re-extraction. A blind refresh silently overwrites the one voiceprint in front of it and misses that the same shift may have quietly invalidated three others — the exact library drift the whole skill is built to prevent.

The room-vs-person distinction maps directly onto the three-layer model: surface and content live in the room; the fingerprint lives in the person. Tying the verdict to specific dimensions (fingerprint dimensions moved → person; only surface/content moved → room) keeps the call grounded rather than impressionistic.

Sibling discovery reuses `os-library/list` rather than reimplementing author lookup — collection-awareness already lives in the library, and the library is the source of truth for what's on file. Building a second sibling-finder here would be exactly the kind of drift-prone duplication the reusability principle warns against.

The never-propagate rule is the most important guardrail. The intuitive move — "the fingerprint changed, so rewrite all the siblings to match" — is wrong, because a fingerprint shift manifests differently in every room and a tweaked-by-inference sibling will sound like a different person wearing the writer's clothes. Faithful capture is always from real samples, room by room, with the user in the loop.

## Cross-mode suggestions

After an update, if the verdict was person-change and the user wants to bring a flagged sibling current, gather fresh samples for that context and run `update` on it. If a flagged context has no voiceprint yet but probably should, point at `from-sample`. If the user just wants to see their whole collection and what's stale, point at `os-library/list`.
