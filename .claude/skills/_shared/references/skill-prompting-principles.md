# Skill prompting principles — how to write instructions a frontier model actually follows well

Modern models are competent skill-writers by default. They're also overfitted to certain patterns — bulleted everything, copy-pasteable example phrasings, rule-heavy specificity. Those patterns work fine for code, analytics, and structured data, and badly for prose, judgment, and craft. This reference exists so every skill made or modified inside this workspace dodges the default failure modes.

Six principles, in the order they matter when you're writing or editing a skill.

**This list grows.** New failure modes get named as they surface, so load this file rather than working from a remembered count — and when you reference it elsewhere, point at it rather than restating what's in it (principle 6).

## 1. Let the shape of the instructions mirror the intended output

The style, shape, and patterns in a prompt influence its output. A skill written as a wall of bullets teaches the model to produce bullets. A skill written in prose with a recognizable cadence teaches the model to produce prose with that cadence. The shape leaks.

This is fine — desirable, even — when the output really is structured: code, schemas, analytics summaries, tables, anything where the consumer is another machine or a developer scanning for fields. Lists belong there. Lists are the right shape.

But for skills whose output is for human consumption — writing of any kind, content, fiction, articles, marketing, business strategy, conversational replies, anything where voice and flow matter — bias the skill itself toward prose. Use the patterns, sentence rhythms, and tonal range you want the output to have. If the skill is supposed to produce warm, paced writing, the skill should read as warm, paced writing. If the skill is supposed to produce sharp, opinionated writing, the skill should read as sharp, opinionated writing. The model will pick up the shape whether you mean it to or not; choose the shape on purpose.

When in doubt, read the skill aloud and ask whether it sounds like the thing it's supposed to produce.

**Before:** A copy-editing skill written as fifteen nested bullets describing what to check.
**After:** The same skill written as three short paragraphs that *demonstrate* the kind of attentive, judgment-led editing the skill is supposed to produce.

### Sub-principle: when the output is pasteable, meta-information lives outside the paste

A specific application of shape-mirrors-output that matters whenever a mode's output is meant to be consumed as a single unit — pasted back into a draft, copied into another tool, handed forward to a downstream process. For those outputs, cross-mode suggestions, audit summaries, follow-up pointers, and other meta-information must live in the hub layer *surrounding* the delivery, not embedded inside it as a footer. The reason is concrete: a postamble inside pasteable output gets pasted with the output, contaminating the user's draft with the model's coordination talk.

The discipline names the failure mode honestly: a mode whose output discipline includes "no preamble" but ends with a postamble has only solved half the problem. The boundary between *the output the user pastes* and *the meta-information about the output* is a real boundary, and the mode's output template is responsible for honoring it. When in doubt, ask: if the user copies everything below the mode's first line, will the paste be clean? If no, the meta needs to move out of the delivery.

A mode that genuinely benefits from cross-mode pointers (most do) still gets to surface them — but in a separate message after the delivery is complete, or in a hub-layer wrap, or in the agent's reply text surrounding the tool output. The pointers exist; their location moves.

The principle applies broadly, not just to obviously-transformed-text outputs like a shortened paragraph or a rewritten draft. It applies wherever the output is meant to be reused as a unit: a positioning blueprint the user copies into a strategy doc, a scored verdict pasted into a review thread, a voiceprint slug-referenced by another skill, a hook dropped into the opener of an article, an offer paragraph handed to a copywriter. Any artifact the user will paste forward — strategic, structural, evaluative, or content-shaped — gets the same discipline: meta lives outside the paste.

## 2. Capture the why behind the why, not the rule

Models follow instructions almost too well. When a skill spells out a specific rule, the model can latch onto the rule and miss the lens behind it — applying it past its useful range, or failing to adapt when the situation is adjacent but not identical.

The fix is to write principles, not rules, wherever the underlying craft can be expressed as a mental model. State the *why*. Name what the move is protecting, what failure mode it's avoiding, what the operator was trying to preserve. A model holding the principle can handle the edge cases the rule didn't anticipate; a model holding only the rule cannot.

Hard-and-fast rules still have their place — frontmatter syntax, file paths, validator constraints, anything where there's literally one right answer and the cost of getting it wrong is breakage. Use rules there. But when the move is a craft move — a sequence, a phrasing pattern, a judgment heuristic — prefer the principle. The user's preference for a certain shape almost always has a *why* underneath it that's more durable than the surface preference. Capture that.

**Before:** "Always start the intake with three questions about goals, audience, and constraints."
**After:** "Open the intake by surfacing the dimensions you'll need to make later decisions confidently — typically what the user is trying to accomplish, who it's for, and what they can't change. Skip questions whose answers are already obvious from context."

The first version gets executed verbatim every time. The second version teaches the model to ask the right question for the situation in front of it.

## 3. Use placeholder-based examples, not verbatim sample text

Whatever you write as a literal example — a greeting, a hook, a question, a section heading, a stock phrase — has a strong chance of being reproduced verbatim, no matter how clearly you frame it as "just an example." This is the most common silent failure in skill design. The user reads the instruction as "here's the *kind* of thing"; the model reads it as "here's the thing."

The fix is to describe the *intent* of the example rather than supplying the text. Use a placeholder that names what the slot is supposed to do — what effect it's supposed to have, what role it plays — instead of filling it with a string the model can grab.

This applies in two places: instructions that tell the model what to say (greetings, prompts, opening lines, transitions, signoffs) and instructions that describe the shape of an output field (hook, headline, takeaway, summary). In both cases, the verbatim version is the trap.

**Before (instructions for what to say):** Open with a greeting like "What's been on your mind today?"
**After:** Open with an easy-to-answer question about what they've been thinking about, working on, figuring out, or preoccupied with.

**Before (field description in an output spec):** `Hook: <how the post would open — the angle that grabs attention>`
**After:** `Hook: <a statement that creates a dopamine spike for the reader — curiosity, pattern-break, or stakes>`

The "before" version describes the field by name. The "after" version describes the effect the field is supposed to have. The effect-description survives the model's instinct to reach for the nearest concrete phrasing.

When a verbatim example genuinely *is* the right teaching tool — because the move is so specific or so subtle that no description captures it — keep it, and surround it with explicit framing about why this exact phrasing is the craft itself and shouldn't be copied. That framing is the difference between a sample and a script.

A particularly leak-prone surface to watch for: blockquoted italic example-answers inside instruction text. The pattern `> *"sample answer phrasing"*` (often appearing under instructions to "think about questions like" or "the kind of answer you're looking for") combines two strong reproduction signals — the blockquote visually presents as an example, and the italic phrasing reads as direct quotation. The model treats both as text-to-reproduce, not pattern-to-emulate. When the underlying intent is to teach the *kind* of answer or the *role* of an answer in a sequence, the placeholder should describe that role explicitly ("a softer reframing answer in the writer's voice; specific enough to anchor a follow-up but informal enough to lower the stakes") rather than supply sample phrasing the model will copy.

## 4. Write for a smart human in plain language

Skills are read by two audiences at once: the model that executes them and the person who installs, audits, or adapts them. Writing that only the model can comfortably parse — compressed jargon, insider shorthand, abstraction stacked on abstraction — fails the second audience silently. The person stops reading, and a skill nobody reads is a skill nobody trusts, fixes, or extends.

So explain complex ideas simply where a simple explanation exists. Prefer the concrete word to the abstract one, the short sentence to the clause-chain, the example to the definition. When a piece of jargon is genuinely load-bearing — a term of art from the source material, a named framework users know by name — keep it, and define it once in plain words the first time it appears.

The test: could a smart person outside the domain read the skill top to bottom and say what it does and why? If a paragraph needs the author present to explain it, the paragraph isn't finished.

This isn't dumbing down, and it isn't a ban on precision. It's the recognition that clarity is a transfer format — the plain version travels across harnesses, across users, and across the gap between the person who wrote the skill and the person debugging it a year later.

## 5. Calibrate the force of a rule to how often the exception is right

Absolute words — never, always, every, only, none, must — steer a model much harder than their literal meaning suggests, and they cost nothing to type. That combination makes them the easiest thing in a skill to overspend.

Spend them where there's genuinely no circumstance under which the exception would serve the process: irreversible actions, safety floors, syntax that breaks if it varies, the things that have to hold when nobody's watching. Everywhere else an absolute costs twice. It suppresses a legitimate move the author never thought to allow, and it devalues the real absolutes elsewhere in the file, which start reading as merely emphatic.

The sharper version of the trap is an absolute bolted onto a condition. Checking a condition takes effort; obeying an absolute takes none. So a rule shaped like *never do X when Y might be true* collapses in practice into *never do X* — the model routes around the whole category rather than evaluating whether Y actually holds. When the checking is the point, the checking has to be the instruction, not a caveat hanging off one.

For everything that isn't absolute, reach for the word that matches the real frequency. Most of the time. Generally avoid. Rarely. Usually prefer. Unless the circumstances warrant it. A calibrated word carries two pieces of information — what to do, and how much room there is — and an absolute deletes the second one.

**Before:** "Never require a prerequisite the user might not have."
**After:** "Prerequisites get a quick check, not a preemptive dodge — look and see whether it's already there, or ask in one sentence. What you're steering around is the twenty-minute side-quest, not the prerequisite itself."

The first version reads as *avoid prerequisites*, so the model quietly downgrades the work rather than asking a one-line question. The second names what's actually being protected, which lets the model tell a cheap check apart from an expensive detour.

## 6. Point at a list; don't restate it

A file that links a reference and also names its contents has made a promise to update itself every time that reference changes. The promise gets broken, quietly, because nothing fails when it does — the enumeration just becomes wrong while still reading as authoritative. That's the damage: a consumer that enumerates reads as *complete*, so whoever loads it trusts the inline list over the canonical file sitting one link away.

The test is one question: **can this list grow?**

If it can, point and stop. Name the reference, say what it's for, and let the file be the list — *"the principles every produced skill follows"*, not *"the three principles (a, b, c)"*. When the enumeration carries routing weight the reader genuinely needs on the spot, keep it and add a short note saying which file is canonical, so a future reader knows what wins when the two disagree.

If it can't — a framework from a published book, a fixed rubric, a closed set the design deliberately pins — leave it inline. The names carry the meaning there, and stripping them to satisfy a rule costs information and buys nothing. Most enumerations in a mature pack are this kind; the sweep is for the ones that aren't.

The other half of this lives at the source. **A list that's designed to grow says so in its own file**, near the top, where anyone about to copy it will see. That way the warning travels with the thing being copied instead of depending on every consumer independently knowing better.

**Before:** "Load `skill-prompting-principles.md` and apply its three principles (shape mirrors output, principle over rule, intent over verbatim)."
**After:** "Load `skill-prompting-principles.md` and apply its principles — the file is canonical and current; don't work from a remembered list."

The "before" went stale twice in one day: once when a fourth principle was added, once when a fifth was. The "after" cannot.

## Used by

- `os-skillify` (SKILL.md operating principles, all four sub-modes, all three file templates) — applied during generation of any new skill, mode, reference, or microtool. Loaded as part of Gate 1 inheritance.
- `os-tune` (`refine` and `extend` modes) — applied during edits to existing skills, so revisions don't regress toward the default failure modes.
- `inheritance-protocol.md` lists this reference as one of the canonical sources loaded by meta-skill operations.

## Malleability note

Canonical: the six principles themselves and their ordering. They name six distinct failure modes — wrong shape, wrong abstraction level, wrong example type, wrong audience, wrong force, wrong locus — that compound when ignored together.

Adaptable: how strictly each principle applies in a given skill. A purely structural routing skill with no prose output and no judgment calls may legitimately be all bullets, all rules, and no examples — that's the shape its output actually has. The principles aren't a stylistic mandate; they're a tool for matching skill-shape to output-shape. A skill that diverges from one or more principles should note the reason in its Design Rationale.

## Source

Surfaced as a workspace principle on 2026-05-24 after the user noticed that earlier skillify runs over-applied list-heavy and rule-heavy patterns to writing-domain skills. Originating note captured in `os-inputs/_os-inbox.md` and elevated here as a shared reference because it applies to every skill-authoring or skill-editing operation.

The fourth principle (plain language for the human reader) was added 2026-08-01 after the user flagged that skill prose was drifting toward high-level compression that reads well to a model and poorly to a person.

The sixth principle (point, don't restate) was added 2026-08-02, immediately after the fifth exposed the cost: thirteen consumer files across nine skills had enumerated this reference's contents inline, so a principle added the day before had been invisible to every one of them. The fix at each site was to point; the fix to the class is this principle plus the grow-warning at the top of this file.

The fifth principle (calibrated force) was added 2026-08-02 after a humanize pass on `os-guided-setup` produced the rule "never require a prerequisite they might not have." The user flagged that an absolute attached to a soft condition collapses into an absolute on the category — the model would dodge prerequisites wholesale rather than spend a sentence checking. Noted as a recurring authoring trap, not a one-off.
