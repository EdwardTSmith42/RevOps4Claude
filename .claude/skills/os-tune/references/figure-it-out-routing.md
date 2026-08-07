# Figure-it-out routing — how os-tune decides among refine / extend / generation handoff

os-tune's user-facing invocation is *"Figure it out."* The user says it (or an equivalent — *"this keeps coming up, handle it"* / *"make this a thing"*) along with their need. os-tune has to decide which mode handles the ask. This document describes the routing logic.

## The decision tree

Given a user ask, os-tune runs three checks in order:

1. **Is this feedback on a skill the user just ran?** → `refine`
2. **Does this map onto an existing skill as a new mode?** → `extend`
3. **Otherwise?** → hand off to `os-skillify` (generation)

The first match wins. The user can override at each gate.

## Check 1: Refine candidate

A `refine` candidate is recognized when:

- The user references a skill they recently ran (*"the email skill,"* *"the daily assist skill,"* *"that thing you just did"*)
- The ask describes feedback or output adjustment (*"this isn't quite right,"* *"next time also include…,"* *"fix the way it…"*)
- Recent context (current session, `os-inputs/_os-inbox.md`) shows a recent skill invocation matching the user's reference

If all three signals are present, os-tune proposes `refine` and surfaces the target skill for confirmation.

If the signals are mixed (recent invocation, but the ask is bigger than a tweak), os-tune surfaces the choice: *"This sounds like more than a tweak — should I extend the skill with a new mode, make a new skill, or refine the existing mode? Pick one."*

If the user says something like *"I keep doing X manually"* with no recent skill invocation matching, this isn't a refine candidate — fall through.

## Check 2: Extend candidate

An `extend` candidate is recognized when:

- The skills inventory scan returns a skill whose purpose is coherent with the user's ask
- The ask describes a behavior the existing skill could plausibly add as a mode
- The existing skill's modes don't already cover the ask

The scan uses the skills inventory loaded per `inheritance-protocol.md`. Match signals include:

- **Direct keyword overlap** between ask and skill description ("email" + "draft" matching `email` skill)
- **Domain overlap** (email, tracker, calendar, drafting, capture, etc.)
- **Job overlap** (the existing skill handles the same job category — generation, classification, summarization, routing)

If a strong match surfaces, os-tune proposes `extend` and names the target: *"This sounds like another mode of your email skill, not a new one. Extend it?"*

If multiple candidate skills match with similar strength, os-tune asks: *"This could fit your email skill or your inbox-routing skill. Which?"*

If no skill matches (or matches are weak), os-tune falls through to check 3.

### Strength thresholds

os-tune classifies match strength into three bands:

- **Strong** — direct keyword overlap + domain overlap + job overlap. os-tune proposes `extend` confidently.
- **Medium** — two of three signals. os-tune proposes `extend` but opens with *"this might be…"* rather than asserting.
- **Weak** — one signal or less. os-tune falls through to the generation handoff and notes the weak match in the audit trail (*"considered extending email skill — domain overlap only, decided new skill is cleaner"*).

The user always sees the routing decision and the alternative considered, so they can correct if the inference was wrong.

## Check 3: Generation handoff (default)

If checks 1 and 2 don't fire, the ask is generation-shaped and os-tune hands off to `os-skillify`, whose dispatcher routes on input shape (existing prompt vs long-form content vs stated need vs microtool) — see `skills/os-skillify/SKILL.md`. os-tune's job ends at the handoff; skillify's own gates take over.

Even when generation is the chosen route, the inheritance protocol still runs before the handoff. New skills inherit voice, conventions, and existing-skill awareness — the inventory scan that informed the routing decision also informs what the new skill's description and modes look like, so it doesn't accidentally re-cover ground.

## User overrides

The user can short-circuit routing at any point:

- *"Make a new skill"* → forces the os-skillify handoff, skips checks 1 and 2
- *"Extend my email skill"* → forces `extend` with a named target, skips checks 1 and 3
- *"Refine the daily skill"* → forces `refine` with a named target, skips checks 2 and 3
- *"What would you do?"* → asks os-tune to surface its routing decision before acting

When the user names the mode and target explicitly, os-tune honors the override and skips the checks. Graceful-degradation rule still applies: if the named target doesn't exist, surface the gap rather than silently approximating.

## Mid-ambiguity behavior

When the user's ask is genuinely ambiguous and os-tune can't tell which mode fits, the default is to ask — not to guess. A typical ambiguous prompt: *"This thing keeps happening — figure it out."*

os-tune responds with the candidates it considered, ranked by strength — typically two or three reads, each naming the route (refine / extend / generate), the target skill, the basis for the match, and the strength band — and asks the user to pick. The user picks; the audit trail records the choice and the rationale.

## Why three routes, not more

Other operations one could imagine (deprecate, merge, split) don't get their own routes by design — they're rare, and when `reflect` surfaces one, it routes to `os-skillify`'s `enhance` (audit / split / modernize) or `consolidate` (merge) sub-modes rather than growing new entry points here (per the workspace's *labels and abstractions denote future actions* rule).

## Routing audit trail

Every os-tune invocation records:

- The user's raw ask
- The candidates considered (with strength bands)
- The chosen route + target
- Any overrides the user supplied
- Whether the user confirmed or corrected the routing decision

Recorded in the session output (visible to user) and optionally in `os-inputs/_os-inbox.md` if the user wants the routing decision to be promotable to a durable pattern later.

## See also

- `inheritance-protocol.md` — what context loads before routing runs
- `../modes/extend.md`, `../modes/refine.md` — the local modes; `skills/os-skillify/SKILL.md` — the generation dispatcher check 3 hands off to
- `os-library/references/matching-discipline.md` — the matching convention this routing builds on
