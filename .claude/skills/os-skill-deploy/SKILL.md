---
name: os-skill-deploy
version: 0.1.0
description: >-
  Manage the edit-here / deploy-to-harness loop for the skills in this vault.
  Portable local deployment uses the Agent Skills standard at ~/.agents/skills/;
  Claude Code can also use its explicit ~/.claude/skills/ compatibility surface.
  Claude Cowork and web Chat hydrate from the
  Anthropic cloud account and only update on manual zip upload via
  claude.ai → Customize → Skills. This skill wraps the `bin/skill-deploy`
  Python tool that hashes each skill folder (including the shared references
  it bundles), tracks the last uploaded hash in `.skill-manifest.json`,
  surfaces drift, zips skills with the correct single top-level folder
  structure, and creates local harness skill symlinks.
  Triggers on "deploy a skill," "which skills have drifted," "zip my skills for
  upload," "check skill sync status," "skill sync," "push my skills to cloud,"
  "mark this skill uploaded," "link my skills into my agent harness." Do NOT trigger
  for authoring skill content (use `os-tune`).
display_name: Skill Deploy
tagline: Keep your skills in sync across local agent harnesses and Claude's cloud surfaces.
category: Meta
packs:
  - personal-os
icon: 'phosphor:CloudArrowUp'
when_to_use: >-
  Reach for this when you've been improving your skills and want the changes to
  show up across your local agent harnesses and Claude's cloud surfaces. Here's the
  catch it solves: filesystem-based harnesses can read your skills locally, so your
  edits are live there instantly. But Claude on the web and in Cowork don't — they
  only update when you hand them a fresh copy, so your skills quietly fall out of
  date on those surfaces. This keeps track of which ones have changed since you
  last updated them, packages them up the right way, and walks you through dropping
  them into claude.ai so every surface is running the same version.


  Run it whenever you've tweaked a skill and want the web and Cowork side to catch
  up.
modes:
  - name: status
    job: Show which skills have drifted, are new, or still need uploading.
  - name: zip
    job: Package the drifted skills into correctly-structured zips for upload.
  - name: mark-uploaded
    job: Record skills as uploaded after the manual claude.ai step.
  - name: link
    job: Symlink vault skills into the standard Agent Skills location or an explicit harness compatibility location.
  - name: unlink
    job: Remove a skill's symlink.
surfaces: [code]
---

# skill-deploy

The vault is the source of truth for every skill. Local and cloud consumers use different sync paths:

- **Agent Skills standard** uses `~/.agents/skills/<name>/` for user-wide skills. This is the default portable local deployment surface.
- **Claude Code compatibility** may also use `~/.claude/skills/<name>/`. This remains an explicit Claude-specific surface; standardization does not remove or overwrite it.
- **Cowork + web Chat** hydrate from the operator's Anthropic cloud account. The only way in is to zip a skill folder and upload it at claude.ai → Customize → Skills. One upload covers both surfaces after an app restart.

This skill drives `bin/skill-deploy`, which tracks what's drifted, builds correctly structured zips, and creates the symlinks.

## When to invoke

- The user asks about sync status, drift, what needs uploading, or how to push skills to Cowork / web.
- The user wants to zip one or more skills for the upload step.
- The user just edited a skill and wants to know if anything else changed.
- The user is setting up a fresh machine and wants local skill symlinks created.

## Tool surface

The script ships inside this skill at `bin/skill-deploy`. Recommended install: symlink it onto PATH (`ln -sf "$(pwd)/skills/os-skill-deploy/bin/skill-deploy" ~/.local/bin/skill-deploy`). Once on PATH, run `skill-deploy <cmd>` from anywhere inside the vault — the script walks up from CWD to find a directory containing `skills/` or `.skill-manifest.json`. Override with `SKILL_VAULT_ROOT=...` env var if needed.

The script discovers skills under `skills/*` automatically — shipped and user-made alike; all skills live in `skills/`.

`link` manages user-wide deployment surfaces. Guided setup separately wires the workspace-standard `<workspace>/.agents/skills/` surface (and `.claude/skills/` when Claude Code compatibility is selected), because those links belong to the workspace scaffold rather than the user's global skill library.

| Command | What it does |
|---|---|
| `skill-deploy` (no args) | Default: `status`. |
| `skill-deploy status` | Table per skill: `clean` / `drifted` / `new` / `never-uploaded` / `n/a`. Computes current hash live; compares to manifest. |
| `skill-deploy zip <name>` | Build `dist/<name>.zip` with the required single top-level folder structure. |
| `skill-deploy zip --all-drifted` | Zip every skill that's drifted, new, or never-uploaded. |
| `skill-deploy mark-uploaded <name>` | Record current hash as the uploaded one. Honor-system; run *after* the upload at claude.ai. |
| `skill-deploy mark-uploaded --all-zipped` | Mark every name currently in `dist/` as uploaded. |
| `skill-deploy link [--target agents\|claude\|all]` | Idempotently symlink every vault skill into the standard Agent Skills directory and/or Claude Code's explicit compatibility directory. Defaults to `agents`; warns (does not overwrite) on conflicts. Legacy `--target codex` remains an alias for `agents`. |
| `skill-deploy unlink <name>` | Remove one symlink. |

## How to talk about output

`status` returns a colored table — `clean` green, `drifted` yellow, `new` blue, `never-uploaded` gray, `n/a` gray (skill marked `surfaces: [code]` only, so it doesn't ship to cloud at all). After running it, summarize what matters: how many drifted, which ones, and offer to zip the drifted set as the natural next step.

For `zip`, surface the absolute zip path(s) so the user can drag straight into Customize → Skills. After a batch zip, remind them they'll run `mark-uploaded --all-zipped` after the upload completes — don't run it preemptively.

For `link`, surface conflicts explicitly. A real (non-symlink) directory at the selected harness path means a prior non-vault install; the user decides whether to remove it.

## Shared-reference bundling (cloud-surface fix)

Skills that load files from `<workspace>/skills/_shared/references/` work fine on filesystem-resolving surfaces (Code, Codex) because the relative path traverses through the symlinked skill folder back to the workspace's `_shared/` tree. Cloud surfaces have no such traversal — the zip Cowork extracts contains only the skill's own folder, so a `../_shared/references/<name>.md` load resolves to nothing once uploaded.

`skill-deploy zip` handles this transparently. Every zip operation:

1. Scans the skill's body files (`SKILL.md`, anything under `modes/`, `references/`, `templates/`) for relative-path loads of the form `(../)*_shared/references/<name>.md`.
2. Finds each referenced file at `<vault>/skills/_shared/references/<name>.md` and includes it in the zip at `<skill-name>/_shared-refs/<name>.md` — a flat sub-folder inside the skill itself, deliberately not named `references/` so it doesn't collide with the skill's own internal references.
3. Rewrites the shared-ref paths in the body files *as written into the zip* so they point at the bundled copies. Depth-aware: `SKILL.md`'s `../_shared/references/<name>.md` becomes `_shared-refs/<name>.md`; a mode file's `../../_shared/references/<name>.md` becomes `../_shared-refs/<name>.md`.
4. Recurses one level — if a bundled shared-ref itself references another shared-ref, the second one is also bundled. Deeper chains emit a warning naming the chain so the author can flatten.

The workspace source-of-truth files are never modified. Only the zipped copies carry rewritten paths. Code and Codex keep reading the originals via the original paths; Cowork reads the bundled copies via the rewritten paths. No surface ends up with a broken reference.

When a shared-ref path appears in the skill body but the file doesn't exist at the expected location, the zip step reports a `missing shared ref` error naming the path and the body file that loads it, and aborts that skill's zip — a zip built without the file would break on cloud surfaces.

Drift detection covers shared refs too: each skill's hash folds in the content of every shared reference it bundles, so editing a file under `skills/_shared/references/` flips all of its consumer skills to `drifted` on the next `status` — the signal to re-zip and re-upload them.

If the zip output shows a `_shared-refs/` folder you didn't put there, that's this — the bundling that makes the cloud copy work.

## Frontmatter convention

Optional `surfaces:` in each SKILL.md. Values: `code`, `cowork`, `web`. Absent = all three. A skill with `surfaces: [code]` is N/A for upload and gets skipped by `--all-drifted` — useful for skills that only make sense with full filesystem access.

## Honor-system caveat

`mark-uploaded` is the only manual checkpoint. The script can't verify the upload actually landed in the cloud — only that the user said it did. If something drifts back to `drifted` immediately after marking, that means the skill was edited between zip and mark; re-zip.

## The two manifests

The workspace carries two manifest files with different jobs — don't conflate them:

- **`.os-manifest.json`** (vault root, written at install by os-guided-setup) — the *release baseline*: what the installed Personal OS version shipped, file by file. It answers "what did the release ship vs. what did the user change." Owned by os-guided-setup's `update` mode; this skill never writes it. Canonical record — losing it degrades future updates.
- **`.skill-manifest.json`** (vault root, written by this skill) — *machine-local deploy state*: current skill hashes + what's been uploaded to which cloud surface. It answers "what's on this machine vs. what's in the cloud." Derived state — rebuildable anytime by rescanning.

The seam between them is expected behavior: after os-guided-setup `update` refreshes skills, this skill's `status` will report those skills as changed and due for re-upload. That's correct — the cloud copies genuinely are outdated. Run the re-upload; don't treat the flags as drift errors.

## .skillignore

Any skill folder may contain a `.skillignore` file listing patterns to exclude from hashing and zips (secrets, local scratch, large fixtures). Patterns use Python `fnmatch` semantics, **not** gitignore semantics — a bare directory pattern like `modes/` matches nothing; write `modes/*` to exclude a directory's contents. Python cache folders, `.DS_Store`, `.git`, and the `.skillignore` file itself are always excluded. The manifest is backed up to `.skill-manifest.json.bak` before each save.

## Doctrine: no plugins

Personal OS deliberately does NOT distribute as a plugin — not to Cowork, not to web Chat, not to Claude Code. Plugins create complex update friction — a buyer can't iterate their own skills inside a plugin without a full plugin republish cycle. That contradicts Personal OS's entire premise (users evolve and refine their skills over time based on real use). The manual zip+upload via `skill-deploy` is also imperfect, but it preserves the buyer's edit → reload → use cadence. Hopefully Claude's cloud surfaces improve their own update story; until then, this is the chosen friction.

If you're tempted to wrap Personal OS skills as a plugin to "make distribution cleaner," don't — re-read this section and `_shared/references/workspace-layout.md`'s no-plugins doctrine.

## Cross-harness adaptation

Cloud upload status remains specific to Claude surfaces because that's where Anthropic's centralized cloud + claude.ai upload story exists. Local deployment defaults to the cross-harness Agent Skills standard: `skill-deploy link --target agents` links into `~/.agents/skills/`, and every later edit or update propagates with zero further steps. Codex is a consumer of that standard; `--target codex` remains only as a backward-compatible alias. Claude Code's `.claude/skills/` path remains a separate, clearly labeled compatibility target. For a harness that does not consume `.agents/skills/`, research and use its own location without overwriting another harness's working surface.

For unfamiliar harnesses, apply the cross-harness adaptation directive at `_shared/references/cross-harness-adaptation.md`. Research whether the harness has a cloud surface analogous to Cowork, whether it has a filesystem skill location, what the manual sync story (if any) looks like — and update this SKILL.md with what was learned.

## Related references

- `_shared/references/workspace-layout.md` — the cross-surface distribution model this skill is one piece of
- `_shared/references/cross-harness-adaptation.md` — the directive for handling non-first-class harnesses
- `os-guided-setup` — wires `skill-deploy` onto PATH during first install
