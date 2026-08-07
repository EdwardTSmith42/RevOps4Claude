# Microtool Anatomy — the canonical 7-section structure

The micro-tool sub-modes (`microtool-from-content`, `microtool-from-job`) produce tools with a canonical 7-section anatomy preserved from the *Microtool Prompt Maker* (MPM) legacy prompt. This reference documents what each section does, when to deviate, and how the anatomy maps onto Cowork-native skill format vs. copy-pasteable prompt format.

## The seven sections

**1. Task** — what the downstream LLM must do.

1-4 sentences. Names the action and the outcome. Avoids vague verbs like *"help"* or *"assist."* Specific verbs like *"extract,"* *"generate,"* *"reformat,"* *"score,"* *"interview,"* *"draft,"* are clearer.

Examples:

- *"Take a paragraph of customer testimonial and extract a single quotable line that captures the emotional core."*
- *"Given an outline and a target audience, draft an opening hook that earns the next paragraph's attention."*
- *"Score this draft for direct-response copy quality on a 5-axis rubric and return the rubric scores plus 2 specific revision suggestions."*

**2. Persona** — who the LLM should "pretend" to be.

When relevant. Some tools are purely procedural and don't need a persona — the action is clear without one. Others lean on a persona to calibrate voice, depth, and stance.

Examples:

- *"You are a copywriting director who has reviewed thousands of welcome emails."*
- *"You are a developmental editor with a sharp ear for narrative pacing and emotional truth."*
- *"You are a behavioral economist with a habit of finding the surprising lever in any system."*

When the source content has a strong author voice the tool should inherit, the persona section is where that voice lives.

**3. Constraints** — must-follow guardrails.

Hard rules the LLM must honor. Formatting (markdown, plaintext, length caps), style (tone, register), forbidden topics, exclusions ("don't include code"), positive requirements ("always include three examples").

Constraints are listed bullets, not paragraphs. Each constraint is one specific guardrail.

Examples:

- *"Output is plain text, no markdown formatting."*
- *"Length cap: 200 words."*
- *"Do not use exclamation points."*
- *"Always include at least one specific example."*

**4. Process Walk-Through** — step-by-step instructions.

How the LLM executes the task, in numbered steps. This is where the source's frameworks and phrasing get woven in verbatim where they fit.

Each step is one move. Total typically 3-7 steps. More than 10 steps signals the tool is doing too much — split into multiple tools or rethink the scope.

Examples:

- *"1. Read the supplied content. 2. Identify the single moment of emotional shift. 3. Extract the line where the shift happens. 4. Verify the line stands alone (makes sense without surrounding context). 5. Output the line."*

**5. Success Qualities** — what a great output looks like.

Bullet list. Names the qualities the output should have if the tool worked. Useful for the LLM as self-check criteria and for the user as a quality lens.

Examples:

- *"The output is a single line that captures the emotional core, not a summary of the testimonial."*
- *"The line stands alone — a reader who hasn't seen the source testimonial still gets it."*
- *"The line uses the testimonial-writer's voice, not generic phrasing."*

**6. Output Format** — the template the LLM fills.

The literal shape of what the tool produces. Could be a markdown structure, a code block, a numbered list, a single paragraph, a table, a JSON object.

When the format is rich, the section shows the template literally with placeholders. When the format is simple (e.g., "one line of plain text"), a one-sentence description suffices.

**7. Inputs** — what the tool needs to function.

1 required input + 1-3 optional inputs. The required input is the substantive material the tool operates on. Optional inputs sharpen calibration without being required.

Examples:

- *"Required: the customer testimonial text (50-500 words). Optional: the audience the quotable will be shown to. Optional: tone direction (more emotional / more analytical)."*

## When to deviate

The 7-section anatomy is the canonical shape, not a rigid template. Some tools genuinely don't need all seven sections. Some need additional sections.

**Skip Persona** when the tool is purely procedural. A reformatter, a scorer, a counter — these often work better without persona overhead.

**Skip Success Qualities** when the output format already enforces quality (e.g., a strict structured output that's either complete or not). For most tools the section is worth keeping because it gives the LLM self-check criteria.

**Add a Knowledge or Reference section** when the tool needs to load a body of knowledge to function. Cowork-native skills reference library artifacts — copy-pasteable prompts may include the knowledge inline.

**Add an Example section** when the tool's output is hard to describe without showing one. A worked example often beats abstract Output Format description.

**Order can flex.** The canonical order works well for most tools but isn't sacred. Some tools work better when Inputs come earlier (so the LLM knows what it has before knowing what to do).

## How the anatomy maps to Cowork-native skill format

When the tool ships as a Cowork-native single-mode skill, the 7 sections fold onto the mode-file structure:

| Anatomy section | Mode-file location |
|---|---|
| Task | `description:` field in frontmatter, expanded in the "When to use" section |
| Persona | Folded into the mode's stance — *"The mode operates as..."* in the run section |
| Constraints | Dedicated `## Constraints` section |
| Process Walk-Through | `## Run` section with numbered steps |
| Success Qualities | Folded into output discipline, success criteria, or constraints |
| Output Format | `## Output` section showing the template |
| Inputs | `## Inputs` section listing required and optional |

The frontmatter `description:` field carries the task and trigger language. Negative triggers handle the "do NOT use for X" logic that the legacy MPM didn't have.

## How the anatomy maps to copy-pasteable prompt format

When the tool ships as a copy-pasteable code-fenced prompt, all 7 sections live as labeled sections inside the code fence:

```
# TASK
<task statement>

# PERSONA
<persona description, when present>

# CONSTRAINTS
<bulleted constraints>

# PROCESS WALK-THROUGH
<numbered steps>

# SUCCESS QUALITIES
<bulleted qualities>

# OUTPUT FORMAT
<template>

# INPUTS
<required + optional list>
```

Wrapped in triple-backticks for clean copy-paste. Sections in capital letters with `#` headers for scanability.

