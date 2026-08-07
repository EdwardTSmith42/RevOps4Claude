# Daily Assist elements catalog

Two tiers. **Default-brief elements** show by default, designed for tight <250-word brief. **Deep-dive elements** appear as options in the "want more?" menu at the bottom — user opts in when they want depth, never forced.

The brief is small on purpose. Everything dropped from the default brief lives in the menu, one ask away.

Catalog earns additions through real use.

---

# Default-brief elements

These show in the brief by default.

## `opener`

**What it surfaces:** Time-aware greeting addressed to the user by name — a warm full greeting before noon, an afternoon variant through evening, or a time-neutral variant when the user invokes late or with a time-agnostic phrase.

**Dependency:** none. Reads system time + user's name from `os-inputs/_os-user-profile.md`.

**Configurable params:**
- `style`: `warm` (default — full greeting), `terse` (just *"Morning."*), `none` (skip)

---

## `focus_picks`

**What it surfaces:** Three options the user picks from for today's lock-in. AI gets a single pick wrong too often — three with brief rationale lets the user choose, then the friction-reducer attaches to the chosen pick.

**Dependency:** `tracker` (auto-creates) + recent session context.

**Configurable params:**
- `count`: `3` (default) | `1` (single forced pick) | `5` (overwhelming for most; available)
- `friction_reducer`: `enabled` (default — attaches to user's chosen pick) | `disabled`
- `active_futuring`: `enabled` (default — *"by 9:30 you're done"* shape, attached to chosen pick) | `disabled`

**Output format (`count: 3` default):**

```
Three to consider for today's lock-in:
  1. <pick 1> — <one-line rationale + time estimate>
  2. <pick 2> — <one-line rationale + time estimate>
  3. <pick 3> — <one-line rationale + time estimate>
```

After the user picks (by number or by naming the pick), surface friction-reducer + active-futuring for that pick. The friction-reducer names the next concrete physical move (open this file, draft this paragraph, open this app); the active-futuring names a realistic landing time tied to the user's day-shape so the work feels finite.

```
Locking in #<n> — <chosen pick>.
First <small interval>: <concrete physical first move>.
Then <focused sprint length> on <the specific target>. By <realistic landing
time tied to day-shape>, <what's done> and you're on to <next anchor on the day>.
```

**Getting Started exclusion:** never draw a `focus_pick` from the tracker's "Getting
Started" section. That section is onboarding setup, not the day's real work — the north-star
must always be live work. Getting Started surfaces separately and gently (see below), or not
at all once it's cleared.

**Selection logic for the three options:**

1. Read tracker `Next` items (exclude the "Getting Started" section)
2. Score each by: continuity from yesterday's work, fit to today's day-shape (available time before next meeting), recently-mentioned priority in inbox or session context, energy level (deep-work vs quick-win)
3. Pick three that span the energy spectrum — typically one quick-win, one medium-stakes, one bigger commitment. Lets the user pick based on their mood/state.
4. If tracker `Next` has fewer than 3 items, use what's there + AI inference from recent context for the rest, with explicit framing: *"Tracker has X; suggesting Y based on yesterday's session."*

**Self-degradation:** none — always produces something useful.

---

## `calendar` *(first-class)*

**What it surfaces:** Today's meetings with prep context where available. Day-shape framing first.

**Dependency:** Calendar MCP (Google Calendar via Workspace MCP is wired in this environment).

**Configurable params:**
- `prep_context`: `enabled` (default) | `disabled`
- `day_shape_framing`: `enabled` (default) | `disabled`
- `transcripts`: `auto` (default — use whatever transcript integration is wired) | `disabled`
- `meeting_lookback_window`: `7` (days back for recurring-meeting prep context)

**Output format:**

```
<day_shape_framing>.
  <time> — <meeting title> (<prep context if available>)
  <time> — <meeting title> (<prep context if available>)
```

**Day-shape framings:**
- *"90 minutes before your first call"*
- *"Open until 2pm"*
- *"Back-to-back from 10 to 4 — find your one priority before then"*
- *"Light calendar today — could be a deep-work block"*
- *"No meetings on the books"*

**Prep context sources (in priority order):**
1. Meeting-transcript integrations if wired (Fathom, Fireflies, Otter, Granola, Read.ai)
2. Email threads related to the meeting
3. Calendar event description prep notes
4. Recent inbox task-audit lines mentioning the meeting topic or attendees

**Self-degradation:**
- No calendar MCP wired: surface `[calendar — not configured — wire a calendar MCP/tool in your harness to enable]` and continue (same `[<element> — not configured — <how to enable>]` shape every element uses)
- Calendar wired but no transcripts: surfaces meetings with email-thread or description context where available

---

## `inbox_urgency`

**What it surfaces:** Only what truly needs the user today. Not counts. Action-required only, framed as *"needs you."*

**Dependency:** `email` set up on at least one account.

**Configurable params:**
- `accounts`: `[primary]` (default) | `[all]` | specific accounts
- `urgency_threshold`: `today` (default) | `this_week`
- `max_items`: `3` (default — hard cap)

**Output format:**

```
<count_phrase> need you today:
- <person/source>: <one-line description> (<reason urgent>)
```

If nothing meets the urgency threshold, omit the section entirely (rather than *"nothing urgent"*). Absence speaks for itself; the brief stays focused.

**Self-degradation:** surface `[inbox_urgency — email not configured — run os-email setup to enable]` and continue.

---

## `delight`

**What it surfaces:** A small useful tidbit from recent saved-for-later content. Light dopamine.

**Dependency:** logging enabled + at least some captures.

**Configurable params:**
- `enabled`: `true` (default)
- `freshness_days`: `7` (default)
- `relevance_filter`: `auto` (default — match to today's focus or upcoming meetings) | `random`

**Output format:**

```
Saved-for-later worth a glance: <one-line framing> argues <claim or insight>. <relevance hook if found>.
```

**When to skip the section:** no captures in window, or none substantive enough. Empty is better than forced — section omits silently.

---

## `more_menu`

**What it surfaces:** A numbered list of deep-dive options the user can ask for if they want more. Generated dynamically based on what has content right now and what's enabled in user config.

**Dependency:** none (it's a meta-element pulling from other elements).

**Configurable params:**
- `enabled`: `true` (default)
- `available_options`: list of deep-dive elements to include in the menu when they have content. Default: all six (`pattern_offers`, `yesterday_loose_ends`, `system_worklog_reminder`, `full_tracker_view`, `inbox_by_category`, `recent_knowledge`). User can disable specific items in setup.

**Output format:**

```
Want more? Just ask:
  1. <option name> (<one-line preview / count>)
  2. <option name> (<one-line preview / count>)
  ...
```

Each line: numbered + name + brief preview where useful (count, one-line summary).

**Selection logic:**
1. For each option in `available_options`, check whether the underlying deep-dive element has content
2. If yes, include with a one-line preview (count, latest item, etc.)
3. If no, omit silently
4. If all are empty or all disabled, omit the menu section entirely

**Why a meta-element:** keeps the default brief tight while the dropped elements stay one ask away. ADHD-friendly: the data is available without overwhelming.

---

## `custom_anchor`

**What it surfaces:** A user-defined opening question, mantra, or daily framing.

**Dependency:** none.

**Configurable params:**
- `prompt` (string, required if enabled) — the user's anchor text
- `position`: `closing` (default — replaces open handoff at end) | `top` (replaces opener) | `inline` (own section)

**Output:** depends on prompt shape — question gets AI's brief answer, mantra surfaces verbatim, reflection prompt surfaces as-is.

---

# Deep-dive elements (menu options)

These don't appear in the default brief. They show as numbered items in the `more_menu` and run when the user asks for them — by number ("show me 2") or natural language ("yesterday's loose ends").

## `pattern_offers`

**What it surfaces:** Proactive-prompting candidates accumulated since the last brief that haven't fired inline. On the first brief ever (no prior brief to anchor to), look over the trailing 14 days — the proactive-prompting window — instead.

**Dependency:** logging enabled + `proactive_prompting.enabled: true`.

**Menu preview:** *"Pattern offers (N accumulated)"*.

**On invocation, output format:**

```
Patterns I noticed:
- You drafted 3 client check-in emails since Tuesday with similar phrasing. Want a skill for that?
- You've added 5 follow-up tasks to your tracker this week. Want a skill that drafts the follow-up email and tracks it together?
```

If user accepts, route to `os-skillify/microtool-from-job`. If user defers/rejects, update `os-inputs/_os-proactive-prompts-rejected.md`.

---

## `yesterday_loose_ends`

**What it surfaces:** Recent task-audit lines from inbox, especially items that left work in flight.

**Dependency:** logging enabled.

**Configurable params (in menu config):**
- `days_back`: `1` (default) | range 1-7

**Menu preview:** *"Yesterday's loose ends (N threads)"*.

**On invocation, output format:**

```
Yesterday's loose ends:
- Drafted client check-in email — saved to inbox, not sent yet
- Researched Lego principle for content — captured to knowledge
- 2 unprocessed inbox captures from Tuesday
```

---

## `system_worklog_reminder`

**What it surfaces:** Long-running unresolved items in `os-tracker/system.md`.

**Dependency:** `tracker`.

**Configurable params (in menu config):**
- `age_threshold_days`: `14` (default) | range 7-90
- `max_items`: `5` (default — broader than the default-brief version since the user explicitly asked)

**Menu preview:** *"System worklog (N long-running items)"*.

**On invocation, output format:**

```
Long-running threads in system worklog:
- Bear adapter for tracker (sitting since 4/18)
- email Cross-account learning (sitting since 4/22)
- skillify-from-job sub-mode (sitting since 4/25)
```

---

## `full_tracker_view`

**What it surfaces:** The user's full tracker (Next + areas + bugs + needs + ideas + backlog) — pass-through to `os-tracker/view`.

**Dependency:** `tracker` (auto-creates).

**Menu preview:** *"Full tracker view"*.

**On invocation:** route to `os-tracker/view --context user`.

---

## `inbox_by_category`

**What it surfaces:** Counts + items per email label. Pass-through to a fuller email report.

**Dependency:** `email` set up.

**Menu preview:** *"Inbox by category"*.

**On invocation:** show counts per label across configured accounts, with top items per label.

---

## `recent_knowledge`

**What it surfaces:** Recent additions to `os-knowledge/` files — what the user has been thinking about or filing away.

**Dependency:** captures landing in knowledge.

**Configurable params (in menu config):**
- `freshness_days`: `7` (default)

**Menu preview:** *"Recent knowledge captures (N)"*.

**On invocation, output format:**

```
Recently added to knowledge:
- claude-agent-harnesses.md (2 days ago)
- 3 captures filed into existing topics
```

---

# Element ordering (default brief)

Default ordering optimized for ADHD-aware reading flow:

1. `opener` (calibration)
2. `focus_picks` (the choice — lead with this; it's the brief's spine)
3. `calendar` (command of time)
4. `inbox_urgency` (command of asks)
5. `delight` (small dopamine spike — only when something earns it)
6. `more_menu` (the deep-dive options)
7. `custom_anchor` if positioned as `closing`, otherwise the open handoff is generated

**Getting Started aside:** when the tracker still has a "Getting Started" section, the brief
may fold in *one* item as a soft, low-pressure offer near the handoff — phrased as a two-door
choice (set up the next thing, or get more from what's already built), leaning toward using
what exists. At most one per brief, never as a `focus_pick`, omitted entirely once the
section is cleared. This is the once-a-day cadence the Getting Started design relies on.

User can reorder. Power-user pattern: put `calendar` first if your day is meeting-dominated; put `custom_anchor` at top if you have a daily mantra.

---

# Visual style options

Per ADHD-coach guidance about emoji overstimulation. Default minimal.

- **`minimal`** (default) — clean prose, blank-line separation, no emoji
- **`sectioned`** — light section markers (▸ or — only)
- **`rich`** — emoji for delight, calendar (📅), inbox (✉️), only when user prefers

---

# Adding new elements

When real use surfaces a useful piece the catalog doesn't cover, propose via `loop refine daily-assist`. New elements should declare which tier they belong to (default-brief or deep-dive). Default-brief elements compete for the <250-word budget; deep-dive elements just join the menu, lower bar.

Required for a new element entry:

- Name (short, conversational, lowercase-with-underscores)
- Tier (default-brief or deep-dive)
- What it surfaces (one sentence)
- Dependency (skill or capability required)
- Configurable params (with defaults)
- Output format (the prose shape)
- Self-degradation behavior
- Selection / fetch logic

The "earns its place" principle: new elements ship with clear daily-use signal, not speculatively. The brief is small on purpose; the menu is open but each item earns its line.
