---
name: npi-lookup
description: >
  On-demand NPI (National Provider Identifier) registry lookup with confidence scoring.
  Use this skill whenever someone asks to find, verify, or check an NPI number for a healthcare
  provider or organization — including dentists, physicians, specialists, clinics, or any medical/dental
  practice. Trigger on phrases like "look up NPI", "find NPI", "check NPI", "what is the NPI for",
  "verify provider credentials", "run an NPI check", "NPI for this practice/doctor/provider", or
  any due diligence credentialing task involving a healthcare entity. Also trigger when a HubSpot
  due diligence ticket URL is provided in the context of healthcare credentialing. Always use this
  skill rather than attempting an ad-hoc NPI search — it encodes the correct tooling, signal
  priority logic, and output format for high-accuracy results.
---

# NPI Lookup — Credentialing Verification Skill

This skill performs accurate, auditable NPI registry lookups for healthcare providers and organizations. It is designed for compliance-sensitive workflows where false positives are unacceptable.

**Prime directive: Never return an incorrect NPI match. A confident wrong answer is worse than an honest "not found."**

---

## Input Signals

Collect as many of these as available before searching. More signals = better disambiguation.

| Signal | Weight | Notes |
|---|---|---|
| State license number | Dispositive | Exact match in registry = conclusive for NPI-1 |
| Practice address (street + city + ZIP) | Dispositive | Exact match in registry = conclusive for NPI-2 |
| Provider first + last name | High | Required for Step 1 search |
| Organization / DBA name | High | Required for Step 2 search |
| State | Required | Used in all searches as a filter |
| Specialty / credential | Supporting | Helps eliminate wrong-name candidates |
| Authorized official name on org | Supporting | Corroborates NPI-2 ownership |

If the user has not provided a state, ask before searching — it dramatically reduces false positives.

---

## Technical Requirement — API Tool

**Always use `mcp__Windows-MCP__PowerShell` with `Invoke-RestMethod` for all NPI API calls.**

Do NOT use the bash sandbox (`mcp__workspace__bash`) — its proxy blocks `npiregistry.cms.hhs.gov`.

Base URL: `https://npiregistry.cms.hhs.gov/api/`
Always include: `version=2.1`

Batch all search steps into a single PowerShell block:

```powershell
$step1 = Invoke-RestMethod "https://npiregistry.cms.hhs.gov/api/?version=2.1&first_name=FIRST&last_name=LAST&state=ST&limit=10"
$step2 = Invoke-RestMethod "https://npiregistry.cms.hhs.gov/api/?version=2.1&organization_name=ORG+NAME&state=ST&limit=10"
Write-Host "=== Step 1 ===" ; $step1 | ConvertTo-Json -Depth 10
Write-Host "=== Step 2 ===" ; $step2 | ConvertTo-Json -Depth 10
```

Encoding note: The `&` character in org names must be encoded as `%26` in the URL.
Example: `Smith & Patel Dental` -> `Smith+%26+Patel+Dental`

---

## Identity Normalization

Before building search URLs, normalize input values:

**Person names:** Remove credential suffixes (DMD, MD, DDS, NP, Jr, Sr). Normalize hyphens (Anne-Marie -> Anne Marie). Try nickname expansions if first search fails (Mike -> Michael, Bob -> Robert).

**Organization names:** Strip legal suffixes (LLC, PLLC, Inc, Corp, PA, PC). Normalize & <-> and. Remove punctuation. If the org name contains `&`, run two searches: one with `%26` and one with `+and+`.

---

## Progressive Search Steps

Run Steps 1 and 2 in the same PowerShell call. Only go deeper if needed.

**Step 1 — Individual Provider/Owner**
```
?version=2.1&first_name=X&last_name=Y&state=Z&limit=10
```
Look for: license number match in `taxonomies[].license`, specialty alignment, sole_proprietor flag.

**Step 2 — Organization / DBA Name**
```
?version=2.1&organization_name=NAME&state=Z&limit=10
```
Look for: exact address match, `authorized_official` name matching the known owner.

**Step 3 — Legal entity name** (only if Step 2 found nothing and legal name differs from DBA)

**Step 4 — Reduced/variant searches** (last resort only — flag for human review, never auto-confirm)

---

## Key Response Fields to Check

- `results[].number` — the NPI
- `results[].enumeration_type` — `NPI-1` (individual) or `NPI-2` (organization)
- `results[].basic.status` — must be `A` (Active)
- `results[].taxonomies[].license` — state license number (compare to ticket)
- `results[].taxonomies[].desc` — specialty description
- `results[].addresses[].address_purpose` — `LOCATION` vs `MAILING`
- `results[].basic.sole_proprietor` — YES/NO
- `results[].basic.authorized_official_first_name` / `_last_name` — NPI-2 owner

---

## Candidate Evaluation Logic

For each result, evaluate:

1. Does the license number match exactly? -> Dispositive yes for NPI-1.
2. Does the practice address match exactly? -> Dispositive yes for NPI-2.
3. Does the specialty align? (dental license + Periodontics taxonomy = match; dental license + Behavior Technician = eliminate)
4. Does the state match?
5. Does the authorized official name match the known owner?

Immediately eliminate candidates with:
- Wrong specialty
- Wrong state
- No license number when one is known
- Credential type mismatch (NP != DMD)

**Address note:** An NPI-1 mailing address that differs from the practice city is NOT a contradiction. Solo practitioners commonly use a personal mailing address. Only the practice `LOCATION` address matters for corroboration.

---

## Dual NPI Pattern — Sole Proprietorships

When entity type is sole proprietorship, always search for and report **both**:

- **NPI-1** (individual): the licensed provider — for individual provider credentialing
- **NPI-2** (organization): the practice entity — for practice-level / billing credentialing

The NPI-1 license number and the NPI-2 practice address are typically the two dispositive signals.

---

## Confidence Levels

| Level | Criteria | Recommendation |
|---|---|---|
| **High** | Exact license match (NPI-1) OR exact address match (NPI-2) + no contradictions | Safe to operationalize |
| **Medium** | Strong name + state + specialty overlap, no contradictions, but no uniquely identifying signal | Human review recommended |
| **Low** | Sparse evidence, multiple plausible candidates remain | Do not operationalize |
| **No match** | No reliable result found | State explicitly — never fabricate |

---

## Output Format

Always return results in this structure:

```
## NPI Lookup — [Provider / Org Name]

### Identity Signals Used
- Provider: [name, credential]
- Organization: [DBA / legal name]
- State: [XX]
- License: [number]
- Address: [if provided]

---

### Search Attempts
1. [Step description] -> [N results]
2. ...

---

### Candidate Evaluation

#### [NPI Type] — [Name]
- NPI: [number]
- Type: NPI-1 / NPI-2
- Status: Active / Inactive
- Supporting Evidence: [list corroborating signals]
- Contradictory Evidence: [list issues, or "None"]

#### [Eliminated candidates — brief reason why]

---

### Final Determination

| | Individual Provider | Practice Organization |
|---|---|---|
| NPI | [number] | [number] |
| Type | NPI-1 | NPI-2 |
| Status | Active | Active |
| Confidence | High / Medium / Low | High / Medium / Low |

Recommendation: [operationalize / human review / do not use]

---

### Notes
[Discrepancies, missing data, anything a reviewer should know]
```

If no match is found, state clearly:
"No reliable NPI match could be confirmed with sufficient confidence." and explain why.

---

## PCI/PII Handling

- Never display Tax ID / EIN — redact as `[REDACTED — PCI/PII Guard]`
- Phone numbers and personal emails from tickets are not needed for NPI lookup — exclude from outputs
- Provider names and organization names are necessary and may appear in results
