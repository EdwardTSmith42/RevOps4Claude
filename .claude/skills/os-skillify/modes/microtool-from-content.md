---
name: microtool-from-content
description: >-
  Sub-mode of `skillify`. Designs a focused single-purpose tool from a body of content (transcript, article, podcast, chapter). Output: single-mode Cowork skill OR copy-pasteable 7-section prompt (Task / Persona / Constraints / Process / Success / Output / Inputs). Mirrors source frameworks, terminology, step-counts; lifts verbatim phrases. Triggers on "make a tool from this transcript," "build a focused tool from this content," "design a micro-tool from this material," "give me a copy-pasteable prompt that does X." Do NOT trigger for full multi-mode skill (sibling `from-content`) or need-only-no-content (sibling `microtool-from-job`).
---

# Mode — Microtool from content

Design a focused single-purpose tool from a body of content. The tool does one thing well — it operationalizes the single highest-leverage move from the source content rather than capturing the full domain.

## When to use

The user has content (transcript, article, podcast, chapter, lecture notes) and wants a focused tool that captures the most useful move from it. The use case is narrower than `skill-from-content` — the user doesn't need a multi-mode skill, they need one tight tool.

If the user wants a multi-mode skill from the same content, route to sibling `from-content`. If the user has no content but does have a need, route to sibling `microtool-from-job`. If the user has a working prompt already, route to sibling `from-prompt`.

## Preconditions

Two gates apply before this sub-mode runs, per the parent `skillify` dispatcher:

1. **Inheritance protocol** — loads Personal OS context per `../../os-tune/references/inheritance-protocol.md`. The produced tool inherits voice and convention compliance.
2. **Map-before-make check** — runs the routing logic per `../../os-tune/references/figure-it-out-routing.md` to surface whether the request is actually a candidate for `extend` or `refine` against an existing skill.

Before writing the produced tool — whether Cowork-native skill or copy-pasteable prompt — load `../../_shared/references/skill-prompting-principles.md` and apply its principles. The copy-pasteable format is especially exposed to verbatim-example leakage, since the whole prompt ships as a single artifact a user will paste into other LLMs; placeholder phrasings should describe effect, not supply text.

Also load `../../_shared/references/self-extending-skills.md` and decide whether the produced tool is additive or complete. Microtools lean *complete* more often than full skills do — they're typically single-job focused tools by design — but exceptions exist. When the tool encodes an additive job (a writing producer, a generator that grows with the user's examples), the produced artifact carries the self-extending section even at microtool scale. When the tool is genuinely single-job (a one-shot classifier, a single-purpose transformer), omit it.

See `SKILL.md` for the gate logic.

## Inputs

- **Required:** Source content. Transcript, article, podcast episode, chapter draft, lecture notes, or other long-form material. Length typically 500-30000 words.
- **Required (or asked):** Output format preference — Cowork-native single-mode skill or copy-pasteable code-fenced prompt. The mode asks if not specified.
- **Optional:** Stated direction on which move to operationalize. Source content often implies multiple potential tools — the user can name which one they want. Without direction, the mode picks the highest-leverage move and surfaces the choice for confirmation.
- **Optional:** Voiceprint via `os-library/find` when the source content is in the user's voice and the tool should preserve that.
- **Optional:** Examples of similar tools the user has used and liked or disliked.

## Run

The mode runs through five steps. The user-decision points are at step 2 (which move to operationalize) and at step 3 (output format if not pre-specified).

### Step 1 — Digest the content

Read the content fully. Identify:

- All micro-tools potentially described or implied (the source often implies multiple)
- Frameworks, catch-phrases, signature terminology, step-counts
- Verbatim lines and paragraphs that drive home concepts and would lose force if paraphrased
- Promised outcomes — what the content claims its readers can do after applying it

### Step 2 — Pick the single highest-leverage micro-tool

The source typically implies multiple potential tools. Surface 2-4 candidates briefly (one-line descriptions), then recommend the highest-leverage one with rationale. The user confirms or picks differently.

The "highest-leverage" tool is the one that:

- Captures the source's most actionable move
- Has the clearest input → output transformation
- Would be used most often by the target audience

When the user has supplied direction ("I want the headline-writing tool from this content"), skip the surface-and-recommend step and design directly.

### Step 3 — Confirm output format

Cowork-native single-mode skill or copy-pasteable code-fenced prompt? The full tradeoff is documented in `../references/output-format-tradeoffs.md`. Short version:

- **Cowork-native** when the tool will live in this Cowork environment, expects iteration, integrates with library
- **Copy-pasteable** when the tool will be used in another LLM, shared with non-Cowork users, dropped into one-shot contexts

If the user already specified, skip this step. Otherwise ask.

### Step 4 — Design the tool

The tool follows the canonical micro-tool anatomy from `../references/microtool-anatomy.md`. Seven sections:

1. **Task** — 1-4 sentences naming what the downstream LLM must do
2. **Persona** — who the LLM should "pretend" to be (when relevant — can be omitted for purely procedural tools)
3. **Constraints** — must-follow guardrails (formatting, style, length caps, forbidden topics)
4. **Process Walk-Through** — step-by-step instructions, weaving in the source's frameworks and phrasing verbatim where they fit
5. **Success Qualities** — bullet list of what a "great" output looks like
6. **Output Format** — markdown or plain-text template the LLM must fill
7. **Inputs** — 1 required input + 1-3 optional inputs needed to make the tool function

For Cowork-native skills, the same anatomy maps onto the mode-file structure (frontmatter description = task, persona folds into the mode's stance, constraints + process + success + output map directly, inputs map to the inputs section).

For copy-pasteable prompts, all seven sections live inside the code-fence as labeled sections.

Apply craft preservation from `../references/craft-preservation-from-content.md`:

- Mirror source frameworks by name
- Lift uniquely memorable verbatim phrases
- Mirror step-counts exactly (3 pillars stays 3, not 5)
- Stay inside the source — flesh out what's implied, don't invent new frameworks
- Capture source terminology

### Step 5 — Output

Writes follow `../../_shared/references/skill-update-protocol.md` — show before write, sanity-check after. The microtool produces fewer files than from-content (one or two), but the protocol's batch-confirmation and sanity-check discipline applies the same way. For Cowork-native skill writes, wrap in auto-save: invoke `os-autosave snapshot` with a name like `pre-microtool-<name>` before persisting, then `os-autosave commit` with message `os-tune skillify: <name> — microtool from content` after a successful sanity check. If sanity check fails, revert to the snapshot. (Copy-pasteable prompt outputs don't touch the workspace and don't need auto-save wrapping.)

For Cowork-native skill:

- Write `SKILL.md` at `/skills/<name>/` with frontmatter, description, single-mode reference, library integration if appropriate
- Write `modes/<name>.md` with full mode structure
- Optional reference if the tool's craft warrants depth beyond what fits in the mode file

For copy-pasteable prompt:

- Output a single markdown code fence containing the full 7-section prompt
- Above the code fence, briefly note the source it came from and which move it captures
- After the code fence, suggest where the user might keep it (paste into a doc, save as a template via `os-library/save`, drop into a project file)

Surface the produced tool to the user. Iterate as needed.

## Output examples

### Cowork-native single-mode skill (skeleton)

```
/skills/<name>/
├── SKILL.md         (frontmatter + description + one-mode skill body)
└── modes/<name>.md  (full mode file with all 7 anatomy sections folded in)
```

### Copy-pasteable code-fenced prompt (skeleton)

_(Triple-backticks shown literally below as `[OPEN CODE FENCE]` / `[CLOSE CODE FENCE]` — copy these markers as real triple-backticks along with the inner content into your destination.)_

    **Source:** <article / transcript / book chapter title>
    **Tool:** <one-line description of what it does>

    [OPEN CODE FENCE]
    # TASK
    <1-4 sentences>

    # PERSONA
    <role description>

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

**One tool per invocation.** Don't try to surface multiple tools from one content body in a single mode run. If the source implies multiple high-leverage tools, the user can re-run the mode for each one.

**Don't pad.** A focused tool is short. The 7-section structure should fit on one screen for most jobs. Long meandering tools fail at the focused-purpose test.

**Lift verbatim where it adds fidelity.** Source content has signature phrasing that the tool inherits. Paraphrasing flattens the tool's voice and authority.

**Mirror step-counts.** Exact count preservation, not rounding for symmetry.

**No new frameworks.** The tool stays inside the source's framework. Inference about what the source implies is fine — invention is not.

**skillify conventions on Cowork output.** When producing a Cowork-native skill, no semicolons in body prose, restrained bullets, frontmatter compliant. The copy-pasteable prompt format follows the source author's voice rather than skillify conventions — that's the point of the portable format.

## Cross-mode suggestions

After `microtool-from-content`:

- Test the tool on real input. Iterate via re-running the mode with adjusted direction, via direct edits, or via `refine` once the tool is a Cowork-native skill.
- If the produced tool feels like it should grow into a multi-mode skill (the content has more useful moves), re-run as sibling `from-content`.
- If the user wants to save the produced copy-pasteable prompt as a reusable template, route to `os-library/save` with `type: template`.

