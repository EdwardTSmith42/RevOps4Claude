# ReportServer Catalog Search

## Table Schema

`ReportServer.dbo.Catalog` is the main table that holds all SSRS items (reports, datasets, folders, data sources). Key columns:

| Column | Type | Description |
|--------|------|-------------|
| `ItemID` | uniqueidentifier | Primary key (used as the `{id}` in REST API URLs) |
| `Name` | nvarchar | Item name (what shows in Report Manager) |
| `Path` | nvarchar | Full folder path + item name (e.g. `/HFD/EXTERNAL/Hybrid Summary Report`) |
| `ParentID` | uniqueidentifier | FK to parent folder's ItemID |
| `Type` | int | Item type code (see below) |
| `Content` | varbinary(max) | The actual RDL/DSD file as UTF-8 XML with BOM |
| `CreationDate` | datetime | When originally created |
| `ModifiedDate` | datetime | Last modification |
| `ModifiedByID` | uniqueidentifier | Who last modified |

## Type Codes

| Code | Type | Notes |
|------|------|-------|
| 1 | Folder | No Content |
| 2 | Report | Main target for migrations |
| 3 | Resource | Images etc. |
| 4 | Linked Report | Rarely used at HFD |
| 5 | Data Source | Shared data source (.rds) |
| 6 | Model | Report Model (deprecated) |
| 7 | Report Part | Reusable component |
| 8 | Shared Dataset | .rsd files - may also contain query text to search |
| 9 | Report Server Project | |
| 11 | Kpi | |
| 12 | Mobile Report | |
| 14 | Power BI Report | |

For content searches targeting database object references, stick with `Type IN (2, 8)` - Reports and Shared Datasets are the only items that embed SQL.

## HFD Folder Layout

Top-level folders on `hfdsqlreport`:

```
/                                          (root)
├── /AT                                    Align Tech stuff
├── /Data Sources                          shared data sources
├── /HFD                                   main business reports
│   ├── /HFD/01 - Originations
│   │   ├── /00 - Datasets                 shared datasets
│   │   ├── /01 - OBS Reports
│   │   ├── /03 - Channel Partners
│   │   ├── /04 - Audit
│   │   └── /V3 Applications
│   ├── /HFD/02 - Servicing
│   ├── /HFD/03 - Funding
│   │   ├── /01 - SAO
│   │   ├── /02 - Balance Sheet
│   │   └── /03 - Hybrid                   (folder only, reports moved to /EXTERNAL/)
│   ├── /HFD/Corp Accounting
│   ├── /HFD/Department Reports
│   │   └── /00 Executive Management
│   ├── /HFD/EXTERNAL
│   │   ├── /Standard Reports
│   │   │   ├── /Capital Partners          e.g. SPV G Portfolio Report
│   │   │   └── /Funding
│   │   │       └── /Hybrid                main hybrid reports + /Archive
│   │   └── /Partner-specific folders
│   └── /HFD/Finance                       Finance team reports
│       └── /Provider Subscription Reports
├── /Report Parts                          reusable components
└── /Testing                               per-user test sandboxes
    ├── /Frederic
    ├── /Lakshmi
    ├── /Angelia
    └── ...
```

When searching for reports that depend on a specific DB object, scope by folder path to avoid full-catalog scans:

```sql
WHERE c.Type IN (2, 8)
  AND (c.Path LIKE '/HFD/EXTERNAL/%' OR c.Path LIKE '/HFD/Finance/%')
  AND CHARINDEX(CAST('fSAOHybridHurdleSSRS' AS VARBINARY(100)), c.Content) > 0
```

## Content Search Patterns

### Safe content search (recommended)

`CHARINDEX` on varbinary is fast and reliable:

```sql
SELECT c.ItemID, c.Name, c.Path
FROM ReportServer.dbo.Catalog c WITH (NOLOCK)
WHERE c.Type IN (2, 8)
  AND c.Content IS NOT NULL
  AND CHARINDEX(CAST('fSAOHybridHurdleSSRS' AS VARBINARY(100)), c.Content) > 0
ORDER BY c.Path
```

Performance tip: narrow by name first where possible:

```sql
WHERE c.Type IN (2, 8)
  AND c.Name LIKE '%Hybrid%'   -- fast prefilter on nvarchar
  AND CHARINDEX(CAST('fSAOHybridHurdleSSRS' AS VARBINARY(100)), c.Content) > 0
```

### Avoid these patterns

```sql
-- BAD: silently times out or returns 0 rows on large catalogs
CAST(CAST(c.Content AS XML) AS NVARCHAR(MAX)) LIKE '%text%'

-- BAD: truncates after ~8000 chars
CONVERT(VARCHAR(MAX), c.Content) LIKE '%text%'

-- BAD: slow, doesn't handle UTF-8 BOM correctly
CAST(c.Content AS NVARCHAR(MAX)) LIKE '%text%'
```

### Distinguishing between function variants

To check whether a report references `fFoo()` vs `fFoo_Detail()` vs `fFoo_HurdleDate()`:

```sql
SELECT c.Name, c.Path,
       CHARINDEX(CAST('fFoo_HurdleDate' AS VARBINARY(50)), c.Content) AS hd_pos,
       CHARINDEX(CAST('fFoo_Detail' AS VARBINARY(50)), c.Content) AS detail_pos,
       CHARINDEX(CAST('fFoo' AS VARBINARY(50)), c.Content) AS main_pos
FROM ReportServer.dbo.Catalog c WITH (NOLOCK)
WHERE c.Type IN (2, 8)
  AND c.Content IS NOT NULL
  AND CHARINDEX(CAST('fFoo' AS VARBINARY(50)), c.Content) > 0
```

If `main_pos > 0` but `hd_pos = 0` and `detail_pos = 0`, the report calls the main function only.

## Getting Context Around a Match

To inspect the SQL around a found reference:

```sql
DECLARE @item_id UNIQUEIDENTIFIER = '43310C4E-F219-425A-AB0B-62B78CB5C18D'
DECLARE @pos INT

SELECT @pos = CHARINDEX(CAST('fSAOHybridHurdleSSRS' AS VARBINARY(100)), Content)
FROM ReportServer.dbo.Catalog WITH (NOLOCK) WHERE ItemID = @item_id

SELECT CAST(SUBSTRING(Content, @pos - 200, 600) AS VARCHAR(800)) AS context
FROM ReportServer.dbo.Catalog WITH (NOLOCK) WHERE ItemID = @item_id
```

Note: SUBSTRING on varbinary works with byte offsets. The result cast to VARCHAR is safe for ASCII content but may lose non-ASCII characters.

## Finding All References in a Single Pass

For a comprehensive audit before dropping a database object, run one query per variant:

```sql
-- All reports/datasets that reference any variant of the target function
SELECT 'fSAOHybridHurdleSSRS' AS needle, c.Name, c.Path, c.Type
FROM ReportServer.dbo.Catalog c WITH (NOLOCK)
WHERE c.Type IN (2, 8) AND c.Content IS NOT NULL
  AND CHARINDEX(CAST('fSAOHybridHurdleSSRS' AS VARBINARY(100)), c.Content) > 0

UNION ALL

SELECT 'SAOHybridBaseData', c.Name, c.Path, c.Type
FROM ReportServer.dbo.Catalog c WITH (NOLOCK)
WHERE c.Type IN (2, 8) AND c.Content IS NOT NULL
  AND CHARINDEX(CAST('SAOHybridBaseData' AS VARBINARY(100)), c.Content) > 0

ORDER BY Path, needle
```

## Finding Reports Modified Recently

Useful for auditing bulk migrations:

```sql
SELECT TOP 20 c.Name, c.Path, c.ModifiedDate
FROM ReportServer.dbo.Catalog c WITH (NOLOCK)
WHERE c.Type = 2
  AND c.ModifiedDate >= DATEADD(hour, -1, GETDATE())
ORDER BY c.ModifiedDate DESC
```

## Subscriptions

Report subscriptions (scheduled emails, file shares) live in `ReportServer.dbo.Subscriptions` linked by `Report_OID` to Catalog. Before dropping or drastically changing a report, check for active subscriptions:

```sql
SELECT c.Name, c.Path, s.Description, s.LastRunTime, s.LastStatus
FROM ReportServer.dbo.Subscriptions s WITH (NOLOCK)
JOIN ReportServer.dbo.Catalog c WITH (NOLOCK) ON s.Report_OID = c.ItemID
WHERE c.Path LIKE '/HFD/EXTERNAL/%'
ORDER BY s.LastRunTime DESC
```

## Quick Report URL Construction

Given a `Name` and `Path`, you can construct clickable URLs for the user:

```python
import urllib.parse

def browse_url(path):
    # Report Manager view
    return f'http://hfdsqlreport/reports/browse{path}'

def render_url(path):
    # Direct render (auto-runs the report)
    encoded = urllib.parse.quote(path, safe='')
    return f'http://hfdsqlreport/ReportServer/Pages/ReportViewer.aspx?{encoded}'
```

The `browse` URL opens the parameters entry page in Report Manager. The `ReportViewer.aspx` URL runs the report immediately with default parameters.
