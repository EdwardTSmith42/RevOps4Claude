# Mode: format-remix

Part of the `os-content-mining` skill — the quick rung of the depth ladder. Selected when the user shares a source and wants a fast set of content ideas across the six-format taxonomy, without a full mining run.

## Job

From any source — one-liner, notes, or full content — generate a set of novel, high-impact content ideas. Each idea is aligned to one of the six content formats. Every idea pushes beyond the obvious and embodies at least one of the five creative criteria.

## Run

1. **Read / orient.** If the source is long, skim for the main claims, angles, and tension points. If it's a one-liner, expand the implicit context mentally. Identify whether it is the writer's own material or an external source, then infer its role using `../../_shared/references/source-to-content-transformation.md`.
2. **Abstract the portable ideas.** Separate the useful principle, tension, mechanism, or implication from the source's particular speaker, story, and setup.
3. **Develop through the writer's lens.** When the source is a catalyst, add intellectual work from the writer's worldview, audience, experience, business, tensions, or adjacent beliefs. Do not manufacture personal experience when the available context does not supply it.
4. **Identify at least one angle per format.** Aim for six ideas minimum (one per format: practical how-to / strategic how-to / lessons listicle / thought leadership / rant / advice). If a particular format doesn't fit the source, force an angle rather than skip — you may discover a non-obvious fit.
5. **For each idea, check creative criteria.** Does it embody at least one of counter-intuitive / awe-inspiring / elegantly simple / relatable / actionable? If not, rework until it does.
6. **Apply the source-removal and contribution tests.** A catalyst-based idea must make complete sense without the source and contain more than a generic paraphrase of it. Subject- or evidence-based requests keep the source visible where it earns its place.
7. **Deduplicate.** If two ideas restate the same underlying insight, keep the stronger one.
8. **Check against "busy, skeptical reader."** Each idea must cut through noise. If an idea would fit into the flood of content the target audience already ignores, sharpen it or drop it.

## Output

Tight, post-idea-list format. No preamble. No framing. No afterword.

```markdown
**[Practical how-to]** [Tight post idea / working title — one sentence, rich with implication]

**[Strategic how-to]** [Tight post idea]

**[Lessons listicle]** [Tight post idea]

**[Thought leadership]** [Tight post idea]

**[Rant]** [Tight post idea]

**[Advice]** [Tight post idea]
```

Optional: 1–2 additional ideas under formats where the source is particularly rich. Cap at ~10 ideas total.

### Each idea should be

- Tight (one line, maybe two)
- Rich with implication (promises more than the title contains)
- Traceable (clearly derives from something in the source)
- Self-sufficient when the source is a catalyst (the reader does not need the original context)
- Developed through the writer's own lens rather than merely anonymized
- Sharp enough that a reader would want to click to see where it goes

### Each idea should not be

- Generic (could describe any post on the topic)
- The source restated
- Source commentary the user did not ask for
- Vague ("some thoughts on X")
- Format-mismatched (a "rant" that reads like neutral analysis, a "lessons listicle" without a theme)

## Design Rationale

- **One idea per format is the minimum, not ceiling** — forces breadth. The ceiling allows extra ideas in formats that fit the source particularly well. [inferred from source]
- **Creative criteria are quality bars, not labels** — every idea should satisfy at least one. Without this, the output devolves to bland. [stated in source]
- **Vantage-point rule (closer-in or bigger-picture)** — a tweet-sized source can become a lessons-listicle-sized angle, and a long article can become a sharp advice post. Without this rule, all ideas stay at the same altitude as the source. [stated in source]
- **Format-mismatch test** — a rant must run hot, a practical how-to must have steps, a lessons listicle must have a unifying theme. Mislabeling destroys the taxonomy's value. See `../../_shared/references/content-format-taxonomy.md`.
- **"Rich with implication"** — a good post idea promises more than the title contains. Flat titles underperform. [stated in source]
