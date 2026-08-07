# Edit Lenses

Catalog of editorial lenses available to `modes/suggest-edits`. Each lens is a focused editorial perspective — a specific kind of issue to look for and a specific way to think about fixes.

The user picks one or more lenses per draft (or `suggest-edits` self-determines from draft state). Running multiple lenses produces a unified suggestion list (numbered sequentially, synthesizing where multiple lenses flag the same passage).

Output format for all lenses: `../templates/suggestion-list.md`.

---

## Lens: copy-edit

**What it checks:** Sentence-level mechanics across six dimensions:

1. **Redundancy and Repetition.** Each sentence should move the narrative forward. Flag where the writer restates the same idea without carrying the writing forward. (For deeper redundancy work, use the `redundancy` lens.)
2. **Active Voice.** Writing should primarily use the active voice. Passive voice is okay when used appropriately or for effect. Seek ways to make writing more active. (For deeper passive-voice work, use the `active-voice` lens.)
3. **Tenses.** Use consistent and impactful tenses. Often the simple tense ("write") is stronger than other tenses ("writing").
4. **Parallelism.** Lists, whether bullets or comma-separated within a sentence, should have parallel structure / tenses / word choice.
5. **Sentence Structure variety.** Inspired by Gary Provost's "Don't just write words, write music." Pay attention to clauses (independent/dependent), compound vs. complex sentences, comma placement, rhythm. Help users combine, split up, vary, and reconstruct sentences.
6. **Specificity over generality.** Lean into quantifiable numbers, specific problems, specific outcomes. Good content answers four questions: why read it, what will they learn, how will it help, why should they trust you. (For deeper specificity work, use the `specificity` lens.)

**When to use:** Default lens for "edit this draft" with no further specification. Sweeps the broadest range of issues at sentence-level granularity.

**Common failure patterns to flag:**
- Passive voice where active would land harder
- Tense drift (past → present → past mid-paragraph)
- Non-parallel list construction ("running, to swim, and biking")
- Sentence rhythm monotony (everything 12-15 words long)
- Vague claims that should be quantified

**Genre carve-outs (do NOT flag in these registers):**

The 6-item checklist calibrates to typical editorial prose. In specific registers, several checks become false positives:

- **Direct-response copy** — fragments are voice ("Quick one today." / "Stop fighting. Start proving."), short paragraphs are scannability not Sentence Structure failure, repeated rhetorical setups across an email sequence ("If you're tired of: → claims dragging on → carriers nit-picking → late nights") are deliberate parallel construction, NOT redundancy. Repeated framing devices across pieces in a campaign ("One roof pays for the whole thing") are reinforcement, not repetition. Pain-triplet rhythm IS the genre. Calibrate accordingly.
- **Dialogue and reported speech** — register shifts, fragments, and ungrammatical constructions are character voice. Don't apply the checklist.
- **Literary fiction** — the wrong lens entirely. Route to `../modes/fiction-edit.md` instead.

When the input shows direct-response signals (named cases, urgency framing, signature voice with playful descriptors, scarcity / guarantee handling), pause before flagging Sentence Structure or Redundancy issues — the rhythm is likely doing genre work.

**Parallelism check carve-out:** distinguish *broken* parallel construction (which is a real flag — "running, to swim, and biking") from *deliberate* parallel construction (which is voice — "Stop fighting. Start proving."). The former is grammatical drift. The latter is rhetorical pattern. Flag only when the construction reads as accidental.

**Synthesis discipline:** When multiple of the six checks flag the same passage, synthesize into one entry. Briefly note the combined logic ("combining suggestions for redundancy + active voice").

---

## Lens: redundancy

**What it checks:** Four cases of redundancy / repetition:

**Case 1 — Repeated words.** Same word used multiple times in close proximity where rotation would help. Example flagged in source: a Twitter hook using "conflict" four times in five sentences. Don't flag if used as a deliberate rhetorical device (anaphora, epistrophe, symploce, antanaclasis, antistasis, negative-positive restatement, epizeuxis / palilogia). Flag only when repetition is awkward, lazy, or unsuccessful.

**Case 2 — Repeated ideas in one paragraph.** Harder to spot than repeated words. The same point made twice in adjacent sentences with different words. Source example: B2B marketers wanting "engagement and growth" then "messaging that engages and drives growth" — same idea, restated.

**Case 3 — Repeated ideas in one draft.** A claim made and supported in the first H2 then revisited and re-supported in the last H2. Triggers déjà vu. Unless explicitly callback / reframe, this redundancy reads as wasting the reader's time.

**Case 4 — Repeated phrases.** Two or more words used together that have the same meaning. Source examples: "unexpected surprise" (surprise implies unexpected), "shouted loudly," "raced hurriedly," "whispered softly," "deliberated thoughtfully," "finished completely," "smiled happily."

**Phrase reduction patterns** (from source, preserved as a reference list):
- "absolutely certain" → "certain"
- "absolutely essential" → "essential"
- "actual experience" → "experience"
- "added bonus" → "bonus"
- "adequate enough" → "enough"
- "in spite of the fact that" → "although"
- "each and every" → "each"
- "biography of her life" → "biography"
- "in the event that" → "if"
- "period of five days" → "five days"
- "shorter in length" → "shorter"
- "larger in size" → "larger"
- "during the course of" → "during"
- "interestingly enough" → "interestingly"
- "manually by hand" → "manually"
- "because of the fact that" → "because"
- "the people who are located in" → "the people in"
- "make decisions about" → "decide on"
- "draw your attention to" → "point out"

**When to use:** Drafts that feel padded, repetitive, or longer-than-necessary. Often paired with `shorten` mode if the goal is compression.

**Don't flag:** Deliberate rhetorical repetition. If the writer uses anaphora ("I have a dream…") or any literary device that depends on repetition, leave it alone unless it's overdone or unsuccessful.

---

## Lens: active-voice

**What it checks:** Passive-voice constructions where active voice would land harder.

**Definition (from source):**
- **Active voice:** the subject performs the action. *"I decided to invest in Content Editing 101."*
- **Passive voice:** the subject has the action done to it. *"Content Editing 101 was invested in by me."*

**When to flag:** Passive voice that flattens immediacy, dilutes ownership, or distances the writer from action. Active voice tends to be more direct, persuasive, and clear.

**When NOT to flag:** Passive voice used deliberately:
- When the actor is unknown or genuinely irrelevant ("the bill was passed in 1972")
- When the object of the action is the focus, not the actor ("The bridge was built by the Romans")
- When passive distances the writer for diplomatic reasons (academic, legal, internal-comms contexts)

**Suggested rewrites:** Maintain the writer's voice. If they use first person, keep first person. If they use fragments, fragments stay fine. Active-voice rewrites should sound like the writer wrote them, not like a grammar textbook.

**When to use:** Drafts that read as distant, indirect, or evasive. Persuasive content (sales copy, calls to action, op-eds) is especially vulnerable to passive-voice softening.

---

## Lens: specificity

**What it checks:** Vague writing that should be specific.

**The four-question test** (every piece of writing should answer specifically):

1. **Why should they read it?** — Not "write better emails," but *"Overcome low open rates and 5x sales."*
2. **What will they learn?** — Not "killer email tactics," but *"How to use personalization to write emails that actually get opened."*
3. **How will it help them?** — Not "get more opens," but *"2x open rates."*
4. **Why should they trust you?** — Not "industry professional," but *"You've helped 100s of people overcome the same problem."*

**Specificity moves:**
- Quantify: "10k words" not "many words", "133 people" not "tons of people", "$10M+" not "lots of revenue"
- Name the problem: "send DMs that generate Twitter responses" not "send good DMs"
- Name the outcome: "overcome low open rates" not "write better emails"
- Name the proof: "10+ years of selling, sourced or closed $10M+" not "experienced"

**When to flag:** Any passage where a specific claim would land harder than the generic version. Headlines, hooks, subheads, claims of credibility, transitional summaries — all high-leverage targets for specificity.

**When NOT to flag:** When the source is genuinely abstract (philosophy, certain literary fiction, theoretical writing) and specificity would distort. Calibrate to the genre.

**When to use:** Most non-fiction drafts benefit from a specificity pass. Especially valuable for marketing copy, personal essays with credibility claims, and how-to content.

---

## Lens: developmental

**What it checks:** Paragraph-level and section-level argument completeness.

**Primary frame — Claim → Support → Takeaway.** Foundation for logical reasoning. The trio is the minimum architecture for a persuasive paragraph.

1. **Make a claim.**
2. **Support it with evidence** (facts, data, unique experiences, examples).
3. **End with a takeaway** (a practical implication or action).

Source example:
- *Claim:* Regular exercise enhances mental well-being.
- *Support:* Studies show regular physical activity boosts mood and reduces symptoms of depression and anxiety.
- *Takeaway:* To maintain mental health, incorporate daily exercise into your routine.

**Argument-amplification variant** (when the focus is sharpening claims for a skeptical audience):

- Strengthen the claim. Make it spiky, specific, defensible.
- Sharpen the support. Cite stats, research, named cases. The source uses 23-minute refocus stat as an example: *"It takes 23 minutes to refocus after a distraction"* — concrete enough to convince.
- Get ahead of objections. What would a reader resist? Address it before they ask.

**When to flag:** Paragraphs that make a claim and move on. Paragraphs that support without claiming. Paragraphs that meander without landing a takeaway. Drafts that introduce concepts without persuading the reader to act on them.

**Macro vs. micro:** Claim-Support-Takeaway works at the section level (each H2 is a claim) and the paragraph level (each paragraph is a sub-claim). Flag at whichever level is failing.

**When to use:** Argumentative or persuasive content (op-eds, thought-leadership posts, sales copy, evidence-based how-to). Less applicable to pure narrative or descriptive prose.

---

## Lens: what-why-how

**What it checks:** Paragraph-level information completeness using the What-Why-How sandwich.

**The frame:**
- **What** — the key statement / claim / instruction
- **Why** — why does this matter? Why is the reader being told this?
- **How** — how does the reader actually do it? What's the mechanism?

**Why this matters (from source):** Writers often state the What and move on, leaving readers with two unanswered questions ("Why does this matter?" and "How do I do this?"). Unanswered questions are how readers stop reading and find answers elsewhere.

**The sandwich layered example** (from source, ConvertKit positioning):

- *What:* "By understanding its place in the market, ConvertKit strategically differentiates on messaging."
- *What + Why:* "...It is laser-focused on attracting creators eager to 'connect with their audience and earn a living online' rather than everybody interested in email marketing. This specificity resonates deeply with their target audience, to the point where they're known as 'the creator's email platform' amongst the crowd."
- *What + Why + How:* "...Their homepage features a widely known creator directly below the fold and boldly states, 'Your favorite creators use ConvertKit to connect with their audience and earn a living online.'"

**Order:** Doesn't always have to be What → Why → How. Sometimes deeper Why before How. Sometimes "anti-how" (showing what NOT to do before what to do) lands harder by contrast.

**When to flag:** Paragraphs that state What without Why or How. Sections that explain mechanisms without motivating them. How-to content that names steps without justifying them.

**Distinct from developmental:** Developmental is about argument (claim/support/takeaway). What-Why-How is about information (statement/motivation/mechanism). Both can apply to the same paragraph — flag whichever is the more pressing gap.

**When to use:** How-to content, instructional writing, technical explanations. Less applicable to pure narrative or argumentative pieces (use `developmental` for those).

---

## Lens: takeaway

**What it checks:** Whether the draft delivers actionable takeaways at micro and macro levels.

**The "big why" questions** (anchor for macro takeaway):
- Why does this piece of content exist?
- Why does my ideal reader need this piece of content?
- Why will they be interested in it?
- What will they hope to achieve from it?

The answers to these are the content angle. The macro takeaway should hit that angle on the nose.

**Micro takeaways** (at section ends or post bottoms, ask):
- Have I included takeaways readers can emulate?
- Have I included strategic CTAs (subtle and obvious) that motivate readers to complete an action?

**What a takeaway is:** Often the first step in a process, a general rule or maxim to follow, or a recommended action. It tells the reader what to do next.

**When to flag:**
- Drafts where the macro takeaway is buried, vague, or missing
- Sections that build to a point but then trail off without prescribing
- Posts that explain a concept without telling the reader what to do with it

**When to suggest a higher-level takeaway:** When the existing takeaway is too narrow ("use this one tactic") and a zoom-out lands stronger ("the principle behind this is X — apply it to your own situation"). The source calls this "moving something more toward the end" or "adding something new entirely."

**When to use:** Long-form content, how-to posts, newsletter pieces with educational intent. Less applicable to pure narrative, pure description, or short reactive content.

---

