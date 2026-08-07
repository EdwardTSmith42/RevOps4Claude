---
name: os-audience
version: 0.1.0
description: >-
  Profile a target audience across multiple lenses — avatar/persona, limiting
  beliefs, empathy map, desires/motivators/obstacles, core transformation.
  Produces portable audience artifacts that downstream content, offer, and
  landing-page skills consume. Triggers when the user asks to profile an avatar
  or audience, build a customer persona, map limiting beliefs, identify
  objections, build an empathy map, analyze desires/motivators/obstacles,
  articulate the transformation an offer produces, or understand buyer
  psychology. Each mode zooms on a different facet. The skill routes based on
  the user's wording and suggests complementary modes in its output.
display_name: Audience
tagline: 'Profile who you''re for, across five lenses.'
category: Research
packs:
  - creator-pack
icon: 'phosphor:UsersThree'
when_to_use: >-
  Reach for this when you want to *understand* an audience before you write for
  them. Each mode zooms on a different facet — pick by what you're missing.


  Produces portable artifacts that downstream skills (drafting, offer,
  content-discovery) consume. Most operators run `avatar` first to anchor the
  persona, then `limiting-beliefs` to know what's blocking the buy decision,
  then `core-transformation` to articulate the before/after.
modes:
  - name: avatar
    job: Build a complete avatar / persona profile.
  - name: limiting-beliefs
    job: Map the beliefs blocking the buy decision.
  - name: empathy-map
    job: Sees / hears / thinks-feels / says-does framework.
  - name: dmo
    job: Desires / motivators / obstacles synthesis.
  - name: core-transformation
    job: Articulate the before-and-after the offer produces.
---

# Audience — profile target buyers across avatar, beliefs, empathy, desires, transformation

## Purpose

Produce psychographic audience artifacts that feed downstream marketing, offer, and content work. The skill covers five modes, each zooming on a different lens — persona, belief, empathy, motivation, transformation — and is trigger-routed so the user can invoke a specific lens or let the skill select.

Each mode produces a portable artifact consumed by other skills (content drafting, landing-page copy, VSL writing, offer design). The skill lives upstream of drafting work — the deliverable is research and articulation, not finished copy.

## When to use

- The user wants to understand a specific audience segment at a psychographic level
- Another skill (drafting, offer design, landing page) needs audience input
- The user is building a new offer, launching a campaign, or repositioning — moments where fresh audience work pays off
- The user has existing research (reviews, sales calls, customer language) and wants it synthesized into usable artifacts

Do NOT use for:
- Finished copy drafting (this produces inputs, not drafts — use os-writing for the drafts themselves)
- Content strategy / ad strategy / messaging architecture (different jobs — those produce campaign structures, not audience artifacts)
- Broad demographic market research without a specific offer or segment in view

## Modes

Five modes, each defined in its own file. All modes share the input expectations in `references/audience-input-context.md`.

### `modes/avatar` — Psychographic persona profile
Produces a named, vivid avatar with current-vs-desired state, silent struggles, dream outcomes, three-layer fears, market context, values in tension. The anchor mode — other modes often ground against a prior avatar output.
**Triggers:** *"profile my avatar"*, *"build a customer persona"*, *"who's my ideal customer"*, *"give me a psychographic profile"*, *"analyze my audience segment"*.

### `modes/limiting-beliefs` — Four-category belief map
Produces NLP deconstruction + 10 direct-response sales bullets + four belief-category tables (Big Domino / Vehicle / Internal / External) with counter-frameworks that dislodge each belief. Feeds VSLs, landing pages, webinars, email launches, lead magnets.
**Triggers:** *"map limiting beliefs"*, *"what's blocking my customer from buying"*, *"identify objections"*, *"dismantle buyer psychology"*, *"build belief-shifting content"*.

### `modes/empathy-map` — Moment-bound 8-field empathy map
Produces a classic empathy map (Thinks/Feels/Says/Does/Sees/Hears/Pains/Goals) for a specific audience-moment. Compact, narrower than avatar.
**Triggers:** *"build an empathy map"*, *"what does my customer think and feel"*, *"empathy map for X audience"*.

### `modes/dmo` — Desires, Motivators, Obstacles (with temporal framing)
Produces a four-section motivational analysis with obstacles split across Before / During / After the offer. Distinguishing move: the temporal framing surfaces post-purchase risks flat analyses miss.
**Triggers:** *"identify desires, motivators, and obstacles"*, *"DMO analysis"*, *"what drives and blocks my customer"*, *"what obstacles will my customer hit"*.

### `modes/core-transformation` — FROM/TO transformation articulation
Produces a FROM/TO statement plus non-obvious insights, expert principles, and potential challenges. Makes the offer's transformation nameable and sharable.
**Triggers:** *"what transformation does my offer produce"*, *"articulate my transformation"*, *"find my core transformation"*, *"what does my audience transform into"*.

## Routing logic

The skill is trigger-routed with a self-determination fallback:

1. **Clear trigger match** → run the matching mode.
2. **Ambiguous wording** → pick the single most-fitting mode based on what the user described. If the user mentions an *offer* or *what my business does*, lean toward `core-transformation` or `avatar`. If they mention *objections* or *what's blocking people*, lean toward `limiting-beliefs`. If they describe a specific *moment* or *scene*, lean toward `empathy-map`. If they emphasize *motivations* or *obstacles*, lean toward `dmo`.
3. **Broad request (e.g., "understand my audience comprehensively")** → default to `avatar` as the anchor mode, then surface cross-mode suggestions pointing at the other lenses.
4. **Multi-mode intent (user asks for multiple lenses)** → chain modes in reasonable order. A common chain for new-offer analysis: `avatar` → `core-transformation` → `limiting-beliefs`.

Before producing output, confirm the mode choice implicitly in the first line of the response — e.g., *"Running avatar mode on [segment]..."* — so the user can catch a wrong route before the full output arrives.

## Cross-mode suggestions (output postamble)

Every mode's output ends with a brief cross-mode suggestion block — one to three other modes that would complement what the user just got, named by what they'd reveal that the current mode didn't. One line per suggestion; no long explanation. The shape is a pointer in the user's direction of what they might want next, not a recital of every adjacent mode.

The suggestions are situational. After `avatar`, the natural next moves are usually `limiting-beliefs` (to surface what's blocking the buy decision) or `core-transformation` (to name the FROM/TO shift the offer produces) — pick the one that fits what the user appears to be working toward. After `limiting-beliefs`, the natural next move depends on whether the user has an avatar yet (run `avatar` to anchor) or is heading into drafting work (suggest the relevant os-writing or os-offer entry). The mode picks what fits and writes it once; it doesn't enumerate.

This turns single-mode calls into a navigable surface — users who didn't know what else the skill can do get a pointer, users who already knew can ignore.

## Inputs

All modes share common input expectations — see `references/audience-input-context.md`. In short:
- **Required:** A specific offer/business and a tight audience segment
- **Strongly preferred:** Existing customer language, prior avatar output (for modes other than avatar itself)
- **Optional:** Business model / pricing, competitive context, awareness stage

Modes that need mode-specific input (e.g., `empathy-map` needs a specific moment/context) ask for it if missing.

## When the requested lens isn't yet a mode

The five modes cover the audience-analysis surfaces most writing, offer, and content work actually need — persona, belief, empathy, motivation, transformation. They don't cover every conceivable lens. When the user asks for something the existing modes don't fit — a jobs-to-be-done analysis, a cohort comparison, a cultural-context profile, an internal-team segmentation, a kind of audience work specific to their domain — the skill surfaces the gap explicitly and offers two paths rather than forcing the request through the wrong existing mode.

The first path is *set up the new lens as a mode for next time*. The user supplies one or more examples — an analysis they've done before in this lens, a published example whose shape they want to mirror, a rough sketch of what the output should look like — and the skill hands off to `os-tune`, which routes it — `extend` adds the mode to this skill, and a genuinely new shape goes to `os-skillify` instead. Either way the new mode file lands inside the skill; next time the user asks for that lens, it runs as a first-class mode.

The second path is *produce it once, no setup*. The skill picks the closest existing mode as a structural starting point and produces the analysis using the supplied source material. No new mode lands; the output is the only artifact.

The skill is greedy about extension when the signal points at recurring need — a research method the user applies to every new audience, a lens specific to their practice they expect to reuse. A one-off curiosity doesn't earn a saved mode. When the signal is ambiguous, the mode asks. The same disposition applies to audience-input templates: when a request would benefit from a saved input scaffolding the library doesn't yet have, the skill offers to extract one via `os-library/save` after the analysis completes.

The why: audience work compounds. The shapes of analysis a writer uses keep growing with their practice — and a skill that stays frozen at five modes shrinks the writer's ambitions to those five. The canonical principle and its application across the workspace lives in `../_shared/references/self-extending-skills.md`.

## First-time setup

Audience analysis is a consumer skill — its value depends on what the user supplies as input. Before producing useful artifacts, the buyer needs at minimum a specific offer or business context and a tight audience segment. The modes will ask for these inline when they're missing; first-time use is smoother when the buyer has either an active brief in `os-inputs/briefs/current/` or rough notes ready to paste.

Recommended setup-adjacent moves: install `os-content-mining` if you have existing customer transcripts, reviews, or call recordings to process into audience inputs; populate `os-inputs/briefs/current/` with the offer brief you'll be analyzing against; have at least one body of customer language ready (interview transcripts, support tickets, sales calls, review excerpts). None of these are hard requirements — the modes work with rough inline input — but the analyses are sharper when the inputs are.

## References

Shared across modes:

- `references/buyer-psychology-beliefs.md` — four belief categories, belief-behind-the-belief, dislodge-vs-counter, reveal-and-restraint. Loaded by `limiting-beliefs` (primary), `avatar` (three-layer fears), `dmo` (psychological roadblocks), `core-transformation` (potential challenges).
- `references/psychographic-frameworks.md` — Schwartz's 5 Stages of Awareness, Hormozi's Value Equation, Behavior → Belief → Identity Driver. Loaded by multiple modes.
- `references/audience-input-context.md` — common input expectations across modes.
- `references/audience-insight-influences.md` — named domain experts kept as context pointers, not personas.
- `references/nlp-psychological-triggers.md` — 20-field NLP excavation. Currently used by `limiting-beliefs` only, skill-internal for now.

## Templates

Per-mode in `templates/`:
- `avatar-output.md`
- `limiting-beliefs-output.md`
- `empathy-map-output.md`
- `dmo-output.md`
- `core-transformation-output.md`

## Examples

The skill produces fresh examples from real input — no canonical examples ship with the skill. The example-selection rules at `../_shared/references/example-rules.md` recommend either five-to-ten strong examples or none rather than a small set of weak ones; the audience modes start at none and grow as the user's runs surface candidates worth saving.

## Where outputs go

Outputs persist per the workspace storage methodology — see `../_shared/references/workspace-layout.md` (Knowledge system invariants): when the work belongs to an ongoing project, save silently to `os-outputs/` with dated frontmatter and a link trail; when the user is exploring, offer once. No skill-specific save scheme.

## Related skills

- `os-voiceprint` — produces a writing-style fingerprint, often paired with audience output by downstream writing skills
- `os-writing` — primary consumer of audience output for hooks, emails, sequences, landing pages, articles
- `os-offer` — consumes core-transformation and dmo output to design offers against surfaced desires
- `os-content-mining` — processes raw customer language (transcripts, reviews, calls) into the kind of input audience modes work from
