---
name: os-content-discovery/topics
description: Generate 5 pillar content topics from an audience statement. Takes a "[group of people] who want [desired outcome]" audience definition and returns 5 broad pillar topics most likely to engage that audience for a content strategy aimed at building awareness, authority, trust, and ultimately converting to leads or sales. Triggers on "give me topics for [audience]," "what pillar topics for X audience," "generate content topics," "5 topics for [audience]." Do NOT trigger when the user has a topic and wants subtopics (use `subtopics`) or wants emotional drivers for a subtopic (use `drivers`).
---

# Mode — Topics (EIB Step 1)

Generate 5 pillar topics from an audience statement. Pillar topics are the broad themes a content strategy returns to repeatedly — not comprehensive coverage of a knowledge domain, but the angles most likely to engage, build trust, and ultimately convert.

## When to use

The user has an audience and wants to know what to write about at the pillar level. Could be the user's own audience, a client's audience, or an audience surfaced via `extract` from a sample piece. The output is the input to `subtopics` for any pillar the user wants to expand.

If the user already has a pillar topic and wants subtopic angles, route to `subtopics`. If the user wants emotional resonance work for a specific subtopic, route to `drivers`. This mode operates at the highest level of the EIB ladder.

## Inputs

- **Required:** An audience statement, ideally in the *"[group of people] who want [desired outcome]"* shape. The mode tolerates looser definitions (a paragraph describing the audience, a tagline, a customer profile) and infers the audience structure when needed.
- **Optional:** Constraints. The user might say *"focus on practical / tactical topics"* or *"avoid deep mindset stuff"* — the mode honors these without abandoning the underlying engagement bias.
- **Optional:** Existing topics to avoid. If the user already has a content strategy with pillars and wants 5 *new* topics, supply the existing ones for negative filtering.

## Run

Read the audience statement. Identify the desired outcome (the pull) and the implied gap (what stops them from getting it today). The pillar topics live in the space between *where they are now* and *where they want to be*, especially the emotional and operational frictions in that gap.

Generate 5 pillar topics. Each topic is a broad theme the content strategy can return to over many pieces — not a single article subject. Where possible, frame each topic as an *Action with a Purpose* (e.g., *"Audience Building on Social"* rather than *"Social Media"*). Topics should have variety with minimum overlap. Mix safer must-cover topics with at least one or two surprising angles the audience would feel compelled to engage with.

Bias toward topics that work for online business audiences specifically — competitive edge, money-making, productivity, mental mastery, mindset shifts, success systems, processes, mental models, business frameworks, immediately actionable tips. Unless the audience description specifically calls for them, avoid topics centered on ethics, sustainability, inclusiveness, data-driven decision-making, or economic uncertainty. The full content-strategy stance is in `../references/content-strategy-stance.md`.

Topics are short — usually 2-6 words. Long enough to be unambiguous, short enough that they read as content pillars not article titles.

## Constraints

Avoid generic / encyclopedic coverage. *"Marketing"* is too broad. *"Content Creation for Professional Audiences"* is the right level — broad enough to cover many pieces but specific enough to define the angle.

Avoid topics that just restate the audience's desired outcome. *"How to grow your business"* for an audience of solopreneurs who want to grow is circular. The pillar topics should illuminate paths to that outcome, not name the outcome itself.

Output as a numbered list, no preamble or commentary. The format should be scannable — no descriptions, no rationale, just the topics.

## Output

```
1. <Topic 1>
2. <Topic 2>
3. <Topic 3>
4. <Topic 4>
5. <Topic 5>
```

Five topics. Numbered list. No headers, no rationale, no postamble.

## Example

Input audience statement:

> *"Aspiring entrepreneurs, online marketers, content creators who want to sell products effectively to a targeted customer base"*

Output:

```
1. Product-Market Fit
2. Audience Building on Social
3. Monetizing Content
4. Branding and Positioning
5. AI Process Design and Automation
```

## Cross-mode suggestions

After `topics`, the natural next step is to pick a pillar and run `subtopics` on it. The user can iterate — request 5 more topics in a different direction, ask for variations on a specific topic, or move directly to subtopic expansion.

If the user wants a richer audience profile to inform topic choice, route to `os-audience` first and feed its output back into this mode.
