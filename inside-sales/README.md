# RevOps4Claude — Inside Sales dashboard refresh

Daily refresh pipeline for the HFD Inside Sales dashboard.
Published artifact: https://claude.ai/artifact/9BLr5mqzuh8CEEXf8gbN3B

Run it with one command:

```bash
python refresh.py
```

Exits `0` on success, `1` on any failed gate. On failure **nothing is published** and
`data/refresh_log.json` names the step and the error.

---

## What it does

| Step | Script | Gates |
|---|---|---|
| extract | `extract.py` | contacts > 0; contact count within ±60% of the previous run; internal bucket-identity self-check |
| cohort | `build.py` | `data/sourced_pids.txt` non-empty; cohort within ±60% of previous |
| revenue | `tableau_revenue.py` | all five period buckets present and non-null; caveats intact |
| transcripts | `mine_transcripts.py` | stages new calls only (see below) |
| build | `build.py` | file exists; 0 non-ASCII; under 15 MB; all five markers consumed; cohort unchanged |

Flags: `--skip-extract`, `--skip-revenue`, `--skip-transcripts`, `--full-transcripts`.

The cohort step runs **before** revenue on purpose. Revenue filters on
`data/sourced_pids.txt`, and running it first meant revenue was cut from the
*previous* run's provider list.

---

## Secrets

| Variable | Notes |
|---|---|
| `HUBSPOT_SERVICE_KEY` | HubSpot private-app token. Set **only this one.** `extract.py` reads `HUBSPOT_ACCESS_TOKEN` first and falls back to this; `mine_transcripts.py` unsets `HUBSPOT_ACCESS_TOKEN` before shelling to the CLI. Setting both to different values makes them authenticate as different apps. |
| `TABLEAU_PAT_NAME` | Personal access token name from 10az.online.tableau.com |
| `TABLEAU_PAT_SECRET` | The token secret |

Optional overrides: `TABLEAU_POD` (default `10az`), `TABLEAU_SITE`
(default `healthcarefinancedirect`), `TABLEAU_REVENUE_DS`
(default `583b19c2-c2ac-4aa4-a207-4714da9a0262`).

**The Tableau PAT user needs View + Connect + API Access** on that datasource.
API Access is a *separate capability* from Connect and is the one that gates VizQL
querying — without it the token authenticates and then returns nothing, which looks
like a query bug rather than a permission problem.

**PATs expire** after 15 consecutive days unused, and at one year. A routine paused
over a holiday comes back to a dead token.

---

## The HubSpot CLI

Transcript mining needs the HubSpot Agent CLI binary. The diarized transcript is not
reachable over REST — `/crm/v3/objects/calls/{id}` returns `hs_call_body` and
`hs_call_summary` but not the transcript, and the four plausible transcript endpoints
all 404.

Install it at runtime rather than committing it (the binary is platform-specific and
self-upgrades):

```bash
curl -fsSL https://api.hubapi.com/hub/cli/backend/hub-cli/latest/install.sh | sh
export PATH="$HOME/.hubspot/bin:$PATH"
```

---

## Transcript mining is two-phase

`mine_transcripts.py` **stages** files — it does not mine them. A model reads the
staged `.txt` files in `data/transcripts_new/` and writes `data/vom_delta.json`;
the next `refresh.py` run merges that delta and advances the watermark.

So a run that reports `STAGED` / `OK_PENDING_MINE` is **not finished**, and it exits
`0`. Anything automating this must check the transcripts step, not just the exit code.

State lives in `data/vom_state.json` — mined ids plus a date watermark. It must be
committed back after a successful run or every run re-mines from scratch. With no
state at all it bootstraps to the last 30 days rather than the full corpus.
`--full-transcripts` re-mines everything; intended for a weekly run so themes cannot
drift.

Volume: ~25–45 transcripts on a typical daily incremental run, against 2,824 calls for
a full re-mine. A 250-file cap per run bounds the worst case after an outage.

---

## Definitions — fixed, approved by Mel Matthews and Ed Smith

- **Call connect** — an outbound dial of **3 minutes or more**.
- **Demo connect** — a demo recording of **10 minutes or more**.
- **No-show** — a demo-titled meeting whose recording ran **under 10 minutes**.
  This is an *interim proxy* for attendance. Laura Rodriguez is building real
  attendance data from meeting records; it should replace this rule when it lands.
- **Demos** — every meeting whose name contains "demo". Unchanged, and deliberately
  so: it keeps parity with the existing Demos dashboard (21888050).
- **Sourced enrollment** — the practice enrolled in the window **and** the team made a
  real outreach touch (outbound dial, outbound email, meeting, or answered inbound
  call) on or before the enrollment date. Notes, inbound-only email and unanswered
  rings do not qualify.

HubSpot's own automation still runs on call *disposition*, so the disposition-based
connect figure is reported alongside the duration one. Neither corrects the other.

---

## Known holes

- **`data/deals.json` is never regenerated** by `refresh.py`. It is injected into the
  page but no step refreshes it, so the Deals section silently freezes while the rest
  of the page rolls forward.
- **`OK_PENDING_MINE` exits 0.** A caller checking only the exit code will report
  success forever while transcripts never actually mine.
- The duration distribution **cannot be rep-scoped** — the per-rep daily buckets carry
  no duration histogram, so under a rep filter it sums whole contact rows.
- Deal "locations" counts include the parent group record, which differs from the
  Combined card's convention on the same page.

---

## Do not use "HFD Datawarehouse"

The Tableau datasource named `HFD Datawarehouse`
(`20fbf488-ff7a-4a94-8d9f-bebe7e3db6f0`) looks right and is not. Its newest contract is
dated **2023-10-22** and its provider-key domain contains none of the sourced
providers. Pointed at it, the revenue step returns **$0 for every period without
erroring**. Use `v.HfdV3`.

Also: filter the cohort on **Provider Unique Key**, not Contract Provider Key. VDS
validates SET filter values against the field's domain and rejects the entire query if
any value is absent — and most sourced providers have never originated a contract, so
they do not exist in the Contract domain.
