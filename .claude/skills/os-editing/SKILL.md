---
name: os-editing
version: 0.1.0
description: >-
  Edit existing prose — content, articles, blog posts, emails, copy, fiction
  manuscripts. Routes across seven modes: suggestion-list edits across selectable
  lenses (copy-edit, redundancy, active-voice, specificity, developmental,
  what-why-how, takeaway), 4-dimensional tone profiling, full AI-tell removal
  that may restructure (`humanize`), scored non-fiction assessment with revision
  verdict, fiction-specific assessment, voice-preserving compression, and
  4-layer fiction manuscript editing. Triggers on "edit this," "review this
  draft," "tighten this up," "what's the tone," "remove AI tells," "humanize
  this," "de-slop this draft," "score this writing/chapter," "shorten this,"
  "edit my chapter/scene/story." Do NOT trigger for drafting from scratch
  (`os-writing`), brainstorming, or generating hooks, headlines, or outlines.
  Do NOT trigger for transcript cleanup or content extraction
  (`os-content-mining`).
display_name: Editing
tagline: Edit existing prose without losing the writer's voice.
category: Editing
packs:
  - creator-pack
icon: phosphor:PencilLine
when_to_use: |
  Reach for this when you have a draft and want *better* prose, not *different* prose. Pick by feedback shape:

  - `suggest-edits` — numbered list of focused improvements across selectable lenses (copy-edit, redundancy, active-voice, specificity, developmental, what-why-how, takeaway).
  - `tone-profile` — describe or score a piece's tone across four dimensions.
  - `humanize` — the machine fingerprints taken off at every altitude, structure included, returned as finished prose.
  - `assessment` — scored verdict with a revision-stage recommendation.
  - `shorten` — compress 5–20% without flattening voice.
  - `fiction-edit` / `fiction-assessment` — manuscript-shaped work with a fiction-calibrated rubric.

  The thing this skill does that bare-LLM editing usually doesn't: respect a stated voiceprint, so the edit lands in the writer's register instead of regressing toward the model's mean.
modes:
  - name: suggest-edits
    job: Numbered suggestion list across selectable lenses — copy-edit, redundancy, active-voice, specificity, developmental, what-why-how, takeaway.
  - name: tone-profile
    job: Describe a piece's tone across four dimensions, or score it against a stated target.
  - name: humanize
    job: Composition pass, skeptical-reader audit, then a line pass — AI-tells removed at every altitude and the draft landed back in the writer's voice. May restructure.
  - name: assessment
    job: Scored verdict with a revision-stage recommendation.
  - name: fiction-assessment
    job: Fiction-calibrated scored assessment using a fiction-specific rubric.
  - name: fiction-edit
    job: Four-layer fiction manuscript editing — proofreading, line, voice-sensitive, editorial.
  - name: shorten
    job: Compress prose by 5–20% while preserving voice.
---

# Editing — multi-mode prose editing hub

## Purpose

Edit existing prose across whatever shape the user needs: focused suggestion lists, tone profiles, direct rewrites, scored assessments, length compressions, and fiction-specific manuscript editing.

Editing here means working on prose the user has already drafted. If the user is producing something new (a hook, an outline, a draft from notes), that is drafting work and lives elsewhere.

## When to use

- User shares a draft and asks for edits, feedback, suggestions, or a review
- User wants tone described, scored, or analyzed
- User wants prose rewritten to remove AI-tells without commentary
- User wants a scored assessment with revision-stage verdict
- User wants a draft compressed by 5–20% while preserving voice
- User wants fiction manuscript editing (layered: proofreading, line, voice-sensitive, editorial)

## Modes

This skill is **trigger-routed**. The user can name a mode directly ("run suggest-edits with the redundancy lens," "score this with the assessment rubric"), or describe the job and let the skill self-determine the right mode.

| Mode | Job | Output shape |
|---|---|---|
| `suggest-edits` | Editorial suggestion list across one or more selectable lenses | Numbered list with bolded `__Location__: / __Issue__: / __Suggestion__:` |
| `tone-profile` | 4-dimensional tone scoring + describers + anti-tones + supporting passages | Structured tone profile |
| `humanize` | Remove what makes non-fiction prose read as machine-made — composition, sentence, and vocabulary tiers — and land it in the writer's voice. May reorder, cut, and instantiate. | Edited content only |
| `assessment` | Multi-dimension scored review of non-fiction prose (1–10 across six non-fiction axes) + revision-stage verdict + 3–5 prioritized recommendations. Handles single pieces and multi-piece campaigns. | Scored rubric + verdict + ranked recs |
| `fiction-assessment` | Multi-dimension scored review of fiction manuscripts (1–10 across six fiction-calibrated axes — Grammar / Mechanics / Prose Texture / Voice & POV / Scene & Story Architecture / Reader Pull) + verdict + recommendations | Scored rubric + verdict + ranked recs (fiction-calibrated) |
| `shorten` | Compress non-fiction prose 5–20% while preserving voice, argument, and specifics | Shortened version + word-count delta + cut summary |
| `fiction-edit` | 4-layer fiction manuscript editing (proofreader → line editor → voice-sensitive filter → editorial judgment) with genre-calibrated voice protection | Sample Edit Format (Original / Rationale / Suggested Edits) per flagged passage |

### Self-determining when not specified

The first routing question is always **fiction or non-fiction.** Fiction signals: story, scene, character, chapter, manuscript, novel, fictional first-person/third-person prose with named characters and dialogue. If fiction, route to `fiction-edit` for line work or `fiction-assessment` for scored diagnostic. If non-fiction, the rest of the routing applies.

Non-fiction routing:
- **"Edit this" / "give me feedback"** without further specification → `suggest-edits` with the copy-edit lens (broadest sweep), and ask whether to add other lenses
- **"How is this writing" / "score this" / "what stage is this at" / "is this ready" / "be specific" / "be brutal"** → `assessment` (the right call when the user wants a *judgment* about quality and revision stage — suggest-edits is the right call when they want *suggestions* to act on)
- **"What's the tone"** → `tone-profile`
- **"Rewrite this to sound less AI-generated"** / "remove the AI tells" / "de-slop this" / "does this read as machine-written" → `humanize`
- **"Cut this down"** / "tighten this" / "make this shorter" → `shorten`

Fiction routing:
- **"Edit my chapter / scene / story" / "line edit this"** → `fiction-edit`
- **"Score this chapter" / "how is this manuscript / story / chapter / scene" / "what stage is this at" / "is this ready for beta readers / submission / agent query"** → `fiction-assessment`
- **"What's the tone of this scene"** → `tone-profile` (works on any prose)

When the request is ambiguous between `suggest-edits` and `assessment` (e.g., "give me detailed feedback on this"), default to `assessment` and offer to follow up with `suggest-edits` on the top recommendation. Same convention for fiction: default to `fiction-assessment` when the request is ambiguous between scored review and line work, then offer to follow up with `fiction-edit` on the top-flagged chapter / scene.

### Cross-mode chain pattern

Common non-fiction workflow: `assessment` → identify weak dimensions → `suggest-edits` with the relevant lens. Or: `humanize` first → then `shorten` if the result is still too long for its slot. That order matters — humanize has no length target and may well come back longer, so compressing first wastes the work.

Common fiction workflow: `fiction-assessment` on a chapter → identify weak dimensions and chapters → `fiction-edit` on the chapters that need line-and-developmental work. Repeat per major revision pass.

Document chains the user requests in the response so the user can run them again.

## Operating principles

These hold across all modes. Full content in `references/editing-principles.md`.

- **Mirror the author's language.** Don't introduce vocabulary the source doesn't use. Suggestions should feel like the author wrote them.
- **Specific over generic.** Vague writing is the most common failure mode and the hardest to self-diagnose. Prefer concrete nouns, named examples, numbers.
- **Preserve voice.** A clean edit that homogenizes voice is worse than a rough draft that's distinctively the writer's. Voice survives is the main constraint.
- **Suggest, don't dictate.** The author has final say. Frame edits as options where voice or style is at issue.
- **Don't edit for the sake of editing.** If a sentence is fine, leave it alone. The urge to "improve" everything degrades clean writing.
- **Read the whole piece before editing any of it.** Local edits without global understanding produce inconsistent voice and broken argument flow.
- **Don't return passages unchanged.** Suggestion-list output focuses on actionable items. A wall of "looks fine" entries hides the real issues.

## Inputs

Most modes accept the same shape of input:

- The draft text (paste or attached file)
- Optional: stated intent (target audience, register, publication context, voice goal)
- Optional: lens or mode selection
- Optional for `assessment` and `shorten`: target verdict tone (strict / friendly) or target reduction (5–20%)

## Output discipline

- `suggest-edits`, `tone-profile`, `assessment`, `fiction-edit` produce **structured analyses** the user reviews
- `humanize` and `shorten` produce **transformed text** the user pastes back into their draft
- Modes do not silently mix outputs. If a user asks for "feedback and a rewrite," run two modes explicitly

## Cross-mode suggestion postamble

After completing a mode, briefly point at the adjacent mode the writer is most likely to want next, framed as a natural continuation rather than recited script. Pick one suggestion that fits the actual output; don't list all candidates.

The common next moves: after a suggestion-list pass on the copy-edit lens, the natural follow-up is the scored diagnostic or a tone read; after a tone profile, structural work via the developmental lens lands if the tone is off; after a humanize pass, an offer to surface a diff or shorten further if length is still off; after an assessment, action on the top recommendation via the matching lens or a direct rewrite; after a fiction assessment, line-level work via `fiction-edit` on the flagged chapters; after `shorten`, an AI-tell pass via `humanize` if the compressed version still reads machine-flavored; after `fiction-edit`, a higher-level diagnostic via `fiction-assessment` if architecture is in question.

The postamble describes the next likely step in the writer's chain. It is not a script to recite, and the wording shifts to match the output.

## Design rationale

- **Seven modes rather than one monolithic editor** because editing has structurally distinct output shapes — suggestion lists, scored profiles, direct rewrites, calibrated verdicts, transformations, and layered manuscript edits don't compose as a single output. Forcing them into one mode would produce incoherent outputs.
- **Fiction and non-fiction assessment as separate sibling modes** rather than one assessment with conditional fiction calibration. The non-fiction rubric (Lexical Precision / Voice & Tone / Structural Coherence / Engagement & Impact) calibrates poorly for fiction concerns (Prose Texture / Voice & POV / Scene & Story Architecture / Reader Pull). Two siblings sharing the 5-step diagnostic cycle, the verdict scale, and the verdict-not-arithmetic rule produce cleaner diagnostics than one mode trying to span both. The mild duplication in mode files is the right trade-off.
- **Lens architecture inside `suggest-edits`** because different drafts need different lenses. Running all lenses on a tight draft produces noise. Running one lens on a sprawling draft misses structural issues. The user (or the skill) picks lenses per draft state.
- **`assessment` and `suggest-edits` as separate modes (not folded)** because their jobs differ: assessment produces a *verdict* (how much rework is needed), while suggest-edits produces *the rework itself*. Rolling them together either dilutes the verdict or buries the suggestions under a rubric.
- **`humanize` outputs ONLY the edited prose** with no commentary, no diff. The user is asking for the corrected text, not an editorial conversation. If they want a diff, they ask for one. Flags from its no-claim-lost check live in the surrounding message, never inside the prose.
- **`humanize` is allowed to restructure, and `shorten` is not allowed to be its lightweight twin.** The document-level tells — a story cashed out into a thesis, abstraction where an instance belongs, an ending that buttons — can't be fixed by swapping words, so the mode gets real surgery rights, bounded by an explicit no-claim-lost check. And it replaced the former `direct-rewrite` outright rather than sitting above it as a deeper option: a quick version of the same job is an invitation to route to the sloppy one.
- **`shorten` is its own mode (not a `suggest-edits` lens)** because it produces transformed text, not a suggestion list. Different output shape, different verification (word count delta, voice preservation).
- **`fiction-edit` lives in editing as a mode (not a separate skill)** because the job is editing prose, and the fiction-specific layers (Voice-Sensitive Filter, Editorial Judgment for scene/character/pacing) are domain calibrations of the same job. Reassess as a separate skill if fiction craft work (story development, character arcs, plotting) gets converted alongside.
- **Voice-Sensitive Filter as a *third* layer in `fiction-edit`** rather than fourth, deliberately placed after Line Editor so it can push back on Line Editor's suggestions before Editorial Judgment runs. Without this layer, line-editing produces voice-homogenized prose. Stated explicitly because the layer's placement directly determines output quality.
- **Cross-mode suggestion postamble** because the modes compose naturally (assessment → suggest-edits → humanize is a common chain) and surfacing adjacents teaches the user the hub's shape without overwhelming.

### TBD rationale (ship explicitly)

- **Why exactly 4 tone dimensions, not 3 or 5** — the framework works empirically but the choice of these specific axes (Formal/Casual, Serious/Funny, Respectful/Irreverent, Matter-of-Fact/Enthusiastic) is not defended in the source. Preserved as default.
- **Why 5–20% as the `shorten` range** — stated as default in source but not defended. Preserved.
- **Why "Polish / Tune-up / Surgery / Rebuild" as the friendly verdict scale** — the medical-procedure metaphor is intuitive but no rationale given. Preserved.
- **Why 3–5 prioritized recommendations in `assessment`** — not stated. Preserve as default, malleable per user request.

## First-time setup

os-editing is a consumer skill — the editing modes work without setup, but voice-targeted editing depends on a voiceprint matching the writer's register. Without one, `humanize` and the voice-match discipline in `suggest-edits` fall back to a voice-neutral cleanup, which is meaningfully weaker for writers with a settled style — and a cleanup with no voice to land in regresses toward the model's own register.

Recommended setup order: install `os-voiceprint` and create at least one voiceprint matching your primary writing register; install `os-writing` if you want the produce-then-edit chain to share references and library conventions; install `os-library` if you want briefs and style samples to surface automatically during edit work. None of these are hard requirements — os-editing graceful-degrades when references aren't available — but voice-targeted editing is the leap from generic to good.

## When the requested editing shape isn't yet a mode

Editing is open-ended at the lens layer: writers discover lenses they want repeatedly — a clarity lens, a CTA-strength lens, an opening-paragraph lens, a developmental lens calibrated specifically to their genre. The seven modes (and the seven lenses inside `suggest-edits`) cover the bulk of editing work but will not cover every shape a writer reaches for. When the user asks for an editing pass the existing modes and lenses don't fit, os-editing surfaces the gap explicitly and offers two paths rather than forcing the request into a wrong-shape mode or declining.

The first path is *set the lens or mode up for next time*. The user describes what the lens or mode should look for, optionally supplies one or two example edits they want the lens to produce, and os-editing hands off to `os-tune`'s `extend` to add the lens to `references/edit-lenses.md` and wire it into `suggest-edits` — or, when the new shape doesn't fit a lens (different output shape, different verification), to add a new mode file. The next request in this shape runs the same pass without re-supplying the framing.

The second path is *run it once, no setup*. The user just wants the pass now. os-editing applies the closest existing lens or mode as a structural starting point and the user's framing as the calibration, returns the output, and saves nothing.

os-editing is greedy about extension when the signal points at recurring need — a lens the user invokes by description multiple times, a register the user keeps producing for, a developmental focus their work routinely calls for. A one-off doesn't earn a saved lens. When the signal is ambiguous, the mode asks. The canonical principle and its application across the workspace lives in `../_shared/references/self-extending-skills.md`.

## Where outputs go

Outputs persist per the workspace storage methodology — see `../_shared/references/workspace-layout.md` (Knowledge system invariants): when the work belongs to an ongoing project, save silently to `os-outputs/` with dated frontmatter and a link trail; when the user is exploring, offer once. No skill-specific save scheme.

## Related skills

- `os-voiceprint` — produces the voice portrait used as a target for voice-fidelity editing. `humanize` removes AI-tells but doesn't enforce a specific voice unless a voiceprint is loaded. Pair with voiceprint output for voice-targeted editing.
- `os-writing` — the producer side of the writing workflow. The chain runs writing → editing in real use; the two share the anti-AI catalog and the voiceprint-loading discipline.
- `os-content-mining` — extracts structured content from transcripts and posts. Editing operates on already-drafted prose, not raw source.
- `os-gold` — surfaces high-leverage insights from existing work, not editing.
- `os-content-template` — extracts repeatable structural templates; adjacent to editing when the question is "what shape is this piece."
