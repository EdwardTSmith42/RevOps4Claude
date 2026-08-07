---
name: hfd-data-source-integration
description: Use when adding ANY new external data source to the HFD warehouse — a new OneDrive/SharePoint Excel file, a new REST/Google API, or evaluating whether an existing source needs a bigger pipeline than it has. Answers "which of our three integration patterns fits this source" and "what schema shape should I land it in" BEFORE writing code. For the deep gotcha checklist once you've picked the staged-tolerant-load pattern, see hfd-revops-api-sync. For OneDrive specifically, this skill has the concrete step-by-step for adding a new file to the existing framework.
---

# HFD data source integration — pick the right pattern first

## Three real patterns exist at HFD today. Don't default to the heaviest one.

| | **OneDrive/Excel sync** | **API → staged tolerant-load** | **EAV landing (generic multi-shape)** |
|---|---|---|---|
| Built for | `TerritoryAssignment`, `ProviderAccountAssignment`, `VerifiedPaymentKeys` | GSC/GA4 → `Analytics.dw`/`ro` (PBI 25416) | Fillout, 53 forms → `dw.FactFilloutAnswers` (PBI 25568) |
| Source shape | One flat table per file, small (~hundreds–low thousands of rows) | Structured, multiple related grains (query×page, date totals) | Heterogeneous — every source record can have a different shape |
| Target shape | Direct SQL table, no staging layer | `stg` → `Fact`/`Dim`, declared grain + `UNIQUE` | Generic `SubmissionId/QuestionId/Value` rows, one schema for everything |
| Write path | Direct `INSERT`/`TRUNCATE` from Python, dev's own Windows identity (`Trusted_Connection`) | `stg` → tolerant-load proc → `Fact` (applock, `DELETE`, reject table) | Same tolerant-load shape as API pattern, but append-only (see below) |
| Auth | Azure AD app registration, client-credentials (no interactive gate, ever) | Google OAuth/ADC (one-time interactive consent) or API bearer key | REST bearer key |
| Where the code lives | `RevOps/OneDriveJobs/` — extend an existing file, usually | `RevOps/<NewJobName>/` — new job folder | Same as API pattern |
| Effort for a new source | Often a ~30-line class + one registry line + one `.bat` line | New DBUp objects + new Python job + Finance_Scratch verification | Same as API pattern, minus a per-source schema |

**Decision rule:** start from "what's the smallest pattern that's actually correct for this source," not "what did we build last time." Ask, in order:

1. **Does a table for this already exist and does the new source match its shape?** → You're extending, not building. See "Adding a new OneDrive/SharePoint file" below — this is usually the cheapest path in the whole org.
2. **Is the source small (thousands of rows, not millions), single-shaped, and does the source system act as sole source of truth (safe to fully replace on every run)?** → OneDrive-style direct write, even if the source isn't literally OneDrive (a small vendor CSV export fits this too). No staging layer, no tolerant-load ceremony — that machinery is overhead this doesn't need.
3. **Is the source large/high-volume with real grain complexity (e.g. a metric that needs both a detail grain and a reconciling totals grain), needs point-in-time revision handling, or feeds Tableau/cross-warehouse joins?** → Staged tolerant-load into `Fact`/`Dim`. Go read `hfd-revops-api-sync` now for the full build checklist — don't reinvent it.
4. **Does the source have no fixed schema — every record (form, event type, ticket type) can carry different fields, and you don't yet know which ones matter for reporting?** → EAV landing layer, raw first, reporting later. See "Choosing EAV vs Fact/Dim" below.

Getting this wrong in either direction is expensive: building a full staged-tolerant-load pipeline for a 200-row lookup table is pure overhead nobody will maintain; building a direct-write table for a source that turns out to need Tableau joins and revision handling means a rebuild later. The design-doc step of brainstorming a new source should name which of the four answers above applies and why, before any schema gets written.

## Choosing EAV vs Fact/Dim vs flat table (the "right data model up front" question)

This was the single highest-leverage decision on the Fillout build, made explicit in the design doc before any DDL was written:

- **Flat table** (one row per record, typed columns) — when the source has ONE shape that isn't going to change. `TerritoryAssignment` (MatchType/MatchValue/Territory) is this. Don't over-model something this simple.
- **Fact/Dim with a declared grain** — when the source has a small number of *known, stable* entity types with real relationships (a submission belongs to a form; a GSC row belongs to a date+query+page), and downstream consumers need to join/aggregate. The SEO pipeline's `FactSeoGscDaily` + separate `FactSeoDailyTotals` exists because the detail grain and the totals grain **do not reconcile to each other** (GSC's own anonymization/aggregation quirks) — that's a real example of "figure out the actual grain(s) before building," not an assumption.
- **EAV** (`SubmissionId, QuestionId, QuestionName, QuestionType, AnswerValue`) — when the source is genuinely heterogeneous and you'd otherwise be building N per-source schemas or one impossibly wide table. Fillout has 54 forms sharing zero common questions; a fixed-column schema would mean constant migrations, and one global wide table would mean hundreds of mostly-NULL columns. The tradeoff: EAV pushes the "what does this data mean" question downstream to reporting time. That's the right tradeoff when you don't yet know which of 54 sources anyone will actually build a dashboard on — don't build 54 dashboards' worth of schema speculatively. Build the reporting view/table for a specific source only once a real consumer exists (this was an explicit, deliberate deferral on the Fillout build, not an oversight).

If a source is EAV-shaped AND high-volume/ever-growing (like form answers, which accumulate forever and where a source-side rename shouldn't destroy history), make the fact table **append-only**: never `UPDATE` a row in place, insert a new row only when the value actually changed (compare against the most-recently-loaded row for that natural key), and never retroactively rewrite an old row's value/redaction decision. This is what lets a source-side field rename become "new history," not "silently corrupted or unexplainably overwritten history."

## Adding a new OneDrive/SharePoint Excel file — concrete steps

The framework already exists at `RevOps/OneDriveJobs/` (`onedrive_sync.py` = base classes + one working example; `provider_assignment_sync.py` = a second file extending the same base classes for two more syncs). **Read both files first** — this walkthrough describes their actual current shape, not a hypothetical.

### 1. Get the sharing link
In OneDrive/SharePoint: right-click the file → **Share** → **Copy Link**. Must be a link the Azure AD app registration backing this framework can resolve via Graph — if it 404s in `resolve_sharepoint_url()`, the app doesn't have access to that drive/site; that's an Azure AD permissions question, not a code bug.

### 2. Pick the base class
- **`OneDriveSync`** (single column, insert-new-keys-only, dedup by a key set) — use when you're syncing a list of values that only ever grows (e.g. `VerifiedPaymentKeysSync`: one column, insert whatever's not already in the target table).
- **`TruncateReloadSync`** (multi-column, whole table replaced every run) — use when the Excel sheet is a small, human-maintained lookup/config table where "the sheet is the current truth, blow away and reload" is correct (e.g. `TerritoryAssignmentSync`, `ProviderAccountAssignmentSync`). This is the more common case for a genuinely new mapping/config source.

### 3. Write the subclass
For `TruncateReloadSync` (the common case), define:
```python
class YourNewSync(TruncateReloadSync):
    SYNC_NAME = "your-new-sync"                          # CLI-facing name
    SHAREPOINT_URL = "https://.../:x:/p/.../<share-id>"  # from step 1
    WORKSHEET = "Exact Sheet Name"                        # case-sensitive, verify against the real file, not a similarly-named old copy
    TARGET_TABLE = "analytics.dw.YourTargetTable"          # must already exist — this framework does NOT create tables

    COLUMNS = [
        ("Excel Header Text", "SqlColumnName", True),   # (excel header, sql column, required)
        ("Another Header",    "AnotherCol",    False),
    ]
```
Override `read_excel_worksheet()` only if you need custom parsing beyond string-trim — real examples already in the codebase: casting a numeric-looking string to `int` (`ProviderKey`), zero-padding zip codes to 5 digits, normalizing an enum value (`"Extended Only"` → `"ExtendedOnly"`). Call `super().read_excel_worksheet()` first, then post-process.

### 4. Register it
At the bottom of the file that defines your class:
```python
SYNC_REGISTRY['your-new-sync'] = YourNewSync
```
(`provider_assignment_sync.py` does this by importing `SYNC_REGISTRY` from `onedrive_sync` and adding to the same dict — new sync files don't need their own `main()`/CLI wiring if they follow this pattern, though `provider_assignment_sync.py` does define its own `main()` for a friendlier multi-sync CLI; either works.)

### 5. Verify the target table's column shape matches exactly
This framework has zero DDL-generation — if `TARGET_TABLE` doesn't exist yet or its columns don't match your `COLUMNS` list, you'll find out at runtime, not at review time. If the table doesn't exist, that's a normal DBUp DDL PR first (see `hfd-database` skill), following the org's naming/type/audit-column conventions — small lookup tables like this typically don't need the full `stg`/`Fact` split, just the table itself.

### 6. Dry-run before anything real
```
python onedrive_sync.py your-new-sync --dry-run
```
(or `python provider_assignment_sync.py your-new-sync --dry-run` if that's where you added it). Confirms parsed row count and preview without touching the database. Do not skip this — a wrong `WORKSHEET` name or a required-column mismatch fails loudly here, cheaply, instead of at 3am against production data.

### 7. Wire it into scheduling
- **If extending an existing job's cadence** (e.g. adding a third sync alongside Provider/Territory Assignment, same acceptable staleness): just add another `python provider_assignment_sync.py your-new-sync` block to the existing `.bat` file. No new scheduled task needed at all — this is the cheapest possible path.
- **If it needs its own independent schedule**: new `.bat` file, then register a new Scheduled Task **locally on revops-server** (RDP/interactive, not WinRM — see `hfd-revops-api-sync`'s RPC/scheduling gotchas, which apply here too). Stagger the trigger time against the existing job list; check what's already scheduled first.

### 8. Config
The framework's `.env` needs `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID` (Graph app-registration credentials, shared across all syncs in this framework — you're not minting new Azure AD credentials per source), plus `SQL_SERVER`/`SQL_DATABASE`. **The SQL connection itself uses `Trusted_Connection=yes`** — it runs as whatever Windows identity the scheduled task executes under, not a separate SQL login/password pair. This is a real architectural difference from the API-pattern jobs (which use SQL auth with a dedicated writer login) — don't assume you need to provision new SQL credentials for a new OneDrive sync; you need the *scheduled task's* Windows identity to already have write access to the target table, which is usually already true if you're extending an existing job that runs under the same identity.

## Cross-cutting lessons (apply regardless of which pattern you pick)

- **Verify real source facts before building, don't assume from docs.** Fillout's actual pagination cap (150, not the docs' example of 50), GSC's ~3-day revision window, and the fact that GSC's query×page grain doesn't reconcile to its own headline totals were all discovered by testing against the live source, not by reading documentation. Budget time for this as its own step.
- **`.env`-driven paths/config must be read AFTER `.env` is loaded, not at module import time.** A module-level `Path(os.environ.get(...))` constant freezes before `load_env()` ever runs if `load_env()` is called inside `main()`. Use a function, called at point of use, not a constant. This exact bug shipped and was caught in review on the Fillout build — check for it explicitly on any new job.
- **Test under the credentials the job will actually run as**, not your own elevated dev login. Different identities can have wildly different grants even in the same "scratch" database (`dw` DDL-only vs `dbo` full DML+ALTER was a real, useful distinction discovered mid-build) — a query that works under your login can silently lack `ALTER`/`REFERENCES`/`INSERT` under the real deploy identity. If you can't get the real identity provisioned yet, at least prove the *mechanics* (parameterized queries, transaction handling) under any identity with equivalent DML rights, and call out clearly what's still unverified under the real one.
- **Every NOT NULL column on the target needs a corresponding NULL-check before promotion — every one, not just the obvious key columns.** This bug shipped THREE separate times across one build (once per fact table) because each fix was checked in isolation instead of as a pattern — the fourth time, a holistic final review caught it before merge. When you fix one, grep for the same shape everywhere else in the same PR.
- **PII/sensitive-field redaction needs two layers**: name-pattern (field label) AND content-pattern (regex on the actual value) — free-text fields can carry sensitive data under an innocuous label. Short name-pattern tokens (3-4 letters) need word-boundary matching or they false-positive on ordinary words ("business" contains "sin"; "company" contains "pan").
- **Concurrent-run protection is two separate layers that don't substitute for each other**: a Python-side exclusive-create lock file (prevents two orchestrator processes running at once) and SQL-side `sp_getapplock` in promotion procs (prevents concurrent writes to the same table even from two different callers). Don't assume one covers the other.
- **A lock/mutex that's "never auto-cleared" (correct, for safety) still needs a staleness *alert*, even if it doesn't auto-clear.** Otherwise an orphaned lock from a crashed run silently defeats every future scheduled run with zero alerting — the exact failure mode the alerting design was supposed to prevent.
- **Credentials for production writer logins are almost always a genuine human/DBA gate**, not something to work around. Build and fully verify against a scratch database first (Finance_Scratch), open the PR as draft with the gate explicitly named, and don't let "no credentials yet" block writing and verifying the code itself.

## See also
- `hfd-revops-api-sync` — the detailed gotcha checklist once you've picked the staged-tolerant-load pattern (proc signature drift, the 5AM revops-server thundering herd, DBUp's global-numbering deploy-order trap, etc.)
- `hfd-database` — general DBUp/DDL conventions (naming, types, audit columns) that apply to any new target table regardless of pattern
- `RevOps/OneDriveJobs/onedrive_sync.py` and `provider_assignment_sync.py` — the actual current OneDrive framework code; read these, not just this summary, before extending them
- `RevOps/SeoSync/` — the staged tolerant-load reference implementation
- `RevOps/FilloutSync/` — the EAV landing reference implementation
