# Mode: atomize

Part of the `os-content-mining` skill. The default mode — selected whenever the user wants the full content kit rather than extracted procedures (`sop`).

## Run

Apply these nine steps in order. Each step produces an artifact the next step builds on. Steps 1–6 are *extraction* (what's already there). Steps 7–8 are *expansion* (what could be there). Step 9 is quality control.

### 1. Orient to the Source

- Skim once to understand the overall theme, domain, and level of sophistication.
- Identify who the content is *for* and what problem-space it operates in.

### 2. Extract Golden Nuggets

Identify high-signal insights that are:
- Counterintuitive or contrarian
- Experience-backed ("this worked / failed because...")
- Principle-driven rather than tactical fluff
- Broadly transferable beyond the original context

Cross-reference `../../_shared/references/what-is-a-golden-nugget.md` for the stand-alone test and quality criteria. Apply `../../_shared/references/creative-criteria.md` as a quality filter.

When the source deserves a deeper insight pass than an inline step can give — it's dense and conceptual, or it's a video or podcast where the speaker's energy and asides carry signal — offer to run `os-gold` here instead (`deep-exploration` for the former, `video-transcript` for the latter) and fold its output into this section. The inline extraction stays the default so the kit remains one self-contained run.

### 3. Surface Answered Questions (Implicit & Explicit)

- List the questions the content answers directly.
- Infer the questions it answers indirectly through examples, stories, or explanations.
- Rewrite each as a clean, audience-facing question.

This step is often the highest-leverage for downstream content — every strong question is a post, thread, or email subject line in waiting.

### 4. Identify Frameworks, Models, and Workflows

- Extract any step-by-step processes, decision rules, mental models, or repeatable sequences.
- **Name each framework descriptively, not creatively.** "Objection-Preemption Sequence" is usable. "The Viper Method" is a dead end.
- Clarify inputs, outputs, and when to use each.

### 5. Capture Sound Bites & Sharp Articulations

- Pull quotable lines, metaphors, or reframes that stand alone.
- Prefer language that compresses meaning or flips a belief.
- These are the artifacts most ready for immediate social use.

### 6. Abstract to Content Primitives

For each extracted element (insight, Q&A, framework, sound bite):
- Identify the *core idea* independent of the original story or example.
- Note what makes it valuable or sticky.
- Identify whether the source is the writer's own material or comes from someone else, then infer whether the source should remain the subject, act as evidence, or serve as a catalyst. See `../../_shared/references/source-to-content-transformation.md`.

A content primitive is the portable form of an idea — the thing you could hand another creator and expect them to work with.

### 7. Generate Content Angles & Concept Clusters

- Propose multiple content angles logically flowing from the source.
- When the source is a catalyst, develop each primitive through the writer's worldview, audience, experience, business, tensions, or adjacent beliefs. The concept should become self-sufficient rather than source commentary with the names removed.
- Preserve genuine first-party language and experience when the source belongs to the writer. Do not invent personal experience when it does not.
- Organize into clusters: education / persuasion / authority / narrative / tactical. (See `../references/angle-cluster-taxonomy.md`.)
- Keep angles format-agnostic — don't lock them to TikTok, email, threads. Channel decisions happen at the user's end.

### 8. Map Expansion Paths

For each primitive or angle, identify which could become:
- Short-form insights (social posts, threads, quick emails)
- Long-form essays or videos
- Email sequences or newsletters
- Framework explainers or mini-lessons

Show how one idea can ladder into others — the strongest content system has primitives that feed multiple pieces.

### 9. Quality Control Pass

- Remove any ideas that are generic, redundant, or weakly supported by the source.
- Ensure every extracted artifact traces back to a real moment, claim, or pattern in the content.
- For generated concepts, preserve that honest derivation while applying the source-removal, writer-ownership, audience-value, and contribution tests. A catalyst-based concept should survive without the source and contain new intellectual work from the writer's lens.
- Keep the source visible when it is the requested subject or useful evidence. Do not force source independence onto source-facing work.
- Check the shape against the source, not the template: sections should be full where the source was rich and sparse-or-empty where it wasn't. If every section came out evenly populated, that's a red flag that slots got filled instead of value extracted.

## Output

Six sections in the final deliverable. See `../templates/content-mining-output.md` for the canonical shape.

```markdown
## 1. Golden Nugget Insights

## 2. Answered & Implied Questions

## 3. Frameworks, Models, and Workflows

## 4. Sound Bites & Sharp Reframes

## 5. Content Angle & Concept List (Clustered)

## 6. Expansion & Repurposing Paths
```

### Cross-mode output rules

- **Extraction stays source-faithful; generation follows the source's intended role.** Nuggets, quotations, and frameworks trace back directly. Catalyst-based concepts retain an honest derivation but must work for a reader who never encountered the source.
- **If you use an uncommon term, define or clarify it.**
- **Explain yourself.** If a framework has four steps, illuminate all four steps in detail. Don't skimp.
- **Assume the reader is unfamiliar with the input.** Explain what needs explaining.
- **Err on the side of giving slightly more where the material is dense** — this skill's bias is depth over brevity, and depth means pushing strong material further, never padding thin material out. Sections earn their length from the source.
