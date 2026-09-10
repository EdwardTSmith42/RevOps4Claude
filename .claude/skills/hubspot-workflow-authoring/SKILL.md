---
name: hubspot-workflow-authoring
description: Author, validate and safely ship HubSpot workflows (v4 flows) via the hubspot agent CLI, including workflows on engagement objects like Call. Use whenever creating, editing, enabling or disabling a HubSpot workflow, or when a workflow must repair historical records. Captures the validated JSON shapes for PLATFORM_FLOW, the filter-operator semantics trap that can silently invert a predicate and overwrite live data, the required confirmation gate before enabling, and the fact that workflows never enrol history so a separate audited backfill is needed. Trigger even for a "quick" workflow tweak.
---

# HubSpot workflow authoring

Reusable rules for building HubSpot workflows that mutate records, learned the hard
way. The CLI mechanics (list / get / create / update / delete, digests, JSONL) are
in the vendored `workflow-automation` skill — read that for plumbing. **This skill is
about not shipping a workflow that quietly corrupts data.**

## Hard rules

1. **CALL and other engagement objects ARE valid workflow object types.** Do not
   conclude otherwise from a sample of existing workflows. "0 of 100 workflows in
   this portal target `0-48`" proves nothing about what HubSpot supports — the object
   picker in the UI is the authority, and it lists Call, Meeting, Email, Task,
   Conversation, Lead, Invoice and more. Never tell the user a workflow is impossible
   without checking the picker or attempting a `--dry-run`.
2. **A workflow that writes a property is a standing automation. Get explicit
   confirmation before ENABLING it**, even when Ed has standing authorization for
   routine CRM writes — his own `hubspot-tickets` rule carves out "creating or
   modifying workflows and other standing automation". Creating it disabled is fine;
   flipping `isEnabled` is the gate.
3. **Prove every filter operator's semantics before enabling.** See the trap below.
   A single wrong operator can invert the enrolment predicate and overwrite live data
   on every record you meant to protect.
4. **Workflows never enrol history.** They act only on records that *newly* meet the
   criteria. Any "backfill" ask needs a separate script. Preview it, cap it, audit it.
5. **Omit `defaultBranch` when a non-match should be left alone.** A default branch
   that falls through to a write action will mis-assign every record you could not
   classify. Silence is safer than a guess.

## The operator trap that nearly shipped

Building an "only touch records with no owner" enrolment filter, this was written:

```json
{"property":"hubspot_owner_id","filterType":"PROPERTY",
 "operation":{"operator":"IS_KNOWN","operatorName":"IS_UNKNOWN",
              "operationType":"ALL_PROPERTY"}}
```

`operatorName` is not a real field. The API ignored it, `--dry-run` returned
`ok: true`, and the effective predicate was **`IS_KNOWN`** — the exact inverse of the
intent. Had it been enabled it would have enrolled every call that *already had* an
owner and overwritten it with a phone-line guess.

**Correct form:**

```json
{"property":"hubspot_owner_id","filterType":"PROPERTY",
 "operation":{"operator":"IS_UNKNOWN","includeObjectsWithNoValueSet":true,
              "operationType":"ALL_PROPERTY"}}
```

### How to catch this class of bug

- **A passing `--dry-run` means the body parsed, not that it means what you think.**
  Dry-run validates shape, never semantics.
- **Read the server's echo, field by field, against your intent.** The create/update
  dry-run response echoes the stored body. Diff it against what you meant. An ignored
  field disappears or survives unchanged — either way you can see it.
- **Never invent a field name.** Harvest operator and action shapes from real
  workflows in the same portal:
  `hubspot workflows get <id>` on a few existing flows, then collect every
  `filterType: PROPERTY` operation and tabulate `(operationType, operator)` pairs.
  If your operator is not in that list, you are guessing.
- **Prefer a reversible proof on real records before enabling.** Run the equivalent
  logic as a preview-only script over live data, eyeball the per-entity counts, apply
  it once with an audit log, verify, and only then enable the workflow. If the
  predicate is inverted the preview shows it immediately, at zero cost.

## Validated JSON shapes (harvested from a live portal, dry-run confirmed)

Top level for any non-Contact object:

```json
{
  "name": "...",
  "type": "PLATFORM_FLOW",
  "flowType": "WORKFLOW",
  "objectTypeId": "0-48",
  "isEnabled": false,
  "startActionId": "1",
  "nextAvailableActionId": "8",
  "enrollmentCriteria": { "...": "..." },
  "actions": [ "..." ]
}
```

- **`flowType: "WORKFLOW"` is required.** Omitting it fails create with
  `400 Some required fields were not set: [flowType]`. It is not in the reference doc.
- `type` is `CONTACT_FLOW` for contacts, `PLATFORM_FLOW` for everything else.
- Common `objectTypeId`s: `0-1` contact, `0-2` company, `0-3` deal, `0-5` ticket,
  `0-48` call, `0-47` meeting, `0-49` email, `0-27` task.

Set a property:

```json
{"actionId":"2","type":"SINGLE_CONNECTION","actionTypeId":"0-5","actionTypeVersion":0,
 "fields":{"property_name":"hubspot_owner_id",
           "value":{"staticValue":"96412056","type":"STATIC_VALUE"}}}
```

Branch:

```json
{"actionId":"1","type":"LIST_BRANCH",
 "listBranches":[{"filterBranch":{"...":"..."},
                  "connection":{"edgeType":"STANDARD","nextActionId":"2"},
                  "branchName":"Steven Kelly"}]}
```

Enrolment criteria:

```json
{"type":"LIST_BASED","shouldReEnroll":false,"unEnrollObjectsNotMeetingCriteria":false,
 "listFilterBranch":{"filterBranches":[],"filters":["..."],
                     "filterBranchType":"AND","filterBranchOperator":"AND"}}
```

Nested OR inside a branch: put each alternative in `filterBranches` as its own
`{"filterBranches":[],"filters":[...],"filterBranchType":"AND","filterBranchOperator":"AND"}`
and set the outer branch to `"filterBranchType":"OR","filterBranchOperator":"OR"`.

Operator sets seen in the wild — if yours is absent, verify before using:

| operationType | operators observed |
|---|---|
| `ALL_PROPERTY` | `IS_KNOWN`, `IS_UNKNOWN` |
| `ENUMERATION` | `IS_ANY_OF`, `IS_NONE_OF` |
| `STRING` | `IS_EQUAL_TO`, `IS_NOT_EQUAL_TO` (singular `value`) |
| `MULTISTRING` | `IS_NOT_EQUAL_TO` |
| `NUMBER` | `IS_EQUAL_TO`, `IS_GREATER_THAN_OR_EQUAL_TO` |
| `BOOL` | `IS_NOT_EQUAL_TO` |
| `TIME_POINT` | `IS_BEFORE`, `IS_AFTER` |
| `TIME_RANGED` | `IS_BETWEEN` |

There is a **15-branch ceiling** per branch action. Collapse per-entity branches by
OR-ing several match values into one branch rather than adding branches.

## Shipping sequence

```bash
# 1. Validate shape. Creates nothing.
hubspot workflows create --file wf.json --dry-run

# 2. Create DISABLED. isEnabled: false in the file.
hubspot workflows create --file wf.json

# 3. Prove the predicate on real records with a preview-only script, then apply once
#    with an audit log. Verify per-entity counts look right.

# 4. Ask the user before enabling. Then:
hubspot workflows get <id> > wf_live.json      # need revisionId
#    set isEnabled true, strip createdAt / updatedAt / dataSources
hubspot workflows update <id> --file wf_enable.json --dry-run   # emits a digest
hubspot workflows update <id> --file wf_enable.json \
  --digest <digest> --confirm <flowId>
```

`update` is a **full replace** — a partial body silently clears fields, so always
start from `get`. The `--confirm` value is the flow **id** for update, and the flow
**name** for delete.

## Backfilling history

Workflows cannot repair existing records, so pair every remediation workflow with a
one-time script. Non-negotiables for that script:

- **Default to preview.** Writing requires an explicit `--apply`.
- **Re-check the guard condition per record at write time**, not just in the search
  filter, so a record that gained a value mid-run is skipped.
- **Never overwrite a non-empty value.** Only fill blanks.
- **Skip what you cannot classify** rather than guessing.
- **Append every intended and actual change to a JSONL audit file** (record id, old
  value, new value, why, timestamp, mode) so the change set can be reviewed or
  reversed.
- **Report scope honestly.** Distinguish "all records with the defect" from "the
  subset in scope for this team". They are rarely the same number, and the difference
  usually reveals that the defect is portal-wide.
- Batch writes via `/crm/v3/objects/<obj>/batch/update`, 100 per call.

## Related

- Vendored `workflow-automation` skill — CLI plumbing, digests, JSONL, pagination.
- `reference_hubspot_v4_flow_api` memory — per-type operator sets, branch ceiling.
- `reference_hubspot_cli_hubsql_scope_gap` memory — unset `HUBSPOT_ACCESS_TOKEN` or
  the reports surface 403s; reports are create-only.
- `reference_hubspot_inside_sales_call_model` memory — the live Aloware
  owner-backfill workflow and its rep line map.
- `hubspot-tickets` skill — the standing-authorization rule and its automation carve-out.
