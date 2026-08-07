# Mode: extract-template

Part of the `os-content-template` skill. Selected when the user pastes a post and wants the structure abstracted into a reusable template.

## Job

Take a specific piece of content and produce a generalized template — the same rhetorical spine with `[ALL CAPS]` slot variables replacing the specifics — that another creator could use to produce their own version without plagiarism. Maintain the rhetorical rhythm and punch even as the content is abstracted.

## Run

Six-step process. Order matters: do not skip ahead.

1. **Cold Read** — Silently skim the post once to feel the emotional beat. Notice rhythm, tension points, the payoff.
2. **Highlight Repetition** — Mentally mark every line that shares a structural twin. Repeated syntactic forms are the spine of most effective short-form writing.
3. **Label the Slots** — Turn concrete content elements into `[ALL CAPS]` variables. Examples: `[CREDENTIAL]`, `[RESULT]`, `[TITLE/ROLE]`, `[EMOTIONAL STATE]`, `[INDUSTRY]`. Be specific enough that the slot name is self-explanatory when someone fills it.
4. **Surface the Spine** — Rewrite each exemplar line with placeholders. Preserve sentence length, contrast structure, punctuation rhythm. `I'm not a [CREDENTIAL], but [RESULT WITHOUT IT]` must feel like the original did.
5. **Group Supporting Lines** — Collect the sentences that frame or support the spine (setup, rising action, turn). Abstract them as needed, but preserve the sequence.
6. **Simplify CTA** — Boil the closing climax into one transformative action anyone can take. The CTA is often the hardest slot to abstract because it's the author's POV. Push for a template that still makes the reader *do something specific*, not "reflect on life."

After the six steps: give the template a distinctive name of 3–6 words (e.g., "The Credential Flip," "Permission-Not-Required Spine") that signals what it's for.

## Output

The deliverable is the template itself, formatted so a creator can copy it directly into their writing tool and start filling slots. The template body is plain text — no surrounding code fence — because code fences add friction when the next step is editing inline. Cross-mode pointers and your own commentary live in the message *around* the template, not appended to it; the boundary between *the template the user pastes* and *meta-information about the template* is real, and a postamble inside the pasteable block contaminates the paste.

The shape:

```markdown
# <a name 3-6 words long that signals what this template is for — e.g., what move it makes or what feeling it produces, not a generic label like "Template 1">

<the template body, line by line, with [ALL CAPS] slots wherever a specific has been abstracted; preserve the source's line breaks, sentence lengths, and punctuation rhythm exactly>

<closing CTA line, with the action slot named clearly enough that a filler knows it must be a concrete action and not a reflective platitude>
```

Rules — each one is here because of a specific failure mode worth naming:

- **Slot names describe the *role* in the structure, not the surface content of the source.** A slot called `[AI-FOUNDER-CREDENTIAL]` traps the template in one industry; the same slot as `[CREDENTIAL]` or `[TRADITIONAL QUALIFIER]` makes it portable. If the slot name reads back as "this was clearly from a post about X," abstract it one level up.
- **Rhetorical rhythm survives the abstraction.** Short sentences stay short. Contrast clauses keep their contrast. Lists keep their length. The template is a skeleton, not a paraphrase — when a creator fills the slots, the resulting post should feel like it was *written*, not assembled. If a slotted version reads flatter than the original, the abstraction went too generic; tighten the slot names or the rhythm and try again.
- **The CTA names an action, not a reflection.** "Reflect on what qualified means to you" is not a CTA; "Build one piece of work this week that proves the credential you don't have" is. The CTA slot is the hardest to abstract well because the author's specific POV is what made the original CTA land — the move is to preserve the *demand for concrete action*, even when the action itself becomes a slot.
- **The template is far enough from the source that a filled version isn't plagiarism-adjacent.** If swapping one or two words would reproduce the original post almost verbatim, the abstraction didn't do its job. The test: could a creator in a completely different niche fill this template and have it read as original work? If no, abstract further.

## Design Rationale

- **Six-step order** — cold read before abstraction, find repetition before labeling slots, slots before spine, spine before supporting lines, CTA last because it's hardest. Skipping straight to label-the-slots produces wrong-level abstractions because the slot-namer hasn't yet felt where the rhythm lives.
- **`[ALL CAPS]` slots** — visually distinct from prose, impossible to mistake for template body, trivial for a filler to find-and-replace. The convention matters more than the specific choice; what matters is that filled vs unfilled state is unmistakable at a glance.
- **Name in 3–6 words** — long enough to be memorable and to signal the template's move ("The Credential Flip" tells you what it does); short enough to be searchable in a growing template library. Generic names like "Template 1" or "LinkedIn Post Template" defeat the purpose.
- **Plain text template body, not a code block** — creators edit directly in their tool of choice. Code-block formatting forces them to strip the fences before they can work with the template.
