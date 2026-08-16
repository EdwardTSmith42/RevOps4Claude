"""
Convert a FinanceOffer.dbo.ProviderConfigs Document (raw DB JSON) into the
Workflow pricing tool's upload/export format (the {ProviderId}.txt files in
SharePoint > Marketing > 06 - Process > Pricing Configurations).

Format rules (reverse-engineered from 22157.txt / 22275.txt / 35767.txt and
byte-verified against 22275.txt):
  - 2-space indented JSON, CRLF line endings, no trailing newline, UTF-8 no BOM
  - null-valued properties are OMITTED everywhere (empty strings/0/[] are kept)
  - within objects, original DB key order is kept (minus dropped nulls) EXCEPT
    the top level, which uses the tool's fixed order ending Sections, Offers,
    Groups, AccessKey
  - integral floats are written as integers (2.0 -> 2, 15000.0 -> 15000)
  - enums are written as names: RegionRateAction 0 -> "None",
    LineAssignmentBehavior 0 -> "ApplyToDownPayment", 1 -> "LimitToMaxFinanceAmount"
  - AccessKey is a constant taken from existing exports (not stored in the DB)
"""
import json, sys

ACCESS_KEY = 'fa5ea626-b23a-4d84-b77a-5c6eb40d7dcd'  # same value in 22157.txt and 22275.txt
REGION_RATE_ACTION = {0: 'None', 1: 'Enforce', 2: 'Override'}
LINE_ASSIGNMENT = {0: 'ApplyToDownPayment', 1: 'LimitToMaxFinanceAmount'}

FEE_TYPE = {0: 'Fixed', 1: 'Percent'}

def clean(x, key=None):
    """Drop nulls recursively; collapse integral floats to ints; map fee-object enums."""
    if isinstance(x, dict):
        out = {}
        for k, v in x.items():
            if v is None:
                continue
            if k == 'Type' and key in ('ProcessingFee',):
                out[k] = FEE_TYPE[int(v)]
            else:
                out[k] = clean(v, k)
        # upload model appends Type to TreatmentDiscount, derived from IsPercent
        if key == 'TreatmentDiscount' and 'Type' not in out and 'IsPercent' in out:
            out['Type'] = 'Percent' if out['IsPercent'] else 'Fixed'
        return out
    if isinstance(x, list):
        return [clean(v, key) for v in x]
    if isinstance(x, float) and x.is_integer():
        return int(x)
    return x

def to_upload(db_doc: dict) -> str:
    out = {}
    for k, v in db_doc.items():   # keep the DB document's own key order
        if v is None:
            continue
        if k == 'RegionRateAction':
            out[k] = REGION_RATE_ACTION[int(v)]
        elif k == 'LineAssignmentBehavior':
            out[k] = LINE_ASSIGNMENT[int(v)]
        else:
            out[k] = clean(v)
    out['AccessKey'] = ACCESS_KEY
    text = json.dumps(out, ensure_ascii=False, indent=2)
    return text.replace('\n', '\r\n')

if __name__ == '__main__':
    db = json.loads(open(sys.argv[1], encoding='utf-8').read())
    txt = to_upload(db)
    with open(sys.argv[2], 'w', encoding='utf-8', newline='') as f:
        f.write(txt)
    print(f'{sys.argv[2]}: {len(txt)} chars')
