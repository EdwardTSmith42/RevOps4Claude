# Mode: video-transcript

Part of the `gold` skill. Selected for video transcripts specifically — interviews, podcasts, talks, YouTube content. Uses signals that only exist in spoken content (energy shifts, incongruence between tone and claim, assumption-revealing asides) that text-extraction modes can't detect.

## Job

Mine a video transcript for the insights others miss. Not summarizing — extracting. The mode runs the T.A.K.I. method to surface speaker signals, then drills through three layers of gold (surface / bedrock / hidden vein), then isolates the "one sentence that changes everything" and runs the S.T.O.R.Y. filter on it.

## Run

### Phase 1 — T.A.K.I. Extraction Method

Apply four-letter signal detection across the transcript:

**T — Timestamp the Turns**
Identify every moment where:
- The speaker's energy shifts
- They transition topics
- They drop into a story or example
- They get uncomfortable or excited

Format: `[Timestamp] - What happened: "Energy shift when discussing..."`

**A — Assumptions Audit**
List every assumption the speaker makes, especially:
- "Everyone knows that..."
- "Obviously..."
- "The thing about X is..."
- Throwaway phrases that reveal their mental models

**K — Keyword Clusters**
Don't just find keywords — find **word families**. If they say "scale" but also "growth," "expand," "multiply" — that's a cluster revealing their mental model.

List the top 3–5 keyword clusters and what they reveal about the speaker's worldview.

**I — Incongruence Intel**
Where does their energy not match their words?
- What do they claim is "easy" but spend forever explaining?
- What do they say "doesn't matter" but keep returning to?
- Where do they contradict themselves?

### Phase 2 — Three Layers of Gold

Extract insights at three depths:

**Layer 1: Surface Gold (What They Said)**
- List 3–5 main tips / tactics / strategies
- Keep brief — everyone finds this stuff

**Layer 2: Bedrock Gold (Why They Said It)**
For each main point:
- What expensive problem were they trying to solve?
- What belief are they challenging?
- What assumption underlies their solution?

**Layer 3: Hidden Vein (What They Didn't Say)**
- What did they skip over?
- What did they assume you already knew?
- What made them uncomfortable?
- What questions did they avoid?

### Phase 3 — Million-Dollar Question Analysis

For the *most important* insight in the transcript, answer four questions:

1. **What expensive problem does this solve?** (Be specific about the cost.)
2. **What's the belief shift required?** (What old belief must die?)
3. **What's the "yeah but" objection?** (What would a skeptic say?)
4. **Where's the leverage point?** (If someone could only implement 10%, which 10%?)

### Phase 4 — Pattern Recognition (Alien Anthropologist lens)

Step back from the content and observe as if you'd never encountered this domain:
- What phrases do they repeat? What does that reveal?
- What "rituals" or processes do they describe?
- What tribal knowledge do they assume everyone has?

### Phase 5 — The One Sentence That Changes Everything

Identify the ONE sentence — from the transcript, or derived from their ideas — that would make a thoughtful reader stop and re-read it, because if it's true a chain of other things they believed must shift. The test is not whether it's clever; it's whether accepting it forces revision somewhere else in the reader's model.

Quote the sentence (or the derived articulation). Then explain in a short paragraph what specifically would have to change downstream if the reader took it seriously — that downstream-cascade is what makes it the game-changer, not the sentence's surface punchiness.

### Phase 6 — Make It Sticky (S.T.O.R.Y. Filter)

Take the biggest insight and run it through the S.T.O.R.Y. filter (see `references/story-filter.md`):
- **S** — Simplify until a 10-year-old gets it
- **T** — Tell it through a specific scene
- **O** — Own it with a personal angle
- **R** — Relate it to a universal truth
- **Y** — Yield a clear next action

### Phase 7 — Contrarian Take

What's the *opposite* of their main insight that might also be true? Sometimes the real gold is in questioning the expert's premise.

## Output

Structured markdown. Clear headers for each phase. Scannable but deep — use bold, bullets, and blockquotes to make the insights pop.

```markdown
## T.A.K.I. Extraction
### T - Timestamped Turns
### A - Assumptions Audit
### K - Keyword Clusters
### I - Incongruence Intel

## The Three Layers of Gold
### Layer 1: Surface Gold
### Layer 2: Bedrock Gold
### Layer 3: Hidden Vein

## Million-Dollar Question Analysis
[Four-question drill on the most important insight]

## Pattern Recognition (Alien Anthropologist Lens)

## The One Sentence That Changes Everything
> [The quoted sentence]

[Why it changes everything]

## S.T.O.R.Y.-Filtered Insight
[Single insight run through all five S.T.O.R.Y. moves]

## The Contrarian Take
[Opposite of the main insight that might also be true]
```

## Design Rationale

- **T.A.K.I. as four specific letters** — Timestamps and Incongruence capture video-specific signals (timing and tone-vs-claim mismatch) that text modes miss. Assumptions and Keyword Clusters are text-extractable but valuable for revealing mental models. The four together cover what the speaker *says* (A, K), *how* they say it (T, I), and *why* (inferred from mental models K exposes). Reference-grade but malleable: a genuine need for a fifth signal (e.g., audience-interaction cues in live talks) may extend the method.
- **Three layers rather than one** — Surface is what any listener would catch. Bedrock is what a thoughtful listener would infer. Hidden Vein is what only a careful extractor would surface. Without the three-layer structure, extraction tends to stop at Surface. [inferred]
- **"One Sentence That Changes Everything" is mandatory** — forces the extractor to commit to a central insight. Without the commitment, output stays multi-point and nothing lands. [inferred]
- **S.T.O.R.Y. filter only on the biggest insight, not all** — running five moves on every nugget produces exhausting output. Selective application respects the reader's attention. [inferred from source placement]
- **Contrarian Take at the end** — the mode ends by questioning the expert's premise, which prevents the extraction from becoming hagiography. Sometimes the gold is in the opposite. [stated in source]
- **"Insights without action are just expensive entertainment"** — closing heuristic from source. The S.T.O.R.Y. filter's "Yield" step (clear next action) is where this bite applies. Every extraction should land somewhere useful, or it doesn't leave the page. [stated in source]

