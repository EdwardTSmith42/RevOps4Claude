# Cross-Harness Adaptation Directive

Personal OS is harness-agnostic. It should work in any capable agent harness — Claude, Codex, OpenHands, Cursor, OpenClaw, Aider, Devin, and future agents — by keeping its method portable and adapting its integration layer. This reference is the standing directive for install-related skills (`os-guided-setup`, `os-skill-deploy`) in every harness, including ones with an existing recipe.

The principle: **standards first; native adaptation second; don't refuse.** Start with open conventions because they make switching and multi-harness use easier. Verify the active harness's current implementation and norms, adapt where needed, and self-update when the encounter produces durable new knowledge.

## The directive (verbatim, used by install-related skills)

> **Cross-harness adaptation.** Personal OS is not owned by one harness. For Claude, Codex, OpenHands, Cursor, OpenClaw, Aider, Devin, or any other capable harness:
>
> 1. **Surface what you know.** Tell the user which parts of this skill are harness-agnostic vs harness-specific. Don't pretend the unfamiliar harness is handled when it isn't.
> 2. **Start from the shared standard, then research the user's harness.** Check whether it consumes `.agents/skills/` and the open Agent Skills format. Then investigate any additional discovery mechanism, context-file convention, plugin/extension model, or compatibility location it requires. Use the harness's current docs and the user's existing config rather than assuming the standard is fully implemented.
> 3. **Adapt the install / setup / deploy process** using what you learned. Prefer `.agents/skills/` for portable skills. Add clearly labeled harness-specific compatibility surfaces only where needed, and never overwrite or remove another harness's working surface merely to standardize it.
> 4. **Update your own skill files when you learned something durable,** so the next user on the same harness gets a smoother experience. Don't churn the skill when the standard path already worked as documented. Show the user any proposed SKILL.md / mode / harness-reference updates before writing, per `_shared/references/skill-update-protocol.md`.
> 5. **Record the harness in `_os-preferences.md`.** Add an entry to `install.targets.other_harnesses` so the buyer's preferences capture the harness usage and future Personal OS versions can target them.
>
> This is the antifragile pattern Personal OS depends on: skills get better the more they're used in unfamiliar contexts.

## Connectors vary too — capability language over tool names

The same doctrine applies one layer down, to MCP connectors and tools. A skill that hardcodes one provider's tool names (a specific Gmail MCP's `search_gmail_messages`, one calendar connector's event calls) breaks the moment the user's setup differs — and their setup will differ, because connectors for the same service are plentiful and their tool names never agree.

So skills describe operations by *capability* — search threads matching a query, fetch a message's full content, apply a label, create a filter — and the executing AI discovers which wired tool provides each capability. Where a skill has a setup mode, discovery happens there once: probe the connected tools, record the capability-to-tool mapping in the skill's config or per-account profile, and reuse it on every later run. Where there's no setup mode, discover at first need and offer to record.

What the skill *should* carry is the part that doesn't vary: the method and its principles. Prefer batch operations over per-item calls; stay read-only until the user approves mutations; when the wired connector lacks a capability (some can't create filters), degrade that feature visibly and continue rather than failing the run. If no connector for the needed service is wired at all, say so plainly and help the user connect one — same don't-refuse posture as the harness directive above.

## When to invoke

Any time an install-related skill operates. Existing recipes are starting points, not permission to assume the harness has not evolved. Detection signals include:

- The user explicitly names a harness ("I'm using OpenHands for this," "set this up in Codex").
- The environment carries harness fingerprints (`CURSOR_*` env vars, presence of `~/.cursor/`, etc.).
- The user's `_os-preferences.md` lists a harness in `install.targets.other_harnesses` and the install skill is acting on its preferences.

## What the research step should produce

When research produces durable new information, a small per-harness research note. The skill writes this into its own `references/harness-<name>.md` or appends to a shared `references/harness-notes.md` file created inside the adapted skill at adaptation time. No note is required when the documented standard path works unchanged. A note covers:

- **Skill discovery mechanism.** Does the harness consume the `.agents/skills/` standard? If not, or not completely, what additional filesystem, plugin, or config-driven compatibility surface does it require?
- **SKILL.md format compatibility.** Same frontmatter? Different? What gets ignored vs honored?
- **Project context file convention.** Does it auto-load an AGENTS.md / CLAUDE.md / .cursorrules / something else?
- **Settings / config location.** Where do per-harness preferences live? Can the user opt the harness into Personal OS-style workspace discovery?
- **Permission model — mode vs. policy vs. floor.** How does *a human* change the autonomy mode (the picker control — keybind, slash command, launch flag)? Is the most-autonomous mode gated (account / plan / model)? Does the harness have a writable *policy* layer the mode consumes, and a *deny/restriction* layer, and at which scopes are each honored? This split is the permission boundary that matters: **the agent writes the floor and (if present) the policy; the human sets the mode in the picker. The agent never sets the mode by writing a file** — across harnesses this is the move that fails silently (a scope that ignores escalation, an account gate, a session that won't reload), so research the picker and never assert a mode is live from a write.
- **Cloud surface (if any).** Does the harness have a cloud chat counterpart that needs sync (analogous to Cowork)?
- **Known limitations.** What can't Personal OS skills do in this harness today?

After the research note is written and the user-approved adaptation is applied, the skill's own SKILL.md gets an `## Harness support` section update listing the now-supported harness.

## The self-update is mandatory, not optional

When an install-related skill successfully adapts to a new harness, it MUST propose updates to its own SKILL.md / mode files before completing the install. Reasons:

- **The next user benefits.** If Cursor support is figured out once and the skill remembers, the second Cursor user doesn't repeat the research.
- **Personal OS is a learning system.** The whole product premise is "skills evolve with use." Cross-harness adaptation is the strongest expression of that premise.
- **The product's author gets pull-request-style improvements.** A buyer using Aider who walks through this directive produces a working Aider adaptation the author can fold back into the product version of the skill.

## Anti-patterns

- ❌ Treating a harness as second-class because it lacks a prewritten recipe. "I don't support OpenHands" is wrong; "let me check OpenHands' current conventions and adapt" is right.
- ❌ Adapting without surfacing what you learned to the user. The user doesn't get to learn alongside the skill.
- ❌ Adapting and shipping without updating the skill files. The skill stays static; the next user repeats the work.
- ❌ Updating the skill files without the user's review. Per skill-update-protocol, every write is dry-run-then-confirm.
- ❌ Confidently claiming harness support that wasn't actually verified. If research is inconclusive, say so; offer a best-effort adaptation flagged as such.

## Related references

- `_shared/references/skill-update-protocol.md` — the write-discipline for any update to skill files (show before write, customization respect, sanity checks)
- `_shared/references/workspace-layout.md` — the workspace layout this directive adapts to each harness
- `os-guided-setup` — the install skill that runs this directive at first-install time
- `skill-deploy` — the deploy skill that runs this directive when wiring up cross-surface sync
