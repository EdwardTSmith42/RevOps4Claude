---
name: os-editing/tone-profile
description: Profile the tone of a writing sample across 4 dimensions (Formal/Casual, Serious/Funny, Respectful/Irreverent, Matter-of-Fact/Enthusiastic). Output is a structured profile with scores 0-10 per dimension, 3 refined describers, 3 anti-tones, and 2-3 supporting passages quoted from the draft. Triggers when the user wants to know "what is the tone of this writing," "describe the voice," "score this for tone," or wants to compare the tone produced against a target tone. Do NOT trigger when the user wants edits suggested (use `suggest-edits`), prose rewritten (use `humanize`), or a quality assessment (use `assessment`).
---

# Mode — Tone Profile

Score and describe the tone of writing across the 4-dimensional tone framework. Produces a structured profile, not a list of edits.

## Purpose

The user wants to know what tone is coming through their writing — measured against orthogonal dimensions, with describers, anti-tones, and supporting passages from the draft itself. Useful for matching a target voice, calibrating brand tone, or diagnosing tone drift across a piece.

## When to use

- "What's the tone of this?"
- "Describe the voice in this piece"
- "Score this for tone"
- "Is this on-brand for [target voice]?"
- "Compare these two samples' tones"
- After a `humanize` to verify the rewrite preserved the original tone

## Inputs

- The writing sample (one piece is the typical input — if comparing two pieces, run the mode twice and present both profiles side-by-side)
- Optional: stated target tone (allows the mode to comment on whether the writing matches the target)
- Optional: stated context (publication, audience, brand voice goal)

## Run

1. **Read the entire sample.** Tone is visible across the whole piece, not in any one sentence.

2. **Make initial impressions on each of the 4 dimensions.** Reference `../references/tone-dimensions.md` for the framework: Formal/Casual, Serious/Funny, Respectful/Irreverent, Matter-of-Fact/Enthusiastic. Note where the writing lands on each axis.

3. **Refine the impressions.** Apply the calibration discipline:
   - **Default to mid-range scores.** Most writing isn't 10/10 on any dimension. A piece that scores 7 toward casual is more accurately profiled than one that scores 10.
   - **Reserve 9-10 and 0-1 for genuinely extreme cases** — and use them when warranted. Genuinely extreme writing (e.g., post-incident engineering reports, legal disclaimers, formal academic abstracts) CAN score in the 1-2 range on multiple dimensions, and that's accurate, not miscalibrated. The test: can you cite 2-3 supporting passages per dimension that show extremity on *that* axis specifically? If yes, the extreme is calibrated. If you're pulling the same one or two markers across multiple axes to justify multiple extremes, that's the failure mode the rule guards against. See `../references/tone-dimensions.md` "Calibration discipline" for the carve-out detail.
   - **Score on the writing as it reads, not the writer's intent.** If the writer says "I meant this to be funny" but the prose lands serious, score it serious.

4. **For each dimension, identify 2-3 supporting passages.** Quote 2-3 short verbatim spans from the draft that exemplify that dimension's reading. Without these, the profile is unfalsifiable — the user can't verify the score against the actual prose.

5. **For each dimension, write 3 refined describers.** Refined describers go beyond the dimension label. "Casual" is the dimension. "Conversational, lived-in, plainspoken" are the describers.

6. **For each dimension, write 3 anti-tones.** Anti-tones name what the writing is *not* — usually adjacent risks the writer has avoided. "Casual without being sloppy / lazy / too-familiar" sharpens the casual rating by exclusion.

7. **Name the profile.** A short, descriptive name (3-7 words) that captures how the dimensions interact. Examples: "Confident Mentor with a Crooked Smile" / "Brisk Industry Insider" / "Self-Effacing Storyteller, Quietly Sharp." This goes in the `## {profile name}` heading at the top of the output.

8. **(Optional) After the four dimensions, add a one-paragraph synthesis** describing how the dimensions interact. Particularly useful when dimensions combine into a recognizable archetype (see `../references/tone-dimensions.md` — "How dimensions interact"). Skip if the dimensions don't produce a coherent archetype.

## Output

Per `../templates/tone-profile-output.md`. Begins with `## {profile name}` and proceeds through the four dimensions with scores, describers, anti-tones, and supporting passages.

## Output discipline

- **No intro, no preamble.** Begin with `## {profile name}`.
- **Quote verbatim from the draft for supporting passages.** Don't paraphrase — exact text or it doesn't anchor.
- **Use mid-range scores** — extreme scores across multiple dimensions is a calibration failure, not a profile.
- **No conclusion or postamble** unless the optional synthesis paragraph is included.

## Cross-mode suggestions (postamble)

After the profile, optionally point at one adjacent next step in one short line that fits the actual reading. The typical next moves: when the profile names a tone the writer didn't intend, the structural lens in `suggest-edits` is usually the right corrective (tone drift is more often a function of evidence, framing, and pacing than of vocabulary); when the writer wants to push toward a different target tone, `humanize` with the target stated explicitly; when the writer wants a side-by-side comparison, run this mode on both samples and present both profiles. Skip the postamble if no next step is obvious.

## Design rationale

- **4 dimensions, not more.** Orthogonal enough to capture meaningful distinctions, few enough to keep the profile interpretable. (TBD why exactly four and not three or five — preserved as the framework's stated default.)
- **Mid-range scoring discipline** because extreme scores across multiple dimensions read as miscalibration. Most writing IS in the middle on most axes — that's the empirical pattern.
- **Anti-tones alongside tones** because defining what the writing is NOT sharpens the profile by exclusion. "Casual" is a wide band. "Casual without being sloppy" narrows it usefully.
- **Quote 2-3 supporting passages per dimension** because the abstract score is unfalsifiable without anchoring text. The user has to be able to look at the score, look at the quote, and verify the connection.
- **Profile name as a header** rather than just dimension scores because the name names the archetype the dimensions produce together — and that's often what the user actually wants to know ("is this writing 'trusted-friend-explaining-something-difficult' or 'late-night-show-monologue'?").

