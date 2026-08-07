# Hook Anatomy

What makes a hook work. Reference for `modes/hooks` and for any other mode that needs to produce an opener (the first paragraph of a longform article, the subject line of an email, the headline of a landing page).

A hook is the moment the reader decides whether to keep going. The job is buying enough attention to earn the body of the piece. Different hook shapes serve different jobs. The strongest hooks share a few core properties regardless of shape.

## The four properties of a strong hook

**Specificity earns trust.** A hook with a specific number, named case, or concrete claim outperforms a hook with vague generalities. *"I shipped two things in 4 days that I'd been putting off for six weeks"* outperforms *"productivity hacks changed my life."* The specifics give the reader a reason to believe. The generic version asks them to take it on faith.

**A reason to read NOW.** A hook should answer the silent question every reader asks at the opener: *what's in it for me?* If the hook tells the reader what they'll learn, what they'll gain, or what mistake they'll avoid, the reader has a reason to keep going. A hook that's just clever or atmospheric without delivering this signal often fails to convert browser to reader.

**Tension or curiosity gap.** Strong hooks open with a question, a contradiction, an unexpected claim, or a setup that demands a payoff. The reader keeps reading to resolve the tension. *"The CMO asked me a question that broke my brain"* sets up the payoff (what was the question?). *"Marketing operations is the most under-appreciated function in GTM"* doesn't — it's a flat assertion the reader can agree or disagree with at no cost.

**Voice congruence.** The hook reads in the writer's voice from word one. A polished landing-page hook on a casual newsletter mismatches and signals "this isn't the writer's actual voice." Voice fidelity at the opener earns the rest of the piece.

## Common hook shapes

Hooks fall into recognizable shapes, each with a different mechanism. Most hook batteries should produce variants across shapes rather than minor variations within one shape.

**Curiosity gap.** Set up an unanswered question or unexpected claim. *"I cancelled all my standing meetings for five days. Want to know what happened?"* The reader keeps going to close the gap.

**Pattern interrupt.** Open with something the reader's not expecting in the format. A list-pattern post that opens with a one-sentence story interrupts the "10 ways to..." pattern. *"Most productivity advice is for people who already do the thing"* interrupts the genre's optimism.

**Stakes raise.** Name what's at risk if the reader doesn't engage. *"You're losing money on every claim you submit. Here's why."* / *"The next campaign you launch will fail unless you fix this first."* Risk activates attention.

**Specific result.** Lead with the concrete outcome someone achieved or could achieve. *"Eleven days from first meeting to full claim approval."* / *"I cut our team's standup time by 40 minutes a week with one rule change."* The specificity earns the read. The implied "want to do this too?" is the hook.

**Provocative claim.** Take a position the reader didn't expect, sometimes against received wisdom. *"Best practices are usually mid practices."* / *"Stop trying to write hooks."* Provocations only work when the body actually defends them — empty contrarianism erodes trust.

**Story opener.** Open with a specific moment that pulls the reader into a scene. *"Last Tuesday, I sat in the conference room watching a $400K deal die."* Story openers work for longform and emails — less for landing pages where the reader is scanning rather than committing.

**Question to the reader.** Direct address. *"What did marketing operations contribute to revenue last quarter?"* Works when the question is one the reader hasn't fully answered for themselves. Fails when it's leading or rhetorical.

A hook battery (multiple hook variants for one piece) should typically span 3-5 of these shapes rather than producing 5 minor variations within one shape. The user picks the shape that lands. Production iterates from there.

## What kills a hook

Hooks fail in recognizable ways. Writing flags these during production rather than waiting for editing to catch them.

**Generic openers.** *"In today's fast-paced world..."* / *"Have you ever wondered..."* / *"Let me tell you about..."* These are AI-default openers that signal generic prose. The anti-AI catalog (`../../_shared/references/ai-writing-patterns.md`) includes these for removal. Writing honors the catalog at production time.

**Buried lead.** The hook is hidden three sentences in. The first sentence is throat-clearing. *"I've been thinking a lot about marketing operations lately. Marketing operations is interesting. The CMO asked me a question that broke my brain..."* The actual hook is sentence three. Sentences one and two need to disappear.

**Promise without payoff signal.** A hook that names a promise but doesn't hint at the payoff in the same opener. *"What if I told you about a system that changes everything?"* The reader's response is "sure, what?" — but the hook doesn't carry forward into the read because it's pure tease without specificity.

**Voice mismatch.** A formal hook on casual prose, or vice versa. The reader's first signal about voice comes from the hook — mismatch costs the reader trust.

**Listicle pattern when the body isn't a listicle.** *"5 ways to draft better emails"* opens a listicle. If the body is a single argument with one through-line, the hook misled the reader.

## Length calibrations

Hook length depends on format:

- **Subject lines:** 3-7 words ideal, occasionally up to 12. Specificity in fewer words.
- **Social posts:** First sentence is the hook. Sometimes the first line plus a one-line beat below it (in the line-break-between-most-sentences format).
- **Newsletter / blog post openers:** 1-3 sentences. Often a one-line hook plus a clarifying or expanding sentence.
- **Landing page headlines:** Single sentence, sometimes with a sub-headline below. Specificity matters more than length.
- **Longform article openers:** First paragraph (3-5 sentences). The "story opener" or "scene opener" shapes work especially well here.
- **VSL / video opens:** First 5-10 seconds spoken. Single hook claim that compels watching the next 30 seconds.

The mode produces hooks calibrated to the requested format's length convention. A subject-line hook battery doesn't produce paragraph-length openers. A longform-article opener doesn't produce three-word headlines.

## Voice and the hook

The hook is the strictest voice test in the piece. Generic-voiced bodies sometimes get a pass because the body has substance to carry it. Generic-voiced hooks fail because the hook is doing nothing else but voice-and-promise.

Writing loads the voiceprint and writes the hook within it. If the voiceprint indicates terse, paratactic openers, the hook is terse and paratactic. If the voiceprint indicates lyrical setup-and-pivot openers, the hook follows that shape. A hook that doesn't honor the voiceprint produces a piece the reader can sense isn't the writer's, even before they identify why.

Style samples for hook patterns are especially valuable when they exist. A sample that shows how a specific writer opens pieces in the relevant shape — captured under `os-inputs/style-samples/<author-slug>/<pattern>.md` — teaches the hook mode more than the voiceprint alone. The voiceprint teaches the writer's *voice*; the style sample teaches the writer's *moves*.
