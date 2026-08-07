# Sequence Architecture

Multi-piece campaign structure. Reference for `modes/email-sequence`. Covers cadence, narrative arc across pieces, opener variety, internal consistency, and how individual emails compose into a campaign.

A sequence is more than a stack of emails. The piece-to-piece progression carries the reader from one state (didn't engage, didn't know about the offer, hadn't decided) to another (engaged, informed, decided). When the architecture works, the sequence feels like one composed thing. When it doesn't, the sequence reads as a collection of unrelated emails the reader unsubscribes from by piece three.

## Sequence types

Different sequence types do different jobs. Writing honors the type as part of the brief.

**Welcome sequence.** New subscribers receive a series introducing the writer and their world. Length: typically 4-7 emails sent over 1-2 weeks. Job: warm the reader, deliver early value, set expectations, segment by interest. The arc usually runs introduction → first useful frame or insight → deeper context → optional offer toward the end (lower conversion than later sequences but cumulative impact).

**Nurture sequence.** Long-term subscribers receive an evergreen flow of value-delivery emails. Length: indefinite, sent weekly or biweekly. Job: keep the reader engaged with the writer's voice and substance over months. Arc is less about progression than about rhythm — each email stands on its own value, with sequence-level voice and recurring themes building familiarity over time.

**Launch / sales sequence.** Time-bound campaign around a specific offer. Length: 5-12 emails over 7-14 days. Job: warm the audience to the offer, surface objections and handle them, build urgency toward a deadline, convert the reader who's been deciding. Arc has clear phases: announcement → value-and-context → social proof → objection-handling → urgency-and-deadline.

**Re-engagement sequence.** Inactive subscribers receive a small flow attempting to reactivate them. Length: 2-4 emails over a week. Job: surface why the subscriber stopped engaging and either reactivate them or cleanly remove them from the active list. Arc: friendly check-in → value reminder → final notice with cleanup.

**Cart-abandonment / pre-purchase sequence.** Triggered by a specific reader behavior. Length: 1-3 emails over 1-3 days. Job: handle the friction or objection that prevented purchase. Arc: gentle reminder → objection-handling → final urgency.

## Cadence

When emails send within a sequence shapes how readers experience the sequence. Cadence too tight crowds the reader. Cadence too loose loses the thread.

Welcome sequences typically run every 1-3 days for the first 4-7 emails, then taper into the nurture flow. Sales sequences run daily or every other day during the active window, with end-of-window emails sometimes hitting twice in the final 24 hours (the "deadline tomorrow" plus "deadline tonight" pattern). Nurture sequences run weekly or biweekly. Deviating from cadence produces unsubscribes from readers who feel surprised.

The brief specifies cadence. Writing honors it without optimization. If the brief says "9 emails over 7 days," the sequence runs that cadence. If the brief is silent, writing asks rather than guessing.

## Narrative arc across pieces

The strongest sequences read as one thing told across pieces. Each email picks up where the prior left off, even when the body content is independent. Common arcs:

**The setup / payoff arc.** Email 1 sets up a question or scenario. Subsequent emails develop it. The final email pays off. Works for nurture sequences and educational drips. Risk: readers who skip the middle miss the payoff context — the final email needs to stand alone enough to land.

**The crescendo arc.** Stakes and urgency rise across the sequence. Early emails are warm and educational. Mid emails introduce the offer with low pressure. Late emails increase urgency. Final emails are direct and time-bound. Works for sales / launch sequences. Risk: the final emails can read as desperate if the arc isn't earned by the middle.

**The thematic-loop arc.** Each email develops a different facet of the same theme. No strict progression, but the theme threads through. Works for nurture sequences, content-series flows. Risk: without progression, the sequence can feel like a series of unconnected pieces — the thread has to be visible.

**The pre-launch / launch / post-launch arc.** Pre-launch emails build anticipation. Launch emails announce and convert. Post-launch emails handle late-deciders and roll into nurture. Works for product / cohort launches. Risk: post-launch emails to people who already bought feel redundant — segmentation matters.

The arc is part of the brief. Writing reads the brief to know which arc the sequence is following, then makes each email play its role in the arc.

## Opener variety

A sequence where every email opens the same way (always with "Hey {{first_name}}," / always with the same setup line) wears thin by piece three. Readers notice patterns. Identical patterns across pieces signal automation rather than authorship.

Variety strategies:

Mix opener shapes across the sequence. Email 1 opens with a story. Email 2 opens with a question. Email 3 opens with a stakes-raise. Email 4 opens with a specific result. Each opener fresh, but each appropriate to its email's job in the arc.

Vary the greeting. Sometimes the email opens with a personal greeting line. Sometimes it opens cold with the first sentence — dropping the reader straight into a moment or a stake. Sometimes it skips the greeting entirely and opens with the subject line's payoff. Variation here keeps the sequence from sounding templated.

Acknowledge the prior email when useful. Email 4 can reference what email 3 promised ("Yesterday I said the system was based on 17 years of experience. Today, the actual mechanic..."). This produces continuity readers feel without forcing every email to open the same way.

Writing flags openers that read identically across pieces. The mode produces sequences with deliberate opener variety. The editor / user can override in specific cases.

## Internal consistency across pieces

Voice, signature, key claims, offer specifics — these stay consistent across the sequence. Drift kills the sequence.

Voice consistency. Every email reads as the same writer. When two writers share a sequence (a co-authored campaign with the writer-switch named in the brief), the signature and voiceprint shift visibly at the handoff — but only at the handoff. Writing honors the per-email author and flags voice drift across pieces by the same author. The mode loads the voiceprint once for the sequence and writes within it across pieces.

Claim consistency. If email 2 names a specific number — claims approved in 11 days, conversion rate of 18%, sequence open rate above 50% — email 6 doesn't say "approved in two weeks" or "about a fifth of subscribers convert." Writing tracks key claims across the sequence and flags inconsistencies before delivery, asking the user which number to standardize on.

Offer specifics. The offer described in email 1 — discount amount, bonuses, cohort date, payment plan, guarantee — stays the same across the sequence. Writing reads the brief for the offer and produces consistent specifics. Drift here is the worst kind: a sequence with conflicting offer specifics confuses the reader and erodes trust.

CTA destinations. All CTAs across the sequence point at the same canonical link (or to logically-consistent variants — a "see the page" link in early emails, a "book a call" link in later emails, both pointing at the same offer). Drift kills attribution and reader trust.

## Sequence-level review

After producing a sequence, the mode runs a brief sequence-level review before delivering. The review checks the four properties above: cadence, arc, opener variety, internal consistency.

The review surfaces any issues without blocking delivery. It names what was checked, what's clean, and what's worth flagging — opener repetition between specific emails, claim drift between specific positions, a CTA that wandered off the canonical destination — so the user can decide whether to revise before sending or ship as-is.

For sequences over 5 emails, the review is especially valuable because consistency is harder to track during piece-by-piece production. The review catches drift the producer might have missed.

## When the brief is missing pieces

A typical sequence brief specifies the audience, the goal, the cadence, the offer, and the writer's voice. If any of these is missing, writing asks.

Common gaps: the brief names "a launch sequence" without specifying length (4 emails or 9?). The brief specifies the offer without specifying the deadline. The brief specifies cadence without specifying which days are off-days — some senders skip Sunday, some don't, and the sequence reads wrong if the producer guesses.

Producing a sequence with gaps in the brief produces a sequence that needs heavy revision. Asking before producing prevents the rework.
