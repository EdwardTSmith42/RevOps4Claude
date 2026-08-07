# Personal OS — Workspace Layout Contract

The directory shape every Personal OS workspace conforms to, plus the rules governing how skills get distributed through the Agent Skills standard, explicit harness compatibility surfaces such as Claude Code, Claude's cloud surfaces (Cowork, web Chat), and future harnesses via cross-harness adaptation. Install-related skills (`os-guided-setup`, `os-skill-deploy`) honor stored preferences when laying artifacts down.

Buyers receive a workspace already conforming to this layout via the install zip. The runtime preferences they pick (which surfaces to install to, install method, security calibration) get recorded in `os-inputs/_os-preferences.md` and read by every install-related skill thereafter.

This reference is the canonical answer to questions like:

- *Where does `os-library/find` look for voiceprints?*
- *Where does `writing` load the user's `name`?*
- *What does Claude Code need to see at workspace root for everything to "just work"?*
- *How do my skills end up available in Cowork and web Chat too?*
- *Codex? Cursor? OpenClaw? Some harness you haven't heard of?*

## The two-layer model

A Personal OS install runs in two layers simultaneously:

| Layer | Path | Scope | What it holds |
|---|---|---|---|
| **Global** | `~/.agents/skills/` plus any harness-specific user config | Sessions outside the Personal OS workspace | Portable cross-project skills at the standard path; harness-specific settings and compatibility skills remain in their own clearly labeled locations. |
| **Workspace** | `<workspace>/` (e.g. `~/personal-os/`) | When an agent harness is opened with this folder as cwd | Personal OS skills and data scaffold, standard `.agents/skills/` discovery, AGENTS.md, and any explicit harness compatibility configuration. The workspace IS the Personal OS install. |

When you open a standards-compatible harness inside a Personal OS workspace, user-wide `~/.agents/skills/` and workspace-scoped `<workspace>/.agents/skills/` can both be active. Harnesses may add their own parallel surface: Claude Code, for example, can use `.claude/skills/`. `<workspace>/AGENTS.md` is the canonical root principles file; `<workspace>/CLAUDE.md` is a Claude-specific wrapper that inlines AGENTS.md through Claude Code's `@filename` syntax.

When you open a harness outside a Personal OS workspace, only user-wide skills and that harness's global configuration are active. Workspace-only Personal OS skills remain scoped to the workspace unless the user explicitly enabled the global Agent Skills target.

## Workspace directory layout

All Personal OS-owned data directories at workspace root carry the `os-` prefix for namespace-collision protection with the buyer's existing setup. Skill folders under `skills/` use their per-pack canonical names (`os-` for everything that ships with Personal OS, `dev-` for the coding pack). User-content subdirectories inside `os-inputs/` (voiceprints, style-samples, templates, briefs) stay unprefixed because they're buyer content, not OS plumbing.

```
<workspace>/                                       # e.g. ~/personal-os/
├── AGENTS.md                                      # canonical root principles (agent-agnostic)
├── CLAUDE.md                                      # 2-line file: "Sync from @AGENTS.md"
├── .agents/skills/                                # standard workspace skill-discovery surface
├── .claude/                                       # OPTIONAL: Claude Code project config
│   ├── settings.json                              # project-level Claude Code settings (optional)
│   └── skills/ → ../skills/                       # symlink — Claude Code workspace-scoped discovery
├── skills/                                        # SOURCE OF TRUTH for installed Personal OS skills
├── .skill-manifest.json                       # hash + upload state for os-skill-deploy
│   ├── os-writing/                               # per-pack prefix baked into canonical name
│   │   ├── SKILL.md
│   │   ├── modes/
│   │   └── references/                            # skill-internal references (NOT os-prefixed)
│   ├── os-library/
│   ├── os-voiceprint/
│   ├── dev-investigate/
│   └── ...
├── os-inputs/                                     # the user-curated reference data layer
│   ├── _os-user-profile.md                        # identity + implied-author name (required)
│   ├── _os-setup-philosophy.md                    # runtime behavior tuning — os-tune thresholds, proactive-prompting (required)
│   ├── _os-preferences.md                         # install/structural preferences — symlink-vs-copy, surfaces (required)
│   ├── _os-proactive-prompts-rejected.md          # AI proactive-offer rejection state (auto-managed)
│   ├── _os-inbox.md                               # the workspace inbox (corrections, captures, audit log)
│   ├── _os-inbox-conventions.md                   # tag taxonomy + routing rules for _os-inbox.md
│   ├── _os-skill-usage.log                        # JSONL log of every skill invocation
│   ├── voiceprints/                               # voice fingerprints (one .md per author/scope)
│   ├── style-samples/                             # few-shot exemplars
│   ├── templates/                                 # proven structural shapes
│   ├── briefs/
│   │   ├── current/                               # active project briefs
│   │   └── archive/                               # completed project briefs
│   └── <org>-rules.md                             # per-org voice / pricing / positioning rules (optional)
├── os-tracker/                                    # task backlog (managed by os-tracker skill)
│   ├── user.md                                    # user-visible backlog
│   └── system.md                                  # Personal OS system worklog (managed by os-tune/refine/extend)
├── os-knowledge/                                  # what's valuable from what you share — ideas, frameworks, insights — kept with their source
│   └── README.md                                  # explainer stub shipped with zip
├── os-outputs/                                    # things the user creates or Personal OS creates on their behalf
│   └── README.md                                  # flexible organization + version-family convention
└── os-references/                                 # workspace-level reference docs (not skill-internal)
    └── README.md                                  # points at _shared/references/workspace-layout.md
```

### Workspace-dir naming convention

Personal OS-owned data directories carry the `os-` prefix at workspace root. Same rationale as skill-name prefixes — collision protection against the buyer's existing setup, plus visual provenance. Applies to:

- `os-inputs/`, `os-tracker/`, `os-knowledge/`, `os-outputs/`, `os-references/` — Personal OS data dirs
- Skill folders under `skills/` carry per-pack prefix (`os-` for Personal OS, `dev-` for the coding pack)

Does NOT apply to:

- User-content subdirs inside `os-inputs/` (voiceprints, style-samples, templates, briefs) — buyer's content, not OS plumbing
- Skill-internal `references/` folders under `skills/<skill>/references/` — skill-local, not workspace-root

Inside `os-inputs/`, plumbing files keep the `_os-` prefix. The double-`os-` (e.g. `os-inputs/_os-user-profile.md`) looks redundant but each prefix carries its own meaning: dir provenance + file plumbing.

### What's required vs optional

- **Required for any skill to function:** `os-inputs/_os-user-profile.md`, `os-inputs/_os-setup-philosophy.md`, `os-inputs/_os-preferences.md`, `skills/<slug>/SKILL.md` for whichever skills are installed
- **Required for os-skill-deploy to function:** `<workspace>/.skill-manifest.json` (auto-created on first run)
- **Feeds cross-session pattern detection (optional):** `os-inputs/_os-inbox.md`, `os-inputs/_os-skill-usage.log`
- **Optional but high-leverage:** `os-inputs/voiceprints/`, `os-inputs/style-samples/`, `os-inputs/templates/`, `os-inputs/briefs/current/`, `os-inputs/<org>-rules.md`
- **Optional but scaffolded for work worth keeping:** `os-outputs/` — organization adapts to the user's clients, projects, content types, themes, and working context
- **Written by the weekly pass, not by hand:** `os-memory/` — distilled session memories plus `_ledger.md`. Machine-written and user-editable; nothing else writes here.
- **Required only if using `os-tracker` skill:** `os-tracker/user.md`, `os-tracker/system.md` (ship the dir scaffolded regardless)

## Cross-skill reference paths

Skills that reference siblings or shared resources use relative paths. The convention depends on where the file lives in the skill folder:

| File location | Path to sibling skill | Path to `_shared/references/` |
|---|---|---|
| `<skill>/SKILL.md` (depth 0) | `../<sibling-skill>/...` | `../_shared/references/<name>.md` |
| `<skill>/modes/<mode>.md` (depth 1) | `../../<sibling-skill>/...` | `../../_shared/references/<name>.md` |
| `<skill>/references/<ref>.md` (depth 1) | `../../<sibling-skill>/...` | `../../_shared/references/<name>.md` |
| `<skill>/templates/<template>.md` (depth 1) | `../../<sibling-skill>/...` | `../../_shared/references/<name>.md` |

Absolute deployed paths (`~/.agents/skills/<skill>/...`, `~/.claude/skills/<skill>/...`) are not used in skill bodies — they're hostile to portability across installs and surfaces. Where a script genuinely needs an absolute path at runtime, the script resolves the active skill directory itself; the skill body describes the discipline, not one harness's literal path.

The two-up path from modes / references / templates is a recurring drift surface: the one-up form silently fails because it resolves inside the skill's own directory instead of escaping to the workspace `skills/` root. Auditors and authors should explicitly check the depth when writing or modifying cross-skill references.

## Filename conventions

Two intersecting prefix patterns govern workspace filenames:

| Pattern | Meaning | Used for |
|---|---|---|
| `_` (leading underscore) | Personal OS plumbing — auto-managed metadata, not user-edited content | `_os-user-profile.md`, `_os-preferences.md`, `_os-inbox.md` |
| `os-` | Personal OS provenance — disambiguates from generic / other-tool filenames | `_os-user-profile.md` (vs OpenClaw's `USER.md`), `os-tune` skill (vs Claude's `/loop` slash command), `_os-inbox.md` (vs other inbox conventions) |

The combination `_os-<name>` marks a file as both plumbing AND Personal OS-provenanced. Standard for every metadata file in `os-inputs/`. Skills writing to `os-inputs/` use the prefixed paths.

User-authored content directories (`voiceprints/`, `style-samples/`, `briefs/`, etc.) inside `os-inputs/` do NOT use prefixes — they're the buyer's content, not OS plumbing.

See also `naming-conventions.md` for the broader skill / mode / file naming rules.

## AGENTS.md vs CLAUDE.md

**`AGENTS.md`** is the canonical, agent-agnostic root principles file. It tells *any* agent (Claude Code, Codex, Cursor, Aider, Devin, OpenClaw) how to behave inside this workspace: the inheritance protocol, the capture decision tree, the eagerness traps, the operating principles. Single source of truth.

**`CLAUDE.md`** is a 2-line file at workspace root that inlines AGENTS.md via Claude Code's `@filename` syntax:

```markdown
# Project context — Claude Code

> Sync from @AGENTS.md

Claude Code-specific overrides live in `.claude/`.
```

This satisfies Claude Code's auto-load convention (which reads CLAUDE.md at project root) while keeping AGENTS.md as the canonical source. Edit AGENTS.md once; Claude Code sees the change automatically via the inline. No drift.

Codex looks for `AGENTS.md` directly (confirmed via `~/.codex/AGENTS.md` convention). Other harnesses either follow the AGENTS.md convention or look at their own root file; the cross-harness adaptation directive (see below) handles unknown cases.

## Skill naming + prefixes

Every Personal OS skill ships with a **per-pack prefix baked into its canonical name** — folder name, `SKILL.md` frontmatter `name` field, and every internal cross-reference. The prefix is not a toggle; it is the name. This serves two purposes: it prevents collisions with skills a buyer may already have under the same root name, and it makes pack provenance visible at a glance in any skill list.

### Per-pack prefix table

| Pack | Prefix | Provenance vs Semantic | Examples |
|---|---|---|---|
| Personal OS (everything that ships with the install) | `os-` | Provenance | `os-tune`, `os-library`, `os-capture`, `os-tracker`, `os-guided-setup`, `os-skill-deploy`, `os-autosave`, `os-skillify`, `os-voiceprint`, `os-writing`, `os-editing`, `os-audience`, `os-offer`, `os-content-discovery`, `os-gold` |
| Coding (dev pack) | `dev-` | Semantic | `dev-investigate`, `dev-review`, `dev-PR` |

`os-` is **provenance** — it names what ships with Personal OS, covering both system / OS-plumbing skills and the writing / content / audience / offer skills that sit alongside them in the operator's daily work. There's no separate "creator" prefix: creator work is part of running your Personal OS, not a boundary you cross into. `dev-` is **semantic** — it carves out coding work, which lives at a different surface, toolchain, and mental mode (different repos, different cwd, different agent-harness considerations) and earns its own namespace. Each skill declares its pack in `SKILL.md` frontmatter via the `packs:` field, and the canonical name matches the prefix for that pack.

### Canonical naming, not install-time renaming

Skills are authored, shipped, and installed under their canonical prefixed names. Nothing is rewritten at install time. This means:

1. The pack ships `os-writing` at `<workspace>/skills/os-writing/` — the canonical name on disk, no install-time translation. The buyer invokes it by that same name.
2. Cross-references inside `SKILL.md` files use the canonical names (`os-library`, `os-writing`, `dev-review`) — no AI graceful-degrade required.
3. Mode-selection rules, `when_to_use` triggers, and any docs that name a skill use the canonical form.

### Verbal convention (for voice agents and spoken contexts)

Prefixes are **verbally silent** in most cases. A voice agent says "Email," "Library," "Tracker" — not "os-email," "os-library," "os-tracker." Two exceptions where the prefix is spoken because it carries meaning about the pack/system itself:

- `os-tune` — spoken as "os-tune"
- `os-autosave` — spoken as "os-autosave"

Written contexts (artifacts, docs, install guides) use the canonical prefixed names throughout.

## Cross-surface distribution

A Personal OS skill needs to be available on multiple surfaces, and the install machinery has to route to each of them. The chain:

```
<workspace>/skills/<slug>/                                    ← source of truth
   │
   ├── (symlink or copy) <workspace>/.agents/skills/<slug>/   ← Agent Skills standard, workspace-scoped
   ├── (symlink or copy) ~/.agents/skills/<slug>/             ← Agent Skills standard, user-wide (per preference)
   ├── (symlink or copy) <workspace>/.claude/skills/<slug>/   ← Claude Code workspace-scoped
   ├── (symlink or copy) ~/.claude/skills/<slug>/             ← Claude Code global (per preference)
   ├── (skill-deploy zip + manual upload via claude.ai)       ← Cowork + web Chat
   └── (cross-harness adaptation)                             ← Cursor / OpenClaw / others — researched in-flight per cross-harness-adaptation.md
```

**Why workspace skills/ is the source of truth:** all other locations either symlink or copy from here. Editing a skill in `<workspace>/skills/<slug>/SKILL.md` propagates automatically to every symlink. Updating cloud surfaces still requires the manual zip+upload step but `skill-deploy` reports drift accurately because it's hashing the source.

### Agent Skills standard; Codex first-class

Portable skill deployment standardizes on `<workspace>/.agents/skills/<slug>/` and `~/.agents/skills/<slug>/`. Codex consumes these locations and the open Agent Skills shape. Its frontmatter loader reads `name` and `description` and tolerates Personal OS-specific extras (`display_name`, `tagline`, `category`, `packs`, `icon`, `when_to_use`, `modes`). The directory shape (SKILL.md + optional `references/`, `agents/`, `scripts/`, `assets/`) aligns with what Personal OS skills ship.

Symlink or copy from `<workspace>/skills/<slug>/` into the chosen `.agents/skills/` surface. Verify discovery with a live sample invocation because harness implementations can lag the standard or change independently.

`~/.codex/skills/` is Codex's legacy user-skill location and still houses some Codex-managed system assets. Personal OS does not install new portable skills there by default and never deletes existing content from it. Older installs can keep working while setup offers a non-destructive move to `.agents/skills/`.

### The install method (symlink vs copy)

| Method | Pros | Cons |
|---|---|---|
| **Symlink** (recommended) | Edits propagate instantly across all surfaces. Less disk used. Cleanup is easy (one `unlink` per surface). | Symlinks fragile on Windows / some sandbox tools. Some tools resolve symlinks to absolute paths, which may break when the workspace moves. |
| **Copy** | Universal compatibility. Symlinks aren't needed at all. | Edits don't propagate — every surface needs an explicit re-copy to refresh. Deletes need explicit cleanup tracking. Three copies of every skill on disk. |

The preference lives in `_os-preferences.md` as `install.method: symlink | copy`. Default: `symlink`. If `copy` is chosen, every install-related skill must read this preference and explicitly track copies for future cleanup.

### The cloud surface (Cowork + web Chat)

claude.ai → Customize → Skills is the only upload path for Cowork and web Chat. They share one cloud store. Personal OS handles this via `skill-deploy`:

1. `skill-deploy status` reports drift (which skills changed since their last marked upload).
2. `skill-deploy zip --all-drifted` produces `dist/<slug>.zip` files with the correct single-top-level-folder structure.
3. **Manual step:** drag the zips into claude.ai's Customize → Skills.
4. `skill-deploy mark-uploaded --all-zipped` baselines the manifest so future drift is real drift.

**Doctrine: Personal OS does NOT distribute as a plugin on any surface, on purpose.** Plugins create complex update friction — buyers can't iterate their own skills inside a plugin without a full plugin republish cycle. That contradicts the *entire* premise of Personal OS, which is that users evolve and refine their skills over time based on real use. The manual zip+upload via `skill-deploy` is also imperfect, but it preserves the buyer's edit → reload → use cadence. Hopefully Claude's cloud surfaces improve their own update story; until then, this is the chosen friction.

### Shared references and surface awareness

Skills load shared references from `<workspace>/skills/_shared/references/<name>.md` via relative paths (`../../_shared/references/<name>.md` from a SKILL.md, `../../../_shared/references/<name>.md` from a mode or reference file). The pattern keeps one source of truth for cross-cutting reference docs (capture-decision-tree, skill-prompting-principles, scaffolding-patterns, etc.) so they don't drift across consumers.

This works natively on filesystem-resolving surfaces — standards-compatible harnesses resolve through `.agents/skills/<slug>/`, while Claude Code may resolve through its explicit `.claude/skills/` compatibility surface. It does **not** work on cloud surfaces (Cowork + web Chat). The zip uploaded to claude.ai contains only the skill's own folder; any `../../_shared/` reference escapes the zip root and resolves to nothing.

The contract that fixes this:

**At zip time (`os-skill-deploy zip`):** the deploy script scans the skill's body files for relative-path loads of `_shared/references/<name>.md`. Each match gets bundled inside the zip at `<skill>/_shared-refs/<name>.md` (a flat subdirectory inside the skill itself, distinct from the skill's own `references/`). The bundled body files get their shared-ref paths rewritten to point at the new in-zip location — depth-aware, so `../../_shared/references/<name>.md` becomes `_shared-refs/<name>.md` from SKILL.md but `../_shared-refs/<name>.md` from `modes/*.md`. The workspace source-of-truth files stay unchanged; only the zipped copies carry the rewritten paths. Code and Codex keep reading from the workspace via the original paths. Cowork reads the bundled copies via the rewritten paths. No surface gets a broken reference.

**Drift and visibility.** The zip-bundling step is run every zip, so a shared ref edited in the workspace propagates to Cowork on the next zip+upload — same cadence as any other skill edit. The bundled copies are recreated each time; they don't accumulate stale.

**What does NOT count as a shared ref.** The bundling logic only looks at `_shared/references/<name>.md` paths. References to sibling skills (`../os-library/SKILL.md`), shared *templates* (no current pattern), or cross-skill examples are out of scope. If those patterns emerge, the contract extends; right now, only `_shared/references/` matters.

**Recursion.** Shared refs that themselves reference other shared refs are bundled too — the scan recurses one level. Deeper nesting is uncommon enough that v0.1 surfaces a warning rather than silently bundling N levels deep. The deploy script's warning names the chain so the author can flatten if needed.

### Cross-harness adaptation for non-first-class harnesses

For harnesses that aren't Claude Code or Codex (Cursor, OpenClaw, Aider, Devin, future agents we haven't heard of), the install-related skills follow the **cross-harness adaptation directive** in `cross-harness-adaptation.md`. Summary: research the harness, adapt the install process, update the install skill's own SKILL.md with what was learned, record the harness usage in `_os-preferences.md`. The skills get smarter the more harnesses they're used in. This is the antifragile pattern Personal OS depends on.

## The `_os-preferences.md` file

The single source of truth for install/structural choices. Read by every install-related skill. Schema:

```yaml
---
install:
  method: symlink                     # symlink | copy
  targets:
    agent_skills_workspace: true      # standard workspace surface: <workspace>/.agents/skills/
    agent_skills_global: false        # standard user surface: ~/.agents/skills/
    claude_code_workspace: false      # Claude-specific compatibility surface
    claude_code_global: false         # symlink/copy from workspace skills/ into ~/.claude/skills/
    other_harnesses:                  # recorded for cross-harness-adaptation runs
      - name: cursor                  # buyer told us they use Cursor
        status: adaptive              # setup follows current harness conventions
      - name: openclaw
        status: deferred
  cloud_upload: prompt                # always | prompt | never — os-skill-deploy default behavior
security:
  calibration: auto-frontier          # auto-frontier | conservative | custom
  deny_list:                          # commands the AI should never run
    - rm -rf /
    - git push --force-with-lease origin main
    - git push --force origin main
    # ...starter list expanded per security-calibration.md
workspace:
  location: ~/personal-os/            # recorded for cross-machine portability hints
---

# Personal OS — Install preferences

This file records the structural choices made at install time. Every install-
related skill (os-guided-setup, os-skill-deploy) reads it
to know how to lay artifacts down for THIS install.

## Install method (symlink vs copy)
[Explanatory prose...]

## Surface targets
[Explanatory prose about Claude Code global, Codex global, cloud upload, cross-harness...]

## Security calibration
[Explanatory prose about auto-frontier vs conservative vs custom; the starter deny-list...]
```

**Note on the prefix system:** previous versions of this schema included a `prefix.enabled` toggle. That toggle has been removed. Prefixes are canonical (baked into skill names) and not configurable. See *Skill naming + prefixes* above for the contract.

The frontmatter is the structured contract; the prose section is human-readable explanation.

## os-inputs/ contract

Every skill that consumes user-curated data reads from `os-inputs/` per a documented matching discipline. The canonical contract is in `os-library/references/matching-discipline.md`; the per-type rules are:

- **`_os-user-profile.md`** — read for the user's name (drives the implied-author rule when no author is named in a brief). Optionally carries default voiceprint scope, default org, default brief.
- **`_os-setup-philosophy.md`** — read for tiered-approval thresholds, what os-tune should/shouldn't auto-touch, proactive-prompting on/off.
- **`_os-preferences.md`** — read for install method, surface targets, security calibration.
- **`voiceprints/<scope>.md`** — loaded by os-writing / os-editing skills via os-library/find.
- **`style-samples/<author>/<pattern>.md`** — few-shot exemplars loaded as drafting context.
- **`templates/<format>.md`** — proven structural shapes loaded by os-writing.
- **`briefs/current/<project>.md`** — active project context loaded when the user names the project.
- **`<org>-rules.md`** — per-org voice / positioning / pricing constraints, layered onto voiceprint when present.

## os-outputs/ contract

`os-outputs/` holds things the user creates or Personal OS creates on their behalf. It includes both work in progress and finished artifacts. It is intentionally flexible: organize by client, project, content type, theme, or another structure that fits the user's practice. Start flat when no grouping has earned its place; use context to choose an obvious home and discuss the choice only when different structures would materially change later retrieval. `os-outputs/README.md` remains the human-readable index as that structure grows.

Preserve meaningful before-and-after states. The first meaningful draft and final human-edited version are separate files, not overwrites; intermediate files are optional and should represent real turns. Every version in one artifact family shares the same filename stem, changing only the lifecycle suffix (`-first-draft`, `-in-progress`, `-final`). Before modifying or renaming one member, inspect its same-stem siblings and decide whether the change also applies to them. Shared identity, metadata, organization, and factual corrections often travel across the family; lifecycle-specific prose stays distinct so the first-to-final comparison remains honest. A genuine pivot starts a new family and links back with `derived_from`.

Draft state is explicit in the filename and frontmatter. Native destinations remain valid — Gmail, Docs, Slides, a client drive, a code repository — while the workspace keeps a copy when the user wants Personal OS to retain the artifact or its revision history.

## Skills/ contract

Each skill lives at `<workspace>/skills/<slug>/` (with optional prefix). Internal shape:

```
skills/<slug>/
├── SKILL.md                    # frontmatter + behavior contract (required)
├── modes/                      # mode files (optional, only if skill has modes)
├── references/                 # internal reference files (optional)
├── templates/                  # output templates the skill emits (optional)
└── bin/                        # executables the skill ships (optional)
```

`SKILL.md` frontmatter conforms to `skills/_shared/references/frontmatter-format.md`. The `name` field matches the folder name (canonical prefixed form, e.g. `os-library`, `os-writing`). No install-time rewriting — what ships is what lives on disk.

## The .skill-manifest.json

Lives at `<workspace>/.skill-manifest.json` (vault root). **Derived, machine-local state** — rebuildable anytime by rescanning; contrast `.os-manifest.json`, the canonical release baseline that cannot be regenerated after install. Tracks current skill hashes + upload state per surface. Managed by `skill-deploy`. Committed (when the workspace is git-tracked) so machines syncing the workspace stay aligned on cloud upload state.

## Resolved decisions (v0.3)

| # | Decision | Resolution |
|---|---|---|
| 1 | AGENTS.md depth | AGENTS.md canonical, CLAUDE.md is `@AGENTS.md` inline with "Sync from" header |
| 2 | tracker / knowledge / references directories | Ship all scaffolded with starter content + headers; files use `_os-` prefix where they're plumbing; tracker contexts are named by context slug per `os-tracker` (`user.md`, `system.md`) |
| 3 | inbox.md + skill-usage.log | Ship with header comments; universal `_os-` prefix on all plumbing files in `os-inputs/` |
| 4 | Workspace location | `~/personal-os/` recommended; install docs include plain-language explanation for Mac, Windows, Linux |
| 5 | Agent Skills / Codex first-class | Standardize portable deployment on `.agents/skills/`; Codex is a first-class consumer. Preserve legacy `.codex/skills/` installs non-destructively. |
| 6 | Cursor / OpenClaw / other harnesses | Supported through the cross-harness adaptation directive: research current conventions, adapt the install, preserve durable findings in the skill files, and record harness usage in preferences. Setup lists known harnesses and asks "anything else?" |

## Doctrine

- **No plugins, anywhere.** Plugins create skill-evolution friction that contradicts Personal OS's whole premise — a skill inside a plugin can't be edited in place. `skill-deploy` zip+upload is the chosen path for cloud surfaces; local surfaces link to the workspace directly.
- **Filename collision avoidance.** Workspace-root and os-inputs/-level filenames use `_os-` prefix to avoid collision with conventions used by other harnesses (OpenClaw's `USER.md`, generic `_os-inbox.md`, etc.). User content directories don't use prefixes.
- **One source of truth, propagated by symlinks.** Edit at `<workspace>/skills/<slug>/`, every consumer surface sees the update.
- **Cross-harness antifragility.** Install-related skills don't refuse unknown harnesses — they research, adapt, and update themselves. The skills get smarter with use.
- **All skills live in `skills/` — provenance by prefix and manifest, not by directory.** There is no separate source directory for the user's own skills: shipped skills carry the `os-`/`dev-` prefixes and are listed (with hashes) in `.os-manifest.json`; a skill directory not in the manifest is the user's own; a manifest skill whose hash differs carries user customizations, which updates preserve. `.agents/skills/` is the standard deployed surface; harness-specific surfaces such as `.claude/skills/` remain explicit compatibility choices.
- **`experiments/<slug>/` is os-skillify's staging surface** (dual-lane drafts, interview briefs) — ephemeral by design; artifacts there either promote into `skills/` or get cleaned up at the end of the skillify run, so the reachability sweep treats it as a sanctioned scratch zone.
- **Cross-pack siblings are self-contained, never dependent.** When two packs need the same craft (e.g. `os-fresh-eyes` / `dev-fresh-eyes`), each pack carries its own complete skill — a buyer may own either pack alone, so a hard dependency across packs breaks real installs. The siblings share significant language by design, each fully optimized for its domain, and each carries a propagation note: improvements to the shared core move to the sibling when relevant. Deliberate duplication, declared lineage, no silent drift.

## Knowledge system invariants (v0.4)

The workspace's knowledge discipline compresses to two invariants plus a promotion rule. Everything an AI or skill writes follows them; the reason each exists matters more than the mechanics.

**Invariant 1 — uniform timestamps.** Every created file carries lean frontmatter: `name`, one-line `description`, `created: YYYY-MM-DD` (ISO, always), optional `tags`/`status`, and links to related files. The frontmatter is the queryable layer, the prose body is the human layer, the links are the graph. Humans retrieve episodically ("that idea from last week") — a uniform date field turns that retrieval into a filter instead of a hunt. The AI pays this tax at write time so the human never pays it at read time.

**Invariant 2 — reachability.** Every file either lives in a directory whose index is listed in the root map (`_os-map.md`, linked from `AGENTS.md`), or is linked from a file that is. The inbox (`os-inputs/_os-inbox.md`) is the one sanctioned home for orphans — an inbox entry *means* "captured, not yet attached." This makes the whole graph discipline mechanically checkable: os-capture's `audit` mode reports files unreachable from the root map. Discovery cost stays constant regardless of corpus size: read the map, hop to an index, grep.

**Promotion rule — structure is earned, not anticipated.** One artifact goes in the broadest existing home with good frontmatter — for work a skill produced, that home is `os-outputs/`; for reference material a skill will later consume, it's the matching `os-inputs/` subdirectory. When a cluster forms (~3 related artifacts, or fewer plus stated intent to return), it earns a *hub note* — one file naming the idea, its current state, and links to every artifact. A hub gets its own directory only when it's crowded with active work across types. A split may be *proposed* when either test fires — a downstream consumer exists (per the coherence doctrine in `os-references/personal-os-system.md`) or mass has accumulated — and proceeds without asking only when both do. Additive moves (frontmatter, index lines, hub notes) are silent; reorganizing moves (new directories, renames) get a one-line proposal first, because moving things edits the user's spatial memory.

**Boundary — AI memory vs. workspace.** Harness-level memory (e.g., Claude Code's memory dir) holds facts about the *user and how to work with them*. The workspace holds the *work*. Memory may point into the workspace; it never duplicates workspace content — duplication across the boundary creates the two-sources-of-truth drift this whole section exists to prevent.
