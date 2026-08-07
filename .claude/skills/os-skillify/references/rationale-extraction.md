# Rationale Extraction

This is the phase that makes converted skills trustworthy under edge cases. A template tells the agent *what* shape to produce. The rationale tells the agent *why* — which is what it needs when the user asks for a variation and the agent has to decide whether deviating breaks the thing.

Rationale is also the tacit craft hiding in the author's head. Much of what made the original prompts work has never been written down. The conversion is our chance to surface it.

## Goal of this phase

For every chunk tagged as a **craft move** or **judgment heuristic** in classification, produce a one-liner:

*"[move] works because [reason]."*

These one-liners become the "Design Rationale" section of the converted skill's SKILL.md. They stay short — not a history lesson, just enough that a future agent reading the skill can make judgment calls consistent with the author's intent.

## Where rationale comes from

Three sources, in order of preference:

1. **Stated in the source.** The original prompt sometimes includes rationale as an aside. Lift it verbatim. Example: *"Return the voiceprint in its own style. Yes, this is very meta, but we've found that the closer a voiceprint is to the style it is trying to emulate, the better."* — the second sentence is rationale. Capture it.
2. **Inferable from structure or context.** Sometimes rationale is implicit in how the prompt organizes steps or which constraints it emphasizes. Infer with care, but flag the inference in the decision log so the user can confirm.
3. **Only in the author's head.** Most important category, and the one that requires explicit elicitation. Ask.

## Eliciting tacit rationale

When the rationale isn't stated, ask the user directly. Don't batch too many at once — three to four questions per round, each focused on one move.

**Good question framing:**

- Specific to the move: "This prompt requires analysis to come before the final output. What does that ordering buy you?"
- Action-oriented: "Under what circumstances would you deviate from this rule?"
- Counterfactual: "If a future version of this skill dropped the 'ratings out of 10' and used 'low/medium/high' instead, what would be lost?"

**Avoid:**

- Vague questions ("Why is this here?") — produces vague rationale.
- Leading questions ("This is because of X, right?") — you'll get agreement even when wrong.
- Asking about every single line — only ask about the moves that genuinely shape the output.

## How much rationale to capture

Target: 3–8 rationale one-liners per skill. Enough to cover the non-obvious moves; not so much that the SKILL.md becomes a treatise.

If a skill needs more than 8 rationale notes, either (a) some of them are actually domain knowledge that belongs in a reference, or (b) the skill is doing too much and should be split.

## Format of the Design Rationale section

In the converted SKILL.md, the Design Rationale section looks like this:

```markdown
## Design Rationale

Why this skill is structured the way it is:

- **[Move or choice]** — [one-sentence reason]. [Optional second sentence on edge cases.]
- **[Move or choice]** — [one-sentence reason].
...
```

Keep each bullet to one or two sentences. The goal is enough clarity to act on, not comprehensive documentation. Longer explanations belong in references.

## Worked example: rationale notes from a voiceprint-generator prompt

A plausible pass through a voiceprint-style source surfaces a handful of consequential moves and their rationales — some stated, some elicited:

- A meta-instruction telling the model to return the voiceprint in the same style it's describing — *stated in source*, with the rationale already in the next sentence (the closer the rendering is to the style being emulated, the truer the voiceprint reads). Lift both.
- An invitation to add "one or two factors that aren't on the checklist" — *not stated*. Ask the author what this buys; a typical answer surfaces *prevents the output from going rote* as the rationale.
- A caution about scoring figurative language too high for everyday writing contexts — *stated in source*, lift.
- An ordering choice (analysis section before the voiceprint itself) — *not stated*. Ask why this order; a typical answer is *forces the model to do the linguistic work first so the voiceprint synthesizes rather than guesses*.
- A specific rating scale (out of 10, not low/med/high or out of 5) — *not stated*. Ask what the scale buys; a typical answer is *granularity without false precision, and inter-voiceprint comparability*.

Result: five rationale notes, each one line, covering the non-obvious moves.

## What not to capture as rationale

- Mechanics that are obvious once stated ("we output markdown because that's readable") — skip.
- Rationale for scaffolding we're dropping — dropped content doesn't need rationale, it needs a log entry.
- Domain knowledge dressed up as rationale ("we check for active voice because passive voice is weaker") — that's domain knowledge, belongs in the reference, not in Design Rationale.

## When the user can't articulate the rationale

Sometimes a move worked for reasons the author never explicitly understood. That's fine. Record it as: *"[Move] — empirically produces better output; specific mechanism unclear. Do not remove without testing."* This is honest documentation and signals future converters to treat the move as essential — don't remove it casually.
