# Problem Promise Paragraph (PPP) — cross-mode template

The PPP is a canonical 7-beat offer-messaging format. Applied specifically to the offer context (not to general positioning), used as a building block by multiple offer modes and loadable as a standalone template.

The underlying narrative structure is the same as the Value Articulation Story in `../../_shared/references/positioning-concepts.md` (Most / And that's a problem because / Because of that / Which means / On the other hand / So that / And consequently). This template specializes the story arc for offer messaging — used in VSLs, landing pages, launch emails, ad copy.

## Shape

```markdown
# Problem Promise Paragraph — [Offer Name]

---

**Most** [target audience] [current struggle or approach — what most of them are doing that isn't working].

**And that's a problem because** [why the current approach fails — specific, not generic].

**Because of that,** [negative consequences — what happens as a result of the failure].

**Which means** [emotional or practical impact — how the consequences show up in the audience's day-to-day].

**On the other hand,** [your different approach — the unique mechanism or vehicle introduced here, using its named form].

**So that** [immediate benefits — what changes right away when the audience adopts the approach].

**And consequently,** [ultimate transformation — the identity-level shift or compounded outcome over time].

**Which means you're not just** [addressing the problem] **but** [reinforcing the ultimate benefit and identity shift].

---

*Optional closing line: a one-sentence summary of the arc that can be pulled out as a hook or headline.*
```

## Usage pattern

The PPP has eight beats (the 7-beat Value Articulation Story + a closing "Which means you're not just X, but Y" identity-shift reinforcement unique to offer messaging).

Each beat is a single sentence. Together they form a belief-shifting arc that:

1. **Opens with the prospect's current state** (what most are doing)
2. **Diagnoses the failure** (why that's a problem)
3. **Names the consequence** (what follows)
4. **Surfaces the emotional reality** (how it feels)
5. **Introduces the offer / mechanism** (the contrast)
6. **Promises immediate benefits** (the short-term lift)
7. **Projects the transformation** (the long-term identity shift)
8. **Seals the identity reframe** (reinforce the shift)

The format is structured enough to be learnable and replicable, flexible enough to adapt to different niches.

## When to use

- **Inside `os-offer/modes/offer-vehicle`** — the PPP is often the "Differentiated Positioning" section's narrative form.
- **Inside `os-offer/modes/unique-mechanism`** — the PPP drafts the Enemy / Old-Way Takedown section of the 75/25 campaign (beats 1-4) and hints at the Mechanism Reveal + Future-Pace (beats 5-7-8).
- **As a standalone template** — when the user already has a vehicle or offer and wants the PPP directly for ad copy, launch emails, or sales page headers.
- **Requested after other modes** — a natural chain move after any offer mode completes.

## Example (from NTPV Designer's fitness offer)

```markdown
**Most** busy business owners and high-performing professionals are trying to get in shape using the same cookie-cutter fitness approaches designed for college kids and unemployed gym rats.

**And that's a problem because** these generic programs completely ignore your reality — demanding 6-day workout schedules, eliminating entire food groups, and treating your body like it doesn't have a demanding career, social obligations, and a life outside the gym.

**Because of that,** you end up triggering your body's survival mechanisms through over-training and under-eating, which slows your metabolism to a crawl and makes your body desperately cling to every ounce of fat.

**Which means** you're stuck in an endless cycle of short-term wins followed by devastating rebounds, feeling frustrated that despite your success in business, you can't crack the code on your own body — constantly hungry, exhausted, and further from your goals than when you started.

**On the other hand,** what we do with our Metabolic Reset Method is flip everything you've been taught on its head and work WITH your body's natural intelligence instead of against it. We dive deep into your unique metabolism, lifestyle demands, and professional reality, crafting a personalized strategy that has you eating more food than ever while training just 2-3 days per week — all while systematically reversing the metabolic suppression that's been sabotaging your results.

**So that** you can finally build that lean, muscular, ab-defined physique without sacrificing your career success, social life, or sanity — eating foods you actually enjoy and training in a way that energizes rather than exhausts you.

**And consequently,** you'll become the high-performer who has it all — the successful business AND the body to match — walking into every boardroom and social event with unshakeable confidence, knowing you've mastered both your professional and physical domains in a way that's sustainable for life.

**Which means you're not just** losing weight **but** stepping into an identity of total-life-mastery that compounds across every domain you care about.
```

## Key rules

- **Use the exact 7-beat transition language.** "Most / And that's a problem because / Because of that / Which means / On the other hand / So that / And consequently" carries the rhythm. Paraphrasing dilutes it.
- **The 8th beat ("Which means you're not just X, but Y") is the offer-messaging extension.** Positioning-only uses of the Value Articulation Story in `_shared/references/positioning-concepts.md` stop at 7 beats. Offer messaging benefits from the explicit identity-shift reinforcement that the 8th beat provides.
- **Each beat is one sentence.** Compressed or expanded beats break the rhythm. Multiple sentences in the "On the other hand" beat (introducing the mechanism) are acceptable when the mechanism needs explanation — see the fitness example above.
- **If the user provides a name for the offer or vehicle, use that name.** Don't invent a new name mid-PPP. Source-stated constraint.
- **Mirror the user's voice and language.** Same discipline as positioning work. Strip generic business-speak. Preserve specific phrasings from the audience's or the practitioner's own voice.
- **Ground in specifics, not generalities.** *"Most business owners struggle with marketing"* is too generic. *"Most SaaS founders at $500K–$5M ARR are running a patchwork of freelancers and agencies that deliver inconsistent results"* lands.

## Cross-references

- **`../../_shared/references/positioning-concepts.md`** — the underlying 7-beat Value Articulation Story. The PPP is the offer-specific specialization of that same narrative structure.
- **`../references/vehicle-theory.md`** — the "On the other hand" beat introduces the Vehicle. This is where the Vehicle name gets its first public utterance in the PPP format.
- **`../references/unique-mechanism-playbook.md`** — the PPP's Enemy Takedown (beats 1-4) is the compressed form of the 75/25 campaign's enemy/old-way section.

## Grounding check before shipping

1. Does the PPP use the exact 7-beat transition language?
2. Is the 8th beat ("Which means you're not just X, but Y") present with an identity-shift reinforcement?
3. Is each beat a single sentence (except "On the other hand" when the mechanism needs a sentence of explanation)?
4. Does the PPP name the unique mechanism using the user-provided name (or the mode's output), not invent a new one?
5. Is the opening specific enough that a reader in the target audience recognizes themselves immediately?
6. Does the closing beat reinforce an identity shift, not just an outcome?
