# Naming Conventions

Keep skill names short, descriptive, and action-oriented where possible. Cowork (and most skill harnesses) uses the skill name for both triggering and invocation, so the name should read well in both contexts.

## Voice and feel — favor language people actually use

Personal OS is bought by creators, operators, consultants, coaches — not engineers. Names throughout the product should match how the buyer would say things out loud, not how a developer would label them.

**Favor:**

- **Conversational over technical** — *"good morning"* over *"daily-briefing-orchestrator,"* *"skillify"* over *"skill-conversion-pipeline,"* *"tracker"* over *"task-management-system"*
- **Evocative over functional** — *"loop"* (suggests cyclic improvement) over *"skill-evolution-engine"*; *"library"* (universal) over *"reference-input-management-subsystem"*
- **Verbs and short noun-phrases people would type** — "good morning," "what's next," "make a skill," "find me a voiceprint"
- **Words that sound like something a friend would mention** — *"I just used Daily Assist to plan my day"* reads natural; *"I just invoked the daily-briefing-orchestrator"* doesn't

**Avoid:**

- AI-product suffixes — *-bot*, *-ai*, *-gpt*, *-engine*, *-pipeline*, *-orchestrator*
- Enterprise-software jargon in user-facing names — *workflow*, *protocol*, *framework* (these are fine inside reference docs and internal architecture, but not skill names)
- Compound technical phrases — *content-management-orchestrator*, *automated-task-routing-system*
- Implementation detail in the name — *shipped-version-tracker*, *log-rotation-handler*
- Acronyms unless they're already universal — buyers shouldn't have to learn a glossary

**Test it:** would the user say this name out loud naturally? *"I need to skillify this prompt"* reads fine. *"I need to invoke skill-conversion-pipeline on this prompt"* doesn't. Personal OS is bought by people who want AI working in their files, not by people who collect tools by acronym. Names that sound conversational earn trust; names that sound like they came from a JIRA ticket erode it.

This applies to skills, modes, configuration keys, file names users will see, and anything else the buyer encounters. Internal artifacts (reference docs, technical conventions, plumbing) can use precise/technical language where it serves clarity — but anything user-facing leans natural.

## Skill names

**Good:** `os-editing`, `os-voiceprint`, `os-offer`, `os-content-mining`, `os-skillify`

**Bad:** `content_editor_bot`, `editor-v2-final`, `MyEditingPrompt`, `edit` (too generic), `editing` (missing pack prefix)

Rules:
- lowercase, hyphen-separated
- **per-pack prefix is mandatory** — every skill name starts with `os-` or `dev-` per the pack it belongs to. See *Per-pack prefix table* in `workspace-layout.md` for the canonical mapping. The prefix is part of the canonical name (folder, frontmatter `name:` field, and every cross-reference).
- after the prefix: noun-phrase or short verb-phrase
- avoid version numbers in the name (versioning lives in frontmatter or changelog)
- avoid "-bot", "-ai", "-gpt" suffixes
- avoid the user's name

### Why prefix-first

Buyers may already have skills with the same root name as a Personal OS skill. The prefix prevents collision *and* tells the buyer at a glance which pack any skill came from. Prefixes are silent in spoken voice contexts (see workspace-layout.md *Verbal convention*) but always present in written / file / frontmatter contexts.

### Exceptions

There are no exceptions to the prefix rule. Skills that historically shipped without a prefix (e.g. `tracker`, `library`, `email`) have been renamed to their canonical prefixed form (`os-tracker`, `os-library`, `os-email`).

## Category skills vs. job skills

- **Category skill:** named for the category. `editing`, `content-planning`, `positioning`.
- **Job skill:** named for the specific job. `voiceprint`, `welcome-sequence`, `audience-profile`.

Use a category skill name when the skill contains multiple modes. Use a job skill name when the skill does one specific job.

## Mode names

Inside a category skill, modes are named for the specific job they perform.

**Pattern:** `<verb>-<object>` or `<short-name>`

**Examples in `os-editing/modes/`:**
- `copy-edit.md`
- `developmental.md`
- `argument-amplify.md`
- `redundancy-check.md`
- `tone-scale.md`
- `takeaway-extract.md`

Match the mode name to how the user would ask for it: "do a copy edit" → `copy-edit`; "extract takeaways" → `takeaway-extract`.

## Reference doc names

Descriptive noun phrases, hyphen-separated, `.md` extension.

**Examples:**
- `copy-editing-checklist.md`
- `voiceprint-definition.md`
- `content-format-taxonomy.md`
- `creative-criteria.md`
- `writer-style-preservation.md`

## Template names

Match the output they produce, suffixed with `.template` or `.md`.

**Examples:**
- `issue-suggestion-report.md`
- `voiceprint-output.md`
- `decision-log-entry.template`

## File structure

Skills live at `<workspace>/skills/<canonical-prefixed-name>/` per the workspace-layout contract. The standard discovery surface is `<workspace>/.agents/skills/`; harness-specific compatibility surfaces may sit beside it. The workspace root contains `AGENTS.md`, `CLAUDE.md`, `.agents/`, `skills/`, and the Personal OS-owned data directories `os-inputs/`, `os-tracker/`, `os-knowledge/`, `os-references/`. Claude Code installations may additionally carry `.claude/`, which is explicitly Claude-specific. Personal OS does not ship or install as a plugin on any surface (see `workspace-layout.md`'s no-plugins doctrine).

```
<workspace>/                              # e.g. ~/personal-os/
├── AGENTS.md                             # canonical operating principles (agent-agnostic)
├── CLAUDE.md                             # 2-line file: "Sync from @AGENTS.md"
├── .agents/skills/                       # standard agent-skill discovery surface
├── .claude/                              # OPTIONAL: Claude Code project config + compatibility skills/
├── skills/                               # source of truth for installed skills
│   ├── .skill-manifest.json              # auto-managed by os-skill-deploy
│   ├── _shared/
│   │   └── references/
│   │       ├── README.md
│   │       └── <shared-ref>.md
│   └── <pack-prefix>-<skill-name>/       # e.g. os-tracker, os-writing, dev-investigate
│       ├── SKILL.md
│       ├── references/                   # skill-internal (NOT os-prefixed)
│       │   └── <topic>.md
│       ├── modes/                        # category skills only
│       │   └── <mode-name>.md
│       ├── templates/
│       │   └── <output-shape>.md
│       └── examples/
│           └── <example-name>.md
├── os-inputs/                            # user-curated reference data (_os- prefixed plumbing + content dirs)
├── os-tracker/                           # task backlog (user.md + system.md)
├── os-knowledge/                         # non-skill knowledge artifacts
└── os-references/                        # workspace-level reference docs
```

## Shared references

When multiple skills need the same reference, it lives at `skills/_shared/references/`. Skills reference it via a relative path from their `SKILL.md` location:

- From `skills/<skill-name>/SKILL.md` → `../../_shared/references/<file>.md`
- From `skills/<skill-name>/references/*.md` or `skills/<skill-name>/modes/*.md` → `../../../_shared/references/<file>.md`

Avoid duplicating reference content across skills. Promote a reference into `_shared/` the moment a second skill needs it for the same reason.

## Frontmatter

Every SKILL.md has YAML frontmatter using the block-folded scalar form:

```yaml
---
name: <skill-name>
description: >-
  <trigger language — see frontmatter-format.md for the full rules>
---
```

The `>-` block-folded scalar lets descriptions contain colons, double quotes, and apostrophes without escaping. Bare strings break on every one of those characters and trip Cowork's validator. Always use `>-`.

Description length: aim for 400–800 characters; hard cap is 1024 (enforced by Cowork). Drop per-mode breakdowns — those belong in the SKILL.md body, not the frontmatter.

Standard optional field: `version` (semver, represents what shipped — see `frontmatter-format.md` Rule 4). Other fields that might be added later: `category`, `source-prompts` (for traceability back to legacy prompts).

## Legacy prompt references

When a converted skill descends from one or more legacy prompts, record the source filenames in the decision log, not in the skill itself. This keeps the skill clean while preserving the audit trail.

## Collision avoidance — the `_os-` prefix rule

Personal OS workspace plumbing files (anything in `os-inputs/` that's auto-managed metadata, not user content) carry the **`_os-`** prefix. Two intersecting conventions:

- **`_` (leading underscore)** marks the file as Personal OS plumbing rather than user-edited content. Standard for any auto-managed file.
- **`os-`** marks the file as Personal OS-provenanced. Avoids collision with conventions used by other harnesses (e.g., OpenClaw's `USER.md`, generic `_os-inbox.md` filenames in other tools).

**Standard names in `os-inputs/`:** `_os-user-profile.md`, `_os-setup-philosophy.md`, `_os-preferences.md`, `_os-inbox.md`, `_os-inbox-conventions.md`, `_os-proactive-prompts-rejected.md`, `_os-skill-usage.log`.

**User-content directories** (`voiceprints/`, `style-samples/`, `templates/`, `briefs/`) do NOT use the prefix — they're the buyer's content, not OS plumbing.

**Skill names** carry per-pack prefixes baked into the canonical name — `os-` for everything that ships with Personal OS (provenance), `dev-` for the coding pack (semantic). The prefix is part of the folder name and the `name` frontmatter; it is not a runtime toggle, and nothing is rewritten at install time. See `workspace-layout.md` for the full prefix system.

**The canonical name is the shipped name.** A skill authored as `os-tune` or `dev-investigate` ships and installs under exactly that name — what's on disk is what's referenced everywhere, so cross-references never dangle.
