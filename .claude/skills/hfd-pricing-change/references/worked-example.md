# Worked example: LaserAway 1st Look term-by-amount limits (ClickUp 86ahzmn6g, 2026-08)

Full artifacts (scripts, before/after JSONs, report): `C:\Users\esmith\temp\pricing-change-86ahzmn6g\`.
Use this as the template for "limit terms by financed amount" and, more broadly, for the
new-program-code-version mechanism.

## The request and the resolutions (Step 2 in action)

- Ticket description said "cap max term by financed amount" (2.5k/5k/7.5k bands); the
  "Reason for Request" field said "minimum financed per term" (300/1k/2k/3.5k/6.5k). The two
  Excel attachments were ROI models, not specs. **User ruled: the Reason-for-Request mins.**
- Mechanism: **new program code version** (user's call): `CUS-LA1ST-PRM-01` ->
  `LWY-MDS-LHR-PRM-STD-1ST-2` (taxonomy + family sequence: 3RD ran 05/06/6.1/PRM-07 -> 3RD-8;
  4TH-2; 5TH-1; 1st look had only PRM-01, so 1ST-2).
- Old program: kept live, offers renamed +A, ArchivedDateUTC set 90 days out (flagged: future
  dating has no precedent - confirm engine semantics).
- Limits in BOTH per-offer MinFinanceAmount AND a Condition clause (in-family precedent
  CUS-LA2ND-PRM-4.2); 18-month floor offers keep a clause-free condition; upper bound mirrors
  the grade cap (A 15000 / B 12000).

## The edit (10 old offers + 10 new + 1 section, on account to copy 22275)

- Account to copy from the daily SharePoint list: **22275** ("LaserAway- BaaS Test", TST) -
  the row whose Program Codes include CUS-LA1ST-PRM-01. NOT the ticket's provider ID (16681,
  the parent - which has no config row at all; 258 locations share doc GUID 9e8f815b-...).
- New offers cloned grade/term/rate/promo-identical from the old ones; only Id (pinned fresh
  GUIDs), Name, ProgramCode, MinFinanceAmount (300/1000/2000/3500/6500 by term 18/24/36/48/60),
  and Condition changed. New section cloned from the old one (new GUID, new Name), text
  matching the Program Codes and Descriptions file ("Laser Hair Removal" / "Provides a
  long-term solution for reducing unwanted hair using laser technology.").

## Validation that caught real problems

- **Spec simulation** (amounts 300..15000 x grades A/B vs the requested table): PASS at every
  boundary - terms unlock at exactly 1000/2000/3500/6500; B stops above 12000.
- **Only-intended-fields diff**: all 180 other offers and 13 other sections byte-identical.
- **Variant scan over all 258 rows** (two independent methods): one minority group - the 4
  Massachusetts locations (15804, 16760, 21872, 22268) with every rate above 20.95 clamped to
  20.95 (46 offers; only 4 BYTES of length difference - length comparison would have missed it).
  Field-diff proved APR-only -> per policy, NO second template; a VARIANT-NOTICE listed the
  providers, the 8 new offers needing the clamp (with GUIDs), and a DE notification draft.
- **Format proof**: converting the current DB doc reproduced the tool's own 22275.txt export
  except 60 explainable content edits (the export was a 7/1 pre-deploy draft; prod fixed
  broken `$.RiskScore >= 40 and <= 46` syntax and bumped MinMonthlyPaymentAmount 0 -> 25).

## Reusable scripts (in the artifacts folder)

- `build_new_doc.py` - the change builder (term-min bands; adapt per change).
- `validate_new_doc.py` - independent only-intended-fields validator + spec rows.
- `to_upload_format.py` - DB -> upload format converter (also shipped with this skill).
- `new_guids.json` - pinned GUIDs pattern (mint once, reuse across rows/variants).
