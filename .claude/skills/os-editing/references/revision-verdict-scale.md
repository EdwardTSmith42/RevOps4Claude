# Revision Verdict Scale

Translates rubric scores into a calibrated revision-stage verdict for `modes/assessment`. Two language variants ship side-by-side: **strict** (Content Editor lineage) and **friendly** (Text Doctor lineage). Same calibration cutpoints, different language. Pick variant by user preference (or default to friendly).

## Cutpoints

Both variants use these score thresholds, applied to the multi-dimensional rubric scores (1-10 across Grammar / Mechanics / Lexical Precision / Voice & Tone / Structural Coherence / Engagement & Impact):

- **Most dimensions 8-10** → top stage
- **Most dimensions 6-7** → second stage
- **Most dimensions 4-5** → third stage
- **Most dimensions below 4** → bottom stage

"Most dimensions" is the calibration anchor. If 5 of 6 dimensions fall in one band and one outlier is higher or lower, place the verdict in the band where most dimensions fall and call out the outlier in the prioritized recommendations.

## Strict variant (Content Editor lineage)

Used when the user wants direct, professional, no-cushioning feedback. Default for B2B / commercial / professional contexts.

### Refinement Stage (8-10)
- **Diagnosis:** Technical elements nearly flawless. Strong, consistent voice and style. Excellent format alignment.
- **Action:** Targeted enhancements for polish.
- **Recommendation depth:** Surface-level — phrasing tweaks, single-sentence sharpenings, specificity bumps. Don't propose structural changes.

### Moderate Revision Stage (6-7)
- **Diagnosis:** Some notable technical issues. Voice/style inconsistencies present. Format adherence varies.
- **Action:** Systematic corrections with explanations.
- **Recommendation depth:** Sentence and paragraph level. Identify recurring patterns and prescribe consistent fixes (e.g., "you slip into passive voice in transitions — switch all eight cases to active").

### Substantial Revision Stage (4-5)
- **Diagnosis:** Frequent technical errors. Major voice/style inconsistencies. Significant format problems.
- **Action:** Comprehensive restructuring guidance.
- **Recommendation depth:** Section and structure level. Reorganize, rebuild paragraphs, reorder sections, sharpen the through-line.

### Foundational Reconstruction Stage (below 4)
- **Diagnosis:** Fundamental technical issues throughout. Voice/style requires complete recalibration. Format needs complete restructuring.
- **Action:** Core principles guidance and exemplars.
- **Recommendation depth:** Whole-piece. Suggest the writer reconsider the angle, audience, or format. Provide exemplars (links or named pieces) the writer can study before redrafting.

## Friendly variant (Text Doctor lineage)

Used when the user is a writer who appreciates a warmer voice in feedback (newsletter writers, hobbyists, students, authors). Same calibration, different framing.

### Polish (8-10)
- **Diagnosis:** Mostly rock-solid. Minor tweaks.
- **Action:** Targeted enhancements. The piece is close to done — final pass to surface a few sharpening opportunities.

### Tune-up (6-7)
- **Diagnosis:** Noticeable issues, but the foundation is sound.
- **Action:** Systematic fixes. Clean the recurring patterns and the piece tightens noticeably.

### Surgery (4-5)
- **Diagnosis:** Major flaws. Needs restructuring.
- **Action:** Section-level revisions. Identify which parts to rebuild and which can stay.

### Rebuild (below 4)
- **Diagnosis:** Time to start from core principles.
- **Action:** Step back from the line-level work and reconsider the angle, audience, or structure. The current draft is a useful map of where the piece could go but not the piece itself.

## Calibration rules

**Don't grade harder than the writer can act on.** Match prescription depth to the writer's skill level. A "Surgery / Substantial Revision" verdict given to a beginner can produce paralysis. The same verdict given to a professional produces useful focus. If the user has signaled their skill level (or it's clear from the draft), calibrate the prescription.

**Voice & Tone score is calibrated to the writer's stated intent, not absolute aesthetic.** A deliberately rough/raw voice scores high on "voice" if the writer intended that register, even if a polished editor would score it low on "polish." Voice score reflects voice fidelity to intent, not voice fidelity to a hypothetical ideal.

**Verdict, not number-crunching.** Even though the verdict maps to score bands, don't reduce the verdict to arithmetic. If the rubric scores produce a borderline case (e.g., three dimensions in the 6-7 band, three in the 4-5 band), use editorial judgment to land the verdict where it best serves the writer. Cite both bands' diagnoses in the verdict explanation.

**Outliers are flagged separately.** If 5 of 6 dimensions are at "Polish" level but Engagement & Impact is at "Surgery," the verdict is Polish (most dimensions) but the prioritized recommendations open with the engagement issue. Don't average — diagnose.

## Variant selection

When the user invokes `assessment`, they can name the variant ("score this with the friendly verdict scale") or the mode self-determines based on context:

- **Default to friendly** when the user is sharing personal writing, hasn't named a publication context, or sounds like they'd benefit from warmer framing
- **Use strict** when the user has named a commercial / professional context (sales copy, white paper, executive comms) or has explicitly asked for blunt feedback ("be brutal," "don't pull punches")

If unclear, default to friendly. The strict variant can feel cold to writers who didn't ask for it.

