# Biz Strategy — Input Context

Common inputs all modes in `biz-strategy` expect, plus per-mode specifics. When the user invokes a mode, the mode should have (or ask for) these inputs before producing output.

## Required input (all modes)

- **The offer or business.** What the product/service is, what it does, who it's for, what the core mechanism is, what it costs. Specific enough that a market reading can be grounded — not *"a coaching business"* but *"a $497 self-paced course that teaches solopreneur creators to run a voice-trained AI content engine in 2 hours per week."*

## Strongly preferred (mode-dependent)

### `market-map` specifically
- **The avatar / audience profile.** This mode is explicitly downstream of audience work. Ideally an avatar output from `os-audience/avatar` or an equivalent. Without an avatar, the market reading is cruder and the positioning recommendations thinner.
- **Some competitive context.** Who the main competitors are, what they claim, what the user has tried in terms of differentiation. Optional but sharpens counter-positioning.

### `blue-ocean` specifically
- **The entry point.** Which of the six entry points matches the user's actual question (Idea Ignition / Market Saturation Escape / Tool Activation / Customer Growth Hunt / GTM Friction Removal / Investor Readiness). If unclear from the input, ask.
- **What's been tried.** Prior strategic moves and their outcomes. Blue Ocean work needs to know what's already in the rearview.

### `models-method` specifically
- **The practitioner's context and goal.** Who they serve and what transformation they create for those people. Without this anchor, the mode has no material to extract genius from.
- **Their genius — what they know or do that most people in their industry don't.** Elicited during the interview; may not exist in input.
- **The business context.** Coach / consultant / course creator / agency — the method applies broadly but the implementation varies.

### `positioning` specifically
- **None beyond the opening question.** The mode is an interview — inputs come from the user's answers, not from pre-supplied context. The mode opens with the structured opening question and extracts from there.

## Optional input (all modes)

- **Prior positioning attempts.** Old taglines, elevator pitches, sales page language. Useful context — surfacing what didn't work is part of the modes' work.
- **Customer language.** Reviews, sales-call objections, community posts. Grounds the analysis in actual prospect voice.
- **Business model / pricing tier.** Informs Sophistication assessment and pricing recommendations.
- **Awareness stage estimate.** Where the prospect sits on Schwartz's ladder — useful across modes.
- **Competitive context.** Direct and adjacent competitors, their messaging, their pricing.

## How to ask for missing input

Ask for the one piece of information that blocks the output most severely. Don't batch-request a questionnaire.

The right shape: *name what you can produce, name the single missing piece, name why it matters for the output, ask for it specifically*. Often it helps to surface two or three concrete possibilities the user can react to rather than asking them to define the missing input from scratch.

The wrong shape: a long questionnaire requesting every input at once. That kind of request stalls the conversation and signals the mode doesn't know how to start.

## Grounding checks — applied by every mode

Before shipping output:

1. **Is every analytical field grounded in specific input?** Thin fields signal thin research — either ask for more context or flag the inference explicitly.
2. **Is the output traceable to the input?** If the user asks *"where did X come from?"*, the answer should point at specific input they provided.
3. **If input was inferred (not given), is that flagged?** When a mode guesses an attribute, the guess is marked as such so the user can correct.
4. **Does the output avoid generic filler?** *"Competitive market"* and *"strong positioning"* are both analytic placeholders, not output. Replace with specifics or remove.

## Cross-mode chaining

Modes chain naturally. The most common chain:

1. `os-audience/avatar` → produces avatar
2. `os-biz-strategy/market-map` → uses the avatar to read Sophistication / Awareness / Temperature
3. `os-biz-strategy/positioning` → turns the market reading into positioning language
4. `os-offer` → uses the positioning to refine or construct an offer

When the user invokes a downstream mode without upstream input, the mode should surface the gap and suggest running the upstream mode first.

## Used by

All `os-biz-strategy` modes.
