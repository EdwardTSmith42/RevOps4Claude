# Scaffolding Patterns — assessment, not auto-drop

Legacy prompts accumulate scaffolding — language that was there to coax older models into compliance. Most scaffolding on modern frontier models adds nothing and often adds noise. But some of what *looks* like scaffolding is quietly doing real work. Dropping by default risks losing craft that was hiding in plain sight.

The default disposition for each pattern below is "candidate for removal, pending assessment." Every scaffolding-tagged chunk gets inspected before being dropped.

## The assessment procedure

For each scaffolding candidate, ask three questions in order:

1. **If I remove this chunk and run the skill on the same input, would the output change in any way beyond cosmetic?**
   - Yes → the chunk is doing real work. Extract the craft into a proper location (Run instructions, reference, template). Drop the ritual wrapping, keep the substance.
   - No → proceed to Q2.

2. **Is there an interpretation under which this chunk encodes something non-obvious about the task — a constraint, a sequencing hint, a domain framing — that I'm not noticing because it's wrapped in scaffolding phrasing?**
   - Yes → surface the craft to the user for confirmation. Don't guess. Common case: "*take a deep breath and approach this step-by-step*" — the "step-by-step" might be a reasoning directive, and "take a deep breath" is coax. Split and keep the directive.
   - No → proceed to Q3.

3. **Does the chunk match a pattern below with a clear "drop" disposition?**
   - Yes → drop it; note in the decision log which pattern matched.
   - No → keep it flagged for now with a note; revisit if the skill underperforms.

The point of this procedure is slow, deliberate inspection. "Obvious scaffolding" is often where useful moves hide because nobody looks twice.

## Pattern catalog

Each pattern has: what it looks like, origin, assessment questions specific to the pattern, and a *default* disposition (which can always be overridden by the three-question procedure above).

### Pattern: Tip bribery

**Examples:**
- *"I will tip you $200 for every request that is answered correctly"*
- *"You'll be tipped $20/month for your efforts"*

**Origin:** Research-era hack showing payment framing produced marginal output improvements on GPT-3.5-class models.

**Assessment:** Rarely carries craft. The only time to preserve is if the tip amount is tied to a specific quality dimension ("tipped $200 for including all edits") — even then, the signal should be extracted and restated as a quality constraint without the tip framing.

**Default disposition:** Drop. Extract any quality constraints buried inside.

### Pattern: Performance coaxing

**Examples:**
- *"Take a deep breath"*
- *"Think carefully"*
- *"Approach this step-by-step"*
- *"Work through this systematically"*

**Origin:** Chain-of-thought elicitation from the era before models defaulted to reasoning.

**Assessment:** This pattern frequently hides genuine sequencing directives. *"Take a deep breath"* alone is coax; *"take a deep breath and approach this step-by-step"* contains an actual instruction to reason sequentially. Split the phrase — drop the coax, extract the directive as a Run step if the task genuinely benefits from stepwise reasoning.

**Default disposition:** Assess per-instance. Default-drop the coax, preserve and relocate any sequencing directives.

### Pattern: Catastrophizing stakes

**Examples:**
- *"If you fail, I could lose my job"*
- *"It's a Monday in October, most productive day of the year"*
- *"Errors will hurt the author's career"*

**Origin:** Attention elevation via emotional stakes.

**Assessment:** Essentially never carries craft. The exception is when the stakes framing specifies a real quality constraint — e.g., *"errors here will cost customer trust"* is stake-framed but contains a real domain constraint (accuracy is paramount). Extract the constraint, drop the stakes.

**Default disposition:** Drop.

### Pattern: Persona cosplay beyond function

**Examples:**
- *"You are a genius-level AI copy editor"*
- *"as if you've just taken lawfully prescribed Adderall"*
- *"world's top expert in X"*

**Origin:** Persona framing to shift domain attention.

**Assessment:** The role-declaration layer (*"AI copy editor"*) is functional — it frames the domain. The ornamentation layer (*"genius-level," "world's top," "Adderall-fueled"*) is decoration. Split: keep the functional role, drop the ornamentation.

**Default disposition:** Keep the functional role, drop the decoration.

### Pattern: XML ritual wrappers

**Examples:**
- `<PRIME_DIRECTIVE>...</PRIME_DIRECTIVE>`
- `<ACTION>...</ACTION>`

**Origin:** Structured tagging helped older models segment instruction types. Anthropic still recommends XML tags for distinct content categories (inputs, examples, instructions).

**Assessment:** When the wrapper genuinely separates different content types, the structure is doing real work — keep the organization, even if the XML is replaced by markdown headers. When the wrapper is just a ritual wrapping of a single paragraph, it's decoration.

**Default disposition:** Assess per-instance. Preserve real organizational structure; drop ritual wrapping.

### Pattern: Step numbering

**Examples:**
- Sequential numbered lists where the numbers may or may not denote real sequencing

**Origin:** Numbered steps provided reliable structure for weaker models.

**Assessment:** If steps depend on each other (step 2 uses output of step 1), the numbering is load-bearing. If steps are just a list of requirements in arbitrary order, the numbering is decorative.

**Default disposition:** Keep sequential numbering where order matters; convert decorative numbering to bullets or prose.

### Pattern: Chatbox placeholders

**Examples:**
- *"<<See user input>>"*
- *"{your content here}"*
- *"Paste your content below"*

**Origin:** Written for chat interfaces where users paste content after the prompt.

**Assessment:** In skill context, input flows naturally through agent tool use. These placeholders are artifacts of a different delivery mode.

**Default disposition:** Drop.

### Pattern: Meta-instructions about output framing

**Examples:**
- *"Return only the output, nothing else"*
- *"Disable intro and conclusion text"*
- *"Do not explain what you're about to do"*

**Origin:** Constrains chatty models; useful for machine-consumed outputs.

**Assessment:** If the skill's output is meant to be pasted into another system or consumed programmatically, these are real output constraints. If the skill is conversational, they're unnecessary.

**Default disposition:** Keep for machine-consumed outputs; drop for conversational skills.

### Pattern: Self-referential reward language

**Examples:**
- *"Reward yourself for good work"*
- *"You'll be proud of this"*
- *"I believe in you"*

**Origin:** Cheerleading for weaker models.

**Assessment:** Essentially never carries craft.

**Default disposition:** Drop.

### Pattern: Reminders to follow instructions

**Examples:**
- *"REMEMBER: follow all instructions exactly"*
- *"IMPORTANT: do not skip steps"*
- *"CRITICAL: match the output format"*

**Origin:** Marginal benefit on weaker models; can produce overly cautious output on frontier models.

**Assessment:** Rarely carries craft. Occasionally the reminder points to a specific constraint that's genuinely critical ("CRITICAL: never include the author's real name") — when so, extract the constraint and state it as a regular rule.

**Default disposition:** Drop the reminder framing; extract any specific constraints hidden inside.

## Logging scaffolding decisions

Every scaffolding chunk that gets dropped goes into the decision log's "Dropped" section with its source phrasing and which pattern (or assessment outcome) justified the drop. Every scaffolding chunk that gets kept because assessment found craft inside goes into the classification table with its extracted purpose noted.

The audit trail matters. Future skillify runs can check the log to see whether a specific kind of scaffolding tends to carry craft on a specific author's prompts — an author's prompt library may have patterns of hidden craft that aren't visible in any single conversion.
