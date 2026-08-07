# SSRS REST API v2.0 Patterns

## Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v2.0/CatalogItems` | List all catalog items |
| GET | `/api/v2.0/CatalogItems({id})` | Get metadata for one item |
| GET | `/api/v2.0/CatalogItems({id})/Content/$value` | Download raw RDL bytes |
| PUT | `/api/v2.0/CatalogItems({id})` | Full update (metadata + content) |

## The Only Upload Pattern That Works

SSRS REST API v2.0 is finicky about content updates. After testing multiple approaches, only one reliably updates the Content column:

```python
def upload_rdl(item_id, new_content, auth):
    # Step 1: GET current metadata
    r = requests.get(f'http://hfdsqlreport/reports/api/v2.0/CatalogItems({item_id})',
                     auth=auth, timeout=15)
    r.raise_for_status()
    body = r.json()

    # Step 2: Strip the OData context annotation (PUT rejects it)
    body.pop('@odata.context', None)

    # Step 3: Merge new content as base64
    import base64
    body['Content'] = base64.b64encode(new_content).decode('ascii')

    # Step 4: PUT the full object
    r = requests.put(f'http://hfdsqlreport/reports/api/v2.0/CatalogItems({item_id})',
                     auth=auth, json=body, timeout=60)
    r.raise_for_status()  # 204 No Content on success
    return r.status_code
```

## What Doesn't Work (and what happens)

| Attempt | Result | Notes |
|---------|--------|-------|
| `PUT /CatalogItems({id})/Content/$value` with raw bytes + `application/octet-stream` | 500 `{"error":{"code":"0","message":""}}` | Endpoint exists but rejects the update |
| `PATCH /CatalogItems({id})` with `{Content: base64}` only | 204 but **silently no-ops** | Dangerous - looks successful but nothing changes. Verify by re-downloading |
| `PATCH /CatalogItems({id})/Content/$value` | 405 Method Not Allowed | |
| PUT with `{Content: raw bytes}` in JSON body | JSON serialization error | Content must be base64 |
| PUT with missing `@odata.type` | 400 | Preserve from GET response |

**Always verify uploads by re-downloading.** The PATCH-no-op is the worst failure mode because it returns a success code.

## Common Upload Errors

### HTTP 500: Tablix column count mismatch

```json
{
  "error": {
    "code": "1027",
    "message": "The tablix 'Tablix1' has an incorrect number of TablixColumns. The number of TablixColumns must equal the number of innermost TablixMembers (TablixMembers with no submembers) in the TablixColumnHierarchy."
  }
}
```

**Cause:** Removed `<TablixColumn>` entries without also removing the corresponding `<TablixMember>` from `<TablixColumnHierarchy>`. See `rdl-editing.md` for the correct removal function.

### HTTP 500: Invalid XML

```json
{
  "error": {
    "code": "rsInvalidReportDefinition",
    "message": "The definition of this report is not valid..."
  }
}
```

**Cause:** Usually a missing closing tag, wrong namespace, or malformed expression. Validate XML parsing locally before upload:

```python
try:
    etree.fromstring(new_content[3:] if new_content.startswith(b'\xef\xbb\xbf') else new_content)
except etree.XMLSyntaxError as e:
    print(f'XML invalid: {e}')
```

### HTTP 500 on a dataset change: Invalid column name

Happens when the new query references a column the underlying table/view doesn't have. The error message usually names the column. Check the underlying view/table schema, not just the report.

### HTTP 401 / 403

Authentication issue. Verify `HttpNegotiateAuth()` works with a simple metadata GET first. If that fails, the user's Windows credentials may not have permission on the Report Server.

## Fetching Metadata Fields

A GET on a CatalogItem returns these fields (as of SSRS 2019):

- `@odata.context`, `@odata.type`
- `Id`, `Name`, `Description`, `Path`, `Type`
- `Hidden`, `Size`
- `ModifiedBy`, `ModifiedDate`, `CreatedBy`, `CreatedDate`
- `ParentFolderId`, `ContentType`
- `Content` (base64-encoded RDL)
- `IsFavorite`, `Roles`
- `HasDataSources`, `HasSharedDataSets`, `HasParameters`

For a PUT, you need to send ALL of these back (minus `@odata.context`). The easiest way is to GET the current state, modify the fields you care about (usually just `Content`), and PUT the whole thing.

## Full Reference Implementation

Here's a complete migration function template that's been tested against the HFD SSRS environment:

```python
import base64
import datetime as dt
from pathlib import Path
import requests
from requests_negotiate_sspi import HttpNegotiateAuth
from lxml import etree

BASE = 'http://hfdsqlreport/reports/api/v2.0'
BACKUP_DIR = Path('./backups')


def process_report(item_id, modify_fn, apply=False):
    """Download, modify, optionally upload a report.

    modify_fn takes rdl_bytes and returns new_rdl_bytes.
    """
    auth = HttpNegotiateAuth()

    # Download
    r = requests.get(f'{BASE}/CatalogItems({item_id})/Content/$value', auth=auth, timeout=60)
    r.raise_for_status()
    content = r.content

    # Backup
    BACKUP_DIR.mkdir(exist_ok=True)
    ts = dt.datetime.now().strftime('%Y%m%d-%H%M%S')
    backup = BACKUP_DIR / f'{ts}-PRE-{item_id}.rdl'
    backup.write_bytes(content)
    print(f'Backup: {backup}')

    # Modify
    new_content = modify_fn(content)

    # Save modified version for review
    modified = BACKUP_DIR / f'MODIFIED-{item_id}.rdl'
    modified.write_bytes(new_content)

    # Validate XML
    body = new_content[3:] if new_content.startswith(b'\xef\xbb\xbf') else new_content
    try:
        etree.fromstring(body)
        print('XML validation: OK')
    except etree.XMLSyntaxError as e:
        print(f'XML INVALID: {e}')
        return False

    if not apply:
        print('Dry run - no upload')
        return True

    # Upload
    r = requests.get(f'{BASE}/CatalogItems({item_id})', auth=auth, timeout=15)
    r.raise_for_status()
    meta = r.json()
    meta.pop('@odata.context', None)
    meta['Content'] = base64.b64encode(new_content).decode('ascii')

    r = requests.put(f'{BASE}/CatalogItems({item_id})', auth=auth, json=meta, timeout=60)
    if r.status_code >= 400:
        print(f'Upload failed ({r.status_code}): {r.text[:2000]}')
        return False
    print(f'Upload: HTTP {r.status_code}')

    # Verify
    r = requests.get(f'{BASE}/CatalogItems({item_id})/Content/$value', auth=auth, timeout=30)
    if r.content == new_content:
        print('Verify: content matches')
    else:
        print(f'Verify: size mismatch (uploaded {len(new_content)}, retrieved {len(r.content)})')
    return True
```
