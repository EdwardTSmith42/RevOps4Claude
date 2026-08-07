---
name: provider-link
description: Use when linking HubSpot contacts or marketing leads to HFD provider IDs, building a lead-to-enrollment-to-utilization funnel, answering "did these leads become providers / utilize", attributing enrollments to a campaign or channel (Meta, LinkedIn, paid social), or refreshing the Lazar paid-social funnel. Also use when someone asks to map contacts to companies/providers in bulk.
---

# provider-link

Deterministic pipeline that links HubSpot contacts to `HFDProd_Finance.dbo.Providers` rows and reports the funnel: leads → demo booked/attended → enrolled (activated) → utilizing (funded originations).

## Run it

```bash
python resources/provider_link.py --filter "lead_source=Paid Social" --meetings --suggest-names --out <dir>
```

- `--filter` any hubspot CLI contact filter, repeatable (defaults to `lead_source=Paid Social`, the Lazar cohort).
- `--meetings` adds demo attendance from meeting engagements (1 extra call per booked contact).
- `--suggest-names` writes fuzzy PracticeName candidates for unmatched leads. NEVER auto-match these; hand the CSV to a human (or review inline) — generic tokens like "Dental Care" collide with the Heartland chains.
- `--write-back` stamps `provider_id` on matched contacts via CLI dry-run (follow the printed digest hint to apply).

Outputs: JSON summary (stdout), `provider_link_funnel.csv`, `provider_link_detail.json`, optional `provider_link_name_suggestions.csv`.

## Match cascade (first hit wins)

1. `contact.provider_id` property (rarely filled)
2. contact→company association → company `provider_unique_key`
3. DB email: `Providers.Email1/Email2/DecisionMakerEmail` (exact, lowercased)
4. DB phone: `Phone1/Phone2` normalized to last 10 digits

Expect steps 3–4 to do most of the work; company associations exist for ~12% of marketing leads.

## Interpretation rules

- **Enrolled ≠ has a ProviderID.** A provider row is auto-created (`Source='AUTO'`) the moment someone opens the e-sign enrollment form; abandoned enrollments sit at Status NULL. Activated = `Status='CUR'`; `PDACT` = pending/deactivated. Report `enrolled_activated_CUR`, footnote the rest.
- **Attribution**: enrollment is campaign-attributable only if `EnrolledOn >= lead created`. Pre-existing providers clicking ads are a separate line.
- **Channel**: `hs_analytics_source_data_1='LinkedIn'` → LinkedIn; record source detail `Zite` → Meta (Meta lead-gen form sync). Contacts created by the Fillout forms integration need Fillout submission `urlParameters.utm_source` for channel (form `9AQEokDA7Vus`, key at `temp/posthog-identify/fillout.env.txt`) — the script buckets them Other/Unattributed.
- **Attendance**: `demo_meeting_date` on contacts is ~always empty. Truth = associated meetings with `hs_meeting_outcome='COMPLETED'`. Outcomes were logged inconsistently before ~May 2026, so old cohorts show "held? (outcome not logged)".
- **Utilizing** = funded originations (`Finance.dbo.SAOPurchaseHistory type='Origination'`); apps count from `dbo.Applications` shows pipeline before funding.

## HubSpot company list (no Lists API in the CLI)

To publish results as a HubSpot list, use the v3 Lists API with the service key at `temp/hubspot_onboarding/.hs_token`:
`POST /crm/v3/lists {"name":..., "objectTypeId":"0-2", "processingType":"MANUAL"}` then `PUT /crm/v3/lists/{id}/memberships/add [companyIds]`.
The live setup is a DYNAMIC list 13253 "Paid Social - Provider Matches (auto)" filtering on company `acquisition_channel` IS_ANY_OF the paid-social values — so stamping that property is what adds a company to the list. Two enabled workflows maintain the properties: flow 1848150432 (contact lead_source='Paid Social' + associated company → stamps company `acquisition_channel` via the 0-5 edit-records action with `association: {HUBSPOT_DEFINED, associationTypeId: 1}` — that block is how a contact flow writes to the company) and flow 1848110394 (paid-social company + provider_account_status='Current' → `provider_dd_status`='Passed - DD ticket', else 'Not started'). Resolve provider IDs → company IDs via `hubspot objects search --type companies --filter "provider_unique_key=<pid>"`.

**Due diligence truth source**: the Due Diligence ticket pipeline `859620878` (live Feb 2026; stages incl. Closed - Passed / Closed - Fail / Conditional Pass). DD tickets are often NOT associated to the company and use the LEGAL entity name ("shori group llc" = Wellness Spa) — match by subject ("New Due Diligence Request: ...") across the whole pipeline. Providers activated before Feb 2026 have no DD ticket.

## Requirements / gotchas

- `hubspot` CLI on PATH (user OAuth fine for reads; `owners list` and some writes need the service key via `HUBSPOT_ACCESS_TOKEN`).
- pyodbc + ODBC Driver 18, integrated auth to `hfdsqlfinance.office.local` (works from Ed's machine; TrustServerCertificate=yes).
- jq is NOT available in Git Bash here — the script paginates itself (`--format json` + `meta.next`), don't shell out to jq.
- One lead can map to several providers (multi-location owners like Darrington 38884-86); the funnel counts the lead once, dollars sum across locations.
