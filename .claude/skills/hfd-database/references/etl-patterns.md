# ETL Patterns Reference

## MERGE Procedure Template

All ETL stored procedures in the `dw` schema follow this structure:

```sql
ALTER PROCEDURE dw.MergeTableName
AS
BEGIN
    SET NOCOUNT ON;

    MERGE dw.TargetTable AS tgt
    USING (
        SELECT
            /* business key */
            T.UniqueKey,
            /* dimension columns */
            T.Column1,
            T.Column2,
            /* computed columns via CROSS APPLY if needed */
            AG.ClassificationColumn,
            /* row hash for change detection */
            BINARY_CHECKSUM(
                T.Column1, T.Column2, AG.ClassificationColumn
            ) AS RowHash
        FROM HFDProd_Finance.dbo.SourceTable T WITH (NOLOCK)
        LEFT JOIN HFDProd_Finance.dbo.OtherTable O WITH (NOLOCK)
            ON T.Id = O.ForeignId
        /* optional: CROSS APPLY for intermediate computations */
        CROSS APPLY (
            VALUES (
                CASE WHEN ... THEN ... END
            )
        ) AG(ClassificationColumn)
        WHERE T.Name IS NOT NULL
    ) AS src (UniqueKey, Column1, Column2, ClassificationColumn, RowHash)
    ON (tgt.UniqueKey = src.UniqueKey)

    WHEN MATCHED
    AND isnull(tgt.RowHash, '') <> isnull(src.RowHash, -1)
    THEN
        UPDATE SET
            Column1 = src.Column1,
            Column2 = src.Column2,
            ClassificationColumn = src.ClassificationColumn,
            RowHash = src.RowHash

    WHEN NOT MATCHED THEN
        INSERT (UniqueKey, Column1, Column2, ClassificationColumn, RowHash)
        VALUES (src.UniqueKey, src.Column1, src.Column2, src.ClassificationColumn, src.RowHash);
END
```

## Key Points

1. **BINARY_CHECKSUM** includes all columns that should trigger an update when they change
2. **Row hash comparison** uses `isnull(tgt.RowHash, '') <> isnull(src.RowHash, -1)` to handle NULLs
3. **WITH (NOLOCK)** on every source table reference
4. **WHERE clause** filters out NULL names or test records as appropriate
5. New columns added to existing procs must be added in all four places: SELECT, src alias list, UPDATE SET, INSERT/VALUES

## CROSS APPLY (VALUES (...)) Pattern

Use when you need multiple intermediate computed values that feed into several output columns. This avoids duplicating CASE expressions.

```sql
CROSS APPLY (
    VALUES (
        /* Value 1: BaseGroup */
        CASE
            WHEN condition1 THEN 'Group A'
            WHEN condition2 THEN 'Group B'
            ELSE 'Group C'
        END,
        /* Value 2: DetailGroup */
        CASE
            WHEN condition3 THEN 'Detail X'
            WHEN condition4 THEN 'Detail Y'
            ELSE 'Detail Z'
        END
    )
) AG(BaseGroup, DetailGroup)
```

Then reference in the SELECT:
```sql
AG.BaseGroup AS OutputColumn1,
CASE WHEN AG.BaseGroup = 'Group C' THEN AG.DetailGroup ELSE AG.BaseGroup END AS OutputColumn2
```

## Adding Columns to Existing MERGE Procedures

When adding new columns to an existing MERGE proc, update all of these locations:

1. **SELECT list** in the source query (add the new column computation)
2. **BINARY_CHECKSUM** (include the new column so changes trigger updates)
3. **src alias column list** (add the column name)
4. **UPDATE SET** (map src.NewColumn to tgt.NewColumn)
5. **INSERT column list and VALUES** (include the new column)

Missing any of these five locations will cause silent data issues or SQL errors.

## DDL Script for New Columns

Always pair a DDL script (sequence number before the proc script) with idempotency guards:

```sql
IF COL_LENGTH('dw.TargetTable', 'NewColumn') IS NULL
    ALTER TABLE dw.TargetTable ADD NewColumn VARCHAR(50) NULL;
```

Use the `Table/` directory. Name it with a lower sequence number than the proc script so it runs first:
- `20260312-1-DimProvider-21578.sql` (DDL, runs first)
- `20260312-2-MergeProviderData-21578.sql` (proc, runs second)

## Standalone Test SQL

When developing new CASE logic for a MERGE proc, create a standalone SELECT query first for validation:
- Extract the FROM, JOINs, CROSS APPLY, and WHERE from the proc
- SELECT only the relevant columns (business key + new computed columns)
- Add ORDER BY for easy manual review
- Save to a temp directory (e.g., `C:\Users\esmith\temp\test-*.sql`), not the repo

This lets you iterate on the logic in SSMS before integrating into the proc.
