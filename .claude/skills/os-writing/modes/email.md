---
name: os-writing/email
description: Draft a single-piece email — subject line, opener, body, close, optional PS. Handles direct-response sales, customer emails, newsletter issues, pitch / outreach, and most one-off email formats. Triggers on "draft an email," "write the PS for this," "draft a customer email about X." Do NOT trigger when the user wants a multi-piece sequence (use `email-sequence`) or when the user wants only the subject lines or hooks (use `hooks`).
---

# Mode — Email

Single-piece email writing. Produces a complete email with subject, opener, body, close, and optional PS — calibrated to the email type from the brief. Email anatomy and section-by-section calibrations live in `../references/email-anatomy.md`.

## When to use

The user is producing one email. Common triggers: "draft an email to subscribers about X," "write the customer email responding to Y," "draft this week's newsletter on Z," "give me a pitch email to send Q." If the user is producing a multi-piece sequence (welcome flow, sales push, nurture campaign), `email-sequence` is the right mode.

The mode handles all common email types: direct-response sales, welcome / nurture, customer service replies, newsletter issues, pitch / outreach. The email type is part of the brief and shapes how the email composes.

## Inputs

The mode loads references via the library convention (`../references/library-loading.md`):

**Required:** What the email is about. Substance, key claims, CTA destination if any. Either inline or via the brief.

**Required (or asked):** What email type. Sales, welcome, customer reply, newsletter, pitch, etc. Different types have different shape calibrations from `../references/email-anatomy.md`. If unclear, the mode asks.

**Required (or asked):** Audience. Who's receiving this email. A subscriber? A customer? A cold prospect? A long-term reader? The audience grounding shapes voice, length, and CTA strength.

**Loaded from library:** Voiceprint at scope matching the type — a customer-email scope for customer / welcome / nurture, the general or social-media scope for direct-response sales (calibrate to the user's actual register), the longform scope for newsletter issues. Style samples if any apply — a rhythm-shaped sample for direct-response, a personal-anecdote-opener sample for newsletters, a clarity sample for customer replies. Template if a relevant one exists.

**Optional:** Stated CTA. If the user is producing a sales or marketing email, the CTA destination should be in the brief. If not, the mode asks rather than fabricating.

**Optional:** Subject-line constraint. Some campaigns have subject conventions (preview text constraints, A/B variants). The mode honors them.

## Run

The procedure runs through six steps.

**Step 1: Read the brief and substance.** What's being said. Who's reading. What action the email expects. What the opener-to-CTA arc looks like.

**Step 2: Load references.** Apply the library-loading convention to find voiceprint, style samples, template, brief. Surface what's loaded so the user has audit trail.

**Step 3: Identify the email type and shape.** Map to one of the email types in `../references/email-anatomy.md`. Confirm with the user if the brief is ambiguous.

**Step 4: Produce the subject line.** Specific, in voice, length-appropriate. For campaign emails, the subject often previews the body's specific angle. For customer emails, the subject names the request directly. For newsletters, the subject teases the issue's central insight.

**Step 5: Produce the body.** Opener honors the email-type shape conventions (story opener for newsletter, urgency setup for sales late-position, warm acknowledgment for customer reply). Body delivers substance in the shape and length the type calls for. Close handles the CTA or the last-impression beat.

**Step 6: Produce the PS if applicable.** Direct-response emails almost always carry a PS. Customer emails and most newsletters skip it. Use the PS to reinforce, name urgency, or surface objection-handling — never as a place to dump leftover content.

The mode runs the era-tells / anti-AI-language pass during production rather than relying on editing. Catalog at `../../_shared/references/ai-writing-patterns.md`. Genre carve-outs apply per email type: direct-response keeps `!` and pain-triplet rhythm, customer email follows online-prose conventions, newsletter follows online-prose conventions.

## Output

The full email, structured:

```
**Subject:** [Subject line]

[Opener]

[Body]

[Close / CTA]

[Signature]

PS [if applicable]
```

Brief reference-loaded note before the email so the user can see what informed it. The shape:

```
**References loaded:**
- Voiceprint: <slug used>
- Brief: <brief slug, with status if relevant>
- Style sample: <author>/<pattern> (if any matched)
- Email type: <type, plus sequence position if applicable>

[Email follows]
```

The block names what shaped the work; it doesn't recite a template. If a field doesn't apply (no brief on file, no style sample matched), the field is omitted rather than left empty.

## Output discipline

No preamble before the email. The reference-loaded note (when used) is short and scannable. The email itself starts with `**Subject:**` and ends with the PS or signature.

The mode never produces a generic email when references are missing. If the voiceprint hasn't been loaded, the mode follows the graceful-degradation flow before producing — surfaces the gap, offers the three options, doesn't silently produce voice-generic prose.

The mode honors email-type length conventions. A direct-response sales email at 600 words is too long — the mode flags the length and offers to compress. A customer-service reply at 50 words may be too short for the substance — the mode flags and asks whether to expand.

The mode does not pad. If the substance is short, the email is short. Filler to feel "complete" produces emails the reader notices as filler.

## Iteration

The mode supports the iteration patterns from `../references/iteration-discipline.md`:

**Prior-output-plus-direction:** "Tighten the body by 30%," "rewrite the subject line, less curiosity-gap, more specific," "add objection-handling for the price concern." The mode produces a revised version that incorporates the change while preserving the rest.

**Batch-then-pick (subject lines specifically):** "Give me 5 subject-line options for this email." The mode produces variants spanning different shapes — curiosity gap, specific result, stakes raise, pattern interrupt, direct-claim. The user picks. The mode uses the chosen subject in the next iteration.

**Section-targeted revision:** "Rewrite the close — make it more direct," "swap the opener for a story-opener," "rework the PS to handle the deadline objection." The mode produces a replacement for the named section, preserving the rest.

## Cross-mode suggestions

After an email, the most likely next step depends on what the user needs. For a quality check before sending, `os-editing/assessment` returns a score and verdict. For length concerns, `os-editing/shorten` compresses without losing voice. For AI-tell cleanup the production didn't catch, `os-editing/humanize` is the right tool. For the next email in an ongoing campaign, switch to `email-sequence` and load the campaign brief.

Suggest the one that fits; don't recite all four after every email.
