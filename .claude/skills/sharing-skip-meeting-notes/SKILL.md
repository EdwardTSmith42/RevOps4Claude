---
name: sharing-skip-meeting-notes
description: Turn a skip-level 1:1 (a senior leader meeting a direct report's report) into structured, fair, developmental themes to share with that person's direct manager. Use whenever the user wants to summarize or share notes from a skip-level or "skip" meeting, write up a 1:1 for someone's manager, turn a Read AI or other meeting transcript of a one-on-one into manager-facing themes, or prepare coaching-ready feedback about a report for their manager. Encodes HFD's COACHING feedback framework, the four company values, the direct-but-curious conversation process, and the fairness and privacy guardrails for passing notes up a level. Trigger even if the user just says "make notes for [manager] from my 1:1 with [report]" without the words "skip-level."
---

# Sharing skip-level meeting notes

How to turn a skip-level conversation into a note the report's direct manager can actually coach from. A skip-level is when a leader meets one of their reports' reports (skipping the manager in the middle). The output is a short, fair, strengths-first themes doc addressed to that direct manager.

The hard part is not summarizing. It is being honest and useful without being unfair, without going around the manager, and without turning a candid conversation into a performance file. This skill exists to get that balance right every time.

## What good looks like

A good skip-level note:

- **Equips the manager, it does not replace their judgment.** You are handing them signal so they can coach better, not grading their report for them.
- **Leads with strengths, specifically.** Real, observed strengths first. Vague praise is useless; specific praise reinforces behavior.
- **Carries at most one or two development threads,** framed as opportunities with a concrete next step, never as a verdict.
- **Separates the person from the process.** Systemic and cross-team issues go in their own section so a process problem is never misread as the person's failing.
- **Stays in the person's corner.** Skip-levels surface candor because the report trusts the room. Honor that trust.

## Hard rules (read before writing)

1. **Audience is the direct manager.** Write to them ("you"). The goal is coaching support, not evaluation, and never a way to bypass them. If the notes contain anything that should go to HR or up the chain instead, say so to the user rather than burying it in a coaching note.
2. **Behavior and impact, never character or mind-reading.** Describe what was observed and its effect. Do not diagnose motivation, attitude, or mental state. "She could not surface specific examples in the moment" is fair; "she is disorganized" is not.
3. **Cap development threads at one or two.** A list of weaknesses is a review, not a coaching aid, and it poisons trust if it leaks.
4. **Protect confidences.** If the report shared something in confidence, or something that could damage them or a third party if repeated, generalize it or leave it out. When in doubt, leave it out and tell the user you did.
5. **Do not name-and-shame third parties.** Describe patterns ("incomplete forms from enrollment"), not individuals, unless naming is clearly fair and necessary.
6. **Anchor to the company values by name where it fits,** but only where the behavior genuinely maps. Forced value-tagging reads as boilerplate.
7. **One consistent message.** If the skip manager already gave the report feedback or an ask in the meeting, note it so the direct manager can reinforce the same thing rather than contradict it.
8. **No unapproved promises.** Do not state or imply the manager can sponsor, promote, or move someone into a role, or commit headcount, budget, or a timeline, until it is approved. Frame growth as developing and advocating for the person, and hold any role talk until there is a real, approved opening.
9. **Verify before you assert.** Names and facts from auto-transcripts are unreliable. Verify them against a source (participant list, SharePoint, Microsoft 365) before they go in the note, and represent events as they actually happened. See the peer-review gate below.

## The conversation process behind the notes

This is the model the notes assume and reinforce: a strategic feedback conversation that is **direct but leads with curiosity**. Use it to read a transcript, and recommend it when coaching the manager on follow-up. Direct means clear and specific. Curiosity-led means you ask before you assert, so the other person stays in the conversation instead of defending.

1. **Set the intention.** Name that feedback is a gift and the point is to help each other get better. Assume positive intent. Ask for feedback in return. This builds a two-way culture rather than a one-way verdict.
2. **Lead with curiosity.** Open with genuine questions, not conclusions. "What patterns have you been seeing?" surfaces more truth than "Here is what is wrong." Curiosity also tends to be where growth starts (it is often how someone discovers the next role they want).
3. **Share observations.** Use the COACHING formula below. Specific, observed, impact-anchored.
4. **Co-create expectations.** Build the next step *with* the person rather than assigning it. Ownership beats compliance.
5. **Close with clarity.** Confirm the takeaways and who owns what, and end on reinforcement.

> Praise can be one person talking. Coaching has to be two people talking. If the note (or the conversation) is all transmit and no receive, it is not coaching yet.

## The COACHING formula

Every strength and every development thread uses the same shape. Feedback that is not specific is not helpful.

- **I observed X.** (Concrete, behavioral, what actually happened.)
- **I believe X had Y impact.** (The effect on the work, the team, the customer, the risk.)
- **What do you think?** (For the live conversation: this invites the person in. In the written note, this becomes the "ask the manager how they would approach it" move.)
- **Here is a suggestion for moving forward.** (Reinforce the behavior if it is a strength; offer a doable next step if it is developmental.)

**Example (strength):**
> *Observed:* She came to the skip-level with a written list of questions about company metrics and what breaks as the team scales.
> *Impact:* She is thinking a level above her role, which makes her a strong peer voice and someone to develop.

**Example (developmental, told honestly):**
> *Observed:* On a banking-change request she acted before verifying it came from the decision maker. She has since tightened her own follow-up.
> *Impact:* The miss created risk on a sensitive change. The encouraging part is she corrected her own process once she saw the gap.
> *Suggestion:* Reinforce verify-first as the default, before acting, every time.

Note the second example does not dress the miss up as a strength. If someone failed a step and then improved, say exactly that, in that order. That honesty is what makes the note trustworthy.

## Values anchors

Tag observed behaviors to the value they express. Only where it genuinely fits.

| Value | Maps to behaviors like |
|---|---|
| **Excellence** | Critical thinking, accountability, integrity, rigor, seeking growth, holding a high bar |
| **Passion** | Engagement, energy, taking pride and ownership, going beyond the ask |
| **Innovation** | Proposing solutions, automating or simplifying, transforming an idea into something real |
| **Collaboration** | Mentoring, generous peer reads, feedback in both directions, building others up, trust and humility |

## Workflow

1. **Get the transcript.** If it is a Read AI meeting, use `list_meetings` to find the 1:1 by participant and date, then `get_meeting_by_id` with `expand: ["summary", "chapter_summaries", "action_items", "key_questions", "topics", "transcript"]`. Read the chronological `text` field, not just the summary; themes live in the back-and-forth.
2. **Confirm the cast.** Identify the report, the direct manager (the audience), and the skip manager. If the user has not said who the manager is, ask once.
3. **Extract themes, not a transcript replay.** Pull the few things that matter: standout strengths, one or two growth threads, operational and cross-team signals, and action items. Map strengths to values.
4. **Apply the COACHING shape** to each strength and development thread (observed, impact, and for developmental items a concrete suggestion).
5. **Draft from the template** at `assets/skip-notes-template.md`.
6. **Run the peer-review gate** (next section) before producing anything. This is not optional: verify names and facts against sources, kill overclaims (especially unapproved role moves), confirm every characterization matches what actually happened, and check fairness and clarity.
7. **Deliver as a markdown file** and offer a tone variant (below).

## Review before you ship (peer-review gate)

Run this pass on the draft before producing the final note. It is the difference between a draft and something a leader can send under their own name. When in doubt on any fact, verify it or leave it out.

1. **Verify every name and fact against a source, not the transcript.** Auto-transcripts mis-hear names and details. Cross-check names against the meeting participant list, SharePoint, or Microsoft 365 before using them. (Real example: an integration analyst transcribed as "Rena" is actually Rina Cho.)
2. **Kill overclaims.** The big one: never state or imply the manager can sponsor, promote, or move the person into a role until it is approved. Frame growth as develop-and-advocate. Same for any unapproved commitment of headcount, budget, or timeline.
3. **Make every characterization match what happened.** Do not upgrade a miss into a strength. If the person failed a step and then improved, say exactly that, in that order.
4. **Check fairness.** Is a systemic or third-party problem being pinned on the person? Is anything shared in confidence being repeated?
5. **Read it as the manager will.** Is the point clear in one pass? Does the tone fit the relationship? Cut anything that does not earn its place.

Only after this pass do you produce the result.

## Output structure

Assume the manager reads in three minutes and acts in two. Keep it to about one screen. Use the template at `assets/skip-notes-template.md`. The sections, in order:

1. **One-line context header** (report, who it is for, date). Keep it small so the hook still lands.
2. **The hook** (a scroll-stopping statement, not a summary, not a question).
3. **Ascending reveals** (the strengths, ordered by increasing importance, each tagged to a value where it fits, behaviors in italics). Build momentum with light signposts ("Then it got better", "Here is the part worth your attention"). Put the most important or most exciting insight last.
4. **One lever** (the single development thread, COACHING shape, with a one-line fairness note if the cause is systemic). Frame it as upside.
5. **The 2-minute action block** (numbered, owner-tagged, fast to start: a message, a greenlight, a single ask).
6. **A closing punch line** (one line that lands the takeaway on a high note).

Operational or cross-team signals usually do not belong in a skip-note about a person. If one genuinely matters to the manager, give it a single line. Otherwise leave it out and tell the user you trimmed it.

## Tone and formatting

**Write it for a three-minute read and a two-minute action.** Cut anything that does not earn its place. A skip-note that takes ten minutes to read does not get read. End with an action block the manager can start immediately.

**Rate of revelation: build, do not front-load.** Order the reveals by ascending importance so the note gains momentum as the manager reads. Save the most important or most exciting insight for near the end, then land the action. This is a deliberate departure from bottom-line-up-front. Use light signposts to escalate ("Then it got better", "Here is the part worth your attention"). Open with a scroll-stopping line, and if your opener is a question, replace it with a direct statement.

**Crisp writing.** Short sentences. Generous whitespace between beats so the manager can scan. Active voice. Specific over vague. No semicolons. No exclamation points. No em-dashes (use commas, colons, or parentheses). No padding words. Avoid clichés and AI-tells: skip "unlock", "elevate", "evolve", "game-changer", "thrive", "skyrocket", "secret weapon", "harness", and the like, and just describe the behavior plainly. Use numbered lists or bullets for steps, never "first, then, finally".

**House conventions.** Bold the value names. Italicize the behavior descriptions when calling out strengths or growth areas. Warm but factual: this is a colleague helping a colleague coach, not a corporate evaluation.

**Offer a tone variant.** After delivering, offer a more direct version and a warmer version, since the right calibration depends on the manager and the relationship. Default to warm and specific.

## A note on what does not belong here

If the conversation surfaced a real performance concern, a policy violation, or anything that warrants documentation or HR, a coaching note to the manager is the wrong vehicle. Flag it to the user plainly and point them at the right process (formal documentation, HR partner) rather than softening it into a development thread. Keeping those channels distinct protects both the report and the manager.
