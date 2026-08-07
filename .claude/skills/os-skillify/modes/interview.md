---
name: interview
description: >-
  Sub-mode of `os-skillify`. Build a skill brief conversationally when source material is thin. Output is a brief artifact downstream sub-modes (`from-prompt`, `from-content`, `microtool-from-content`, `microtool-from-job`, `enhance`, `dual-lane`) consume. Six phases: Sufficiency check → Type-lens detection → Targeted questions (paced, one or few at a time, type-lens-aware) → Assemble brief artifact → Confirm with user → Hand off. Brief quality bounds output quality — this mode treats brief-building as craft, not setup overhead. Triggers on "interview me for a skill brief," "help me figure out what this skill should do," "build me a brief before drafting," and auto-invoked when downstream sub-modes detect insufficient input. Do NOT trigger when the input is already a complete brief (proceed directly), or for tool-design clarification inside `microtool-from-job` (that mode runs its own narrower interview).
---

# Sub-mode — Skillify interview

Build a skill brief conversationally. The output is a brief artifact downstream sub-modes consume.

This mode exists because **brief quality bounds output quality**. The single highest-leverage point in the skillify workflow is the brief: it sets the correctness floor for `consolidate`, the divergence target for `dual-lane`, the conversion scope for `from-prompt` / `from-content`, and the long-term intent record for any later `enhance` run. Building the brief is itself craft, not setup overhead.

## When to use

- **Standalone:** *interview me for a skill brief*, *help me figure out what this skill should do*. The user wants to think through a skill before drafting starts.
- **Auto-invoked:** when `from-prompt`, `from-content`, `enhance`, or `dual-lane` detects insufficient input (no spec, no existing skill, vague intent, missing failure-mode awareness, no named target output, no boundary statements).

Don't trigger when the input is already a complete brief — proceed directly to the requested mode.

Note the boundary with the narrower interview inside `microtool-from-job`: that mode runs its own thin clarification (three pieces — input, output, transformation) when a stated need is too thin to design from. The two patterns share craft and share a reference (`../references/interview-the-need.md`) but operate at different scopes. `microtool-from-job` clarifies *one tool's design-readiness* in 2-4 questions; `interview` mode builds *a full skill brief* across the core question pool and type-lens follow-ups.

## Preconditions

The parent dispatcher's two gates apply (inheritance protocol + map-before-make), but with a softer touch — interview mode is conversation, not generation. The inheritance protocol's outputs (especially voice, conventions, existing-skill awareness) inform what questions are worth asking and which are answerable from context already.

This mode doesn't write skill files. Writes follow `../../_shared/references/skill-update-protocol.md` only when the brief artifact itself gets persisted in Phase 4.

## Workflow

### Phase 1 — Sufficiency check

Before asking any questions, check what the user already provided. Skip questions whose answers are evident.

Signals the input is sufficient *without* an interview:

- A complete brief artifact already exists
- A thorough spec / design doc covers the skill
- An existing skill stub captures purpose, modes, ownership, inputs, outputs

If sufficient → don't interview. Confirm: *"I see you've given me [X]; this looks complete enough to skip the interview. Should I proceed with [target mode]?"*

### Phase 2 — Type-lens detection

If type isn't specified, ask early — this changes which questions you'll ask:

> *Is this skill creative-leaning (variety / voice / subjective quality — like fiction or persona skills), technical-leaning (precision / invariants / verifiable — like code or deployment skills), or hybrid?*

Don't ask other questions until type is settled. The question pools differ.

If the user is uncertain, offer a quick-disambiguation: *"What's the failure you're most afraid of — output that feels like AI wrote it, output that breaks in production, or both?"* The answer usually settles type.

### Phase 3 — Targeted questions (paced, one or few at a time)

Per the AGENTS.md *Pace me* principle, ask questions one at a time (or in small clusters of 2-3 closely related questions) rather than dumping a full list. Wait for answers; let answers inform follow-ups.

See `../references/interview-the-need.md` for the full question bank (folded together with the microtool-clarification pattern — same craft, two scopes). The five universal questions, in rough order:

1. **One-line purpose.** *"What's the one-line purpose of this skill?"* — forces concreteness.
2. **Concrete examples (in and out of scope).** *"Give me one concrete example of a request this skill should handle. And one example of a request it should NOT handle — something adjacent that could be confused for it."* — forces description discipline and lane boundaries.
3. **Good vs bad output.** *"What does good output look like? What does bad output look like — specifically, what would the model produce by default that you want to prevent?"* — surfaces failure-mode awareness (for creative skills, the anti-collapse target; for technical, the edge cases).
4. **Boundaries.** *"What does this skill NOT touch? Where does it hand off, and to whom?"* — forces lane-discipline; surfaces handoff partners.
5. **Source material.** *"Are there existing prompts, docs, examples, or sibling skills I should read first?"* — hunts for material the user has but didn't mention. Often the biggest leverage in the interview.

Type-lens-specific follow-ups:

- *Creative:* anti-collapse mechanism, persona/voice considerations, craft discipline, where variety helps vs hurts, per-output judgment surfaces.
- *Technical:* invariants, test fixtures, boundaries it must not cross, failure modes that break production, edge cases.
- *Hybrid:* draw from both pools situationally — ask which sections want which lens.

Optional probe questions (when the brief is still thin after the core five — see `../references/interview-the-need.md`).

### Phase 4 — Assemble the brief artifact

After enough has been gathered, write the brief as a markdown file. Convention: `experiments/<skill-slug>/BRIEF.md` (or wherever the user prefers). Standard brief sections (adapt to project house style):

- *Project context + authoritative reading order*
- *Target skill purpose + existing stub (if any)*
- *Source material pointers*
- *Hard constraints*
- *Required capabilities + outputs*
- *Composition (runtime inputs)*
- *Hard things to get right (the decisions that hinge on judgment)*
- *Test fixture (if applicable)*
- *Form & style expectations*
- *Output paths*
- *Divergent-strengths instructions* (if heading to `dual-lane`)

The brief follows the skill-update-protocol's show-before-write when persisted: surface the proposed brief, wait for confirmation.

### Phase 5 — Confirm with the user

Show the brief. Ask: *"Does this capture what you want? Anything missing, wrong, or worth tightening before we proceed?"*

If revisions needed → revise → re-confirm.

### Phase 6 — Hand off

Return the brief path and the next-mode invocation: *"Brief at [path]. Ready to proceed with [from-prompt / from-content / enhance / dual-lane]?"*

The brief is now a first-class artifact. Downstream sub-modes consume it.

## Operating principles

- **Pace the questions.** One or a few at a time. The user's AGENTS.md *Pace me* principle applies — 25 follow-up questions trivially overwhelm a human even if all 25 need answering.
- **Skip questions whose answers are evident from prior input.** Read what's there first.
- **Settle type-lens early.** Don't ask other questions until type is known — the pools differ.
- **Pull the user's genius out.** This is content-interview territory. Frame the question that exposes their judgment, not the question that lets them rubber-stamp a generic skill. AGENTS.md *Pull my genius out* is the right register here.
- **Brief is a first-class artifact.** Worth writing it down and confirming, not just holding in conversation.
- **Don't manufacture scope.** If the user's initial request is *"a skill that helps with writing,"* don't expand it into a five-mode multi-input orchestration. Most thin requests are thin for a reason — the user hasn't decided what they want, and the interview's job is to surface their thinking, not to scope it up.

## Failure modes to watch for

- **Question-dumping.** Asking all five core questions at once. The user can't engage with that many in parallel. Slow down.
- **Skipping type-lens.** Asking creative-flavored questions for a technical skill (or vice versa) produces a brief that doesn't match the work.
- **Skipping the source-material question.** The user often has more material than they remember to mention.
- **Skipping confirmation.** Drafting the brief and proceeding without showing it to the user means downstream modes work from your interpretation, not the user's intent.
- **Recursive clarification.** If the user's answers are short or noncommittal and the conversation gets recursive (*"what kind of output?"* / *"I'm not sure"*), stop interviewing and surface a draft for them to react to. A draft to redirect is often easier than questions to answer in the abstract.

## See also

- `SKILL.md` — parent dispatcher
- `../references/interview-the-need.md` — folded question bank covering both microtool-clarification (3-piece input/output/transformation) and full-brief (universal questions + type-lens follow-ups)
- `../references/type-lens.md` — the type framework that shapes which question pool fires
- Downstream consumers: `modes/from-prompt.md`, `modes/from-content.md`, `modes/microtool-from-content.md`, `modes/microtool-from-job.md`, `modes/enhance.md`, `modes/dual-lane.md`

## Source provenance

The five universal questions and pacing discipline are adapted from the user's `os-content-interview` (formerly a mode of os-content-discovery) pattern (which itself adapted from legacy *I interview you to find content ideas* and *Content-Finder Interview Bot 2.0* prompts). The three-piece (input / output / transformation) framing folded into `interview-the-need.md` is preserved from the legacy *Inputs-to-Outputs Helper* prompt. The type-lens-aware follow-ups and full-brief scope are new in v2 — emerged from real-world experience drafting the Autowriter Fiction stack and observing that brief quality consistently bounded what either single-lane or dual-lane drafts could produce.
