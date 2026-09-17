# Lookup paths - where the evidence lives and how to read it

Everything here works without database access. SQL is an optional accelerator, never a requirement.

## Repository 1 - Legal contract library

```
https://healthcarefinancedirect.sharepoint.com/sites/Legal/Shared Documents/Provider and Merchant Contracts/
```

**The folder was renamed.** The Contract Requirements SOP links to `Provider Contracts`, which 404s. The current name is `Provider and Merchant Contracts`.

Structure: A-Z letter folders by first letter of Legal Name (~3,600 provider folders), plus `_#`, `.Folder Structure Template` and `_Contracting Status Log.xlsx`.

Each provider folder holds five subfolders. Only one matters:

```
<Legal Name> dba <Practice Name>/
├── Contracts Executed/     <- the only folder that is evidence
├── Due Diligence/
├── Correspondence/
├── Working Files/
└── Other/
```

Multi-location entities may also have `_Individual Locations/` containing per-location folders with the same five-folder shape.

Two quirks: `.Folder Structure Template` contains real provider folders as well as the template, and per-location folders are frequently empty even when the parent holds the contract.

### Enumerating it

The document-library web part often renders blank in an automated browser. Use the REST API instead - it is reliable and fast.

```js
const B = 'https://healthcarefinancedirect.sharepoint.com/sites/Legal/_api/web/GetFolderByServerRelativeUrl(';
const H = { headers: { 'Accept': 'application/json;odata=nometadata' } };

async function ls(serverRelativePath) {
  const e = "'" + encodeURIComponent(serverRelativePath).replace(/'/g, "''") + "'";
  const folders = await fetch(B + e + ')/Folders?$select=Name&$top=2000', H).then(r => r.json());
  const files   = await fetch(B + e + ')/Files?$select=Name,TimeLastModified', H).then(r => r.json());
  return { folders: folders.value.map(x => x.Name), files: files.value.map(x => x.Name) };
}
```

Build the full A-Z index once (26 parallel calls), then match locally. That is both faster than per-provider search and immune to the "filed under the other letter" problem.

### Full-text search

```
/sites/Legal/_api/search/query?querytext='<KQL>'&rowlimit=6&selectproperties='Path,FileName'&trimduplicates=false
```

The KQL **must** be wrapped in single quotes inside the URL, or you get HTTP 500. Scope with `path:"<folder URL>"`. Covers SharePoint sites only - **not** the personal OneDrive.

Hits under `/sites/Compliance/...` or `/sites/HFDFraudCases/...` are case copies, not a contract repository. Ignore them as sources of truth.

## Repository 2 - a `Provider Contracts` folder on an individual's OneDrive

**This is a personal drive, not an org system. Never hardcode the owner, the path, or the drive id.**

Known copy as of September 2026: **Ed Smith (esmith@gohfd.com)**, `OneDrive > Provider Contracts` — a flat list of ~1,370 provider folders named by Legal Name, each holding contract files directly (sometimes one subfolder deep). **This is where recent contracts live while Legal's library catches up.**

Another operator will hit one of three situations. Establish which before relying on anything here:

| Situation | What to do |
|---|---|
| You own the folder | Resolve your own drive id (below) and enumerate |
| It is shared with you | Find it under OneDrive > Shared, or add a shortcut to your own OneDrive, then resolve the drive id of the **owner's** drive |
| No access | Report it. Mark unsettled rows `VERIFY` with reason "second contract repository not accessible". Never downgrade them to `NEEDS_NEW_CONTRACT` |

### Resolving the drive id - do not reuse someone else's

The personal-site `_api/web` and `_api/v2.0/drive` endpoints return 403. The drive-id form works, but the id is specific to one person's drive.

Get the id for whichever drive you actually have access to:

```js
// Option A - from any sharing link to a file in that drive
const shareId = 'u!' + btoa('<share URL>').replace(/=+$/,'').replace(/\//g,'_').replace(/\+/g,'-');
const item = await fetch('/_api/v2.0/shares/' + shareId + '/driveItem',
  { headers: { Accept: 'application/json' } }).then(r => r.json());
const D = item.parentReference.driveId;      // <- the drive id

// Option B - your own drive, from a tab on the -my.sharepoint.com origin
// browse to the folder in the OneDrive UI and read the driveId out of a network call,
// or use Option A against any sharing link you hold.
```

Then enumerate:

```js
const H = { headers: { 'Accept': 'application/json' } };
await fetch('/_api/v2.0/drives/' + D + '/root:/Provider Contracts:/children?$select=name,folder&$top=999', H);
// follow @odata.nextLink to page beyond 999
```

Run it from a tab already on the `-my.sharepoint.com` origin so the fetch is same-origin. If the folder sits at a different path under that drive, adjust the `root:/<path>:` segment — the folder name is a convention, not a guarantee.

**Standing risk:** a contract repository on one person's personal drive means coverage varies by operator and disappears if that person leaves. Flag it when it affects a result; the durable fix is relocating the content to the Legal library or a shared SharePoint site.

### Reading an .xlsx from SharePoint without a workbook API

The Excel workbook endpoints are not exposed on this tenant. Fetch the bytes and unzip in the browser - xlsx is a ZIP, and `DecompressionStream('deflate-raw')` is native:

1. `GET /_api/v2.0/shares/u!<base64url of share URL>/driveItem/content` -> ArrayBuffer
2. Parse the ZIP central directory, inflate `xl/worksheets/sheet1.xml` and `xl/sharedStrings.xml`
3. Read `<row>` elements; `hidden="1"` marks rows filtered out of the user's view - honour it, because the visible set is usually the intended working list

## Repository 3 - HubSpot (identity only)

Object: **COMPANY** (`0-2`). Join key: `provider_unique_key` (label "Provider ID") - the ELI provider id, populated on 22,317 records.

| Property | Use |
|---|---|
| `legal_business_name` | **The Legal Name.** What contract folders are filed by |
| `provider_name` | DB `providername` |
| `doing_business_as` | DB `PracticeName`, the DBA |
| `parent_provider` | Parent provider id, `"0"` when none |
| `ric_baas` | Current configuration - **NOT contract evidence** |
| `entity_type` | LLC / PC / PLLC etc. |
| `authorized_signer` | Who signs |

Traps: `company_id` holds a city name, not an id - never join on it. `practice_name` is a separate unreliable field that disagrees with `doing_business_as` on real records - use `doing_business_as`.

**HubSpot holds no usable contract-instance data.** The DocuSign/"Glue" property set exists but is 100% empty. Deal-level "HFD Servicing Agreement - Signed" covers 15 records out of 22k. Note attachments are bare file ids with no filename and no fetch tool. Use HubSpot for identity, never for which paper was signed.

Note: the description on `legal_business_name` reads "Also known as Provider Name in the ELI system", which contradicts the actual field mapping and is worth correcting at source.

## Repository 4 - Tableau (hierarchy and instrument)

Primary datasource: **`v.HfdV3`**, LUID `583b19c2-c2ac-4aa4-a207-4714da9a0262`. Use `query-datasource`.

| Need | Field caption |
|---|---|
| Provider id | `Provider Unique Key` |
| Names | `Provider Name`, `Provider Practice Name`, `Parent Name`, `Parent Practice Name` |
| Hierarchy | `Provider Parent Key`, `Provider Is Parent`, `flag_Is DSO`, `DSO Type` |
| Instrument | `Provider Financial Instrument`, `Parent Financial Instrument` |
| Funding type | `Provider Funding Type`, `Provider Funding Type Description` |
| Status | `Provider Status`, `Provider Is Active`, `Provider Activated On` |

Alternative: `HFD V.2`, LUID `9cffc20f-2e85-475e-a24d-2687cc566ace` (note its caption typo `Provider Funding Type Desciption`).

Traps:

- **No `legalname` in any Tableau datasource.** Verified by grepping the full metadata of both. `Provider Name` is a proxy that degrades to the trade name. Use HubSpot.
- `Provider Financial Instrument` is NULL for ~10,358 providers, so a RIC filter silently drops them. Pair it with funding type.
- `Provider Company Id` is a branch label (`Houston`, `Tempe`), not an id.
- **Hybrid is not an instrument.** It is funding type `10002`, orthogonal to RIC/BankLoan.
- `Provider Status` and `Provider Is Active` disagree on ~700 records. Return both.

Funding type codes: `10000` OBS (Cash Over Time), `10001` SAO (Cash Up Front), `10002` Hybrid.

## Matching algorithm

This is the part that gets answers wrong. Follow it exactly.

1. Build the candidate set from **all** tiers, as a union - exact legal name, legal-name substring, exact practice name, practice-name substring. Record which tier produced each hit.
2. Fetch `Contracts Executed` for **every** candidate separately. Never flatten before fetching.
3. Prefer candidates that actually hold documents over better-named empty ones.
4. If several candidates hold documents, decide whether they are the same company (union the evidence) or different companies sharing a name (flag, do not merge).
5. Emit a match-quality field on every row: exact-legal / legal-substring / practice-only / ambiguous / none.

Failure modes this prevents, all observed in production data:

- Exact-match-first picked `S/Sono Bello` (empty) over `B/Body Contour Centers, LLC dba Sono Bello` (holds the bank-loan agreement)
- Token-subset matching attributed another provider's RIC documents to `Dentistry by Design` and `Petland Corporate`
- `Preferred Dental PC` matched `Preferred Dental Care`, a different provider holding no contract
