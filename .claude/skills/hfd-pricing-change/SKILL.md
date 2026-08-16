---
name: hfd-pricing-change
description: "Use when executing an HFD pricing change request: a ClickUp 'Pricing Change Request' ticket, a new or updated program code, changing offer terms/rates/down payments/finance-amount limits, building or editing a pricing JSON, producing a {ProviderId}.txt upload file for the Workflow pricing tool, or anything touching FinanceOffer ProviderConfigs. Trigger on 'pricing change', 'pricing JSON', 'program code', 'account to copy', 'offer condition', 'credit limit change', 'term caps', 'promo change', or a link to the Pricing Changes - Master List Confluence page."
---

# HFD Pricing Change

Turn a pricing change request into a validated, upload-ready pricing JSON for the Workflow
pricing tool. The deliverable is always: **one `{AccountToCopyId}.txt` file in the upload
format + a validation report + (when the family has variants) a variant notice for Data
Engineering.** This skill never deploys anything - a human uploads to Sandbox, tests, and
promotes.

**Read `references/json-conventions.md` before editing any JSON, and
`references/upload-format.md` before writing the output file.** Both encode rules that were
reverse-engineered and byte-verified against production; violating them produces files the
tool rejects or, worse, silently accepts with wrong behavior.

## Sources of truth (in order)

| What | Where | Notes |
|---|---|---|
| The request | ClickUp ticket (list "Pricing Change Request") | Description AND custom fields AND comments AND attachments - they can conflict; see Step 2 |
| Worked examples per change type | Confluence RO space: "Pricing Changes - Master List" (page 4646633473) | Follow the linked example ticket for your change type |
| Field meanings | Confluence RO space: "Pricing JSON Field Definitions" (page 3970629671) | |
| **Account to copy** (start here for the ProviderId) | SharePoint Marketing site: `Shared Documents/02 - Price/Accounts to Copy - Pricing Only - ID List - 10172024.xlsx`, sheet "IDs to Copy" | **Refreshes daily - always read live via the SharePoint connector, never reuse a cached copy.** Find the row whose Program Codes column contains the target program code |
| Section descriptions | SharePoint: `02 - Price/Pricing Naming/Program Codes and Descriptions.xlsx` | DisplayTitle / ShortDescription / LongDescription per program code. Its "Category" column is the treatment vertical, NOT the JSON Standard/Highline field. New codes must be ADDED to this file |
| Current config (no DB access) | SharePoint: `06 - Process/Pricing Configurations/{ProviderId}.txt` | **These are pre-deploy drafts, often stale or containing later-fixed bugs.** Verify freshness (Step 3) or request a fresh export |
| Current config (with DB access) | `FinanceOffer.dbo.ProviderConfigs` / `ProviderConfigsArchive` | Authoritative. See `references/json-conventions.md` for query patterns |

SharePoint share links do not resolve in the M365 connector - use `sharepoint_search` for the
file name, then `read_resource` with the returned `file:///{driveId}/{itemId}` URI.
ClickUp attachment URLs are single-use and expire in ~5 minutes: request the URL and download
it immediately, exactly once, copying the URL byte-for-byte (write it to a file first).

## Workflow

### Step 1 - Understand the change type
Read the ticket fully (description, every custom field, comments, attachment list). Match it
to a master-list change type (new single program / multiple new programs / add code keeping
existing / add code archiving existing / feature update / offer conditions). Read that
example's ClickUp ticket. The attached Excel "program models" are the requester's ROI analysis,
NOT the implementation spec - the spec is the ticket text plus the requester's answers.

### Step 2 - Resolve ambiguities with the user (mandatory)
Tickets routinely contain conflicting specs (description vs "Reason for Request" field vs
attachments). NEVER pick silently. Ask the user (AskUserQuestion or direct) at minimum:
1. Which spec governs, if any two disagree (quote both verbatim).
2. Edit-in-place vs new program code version (ticket wording "New Program Code" field empty +
   "put limits on code X" suggests in-place; house habit for economics changes is a NEW code).
3. The new program code (follow the 7-part taxonomy + the family's version sequence, e.g.
   3rd look ran 05, 06, 6.1, PRM-07 then LWY-MDS-LHR-PRM-STD-3RD-8; propose the next one but
   let the user confirm - the pricing team owns code assignment).
4. Disposition of the superseded program (keep live during integration cutover vs archive now;
   exact ArchivedDateUTC if scheduled).
5. Exact boundary conventions for any amount/score band (>= 2000 vs > 2000 vs 2000.99 endings).

### Step 3 - Get the current config and find the account to copy
1. In the live Accounts to Copy sheet, find the row whose Program Codes include the target
   code. That ProviderId is the account to copy - the generated JSON carries THIS ProviderId.
2. Get the current config for that account. With DB access: pull
   `ProviderConfigs.Document` for that ProviderId. Without: get the freshest
   `{ProviderId}.txt` export and CHECK ITS DATE against the ticket trail / last known change
   to this family; if in doubt, ask the pricing team (Dream Weaver) for a fresh export from
   the Workflow tool. Building on a stale base silently reverts someone else's change.
3. Confirm the account-to-copy's config actually contains the target program code.

### Step 4 - Build the change
Follow `references/json-conventions.md` exactly (GUID rules, offer naming, condition syntax,
Min/MaxFinanceAmount sync, splice positions, supersession via +A rename and ArchivedDateUTC,
section content from the Program Codes and Descriptions file). Make the edit with a script
(not by hand) against the parsed JSON; keep every untouched byte untouched.
`references/worked-example.md` has a complete precedent with build + validation scripts.

### Step 5 - Validate (hard gate, no exceptions)
1. **Only-intended-fields diff:** field-by-field comparison of before vs after proving nothing
   changed except the intended edits (use an independently-written checker, not the builder).
2. **Spec simulation:** compute what the offer engine would present (per grade x amount/score)
   from the new offers' fields and conditions; compare to the requested table at every
   boundary value.
3. **GUID audit:** new objects have fresh GUIDs, edited objects kept theirs, no duplicates,
   document `$.Id` unchanged.
4. If any check fails, fix and re-run. Never hand over a file that has not passed all three.

### Step 6 - Variant scan and the APR-only rule
Configs are per-location; families share one doc but carry per-location carve-outs (e.g.
state APR caps). With DB access, hash-group every family row's Document (normalize the
embedded ProviderId) and field-diff any minority group. Without DB access, ask RevOps to run
the scan - do not assume uniformity.

**Policy: a variant that differs ONLY in InterestRate values does NOT get its own template.**
Maintain one template; produce a **variant notice** listing each differing ProviderId, the
difference type, and exactly which offers (with GUIDs) need the custom APR re-applied after
fan-out; include a ready-to-paste notification for Data Engineering. Only a STRUCTURAL variant
(different offers/terms/fees/conditions) justifies asking the user about a second template.

### Step 7 - Produce the deliverables
1. `{AccountToCopyId}.txt` in the upload format - build with
   `scripts/to_upload_format.py` and verify per `references/upload-format.md`.
2. Validation report: the request, decisions made (who decided what), before/after tables,
   simulation matrix, checks run, variant notice, open items.
3. Checklist of follow-ups (do not do these silently; list them): ClickUp "New Program Code"
   field, new code row in Program Codes and Descriptions, rate sheet / price exhibit,
   integration/engineering ticket if the request routing must point at a new code, Sandbox
   test on the account to copy, pricing approvals sign-off, DE variant notification.

## Red flags - stop and ask

- Two parts of the ticket give different numbers -> Step 2, never average or pick.
- The account-to-copy's export predates the family's last change -> stale base, get a fresh one.
- You are about to create a second template for a rate-only difference -> policy says no.
- An offer condition you are writing can never match (e.g. grade token typo, `and` lowercase,
  missing `$.RiskScore` before a comparator) -> conditions are copied verbatim by the engine;
  broken syntax = offer never fires. Diff your condition against a working production example.
- Anything suggests deploying, updating the DB, or uploading to the tool -> out of scope;
  deliverables are files for human review.

## Common mistakes

| Mistake | Reality |
|---|---|
| Using the ticket's Provider ID as the JSON ProviderId | The JSON carries the ACCOUNT TO COPY's ProviderId (from the daily SharePoint list); the ticket's provider field is often the parent or a display name |
| Treating attachments as the spec | Program-model xlsx files are ROI analyses; the spec is ticket text + user answers |
| Trusting the `{ProviderId}.txt` exports as current state | They are pre-deploy drafts; the DB (or a fresh tool export) is authoritative |
| Writing the output as raw DB-style JSON | The tool needs the upload format (indented, CRLF, nulls dropped, enums as names, AccessKey) - see `references/upload-format.md` |
| New template per variant | APR-only variants = one template + DE re-apply notice |
| Filtering "live" offers by `Active` | Live = `ArchivedDateUTC IS NULL` (+ section Active + grade token not '-Archive'); `Active` stays true on archived offers |
| Minting different GUIDs per provider row | Offer/section GUIDs are shared across a family - mint once, reuse |
