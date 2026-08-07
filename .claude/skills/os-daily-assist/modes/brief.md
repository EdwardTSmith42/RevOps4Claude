---
name: brief
parent: daily-assist
description: >-
  Default mode of `daily-assist`. Surface a morning brief — opener, three focus options to choose from, calendar with prep context, anything in inbox that needs the user, optional delight, plus a "want more?" menu of deep-dive options at the bottom. ADHD-aware tone: warm but precise, short sentences, choices not demands, friction-reducer when the user picks. Triggers on "good morning," "daily brief," "morning briefing," "what's on for today," "start my day."
---

# Mode — brief

The user says "good morning" (or equivalent). Surface the morning brief.

## What this mode is

A companion-feel briefing, not a status report. Helps the user feel in command of the day, presents three focus options for them to pick from, surfaces what genuinely needs them, hands control back. Includes a "want more?" menu at the bottom for deep-dive options the user can opt into. Designed to fit in <250 words for the default-visible portion.

## Procedure

### 1. Load configuration

Read `os-inputs/_os-setup-philosophy.md` for the `## good_morning` section.

- **If found:** parse elements list, ordering, params.
- **If not found:** offer setup with a one-liner that names the choice (run setup now in a few minutes, or use sensible defaults today and configure later). Defaults: `opener + focus_picks (3) + calendar + inbox_urgency + more_menu`. Hand off to `setup` if the user prefers.

### 2. Run each enabled default-brief element in configured order

For each enabled element in the default brief, in configured `ordering`:

- Look up the element's fetch logic in `references/elements.md`
- Run the fetch
- If a dependency is missing, self-degrade with a one-line `[<element> — not configured — <how to enable>]` note and continue
- If the fetch succeeds, format the output per the element's spec

### 3. Generate the "want more?" menu

For each deep-dive element (pattern_offers, yesterday_loose_ends, system_worklog_reminder, full_tracker_view, inbox_by_category), check whether it has content right now and whether the user has it enabled in their menu config. Build a numbered list of available deep-dives with one-line previews where useful.

If a deep-dive has no content (e.g., no pattern_offers accumulated since last brief), omit that line. Self-degrading at the menu level too — the user never sees an empty option.

If all deep-dives are empty or disabled, omit the menu entirely.

### 4. Assemble in companion voice

Combine the element outputs into one brief. Voice principles:

- **Warm but tactically precise.** Espresso-shot enthusiasm paired with a bulletproof first move.
- **Short sentences. Vivid verbs.** No info-dump monologues.
- **Three focus picks, not one or many.** AI gets a single pick wrong too often; the user picks from three with brief rationale per option. The friction-reducer attaches to the user's chosen pick after they decide.
- **Calendar framing first-class.** Lead with day-shape (how much open time, or whether the day is back-to-back), not the meeting list.
- **Inbox = urgency only.** Frame as *who is waiting on what*, never as label counts.
- **No overstimulation.** Default visual style is minimal (clean prose, no emoji). Section breaks via blank lines.

### 5. Close with handoff

The brief ends with a low-stakes choice that combines the focus picks and the menu:

> *"Pick a focus to start (1, 2, or 3), or ask for more from the menu above."*

If `custom_anchor` is configured with `position: closing`, that's the closing line instead — the user's mantra or framing question.

### 6. Handle the response

If the user picks a focus number → load the friction-reducer + active-futuring for that pick, surface, route to whatever skill makes that work happen.

If the user picks a menu item → run the selected deep-dive element (daily-assist's pattern_offers / yesterday_loose_ends / system_worklog_reminder) OR route to the appropriate skill (os-tracker/view for full tracker, email views for inbox-by-category).

If the user does something else (asks a question, changes topic, etc.) → just go with their flow. The brief was the offering; the handoff is open, not gating.

## Example brief shape

For a user with the setup-written default config (`opener + focus_picks + calendar + inbox_urgency + delight + more_menu` — note `delight` is present here but absent from the no-config first-run set, because it needs the config's freshness and relevance settings), the assembled brief follows this skeleton — every angle-bracketed slot describes what the slot is *supposed to produce*, not text to copy:

```
<time-aware greeting addressed to user by name>.

Three to consider for today's lock-in:
  1. <quick-win pick> — <one-line rationale + time estimate>
  2. <medium-stakes pick> — <one-line rationale + time estimate>
  3. <deeper-work pick> — <one-line rationale + time estimate>

<day-shape framing line — open time before first call, or back-to-back warning, etc.>
  <time> — <meeting title> (<prep context where available>)
  <time> — <meeting title> (<prep context where available>)

<count phrase> need you today:
- <person or source>: <what they're waiting on> (<why urgent>)
- <person or source>: <what they're waiting on> (<why urgent>)

Saved-for-later worth a glance: <one-line framing of a recent capture> argues <its claim>.

Want more? Just ask:
  1. <deep-dive name> (<one-line preview / count>)
  2. <deep-dive name> (<one-line preview / count>)
  ...

Pick a focus to start (1, 2, or 3), or ask for more above.
```

Target: <250 words for the default-visible portion. Three focus picks span the energy spectrum. Calendar leads with day-shape, then meetings with prep. Inbox is urgency-only. Delight is one line and only when something earns it. Menu shows only deep-dives that have content right now. Open handoff with two paths.

## Operating principles

- **<250 words target for the default-visible portion.** The "want more?" menu adds a few lines but stays terse — one item per line, no preview bloat.
- **Self-degrade gracefully.** Missing dependencies are one-line notes; never break the brief. Empty deep-dives drop from the menu silently.
- **Read-only.** No writes. No mutations. The brief is a read.
- **Three focus picks is the default, not a mandate.** User can configure `count: 1` (single pick), `count: 5`, or use `style: top_three_with_rationale`. Default 3 reduces wrong-pick risk without overwhelming.
- **Friction-reducer attaches to the chosen pick.** The brief shows three options without all the futuring; once the user picks one, surface *"by 9:30 you'll have it landed"* + suggested first physical action.
- **Time-aware greeting.** Match time of day — "Good morning" before noon, "Good afternoon" through 5pm, "Hey there" if user invoked late or with time-neutral phrase.
- **No scheduled fire.** Mode runs only when invoked.

## Output

A multi-element markdown briefing surfaced inline. No file writes. If user picks a focus or menu item afterward, route accordingly.

## Approval gates

None — read-only.
