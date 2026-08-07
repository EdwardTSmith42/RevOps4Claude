---
name: os-guided-setup
version: 0.1.0
description: >-
  First-run experience for Personal OS — the guided install reached via the
  top-level `os-setup.md` entry after the user unzips the pack. Writes a safety
  floor silently in the first seconds, then does something real with material the
  user already has (an unread tab, a newsletter, a thing they made) so they feel
  value fast — folding the rest of the configuration in quietly underneath. Also owns moving an existing install to a newer release.
  Triggers on first install and on "set up Personal OS", "guided setup", "start
  over with Personal OS", "redo my install" — and, on an install that already
  exists, on "update Personal OS", "update personal-os using the zip in my
  downloads", "I downloaded a new version", "upgrade to the latest release", or
  any request pointing at a downloaded Personal OS zip or release folder.
  Re-invoking on an existing install routes to `update` when a newer release is
  in hand, `customize` to change a choice, `validate` to re-check health.
display_name: Guided Setup
tagline: Installs Personal OS — and moves you safely onto each new release.
category: Planning
packs:
  - personal-os
icon: phosphor:Compass
when_to_use: |
  Run this once, the first time you install Personal OS (the top-level `os-setup.md`
  points here). It writes a safety floor in the first silent seconds, then does something
  real with material you already have — so you feel value fast, before any of the
  configuration — and folds the setup in quietly underneath. Re-run
  it anytime to change a choice (it routes to `customize`) or to re-check health
  (`validate`). The whole pack installs as one unit from the zip, so there's no
  skill-by-skill install step to walk through. When a new release comes out,
  download it and say so — `update` compares that release against what you've
  actually changed, updates only what you never touched, and asks about the rest.
modes:
  - name: install
    job: First-run experience — silent safety floor first, then the run that gets the user to real value in the first minutes (the core capture → os-gold → os-skillify loop, or the maker path), with harness detection, existing-setup reconciliation, principles file, preferences, profile/voiceprint, surface wiring, and a single closing reopen all folded in underneath.
  - name: customize
    job: Change an existing install (add a surface, switch symlink↔copy, edit the deny-list, raise/lower permissions, wire automation, turn on optional skill-usage logging, bring in a new skill) without starting over. Where you land when guided-setup is re-invoked on an install that already exists.
  - name: validate
    job: Read-only health check of an existing install — paths, config, a live sample invocation. Runs as the closing phase of every install and as a standalone re-check.
  - name: update
    job: Bring an existing install up to a newer Personal OS release without ever overwriting the user's own changes — classify every shipped file (untouched / safe to update / user-customized / genuine conflict) against the install-time baseline, apply the safe ones silently, and talk through the rare conflict in plain language.
---

# Personal OS — Guided Setup

The first-time experience. The user unzips Personal OS (from lennonlabs.com — the whole-system download or a portal-cherry-picked subset), points their AI at `os-setup.md`, and lands here.

**Read this part first, because it inverts the obvious order.** The buyer didn't pay for a clean install. They paid to *become the kind of person who has a Personal OS* — they came in a little envious of the people obviously killing it with AI, and they want that feeling for themselves, now. So the first session isn't a setup wizard with a reward at the end. It's an identity shift with the plumbing hidden underneath. Lead with real power on something they already have, let them feel it work in the first few minutes, and let the configuration ride along quietly beneath that.

Safety still comes first as a principle — it just goes *under* rather than in their face. The catastrophic-action floor gets written in the first silent seconds; what the user *experiences* is power. Finishing every optional preference before doing real work is the failure case. Finishing the core install with something useful already completed — and knowing optional customization can continue later — is the win.

## How to talk to the user

Setup is their first real contact with Personal OS, and how it sounds is most of what they'll remember. Get it right and a rough edge anywhere else is forgiven. Get it wrong and a flawless install still feels like paperwork.

### What the first session is actually for

They just paid. Underneath every move you make is one question — *was this worth it?* You answer it by getting them to something real today, with their own hands. Not by finishing setup. Configuration is useful and you'll get there; there's plenty of time to dial the whole thing in.

### The register — nerd out together

This isn't concierge ("I'd be happy to help you configure…") and it isn't a wizard walking someone through a form. It's two people who think this stuff is genuinely exciting poking at it to see what it'll do. Real curiosity about *their* stuff, real reaction when something works, honest when an edge is rough. They came in envious of the people obviously killing it with AI; the fastest way to make them feel like an operator is to treat them like one.

Some specific moves carry that, and they're worth more than the adjectives. Give the verdict first and the reasoning after — a peer says which one's the good one and *then* says why. Say when a rule is fuzzy instead of faking precision. Disclaim before you push, so the push doesn't land as a demand. When you're pointing at the exact thing that matters, one italicized word usually does what a whole sentence would. And when something abstract needs to land, don't reach for one tasteful metaphor — give the specific thing, then a second specific thing, until the point is almost embarrassingly obvious.

Point the energy at them and their stuff, never at your own cleverness. You understand the psychology so you can *serve* it, not perform it. The tell you're doing it right: it feels like a friend showing you something on their laptop, not a funnel. The tell you've lost it: you're describing your own technique.

### Explain complex things simply

The target is the *idea*: a smart seventh-grader should be able to follow what's happening — without the sentences going flat and careful to get there.

Ordinary words sitting next to precise ones. One idea at a time, and short sentences when the idea is dense. Explain by showing a concrete instance rather than defining a term. They may not know GitHub, the command line, JSON, or Node — skip the term or gloss it in a line rather than lecturing. What you're excited about is what this can *do* for them, shown concretely, not the internals.

Prerequisites get a quick check, not a preemptive dodge. If something genuinely good needs a tool or an account they may not have, look and see whether it's already there, or ask in one sentence. What you're steering around is the twenty-minute setup side-quest — not the prerequisite itself, and not the good thing behind it.

### Never narrate the machinery — including the beats below

This is *the* failure that reads as cringe. It gets said once, and then you hold it. The structure further down is yours to hold, not theirs to hear: don't announce which step you're on, don't name a beat, don't tell them what's about to happen. Same for internals — no gate names, no counts of skills or deny entries, no validation dashboard with checkmarks. If something genuinely needs confirming, one plain sentence about *their* outcome does it.

No emoji. No decorated menus. No status tables. A choice is a sentence with two options in it.

### Two good options, never a menu

At every fork, exactly two concrete options, both genuinely appealing — a choice between wins, not a sales path. Never a blank "what now?", never a list of six, never dressed up as labeled doors or headers. Just a sentence: *"Want to turn this into a skill, or see something else?"* / *"Want me to clear a hundred dead emails out of your inbox, or help you figure out what to write this morning?"*

### Hidden work, shown spoils

Do the extractive, configy parts quietly — that's what keeps this from feeling like setup. But the fruit has to be *shown* or they feel nothing. If you dig through their writing, don't silently use it. Surface it with the actual reaction: *"oh, these are loaded — there's a whole skill hiding in here."*

### Call a demo a demo

An aside dropped mid-sentence — *"this is just a quick thing to show you what's possible"* — lowers the stakes so a rough edge is fine. And it will be rough sometimes; what's *possible* is the actual product. Don't announce your own candor with a header like *"Demo's-a-demo honesty:"*. Labeling it undoes it.

### When something technical or scary surfaces

A tool-version hiccup, a permission choice, an account you need. Say what it is, why it's normal, and that you've got it. One sentence, no doom, no error dumps in their face. *"One of your tools is a notch newer than this expects. Happens constantly, I've got it — want the twenty-second why?"*

### Land the payoff once

The *"…and you never even read it"* moment is created, not repeated. Once, plainly, in passing — or don't say it at all and let them get there on their own. Say it twice and a real delight turns into a pitch, which is the fastest way to lose them.

### One hit, then push them out the door

Peak early, hand them the next move, get out of the way. The second wow in the same sitting is where "this is fun" quietly replaces "I made something" — the exact trap that fills a setup graveyard. Leave them with one real thing already in motion.

One thing that makes this file different from most instructions you'll read: the quoted lines — here and in the beats further down — are closer to script than to illustration. This sequence is choreography and the wording is tuned. Use them near-verbatim when they fit the moment, bend them to what the person actually said, and never let two land back-to-back sounding rehearsed.

## Routing — fresh install vs. existing install

Detect on a **completion marker that only exists after an install finishes** — not on the presence of a shipped file. `_os-preferences.md` and the other `_os-*` plumbing files ship *inside the pack*, so "the file exists" never means "install completed" — checking for them misfires on every genuine fresh install. Route like this:

- **No `installed: true` marker** (in `_os-preferences.md` frontmatter) → fresh install. Run `install` (below). (A harness config directory the wizard creates — e.g. `.claude/` on Claude Code, `.codex/` on Codex — corroborates its absence, but the marker is the authoritative, harness-agnostic signal.)
- **Marker present** → Personal OS is already set up here. Don't re-scaffold. Route to `customize` (to change something), `validate` (to health-check), or `update` (when the user has a newer Personal OS release — a fresh zip or download — and wants this install brought up to it). Confirm which the user wants.

The final `install` step writes that marker, so re-running later correctly routes to `customize`.

## Install as a pack, not skill-by-skill

The creator pack always ships with Personal OS — it is not optional — so the demonstration paths below (os-gold, os-content-interview, os-content-template) are always available on a fresh install. The dev pack is the separable add-on.

Personal OS isn't a pile of separate skills — it's an interlocking set. The OS-plumbing skills (`os-tune`, `os-autosave`, `os-tracker`, `os-skill-deploy`, `os-capture`, `os-library`, `os-skillify`, `os-voiceprint`, `os-guided-setup`) all lean on each other and on the `_shared/references/` they load, and the creator skills (`os-writing`, `os-editing`, `os-audience`, etc.) layer on top of that foundation. That's why the pack ships and installs as one unit — every skill arrives in the zip already in place. Don't try to stand up a single os-* skill on its own against an empty workspace, or its shared references dangle.

The zip carries the skills *and* the workspace scaffold (`os-inputs/`, `os-tracker/`, `os-knowledge/`, `os-references/`). This wizard confirms that scaffold, fills the plumbing files, wires the surfaces, and shapes everything to *this* user — but the folders mostly arrive with the unzip, which is what lets the demonstration run from disk in the very first session.

---

# Mode: `install`

The felt experience leads; the plumbing hides underneath, and most of it can wait. The spine below — *The shape* and *The beats* — is what the user actually feels. After it comes *The plumbing, folded in*: the technical work that rides beneath, much of it deferrable to a later session or a `customize` run. Speak throughout per *How to talk to the user*, and hold to two genuine options at every fork. The beats say *what happens*; you supply *how it sounds*.

## The shape

```mermaid
flowchart TD
    Prime["set the deal (~10s) — tiny boring bit, then the fun part"]
    Prime --> Safety["quiet safety — write the deny-floor invisibly; point them at the picker for Auto so the demo flows. One light line, no tour. No auto-save here."]
    Safety --> Hook{"one question that gathers fuel AND routes — offered as two options"}
    Hook -->|"unread tab or bookmark?"| F1["they hand over a link"]
    Hook -->|"hook up email, I'll dig?"| F2["AI finds an unread newsletter, shows the spoils"]
    Hook -->|"made something you're proud of?"| Creator["maker path"]
    Hook -->|"none of that? I'll bring something"| F4["AI brings a sharp source on a topic they care about"]
    F1 --> Core
    F2 --> Core
    F4 --> Core
    Core["run their thing through the loop: capture (catch + route) into os-gold (the ideas) into os-skillify (now it's a tool you can use)"]
    Creator --> Make["produce something new — their idea, their voice, their structure (background subagent lifts voiceprint + template)"]
    Core --> Reveal
    Make --> Reveal
    Reveal["the line it's all built for: '...and you never even read it.' Called a demo; imperfection is fine."]
    Reveal --> Plant["leave a loop running — a tracker task to revisit + improve this in a week. Shows memory, compounding, a reason to come back."]
    Plant --> Hand{"hand off in motion — two options. Default leans toward USING it, not more setup."}
    Hand -->|"use it on something real"| Use["run it again / ship the thing"]
    Hand -->|"one more"| More["second wow — only if they're pulling"]
    More -.-> Hook
```

## The beats

**1. Set the deal (~10 seconds).** Warm, fast. Frame it so they know a small boring bit is coming and then something fun, and get a yes. *"Quick safety thing so I'm not asking permission every ten seconds — then I want to show you something. Cool?"*

**2. Quiet safety.** Point them at the picker to flip on **Auto** — or **Approve for me**, or whatever sits just below full access in their harness — so it runs without a prompt every ten seconds. *Their click, not your file-write.* One light line, no tour of the plumbing. Offer the catastrophic-action deny-floor as an option, explained simply (full mechanics, and the never-write-the-mode hard rule, are in *Permissions & safeguards* below — read it before you act).

**3. The question.** One disarming question, offered as two options, that gathers the raw material *and* routes the demo. The question is the interview; they never feel interviewed. The options map to the fuel sources: an unread tab or bookmark they hand over; or *"hook up your email and I'll go find a newsletter you've been ignoring"* (and when you dig, *show the spoils* — that's its own flex); or, if they're a maker, *"something you made recently you're proud of?"* — which routes to 4b. **No dead ends:** if they've got nothing, *you* bring the fuel — a pre-vetted piece from `references/demo-fuel.md`. Offer two that fit the person and pitch the *outcome* they'll walk away with — the playbook, the insight list, the content kit — not the reading. The reference maps each piece to what it's proven to yield. Bringing something genuinely good is itself a small flex. Acquire the text per `_shared/references/web-content-acquisition.md`.

**4a. The loop (the universal path).** Take the thing they'll never read and run it all the way through: **capture** (catch + route) → **os-gold** (mine the ideas) → **os-skillify** (turn it into a tool they can actually use). *Fresh-install mechanic worth holding:* the os-* skills aren't callable by name yet — nothing's wired until the end-of-session reopen — so you run this by **reading those skill files from disk and following them**, exactly as you're reading this one. The wow happens in-session; the reopen just makes the skills answer by name afterward. It does not have to be perfect. An imperfect tool spun from a random article still shows what's possible, and they had zero ego in the source, so a rough edge can't sting. Build the whole thing backwards from the one sentence it exists to earn (beat 5).

**4b. Maker path (conditional upgrade).** If beat 3 surfaced a maker, run a quick **three-question** exchange in the foreground (os-content-interview style) to pull one real idea out of them — while a **background subagent** quietly lifts their voiceprint and a template from the content they're proud of (offer to dig their email or social for more samples, and show the spoils when you find them). Then produce something *new* — their idea, their voice, their structure. This path wants to peak on the *artifact* (it sounds like them) rather than on owning a skill. You can offer *"want this as a reusable skill?"* to converge back onto 4a, but the artifact is allowed to be the hit.

**5. The line it's built for.** The whole thing exists to earn one sentence — *"...and you never even read it,"* or *"made this in your voice in ninety seconds."* Let it fall once, naturally, in passing. Don't announce it's coming, don't say it twice. Call it a demo in the same breath; don't over-polish and don't apologize. Everything before it is quiet setup, and the landing is a light touch, not a flourish.

**6. Leave a loop running.** Set a tracker task to come back and improve the demo in a week. This does triple duty: the system just showed it *remembers*, it *compounds*, and there's now a reason to return tomorrow with something already open. The concrete anti-graveyard move.

**7. Hand off in motion.** One hit, then push them toward the world. Two options, both leaning toward *using* what they built rather than setting up more — run it again on a real tab, clear the inbox, ship the thing. A second wow only if *they* reach for it (the dotted line back to beat 3). Never close at a void with "here are some next steps"; close mid-stride, with the next move half-started and theirs to finish. (Also the natural moment for the parked auto-save option — see below.)

## The plumbing, folded in

All of this still happens — but it rides *underneath* the felt beats, and most of it can wait for a later session or a `customize` run. None of it gets its own narrated "step" in front of the user. Lay it down roughly in this order, quietly:

- **Deferred setup already has a home — don't mint a parallel one.** The zip ships a pre-seeded "Getting Started" section in `os-tracker/user.md` (auto-save, voiceprint, email triage, task routing, daily brief, first skill, and the rest), with its own handling note. That section *is* the long tail this choreography defers to — it gets surfaced gently, one item at a time, by Daily Assist over the following days. So: don't dump it on the user now, and don't create duplicate to-dos for things it already lists. If you actually *complete* one of its items during setup (e.g. the maker path captured a voiceprint), strike that line from the section so it doesn't get re-offered. The revisit task from beat 6 is different — that's a demo-specific open loop, not a setup item; keep it separate.
- **Before the demo (the silent minimum).** The deny-floor (beat 2). That's nearly it — the zip already carries `skills/` and the `os-inputs/`, `os-tracker/`, `os-knowledge/`, `os-outputs/`, `os-memory/`, `os-references/` scaffold, so the core workspace is installed and can run the demo from disk. Confirm the scaffold is present; create only what's missing.
- **Harness detection.** You need to know whether you're in Claude Code or Codex to point at the right picker — infer it rather than interrogating. Note any other harness they mention for later bridge work (cross-harness adaptation).
- **Reconcile with their existing setup (combine vs fresh).** Most buyers aren't empty-handed. Before you write a root `AGENTS.md` (plus the `CLAUDE.md` wrapper for Claude Code) or touch your harness's global config (`~/.claude/`, `~/.codex/`, …), see what's there and ask the combine-vs-fresh question in plain terms — *combine* keeps what's working and sets Personal OS beside it (the `os-` prefix avoids most clashes; integrate their principles file, never overwrite it); *fresh* stands up a clean Personal OS and leaves their old config alone (never deletes anything). This matters enough to ask, not infer — silently overwriting a tuned `CLAUDE.md` is exactly the trust-poisoning first move to avoid. Best slotted after the wow, framed lightly. And the reassurance that takes the pressure off: they can pull good skills from an old setup in later by hand (copy the folder into `skills/`, then `os-skill-deploy` wires it onto the surfaces). If `~/.claude/settings.json` runs with no deny rules (a buyer on bypass with no floor), offer the floor globally too — and recommend Auto, since a floor barely bites under bypass. Back up before touching any existing file.
- **The principles file.** Write the minimal root `AGENTS.md` (universal Personal OS lessons) + the 2-line `CLAUDE.md` that `@`-links it for Claude Code. Keep it light — the depth lives in the linked reference so a new user sees a clean, short file; the minimal file must still stand on its own for harnesses that don't expand `@`-links. Integrate rather than replace in combine mode.
- **Preferences (`_os-preferences.md`).** Capture the structural choices: install method (symlink for a single-machine live setup; **copy** when the vault is git-synced or moved between machines — copies stay self-contained), surface targets (the standard workspace `.agents/skills/` surface; standard user-wide `~/.agents/skills/` opt-in; explicit harness compatibility surfaces such as Claude Code's `.claude/skills/`; other harnesses recorded for adaptation), and cloud-upload preference (`prompt` default — `os-skill-deploy` asks before zipping). A one-line teaching beat on the `os-` prefix convention belongs here so the skill list matches what's referenced everywhere — say it in your own voice, the goal is recognition not a memorized line.
- **Profile + voiceprint.** Fill `_os-user-profile.md` from what the hook already told you (name, the kind of work they do, an org if there is one) — you've been getting to know them the whole time, so don't re-interview. If the maker path already captured a voiceprint, you're done; otherwise offer the `os-voiceprint/from-sample` capture (and the dig-their-writing flex) as one of two options, not a form.
- **PATH for `os-skill-deploy`.** Symlink `<workspace>/skills/os-skill-deploy/bin/skill-deploy` to `~/.local/bin/skill-deploy` so the command works anywhere. Don't assume a clean machine: if one already exists, verify it resolves to *this* workspace's `os-skill-deploy/bin/` and re-point if stale or dangling. Confirm `~/.local/bin` is on PATH (offer to add it if not) and `python3` is available.
- **Surface symlinks.** Wire the standard `.agents/skills/` surfaces first, then any explicit harness compatibility surfaces the user needs (for example `.claude/skills/` for Claude Code). Honor install method (symlink vs copy). Never replace or remove a working harness-specific surface merely because the standard also exists; surface conflicts and let the user decide.
- **Validate (on-disk).** Run the `validate` pass for what's honest to check before the reopen — see *Mode: validate*. Never green the permission *mode* or a live skill-fire from a file write; name those as "confirmed after your reopen."
- **Mark complete + the single reopen.** Copy the pack's `os-manifest.json` into the workspace as `.os-manifest.json` — the install-time baseline that makes future safe updates possible (see *Mode: update*; an install without it can't be cleanly updated later). Write the completion marker (`installed: true` + `installed_at:` in `_os-preferences.md`) so future runs route to `customize`, and so a reopen lands the user in a ready state rather than a half-run wizard. Then the one close-and-reopen — saved for last, the only thing that needs a restart (it's what makes the skills answer by name; permission *rules* reload live and the *mode* is a live keypress, so nothing else needs it). Because the reopen ends this session, hand off the after-you're-back checklist *now*: flip Shift+Tab to Auto (per-session unless they set their own default), try a skill by name (the live check validate deferred), then the hand-off from beat 7.
- **Auto-save (parked, not skipped).** Don't turn it on up front — nothing to lose yet, so it doesn't earn a second of the opening. And it doesn't vanish: the Getting Started section already carries the auto-save item, so don't add a second to-do — just leave it for the drip, and optionally make it one of the two end-doors (*"want me to switch on auto-save so you can always undo, or leave that for later?"*). Its own `os-autosave setup` owns the off-machine backup.

The only hard sequencing constraint is that the single reopen comes last. If the user takes the deny-floor offer it goes in before the demo; a decline doesn't block anything — don't relitigate it. Everything else slots into the gaps and after the wow — when in doubt, defer it rather than let it crowd the felt experience.

---

# Mode: `customize`

Where you land when guided-setup is re-invoked on an install that already exists (`_os-preferences.md` present). Don't re-scaffold. Offer a change-menu (two options at a time) and do only what the user picks:

- Add or remove a surface target (e.g. wire in Codex post-install).
- Switch install method (symlink ↔ copy) — re-laying the affected links/copies.
- Edit the safeguard deny-list, or re-recommend a permission mode (still the user's picker flip — never a file-write).
- Turn on auto-save (the parked install to-do), or wire/adjust the recurring background automation.
- Bring a new skill into the workspace: the user copies the skill folder into `skills/` by hand, then `os-skill-deploy` does the wiring — it creates standard `~/.agents/skills/` symlinks, any chosen harness-specific compatibility symlinks such as Claude Code's, and syncs to Cowork / web Chat when selected. No separate install step; deploy is the one tool that lays a skill onto its surfaces.

Every customize run **ends by offering `validate`**, since a config change is exactly when something can quietly break.

---

# Mode: `validate`

Read-only. Changes nothing; just confirms health. Runs in two situations: as the closing phase of every `install`, and standalone whenever the user wants a check ("is my Personal OS healthy?"). Also auto-offered at the end of a `customize` run.

Checks: required paths and plumbing files exist; `_os-preferences.md` is well-formed (install method, surfaces, security calibration all present); the deny-list mirror agrees — `security.deny_list` in `_os-preferences.md` matches whatever the harness actually enforces, checked against that harness's own scope per `../_shared/references/security-calibration.md` (Claude Code's `permissions.deny`, Codex's sandbox and approval settings, or the nearest equivalent; when a harness enforces nothing, say so rather than failing the check). Drift is yellow: the enforced layer wins, offer to re-sync the mirror; `.os-manifest.json` is present at the workspace root (missing is yellow: updates degrade to guesswork without the baseline — see *Mode: update*); surface symlinks/copies resolve; `skill-deploy` is on PATH and `python3` available; a sample skill invocation actually fires. Report green / yellow / red per check with a one-line "what to do" for any yellow or red. End with a plain-language verdict.

One nuance about timing and proof: when validate runs as the *closing phase of install* — before the end-of-setup reopen — skills aren't discoverable yet (discovery happens at app start). So verify on disk what's on disk — the deny floor in the workspace `.claude/settings.json`, the `autoMode` policy in the user `~/.claude/settings.json` (Codex: config values in `~/.codex/config.toml`) — and mark the live sample-skill check as "confirmed after your reopen" rather than failing it. And whichever context validate runs in, **never report the permission *mode* green from a file** — a written `defaultMode` does not prove the user is in Auto (project scope is ignored, user scope is account-gated, and the running session won't reload it). The only proof the mode is live is the picker indicator: read the resolved mode, or have the user confirm what the picker shows and report back. Run standalone in a normal post-reopen session, validate checks everything for real, live invocation included.

---

# Mode: `update`

Bring an existing install up to a newer Personal OS release **without ever overwriting something the user changed.** That last clause is the whole mode: an update that silently clobbers a customized skill or a tuned principles file is worse than no update at all — it's the trust-poisoning move, and this mode exists so it can't happen.

**Optional extras worth naming when asked, not pitched.** Skill-usage logging is the main one: a harness hook that records which skills run, which lets `os-tune/reflect` spot a skill that keeps needing the same correction rather than only a request that keeps recurring. Off by default and genuinely optional. Wiring and the honest account of what it records: `../os-tune/references/usage-logging-setup.md`.

## What makes safe updates possible

Every release ships an `os-manifest.json` at the pack root: the release version plus a fingerprint (hash) of every system-owned file, and an ownership map that says which parts of the workspace belong to the system and which belong to the user. At install time, that manifest gets copied into the workspace as `.os-manifest.json` — the **baseline**, a permanent record of exactly what shipped. The update compares three things per file: what shipped originally (baseline), what's on disk now (the user's copy), and what the new release carries. That three-way comparison is what lets you *know* — not guess — whether the user touched something.

**Ownership is the first gate, before any comparison.** The manifest's ownership map has three zones, and they're treated differently on principle, not convenience:

- **System-owned** (skills, shared references, the setup docs) — the update's whole territory. Everything below applies here.
- **User-owned** (`os-inputs/`, `os-tracker/`, `os-knowledge/` — their data, their tasks, their notes) — the update *never reads, writes, or reasons about these*. Not in the manifest, not on the table.
- **Install-once** (starter files like the session log) — copied only if absent; once the workspace has one, it's the user's forever.

## The classification, per system-owned file

Compare the three fingerprints and every file lands in exactly one bucket:

| | New release didn't change it | New release changed it |
|---|---|---|
| **User never touched it** | nothing to do | **update it** — safe, silent |
| **User modified it** | **keep theirs** — their customization stands, say nothing | **conflict** — the only case that needs the user |

The bottom-right cell has one impostor worth separating out. If the file on disk differs from the baseline but is *byte-identical to the new release*, that is not a user edit — nobody hand-writes a file into exactly the next version's contents. The release simply arrived here by another route, and treating it as a conflict invents a decision that doesn't exist. It lands in **already applied** instead.

Plus three edge buckets: files **new in the release** (add them), files the baseline lists that are **missing locally** (the user deleted it, or it was never installed — ask, don't resurrect unprompted), and files the release **retired** (each tagged with whether the user had customized it, so an untouched retirement doesn't become a question).

**Conflicts get a conversation, not a diff.** This is where being an AI matters: read both versions, understand *what the user's change does* and *what the release's change does*, and say it in plain language — *"you added a note about your deep-work hours to this file; the update adds a new section about the workspace map. They don't overlap — want me to keep both?"* Most conflicts merge cleanly because user edits and release edits rarely touch the same thing. When they genuinely collide, present both intents and let the user pick; never average silently, never pick for them. Files the manifest marks as **hybrid** (shipped *and* expected to be customized, like the principles file) route straight to this conversation without pretending to be surprised.

## The run

1. **Confirm the inputs.** An existing install (baseline `.os-manifest.json` present) and a newer release — a folder on disk containing an `os-manifest.json`.

   Usually the user has a `.zip` and describes it rather than handing you a path (*"the latest one in my downloads"*). Find it, unpack it, and locate the release root yourself; don't make them do filesystem archaeology:

   - **Unpack somewhere scratch** — a temp directory, never inside the workspace and never over the install. Unpacking the new version on top replaces their files before anything can be compared, and whatever they'd customized is gone at that moment. It's detectable after the fact (`likely_already_applied` in step 5), not reversible.
   - **Descend to the release root.** The pack unzips into a single top-level folder, so `os-manifest.json` usually sits one level below where you extracted. The release root is whichever directory actually contains that file — pass *that* as `--release`.
   - **If several zips match** what they described, don't guess at "most recent" and hope. Read the `pack_version` out of each candidate's manifest and confirm which one they mean.
   - **Clean up the scratch copy** once the update is finished, so a stale duplicate of the pack isn't left lying around to confuse a later session.
2. **Say what they're getting, before you touch anything.** Read `WHATS-NEW.md` from the release they pointed you at and cover the entries between their version and this one — in your own words, short, the two or three things this person would actually notice given what they use. It's a decision point, not an announcement: someone who hears what's coming can say *not yet*.

   Two cases where there's nothing honest to summarize, and both get said out loud rather than papered over. The file may be **absent** — older releases won't have it. Or it may be **present but start after the version they're on**, which happens on a long jump or once old entries get trimmed. In that second case the newest entries are *not* their delta; describing them as such tells someone about changes they already have while staying silent about the ones they don't. Say plainly that the notes only go back to whichever version is oldest in the file, and that the jump covers more than what's written there.
3. **Save a restore point first.** os-autosave when it's on; otherwise a one-line offer to snapshot before touching anything. The promise that makes boldness safe: worst case is a one-sentence undo.
4. **Classify everything — with the script, not by hand.** Run:

   ```
   python3 <skill-dir>/scripts/classify_update.py --workspace <install> --release <new-release>
   ```

   It does the three-way comparison across every system-owned file and returns the buckets as JSON (`--format text` for a quick human read). Do it silently — this is plumbing. **Don't hash and compare files yourself.** Hundreds of files of hash arithmetic done in-context is slow, and worse, it's fallible in exactly the way this mode promises it isn't: one miscompared file and someone's customization is silently gone. The script is deterministic; your judgment is for what the buckets *mean*.

   Read the exit code before the output — `2` means no baseline (go to *When there's no baseline*), `3` means already current (say so and stop), `1` means the inputs are wrong and the message says how.
5. **Report in one plain paragraph, then act.** Counts and the few files that need attention — *"142 files updated, your 3 customizations kept, one file needs a decision"* — not a wall of paths. Apply `safe_update` and `new`, say nothing about `keep_theirs` and `unchanged`, copy `install_once`, and walk through the rest one at a time.

   Three buckets are questions rather than actions: `removed_upstream` (the release retired it — each entry carries `customized`, so quietly remove the untouched ones and only ask about the files they'd made their own), `missing_locally` (they deleted it — don't resurrect unprompted), and `release_incomplete` (a file the release manifest claims but didn't deliver intact — a partial or corrupted download; stop and have them re-download rather than applying half a release).

   **`already_applied` is not a conflict and must never be reported as one.** Those files already carry the new release's content, which means it reached this workspace some other way. When `likely_already_applied` is set, most of the release is already there — almost always the new version unpacked over the install, occasionally an earlier update that stopped partway. Say so plainly rather than reporting a clean success: there's nothing to decide, but if it was unpacked over the top, anything they'd customized in those files is already gone and a snapshot is the only way back. Check whether they have one before moving on.
6. **Finish the bookkeeping.** Write the new release's manifest as the workspace's new baseline. Refresh any deployed surface copies (`os-skill-deploy` owns that wiring). Offer `validate` to close, same as `customize` does.
7. **If new skills arrived**, note the one-reopen rule from install: they answer by name after the app restarts.

## When there's no baseline

Installs that predate the manifest can't be classified — there's no record of what shipped, so "did the user change this?" has no honest answer. Say exactly that, then offer the two real paths: **adopt-and-review** (bring in the new release's files one area at a time, showing what would change before each write — slower, safe, converts the install to baselined at the end) or **fresh-alongside** (stand up the new release clean, migrate their user-owned data — which needs no migration, it's just their files — and cherry-pick any skill customizations by hand). Never bulk-overwrite an unbaselined install; uncertainty defaults to the user's side.

## Update doctrine

- **The user's changes are load-bearing until proven otherwise.** A modified file is a decision the user made; the update's job is to honor it, not to route around it.
- **Uncertainty resolves toward the user.** No baseline, ambiguous hash, missing file — every unclear case defaults to keep-theirs-and-ask, never to overwrite.
- **Plumbing invisible, changes visible.** The user shouldn't see hashes, manifests, or bucket names — they should hear what changed in their system and what stayed theirs, in a paragraph.
- **Never update user-owned territory.** Not even to "fix" something. If a release genuinely needs to touch user data (a format migration, say), that's a named, explained, opt-in conversation — not an update step.

---

## Permissions & safeguards

Two layers the agent *writes* (the deny floor + the policy rules) and one the user *clicks* (the mode). The recommended posture is **Auto mode plus the enforced deny-list** — and the pairing is the point: under Auto the deny rules actually bite, which is what makes a permissive mode safe (under bypass they mostly don't — see *Where the floor actually bites*).

### The hard rule: you write the floor and the policy; the user clicks the mode

This is the part an agent gets wrong by reflex, so hold the line: **the permission *mode* (Auto, bypass) is never set by writing a file — not any scope, not any harness.** Writing `defaultMode: auto`/`bypassPermissions` fails silently and the failure looks like success: a project file can't escalate itself (Claude Code ignores `auto`/`bypass` from `.claude/settings.json` so a repo can't self-grant), a user-file write is account-gated (Auto needs an eligible plan/admin/model — otherwise it's ignored and you fall back to Ask), the running session won't reload the mode, and a saved per-project mode can override the boot mode. So the file "succeeds," the user is still on Ask, and everyone believes setup worked. Split the work and never blur the two:

- **What *you* write — the policy layer (safe, reliable, the valuable half).** These are the rules the mode *consumes*, not the mode itself. For Claude Code, populate the `autoMode` object in the user's `~/.claude/settings.json` (it's a global posture — get consent and back the file up first). Four model-read, plain-language fields; keep the `$defaults` token in each so you *extend* the built-ins instead of replacing them (drop `$defaults` and you wipe the defaults for that field): `environment` (trusted scopes — e.g. their workspace), `allow` (auto-approve exceptions — read/search/edit the workspace, web research, save restore points), `soft_deny` (blocks they can override — send email, publish, spend money, delete outside the workspace → ask first), `hard_deny` (unconditional — force-push or merge in repos they don't own, destructive deletes outside the workspace, exfiltrate secrets). This is a *pull-their-judgment-out* beat, not a silent write: recommend Auto, explain it's a global posture, offer these as plain-language starter rules they keep / cut / edit, then write the chosen set. For Codex, the equivalent is config values in `~/.codex/config.toml` (`sandbox_mode = "workspace-write"`, `approval_policy = "on-request"`, per-project `trust_level = "trusted"`) — Codex has no natural-language rule layer, so don't promise it "rules"; its guardrails *are* the sandbox plus approval policy.
- **What the *user* clicks — the mode (only a human can).** Recommend **Auto**, then tell them exactly where the control is and wait for them to confirm what it shows. Claude Code: press **Shift+Tab** until the mode reads **Auto** (no `/permissions` command does this — it's Shift+Tab, or a `--permission-mode` flag at launch; and if Auto isn't in the list, the account doesn't have it — pick **acceptEdits**, or stay on Ask). Codex: open its approvals/permissions picker and choose its autonomous workspace-write mode. You recommend and point; you do **not** write the switch, and you don't assert it worked from your own writes — the picker indicator is the proof.

*These specifics — the Shift+Tab control, the mode names, the `autoMode` schema and its fields — are accurate as written, but this surface moves fast; treat them as a strong starting point, confirm against what the user's app actually shows (or current Claude Code docs) if anything looks off, and if their options differ — Auto missing, a renamed control, a changed schema — adapt to what's real and tell the user what you see rather than forcing these exact steps.*

**Why Auto and not bypass.** Under **Auto**, your deny floor *and* a background classifier both still vet each action — that's what makes a permissive mode safe. Under **bypass**, the permission layer is skipped entirely: only the hardcoded `rm -rf /` and `rm -rf ~` circuit-breakers remain, so your carefully-built floor mostly *doesn't apply*. Auto is the recommendation; bypass (which only appears once launched with a flag) is a fallback when Auto is unavailable and the user accepts the thinner protection.

**Two honest caveats to say plainly.** The floor and policy you *wrote* reload live — but the **mode** is the user's to flip, and **Shift+Tab is per-session**, so Auto resets to Ask on a fresh start unless they later make it their own default (an optional, account-dependent thing *they* do, not you). And freshly-wired skills aren't callable until the app is reopened. Both land at the **single reopen at the very end** — so don't promise the rest of *this* session is prompt-free; for now they approve as you go (a few minutes, one time) or flip Shift+Tab to Auto live.

### The starter deny-list

Write the floor into the harness's enforcement layer and mirror it in `_os-preferences.md` `security.deny_list`. **The enforced syntax — and the check that it hasn't moved — is in `../_shared/references/security-calibration.md`; read it before writing anything.** Plain language stays in the mirror; the reference translates. Show the list, invite edits. Starter entries:

- `rm -rf` — destructive recursive delete. Default to blocking it broadly (not just against `/`, `~`, `$HOME`); a stray `rm -rf ./something` from a confused prompt is exactly the case to catch. Offer the user the choice: block *all* `rm -rf`, or only against root/home.
- `git push --force` / `--force-with-lease` to a default branch (`main`/`master`)
- Direct merge to a default branch in a repo not owned by the user's personal account (shaped as a pattern over `gh pr merge`)
- `git reset --hard origin/<protected-branch>` patterns
- `chmod 777 -R /` and overly broad recursive permission changes
- Publishing to a customer-facing surface (product hub, org-wide chat) without explicit, named authorization

A starter list — users add their own (a "never delete `~/personal-os/`" rule, say). Keep this beat short: it's a floor, not a security review. If the user starts asking about per-project rules, unoverridable managed settings, or secret-path denies, that curiosity is real but it isn't a first-session job — offer to drop it on their tracker and move on. **Where the floor actually bites:** deny rules are enforced under **Auto** (and `default` / `acceptEdits`) — the permission layer evaluates them before anything runs. Under **bypass** they're skipped except the hardcoded `rm -rf /` and `rm -rf ~` circuit-breakers, so a custom floor buys you little there — which is the safety reason to recommend Auto, not bypass. Write the floor *first*, recommend Auto, and the user flips the mode in the picker (you never write it). For a floor that holds even against an overriding scope, *managed settings* are the only truly-unoverridable home — overkill for most buyers, worth knowing for the security-strict.

## Recurring background automation (offered late, opt-in)

Not part of the first-session felt experience — offer it later (a `customize` run, or once the user's been using Personal OS a while). It asks a different question than the rest of setup: *what should the OS do on its own, even when the user isn't in a session?*

Two skills earn that background role, as a pair. **`os-autosave`** is the safety net — it commits at session start (capturing offline edits), commits at session end, and snapshots before any moderate or large `os-tune` apply so revert always has a clean target. A scheduled wake-up is what makes those same moments fire when no one's in a session: a brief automated session runs `os-autosave commit` against whatever changed since last time, idempotent by design. (Auto-save is parked at install — this is where it earns its place, once there's something worth protecting.) **`os-tune`** is the meta-loop — its reflect pass surfaces patterns from accumulated logs (skill-usage + inbox task-audit lines) and runs the proactive-prompting scan that wants to notice clusters across days, not just within a session. A morning sweep is the canonical pairing: `os-autosave` captures what the night left behind, `os-tune reflect` notices what's been recurring, and the user opens their day to a brief pattern report instead of having to remember to ask.

Wire them together because they reinforce each other — tuning without auto-save is reckless (no revert target), auto-save without tuning is inert (commits without insight). The user's mental model wants one cadence — *"Personal OS wakes up each morning and tidies itself"* — not two schedules to reason about.

**Use the harness's own scheduler — don't build custom code.** Teaching the user that their harness *has* a built-in scheduler is part of the point of Personal OS. Default hard to the native primitive; reach for custom code only if the user emphatically asks for "run even when the app is fully closed." There are three mechanisms and the difference between them matters:

| Mechanism | Runs where | Local file/git access? | Runs when app closed? |
|---|---|---|---|
| **Local Scheduled Tasks** (`mcp__scheduled-tasks`, the in-app scheduler) | the user's machine, in-app | ✅ yes | ⚠️ runs while the app is open; catches up on next launch |
| Cloud Routines (`/schedule`) | Anthropic cloud | ❌ no | ✅ yes |
| launchd / cron (custom) | the machine, headless | ✅ yes | ✅ yes |

For this morning sweep, the right tool is **Local Scheduled Tasks**: the sweep reads local logs and saves a local restore point, which **Cloud Routines can't do** (no local access), and it runs inside the already-working app so it sidesteps any headless-`claude` problems entirely. **launchd/cron is a last resort** — custom code, more to explain and maintain, only worth it for "the app is never open" (overkill for a personal daily tidy, and the only path exposed to a headless-Node crash, so preflight `claude` headless before ever choosing it). Cloud Routines is wrong for anything local. Unknown harness → cross-harness adaptation to find its native scheduler.

**Be honest about the catch:** an in-app schedule only fires when the app is open and the machine is awake; a missed run catches up on next launch. Say this plainly so the user isn't surprised — and show them they can always run it by hand anytime (teach the harness's manual trigger — typically `$os-daily-assist` or the slash form), which doubles as teaching a capability they'll use constantly.

**Frame it around the payoff, not the plumbing.** Lead with what `os-daily-assist` *does for them* — opens their day with the night's changes already saved and a short "here's what's been recurring / worth your attention" report, instead of a blank prompt — with a quick concrete example. Then: propose a default cadence (a morning sweep is the common default), register it via the native scheduler, confirm in one line, and record it in `_os-preferences.md` under `automation.recurring_schedule`. Skipping is a first-class outcome — move on without grumbling and note the skip so a future `customize` can offer it again.

**The weekly tune-up is the one worth offering by name.** `os-weekly-tuneup` is what keeps the OS learning instead of drifting, and it depends on a cadence — the transcripts it learns from are deleted by the harness on a rolling window, so a pass that never runs quietly loses history rather than merely postponing it. Offer it here, route to `os-weekly-tuneup/setup` for the cadence, day, project scope, and retention check, and if the harness has no scheduler say so plainly — the skill falls back to a staleness nudge rather than pretending a schedule exists.

## Cross-harness adaptation

Personal OS is harness-agnostic. **For every harness — Claude, Codex, OpenHands, Cursor, OpenClaw, Aider, Devin, or anything else — apply the cross-harness adaptation directive at `_shared/references/cross-harness-adaptation.md`.** Start with `AGENTS.md`, `SKILL.md`, and `.agents/skills/` where supported; verify the harness's current discovery, context, permission, and scheduling conventions; then add clearly labeled native adapters where needed. Update this skill only when the encounter produces durable new knowledge, and record nonstandard compatibility needs in `_os-preferences.md`.

The posture split holds for *every* harness, not just these two: restrictions / deny rules → the harness's nearest enforced scope (the agent writes them); the escalated-autonomy **mode** → the user's own picker (the agent recommends + points + waits for confirmation, **never** writes a mode to a file); the policy layer, *if the harness has one* → the agent writes it at user scope with consent. Research the new harness's mode-picker control and its config keys before recommending anything.

## Doctrine

- **The first session sells the purchase — with their hands, not your config.** Lead with something real on material they already have and get them to felt value in the first minutes. Fully configured and unmoved is the failure case. Safety stays first as a principle, but it runs silent and underneath.
- **Two good options at every fork; one hit, then out.** Never a blank menu or a list of six. Peak early and push them toward *using* what they built — a second wow in the same sitting trades "I made something" for "this is fun," which is how setup graveyards get filled.
- **Hidden work, shown spoils; call a demo a demo.** Run the configy parts silently, then show the fruit plainly — the payoff has to be visible or they feel nothing, but the showing isn't a performance. Naming it as a demo is what makes a rough edge fine. If you catch yourself describing your own technique instead of being curious about the person, stop.
- **Mode is the human's; policy and floor are yours.** Never set the permission *mode* (Auto / bypass) by writing a file — any scope, any harness. It fails silently and looks like success: project scope is ignored, user scope is account-gated and won't reload the running session, a saved per-project mode can override it. Your jobs around posture are four: write the **deny floor** (workspace `permissions.deny`), write the **policy layer** (Claude Code `autoMode` rules at user scope; Codex sandbox + approval config), **recommend** the right mode (Auto, not bypass — the floor only bites under Auto), and **point** the user at the picker (Shift+Tab → Auto) then **wait** for them to confirm what the indicator reads. Recommend, point, confirm — never write the switch, never infer it's live from your own write.
- **One reopen, for skills — and never fake a live check.** Skills are discovered at session start, so a single close-and-reopen at the very end is what makes them callable. Permission *rules* reload live and the *mode* is a live keypress, so nothing else needs a restart — don't scatter reopens through setup; repeated ones feel tedious and break the calm. And never report the permission mode (or a live skill firing) as green from a file write — only the picker indicator and an actual invocation prove those, after the reopen.
- **Plumbing invisible, value visible.** The user shouldn't have to see or understand git, JSON, PATH, or Node to get set up. Use plain language, breeze past (or hide) the machinery, offer to explain on request. Never expose git vocabulary for auto-save — "restore point," not "commit/push."
- **Use the harness's own capabilities; avoid custom code.** Scheduling uses the native scheduler (Local Scheduled Tasks for local work), not launchd/cron. Defer or skip anything that requires building and running custom code unless the user emphatically asks. Teaching the harness's built-in powers is part of the product.
- **The user's existing setup is theirs.** Combine vs fresh is the user's call, asked not inferred. Never silently overwrite a tuned `CLAUDE.md` or clobber an existing skill. Cherry-picking later is always open.
- **The workspace is the source of truth.** `<workspace>/skills/` is canonical; surface targets symlink/copy from there.
- **No plugins, anywhere.** A skill inside a plugin can't be edited in place, which breaks the whole premise. Cowork sync happens via `skill-deploy` zip + manual upload; local surfaces link to the workspace. See `os-skill-deploy`'s no-plugins doctrine.
- **Preferences are persistent and editable.** Everything captured lands in `_os-preferences.md`; edit by hand or via `customize` anytime.
- **Cross-harness adaptation is mandatory, not optional.** Don't refuse an unknown harness — research and adapt.

## What you'll have when it's done

A Personal OS that already *did something for you* in the first sitting — a tool spun out of something you'd never have gotten to, or a piece made in your own voice — with a loop already running and a reason to come back tomorrow. The safety floor is in place, the dangerous things fenced off, and the rest of the configuration is there to dial in whenever you want it. Nobody watched a wizard finish. You just did the thing.

## Related references

- `os-setup.md` (workspace root) — the entry file the user points their AI at first; routes here
- `os-manifest.json` (pack root) / `.os-manifest.json` (workspace) — the release fingerprints + ownership map that `install` records and `update` classifies against
- `scripts/classify_update.py` — the three-way comparison itself: baseline vs. disk vs. new release, sorted into buckets. Reports; never writes. `update` runs it instead of comparing files by hand
- `WHATS-NEW.md` (pack root) — plain-language release notes; `update` reads the new release's copy to tell the user what they're getting before it touches anything
- `_shared/references/workspace-layout.md` — the canonical folder/layout contract this skill scaffolds to
- `_shared/references/cross-harness-adaptation.md` — the standards-first adaptation directive for every harness
- `_shared/references/skill-update-protocol.md` — write-discipline for the self-update part of cross-harness adaptation
- `os-capture`, `os-gold`, `os-skillify` — the core-loop demonstration the first session runs (followed from disk on a fresh install)
- `os-content-interview`, `os-voiceprint/from-sample`, `os-content-template` — the maker path's three-question exchange + background voiceprint/template lift
- `os-tracker` — where the "revisit this in a week" follow-up task is planted
- `os-skill-deploy` — Cowork + web Chat sync, wired onto PATH by setup
- `os-autosave` — parked at install (nothing to lose yet); turned on later via `customize` or the recurring-automation pairing, and owns the optional off-machine backup
- `os-daily-assist` / `os-tune` — what the native-scheduler morning sweep runs; frame that later offer around os-daily-assist's payoff
