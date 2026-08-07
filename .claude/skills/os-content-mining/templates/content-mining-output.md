# Template: content-mining-output

Canonical shape for `content-mining` outputs. Markdown.

**Follow the density, not the template.** The six sections are containers, not quotas. A source concentrates its value unevenly — mine hardest where the material is rich and go deeper there than the section skeleton implies, and leave a section sparse or empty where the source is thin. An empty section with one line ("the source doesn't work in frameworks") is a correct output; a padded one is a defect. Never invent an entry to fill a slot — a weak area dressed up to average dilutes the strong material it sits next to.

```markdown
# [Brief descriptive title drawing from source's domain]

## 1. Golden Nugget Insights

**[Insight 1 — stand-alone articulation]**
- [Expansion / why it's a nugget / 1–3 bullets]

**[Insight 2]**
- [...]

...

## 2. Answered & Implied Questions

### Directly answered

- **Q:** [Clean audience-facing question]
  **A:** [Source's answer, compressed]

- **Q:** [...]
  **A:** [...]

### Indirectly answered

- **Q:** [Question the source implies through examples or framing]
  **A:** [Derived answer, flagged as inferred]

## 3. Frameworks, Models, and Workflows

### [Descriptive framework name 1]
- **What it is:** [One-line definition]
- **Inputs:** [What it takes]
- **Outputs:** [What it produces]
- **When to use:** [Conditions]
- **Steps / structure:** [If applicable]

### [Descriptive framework name 2]
- [...]

## 4. Sound Bites & Sharp Reframes

A handful of quoted or near-quoted lines from the source that compress meaning, flip a belief, or land a metaphor cleanly enough to stand alone outside the original context. Render each on its own line as an italicized quotation. The failure mode is filler: lines that sound quotable in context but don't carry weight stripped of it. If a candidate sound bite doesn't survive removal from the surrounding paragraph, cut it.

## 5. Content Angle & Concept List (Clustered)

### Education
- **[Angle]** — [Format tag from content-format-taxonomy.md]
- **[Angle]** — [Format tag]

### Persuasion
- **[Angle]** — [Format tag]
- **[Angle]** — [Format tag]

### Authority
- [...]

### Narrative
- [...]

### Tactical
- [...]

## 6. Expansion & Repurposing Paths

### [Primitive or angle to expand]
- **Short-form:** [How this becomes a post or thread]
- **Long-form:** [How this becomes an essay or video]
- **Email sequence:** [How this becomes a multi-part series]
- **Framework explainer / mini-lesson:** [If applicable]
- **Laddering:** [Which other primitives this could chain into]

### [Next primitive or angle]
- [...]
```

## Rules

- **Extraction stays source-faithful.** Nuggets, answers, frameworks, and sound bites must trace back to the source.
- **Generated concepts follow the source's intended role.** If the source is a catalyst, Sections 5–6 must make sense without it and add the writer's own contribution. If the source is the subject or evidence, keep it visible where the content depends on it.
- **Distinguish the writer's material from external material.** Preserve genuine first-party language and experience; do not invent personal experience to make an external idea feel owned.
- **Every framework is named descriptively.** No cutesy names. One strong framework — or none — beats three padded ones; the section header is plural, the source decides the count.
- **Populate where the source is strong; leave it sparse where it isn't.** If all angles fall into one cluster, take one honest second look at the others — then let the skew stand if that's genuinely where the source lives. A dominant cluster is a finding about the source, not a defect in the extraction.
- **Expansion paths are format-agnostic.** Don't lock to TikTok / LinkedIn / etc. The user picks the channel.
- **Bias toward depth where the value is dense.** Per source rules: explain yourself, define uncommon terms, assume reader is unfamiliar with source. Depth means pushing the strong material further — never stretching thin material longer.

## Pasteable output

The filled-in version of this template is the artifact the user pastes forward into downstream content work — into a CMS, into the next mining run for cross-source comparison, into a hand-off to an editor or a repurposing skill. Render the output so it's clean to copy: no meta-commentary around the document ("here is your content map…"), no preamble framing the deliverable, no closing remarks about what you produced. The headed markdown document is the response.

Honesty about coverage belongs *inside* the document, not around it: a sparse section carries its own one-line note ("the source doesn't work in frameworks"), and if the QC pass has something material to say about where the source's value concentrated, it goes in a short **Coverage notes** section at the end of the document — part of the artifact, pasteable with it.
