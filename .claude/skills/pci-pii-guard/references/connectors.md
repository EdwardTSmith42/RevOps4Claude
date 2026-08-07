# Connector-Specific PCI/PII Guidance

---

## SQL Server

### Inline Query Masking (Preferred)
Always apply masking in the SELECT clause — never pull raw and mask in code.
See SKILL.md Step 2 for full templates.

### Dynamic Data Masking (DDM)
If the database has DDM enabled, masked users will automatically receive masked output.
However, DDM is a display-layer feature only — it does NOT encrypt at rest.
Never assume DDM is enabled; always apply query-level masking explicitly.

To check if DDM is active on a column:
```sql
SELECT c.name, c.is_masked, c.masking_function
FROM sys.masked_columns c
JOIN sys.tables t ON c.object_id = t.object_id
WHERE t.name = 'YourTable'
```

### Column-Level Encryption (Always Encrypted)
If Always Encrypted is configured, SQL Server handles encryption/decryption
transparently at the driver level. Claude still should NOT select raw sensitive
columns unnecessarily — treat Always Encrypted as a floor, not a ceiling.

### Row-Level Security
If RLS is configured, queries automatically filter to authorized rows.
Still apply column-level masking on top of RLS.

### Recommended Pattern for HFD SQL Server
Known sensitive tables/columns to treat with caution:
- Any table with `SSN`, `TaxID`, `DOB`, `AccountNumber`, `RoutingNumber` columns
- LedgerDetail: flag any payment account references
- DimProvider: flag NPI (National Provider Identifier) as quasi-identifier

---

## HubSpot (via MCP)

### Property Exclusion
When calling HubSpot's CRM search or get-contact endpoints via MCP, always
specify the `properties` array explicitly. Never use a wildcard fetch that returns
all properties.

Safe properties to include freely:
- `hs_object_id`, `id`, `createdate`, `lastmodifieddate`
- `lifecyclestage`, `hs_lead_status`, `dealstage`
- `company`, `jobtitle` (professional context)

Properties to exclude or handle carefully:
- Any custom property with `ssn`, `dob`, `tax`, `account`, `routing` in the name
- `date_of_birth` if populated
- Full mailing address combinations

### Surrogate Key
Always use `hs_object_id` (contact ID) or `deal_id` as the join/reference key.
Never use email or phone as a join key between systems.

### Sensitive Property Flag
If you discover a HubSpot property that appears to store PII unexpectedly
(e.g., a Notes field containing SSNs), flag it to the user immediately:
> "⚠️ I found what appears to be raw PII in HubSpot property `[name]`. This data
> should not be stored here unencrypted. Recommend reviewing HubSpot data hygiene."

---

## Tableau

### Live Connection Considerations
In live mode, Tableau passes queries directly to the source. Masking must happen
at the data source level (SQL view, calculated field, or DDM).

Recommend creating masked SQL views for any Tableau data source that touches
sensitive tables:
```sql
CREATE VIEW vw_BorrowerSafe AS
SELECT
    borrower_id,  -- surrogate key
    '***-**-' + RIGHT(CAST(ssn AS VARCHAR(11)), 4) AS ssn_masked,
    YEAR(date_of_birth) AS birth_year,
    city + ', ' + state AS location_display
    -- street_address intentionally omitted
FROM BorrowerTable
```

### Extract Considerations
Extracts snapshot data. If an extract is built on a query that includes raw PII,
that PII is stored in the .hyper file. Flag this to the user and recommend
rebuilding the extract from a masked view.

### Row-Level Security
For sensitive dashboards, confirm RLS is configured so users only see records
they're authorized for — masking alone is not sufficient if a user can see
someone else's (even masked) record.

---

## Generic REST APIs / MCP Connectors

### Request Design
- Use field selection parameters (`fields=`, `select=`, `properties=`) to request
  only what you need
- Review the API schema before calling to identify sensitive response fields
- If the API doesn't support field selection, note this as a data exposure risk

### Response Scrubbing
If a raw API response arrives in context with sensitive fields:
1. Do NOT display the raw response to the user
2. Extract only the non-sensitive fields you need
3. Replace sensitive values with `[REDACTED - PCI]` or `[REDACTED - PII]` in your output
4. Note what was redacted: "Response contained `account_number` — field redacted per PII policy."

### Webhook / Event Payloads
If processing webhook data (e.g., from HubSpot, payment processors), apply
the same redaction rules before logging or displaying payload contents.

---

## General API Authentication & Credentials

Credentials (API keys, tokens, passwords) are treated as PCI-equivalent:
- Never display a full API key, even if the user provides it
- Mask as: `sk-...` + last 4 chars, e.g., `sk-...ab3f`
- Never include credentials in query strings (URL parameter exposure)
- Never echo credentials back in responses or summaries
