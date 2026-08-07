---
name: os-editing/fiction-assessment
description: Score fiction manuscripts (chapters, scenes, stories, novels) across 6 fiction-calibrated dimensions (Grammar & Syntax, Mechanics, Prose Texture, Voice & POV, Scene & Story Architecture, Reader Pull) on a 1-10 rubric, deliver a calibrated revision-stage verdict (Polish / Tune-up / Surgery / Rebuild — or strict variant Refinement Stage / Moderate Revision Stage / Substantial Revision Stage / Foundational Reconstruction Stage), and produce 3-5 prioritized recommendations ordered by impact. Cite specific passages for every score. Triggers when the user wants a quality diagnosis with verdict on FICTION prose — "score this chapter," "how is this manuscript," "what stage is this story at," "is this novel chapter ready." Do NOT trigger when the user wants line edits (use `fiction-edit`), prose rewritten (rare for fiction — usually `fiction-edit` instead), tone described (use `tone-profile`), or non-fiction assessment (use `assessment`).
---

# Mode — Fiction Assessment

Multi-dimension scored review of a fiction manuscript section, with calibrated revision-stage verdict and 3–5 prioritized recommendations. The fiction-calibrated counterpart to `assessment` — different rubric dimensions, different scoring discipline, different format-specific notes.

## Why this is its own mode

Non-fiction `assessment` calibrates to argument, evidence, persuasion, scannability, and audience-appropriate clarity. Fiction calibrates to voice, POV, scene architecture, reader immersion, and pacing. Forcing both jobs into one rubric means either non-fiction prose gets graded on irrelevant fiction metrics or fiction gets graded on non-fiction defaults. Two rubrics, side by side, serve both jobs better than one rubric trying to span both.

## When to use

- "Score this chapter / scene / story / manuscript section"
- "How is this novel chapter doing?"
- "What revision stage is this manuscript at?"
- "Is this ready for beta readers / submission / agent query?"
- After running `fiction-edit` on a chapter, to verify the revised version's stage
- Before running `fiction-edit`, to identify which chapters most need the layered editing pass

## When NOT to use

- **Non-fiction prose** — use `assessment` instead. Different rubric.
- **Line-level fiction editing** — use `fiction-edit` directly. This mode produces a verdict and recommendations, not line edits.
- **Story development, plot architecture, character arcs across a manuscript** — those are fiction (story development) work, not editing. A future `fiction` skill will handle them. This mode comments on architecture *as it appears in the prose under review*, not on macro story structure across chapters not provided.

## Inputs

- The manuscript section (chapter, scene, short story, or novel excerpt)
- Optional: stated genre, target audience, voice goal, manuscript context (where the section sits in the larger work, debut vs. published author, intended publication path — traditional / indie / serial)
- Optional: stated writer skill level — informs prescription depth
- Optional: verdict variant preference (strict / friendly) — defaults to friendly unless the writer explicitly asks for blunt framing or names a publication-deadline context

## Run — the 5-step diagnostic cycle

### 1. Get the lay of the land — name the genre and intent BEFORE scoring

Fiction scoring is meaningless without knowing what the manuscript is trying to be. Establish before reading the second time:

- **Genre / sub-genre** — literary fiction, urban fantasy, hard-boiled crime, romance, YA contemporary, science fiction, etc. Different genres carry different conventions, and the rubric scores against the manuscript's genre, not absolute literary aesthetic.
- **POV and tense** — close third / first / omniscient / second, past or present. Note POV shifts, free indirect discourse, head-hopping (intentional or not).
- **Voice intent** — what is the writer reaching for? Noir-cool / lyrical-quiet / fast-pulpy / voice-forward-comedic? Infer from the prose if not stated, and flag the inference.
- **Manuscript stage** — finished draft / mid-revision / first draft / scene fragment. Affects what "Polish" vs. "Surgery" mean.
- **Position in larger work** — opening chapter / mid-novel / climax / standalone scene? Different positions have different jobs.
- **Author concerns** — anything the writer flagged. Even one sentence ("voice is intentional throughout") prevents miscalibration.

If parameters aren't explicit, infer them from the prose and *name the inference* in the top-line summary so the writer can correct it — what genre and sub-genre you're reading the piece as, what POV and tense, what voice register, what position in the larger work. The naming is brief and specific to what you actually inferred, so the writer can confirm or adjust in one line.

### 2. Diagnose the text

Read once for whole shape (chapter arc, voice, scene goals). Read a second time for line and texture. Score each of the 6 fiction-calibrated dimensions, then translate scores into verdict.

**Score the 6 dimensions:**

Technical foundation:
- **Grammar & Syntax (X/10)** — subject-verb agreement, tense consistency where intended, pronoun clarity, sentence structure correctness. Calibrated to allow intentional rule-breaks (fragments, run-ons, comma splices) when the manuscript demonstrably uses them as voice. Score the *intentional vs. accidental* distinction.
- **Mechanics (X/10)** — spelling, punctuation conventions (em-dash style, ellipsis style, quote style), capitalization, formatting consistency. Note inconsistencies that suggest copy-paste artifacts vs. intentional choices.

Stylistic effectiveness:
- **Prose Texture (X/10)** — word choice precision, sensory specificity, register consistency, lexical variety, vocabulary calibrated to genre, avoidance of generic / abstract verbs where concrete ones earn more, avoidance of stale metaphor (calibrated to the manuscript, not absolute aesthetic).
- **Voice & POV (X/10)** — POV consistency (no head-hopping unless intentional), free indirect discourse handling, distinction between narrator voice and character voice, voice fidelity to author's stated or inferred intent. The most important fiction dimension — weight accordingly when surfacing recommendations.

Story craft:
- **Scene & Story Architecture (X/10)** — scene goals and beats, scene-to-scene flow, exposition placement (info-dump vs. integrated), chapter shape, plot logic within the section under review, transitions and time markers. Comments on architecture *as it appears in the prose*, not macro story-structure questions outside the section.
- **Reader Pull (X/10)** — curiosity (what makes the reader keep going), immersion (sensory and emotional anchoring), character empathy / interest, momentum (pacing, scene-end hooks, micro-tension), through-line clarity. Sometimes called "engagement" in non-fiction. In fiction it's specifically the felt experience of reading forward.

For each score:
- **Cite specific passages.** Quote 2-3 words or a short span — abstract grades ("voice is good") are useless.
- **Voice & POV calibrated to writer's stated or inferred intent.** A deliberately rough voice scores high if intentional. A rough voice that drifts in and out of consistency scores lower regardless of polish.

**Translate the scores into a verdict** using the calibrated scale from `../references/revision-verdict-scale.md`:

| Most dimensions | Friendly variant | Strict variant |
|---|---|---|
| 8-10 | **Polish** | **Refinement Stage** |
| 6-7 | **Tune-up** | **Moderate Revision Stage** |
| 4-5 | **Surgery** | **Substantial Revision Stage** |
| Below 4 | **Rebuild** | **Foundational Reconstruction Stage** |

"Most dimensions" is the calibration anchor. If 5 of 6 dimensions fall in one band and one outlier is higher or lower, place the verdict in the band where most dimensions fall and call out the outlier in the prioritized recommendations.

Default to the **friendly variant** unless the writer has signaled blunt framing.

### 3. Prescribe improvements (3–5 prioritized recommendations)

Order by impact. For fiction, "impact" means: *if the writer acted on this single recommendation, how much would the chapter improve?*

Each recommendation:
- **Names the issue specifically** with a passage citation. Not abstract ("improve voice") but anchored — the specific passage where the voice contract breaks, the specific scene whose beats don't earn their space, the specific POV slip that pulls the reader out. Name what's happening, name where, and name the structural choice the writer can make (move the description, fold the scene, restore narrative distance) without dictating the specific replacement prose.
- **Says what to do.** Diagnostic without prescription is half a recommendation.
- **Calibrates to the writer's likely level of revision tolerance.** Don't recommend wholesale chapter restructuring on a Polish-stage draft unless absolutely warranted.

For fiction at Surgery / Rebuild stage, recommendations may include scene-level or chapter-level direction. For fiction at Polish / Tune-up stage, recommendations stay line- and passage-level.

3–5 recommendations is the default range.

### 4. Tailor to the manuscript context (format-specific notes)

After the core feedback, add a short paragraph calibrated to the manuscript's apparent target. Not all fiction has the same targets:

- **Literary fiction (debut / mid-career)** — agent / editor expectations on opening pages, prose-density vs. forward motion, ambition vs. legibility
- **Genre fiction (UF / fantasy / sci-fi / mystery / thriller)** — reader-promise satisfaction, genre-convention handling, world-building integration, series-vs-standalone signals
- **Romance** — POV intimacy, tension pacing, on-the-page chemistry, beat structure
- **YA / MG** — voice-forward first-person sustainability, pacing for the target reader's attention span, sensitivity considerations
- **Short story** — opening-page weight (story has to start in motion), word-economy
- **Novel chapter (mid-manuscript)** — connection to surrounding chapters, pacing relative to overall arc, scene goal achievement
- **Manuscript-in-progress vs. final draft** — recommendations for in-progress work focus on patterns, while for final-draft work they focus on the specific scene under review

If the user didn't specify, use what you inferred during step 1.

### 5. Double-check before delivering

Before returning the assessment:
- All 6 dimensions scored with specific passage citations
- Verdict calibrated to "most dimensions" rule
- 3-5 recommendations ordered by impact, each specific and prescriptive
- No advice that conflicts with the writer's voice, POV, stated intent, or genre
- Voice & POV score honors intent
- Did NOT slip into rewriting the manuscript — assessment produces guidance, not a revised version
- Recommendations match the manuscript's commercial register, not the editor's literary preference

## Output

```
## Top-line summary

{One paragraph — must-knows. Lead with the genre / POV / voice inference (so the writer can correct), the verdict, and the single biggest leverage point.}

## Scores

**Grammar & Syntax (X/10)** — {one-line rationale, cite specific passages, note intentional rule-breaks}
**Mechanics (X/10)** — {one-line rationale, cite specific passages}
**Prose Texture (X/10)** — {one-line rationale, cite specific passages, note generic-vs-concrete diction}
**Voice & POV (X/10)** — {one-line rationale, cite specific passages, note POV consistency or intentional shifts}
**Scene & Story Architecture (X/10)** — {one-line rationale, cite scene beats / structural choices}
**Reader Pull (X/10)** — {one-line rationale, cite where momentum / immersion / curiosity work or fail}

## Verdict

**{Stage label}** — {1-2 sentence diagnosis based on combined scores}

## Prioritized recommendations (top 3-5)

1. **{Specific issue, named, with passage citation}** — {what to do, why first}
2. ...

## Format-specific notes

{One short paragraph calibrated to the manuscript's apparent target — genre / publication path / position-in-work}
```

## Output discipline

- **Don't rewrite the manuscript.** This mode produces a diagnostic and prescription, not an edited version. If the writer wants line edits, they invoke `fiction-edit` next.
- **The author is unoffendable** but the diagnosis still has to be useful. Be blunt where it serves. Don't pad with reassurance for its own sake.
- **Cite passages for every score.** Without citations, the rubric is unfalsifiable.
- **Match prescription depth to revision tolerance.** Recommending wholesale restructuring on a near-final draft produces friction, not help.
- **Stay in the prose under review.** Don't speculate on chapters you haven't seen.

## Cross-mode suggestions (postamble)

After the assessment, point at the natural next action in one short line that fits the actual verdict. The typical next moves: act on the top recommendation at the line level via `fiction-edit` on the passages flagged here; verify tone register on a representative passage via `tone-profile`; re-run this mode on the revised section after the writer takes a pass. Pick the one suggestion that fits — don't list all candidates.

## Design rationale

The 6 dimensions are calibrated for fiction, not the non-fiction defaults. Lexical Precision becomes Prose Texture (sensory, register, vocabulary — fiction concerns). Structural Coherence becomes Scene & Story Architecture (scene beats, chapter shape, plot logic). Engagement & Impact becomes Reader Pull (curiosity, immersion, momentum). Voice & Tone widens to Voice & POV, because POV is a central fiction concern absent from most non-fiction.

Step 1 (Lay of the Land) requires naming genre and voice intent before scoring because fiction scoring is meaningless without that calibration. Pre-anchoring prevents the rubric from defaulting to literary-aesthetic norms when the manuscript is genre fiction.

Voice & POV is weighted highest among recommendations because POV consistency and voice fidelity are the most common fiction failure modes and the issues that most affect reader experience. A grammatically clean chapter with broken POV is worse than a slightly rough chapter with consistent POV.

Recommendations match the manuscript's commercial register, not the editor's literary preference. Pulpier fiction has different success criteria than literary fiction. YA has different criteria than adult. Series fiction has different criteria than standalone. The rubric scores against the manuscript's apparent target.

The mode was forked from `assessment` rather than overloaded into it because fiction and non-fiction calibrations are different enough that a single mode would muddle both. Two siblings with different calibration produce cleaner diagnostics than one mode trying to span both. The non-fiction `assessment` rubric calibrates poorly for fiction in specific ways: "Engagement & Impact" framed as message clarity and persuasive effectiveness doesn't fit fiction (Reader Pull — curiosity, immersion, momentum — is the equivalent); "Structural Coherence" framed as information hierarchy doesn't fit fiction (Scene & Story Architecture is the equivalent); "Lexical Precision" framed as register consistency undersells sensory specificity and prose texture; "Voice & Tone" doesn't carry POV concerns, which are the most common fiction failure mode. Two siblings sharing the 5-step diagnostic cycle, the verdict scale, and the verdict-not-arithmetic rule produce cleaner diagnostics than one mode trying to span both.

## Related references

- `../references/fiction-editing-layers.md` — the 4-layer process used by `fiction-edit`. Fiction-assessment can recommend fiction-edit as the follow-up, and this reference describes what that follow-up will do.
- `../references/revision-verdict-scale.md` — strict and friendly verdict variants, shared with `assessment`.
- `../references/editing-principles.md` — cross-mode principles. "Suggest, don't dictate" applies to recommendation framing.
