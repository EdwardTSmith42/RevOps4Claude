---
name: hfd-data-standards
description: HFD Data Standards Rule Book — naming, types, audit columns, null handling, and grain conventions for any analytics file, table, view, or CSV that will land in or feed the HFD warehouse. Use whenever producing a deliverable that is intended to be loaded, queried, joined, reported on, or handed to Data Engineering. Trigger on any task involving SQL Server DDL, fact/dim tables, CSV/xlsx exports for warehousing, schema proposals in ADO tickets, ETL pipeline design, or analytics-ready data shape decisions.
---

# HFD Data Standards Rule Book

Source: Confluence — Data Standards Rule Book (IT space, page id 4334714885). Apply these rules to every analytics deliverable that touches the warehouse or its inputs.

## How to use this skill

1. Read `reference.md` for the full rule digest with exact format strings.
2. Before producing column names, data types, file names, or null encodings in any deliverable, verify each one against the digest.
3. When in doubt, default to: PascalCase, plural tables, `Utc` suffix for UTC timestamps, `DATE` (YYYY-MM-DD) for business dates, empty cells for nulls, `0/1` for booleans, `NVARCHAR` strings for IDs, `DECIMAL(19,4)` for money, `DECIMAL(19,8)` decimal fractions for rates, surrogate `Id INT IDENTITY(1,1)` PK plus a UNIQUE on the natural grain.
4. For per-period snapshots / facts: declare grain up front (one row per X), enforce with UNIQUE, pin `ReportingMonth` to first of month, and include the audit column set.

## Cheat-sheet at a glance

| Concept | Rule |
|---|---|
| Column case | PascalCase, never snake_case or camelCase |
| Table names | PascalCase, plural, no Tbl/Table/Data suffix |
| Object prefixes | `Dim` / `Fact` / `LK_` / `VW_` / `usp_` / `IX_` / `UIX_` / `PK_` / `FK_` / `UQ_` / `CHK_` / `DF_` |
| Schemas | `dbo` app-owned, `ro` reporting/read-only |
| Booleans | `BIT NOT NULL` default, `Is`/`Has` prefix, never nullable without tri-state justification. CSV: `0`/`1` |
| Business dates | `DATE` → `YYYY-MM-DD` |
| Timestamps | `DATETIME2(3)` UTC, column suffix `Utc`, default `SYSUTCDATETIME()` |
| Reporting month | `ReportingMonth DATE` pinned to first of month (`2026-04-01`) |
| Cohort age | `MonthOnBook INT` (consistent 0- or 1-based) |
| Money | `DECIMAL(19,4)` — never FLOAT/REAL/MONEY |
| Rates / percentages | `DECIMAL(19,8)` decimal fraction (`0.125`, not `12.5`) |
| Strings | `NVARCHAR(n)` tiered: 2/4/6/8 codes, 16/32 status, 64/128 names, 256/512 desc, 1024, MAX only when needed |
| Surrogate PK | `Id INT IDENTITY(1,1) NOT NULL` + `PK_<Table>` clustered |
| Natural key | enforced with `UQ_` / `UIX_` |
| External IDs | `ExternalSystem NVARCHAR(32) + ExternalId NVARCHAR(128)` with `UQ_<Table>_External` |
| Status enums | UPPERCASE strings with CHECK constraint when domain <30 stable values |
| Nulls | actual NULL or empty cell — never `-1`, `'UNKNOWN'`, `1900-01-01`, `9999-12-31` |
| Soft delete | `ArchivedOnUtc DATETIME2(3) NULL`; NULL = active |
| Audit columns | `CreatedOnUtc`, `UpdatedOnUtc`, `CreatedBy`, `UpdatedBy`, `ArchivedOnUtc` on every table |

## Required audit column set

```sql
CreatedOnUtc    DATETIME2(3)    NOT NULL DEFAULT SYSUTCDATETIME(),
UpdatedOnUtc    DATETIME2(3)    NOT NULL DEFAULT SYSUTCDATETIME(),
CreatedBy       NVARCHAR(128)   NOT NULL DEFAULT SYSTEM_USER,
UpdatedBy       NVARCHAR(128)   NULL,
ArchivedOnUtc   DATETIME2(3)    NULL
```

## When producing a CSV / xlsx for the warehouse

- One sheet = one entity; do not pivot metrics into columns. Long format unless you have a documented reason.
- Header row uses PascalCase column names that match the target table.
- `ReportingMonth` written as `YYYY-MM-DD`, first of month.
- UTC timestamps in column with `Utc` suffix, written as `YYYY-MM-DD HH:MM:SS.sss`.
- Nulls represented as empty cells, never `NULL`/`#N/A`/`-`/`UNKNOWN`/sentinel dates.
- Booleans as `0`/`1`.
- Money preserved as decimal with 4 places (`12345.6700`); rates as decimal fractions with up to 8 places (`0.12500000`).
- Always include `SourceFile` (or equivalent provenance column) and `LoadedOnUtc` audit columns for traceability.

## Hard anti-patterns (will fail review)

- snake_case or camelCase column names
- columns ending in `Date` that hold timestamps with time-of-day, or columns ending in `Utc` that aren't actually UTC
- storing percentages as `12.5` instead of `0.125`
- `FLOAT`, `REAL`, `MONEY`, `SMALLMONEY` for currency
- sentinel values: `-1`, `'UNKNOWN'`, `'1900-01-01'`, `'9999-12-31'`
- physical deletes — soft delete via `ArchivedOnUtc`
- nullable boolean without explicit tri-state justification
- facts without a declared grain and a UNIQUE constraint enforcing it
- pluralizing dimension tables in singular (`Customer` should be `Customers`) or vice versa
- numbering a multi-object DBUp PR's scripts **per folder** — the deploy orders every `.sql` by a global, folder-agnostic numeric key (`date*10000 + N`), so the `N` in each filename must be a single unique sequence, ascending in dependency order (tables → procs → views) across all folders; per-folder `-1-`/`-1-`/`-1-` collides and can run a view before its table (broke a build 2026-07-09)

## See also

- `reference.md` — full digest, including verbatim format strings and the original rule wording
- `hfd-database` skill → "File Naming Convention & Execution Order" — how DBUp actually orders/deploys migration scripts (numbering across folders, non-atomic deploy, journal)
