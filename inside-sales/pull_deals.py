"""Pull every Deal owned by the four AEs, resolve each to a practice, and stage
the raw material for build_deals.py. Writes data/deals_raw.json.

Owner-scoped, ALL pipelines, no date filter: a Deal is a standing opportunity,
not a periodic activity, so the 90-day extract window does not apply to it.
"""
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

TOKEN = os.environ.get("HUBSPOT_ACCESS_TOKEN") or os.environ.get("HUBSPOT_SERVICE_KEY")
if not TOKEN:
    sys.exit("No HUBSPOT_ACCESS_TOKEN in environment")
BASE = "https://api.hubapi.com"
HDRS = {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"}
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

AE = {
    "96412054": "Taylor Sloan",
    "96412056": "Steven Kelly",
    "88456783": "Gabrielle Nurod",
    "96412059": "Andrea Chacin",
}


def req(path, payload=None, method="GET", tries=6):
    body = json.dumps(payload).encode() if payload is not None else None
    for attempt in range(tries):
        r = urllib.request.Request(BASE + path, data=body, headers=HDRS, method=method)
        try:
            with urllib.request.urlopen(r, timeout=90) as f:
                return json.loads(f.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 502, 503, 504):
                time.sleep(2 ** attempt)
                continue
            sys.stderr.write("HTTP %d on %s: %s\n" % (e.code, path, e.read()[:400].decode("replace")))
            raise
        except Exception:
            time.sleep(2 ** attempt)
    raise RuntimeError("failed after %d tries: %s" % (tries, path))


def post(path, payload):
    return req(path, payload, "POST")


DEAL_PROPS = ["dealname", "hubspot_owner_id", "pipeline", "dealstage", "amount",
              "createdate", "closedate", "hs_lastmodifieddate", "notes_next_step",
              "hs_is_closed", "hs_is_closed_won", "num_associated_contacts",
              "hs_num_associated_companies", "description", "hs_deal_stage_probability"]


def search_deals():
    out, after = [], None
    while True:
        p = {"filterGroups": [{"filters": [{"propertyName": "hubspot_owner_id",
                                            "operator": "IN", "values": list(AE)}]}],
             "properties": DEAL_PROPS, "limit": 100}
        if after:
            p["after"] = after
        d = post("/crm/v3/objects/deals/search", p)
        out.extend(d.get("results", []))
        after = d.get("paging", {}).get("next", {}).get("after")
        if not after:
            return out


def pipelines():
    """Pipeline and stage LABELS, plus the closed / closed-won metadata.

    GOTCHA, already bit once: HubSpot returns stage metadata values as STRINGS.
    isClosed comes back as "true" / "false", and every non-empty string is truthy
    in both Python and JS, so a bare truth test reads EVERY stage as closed.
    Compare against the string, which is what this does.
    """
    d = req("/crm/v3/pipelines/deals")
    pl, st = {}, {}
    for p in d.get("results", []):
        pl[p["id"]] = p["label"]
        for s in p.get("stages", []):
            md = s.get("metadata") or {}
            st[s["id"]] = {
                "label": s["label"], "pipeline": p["id"], "pipelineLabel": p["label"],
                "closed": str(md.get("isClosed", "")).lower() == "true",
                "won": str(md.get("isClosedWon", "")).lower() == "true",
                "probability": md.get("probability"),
            }
    return pl, st


def assoc(from_obj, to_obj, ids):
    """v4 batch associations, 100 ids per call."""
    out = {}
    ids = [str(i) for i in ids]
    for i in range(0, len(ids), 100):
        chunk = ids[i:i + 100]
        d = post("/crm/v4/associations/%s/%s/batch/read" % (from_obj, to_obj),
                 {"inputs": [{"id": x} for x in chunk]})
        for r in d.get("results", []):
            out.setdefault(str(r["from"]["id"]), []).extend(
                str(t["toObjectId"]) for t in r.get("to", []))
    return out


CO_PROPS = ["name", "legal_business_name", "doing_business_as", "practice_name",
            "provider_unique_key", "provider_id", "enrollment_date", "hs_object_id",
            "city", "state", "lifecyclestage", "hubspot_owner_id"]
# The four name fields Ed named, with the UI labels they carry in this portal.
NAME_FIELDS = [("name", "Company name"),
               ("legal_business_name", "Legal Business Name"),
               ("doing_business_as", "Doing Business As"),
               ("practice_name", "Practice Name")]


def companies_batch(ids):
    out = {}
    ids = [str(i) for i in ids]
    for i in range(0, len(ids), 100):
        d = post("/crm/v3/objects/companies/batch/read",
                 {"properties": CO_PROPS, "inputs": [{"id": x} for x in ids[i:i + 100]]})
        for r in d.get("results", []):
            out[str(r["id"])] = r.get("properties", {})
    return out


# ---- name normalisation ----------------------------------------------------
# A company record's name carries a trailing provider id ("Perla Dental of Farmers
# Branch - 39738") and a parent reads "- Parent -" / "- Corporate -". A deal name
# carries a trailing " - New Deal". Neither is part of the business's name, so both
# sides are stripped to a comparable stem before anything is compared.
LEGAL = r"(?:llc|pa|dds|dmd|corp|corporation|inc|incorporated|pc|pllc|ltd|co)"


def clean(s):
    if not s:
        return ""
    s = str(s)
    s = re.sub(r"\s*-\s*New Deal\s*$", "", s, flags=re.I)
    s = re.sub(r"\s*-\s*\d{3,}\s*$", "", s)
    s = re.sub(r"\s*-\s*(Parent|Corporate)\s*-\s*", " ", s, flags=re.I)
    s = re.sub(r"\s*-\s*(Parent|Corporate)\s*$", "", s, flags=re.I)
    s = s.casefold()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\b%s\b" % LEGAL, " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def search_companies_by_name(stem, field):
    if not stem:
        return []
    p = {"filterGroups": [{"filters": [{"propertyName": field,
                                        "operator": "CONTAINS_TOKEN", "value": stem}]}],
         "properties": CO_PROPS, "limit": 100}
    try:
        d = post("/crm/v3/objects/companies/search", p)
    except Exception as e:
        sys.stderr.write("  name search failed (%s / %s): %s\n" % (field, stem, e))
        return []
    return d.get("results", [])


def main():
    deals = search_deals()
    sys.stderr.write("deals owned by the four AEs: %d\n" % len(deals))
    pl, st = pipelines()
    ids = [d["id"] for d in deals]

    d2c = assoc("deals", "companies", ids)
    d2p = assoc("deals", "contacts", ids)
    sys.stderr.write("deals with >=1 associated company: %d\n" % sum(1 for i in ids if d2c.get(i)))
    sys.stderr.write("deals with >=1 associated contact: %d\n" % sum(1 for i in ids if d2p.get(i)))

    all_contacts = sorted({c for v in d2p.values() for c in v})
    c2co = assoc("contacts", "companies", all_contacts) if all_contacts else {}

    want = {c for v in d2c.values() for c in v} | {c for v in c2co.values() for c in v}
    co = companies_batch(sorted(want)) if want else {}

    out = {"generatedAtUtc": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
           "owners": AE, "pipelines": pl, "stages": st,
           "deals": [], "companies": co, "nameSearch": {}}

    for d in deals:
        p = d.get("properties", {})
        did = d["id"]
        out["deals"].append({
            "id": did, "props": p,
            "companies": d2c.get(did, []),
            "contacts": d2p.get(did, []),
            "contactCompanies": sorted({x for c in d2p.get(did, []) for x in c2co.get(c, [])}),
        })

    # ---- route (c): name search, all four name fields -----------------------
    # Run for EVERY deal, not only the unassociated ones. An association can
    # resolve to a company record that carries no Provider ID, which reaches a
    # practice but not the warehouse; when that happens the name search is the
    # only remaining way to a provider key, and the candidates have to already be
    # in hand for the resolver to consider them.
    for d in out["deals"]:
        did = d["id"]
        raw = d["props"].get("dealname") or ""
        # "Nutmeg Dental/Dental Smiles" may name TWO practices. Try the whole
        # string and each half, and report when more than one half resolves.
        halves = [raw] + ([h.strip() for h in raw.split("/")] if "/" in raw else [])
        got = {}
        for h in halves:
            stem = clean(h)
            if not stem:
                continue
            for field, label in NAME_FIELDS:
                res = search_companies_by_name(stem, field)
                if res:
                    got.setdefault(h, {})[field] = [
                        {"id": r["id"], "props": r.get("properties", {}), "fieldLabel": label}
                        for r in res]
                time.sleep(0.12)
        out["nameSearch"][did] = {"dealName": raw, "halves": halves, "hits": got}
        sys.stderr.write("  name search %-42s -> %s\n" % (
            raw[:42], {h: {f: len(v) for f, v in m.items()} for h, m in got.items()} or "NOTHING"))

    json.dump(out, open(os.path.join(DATA, "deals_raw.json"), "w", encoding="utf-8"), indent=1)
    sys.stderr.write("wrote data/deals_raw.json\n")


if __name__ == "__main__":
    main()
