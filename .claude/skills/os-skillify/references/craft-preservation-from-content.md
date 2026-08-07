# Craft Preservation from Content

How os-skillify extracts frameworks, terminology, verbatim phrases, and step-counts from source content and preserves them in produced tools. The patterns in this reference apply across `from-content` and `microtool-from-content`. Without these moves, content-derived tools read as generic AI summaries of the source rather than as tools that operationalize what makes the source distinctive.

## What carries source authority

Source content has several elements that carry authority — the things that make readers think *"this person knows what they're doing."* When os-skillify produces a tool from content, those elements need to survive into the tool, or the tool loses the source's edge.

### Named frameworks

Specific frameworks the source introduces or relies on. These usually have names — *"the 3-pillar framework," "the Hormozi value equation," "the 5-day learning architecture," "the FFGA model."* The name itself carries meaning. Tools that use the framework but rename it (or use it without the name) lose the recognition.

**The move:** when the source has a named framework, the tool references it by name. Use the name in the tool's task description, in process steps, in success qualities, in output format. Don't quietly rename to something more generic.

### Signature terminology

Specific words the source uses repeatedly that carry weight. Could be neologisms (the source coined a term), branded terms (the source's specific phrase for a common concept), or signature words used with unusual frequency or in a specific way.

**Typical shapes:** a neologism the source coined for a concept that doesn't have a clean existing word; a branded term that names the author's specific take on a common idea; an acronym the source returns to repeatedly (a 4-letter rollup of an audience's fears / frustrations / goals / aspirations, for instance).

**The move:** capture signature terminology in step 1 of the digest phase. Use the same words in the produced tool. Don't paraphrase them away.

### Verbatim phrases

Uniquely memorable lines or paragraphs that drive home concepts. Often live as quotables — the part of the source that gets screenshot, retweeted, or remembered as the line.

**Examples:**

- *"Fast, free, easy — pick two."*
- *"The riches are in the niches."*
- *"Don't sell the steak — sell the sizzle."*

**The move:** lift verbatim phrases into the produced tool where they sharpen clarity or authority. Typical placements: success quality descriptions, example outputs, framing lines in process steps. Don't paraphrase these — paraphrasing flattens them.

### Step-counts

Where the source uses a numbered structure — *"3 pillars," "9 accelerators," "5 days," "7 sections," "12 phases"* — the count is part of the framework. Rounding to a more symmetric number (3 → 5, 9 → 10) breaks the framework's recognition.

**The move:** mirror exact step-counts. If the source has 9 accelerators, the tool processes 9 accelerators. If the source has 5 days, the tool runs 5 days. The mode resists the temptation to "improve" the count.

### Worked examples

Specific cases the source walks through that demonstrate moves in action. These are often more instructive than the framework's abstract description because they show how the framework applies to real situations.

**The move:** when the source has worked examples, the produced tool should reference them in success qualities or in examples sections — the example illustrates what good output looks like.

## How os-skillify extracts these from content

Step 1 of `skill-from-content` and `microtool-from-content` is the digest phase. During digest, the mode actively scans for the elements above:

1. **Named frameworks** — Look for capitalized phrases, "the X model" / "the X framework" / "the X approach," section headers in the source that name a structure, repeated references to a specific labeled system
2. **Signature terminology** — Look for unusual words used 3+ times, words in quotes (the source is treating them as terms of art), words the source defines explicitly
3. **Verbatim phrases** — Look for short memorable lines, paragraph-length statements that summarize a concept, quotables / pull-quote-shaped material, lines the source repeats or returns to
4. **Step-counts** — Look for numbered lists, "X pillars," "Y steps," "Z stages," "N principles"
5. **Worked examples** — Look for "for example," walked-through case studies, before-after comparisons, specific named cases

Surface what was found before designing the tool — confirmation step lets the user catch missed signals.

## What os-skillify resists

**Don't add new frameworks.** The skill stays inside the source. If the source has 3 pillars, the tool doesn't have 5. If the source uses one mental model, the tool doesn't synthesize that model with a different one.

**Don't paraphrase signature language.** The source's distinctive phrasing is part of its authority. Paraphrasing flattens it. Lift verbatim where it adds fidelity.

**Don't generalize away specificity.** Source content is often valuable because it's specific — a specific industry, a specific case, a specific framework applied in a specific way. Tools that generalize the specificity into universal advice lose what made the source useful.

**Don't fabricate examples.** If the source's worked example was about real estate, the tool's example shouldn't suddenly be about SaaS to "make it more relatable." Use the source's domain or generalize the example's structure without inventing details that didn't exist in the source.

## Tradeoffs

**Verbatim lift vs. pack conventions.** Cowork-native skills follow pack conventions (no semicolons, restrained bullets, frontmatter rules). Source content often violates these — it has semicolons, dense bullets, vivid emoji. When verbatim lifting would import a convention violation:

- For Cowork-native output: paraphrase to pack-convention standards while preserving meaning, OR keep verbatim only inside quoted blocks (which exempt the lifted text from pack-convention rules)
- For copy-pasteable output: keep verbatim (the format follows source author voice rather than pack-convention)

**Framework-specific terminology vs. accessibility.** Some signature terms are clear in context but opaque without source familiarity. The tool should use the source's term *and* briefly define it when first introduced — the term carries authority, the definition makes the tool usable for someone who hasn't read the source.

**Example-source-domain vs. user-relevance.** Source examples are in the source's domain (real estate, education, copywriting). The user's domain may differ. The tool can preserve the source's example as the canonical illustration *and* invite the user to bring their own example as input — the source example demonstrates the move, the user example tests it.

