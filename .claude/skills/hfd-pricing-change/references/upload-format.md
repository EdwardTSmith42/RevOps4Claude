# The upload format ({ProviderId}.txt)

The Workflow pricing tool exchanges configs as `{ProviderId}.txt` files (SharePoint Marketing
site, `Shared Documents/06 - Process/Pricing Configurations/`). This format differs from the
raw DB `Document` column. The converter `scripts/to_upload_format.py` implements all rules and
was **byte-verified**: re-serializing a parsed production export reproduces it exactly.

## Rules (DB Document -> upload file)

1. Pretty-printed JSON, 2-space indent, **CRLF** line endings, **no trailing newline**,
   UTF-8 **without BOM** (real characters like the TM sign stay raw, not \u-escaped).
2. **Drop every null-valued property, recursively.** Keep empty strings, zeros, and empty
   arrays. (An offer's SectionName/GroupName/DisplayTitle/Criteria/SectionId/GroupId/Banners/
   ProcessingFee/... disappear when null; `ArchivedDateUTC` APPEARS when set, in its DB
   position near the end. Archived offers are NOT dropped.)
3. **Keep the DB document's own key order** (top level and within every object) - exports
   differ in e.g. Groups position because the underlying DB docs differ; do not impose a
   fixed order.
4. **Integral numbers lose the `.0`**: `2.0 -> 2`, `15000.0 -> 15000`, `0.0 -> 0`.
   Non-integral stay as stored (`24.99`, `0.951`).
5. **Enums become names**:
   - `RegionRateAction`: `0 -> "None"` (1/2 unobserved; map "Enforce"/"Override" and flag)
   - `LineAssignmentBehavior`: `0 -> "ApplyToDownPayment"`, `1 -> "LimitToMaxFinanceAmount"`
   - `ProcessingFee.Type`: `0 -> "Fixed"`, `1 -> "Percent"`
   - `TreatmentDiscount` gains a derived trailing `"Type"`: `"Percent"` if IsPercent else `"Fixed"`
6. **Append `"AccessKey"` as the last property**: constant
   `fa5ea626-b23a-4d84-b77a-5c6eb40d7dcd` (identical in every observed export; it is NOT
   stored in the FinanceOffer database).

## Verification of an output file (always run)

- Parses as JSON; `\n` count equals `\r\n` count; no BOM; expected offer/section counts.
- Spot-check one edited offer and one untouched offer against the DB values.
- If a recent export of the SAME account exists: convert the current DB doc and diff against
  it - every difference must be an explainable content change, not a format change.

## Staleness warning

The SharePoint exports are UPLOAD DRAFTS, not prod snapshots: one export dated 7/1 deployed
7/16 with post-draft fixes (broken condition syntax repaired, MinMonthlyPaymentAmount 0 -> 25
on 51 offers). The DB is authoritative; an export is trustworthy only if freshly generated
from the tool.
