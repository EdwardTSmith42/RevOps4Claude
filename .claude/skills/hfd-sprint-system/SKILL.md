---
name: hfd-sprint-system
description: Use when working on the HFD Analytics team's sprint management system — modifying sprint cadence or naming, changing the dashboard layout or charts (burndown lines, per-person tiles, BU breakdown, KPIs), adjusting rollup math, adding or removing team members, changing pipeline stages that count as sprint-eligible, debugging the daily HubSpot workflow (Action A or Action B), troubleshooting why the SharePoint dashboard is stale or charts aren't rendering, or onboarding to the project for the first time.
---

# HFD Analytics Sprint System

A scrum system for the HFD RevOps Analytics team built entirely on top of HubSpot, with a self-publishing **inline-SVG** HTML dashboard hosted via SharePoint embed. This skill is the on-ramp for anyone modifying the system.

**Read [the spec](../../docs/superpowers/specs/2026-04-14-hubspot-analytics-sprint-system-design.md) and [the runbook](../../docs/runbook.md) before making structural changes.** This skill is the index pointing at them.

## When to use this skill

Pull this skill in when you hear or see any of:

- "Sprint", "burndown", "scrum", "story points", "velocity" in the HFD analytics context
- A request to **change sprint structure** — cadence (currently 2 weeks), naming (`YYYY-S##`), pipeline stages, or which stages count as in-scope
- A request to **change dashboard reporting** — KPI tiles, burndown chart styling/lines, per-person tiles, BU breakdown, charts
- A request to **add or remove a team member** from the sprint roster
- The dashboard is broken (charts blank, file empty, stale, throwing errors)
- The **SharePoint copy looks stale** but the server copy is current (folder path mismatch — see troubleshooting)
- The HubSpot workflow `Analytics Sprint — Daily` failed
- A ticket "isn't showing up" in the sprint or "is stuck tagged in Backlog"
- A new sprint started and something didn't transition correctly
- You're being onboarded to the project and don't know where anything lives

## Architecture in 30 seconds

```
HubSpot                            REVOPS-SERVER                    SharePoint
─────────                          ─────────────                    ──────────
[Team] ─→ [Workflow @ 5am CST]                                       Marketing
   ├ Action A: tag tickets         [Task @ every 15 min, 7am-7pm]      site
   └ Action B: rollups + lifecycle      ├ run-dashboard.bat           ↑
                                        ├ Node generator              │
[Tickets w/ analytics_sprint]           │  → dashboard.html            │
                                        │    (pure inline SVG, no JS) │
[Sprint tickets in pipeline             └ Python push-to-sharepoint───┘
 "Analytics Sprints"]                     (via Graph API, reuses
                                           OneDriveSyncJobs Entra app)
                                                                     Site Page
                                                                     iframes
                                                                     dashboard.html
```

Three pieces, each in its own place:

1. **HubSpot daily workflow** (Ops Hub Pro, custom-coded actions) — owns ticket tagging and sprint metadata
2. **REVOPS-SERVER scheduled task** — generates the HTML and pushes to SharePoint via Graph API every 15 min
3. **SharePoint Marketing site page** — embeds the dashboard via iframe at a stable share URL

**Critical:** the dashboard is **strictly inline SVG** with **no JavaScript at view time**. SharePoint's CSP blocks inline `<script>` tags inside iframe-embedded pages. Anyone "modernizing" by re-adding Chart.js, React, or any client-side library breaks SharePoint embed. This is a hard architectural constraint, not a stylistic choice.

## Quick reference: where things live

| Concern | Path |
|---|---|
| Spec (design rationale) | `docs/superpowers/specs/2026-04-14-hubspot-analytics-sprint-system-design.md` |
| Runbook (operational tasks) | `docs/runbook.md` |
| Admin guide (HTML, for HubSpot admins) | `docs/admin-guide.html` |
| Pure logic (testable, reused in actions) | `src/lib/*.js` — `sprint-math`, `ticket-scoping`, `rollup-compute`, `health-compute`, `yaml-capacity`, `stages`, `constants` |
| Action A wrapper (HubSpot custom code) | `src/actions/action-a-tag-tickets.js` |
| Action B wrapper (HubSpot custom code) | `src/actions/action-b-rollups.js` |
| Build concatenator (lib + wrapper → single file) | `tools/build-actions.js` |
| Built actions to paste into HubSpot | `build/action-a.js`, `build/action-b.js` |
| Dashboard generator (runs on REVOPS-SERVER) | `src/scripts/generate-dashboard.js` |
| Dashboard push to SharePoint (Python, runs after generator) | `src/scripts/push-to-sharepoint.py` |
| Server-side bat wrapper (sequences generate → push) | `tools/run-dashboard.bat` |
| Scheduled-task installer (PowerShell) | `tools/schedule-dashboard.ps1` |
| Setup scripts (idempotent) | `src/scripts/setup-hubspot-schema.js`, `preseed-sprint-options.js`, `bootstrap-sprint-1.js`, `verify-shapes.js`, `verify-hubspot.js` |
| Local dry-run harness for actions | `src/scripts/run-action-locally.js` |
| Tests | `test/*.test.js` (run with `npm test`) |

## Quick reference: the dashboard generator's structure

`src/scripts/generate-dashboard.js` is one large file. Major sections, top-to-bottom:

1. **Imports + Chart.js note** (top ~25 lines)
2. **SVG generators** — `renderBurndownSvg`, `renderSparklineSvg`, `renderBuBarSvg`, `renderBuHistorySvg`. Edit these to change chart visuals. Each builds raw SVG markup as a string.
3. **HubSpot data fetchers** — `getSprintPipeline`, `getActiveSprintTicket`, `getAllSprintTickets`, `getTaggedWorkTickets`, `getOwnerLookup`. Wrapped by `api()` which includes 429 retry-with-backoff.
4. **Number/data helpers** — `num`, `isOpen`, `pctOf`, `escapeHtml`, `parseCapacityYamlSimple`
5. **`buildBurndownData`** — produces `{ labels, ideal, committedRemaining, totalRemaining }` per-day series for the team chart. Uses `analytics_sprint_added_mid_sprint` to classify committed vs added tickets.
6. **`buildPerPersonBurndown`** — same logic scoped per-owner, returns `{ name, committed, addedPoints, totalRemaining[], committedRemaining[] }` per person.
7. **`htmlTemplate`** — one giant template literal with the full HTML. KPI tiles live here, as does the section markup.
8. **`main`** — orchestrates fetch, compute, render, write, push.
9. **Watchdog + exit** — 90-second self-kill timer, explicit `process.exit(0)` after main.

## Quick reference: the data model

| Object | Property | Purpose |
|---|---|---|
| Ticket (work) | `analytics_sprint` | Multi-select; ticket's sprint history. Additive-only by Action A. |
| Ticket (work) | `analytics_sprint_count` | Length of `analytics_sprint`. Used for sort/carryover. |
| Ticket (work) | `analytics_sprint_added_mid_sprint` | True when first tagged after sprint start (scope addition). Reset on each new first-time tag. **Drives the dual-line burndown's classification.** |
| Ticket (work) | `analytics_point_warning` | `ok` / `unpointed` / `too_large` |
| Ticket (work) | `is_blocked`, `blocked_reason` | Blocker tracking |
| Ticket (sprint) | `sprint_name`, `sprint_start_date`, `sprint_end_date` | Sprint identity |
| Ticket (sprint) | `sprint_committed_points` | Frozen at kickoff |
| Ticket (sprint) | `sprint_completed_points`, `sprint_carryover_points`, `sprint_scope_added_points`, `sprint_blocked_count`, `sprint_forecast_points`, `sprint_health` | Recomputed daily by Action B |
| Ticket (sprint) | `sprint_capacity_yaml` | Per-person commitment in YAML; source of truth for per-person committed |
| Ticket (sprint) | `sprint_per_person_summary_yaml` | Derived per-person rollup |
| Ticket (sprint) | `sprint_kickoff_posted`, `sprint_closeout_posted` | Idempotency markers for note posting |
| HubSpot Team | `RevOps Analytics` | Members are the sprint roster (Plan A); `secondary_owner` also counts |
| Pipeline | `Analytics Sprints` (id `890861150`) | Holds one ticket per sprint, stages: Planning → Active → In Review → Closed |
| Stage filter | `EXCLUDED_STAGE_IDS` in `src/lib/stages.js` | Currently excludes Backlog (`210361775`); add IDs here to exclude additional stages |
| SharePoint target | `Analytics Sprint/dashboard.html` in Marketing site Documents | Hardcoded in `src/scripts/push-to-sharepoint.py` as `TARGET_FILE`. Must match the path the iframe is reading from. |

## Common operations — how to do X

### Add a new team member

1. **HubSpot:** Settings → Users & Teams → `RevOps Analytics` team → Add member
2. **Done.** The next 5am workflow run picks them up automatically. Their tickets get tagged starting that morning. The dashboard's per-person row auto-grows.
3. *Optional:* Edit `sprint_capacity_yaml` on the active sprint ticket to add their per-sprint capacity. Without this, they appear with 0 committed (which is correct if they have no tagged tickets at kickoff).

### Remove someone from the team

1. HubSpot Settings → Teams → remove from `RevOps Analytics`
2. Their existing sprint tags stay (additive-only). Future tags stop. Their per-person row eventually drops off the dashboard once they have no tagged tickets.
3. The system never auto-removes historical attribution.

### Change sprint cadence (e.g., 2 weeks → 3 weeks)

This is **structural** — touches sprint-math, breaks all historical comparisons, and requires re-running tests. Read `src/lib/sprint-math.js` first.

1. Edit `SPRINT_LENGTH_DAYS` in `src/lib/sprint-math.js` (currently 14)
2. Update tests in `test/sprint-math.test.js` to reflect new dates
3. Run `npm test` — all 47 tests must pass
4. Run `npm run build` to regenerate `build/action-a.js` and `build/action-b.js`
5. **Re-paste both Actions** into HubSpot workflow custom-code editors
6. Update spec/runbook/admin-guide to reflect the new cadence
7. Re-run `npm run setup:preseed` if pre-existing options for the year don't match new dates

### Add or remove an excluded stage

Currently only `Backlog` is excluded. To, e.g., also exclude `Closed: Sent to Business Development`:

1. Find the stage ID via HubSpot → Settings → Tickets → Pipelines, OR via `mcp__834fdc2a-…__get_properties` for `hs_pipeline_stage`
2. Add the ID to `EXCLUDED_STAGE_IDS` in `src/lib/stages.js`
3. `npm test` — `test/ticket-scoping.test.js` should still pass
4. `npm run build`
5. Re-paste `build/action-a.js` into HubSpot

### Modify the burndown chart

Two functions to know:

- `buildBurndownData(workTickets, sprint, committed)` — returns `{ labels, ideal, committedRemaining, totalRemaining }`. The math. Edit if you want to change WHAT is shown (e.g., add a third series, change classification logic).
- `renderBurndownSvg(data)` — returns SVG markup. Edit if you want to change HOW it's shown (line styles, annotations, legend, axes).

The current chart shows two step lines: solid blue for total scope (committed + added), dotted gray for committed-only. Each upward step on total scope is annotated with a `+N pts` badge so additions are explicit. The "ideal" series is computed but not rendered — kept in the data shape for backward compatibility.

The per-person sparklines mirror this: `buildPerPersonBurndown` produces the same per-day series scoped to one owner, and `renderSparklineSvg(totalSeries, committedSeries)` renders both as steps in 220×60.

### Add a chart, KPI, or column to the dashboard

The dashboard is a single HTML template inside `src/scripts/generate-dashboard.js`. To add something:

**A new KPI tile (5th, 6th, etc.):**
1. Edit `grid-template-columns: repeat(5, 1fr)` in the CSS to match the new tile count.
2. In the data prep block (search `const data = {`), add the value you need.
3. In the template's KPI section, add another `<div class="kpi">...</div>`.

**A new chart:**
1. Compute the data in the data-prep section.
2. Write a new SVG renderer next to `renderBurndownSvg` etc.
3. Add a section in the HTML template that calls your renderer.
4. Test locally with `DASHBOARD_OUTPUT_PATH='./build/dashboard.html' node src/scripts/generate-dashboard.js`. Open in a browser.
5. Deploy: copy file to server (see "Deploy generator changes" below).

**A new column on the open-tickets table:**
1. Add a `<th>` and `<td>` to the table markup.
2. Compute the new value in the `data.openTickets` map block.
3. Test, deploy.

**Hard rule:** never add `<script>` tags or `<canvas>` elements. Pure SVG only. SharePoint CSP blocks scripts even inside the iframe.

### Change the rollup math

Pure functions in `src/lib/rollup-compute.js` and `src/lib/health-compute.js`. Each has tests in `test/`. Edit, run `npm test`, rebuild actions, re-paste.

**Rule:** never change rollup math without a test. The math is the contract with stakeholders. Untested changes break trust.

### Deploy generator changes (quickly, without re-registering the task)

1. Copy `src/scripts/generate-dashboard.js` (or whatever changed) to `\\REVOPS-SERVER\Scripts\AnalyticsSprintDashboard\project\src\scripts\` via PSSession `Copy-Item -ToSession`
2. Trigger one immediate run: `Invoke-Command -ComputerName REVOPS-SERVER.OFFICE.LOCAL -ScriptBlock { Start-ScheduledTask -TaskName 'AnalyticsSprintDashboard' }`
3. Wait ~10 seconds, check `Get-ScheduledTaskInfo -TaskName 'AnalyticsSprintDashboard'` — `LastTaskResult` should be `0`
4. SharePoint copy refreshes within seconds via the Graph API push

### Deploy a new HubSpot Action (Action A or B)

1. `npm run build` regenerates `build/action-a.js` and `build/action-b.js`
2. In HubSpot: Automation → Workflows → `Analytics Sprint — Daily` → click the action → paste the entire file content into the code editor → save
3. Test in HubSpot's "Test" panel with `dryRun: "true"` first if making logic changes
4. Save & enable

### Change the SharePoint target folder

If the team reorganizes the Marketing doc library:

1. Edit `TARGET_FILE` near the top of `src/scripts/push-to-sharepoint.py`. Use forward slashes for folder separators (e.g., `"Analytics Sprint/dashboard.html"`).
2. Copy the updated file to the server.
3. Trigger an immediate run; verify the file appears at the new path in the SharePoint library.
4. **Update the SharePoint Embed web part** to use the new file's `:u:/s/` share URL — the old URL still resolves to the old item ID and won't show the auto-updated content.

The Entra app reused from `OneDriveSyncJobs/.env` has tenant-wide write access, so any site path works.

## Troubleshooting

| Symptom | First check | Likely cause |
|---|---|---|
| Dashboard shows stale data | Server scheduled task `LastRunTime` | Task disabled, server down, or generator throwing |
| Dashboard is empty (0 bytes) | `LastTaskResult` on the task | Generator crashing — run manually on server, read stderr |
| **Server copy is current but SharePoint copy is stale** | Diff between `TARGET_FILE` in `push-to-sharepoint.py` and the path the iframe is reading from | The iframe is pointing at a different file in the library than the script is updating. Either fix the path in the script (preferred) or update the iframe URL. |
| Charts not rendering in SharePoint | Source HTML has `<script>` or `<canvas>` tags? | Almost certainly someone re-introduced JS or Chart.js to the template — SharePoint's CSP blocks inline scripts even via iframe |
| Sprint 2 (or any future sprint) didn't auto-create | HubSpot workflow run history | Action A failed, or stage transition logic blocked. Check S1 ticket — should be in In Review/Closed |
| Tickets in Backlog stage are tagged | They are — until next Action A run | Backlog untag runs every 15 min via Action A; should self-resolve |
| Person missing from dashboard | Their owner ID in `sprint_capacity_yaml` of active sprint? | Add them to the YAML; they'll show with 0/0 |
| HubSpot 429 rate limits | Action A/B logs in workflow history | Retry-with-backoff is built in; if persistent, spread runs across more time |
| Server unreachable | Ping (kernel responsive?) and WinRM (Test-WSMan) | Possibly Node OOM regression — see runbook crisis section. Hardened version uses `IgnoreNew` + `--max-old-space-size=200` to prevent it |
| SharePoint upload returns 403 | Graph token / app permissions | The Entra app at `C:\Scripts\OneDriveSyncJobs\.env` may have lost write scope; talk to whoever provisioned it |

For full crisis recovery (server unresponsive, OOM event, etc.), see the **Troubleshooting** section in `docs/runbook.md`.

## Don'ts — things to think twice about

- **Don't add inline `<script>` tags or `<canvas>` elements to the dashboard template.** SharePoint's iframe CSP blocks them; the dashboard goes blank for everyone. All visualization must be pre-rendered SVG.
- **Don't run two folders' worth of `dashboard.html` in SharePoint.** If you reorganize the doc library, pick one canonical path, update `TARGET_FILE` in `push-to-sharepoint.py`, and **delete the old file** so future operators don't get confused which one is fresh.
- **Don't remove a sprint enum option** while it's still on existing ticket records. The ticket's stored value will become orphaned. Wait until 18+ months after the sprint to prune.
- **Don't `git commit` the `.env` file.** It contains the HubSpot private app token. The repo's `.gitignore` already excludes it.
- **Don't bypass the `npm run build` step** before pasting actions. The wrapper depends on inlined lib files, and editing the built file directly creates drift.
- **Don't manually edit `sprint_committed_points` mid-sprint.** It's frozen at kickoff by design. If you need to override, do it before the first Action B run after Planning → Active.
- **Don't run `bootstrap-sprint-1.js` more than once.** It's a one-time recovery script. For new sprints, the daily workflow handles everything.
- **Don't manually delete the SharePoint dashboard file.** The Python pusher overwrites in place — the share URL stays valid only because the file's underlying SharePoint item ID is preserved. If deleted, the embed breaks and the site page needs a new share URL.

## Setup for a new contributor (first time on this project)

1. Clone the repo
2. `npm install`
3. Get a HubSpot private app token (ask the team lead) and create `.env` at the project root: `HUBSPOT_PRIVATE_APP_TOKEN=pat-na1-...`
4. `npm test` — confirm 47/47 tests pass on your machine
5. `npm run dashboard` — generates a dashboard locally at `build/dashboard.html`. Open it to confirm rendering. Charts should be SVG.
6. Read `docs/runbook.md` cover-to-cover (about 5 minutes)
7. You can now run actions in dry-run mode locally: `node src/scripts/run-action-locally.js a --dry-run --use-known-roster`

## Installing this skill in your Claude session

The skill ships in this project's `skills/hfd-sprint-system/` folder. To make Claude Code load it:

**Option 1 — Per-project (recommended for the team):**
Symlink or copy the skill folder into your project's `.claude/skills/`:
```bash
ln -s ../../skills/hfd-sprint-system .claude/skills/hfd-sprint-system
```
(Note: the project's `.gitignore` excludes `.claude/`, so each contributor sets this up locally.)

**Option 2 — User-global (if you work on this often):**
Copy the folder to `~/.claude/skills/hfd-sprint-system/`.

Once loaded, Claude finds it automatically when you describe tasks matching the description above.

## Key facts a future Claude WILL forget

- **The dashboard is strictly inline-SVG, no JavaScript at view time.** This is enforced by SharePoint's CSP and is not a stylistic choice. Anyone "modernizing" the dashboard by re-adding Chart.js, React, or any client-side renderer breaks SharePoint embed. Inline SVG is the design contract.
- **The burndown is two step lines, not one smooth line.** Total scope (solid blue) and committed-only (dotted gray). Step rendering (vertical jumps) makes individual scope events visible. Each upward step on total scope is annotated with a `+N pts` badge.
- **Per-person sparklines mirror the team chart at miniature size**, plus a numerical breakdown row underneath (`CMT N · ADD N · DONE N · OPEN N`). The numbers compensate for what the small chart can't show clearly.
- **The SharePoint upload path must match the iframe URL.** If the script pushes to `Analytics Sprint/dashboard.html` but the iframe points at `09 - Analytics/dashboard.html`, the dashboard will look stale forever even though the server is updating.
- **The Entra app credentials live at `C:\Scripts\OneDriveSyncJobs\.env`** (not in this repo). They're shared with other sync jobs. Don't move them, don't recreate them.
