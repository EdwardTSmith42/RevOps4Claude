# Contract taxonomy - how to tell a bank-loan contract from a RIC

Canonical source: SharePoint > Legal > Shared Documents > **Agreement Templates > Provider Agreements**.

```
Provider Agreements/
├── SAO (Cash Up Front)/            <- funding type 10001
│   ├── Bank Loans Agreement/            BANK LOAN
│   ├── RICs/                            RIC only
│   ├── Combined Program Agreements/     BOTH
│   └── Archive/                         historical versions
├── OBS (Cash Over Time)/           <- funding type 10000
└── Network Partner Provider Agreements/  (Rectangle Health, Align)
```

The template folders tell you what HFD *issues*. Executed files are named differently - see "Executed file naming" below.

## Axis 1 - INSTRUMENT

Match case-insensitively, and allow spaces to be absent or replaced by underscores.

| Pattern in the name | Instrument | Notes |
|---|---|---|
| `Bank Loan Program Agreement ...` | **BANK LOAN** | Current naming, 2024 onward |
| `Bank Loan Program PROVIDER Agreement ...` | **BANK LOAN** | 2023-2024 naming; "Provider" was later dropped |
| `BankLoanProgramProviderAgreement_...` | **BANK LOAN** | Concatenated form, common on executed files in OneDrive |
| `BaaS Provider Agreement ...` | **BANK LOAN** | 2023-era name. BaaS = Banking as a Service = bank loan |
| `... _ Banking as a Service.pdf` | **BANK LOAN** | Executed-file form of the same thing |
| `Combined RIC and Bank Loan Program Agreement [...]` | **BOTH** | Switchable |
| `HFD - Merchant Servicing Agreement (RIC SAO ...)` | **RIC** | Half of the RIC pair |
| `Crosscheck - Merchant Purchase Agreement (RIC SAO ...)` | **RIC** | The other half. Crosscheck is the purchasing entity |
| `... _ RIC Agreement _ <date>.pdf` | **RIC** | Executed-file form |

**RIC is always a pair**: an HFD Merchant Servicing Agreement plus a Crosscheck Merchant Purchase Agreement. Seeing only one of them still means RIC.

A provider holding both RIC and bank-loan paper is **switchable** - the bank-loan agreement is what matters. Do not treat the presence of RIC paper as disqualifying.

## Axis 2 - ENTITY SCOPE

Read the `[bracketed]` token. Spacing and underscores vary; match on the word.

| Token | Scope | Effect |
|---|---|---|
| `[DSO_Management_Merchant]`, `[DSO Management Merchant]`, `[DSO_Management FINAL]`, `[DSO]` | **UMBRELLA** | Covers the group's locations indefinitely, if signed after April 2024 |
| `[Single Practice_Merchant]`, `[MedSpa Single Practice]`, `[Single Practice FINAL]` | **ONE ENTITY** | Siblings are NOT covered |
| `[MedSpa Multi-Practice]` | **MULTI-SITE** | Covers the listed practices |
| `[Single Align Foundational]` | **ONE ENTITY** | Align-specific combined variant |
| `[FINAL]` alone, or no bracket | **UNKNOWN** | Scope is not encoded. Fall through to content search |

**An umbrella can come from any location, not just the parent.** One location signing a DSO agreement covers its siblings. Do not assume the parent must be the signer.

## Noise to strip before matching

- Prefix `Merged from ...`
- Suffixes `-merged`, `.docx.pdf`, ` (1)`, `(Pre-Signed)`
- `(Align Pre-Signed)` - a pre-signed Align variant, still a real executed agreement

## Files that are NOT contracts

Exclude before classifying, or they pollute the result: Price Exhibit, BAA / BAA Agreement, Enrollment Form, SmartLinx Business Report, License / NPI / SOS / Secretary of State, Entity Info, W-9, Articles, Summary.pdf, Loyalty Opt-In, Pricing Amendment, `.url` shortcuts, anything under a `Due Diligence` subfolder.

## Executed file naming

Executed contracts do **not** follow template naming. Observed real forms:

- `Bank Loan Program Provider Agreement [Single Practice_Merchant] (Align Pre-Signed).docx.pdf`
- `BankLoanProgramProviderAgreement_Single Practice_Merchant__Align_Pre_Signed_10_25_2025.pdf`
- `Diverse Management LLC _ Banking as a Service.pdf`
- `Puppygram Com LLC (Puppygram) _ Servicing Agreement.pdf`
- `Merged from Bank Loan Program Agreement [DSO_Management_Merchant] Final (Pre-Signed) (10.20.25) (1).pdf`
- `Premier Dental Club PC.pdf` - **no type at all**
- `Francesca_Velasco_DDS_LLC_38332-_Please_Docu.pdf` - DocuSign artefact; note the provider id embedded in the name

The last two are why filename matching alone is not sufficient.

## When the filename carries no type

Two mechanisms, in order of cost.

**1. Full-text search (preferred - no need to open the file).** SharePoint indexes document content.

```
/sites/Legal/_api/search/query?querytext='<KQL>'&selectproperties='Path'
```

The KQL must be wrapped in single quotes inside the URL or the endpoint returns HTTP 500.

- Bank loan test: `"Bank Loan Program" AND path:"<provider folder URL>"`
- RIC test: `"Merchant Servicing Agreement"`, `"Crosscheck"`, `"Retail Installment"`

A hit on the RIC phrases with no hit on `"Bank Loan Program"` means RIC only.

Worked example: `Premier Dental Club PC.pdf` carries no type. Content matched *Merchant Servicing Agreement*, *Crosscheck* and *Retail Installment*, and did not match *Bank Loan Program*. Verdict: RIC, needs new paper.

**Limit:** search does not index the personal OneDrive. Control test - "Edge Dental Designs" returned zero search hits despite holding a real bank-loan agreement there. Never read a search miss as absence; enumerate OneDrive directly.

**2. Open the document and read the FOOTER.** Required for anything signed before 19 Nov 2024, when the contract type lived in the footer rather than the filename.

## Date boundaries

| Boundary | Effect |
|---|---|
| **19 Nov 2024** | On/after: type is in the FILE NAME. Before: type is in the document FOOTER |
| **April 2024** | DSO_Management template signed on/after this date grants umbrella coverage indefinitely, even years later. Before: each location needs its own contract or a Joinder |

Legal has confirmed non-DSOs may use the DSO form with no risk to HFD.

## Historical variants (Archive)

The Archive folders hold the version history and confirm the naming drift. Notable:

- `BaaS Provider Agreement [Draft] 7.24.23 ar_ws [NO BAA].docx` - the 2023 name for bank loan
- `Bank Loan Program Provider Agreement [FINAL].docx` - no scope token, so scope is unknowable from the name
- `Bank Loan Program Provider Agreement [DSO_Management FINAL] 06.24.24.docx`
- `Bank Loan Program Provider Agreement [Single Practice FINAL] v2_06.24.24.docx`
- `ChaseHealthAdvance-Vision(SP) Agreement.pdf` - a legacy acquired-portfolio agreement

Treat the Archive as the authority on what old names meant; expect more variants than this list and match on the instrument and scope *words* rather than on exact strings.
