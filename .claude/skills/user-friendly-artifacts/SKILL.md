---
name: user-friendly-artifacts
description: Make dashboards, data dictionaries, source notes and any number-bearing deliverable validatable by a business reader — owner names never owner IDs, UI field labels never API names, a reproducible filter recipe never a code predicate, and an explicit grain on every count. Use whenever building or reviewing a dashboard, artifact, report, data dictionary, "where this number comes from" section, or any hand-off where someone else must confirm a figure. Trigger even when the deliverable is "just for us" — internal identifiers leaking into a deliverable is the single most common reason a stakeholder cannot validate it.
---

# User-friendly artifacts

A number a reader cannot reproduce is not a delivered number. This skill is about the
gap between "technically documented" and "actually validatable", which is where most
otherwise-good dashboards fail.

## The rule behind all of it

**Every identifier and every field name in a deliverable must be the one the reader
sees in their own tool.** They validate by opening HubSpot, or Tableau, or the report
and typing filters in. If your source note names things the way your code names them,
they cannot follow it, and the number is unverifiable no matter how correct it is.

## Hard rules

1. **Never publish an internal identifier where a human-readable name exists.**
   Owner IDs, GUIDs, object type IDs, pipeline/stage IDs, list IDs, provider keys.
   Resolve them at build time and publish the name. Keep the ID in the code only.
   - `hubspot_owner_id IN [80632115, 84616314, ...]` is unreadable.
   - `Owner is any of Brandon Slaughter, Mel Matthews, Gabrielle Nurod, ...` is the same
     filter, and the reader can act on it.
   - Same for enum GUIDs: publish `Call outcome is Connected`, not
     `hs_call_disposition = f240bbac-87c9-4f6e-bf70-924b57d47db7`.
2. **Never publish an API field name where a UI label exists — and look the label up,
   never guess.** `hs_timestamp` on a meeting is *not* "timestamp"; the reader will
   never find it. The API name belongs in a separate field for our code, or in a
   collapsed technical appendix, never in the primary text.
3. **Publish a recipe, not a predicate.** A source note must be executable by hand in
   the reader's tool: which object, which filters in UI operator language ("is between",
   "contains any of", "is any of"), in what order, and the count it should return. A
   boolean expression lifted out of Python is documentation of our implementation, not
   a validation path.
4. **State the grain on every count, in words.** "One row per call" vs "one row per
   contact" vs "one row per contact-activity pair". Two numbers on one page that share
   a label and differ in grain is a defect, not a caveat — either reconcile them or
   relabel both.
5. **Verify the recipe reproduces the number before shipping.** Actually run the
   equivalent search. If the UI cannot express one of your filters, say so in the
   artifact and give the closest expressible approximation plus the residual
   difference. An unverified recipe is worse than none, because it burns the reader's
   trust when it fails.
6. **Resolve at build time, not render time.** The artifact must be self-contained —
   no live lookups, no "see the owners table". Bake the names in.

## Lookups

Get the real label before you write it down. Do not infer it from the API name.

```bash
export HUBSPOT_ACCESS_TOKEN="$HUBSPOT_SERVICE_KEY"   # CLI reads a different var name

hubspot properties get --type meetings hs_timestamp     # -> the "label" field is the truth
hubspot owners list                                     # id -> firstName/lastName/email
hubspot pipelines list --type deals                     # stage ids -> stage labels
```

Enum options whose property has `externalOptions: true` are **not** in the property
schema — `properties options-list` returns an empty array, which is a false negative,
not a finding. Call dispositions live at `GET /calling/v1/dispositions`. Check
`custom: false` before claiming an option set is portal-specific; most are HubSpot
global defaults.

For SQL-backed numbers, publish the table and the business column caption, and keep
`WITH(NOLOCK)` on every table reference (house rule). Name the date column by what it
means to the business ("contract created"), then the column name in the appendix.

## Applies to Tableau too

Field captions in plain business terms, sheet names describing the task not the
mechanic, one filter card per filter, and a data dictionary as an on-canvas Text
object — subscriptions send a static image, so tooltip definitions never reach the
subscriber. See `tableau-twb` for the mechanics.

## Review checklist

Before shipping any number-bearing deliverable, grep your own output for:

- [ ] Bare numeric IDs in user-visible text (owner, stage, list, pipeline, object type)
- [ ] GUIDs in user-visible text
- [ ] `hs_*`, `snake_case`, or any API/column name in a label, caption or source note
- [ ] A count with no stated grain
- [ ] Two numbers sharing a label with different grains or different scopes
- [ ] A rate whose numerator and denominator come from different populations
- [ ] A source note that is a code expression rather than a clickable/typeable recipe
- [ ] Hardcoded prose numbers left over from an earlier run — regenerate or delete them
- [ ] Any recipe you did not actually execute

## Why this exists

Ed asked for a "where every number comes from" section specifically so he could
validate the inside-sales dashboard. The first thing he tried to validate, he could
not — the source note named the date field `hs_timestamp` and expressed the owner
filter as a list of six numeric IDs, and the definition it described silently used a
different date field than the report it claimed to build on. The numbers were right;
the artifact still failed, because it documented the implementation instead of giving
him a path to check it. Related: [[feedback_tableau_user_friendly_naming]],
[[project_inside_sales_activity_dashboard]].
