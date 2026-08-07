# HFD Data Standards — Full Digest

Sourced from the Confluence page "Data Standards Rule Book" (IT space, page id 4334714885). This file captures every rule that affects how analytics deliverables (tables, views, CSVs, spreadsheets, ADO schema proposals) should be shaped.

## 1. Dates and timestamps

- Business dates use `DATE`. Examples called out: `LoanDate`, `EffectiveDate`, `DueDate`, `ChargeOffDate`, `StartDate`, `EndDate`, `ReportingMonth`. CSV format: `YYYY-MM-DD`.
- System and event timestamps use `DATETIME2(3)`, always in UTC. The column name must carry the `Utc` suffix: `CreatedOnUtc`, `UpdatedOnUtc`, `ProcessedOnUtc`, `LoadedOnUtc`, `ArchivedOnUtc`. Default `SYSUTCDATETIME()`. CSV format: `YYYY-MM-DD HH:MM:SS.sss` (millisecond precision). Use `(7)` only for sub-millisecond logging needs.
- `ReportingMonth` must always be the first day of the month (`2025-01-01`, `2025-02-01`). Never store arbitrary dates here.
- `MonthOnBook` is an `INT`. Pick 0-based or 1-based once, then be consistent. It must align with `ReportingMonth`.
- `AsOfDate` (`DATE`) is recommended for snapshot, CECL, model output, and regulatory reporting tables.
- `StartDate` is inclusive. `EndDate` is `NULL` while the row is active. Do not use `EndDate = '9999-12-31'` as a sentinel.
- Anti-patterns: storing local time, missing `Utc` suffix, dates stored as strings, mixing `DATE` and `DATETIME2` semantics in the same column.

## 2. Column naming

- PascalCase for all columns, tables, views, and most objects. Never snake_case or camelCase. Forbidden examples: `create_dt`, `cust_nm`, `program_status_cd`, `EnabledFlag`.
- Use `Id` (not `ID`).
- Tables are plural (`Customers`, `Loans`, `PaymentSchedules`). No `Tbl` / `Table` / `Data` suffixes.
- Booleans prefixed `Is` or `Has` and read as true/false statements: `IsActive`, `IsEnabled`, `IsDeleted`, `HasChildren`.
- Dates indicate meaning in the name: `CreatedOn`, `EffectiveDate`, `ProcessedOnUtc`.
- Classification suffixes when applicable: `Code`, `Type`, `Status`, `Category`.
- Units in column names are not explicitly specified beyond: money fields are named by concept (`PrincipalAmount`, `InterestAmount`) and rates are decimal fractions with no `Pct` suffix in examples.

## 3. Long-format vs wide-format

Not directly prescribed. The closest guidance: every snapshot or fact table declares a grain (e.g. "one row per `LoanId + ReportingMonth`") enforced with a `UNIQUE` constraint. Default grain ceiling for wide analytic snapshots is monthly unless approved otherwise. Carry that posture to file deliverables: prefer long format unless there is a documented reason to pivot.

## 4. Null and missing values

- Use actual `NULL` for unknown / not applicable / not yet available.
- Sentinel values are an anti-pattern. Do not use `-1` for unknown IDs, `'UNKNOWN'` for strings, `1900-01-01` as a fake date, or `EndDate = '9999-12-31'`.
- For CSV: represent nulls as empty cells, never the strings `NULL`, `N/A`, `#N/A`, `-1`.
- Numeric fields default to `NOT NULL DEFAULT 0`. Allow `NULL` only when "unknown is materially different than zero" (forecasts not yet computed, external data not yet received, metrics where absence is meaningful).
- Booleans are never nullable without explicit tri-state justification.
- Soft delete: a `NULL` in `ArchivedOnUtc` / `DeletedOnUtc` indicates the row is active.

## 5. Booleans

- In-warehouse: `BIT NOT NULL` with an explicit default.
- CSV / spreadsheet: `0` / `1` integers. True/false strings and Y/N are not specified as accepted alternatives — `0`/`1` is the safe analog.

## 6. Identifiers

- Surrogate primary key on every table: `Id INT IDENTITY(1,1) NOT NULL`. `BIGINT` only when justified.
- Business / natural keys (external IDs) are `NVARCHAR` strings — `ExternalCustomerNumber NVARCHAR(64)`, `ProgramCode NVARCHAR(32)`, `ExternalId NVARCHAR(128)`. Treat as strings in CSV to preserve leading zeros.
- External identifier pattern: pair `ExternalSystem NVARCHAR(32)` + `ExternalId NVARCHAR(128)` with `UQ_<Table>_External UNIQUE (ExternalSystem, ExternalId)`.
- `UNIQUEIDENTIFIER` (GUID) is allowed but not as the default clustered PK.

## 7. File and table naming

- Tables: PascalCase, plural, no `Tbl` / `Table` / `Data` suffixes.
- Approved prefixes: `Dim` (dimensions), `Fact` (facts), `LK_` (lookups), `VW_` (views), `usp_` (procedures), `IX_` / `UIX_` (indexes), `PK_` / `FK_` / `UQ_` / `CHK_` / `DF_` (constraints).
- Schemas: `dbo` for app-owned, `ro` for read-only / reporting views. Other schemas only with governance approval.
- File naming for CSV exports is not specified in the page. By analogy, apply PascalCase and entity-driven naming, e.g. `FactLoanPerformance_2025-01.csv`.

## 8. Fact and metric table standards

- Surrogate PK is required on every table: `Id INT NOT NULL IDENTITY(1,1)` + `CONSTRAINT PK_<Table> PRIMARY KEY CLUSTERED (Id)`.
- Business / natural key uniqueness is also enforced with `UNIQUE` or `UIX_`. Examples called out: `LoanId + ReportingMonth`, `CustomerId + ProgramId + StartDate`, `ExternalSystem + ExternalKey`.
- Required audit column set (every table, including derived and lookup):

```sql
CreatedOnUtc    DATETIME2(3)    NOT NULL DEFAULT SYSUTCDATETIME(),
UpdatedOnUtc    DATETIME2(3)    NOT NULL DEFAULT SYSUTCDATETIME(),
CreatedBy       NVARCHAR(128)   NOT NULL DEFAULT SYSTEM_USER,
UpdatedBy       NVARCHAR(128)   NULL,
ArchivedOnUtc   DATETIME2(3)    NULL
```

  `CreatedOnUtc` and `CreatedBy` are always required. `ArchivedOnUtc IS NULL` means the row is active.

- Money: `DECIMAL(19,4)` — never `FLOAT`, `REAL`, `MONEY`, or `SMALLMONEY`.
- Rates and percentages: `DECIMAL(19,8)` as decimal fractions (`0.125`, not `12.5`).
- Strings: `NVARCHAR(n)` (Unicode), tiered sizes: 2/4/6/8 (short codes), 16/32 (status/enum), 64/128 (names), 256/512 (descriptions), 1024, `MAX` only when required.
- Grain must be explicit and defensible before a fact or snapshot table is approved (documented one-row-per-X statement, growth forecast required for sub-monthly grains).

## 9. Other rules that affect file structure

- Status values are uppercase strings enforced with a `CHECK` constraint when the domain is fewer than 30 stable values. Examples called out: `Severity IN ('CRITICAL','HIGH','MEDIUM','LOW')`, `Status IN ('ACTIVE','INACTIVE','PENDING','ARCHIVED')`. Use the string, not a surrogate `StatusId`.
- One concept per field name globally: `Status`, `PrincipalAmount`, `ReportingMonth` must mean the same thing in every file.
- No physical deletes. Rows are soft-deleted via `ArchivedOnUtc` / `DeletedOnUtc`.
- Canonical vs. derived: per-provider / per-month files are derived outputs and must trace to a canonical source, preserve grain, and not redefine business meaning.
- Data quality: critical datasets (financial / CECL / executive / investor reporting) require documented grain, uniqueness validation, null checks, reconciliation checks, and registered tests in the `TestRegistry`.

## 10. Verbatim format strings (paste-ready)

| Concept | Exact form |
|---|---|
| Business date | `DATE` → `YYYY-MM-DD` |
| System timestamp | `DATETIME2(3)` UTC, column suffix `Utc` |
| Money | `DECIMAL(19,4)` |
| Rate / percent | `DECIMAL(19,8)` decimal fraction |
| Boolean | `BIT` → `0` / `1`, NOT NULL with default |
| String | `NVARCHAR(n)` tiered sizes |
| Reporting period | `ReportingMonth DATE` = first day of month |
| Cohort age | `MonthOnBook INT` (consistent 0- or 1-based) |
| Audit columns | `CreatedOnUtc`, `UpdatedOnUtc`, `CreatedBy`, `UpdatedBy`, `ArchivedOnUtc` |
| Soft delete | `ArchivedOnUtc DATETIME2(3) NULL` |
| Fact grain example | one row per `LoanId + ReportingMonth` |

## Source

- Confluence: https://healthcarefinancedirect.atlassian.net/wiki/spaces/IT/pages/4334714885/Data+Standards+Rule+Book
- Last reviewed: 2026-05-26
