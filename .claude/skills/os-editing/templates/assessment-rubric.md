# Template — Assessment Rubric

The output shape for `modes/assessment`. A scored multi-dimension review, a calibrated revision-stage verdict, and 3-5 prioritized improvement recommendations.

## Format

```
## Top-line summary

{One tight paragraph — the must-knows. What stage is this at? What's the single biggest opportunity? Where would the writer get the most leverage from a revision pass?}

## Scores

**Grammar & Syntax (X/10)** — {one-line rationale, cite specific passages}
- Subject-verb agreement, tense consistency, pronoun clarity, sentence structure correctness, subordination/coordination

**Mechanics (X/10)** — {one-line rationale, cite specific passages}
- Spelling, punctuation, capitalization, formatting conventions

**Lexical Precision (X/10)** — {one-line rationale, cite specific passages}
- Word choice accuracy, terminology, redundancy, cliché avoidance, register consistency

**Voice & Tone (X/10)** — {one-line rationale, cite specific passages}
- Consistency, audience appropriateness, alignment with stated intent, distinctiveness, emotional resonance

**Structural Coherence (X/10)** — {one-line rationale, cite specific passages}
- Logical progression, paragraph unity, transitions, information hierarchy, beginning/ending effectiveness

**Engagement & Impact (X/10)** — {one-line rationale, cite specific passages}
- Reader interest, message clarity, memorability, persuasive effectiveness

## Verdict

**{Stage label}** — {1-2 sentence diagnosis of the revision stage based on combined scores. See `../references/revision-verdict-scale.md` for stage definitions.}

## Prioritized recommendations (top 3-5)

1. **{Specific issue, named}** — {what to do about it, why it's first}
2. **{Specific issue, named}** — {what to do about it}
3. **{Specific issue, named}** — {what to do about it}
{4-5 if warranted}

## Format-specific notes

{One short paragraph — if the user named a publication context (LinkedIn post, sales email, fantasy novel, etc.), how to make the piece shine for that medium. Skip if the format is generic or the user didn't specify.}
```

## Scoring rules

- **Cite specific passages for every score.** Abstract grades ("voice is good") are useless. Quote 2-3 words or a short span from the draft and name what the quoted passage exemplifies for that dimension — the score becomes auditable when the writer can read the quote and see the move.
- **Voice score is calibrated to the writer's stated intent, not absolute aesthetic.** A deliberately rough/raw voice scores high on "voice" if the writer intended that register, even if a polished editor would score it low on "polish." If intent isn't stated, infer from the draft and note the inferred intent.
- **Don't grade harder than the writer can act on.** Match prescription depth to writer skill level — wholesale restructuring recommendations to a beginner produce paralysis. Tweaks-only to an experienced writer produce under-improvement.
- **Per-dimension scoring forces specificity.** A single overall grade hides the lopsidedness that determines what to fix first.

## Verdict mapping

The verdict translates rubric scores into a revision stage. Two language variants are available — pick based on user preference (or default to the writer-friendly variant):

**Strict variant (Content Editor lineage):**
- 8-10 across most dimensions → **Refinement Stage**
- 6-7 across most → **Moderate Revision Stage**
- 4-5 across most → **Substantial Revision Stage**
- Below 4 across most → **Foundational Reconstruction Stage**

**Friendly variant (Text Doctor lineage):**
- 8-10 → **Polish**
- 6-7 → **Tune-up**
- 4-5 → **Surgery**
- Below 4 → **Rebuild**

Same calibration cutpoints, different language. See `../references/revision-verdict-scale.md` for the full stage definitions and recommended actions per stage.

## Recommendations rules

- **3-5 prioritized recommendations.** Fewer than 3 misses obvious wins. More than 5 produces overwhelm. (Why 3-5 specifically — TBD, preserved as default, malleable per user request.)
- **Order by impact, not by dimension.** The top recommendation is the one that, if acted on, would most improve the piece. Don't run through dimensions in order.
- **Each recommendation names the issue specifically.** Not abstract ("improve voice") but anchored — the specific passage where the issue lives, the specific contrast the writer can hear (the opener that clashes with the body register; the claim that goes unsupported across three paragraphs; the takeaway that trails into hedging). The writer should be able to point at the named passage and recognize the problem.
- **Each recommendation says what to do.** Diagnostic without prescription is half a recommendation.

## Output discipline

- Begin with `## Top-line summary` — no preamble before it
- Don't rewrite the author's text. The mode produces guidance, not a revised version. If the writer wants a rewrite, they invoke `humanize` or `suggest-edits`
- The user is unoffendable and crave feedback. Be blunt where the diagnosis warrants. Don't pad with reassurance

