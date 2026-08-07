---
name: os-offer
version: 0.1.0
description: >-
  Design, improve, and differentiate offers — brainstorm, full offer vehicles,
  unique mechanism / Todd Brown 75-25 campaign architecture, strategic critique.
  Produces portable offer artifacts consumed by drafting, content-discovery, and
  launch work. Four modes: `offer-brainstorm`, `offer-vehicle`,
  `unique-mechanism`, `offer-improve`. Triggers on "generate offer ideas,"
  "build out an offer," "develop a unique mechanism," "critique my offer,"
  "design a full offer end-to-end," "Hormozi-style brainstorm," "name this
  mechanism." Do NOT trigger for audience research (use `audience`), positioning
  (use `os-biz-strategy/positioning`), or copywriting (use `writing`).
display_name: Offer Design
tagline: 'Design, differentiate, and stress-test offers.'
category: Offers
packs:
  - creator-pack
icon: 'phosphor:Gift'
when_to_use: >-
  Reach for this any time the question is *what are we selling and why is it
  different*. Pick by where you are:


  - `offer-brainstorm` — wide ideation across vehicles, hooks, and positioning
  angles.

  - `offer-vehicle` — full vehicle spec with movement mechanics, clear
  container, milestones, and differentiated positioning.

  - `unique-mechanism` — Todd Brown 75/25 campaign architecture and named
  mechanism.

  - `offer-improve` — strategic critique of an existing offer with profitability
  recommendations.


  Produces portable offer artifacts consumed by drafting, content-discovery, and
  launch work.
modes:
  - name: offer-brainstorm
    job: Wide ideation — breadth catalog or Hormozi-depth.
  - name: offer-vehicle
    job: 'Full vehicle spec — mechanics, container, milestones, positioning.'
  - name: unique-mechanism
    job: 'Mechanism excavation, naming, and Todd Brown 75/25 campaign build.'
  - name: offer-improve
    job: Strategic review with profitability recommendations.
---

# Offer — design, improve, and differentiate offers

## Purpose

Produce offer artifacts for a specific business: offer idea catalogs, full offer vehicle specs, unique mechanisms with campaign architectures, and strategic profitability reviews. The skill covers four modes — each addresses a distinct offer job — and is trigger-routed so the user can invoke a specific lens or let the skill select.

Each mode produces a portable artifact consumed by downstream skills (content strategy, drafting, launch). The skill lives upstream of copywriting and launch — the deliverable is offer design and articulation, not finished sales copy.

## When to use

- The user is generating offer ideas for a new audience or product
- The user has an offer concept and needs to flesh it out into a full vehicle spec
- The user needs a proprietary Unique Mechanism + 75/25 campaign for a premium offer
- The user has an existing offer and wants a strategic review + profit recommendations
- Another skill (`os-biz-strategy`, `os-content-discovery`, `os-writing`) needs an offer spec as input

Do NOT use for:
- Audience research or psychographic profiling (use `../os-audience`)
- Positioning interviews or elevator-pitch work (use `../os-biz-strategy/modes/positioning`)
- Finished sales copy, landing pages, VSLs (use `../os-writing`)
- Content strategy / messaging architecture (use `../os-content-discovery` for surfacing angles; finished sequences live in `os-writing`)
- Idea-scoping or productization before an offer is defined

## Modes

Four modes, each defined in `modes/<mode>.md`. All modes share input expectations in `references/offer-input-context.md`.

### `modes/offer-brainstorm` — Generate offer options (breadth + depth patterns)

Two patterns in one mode:
- **Breadth:** 10-category catalog of ~40 named offer ideas (from Offer Brainstormer AI)
- **Depth:** Hormozi-style 3 offers fleshed out with Value Equation framing, obstacle-as-solution formula, 5 delivery vehicles, sub-offers, scarcity/urgency/guarantee

**Triggers:** *"brainstorm offers,"* *"give me offer ideas,"* *"Hormozi offer,"* *"what could I sell,"* *"100M offer."*

### `modes/offer-vehicle` — Full offer vehicle spec

Movement Mechanics (FROM / TO / PATH) + named Unique Mechanism + Clear Container (included/excluded/engagement) + Journey Milestones (A → B → C → D → E) + Differentiated Positioning. Optional compact Dream Outcome/Vehicle/Journey/Price variant.

**Triggers:** *"build my offer vehicle,"* *"flesh out my offer,"* *"design the full offer,"* *"offer spec,"* *"dream outcome."*

### `modes/unique-mechanism` — Todd Brown Dominant Differentiation

Excavate, formalize, and name a proprietary Unique Mechanism, then build the 75/25 campaign architecture (Education Phase + Offer Phase) with Three-Tier Evidence Stack. Full 11-step playbook by default, compressed naming-sprint variant (10 candidates / 3 types) on request.

**Triggers:** *"unique mechanism,"* *"Todd Brown,"* *"dominant differentiation,"* *"75/25 campaign,"* *"name my offer,"* *"blue vehicle,"* *"what makes my offer different."*

### `modes/offer-improve` — Strategic review + profit levers

6-section analysis (Offer Summary / Market Fit / Value + Differentiation / Profit Levers / Recommendations / Next Steps) ending with 3-5 prioritized specific recommendations grounded in buyer psychology, pricing theory, competitive advantage. Optional financial-benefits lens when ROI articulation is weak.

**Triggers:** *"improve my offer,"* *"review my offer,"* *"profit levers,"* *"offer critique,"* *"make my offer more profitable."*

## Cross-mode template

`templates/problem-promise-paragraph.md` — the 7-beat PPP format specialized for offer messaging. Used by `offer-vehicle` and `unique-mechanism` modes, also available as a standalone template when the user wants PPP directly.

## Integrated offer chain pattern

When a user wants the complete integrated offer design (what NTPV Designer accomplished in one shot — Niche + Transformation + Promise + Vehicle + Unique Method + 3 Pillars + Authority + Risk Reversal + PPP), don't build it as a mode — **chain separable skills**:

1. **`../os-audience/modes/avatar`** — profile the audience (Niche + emotional identity)
2. **`../os-audience/modes/limiting-beliefs`** — surface what's blocking the purchase (informs Enemy Takedown in `unique-mechanism`)
3. **`../os-biz-strategy/modes/market-map`** — read Sophistication / Awareness / Temperature (calibrates mechanism education depth via Promise-Exposure Spectrum)
4. **`../os-biz-strategy/modes/positioning`** — articulate the positioning blueprint (provides NTPV + USP + Value Articulation Story)
5. **`modes/offer-vehicle`** — spec the full offer vehicle (Movement Mechanics + Clear Container + Milestones + Differentiated Positioning)
6. **`modes/unique-mechanism`** — excavate and name the mechanism + build 75/25 campaign
7. **`templates/problem-promise-paragraph.md`** — draft the PPP for ad / landing-page use

This chain produces an integrated NTPV-style output by composing modes the user can also invoke independently.

## Routing logic

Trigger-routed with self-determination fallback:

1. **Clear trigger match** → run the matching mode.
2. **Ambiguous wording** → pick best-fit based on input content. If the user mentions *generating* / *ideating* / *multiple options* → lean `offer-brainstorm`. If they mention *structure* / *components* / *container* → lean `offer-vehicle`. If they mention *differentiation* / *mechanism* / *campaign* / *Todd Brown* → lean `unique-mechanism`. If they mention *critique* / *improve* / *review* / *profit* → lean `offer-improve`.
3. **"Design my complete offer"** → chain pattern (above) rather than a single mode.
4. **Multi-mode intent** — chain in reasonable order.

Before producing output, confirm the mode choice in the first line — *"Running offer-brainstorm (breadth) for [segment] + [offer context]..."*

## Cross-mode suggestions (output postamble)

Every mode's output ends with one to three pointers to the modes that naturally follow from where the user is now — what to map next, what to flesh out, what to critique, what to draft from this artifact. Pick the pointers that fit what the user appears to be working toward; don't enumerate every option. Phrase each as a short pointer at the next move with the mode name, not as a sales pitch for the adjacent mode.

This turns single-mode calls into a navigable surface — users who didn't know what else the skill can do get a path forward, users who already knew can ignore.

## Inputs

Shared across modes — see `references/offer-input-context.md`. Core inputs:
- **Required:** offer / business / offer concept
- **Strongly preferred:** avatar from `../os-audience/modes/avatar`; offer or service description
- **Optional:** performance metrics, competitive context, prior positioning

Mode-specific inputs (e.g., `unique-mechanism` needs the delivery process detail, and `offer-improve` needs enough existing offer detail to critique) are handled within each mode.

## References

Within-skill references loaded by multiple modes:

- **`references/unique-mechanism-playbook.md`** — Todd Brown's Dominant Differentiation full methodology (excavation, naming, 75/25 campaign, evidence stacking, promise-exposure spectrum, defensibility). Loaded primarily by `modes/unique-mechanism`.
- **`references/vehicle-theory.md`** — Brunson/Hormozi vehicle foundations (Service < Offer < Vehicle, A → B transportation, three mechanism types, Big Idea, perceived value, five vehicle components, program structuring). Loaded primarily by `modes/offer-vehicle` + `modes/offer-brainstorm`.
- **`references/offer-frameworks.md`** — Vehicle-vs-Method distinction, root-problem-vs-symptoms, high-ticket psychology ($3K+), 3-pillar vehicle structure, Hormozi's four offer-worthy-market criteria. Loaded across all four modes.
- **`references/offer-input-context.md`** — common input expectations across modes.
- **`references/offer-design-influences.md`** — named domain influences (Hormozi, Brunson, Todd Brown, Schwartz, Kennedy, et al.). Pointers to bodies of work, not personas to cosplay.

External loads from `_shared/`:

- **`../_shared/references/hormozi-value-equation.md`** — the four-lever Value Equation. Core reference for `offer-brainstorm` (depth) + `offer-vehicle` (pricing) + `offer-improve` (value articulation check).
- **`../_shared/references/positioning-concepts.md`** — USP / NTPV / Unlike Statement / Value Articulation Story. Loaded by `offer-vehicle` (Differentiated Positioning) + `unique-mechanism` (Enemy Takedown) + `templates/problem-promise-paragraph.md`.
- **`../_shared/references/schwartz-awareness-ladder.md`** — Promise-Exposure Spectrum calibrates to awareness stage. Used by `modes/unique-mechanism`.
- **`../_shared/references/creative-criteria.md`** — quality filter for offer idea brainstorming.

## Templates

Per-mode in `templates/`:
- `offer-brainstorm-output.md` — both breadth and depth shapes
- `offer-vehicle-output.md` — full 5-component spec + compact Dream Outcome/Vehicle/Journey/Price variant
- `unique-mechanism-output.md` — full 11-step shape + compressed naming-sprint variant
- `offer-improve-output.md` — 6-section strategic review + optional financial-benefits lens
- `problem-promise-paragraph.md` — cross-mode PPP template

## Examples

Four worked examples ship to illustrate the breadth and vehicle patterns:

- **`examples/solopreneur-coach-offers.md`** — `offer-brainstorm` breadth pattern (~40 named offers across 10 categories for solopreneur coaches)
- **`examples/fractional-cmo-offers.md`** — `offer-brainstorm` breadth pattern (~40 offers for a fractional-CMO avatar)
- **`examples/revenue-radar-workshop.md`** — `offer-vehicle` (Marketing Blueprint Workshop → Revenue Radar™ Accelerator System)
- **`examples/storyscale-authority.md`** — `offer-vehicle` (Story-Driven Marketing Initiative → StoryScale™ Authority System)

These illustrate the breadth pattern of `offer-brainstorm` and the vehicle pattern of `offer-vehicle`. Depth-pattern and `unique-mechanism` examples don't ship — the skill grows those from real runs per the discipline in `../_shared/references/example-rules.md` (either several strong examples or none, not a small set of weak ones).

## Self-extending behavior

The four modes cover the offer-design surfaces most operators routinely need — wide ideation, full vehicle spec, mechanism + campaign architecture, strategic critique. They don't cover every conceivable offer job. When the user asks for something the existing modes don't fit — a productization / idea-scoping pass before an offer exists, a value-clarity facilitation interview, a tiered-pricing architecture sprint, a guarantee-design workshop, an offer kind specific to their niche — the skill surfaces the gap explicitly and offers two paths rather than forcing the request through the closest existing mode.

The first path is *set up the new offer job as a mode for next time*. The user supplies one or more examples — an offer artifact they've built before in this shape, a published example whose structure they want to mirror, a rough sketch with notes — and the skill hands off to `os-tune`, which routes it — `extend` adds the mode to this skill, and a genuinely new shape goes to `os-skillify` instead. Either way the new mode file lands inside the skill; next time the user asks for that shape, it runs as a first-class mode.

The second path is *produce it once, no setup*. The skill picks the closest existing mode as a structural starting point and produces the artifact using the supplied source material. No new mode lands; the output is the only artifact.

The skill is greedy about extension when the signal points at recurring need — an offer shape the user builds for every new product, a critique lens specific to their consulting practice they expect to reuse. A one-off curiosity doesn't earn a saved mode. When the signal is ambiguous, the mode asks.

The why: offer-design work compounds. The shapes of artifact a strategist uses keep growing with their practice — and a skill frozen at four modes shrinks the strategist's ambitions to those four. The canonical principle and its application across the workspace lives in `../_shared/references/self-extending-skills.md`.

## First-time setup

Offer-design is a consumer skill — its value depends on what the user supplies as input. Before producing useful artifacts, the buyer needs at minimum an offer concept (or an existing offer to critique) and ideally a tight audience segment. The modes will ask for these inline when they're missing; first-time use is smoother when the buyer has the upstream artifacts already on hand.

Recommended setup-adjacent moves: install `os-audience` if you'll be designing offers for new audiences (the avatar and limiting-beliefs outputs feed directly into `offer-brainstorm`, `offer-vehicle`, and `unique-mechanism`'s Enemy Takedown step); install `os-biz-strategy` if you'll need market-mapping (sophistication / awareness / temperature) and positioning context that calibrates the Promise-Exposure Spectrum and the Differentiated Positioning section. None of these are hard requirements — the modes graceful-degrade on inline input — but the artifacts are sharper when the upstream context is in place.

## Where outputs go

Outputs persist per the workspace storage methodology — see `../_shared/references/workspace-layout.md` (Knowledge system invariants): when the work belongs to an ongoing project, save silently to the broadest existing home with dated frontmatter and a link trail; when the user is exploring, offer once. No skill-specific save scheme.

## Related skills

- **`os-audience`** — upstream producer. `modes/avatar` is the natural input for `offer-brainstorm` (who is this offer for?) and `offer-vehicle` (whose FROM state does this vehicle address?). `modes/limiting-beliefs` feeds into `unique-mechanism`'s Enemy Takedown step.
- **`os-biz-strategy`** — upstream / peer. `modes/market-map` informs Promise-Exposure Spectrum calibration in `unique-mechanism`. `modes/positioning` produces USP / NTPV / Unlike Statement content that `offer-vehicle` and `unique-mechanism` consume.
- **`os-voiceprint`** — produces the writing-style fingerprint downstream writing skills use alongside offer output.
- **`os-writing`** — primary downstream consumer for finished assets (VSL, landing page, email, longform) built from the offer vehicle + 75/25 campaign architecture.
- **`os-content-discovery`** — consumes PPP and unique-mechanism output when surfacing content angles around the offer.

## TBD rationale items

A few defaults in this skill come from source convention without an articulated rationale. They ship explicitly named rather than papered over, per the workspace's TBD-rationale discipline:

- **Why 75/25 ratio specifically, not 70/30 or 80/20** — Todd Brown states *"roughly three-quarters"*. Hyper-jaded markets may need 80%+. Default 75/25, adjusted per the Promise-Exposure Spectrum reading.
- **Why "1–6 words" for mechanism names** — preserved from the Blue Ocean naming tradition as a readability / memorability heuristic. The constraint holds; the rationale is inferred, not defended in source.
- **Why 10 categories in the breadth catalog, not 15 or 20** — source convention, likely "enough variety without overwhelm." Malleable per user request.
