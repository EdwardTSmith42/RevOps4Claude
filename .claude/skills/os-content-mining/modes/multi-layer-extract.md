# Mode: multi-layer-extract

Part of the `os-content-mining` skill — the analytical middle rung of the depth ladder. Selected when the source is dense enough to reward layered analysis but the user wants idea generation rather than the full six-section kit `atomize` produces — a structured extraction + expansion across five analytical layers.

## Job

Apply the five-layer analytical framework to a source, then generate at least one content concept per angle surfaced in each layer. The output is a modular content atomization kit — every angle and every idea can be lifted out on its own and used without the rest of the document.

## Run

Apply the five layers in order. For each layer, surface angles. For each angle, brainstorm at least one actionable content concept. The content concepts are format-agnostic — don't lock them to TikTok / email / thread / etc.

Before generating concepts, identify whether the material belongs to the writer or comes from an external source, then infer whether it is acting as subject, evidence, or catalyst using `../../_shared/references/source-to-content-transformation.md`. The analytical angles may remain source-facing because they explain what the analysis found. When the source is a catalyst, the content concepts beneath them must make sense without the source and add the writer's own lens rather than merely restating the analysis.

See `../references/multi-layer-analysis-framework.md` for the full framework. Run summary:

1. **Layer 1 — Surface Analysis** ("face value"): core argument, actionable insights, counterpoints, pitfalls, solutions.
2. **Layer 2 — Truth Mapping & Reality Testing**: foundation check (what must be true), evidence test, broader context, futurecasting.
3. **Layer 3 — Assumption, Bias, & Blind Spot Analysis**: hidden beliefs, blind spots / gaps, competing approaches, flaw analysis.
4. **Layer 4 — Consequence & Impact Chains**: immediate impact, short/mid-term effects, long-term / ripple effects, macro industry evolution.
5. **Layer 5 — Narrative & Engagement Amplifiers**: personal story hook, what-if scenario, pattern interrupt, empathy / identity tie-in.

**Force at least one insight per layer, even if speculative.** This is the safeguard against the common LLM weakness of skipping layers when the source looks shallow. If a layer genuinely has no material, say so explicitly with a speculative angle rather than silently dropping the layer.

## Output

Per-layer section. Each layer lists surfaced angles in bold, and under each angle lists content repurposing ideas.

```markdown
## 1. Surface Analysis ("Face Value")

**[Angle 1 — a sharp one-sentence framing of the angle, written so it could anchor a post on its own]**
- [Practical how-to] [Idea concept / hook]
- [Thought leadership] [Idea concept / hook]

**[Angle 2]**
- [Lessons listicle] [Idea concept / hook]
- [Rant] [Idea concept / hook]

---

## 2. Truth Mapping & Reality Testing

**[Angle 1]**
- [Format] [Idea concept / hook]
...
```

Continue through all five layers.

### Modularity rule

Each section must stand alone. A reader should be able to lift any angle + its ideas and use them without the surrounding structure. Avoid references across sections ("building on angle 2" clutters modularity). For catalyst-based work, "stand alone" also means the eventual audience does not need the original source, speaker, or story. Apply the source-removal, writer-ownership, audience-value, and contribution tests before retaining a concept.

### Format labeling

Every idea is labeled with one of the six formats from `../../_shared/references/content-format-taxonomy.md`. If an idea fits multiple formats, pick the strongest fit and move on.

## Design Rationale

- **Force one insight per layer, even speculative** — the source names this as preempting an LLM weakness: skipping layers when the source "looks shallow." The safeguard catches the collapse where the model merges four layers into one. [stated in source]
- **Modular output (angles + ideas stand alone)** — the reader's job is atomization: lifting pieces. Cross-references between sections hurt modularity. [stated in source]
- **Five layers, not three or seven** — each layer operates on a different analytical axis: surface (what's said), truth (what must hold), bias (what's missed), consequence (what happens), narrative (how it feels). Collapsing any layer loses a distinct kind of angle. [TBD: this specific count-of-five is the source's framing; reference-grade but malleable per the framework's own malleability note.]
- **Format labels on content ideas** — every idea must resolve to a specific content format so the user can pick based on their own channel strategy. [inferred from source]
- **Preempts common LLM weaknesses** — the source names the failure modes (shallow analysis, skipping layers, lack of counterpoints, vague brainstorming, failing to connect to actionable outputs). Naming them explicitly gives the agent a checklist to self-correct against. [stated in source]

## References

- `../references/multi-layer-analysis-framework.md` — the five-layer framework in full
