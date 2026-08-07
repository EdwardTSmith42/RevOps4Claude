---
name: os-daily-assist
version: 0.1.0
description: >-
  Daily orchestrator for Personal OS — your invoked morning start. Pulls
  together a brief that helps you feel in command of your day: today's
  north-star focus, calendar with prep context from prior meetings, anything in
  your inbox that genuinely needs you, optional delight items. ADHD-aware
  design: one north-star not a long list, warm but precise, reduces initiation
  friction with a suggested first action. Two modes — brief (default, fires on
  "good morning"), setup. Triggers on "good morning," "daily brief," "morning
  briefing," "what's on for today," "start my day," "set up good morning,"
  "configure my morning brief."
display_name: Daily Assist
tagline: A morning brief that makes the day feel handle-able.
category: Planning
packs:
  - personal-os
icon: 'phosphor:Sun'
when_to_use: >-
  Your invoked morning start. Pulls together a brief that helps you feel in
  command of your day: today's north-star focus, your calendar with prep context
  from prior meetings, anything in your inbox that genuinely needs you, optional
  delight items.


  ADHD-aware design: one north-star, not a long list. Warm but precise. Reduces
  initiation friction with a suggested first action. Fires on `good morning`,
  `daily brief`, `morning briefing`, or whatever wake-up phrase you set up.
modes:
  - name: brief
    job: The morning brief itself — fires on 'good morning'.
  - name: setup
    job: Configure what your daily brief includes.
---

# Daily Assist — daily orchestrator

## Purpose

You say "good morning" and Personal OS hands you a brief that helps you feel in command of the day. Not a status report. Not a dashboard. A companion that frames where you stand, picks the one thing to lock in, surfaces what genuinely needs you, and hands control back so you can start moving.

Designed around how mornings actually work for high-performers — especially anyone who runs hot on attention or works with ADHD. The shaping principles: one north-star not a list, warm but tactically precise, short sentences, friction-reducers attached to first actions, dopamine bricks instead of giant task piles, no overstimulation. The brief is small on purpose — you can always ask for more.

## When to use

- *"Good morning"* / *"daily brief"* / *"what's on for today"* / *"start my day"* → `brief` (the default)
- *"Set up good morning"* / *"configure my morning brief"* → `setup`

## Modes

| Mode | Job |
|---|---|
| `brief` | Read your config, run each enabled element, surface the morning brief |
| `setup` | Walk you through what you want in your mornings |

## What's in the brief

Six elements compose the brief. The user picks which to enable + their order via setup. Element catalog with full specs in `references/elements.md`.

- **`opener`** — time-aware greeting addressed to the user by name. One line; no warm-up monologue.
- **`focus_pick`** — ONE thing to lock in today, with a friction-reducer that names the next concrete physical move and a realistic time estimate. Drawn from tracker Next + recent context.
- **`calendar`** — today's meetings with prep context. First-class element. Includes a day-shape framing line (how much open time before the first call, or whether the day is back-to-back) and per-meeting context where available — last week's commitments, prior thread, deal stage. When meeting-transcript integrations are wired (Fathom, Fireflies, Otter, Granola, Read.ai, etc.), pulls from those.
- **`inbox_urgency`** — only what truly needs the user today. A short list of who is waiting and what they're waiting on, framed as *needs you*. Not counts. Not a digest. Action-required only.
- **`delight`** — optional. A small useful tidbit from recent newsletters or saved-for-later items in knowledge. Light dopamine. Only when something genuinely earns the spot — never forced.
- **`custom_anchor`** — user-defined. A mantra, an opening question, a daily framing the user wants present every morning.

After elements: the brief closes with an open handoff — a low-stakes choice that lets the user either pick a focus and start, or pull a deep-dive from the menu. Choice without demand.

## Operating principles

- **One north-star, not a list.** ADHD-aware: a giant task pile is paralyzing. The brief picks ONE focus item and reduces its initiation friction. The full backlog is one ask away (*"show me my full tracker"*).
- **Warm, tactically precise, staccato.** Short sentences. Vivid verbs. No info-dump monologues. Espresso-shot enthusiasm paired with a bulletproof first move.
- **Calendar is first-class, never deferred.** The brief almost always includes calendar context. Even with no upcoming meetings, the day-shape framing matters — naming an open day as a deep-work block is itself orientation.
- **Cautious with emoji.** Default visual style is `minimal` (clean prose, no emoji) because emoji can overstimulate readers who run hot on attention. Users can opt up to `sectioned` (one mark per section) or `rich`.
- **Self-degrading, never blocking.** If a dependency (email, calendar, etc.) isn't set up but its element is enabled, the brief shows a one-line `[<element> — not configured — <how to enable>]` note and the rest proceeds. Configure daily-assist early; the brief enriches as dependencies wire up.
- **User invokes, never automatic.** No scheduled fire, no surprise pop-ups. Scheduled briefings are a harness-level concern — use the harness's native local scheduler per os-guided-setup's mechanism table (the brief reads local files, so cloud-side schedulers can't run it), not this skill's responsibility.
- **Sensible defaults on first run.** A user who hasn't done setup yet gets a useful brief on day one — `opener + focus_picks (3) + calendar + inbox_urgency + more_menu` (the same first-run set brief mode uses; `delight` joins once setup writes a config, since it needs freshness/relevance settings to run well). Setup invites refinement after.
- **Read-only on data sources.** Brief reads tracker, calendar, inbox, logs; never modifies them. Setup writes only to `_os-setup-philosophy.md`.
- **The Getting Started section is handled gently.** A fresh install ships a "Getting Started" onboarding checklist in the user tracker. The brief treats it as a soft aside, never live work: it is *never* a `focus_pick` (the north-star stays real work), it surfaces at most one item as a low-pressure offer ("when you've got a few minutes, you could set up X"), and it goes silent the moment the section is cleared or gone. Honor the section's own handling note — one at a time, lean toward using what's already built, remove without fuss. Never dump the checklist into the brief.

## Configuration

Lives in `os-inputs/_os-setup-philosophy.md` under `## good_morning`. Setup mode writes it; user can hand-edit. Starting shape in `templates/config.md`.

## Cross-mode chain

After `setup`, offer to run `brief` once with the new config so the user sees what their morning looks like. Useful for catching *"oh, I want this on too"* before they start using it daily.

After `brief`, if a dependency self-degraded, the skill suggests setting that up next — connecting daily-assist to the broader Personal OS setup.

## References

- `references/elements.md` — element catalog with full specs (data fetch, dependencies, params, output format)
- `templates/config.md` — starting shape for `## good_morning` config

## See also

- `os-email`, `os-tracker`, `os-capture` — the dependencies the brief reads from
