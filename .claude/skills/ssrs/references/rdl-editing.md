# RDL XML Editing

RDL files are XML documents with SSRS-specific schemas. Understanding the tablix structure is essential for any report modification.

## Namespaces

RDL files use multiple XML namespaces:

```xml
<Report xmlns="http://schemas.microsoft.com/sqlserver/reporting/2016/01/reportdefinition"
        xmlns:rd="http://schemas.microsoft.com/SQLServer/reporting/reportdesigner">
```

The default namespace (no prefix) holds layout/data elements. The `rd:` prefix holds designer metadata like TypeName. When iterating with lxml use `{*}ElementName` to match regardless of which prefix:

```python
for dataset in tree.iter('{*}DataSet'):
    ...
```

## Dataset Structure

```xml
<DataSets>
  <DataSet Name="DataSet1">
    <Query>
      <DataSourceName>Finance</DataSourceName>
      <CommandText>SELECT ...</CommandText>
      <QueryParameters>
        <QueryParameter Name="@ParentProvider">
          <Value>=Parameters!ParentProvider.Value</Value>
        </QueryParameter>
      </QueryParameters>
    </Query>
    <Fields>
      <Field Name="HurdleGroup">
        <DataField>HurdleGroup</DataField>
        <rd:TypeName>System.String</rd:TypeName>
      </Field>
      ...
    </Fields>
  </DataSet>
</DataSets>
```

- `<CommandText>` holds the SQL
- `<QueryParameters>` binds SQL parameters (`@Foo`) to report parameters (`Parameters!Foo.Value`)
- `<Fields>` declares what columns the query returns
- SSRS does NOT require Fields to match query columns exactly. Extra query columns are ignored. Missing declared fields cause runtime errors.

## Tablix Structure (The Tricky One)

A tablix has FOUR parallel structures that all must stay in sync when editing:

```xml
<Tablix Name="Tablix1">
  <TablixBody>
    <TablixColumns>
      <TablixColumn><Width>1in</Width></TablixColumn>
      <TablixColumn><Width>2in</Width></TablixColumn>
      <TablixColumn><Width>1in</Width></TablixColumn>
      <!-- one per column -->
    </TablixColumns>

    <TablixRows>
      <TablixRow>
        <Height>0.3in</Height>
        <TablixCells>
          <TablixCell><CellContents>...header 1...</CellContents></TablixCell>
          <TablixCell><CellContents>...header 2...</CellContents></TablixCell>
          <TablixCell><CellContents>...header 3...</CellContents></TablixCell>
          <!-- one per column in this row -->
        </TablixCells>
      </TablixRow>
      <TablixRow>
        <Height>0.25in</Height>
        <TablixCells>
          <TablixCell><CellContents>...data 1...</CellContents></TablixCell>
          <TablixCell><CellContents>...data 2...</CellContents></TablixCell>
          <TablixCell><CellContents>...data 3...</CellContents></TablixCell>
        </TablixCells>
      </TablixRow>
    </TablixRows>
  </TablixBody>

  <TablixColumnHierarchy>
    <TablixMembers>
      <TablixMember />
      <TablixMember />
      <TablixMember />
      <!-- one per column, at the innermost level -->
    </TablixMembers>
  </TablixColumnHierarchy>

  <TablixRowHierarchy>
    <TablixMembers>
      <TablixMember>
        <KeepWithGroup>After</KeepWithGroup>  <!-- header row -->
      </TablixMember>
      <TablixMember>
        <Group Name="Details" />  <!-- detail row -->
        <Visibility>...</Visibility>
      </TablixMember>
    </TablixMembers>
  </TablixRowHierarchy>

  <DataSetName>DataSet1</DataSetName>
</Tablix>
```

**Critical constraint:** The number of `<TablixColumn>` entries must equal the number of innermost `<TablixMember>` entries in `<TablixColumnHierarchy>`. SSRS enforces this on upload with error 1027.

## Removing a Tablix Column (Correct Implementation)

To remove a column, you MUST remove all three parallel entries at the same index:

```python
def remove_tablix_columns(tablix, column_indices):
    """Remove columns at the given indices from the tablix.

    Must remove three parallel entries per column:
      1. <TablixColumn> in <TablixColumns>
      2. <TablixCell> from every <TablixRow> (one cell per row at this index)
      3. <TablixMember> from <TablixColumnHierarchy><TablixMembers>

    Remove from highest index to lowest to avoid index shifting.
    """
    if not column_indices:
        return 0

    indices = sorted(column_indices, reverse=True)

    # 1. TablixColumns
    for tc in tablix.iter('{*}TablixColumns'):
        tc_list = list(tc)
        for idx in indices:
            if idx < len(tc_list):
                tc.remove(tc_list[idx])
        break

    # 2. Cells in each row
    for row in tablix.iter('{*}TablixRow'):
        for cells in row.iter('{*}TablixCells'):
            cells_list = list(cells)
            for idx in indices:
                if idx < len(cells_list):
                    cells.remove(cells_list[idx])

    # 3. TablixMembers in TablixColumnHierarchy
    # Only touch the direct children of the hierarchy element (the top-level members).
    # Nested TablixMembers represent sub-groupings which we don't touch.
    for hierarchy in tablix.iter('{*}TablixColumnHierarchy'):
        for members in hierarchy.iter('{*}TablixMembers'):
            if members.getparent() is hierarchy:
                m_list = list(members)
                for idx in indices:
                    if idx < len(m_list):
                        members.remove(m_list[idx])
                break

    return len(indices)
```

**Why remove from highest index to lowest:** If you remove column 2 first, the old column 4 becomes the new column 3. Working backwards (4, then 2) keeps the indices stable.

## Identifying Columns to Remove

Column headers are static text in the first `<TablixRow>`. Data bindings are `=Fields!X.Value` expressions in the second `<TablixRow>`. Map columns to headers and fields:

```python
def get_tablix_column_header_map(tablix):
    """Return header text for each column (from row 0)."""
    rows = list(tablix.iter('{*}TablixRow'))
    if not rows:
        return []
    header_row = rows[0]
    cells = list(header_row.iter('{*}TablixCell'))
    result = []
    for cell in cells:
        text = None
        for val in cell.iter('{*}Value'):
            if val.text and not val.text.startswith('='):
                text = val.text
                break
        result.append(text)
    return result


def get_tablix_column_field_map(tablix):
    """Return field name for each column (from row 1 data bindings)."""
    import re
    rows = list(tablix.iter('{*}TablixRow'))
    if len(rows) < 2:
        return []
    detail_row = rows[1]
    cells = list(detail_row.iter('{*}TablixCell'))
    result = []
    for cell in cells:
        field_name = None
        for val in cell.iter('{*}Value'):
            if val.text and val.text.startswith('=Fields!'):
                m = re.search(r'Fields!(\w+)\.Value', val.text)
                if m:
                    field_name = m.group(1)
                    break
        result.append(field_name)
    return result


# Usage: identify columns to remove by header text
headers = get_tablix_column_header_map(tablix)
indices_to_remove = [i for i, h in enumerate(headers) if h in {'Provider ID', 'Provider Name'}]
remove_tablix_columns(tablix, indices_to_remove)
```

## Removing Fields from the Dataset

Removing unused `<Field>` declarations is safer than removing columns because it doesn't require hierarchy bookkeeping:

```python
def remove_fields(dataset, field_names_to_remove):
    removed = []
    for fields in dataset.iter('{*}Fields'):
        for field in list(fields):
            name = field.get('Name')
            if name in field_names_to_remove:
                fields.remove(field)
                removed.append(name)
    return removed
```

Before removing a field, verify it's not referenced anywhere in the RDL:

```python
import re
text = rdl_bytes.decode('utf-8')
refs = set(re.findall(r'Fields!(\w+)\.Value', text))
safely_removable = set_of_declared_fields - refs
```

This catches references in visibility expressions, color expressions, filters, sort expressions, parameter defaults, etc. - not just tablix cells.

## Replacing a Dataset Query

```python
def replace_command_text(dataset, new_query):
    for ct in dataset.iter('{*}CommandText'):
        ct.text = new_query
        return True
    return False
```

When inlining a CTE-based query that uses SQL features like `WITH`, make sure the query begins with `;WITH` if it might follow another statement. Inside `<CommandText>`, a bare `WITH` is fine because it's the first and only statement.

## Preserving the UTF-8 BOM

RDL files always start with a UTF-8 BOM (`EF BB BF`) followed by `<?xml version='1.0' encoding='utf-8' standalone='yes'?>`. The BOM must be preserved when serializing back:

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

SSRS Report Server accepts RDLs without the BOM too, but preserving it keeps the file byte-identical when no changes are made to that region, which is useful for diffs.

## Validating After Modification

```python
try:
    body = new_content[3:] if new_content.startswith(b'\xef\xbb\xbf') else new_content
    etree.fromstring(body)
    print('XML validation: OK')
except etree.XMLSyntaxError as e:
    print(f'XML INVALID: {e}')
```

This catches structural issues (unclosed tags, malformed namespaces) but NOT semantic issues (mismatched tablix column counts, missing required elements). The SSRS upload will reject those with error 1027 or rsInvalidReportDefinition.

## Text-Based Query Replacement (Simpler Alternative)

For pure query replacements where you don't need to touch the tablix, a regex-based edit on the text content can be simpler than parsing XML:

```python
import re

def replace_query_only(rdl_bytes):
    bom = b'\xef\xbb\xbf' if rdl_bytes.startswith(b'\xef\xbb\xbf') else b''
    text = rdl_bytes[len(bom):].decode('utf-8')

    # Find and replace within <CommandText>...</CommandText>
    pattern = re.compile(r'(<CommandText>)(.*?)(</CommandText>)', re.DOTALL)
    new_text = pattern.sub(lambda m: m.group(1) + NEW_QUERY + m.group(3), text)

    return bom + new_text.encode('utf-8')
```

This avoids the XML parser entirely. Use when:
- Only the query is changing, nothing else
- The new query doesn't contain characters that need XML escaping (`<`, `>`, `&`)
- You're doing bulk updates and want to minimize per-file processing
