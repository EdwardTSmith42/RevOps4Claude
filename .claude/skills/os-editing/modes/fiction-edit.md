---
name: os-editing/fiction-edit
description: Edit fiction manuscripts (chapters, scenes, stories, novels) across 4 layers — Proofreader (mechanics), Line Editor (sentence-level prose), Voice-Sensitive Filter (push back on Line Editor where voice is at risk), Editorial Judgment (technical-but-awkward prose + developmental observations on narrative flow, character, scene purpose, motivation, pacing). Output uses Sample Edit Format (Original / Rationale / Suggested Edits with two rewrite options) for flagged passages, or in-line edited manuscript for clean-up requests. Triggers on "edit my chapter / scene / story / novel," fiction context, manuscript editing. Do NOT trigger for non-fiction prose (use `suggest-edits` or other modes), story drafting (use a writing skill), or character/plot development (deferred to a future fiction skill).
---

# Mode — Fiction Edit

Layered manuscript editing for fiction. Proofreader → Line Editor → Voice-Sensitive Filter → Editorial Judgment, with Sample Edit Format as the default output for flagged passages.

## Purpose

The user has fiction prose — a chapter, scene, short story, or novel passage — and wants editorial work that respects voice. Fiction editing has distinct concerns from non-fiction. Voice is more fragile, character voice may differ from narrator voice, deliberate rule-breaking is often craft, and developmental observations span scene/character/pacing rather than argument/evidence.

## When to use

- "Edit my chapter / scene / story"
- "Line-edit this manuscript section"
- "Proofread my novel chapter"
- Any request where the prose is fiction (story, character, dialogue, scene, novel context)

## When NOT to use

- **Non-fiction prose** — use `suggest-edits` or `humanize` instead. Fiction-edit is over-equipped for non-fiction and under-equipped for non-fiction's structural concerns.
- **Drafting new fiction** — fiction-edit operates on existing prose. Generating new prose is drafting work and lives in a future os-writing/fiction skill.
- **Pure plot or character development** — fiction-edit can FLAG developmental issues but doesn't develop story. If the user wants story development, that's a separate (future) skill.

## Inputs

- The manuscript section (text, attached file, or pasted)
- Optional: stated genre, target audience, voice goal, chapter context (where this scene sits in a larger work)
- Optional: requested output format — `in-line` (edited manuscript without markup) or `sample-edits` (Original / Rationale / Suggested Edits format, default)

## Run — the 4-layer process

Apply the layers in this order. Reference `../references/fiction-editing-layers.md` for the full architectural rationale.

### Layer 1 — Proofreader (Surface Clean-Up)

Cheapest fixes. Pure mechanical correctness.
- Fix spelling, grammar, and punctuation errors
- Remove double spaces, inconsistent dashes, or extra line breaks
- Apply standard rules unless clearly overridden by style

If the writer uses an em-dash style consistently, that's style — leave it. Layer 1 catches *errors*, not *deviations from convention*.

### Layer 2 — Line Editor (Flow + Clarity)

Sentence-level prose work.
- Break up overly long or tangled sentences
- Improve rhythm and readability
- Replace vague or repetitive phrasing
- Tighten redundancies and filler words

Layer 2 produces a list of *candidate* edits. The next layer reviews them.

### Layer 3 — Voice-Sensitive Filter (Style Awareness)

Reviews Layer 2's candidates and pushes back where they would erase voice.
- Don't over-polish sentences that intentionally break rules for tone or character
- Respect stylistic quirks unless they interfere with clarity or pacing
- Make edits that enhance voice, not erase it

**This layer is what keeps the whole process honest.** Without it, fiction editing produces voice-homogenized prose that reads cleaner but worse.

Common Layer 3 push-backs against Layer 2:
- A fragment Layer 2 wanted to complete is a voice signature → leave it
- A repeated word Layer 2 flagged is doing rhythmic work → leave it
- A run-on Layer 2 wanted to split is the character's voice in close-third POV → leave it
- A "vague" verb Layer 2 wanted to sharpen is ambient atmospheric, not weak → leave it

When Layer 3 fires, the suggested edit is dropped, downgraded to optional (an alternative rhythm offered only if the writer wants that direction, with the original named as the deliberate choice), or flagged as a subjective choice (the editor's preference noted plainly while making clear it's a taste call the writer may have meant).

### Layer 4 — Editorial Judgment

Manuscript-level concerns.
- If something is technically correct but still awkward, fix it
- Use comments sparingly to flag author choices or alternatives
- Surface developmental observations on narrative flow, character consistency, scene purpose, motivation clarity, pacing
- Edit like a pro: confident, honest, efficient

Layer 4 developmental notes are *NOT* rewrites. They diagnose. The author decides what to do.

## Output

Two formats, depending on user request (default: Sample Edit Format).

### Sample Edit Format (default for flagged passages)

Per `../templates/fiction-sample-edit.md`:

```
> **Original:** "{verbatim passage}"
>
> **Rationale:** {what's wrong, plain terms — clichés, redundancy, vague verbs, awkward construction, voice issue. Distinguish subjective from objective.}
>
> **Suggested Edits:**
>
> 1. {first rewrite option, in author's voice}
> 2. {second rewrite option, alternate emphasis or rhythm}
```

Two rewrite options because voice judgments are subjective — the author picks the fit (or declines both). One option dictates. Two respect agency.

**When Layer 3 fires hard (the "leave it" case):** the two options can be `(Leave as written.) — {one-line reason the rhythm is voice}` paired with an optional alternative `(Only if you want X:) — {alternative rewrite}`. This is preferred over manufacturing a fake second option just to hit the count. The conditional alternative makes the choice auditable: the author sees the case for keeping AND the case for changing, side by side.

**Mechanical-only corrections (Layer 1):** if the manuscript has only mechanical errors (typos, grammar, punctuation), summarize them in a brief proofreader note rather than producing a Sample Edit block per fix. Sample Edit Format is for passages where rationale earns its space.

### In-Line Edited Manuscript (when the user wants the cleaned text)

The improved version, in full, without markup. Returned directly. The author pastes back into their draft. (Equivalent to running `humanize` for fiction — but with the Voice-Sensitive Filter applied.)

### Developmental Observations (Layer 4 output, when applicable)

For manuscript-level issues, looser format without rewrites:

```
> **{Issue type}:**
> "{specific observation about a chapter, scene, or beat}"
>
> **Suggestion:** {a structural suggestion, NOT a rewrite}
```

Issue types: Narrative Flow, Character Consistency, Scene Purpose / Redundancy, Motivation Clarity Gap, Pacing.

Worked examples of each issue type and the kind of suggestion that fits live in `../references/fiction-editing-layers.md` under "Developmental observation patterns."

## Output discipline

- **Don't rewrite or reimagine the author's scenes.** Clean, polish, elevate the original. Don't ghostwrite.
- **Distinguish subjective preferences from objective issues.** Flag both, weight differently. The author should know when you're naming a typo vs. a taste call.
- **Show options, don't dictate, when voice is the issue.** Voice judgments are subjective. Offering 2-3 alternatives respects agency.
- **Style of edits:** clean and confident, occasionally witty or sharp when warranted, never snide, minimal explanation unless requested.
- **Reads like a manuscript touched by a pro, not an algorithm.**

## Cross-mode suggestions (postamble)

After the fiction edit, point at the natural next move in one short line that fits the actual output. The typical next steps: when the issue is purely line-level and the developmental layer didn't fire, `suggest-edits` with the copy-edit lens is a faster pass for the next chapter; when tone is in question across a scene, `tone-profile`; when a chapter needs to come down in length without losing voice, `shorten`. Pick the one suggestion that fits — don't list all candidates.

## Design rationale

The 4 layers run in this specific order because each layer matches cost-of-fix (cheap to expensive) and the order lets the editor flag layered issues coherently. Proofreader catches mechanical errors (cheap to fix). Line Editor catches sentence-level prose. Voice-Sensitive Filter pushes back on the prior two when they'd homogenize. Editorial Judgment addresses story/character/pacing (most expensive to act on).

The Voice-Sensitive Filter sits as the *third* layer rather than fourth, deliberately positioned after Line Editor so it can push back on Line Editor's suggestions before Editorial Judgment runs. Without this layer, line-editing produces voice-homogenized prose — which is why the ordering matters for output quality.

Sample Edit Format uses two rewrite options because fiction editing requires showing the *original* alongside the change — voice and style are perceptible only by side-by-side comparison. The CE 101 suggestion-list format would lose this. Two options respect author agency. One option dictates.

"Show options, don't dictate, when voice is the issue" follows from the same logic: voice judgments are subjective, and offering alternatives lets the author pick the fit. "Distinguish subjective from objective, flag both, weight differently" follows too — the editor's role is not to impose taste but to make the gap between objective issues (typos, broken grammar) and subjective preferences visible to the author.

Developmental observations don't include rewrites because manuscript-level work — narrative flow, character, pacing — is the author's territory. The editor diagnoses the issue. The author decides the fix.

"Don't rewrite or reimagine the author's scenes" is the line between editing and ghostwriting. Editing keeps the setup, characters, beats, and outcomes. Ghostwriting changes them. Fiction-edit stays on the editing side.

