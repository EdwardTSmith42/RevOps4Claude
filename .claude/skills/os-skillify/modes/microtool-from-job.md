---
name: microtool-from-job
description: Sub-mode of `skillify`. Designs a focused single-purpose tool from a stated need — a pain point ("I keep getting stuck on X"), a concept name ("design something around the Hormozi value equation"), or a job-to-be-done description ("when I'm reviewing weekly metrics, I want to..."). No source content required. Brief one-question-at-a-time clarification interview if the stated need is too thin to design from. Output is either a single-mode Cowork skill or a copy-pasteable code-fenced prompt with the canonical 7-section anatomy. Triggers on "design a tool that does X," "I have this pain point — what tool would help," "make me a micro-tool for [job]," "I need something that helps when I [scenario]." Do NOT trigger when source content is supplied (use sibling `microtool-from-content`), when the user wants a multi-mode skill (use sibling `from-content`), or when converting an existing prompt (use sibling `from-prompt`).
---

# Mode — Microtool from job

Design a focused single-purpose tool from a stated need — no source content required. The user describes a pain point, a concept they want operationalized, or a job-to-be-done, and the mode produces a tool that helps with it.

## When to use

The user has an immediate use case but no source content to work from. They know what the tool should help with, but they haven't written or read content that captures the framework yet — they just need a working tool, fast.

Common triggers:

- *"Design a tool that helps me [specific scenario]."*
- *"I keep getting stuck on [pain point] — what tool would help?"*
- *"Make me a micro-tool around [concept name]."*
- *"I need something for when I [job-to-be-done]."*

If the user has source content the tool should be built from, route to sibling `microtool-from-content`. If the user wants a multi-mode skill rather than a focused tool, route to sibling `from-content`. If the user has a working prompt, route to sibling `from-prompt`.

## Preconditions

Two gates apply before this sub-mode runs, per the parent `skillify` dispatcher:

1. **Inheritance protocol** — loads Personal OS context per `../../os-tune/references/inheritance-protocol.md`. The produced tool inherits voice and convention compliance.
2. **Map-before-make check** — runs the routing logic per `../../os-tune/references/figure-it-out-routing.md` to surface whether the request is actually a candidate for `extend` or `refine` against an existing skill.

Before writing the produced tool, load `../../_shared/references/skill-prompting-principles.md` and apply its principles. Because this sub-mode designs from a stated need rather than from source content, the temptation to fill placeholders with concrete sample phrasings is unusually strong — resist it; the placeholders should name the effect each slot is supposed to produce.

Also load `../../_shared/references/self-extending-skills.md` and assess whether the stated need is additive or complete. Asking the user "is this need likely to recur in new shapes, or is it stable as you've described it?" surfaces the answer quickly. Additive needs warrant a self-extending tool; complete needs don't, and adding the section would be over-engineering.

See `SKILL.md` for the gate logic.

## Inputs

- **Required:** A statement of need. Could be a pain point, a concept / framework name, or a job-to-be-done description. The shape of the statement varies — clarity matters more than format.
- **Required (or asked):** Output format preference — Cowork-native single-mode skill or copy-pasteable code-fenced prompt.
- **Optional:** Audience for the tool — *"this is for me"*, *"for my team"*, *"for my coaching clients"*, *"for public release."*
- **Optional:** Tone or stylistic direction — *"keep it tight,"* *"warm and conversational,"* *"strictly procedural."*
- **Optional:** Examples of similar tools the user has used and liked or disliked — calibrates design without forcing imitation.
- **Optional:** Voiceprint via `os-library/find` if the produced tool should match the user's voice.

## Run

The mode runs through five steps. Step 2 is the clarification interview, which fires only when the stated need is too thin to design from.

### Step 1 — Read the stated need

Parse what the user supplied. Try to identify three things:

- **The input.** What does the user have when they want to use the tool? (Notes? A piece of content? A blank page?)
- **The output.** What should the tool produce?
- **The transformation.** What's the move the tool makes between input and output?

If all three are clear from the user's statement, skip to step 3. If any is missing or ambiguous, run step 2.

### Step 2 — Brief clarification interview (only if needed)

When the stated need is too thin, run a brief one-question-at-a-time interview to clarify input / output / transformation. The full pattern is documented in `../references/interview-the-need.md`. Briefly:

- Ask one question per turn
- Bias toward the missing piece — if input is unclear, ask about input first
- Keep it short — typically 2-4 questions to reach design-readiness
- Don't drift into a full requirements-gathering session — the goal is just enough clarity to start designing

Common clarifying questions:

- *"What do you typically have at hand when you'd want to use this — notes, a transcript, a blank page, an existing draft?"*
- *"What does the output look like when it's right — a list, a paragraph, a structured document, a one-line answer?"*
- *"Walk me through one specific time you wanted this — what were you trying to do?"*
- *"What's the smallest version of this that would still be useful?"*

Once the clarification produces enough signal, proceed to step 3.

### Step 3 — Confirm output format

Cowork-native single-mode skill or copy-pasteable code-fenced prompt? See `../references/output-format-tradeoffs.md` for the full tradeoff. If the user already specified, skip. Otherwise ask.

### Step 4 — Design the tool

Without source content, the design relies on the user's stated need plus the mode's general knowledge. The seven-section canonical micro-tool anatomy from `../references/microtool-anatomy.md` applies:

1. **Task** — what the LLM must do
2. **Persona** — the role the LLM plays (when relevant)
3. **Constraints** — must-follow guardrails
4. **Process Walk-Through** — step-by-step instructions
5. **Success Qualities** — what a great output looks like
6. **Output Format** — template the LLM fills
7. **Inputs** — required + optional inputs

Without source content, the design tradeoffs are different from `microtool-from-content`:

- **No frameworks to mirror.** The tool's structure comes from the design itself, calibrated to the job. The mode can borrow well-known frameworks if the user names a concept (e.g., "Hormozi value equation" → use the value equation structure), but doesn't invent new ones.
- **No verbatim phrases to lift.** The tool's voice comes from the user's stated direction (or default professional tone), not from source language.
- **Heavier emphasis on input / output clarity.** Without content to anchor the transformation, the input and output sections need to be especially clear.

Apply pack conventions on Cowork-native output: no semicolons, restrained bullets, frontmatter compliant.

### Step 5 — Output

Writes follow `../../_shared/references/skill-update-protocol.md` — show before write, sanity-check after. Same discipline as sibling sub-modes. For Cowork-native skill writes, wrap in auto-save: invoke `os-autosave snapshot` with a name like `pre-microtool-<name>` before persisting, then `os-autosave commit` with message `os-tune skillify: <name> — microtool from job` after a successful sanity check. If sanity check fails, revert to the snapshot. (Copy-pasteable prompt outputs don't touch the workspace and don't need auto-save wrapping.)

For Cowork-native skill: full single-mode skill structure at `/skills/<name>/`.

For copy-pasteable prompt: single markdown code fence with the 7-section anatomy, a brief note above naming the job and a brief note below suggesting where to keep it.

Surface to the user. Iterate as needed — common adjustments include tightening constraints, adjusting persona, refining the process, sharpening the output format.

## Output examples

### Cowork-native single-mode skill (skeleton)

Same as `microtool-from-content` — full skill structure at `/skills/<name>/`.

### Copy-pasteable code-fenced prompt (skeleton)

_(Triple-backticks shown literally below as `[OPEN CODE FENCE]` / `[CLOSE CODE FENCE]` — copy these markers as real triple-backticks along with the inner content into your destination.)_

    **Job:** <one-line description of what need this tool addresses>
    **Designed for:** <audience — self / team / client / public>

    [OPEN CODE FENCE]
    # TASK
    <1-4 sentences>

    # PERSONA
    <role description, when relevant>

    # CONSTRAINTS
    <list>

    # PROCESS WALK-THROUGH
    <step-by-step instructions>

    # SUCCESS QUALITIES
    <bullet list>

    # OUTPUT FORMAT
    <template>

    # INPUTS
    - Required: <what>
    - Optional: <what>
    [CLOSE CODE FENCE]

## Constraints

**Don't design from a thin need.** If the stated need is genuinely unclear, run the clarification interview. Designing from ambiguous input produces tools that don't fit any actual use.

**Don't over-interview.** The goal is design-readiness, not full requirements specification. Typically 2-4 clarifying questions suffice. If the conversation extends beyond that, surface a draft and iterate from there rather than continuing to clarify in the abstract.

**Don't invent frameworks.** Borrow from well-known frameworks the user names (e.g., named author frameworks). Don't invent novel structures the source need doesn't imply.

**One tool per invocation.** If the user surfaces multiple jobs during the interview, design for the highest-leverage one and note the others as candidates for future runs.

**pack conventions on Cowork-native output.** Same standards as the rest of the pack.

## Cross-mode suggestions

After `microtool-from-job`:

- Test the tool on a real input. Iterate (via `refine` if the tool is a Cowork-native skill, or via direct edits if a copy-pasteable prompt).
- If the user's job hinted at adjacent needs, run the mode again on those needs.
- If the user finds source content that captures the tool's framework better, re-run as sibling `microtool-from-content` with that content.
- If the produced tool reveals the user actually needs a multi-mode skill (the job is bigger than one tool), re-run as sibling `from-content` once they have content.

