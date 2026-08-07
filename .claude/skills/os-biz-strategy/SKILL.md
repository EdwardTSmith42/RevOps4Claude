---
name: os-biz-strategy
version: 0.1.0
description: >-
  Analyze a market, differentiate a positioning, and build visual frameworks
  that shape how a market perceives an offer. Four modes — market-map (Schwartz
  sophistication + awareness + Brunson temperature + competitive analysis),
  blue-ocean (Kim/Mauborgne value-innovation toolkit), models-method (Simon
  Bowen visual models), and positioning (structured interview → complete
  positioning blueprint). Produces portable strategic artifacts that downstream
  offer, content, and writing skills consume. Triggers when the user wants to
  map a market, analyze competitors, find uncontested space, build a visual
  differentiation model, develop an elevator pitch or USP, articulate
  positioning, or make a strategic decision about where to compete.
display_name: Business Strategy
tagline: 'Map markets, position offers, find uncontested space.'
category: Research
packs:
  - creator-pack
icon: 'phosphor:Compass'
when_to_use: >-
  Reach for this when you need to make a strategic call about *where to compete*
  or *how to differentiate*. Four modes, each from a different lineage:


  - `market-map` — Schwartz sophistication + awareness + Brunson temperature +
  competitive analysis.

  - `blue-ocean` — Kim & Mauborgne value-innovation toolkit.

  - `models-method` — Simon Bowen visual differentiation models.

  - `positioning` — structured interview that produces a complete blueprint.


  Produces portable artifacts that downstream offer, content, and drafting
  skills consume.
modes:
  - name: market-map
    job: Sophistication + awareness + temperature + competitive analysis.
  - name: blue-ocean
    job: Kim & Mauborgne value-innovation toolkit.
  - name: models-method
    job: Simon Bowen visual differentiation models.
  - name: positioning
    job: structured interview → complete positioning blueprint.
---

# Biz Strategy — market analysis, differentiation, and positioning blueprints

## Purpose

Produce strategic market artifacts for a specific offer or business: market readings, competitive positioning, visual differentiation frameworks, and positioning blueprints. The skill covers four modes — each zooms on a different angle of the strategic landscape — and is trigger-routed so the user can invoke a specific lens or let the skill select.

Each mode produces a portable artifact consumed by downstream skills (offer design, content strategy, drafting). The skill lives upstream of copy and offer construction — the deliverable is strategy and articulation, not finished copy.

## When to use

- The user has an offer and wants to understand where it fits in the market
- The user is repositioning, pivoting, or fighting market saturation
- Another skill (landing-page copy, VSL, launch messaging) needs positioning input
- The user wants a memorable visual framework for sales conversations or keynotes
- The user is building an elevator pitch, USP, or NTPV messaging blueprint

Do NOT use for:
- Audience research or psychographic avatar work (use `os-audience`)
- Offer construction or unique-mechanism design for an offer's internals (use `os-offer`)
- Finished copy drafting (use `os-writing` and the content-domain skills)

## Modes

Four modes, each defined in `modes/<mode>.md`. All modes share the input expectations in `references/market-input-context.md`.

### `modes/market-map` — Market Sophistication + Awareness + Temperature + Competitive Analysis

Produces a market reading across Schwartz's 5 stages of sophistication, the 5 stages of awareness, Brunson's hot/warm/cold temperature, plus a competitive analysis with counter-positioning recommendations and a final positioning hook.

**Triggers:** *"map my market,"* *"market mapping,"* *"sophistication and awareness analysis,"* *"competitive positioning analysis,"* *"how do I position against competitors,"* *"where does my offer fit in the market."*

### `modes/blue-ocean` — Kim/Mauborgne Value-Innovation Toolkit (modular)

Applies Blue Ocean Strategy frameworks (Strategy Canvas, ERRC Grid, Six Paths, Three Tiers of Noncustomers, Buyer Utility Map, Adoption Hurdles, Strategic Overlays). Entry-point-driven — the user picks from six entry points or the skill selects based on their question.

**Triggers:** *"blue ocean,"* *"value innovation,"* *"uncontested market space,"* *"escape red ocean,"* *"ERRC,"* *"strategy canvas,"* *"six paths,"* *"who else could buy this,"* *"investor-ready strategy."*

### `modes/models-method` — Simon Bowen Visual Models (Genius / Conversion / Clarity)

Interactive 9-step extraction and model-building. Helps the user develop a Genius Model, Conversion Model, or Clarity Model — 3-4 pillars, geometric visual container, core belief shift, explainer script.

**Triggers:** *"build my Genius Model,"* *"visual model for my business,"* *"Simon Bowen,"* *"models method,"* *"visual framework,"* *"signature model."*

### `modes/positioning` — 12-Question Interview → Complete Positioning Blueprint

Conducts a structured interview drawn from a menu of question shapes (one question at a time) and generates a full positioning blueprint in the user's voice — Elevator Pitch, Value Breakdown, USP Snapshot, NTPV Messaging Blueprint, Value Articulation Story (7-beat format), Top 5 Objections.

**Triggers:** *"help me find my positioning,"* *"positioning blueprint,"* *"clarify my positioning,"* *"elevator pitch,"* *"USP,"* *"NTPV,"* *"what should I say about my business."*

## Routing logic

Trigger-routed with a self-determination fallback, matching the pattern from `audience`:

1. **Clear trigger match** → run the matching mode.
2. **Ambiguous wording** → pick the single most-fitting mode based on what the user described. If they mention *competitors* or *market landscape*, lean toward `market-map`. If they mention *value innovation* or *uncontested space*, `blue-ocean`. If they mention *visual frameworks* or *diagrams prospects remember*, `models-method`. If they mention *USP, elevator pitch, NTPV, or articulating positioning*, `positioning`.
3. **Broad request** (e.g., *"help me figure out my market strategy"*) → pick the most-fitting starting mode based on what the user actually described, then suggest complementary modes.
4. **Multi-mode intent** — chain in reasonable order. Common chain: `market-map` → `positioning` (market reading informs positioning language) or `positioning` → `models-method` (positioning informs the visual framework).

Before producing output, confirm the mode choice implicitly in the first line — e.g., *"Running market-map for the $497 AI Content System offer..."* — so the user can catch a wrong route.

## Cross-mode suggestions (output postamble)

Every mode's output ends with a brief cross-mode suggestion block — one to three complementary modes, one line each. Name the next likely strategic move and the adjacent mode that produces it; describe the *effect* the adjacent work would have on the current artifact rather than reciting a fixed sentence. Pick the one or two suggestions that genuinely fit what just shipped — not the full catalog.

When a mode produces a *pasteable strategic artifact* (an Elevator Pitch, a USP paragraph, a positioning hook, an NTPV blueprint, a Model name + Core Logic), the cross-mode suggestions live in a separate trailing block — never inside or stitched onto the pasteable artifact itself, where they would contaminate downstream copy/paste.

## Inputs

All modes share common input expectations — see `references/market-input-context.md`. In short:
- **Required:** A specific offer / business
- **Strongly preferred:** An audience segment or avatar (ideally from `os-audience`)
- **Optional:** Competitive context, prior positioning, awareness stage estimate

Mode-specific inputs (e.g., entry point selection for `blue-ocean`, who-do-you-serve for `models-method`) are handled within each mode.

## First-time setup

This skill graceful-degrades when run cold, but the analytical depth improves substantially when an avatar is already in the library. Recommended install order if you're starting fresh in the strategy lane: install `os-audience` first, run its `avatar` mode for the offer you want to position, then run `os-biz-strategy/market-map` or `positioning` with that avatar as input. Skip the avatar step if you're working from a domain you already understand deeply or testing a quick positioning angle — the modes will ask for what they need.

(This note can be deleted from your local copy of the skill once your library has at least one avatar in it and you've used the skill enough times that the routing is muscle memory.)

## References

Shared across modes:

- `references/market-frameworks.md` — Schwartz sophistication + Brunson temperature + Kim/Mauborgne toolkit + Strategic Overlays. Loaded by `market-map` (primary) + `blue-ocean` (primary). Schwartz/Brunson awareness ladder is loaded from `_shared/references/schwartz-awareness-ladder.md`.
- `references/models-method.md` — Simon Bowen's Models Method full playbook (prose reference). Loaded by `models-method`.
- `references/positioning-concepts.md` — pointer to `_shared/references/positioning-concepts.md` (USP, NTPV, Unlike Statement, Elevator Pitch, Value Articulation Story, Zone of Genius, Silent observation). Loaded by `positioning` (primary) + occasionally by other modes.
- `references/market-input-context.md` — common input expectations.
- `references/biz-strategy-influences.md` — named domain experts (Schwartz, Kennedy, Brunson, Hormozi, Kim/Mauborgne, Bowen, Miller, others). Kept as context pointers, not personas.

## Templates

Per-mode in `templates/`:
- `market-map-output.md` — 4 analytical sections + recommendations + positioning hook
- `blue-ocean-output.md` — catalog of canonical artifact shapes (Strategy Canvas, ERRC Grid, Six Paths, Noncustomer Tiers, Adoption Hurdles, Strategic Overlays, entry-point menu)
- `models-method-output.md` — model deliverable (type, shape, pillars, core logic, explainer script)
- `positioning-output.md` — 6-section positioning blueprint

## Examples

Seeded with one legacy example used as a shape demonstration for `market-map`. Other modes are unseeded — fresh examples accumulate from real runs per `_shared/references/example-rules.md`. The templates carry the structural teaching; examples are belt-and-suspenders for the cumulative-depth view.

## Where outputs go

Outputs persist per the workspace storage methodology — see `../_shared/references/workspace-layout.md` (Knowledge system invariants): when the work belongs to an ongoing project, save silently to the broadest existing home with dated frontmatter and a link trail; when the user is exploring, offer once. No skill-specific save scheme.

## Related skills

- `os-audience` — upstream producer. `market-map` and `positioning` both benefit substantially from a prior avatar.
- `os-voiceprint` — provides writing-style fingerprint, often paired with biz-strategy output when downstream writing skills need to match voice to positioning.
- `os-offer` — consumes biz-strategy output (unique mechanism recommendations from `market-map`, differentiation insights from `blue-ocean`) to construct offers.
- `os-writing` and content-domain skills — primary consumers of positioning blueprints and market-map positioning hooks.

## Extending this skill

The strategy domain keeps producing new lenses worth treating as modes — a new pricing framework, a different positioning interview, a fresh visual-model tradition. When you find yourself wanting a strategic angle this skill doesn't cover, surface the gap explicitly rather than forcing the request into one of the four existing modes. Two paths from there: (a) produce it once with the closest existing mode as a structural starting point, gaps named; or (b) set it up for next time — hand off to `os-tune`'s `extend` with an example or two, so the lens lands as a first-class mode. A recurring lens earns a saved mode; a one-off doesn't. The four-mode set is a starting point, not a closed inventory. Full principle: `../_shared/references/self-extending-skills.md`.
