# Email Anatomy

How email writing works. Reference for `modes/email` (single-piece) and `modes/email-sequence` (multi-piece campaigns). Covers subject line, opener, body, close, PS, and the calibration differences across email types.

Email is one of the highest-leverage writing formats because the production cycle is short and the volume is high. A single launch push might run a nine-email sequence; a steady newsletter practice puts out one or more pieces a week; customer-facing operations produce email constantly. Most writing practices touch a lot of email. The anatomy below is the producer's view — what each section does, how the parts compose, what kills an email.

## The five sections of an email

Most emails have five working sections, even when the visible structure looks shorter. Some emails compress sections into one line. Some omit sections entirely. The five-section view names the jobs each part of an email needs to do.

**Subject line.** The first job is buying the open. The subject line is the only part of the email the reader sees before deciding whether to engage. Specific subject lines outperform vague ones. Curiosity gaps work when the body pays them off. Click-bait fails when it doesn't. Length convention: 3-7 words ideal, occasionally up to 12. Specificity in fewer words.

**Opener.** The first 1-3 sentences after the greeting. Opener does for the email what the hook does for an article — sets up the read with specificity, voice, and a reason to keep going. Common opener shapes: a specific moment ("Last Tuesday, watching a $400K deal die..."), a question ("Did you eat anything today?"), a setup the body pays off ("Here's the thing about claims that took three months..."). Voice fidelity at the opener is critical — the opener establishes whether the reader's ear settles in or notices "this isn't the writer's voice."

**Body.** The substantive content. What the email is actually about. Length varies by email type — a sales-sequence email might have a 60-word body that pivots to the CTA, a newsletter issue might have a 600-word body that develops a single argument, a customer-service reply might have a 200-word body that handles a specific request. The body honors the brief's promise from subject and opener.

**Close.** How the email ends. Not always a separate section visually, but the close handles the last impression. For sales emails: a clear CTA. For newsletters: often a question or a small reflection that invites a reply or thought. For customer emails: a clear next step. The close is where the reader's last impression is set, and it's where many drafts fall flat — often by trailing off rather than landing.

**PS.** The optional addendum after the signature. PS lines do surprisingly heavy lifting in direct-response email — the reader who skipped the body sometimes reads only the subject and the PS. A good PS reinforces the offer, names urgency, surfaces objection handling, or adds personality the body didn't have room for. PS is mostly a direct-response convention. Newsletters and customer emails often skip it.

## Email types and their calibrations

Different email types have different shape conventions. Writing honors the type as part of the brief.

**Direct-response sales email (campaign).** Subject is curiosity- or stakes-driven. Opener establishes urgency or names a specific case. Body is short — 80-200 words — pivoting to a clear CTA. Close is the CTA itself. PS reinforces deadline or stacks an additional reason. Voice is high-energy, exclamation marks acceptable, em-dash asides for pacing, sentence-starts with "And" / "But" common. Pain-triplet rhythm characteristic ("Your X is suffering. Your Y is suffering. Your Z is suffering."). Multiple CTAs throughout the body are normal — the reader who scrolls and clicks gets the offer at any point.

**Welcome email (sequence position 1).** Subject is warm, often introductory. Opener thanks the reader and sets context for the sequence. Body delivers immediate value (a quick win, a useful framework, a piece of context the reader didn't have) plus sets expectations for the rest of the sequence. Close warms toward the next email. PS often a personal aside establishing the writer's voice and personality.

**Nurture email (sequence position middle).** Subject is value-forward, not urgent. Opener picks up where the prior email left off (in a sequence) or stands alone (in an evergreen flow). Body delivers substance — a story, a tactical insight, a customer case. Close points to next thing or invites a reply. PS optional.

**Sales / launch email (sequence late position).** Subject is increasingly direct as the sequence approaches the close — "3 days left," "deadline tonight," etc. Opener doesn't bury the lead — it names the deadline or the offer-state directly. Body is shorter than nurture — the reader knows the offer by now and just needs the reminder. Close is the CTA. PS reinforces deadline and any final objection handling.

**Customer email (one-off).** Subject is direct and specific to the request. Opener acknowledges what the customer wrote. Body addresses the request with care and specifics. Close is a clear next step or confirmation. PS rare. Voice is the writer's customer-email voiceprint scope — usually warmer and more empathetic than their general voice.

**Newsletter issue.** Subject is intriguing without being clickbait. Opener uses one of the hook shapes from `hook-anatomy.md`. Body develops one core argument or story (newsletter issues that try to cover multiple things lose readers). Close lands a takeaway or asks a question. PS optional, often used for housekeeping (event announcements, links).

**Pitch / outreach email.** Subject is short and specific to the recipient. Opener is one sentence personalizing the connection. Body states the ask directly and gives the recipient a low-cost way to respond. Close is a specific next step. PS rare.

## What kills an email

Common failure modes that writing flags during production.

**Generic subjects.** Any subject that could apply to a thousand other emails. *"Our latest update."* / *"Important news."* / *"Quick question."* These produce low open rates. The fix is specificity — a number, a name, a curiosity gap with a real payoff.

**Buried lead.** The actual point of the email is paragraph three. The first two paragraphs are throat-clearing. Cut to the point.

**Voice mismatch with sequence.** In a multi-email sequence, each email should sound like the same writer. A sequence where some emails read warm and some read cold-formal usually means the voiceprint wasn't loaded consistently across pieces. The mode flags voice drift in the sequence-level review.

**Wrong CTA position.** Sales emails with the CTA buried at the end of a long body. Add a CTA near the top too — a percentage of readers click before scrolling.

**Vague close.** "Let me know what you think!" without specifying what kind of response is wanted. The reader either replies generically or doesn't reply. Specific closes invite specific responses.

**Email length that doesn't match the goal.** A 600-word sales email when 150 would convert better. A 100-word newsletter when the reader expected a full issue. Length serves the goal. It's not a virtue in itself.

## CTA conventions

Sales emails and many marketing emails carry a CTA — a specific action the reader should take. CTA conventions worth honoring:

The CTA is specific. *"Get the details here"* outperforms *"learn more."* The reader knows what's on the other side of the click.

The CTA is repeated, especially in longer emails. The reader who scrolls past one CTA may engage with the next. Placing CTAs at multiple points captures readers at different scroll-depths.

The CTA matches the brief's commitment. Sales emails name the action ("Grab the pre-sale price"). Lead-magnet emails name the resource ("Download the template"). Webinar emails name the event ("Save your seat for Tuesday's call").

The PS line often carries the strongest CTA. Readers who skim the body sometimes engage with the PS — a strong PS-CTA captures them.

## Sequence-level concerns

Multi-piece email campaigns have campaign-level concerns beyond per-email anatomy. Cadence (how often emails send), narrative arc (how the reader's understanding develops across the sequence), opener variety (each opener should feel fresh — repeated openers wear thin), CTA consistency (each email's CTA should align with the campaign's overall offer), and the close email's role (the final email often does heavier lifting on urgency and objection-handling).

`sequence-architecture.md` covers these in depth for `modes/email-sequence`.
