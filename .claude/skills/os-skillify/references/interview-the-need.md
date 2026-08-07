# Interview the Need — question bank for clarification and brief-building

> **Malleability note:** Two scopes share this reference because they share craft (one-question-at-a-time pacing, surface-the-missing-piece bias, draft-when-asking-fails). The question categories — input / output / transformation for thin needs, and purpose / examples / good-vs-bad / boundaries / source for full briefs — are canonical. Specific wording is adaptable.

This reference covers two adjacent jobs that share underlying craft:

- **Microtool clarification** (used by `microtool-from-job`) — get to *design-readiness* on a thin need: input, output, transformation clear. 2-4 questions, narrow scope.
- **Full skill brief-building** (used by the top-level `interview` mode) — produce a complete brief artifact downstream sub-modes consume. Five universal questions + type-lens follow-ups, broader scope.

The two scopes share pacing, framing, and draft-when-stuck discipline. The question pools differ.

## Shared craft (both scopes)

### One question per turn

Hard rule. No multi-part questions. The agent may respond with a brief acknowledgment (*"got it,"* *"makes sense"*) before asking the next question. This is the AGENTS.md *Pace me* principle applied at micro-scale.

Two-or-three closely related questions can occasionally cluster (e.g., *"What's the input? What does the output look like?"*) when the answers would naturally come together. Default to one.

### Bias toward the missing piece

Ask about what isn't clear yet, not what already is. If input is unclear, ask about input first. If output is unclear, ask about output. Don't run a fixed sequence — read the user's prior signal and bias to where the gap is.

### Keep it short

Microtool clarification: 2-4 questions reach design-readiness. If the conversation extends past 6, surface a draft and iterate from there.

Full brief building: the five universal questions plus 0-3 type-lens follow-ups is enough for most skills. Don't keep asking if the brief is sufficient.

### Don't drift into requirements gathering

The interview is for *clarity on what to design*, not full specification of every constraint and edge case. Constraints and details can be adjusted during iteration. Resist the impulse to scope-up just because asking is cheap.

### Don't ask questions whose answers are evident

Read what the user already provided first. If they've already said *"output should be a single quotable line,"* don't ask *"what does the output look like?"*

### Don't ask leading questions

*"Is this for headline writing?"* puts an answer in the user's mouth. *"What's the kind of writing this tool would help with?"* lets them tell you.

### Don't ask the user to abstract

*"What's the underlying job-to-be-done?"* is too abstract for most users. *"Walk me through one specific time you wanted this"* gets concrete material the mode can abstract from itself.

### Surface a draft when asking stops working

If the user's answers are short or noncommittal, or if the conversation gets recursive (*"what kind of output?"* / *"I'm not sure"*), stop asking and surface a draft instead. Draft from best-guess input + output + transformation (or best-guess brief shape), label the assumptions, let the user redirect:

> *"Here's a draft based on my best guess — assumes input is X, output is Y, transformation is Z. Adjust any of these and I'll re-design."*

A draft to react to is often easier than questions to answer in the abstract.

## Scope A — Microtool clarification (used by `microtool-from-job`)

### The goal

Get to **design-readiness**, not full requirements specification. Design-readiness means three things are clear:

- **The input.** What does the user have when they want to use the tool?
- **The output.** What should the tool produce?
- **The transformation.** What's the move the tool makes between input and output?

When all three are clear, design begins. The interview's job is to surface the missing pieces, not to interrogate every aspect of the user's situation.

### When the interview fires

Skip the interview when the user's statement already covers input + output + transformation. Examples that don't need interviewing:

- *"Design a tool that takes a customer testimonial and extracts the single most quotable line."* (Input: testimonial. Output: a line. Transformation: extraction.)
- *"Make me a micro-tool that scores a draft against the FFGA framework."* (Input: draft. Output: scores. Transformation: scoring.)
- *"I need something that turns my Friday weekly notes into a short Saturday-morning recap email I send myself."* (Input: notes. Output: email. Transformation: notes → recap.)

Run the interview when the statement is missing one or more of the three pieces. Examples that need interviewing:

- *"I need a tool for content stuff."* (Missing all three — content stuff to what end?)
- *"Help me with my newsletter."* (Missing input and output specifics — what aspect of the newsletter?)
- *"Make me a tool around the value equation."* (Missing input and transformation — apply the framework to what, in what way?)

### Useful question shapes

Questions that surface the input:

- *"What do you typically have at hand when you'd want to use this — notes, a transcript, a blank page, an existing draft?"*
- *"What's the raw material this tool would operate on?"*
- *"Show me the kind of thing you'd paste in when running this."*

Questions that surface the output:

- *"What does the output look like when it's right — a list, a paragraph, a structured document, a one-line answer?"*
- *"After running this tool, what do you have that you didn't have before?"*
- *"If the output were perfect, what would you do with it next?"*

Questions that surface the transformation:

- *"Walk me through one specific time you wanted this — what were you trying to do?"*
- *"What's the move the tool makes — is it extracting something, generating something new, restructuring something, scoring something, or something else?"*
- *"What would you do manually if the tool didn't exist?"*

Questions that calibrate scope (when not the missing piece, but useful sometimes):

- *"What's the smallest version of this that would still be useful?"*
- *"Is this a one-shot or something you'd run repeatedly?"*

### Don't ask about audience too early

Audience matters for tone and persona, but doesn't block design-readiness. Save it for a follow-up after the three core pieces are clear.

### Acknowledging and moving forward

After 2-4 questions, the mode should reach a point where input + output + transformation are clear enough to design. At that point the mode briefly summarizes what it heard and starts designing:

> *"OK — sounds like you want a tool that takes Friday weekly notes (input) and produces a short Saturday-morning recap email (output) by extracting the wins and surfacing one thing worth thinking about over the weekend (transformation). I'll design a microtool for that — single-mode skill or copy-pasteable prompt?"*

The summary serves as a confirmation step and the mode-or-prompt question moves to design.

## Scope B — Full skill brief-building (used by the top-level `interview` mode)

### The five universal questions

These five are the core. Skip any whose answers are evident from prior input.

**1. One-line purpose**

> *"What's the one-line purpose of this skill?"*

Forces concreteness. If the answer is more than one sentence, the skill probably needs to be split or scoped down.

**2. Concrete examples (in and out of scope)**

> *"Give me one concrete example of a request this skill should handle. And one example of a request it should NOT handle — something adjacent that could be confused for it."*

Surfaces description discipline and the lane boundary. The *should NOT* example is the source of negative triggers in the eventual frontmatter description.

**3. Good vs bad output**

> *"What does good output look like? What does bad output look like — specifically, what would the model produce by default that you want to prevent?"*

Forces failure-mode awareness. For creative skills, surfaces the anti-collapse target. For technical, surfaces the edge cases / wrong outputs to guard against.

**4. Boundaries**

> *"What does this skill NOT touch? Where does it hand off, and to whom?"*

Forces lane-discipline. Maps to one-mutator-per-artifact thinking when applicable. Surfaces handoff partners.

**5. Source material**

> *"Are there existing prompts, docs, examples, or sibling skills I should read first?"*

Hunts for material the user has but didn't mention. Often the biggest leverage in the interview — what looked like a thin request becomes a substantial brief once the existing material is named.

### Creative-type follow-ups

Ask these *in addition to* the universal questions when type is creative.

**Anti-collapse mechanism**

> *"What's this skill's anti-pattern-collapse mechanism, if any? How does it prevent the model from defaulting to genre-mean output — wildcards, destabilizers, deliberate randomness, prose-form distinctions?"*

Names the active counter-pressure. If the answer is *"nothing yet,"* that's a craft conversation to have — the skill probably needs one.

**Persona / voice considerations**

> *"Whose voice or persona does this skill carry, if any? Is there a pen-name / character / brand identity it operates as? What does protecting that voice require?"*

Surfaces persona discipline. Even when there's no formal pen name, there's often an implicit voice (the user's, a target audience's, a genre's).

**Craft discipline**

> *"What's the craft discipline this skill enforces — one-mutator-per-artifact, plan / apply separation, another rule that keeps quality from getting diluted?"*

Many creative skills have a single discipline that, if violated, the skill fails. Naming it surfaces it.

**Where variety helps, where it hurts**

> *"Where does variety / randomness / risk-taking help in this skill's outputs? Where does it hurt? What stays consistent across all invocations?"*

Distinguishes variety-as-feature from inconsistency-as-bug.

**Per-output judgment surface**

> *"Does this skill make per-output judgments — picking a tone, choosing among options, deciding how much to lock vs leave open? If so, name 2-3 of those judgment points."*

Surfaces the decision points that matter most so they get explicit treatment in the `SKILL.md`.

### Technical-type follow-ups

Ask these *in addition to* the universal questions when type is technical.

**Invariants**

> *"What invariants must hold across all invocations of this skill? What must always be true after it runs, regardless of input?"*

The skill's contract. Often best stated as *"after this skill runs, [X] is true."*

**Test fixtures / example inputs**

> *"What's the test case — real or hypothetical — that would prove this skill works? Can you give a concrete input + expected output?"*

Surfaces verification shape. Often reveals the skill's actual shape better than abstract description.

**Boundaries it must not cross**

> *"What files, systems, side effects, or state must this skill NOT touch? What's the blast-radius constraint?"*

Maps to the lane-discipline principle. Often surfaces explicit *"do not write to X"* rules.

**Failure modes that break production**

> *"What's the failure mode that would break a real use of this skill — wrong output silently passing validation, partial state on error, race condition, missed edge case?"*

Surfaces the catastrophic failure to defend against.

**Edge cases**

> *"What edge cases does this skill need to handle — empty input, null, race, retry, timeout, partial failure, data-shape drift?"*

Forces explicit edge-case enumeration.

### Hybrid-type follow-ups

When type is hybrid, draw from both pools situationally. Useful framing question:

> *"This skill has both creative-feeling and technical-feeling aspects. Which sections want more voice / variety / craft, and which want more precision / verifiability / invariants?"*

Then ask creative or technical follow-ups per section as warranted.

### Optional probe questions (use when the brief is still thin after the above)

- *"If I were going to write this skill myself, what's the one thing I'd most likely get wrong that you'd want to catch before drafting starts?"*
- *"What sibling skills (in your skill library or elsewhere) are closest to this one? What should this one have in common with them, and what should be different?"*
- *"Is this skill going to be referenced or invoked by other skills? Which?"*
- *"Is this a one-off operation or a recurring workflow? How often does this get used?"*
- *"What's a previous version of this skill (mental, written, in some other tool) that didn't work, and why?"*

## Anti-patterns (both scopes)

- **Don't ask all questions in one message.** Pace them. Let answers inform the next question.
- **Don't ask creative-type questions for a technical skill (or vice versa).** Settle type first.
- **Don't manufacture scope.** If the user wants something small, don't expand it. The interview surfaces their intent; it doesn't scope-creep.
- **Don't skip the source-material question.** The user often has more material than they remember to mention.
- **Don't ask questions whose answers are evident from prior input.** Read what's there first.

## Used by

- `microtool-from-job` mode — uses Scope A (microtool clarification) when the stated need is too thin to design from.
- `interview` mode — uses Scope B (full skill brief-building) as the primary surface, with type-lens-aware follow-ups.
- Other sub-modes — auto-invoke `interview` mode when input is insufficient; `interview` reads from this reference.

## Source provenance

The one-question-at-a-time pacing and draft-when-stuck pattern come from `os-content-interview` (formerly a mode of os-content-discovery) (which itself adapted from legacy *I interview you to find content ideas* and *Content-Finder Interview Bot 2.0* prompts).

The three-piece (input / output / transformation) framing of Scope A is preserved from the legacy *Inputs-to-Outputs Helper* prompt — that prompt's central thinking framework was that any tool is a transformation function and the user usually has the input but hasn't named the output. The full thinking framework lives at `os-knowledge/inputs-to-outputs-thinking.md`.

The five universal questions of Scope B and the type-lens-aware follow-ups are new in v2 — emerged from real-world experience drafting the Autowriter Fiction stack and observing that brief quality consistently bounded what either single-lane or dual-lane drafts could produce.

What's new in `os-skillify` overall: the design-readiness threshold ending the microtool interview when design begins; the full-brief scope as a top-level interview mode rather than only a sub-pattern; the type-lens parameter shaping which question pool fires.
