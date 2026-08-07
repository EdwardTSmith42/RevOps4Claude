---
name: ssrs
description: "Use this skill when working with Healthcare Finance Direct's SQL Server Reporting Services (SSRS) at hfdsqlreport.office.local. Trigger when: searching for reports that reference a specific table/function/column, downloading or modifying RDL files, editing report datasets or query logic, adding/removing tablix columns and fields, migrating reports off deprecated database objects, or bulk-updating multiple reports via API. Also trigger when the user mentions SSRS, Report Server, RDL, report catalog, Report Manager, 'which report uses X', or asks to update reports that call a function that's being dropped. Even if the user just says 'find the reports that use fFoo()' or 'update the Hybrid Summary report', use this skill."
---

# HFD SSRS Skill

Guide for finding, modifying, and bulk-updating SSRS reports on `hfdsqlreport.office.local` via the REST API and direct catalog queries.

## Environment

- **Report Server:** `hfdsqlreport.office.local` (fqdn) / `hfdsqlreport` (short)
- **REST API base:** `http://hfdsqlreport/reports/api/v2.0/`
- **Report Manager URL base:** `http://hfdsqlreport/reports/browse/<path>`
- **Direct render URL:** `http://hfdsqlreport/ReportServer/Pages/ReportViewer.aspx?<url-encoded-path>`
- **Catalog database:** `ReportServer.dbo.Catalog` (varbinary `Content` column holds RDL XML as UTF-8 with BOM)
- **Auth:** Windows integrated (NTLM/Kerberos)

## When to Use Each Tool

| Task | Tool |
|------|------|
| Find reports that reference a function/table/column | SQL query on `ReportServer.dbo.Catalog` |
| Inspect a single report's RDL | REST API `GET /CatalogItems({id})/Content/$value` |
| Modify and upload a report | REST API `PUT /CatalogItems({id})` with full metadata + base64 Content |
| Bulk migrate multiple reports | Python script using `requests` + `requests-negotiate-sspi` + `lxml` |

## Finding Reports by Content

**Never search `CAST(Content AS NVARCHAR(MAX))`** - the XML-cast-to-nvarchar path fails silently for large documents or encoding edge cases. Always use `CHARINDEX` on the raw varbinary:

```sql
SELECT c.Name, c.Path, c.Type
FROM ReportServer.dbo.Catalog c WITH (NOLOCK)
WHERE c.Type IN (2, 8)  -- 2 = Report, 8 = Shared Dataset
  AND c.Content IS NOT NULL
  AND CHARINDEX(CAST('fSAOHybridHurdleSSRS' AS VARBINARY(100)), c.Content) > 0
ORDER BY c.Path
```

Narrow by folder path (`WHERE c.Path LIKE '/HFD/03 - Funding/%'`) for faster searches on 1000+ report catalogs. Searching all reports with complex casts can time out silently.

See `references/report-search.md` for Catalog table structure, Type codes, and folder layout.

## REST API Usage

### Authentication

```python
import requests
from requests_negotiate_sspi import HttpNegotiateAuth
auth = HttpNegotiateAuth()
```

`requests-negotiate-sspi` handles Windows integrated auth. Install with `pip install requests-negotiate-sspi`.

### Download an RDL

```python
r = requests.get(
    f'http://hfdsqlreport/reports/api/v2.0/CatalogItems({item_id})/Content/$value',
    auth=auth, timeout=60
)
rdl_bytes = r.content  # varbinary with UTF-8 BOM
```

### Upload a modified RDL

**This is the tricky one.** The REST API v2.0 does NOT accept:
- `PUT /CatalogItems({id})/Content/$value` with raw bytes (returns 500)
- `PATCH /CatalogItems({id})` with just `{Content: base64}` (returns 204 but silently no-ops - the content is NOT updated)

The **only reliable pattern** is: GET the full metadata, merge Content as base64, PUT the whole thing back:

```python
import base64

# 1. Fetch current metadata
r = requests.get(f'{base}/CatalogItems({item_id})', auth=auth, timeout=15)
r.raise_for_status()
body = r.json()
body.pop('@odata.context', None)  # must not be present in PUT body

# 2. Merge new content as base64
body['Content'] = base64.b64encode(new_rdl_bytes).decode('ascii')

# 3. PUT the full object
r = requests.put(f'{base}/CatalogItems({item_id})', auth=auth, json=body, timeout=60)
r.raise_for_status()  # 204 No Content on success
```

**If you get HTTP 500 on upload**, the response body usually contains a specific error code and message - read `r.text` to see it. Common causes covered in `references/rest-api-patterns.md`.

## Modifying RDL XML

RDL files are XML with SSRS-specific schemas. Use `lxml` for reliable manipulation - `xml.etree.ElementTree` works but preserves less formatting.

### Preserving the BOM

```python
def parse_rdl(rdl_bytes):
    bom = b''
    body = rdl_bytes
    if rdl_bytes.startswith(b'\xef\xbb\xbf'):
        bom = b'\xef\xbb\xbf'
        body = rdl_bytes[3:]
    tree = etree.fromstring(body)
    return bom, tree

def serialize_rdl(bom, tree):
    xml_bytes = etree.tostring(tree, xml_declaration=True, encoding='utf-8', standalone=True)
    return bom + xml_bytes
```

### Namespace-aware iteration

RDL has multiple namespaces (`rdl:`, `rd:`). Use `{*}ElementName` in iteration to match regardless of prefix:

```python
for ct in tree.iter('{*}CommandText'):
    ct.text = new_query
```

### Modifying the dataset query

```python
def find_dataset(tree, name='DataSet1'):
    for ds in tree.iter('{*}DataSet'):
        if ds.get('Name') == name:
            return ds
    return None

ds = find_dataset(tree, 'DataSet1')
for ct in ds.iter('{*}CommandText'):
    ct.text = new_query
    break
```

### Removing tablix columns

**This is the most common bug source.** A tablix column has THREE parallel structures that must all be kept in sync:

1. `<TablixColumn>` in `<TablixColumns>` - defines the width
2. `<TablixCell>` in every `<TablixRow>` - the cell at each row position
3. `<TablixMember>` in `<TablixColumnHierarchy><TablixMembers>` - the grouping structure

**Removing just the first two causes HTTP 500 on upload**: *"The tablix 'Tablix1' has an incorrect number of TablixColumns. The number of TablixColumns must equal the number of innermost TablixMembers."*

See `references/rdl-editing.md` for the full removal function and tablix anatomy.

## 2016 RDL Schema Gotchas (cause HTTP 500 on upload)

When building an RDL from scratch with `lxml`, these schema requirements are non-obvious and not enforced until upload. Skipping any of them returns HTTP 500 with a verbose XML-schema validation error from the server. Always handle all four.

1. **`MustUnderstand="df"` requires the `df` namespace declared.** Include `df` and `am` namespaces on the root `<Report>` element:

   ```python
   NSMAP = {
       None: "http://schemas.microsoft.com/sqlserver/reporting/2016/01/reportdefinition",
       "rd": "http://schemas.microsoft.com/SQLServer/reporting/reportdesigner",
       "df": "http://schemas.microsoft.com/sqlserver/reporting/2016/01/reportdefinition/defaultfontfamily",
       "am": "http://schemas.microsoft.com/sqlserver/reporting/authoringmetadata",
   }
   report = etree.Element("{...rdl ns...}Report", nsmap=NSMAP)
   report.set("MustUnderstand", "df")
   ```

2. **`Body` and `Page` must be wrapped in `ReportSections/ReportSection`.** The 2016 schema rejects them as direct children of `<Report>`. The wrapper also owns `<Width>`:

   ```xml
   <Report>
     <DataSources>...</DataSources>
     <DataSets>...</DataSets>
     <ReportParameters>...</ReportParameters>
     <ReportSections>
       <ReportSection>
         <Body>...</Body>
         <Width>10in</Width>
         <Page>...</Page>
       </ReportSection>
     </ReportSections>
   </Report>
   ```

3. **`BorderStyle` is NOT a child of `Style`.** Use `<Border><Style>None</Style></Border>` instead. Tablix and matrix elements with `<BorderStyle>None</BorderStyle>` directly under `<Style>` fail validation.

4. **Child element order matters in `Rectangle`.** `<Style>` must be LAST. Put `<PageBreak>`, `<KeepTogether>`, `<Top>`, etc. before `<Style>`.

If upload returns 500, ALWAYS read `r.text` first. The schema validator's error message points to the exact element and expected children.

## Layout: PageBreaks and Totals

### PageBreak placement

`<PageBreak>` can attach to a `Tablix`, `Matrix`, or `Rectangle` (NOT directly to a `Textbox` - wrap the textbox in a Rectangle if you need to break-before it).

```xml
<Tablix Name="...">
  ...
  <DataSetName>...</DataSetName>
  <PageBreak>
    <BreakLocation>Start</BreakLocation>   <!-- always start on a new page -->
  </PageBreak>
  <Top>...</Top>
  ...
</Tablix>
```

**Avoid compound breaks.** A `PageBreak.End` on one element AND `PageBreak.Start` on the next produces a blank page between them. Pick one.

### Tablix grand-total footer row

Adding a "Grand Total" row at the bottom of a grouped tablix requires three changes that must all match up:

1. Add a static `TablixMember` AFTER the group members in `<TablixRowHierarchy><TablixMembers>`:

   ```xml
   <TablixMember>
     <KeepWithGroup>Before</KeepWithGroup>
   </TablixMember>
   ```

2. Add a third `TablixRow` to `<TablixRows>` with the aggregate expressions (one cell per column, same count as detail row):

   ```xml
   <TablixRow>
     <Height>0.3in</Height>
     <TablixCells>
       <TablixCell><CellContents>...textbox "Grand Total"...</CellContents></TablixCell>
       ...
       <TablixCell><CellContents>...textbox value =Sum(Fields!Amount.Value)...</CellContents></TablixCell>
     </TablixCells>
   </TablixRow>
   ```

3. The cell count must equal the count of `TablixColumn` entries AND the count of innermost `TablixMember` entries in the column hierarchy. Mismatch -> HTTP 500 with `"incorrect number of TablixColumns"`.

### Matrix totals (per-row, per-column, grand)

For a matrix with vintage rows x SPV columns:

- **Column totals (one per SPV at the bottom)**: add a static `TablixMember` at the end of the row hierarchy AFTER the vintage group member.
- **Row totals (one per vintage at the right)**: add a static `TablixMember` at the end of the column hierarchy AFTER the SPV group member.
- **Grand total (bottom-right corner)**: emerges automatically at the intersection.

Cell expression for any total cell: `=Sum(Fields!Amount.Value)`. SSRS scopes it correctly based on which static-vs-group members it sits under.

## Render smoke test (catch issues before users see them)

After upload, render the report to PDF as a smoke test. HTTP 200 with HTML body = SSRS rendered an error page; check the magic bytes:

```python
from urllib.parse import quote
path = "/HFD/EXTERNAL/Standard Reports/Servicing/My Report"
url = ("http://hfdsqlreport/ReportServer?"
       + quote(path, safe="")
       + "&StartDate=2024-01-01&EndDate=2026-04-01&rs:Format=PDF")
r = requests.get(url, auth=auth, timeout=120)
if not r.content.startswith(b"%PDF"):
    # Server returned an HTML error page instead. Save it for inspection.
    err = r.content[:2000].decode("utf-8", errors="replace")
    raise SystemExit(f"Render failed:\n{err}")
```

**Required parameters must be supplied via URL** or you get back the parameter-prompt HTML page instead of a PDF. If a report has a required parameter with no default, pass any sentinel value (e.g., `&ProviderID=-1`) just to exercise the SQL end-to-end.

## Reproducibility: as-of-date filters

If a report's purpose is to reproduce a historical reconciliation (close-of-period, audit trail), do NOT filter on live operational tables like `applications.PaymentStatus` or `applications.status`. Those change daily as accounts move through workflows, so the same `EndDate` parameter returns different numbers when re-run a week later.

Use status-history tables instead. For PaymentStatus in HFD:

```sql
PaymentStatusAsOf AS (
    SELECT x.ApplicationId AS HFDID, x.NewStatus AS PaymentStatusAsOfDate
    FROM (
        SELECT ApplicationId, NewStatus,
               ROW_NUMBER() OVER (PARTITION BY ApplicationId ORDER BY CreatedDate DESC) AS rn
        FROM HFDProd_Finance.dbo.ApplicationPaymentStatusHistory WITH (NOLOCK)
        WHERE CAST(CreatedDate AS DATE) <= @EndDate
    ) x
    WHERE x.rn = 1
)
```

Then `INNER JOIN PaymentStatusAsOf psao ON a.AutoID = psao.HFDID AND psao.PaymentStatusAsOfDate IN ('TPROV','TCOL')` in place of `WHERE a.PaymentStatus IN ('TPROV','TCOL')`.

See `references/hfd-data-conventions.md` for status codes, ledger fee codes, and SAOPurchaseHistory patterns used in reconciliation queries.

## Safety Pattern: Backup First, Dry Run, Then Apply

Every RDL modification script should follow this pattern to enable rollback:

```python
# 1. Download current content
content = download_rdl(item_id, auth)

# 2. Save timestamped backup before any modification
backup_path = BACKUP_DIR / f'{timestamp}-PRE-CHANGE-{item_id}.rdl'
backup_path.write_bytes(content)

# 3. Apply modifications and save the modified version to disk
new_content = modify(content)
(BACKUP_DIR / f'MODIFIED-{item_id}.rdl').write_bytes(new_content)

# 4. Validate the resulting XML parses
etree.fromstring(new_content[3:] if new_content.startswith(b'\xef\xbb\xbf') else new_content)

# 5. Only upload when --apply flag is set
if args.apply:
    upload_rdl(item_id, new_content, auth)
```

Default to dry run. Require an explicit `--apply` flag for uploads. Keep backups indefinitely - they're small and cheap, and rollback requires the original bytes.

**Verify after upload** by re-downloading and confirming the expected text is present (and the old text is gone):

```python
r = requests.get(f'{base}/CatalogItems({item_id})/Content/$value', auth=auth, timeout=30)
assert b'new_function_name' in r.content
assert b'old_function_name' not in r.content
```

## Rolling Back a Change

If a migration causes problems, roll back from the PRE-CHANGE backup:

```python
with open(backup_path, 'rb') as f:
    original = f.read()
r = requests.get(f'{base}/CatalogItems({item_id})', auth=auth, timeout=15)
body = r.json()
body.pop('@odata.context', None)
body['Content'] = base64.b64encode(original).decode('ascii')
r = requests.put(f'{base}/CatalogItems({item_id})', auth=auth, json=body, timeout=60)
```

## Python Dependencies

```bash
pip install requests requests-negotiate-sspi lxml pyodbc
```

`lxml` is preferred over built-in `xml.etree.ElementTree` for RDL work because:
- Namespace-aware iteration with `{*}ElementName` is cleaner
- `etree.fromstring(...).getparent()` works, allowing upward tree navigation
- Output formatting is more predictable for the XML declaration line

### ODBC connection (for validation scripts)

The standard HFD machine has **ODBC Driver 18 for SQL Server** (not Driver 17). Driver 18 defaults to `Encrypt=yes`, so the internal SQL Server requires `TrustServerCertificate=yes`:

```python
CONN = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=hfdsqlfinance.office.local;"
    "Database=HFDProd_Finance;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)
```

Without `TrustServerCertificate=yes`, Driver 18 raises a TLS trust error against the internal cert. Verify the driver is installed: `python -c "import pyodbc; print([d for d in pyodbc.drivers() if 'SQL Server' in d])"`.

## Common Migration Patterns

### Replacing a TVF call with a view reference

If a report calls `SELECT * FROM dbo.fMyFunction()` and you need to point it at a view:

1. If the function was aliased (`fMyFunction() M`), use regex to capture and preserve the alias
2. If the function was bare (`fMyFunction()\n\nwhere ...`), you must inject an alias when wrapping in a subquery - SQL requires aliases on derived tables
3. A helper regex approach:

```python
import re

def replace_fn(text):
    pattern = re.compile(r'dbo\.fMyFunction\s*\(\s*\)(\s+)(\w+)', re.IGNORECASE)
    subq = '(SELECT ... FROM dbo.MyView WITH (NOLOCK))'
    default_alias = ' HP'
    sql_keywords = {'where', 'order', 'group', 'having', 'left', 'right', 'inner', 'outer', 'cross', 'join', 'on', 'union', 'for', 'option', 'with'}

    def sub(m):
        whitespace, next_word = m.group(1), m.group(2)
        if next_word.lower() in sql_keywords:
            # No existing alias, inject default
            return f'{subq}{default_alias}{whitespace}{next_word}'
        else:
            # Preserve existing alias
            return f'{subq}{whitespace}{next_word}'

    return pattern.sub(sub, text)
```

### Removing fields that reports don't display

When cleaning up a report, a `<Field>` in `<Fields>` can be safely removed if:
- It's not referenced in any `Fields!X.Value` expression in the tablix
- It's not in a parameter value expression
- It's not in a visibility/color/tooltip expression

Check with a regex sweep before removing:

```python
refs = set(re.findall(r'Fields!(\w+)\.Value', rdl_text))
safely_removable = declared_fields - refs
```

SSRS does NOT require `<Fields>` to match the query result columns exactly - the query can return more columns than declared, and unreferenced columns are ignored.

## Content Column Gotchas

The `ReportServer.dbo.Catalog.Content` column is varbinary holding UTF-8-encoded XML with a BOM (`EF BB BF 3C 3F 78 6D 6C` = BOM + `<?xml`).

**What works:**
- `CHARINDEX(CAST('text' AS VARBINARY(100)), Content)` - reliable text search
- Python: decode with `content.decode('utf-8')` after stripping the BOM
- `CAST(Content AS XML)` - works for most reports but fails silently on some encoding edge cases

**What does NOT work reliably:**
- `CAST(CAST(Content AS XML) AS NVARCHAR(MAX)) LIKE '%text%'` - times out or returns 0 rows on some reports
- `CAST(Content AS VARCHAR(MAX)) LIKE '%text%'` - same issue
- `CONVERT(NVARCHAR(MAX), Content)` - loses content above byte 8000

Stick with the `CHARINDEX(CAST('...' AS VARBINARY(100)), Content) > 0` pattern for any text search across reports.

## Creating New Reports via REST API

To create a new report, `POST` to `/CatalogItems` with the `@odata.type` annotation. Without it, you get "Cannot create an abstract class."

```python
body = {
    '@odata.type': '#Model.Report',
    'Name': 'My Report',
    'Path': '/Testing/Ed/My Report',
    'ParentFolderId': folder_id,
    'Content': base64.b64encode(rdl_bytes).decode('ascii'),
    'ContentType': '',
    'Description': 'Report description'
}
r = requests.post(f'{base}/CatalogItems', auth=auth, json=body, timeout=60)
# 201 on success
```

### Data Source Binding (required after upload)

The `<DataSourceReference>` element in the RDL does **NOT** automatically bind to the shared data source after upload. Without explicit binding, you get: *"The ConnectionString property has not been initialized."*

After every upload (create or update), bind the data source via PUT:

```python
ds_payload = [{
    'Name': 'Finance',                    # must match the DataSource Name in the RDL
    'Path': '/Data Sources/HFDProd_Finance',
    'Type': 'DataSource',
    'IsEnabled': False,
    'ConnectionString': None,
    'DataSourceType': None,
    'IsOriginalConnectionStringExpressionBased': False,
    'IsConnectionStringOverridden': False,
    'CredentialRetrieval': 'prompt',
    'CredentialsByUser': None,
    'CredentialsInServer': None,
    'IsReference': True
}]
r = requests.put(f'{base}/Reports({report_id})/DataSources', auth=auth, json=ds_payload, timeout=30)
# 200 on success
```

**Key fields:** `IsReference` must be `True` and `Path` must point to the shared data source path. `PATCH` returns 501 on this endpoint; only `PUT` works.

### Available Shared Data Sources

| Name | Path | ID |
|------|------|----|
| HFDProd_Finance | /Data Sources/HFDProd_Finance | 5997a928-e223-4634-b6f8-d74f8b2b8642 |
| HFD Dev | /Data Sources/HFD Dev | b22e1aeb-6847-4641-847a-4b4119f52e10 |
| DBA | /Data Sources/DBA | f5dd6fd2-b96d-40c8-ad6a-97509a5b747d |
| GoldenGate | /Data Sources/GoldenGate | 5d47d1c0-63fe-4f5e-8c26-595b7fa919bb |
| ReportServerDB | /Data Sources/ReportServerDB | efb77ed3-532c-4b41-a272-6a27555c01a5 |

Most HFD reports use `HFDProd_Finance`. The RDL `<DataSource Name="...">` value can be anything (e.g., "Finance", "DataSource1") -- it just needs to match the `Name` field in the binding payload.

### Multi-value Parameter Constraints

SSRS does not allow multi-value parameters to also be nullable. Setting both `<MultiValue>true</MultiValue>` and `<Nullable>true</Nullable>` causes error 1027 on upload. Remove `<Nullable>` from any multi-value parameter.

## HFD Logo

The HFD logo is embedded as a JPEG in the Contracts report at `/HFD/EXTERNAL/Standard Reports/Datasets/Contracts`. The embedded image is named "Untitleddesign" (image/jpeg, ~14KB).

To extract and re-embed in a new report:

```python
# 1. Download the Contracts report RDL
r = requests.get(f'{base}/CatalogItems', auth=auth, timeout=15,
    params={'$filter': "Path eq '/HFD/EXTERNAL/Standard Reports/Datasets/Contracts'"})
ref_id = r.json()['value'][0]['Id']
r2 = requests.get(f'{base}/CatalogItems({ref_id})/Content/$value', auth=auth, timeout=30)
rdl_text = r2.content.decode('utf-8', errors='replace')

# 2. Extract the base64 image data
import re
img_match = re.search(
    r'<EmbeddedImage\s+Name="([^"]+)".*?<MIMEType>([^<]+)</MIMEType>.*?<ImageData>([^<]+)</ImageData>',
    rdl_text, re.DOTALL
)
logo_b64 = img_match.group(3).strip()
```

To embed in a new RDL, add under `<Report>`:

```xml
<EmbeddedImages>
  <EmbeddedImage Name="HFDLogo">
    <MIMEType>image/jpeg</MIMEType>
    <ImageData>...base64...</ImageData>
  </EmbeddedImage>
</EmbeddedImages>
```

And reference in the report body:

```xml
<Image Name="imgLogo">
  <Source>Embedded</Source>
  <Value>HFDLogo</Value>
  <Sizing>FitProportional</Sizing>
  <Top>0.05in</Top>
  <Left>0.1in</Left>
  <Height>0.6in</Height>
  <Width>1.8in</Width>
  <Style />
</Image>
```

## MCP Connector Notes for Report Catalog

The `ReportServer.dbo.Catalog` table lives on `hfdsqlreport.office.local`, not `hfdsqlfinance`. Use the `mcp__SSRSReportServer__execute_sql` connector for catalog queries. The `mcp__mssql__execute_sql` and `mcp__mssql2__execute_sql` connectors connect to `hfdsqlfinance` and cannot reach `ReportServer.dbo.Catalog`.

## Reference Files

- `references/rest-api-patterns.md` - Detailed REST API endpoints, error codes, upload pattern variants
- `references/rdl-editing.md` - Tablix anatomy (columns, rows, cells, hierarchy, members), field cleanup, full removal function with comments
- `references/report-search.md` - ReportServer.dbo.Catalog schema, Type codes, folder layout at HFD, search query patterns
- `references/hfd-data-conventions.md` - HFD-specific data patterns: PaymentStatus codes, FeeCode meanings, AccountingCode filters, SAOPurchaseHistory columns, AmortizationSched term derivation

## Disallowed in Output

Em-dashes, exclamation points, metaphors, analogies, purple prose. See CLAUDE.md for the full disallowed list.
