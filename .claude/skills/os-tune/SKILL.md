---
name: os-tune
version: 0.1.0
description: >-
  The meta-skill of Personal OS — the inheritance layer that makes skills
  tuned here different from skills tuned in a fresh chat. Five
  modes: `distill`, `extend`, `refine`, `close-out`, `reflect`. (Generation lives in the
  sibling `os-skillify` skill — os-tune's `figure it out` router calls os-skillify
  when the routing decision lands on "make.") Loads voiceprint, conventions,
  skills inventory, recent inbox entries, and system tracker before any mode
  runs — that load is the moat. Triggers on "figure it out," "tune this
  skill," "I keep doing X — turn it into a skill," "extend this skill," "fold
  this into my email skill," "what patterns have I been hitting." Do NOT trigger for writing prose (use `os-writing`),
  generating a new skill from a prompt or content (use `os-skillify`), or
  storing references (use `os-library/save`).
display_name: os-tune
tagline: 'Tune the skills in your Personal OS — extend, refine, reflect.'
category: Planning
packs:
  - personal-os
icon: 'phosphor:ArrowsClockwise'
when_to_use: >-
  os-tune is the inheritance layer that makes skills generated here different from
  skills generated in a fresh chat. It loads your voiceprint, conventions,
  skills inventory, recent inbox entries, and system tracker before any mode
  runs — that *load* is the moat.


  Use `extend` to add capability to an existing skill. Use `refine` to improve
  one. Use `close-out` at session end. Use `reflect` to surface patterns across
  recent work, and `distill` to turn archived threads into the memories reflect
  reads. To make a new skill from a prompt, content, or a stated need,
  os-tune's `figure it out` router hands off to the sibling `os-skillify` skill.
modes:
  - name: distill
    job: Turn archived agent threads into durable memories under `os-memory/` before the harness deletes them. The input side of `reflect`.
  - name: extend
    job: Add a mode or capability to an existing skill.
  - name: refine
    job: Improve an existing skill in place.
  - name: close-out
    job: End-of-session capture and routing.
  - name: reflect
    job: Surface skill-able patterns across recent skill-usage logs.
---

# os-tune — extend, refine, and reflect on the skills in your Personal OS

## Purpose

os-tune is the meta-skill at the heart of Personal OS. The same operation set used to grow the OS — make a skill, refine it as it gets used, extend it when scope expands — is what os-tune gives you.

It's the integration moat for Personal OS. A skill tuned inside os-tune inherits everything the OS already knows about you (voice, conventions, library, existing-skills inventory, recent feedback in `os-inputs/_os-inbox.md`). A skill made anywhere else — a fresh Claude tab, a new GPT, your harness's stock skill-builder (`skill-creator` in Claude and Codex; most harnesses ship something equivalent under some name) — starts from a blank slate. The inheritance is the differentiator: a skill made inside Personal OS is meaningfully different from a skill made anywhere else, because the loaded context shapes every generated and modified line.

## When to use

Common triggers:

- *"Figure it out."* (with a need or recent friction described) → routing decides among make (hands off to `os-skillify`) / extend / refine
- *"Make me a skill that…"* → routes to sibling `os-skillify` skill
- *"I keep doing X — turn it into a skill."* → routes to sibling `os-skillify` skill after map-before-make check
- *"Build me a tool from this content / transcript / article."* → routes to sibling `os-skillify` skill (content path)
- *"Extend my email skill to handle X."* → `extend` with named target
- *"Update this skill so it [does Y by default]."* → `refine`
- *"This isn't quite right — fix the skill."* → `refine`
- *"Fold this into my email skill."* → `refine`

Don't fire for:

- Generating a skill from a prompt or content → `os-skillify` (sibling skill, called by os-tune's router)
- Writing prose for an audience → `os-writing`
- Storing reference inputs → `os-library/save`
- Extracting insights from content as thinking artifacts → `os-content-discovery/explore` or `os-content-mining`

## Modes (v0.2)

| Mode | Job | When |
|---|---|---|
| `distill` | Turn archived threads into memories in `os-memory/` | Weekly, before the harness deletes the transcripts it reads |
| `extend` | Add a mode to an existing skill | The ask is coherent with a skill the user already has |
| `refine` | Fold a tweak / feedback into an existing skill | The user ran a skill, edited the output, and wants the skill itself updated |
| `close-out` | Capture end-of-session learnings | User wraps up a working session; os-tune reads what happened and proposes durable lessons |
| `reflect` | Surface longer-cadence patterns | Weekly/monthly cadence; os-tune reads accumulated inbox + skill-usage logs and proposes consolidations or new skills based on accumulated patterns |

**Generation lives in the sibling `os-skillify` skill.** When os-tune's `figure it out` router decides the right action is to make a new skill (rather than extend / refine an existing one), it hands off to os-skillify, which carries the four input-shape sub-modes (`from-prompt`, `from-content`, `microtool-from-content`, `microtool-from-job`). See `../os-skillify/SKILL.md`.

**Seeing across sessions.** A harness thread can't see the thread before it, so the substitute is written down. Several things write: `close-out` deposits what a session's participant saw into `os-inputs/_os-inbox.md`; `distill` builds memories from past transcripts into `os-memory/`; the harness's invocation log records which skills ran, when the user has wired it. None of those is the remembering — `reflect` is, because it's the one that reads all of them together and finds the pattern. The promise ("os-tune notices your patterns") rests on reflect having something to read, which is why the writers matter even though none of them is doing the noticing.

## The "Figure it out" entry

The user-facing front door is the phrase *"Figure it out."* The user says it (or an equivalent — *"this keeps coming up, handle it"* / *"make this a thing"*) along with their need. The os-tune:

1. Loads Personal OS context per `references/inheritance-protocol.md`
2. Runs the routing decision tree in `references/figure-it-out-routing.md` (refine candidate? extend candidate? otherwise os-skillify? if os-skillify, which sub-mode?)
3. Surfaces the chosen mode and target with rationale (*"Reading this as a refine on your email skill — the recent invocation captured in inbox.md matches"*)
4. Awaits user confirmation before any file changes
5. Routes to the chosen mode

The user can short-circuit by naming the mode explicitly — *"skillify this"* (routes directly to the sibling `os-skillify` skill), *"extend my email skill,"* *"refine the daily assist skill"* — and routing is bypassed. The graceful-degradation rule still applies: if the named target doesn't exist, surface the gap rather than silently approximating.

## Inheritance from Personal OS

os-tune's value collapses without inheritance. Before any mode runs, os-tune loads:

1. **Identity.** `os-inputs/_os-user-profile.md` — drives the implied-author rule for voiceprint matching
2. **Voiceprint.** Per matching-discipline, the user's default voiceprint scoped to the skill being made/touched
3. **Conventions.** `AGENTS.md` (and companion files like `os-inputs/<org>-rules.md`) — operating principles new/modified skills must comply with
4. **Skills inventory.** Scans `skills/` (and the harness's own skills directory if the user keeps extras there) to know what already exists; Personal OS skills carry the `os-`/`dev-` prefixes, and canonical-vs-customized is determined by manifest membership and hash (`.os-manifest.json`) — a skill directory not in the manifest is the user's own; a manifest skill whose hash differs carries user customizations (used by routing for map-before-make and by `extend`/`refine` to avoid overwriting customizations)
5. **Brief.** If a brief in `os-inputs/briefs/current/` matches the project context
6. **Inbox.** `os-inputs/_os-inbox.md` — recent corrections and captures, especially relevant for `refine`'s inline path
7. **Setup philosophy.** `os-inputs/_os-setup-philosophy.md` — the user's stated preferences about how their OS should evolve. Tier thresholds, what os-tune should/shouldn't auto-touch, opt-outs. Configurable per user.
8. **Skill-usage signals (two channels).** Cross-session pattern detection runs on the harness invocation log when the user wired it (skill invocations and frequency — read via `scripts/skill_usage_report.py`) plus `os-inputs/_os-inbox.md` task-audit lines (`[type: audit] [skill: none] [task: <slug>]` — substantive non-skill work, drives make-skill candidate detection via verbatim-Request clustering). Privacy configurable per `_os-setup-philosophy.md`. Full spec: `_shared/references/skill-usage-logging.md`.
9. **Tracker.** The user's active task backlog (managed by the Tracker skill, pluggable across Bear/Apple Notes/Obsidian/Markdown). os-tune reads recent and repeating tracker entries to know *intent* — what the user is trying to do. A repeating entry like "draft client follow-up email" becomes a make-skill candidate. The system context (`os-tracker/system.md`) carries ongoing Personal OS system work so os-tune avoids restarting refinements already in flight. Distinct from inbox: tracker = the work itself; inbox = signal *about* the work. See `os-inputs/_os-inbox-conventions.md`.
10. **Org rules.** `os-inputs/<org>-rules.md` (when present) — per-org operating rules layered onto voiceprint: voice/positioning constraints, jargon avoidance, pricing or business rules. Optional. When present, generated content complies; when absent, voiceprint alone carries voice.
11. **Capture decision tree.** `skills/_shared/references/capture-decision-tree.md` — behavioral inheritance for capture-related os-tune work. When an os-tune mode itself captures content (e.g., `refine`'s inline-after-running path), it applies the same lane-picking logic that workspace-wide capture follows: direct route, sub-agent for heavy work, inbox only when queueing earns its place.

Full protocol in `references/inheritance-protocol.md`. Graceful degradation when sources are missing — os-tune surfaces the gap and asks rather than silently approximating.

## Operating principles

- **Map before make.** Always check the skills inventory before generating new files. Duplication is the failure mode.
- **Dry-run before write.** Every file proposal — new skill, new mode, modified mode, edited principle — surfaces as a diff for user approval before persisting. Inheritance from `AGENTS.md`'s mutation discipline.
- **Tiered approval.** Trivial fixes (output formatting that conforms to existing principles, defaults that match patterns already locked in) auto-apply with audit trail. Moderate changes (principle additions, mode behavior changes) ask before applying. Large changes (new skills, new modes, purpose edits) propose with alternatives and require confirm. Tiers and thresholds in `references/approval-tiers.md`; user-configurable via `_os-setup-philosophy.md`.
- **Minimum viable edit.** `refine` makes the smallest change that accomplishes the user's intent. No drive-by refactors.
- **Surface the route.** When the user's ask doesn't fit cleanly in one mode (e.g., a "tweak" that's actually a new skill), os-tune surfaces the alternative routing rather than forcing the wrong fit.
- **Skills ship empty.** Per `AGENTS.md`, skills generated for distribution carry no user-specific data inline. Per-context profiles populate at runtime.
- **No silent approximation.** When inheritance sources are missing, os-tune surfaces the gap.
- **Capture corrections in inbox; track active work in system tracker.** When `refine` (or `extend`) fires inline, the *correction* (the tweak pattern that should generalize) gets logged to `os-inputs/_os-inbox.md` as `[type: correction]`. The *active refinement / extension task* gets written to `os-tracker/system.md` via `os-tracker/add` so it's visible as work-in-progress. See `os-inputs/_os-inbox-conventions.md` for the full model.
- **Respect customizations.** os-tune reads each skill's `version` tag and tracks delta to user customization. When refining or extending a customized skill, os-tune never overwrites the customization without explicit consent — the user's version is the source of truth, not the canonical.
- **Proactive prompting once per session.** When a strong pattern is detected from recent inbox + skill-usage logs, os-tune surfaces a single short pattern observation paired with one clear offer — surface what's been happening, name the candidate action, leave the decision with the user. One offer per pattern per session; the goal is useful, not interruptive. Configurable in `_os-setup-philosophy.md`. The session-start scan that triggers this is manual in v1 (the AI runs it when a fresh session opens with the right cues); the intended pairing is for `os-guided-setup` to wire it as a recurring scheduled automation alongside `os-autosave`'s schedule, so the proactive-prompting cadence is a side-effect of how the OS already runs rather than a separate ritual.
- **Wrap, don't reimplement.** The sibling `os-skillify` skill delegates structural skill generation to a stock skill-builder (`anthropic-skills:skill-creator` where it exists; otherwise the harness's nearest equivalent) and post-processes with inheritance + voiceprint + conventions. os-tune's value (when it routes to os-skillify) is the layer on top — gates, voice, convention compliance, existing-skill awareness — not the underlying generator.

## os-tune is additive — the repertoire of patterns grows with use

The five modes are stable, but the *patterns* os-tune notices and acts on are not. New refine candidates, new extend shapes, new reflect signals emerge as the user's skill library and feedback history grow. When os-tune encounters a tuning pattern it doesn't have crisp routing for, the right response is three-beat: name the gap honestly (*"this looks like a tweak that fights the host skill's purpose — that's not a shape I have a clean route for yet"*), offer two paths (handle this one inline as a one-off, or set up a small reusable pattern for the next time), and hand off cleanly to `os-skillify` if the pattern is new-skill-shaped. The self-extending disposition lives in `_shared/references/self-extending-skills.md` and is loaded by every mode that writes to a skill file.

## Related skills

- `os-skillify` — sibling skill. Generation lives here. os-tune's `figure it out` router hands off to os-skillify when the decision lands on "make."
- `os-library` — stores produced tools and reference inputs; provides matching-discipline that os-tune inherits
- `os-voiceprint` — produces voiceprints; chained when generated skills need voice and none exists in the library
- `os-writing` — consumer of os-tune's outputs in many cases
- `os-content-mining` — adjacent extraction skill; os-tune uses similar internals for content-driven the os-skillify handoff
