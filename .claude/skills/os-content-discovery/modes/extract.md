---
name: os-content-discovery/extract
description: Reverse-engineer the AUDIENCE, SUBJECT, and EMOTIONAL DRIVER from a piece of existing content. Takes a tweet, email, post, blog excerpt, or any short piece and produces a three-line structured output naming who the content is for, what it's actually about (in specific detail), and the psychological appeal in the audience's own words. Triggers on "who is this post for," "extract the audience for this," "reverse-engineer who this is talking to," "what's the emotional driver behind this content." Do NOT trigger for full audience profiling (use `os-audience`) or for extracting voice and structure (use `os-voiceprint` and `os-content-template`).
---

# Mode — Extract (EIB Step 0)

Reverse-engineering audience and emotional driver from a single piece of existing content. Fast, narrow, structured. Produces one audience line, one subject line, one emotional-driver line — the inputs the rest of the EIB chain needs to run.

## When to use

The user has a piece of content (theirs or someone else's) that worked, and wants to understand who it spoke to and what emotional appeal made it land. Common triggers include reverse-engineering a competitor's post, analyzing one of the user's own pieces that performed well, or starting the EIB chain from sample content rather than from a clean audience statement.

If the user already has a clear audience statement and just wants topics, skip to `topics`. If the user wants a deep psychographic profile (jobs-to-be-done, fears, beliefs, motivations across the whole audience), use `audience` instead. This mode produces one line per dimension — a starter for the EIB chain, not a complete profile.

## Inputs

- **Required:** A piece of content. Could be a tweet, an email, a LinkedIn post, a paragraph from a sales page, a blog excerpt. Length typically 100-1500 words.
- **Optional:** Context about the source ("this is by Justin Welsh," "this is from my own newsletter"). Helps calibrate the output but the mode works without it.

## Run

Read the content carefully. Identify the surface signals (vocabulary, references, assumed knowledge) and the deeper signals (what fear or aspiration the piece is implicitly addressing, who's nodding along while reading).

Produce three lines:

**AUDIENCE.** *"[Group of people with up to 3 adjectives]* who wants to *[main desired outcome they want to achieve]."* The adjectives sharpen the group identity (e.g., "ambitious solopreneurs" rather than just "solopreneurs"). The desired outcome is the pull — what they're trying to move toward. This line, on its own, should be parseable as input to `topics`.

**SUBJECT.** *"[The subject or issue of the content, in specific detail]."* Not the topic at the highest level ("marketing"), but the specific issue this piece addresses ("how to figure out and address the specific needs and pain points of a target market because you need to build trust before selling"). Specificity is the value here.

**EMOTIONAL DRIVER.** *"[Psychological appeal in the audience's own words, often expressed as a fear, frustration, goal, or aspiration]."* First-person voice, like the audience is speaking. Captures the why-it-resonates beneath the surface message. Drafted in the way someone might say it to a therapist or close friend.

## Constraints

Avoid clichés and generic descriptors. *"Entrepreneurs who want to grow their business"* is too broad — sharpen to *"first-time SaaS founders shipping their MVP who want their first 10 paying customers."* The adjectives carry weight.

The emotional driver is not a benefit-statement. A line like *"they want to make more money"* is too dry. The right level reads like the audience venting to a close friend — naming the specific tension between what they're trying for and what's not working — long enough to carry a real feeling, not a tagline.

Don't pad with explanation. The mode produces three lines, no preamble or commentary. The user can ask follow-up questions if they want depth.

## Output

```
AUDIENCE: <audience line>
SUBJECT: <subject line>
EMOTIONAL DRIVER: <driver line in audience's own voice>
```

Three lines. No headers beyond the three labels. No commentary.

## Example

Input — a LinkedIn post fragment:

> *"Stop trying to network at events. Most of you are doing it wrong. The people who win at networking aren't the ones with the best business cards or the smoothest pitches. They're the ones who show up curious, ask good questions, and remember what people told them three months later. Your network isn't about quantity. It's about whether anyone would actually take your call."*

Output:

```
AUDIENCE: Mid-career professionals, founders, and consultants who want to build a network that converts to actual opportunities
SUBJECT: Why typical event-networking tactics produce shallow connections and why curiosity, depth, and follow-up over months matters more than business-card volume
EMOTIONAL DRIVER: I've been to so many events and collected hundreds of business cards but my network feels useless when I actually need help — I want connections that mean something but I have no idea what to do differently
```

## Cross-mode suggestions

After `extract`, the natural next step is `topics` using the surfaced audience as input. If the user wants a deeper profile, route to `os-audience`. If the user wants to reproduce the voice and structure of the analyzed content, run `os-voiceprint/from-sample` and `os-content-template` on the same input.
