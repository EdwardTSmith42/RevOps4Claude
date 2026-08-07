---
name: os-content-discovery/explore
description: >-
  Develop a kernel idea into a multi-section thinking essay. Used to test whether an idea has substance, develop a half-formed thought before drafting, or think *with* one idea from a book, lecture, or podcast. Triggers on "unpack this for me," "what's underneath this idea," "develop this thought," "think with me about X," "explore this thesis," "what's interesting about this." Do NOT trigger for finished prose for an audience (use `os-writing`) or topic ideation across an audience (siblings `topics` / `subtopics`).
---

# Mode — Explore

Develop a kernel idea into a rich thinking essay. The user has a small piece of substance — a sentence, a tweet, a few bullets, a half-formed thought — and wants to know what's actually interesting about it before deciding whether to draft, what to draft, or how the idea hangs together intellectually. The output is a substantive exploratory analysis, not a draft for publication.

## When to use

The user has a kernel idea and wants to think with it rather than turn it into finished content yet. Common triggers include:

- A tweet-sized insight the user is wondering whether to develop further
- A bullet list of observations the user wants to explore as connected ideas rather than separate items
- A thesis statement the user wants to pressure-test for substance
- Notes from a book, lecture, or podcast where one idea stuck and the user wants to think with it
- A half-formed concept the user wants to develop before pitching, drafting, or teaching

If the user wants finished prose for an audience, route to `os-writing`. If the user wants to break the idea into multiple format variants, route to `os-content-mining` (`format-remix`). If the user wants topics or subtopics generated from an audience, route to `topics` / `subtopics`. This mode operates on a single idea and produces a single deep exploration of it.

## Inputs

- **Required:** The source idea. Could be one sentence, a tweet, a thesis, a 5-bullet observation, a concept name with brief context, or a quoted passage the user found resonant.
- **Optional:** Context — where the idea came from (a book, a conversation, a personal observation), what domain it lives in (education, business, design, writing), what the user is considering doing with it (drafting a post, building a course, just thinking).
- **Optional:** Direction or constraint — *"focus on the business implications,"* *"keep it short,"* *"go deep on the psychology underneath,"* *"don't get into objections, just explore the mechanism."* The mode honors direction without abandoning the rich-exploration shape.

## Run

Read the source idea. Resist the temptation to react quickly — the value of this mode is sustained intellectual attention, not summary. Spend time inhabiting the idea before producing output.

The output is structured as a multi-section essay. The exact section list flexes per idea, but the canonical shape draws from the following moves. Use the ones that fit. Skip the ones that don't.

**Open with the core insight.** Lead the essay with a one-paragraph statement of what makes the idea interesting or important. Not a topic-frame ("this is an idea about X") — the actual claim about *why it matters*. This anchor sets the rest of the exploration. The opener should make a concrete claim about the leverage point or the surprise in the idea, in a way the reader can argue with — not a generic "this is sophisticated" frame the reader can't push against.

**Identify the fundamental problem the idea solves.** What's the trouble that exists in the world without this idea? Who has it? Why is it troublesome? The sharper the problem-articulation, the more the idea's value becomes visible.

**Break down the essential elements or mechanism.** Most interesting ideas have 3-5 component moves that combine to produce the effect. Surface them. For each, contrast the old / traditional way with the new / proposed way. *"Traditional: [X]. New: [Y]. Result: [Z]."* The contrast is what makes mechanisms legible.

**Surface the deeper philosophy or principle underneath.** Many ideas worth exploring are surface manifestations of deeper principles — the surface idea is a useful container, but the principle is what travels to other domains. Ask what abstract principle the specific idea instantiates, name it directly, and show one or two other places the same principle shows up. The principle often outlives the specific instance.

**Anticipate objections and reframe them.** What would skeptics say? *"It won't work because…"* *"The downside is…"* *"This is too simple to be that powerful."* List the strongest 2-3 objections, then answer each one — not by dismissing, but by exposing the assumption underneath the objection that the idea overturns. Objections often reveal *why* an idea is novel.

**Identify ripple effects or second-order consequences.** What changes downstream of this idea? Who else benefits? What new problems does it create? What previously-hidden patterns become visible? Ripple effects extend the idea's territory and surface adjacent angles the user might draft about later.

**Close on the elegant heart.** End with a paragraph that distills what makes the idea work — often the elegant simplicity, the surprising leverage point, the insight the whole thing rests on. This closing isn't summary — it's the high-density restatement that the reader walks away with.

Section headers can be used liberally — the output is a structural / scannable essay, not a wall of prose. Sub-headers within each section are fine when the section has multiple parallel moves to make.

## Output shape

A multi-section essay typically 600-2000 words depending on the idea's depth. The structure follows the moves listed above, but the mode picks which sections fit and which to skip. Not every idea warrants a full ripple-effects section. Not every idea has serious objections to address.

The essay opens with a one-paragraph anchor that names what makes the idea interesting. Sections follow with descriptive headers (`## The Core Innovation: Making Thinking Visible`, `## Why Teachers Resist (And Why They Shouldn't)`, etc.) — headers should be specific to this idea, not generic templates.

Bold sub-headers within sections (`### **Cognitive Load Management**`) call out the major moves. Bulleted lists work for breakdowns of essential elements, contrast tables, ripple effects, and objection-and-response pairs. Prose carries the connective tissue and the philosophical / closing sections.

The closing section restates the elegant heart in 1-2 paragraphs.

## Constraints

**Don't pad.** If the idea is thin, the exploration is short — and the mode says so directly: *"This idea has a clean core but doesn't seem to extend to deeper philosophy or significant ripple effects. Here's the core insight, briefly."* Padding a thin idea into a long essay produces noise.

**Don't drift into draft mode.** This is a thinking tool, not a public-facing piece. Skip the pleasantries, the audience-warm-up, the *"You've probably noticed that..."* opening. Go directly into the analysis. The output is for the user, who already cares about the idea.

**Honor what's actually interesting.** Don't manufacture depth. If the idea is interesting because of its mechanism, focus there — don't force a philosophy section if the philosophy is generic. The mode adapts its section list to what the idea actually has to offer.

**Resist universal templates.** The structural moves listed above are a menu, not a checklist. An idea that's mostly a contrarian thesis might be best explored through objection-and-reframe alone. An idea that's mostly mechanical might need essential-elements alone.

**No semicolons.** Per the format-mirrors-output principle.

**Bullets are tools.** Use them for breakdowns and contrast tables, not for everything. Prose handles the connective tissue and the philosophical / closing material.

## Iteration

After producing the initial exploration, the user often wants to dig further on a specific section. *"Go deeper on the philosophy."* *"What other objections might exist?"* *"What's the business application of this?"* The mode supports targeted iteration — re-running on the same idea with a focused direction, producing an extended treatment of one section rather than rewriting the whole essay.

## Cross-mode suggestions

After `explore`, useful follow-ups depend on what the user wants to do with the developed idea:

- *Draft a post or essay built on the idea.* Route to `os-writing/longform-article` or `os-writing/email`, supplying the explored essay as source material.
- *Find the audience this idea speaks to.* Route to `extract` or `audience`.
- *Reshape the idea into multiple formats.* Route to `os-content-mining/format-remix`.
- *Save the exploration as a brief* for downstream drafting work. Use `os-library/save` with `type: brief`.
- *Test the idea by exploring an opposing one* and comparing. Re-invoke `explore` on the opposing thesis.
