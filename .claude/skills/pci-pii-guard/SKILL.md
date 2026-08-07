---
name: pci-pii-guard
description: >
  Protects PCI and PII data when querying or retrieving data via MCP connectors,
  databases, CRMs, BI tools, or any API. Use this skill whenever Claude is about
  to write a SQL query, HubSpot API call, REST request, or any MCP-based data
  retrieval that might touch sensitive fields — even if the user hasn't explicitly
  asked for protection. Sensitive field patterns include SSN, DOB, card numbers,
  bank/routing numbers, account numbers, names, and addresses. Claude MUST consult
  this skill before writing any query or API call against a database, CRM, or
  external data source — do not skip this even for "quick" or "simple" lookups.
---

# PCI/PII Guard

Protect PCI and PII data at the query and API level — before sensitive values ever
reach Claude's context window or the user's screen.

## Core Principle

**Sensitive data must be masked, hashed, or excluded at the source.**  
Never SELECT a raw sensitive field. Never display one. Never join on one.

The protection hierarchy, in order of preference:
1. **Exclude** — omit the field entirely if not needed
2. **Mask at source** — wrap in a masking/hashing function in the query itself
3. **Surrogate key** — use a non-sensitive ID (loan ID, borrower ID, contact ID) for joins
4. **Hash for joins** — if no surrogate exists, hash both sides consistently and join on the hash

---

## Step 1: Scan Before You Query

Before writing any query or API call, scan the requested fields and the likely
schema for sensitive patterns. Consult `references/field-patterns.md` for the full
list of sensitive field name patterns.

**Quick reference — always treat these as sensitive:**

| Category | Field name signals |
|----------|--------------------|
| SSN / Tax ID | `ssn`, `social_security`, `tax_id`, `sin`, `itin`, `ein` |
| Date of Birth | `dob`, `date_of_birth`, `birth_date`, `birthdate` |
| Name | `full_name`, `first_name` + `last_name` together, `legal_name` |
| Address | `address`, `street`, `city` + `state` + `zip` together |
| Card / PCI | `card_number`, `cc_num`, `pan`, `cvv`, `cvc`, `expiry`, `card_holder` |
| Bank / Account | `account_number`, `routing_number`, `bank_account`, `iban`, `aba` |
| Contact | `phone`, `mobile`, `email` (flag but context-dependent) |

**Decision tree:**
- Field needed for display? → Mask at source (see Step 2)
- Field needed for a join? → Use surrogate key or hash (see Step 3)
- Field not needed at all? → Exclude from SELECT / API fields list

---

## Step 2: Mask at Source

### SQL Server

Apply masking inline in the query. Do not pull the raw value and mask in application logic.

**SSN** — show last 4 only:
```sql
'***-**-' + RIGHT(CAST(ssn AS VARCHAR(11)), 4) AS ssn_masked
```

**Date of Birth** — year only:
```sql
YEAR(date_of_birth) AS birth_year
```

**Card Number (PAN)** — last 4 only:
```sql
'************' + RIGHT(CAST(card_number AS VARCHAR(20)), 4) AS card_masked
```

**Account / Routing Number** — fully redacted:
```sql
'[REDACTED]' AS account_number
```

**Full Name** — first initial + last name:
```sql
LEFT(first_name, 1) + '. ' + last_name AS name_display
```

**Address** — city/state only, suppress street:
```sql
city + ', ' + state AS location_display
-- omit street_address entirely
```

**Hashing for reference/audit (not for display):**
```sql
CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', UPPER(LTRIM(RTRIM(ssn)))), 2) AS ssn_hash
```

### HubSpot (via MCP)

When fetching contact or deal properties, explicitly exclude sensitive fields from
the `properties` parameter. Use contact/deal ID as the surrogate key.

```
properties: [id, hs_object_id, createdate, ...]
-- Never include: ssn, tax_id, date_of_birth, full_address, bank_account
```

If a sensitive property must be referenced, note it in your response as `[FIELD EXCLUDED - PII]`
and explain to the user what was omitted and why.

### REST APIs / Generic MCP Connectors

- Request only the fields you need (principle of minimum data exposure)
- If the API returns a full record with sensitive fields, redact before displaying:
  replace raw values with `[REDACTED - PCI]` or `[REDACTED - PII]` in your response
- Never log, echo, or summarize raw sensitive values

---

## Step 3: Surrogate Keys for Joins

**Always prefer a non-sensitive surrogate key.** Common patterns in financial/healthcare systems:

| Instead of joining on... | Use... |
|--------------------------|--------|
| SSN | borrower_id, loan_id, patient_id, applicant_id |
| Account number | account_id, ledger_id |
| Card number | token_id, payment_method_id |
| Email | contact_id, hs_object_id (HubSpot) |

**If no surrogate key exists**, create a consistent hash on both sides:
```sql
-- Table A
CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', UPPER(LTRIM(RTRIM(a.ssn)))), 2) AS join_key

-- Table B  
CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', UPPER(LTRIM(RTRIM(b.ssn)))), 2) AS join_key

-- Join
ON a.join_key = b.join_key
```

This lets you join without either side ever exposing the raw SSN in the result set.

---

## Step 4: Response Rules

Even after masking at source, apply these rules to every response:

1. **Never display** a value that looks like a raw SSN, card number, bank account,
   or routing number — even if the user provided it in their message
2. **Flag omissions** — tell the user which sensitive fields were excluded and why,
   so they know the query is purposefully limited
3. **Confirm masking** — when returning query results or previewing data, note:
   *"Sensitive fields (SSN, DOB) are masked at source per PCI/PII guard policy."*
4. **No raw values in explanations** — don't use real-looking example values
   (e.g., `123-45-6789`) even as placeholders; use `XXX-XX-XXXX` instead

---

## Step 5: When You're Uncertain

If you encounter a field name you don't recognize and it *might* be sensitive:
- **Assume sensitive** until proven otherwise
- Ask the user: *"The field `[field_name]` may contain sensitive data. Should I mask it,
  exclude it, or do you know it's safe to display?"*
- Default to exclusion while waiting for confirmation

---

## Connector-Specific Notes

Read `references/connectors.md` for platform-specific guidance on:
- SQL Server (Dynamic Data Masking, column-level encryption)
- HubSpot (property field exclusion, sensitive property flags)
- Tableau (live vs. extract considerations, row-level security)
- Generic REST/MCP (field filtering, response scrubbing)

---

## What This Skill Cannot Do

Be transparent with the user about scope:
- This skill controls **how Claude queries and displays data** — it does not encrypt
  data in the underlying system or in transit between the MCP server and Claude
- Infrastructure-level protections (TLS, column encryption, DDM, tokenization vaults)
  must be implemented at the database/platform level
- If a system returns sensitive data with no way to mask at source, Claude will redact
  in the response and flag the gap to the user for remediation
