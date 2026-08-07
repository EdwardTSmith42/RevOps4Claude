# Self-extending skills — when a skill should grow in response to use

Some skills serve a domain where the user's needs keep producing new shapes the original author didn't anticipate. A writing skill that ships with five mode types meets users who write a sixth; an editing skill with four lenses meets users who want a fifth; a voiceprint skill with one capture method meets users whose voice doesn't fit cleanly. For these skills, the buyer's experience improves when the skill itself is *greedy about extension* — when asked to do something it doesn't yet support, it surfaces the gap explicitly and offers to set up the new capability based on examples the user supplies, rather than declining the request or forcing it through the wrong existing capability.

This reference is the canonical doc for that disposition. It exists because the lesson otherwise scatters across the skill bodies that embody it, the audit lens that checks for it, and the meta-skills that build new skills without baking it in. One source of truth keeps all three aligned.

## The additive-vs-complete distinction

Not every skill needs this disposition. The first question is which kind of skill you're looking at.

**Additive skills** gain value from accumulating capability over time. The original mode / lens / scope list is a starting point, not an enclosure. Writing is additive — every new format the user produces could become a new mode. Editing is additive — every new edit-lens the user wants applied could become a new lens. Voiceprint capture is additive — every new author or scope is a new entry. Audience analysis is additive — every new audience type fills out the library. Skills like these become *more theirs* the longer the user works with them.

**Complete skills** do one well-defined job, done once well. The capability list is enumerated, not open. A deployment skill ships files to known surfaces. A tracker skill manages a backlog. An auto-save skill keeps restore points. Adding "more capability" to a complete skill is feature creep, not extension — the skill is already what it's supposed to be. These skills don't need self-extension language and would be over-engineered if it were added.

When in doubt, ask whether the skill is the kind that *accumulates* (its value compounds with use because the user's library / mode list / coverage keeps growing) or the kind that *performs* (its value is the same on day 1 as on day 100 because the job is stable). Accumulating skills get this lens. Performing skills don't.

A few skills sit on the edge — content discovery, business strategy, offer design — where the answer depends on whether the user's domain keeps producing new analytical shapes (additive) or whether the existing modes cover the analytical space (complete). When the edge case shows up, the question to ask the user is whether they expect their needs in this domain to grow over time or stay roughly the same shape. Their answer settles it.

## The three-beat pattern (for additive skills)

When an additive skill meets a request it doesn't currently support, the response has three beats — surface, offer, hand off.

**Surface the gap clearly.** The skill doesn't currently have this format / lens / scope. Naming that openly is better than approximating. A skill that quietly forces a request through the closest existing capability produces a wrong-shape output the user will recognize as off; a skill that names the gap explicitly preserves the user's trust and earns the right to suggest a path forward.

**Offer two paths.** First path: set the new capability up for next time. The user supplies one or more examples — a sample they've done before, a sample from another source whose shape they want to mirror, a rough sketch with notes — and the skill hands off to the appropriate skill-creation or library-save flow to make the new capability first-class. Second path: run once without setup. The skill uses the closest existing capability as a starting point and the supplied source as substance; no artifact gets saved; the output is the only result. The user picks based on whether the need is recurring or a one-off.

**Hand off cleanly when setup is chosen.** The skill isn't trying to do skill-creation itself — that's `os-skillify`'s job — and it isn't trying to be the library — that's `os-library`. When the user picks the setup path, the skill hands the examples and framing to the appropriate flow and gets out of the way. Knowing when to invite another skill is the craft; trying to do everything is the failure mode.

## The greedy-when-recurring discipline

The disposition is greedy when the signal points at recurring need. A request that mentions weekly use, an ongoing publication context, a format the user's work routinely calls for, an editing lens they want for every piece — these signal that setting up the new capability now is an investment in every future request. The skill should offer the setup path eagerly.

The disposition is restrained when the signal is a one-off. A request framed as "just this one time" or "I'm curious what would happen" doesn't earn a saved capability. The skill produces it once and moves on; a saved one-off becomes clutter in the user's skill or library.

When the signal is ambiguous, the skill asks. The cost of the question is low. The cost of saving capability the user didn't want, or failing to save capability the user wanted, is higher.

## The why behind the why

A skill frozen at its initial capability list quietly shrinks the user's ambitions to what the skill already supports. The user stops asking for the things the skill won't do — not because they don't need them, but because they've learned the skill says no. Over months, the user's actual range of work gets compressed into the skill's original scope, and the skill becomes a ceiling.

A skill that extends in response to use does the opposite — it grows alongside the user's practice. The user asks for something new, the skill adds the capability, the next user-ask reaches further. The skill becomes more *theirs* over time. That's what makes the skill an investment rather than a tool, and it's the difference between a buyer who renews and a buyer who stops opening the skill after a month.

This pattern is what justifies the workspace-shaped install (per `workspace-layout.md`) — the user's workspace is the source of truth for their capabilities, the skills they install are seeds, and the meta-skills (`os-skillify`, `os-tune`, `os-library`) are the machinery for growing those seeds into something shaped to the user's actual work.

## Before and after

**Before — frozen skill response to an unsupported format:**

User asks the writing skill for a VSL script. The skill produces a longform-article-shaped output (closest existing mode) and calls it a draft. The user notices it's the wrong shape and either rewrites it themselves or asks again with more specific instructions. The skill stays at five modes; the user does the adaptation work each time.

**After — self-extending response:**

User asks the writing skill for a VSL script. The skill names the gap — VSL isn't currently a mode — and offers two paths: set it up as a new mode using examples the user supplies, or produce one this time using the closest existing structure. The user mentions they produce VSLs monthly; the skill takes the recurring signal as license to extend, asks for one or two examples, hands off to `os-skillify` with the examples and framing, and produces the requested VSL while the new mode lands. Next month, the user asks for another VSL; the new mode runs as a first-class capability.

The structural difference is one round-trip and a hand-off. The experiential difference is whether the skill grows or stays frozen.

## Used by

- `audit-lens.md` (the os-skillify `enhance` audit lens) loads this reference as Lens 6 when auditing skills. The additive-vs-complete distinction tells the auditor whether the lens applies to the skill in front of them.
- `os-skillify` (SKILL.md + four sub-modes) loads this reference during the build phase. When the skill being created is additive, the produced skill includes a self-extending section pointing at this reference; when complete, the section is omitted.
- `os-tune` loads this reference in three modes. `extend` consults it when designing a new mode (the new mode may itself need self-extension awareness, and adding a mode is a moment to ask whether the host skill should gain the disposition if it doesn't have it). `refine` consults it because a tweak request framed as "the skill should handle X too" is literally a self-extension trigger that should be offered the cleaner path. `reflect` uses it as a pattern-detection lens — a heavily-used additive skill missing self-extending behavior is a refine candidate.
- `inheritance-protocol.md` (in `os-tune/references/`) lists this as one of the canonical sources loaded by meta-skill operations.
- `os-writing` and similar additive skills reference this doc explicitly so readers encountering the self-extending section in those skills can find the principle behind it.

## Malleability note

Canonical: the additive-vs-complete distinction, the three-beat pattern, and the greedy-when-recurring discipline. These are the core concepts; skills that diverge from them confuse the user about which path they're being offered.

Adaptable: how the three-beat pattern actually surfaces in a given skill. A writing skill's "surface the gap" may use the language of formats and modes; an editing skill's may use lenses; a voiceprint skill's may use scope names. The shape of the offer-two-paths beat may vary too — the "set up for next time" path could hand off to skillify (for a new mode) or to os-library/save (for a new template, brief, or style sample). What matters is that both paths exist explicitly and the hand-off is clean, not the exact phrasing or destination.

Skills that genuinely don't fit the additive category — a skill that performs one stable job once well — should not have this lens forced on them. The malleability includes the freedom to *not apply* the pattern when the skill is complete.

## Source

Surfaced as a workspace principle on 2026-05-24 during the os-writing audit. The user noticed that os-writing — and several other os-* skills — would benefit from being greedy about extension when meeting requests outside their current capability list. Promoted from the inline os-writing section and the inline audit-lens Lens 6 to this shared reference because the lesson applies to every additive skill the workspace ships, every additive skill `os-skillify` builds, and every additive skill `os-tune` extends or refines. Single source of truth keeps the skill bodies, the audit, and the meta-skills aligned.
