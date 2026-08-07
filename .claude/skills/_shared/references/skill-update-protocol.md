# Skill update protocol

Shared write-discipline for any operation that creates or modifies skill files. Loaded by `refine`, `extend`, and the four `skillify-*` sub-modes. Mode-specific concerns layer on top.

This protocol is for *skill-file mutations* specifically. Tracker writes through its own contract (`skills/os-tracker/references/contract.md`); capture writes through its own conventions; this protocol stays focused on skill files (SKILL.md, mode files, references, templates).

## Two write modes

Skill-file work splits into two shapes. The protocol covers both, with branches where they diverge.

**Modify** — an existing file changes. The original content is the starting state; the proposed change is computed against it. Customization respect applies. Used by `refine` (output tweaks fold into existing skills), `extend` (the parent SKILL.md gets its mode index updated), and any future bundled-update mechanism.

**Create** — a new file is written where none existed. No prior state; no diff to compute. Customization respect doesn't apply (the file didn't exist; nothing was customized). Used by `extend` (the new mode file itself), and by all four `skillify-*` sub-modes.

A single os-tune operation may involve both — `extend` creates a new mode file (Create) and modifies SKILL.md to register it (Modify). The protocol applies to each file write per its mode.

## Show before write

Dry-run is the default for every write. The mode surfaces the proposed change before persistence and waits for explicit confirmation. Three pieces:

**For Modify:** Surface a diff against the current file. Show what's changing — added lines, removed lines, modified lines — with enough surrounding context that the user can judge intent. Don't surface the whole file unless the diff is substantial enough that the diff itself becomes harder to read than the result.

**For Create:** Surface the full proposed file content with its target path. The user sees what will be written and where. Frontmatter, body, and structural conventions all visible before write.

**For multi-file operations** (e.g., `extend` writing the new mode + updating SKILL.md, or `os-skillify/from-content` producing 1-N modes + references): surface all proposed changes as a batch. The user confirms once for the batch. If a single file in the batch fails its sanity check after write, the whole batch is reverted (file system permits) or the failure is surfaced explicitly so the user can fix and rerun.

After surfacing, wait for confirmation. The user's options: accept (proceed with write), accept with edits (the user adjusts before confirming), reject (no write happens), or defer (save the proposal somewhere for later — typically inbox as `[type: capture]`). Don't write without one of these signals.

The confirmation step matches os-tune's tier vocabulary. Trivial-tier changes (adding a line to a list, fixing a typo) can opt into single-confirm batches per `_os-setup-philosophy.md`. Moderate and large always ask per item.

## Customization respect

For Modify operations, respect user customizations. The discipline is **always diff, never silent overwrite** — even when an automatic mechanism (e.g., a future os-tune update) initiates the change, the user sees the diff and confirms before the file changes.

At v0.1, customization respect is behavior-only. The mode never silently overwrites because dry-run is mandatory; the user sees what's changing and can stop it. No detection plumbing is needed.

When detection ships (forward-looking — likely tied to a os-tune auto-update mechanism), the `version` frontmatter field is the comparison anchor. If the file's content differs from what shipped at its `version`, the file is customized. The mode then surfaces the customization explicitly: *"this skill is customized from the shipped version 0.1.0 — proposed update may conflict; review carefully."* The dry-run-and-confirm discipline still covers the actual mutation; the detection just adds a heads-up.

For Create operations, customization respect doesn't apply (no prior state to respect). The protocol skips this section for create-mode writes.

## Sanity checks

After every write — Modify or Create — run sanity checks to catch breakage before the user moves on:

- **Frontmatter parses.** YAML validates; required fields (`name`, `description`) present; `name` matches directory name (per `frontmatter-format.md` Rule 1); description is at most 1024 characters (Rule 3).
- **Markdown structure intact.** Headers nest sensibly, no truncated code fences, no orphan list items.
- **Cross-references resolve.** Every `path/to/file.md` mentioned in the file points at something that exists on disk. Same for `../references/<name>.md` and `../../_shared/references/<name>.md` style relative paths.
- **No broken sibling references.** If the file references a sibling skill or mode, that target still exists and is accessible (handles the case where a file move broke a reference).

If a sanity check fails, surface the failure to the user immediately. Don't silently accept broken state. Two paths from there:

- **Fixable inline** — the failure is small (typo in a path, missing required field). Propose the fix; user confirms; rerun sanity checks.
- **Not fixable inline** — the failure indicates the proposed change was structurally wrong. Revert the write if the file system permits; otherwise surface the bad state and ask the user to correct manually before continuing.

For multi-file batch operations, run sanity checks per file after each write. If any fail, halt the batch and surface — don't continue writing potentially-broken files on top of an already-broken one.

## Reference from consumer modes

os-tune modes that perform skill-file writes reference this protocol rather than restating its prose. The expected pattern in each mode's "Operating principles" section:

> **Writes follow `_shared/references/skill-update-protocol.md`.** Plus the mode-specific concerns below.

Mode-specific concerns to keep inline:
- `refine` — minimum-viable-edit (no drive-by refactors); preserve existing skill's craft
- `extend` — two files change together (new mode + SKILL.md mode index); both diffs surface in the same batch; don't break existing modes
- `os-skillify/from-prompt` — 6-phase workflow (classify → rationale → destination → build → verify → log) with the build phase using this protocol
- `os-skillify/from-content` — content-craft preservation (mirror frameworks, lift verbatim, mirror step-counts) for content the build phase consumes
- `os-skillify/microtool-from-content` — 7-section microtool anatomy in the build phase
- `os-skillify/microtool-from-job` — clarification interview when the need is thin; build phase same as siblings

The protocol covers the *how to write safely*; mode-specific concerns cover the *what each mode produces*.

## See also

- `_shared/references/frontmatter-format.md` — frontmatter rules sanity checks enforce; also documents the `version` field convention
- `_shared/references/skill-vs-mode-vs-reference.md` — destination decision tree for what gets created during `os-skillify/from-prompt`'s Phase 3
- `_shared/references/scaffolding-patterns.md` — three-question scaffolding assessment used during Phase 1 classification
- `skills/os-tune/references/inheritance-protocol.md` — the read-side companion (what os-tune loads before any mode runs); this protocol covers the write-side
- `skills/os-tracker/references/contract.md` — separate write contract for tracker mutations; not covered by this protocol

## Future split

If a third write-context emerges (e.g., a Knowledge writer skill, a Brief manager) that shares enough of this discipline, promote the dry-run / sanity-check core to a more generic `mutation-protocol.md` under `_shared/references/` and keep skill-update-protocol as the skill-files specialization. For v0.1, the two-skill-context threshold (Tracker has its own; this protocol covers six modes' shared discipline) doesn't yet justify that split — the doc stays as one.
