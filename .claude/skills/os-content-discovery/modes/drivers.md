---
name: os-content-discovery/drivers
description: Generate 8 FFGAs (2 fears, 2 frustrations, 2 goals, 2 aspirations) capturing how an audience feels about a specific subtopic. Takes an audience statement and a subtopic and returns 8 first-person emotional statements written in the audience's own voice — the way someone would describe their feelings to a therapist or close friend. FFGAs draw on Maslow, Plutchik, Cialdini, Fogg, empathy maps, and the 5 whys for depth. Triggers on "give me FFGAs for [subtopic]," "what's the audience feeling about X," "fears and frustrations and goals and aspirations," "emotional drivers for this subtopic." Do NOT trigger for surface emotional-appeal-from-content (use `extract`) or for full audience profiling (use `os-audience`).
---

# Mode — Drivers (EIB Step 3)

Generate 8 FFGAs (Fears, Frustrations, Goals, Aspirations) for a specific subtopic and audience. FFGAs are the emotional-driver layer that powers persuasive content — written in the audience's own first-person voice, capturing what they actually feel rather than what they would politely say.

## When to use

The user has an audience and a specific subtopic, and wants to understand the emotional terrain underneath that subtopic before writing about it. Could come from `subtopics` (the user picks one and runs drivers on it) or supplied directly when the user already has both inputs.

This mode produces emotional resonance work for one subtopic. It's not a full audience-feeling profile — for that, use `audience`. It's not a one-line emotional-driver extraction from existing content — for that, use `extract`. Drivers operates between those at the subtopic level.

## Inputs

- **Required:** An audience statement, in the *"[group] who want [outcome]"* shape or looser equivalent.
- **Required:** One subtopic, or a list of subtopics. The mode produces 8 FFGAs per subtopic.
- **Optional:** Already-used FFGAs to avoid (so the mode generates fresh ideas when expanding existing emotional-driver work).
- **Optional:** Calibration. *"Mostly fears and frustrations"* or *"focus on aspirations"* — honored within the 2/2/2/2 default unless explicitly overridden.

## Run

Read the audience and the subtopic together. Meditate on the issue from the audience's perspective — not as an outside analyst, but from inside their daily experience of the problem.

Produce 8 FFGAs. The default mix is 2 fears, 2 frustrations, 2 goals, 2 aspirations. Each is a first-person statement written the way the audience would actually express the feeling — to a therapist, a close friend, a magic crystal ball reading their mind. Not the way they would describe it on a sales call or in a polite product survey.

The four FFGA types each capture a different emotional valence:

- **Fears.** Negative feelings about what *might* happen — what they might lose, what they're scared of being seen as, what could go wrong if they keep going (or stop). Forward-looking and conditional.
- **Frustrations.** Negative feelings about what's *already happening* — what isn't working, what's stuck, what keeps tripping them up despite effort. Present-tense and concrete.
- **Goals.** Positive desired outcomes, often tactical or operational — what they want to achieve, the move they're trying to make.
- **Aspirations.** Positive desired states of being, often identity-level or transformational — who they want to become, the version of themselves they're reaching for.

Aspirations and goals should not just be the sign-flipped inverses of fears and frustrations. A goal that's the polite mirror of a frustration produces thin output (the audience already knows they want the opposite of what's bothering them). Each FFGA should stand alone and offer a distinct emotional angle the others don't cover.

Draw depth from the source frameworks documented in `../references/ffga-frameworks.md`: Plutchik's Wheel of Emotions for emotional nuance, Maslow's Hierarchy of Needs for level-of-need, the 5 Whys for going beneath surface feelings, Cialdini's Persuasion Principles for what's psychologically pulling them, the Fogg Behavior Model for friction points, empathy maps for what they say versus think.

Mix surface and depth. Some FFGAs should hit feelings the audience would name without prompting. Others should surface deeper feelings the audience would recognize as true once stated but hadn't articulated.

## Constraints

First-person voice. *"I'm exhausted..."* not *"They feel exhausted..."* The voice is the craft move that makes the difference — drafted prose pulled from third-person FFGAs reads dry, while drafted prose pulled from first-person FFGAs reads alive.

Variety with minimum overlap. Eight FFGAs that all circle the same fear waste the slots.

Each FFGA stands alone. Don't reference earlier FFGAs or build chains. The output is a list of independent emotional snapshots, not a narrative.

Sentence case. Emojis allowed but not required and not in every line.

Replace any FFGA that drifts into ethics-y territory with one about feelings around solving a specific problem instead, per the content-strategy stance.

Output as a labeled list — Fears / Frustrations / Goals / Aspirations as section headers, two FFGAs per section, no preamble.

## Output

```
**Fears**
1. <FFGA in audience's first-person voice>
2. <FFGA in audience's first-person voice>

**Frustrations**
3. <FFGA in audience's first-person voice>
4. <FFGA in audience's first-person voice>

**Goals**
5. <FFGA in audience's first-person voice>
6. <FFGA in audience's first-person voice>

**Aspirations**
7. <FFGA in audience's first-person voice>
8. <FFGA in audience's first-person voice>
```

## Example

Input:

> Audience: solopreneurs and creators with day jobs who want to build a following on social
>
> Subtopic: How to actually niche down when creating content (without over-niche-ing)

Output:

```
**Fears**
1. I'm terrified that if I niche too hard I'll cap out my growth — what if the niche is too small and I plateau before I even build something?
2. I'm scared everyone is going to think I'm boring or one-note if I keep posting about the same thing

**Frustrations**
3. I keep posting about three different things and nothing sticks — my engagement is all over the place and I have no idea what's actually working
4. The advice to "pick a niche" sounds simple until you actually try it and realize you have like seven things you care about

**Goals**
5. I want a clear answer to what I post about so I stop second-guessing every piece I draft
6. I need a way to test niche directions without committing to one for the next 12 months

**Aspirations**
7. I want to be the person someone immediately thinks of when their friend says "do you know anyone who does X?"
8. I want to feel like I've finally found my lane — that thing where the content flows because I know exactly who I'm writing for
```

## Cross-mode suggestions

After `drivers`, the user has audience + subtopic + 8 FFGAs and is ready to write a brief or draft directly. If the brief covers a recurring subtopic, save it via `os-library/save` so future drafting work can load it.

If the user wants emotional-driver work that goes deeper than 8 FFGAs (full empathy map, jobs-to-be-done analysis, beliefs and objections), route to `os-audience`.
