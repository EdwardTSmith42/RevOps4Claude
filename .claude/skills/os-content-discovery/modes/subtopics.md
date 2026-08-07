---
name: os-content-discovery/subtopics
description: Expand a pillar topic into 5 specific subtopic angles for a given audience. Takes an audience statement plus a pillar topic (or list of topics) and returns 5 specific subtopic angles per topic — the subjects individual content pieces would actually address. Subtopics are descriptive titles, sentence case, varied with minimum overlap, biased toward "stop the scroll" specificity. Triggers on "expand this topic," "give me subtopics for X," "what specific angles can I take on [topic]," "break this topic into subtopics." Do NOT trigger for generating pillar topics from an audience (use `topics`) or for emotional drivers per subtopic (use `drivers`).
---

# Mode — Subtopics (EIB Step 2)

Expand a pillar topic into 5 specific subtopic angles. Subtopics live one level below pillar topics — they're the actual subjects individual posts, emails, and articles address. Where a pillar might be *"Audience Building on Social"*, a subtopic might be *"Strategies for building a following on LinkedIn without dedicating hours a day."*

## When to use

The user has an audience and at least one pillar topic, and wants to know what specific angles to take on that topic for content. Could come straight out of `topics` (the user picks one pillar and expands it) or supplied directly when the user already has a pillar in mind.

If the user has a subtopic and wants emotional-driver work for it, route to `drivers`. If the user has multiple pillar topics and wants subtopics for all of them, supply them as a list — the mode runs subtopics for each.

## Inputs

- **Required:** An audience statement, in the *"[group] who want [outcome]"* shape or looser equivalent.
- **Required:** A pillar topic, or a list of pillar topics. If a list, the mode produces 5 subtopics per topic.
- **Optional:** Existing subtopics to avoid (negative filtering for content-strategy refresh).
- **Optional:** Calibration cues. *"Focus on tactical subtopics"* or *"more mindset-leaning subtopics"* — honored without abandoning the engagement bias.

## Run

Read the audience and the pillar topic together. The subtopic angles live where the audience's frictions, fears, and successes intersect with the pillar's territory.

Generate 5 subtopics per pillar. Each subtopic is a descriptive title — a sentence (or sentence fragment) describing what a single content piece on this subtopic would address. Sentence case. Varied with minimum overlap.

Bias toward specific over generic. *"Common pitfalls in managing a one-person business and how to re-wire your brain to avoid them"* is the right level. *"Productivity tips"* is too broad. The subtopics should make a content creator immediately think *"I could write that post."*

Mix surface and depth. Some subtopics should hit familiar pain-points the audience already names. Others should surface less-obvious angles the audience would recognize as true once stated but hadn't articulated. The mix is what separates content-strategy work from generic listicles.

Bias toward actionable, business-relevant content per the stance documented in `../references/content-strategy-stance.md`. Replace any subtopic that drifts into ethics / sustainability / inclusiveness / data-driven decision-making with one about solving a specific problem instead.

## Constraints

Avoid redundancy. Five subtopics that all cover the same idea waste the slot. Each should be a meaningfully different angle.

Sentence case throughout. *"Why clarity and conciseness must be THE top priority if you're writing for internet audiences"* — not Title Case, not all caps.

Output as a numbered or bulleted list with no preamble or commentary. If running on multiple pillar topics, group output by topic.

## Output

For a single pillar topic:

```
1. <Subtopic angle as a descriptive title>
2. <Subtopic angle as a descriptive title>
3. <Subtopic angle as a descriptive title>
4. <Subtopic angle as a descriptive title>
5. <Subtopic angle as a descriptive title>
```

For multiple pillar topics:

```
**<Pillar topic 1>**
1. <Subtopic 1>
2. <Subtopic 2>
...

**<Pillar topic 2>**
1. <Subtopic 1>
2. <Subtopic 2>
...
```

## Example

Input:

> Audience: aspiring solopreneurs and content creators who want to build a following while still doing client work
>
> Topic: Audience Building on Social

Output:

```
1. Strategies for building a following on LinkedIn without dedicating hours a day
2. How to actually niche down when creating content (without over-niche-ing)
3. Mental breakthroughs all solopreneurs need if they're going to build an audience
4. Why clarity and conciseness must be THE top priority if you're writing for internet audiences
5. Psychology-driven content: using cognitive biases to your advantage
```

## Cross-mode suggestions

After `subtopics`, the natural next step is to pick one and run `drivers` on it to surface the emotional appeal. With audience + subtopic + drivers in hand, the user has enough to write a brief and start drafting.

If the user wants more variety on a single pillar topic, run `subtopics` again with the existing 5 supplied as negative filter.
