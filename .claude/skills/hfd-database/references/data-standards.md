# HFD Data Standards Rule Book

Mandatory standards for all HFD database objects. Source: https://healthcarefinancedirect.atlassian.net/wiki/spaces/IT/pages/4334714885/Data+Standards+Rule+Book

All new code and all modified code must comply. This document is a summary; when in doubt, read the full rule book.

## Table of Contents

1. Naming Conventions
2. Data Types
3. Nullability & Defaults
4. Date/Time Handling
5. Constraints & Integrity
6. Indexes
7. Programmability
8. Structural Rules
9. Style & Formatting
10. Canonical Data & Business Keys
11. Data Quality & Validation

---

## 1. Naming Conventions

**General:** PascalCase for all object names. Use `Id` not `ID`. Avoid abbreviations unless widely understood. Prefer plural table names.

**Tables:**
- Plural preferred: `Customers`, `Loans`, `PaymentSchedules`
- Approved prefixes only: `Dim` (dimension), `Fact` (fact), `LK_` (lookup)
- AVOID: `tblCustomer`, `CustomerTable`, `lk_program_status`

**Columns:**
- Primary key: `Id`
- Foreign keys: `<ReferencedEntity>Id` (e.g., `CustomerId`, `LoanId`)
- Booleans: `Is`/`Has` prefix (`IsActive`, `HasChildren`)
- Dates: meaningful names (`CreatedOn`, `EffectiveDate`, `ProcessedOnUtc`)
- User attribution: `CreatedBy`, `UpdatedBy`

**Views:** `VW_<EntityOrPurpose>` (`VW_Customers`, `VW_LoanPerformance`)
- AVOID: `vwCustomers`, `CustomerView`

**Stored procedures:** `usp_<Entity><Action>` (`usp_CustomerGetById`, `usp_LoanPerformanceProcess`)
- Use clear verbs: Get, List, Insert, Update, Delete, Upsert, Merge, Validate, Process

**Constraints:** Explicitly named with prefixes:
- `PK_<TableName>` for primary key
- `FK_<FromTable>_<ToTable>` for foreign key
- `UQ_<TableName>_<Column>` for unique constraint
- `CHK_<TableName>_<Rule>` for check constraint
- `DF_<TableName>_<Column>` for default constraint
- **System-generated constraint names are not allowed.**

**Indexes:**
- `IX_<TableName>_<Columns>` for standard
- `UIX_<TableName>_<Columns>` for unique index

**Schemas:** Only `dbo` (standard) and `ro` (read-only/reporting). Do not create new schemas casually.

---

## 2. Data Types

**Monetary values:** `DECIMAL(19,4)` - NEVER `FLOAT`, `REAL`, `MONEY`, or `SMALLMONEY`.

**Rates/percentages:** `DECIMAL(19,8)` as decimal fractions (0.125, not 12.5).

**Integers:** `INT` as default. `BIGINT` only when justified. Avoid `SMALLINT`/`TINYINT`.

**Strings:** **ALL** string data uses `NVARCHAR(n)`. **`VARCHAR` IS BANNED.** Standard size tiers:
- Short codes: 2, 4, 6, 8
- Status/enums: 16, 32
- Names: 64, 128
- Descriptions: 256, 512
- Large text: 1024
- Unbounded: MAX (only if truly required)

**Dates/times:**
- `DATE` for business dates (loan lifecycle, payment due, reporting periods)
- `DATETIME2(3)` for timestamps (default precision 3)
- **NEVER `DATETIME`**
- All timestamps in UTC with `Utc` suffix (`CreatedOnUtc`)
- Default to `SYSUTCDATETIME()` not `GETDATE()`

**Booleans:** `BIT NOT NULL DEFAULT 0 or 1`. Avoid nullable booleans unless tri-state is intentional.

**GUIDs:** `UNIQUEIDENTIFIER` allowed but avoid as clustered PKs. Prefer `INT IDENTITY` for core transactional tables.

**Audit columns (required on all transactional tables):**
```sql
CreatedOnUtc   DATETIME2(3)    NOT NULL DEFAULT SYSUTCDATETIME()
UpdatedOnUtc   DATETIME2(3)    NOT NULL DEFAULT SYSUTCDATETIME()
CreatedBy      NVARCHAR(128)   NOT NULL DEFAULT SYSTEM_USER
UpdatedBy      NVARCHAR(128)   NULL
```

---

## 3. Nullability & Defaults

- Nullability reflects business meaning, not developer convenience
- `NOT NULL DEFAULT 0` for counters, amounts, rates, booleans unless NULL is materially different from zero
- `NOT NULL` for required foreign keys; `NULL` for optional relationships
- All `NOT NULL` columns should have an explicit default unless the application must provide the value
- Defaults must be named: `DF_<Table>_<Column>`

**Sentinel values are an anti-pattern.** Don't use `-1`, `'UNKNOWN'`, `1900-01-01` to represent missing data. Use `NULL` instead.

**Soft deletes:** Use timestamps (`DeletedOnUtc DATETIME2(3) NULL` or `ArchivedOnUtc`), NOT booleans like `IsDeleted`. NULL means active.

---

## 4. Date/Time Handling

- Separate business dates from system timestamps
- `DATE` for business logic, `DATETIME2(3)` for system events
- All timestamps UTC, always suffix `Utc`
- `StartDate` inclusive, `EndDate` NULL means still active (not `'9999-12-31'`)
- Query pattern: `WHERE @AsOfDate >= StartDate AND (@AsOfDate < EndDate OR EndDate IS NULL)`

**Reporting month:** Always `DATE`, always first day of month. Never arbitrary dates.

**MonthOnBook (MOB):** `INT NOT NULL`, starts at 0 or 1 (must be consistent per model).

---

## 5. Constraints & Integrity

**Enforcement order:** Database first, middleware second, UI third. The database must be structurally sound - never rely only on application or UI validation.

**Primary keys:** Every table must have an explicit PK. Named `PK_<TableName>`. Usually `Id INT IDENTITY(1,1)`.

**Foreign keys:** Use by default. Soft relationships (unenforced FKs) acceptable only when:
- Referenced data lives in another system
- Ingestion timing requires temporary decoupling
- Polymorphic references can't be cleanly enforced

**CHECK constraints vs lookup tables:**
- CHECK for small stable domains (<30 values, low volatility)
- Lookup table when domain is large, changes, or carries metadata

**Status fields:** Prefer readable string with CHECK constraint over StatusId:
```sql
Status NVARCHAR(32) NOT NULL
    CONSTRAINT CHK_<Table>_Status
    CHECK (Status IN ('ACTIVE', 'INACTIVE', 'PENDING', 'ARCHIVED'))
```

**Unique constraints and grain enforcement:** CRITICAL. Enforce uniqueness wherever duplicate rows would violate business meaning. Match the natural grain, not just the surrogate key.

**Delete policy: Physical deletes are prohibited by default.** Require CTO authorization. Use soft-delete/archival timestamps.

**`ON DELETE CASCADE` is not allowed.** All deletes must be explicit.

---

## 6. Indexes

- Create intentionally based on workload evidence
- **ALL indexes must use data compression** (ROW or PAGE) by default
  - ROW for moderate write workloads / OLTP
  - PAGE for read-heavy, analytics, warehouses, history
  - NONE only when proven necessary
- Primary key usually clustered with PAGE compression:
```sql
CONSTRAINT PK_<Table> PRIMARY KEY CLUSTERED (Id)
    WITH (DATA_COMPRESSION = PAGE)
```
- Use `INCLUDE` columns for covering indexes
- Foreign keys heavily used in joins should be indexed
- Partitioning: recent partitions ROW, historical PAGE

**Anti-patterns:** Over-indexing write-heavy tables, unindexed FKs, wide key columns instead of INCLUDE, speculative indexes, leaving unused indexes, clustering on random GUIDs by default.

---

## 7. Programmability

**User-defined functions (UDFs) should be avoided entirely.** This includes both scalar UDFs and table-valued functions. Use views, inline SQL, CTEs, or application logic instead.

**Triggers are strongly discouraged.** Only in exceptional, explicitly-approved scenarios.

**Views are the preferred abstraction layer.** Tables = internal storage, views = consumption layer. Pattern: `dbo.Loans` (internal) vs `ro.VW_Loans` (external).

**Stored procedures are allowed but not required** as the primary data access layer. `usp_` prefix, entity+action pattern.

**Dynamic SQL** must always be parameterized. Use `sp_executesql`. Never concatenate user input.

**Required SET options in all procedures:**
```sql
SET NOCOUNT ON;
SET XACT_ABORT ON;
```

**MERGE statement:** Caution advised - has known edge cases and bugs in SQL Server. Use explicit INSERT/UPDATE when clarity is preferred. Only use MERGE when fully understood and tested.

---

## 8. Structural Rules

**Every table must have:**
- A clearly defined purpose
- A defensible and documented grain
- A surrogate key `Id INT NOT NULL IDENTITY(1,1)` with named PK constraint
- Natural business uniqueness enforced via UNIQUE constraint or UIX_ index
- Audit columns (CreatedOnUtc, UpdatedOnUtc, CreatedBy, UpdatedBy)

**Grain must be explicit.** Before a table is approved, its grain must be clearly stated. Snapshot tables finer than monthly require explicit approval.

**History tables:** Separate from current-state table. Include surrogate Id, FK to parent, history-effective timestamps, prior-state values, audit columns.

---

## 9. Style & Formatting

**Required:**
- **UPPERCASE SQL keywords** (SELECT, FROM, WHERE, INNER JOIN, etc.)
- **Leading commas** in SELECT lists and DDL
- **Schema-qualified names** always (`dbo.Customers`, not `Customers`)
- **Idempotent scripts** - safe to run more than once. Use existence checks before CREATE/DROP
- **`GO` between object definitions** and logical script batches

**Preferred layout:**
```sql
SELECT c.Id
     , c.Name
     , c.Status
FROM dbo.Customers c WITH (NOLOCK)
WHERE c.Status = 'ACTIVE'
ORDER BY c.Name
```

**DDL:**
- One column per line
- Leading commas after the first line
- Data type and nullability visually aligned
- Constraints clearly named
- Simple DEFAULT/CHECK inline; PK/FK/composite at the bottom

**Comments:**
- `--` for short inline explanations
- `/* ... */` for block headers and multi-line notes
- Explain intent, business meaning, non-obvious decisions
- Don't restate the obvious

**Migration script safety:**
- Check existence before CREATE/DROP
- Explicitly name constraints and indexes
- Avoid destructive patterns without authorization
- Make irreversible operations obvious
- Never rely on system-generated names during alters/drops

---

## 10. Canonical Data & Business Keys

Every business entity needs a **stable business identifier** independent of surrogate keys.

- Surrogate `Id` = internal identity
- Business key = real-world identity for integration
- Both must exist
- Business keys enforced with UNIQUE/UIX_

**Canonical tables** (sources of truth) require formal approval: grain defined, fields agreed, ownership assigned, governance approved.

**Derived tables must trace back to canonical sources.** No "shadow truth" tables that compete with the official definition.

**Field names represent one concept globally.** `Status`, `PrincipalAmount`, `ReportingMonth` must mean the same thing everywhere they appear.

---

## 11. Data Quality & Validation

"Data is not considered usable until it is validated, measurable, and explainable."

**Quality layers:**
1. Structural integrity (PK/FK/constraints)
2. Validation rules (domain, cross-field, distribution)
3. Reconciliation (source vs destination)
4. Monitoring (failures, anomalies, trends)

**Test registry:** All validations should be registered in a central `TestRegistry` with severity levels (CRITICAL, HIGH, MEDIUM, LOW).

**Assertion SQL standard:** Tests should return zero rows when passing, failing records when failing.

**Critical datasets** (financial reporting, CECL, executive/investor reporting) must have: defined grain, uniqueness validation, null checks, reconciliation checks, documented test coverage.

**Failures** must be logged, visible, traceable. Critical failures block downstream and trigger alerts.

---

## Disallowed (Quick Reference)

| Item | Use Instead |
|------|-------------|
| `VARCHAR` | `NVARCHAR` |
| `DATETIME` | `DATETIME2(3)` |
| `FLOAT`, `REAL`, `MONEY`, `SMALLMONEY` for money | `DECIMAL(19,4)` |
| Scalar UDFs | Views, inline SQL, CTEs |
| Table-valued functions | Views |
| Triggers (unapproved) | Application logic, procedures |
| `ON DELETE CASCADE` | Explicit archival/soft delete |
| Physical DELETE (unapproved) | `ArchivedOnUtc DATETIME2(3) NULL` |
| System-generated constraint names | Named: `PK_`, `FK_`, `UQ_`, `CHK_`, `DF_` |
| Sentinel values (`-1`, `'UNKNOWN'`, `1900-01-01`) | `NULL` |
| `IsDeleted` boolean | `DeletedOnUtc DATETIME2(3) NULL` |
| Lowercase SQL keywords | UPPERCASE |
| Trailing commas | Leading commas |
| System-generated temp names in migrations | Explicit names |
| `GETDATE()` for audit | `SYSUTCDATETIME()` |
