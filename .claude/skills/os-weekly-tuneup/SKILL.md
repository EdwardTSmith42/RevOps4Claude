---
name: os-weekly-tuneup
version: 0.1.0
description: >-
  The weekly maintenance pass for the whole OS — the one recurring ritual that
  keeps everything else honest. Runs in perishability order: distills archived
  threads into durable memories before the harness deletes them, snapshots the
  workspace, surfaces patterns worth acting on, tidies stale todos, and reports
  disk health for developers. Delegates every step to the skill that owns it and
  reimplements none of them. Two modes, `setup` and `run`. Triggers on "run the
  weekly tuneup", "weekly maintenance", "time for the tune-up", "it's been a
  while — catch my OS up", and on a scheduled reminder firing. Do NOT trigger for
  ad-hoc pattern questions (use `os-tune/reflect`), for making or changing one
  skill (use `os-tune`), or for end-of-session capture (use `os-tune/close-out`).
display_name: Weekly Tune-Up
tagline: One weekly pass that keeps your OS learning instead of drifting.
category: Planning
packs:
  - personal-os
icon: 'phosphor:CalendarCheck'
when_to_use: >-
  Run this once a week. It captures what your AI harness is about to throw away,
  turns it into memory your OS can actually learn from, and then does the
  household chores — patterns worth acting on, stale todos, disk health. Every
  step is optional except the first, and the whole thing is designed to be
  abandoned halfway without losing anything that matters.
modes:
  - name: setup
    job: Decide cadence, which day to run, which projects are in scope, and confirm the harness's transcript retention is longer than the cadence.
  - name: run
    job: The weekly pass itself, in perishability order — distill, snapshot, reflect, tidy, disk report.
---

# os-weekly-tuneup — the weekly pass that keeps the OS learning

## Purpose

Personal OS improves by noticing what you actually do. That noticing needs raw material, and the raw material is perishable: agent harnesses record full session transcripts and then delete them on a rolling window. Anything not captured before that window closes is gone, silently, forever.

This skill is the recurring appointment that captures it — and since it's already reading the week's work, it does the rest of the household chores in the same sitting.

**It owns nothing but the sequence.** Distilling belongs to `os-tune/distill`, patterns to `os-tune/reflect`, todos to `os-tracker/tidy`, snapshots to `os-autosave`, worktrees to `dev-stale-worktree-curator`. This skill decides *when*, *in what order*, and *how much*, then gets out of the way.

## The ordering principle — perishability first

The steps below are ordered by what's lost if you stop early, not by importance.

A weekly ritual that asks for forty minutes is a weekly ritual you skip in a busy week, then skip again, and then it's the thing that never runs. So the run is built to be abandoned: step 1 takes a couple of minutes and captures everything time-sensitive. Everything after it can wait a week at no cost.

When the user seems pressed, say so directly — offer step 1 alone and stop there. A two-minute tune-up that happens beats a thorough one that doesn't.

## Mode: `setup`

Decide four things once, record them in `os-inputs/_os-setup-philosophy.md`, and don't ask again:

**Cadence and day.** Weekly is the default. Ask which day.

**Timing against the token reset.** Distilling a week of threads is the most token-hungry thing this skill does. Ask when their usage window resets and schedule the run *just before* it, so a heavy pass draws down the budget they're about to lose rather than the one they're about to start. If they don't know or don't care, don't belabor it — pick their chosen day and move on.

**Project scope.** Show them the actual list of projects their harness has transcripts for, not an abstract question. Default is everything, because the strongest signal comes from work that repeats across contexts — and for most people the heaviest repetition lives in client work, which makes excluding it by default exactly backwards.

State the trade-off in one plain sentence and let them decide: *learnings from these threads become part of your personal OS, so if a given client's work shouldn't leave its own context, exclude that project.* Not a warning, just a fact they should own. Record exclusions with the distill script's `exclude` command.

**Retention headroom.** Check that the harness keeps transcripts longer than the cadence, with slack for missed runs. On Claude Code that's `cleanupPeriodDays` in `~/.claude/settings.json`, default 30. Weekly runs want 60 or more so a few skipped weeks don't quietly cost history. If it's shorter than the cadence, say plainly that data will be lost between runs and offer to raise it.

**Invocation logging (optional, mention once).** If the harness can run a command after a tool fires, offer it in a sentence — it records which skills get used, which is what lets `reflect` see a skill that keeps needing the same correction rather than only a request that keeps recurring. Everything works without it. Setup and the honest version of what it records are in `../os-tune/references/usage-logging-setup.md`. Don't sell it and don't re-offer if they pass.

**Scheduling.** Wire the recurring reminder through whatever the harness offers, per `os-guided-setup`'s recurring-automation beat. If it offers nothing, say so and fall back to the staleness nudge below rather than pretending a schedule exists.

## Mode: `run`

Announce what you're about to do in one line, then work. Between steps, a short progress note is enough — this is a chore, not a performance.

### 1. Distill — the only step that can't wait

Route to `os-tune/distill`. It finds threads the harness hasn't deleted yet and hasn't already been distilled, turns the user's own words into memories under `os-memory/`, and marks them done.

If the oldest pending thread is close to the retention edge, say so and do this step even if the user wants to skip everything else.

### 2. Snapshot — before anything writes

Everything below this line changes files. Take a restore point first via `os-autosave`.

If auto-save isn't set up, don't stall and don't nag: say once that there's no restore point, offer to set it up, and continue either way. This skill works without it; the user just carries the risk knowingly. Commit at the end of a successful run the same way.

### 3. Reflect — the payoff

Route to `os-tune/reflect`, which reads the memories distilled in step 1 plus the harness's skill-invocation log. It proposes; it doesn't apply. Anything acted on gets a line in the ledger (below) so the next run doesn't re-propose it and the run after that doesn't either.

### 4. Tidy the todos

Route to `os-tracker/tidy`. Stale items, things quietly completed in the week's work, things that have drifted past relevance.

### 5. Disk health — developers only, report only

If the dev pack is installed, run `dev-stale-worktree-curator`, stopping after its audit step and report what it finds: how many worktrees, how much disk, which are safe to remove.

**Do not remove anything here.** That skill can delete unpushed work, and a recurring pass should never be the thing that decides. Surface the numbers and let removal be a deliberate act on a different day.

## The action ledger

`os-memory/_ledger.md`, newest first. One line per action taken: the date, the pattern that prompted it, what was done, and which memories drove it.

Its job is a fast answer to *"have we already dealt with this?"* — reading every memory to find out is exactly the cost that makes a weekly ritual too expensive to keep. Rejections belong here too: a pattern the user declined is a decision, and re-proposing it next week is how a helpful system becomes an annoying one.

## Staleness — the backstop

Scheduled runs fail quietly. Machines are asleep, automations break, weeks get away from people.

So when a session opens and the last run is well past the chosen cadence, say so once, briefly, with the number that matters — how close the oldest uncaptured thread is to deletion. Then drop it. One mention per session; a nag that repeats gets tuned out, and a tuned-out warning is the same as no warning.

## Guardrails

- **Propose, don't apply.** Every step surfaces; the user decides. The only things written without asking are memories and ledger lines, which are records rather than changes.
- **Never delete on a schedule.** Worktrees, todos, skills, memories — a recurring pass may recommend removal and may never perform it.
- **Degrade out loud.** No transcripts, no auto-save, no scheduler, no dev pack — each is fine, and each is said once plainly rather than silently skipped.
- **Client-work memories carry their origin.** A memory distilled from a client project records which project it came from, so it can be found and removed later if that relationship ends.
- **One session, one nudge.** The staleness warning and any pattern offers are capped per session.

## Related skills

- `os-tune` — owns `distill` (step 1) and `reflect` (step 3); this skill only sequences them
- `os-tracker` — owns `tidy` (step 4)
- `os-autosave` — owns the snapshot and commit in step 2; optional, and this skill runs without it
- `dev-stale-worktree-curator` — owns the disk audit in step 5; dev pack only, audit only here
- `os-guided-setup` — wires the recurring schedule during install, alongside the other background automation
