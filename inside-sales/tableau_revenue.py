import argparse
import base64
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

POD = os.environ.get("TABLEAU_POD", "10az")
SITE = os.environ.get("TABLEAU_SITE", "healthcarefinancedirect")
HOST = "https://%s.online.tableau.com" % POD
API = "3.29"
DS_LUID = os.environ.get("TABLEAU_REVENUE_DS", "583b19c2-c2ac-4aa4-a207-4714da9a0262")
DS_NAME = "v.HfdV3"

F_VALUE = "Contract Value"
F_CREATED = "Contract Created"
F_STATUS = "Contract Status"
F_CONTRACT_ID = "Contract Id"
F_CONTRACT_KEY = "Contract Unique Key"
F_CONTRACT_PROVIDER = "Contract Provider Key"
F_PROVIDER = "Provider Unique Key"

CANCELLED = ["CAN"]


class TableauError(RuntimeError):
    pass


def _post(url, payload, headers, retries=3):
    body = json.dumps(payload).encode("utf-8")
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    h.update(headers)
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=body, headers=h, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:600]
            last = "HTTP %s %s" % (e.code, detail)
            if e.code in (401, 429, 500, 502, 503, 504):
                time.sleep(2 * (attempt + 1))
                continue
            raise TableauError(last)
        except Exception as e:
            last = str(e)
            time.sleep(2 * (attempt + 1))
    raise TableauError("gave up after %d attempts: %s" % (retries, last))


def signin():
    name = os.environ.get("TABLEAU_PAT_NAME")
    secret = os.environ.get("TABLEAU_PAT_SECRET")
    if not name or not secret:
        raise TableauError(
            "TABLEAU_PAT_NAME / TABLEAU_PAT_SECRET are not set. The revenue step reads the "
            "published datasource '%s' over the VizQL Data Service and cannot run without a "
            "Tableau personal access token. The token's user needs View + Connect + API Access "
            "on that datasource." % DS_NAME)
    url = "%s/api/%s/auth/signin" % (HOST, API)
    payload = {"credentials": {"personalAccessTokenName": name,
                               "personalAccessTokenSecret": secret,
                               "site": {"contentUrl": SITE}}}
    d = _post(url, payload, {})
    c = d["credentials"]
    return c["token"], c["site"]["id"]


def vds(token, fields, filters):
    url = "%s/api/v1/vizql-data-service/query-datasource" % HOST
    payload = {"datasource": {"datasourceLuid": DS_LUID},
               "query": {"fields": fields, "filters": filters}}
    d = _post(url, payload, {"X-Tableau-Auth": token})
    if "data" not in d:
        raise TableauError("VDS returned no data key: %s" % json.dumps(d)[:400])
    return d["data"]


def cohort_filter(pids):
    return {"field": {"fieldCaption": F_PROVIDER}, "filterType": "SET",
            "values": list(pids), "exclude": False}


def not_cancelled():
    return {"field": {"fieldCaption": F_STATUS}, "filterType": "SET",
            "values": CANCELLED, "exclude": True}


def date_range(lo, hi):
    return {"field": {"fieldCaption": F_CREATED, "function": "TRUNC_DAY"},
            "filterType": "QUANTITATIVE_DATE", "quantitativeFilterType": "RANGE",
            "minDate": lo, "maxDate": hi}


def read_cohort():
    p = os.path.join(DATA, "sourced_pids.txt")
    raw = open(p, encoding="utf-8").read().strip()
    pids = [x.strip().strip("'").strip() for x in raw.split(",") if x.strip()]
    pids = [x for x in pids if x]
    if not pids:
        raise TableauError("data/sourced_pids.txt is empty - build.py has not run")
    return pids


def periods(today):
    mon = today - dt.timedelta(days=today.weekday())
    lw = mon - dt.timedelta(days=7)
    y = today - dt.timedelta(days=1)
    lm_end = today.replace(day=1) - dt.timedelta(days=1)
    return {
        "thisWeek": (mon, today, "This week"),
        "lastWeek": (lw, mon - dt.timedelta(days=1), "Last week"),
        "mtd": (today.replace(day=1), today, "Month to date"),
        "lastMonth": (lm_end.replace(day=1), lm_end, "Last month"),
        "last90": (y - dt.timedelta(days=89), y, "Last 90 days"),
    }


def fmt(d):
    return d.isoformat()


def nice(d):
    return d.strftime("%b %-d, %Y") if os.name != "nt" else d.strftime("%b %#d, %Y")


def run(today, raw_path=None):
    pids = read_cohort()
    P = periods(today)
    lo = min(v[0] for v in P.values())
    hi = max(v[1] for v in P.values())

    if raw_path:
        blob = json.load(open(raw_path, encoding="utf-8"))
        days = blob["days"]
        lifetime = blob["lifetime"]
        producing = blob["producing"]
        token = None
    else:
        token, _ = signin()
        base = [not_cancelled(), cohort_filter(pids)]
        days = vds(token, [
            {"fieldCaption": F_CREATED, "function": "TRUNC_DAY"},
            {"fieldCaption": F_VALUE, "function": "SUM"},
            {"fieldCaption": F_CONTRACT_ID, "function": "COUNT"},
            {"fieldCaption": F_CONTRACT_KEY, "function": "COUNTD"},
        ], base + [date_range(fmt(lo), fmt(hi))])
        life = vds(token, [
            {"fieldCaption": F_VALUE, "function": "SUM"},
            {"fieldCaption": F_CONTRACT_ID, "function": "COUNT"},
            {"fieldCaption": F_CONTRACT_PROVIDER, "function": "COUNTD"},
            {"fieldCaption": F_CREATED, "function": "MIN"},
        ], base)[0]
        lifetime = {"value": round(life["SUM(%s)" % F_VALUE], 2),
                    "contracts": life["COUNT(%s)" % F_CONTRACT_ID],
                    "producingProviders": life["COUNTD(%s)" % F_CONTRACT_PROVIDER],
                    "earliestContract": life["MIN(%s)" % F_CREATED][:10]}
        producing = {}
        for k, (a, b, _lab) in P.items():
            r = vds(token, [{"fieldCaption": F_CONTRACT_PROVIDER, "function": "COUNTD"}],
                    base + [date_range(fmt(a), fmt(b))])
            producing[k] = r[0]["COUNTD(%s)" % F_CONTRACT_PROVIDER] if r else 0
        mr = vds(token, [
            {"fieldCaption": F_CREATED, "function": "TRUNC_MONTH"},
            {"fieldCaption": F_CONTRACT_PROVIDER, "function": "COUNTD"},
        ], base + [date_range(fmt(lo), fmt(hi))])
        producing["_months"] = {r["MONTH(%s)" % F_CREATED][:7]:
                                r["COUNTD(%s)" % F_CONTRACT_PROVIDER] for r in mr}

    byday = {}
    for r in days:
        d = r["DAY(%s)" % F_CREATED][:10]
        v = r["SUM(%s)" % F_VALUE]
        n = r["COUNT(%s)" % F_CONTRACT_ID]
        uk = r.get("COUNTD(%s)" % F_CONTRACT_KEY, n)
        if uk != n:
            raise TableauError(
                "fan-out on %s: COUNT(Contract Id)=%d but COUNTD(Contract Unique Key)=%d. "
                "A relationship in %s is duplicating contract rows and SUM(Contract Value) "
                "is therefore inflated." % (d, n, uk, DS_NAME))
        byday[d] = (v, n)

    def agg(a, b):
        v = n = 0.0
        for d, (vv, nn) in byday.items():
            if fmt(a) <= d <= fmt(b):
                v += vv
                n += nn
        return round(v, 2), int(n)

    out_periods = {}
    for k, (a, b, lab) in P.items():
        v, n = agg(a, b)
        out_periods[k] = {"start": fmt(a), "end": fmt(b), "value": v, "contracts": n,
                          "producingProviders": producing.get(k, 0), "label": lab,
                          "range": "%s - %s" % (nice(a), nice(b))}

    tw = P["thisWeek"]
    complete_week = today.weekday() == 6
    out_periods["thisWeek"]["note"] = (
        "Mon %s to Sun %s. %s" % (
            fmt(tw[0]), fmt(tw[1]),
            "Today is the Sunday that closes the week, so this is a COMPLETE Mon-Sun week."
            if complete_week else
            "PARTIAL: today is %s, so this is %d of 7 days and is NOT directly comparable to "
            "Last week without pro-rating." % (today.strftime("%A"), today.weekday() + 1)))
    out_periods["lastWeek"]["note"] = (
        "Mon %s to Sun %s. A complete Mon-Sun week." % (fmt(P["lastWeek"][0]), fmt(P["lastWeek"][1])))
    mdays = (today.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    out_periods["mtd"]["note"] = (
        "%s to %s, %d of %s's %d days. PARTIAL: do not compare its total to Last month's "
        "without pro-rating." % (fmt(P["mtd"][0]), fmt(today), today.day,
                                 today.strftime("%B"), mdays.day))
    out_periods["lastMonth"]["note"] = (
        "All %d days of %s. A complete month." % (P["lastMonth"][1].day,
                                                  P["lastMonth"][0].strftime("%B %Y")))
    out_periods["last90"]["note"] = (
        "%s to %s, the SAME 90 complete days the activity extract ran on, so revenue and "
        "activity on this page cover the identical window."
        % (fmt(P["last90"][0]), fmt(P["last90"][1])))

    monthly = {}
    for d, (vv, nn) in byday.items():
        m = d[:7]
        monthly.setdefault(m, [0.0, 0])
        monthly[m][0] += vv
        monthly[m][1] += nn
    mprov = producing.get("_months") or {}
    missing = [m for m in monthly if m not in mprov]
    if missing:
        raise TableauError(
            "no distinct-provider count for month(s) %s. The page prints m.providers "
            "verbatim, so a missing value would render as 'null providers'." % ", ".join(sorted(missing)))
    monthly_out = [{"m": dt.date(int(m[:4]), int(m[5:7]), 1).strftime("%b %Y"),
                    "value": round(v, 2), "contracts": n, "providers": mprov[m]}
                   for m, (v, n) in sorted(monthly.items())]

    l90 = out_periods["last90"]
    prev = {}
    rp = os.path.join(DATA, "revenue.json")
    if os.path.exists(rp):
        try:
            old = json.load(open(rp, encoding="utf-8"))
            prev = {"asOf": old.get("asOf"),
                    "last90Window": [old.get("periods", {}).get("last90", {}).get("start"),
                                     old.get("periods", {}).get("last90", {}).get("end")],
                    "last90Value": old.get("periods", {}).get("last90", {}).get("value"),
                    "sourcedProviders": old.get("sourcedProviders"),
                    "restatement": old.get("restatement")}
        except Exception:
            prev = {}

    doc = {
        "asOf": fmt(today),
        "source": "Tableau Cloud published datasource '%s', Contracts table, joined to the %d "
                  "providers this team sourced" % (DS_NAME, len(pids)),
        "system": "Tableau Cloud VizQL Data Service (%s, site %s, datasource LUID %s). "
                  "Moved off direct SQL on 2026-09-20 because a scheduled cloud session has no "
                  "VPN and cannot reach Analytics.dw.FactContract." % (HOST, SITE, DS_LUID),
        "tableauQuery": {
            "datasource": DS_NAME,
            "measure": "SUM(%s)" % F_VALUE,
            "dateField": F_CREATED,
            "statusFilter": "%s excludes %s" % (F_STATUS, ", ".join(CANCELLED)),
            "cohortFilter": "%s is one of the %d ids in data/sourced_pids.txt" % (F_PROVIDER, len(pids)),
            "grain": "TRUNC_DAY(%s), one result set re-aggregated into every period below" % F_CREATED,
            "fanoutGuard": "COUNT(%s) is compared to COUNTD(%s) on every day; the run aborts if "
                           "they diverge, which is how a relationship fan-out in a multi-fact "
                           "datasource would present" % (F_CONTRACT_ID, F_CONTRACT_KEY),
        },
        "joinKey": "%s = the HubSpot COMPANY.provider_unique_key of each sourced company. The "
                   "cohort is filtered on the Providers-table field %s, not on %s, because the "
                   "contract-side field only contains providers that have originated and a SET "
                   "filter on it rejects the whole query when a sourced provider has produced "
                   "nothing yet." % (F_PROVIDER, F_PROVIDER, F_CONTRACT_PROVIDER),
        "dateProperty": F_CREATED,
        "grain": "one row per contract",
        "cohortFile": "data/sourced_pids.txt, regenerated by build.py from the current sourced "
                      "flag - never a hand-typed list",
        "weekStart": "Monday",
        "today": "%s (%s)" % (fmt(today), today.strftime("%A")),
        "sourcedProviders": len(pids),
        "producingProviders": lifetime["producingProviders"],
        "contracts": l90["contracts"],
        "trailing90d": l90["value"],
        "lifetime": lifetime["value"],
        "contractsLifetime": lifetime["contracts"],
        "earliestContractInCohort": lifetime.get("earliestContract"),
        "periods": out_periods,
        "monthly": monthly_out,
        "avgTicket": round(l90["value"] / l90["contracts"], 2) if l90["contracts"] else 0,
        "recomputedOn": fmt(today),
        "stale": False,
        "priorRun": prev,
        "restatement": prev.get("restatement") or {},
        "validation": {
            "method": "Tableau VDS figure compared to the identical query against "
                      "Analytics.dw.FactContract over the local SQL connection",
            "lastCheckedOn": "2026-09-20",
            "result": "exact agreement on all five periods and on lifetime",
        },
    }

    doc["caveats"] = [
        "Cancellations restate this DOWNWARD after the fact. Re-running the identical query on "
        "the identical window days later returns less, because contracts inside the window have "
        "since been cancelled. A figure quoted from a screenshot will not reconcile later, and "
        "that is the data behaving correctly, not an error. Always read these as as-of the run "
        "date.",
        "Read through Tableau Cloud, not the SQL warehouse. On 2026-09-20 the two were compared "
        "on the identical cohort and windows and agreed to the cent and to the contract on all "
        "five periods and on lifetime. The Tableau side is the Contracts logical table of "
        "%s, which is one row per contract, and the run aborts if a day's contract count ever "
        "stops matching its distinct-contract-key count." % DS_NAME,
        "%s is a rolling extract. The earliest contract in this cohort is %s, so nothing in "
        "these figures is clipped by that window today - but a cohort with older history would "
        "show a lifetime figure that is short by whatever falls off the back of the extract."
        % (DS_NAME, lifetime.get("earliestContract") or "unknown"),
        "The cohort moves as the 90-day window rolls, so month values shift between refreshes "
        "for two reasons at once: different days AND a different set of practices. Compare "
        "cohorts, not just months.",
        "All five periods are cut from ONE day-grain result set, so they are mutually "
        "consistent by construction. producingProviders is a DISTINCT count WITHIN each period "
        "and therefore does NOT add up across periods: a practice that produced in both weeks is "
        "counted in both.",
        "Weeks start MONDAY.",
        "This is originated treatment volume, not HFD revenue. Cash actually released to "
        "providers runs about 82% of it.",
        "Not computable in HubSpot: every money property there is a lifetime total or a fixed "
        "calendar snapshot with no date dimension.",
        "The join rests on the contact-to-company link, which is the weakest joint in the build.",
    ]

    if lifetime["producingProviders"] < len(pids):
        doc["caveats"].insert(3, "Only %d of the %d sourced practices have originated anything "
                                 "at all." % (lifetime["producingProviders"], len(pids)))

    tmp = os.path.join(DATA, "revenue.json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)
    os.replace(tmp, os.path.join(DATA, "revenue.json"))
    return doc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default=None)
    ap.add_argument("--raw", default=None,
                    help="path to a pre-fetched {days, lifetime, producing} blob, for the case "
                         "where the Tableau read was done through the MCP connector instead of "
                         "a PAT")
    a = ap.parse_args()
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    try:
        doc = run(today, a.raw)
    except TableauError as e:
        print("REVENUE FAIL: %s" % e, file=sys.stderr)
        return 2
    p = doc["periods"]
    print("revenue asOf %s | cohort %d providers, %d producing" %
          (doc["asOf"], doc["sourcedProviders"], doc["producingProviders"]))
    for k in ("thisWeek", "lastWeek", "mtd", "lastMonth", "last90"):
        print("  %-10s %14.2f  %4d contracts  %s" %
              (k, p[k]["value"], p[k]["contracts"], p[k]["range"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
