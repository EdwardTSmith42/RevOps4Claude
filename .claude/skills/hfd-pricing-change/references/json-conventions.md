# Pricing JSON conventions (validated against production, 2026-08)

Every rule below was verified against `FinanceOffer.dbo.ProviderConfigs` and the archive
history of real changes (AffordableCare V16, Alter 2.3, Heartland 1.1, Aspen HIL tiers,
LaserAway 1ST-2). Cite: Confluence "Pricing JSON Field Definitions" (page 3970629671).

## Document identity and GUIDs

- One `ProviderConfigs` row per LOCATION; a family (parent) shares one document replicated
  per row with only the embedded `ProviderId` (and any per-location carve-outs) differing.
- Document `$.Id` GUID: NEVER changes on edits (survives years of changes); differs from the
  table PK. It only changes when a config is wholesale-replaced from a template.
- Offer/Section GUIDs: new objects get fresh GUIDs (lowercase uuid4); edited or renamed
  objects KEEP their GUIDs. GUID = identity; Name = display label (freely renamed).
- GUIDs are SHARED across all rows of a family. Mint new GUIDs once per change and reuse them
  in every row/variant.

## Offer shape and naming

- Name = `{ProgramCode}_{Grade}_Grade_{Term}{suffix}`. `P` suffix = carries a converted-interest
  Promotion. A trailing `A` = superseded marker (see below). Amount-banded splits append the
  band to the name (e.g. `E_Grade_18<=2500`).
- Promo ladder convention (LaserAway example): 18P -> 6_month_deferred_interest,
  24P -> 12_month, 36P -> 18_month, 48P -> 24_month; standard vs tabbed promo language per the
  field-definitions page. Copy Promotion objects verbatim from the source offer.
- Category (section): "Standard" when program max finance <= $15,000, "Highline" above.
- Section Name = program code EXACTLY (the condition routing tail matches on it).
  DisplayTitle / ShortDescription / LongDescription come from the Program Codes and
  Descriptions file on SharePoint.

## Condition syntax (copied verbatim by the engine - broken syntax = offer never fires)

```
$.CreditGrade = 'A' [AND $.FinanceAmount >= 1000 AND $.FinanceAmount <= 15000] AND ($.Request.ProgramCode = $.ProgramCode OR $.Request.Section = $.ProgramCode [OR $.Request.Section IS NULL])
```

- FinanceAmount clause sits BETWEEN the grade clause and the routing tail.
- The `<=` bound mirrors the offer's own `MaxFinanceAmount`; the `>=` bound mirrors
  `MinFinanceAmount`. Keep fields and condition in sync - both are enforced.
- Offers at the program floor carry no FinanceAmount clause.
- `OR $.Request.Section IS NULL`: include on new-generation offers (all recent programs carry
  it) UNLESS the family deliberately request-pins (match what the family's newest offers do).
- Multi-tier (Aspen style): OR-ed closed ranges with `.99` endings so adjacent tiers cannot
  double-match: `(($.FinanceAmount >= 5000 AND $.FinanceAmount <= 9999.99) OR (...))`. The
  newest edits leave the TOP tier open-ended (`>= 15000`) with MaxFinanceAmount as the cap.
- RiskScore bands: `$.RiskScore >= 40 AND $.RiskScore <= 46`; open band `$.RiskScore > 51`.
  C-grade risk-banded offers need BOTH `$.CreditGrade = 'C'` AND the RiskScore clause, and the
  bands must partition the grade.
- FinanceAmount = treatment minus THAT offer's down payment. With a non-zero DP, band
  boundaries encode treatment-minus-DP (e.g. 1951 = $2,000 - $49). Recompute when DP changes.
- Known production bug pattern to never reproduce: `$.RiskScore >= 40 and <= 46` (lowercase
  `and`, missing operand) - shipped in a draft once, can never match.

## Supersession and archiving

- Supersede a program: add the new section (Active=true) + new offers; rename the old
  program's offers by appending `A` (`_18P` -> `_18PA`), KEEPING GUIDs, economics, conditions.
- Retirement idioms (observed): set per-offer `ArchivedDateUTC` (ISO-8601 Z) and flip the old
  SECTION Active=false. Older idiom: rename the grade token to `'A-Archive'` (condition can
  never match). Offers are NEVER deleted from the array.
- `Active` stays true on archived offers. LIVE = `ArchivedDateUTC IS NULL` + section Active +
  grade token intact.
- `ArchivedDateUTC` stamps are authoring-time, not deploy-time. A FUTURE-dated value has no
  production precedent - if scheduling a sunset, confirm the engine treats non-null-but-future
  as still live, or plan a follow-up change instead.
- Splice positions: new sections and offer blocks go adjacent to their family (section right
  after the source section, offers right after the source block), not appended at the end.

## Top-level fields

- Loose guardrails, not strictly synced to offers (doc MinFinanceAmount 500 coexists with
  300-min offers in production). Change only when the intent is to change the envelope.
- `RegionRateAction` / `LineAssignmentBehavior` are numeric in the DB, enum names in the
  upload format (see upload-format.md).

## DB query patterns (for users with DB access)

- mssql MCP: ONE statement per call, inline `WITH (NOLOCK)` on every table, no leading CTE.
  Never SELECT a whole Document (~300KB, times out): use
  `CROSS APPLY OPENJSON(c.Document,'$.Offers') WITH (...)` for inventories and
  `JSON_QUERY(c.Document,'$.Offers[n]')` for one object. `-1` may mean timeout, not empty.
- Whole-document work: pyodbc direct
  (`DRIVER={ODBC Driver 18 for SQL Server};SERVER=hfdsqlfinance.office.local;DATABASE=FinanceOffer;Trusted_Connection=yes;TrustServerCertificate=yes`),
  export Document to a file. Documents round-trip byte-identically through
  `json.dumps(obj, ensure_ascii=False, separators=(',',':'))` - safe to edit programmatically.
- `ProviderConfigsArchive` rows are PRE-images (the doc as it was BEFORE the save at
  ArchivedOn). No-op saves still write rows - hash-compare before declaring a diff.
- Variant scan: pull every family row, normalize `ProviderId`, SHA-256 group, field-diff any
  minority group. Doc LENGTH comparison is NOT sufficient (a 46-rate MA variant differed by
  4 bytes).

## Deploy flow context (do not perform - for awareness)

Build/test on the account to copy in Sandbox -> copy to prod -> fan out to family rows (the
tool loops rows; archive rows land ms apart). Integrated families route requests by program
code, so a NEW code needs engineering/EasyAPI repointing before the old one is archived, or
1st-look requests get zero offers.
