---
name: setup
parent: daily-assist
description: >-
  Configure or reconfigure the Daily Assist brief. Walks the user through what they want their mornings to feel like and what level of depth to surface — anchored on user-feel, not feature toggles. Covers default brief shape, focus-picks count, calendar prep depth, inbox scope, delight, custom anchor, and which deep-dive options appear in the bottom menu. Triggers on "set up good morning," "configure my morning brief," "change what's in my morning brief."
---

# Mode — setup

Walk the user through what they want their mornings to feel like, then write it to `os-inputs/_os-setup-philosophy.md`.

## What this mode is

Setup is configuration, but it should feel like a thoughtful conversation about how the user starts their day. The user is here because they want help; reward that with quick wins, choices framed in user language, and flexibility on the decisions that matter.

## Procedure

### 1. Load existing config if present

Read `os-inputs/_os-setup-philosophy.md` `## good_morning` section.

- **If found:** name the current config in one sentence (which elements are on, focus-picks count, menu items enabled) and ask whether to adjust or start fresh.
- **If not found:** open with a low-friction framing — about three minutes of questions, sensible defaults suggested, everything adjustable.

### 2. Frame on user-feel before features

Open with a single user-feel calibration question — how does the user want to feel when they finish their morning brief? *In command of the day*, *energized to start*, *calm and grounded*, or something the user names themselves.

Capture the answer. Bias subsequent defaults toward it. For example, an *in-command* answer biases toward calendar prominence and the full focus-picks slate; an *energized* answer biases toward delight + active futuring; a *calm-and-grounded* answer biases toward terse opener, custom anchor, and fewer focus picks to lower choice load.

### 3. Walk default-brief elements as choices

For each default-brief element, ask one short question framed in user language, capture the answer, set the param, move on. No element should take more than 30 seconds of conversation.

- **`opener`** — warm-with-name, terse, or skip.
- **`focus_picks`** — explain briefly that the brief offers three options because AI tends to get a single forced pick wrong, and three lets the user choose by mood (quick-win / medium / deeper). Confirm count: default 3, options 1 or 5. Friction-reducer + active-futuring on the chosen pick are default-on.
- **`calendar`** — confirm prep context on (uses email threads, calendar descriptions, recent inbox lines), and ask whether any meeting-transcript tool is wired (Fathom, Fireflies, Otter, Granola, Read.ai, or other). If the user names a tool that isn't yet integrated, log a follow-up to `os-tracker/system.md` rather than blocking setup.
- **`inbox_urgency`** — counts vs urgency-only. Default `urgency_threshold: today`; counts available for users who explicitly want them.
- **`delight`** — a small useful tidbit from recent saved content, surfaced only when something earns the spot. Default on; expect it to often skip.
- **`custom_anchor`** — invite the user to name a mantra, opening question, or daily framing, and where they want it positioned (top, closing, inline, or skip).

### 4. Walk the "want more?" menu

Explain the menu in one sentence: it lives at the bottom of the brief, shows numbered deep-dive options, and each only renders when it has content right now. Then walk the six default options:

- Pattern offers — proactive-prompting candidates accumulated since the last brief
- Yesterday's loose ends — task-audit lines from yesterday showing what was in flight
- System worklog — long-running unresolved threads (default age threshold: 14 days)
- Full tracker view — the entire tracker beyond just `Next`
- Inbox by category — counts + items per label across configured accounts
- Recent knowledge — what's been added to knowledge files in the last 7 days

Default: include all six; user can disable specific items.

### 5. Confirm visual style

Confirm visual style with a one-sentence framing: default is minimal (clean prose, no emoji) because emoji can overstimulate readers who run hot on attention; sectioned (light markers) and rich (full emoji) are available. Default minimal.

### 6. Show the assembled config

Render the resulting YAML for `## good_morning`. The user reviews. Common adjustments: reorder, toggle one element, change focus-picks count.

### 7. Dry-run write to `_os-setup-philosophy.md`

Per workspace mutation discipline (dry-run + explicit approval before writing user config), surface the diff before writing. On confirmation, write the `## good_morning` section. If a `## good_morning` already exists, replace it. If `_os-setup-philosophy.md` doesn't exist, create it.

### 8. Capture aspirations as follow-up tasks

If during setup the user mentioned anything not yet supported (e.g., a transcript tool integration), log a follow-up to `os-tracker/system.md` via `os-tracker/add` — phrased as the concrete next step needed to wire that capability into the daily brief. This honors the stated need without blocking setup completion.

### 9. Offer a dry-run brief

Offer a one-time dry-run brief so the user can see what their morning will look like and catch any *oh, I want this on too* before tomorrow. If they accept, hand off to `brief` mode. If not, close with a single affirmation that names the wake-up phrase they configured.

## Operating principles

- **Configuration as conversation, not form.** Each element is a question framed in user language.
- **User flexibility on the decisions that matter.** Three focus picks vs one is a real choice, not a hidden default. The deep-dive menu items are user-pickable. Visual style is user-pickable.
- **Anchor on user-feel before features.** The opening *"how do you want to feel"* question calibrates everything that follows.
- **Capture aspirations, don't gate on them.** If the user mentions something we don't support yet, log it as a follow-up — never block setup.
- **Quick wins fast.** First-time users should be done in 3 minutes with a working brief they're excited about.
- **Re-run is normal.** Setup is designed to be invoked repeatedly as needs evolve.

## Output

- Updated `## good_morning` section in `os-inputs/_os-setup-philosophy.md`
- Optional immediate `brief` run for sanity check
- Any aspirations logged to `os-tracker/system.md` as follow-ups

## Approval gates

- Dry-run + confirmation before writing to `_os-setup-philosophy.md`.
- No other gates — setup is configuration.
