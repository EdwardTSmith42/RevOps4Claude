---
name: os-writing/email-sequence
description: Draft a multi-piece email campaign — welcome sequence, nurture flow, sales / launch sequence, re-engagement push, or other multi-piece arc. Produces the full sequence with cadence notes, narrative arc across pieces, and sequence-level voice consistency. Triggers on "draft a 7-day welcome sequence," "write the Black Friday email push," "I need a 5-email nurture flow." Do NOT trigger when the user wants a single email (use `email`) or only the sequence outline / strategy (run a brief in `os-inputs/briefs/` first).
---

# Mode — Email Sequence

Multi-piece email campaign writing. Produces a full sequence calibrated to the campaign type, cadence, and audience. Each individual email follows the email-anatomy from `../references/email-anatomy.md`. The sequence-level architecture (cadence, arc, opener variety, internal consistency) lives in `../references/sequence-architecture.md`.

## When to use

The user is producing a multi-piece email campaign. Common triggers: "draft the 7-email welcome sequence," "I need 9 emails for the Black Friday push," "write a 5-email nurture flow about X," "draft the re-engagement sequence for inactive subscribers."

If the user wants a single email (even one that's part of a sequence), `email` is the better mode. If the user wants to plan a sequence at the strategy level (audience profiling, offer architecture, sequence arc design) before producing, that's brief / planning work — produce the brief first, then come back here.

## Inputs

The mode loads references via the library convention (`../references/library-loading.md`):

**Required:** What the campaign is about. The offer (for sales sequences), the welcome context (for welcome sequences), the topic arc (for nurture flows). Either inline or via the brief.

**Required (or asked):** Sequence type. Welcome, nurture, sales / launch, re-engagement, cart-abandonment, or other. Different types have different cadence and arc conventions from `../references/sequence-architecture.md`.

**Required (or asked):** Length and cadence. How many emails, sent over what period, on what days. Welcome sequences typically 4-7 emails over 1-2 weeks. Sales sequences typically 5-12 emails over 7-14 days. The brief specifies. If missing, the mode asks.

**Required (or asked):** Audience and goal. Who's receiving the sequence, what state they're in (new subscriber, engaged reader, decided-not-yet-bought), what action the sequence drives toward.

**Loaded from library:** Voiceprint, loaded once and used across all pieces in the sequence. When pieces switch authors mid-sequence (a co-authored campaign where one writer handles the opening emails and another handles the close, for instance), the mode loads multiple voiceprints and tracks which piece uses which. Style samples if the campaign has signature patterns. Template if a proven template exists for this campaign type. Brief from `os-inputs/briefs/current/`.

**Optional:** Specific structural preferences. The user can specify "email 1 should open with a story, email 4 should be the social proof email, email 8 should be the deadline-tonight email" if they have a planned arc. When supplied, the mode honors it. When not, the mode produces the arc per the campaign-type conventions.

## Run

The procedure runs through five stages.

**Stage 1: Read the brief and confirm the contract.** The mode reads the brief, identifies the sequence type, confirms cadence and length, identifies the audience and goal. If anything is ambiguous, the mode asks before producing. A wrong-shape sequence is expensive to rework.

**Stage 2: Load references and plan the arc.** Apply the library-loading convention. With the references loaded, the mode plans the sequence's narrative arc: what each email's role is in the campaign. For a sales sequence, the typical arc moves through announcement, value-and-context, social proof, objection handling, urgency-and-deadline, final close. For a welcome sequence: introduction, first useful insight, deeper context, optional offer toward the end. The mode surfaces the planned arc to the user before producing — naming each email's intended role and the overall progression, then asking for confirmation or adjustment. This is a checkpoint: a wrong arc planned now costs one round-trip; a wrong arc discovered after production costs the whole sequence.

**Stage 3: Produce each email in turn.** With the arc approved, produce the emails one at a time. Each email follows the per-email procedure from `email.md`: subject, opener, body, close, optional PS. Each email loads the voiceprint and writes within it. Each email's role in the arc shapes its content (announcement emails open differently from urgency emails).

**Stage 4: Sequence-level review.** After all emails are produced, run a sequence-level review per `../references/sequence-architecture.md`:
- **Cadence check:** does the per-email send timing fit the brief?
- **Arc check:** does the sequence carry the reader through the planned progression?
- **Opener variety:** do the openers vary across emails, or do multiple emails open identically?
- **Internal consistency:** do voice, key claims, offer specifics, and CTA destinations stay consistent across pieces?

The review surfaces any issues without blocking delivery. The user sees the issues alongside the sequence and can request targeted revisions.

**Stage 5: Deliver the sequence.** Present each email with its position in the sequence and any per-email cadence notes ("send Day 1, 9am" / "send Day 4, 2pm"). The user has the full sequence to review before scheduling.

## Output

The full sequence, structured with each email labeled by its position and send-day:

```
## Sequence: <campaign name>

**References loaded:**
- Voiceprint: <name>
- Brief: <brief filename>
- Style samples: <list>
- Cadence: <X emails over Y days>
- Arc: <planned progression>

---

### Email 1 — Day 1, <description of role>
**Subject:** [Subject line]

[Email body]

PS [if applicable]

---

### Email 2 — Day 3, <description of role>
[etc.]

---

[All emails in sequence]

---

## Sequence-level review

**Cadence:** [confirmed / flagged]
**Arc:** [confirmed / flagged]
**Opener variety:** [observations]
**Internal consistency:** [observations on voice, claims, offer specifics, CTA destinations]

**Notes for the user:** [any issues worth a follow-up revision]
```

## Output discipline

The sequence delivers as a unit. Each email is complete (subject, opener, body, close, PS if applicable). The sequence-level review is appended after all emails so the user can see the production quality and any flagged items.

No preamble before the sequence. Reference-loaded note opens, sequence follows, review closes.

The mode honors per-email length conventions from `email-anatomy.md`. A sales sequence email isn't 800 words because the arc says so. If the substance is 200 words, the email is 200 words. Padding to feel "complete" produces emails readers skip.

Voice consistency is non-negotiable. If the sequence loads multiple voiceprints (a co-authored campaign with the writer-switch named in the brief), each piece is in the right voice and the writer-switch is intentional, not accidental. If voice drifts unintentionally across pieces by the same writer, the sequence-level review flags it.

## Iteration

The mode supports section-targeted revision (per `../references/iteration-discipline.md` pattern 3): "Revise email 4," "rewrite the close email," "swap email 2's opener for a story-opener." The mode produces a replacement for the named email while preserving the surrounding sequence and the campaign's voice and arc.

The mode also supports prior-output-plus-direction at the sequence level: "Tighten the whole sequence by 15%," "make the urgency emails (7-9) more direct," "add objection-handling to email 5." The mode revises in the direction supplied while preserving the campaign's overall structure.

Batch-then-pick at the email level (multiple variants of email 4 to compare) is supported but typically belongs in `email` mode rather than `email-sequence` — call `email` directly for the variant production, then bring the picked one back into the sequence.

## Cross-mode suggestions

After a sequence, the natural next steps depend on what comes next. For a unit-level quality pass before scheduling, `os-editing/assessment` in multi-piece campaign mode scores the campaign as a whole. For targeted revision of specific emails, invoke this mode again with section-targeted revision. For verification that the sequence matches the brief's audience profile and goal, re-read the brief alongside the sequence and surface any drift.

Pick the one that fits; don't enumerate all three.
