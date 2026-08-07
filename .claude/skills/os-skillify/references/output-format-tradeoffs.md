# Output Format Tradeoffs — Cowork-native skill vs. copy-pasteable prompt

The microtool sub-modes produce tools in two output formats. The choice affects portability, integration, and iteration. This reference documents when each format wins and how to decide.

## The two formats

**Cowork-native skill.** Full skill structure at `/skills/<name>/`:

- `SKILL.md` with pack-convention-compliant frontmatter (name, description, triggers, negative triggers)
- `modes/<name>.md` for each mode (single mode for microtool, multiple for full skills)
- `references/<name>.md` for shared craft (optional)
- Library integration where appropriate (voiceprint loading, brief loading, save patterns)
- Triggered by Cowork's skill discovery — description matching surfaces the skill when the user describes a matching job

**Copy-pasteable code-fenced prompt.** A single markdown code fence containing the 7-section canonical micro-tool anatomy:

- Task / Persona / Constraints / Process / Success Qualities / Output Format / Inputs
- No frontmatter, no skill structure
- Drops directly into any LLM environment — ChatGPT, Claude, Gemini, another Cowork session, a Notion doc, a colleague's hands

## When Cowork-native wins

Cowork-native skills are the right choice when:

**The tool will be used inside this Cowork environment.** When the user is the primary consumer and they're working in Cowork day-to-day, the skill format gives them automatic discovery, iteration through skill edits, and integration with the rest of the pack.

**The tool integrates with library.** When the tool benefits from voiceprint loading (voice-fidelity-sensitive output), brief loading (project-scoped work), or template loading (structural shape), the Cowork-native format is the way. Copy-pasteable prompts can't load library artifacts.

**Iteration is expected.** Skills get refined through use — patches to constraints, additions to the process, adjusted output formats. Skill edits are clean and version-controlled. Editing copy-pasteable prompts in-place loses history and tends to drift.

**The tool will compose with other skills.** When the produced tool naturally chains with other pack skills (drafting, editing, content-discovery, etc.), the Cowork-native format makes the chain ergonomic.

**The tool needs negative triggers.** When the tool is at risk of being invoked in adjacent contexts where another skill is better, frontmatter negative triggers prevent misrouting. Copy-pasteable prompts have no routing layer.

## When copy-pasteable wins

Copy-pasteable code-fenced prompts are the right choice when:

**The tool will be used outside Cowork.** A colleague who doesn't have Cowork installed needs the tool. The user wants to drop the tool into a vanilla ChatGPT or Claude session for a one-off job. The tool will be embedded in documentation, a course, a tutorial, a blog post.

**The tool is a one-shot.** Some tools are single-use — the user runs the tool once, gets the output, and never thinks about it again. Building a Cowork skill for a one-shot tool is overhead. A code-fenced prompt is faster to produce and faster to use.

**The tool is being shared with non-Cowork users.** When the user wants to share a tool with their audience, their team, or the open internet, the portable format lives anywhere a markdown code fence does.

**The tool's voice should preserve the source's, not pack-convention conventions.** Copy-pasteable prompts don't follow the pack's own conventions internally — they follow the source author's voice. When source content has signature phrasing that the tool inherits verbatim, that voice survives in the copy-pasteable format. Cowork-native skills follow pack-convention (which sometimes means stripping voice idiosyncrasies for consistency).

**The tool is meant to be visible / inspectable.** Copy-pasteable prompts are transparent — the user reads the prompt and understands what it does. Cowork skills hide some of the structure inside frontmatter and reference files. Transparency matters for trust, for teaching others how prompts work, and for auditing what a tool actually does.

## When the choice is genuinely ambiguous

For most users most of the time, both formats would work and the choice depends on use case rather than tool quality. When ambiguous, two heuristics help:

**Default to copy-pasteable for personal one-shot use.** If the user's immediate use case is *"I have this job right now, I need a tool, I'll figure out long-term storage later,"* copy-pasteable produces faster and is easier to iterate inline. Saving to library as a template after the fact is one save call.

**Default to Cowork-native for pack-resident infrastructure.** If the tool is going to be invoked many times across many projects, integrate with library, or compose with other skills, Cowork-native is the right starting point. The skill structure pays off across uses.

When the user specifies, honor the specification. When they don't, the mode asks once: *"Cowork-native skill or copy-pasteable prompt?"* with brief one-line tradeoff explanations. Don't over-explain — most users decide quickly once given the choice.

## Format conversion after the fact

A Cowork-native skill can be exported as a copy-pasteable prompt by collapsing the SKILL.md and mode file into a single 7-section code-fence — useful when sharing a skill with non-Cowork users. The reverse is also possible — a copy-pasteable prompt can be expanded into a Cowork-native skill by routing it through `skillify`.

So the format choice isn't permanent. If the user picks copy-pasteable for an immediate use and later wants the Cowork-native version, they can convert via skillify. If they pick Cowork-native and later want to share, they can collapse to a code fence.

