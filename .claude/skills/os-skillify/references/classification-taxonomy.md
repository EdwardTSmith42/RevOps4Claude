# Classification Taxonomy

Every chunk of a legacy prompt falls into one of six categories. When a chunk spans categories (common), tag it with the primary category and add a note.

## 1. Trigger / framing

**What it is:** The part of the prompt that establishes what the job is, who it's for, and when it applies. Includes role statements, task declarations, context about intended use.

**Where it goes:** SKILL.md — the `description` frontmatter (trigger language) and the "When to use" / "Purpose" sections.

**Typical shapes:** opening lines that declare a job ("You are tasked with generating…"), capability statements ("You analyze written text and create…"), or role + specialty framings ("You are an AI copy editor who specializes in…").

**Gotcha:** The role statement often contains both genuine framing ("AI copy editor") and ego-puffery ("genius level"). Keep the framing, drop the puffery.

## 2. Craft moves

**What it is:** Specific phrasings, sequences, or directives that shape output quality in ways that are non-obvious and tuned through experience. These are the moves that make one prompt produce noticeably better output than a naive version of the same ask.

**Where it goes:** Preserved verbatim in SKILL.md run instructions. The exact wording matters.

**Typical shapes:** a meta-instruction that bends how the output is formed (a voiceprint generator told to return the voiceprint *in its own style*); a synthesis directive that prevents an obvious failure mode (an editor told to combine or discard overlapping edits rather than emit them as separate suggestions); an invitation to creative extension that keeps outputs from going rote (a checklist that ends *and one or two factors you think need to be there*).

**How to recognize them:** A craft move is usually something that, if you removed it, the output would look superficially similar but feel noticeably worse. They often read as opinionated directives with no obvious justification — because the justification lives in the author's experience.

**Do not paraphrase.** Preserve wording exactly.

## 3. Domain knowledge

**What it is:** Definitions, taxonomies, checklists, criteria, frameworks. Content that is true independent of the job — multiple skills could reference the same domain knowledge.

**Where it goes:** `references/*.md` in the skill directory, or in a shared references library if multiple skills use it.

**Typical shapes:** a craft checklist reused across a family of related skills (e.g., copy-editing dimensions reused across every editor variant); a labelled taxonomy that multiple skills sort against (content formats, persona archetypes); a definition of a domain object that several skills produce or consume (e.g., what a voiceprint is); a set of quality criteria multiple skills evaluate against.

**How to recognize it:** If you can imagine a different job using the same content without modification, it's domain knowledge. If it only makes sense inside this one job, it's a craft move.

## 4. Output shape

**What it is:** Strict format requirements — section order, heading levels, field structures, required elements in a specific sequence.

**Where it goes:** `templates/*.md`. Templates are loaded only when the user (or calling skill) requests strict mode.

**Typical shapes:** a strict ordered structure (label → analysis section → scored trait list with a fixed rating scale); a per-finding template the output repeats N times (`### N - title` / location / issue / suggestion); a multi-part assessment format (scored dimensions → improvement hierarchy → delivery section).

**Gotcha:** Many legacy prompts over-specified output shape as a defense against unreliable models. Modern agents can adapt. Default to flexible output unless (a) the user explicitly asks for the canonical shape, or (b) the shape is the product (voiceprints have a canonical form; an off-shape voiceprint isn't a voiceprint).

## 5. Examples

**What it is:** Canonical sample outputs included in the prompt to show the model what "good" looks like.

**Where it goes:** Depends on quality and era. See `example-rules.md` for the full decision framework. Four possible dispositions:

- **Keep as-is** in `examples/*.md` — if the example reads as current strong output.
- **Keep with legacy-prefix flag** — if adequate but dated; schedule replacement.
- **Flag for cleanup** — if human-written but weak; improve once editing skills are available.
- **Drop and defer** — if the example reads as AI-generated with era-specific tells. Plan fresh examples from real test runs.

**Typical shapes:** a named exemplar the original author wrote (often years ago — re-evaluate against current AI-tell patterns before keeping); an "example" block that's really a shape demonstration (those go to `templates/`, not `examples/`); a worked output the prompt walked through inline.

**Note:** Examples often double as templates (they demonstrate the shape). In conversion, distinguish between shape-demonstration (goes to `templates/`) and output-exemplar (goes to `examples/` only if quality passes). The 5–10 rule in `example-rules.md` matters: single examples are overfitting hazards.

## 6. Scaffolding candidate

**What it is:** Content that looks like it was added to coax older models into compliance. Modern frontier models don't measurably benefit from most of this — but some of what looks like scaffolding carries real craft.

**Where it goes:** Depends on assessment. Scaffolding candidates are not auto-dropped. Each chunk runs through the three-question assessment in `scaffolding-patterns.md`:

1. Would removing this change the output beyond cosmetic?
2. Is there a non-obvious task constraint hidden in the scaffolding framing?
3. Does it match a pattern with a clear "drop" disposition?

Most scaffolding does drop, but the assessment happens first so hidden craft gets extracted rather than lost.

**Candidate patterns (see `scaffolding-patterns.md` for full catalog and per-pattern assessment):**
- Tip bribery ("I'll tip you $200")
- Performance coaxing ("take a deep breath") — note: this pattern frequently hides real sequencing directives
- Catastrophizing stakes
- Persona cosplay ornamentation (keep functional role, drop decoration)
- XML ritual wrappers (keep real structure, drop empty wrapping)
- Step numbering (keep when sequential, drop when decorative)
- Chatbox placeholders
- Meta-instructions about output framing (context-dependent)
- Self-referential reward language
- Reminders to follow instructions

**Rule:** Assess every scaffolding candidate before dropping. Record the assessment outcome in the decision log — both drops (with pattern match) and keeps (with extracted craft noted).

## Tagging rules

- Tag the whole prompt at chunk-level (paragraph or semantic unit, not line-by-line).
- Ambiguous chunks get the best-fit category with a note. When in doubt between "craft move" and "domain knowledge," ask: *could another skill use this unchanged?* Yes → domain knowledge. No → craft move.
- Record the disposition in the decision-log table: what's going where.
