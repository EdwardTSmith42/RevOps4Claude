# Writing Principles

Cross-mode principles for `writing`. Every mode loads or honors these. Stated here once so they don't get repeated in every mode file.

## Voice fidelity is the load-bearing constraint

A draft that's structurally sound but voice-generic reads as AI-produced and underperforms. The first thing every writing mode does is load a voiceprint via the library matching convention. By default, the user's scope-specific voiceprint matching the requested output format. Falling back to the user's general default voiceprint. Never falling back to "no voiceprint, write generically."

If no voiceprint matches and the user hasn't supplied one, writing surfaces the gap with the three options from the matching discipline (proceed without voice fidelity, supply sample text for on-the-fly voiceprint creation, point at a related voiceprint as substitute). The default behavior when no voiceprint exists is to ask, never to produce voice-generic prose.

When a voiceprint loads, the writing mode reads the `# Voiceprint` section (the portrait) — not the `# Analysis` section, which is the audit layer not meant for downstream consumption. The portrait teaches the voice. The mode writes within it.

## Specificity over generality

Vague prose is the most common writing failure. Writing modes prioritize concrete nouns, named examples, exact numbers, specific outcomes. The four-questions test (from `../../os-editing/references/edit-lenses.md` specificity lens) anchors this work — every piece of content should be able to answer:

1. Why read it?
2. What will they learn?
3. How will it help?
4. Why should they trust you?

If the brief or source material doesn't supply specifics, writing surfaces the gap rather than inventing fake specifics. A "10X your sales" promise without backing data is generic. The same claim becomes specific only when the brief supplies the underlying numbers — what the system actually does, by how much, validated against what evidence base — and the writing draws those numbers through to the prose.

When the user is iterating on a draft and the mode notices specificity gaps, the mode flags them rather than papering over with generic phrasing.

## The brief is the contract

What's promised in the brief is what gets produced. If the brief is unclear or ambiguous, writing asks rather than guessing. Producing the wrong piece because the brief was vague is wasted work.

When the user invokes writing without a brief on file, the mode asks for a quick brief inline — what's being made, for whom, why, any constraints. The brief doesn't have to be elaborate (a paragraph is often enough), but the mode needs the contract before producing.

When a saved brief exists in `os-inputs/briefs/current/` and the user references the project ("draft email 3 of the Black Friday campaign"), the mode loads the brief and proceeds. If the saved brief is missing constraints the mode would normally ask about, the mode surfaces the gap and asks before producing.

## Audience grounding

Prose calibrates to who's reading. Writing honors the audience profile from the brief — what the reader knows, what they want, what they're skeptical of, what they've already heard from competitors. A landing page for a warm-traffic audience works differently than a landing page for cold traffic. An email to a subscriber list works differently than a customer-service reply.

If the brief doesn't supply an audience profile, writing asks. "Customer email" without knowing whether the customer is a hot lead, a cold prospect, a long-term subscriber, or a churned-out alumnus produces generically-warm prose that lands wrong somewhere.

The audience grounding extends beyond demographic. What scares them about the alternative? What have they tried that didn't work? What do they want to be true? These are the prose-shaping signals — and they live in the brief or the audience artifacts the brief points at.

## Anti-AI-language calibrated to genre

The catalog at `../../_shared/references/ai-writing-patterns.md` is the editing skill's reference for AI-tells. Writing honors it during production rather than relying on editing to clean up after.

The calibration matters as much as the catalog. Direct-response copy keeps `!` for energy, em-dash asides, pain-triplet rhythm, sentence-starts with "And" / "But," signature voice with playful descriptors. Online prose for newsletters and blog posts uses conversational connectors instead of formal ones. Academic and technical prose follows its own conventions. Fiction stays out of scope (writing v0.1 doesn't produce fiction — that's a future fiction skill).

When the brief specifies a register that conflicts with default catalog rules, the brief wins. A direct-response email brief explicitly invites high-energy punctuation — the mode produces it. A formal academic abstract excludes that punctuation — the mode produces formal prose.

## Iteration is normal

A first pass is the starting point, not the final piece. Modes accept prior output and revision direction. The user iterates as the piece develops. Writing doesn't pretend one-shot work is enough.

The three iteration patterns (prior-output-plus-direction, batch-then-pick, section-targeted revision) live in `iteration-discipline.md`. Modes apply them transparently — the user supplies what they want changed, the mode revises in that direction without re-doing the whole piece.

Whether iteration materially improves output is a question for measurement, not assertion. Modes are built to support iteration without enforcing how many passes to run.

## Restraint over thoroughness

A draft that feels thorough often reads as bloated. Writing modes don't pad to feel comprehensive — they produce the shape the brief calls for and stop. Hook batteries don't auto-extend to 12 hooks when 5 are clearly enough. Landing pages don't pad sections beyond what the audience needs.

When a section is short because the substance is short, that's the right answer. The mode notes any section that felt thin so the user can decide whether to expand it (with more brief detail) or trust that it's tight rather than thin.

## Source material vs. references

The mode distinguishes between source material (what the piece is *about* — research, transcripts, customer quotes, topic notes) and references (voiceprint, style samples, templates, briefs — what shapes the piece without supplying its substance).

Source material is the substantive input. The piece draws claims, evidence, and content from it. Source material is project-specific and lives wherever the user puts it (inline supply, attached file, link).

References shape the piece without supplying its content. A voiceprint teaches the voice but doesn't tell the piece what to argue. A template teaches the structure but doesn't fill in the sections. A brief sets the contract but doesn't write the prose.

Mixing source material and references confuses production. Source material from another author supplies substance, not voice; use the voiceprint rather than cloning it. When the source is the writer's own interview, transcript, or notes, treat distinctive wording as voice-bearing material too — preserve their specific phrases where they strengthen the draft instead of reflexively paraphrasing them. A draft that pulls structure from the brief instead of from a template produces structure that wasn't validated. Writing keeps the streams separate and consumes each appropriately.

## Don't write the wrong piece

The single biggest writing failure isn't bad prose — it's good prose for the wrong piece. A polished landing page for the wrong audience, a beautiful email in the wrong sequence position, a sharp hook for a piece that needed a different opener.

Before producing, the mode confirms the basics: what's being made, for whom, what comes before and after (for sequences and chained pieces), what the piece needs to accomplish. If any of those is unclear, ask before producing. The cost of asking is one round-trip. The cost of producing the wrong piece is the entire production cycle.
