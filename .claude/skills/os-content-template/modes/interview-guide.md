# Mode: interview-guide

Part of the `os-content-template` skill. Selected when the user has a template (or source post) and needs a ghostwriter-style interview guide to elicit the raw material from a client.

## Job

Produce an interview guide that a ghostwriter (or the user themselves) can use to surface the specific details, stories, and reframes needed to fill the template for a particular person. The role is *part therapist, part journalist, part creative director* — behind-the-scenes documentary work that produces the material for the final post.

## Run

1. **Start from the template.** If a template exists (produced by `extract-template` mode), build the interview around its slots. Every slot should correspond to at least one question; the make-or-break slots (the ones whose specificity decides the filled post) may take two or three different framings.
2. **Set the high-level objective.** One sentence at the top of the guide naming what the interview is *really* trying to surface — the underlying reveal, not the surface topic. A clear objective at the top keeps the interviewer oriented when the conversation drifts.
3. **Write questions that feel like conversation, not a questionnaire.** A short main question, then two to four softer follow-up prompts underneath, framed casually. If a question could appear unchanged on a job application form, rewrite it until it sounds like something a thoughtful friend would actually ask.
4. **Surface tension first, specifics second, reframes last.** Order matters. A ghostwriter interview starts by finding the emotional charge (the absence, the gap, the thing the interviewee feels they shouldn't have done), then gets concrete (what they actually did anyway, who paid them, what worked), then invites the interviewee to articulate their own reframe (their current POV on what makes someone qualified / valuable / legitimate in this domain). Inverting this order — leading with reframes — produces sanitized answers that miss the raw material.
5. **Include a small "for instance" cluster under questions where clients tend to default to abstractions.** Two or three short concrete openers in the interviewee's voice, framed as a tonal aim rather than as scripts to read aloud. The aim is to anchor what kind of *texture* a strong answer has — specific people, specific moments, specific numbers — without putting words in the interviewer's mouth. Don't include these under every question; reserve them for the questions where, in practice, interviewees reach for generalities ("I just work hard," "I'm passionate about people") instead of the textured answer the template needs.
6. **Close with an interview summary.** A compact numbered list of the questions in their cleanest form, one line each — the cheat-sheet the interviewer glances at during the conversation when they need to remember what's left.

## Output

Markdown. Structure the guide so the interviewer can read it once beforehand and skim the summary during the call. Don't append cross-mode pointers or audit commentary to the guide itself; the guide is a document the interviewer hands forward, and any meta-information belongs in the message *around* the guide, not inside it.

The shape:

```markdown
# Interview Guide: <template name, matching the extract-template output if one exists>

**High Level Objective:** <one sentence naming what the interview is trying to surface — the underlying reveal, not the surface topic>

## Questions

---

### 1. <main question in conversational form, opening the emotional terrain the interview needs to enter; ends with a question mark>
- <a softer reframing that gives a hesitant interviewee a second entry point>
- <a specific-anchor follow-up that pulls toward a concrete moment or person>
- <a permission-giving follow-up that signals it's safe to admit the awkward version>

> For instance — answers in this range:
> *<a short, specific, textured opener in the interviewee's likely voice — names a person, a result, or a moment, not a category>*
> *<a second opener that ranges in a different direction so the interviewee doesn't latch onto the first as a script>*

---

### 2. <main question 2 — moves from tension toward specifics>
- <follow-ups in the same shape>

---

<continue for 5–8 main questions total, moving across the tension → specifics → reframes arc>

---

## Interview Summary

<numbered list of the questions in their cleanest one-line form, suitable for at-a-glance reference during the call>
```

Tone rules:

- Casual, warm, second-person. The guide should read like a thoughtful collaborator's notes, not an HR intake form.
- No corporate-questionnaire phrasing. If a question sounds like a survey, rewrite until it sounds like something said across a coffee table.
- Questions invite vulnerability without demanding it. Give the interviewee room to pivot to a different angle without losing face.

## Design Rationale

- **Part therapist, part journalist, part creative director** — the three roles cover the three things the interview needs to do: create safety (therapist), elicit specifics (journalist), shape what matters (creative director). A guide that's only one of the three produces lopsided material — pure therapy yields catharsis without usable copy; pure journalism yields facts without emotional charge; pure creative direction yields polish without depth.
- **"For instance" clusters under questions that need them, not under every question** — interviewees default to generalities when asked open questions, so a concrete anchor helps. But over-anchoring trains the interviewee to match the anchor's shape, narrowing the range of answers. The discipline is to use anchors where they unlock specificity and skip them where the question already invites concrete answers naturally.
- **Tension → specifics → reframes order** — the emotional charge has to surface first, or the specifics that follow will be sanitized. The reframe comes last because the interviewee can only articulate "what does qualified mean to me now" honestly after they've already named the gap and the work that filled it. Inverting the order produces a guide that asks for conclusions before evidence.
- **Two artifacts at different densities** — the guide itself is the prep document the interviewer reads beforehand; the summary is the cheat-sheet they glance at during the call. Same content, different use-moments, different density.
- **Written like a conversation** — formal questioning shuts down the vulnerability the interview needs. A casual register invites honesty, and honesty is the raw material the template needs to come alive.
