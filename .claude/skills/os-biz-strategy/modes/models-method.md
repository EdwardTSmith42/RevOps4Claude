# Mode: models-method

## Purpose

Help a user develop a unique visual model — a Genius Model, Conversion Model, or Clarity Model — based on Simon Bowen's Models Method. The mode is an interactive extraction: guide the user through clarifying their value, uncovering their thinking patterns, and distilling those into a visual structure. The final deliverable is a usable model (3–4 pillars with core logic) plus an explainer script and use suggestions.

## Triggers

Phrases like: *"build my Genius Model,"* *"create a visual model for my business,"* *"Simon Bowen method,"* *"models method,"* *"help me build a visual framework,"* *"my signature model,"* *"Genius / Conversion / Clarity model,"* *"model for my sales conversation,"* *"visual differentiation."*

## Inputs

See `references/market-input-context.md`. This mode specifically needs:

- **Required:** Who the user serves (context) and what transformation they help clients create (goal). These two pieces anchor the whole model.
- **Strongly preferred:** Some surface of the user's *genius* — what they know or do differently from most in their industry. May need to be elicited during the run.
- **Optional:** Prior model attempts, industry they operate in, strategic outcome they want the model to produce (sales conversation support, keynote, homepage, etc.)

If context and goal are not supplied, open with a single question that invites the user to name *who they serve* and *what transformation they create for them* in one breath. The exact phrasing is the user's to discover — what matters is that the opener anchors both context and outcome before any extraction work begins.

## Run

Nine-step interactive process. Preserve source wording where marked. See `references/models-method.md` for the full domain reference.

**Step 1 — Clarify context and goal.** Ask one question that surfaces *who they serve* and *what transformation they create* together. Get a tight answer, then mirror back what you heard so the user can correct framing before you build on top of it.

**Step 2 — Identify their genius.** Ask a question that invites the user to name what they know or do that most peers in their industry don't — and probably should. Listen for energy: when the user gets animated or unusually specific, that's the genius surface. Extract it in their language, not yours.

**Step 3 — Determine model type.** Based on where the user is stuck:
- Struggles to explain their offer clearly → **Genius Model**
- Struggles to get leads to convert → **Conversion Model**
- Clients are confused about their own situation → **Clarity Model**

If unclear, ask. Don't force a type — a forced type produces a flat model.

**Step 4 — Surface core elements.** Ask the user to name the three or four essential parts of their approach, system, or philosophy — the essential components without which the work doesn't work. Help them name those in plain, sticky language. Three to four pillars max. More dilutes memorability.

**Step 5 — Choose a visual container.** Based on the model type and the relationship between pillars:
- **Genius Model** → often triangle, Venn diagram, or concentric circles
- **Conversion Model** → quadrant (Four Futures-style), arc, or before/after contrast
- **Clarity Model** → quadrant, spectrum, or diagnostic scorecard

The shape choice is semantic (triangle = all required, circle = cyclical, Venn = intersection is the value, 2×2 = comparison, line = continuum). Not decorative. See `references/models-method.md` on geometric principles.

**Step 6 — Draw the connection.** Ask what *story* the model tells — what belief or insight it installs in the viewer. This is the model's payload, the core logic. If there isn't a clear belief shift, the model isn't done yet. Go back.

**Step 7 — Make it visual + verbal.** Help the user articulate:
- A name for the model (2–4 words, credible, memorable, no over-the-top modifiers)
- Names for each section or pillar (plain language, distinct, necessary)
- A simple explainer-script skeleton — an opener that introduces the model in terms of the transformation it produces, followed by one short beat per pillar. The skeleton is the user's to expand in real conversation; don't draft polished prose for them.

**Step 8 — Confirm transformation.** Ask what someone *now believes or feels* after seeing the model that they didn't before. This is the belief-shift test. If the user can't articulate it, the Core Logic isn't sharp enough.

**Step 9 — Refine and apply.** Help the user brainstorm:
- Where they'll use this model (sales calls, homepage, talks, keynote)
- How they can sketch or animate it
- How it fits into their existing messaging system

**Constraints throughout the run:**

- Don't overload the model with too many concepts — **3–4 pillars max**
- **Avoid buzzwords or vagueness** — insist on language that makes sense to outsiders. 7th-grade readability target. Source explicitly requires this.
- **Don't move forward with visuals until the core logic is sound.** A beautifully-drawn bad model is worse than a rough sketch of a good one.
- **Don't try to force a model type** — listen for what the message needs.
- **Avoid drawing for them.** Guide them to sketch it and verbalize it first. Ownership is part of the model's power.

See `templates/models-method-output.md` for the canonical output shape.

## Output

Per `templates/models-method-output.md`. Final output includes: Model Name, Type, Visual Container, 3–4 Pillars with plain-language descriptions, Core Logic (the belief shift), Explainer Script (skeleton the user will expand), optional ASCII sketch, Use Suggestions, and Refinement Prompts if the user wants to iterate.

After output, include a brief cross-mode suggestion block — separate from the artifact, so the model the user is about to draw doesn't end up containing a paragraph about which mode to run next. Pick the one or two adjacent moves that fit, and describe the effect. Common next moves: turning the model into a complete positioning blueprint (`positioning`), pressure-testing how it differentiates in the market (`blue-ocean`), or mapping where it lands on sophistication / awareness / temperature (`market-map`).

## Design Rationale

- **Models as mental maps, not content** — the goal is a framework prospects carry with them and use to evaluate future alternatives ("framework dependency"). Generic feature lists don't lodge this way.
- **Listen for the model the message needs** — don't force a type. Different user situations require different model types (Genius / Conversion / Clarity). A forced type produces a flat model that doesn't land.
- **3–4 pillars max** — cognitive-load constraint. More pillars dilute memorability.
- **Core logic before visuals** — don't move to shape or sketch until the underlying insight is sound. The visual serves the logic, not the other way around.
- **User sketches and verbalizes, not the mode** — the mode guides; the user owns the visual. Ownership matters — a model someone else drew is never as sticky as one you drew yourself. This also honors the Models Method's real-time-drawing principle.
- **Anti-jargon / 7th-grade readability** — the whole premise of the method is *visual + simple beats complex + text-heavy*. A jargon-laden output violates the method on its own terms.
- **Belief-shift test at step 8** — if the user can't articulate what someone now believes after seeing the model, the Core Logic isn't sharp enough. This is the mode's quality gate.
- **The 9-step sequence runs in order** — the ordering matters. Skipping steps (e.g., moving to shape before pillars are named) produces flat models that don't compose.

## References

- `references/models-method.md` — primary consumer, Simon Bowen's full playbook (philosophy, supporting models, geometric principles, implementation phases, psychology, Green/Red Zone positioning)
- `references/positioning-concepts.md` — when the model work surfaces positioning material (NTPV, Zone of Genius)
- `references/biz-strategy-influences.md` — Simon Bowen cited briefly
- `references/market-input-context.md` — input expectations

## Templates

- `templates/models-method-output.md`

## Examples

None seeded. The mode's output is heavily user-specific (their genius, their pillars, their visual) and the prose reference plus template carry the structural teaching. Fresh examples accumulate from real runs per `_shared/references/example-rules.md`.
