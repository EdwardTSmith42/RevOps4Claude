"""Join the resolved deals to the warehouse and write data/deals.json, the payload
the Deals section renders.

data/deal_contracts.csv is the warehouse pass, run once against
Analytics.dw.FactContract WITH(NOLOCK), ContractStatus <> 'CAN', for exactly the
provider ids resolve_deals.py reached, aggregated to provider-day so the two
windows below can be cut from it without another round trip:

  SELECT c.ContractProviderKey, CONVERT(date, c.ContractCreated), COUNT(*), SUM(c.ContractValue)
  FROM Analytics.dw.FactContract c WITH(NOLOCK)
  WHERE c.ContractStatus <> 'CAN' AND c.ContractProviderKey IN (...)
  GROUP BY c.ContractProviderKey, CONVERT(date, c.ContractCreated)

TWO WINDOWS, both on ContractCreated - the same origination date column the
"What the sourced providers originated" section already uses, so the two cannot
mean different things on one page:

  first40  Close date inclusive through Close date + 40 days exclusive. This is
           the COMP METRIC: AEs are paid on "% of first 40-days funding".
  last30   The 30 complete days ending at midnight today. Ends yesterday, like
           every other window on this page, so no figure sits on a partial day.
"""
import csv
import datetime as dt
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

TODAY = dt.date(2026, 9, 20)          # the anchor the rest of the page uses
L30_END = TODAY                        # exclusive
L30_START = TODAY - dt.timedelta(days=30)
FIRST40_DAYS = 40

R = json.load(open(os.path.join(DATA, "deals_resolved.json"), encoding="utf-8"))

byprov = {}
with open(os.path.join(DATA, "deal_contracts.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        byprov.setdefault(row["ContractProviderKey"], []).append(
            (dt.date.fromisoformat(row["ContractCreated"]),
             int(row["contracts"]), float(row["value"])))


def cut(pids, lo, hi):
    """[lo, hi) across every provider id in the group. Returns (contracts, dollars)."""
    n = v = 0
    for p in pids:
        for d, c, val in byprov.get(p, []):
            if lo <= d < hi:
                n += c
                v += val
    return n, round(v, 2)


def iso(d):
    return d.isoformat()


def iso_last(d):
    """The LAST DAY a half-open window [lo, d) actually counts.

    cut() is half-open, so a window written out as [lo, hi) and then rendered as
    "lo - hi" reads as one day longer than it is and appears to include today, on
    a page whose whole window convention is that no figure sits on a partial day.
    Every date that reaches the payload as the end of a window goes through here.
    """
    return (d - dt.timedelta(days=1)).isoformat()


out = []
for r in R["deals"]:
    pids = r["providerIds"]
    linked = bool(pids) and not r["ambiguous"]
    close = dt.date.fromisoformat(r["closeDate"]) if r.get("closeDate") else None
    created = dt.date.fromisoformat(r["createDate"]) if r.get("createDate") else None

    f40 = None
    if linked and close:
        end = close + dt.timedelta(days=FIRST40_DAYS)
        n, v = cut(pids, close, end)
        f40 = {"contracts": n, "value": v, "start": iso(close), "end": iso_last(end),
               # A window that has not finished yet is a running total, not a result.
               "partial": end > TODAY,
               "daysElapsed": max(0, min(FIRST40_DAYS, (TODAY - close).days)),
               # Close date on an OPEN deal is HubSpot's forecast date, not a date
               # the deal reached. The window is still computed, and still labelled.
               "forecastDate": not r["closed"]}

    l30 = None
    if linked:
        n, v = cut(pids, L30_START, L30_END)
        l30 = {"contracts": n, "value": v, "start": iso(L30_START), "end": iso_last(L30_END)}

    days_open = (TODAY - created).days if created else None
    lastmod = dt.date.fromisoformat(r["lastModified"]) if r.get("lastModified") else None

    out.append({
        "id": r["id"], "name": r["name"], "owner": r["owner"],
        "pipelineLabel": r["pipelineLabel"], "stageLabel": r["stageLabel"],
        "closed": r["closed"], "won": r["won"],
        "amount": r["amount"],
        "createDate": r["createDate"], "closeDate": r["closeDate"],
        "lastModified": r["lastModified"],
        "daysOpen": days_open,
        "daysStale": (TODAY - lastmod).days if lastmod else None,
        "companyCount": r["companyCount"], "contactCount": r["contactCount"],
        "nextStep": r["nextStep"],
        "route": r["route"], "ambiguous": r["ambiguous"], "notes": r["notes"],
        "duplicateOf": r.get("duplicateOf") or [],
        "linked": linked,
        "providerIds": pids,
        "locations": len(r["candidates"]) if linked else 0,
        "matches": [{"company": c["companyName"], "providerId": c["providerId"],
                     "field": c["matchedFieldLabel"] or "Association",
                     "value": (c.get("legalBusinessName") if c["matchedField"] == "legal_business_name"
                               else c.get("doingBusinessAs") if c["matchedField"] == "doing_business_as"
                               else c.get("practiceName") if c["matchedField"] == "practice_name"
                               else c.get("companyName")),
                     "enrolled": c["enrollmentDate"]}
                    for c in r["candidates"]],
        "first40": f40, "last30": l30,
    })

out.sort(key=lambda r: (-(r["amount"] or -1), -(r["daysStale"] or 0)))

doc = {
    "generatedAtUtc": R["generatedAtUtc"],
    "today": iso(TODAY),
    "last30": {"start": iso(L30_START), "end": iso_last(L30_END)},
    "first40Days": FIRST40_DAYS,
    "owners": sorted(R["owners"].values()),
    # Per-provider last-30-day originations, so the section rollup can sum over the
    # UNION of provider ids in view instead of adding deal rows together. The two
    # duplicated deals point at the same practice, so adding their rows would book
    # the same dollars twice.
    "providerLast30": {p: dict(zip(("contracts", "value"), cut([p], L30_START, L30_END)))
                       for p in sorted(byprov)},
    "warehouse": "Analytics.dw.FactContract WITH(NOLOCK), ContractStatus <> 'CAN', "
                 "ContractProviderKey = the company record's Provider ID",
    "deals": out,
}
json.dump(doc, open(os.path.join(DATA, "deals.json"), "w", encoding="utf-8"),
          separators=(",", ":"))

_n = len(out)
print("deals %d | open %d | closed %d | closed won %d"
      % (_n, sum(1 for r in out if not r["closed"]), sum(1 for r in out if r["closed"]),
         sum(1 for r in out if r["won"])))
from collections import Counter
print("owners:", dict(Counter(r["owner"] for r in out)))
print("routes:", dict(Counter(r["route"] or "unresolved" for r in out)))
print("linked %d | ambiguous %d | not linked %d"
      % (sum(1 for r in out if r["linked"]), sum(1 for r in out if r["ambiguous"]),
         sum(1 for r in out if not r["linked"])))
print()
for r in out:
    f = r["first40"]
    l = r["last30"]
    print("%-32s %-24s %-10s | 40d %-22s | 30d %-14s | %s" % (
        (r["name"] or "")[:32], (r["stageLabel"] or "")[:24],
        ("$%s" % format(int(r["amount"]), ",")) if r["amount"] else "no amount",
        ("$%s (%d)%s" % (format(int(f["value"]), ","), f["contracts"],
                         " PARTIAL" if f["partial"] else "")) if f else "n/a",
        ("$%s (%d)" % (format(int(l["value"]), ","), l["contracts"])) if l else "not linked",
        "route " + (r["route"] or "-") + (" AMBIGUOUS" if r["ambiguous"] else "")))
assert all(r["amount"] is None or r["amount"] >= 0 for r in out)
_bad = [r["name"] for r in out if r["linked"] and not r["providerIds"]]
assert not _bad, "linked with no provider id: %s" % _bad
