# Example Rules

Examples are the highest-leverage artifact for shaping future output — and the most dangerous for overfitting. Modern AI models can latch onto a single example and reproduce its quirks even when the skill's craft would suggest otherwise. A bad example can actively mis-train a skill; a missing example lets the skill work from first principles. The cost of a cringe example is higher than the cost of no example.

## Templates carry most of the teaching when they're written well

Before deciding whether a skill needs examples — or whether existing examples should be kept, replaced, or dropped — assess what the skill's template is already doing. Examples and templates do different work. The template carries the structural teaching: what fields exist, what each field is for, what shape the output takes overall. Examples carry cumulative-depth teaching: what a strong filled-in version of the whole shape feels like, what depth across every section looks like simultaneously.

When a template's placeholders genuinely describe the *effect* each field should produce, name depth markers, and cite the failure mode in shorthand, the template can carry most of the work that examples would have done. A well-written placeholder along the lines of `[a named feeling, not "satisfaction" or "fulfillment"]` does more depth-teaching than a list-item placeholder like `[feeling 1]` ever could — it names what good looks like *and* what bad looks like in the same breath. Strong templates are dense with this kind of effect-description.

When the template is mostly structural — bare section headers, generic field placeholders, no depth markers — the implicit "this is what good looks like" teaching has to come from somewhere. That's where examples carry the teaching. Dropping examples from a skill with a thin template strips out the depth-teaching with nothing to replace it.

The audit move, before any decision about examples: read the template through the skill-prompting-principles lens. Are the placeholders effect-described or just field-named? Do they signal depth (specific markers, contrast with failure modes)? Do the "rules" or "what this is not" sections do work beyond restating the structure? If the template is dense, fewer examples are needed. If the template is thin, strengthen the template first — that's usually more leverage than adding examples, because the strengthening flows through every future invocation, where examples only teach when the model happens to weight them. Examples are belt-and-suspenders when the template is already strong.

## Quantity guidelines

## Quantity guidelines

- **One example is the worst case.** A single example gets treated as the canonical shape; any stylistic quirk in it becomes mandatory-looking. Avoid single-example skills.
- **5–10 examples is the sweet spot for most skills.** Enough variety that the model generalizes the pattern rather than copying any specimen. Small enough that context remains focused.
- **More than 10 typically degrades helpfulness** — context gets bloated and the model spends attention on comparing examples rather than producing good output.
- For very compact examples (a single line, a short reply), the upper bound can flex higher. For long examples (multi-page outputs), 3–5 may be the practical ceiling.
- **Zero examples is acceptable — often preferable — when the template is doing strong work.** A skill with effect-described placeholders that signal depth, named failure modes, and a "grounding check" or "what this is not" section can ship without examples and still produce strong output. Missing examples is better than bad ones, and frequently better than mediocre ones when the template earns its keep.

## Quality criteria

Every retained example must exemplify a strong outcome. Screen each candidate against:

- **Not obviously AI-generated.** Examples that read as 2022–2023 AI output will teach the skill to reproduce that aesthetic. Tells: aphoristic contrast-clauses ("*approachable but polished*"), closing codas in descending line length, uncanny self-praise, default-model tics like "*it's not X, it's Y*", linkedin-sage cadence, pull-quote framing. Be assertive about removing or replacing these. Source-prompts from the GPT-3.5/early-GPT-4 era are likely to have AI-written examples.
- **Demonstrates the craft moves.** The example should make the skill's distinguishing moves visible. If an example doesn't show the moves the skill is supposed to produce, it's not an exemplar — it's just output that happens to exist.
- **Grounded in real content.** Human-written examples on real inputs are always preferable to synthetic examples. If a human example is weak but the skill is otherwise good, flag it for cleanup rather than keep the weak version.

## Decisions during conversion

When classifying an example chunk from a legacy prompt, each example gets one of four dispositions:

- **Keep as-is** — reads as current strong output, demonstrates the craft, grounded.
- **Keep with flag** — adequate but dated or imperfect. Rename with a `legacy-` or `dated-` prefix and schedule replacement. Note in the decision log.
- **Flag for cleanup** — human-written but weak. Schedule replacement once the editing skills are available to improve it. Keep in place until then only if it's better than nothing.
- **Drop and defer** — reads as AI-generated with era-specific tells. Delete the file. Plan fresh examples from real test runs once the skill is validated. Note the deletion in the decision log.

The default for AI-generated single-example legacy sources is **drop and defer**. The cost of a cringe canonical example is higher than the cost of a missing one.

## Sourcing fresh examples

Fresh examples come from:

- Running the converted skill against real input (the author's own writing, client samples, inputs the original prompt was designed for)
- Extracting good outputs the skill produces in early sessions, once the skill is stable
- Hand-written exemplars the author creates to anchor the skill

When fresh examples are generated, capture them in `examples/canonical-<short-desc>.md` with a one-line note about the input that produced them. Aim for 5–10 examples over time, spanning different inputs so the skill generalizes rather than copies.

## A useful sanity check

If you can't easily generate a strong example on real input after the skill is built, the skill may have a gap — the craft moves aren't specific enough, the references are thin, or the output shape isn't serving the job. The inability to produce exemplars is a signal, not a failure of the test.
