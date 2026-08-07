---
name: tableau-twb
description: "Use this skill when programmatically creating or modifying Tableau workbooks (TWB/TWBX). Trigger when: generating Tableau dashboards from data, converting SSRS reports to Tableau, modifying existing TWB files to add labels/formatting/zones, building Custom SQL data sources, or publishing workbooks to Tableau Cloud. Also trigger when the user mentions TWB, TWBX, Tableau workbook, Tableau dashboard, or asks to create/modify a Tableau report."
---

# Tableau TWB Programmatic Generation Skill

Guide for programmatically creating and modifying Tableau workbooks (TWB/TWBX files) using Python.

## Critical Rule: TWB Modification Strategy

**NEVER use ElementTree (or any XML parser) to modify a Tableau Desktop-saved TWB.** XML parsers corrupt the file during re-serialization (attribute reordering, namespace handling, encoding changes) causing the generic `2805CF18` internal error.

**Two-phase approach:**
1. **Phase 1 (ElementTree OK):** Generate worksheets, data sources, columns, calculated fields from a template. No dashboard.
2. **Phase 2 (Raw string only):** All modifications to Tableau Desktop-saved files must use raw string manipulation (find/replace, regex, string insertion). This includes adding dashboard zones, labels, formatting, and any post-Desktop changes.

## Critical Rule: Self-Test Before Delivery

**MANDATORY: before sending, publishing, or handing off ANY generated or modified .twb/.twbx, run the `twb-selftest` skill: static lint, then the Tableau Desktop open smoke test with `-ExpectText`.** Static validation alone shipped a D2E8DA72 file and then a 2805CF18 file on the same day (2026-06-10); Desktop is the only authoritative validator (no public XSD exists). The smoke test needs no credentials -- load errors fire before sign-in.

## Environment

- **Tableau Cloud site:** healthcarefinancedirect
- **Tableau Cloud URL:** `https://10az.online.tableau.com`
- **Bridge:** Active, with virtual connections to `hfdsqlfinance.office.local`
- **Tableau Desktop:** Installed locally, version 2026.1.0
- **Template TWB:** `C:\Users\esmith\PycharmProjects\DB-Analytics\HFD Datawarehouse.twb` (version 18.1, source-build 2021.2.7)
- **HFD Logo:** `C:\Users\esmith\temp\hfd_logo.jpg` (extracted from SSRS Contracts report)
- **Reference dashboards:** `C:\Users\esmith\temp\TableauExamples\` (KYC, Bing Bong, CRO, Portfolio, Sales Territory)

## TWB/TWBX File Structure

- **TWB:** Plain XML describing data sources, worksheets, dashboards, windows
- **TWBX:** ZIP archive containing: `*.twb` (workbook XML), `Data/Extracts/*.hyper` (extracts), `Image/*.png|jpg` (images)
- **Version:** `version='18.1'` for Tableau 2021.2+. The `source-build` attribute updates when Desktop saves.

### Root Element Order (strict sequence)

```
document-format-change-manifest
preferences
style (animation)
datasources
shared-views (optional)
worksheets
dashboards (optional)
windows
thumbnails
```

Dashboards MUST come after worksheets and before windows. Use `root.insert(windows_idx, dashboards)` when adding programmatically.

## Phase 1: Generating Worksheets (ElementTree)

### Template Selection

Use `HFD Datawarehouse.twb` as the base template. It provides:
- Valid `document-format-change-manifest` for version 18.1
- Correct animation style block
- Proper preferences

### Data Source with Custom SQL

```python
DS_NAME = 'federated.spvlookup'
CONN_NAME = 'sqlserver.spvconn1'

main_ds = ET.SubElement(datasources, 'datasource')
main_ds.set('caption', 'My Report')
main_ds.set('inline', 'true')
main_ds.set('name', DS_NAME)
main_ds.set('version', '18.1')

conn = ET.SubElement(main_ds, 'connection')
conn.set('class', 'federated')

# Named connection
named_conns = ET.SubElement(conn, 'named-connections')
nc = ET.SubElement(named_conns, 'named-connection')
nc.set('caption', 'hfdsqlfinance.office.local')
nc.set('name', CONN_NAME)
db = ET.SubElement(nc, 'connection')
for k, v in [
    ('IsolationLevel', 'ReadUncommitted'),
    ('authentication', 'sqlserver'),
    ('class', 'sqlserver'),
    ('dbname', 'Finance'),
    ('odbc-native-protocol', 'yes'),
    ('one-time-sql', ''),
    ('server', 'hfdsqlfinance.office.local'),
    ('server-oauth', ''),
    ('username', ''),
    ('workgroup-auth-mode', 'prompt'),
]:
    db.set(k, v)

# Custom SQL relation (BOTH legacy variants required)
for pfx in [
    '_.fcp.ObjectModelEncapsulateLegacy.false...relation',
    '_.fcp.ObjectModelEncapsulateLegacy.true...relation',
]:
    rel = ET.SubElement(conn, pfx)
    rel.set('connection', CONN_NAME)
    rel.set('name', 'Custom SQL Query')
    rel.set('type', 'text')
    rel.text = "SELECT ... FROM ... WITH (NOLOCK)"
```

### Custom SQL Parameter Limitation

**Tableau parameters CANNOT be injected into Custom SQL via `<Parameters.X>` syntax when generating TWBs programmatically.** This pattern exists in Tableau's documentation but requires internal bookkeeping that only Tableau Desktop creates.

**Alternative:** Use Tableau-native filters instead. The Custom SQL handles joins/transforms; Tableau filters handle user interaction. Tableau pushes filter predicates down to SQL automatically.

### Custom SQL Cannot Use a Top-Level WITH / CTE

**Tableau wraps Custom SQL as a derived table (`SELECT ... FROM (<your sql>) Custom_SQL_Query`), and SQL Server rejects a `WITH` clause at the start of a parenthesized subquery.** Custom SQL that begins with `WITH cte AS (...) SELECT ...` fails on connect with `Incorrect syntax near the keyword 'WITH'`. This is NOT caught by opening the workbook: the file parses from saved metadata and even reaches the Custom SQL connect prompt, then fails only when Tableau executes the query.

**Fixes:**
- **Preferred:** rewrite each CTE as a derived table or inline subquery so there is no leading `WITH`. `WITH funded AS (<body>) SELECT ... FROM funded f` becomes `SELECT ... FROM (<body>) f`. A CTE referenced only inside `IN (...)` or a `CASE` becomes a direct subquery there. Nested derived tables are fine; only a leading `WITH` breaks.
- **When CTEs are genuinely needed (complex multi-step logic):** put the logic in the connection's **Initial SQL** to populate a `#temp` table, then make the Custom SQL `SELECT * FROM #temp`.

**ALWAYS test Custom SQL the way Tableau runs it** by wrapping it in a subquery against the database before shipping: `SELECT TOP 10 * FROM (<your custom sql>) Custom_SQL_Query;` (or `COUNT(*)` to also confirm row counts). Running the query as a top-level statement (SSMS, MCP execute_sql) hides this bug because a leading `WITH` is legal there. Workbook-load success is NOT sufficient verification.

### Column Definitions

```python
# In the connection block:
cols_map = ET.SubElement(conn, 'cols')
for col_name in columns:
    m = ET.SubElement(cols_map, 'map')
    m.set('key', f'[{col_name}]')
    m.set('value', f'[Custom SQL Query].[{col_name}]')

# Metadata records:
metadata = ET.SubElement(conn, 'metadata-records')
for col_name, local_type, remote_type in columns:
    mr = ET.SubElement(metadata, 'metadata-record')
    mr.set('class', 'column')
    ET.SubElement(mr, 'remote-name').text = col_name
    ET.SubElement(mr, 'remote-type').text = remote_type  # 130=nvarchar, 129=varchar, 3=int, 5=real, 20=bigint
    ET.SubElement(mr, 'local-name').text = f'[{col_name}]'
    ET.SubElement(mr, 'parent-name').text = '[Custom SQL Query]'
    ET.SubElement(mr, 'remote-alias').text = col_name
    ET.SubElement(mr, 'local-type').text = local_type  # string, integer, real, date, datetime, boolean
    ET.SubElement(mr, 'aggregation').text = 'Count'  # or Sum for measures
    ET.SubElement(mr, 'contains-null').text = 'true'

# Column definitions on datasource (for field roles):
for col_name, local_type, role, type_attr, caption in columns:
    col_el = ET.SubElement(main_ds, 'column')
    col_el.set('caption', caption)
    col_el.set('datatype', local_type)
    col_el.set('name', f'[{col_name}]')
    col_el.set('role', role)       # 'dimension' or 'measure'
    col_el.set('type', type_attr)  # 'nominal' for dimensions, 'quantitative' for measures
```

### Integer Dimensions

Cast integer IDs to `NVARCHAR` in the Custom SQL and define as `string` type. This avoids filter compatibility issues:

```sql
CAST(s.ParentOfficeID AS NVARCHAR(10)) AS ParentOfficeID
```

### Required Datasource Elements

```python
# Aliases
ET.SubElement(main_ds, 'aliases').set('enabled', 'yes')

# Layout (exact attribute names matter)
layout = ET.SubElement(main_ds, 'layout')
layout.set('_.fcp.SchemaViewerObjectModel.false...dim-percentage', '0.5')
layout.set('_.fcp.SchemaViewerObjectModel.false...measure-percentage', '0.4')
layout.set('dim-ordering', 'alphabetic')
layout.set('measure-ordering', 'alphabetic')
layout.set('show-structure', 'true')

# Semantic values
sv = ET.SubElement(main_ds, 'semantic-values')
ET.SubElement(sv, 'semantic-value').set('key', '[Country].[Name]')
sv.find('semantic-value').set('value', '"United States"')
```

### Calculated Fields

```python
calc_col = ET.SubElement(main_ds, 'column')
calc_col.set('caption', 'Loan Count')
calc_col.set('datatype', 'integer')
calc_col.set('name', '[Calculation_LoanCount]')
calc_col.set('role', 'measure')
calc_col.set('type', 'quantitative')
calc = ET.SubElement(calc_col, 'calculation')
calc.set('class', 'tableau')
calc.set('formula', '1')
```

### Worksheet Construction

```python
ws = ET.SubElement(worksheets, 'worksheet')
ws.set('name', 'My Sheet')

table = ET.SubElement(ws, 'table')
view = ET.SubElement(table, 'view')

# Datasource reference
vds_el = ET.SubElement(view, 'datasources')
vds = ET.SubElement(vds_el, 'datasource')
vds.set('caption', DS_CAPTION)
vds.set('name', DS_NAME)

# Datasource dependencies (declare ALL fields used on shelves + filters)
deps = ET.SubElement(view, 'datasource-dependencies')
deps.set('datasource', DS_NAME)
# Add column + column-instance pairs for each field

# Filters (categorical)
filt = ET.Element('filter')
filt.set('class', 'categorical')
filt.set('column', f'[{DS_NAME}].[none:FieldName:nk]')
gf = ET.SubElement(filt, 'groupfilter')
gf.set('function', 'member')
gf.set('level', '[none:FieldName:nk]')
gf.set('member', '"value"')
view.append(copy.deepcopy(filt))

# Aggregation
ET.SubElement(view, 'aggregation').set('value', 'true')

# Style (can be empty or contain format rules)
ET.SubElement(table, 'style')

# Panes
panes = ET.SubElement(table, 'panes')
pane = ET.SubElement(panes, 'pane')
pane.set('selection-relaxation-option', 'selection-relaxation-allow')  # ATTRIBUTE, not child
pv = ET.SubElement(pane, 'view')
ET.SubElement(pv, 'breakdown').set('value', 'auto')
ET.SubElement(pane, 'mark').set('class', 'Bar')  # or 'Automatic'

# Rows/Cols
ET.SubElement(table, 'rows').text = row_expression
ET.SubElement(table, 'cols').text = col_expression

# Simple ID (required)
ET.SubElement(ws, 'simple-id').set('uuid', '{GUID}')
```

### Row Shelf Syntax

Nested hierarchy with `/`:
```python
def nest_fields(fields):
    if len(fields) == 1:
        return fields[0]
    return f'({fields[0]} / {nest_fields(fields[1:])})'

# Usage:
row_refs = [f'[{DS_NAME}].[none:{f}:nk]' for f in dim_fields]
rows_el.text = nest_fields(row_refs)
```

### Column-Instance Naming Convention

| Role | Derivation | Name Pattern | Type |
|------|-----------|-------------|------|
| Dimension | None | `[none:FieldName:nk]` | nominal |
| Measure | Sum | `[sum:FieldName:qk]` | quantitative |
| Measure | Count | `[cnt:FieldName:qk]` | quantitative |
| Measure | CountD | `[ctd:FieldName:qk]` | quantitative |
| Dimension | Attribute | `[attr:FieldName:nk]` | nominal |
| Measure | User | `[usr:CalcName:qk]` | quantitative |

### Text Table (Crosstab) Pattern

```python
# Rows: nested dimensions
rows_el.text = nest_fields([f'[{DS_NAME}].[none:{f}:nk]' for f in dim_fields])
# Cols: Measure Names
cols_el.text = f'[{DS_NAME}].[:Measure Names]'
# Pane text encoding:
enc = ET.SubElement(pane, 'encodings')
ET.SubElement(enc, 'text').set('column', f'[{DS_NAME}].[Multiple Values]')
# Measure Names filter to select which measures
```

### KPI Big Number Pattern

```python
# Empty rows AND cols
rows_el.text = ''
cols_el.text = ''
# Text encoding with the measure
enc = ET.SubElement(pane, 'encodings')
ET.SubElement(enc, 'text').set('column', f'[{DS_NAME}].[sum:MyMeasure:qk]')
# Font size 36 in table style (added via string manipulation after Desktop save)
```

### Window Definitions

```python
# Worksheet windows
for ws_name in worksheet_names:
    w = ET.SubElement(windows, 'window')
    w.set('class', 'worksheet')
    w.set('name', ws_name)
    cards = ET.SubElement(w, 'cards')
    for edge_name, strip_size, card_types in [
        ('left', '160', ['pages', 'filters', 'marks']),
        ('top', '31', ['columns', 'rows']),
    ]:
        e = ET.SubElement(cards, 'edge')
        e.set('name', edge_name)
        s = ET.SubElement(e, 'strip')
        s.set('size', strip_size)  # MUST be integer string
        for ct in card_types:
            ET.SubElement(s, 'card').set('type', ct)
    ET.SubElement(w, 'simple-id').set('uuid', uid())

# Dashboard window (LAST in windows list)
dw = ET.SubElement(windows, 'window')
dw.set('class', 'dashboard')
dw.set('maximized', 'true')
dw.set('name', 'Dashboard Name')
ET.SubElement(dw, 'cards')
ET.SubElement(dw, 'simple-id').set('uuid', uid())
```

### Template Cleanup

When cloning a template, remove these leftover elements:

```python
for tag in ['shared-views', 'actions', 'datasource-relationships', 'mapsources']:
    for el in root.findall(tag):
        root.remove(el)
```

## Phase 2: Dashboard and Post-Desktop Modifications (Raw String Only)

### The Dashboard Problem

ElementTree re-serialization causes `2805CF18` errors on ANY Tableau Desktop-saved file. Even changing a single attribute via ElementTree and re-serializing breaks the file. Raw string manipulation works reliably.

### Workflow

1. Generate worksheets-only TWB with ElementTree (Phase 1)
2. Open in Tableau Desktop, create dashboard (drag sheets, add filters), save as TWB
3. Modify the Desktop-saved TWB via raw string manipulation (Phase 2)

### Adding Mark Labels

```python
with open('workbook.twb', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the worksheet's </style> and insert before it
ws_idx = content.index("name='MySheet'>")
style_end = content.index('</style>', ws_idx)

label_rule = '''
              <style-rule element='mark'>
                <format attr='mark-labels-show' value='true' />
                <format attr='mark-labels-cull' value='true' />
              </style-rule>'''

content = content[:style_end] + label_rule + '\n            ' + content[style_end:]
```

### KPI Big Number Formatting

```python
# 1. Clear cols
content = content.replace(
    "<cols>[ds].[sum:Measure:qk]</cols>",
    "<cols />"
)

# 2. Add text encoding after <mark class='...' />
mark_end = ws_xml.index("/>", ws_xml.index("<mark class='")) + 2
text_enc = """
    <encodings>
      <text column='[ds].[sum:Measure:qk]' />
    </encodings>
    <style>
      <style-rule element='mark'>
        <format attr='mark-labels-show' value='true' />
        <format attr='mark-labels-cull' value='true' />
      </style-rule>
    </style>"""
ws_xml = ws_xml[:mark_end] + text_enc + ws_xml[mark_end:]

# 3. Add font-size 36 to table style
big_number_style = f"""
    <style-rule element='cell'>
      <format attr='text-align' field='[ds].[sum:Measure:qk]' value='center' />
      <format attr='vertical-align' field='[ds].[sum:Measure:qk]' value='center' />
      <format attr='font-weight' field='[ds].[sum:Measure:qk]' value='bold' />
      <format attr='font-size' field='[ds].[sum:Measure:qk]' value='36' />
    </style-rule>"""
```

### Removing Dashboard Zones

```python
import re
zone_match = re.search(
    r"<zone h='\d+' id='7' name='SPV Count'.*?</zone>\s*\n",
    content, re.DOTALL
)
content = content.replace(zone_match.group(), '')
```

### Adding Dashboard Zones

Insert after a sibling zone (find the closing `</zone>` of the preceding zone):

```python
zone6_end = re.search(
    r"(<zone h='\d+' id='6' name='Total SAO Price'.*?</zone>)",
    content, re.DOTALL
)
insert_pos = zone6_end.end()
new_zone = """
              <zone h='24426' id='7' name='SPV Count' w='21419' x='22071' y='1148'>
                <zone-style>
                  <format attr='border-color' value='#000000' />
                  <format attr='border-style' value='none' />
                  <format attr='border-width' value='0' />
                  <format attr='margin' value='4' />
                </zone-style>
              </zone>"""
content = content[:insert_pos] + '\n' + new_zone + content[insert_pos:]
```

### Number Formatting

```python
# In style-rule element='cell':
# Currency: c"$"#,##0.00    -> $1,234.56
# Thousands: c"$"#,##0,K    -> $1,235K
# Millions: n#,##0,,.0M     -> 1.2M
# Percent: 0.0%             -> 12.3%
```

## TWBX Packaging

```python
import zipfile
with zipfile.ZipFile('output.twbx', 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write('workbook.twb', 'workbook.twb')
    zf.write('logo.jpg', 'Image/logo.jpg')  # Images go in Image/ folder
    # Extracts go in Data/Extracts/ folder
```

## Dashboard Zone Structure (from Tableau Desktop)

Tableau Desktop generates this zone hierarchy:

```xml
<zones>
  <zone id='2' type-v2='layout-basic' h='100000' w='100000' x='0' y='0'>
    <!-- Tiled content zones as children -->
    <zone id='10' param='horz' type-v2='layout-flow'>
      <zone id='8' type-v2='layout-basic'>  <!-- main content area -->
        <zone id='3' name='WorksheetName' h='' w='' x='' y=''>
          <zone-style><!-- border/margin --></zone-style>
        </zone>
        <!-- more worksheet zones -->
      </zone>
      <zone id='9' param='vert' type-v2='layout-flow'>  <!-- filter sidebar -->
        <zone id='11' name='SheetName' type-v2='filter' param='[ds].[field]'>
          <zone-style><!-- border/margin --></zone-style>
        </zone>
      </zone>
    </zone>
    <zone-style><!-- root zone margin=8 --></zone-style>
  </zone>
</zones>
```

### Zone Types (type-v2 values)

| type-v2 | Purpose | Key Attributes |
|---------|---------|---------------|
| `layout-basic` | Container / root | Always root, 100000x100000 |
| `layout-flow` | Auto-layout stack | `param='horz'` or `param='vert'` |
| `filter` | Filter dropdown | `mode='checkdropdown'`, `param='[ds].[field]'`, `values='database'` |
| `paramctrl` | Parameter control | `mode='datetime'`/`'compact'`/`'type_in'` |
| `bitmap` | Image | `is-scaled='1'`, `param='Image/file.png'` |
| `text` | Static text | `forceUpdate='true'`, contains `<formatted-text>` |
| `color` | Color legend | `pane-specification-id`, `leg-item-layout='horz'` |
| `title` | Dashboard title | No special attrs |
| (none) | Worksheet | Just `name='WorksheetName'` -- NO type-v2 |

### Zone-Style (required on all non-root zones)

```xml
<zone-style>
  <format attr='border-color' value='#000000' />
  <format attr='border-style' value='none' />
  <format attr='border-width' value='0' />
  <format attr='margin' value='4' />  <!-- 8 for root -->
</zone-style>
```

## Gotchas and Lessons Learned

1. **ElementTree corrupts Desktop-saved TWBs.** Always use raw string manipulation for post-Desktop changes.
2. **`selection-relaxation-option` is an ATTRIBUTE on `<pane>`, not a child element.**
3. **Strip `size` must be an integer string**, not a float like "2.5".
4. **Layout attributes need prefixed names:** `_.fcp.SchemaViewerObjectModel.false...dim-percentage`.
5. **Dashboard zones referencing worksheets have NO `type-v2` attribute.** The absence of type-v2 + presence of `name` identifies worksheet zones.
6. **Integer dimension fields should be CAST to NVARCHAR in Custom SQL** to avoid filter compatibility issues.
7. **`enable-sort-zone-taborder='true'`** is required on dashboards saved with newer Tableau versions (2026.1+) but rejected by older versions (2021.2).
8. **`devicelayouts` element cannot be empty** -- it requires at least one `devicelayout` child. Omit entirely if not needed.
9. **Every filtered field must be declared in `datasource-dependencies`** of the worksheet view, even if not on a shelf.
10. **`<shared-views>`, `<actions>` from template TWBs leak datasource references.** Always remove them when cloning.
11. **Measure Names filter needs `groupfilter function='union'`** with member entries for each measure.
12. **Dashboard window must be LAST in `<windows>` list** (after all worksheet windows).
13. **Tableau Desktop strips unused column-instances from empty KPI worksheets.** When adding text encodings via raw string manipulation post-Desktop, you must also inject `<datasource-dependencies>` with the column + column-instance definition. Without this, Tableau errors: "There is no field named 'X'."
14. **`datasource-dependencies` must be inserted right after `</datasources>`** in the `<view>` element. Inserting before `<aggregation>` causes schema error: "element 'datasource-dependencies' is not allowed for content model."
15. **`datetimeoffset` SQL columns cause ODBC driver error** `HY106`. Always `CONVERT(NVARCHAR(30), column, 120)` in the Custom SQL.
16. **Database for Analytics views is `Analytics`, not `Finance`.** Set `dbname='Analytics'` in the connection when querying views in the `dbo` or `dw` schema on `hfdsqlfinance`.
17. **For single-account dashboards (1 row per filter), text tables with 30+ columns are unreadable.** Split into logical card groups (Identity, Compliance, Public Records, Connections) with separate worksheets per group.
18. **Dashboard `<size>` determines scrollability.** Use `sizing-mode='fixed'` with a tall `maxheight` (e.g., 4000) for scrollable single-page dashboards. The default Desktop size (800x1000) is too small for data-heavy dashboards.
19. **`<style />` (self-closing) vs `<style>...</style>` (with children):** When adding mark-labels to a worksheet, handle both forms. Replace `<style />` with `<style><style-rule>...</style-rule></style>`; for `<style>...</style>`, insert before `</style>`.
20. **Calculated field formulas must escape `<` and `>` to `&lt;` and `&gt;` in XML attributes.** Tableau formulas with `<=` or `>=` operators (like `IF [Score] <= 5 THEN ...`) cause `Fatal Error: '<' character cannot be used in attribute value 'formula'`. The `formula` attribute on `<calculation>` elements stores text -- always pre-encode these characters when writing formulas via raw string manipulation. Quote characters must use `&quot;` and ampersands `&amp;`.
21. **Worksheet titles eat dashboard space.** When a worksheet zone is on a dashboard, the worksheet's title bar takes 25-40px of internal space. To hide it, add `show-title='false'` to the dashboard zone reference (not the worksheet itself). Pattern: `<zone ... name='WorksheetName' show-title='false' w='...' x='...' y='...'>`. This is essential for text-display worksheets where every pixel matters.
22. **Dashboard zone references for worksheets:** identified by `name='X'` attribute and absence of `type-v2`. When iterating zones with regex to add `show-title='false'`, skip any zone with `type-v2` (those are layout-flow, layout-basic, filter, etc.). Use `re.search(r"<zone[^>]*name='X'[^>]*>", content)` to find them; check `'type-v2' not in match` before modifying.
23. **Number formatting with NULL handling:** Tableau number format strings support 4 sections separated by `;` -- positive;negative;zero;null. To show `$0` for null/zero values: `c"$"#,##0;("$"#,##0);"$0";"$0"`. Without the null section, NULL values render as blank (which looks broken).
24. **Showing calc fields as text marks (no shelves):** For single-account dashboards where you want to display a long formatted string, use the KYC pattern: empty `<rows />` and `<cols />`, mark class `'Automatic'`, with the calc field on `<text>` encoding inside `<encodings>`. Do NOT put the field on Rows -- that makes it a row header (which truncates as "Addr.." / "Comp..").
25. **`<datasource-dependencies>` is required for fields used only in encodings.** Even text mark encodings need the field declared in dependencies. Pattern: declare both `<column>` and `<column-instance>` for the field. Without dependencies, Tableau errors "There is no field named 'X'".

26. **"Apply to all sheets using this datasource" is encoded as `<slices>` blocks inside each affected worksheet's `<view>`.** When a user enables that filter scope in Desktop, Tableau adds `<slices><column>[ds].[none:FieldName:nk]</column></slices>` to every worksheet that uses the datasource. A workbook with 22 worksheets touched by an apply-to-all filter has ~22 `<slices>` blocks. Polish scripts that overwrite or rebuild worksheets MUST preserve these blocks or the filter scope silently resets to one sheet. Detection: `len(re.findall(r'<slices>.*?</slices>', content, re.DOTALL))` -- a count near worksheet count means apply-to-all is set; a count of 1-2 means it's not. Symptom: user reports "you keep resetting my filter."

27. **Always source from the user's latest `.twbx`, not from a frozen template.** Tableau Desktop saves to `.twbx` (zip containing the latest `.twb`). If a polish script reads from an older template (`KYB v2 Complete.twb`) and writes to `KYB Due Diligence Dashboard v2.twb`, it discards every Desktop save the user made since. Workflow: `unzip` the `.twbx` to get the latest `.twb`, modify that, `zip` back into `.twbx`, optionally also write the modified `.twb` to disk so both files agree. Symptom: user reports "you overwrote my file" after every polish run.

28. **Backup before every polish run.** `cp X.twbx X.BACKUP.twbx` before modifying. The `.twbx` is the source of truth; the on-disk `.twb` may already have been overwritten by a previous polish and look stale even though the user's real work survived in the `.twbx`. The `.twbx` modification timestamp is what tells you when the user last saved.

29. **Don't override user-set values blindly.** When polishing a Desktop-saved file, distinguish "first run" from "subsequent run." A naive `font-size = 48` rule blows away the 24pt the user manually set. Either (a) only apply formatting to fields that lack the attribute, or (b) take the user's manual values as the new baseline. The user's manual customizations live in the saved file -- treat the file as authoritative for values it already has.

30. **Tableau Measure Names dimension is NUMERIC-ONLY.** A common pattern for "show N values as N rows from 1 source row" is to make N calculated string measures and put `[:Measure Names]` on Rows with `[Multiple Values]` on Text. **This does not work with string measures.** Even with `role='measure' type='nominal'` on the column and `derivation='User' name='[usr:X:qk]' type='quantitative'` on the column-instance, Tableau's Measure Names dimension silently excludes them. The filter dialog reports "5 not shown" and the canvas is blank. **Use separate worksheets instead** -- one worksheet per row, each showing one URL/string via a single text mark. This is reliable and Tableau auto-detects URLs in text marks for hyperlink behavior.

31. **`<column>` must come BEFORE `<column-instance>` in the datasource.** Schema content model order: `..., dimension*, ..., aliases?, column, column-instance, group?, ..., extract?, layout?, style, semantic-values?, ..., datasource-dependencies*, ..., filter, object-graph?`. Inserting `<column>` at end of datasource (after `<object-graph>`) causes `D2E8DA72: element 'column' is not allowed for content model`. Correct insertion: find first `<column-instance>` in the datasource and insert new columns just before it.

32. **Dynamic per-link click handling needs N worksheets, not 1.** When you want N clickable rows (one URL each), the only reliable Tableau pattern is N separate worksheets stacked in a layout-flow zone. Each worksheet has empty rows/cols, mark class Automatic, text encoding showing one URL field, with `<slices><column>[ds].[none:Filter:nk]</column></slices>` to participate in the dashboard apply-to-all filter. Tableau auto-detects URLs in text marks; clicking the mark opens the URL.

33. **Splitting a dashboard worksheet zone into N new worksheet zones fails programmatically.** Removing one `<zone name='X' h='H' w='W' x='X' y='Y'>` and replacing with five sibling `<zone name='X1' h='H/5' w='W' x='X' y='Y+i*H/5'>` zones causes a generic internal error on file open even though the XML validates. Tableau seems to require the zone hierarchy to come from Desktop's layout engine when adding child zones to an existing layout-basic container. **Workaround:** generate the worksheets, then have the user drag-and-place them in Desktop. Removing and replacing a single zone (1->1) works; multiplying zones (1->N) does not.

34. **Color mapping for categorical fields is stored as `<map to='#hex'><bucket>"value"</bucket></map>` entries inside `<encoding attr='color' field='X' type='palette'>`.** To change the color for a specific value (e.g. UNKNOWN from green to amber), find the encoding block matching the field and replace the `<map>` children. The `<bucket>` text is XML-escaped (`&quot;value&quot;`) for string values and literal `%null%` for nulls. Tableau preserves these mappings across saves once user has explicitly set them in Desktop. Pattern is reliable for Phase 2 raw-string edits.

35. **Each `<map to='#hex'>` must have a UNIQUE hex value within an `<encoding>`.** Tableau treats the color palette as a one-to-one map; two `<map>` entries pointing to the same `to='#DC2626'` cause `2805CF18` internal error on load. Use distinct shades for semantically similar values (e.g., `#e15759` / `#b81d24` / `#7d1416` for three flavors of "fail"). Also use **lowercase hex codes** (`#f28e2b` not `#F28E2B`) to match Tableau's saved format -- mixing case has not been observed in Desktop output and may contribute to the same generic error.

36. **Removing a worksheet zone from the main dashboard requires also fixing `<devicelayouts>`.** Tableau auto-generates a Phone layout that mirrors the main dashboard. When you remove or rename a zone in the main dashboard but leave the Phone layout untouched, the orphan reference causes `2805CF18` on the SECOND load (Tableau seems lenient on first save, strict on reload). **Safe fix:** delete the entire `<devicelayouts>...</devicelayouts>` block. Tableau will regenerate it on next Desktop save. Don't leave an empty `<devicelayouts />` -- per lesson 8, that fails too. Detection: orphan = a worksheet zone name appearing in `<devicelayout>` but missing from the main dashboard's tile zones.

37. **CRITICAL: Modify .twbx files in-memory via `zipfile`, never extract-modify-repack.** The standard approach (extract to dir, modify with text I/O, repack) silently corrupts .twbx files on Windows in ways that XML validation doesn't catch but Tableau rejects with `2805CF18` on subsequent loads. Suspected culprits: text-mode `open()` mangling line endings, ZipInfo regeneration changing zip metadata, character encoding round-trip artifacts. **Reliable pattern:**

    ```python
    import zipfile, shutil
    SOURCE = 'working.twbx'
    TARGET = 'output.twbx'
    with zipfile.ZipFile(SOURCE, 'r') as zin:
        entries = []
        for item in zin.infolist():
            data = zin.read(item.filename)  # bytes
            if item.filename.endswith('.twb'):
                # Byte-level replace -- avoid str ops that touch line endings
                old = b"<map to='#59a14f'>\r\n              <bucket>&quot;UNKNOWN&quot;</bucket>"
                new = b"<map to='#f28e2b'>\r\n              <bucket>&quot;UNKNOWN&quot;</bucket>"
                data = data.replace(old, new)
            entries.append((item, data))
    with zipfile.ZipFile(TARGET, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item, data in entries:
            zout.writestr(item, data)  # preserves ZipInfo metadata
    ```

    Use this pattern for ANY surgical edit (color swaps, single-value changes, small calc field edits). The inner `.twb` filename inside the .twbx does NOT need to match the outer .twbx filename -- Tableau opens whichever `.twb` it finds. For two-way swaps (X→Y and Y→X simultaneously), use a sentinel value to avoid clobbering.

38. **Extract-and-repack IS still required for large structural changes.** Adding new worksheets, modifying calculated field formulas with complex multi-line text, restructuring panes -- these are easier with text-mode operations on the extracted file. Accept the corruption risk and validate by opening in Desktop after each run, with a fresh backup before each attempt. For point edits to existing values, prefer in-memory byte replacement (lesson 37).

39. **Tableau Desktop URL Action "Insert Field" can produce wrong field names.** Reported behavior: user selects a field via the Insert dropdown in the URL Action dialog, Desktop inserts a slightly different name than the actual field. Observed: caption `OFAC Search URL` for field `[Calc_OFACURL]` got inserted as `<[Calc_OFAC_URL]>` (extra underscore). The action saves silently and clicks do nothing because the field doesn't exist with that name. **Fix:** byte-level replace the wrong reference inside `<actions>...</actions>`. Pattern: `expression='&lt;[WrongName]&gt;'` -> `expression='&lt;[CorrectName]&gt;'`. Validate by checking that all `expression=` values reference actual `<column name='...'>` definitions in the datasource. The Insert dropdown is unreliable; manual typing of the bracketed field name is safer.

40. **Customized mark labels: field references MUST be CDATA-wrapped, not literal runs.** When a user types `Label: <FieldName>` in Tableau Desktop's Edit Label dialog and clicks Apply, Desktop sometimes saves the field reference as three separate `<run>` elements with the angle brackets as literal text:
    ```xml
    <!-- BROKEN -- Tableau saves this if user types <field> manually -->
    <run>Label: &lt;</run>
    <run>[ds].[none:Field:nk]</run>
    <run>&gt;</run>
    ```
    This renders as the literal string `Label: <[ds].[none:Field:nk]>` not as the substituted value. Worse, Tableau silently falls back to the bare text encoding rendering, so the label appears to "do nothing." **Correct format** (matches Desktop output when user picks a field via the Insert dropdown):
    ```xml
    <run>Label: </run>
    <run><![CDATA[<[ds].[none:Field:nk]>]]></run>
    ```
    The CDATA wrapping tells Tableau the bracketed expression is a placeholder. **Also required:** `<format attr='mark-labels-show' value='true' />` on a `<style-rule element='mark'>` inside the pane's `<style>` block, otherwise the label is computed but never rendered. Detection: search for `<run>[a-z\.\[\]:_]+</run>` patterns (literal run with what looks like a field path) -- those need to be CDATA-wrapped.

41. **Per-worksheet byte edits beat global pattern replace.** When patching multiple worksheets in a .twb, scope each replacement to that worksheet's byte range (`data.find(start_marker, ...)` to find `<worksheet name='X'>...</worksheet>`) rather than running a global `str.replace`. A pattern like `</style-rule>\r\n            </style>\r\n          </pane>` exists in many worksheets; replacing globally adds your change everywhere. Five-QL-worksheet polishes turning into 24-worksheet polishes is the failure mode. Always extract the worksheet, modify in-place, splice back.

42. **Inside a `<column>`, `<calculation>` MUST precede `<desc>`.** Building a calculated-field column with the description first (`<desc>` then `<calculation>`) throws `Error Code: D2E8DA72 - element 'calculation' is not allowed for content model '...captions, calculation, ... aliases ... semantic-values ... desc ...'` when Tableau Desktop loads the workbook. The column content-model order is fixed: calculation is near the start, desc near the end. Regular (non-calc) columns with only `<desc>` are fine. Verified against Desktop 2026.1.

43. **Field descriptions ARE the data dictionary.** `<column caption='X' ...><desc><formatted-text><run>plain English meaning</run></formatted-text></desc></column>` renders as the field Comment (hover tooltip in the data pane, and available in viz tooltips). Reliable way to ship a self-documenting workbook. Keep `<` `>` `&` out of the text or pre-escape them.

44. **Shown interactive quick-filter card via code (two parts, both required).** (a) Shelf filter in the worksheet `<view>`: `<filter class='categorical' column='[ds].[none:F:nk]'><groupfilter function='level-members' level='[none:F:nk]' user:ui-domain='database' user:ui-enumeration='all' user:ui-marker='enumerate' /></filter>` (selects all members, shown). (b) Card in the worksheet `<window>`: under `<cards><edge name='right'><strip size='160'>` add `<card mode='checklist' param='[ds].[none:F:nk]' type='filter' values='database' />`. The `user:` attributes need the namespace registered in ElementTree: `ET.register_namespace('user','http://www.tableausoftware.com/xml/user')`, then set keys as `{http://www.tableausoftware.com/xml/user}ui-domain`. ElementTree serializes attributes with double quotes -- valid XML, Tableau loads it fine.

45. **`<drill-paths>` for drill-down hierarchies** goes after the `<column>` list and before `<layout>` in the datasource: `<drill-paths><drill-path name='X'><field>[Field1]</field><field>[Field2]</field></drill-path></drill-paths>`. Place the top field on a shelf and Tableau shows the +/- drill control to expand to the next level. Matches Tableau-native output exactly.

46. **Custom SQL cannot start with a `WITH`/CTE; Tableau wraps it as a derived table.** A Custom SQL relation whose text begins with `WITH cte AS (...) SELECT ...` throws `Incorrect syntax near the keyword 'WITH'` at query time. Tableau executes `SELECT ... FROM (<your sql>) Custom_SQL_Query`, and SQL Server forbids a CTE at the start of a parenthesized subquery. This is invisible at workbook-load time -- the file parses, the connect prompt appears, the user even signs in -- and only surfaces on the first query. A clean Desktop open is NOT proof; always wrap-test (`SELECT TOP 10 * FROM (<sql>) q`) against the DB before shipping.

    **Two recovery patterns. Pick based on the CTE's cost.**

    **A. Derived-table rewrite (default for small CTEs).** Inline the CTE body as a subquery in the FROM clause:

    ```sql
    -- WRONG
    WITH base AS (SELECT ... FROM Foo)
    SELECT b.x, j.y FROM base b JOIN Bar j ON ...

    -- RIGHT
    SELECT b.x, j.y FROM (SELECT ... FROM Foo) b JOIN Bar j ON ...
    ```

    Simple, single source of truth, no connection-scope concerns. Use this when the CTE is one or two stages and re-running it per Tableau query is cheap.

    **B. Initial SQL + `#temp` table (for heavy, multi-stage CTEs).** Tableau runs the named-connection's `one-time-sql` ONCE per connection, then the Custom SQL many times. Move expensive CTE work to Initial SQL, materialize a local temp table, and let the Custom SQL relation become a cheap `SELECT ... FROM #temp WHERE ...`. Much more performant when the CTE involves multi-stage string cleanup, multiple `CROSS APPLY`s, window functions over the whole row set, or several `UNION`s -- none of those re-run on every viz interaction.

    The Initial SQL lives in the `one-time-sql=` attribute on the named-connection's inner `<connection>` element (the same slot we usually leave empty). XML-escape `'`, `<`, `>`, newlines (`&#10;`), tabs (`&#9;`), carriage returns (`&#13;`) -- Tableau's saved .tds shows the encoding pattern. A working real example lives at `C:\Users\esmith\temp\HubspotEmailSync.tdsx` (unzip and read `HubspotEmailSync.tds`): nine CTEs build a deduped provider-email-with-type set into `#demo`, then the Custom SQL is six lines.

    ```xml
    <named-connection caption='HFDSQLFINANCE.office.local' name='sqlserver.<id>'>
      <connection
          authentication='sqlserver'
          class='sqlserver'
          dbname='HFDProd_Finance'
          odbc-native-protocol='yes'
          one-time-sql='WITH CleanedData AS (
              SELECT ... FROM providers WHERE status NOT IN (...) AND IsActive = 1
          ),
          SplitNames AS ( SELECT ... FROM CleanedData ),
          dmemails AS ( ... ),
          officeemails AS ( ... CROSS APPLY [Finance].dbo.SplitEmails(email1) e ... ),
          /* more CTEs */
          agged AS ( SELECT email, MAX(...) AS firstname, ..., providerid FROM domained GROUP BY ... )
          SELECT email, firstname, lastname, middlename, providerid, type,
                 ROW_NUMBER() OVER (PARTITION BY email, providerid ORDER BY firstname) AS rn
          INTO #demo
          FROM agged
          GROUP BY email, providerid, firstname, lastname, middlename, title'
          server='HFDSQLFINANCE.office.local'
          sslmode='require'
          username='ReportUser'
          workgroup-auth-mode='prompt' />
    </named-connection>

    <!-- The Custom SQL relation is now tiny and fast: -->
    <relation connection='sqlserver.<id>' name='Custom SQL Query' type='text'>
      SELECT email,
             firstname AS first_name,
             lastname  AS last_name,
             middlename AS middle_name,
             providerid AS provider_id,
             type
      FROM #demo
      WHERE rn = 1
    </relation>
    ```

    **Pitfalls and notes for pattern B:**

    - Use single-hash `#temp` (session-scoped to this connection), NOT double-hash `##temp` (global; cross-session collisions).
    - Initial SQL runs PER CONNECTION. Tableau Cloud extract refreshes, scheduled subscriptions, and Bridge re-runs each establish a fresh connection -- `#temp` materializes again each time. That is the intended behavior; the cost is one-shot per session, not per viz.
    - If multiple datasources share the same connection they share the `#temp`. Convention: each datasource gets its own connection and its own temp name.
    - `SELECT ... INTO #temp` requires permission to write to `tempdb` (`ReportUser` has this).
    - When the connection drops (timeout, retry, manual reconnect) Tableau re-runs Initial SQL automatically. No cache-lifecycle code needed on your side.
    - Pre-validate with `SELECT TOP 10 * FROM (<Custom SQL body>) q` AFTER running the Initial SQL once in a SSMS session -- you cannot wrap-test the Custom SQL without the temp table existing.

    **Choosing between A and B:** A if the CTE inlines to a similar plan and re-running it per query is cheap (single-source rollups, lookups, light derived tables). B if the CTE involves expensive string cleanup, multi-source UNIONs, ROW_NUMBER window functions over the full row set, or anything you'd hate to recompute on every dashboard interaction.

47. **You CAN splice a new `<worksheet>` into a Desktop-saved .twb via raw string (unlike new dashboard zones, which fail).** Insert the `<worksheet>...</worksheet>` just before `</worksheets>`, and a matching `<window class='worksheet' name='...'>` just before `<window class='dashboard'>` (the dashboard window must stay last). Reference the existing datasource by name. Putting a `<filter>` AFTER sort/slices elements throws `D2E8DA72: element 'filter' is not allowed for content model`. **A shelf-sorted sheet scopes via `<slices>` (apply-to-all), not a direct `<filter>`** -- copy the structure of a sibling sheet that already has the same sort. `D2E8DA72` only surfaces on load, so always run the `twb-selftest` skill's Desktop smoke test on the result.

    **CORRECTION (2026-06-10): do NOT emit `<single-value-per-nest-shelf-sorts>` in generated files.** A fresh workbook carrying it failed Desktop 2026.1 load with `D2E8DA72: no declaration found for element 'single-value-per-nest-shelf-sorts'`. The error's own content model is authoritative for the base view schema: `(datasources?, mapsources?, datasource-dependencies*, filter, ((computed-sort)|(manual-sort)|(natural-sort)|(alphabetic-sort)), perspectives, shelf-sorts, slices?, aggregation)` -- the element this lesson previously recommended is not in it (it appears only in files whose document format gates it; the earlier observation came from such a file). Sort-by-measure in generated workbooks: leave the default sort and document the one-click Desktop step, or use the legacy `computed-sort` family if a verified sample exists. Note also that Desktop-saved files legally interleave `filter` and `*-sort` elements; the printed model elides repetition, so only treat UNKNOWN elements (and filter-after-slices) as errors.

48. **One-level subtotals on a deep text table are not worth hand-authoring; use a compact summary sheet instead.** A user wanted "one total per date" on a 19-dimension detail table. Tableau's "Add All Subtotals" fires at every nesting level (and where a dimension like HFD ID is unique, that is a subtotal on every row), and limiting subtotals to one level is a layout-engine operation with no clean reusable XML. The reliable answer is a separate summary worksheet: the grouping dimension on Rows (with the descending shelf-sort), the measure on Text, scoped via `<slices>`. One row per group = one total per group, which is what "totals at a glance" actually needs.

49. **Calculated-field formulas (including LODs) reference fields by INTERNAL name, not caption.** The calc editor shows captions, but the saved `.twb` stores the field's `name='[...]'`. A field captioned 'Amount Funded' with `name='[FundedAmount]'` is referenced in a formula as `[FundedAmount]`, NOT `[Amount Funded]` -- get it wrong and the calc silently fails to resolve. Calc column format: `<column caption='Deposit Total' datatype='real' default-format='...' name='[Calculation_DepositTotal]' role='measure' type='quantitative'><calculation class='tableau' formula='{ FIXED [FundingSentDate],[ProviderId] : SUM([FundedAmount]) }' /></column>` (escape `<` `>` `&` per gotcha 20; `{}` `:` `,` are fine). **To surface a calc as a column in an existing Measure-Names text table:** (1) add the `<column>`+`<calculation>` to the datasource; (2) in that worksheet's `<datasource-dependencies>` add a `<column>` and a `<column-instance derivation='Sum' name='[sum:Calculation_X:qk]'>` (Desktop groups all columns before all column-instances -- insert each in its own group); (3) add a member to the worksheet's Measure Names filter: `<groupfilter function='member' level='[:Measure Names]' member='&quot;[ds].[sum:Calculation_X:qk]&quot;' />`. The `[Multiple Values]` text encoding then includes it. A FIXED LOD shown at a finer grain (e.g., one transaction per row) displays the group total on every row, which is the no-click "subtotal inline" pattern.

50. **Default a shown filter to specific values to scope an otherwise-unscoped source.** Keep the Custom SQL free of hard-coded IDs (reusable across all providers), then set the shown filter's SAVED selection so the workbook opens scoped: `<filter class='categorical' column='[ds].[none:ProviderId:nk]'><groupfilter function='union' user:ui-domain='database' user:ui-enumeration='inclusive' user:ui-marker='enumerate'><groupfilter function='member' level='[none:ProviderId:nk]' member='&quot;25233&quot;' /><groupfilter function='member' level='[none:ProviderId:nk]' member='&quot;32588&quot;' /></groupfilter></filter>`. Tableau pushes the selection down to SQL, so the sheet opens querying only those members, not the full table. This is the right pattern for "de-hardcode the WHERE clause but still open to the relevant subset" and for per-subscriber subscription defaults. NOTE: a FIXED LOD computes before such dimension filters, so include the scoping field inside the FIXED (e.g. `{ FIXED [FundingSentDate],[ProviderId] : ... }`) or the LOD will total across all members.

51. **Calc-field `<column>` does NOT accept a `<format>` child.** Emitting `<format attr='default-number-format' value='0.0%'/>` as a child of a calc-field column throws `D2E8DA72: element 'format' is not allowed for content model '(server-captions,calculation,utility-members?,aliases,statistical-model?,semantic-values*,desc,((members)|(range)))'` at Desktop load. Column-level number-format hints are not in this content model. Emit formatting at the worksheet level: `<table><style><style-rule element='cell'><format attr='text-format' field='[ds].[usr:Caption:qk]' value='0.0%' /></style-rule></style>`. **Do not** carry a `number_fmt` field through the calc-field table and emit it onto the column; carry it to the worksheet style-rule builder instead.

52. **`<aliases>` must come BEFORE the first `<column>` in `<datasource>`.** The datasource content model is `(repository-location?, connection?, utility-dimensions?, dimension*, overridable-settings?, aliases?, column, column-instance, group?, ...)`. Build order: connection, named-connections, cols-map, metadata-records, aliases, data columns, calc/parameter columns, layout, style. When inserting calc and parameter columns dynamically AFTER `build_datasource` runs, target the position immediately before `<layout>` (the boundary between columns and post-column structural children), NOT before `<aliases>`. A helper named `_insert_before_layout(main_ds, elem)` is more durable than `_insert_before_aliases` and survives reordering aliases.

53. **Mark "Detail" shelf uses `<lod>`, NOT `<detail>`.** The `<encodings>` content model only allows `((color|size|text|shape|wedge-size|lod|geometry|image|tooltip|path|level|edge|custom))`. There is no `<detail>` element; emitting one throws `D2E8DA72: element 'detail' is not allowed for content model`. For a Detail-shelf dimension on a scatter: `ET.SubElement(enc, 'lod').set('column', '[ds].[none:AccountName:nk]')`. Cross-check against `TableauExamples/` — `<lod>` appears 20+ times in those reference workbooks, `<detail>` appears nowhere.

54. **In `<table>`, `<rows>` and `<cols>` must come AFTER `<panes>`.** Schema: `(view, style, panes, mark-layout?, rows, cols, table-calc-densification?, pages?, ...)`. The text-table helper `_add_text_table_pane` adds `<panes>` before the caller sets rows/cols (correct). Custom-pane builders (scatter, etc.) must explicitly add `<panes>` first, then `<rows>`, then `<cols>`. Wrong order produces `D2E8DA72: element 'cols' is not allowed for content model (view,style,panes,mark-layout?,rows,cols,...)`.

55. **`<rows>` and `<cols>` are REQUIRED; they can be empty, but they CANNOT be absent.** Neither has `?` in the content model. Omitting them produces `D2E8DA72: missing elements in content model '(view,style,panes,mark-layout?,rows,cols,...)'`. KPI-style worksheets (Measure Names on Rows, nothing on Cols) emit `ET.SubElement(table, 'cols')` with no text — present per schema, empty per intent. **Do not** put `[ds].[:Measure Values]` (or any other made-up placeholder) on Cols to "fill it" — `:Measure Values` is not a field name and Desktop reports `There is no field named ':Measure Values'` at sheet-render time. Empty `<cols></cols>` is correct.

56. **Parameter `<column>` REQUIRES a `value=` attribute holding the current value as a literal expression.** For a string list parameter with default "Year to Date": `param_col.set('value', '"Year to Date"')` — serializes to `value="&quot;Year to Date&quot;"`. The same expression also goes in the `<calculation formula='...'/>` child, and BOTH must be set. Without the column-level `value=` attribute, Desktop fails to load the datasource with the bare warning `value - empty text` (followed by "data source could not be opened" warnings on every worksheet). This warning specifically diagnoses a parameter's missing current-value attribute — it is NOT a generic empty-text complaint. When you see `value - empty text`, search every `<column param-domain-type=...>` and confirm `value=` is set.

57. **SQL Server connections need `sslmode='require'` (and template-matching attrs).** Without `sslmode`, Desktop reports "data source could not be opened" before the auth prompt — the failure is in the SSL connection negotiation, not auth. Match the HFD Datawarehouse template's named-connection attrs exactly: `authentication='sqlserver'`, `sslmode='require'`, `odbc-native-protocol='yes'`, `minimum-driver-version='SQL Server Native Client 10.0'`, `username=''` (let Desktop prompt for credentials), `workgroup-auth-mode='prompt'`. The HFD template path is in this skill's "Environment" section; diff your generated connection against it whenever a connection refuses to open before the auth dialog appears.

58. **Pre-Desktop structural validator: run this Python check before declaring Phase 1 done.** `lxml.etree.parse` accepts what Desktop rejects; lessons 51-56 are all schema-content-model errors a static check can catch in milliseconds instead of minutes per Desktop round-trip.

    ```python
    # validate_twb.py -- run after every Phase 1 build, before opening in Desktop.
    from lxml import etree
    import sys

    def validate_twb(path):
        r = etree.parse(path).getroot()
        errors = []

        # Lesson 51: no <format> child of calc-field <column>
        for c in r.findall('.//datasource/column'):
            if c.find('format') is not None:
                errors.append(f"column {c.get('name')!r} has <format> child (move to worksheet style-rule)")

        # Lesson 52: aliases precedes first column in each datasource
        for ds in r.findall('.//datasource'):
            tags = [c.tag for c in ds]
            if 'aliases' in tags and 'column' in tags and tags.index('aliases') > tags.index('column'):
                errors.append(f"datasource {ds.get('name')!r}: <aliases> appears after <column>")

        # Lessons 53-55: per worksheet
        for ws in r.findall('.//worksheet'):
            tbl = ws.find('table')
            if tbl is None: continue
            name = ws.get('name')

            # Lesson 53: <detail> in encodings (should be <lod>)
            for enc in tbl.findall('.//encodings'):
                if enc.find('detail') is not None:
                    errors.append(f"worksheet {name!r}: <detail> in encodings (use <lod>)")

            # Lesson 54: panes < rows < cols
            order = [c.tag for c in tbl]
            for a, b in (('panes', 'rows'), ('rows', 'cols')):
                if a in order and b in order and order.index(a) > order.index(b):
                    errors.append(f"worksheet {name!r}: <{b}> appears before <{a}>")

            # Lesson 55: rows and cols both present (may be empty)
            for tag in ('rows', 'cols'):
                if tbl.find(tag) is None:
                    errors.append(f"worksheet {name!r}: missing required <{tag}>")

            # Lesson 55 (extra): no fake :Measure Values on a shelf
            for tag in ('rows', 'cols'):
                el = tbl.find(tag)
                if el is not None and el.text and ':Measure Values]' in el.text:
                    errors.append(f"worksheet {name!r}: <{tag}> uses fake field ':Measure Values'")

        # Lesson 56: every parameter column has value=
        for col in r.findall('.//datasource/column'):
            if col.get('param-domain-type') and not col.get('value'):
                errors.append(f"parameter column {col.get('name')!r} missing value= attribute")

        return errors

    if __name__ == '__main__':
        bugs = validate_twb(sys.argv[1])
        if bugs:
            print('FAIL: structural issues in', sys.argv[1])
            for b in bugs: print('  -', b)
            sys.exit(1)
        print('PASS:', sys.argv[1], 'structural validation OK')
    ```
    Wire it into the build script (`subprocess.run(['python','validate_twb.py',OUTPUT], check=True)`) or run as a separate step. Pre-validation catches lessons 51-56 in milliseconds and saves the load-edit-reopen cycle in Desktop. **`XML OK` from lxml is NOT proof a TWB will load.**

59. **Tableau parses any `<...>` pattern in Custom SQL as a parameter reference -- in SQL operators AND comments.** A Custom SQL relation containing `<>` (SQL Server's not-equal), or any text matching `<word>`, fails at connect time with `F024F6FE: Custom SQL relation refers to a non-existent parameter: <whatever text>` and the workbook cannot open the data source. Tableau's parameter-substitution scan is naive text matching applied to the entire relation body, comments included. Rules:

    - Use `!=` instead of `<>` for not-equal. SQL Server accepts both; `!=` has no angle brackets.
    - Never use `<placeholder>` style in SQL comments. Replace with words or backticks: `-- (the whole query)`, `` -- `the body` ``, etc.
    - Keep the entire Custom SQL file free of `<` and `>` characters, including line comments. Even `--   SELECT * FROM (<the query>) test_wrap` at the top of the file will be parsed.

    Detection: scan the saved .twb's `<relation type='text'>` element text for any `<[^>]+>` pattern. The validator in lesson 58 should also check this -- add:
    ```python
    import re
    for rel in r.iter():
        if rel.tag.endswith('relation') and rel.get('type') == 'text' and rel.text:
            finds = re.findall(r'<[^>]+>', rel.text)
            if finds:
                errors.append(
                    f"Custom SQL relation has angle-bracket patterns Tableau will "
                    f"misread as parameter refs: {finds[:3]}")
    ```

60. **For HFD provider workbooks, default `AccountName` to `ProviderPracticeName` (with fallback).** `DimProvider.ProviderName` is the legal entity ("Cody Wallace Enterprises, LLC", "A1212 DP LLC"); `DimProvider.ProviderPracticeName` is the consumer-facing brand ("Iridescent Medical Spa", "YOU Just Better"). Practice name is what a business user reading the dashboard recognizes. Use `COALESCE(dp.ProviderPracticeName, dp.ProviderName, providerkey)` for AccountName; same swap for ParentProvider when joining to the parent row.

61. **Join DimProvider to DimPartner on the right key.** The relationship is `DimProvider.ProviderPartnerKey = DimPartner.PartnerUniqueKey` -- NOT `DimPartner.PartnerKey`, which does not exist. DimPartner columns: `PartnerUniqueKey, PartnerName, PartnerType` (e.g. 'Network'), `PartnerClass, PartnerTechnology, PartnerIsActive`. Always `LEFT JOIN`: a missing partner is normal. For medspas roughly 14% of providers carry a partner (the rest are direct); for dental/ortho the coverage is much higher.

62. **Tableau parameters on a dashboard: there is no "Show Parameter" item in the dashboard right-click menu.** Two reliable Desktop paths to add a parameter card to an assembled dashboard:
    - **Per-zone dropdown:** click any worksheet zone on the dashboard, then click the small chevron in its top-right corner -> `Parameters` -> check the parameter name. The card appears (usually right side); drag to the desired position.
    - **From the data pane:** with the dashboard tab active, right-click the parameter under `Parameters` in the left data pane -> `Show Parameter`.

    Programmatic equivalent for pre-emitting it: a parameter card on a dashboard is a `<zone type-v2='paramctrl'>` under the dashboard's layout-flow zone, with `mode='compact'` / `'slider'` / `'type_in'` depending on the parameter's domain. The parameter `<column param-domain-type=...>` must already exist on the datasource (lesson 56) and have a `value=` attribute set. Wiring this in Phase 1 is doable but not standard -- the convention is to leave it as a Desktop step.

63. **Three styling tasks that genuinely have to be done in Desktop.** None has a clean, reproducible Phase 1 XML pattern; attempting them in ElementTree risks `D2E8DA72` or silent rendering failures. Document these in the build script as known Desktop steps and tell the user.
    - **Median (or other percentile/constant) reference lines on a continuous axis.** Desktop: right-click axis -> Add Reference Line -> per Pane -> Median (X and Y separately for a scatter). None of the bundled reference workbooks contain a `<reference-line>` element, and the HFD Datawarehouse template does not either.
    - **Conditional/heatmap color on a single column in a Measure-Names crosstab.** The shared `[Multiple Values]` text encoding makes per-cell value-driven color on a single measure hard to express. Desktop: drag the target measure (e.g. 30-Day FPD) onto Color on the Marks card; Edit Colors -> Red-Green Diverging, Reversed (so green = low FPD = good). 30 seconds.
    - **Tooltip body layout** (bold/color/line breaks/headers in the tooltip). Tableau's Edit Tooltip dialog. Phase 1 tooltip-encoding declarations make a field *appear* in the tooltip but do not control its visual layout. (UPDATE 2026-06-22: embedding a breakdown/viz sheet in a tooltip -- "Viz-in-Tooltip" -- IS scriptable; see lesson 75. Only pure text-layout polish of the default tooltip stays a Desktop nicety.)

64. **Build-script pattern for default-to-specific-members filters (lesson 50, build edition).** Extend the FILTER_DIMS table from a `(field, caption)` pair to a `(field, caption, default_members)` triple. `None` keeps the existing show-all `level-members` / `ui-enumeration='all'` shape. A list of strings switches to the `function='union'` shape with one `<groupfilter function='member' member='"X"'/>` child per pre-selected value -- the filter card opens scoped to those members and the user can re-select at runtime. The two emit shapes share the same `<filter>`/`<slices>` insertion ordering (lesson 47); only the inner `<groupfilter>` differs:

    ```python
    FILTER_DIMS = [
        ('AccountName',      'Account Name',       None),
        ('ParentProvider',   'Parent Provider',    None),
        ('ProgramCode',      'Program Code',       None),
        ('InLoyaltyProgram', 'In Loyalty Program', None),
        ('ProviderStatus',   'Provider Status',    ['CUR']),  # default to active
    ]

    for field, caption, default_members in FILTER_DIMS:
        col_ref = f'[{DS_NAME}].[none:{field}:nk]'
        filt = ET.Element('filter')
        filt.set('class',  'categorical')
        filt.set('column', col_ref)

        if default_members:
            gf = ET.SubElement(filt, 'groupfilter')
            gf.set('function', 'union')
            gf.set(f'{{{_USER_NS}}}ui-domain',      'database')
            gf.set(f'{{{_USER_NS}}}ui-enumeration', 'inclusive')
            gf.set(f'{{{_USER_NS}}}ui-marker',      'enumerate')
            for m in default_members:
                mgf = ET.SubElement(gf, 'groupfilter')
                mgf.set('function', 'member')
                mgf.set('level',    f'[none:{field}:nk]')
                # ET encodes the literal " to &quot; on serialisation,
                # matching Tableau's saved form.
                mgf.set('member',   f'"{m}"')
        else:
            gf = ET.SubElement(filt, 'groupfilter')
            gf.set('function', 'level-members')
            gf.set('level', f'[none:{field}:nk]')
            gf.set(f'{{{_USER_NS}}}ui-enumeration', 'all')
            gf.set(f'{{{_USER_NS}}}ui-marker',      'enumerate')
        # ... insert filt before <aggregation> in <view>, then add the
        #     col_ref to the shared <slices> block (lesson 26) ...
    ```

    The same FILTER_DIMS entry drives the `<datasource-dependencies>` declaration (lesson 9), the per-view `<filter>` element, and the `<slices>` column reference -- one source of truth, one new tuple per default-scoped filter.

65. **Auto-merge Desktop polish on rebuild — never wipe the user's dashboard.** Lesson 27 says "always source from the user's latest save." In practice, build scripts that rewrite `OUTPUT` from a template will silently destroy any dashboards, dashboard windows, reference lines, and color/format tweaks the user added in Desktop. The fix is to splice that Desktop-only state back in via Phase 2 raw-byte surgery at the end of `main()`. Three classes of polish to preserve:

    - **Dashboards** — extract `<dashboards>...</dashboards>` and either replace the (rare) existing dashboards block in the rebuilt TWB or insert it after `</worksheets>`.
    - **Dashboard windows** — `<window class='dashboard'>...</window>` lives in `<windows>`. Insert just before `</windows>` so it ends up last (Tableau convention).
    - **Reference lines / pane-level Desktop edits** — `<reference-line .../>` elements live inside a worksheet's `<pane>`, right after `</encodings>`. Find the source worksheet block, regex out the ref-lines, splice them after `</encodings>` in the target's matching worksheet.

    **Quote-style trap:** `ElementTree.write()` emits attributes with double quotes, Tableau Desktop saves with single. A regex like `<worksheet name='Provider Health Scatter'>` will silently miss the build output. Always use a character class: `<worksheet name=['"]Provider Health Scatter['"]>`.

    **Manifest-sync trap (D2E8DA72 on dashboard/devicelayout attributes):** Modern Tableau Desktop emits attributes that are gated by `<document-format-change-manifest>` entries. Examples seen in the wild:

    | Attribute | Element | Required manifest entry |
    |---|---|---|
    | `enable-sort-zone-taborder='true'` | `<dashboard>` | `<AccessibleZoneTabOrder />` |
    | `auto-generated='true'` | `<devicelayout>` | `<AutoCreateAndUpdateDSDPhoneLayouts />` |

    If the rebuilt-from-template TWB's manifest is missing these, Tableau Desktop rejects the merged file with `Error(L,C): attribute 'X' is not declared for element 'Y'`. Fix: before splicing dashboards/windows, sync the source manifest's bare-element entries into the target manifest. Idempotent — only add entries not already present in either bare (`<X />`) or prefixed (`_.fcp.X.true...X`) form. Don't strip the attributes — those entries may be needed by other Desktop-only attributes you haven't hit yet.

    Wire the merge into the end of `main()` so a single `python build_xxx.py` does both the rebuild AND the polish-restore:

    ```python
    tree.write(OUTPUT, encoding='utf-8', xml_declaration=True)
    try:
        import merge_desktop_polish as _mdp
        src = _mdp._newest_backup()              # finds newest BACKUP-*.twb
        if src and os.path.abspath(src) != os.path.abspath(OUTPUT):
            _mdp.merge(src, OUTPUT)
    except Exception as exc:                     # don't fail the build
        print(f'Polish auto-merge skipped: {exc}')
    ```

    The merge utility also writes a `PREMERGE-{ts}.twb` snapshot of the target before overwriting, so the merge itself is reversible. See `C:\Users\esmith\temp\merge_desktop_polish.py` for the reference implementation.

66. **Workbooks on a LAYERED published datasource (sqlproxy) reference fields by deterministic GUIDs, not column names.** `v.HfdV3`-era published sources (multi-table relationship model) expose each field as a UUIDv3-style GUID (`28869b54-8a0e-3c60-...` = Person Hashed National Id). Shelf refs are `[sqlproxy.<id>].[none:GUID:nk]`, calc formulas reference `[GUID]` directly (including inside FIXED LODs), and Measure-Names filter members use the datasource CAPTION: `&quot;[v.HfdV3].[usr:Calculation_X:qk]&quot;`. Older published sources (CRO-era, single table) use plain column names (`[ContractCreated]`). You cannot invent GUIDs: harvest the caption-to-GUID map from the `<metadata-record>` cache of any existing Desktop-saved workbook on the same datasource. **Generation strategy that works:** clone that workbook's entire `<datasource>` block verbatim (raw string), strip its workbook-local state, inject your own calcs, then write your own worksheets/dashboard/windows. Strip list, in order: (a) the `<calculations>` registry inside `<connection>`; (b) every ds-level `<column>` with a `<calculation>` child or `[Calculation_*]` name (catches `(copy)_NNN`-named calcs too; collect removed names); (c) `<column-instance>` / `<folder-item>` referencing removed names, then empty folders; (d) `<metadata-record>`s whose remote-name is a removed name or that carry a `name='formula'` attribute (transient calc cache); (e) blank the ds-level `<style>` (its encodings reference removed instances); (f) drop the Parameters datasource once `[Parameters].` refs hit zero; (g) remove the workbook-level `<repository-location path='/t/.../workbooks'>` so the file is not identified as the source workbook. Verify zero refs to removed names before proceeding. New calc columns: def-only is sufficient (no connection registry entry needed; Desktop rebuilds it on save) using the layered column shape (`default-type`, `pivot='key'`, `user-datatype`, `visual-totals` attrs). Numeric fields live in `<metadata-record class='measure'>`, strings/dates in `class='column'` - scan both when harvesting GUIDs. Context filters are `context='true'` on `<filter>`; pair them with FIXED LODs for within-filter-scope semantics on self-serve dashboards.

67. **Manifest gating applies to ELEMENTS and FILTER ATTRIBUTES too, not just dashboard attrs (extends lesson 65) - and the old 2021.2 template lacks all the modern entries.** Three more `document-format-change-manifest` gates isolated by Desktop-open bisection (2026-06-10, AM Business Review build; each one is a load-time `D2E8DA72` with a generic dialog and NO element detail):

    | Construct | Required manifest entry | Old-grammar alternative |
    |---|---|---|
    | `<filter class='relative-date' ... period-type-v2='month'>` | `<ISO8601PeriodTypes />` | use `period-type='month'` (works in the old template, verified) |
    | `<computed-sort column=... direction=... using=... />` in `<view>` | `<SortTagCleanup />` | none found on disk; sync the manifest entry instead (verified) |
    | `<single-value-per-nest-shelf-sorts>` in `<view>` | `<SingleValuePerNestSorting />` | use `<computed-sort>` + SortTagCleanup (one element per row dim, all `using=` the same measure, replicates a Desktop global sort) |

    Rules of thumb: (a) any attribute ending `-v2` or element that exists only in recent Desktop saves is suspect - grep your reference workbook's manifest before copying its XML into an old-template build; (b) reference workbooks PROVE a construct only if your generated file carries the same manifest entries - Sales Territory Performance carries ~20 entries the HFD Datawarehouse template lacks; (c) syncing an entry is one line in `clone_template` (`ET.SubElement(manifest, 'SortTagCleanup')`) and is preferable when no old grammar exists. The generic-dialog D2E8DA72 (no element named) is bisectable in ~6 Desktop runs with build-script strip flags (`nodesc nosorts ...` gating each construct class) - strip everything suspect, confirm PASS, re-add one class at a time. The twb-selftest lint now encodes all three (MANIFEST_GATED / ELEMENT_MANIFEST_GATED tables + fixtures `broken_period_type_v2.twb`, `broken_computed_sort_no_manifest.twb`). Related observation: the per-field window filter card that is PROVEN on disk is the minimal `<card param='[ds].[none:F:nk]' type='filter' />` (SPV Dashboard); lesson 44's `mode='checklist' values='database'` variant was never isolated on 2026.1 and the minimal shape is the safer emit.

68. **2026.1 dashboards with filter/param zones REQUIRE dashboard-level `<datasources>` + `<datasource-dependencies>`, and the dashboard window needs populated `<viewpoints>` + a real `<active id>`.** A generated dashboard whose `type-v2='filter'` zones referenced `[ds].[none:GUID:nk]` fields loaded as `2805CF18` (generic internal error) until the dashboard element declared, in order after `<size>`: `<datasources><datasource caption='...' name='ds'/></datasources>` then `<datasource-dependencies datasource='ds'>` containing the `<column>` + `<column-instance>` for every field any zone's `param=` references (exactly what Desktop-saved 2026.1 dashboards carry). Dashboard element child order: repository-location?, style, size, datasources, datasource-dependencies*, zones, devicelayouts?, simple-id. Also: the `<window class='dashboard'>` should contain `<viewpoints>` with one `<viewpoint name='SheetName'/>` per worksheet and `<active id='N'/>` pointing at a REAL worksheet zone id (not -1 with empty viewpoints). `2805CF18` is semantic, not schema: the static D2E8DA72 checks pass and only a Desktop open catches it -- which is why the `twb-selftest` smoke test is mandatory.

69. **The `class='capability'` metadata-record embeds the entire published-datasource definition in a CDATA blob - stash it before any scan or splice.** That blob contains its own `<datasource>`, `<folders-common`, `<metadata-records>`, `[Parameters].` refs, and `Calculation_*` names (the server-side calcs of the published source). Three failure modes observed: naive open/close tag counting goes unbalanced; `ds.find('<folders-common')` lands INSIDE the CDATA so injected columns end up inside the blob (parsed count of your calcs = 0); leftover-reference verification false-positives on the blob's legitimate server-side names. Fix: extract the capability record CDATA-aware (walk `<![CDATA[`...`]]>` spans before trusting `</metadata-record>`), replace with a placeholder token, do ALL stripping/injection/verification on the remainder, restore the block verbatim LAST. Also slice the datasource block end with `rindex('</datasource>', start, index('</datasources>'))`, not the first `</datasource>` after the start. Worked example: `C:\Users\esmith\temp\build_repeat_loans.py` (+ `validate_repeat_loans.py`, which must also blank CDATA spans before raw-text leftover checks).

70. **Full programmatic dashboard generation WORKS on 2026.1 (user-verified) - the complete recipe.** A generated dashboard with a title text zone, 7 KPI big-number zones (2 rows), 4 chart zones, a data-dictionary footer text zone, and a fixed right sidebar of 6 filter zones opened, rendered, and was praised, with zero Desktop assembly. Requirements stack: SPV zone tree (root layout-basic id=2, layout-flow horz, main layout-basic + fixed-size 160 layout-flow vert sidebar, explicit h/w/x/y in 0-100000 units) + dashboard-level `<datasources>`/`<datasource-dependencies>` for every filter-zone field (lesson 68) + `<window class='dashboard'>` with populated `<viewpoints>` and real `<active id>` + `<size ... sizing-mode='fixed'>`. **Sizing tricks:** zone units are FRACTIONS of the canvas, so changing only the `<size>` height rescales every zone proportionally (the painless fix for cramped rows - including the user's own Desktop tweaks); KPI big-number cards show SCROLLBARS when content exceeds the zone - at 1300x1200 with ~108px rows, 36pt bold overflows; 28pt with ~135px rows (canvas 1500 tall) renders clean. Sheet-name zone titles act as the KPI card labels.

71. **Measure Names filter members MUST use the workbook-internal datasource name, not the caption.** `member='&quot;[v.HfdV3].[usr:Calc:qk]&quot;'` (caption form, copied from a COLOR-encoding bucket) matches nothing; members are `member='&quot;[sqlproxy.&lt;id&gt;].[usr:Calc:qk]&quot;'`. Symptom chain on the next Desktop SAVE: the filter is rewritten to `<groupfilter function='empty-level' member='[:Measure Names]' user:op='manual' />`, the now-unused measure calc defs AND their `[usr:...]` column-instances are STRIPPED from that sheet's deps, and worksheet `<style>` number-format rules go with them - the user sees a dimension-only table ("no measures"). Repair on the saved file: restore deps (defs + usr instances), replace empty-level with a union of internal-name members. Related: Desktop save also DROPS worksheet-level `text-format` cell style rules from generated files - put number formats in `default-format` on the ds-level calc `<column>` instead, which drives cards, axes, labels, and table cells. Native tokens (verified from Desktop output): percent `p0.0%` / `p0.00%`, integer `n#,##0;-#,##0`, two-decimal `n#,##0.00;-#,##0.00`, currency `c!en_US!&quot;$&quot;#,##0;-&quot;$&quot;#,##0`.

72. **Relationship-model population trap: FIXED COUNTD across a relationship returns 0 (not NULL) for parents with no child rows, and ELSE-buckets silently absorb them.** v.HfdV3's root grain is FactApplication: 2.0M persons exist but only ~560K have any FactContract. `{FIXED [person]: COUNTD([contract key])}` = 0 for the 1.45M never-signed applicants; a bucket calc ending `ELSE '3+ loans'` classified them all as heavy repeaters, COUNTD(person) KPIs counted applicants instead of borrowers. Any consumer-level workbook on this datasource needs the population guard in the per-sheet filter calc: `ELSEIF ZN([LoansPerConsumer]) &lt; 1 THEN 'Exclude'`. Validate distributions extract-side with the Tableau MCP query-datasource tool - it accepts `{FIXED ...}` custom calculations (e.g. LoanCnt x COUNTD persons proved 524,885 / 27,104 / ~6,000 for 1/2/3+ and matched the rendered KPIs to within refresh drift).

73. **v.HfdV3 is a WINDOWED extract: rolling 3-year contract history (cliff at month -36; ~44 stray rows/month before).** 725,820 contracts / 2,003,861 persons vs 1.76M contracts all-time in the warehouse. Consequences: KPI verification numbers must be computed with the same date floor (`ContractCreated >= DATEADD(YEAR,-3,GETDATE())` matched the rendered dashboard to 0.06%); duration metrics (months-to-second-loan) are right-censored by the window (5.0 in-window vs 9.05 full-history for Aspen at 8.2 in-window); cohort charts show near-zero bars for stray pre-window years. Disclose the window in the on-canvas dictionary.

74. **Hidden fields on a PUBLISHED datasource are server-side state; the workbook cannot unhide them.** Desktop propagates them as `hidden='true'` on worksheet dep copies (informational). To unhide (e.g. Person Hashed National Id): Tableau Cloud > the datasource > Edit Data Source (web authoring) > field list > Show hidden fields > Unhide > Publish. Workbook calcs referencing hidden published fields compute fine; hiddenness only affects the data pane / drag-and-drop.

75. **Viz-in-Tooltip (an embedded breakdown sheet that filters to the hovered mark) IS scriptable -- supersedes lesson 63's "tooltip layout is Desktop-only" for this case.** Reverse-engineered from a Desktop-saved file (2026-06-22, carry dashboard: the `By Vertical` / `By Financed Range` / `By Days to Expiration` bars each embed a breakdown sheet that auto-filters to the bar you hover). Exact structure and rules:

    - **Placement:** `<customized-tooltip>` is a child of `<pane>`, immediately AFTER `<mark .../>` (and after `<encodings>` if present), before `</pane>`. Pane child order: `view, mark, encodings?, customized-tooltip`.
    - **Body** is one `<formatted-text>` of `<run>` elements. Each shown field is a gray label run + a bold CDATA-wrapped value run, then a line-break run; the embedded sheet is its own bold CDATA run:
      ```xml
      <pane selection-relaxation-option='selection-relaxation-allow'>
        <view><breakdown value='auto' /></view>
        <mark class='Bar' />
        <customized-tooltip>
          <formatted-text>
            <run fontcolor='#757575'>Vertical:&#9;</run>
            <run bold='true'><![CDATA[<[ds].[none:Vertical:nk]>]]></run>
            <run>&#198;&#10;</run>
            <run fontcolor='#757575'>Carrying Amount:&#9;</run>
            <run bold='true'><![CDATA[<[ds].[sum:CarryingAmount:qk]>]]></run>
            <run>&#198;&#10;</run>
            <run bold='true'><![CDATA[<Sheet name="Program Breakdown" maxwidth="900" maxheight="900" filter="<All Fields>">]]></run>
            <run>&#198;&#10;</run>
          </formatted-text>
        </customized-tooltip>
      </pane>
      ```
    - **CDATA is mandatory** for BOTH the field placeholders (`<![CDATA[<[ds].[none:Field:nk]>]]>`) and the sheet embed (`<![CDATA[<Sheet name="..." ...>]]>`). The literal `<...>` would otherwise be escaped/misparsed (same root cause as lesson 40). **ElementTree cannot emit CDATA**, so build the whole `<customized-tooltip>` block as a RAW STRING and splice it into each target pane after `<mark .../>` (Phase-2 style) -- do NOT try `ET.SubElement(...).text`.
    - **Sheet-embed attributes:** `name="WorksheetName"` (the embed sheet -- must exist in the workbook; hide it from the tab strip after wiring), `maxwidth`/`maxheight` in **pixels**, `filter="<All Fields>"` (auto-filters the embed by every dimension on the hovering mark, so hovering one Vertical shows just that vertical's breakdown). Attribute quotes inside the CDATA are double quotes; the angle brackets in `<Sheet ...>` and `<All Fields>` are literal thanks to the CDATA.
    - **Sizing is the thing to parameterize: the 300x300 default is far too small for a breakdown table -- the real values used were 900x900 (and 700x900 for a narrower table).** Start a table-in-tooltip at `maxwidth="900" maxheight="900"`.
    - **Line break** is a literal run `<run>&#198;&#10;</run>` -- the character U+00C6 (AE ligature, Tableau's internal line-break marker; saved literally in the .twb, but emit it as the entity `&#198;`) followed by `&#10;` (LF). One after each field row and after the sheet embed.
    - **Helper shape:** `tooltip_with_sheet(field_rows, sheet_name, w=900, h=900) -> str` returns the raw block; then per target worksheet `pane_xml = pane_xml.replace("<mark class='Bar' />", "<mark class='Bar' />\n" + block, 1)`. Always run the `twb-selftest` Desktop open afterward -- malformed CDATA/format runs only surface on load. **Worked example:** `build_carry_dashboard.py` bakes three bar tooltips at build time -- it emits each block with `tooltip_with_sheet(ds, field_rows, sheet_name, w, h)` and inserts it with `splice_tooltip(xml, ws_name, block)` (a per-worksheet `re.subn` on `<mark class="Bar" ?/>`) right after `ET.tostring`, before writing the file.

## Python Dependencies

```
pip install requests requests-negotiate-sspi  # for Tableau Cloud publishing
```

No Tableau-specific libraries needed for TWB generation. `xml.etree.ElementTree` for Phase 1, raw string ops for Phase 2.

## VIZFACTS Design Principles

VIZFACTS is HFD's data visualization standard. Apply it to every worksheet and
dashboard. Full standard with descriptions, examples, and per-principle
guidelines: `references/vizfacts.md`.

1. **Start Simple** -- line charts for trends, bar charts for comparisons, pie/stacked bar for part-to-whole
2. **Clarity in Data Points** -- every point visible and labeled; callouts for key points
3. **Contextual Information** -- annotations, KPI summary cards, small multiples for context
4. **Highlight Key Insights** -- color, size, position, annotations to draw attention to the takeaway
5. **Clear Labeling** -- concise axis/title labels, 12pt+ fonts, hierarchical typography
6. **Color with Purpose** -- consistent, color-blind-friendly palette; color to group or highlight
7. **Iterative Refinement** -- refine on feedback; try alternative chart types if one is not working
8. **Avoid Clutter** -- drop gridlines/borders unless needed, use whitespace, 5 or fewer series per chart
9. **Responsive to User Needs** -- match detail level and chart type to the audience's expertise
10. **Tell a Story** -- title summarizes the insight, arrange elements to guide the viewer's eye

## Building User-Facing Dashboards (naming, filters, data dictionary)

Learnings from how HFD users refine a generated workbook into a friendly, subscription-ready dashboard. Apply these when generating, so the first version needs less hand-editing.

### Name fields and sheets in plain business language

- **Field captions: plain business terms, no parentheticals or jargon.** A user renamed the generated `Parent (Brand)` to `Parent Name`. Avoid clever or qualifier-laden captions; use the word the audience already uses. Prefer `Parent Name`, `Provider`, `Amount Funded`, `Funding Batch ID`.
- **Worksheet / tab names describe the task or view, not the mechanic.** Users renamed `Funded $ by Batch` -> `By Deposit/Debit Day`, `Funded Detail` -> `Funding Detail by Deposit Date`, `Signed, Awaiting Funding` -> `Awaiting Funding`. Generate task-oriented sheet names from the start.
- Apply the rename to the field caption on **every datasource** that exposes it. Renaming on only one datasource (e.g., the one driving the dashboard) leaves the other sheets showing the old caption, which looks inconsistent.

### Consolidate filters on a dashboard (avoid duplicate cards)

When several worksheets share one datasource and each shows the same filters, dragging them all onto a dashboard produces **duplicate filter cards** (one set per sheet). The fix the user applied: set each shared filter to **"Apply to all worksheets using this data source,"** which Tableau encodes as `<slices>` blocks inside each affected worksheet's `<view>` (see gotcha 26). Then the dashboard shows **one** card per filter, controlling all sheets on that datasource.

- **Generate this proactively:** for filters that define shared scope (here `ParentName`, `ParentProviderId`, `ProviderId`), add `<slices>` to every worksheet on that datasource so a combined dashboard does not get duplicates.
- **Show only the relevant filters per view.** The user kept the three provider-scope filters as the shared control and added an `Activity Type` filter only on the funded detail view, where it matters. Do not blanket every filter onto every sheet.
- **Filters are scoped to their datasource.** A filter on `federated.funded` does not affect a sheet built on `federated.signed`. On a multi-source dashboard, give each source its own scope filter, or bridge them with a parameter or a filter action. Per-sheet default selections (set via member filters) still scope each sheet independently even without a shared card.

### Where to put the data dictionary

Field-level `<desc>` comments (gotcha 43) are the canonical dictionary, but they only surface on hover in the data pane and in interactive tooltips. **A subscription delivers a static image or PDF, so hover/tooltip definitions never reach the subscriber.** Placement options, best-to-worst for a subscription:

1. **On-canvas, always-visible Text object** on the dashboard (a footer strip on a tall layout, or a side column). Holds the 6-10 fields the audience needs in plain language. This renders in the subscription image. This is the primary mechanism for subscribed dashboards.
2. **A dedicated "Field Guide" dashboard/tab** with a single Text object holding the full dictionary. Serves interactive and Cloud viewers; a subscription only sends one view, so this is a complete reference rather than what the subscriber sees.
3. **Keep the field `<desc>` comments** for authors and interactive hover/tooltips.
4. **Avoid a collapsible/show-hide info panel for subscriptions** -- the static image captures only the collapsed state, so the definitions would not appear in the emailed image.

Adding the Text object is a Phase 2 raw-string edit on the Desktop-saved file (or have the user drop a Text object and paste the supplied text, which avoids touching their saved layout).

### Dashboard polish rules (user feedback on the Program Code Lookup build, 2026-07-08)

Four corrections the user gave after an otherwise good generated dashboard. Apply them to every future build.

1. **No dead space at the top.** Do not leave an empty band or a half-empty strip in the top fold (the generated build left whitespace around the KPI row). Size the title / how-to / KPI bands tight, and if a horizontal strip has fewer zones than the width needs, widen the zones to fill it or move filter cards into the gap.
2. **Data dictionary gets full width and clear line separation.** The on-canvas dictionary must span the full dashboard width, one definition per line, with a visible break between entries (blank break-run between lines, not one crammed paragraph in a partial-width footer block).
3. **Default quick filters to relevant values ("relative filters"), and performance-test.** Filters should cascade: picking Vertical = Dental should narrow the Segment dropdown to dental segments. In the UI this is "Only Relevant Values"; in the XML the filter zone / window card carries `values='relevant'` (VERIFIED in Desktop-saved files on disk: `Provider Funding Activity - Totals by Date.twb`, `CarryAmountDashboard\Decline Rates.twb`; all-values is `values='database'` as in SPV Dashboard Complete.twb). Fall back to all-values only when relevant-values queries are slow. Always performance-test the result: publish, then render server-side (Tableau MCP `get-view-image` on the dashboard view) and interact once; the live Custom SQL Program Code Lookup passed this.
4. **Filter card mode by cardinality: dropdowns beyond a handful of values.** Fields with more than roughly 5 values must be multi-value DROPDOWNS (`mode='checkdropdown'`), never checklists (`mode='checklist'`), which eat sidebar space. Checklists are acceptable only for tiny domains (2-5 values, e.g. Program Type / Pricing Tier / Waterfall Position). Do not rely on Tableau's default mode selection; set `mode` explicitly on each filter zone and window card.

## Reference Files

- VIZFACTS visualization standard: `references/vizfacts.md`
- Template TWB: `C:\Users\esmith\PycharmProjects\DB-Analytics\HFD Datawarehouse.twb`
- Example dashboards: `C:\Users\esmith\temp\TableauExamples\`
- Build script (current): `C:\Users\esmith\temp\build_tableau_v4b.py`
- Working dashboard reference: `C:\Users\esmith\temp\SPV Dashboard Complete.twb`

## HFD Logo

Extracted from the SSRS Contracts report. Stored at `C:\Users\esmith\temp\hfd_logo.jpg`. Package in TWBX under `Image/hfd_logo.jpg`.

## Disallowed in Output

Em-dashes, exclamation points, metaphors, analogies, purple prose. See CLAUDE.md for the full disallowed list.
