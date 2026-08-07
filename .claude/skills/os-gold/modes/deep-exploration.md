# Mode: deep-exploration

Part of the `gold` skill. Selected when the user wants analytical depth, not just extraction — when the source is dense, conceptual, or worth thinking-partner work.

## Job

Apply three orthogonal insight engines to the source content, then extract golden nuggets from both the source *and* the exploration those engines produced. The output is part discussion, part nugget list — the exploration surfaces insights the user wouldn't spot in a fast read, and the nugget list captures what's worth saving.

You are not summarizing. You are exploring, understanding, and interrogating. Dig deeper. Always ask: *What does this really mean? What would make it false? What would push it further?*

## Run

1. **Apply Engine 1 — Recursive Question Architectures** (see `references/insight-engines.md`).
   - Run Question Cascades on the source's main claims.
   - Run Default Challenging on statements presented as obvious.
   - Run Problem Behind the Solution on any prescribed fix.

2. **Apply Engine 2 — Analytical Skeleton Mapping**.
   - Run Argument Scaffolding on the 2–3 key arguments (strip stories, rebuild as premise / logic / conclusion).
   - Run Connection Mapping to show how concepts causally or correlatively link.

3. **Apply Engine 3 — Authorial Cognition Tracing**.
   - Run Rule Extraction: surface the author's implicit operating principles.
   - Run Explanation Style Analysis: sequence / system / contrast / taxonomy.
   - Run Abstraction Ladder Tracking: where is the author confident-in-specifics vs. vague-in-abstract?
   - Run Repetition Significance: which ideas does the source restate? Those are the author's core commitments.

4. **Golden Nugget Extraction.** After the three-engine review, compile a list of golden nuggets from both the source and the exploration. Apply `../../_shared/references/what-is-a-golden-nugget.md` criteria. Include nuggets the exploration surfaced that the source itself didn't state — these are often the most valuable.

## Output

Structured markdown. Heavy prose (paragraph form) for the exploration sections, bullet list for the final nugget extraction.

```markdown
# [Title derived from source topic]

## Insight Engine 1: Recursive Question Architectures
[Paragraph exploration. Each sub-engine gets its own sub-discussion — Question Cascades, Default Challenging, Problem Behind the Solution.]

## Insight Engine 2: Analytical Skeleton Mapping
[Argument scaffolding and connection mapping, with claims rebuilt into premise / logic / conclusion form.]

## Insight Engine 3: Authorial Cognition Tracing
[Rules extracted, explanation style identified, abstraction ladder tracked, repetition noted.]

## Golden Nuggets
[Bulleted list. Each nugget: bold one-line articulation + 1–3 bullets of expansion. Deduplicated. Stand-alone.]
```

### Tone and style

- **Precise, curious, slightly provocative.** An active thought partner, not a passive reader.
- **Paragraph form** for the exploration sections. Bulleted only for the final nugget list.
- **Flesch-Kincaid grade level roughly 5–8** for the prose. Concepts requiring specific terminology should not be dumbed down, but the surrounding explanation should read accessibly. [TBD rationale — preserved from source as default; the source landed here and the level keeps insights accessible without intellectual preening, but the specific 5–8 band is not independently defended.]
- **Avoid emojis and em-dashes.** Note the latter — em-dashes get overused in LLM-prose. Use commas, colons, or parentheses instead.

## Design Rationale

- **Three engines, not one** — each engine operates on a different axis: Engine 1 on logic, Engine 2 on structure, Engine 3 on the author's mind. Using one alone misses what the others would catch.
- **Exploration before nugget list** — the engines surface material the source didn't state directly. Running the final nugget pass over both source *and* exploration means the extraction benefits from the analytical work. Without it, the nuggets are just what was already written. [inferred from source structure]
- **Paragraph prose for exploration, bullets only at the end** — bullets force a rigid structure onto analytical work that flows better in prose. The final nugget list benefits from the discrete structure bullets provide. The exploration doesn't. [stated in source: "Write primarily in paragraph form in great detail"]
- **FK grade 5–8 writing level** — keeps insights accessible even when the concept is complex. Prevents intellectual preening that would make a nugget less shareable.
