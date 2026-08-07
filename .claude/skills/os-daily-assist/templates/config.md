# Starting shape for `os-inputs/_os-setup-philosophy.md` good_morning section

The `setup` mode writes this. User can hand-edit. Sensible defaults below — companion-feel, ADHD-aware, three focus picks, full deep-dive menu.

```yaml
## good_morning
visual_style: minimal     # minimal | sectioned | rich (per ADHD-coach guidance, default minimal)
elements:
  - name: opener
    enabled: true
    style: warm           # warm | terse | none
  - name: focus_picks
    enabled: true
    count: 3              # 3 (default) | 1 | 5
    friction_reducer: enabled
    active_futuring: enabled
  - name: calendar
    enabled: true
    prep_context: enabled
    day_shape_framing: enabled
    transcripts: auto     # auto (use any wired transcript integration) | disabled
    meeting_lookback_window: 7
  - name: inbox_urgency
    enabled: true
    accounts: [primary]
    urgency_threshold: today
    max_items: 3
  - name: delight
    enabled: true
    freshness_days: 7
    relevance_filter: auto
  - name: more_menu
    enabled: true
    available_options:
      - pattern_offers
      - yesterday_loose_ends
      - system_worklog_reminder
      - full_tracker_view
      - inbox_by_category
      - recent_knowledge
  - name: custom_anchor
    enabled: false        # default off — user opts in if they have one
    prompt: ""
    position: closing
ordering: [opener, focus_picks, calendar, inbox_urgency, delight, more_menu, custom_anchor]
```

## Defaults rationale

- **`visual_style: minimal`** — per ADHD coach pattern, emoji can overstimulate. Default to clean prose. User can opt up.
- **`opener: warm`** — calibration matters. Terse feels cold for most users.
- **`focus_picks: count 3`** — three options for the user to pick from. AI tends to get a single forced pick wrong; three lets the user choose their shape (quick-win / medium / deeper) without overwhelming. Friction-reducer attaches to the chosen pick after the user decides.
- **`calendar: enabled with prep_context + day_shape`** — first-class, never deferred. Day-shape framing leads; meetings come after. Transcript integration auto-detects what's wired.
- **`inbox_urgency: urgency_threshold: today`** — needs-you-only, not counts. Cap at 3 items.
- **`delight: enabled with auto relevance`** — light dopamine, only when something genuinely earns the spot. Section omits when nothing qualifies.
- **`more_menu: all six options`** — full deep-dive menu by default; each option only shows if it has content right now. The dropped-from-default-brief elements live here, one ask away.
- **`custom_anchor: disabled by default`** — opt-in for users with daily mantras or framing questions.

## Ordering rationale

Default ordering reflects ADHD-aware reading flow:

1. **`opener`** — calibrate state
2. **`focus_picks`** — the choice (three options; the brief's spine)
3. **`calendar`** — command of time
4. **`inbox_urgency`** — command of asks
5. **`delight`** — small dopamine spike
6. **`more_menu`** — opt-in depth
7. **`custom_anchor`** — close, if configured

## Power-user reorderings

- **Meeting-dominated days:** `[opener, calendar, focus_picks, inbox_urgency, delight, more_menu, custom_anchor]` — calendar first
- **Mantra-led mornings:** `custom_anchor` with `position: top`
- **Light-touch users:** disable `delight`, `custom_anchor`, and trim `more_menu` options to just 2-3 favorites
- **Single-pick AI-led:** `focus_picks: count: 1` — accept AI's pick (be ready for some misses)
- **Deep-dive heavy:** `focus_picks: count: 5` plus `more_menu: enabled: true` with all six options

## Self-degradation behavior

The brief always renders something useful even when dependencies aren't set up:

- `inbox_urgency` without email → shows *"[email not configured]"* line
- `calendar` without calendar MCP → shows *"[calendar integration not wired]"* line
- `more_menu` items only appear if they have content; empty options omitted silently
- If everything degrades, the user still gets opener + focus_picks (which uses tracker, which auto-creates)

The user can configure daily-assist early; the brief enriches as dependencies come online.
