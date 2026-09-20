"""Turn data/deals_raw.json into data/deals.json: one row per Deal, each resolved
to a practice (or honestly marked unresolved), ready for the warehouse pass.

THE RESOLUTION LADDER (Ed, 2026-09-20). A deal only earns originations dollars if
it reaches a PROVIDER ID, because that is the only key Analytics.dw.FactContract
joins on. Routes are tried in order and the one that produced the provider id is
recorded on the row and rendered on the page:

  (a) deal -> company association
  (b) deal -> contact -> company association
  (c) NAME SEARCH across the four name fields on the company record:
        Company name, Legal Business Name, Doing Business As, Practice Name.

A route that lands on a company record carrying NO Provider ID does not stop the
ladder - it resolved a company but not a practice we can measure, so the next
route still runs. The associated company is still shown, labelled for what it is.

WHY NAME SEARCH NEEDS A SECOND FILTER: HubSpot's CONTAINS_TOKEN is a token match,
not a phrase match. Searching "Dental Smiles" returns 100 companies including
"Healthy Smiles Dental Care" and "7 Day Dental Smiles". So the search is only a
CANDIDATE GENERATOR; every candidate is then re-checked here by requiring the
cleaned deal stem to appear as a CONTIGUOUS run of words inside the cleaned value
of the field that matched. That is what rejects "Lee's Summit Family & Cosmetic
Dental Care" for a deal named "Summit Family Dental".
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
RAW = json.load(open(os.path.join(DATA, "deals_raw.json"), encoding="utf-8"))

LEGAL = r"(?:llc|pa|dds|dmd|corp|corporation|inc|incorporated|pc|pllc|ltd|co|prof|dr)"
FIELD_LABEL = {"name": "Company name", "legal_business_name": "Legal Business Name",
               "doing_business_as": "Doing Business As", "practice_name": "Practice Name"}


def clean(s):
    if not s:
        return ""
    s = str(s)
    s = re.sub(r"\s*-\s*New Deal\s*$", "", s, flags=re.I)
    s = re.sub(r"\s*-\s*\d{3,}\s*$", "", s)
    s = re.sub(r"\s*-\s*(Parent|Corporate)\s*-?\s*$", "", s, flags=re.I)
    s = re.sub(r"\s*-\s*(Parent|Corporate)\s*-\s*", " ", s, flags=re.I)
    s = s.casefold()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\b%s\b" % LEGAL, " ", s)
    return re.sub(r"\s+", " ", s).strip()


def phrase_in(stem, value):
    """True when the cleaned stem is a CONTIGUOUS run of words inside the cleaned
    value, or the other way round. Word-boundary aware, so 'zak dental' does not
    match 'zak downey dental'."""
    a, b = clean(stem), clean(value)
    if not a or not b:
        return False
    at, bt = a.split(), b.split()
    for seq, hay in ((at, bt), (bt, at)):
        n = len(seq)
        for i in range(len(hay) - n + 1):
            if hay[i:i + n] == seq:
                return True
    return False


def cand(cid, props, route, via):
    return {"companyId": str(cid), "companyName": props.get("name"),
            "providerId": (props.get("provider_unique_key") or props.get("provider_id") or None),
            "enrollmentDate": props.get("enrollment_date") or None,
            "legalBusinessName": props.get("legal_business_name"),
            "doingBusinessAs": props.get("doing_business_as"),
            "practiceName": props.get("practice_name"),
            "city": props.get("city"), "state": props.get("state"),
            "route": route, "matchedField": via, "matchedFieldLabel": FIELD_LABEL.get(via or "")}


def group_key(c):
    """Records that belong to the same business. The Legal Business Name is the
    entity, so records sharing one are one practice group (this is what makes the
    13 Dr. Zak locations a single practice rather than 13 ambiguous candidates);
    otherwise fall back to the record's own cleaned name."""
    return clean(c.get("legalBusinessName")) or clean(c.get("companyName")) or c["companyId"]


def resolve(d):
    co = RAW["companies"]
    name = d["props"].get("dealname") or ""
    out = {"candidates": [], "route": None, "ambiguous": False, "notes": []}

    a = [cand(c, co.get(c, {}), "a", None) for c in d["companies"]]
    b = [cand(c, co.get(c, {}), "b", None) for c in d["contactCompanies"]
         if c not in d["companies"]]

    # route (c): every candidate the search returned, re-checked here.
    c_list, seen = [], set()
    ns = RAW.get("nameSearch", {}).get(d["id"], {})
    for half, fm in (ns.get("hits") or {}).items():
        for field, hits in fm.items():
            for h in hits:
                p = h.get("props", {})
                if not phrase_in(half, p.get(field)):
                    continue
                k = (h["id"], field)
                if k in seen:
                    continue
                seen.add(k)
                c_list.append(cand(h["id"], p, "c", field))
    # one row per company: keep the first field that confirmed it, but remember all
    bycid = {}
    for c in c_list:
        cur = bycid.get(c["companyId"])
        if cur:
            cur.setdefault("alsoMatched", []).append(c["matchedFieldLabel"])
        else:
            bycid[c["companyId"]] = c
    c_list = list(bycid.values())

    out["assoc"] = a + b
    out["nameCandidates"] = c_list

    for route, pool in (("a", a), ("b", b), ("c", c_list)):
        withkey = [x for x in pool if x["providerId"]]
        if not withkey:
            continue
        enrolled = [x for x in withkey if x["enrollmentDate"]]
        picked = enrolled or withkey
        if enrolled and len(enrolled) != len(withkey):
            out["notes"].append(
                "%d of %d candidate company records carry an Enrollment date; the "
                "un-enrolled ones were dropped." % (len(enrolled), len(withkey)))
        groups = {}
        for x in picked:
            groups.setdefault(group_key(x), []).append(x)
        # AMBIGUITY IS ONLY EVER RAISED ON THE NAME-SEARCH ROUTE, on purpose.
        # An association is the CRM's own statement that these company records
        # belong to this deal (route a) or to the person on it (route b), so a set
        # of them is a multi-location practice group and is summed - that is the
        # "8 or more locations" case Mel asked the section to cover. A name match
        # is a guess, so two name-matched records that do not share a Legal
        # Business Name are two different businesses until a human says otherwise.
        if route == "c" and len(groups) > 1:
            out["ambiguous"] = True
            out["route"] = route
            out["candidates"] = picked
            out["notes"].append(
                "Route (%s) found %d company records that do not share a Legal Business "
                "Name, so they are not one practice. No dollars are shown - the "
                "candidates are listed instead of one being picked silently."
                % (route, len(picked)))
            return out
        out["route"] = route
        out["candidates"] = picked
        return out

    if a or b or c_list:
        out["notes"].append(
            "A company record was found but it carries no Provider ID, so it cannot "
            "reach the warehouse. Originations are shown as not linked, not as zero.")
    return out


rows = []
for d in RAW["deals"]:
    p = d["props"]
    st = RAW["stages"].get(p.get("dealstage"), {})
    r = resolve(d)
    rows.append({
        "id": d["id"],
        "name": p.get("dealname"),
        "ownerId": p.get("hubspot_owner_id"),
        "owner": RAW["owners"].get(p.get("hubspot_owner_id"), "Unassigned"),
        "pipelineLabel": st.get("pipelineLabel") or RAW["pipelines"].get(p.get("pipeline")),
        "stageLabel": st.get("label"),
        # isClosed arrives as the STRING "true"/"false" from HubSpot. pull_deals.py
        # already compared it AS A STRING; if it had been read as a boolean every
        # stage would read closed, which is the bug this comment exists to prevent.
        "closed": bool(st.get("closed")),
        # No stage in either pipeline carries isClosedWon at all, so the deal-level
        # Closed won property is the source of truth and the stage probability is
        # the cross-check: 1.0 with isClosed true is a won-and-in-delivery stage.
        "won": str(p.get("hs_is_closed_won", "")).lower() == "true",
        "stageProbability": st.get("probability"),
        "amount": float(p["amount"]) if p.get("amount") else None,
        "createDate": (p.get("createdate") or "")[:10] or None,
        "closeDate": (p.get("closedate") or "")[:10] or None,
        "lastModified": (p.get("hs_lastmodifieddate") or "")[:10] or None,
        "companyCount": len(d["companies"]),
        "contactCount": len(d["contacts"]),
        "nextStep": p.get("notes_next_step") or "",
        "route": r["route"], "ambiguous": r["ambiguous"], "notes": r["notes"],
        "candidates": r["candidates"], "assoc": r["assoc"],
        "nameCandidates": r["nameCandidates"],
        "providerIds": sorted({c["providerId"] for c in r["candidates"] if c["providerId"]}),
    })

# duplicates: same owner, same cleaned deal name
bykey = {}
for r in rows:
    bykey.setdefault((r["owner"], clean(r["name"])), []).append(r)
for k, grp in bykey.items():
    if len(grp) > 1:
        for r in grp:
            r["duplicateOf"] = [x["id"] for x in grp if x["id"] != r["id"]]

json.dump({"generatedAtUtc": RAW["generatedAtUtc"], "owners": RAW["owners"], "deals": rows},
          open(os.path.join(DATA, "deals_resolved.json"), "w", encoding="utf-8"), indent=1)

print("%-34s %-6s %-5s %-9s %s" % ("DEAL", "ROUTE", "AMBIG", "PIDS", "MATCHED ON"))
for r in rows:
    print("%-34s %-6s %-5s %-9s %s" % (
        (r["name"] or "")[:34], r["route"] or "-", "yes" if r["ambiguous"] else "",
        ",".join(r["providerIds"])[:9],
        "; ".join(sorted({(c["matchedFieldLabel"] or "association") for c in r["candidates"]}))))
from collections import Counter
print("\nroutes:", dict(Counter(r["route"] or "unresolved" for r in rows)))
print("ambiguous:", sum(1 for r in rows if r["ambiguous"]))
print("all provider ids:", sorted({p for r in rows for p in r["providerIds"]}))
