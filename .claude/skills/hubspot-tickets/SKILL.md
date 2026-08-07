---
name: hubspot-tickets
description: Create or update HubSpot tickets for HFD's RevOps and Analytics intake. Use when the user asks to file, create, raise, log, or open a ticket in HubSpot, especially for RevOps, Analytics & Data Requests, or any finance-reporting or data-quality issue. Captures pipeline IDs, stage IDs, RevOps ticket types, analytics subtypes, the full intake-field checklist, contact-association practice, and the plain-text-only content rule.
---

# HubSpot tickets (HFD RevOps / Analytics intake)

How to file a HubSpot ticket the way HFD's RevOps and Analytics team expects it. The MCP tools live behind the `mcp__834fdc2a-10f9-4b3b-bc2e-646b63d46c10__*` server. Use `manage_crm_objects` to create or update, `search_crm_objects` to find records, `get_properties` / `search_properties` to discover field options.

## Hard rules

1. **Ticket `content` is plain text. No HTML.** HubSpot renders the raw HTML tags inside the ticket body so `<p>`, `<strong>`, `<code>`, `<ol>`, `<li>` show up as literal source. Use newlines (`\n`) and blank lines for structure. Headings can be a single line followed by a blank line.
2. **Always associate at least one contact.** Tickets created via the MCP do not auto-create a conversation thread, so they don't appear in the helpdesk inbox feed. Associating the requesting person as a contact makes the ticket visible on that person's contact record and easier to find. If conversation-feed visibility is required, ask the user to email the helpdesk inbox instead of filing through the API.
3. **Ed has standing authorization for routine HubSpot writes. No per-action confirmation needed.** Ed said (2026-08-06): good to update HubSpot without asking, and he will give feedback if a specific change was unwanted. So for creating or updating tickets, notes, properties, stages, and associations, call `manage_crm_objects` with `confirmationStatus: "CONFIRMED"` directly and briefly state what you changed afterward. You do not need to present an approval table first. Exception: still confirm before HubSpot actions that reach outside the CRM record set, namely sending email or marketing to contacts, publishing public content (landing pages, blog), or creating or modifying workflows and other standing automation. See the `feedback_hubspot_update_without_confirmation` memory.
4. **Respect the style guide.** No em-dashes, no exclamation points, no fluff words. Keep the body factual.

## Field checklist for RevOps Analytics tickets

Always fill all of these. If a value isn't obvious, ask the user once with `AskUserQuestion` rather than guessing silently.

| Field | API name | Type | Notes |
|---|---|---|---|
| Subject | `subject` | text | One-line description. Lead with the system + symptom (e.g. "HybridHurdlePerformance returns 18 cohorts with ProviderID = 0"). |
| Body | `content` | text | Plain text only. Use the body template below. |
| Pipeline | `hs_pipeline` | enum | `118851585` (RevOps) for analytics work tickets. See pipeline table. |
| Stage | `hs_pipeline_stage` | enum | `210361775` (Backlog) for new intake. |
| RevOps Ticket Type | `revops_ticket_type` | enum | `Analytics` (label "Analytics & Data Requests") for analytics requests. |
| Analytics Subtype | `analytics_request_subtype` | enum | See subtype table. Active property is `analytics_request_subtype`, NOT `analytics__data_request_subtype`. |
| Priority | `hs_ticket_priority` | enum | `LOW` / `MEDIUM` / `HIGH` / `URGENT`. |
| Owner | `hubspot_owner_id` | id | Usually set to the requester's owner ID. Look up via `get_user_details`. |
| Requesting Business Function | `requesting_business_function` | enum | See enum list. No "Analytics" option exists; pick the function the issue belongs to (Financial Operations, Capital Solutions and Specialty Finance, Borrowing Bases, etc.). |
| The why | `the_why_business_need_and_dependencies` | text | Business need, downstream impact, and dependencies. State revenue / reporting impact here if relevant. |
| Existing Process | `existing_process` | enum | `Manual` or `N/A` (label "Does not exist"). For bug fixes where analysts are working around the defect today, use `Manual`. |
| Hours Saved | `hours_saved` | number | Hours per month saved by completing this request. Estimate conservatively. |
| Automates manual process | `automation` | enum | `Yes` / `No`. Bug fixes are `No`; new tooling that replaces a manual process is `Yes`. |
| Complexity | `complexity` | enum | `Low` / `Medium` / `Hard`. |
| Needs Peer Review | `criticalityneeds_peer_review` | enum | `true` (Yes) / `false` (No). Default `true` for anything touching finance views or revenue reporting. |
| Contact association | `associations` | list | Always associate the requester. Edward Smith = contact `35832151446`. |

## Pipeline IDs

| Pipeline | ID | Use |
|---|---|---|
| RevOps | `118851585` | Default for RevOps Analytics & Data Request work tickets. |
| Analytics Sprints | `890861150` | Holds one ticket per sprint (sprint containers). Do NOT file work tickets here. Daily workflow tags RevOps tickets into the active sprint automatically. |
| Support Pipeline | `0` | Customer support tickets. |
| Provider Support Pipeline | `89745996` | Provider-side support. |
| SAO FinOps | `114623645` | Finance operations. |
| Disputes Pipeline | `26466881` | |
| Payment Ops | `136055355` | |
| Investor Relations | `720627732` | |
| Integration Support | `729242140` | |
| Credit and Risk | `835617071` | |
| Due Diligence | `859620878` | |
| Portfolio Administration | `875075362` | |
| Sales Enablement | `884651821` | |
| Shipments | `888530948` | |

## RevOps pipeline stages (id `118851585`)

| Stage | ID |
|---|---|
| Backlog | `210361775` |
| Ready for Work | `1219677030` |
| In Progress | `210361861` |
| Waiting on Stakeholder | `1295464463` |
| Needs More Information | `210361862` |
| Peer Review | `1295464464` |
| Blocked | `264264586` |
| Waiting on Due Diligence | `1356914212` |
| Stakeholder Review | `955164805` |
| Closed as Resolved | `210361778` |
| Closed as Unresolved | `213866243` |
| Closed as Duplicate | `1340014636` |
| Closed: Sent to Business Development | `228305758` |
| Closed: Transferred to Provider Support | `228305759` |
| Closed: Transferred to Finops | `228305760` |
| Closed: Transferred to Customer Success | `228690336` |
| Moved to ClickUp | `1048469353` |

`Backlog` (`210361775`) is excluded from sprint scope by the daily Action A workflow. New intake still lands there; tickets get promoted to `Ready for Work` once triaged.

## RevOps Ticket Type values (`revops_ticket_type`)

The full enum is long; values most commonly used for Analytics tickets:

| API value | Label |
|---|---|
| `Analytics` | Analytics & Data Requests |
| `Marketing: Analytics Request` | Marketing: Analytics Request |
| `Reporting: New Request` | Reporting: New Request |
| `Reporting: Modify Existing Report` | Reporting: Modify Existing Report |
| `Reporting Issues` | Reporting Issues |
| `Data Sync: New Setup` | Data Sync: New Setup |
| `Data Sync: Troubleshooting` | Data Sync: Troubleshooting |
| `Data Migration: System Transfer` | Data Migration: System Transfer |
| `Data Hygiene: Ops Cleansing` | Data Hygiene: Ops Cleansing |
| `Due Diligence` | Due Diligence |

If unsure, default to `Analytics` for any analytics-team request.

## Analytics Request Subtype values (`analytics_request_subtype`)

| Value |
|---|
| `Reporting: New Report Development` |
| `Reporting: Modify Existing Report` |
| `Reporting: Data Mismatch or Error Resolution` |
| `Data Update Request` |
| `Data Sync: New Setup` |
| `Data Sync: Troubleshooting` |

`Reporting: Data Mismatch or Error Resolution` is the right subtype for any data-quality / data-correctness defect (wrong values, missing rows, mis-aggregated cohorts, etc.).

## Requesting Business Function values (`requesting_business_function`)

`Borrowing Bases`, `Capital Solutions and Specialty Finance`, `Customer Care`, `Enterprise Sales Enablement`, `Financial Operations`, `Marketing`, `Payment Operations`, `Product`, `Provider Support`, `Sales`, `Servicing`, `Other`.

No "Analytics" option. For finance-data defects, `Financial Operations` is usually the right call; for hybrid hurdle / investor-cohort work, `Capital Solutions and Specialty Finance` is also defensible.

## Body template (plain text)

```
Issue
One paragraph: the symptom, where it shows up, why it matters.

Root cause
What you found and the mechanism. Reference table/view/file names with backticks (literal backticks render fine in plain text; they just look like backticks).

Effects
Numbered list with plain "1." / "2." prefixes. No <ol>/<li>.

Likely trigger
The change that introduced the issue, if known. Cite PBI / PR / commit / date.

Affected data
Counts, date ranges, affected entities.

Suggested fix
What you'd change, in concrete terms.

Reproduce
A query or steps the reviewer can run.
```

Separate sections with a single blank line. No headings markup, no bold, no HTML.

## Creation flow

1. Gather context. Run the diagnostic queries you need to root-cause the issue before writing the ticket. The ticket should explain the mechanism, not just the symptom.
2. Look up enums you're unsure of. `get_properties` on the TICKET object with the property name returns the option list.
3. Look up the requester's contact ID. `search_crm_objects` on CONTACT with their email.
4. Draft all fields and the body. Per Ed's standing authorization (hard rule 3) you can proceed without an approval table; a one-line summary of what you are filing is courteous but optional.
5. Call `manage_crm_objects` with `confirmationStatus: "CONFIRMED"`, a `createRequest`, and an `associations` entry pointing at the contact.
6. Return the ticket URL: `https://app.hubspot.com/contacts/2520274/record/0-5/{id}`.

## Update / fix flow

Same shape as create, but with `updateRequest` and an `objectId`. Common fixes:

- Content was created with HTML. Pull the ticket with `get_crm_objects`, send a plain-text replacement via `manage_crm_objects` updateRequest with `content`.
- Missing associations. Send an updateRequest with only `associations` (leave `properties` empty).
- Wrong stage. Send `hs_pipeline_stage` with the new ID.

## Known pitfalls

- **HTML in `content`.** Renders as literal source. Always plain text.
- **No conversation thread.** API-created tickets don't appear in the helpdesk inbox feed. Associating a contact makes the ticket discoverable from the contact record; for inbox visibility, the ticket has to originate from an email to a helpdesk address.
- **Two analytics subtype properties exist.** `analytics_request_subtype` is the active one. `analytics__data_request_subtype` exists with identical options but is not populated on recent tickets. Use the single-underscore name.
- **`analytics_request_subtype` is not the same as `revops_ticket_type`.** Both fields exist and both should be set on an Analytics ticket. The ticket type is the broad category; the subtype narrows it.
- **`hs_ticket_priority` values are uppercase.** `LOW` / `MEDIUM` / `HIGH` / `URGENT`, not `Low`/`Medium`/etc.
- **Enum-typed property values are case-sensitive.** Send the exact `value` from `get_properties`, not the `label`.
- **`criticalityneeds_peer_review`** takes string `"true"` / `"false"`, not booleans.
- **Don't paste sensitive data into the body.** Mask SSN, account numbers, card numbers, etc. before they reach the ticket content. See the `pci-pii-guard` skill.

## Quick reference: the canonical RevOps Analytics ticket

```
objectType: tickets
properties:
  subject:                                <one-line summary>
  content:                                <plain-text body, no HTML>
  hs_pipeline:                            "118851585"           # RevOps
  hs_pipeline_stage:                      "210361775"           # Backlog
  revops_ticket_type:                     "Analytics"           # Analytics & Data Requests
  analytics_request_subtype:              "<subtype value>"
  hs_ticket_priority:                     "MEDIUM"              # uppercase
  hubspot_owner_id:                       "<requester owner id>"
  requesting_business_function:           "<function>"
  the_why_business_need_and_dependencies: "<business need + impact>"
  existing_process:                       "Manual" | "N/A"
  hours_saved:                            "<number>"
  automation:                             "Yes" | "No"
  complexity:                             "Low" | "Medium" | "Hard"
  criticalityneeds_peer_review:           "true" | "false"
associations:
  - targetObjectId:   <contact id>
    targetObjectType: contacts
```

## Edward's working context

- Owner ID: `794791307`
- Contact ID: `35832151446`
- Email: `esmith@gohfd.com`
- Default requester to associate when Edward is filing the ticket.
