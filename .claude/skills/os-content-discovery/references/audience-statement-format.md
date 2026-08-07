# Audience Statement Format

The canonical audience-statement shape used across content-discovery's EIB modes (and consumed by `writing`, `audience`, `offer`, and others). This document defines the format, the constraints, and how to interpret looser inputs.

## The canonical shape

> *"[Group of people, with up to 3 adjectives] who want to [main desired outcome]"*

Examples:

- *"Aspiring entrepreneurs, online marketers, content creators who want to sell products effectively to a targeted customer base"*
- *"First-time SaaS founders shipping their MVP who want their first 10 paying customers"*
- *"Mid-career creative professionals who want to build a personal brand without quitting their day job"*

The format has two halves:

- **Identity** — who the people are. Up to 3 groupings (the example above lists three: entrepreneurs, marketers, creators), each can be modified by adjectives that sharpen the identity (*aspiring*, *first-time*, *mid-career*).
- **Pull** — what they want. The main desired outcome they're trying to move toward.

## Why this shape

The canonical shape forces specificity in two places that tend to drift toward generic:

**Identity.** *"Entrepreneurs"* is too broad. *"Aspiring entrepreneurs"* narrows. *"Aspiring entrepreneurs, online marketers, content creators"* names the actual cluster — overlapping but distinct sub-populations who share the desired outcome. The adjective layer is where the identity becomes useful for content strategy.

**Pull.** *"Who want success"* is empty. *"Who want to sell products effectively to a targeted customer base"* names the concrete state they're trying to reach. The pull defines the gap content has to bridge.

A statement that's vague in either half produces vague EIB output. Sharpening either half sharpens everything downstream.

## Constraints

**Up to 3 identity groupings.** More than 3 typically signals the audience isn't well-defined yet — the user is hedging by listing every possible reader. The mode can produce statements with more, but the surfacing question is whether a tighter audience exists.

**One pull per statement.** *"Who want to grow their business and feel confident and find purpose"* is three pulls stacked. Pick the one most central to the content angle.

**Concrete pull, not abstract.** *"Who want to make money"* is too vague. *"Who want to land their first $5K consulting client"* is concrete. Concrete pulls produce concrete topics.

## Interpreting looser inputs

The EIB modes tolerate looser inputs and translate to the canonical shape internally. Common inputs and how to interpret:

**A paragraph describing the audience.** Extract the identity groupings and the desired outcome from the paragraph. If multiple outcomes appear, surface them and ask which is most central.

**A persona-style profile.** Profiles often include identity, pain points, goals, and demographics. Pull identity + adjectives from the demographic / role section, pull desired outcome from the goals section.

**A tagline or product description.** Reverse-engineer the audience from the tagline. *"Helping busy parents get fit in 20 minutes a day"* → *"Busy parents who want to stay fit despite limited time."*

**A single-word audience.** *"Entrepreneurs"* — ask for adjectives and a desired outcome before proceeding. The mode can run on a thin audience but produces thin output.

## When to push back on the input

If the supplied audience is too broad to produce useful EIB output, the mode flags this rather than producing weak topics. *"All entrepreneurs who want to succeed"* will produce generic pillar topics that any business audience could use. The mode asks what kind of entrepreneurs and what kind of success before generating.

If the supplied audience contains contradiction (*"Solopreneurs and Fortune 500 executives who want to grow their business"* — too different), the mode flags the contradiction and asks which to focus on.

