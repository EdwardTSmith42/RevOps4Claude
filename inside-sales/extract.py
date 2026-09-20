"""
Extract 90 days of Inside Sales engagement from HubSpot into a lead-grain dataset.

Grain: one row per CONTACT touched by an Inside Sales / SDR rep in the window.
Sources: CALL, MEETING_EVENT, EMAIL, NOTE, TASK  + contact & company context.

Writes:
  data/raw_<obj>.jsonl        raw engagement pulls
  data/leads.json             aggregated lead-grain rows for the artifact
  data/summary.json           team/rep rollups + data-quality counters

PII: phone and email are pulled only to identify/dedupe records. They are MASKED
before anything is written to leads.json, which is what feeds the published
artifact. Full detail stays in HubSpot, reachable via the per-row record link.
"""
import datetime as dt
import json, os, re, sys, time, urllib.request, urllib.error
from collections import defaultdict

# How the sourced rule is worded on the dashboard. Shared with build.py so the
# data dictionary cannot drift from the recomputation build.py does for the
# current, already-extracted window.
from sourced_rule import ENROLLED_PREDICATE, ENROLLED_WHY

TOKEN = os.environ.get("HUBSPOT_ACCESS_TOKEN") or os.environ.get("HUBSPOT_SERVICE_KEY")
if not TOKEN:
    sys.exit("No HUBSPOT_ACCESS_TOKEN in environment")

BASE = "https://api.hubapi.com"
HDRS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Rolling 90-day window ending YESTERDAY, so every figure sits on a complete day
# and a refresh needs no edits. Today is deliberately excluded: partial-day counts
# make week-over-week comparisons lie.
_TODAY = dt.date.today()
_END = _TODAY                                 # exclusive upper bound == midnight today
_START = _END - dt.timedelta(days=90)         # 90 complete days, ending yesterday
START = _START.isoformat()
END = _END.isoformat()
_EPOCH = dt.date(1970, 1, 1)
START_MS = (_START - _EPOCH).days * 86400000
END_MS = (_END - _EPOCH).days * 86400000

INSIDE_SALES = {
    "84616314": "Mel Matthews",
    "96412056": "Steven Kelly",
    "88456783": "Gabrielle Nurod",
    "96412059": "Andrea Chacin",
    "96412054": "Taylor Sloan",
}
SDR = {"80632115": "Brandon Slaughter"}
TEAM = {**INSIDE_SALES, **SDR}
TEAM_OF = {**{k: "Inside Sales" for k in INSIDE_SALES}, **{k: "SDR" for k in SDR}}

# Portal-specific disposition GUIDs — verified via get_properties, NOT the public defaults.
DISPOSITION = {
    "f240bbac-87c9-4f6e-bf70-924b57d47db7": "Connected",
    "9d9162e7-6cf3-4944-bf63-4dff82258764": "Busy",
    "73a0d17f-1163-4015-bdd5-ec830791da20": "No answer",
    "a4c4c377-d246-4b32-a13b-75a56a4cd0ff": "Left live message",
    "b2cf5968-551e-4856-9783-52b3da59a7d0": "Left voicemail",
    "2e7360c1-6b71-40e9-ab2b-30ae98a4678c": "Meeting booked",
    "17b47fee-58de-441e-a44c-c6300d46f273": "Wrong number",
}
# A dial where a HUMAN answered. Disposition-based; see the findings brief for why
# the ">5 minute" rule is not usable across these reps.
#
# "Left live message" is included deliberately: despite the name it means a live
# person was reached (a gatekeeper), not a voicemail. Verified on transcripts --
# 116 of 116 have two distinct speakers and 20+ words from the counterparty, with a
# median duration (88s) essentially identical to Connected (95s). Excluding it
# understates the SDR connect rate by ~15 points.
CONNECTED_DISPOSITIONS = {
    "f240bbac-87c9-4f6e-bf70-924b57d47db7",  # Connected
    "2e7360c1-6b71-40e9-ab2b-30ae98a4678c",  # Meeting booked
    "a4c4c377-d246-4b32-a13b-75a56a4cd0ff",  # Left live message (gatekeeper reached)
}
# The narrower subset: reached the person who can actually decide.
DECISION_MAKER_DISPOSITIONS = {
    "f240bbac-87c9-4f6e-bf70-924b57d47db7",  # Connected
    "2e7360c1-6b71-40e9-ab2b-30ae98a4678c",  # Meeting booked
}

# ---- DURATION RULE (Mel Matthews, Laura/Ed/Mel weekly chat 2026-09-14) -------
# "A call connect and a demo connect need to be different lengths IMO.
#  Call connect: >=3 minutes. Demo connect: >=10 minutes."
# Approved by Ed 2026-09-20. Two different bars on purpose: three minutes is long
# enough that a dial cannot be a gatekeeper hand-off, ten minutes is long enough
# that a demo cannot be an AE sitting alone on a recording waiting for a no-show.
CALL_CONNECT_MS = 180000        # 3 minutes
DEMO_CONNECT_MS = 600000        # 10 minutes

# Outbound-dial duration histogram. Upper bound is EXCLUSIVE; the last bucket is
# open-ended. The 3-minute connect line falls exactly on the h3 boundary, so
# h3+h4+h5+h6 == call_connects by construction and the two cannot drift.
DUR_BUCKETS = [
    ("h0", "Under 30 sec",  0,       30000),
    ("h1", "30-60 sec",     30000,   60000),
    ("h2", "1-3 min",       60000,   180000),
    ("h3", "3-5 min",       180000,  300000),
    ("h4", "5-10 min",      300000,  600000),
    ("h5", "10-20 min",     600000,  1200000),
    ("h6", "20 min+",       1200000, None),
]
DUR_KEYS = [b[0] for b in DUR_BUCKETS]


def dur_bucket(ms):
    """Which histogram key this call duration falls in. Never returns None:
    every non-negative duration lands somewhere, so the histogram always sums
    to the outbound dial count."""
    for key, _lab, lo, hi in DUR_BUCKETS:
        if ms >= lo and (hi is None or ms < hi):
            return key
    return DUR_KEYS[0]

_UNOWNED = [0, 0]   # [unowned dialer calls seen, rep recovered from the body]
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA, exist_ok=True)


def post(path, payload, tries=6):
    body = json.dumps(payload).encode()
    for attempt in range(tries):
        req = urllib.request.Request(BASE + path, data=body, headers=HDRS, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 502, 503, 504):
                time.sleep(2 ** attempt)
                continue
            sys.stderr.write(f"HTTP {e.code} on {path}: {e.read()[:400].decode(errors='replace')}\n")
            raise
        except Exception:
            time.sleep(2 ** attempt)
    raise RuntimeError(f"failed after {tries} tries: {path}")


def _search_page(obj, props, filters):
    out, after = [], None
    while True:
        payload = {
            "filterGroups": [{"filters": filters}],
            "properties": props,
            "limit": 100,
            "sorts": [{"propertyName": "hs_timestamp", "direction": "ASCENDING"}],
        }
        if after:
            payload["after"] = after
        d = post(f"/crm/v3/objects/{obj}/search", payload)
        out.extend(d.get("results", []))
        after = d.get("paging", {}).get("next", {}).get("after")
        if not after or len(out) >= 9900:
            return out, (len(out) >= 9900)


def search_all(obj, props, extra_filters):
    """Page a CRM search to exhaustion.

    HubSpot's search API hard-caps paging at 10k results per query. EMAIL volume
    for this team blows past that, so when we hit the cap we recursively split the
    time window into weekly slices and union the results. Without this, email
    counts silently truncate.
    """
    rows, capped = _search_page(obj, props, extra_filters)
    if not capped:
        sys.stderr.write(f"  {obj}: {len(rows)}\n")
        return rows

    sys.stderr.write(f"  {obj}: hit 10k cap — splitting into weekly slices\n")
    non_window = [f for f in extra_filters if f.get("propertyName") != "hs_timestamp"]
    seen, out = set(), []
    week = 7 * 24 * 3600 * 1000
    lo = START_MS
    while lo < END_MS:
        hi = min(lo + week, END_MS)
        slice_rows, still = _search_page(
            obj, props,
            non_window + [{"propertyName": "hs_timestamp", "operator": "BETWEEN",
                           "value": str(lo), "highValue": str(hi - 1)}])
        if still:
            sys.stderr.write(f"    !! week {lo} still capped at 10k — counts are a floor\n")
        for r in slice_rows:
            if r["id"] not in seen:
                seen.add(r["id"])
                out.append(r)
        sys.stderr.write(f"\r    {obj}: {len(out)}")
        sys.stderr.flush()
        lo = hi
    sys.stderr.write(f"\n  {obj}: {len(out)} (weekly union)\n")
    return out


def assoc_batch(from_obj, to_obj, ids):
    """Map from-id -> [to-id]. Chunks of 100."""
    m = defaultdict(list)
    for i in range(0, len(ids), 100):
        chunk = ids[i:i + 100]
        d = post(f"/crm/v4/associations/{from_obj}/{to_obj}/batch/read",
                 {"inputs": [{"id": str(x)} for x in chunk]})
        for row in d.get("results", []):
            fid = str(row.get("from", {}).get("id"))
            for t in row.get("to", []):
                m[fid].append(str(t.get("toObjectId")))
        sys.stderr.write(f"\r  assoc {from_obj}->{to_obj}: {min(i+100,len(ids))}/{len(ids)}")
        sys.stderr.flush()
    sys.stderr.write("\n")
    return m


def batch_read(obj, ids, props):
    out = {}
    ids = list(ids)
    for i in range(0, len(ids), 100):
        chunk = ids[i:i + 100]
        d = post(f"/crm/v3/objects/{obj}/batch/read",
                 {"inputs": [{"id": str(x)} for x in chunk], "properties": props})
        for r in d.get("results", []):
            out[str(r["id"])] = r.get("properties", {})
        sys.stderr.write(f"\r  read {obj}: {len(out)}/{len(ids)}")
        sys.stderr.flush()
    sys.stderr.write("\n")
    return out


def search_companies_by_provider_ids(pids, props):
    """Company records looked up by provider_unique_key.

    PARENT practices carry no contacts of their own, so they never appear in the
    contact -> company map and batch_read cannot reach them. This is the only way
    to pull them in.
    """
    out = {}
    pids = sorted({str(p).strip() for p in pids if str(p).strip()})
    for i in range(0, len(pids), 100):
        chunk, after = pids[i:i + 100], None
        while True:
            body = {
                "filterGroups": [{"filters": [{"propertyName": "provider_unique_key",
                                               "operator": "IN", "values": chunk}]}],
                "properties": props, "limit": 200,
                "sorts": [{"propertyName": "hs_object_id", "direction": "ASCENDING"}],
            }
            if after:
                body["after"] = after
            d = post("/crm/v3/objects/companies/search", body)
            for r in d.get("results", []):
                out[str(r["id"])] = r.get("properties", {})
            after = ((d.get("paging") or {}).get("next") or {}).get("after")
            if not after:
                break
        sys.stderr.write(f"\r  parent lookup: {min(i + 100, len(pids))}/{len(pids)}")
        sys.stderr.flush()
    sys.stderr.write("\n")
    return out


NAME_TO_OWNER = {v.lower(): k for k, v in TEAM.items()}
_REP_IN_BODY = re.compile(r"Line:\s*Sales-\s*([A-Za-z][A-Za-z.'-]+(?: [A-Za-z][A-Za-z.'-]+)+)", re.I)
_REP_FALLBACK = re.compile(r"([A-Z][a-z]+ [A-Z][a-z]+)\s*\(Browser", re.I)

# Each rep's dedicated Aloware line. Derived from the "Line:" label in call bodies
# and verified against calls that DO carry an owner. This is the only way to
# attribute an inbound missed call, because nobody answered so no name is written.
# Note the labels are inconsistent in Aloware ("Sales- Steven Kelly" vs
# "Sales - Brandon Direct Line" vs "Gabrielle's Personal Line"), which is exactly
# why matching on the NUMBER is more reliable than matching on the label text.
LINE_TO_OWNER = {
    "+1 469-214-6446": "88456783",   # Gabrielle's Personal Line
    "+1 469-689-7394": "96412056",   # Sales- Steven Kelly
    "+1 469-402-1963": "96412054",   # Sales- Taylor Sloan
    "+1 469-277-9101": "80632115",   # Sales - Brandon Direct Line
    "+1 469-966-7744": "80632115",   # Sales - Brandon Direct Line (second number)
    "+1 469-273-1112": "96412059",   # Sales- Andrea Chacin
    "+1 469-727-8793": "84616314",   # Sales - Mel's Direct Line
}
# Lines belonging to people outside this team - never attribute these to it.
OFF_TEAM_LINES = {
    "+1 469-750-2908": "Alysha Alley",
    "+1 469-747-0653": "Tenae Walker",
}


def rep_from_call(props):
    """Recover the rep when HubSpot left hubspot_owner_id null.

    Root cause: Aloware writes the engagement at ring time with no acting HubSpot
    user, so owner / created-by / team are all null. Every such record also has
    hs_call_duration = 0 - the owner and the duration arrive together in the
    post-call update, and when that update never lands you get an orphan stub.

    Two recovery paths, in order:
      1. The body names the rep: "Steven Kelly (Browser / Apps) has made an
         outbound call ...". Covers outbound work.
      2. The rep's own line number. Required for INBOUND missed calls, where
         nobody answered so the body carries no name at all - only
         "Line: Sales - Brandon Direct Line - (469) 277-9101".
    Direction decides which end of the call is the rep: from-number on outbound,
    to-number on inbound.
    """
    body = props.get("hs_call_body")
    if body:
        txt = re.sub(r"<[^>]+>", " ", body)
        for pat in (_REP_IN_BODY, _REP_FALLBACK):
            m = pat.search(txt)
            if m:
                owner = NAME_TO_OWNER.get(" ".join(m.group(1).split()).lower())
                if owner:
                    return owner
    direction = props.get("hs_call_direction")
    line = props.get("hs_call_from_number") if direction == "OUTBOUND" else props.get("hs_call_to_number")
    line = (line or "").strip()
    if line in OFF_TEAM_LINES:
        return None
    return LINE_TO_OWNER.get(line)


def is_missed_inbound(props):
    """An inbound ring nobody picked up: no rep did anything, so it is demand,
    not activity. Counted separately and kept out of dials and connects."""
    return (props.get("hs_call_direction") == "INBOUND"
            and not props.get("hs_call_disposition")
            and int(props.get("hs_call_duration") or 0) == 0)


def owner_filter():
    return {"propertyName": "hubspot_owner_id", "operator": "IN", "values": list(TEAM)}


def window_filter(prop="hs_timestamp"):
    return {"propertyName": prop, "operator": "BETWEEN",
            "value": str(START_MS), "highValue": str(END_MS)}


def mask_email(e):
    if not e or "@" not in e:
        return ""
    local, _, dom = e.partition("@")
    keep = local[:1] if local else ""
    return f"{keep}{'*' * max(len(local) - 1, 1)}@{dom}"


def main():
    print(f"Window {START} .. {END} (exclusive)  |  {len(TEAM)} reps", file=sys.stderr)

    print("\n[1/6] engagements", file=sys.stderr)
    CALL_PROPS = [
        "hs_timestamp", "hs_call_duration", "hs_call_disposition", "hs_call_direction",
        "hs_call_source", "hs_activity_type", "hubspot_owner_id", "hs_call_has_transcript",
        "hs_call_title", "hs_call_body", "hs_call_summary", "hs_call_owner_talk_time",
        # needed to attribute unowned calls by the rep's own line number
        "hs_call_from_number", "hs_call_to_number",
    ]
    calls = search_all("calls", CALL_PROPS, [window_filter(), owner_filter()])

    # Dialer calls frequently arrive with a null owner. Pull those separately and
    # attribute them from the body, which names the rep and their line. Without this
    # the three reps who dial from their own Aloware lines report zero dials.
    orphans = search_all("calls", CALL_PROPS, [
        window_filter(),
        {"propertyName": "hubspot_owner_id", "operator": "NOT_HAS_PROPERTY"},
    ])
    recovered, seen_ids = 0, {c["id"] for c in calls}
    _unowned_total = len(orphans)
    for c in orphans:
        if c["id"] in seen_ids:
            continue
        owner = rep_from_call(c.get("properties", {}))
        if owner:
            c["properties"]["hubspot_owner_id"] = owner
            c["properties"]["_owner_recovered"] = "true"
            calls.append(c)
            recovered += 1
    _UNOWNED[0], _UNOWNED[1] = len(orphans), recovered
    print(f"  calls: {len(calls)} ({recovered} recovered from {len(orphans)} unowned)",
          file=sys.stderr)

    meetings = search_all("meetings", [
        "hs_timestamp", "hs_meeting_title", "hs_meeting_outcome", "hs_activity_type",
        "hubspot_owner_id", "hs_meeting_start_time", "hs_meeting_end_time", "hs_meeting_source",
        "hs_meeting_recording_duration",
    ], [window_filter(), owner_filter()])

    try:
        emails = search_all("emails", [
            "hs_timestamp", "hs_email_direction", "hs_email_status", "hs_email_subject",
            "hubspot_owner_id",
        ], [window_filter(), owner_filter()])
    except Exception as e:
        sys.stderr.write(f"  emails unavailable: {e}\n")
        emails = []

    try:
        notes = search_all("notes", ["hs_timestamp", "hubspot_owner_id"],
                           [window_filter(), owner_filter()])
    except Exception:
        notes = []

    try:
        tasks = search_all("tasks", [
            "hs_timestamp", "hs_task_type", "hs_task_status", "hs_task_subject", "hubspot_owner_id",
        ], [window_filter(), owner_filter()])
    except Exception:
        tasks = []

    for name, rows in [("calls", calls), ("meetings", meetings), ("emails", emails),
                       ("notes", notes), ("tasks", tasks)]:
        with open(os.path.join(DATA, f"raw_{name}.jsonl"), "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        print(f"  {name}: {len(rows)}", file=sys.stderr)

    print("\n[2/6] engagement -> contact associations", file=sys.stderr)
    amap = {}
    for name, rows, api in [("calls", calls, "calls"), ("meetings", meetings, "meetings"),
                            ("emails", emails, "emails"), ("notes", notes, "notes"),
                            ("tasks", tasks, "tasks")]:
        if rows:
            amap[name] = assoc_batch(api, "contacts", [r["id"] for r in rows])
        else:
            amap[name] = {}

    contact_ids = set()
    for m in amap.values():
        for v in m.values():
            contact_ids.update(v)
    print(f"  distinct contacts touched: {len(contact_ids)}", file=sys.stderr)

    print("\n[3/6] contacts", file=sys.stderr)
    contacts = batch_read("contacts", contact_ids, [
        "firstname", "lastname", "email", "jobtitle", "company", "city", "state",
        "lifecyclestage", "hubspot_owner_id", "createdate", "lastmodifieddate",
        "lead_source", "first_touch_lead_source", "last_touch_lead_source",
        "hs_analytics_source", "hs_object_source_label", "hs_object_source_detail_1",
        "provid_test", "hs_lead_status", "notes_last_contacted", "num_contacted_notes",
        "associatedcompanyid", "clay_source_details", "clay_scraped_date",
        "hs_last_sales_activity_type", "hs_last_sales_activity_date",
        "demo_booking_status", "ae_demo_attended", "demo_closed_won_date",
        "demo_closed_lost_date", "industry_vertical", "unqualified_reason",
        "marketing_acquisition_channel", "hs_latest_sequence_enrolled",
    ])

    print("\n[4/6] contact -> company", file=sys.stderr)
    c2co = assoc_batch("contacts", "companies", list(contact_ids))
    company_ids = {cid for v in c2co.values() for cid in v}
    companies = batch_read("companies", company_ids, [
        "name", "city", "state", "industry", "domain", "createdate", "lifecyclestage",
        "enrollment_date", "provider_unique_key", "provider_activated_date",
        "ae_demo_converted_by", "ae_evaluation_status", "total_loan_applications",
        "total_loan_activations", "total_loan_volume", "last_month_loan_volume",
        "total_contract_value", "contract_value_month_to_date", "total_activations",
        "provider_workflow", "provider_status", "hubspot_owner_id", "parent_provider",
        # Practice-identity fields (Ed, 2026-09-20: "check legalname, practice name
        # and dba when matching"). Provider ID alone under-dedupes: the same
        # practice is routinely entered twice, once before it has an ID and once
        # after, or once per location under one shared legal entity.
        "legal_business_name", "practice_name", "doing_business_as",
    ]) if company_ids else {}
    print(f"  companies: {len(companies)}", file=sys.stderr)

    def in_window(d):
        return bool(d) and START <= d[:10] < END

    # ---- practice identity (Ed, 2026-09-20) --------------------------------
    # "Be sure to check legalname, practice name and dba when matching."
    #
    # A LOCATION is a company record. A PRACTICE is the business behind it, and
    # one practice routinely owns several company records: a parent group record
    # plus each treating location, or the same practice entered twice under two
    # Provider IDs. Deduping on Provider ID alone therefore counts locations and
    # calls them practices. This resolver builds practice identity by joining
    # company records that are demonstrably the same business, on two signals:
    #
    #   1. the same Provider ID
    #   2. a matching normalised name on ANY of the four name fields --
    #      Company name, Legal Business Name, Practice Name, Doing Business As.
    #      Cross-field on purpose: one record's Legal Business Name is routinely
    #      another record's Practice Name for the same business.
    #
    # Normalisation lowercases, folds punctuation and "&", and strips entity
    # suffixes and clinical credentials (Inc, LLC, PLLC, PC, PA, DDS, DMD, ...)
    # so "Perla Dental PC" and "Perla Dental " are one name.
    #
    # NOT parent_provider. That link is what LOCATIONS already rolls up, and it is
    # the wrong signal for practice identity: Amulet Management LLC is the parent
    # of 48 records that include Williams Orthodontics in Gilbert AZ and Jensen
    # Orthodontics in Las Cruces NM. That is one OWNER, not one practice. Joining
    # on the parent link would collapse a whole DSO footprint into a single
    # practice and make the locations/practices gap meaningless.
    #
    # CORROBORATION GUARD - this is the load-bearing one. A shared name only joins
    # two records when the shared name actually appears in BOTH records' own
    # Company name. The reason is that Practice Name is a defaulted field in this
    # portal: 48 unrelated records carry practice_name "Children's Choice Dental
    # Care Stockton", and 7 unrelated Brooklyn practices carry "Avenue D Dental",
    # each copied from one sibling. Requiring the name to show up in the company
    # name rejects all of those, while still joining the real cases:
    #   "Bayou Orthodontics" (legal name on 7 records whose company names are
    #   "Bayou Orthodontics - Harvey", "- Baton Rouge", ... ) -> one practice.
    #   "Perla Dental" (parent "Perla Dental - Parent", child "Perla Dental of
    #   Farmers Branch") -> one practice.
    # A blunt "reject any name shared by more than N providers" threshold cannot
    # separate those two cases: the junk groups and the real multi-location brands
    # are the same size. Corroboration can.
    #
    # NAME_SPAN_MAX is only a runaway backstop against a single name swallowing the
    # book. Every name rejected by either guard is reported in
    # summary.practice_identity so neither can silently throw away a real match.
    NAME_SPAN_MAX = 25
    _SUFFIX = re.compile(
        r"\b(inc|llc|l l c|pllc|pc|pa|pl|plc|ltd|limited|co|corp|corporation|"
        r"company|group|dds|dmd|md|do|dpm|od|dc|the|and|of)\b")
    NAME_FIELDS = ("name", "legal_business_name", "practice_name", "doing_business_as")

    # Category words. A name built ONLY from these describes an industry, not a
    # business: "Family Dental Care" is not evidence that two records are the same
    # practice, while "Perla Dental" is, because "perla" is not a category word.
    # Without this, suffix stripping alone turns "Company Dental" into "dental"
    # and every dental record in the book joins one practice.
    _CATEGORY = {
        "dental", "dentistry", "dentist", "dentists", "ortho", "orthodontic",
        "orthodontics", "orthodontist", "endodontic", "endodontics", "periodontic",
        "periodontics", "prosthodontic", "prosthodontics", "oral", "surgery",
        "surgical", "surgeons", "surgeon", "medical", "medicine", "health",
        "healthcare", "care", "clinic", "clinics", "center", "centers", "centre",
        "associates", "association", "practice", "practices", "family", "smile",
        "smiles", "aesthetic", "aesthetics", "spa", "med", "plastic", "cosmetic",
        "vision", "eye", "optical", "foot", "ankle", "podiatry", "chiropractic",
        "veterinary", "hospital", "office", "offices", "pediatric", "pediatrics",
        "implant", "implants", "wellness", "institute", "partners", "management",
        "services", "holdings", "specialists", "specialty", "advanced", "modern",
        "premier", "complete", "total", "general", "new", "first", "best",
    }

    def norm_name(v):
        """Normalised practice name, or '' when the name is not identity evidence.

        Returns '' for anything under 4 characters and for any name whose every
        remaining token is a category word, because neither can tell two
        businesses apart."""
        v = (v or "").lower().replace("&", " and ")
        v = re.sub(r"[^a-z0-9]+", " ", v)
        v = _SUFFIX.sub(" ", v)
        v = re.sub(r"\s+", " ", v).strip()
        if len(v) < 4:
            return ""
        toks = v.split()
        if all(t in _CATEGORY for t in toks):
            return ""
        return v

    def _props(cid, extra=None):
        if cid in companies:
            return companies[cid]
        if extra and cid in extra:
            return extra[cid]
        return {}

    def _pid_of(cid, extra=None):
        return str(_props(cid, extra).get("provider_unique_key") or "").strip()

    def build_practice_index(cids, extra=None):
        """Union-find over company records -> {company_id: practice_key}.

        The practice key is the smallest company id in the group, so it is stable
        for a given input set and reproducible by hand from the same records.
        Returns (key_by_company, report).
        """
        cids = sorted(set(cids))
        parent = {c: c for c in cids}

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)

        by_pid = defaultdict(list)
        for c in cids:
            pid = _pid_of(c, extra)
            if pid:
                by_pid[pid].append(c)
        for group in by_pid.values():
            for c in group[1:]:
                union(group[0], c)

        # Every record's OWN company name, normalised, as a token set. This is what
        # a candidate name has to be corroborated against.
        own = {c: set(norm_name(_props(c, extra).get("name")).split()) for c in cids}

        by_name = defaultdict(set)
        for c in cids:
            pr = _props(c, extra)
            for f in NAME_FIELDS:
                n = norm_name(pr.get(f))
                if n:
                    by_name[n].add(c)
        rejected, name_joins = [], 0
        for n, group in sorted(by_name.items()):
            if len(group) < 2:
                continue
            toks = set(n.split())
            # Corroboration: keep only the records whose own Company name contains
            # every token of the shared name. A Practice Name copied across
            # unrelated siblings fails here; a real brand shared by its locations
            # passes, because each location is named after the brand.
            ok = sorted(c for c in group if toks <= own[c])
            if len(ok) < 2:
                rejected.append({
                    "normalised_name": n, "company_records": len(group),
                    "distinct_provider_ids": len({_pid_of(c, extra) for c in group} - {""}),
                    "reason": "not corroborated - the shared name does not appear in the "
                              "Company name of two or more of these records, so it is a "
                              "copied or defaulted value, not evidence of one business",
                    "company_names": sorted({_props(c, extra).get("name") or "" for c in group})[:8]})
                continue
            if len(ok) > NAME_SPAN_MAX:
                rejected.append({
                    "normalised_name": n, "company_records": len(ok),
                    "distinct_provider_ids": len({_pid_of(c, extra) for c in ok} - {""}),
                    "reason": "runaway - one name would join more than %d records; treated "
                              "as a trade name rather than one business" % NAME_SPAN_MAX,
                    "company_names": sorted({_props(c, extra).get("name") or "" for c in ok})[:8]})
                continue
            for c in ok[1:]:
                union(ok[0], c)
                name_joins += 1

        key_by_co = {c: find(c) for c in cids}
        groups = defaultdict(list)
        for c, k in key_by_co.items():
            groups[k].append(c)
        merged = sorted(
            ({"practice_key": k,
              "company_records": sorted(v),
              "provider_ids": sorted({_pid_of(c, extra) for c in v} - {""}),
              "names": sorted({(_props(c, extra).get("name") or "") for c in v})}
             for k, v in groups.items() if len(v) > 1),
            key=lambda g: g["practice_key"])
        return key_by_co, {
            "company_records": len(cids),
            "practices": len(groups),
            "multi_record_practices": len(merged),
            "name_joins_used": name_joins,
            "rejected_names": rejected,
            "merged_groups": merged,
        }

    PRACTICE_KEY, PRACTICE_REPORT = build_practice_index(companies.keys())
    print(f"  practice identity: {PRACTICE_REPORT['company_records']} company records "
          f"-> {PRACTICE_REPORT['practices']} practices "
          f"({PRACTICE_REPORT['multi_record_practices']} span more than one record)",
          file=sys.stderr)

    def pick_company(co_ids):
        """A contact can be linked to hundreds of companies (bad merges / shared
        domains). Prefer the one that actually looks like the practice: enrolled in
        window > has a provider id > earliest created."""
        if not co_ids:
            return None
        scored = []
        for cid_ in co_ids:
            p = companies.get(cid_, {})
            scored.append((
                0 if in_window(p.get("enrollment_date")) else 1,
                0 if p.get("provider_unique_key") else 1,
                p.get("createdate") or "9999",
                cid_,
            ))
        scored.sort()
        return scored[0][3]

    def is_demo(p):
        """Demo == meeting title contains 'demo'.

        This is the definition behind Laura's existing "Demos" dashboard (21888050)
        and reproduces it exactly. The hs_activity_type picklist is set on only ~32%
        of demo meetings, so it badly undercounts.
        """
        return "demo" in (p.get("hs_meeting_title") or "").lower()

    def is_demo_performed(p):
        # Same 5-minute recording threshold the existing dashboard uses for "performed".
        # SECONDARY now, not the headline. Kept so our number still ties to Laura's
        # report 345792760 and so a reader can see what the old gate was counting.
        try:
            return is_demo(p) and int(p.get("hs_meeting_recording_duration") or 0) > 300000
        except (TypeError, ValueError):
            return False

    def is_demo_connect(p):
        """DEMO CONNECT: a demo-titled meeting whose recording ran >= 10 minutes.

        This does NOT change the Demos count. Demos stays every demo-titled
        meeting - Laura's house definition, which reproduces her Demos dashboard
        (21888050) exactly. The 10-minute bar splits the QUALITY beneath that
        count: at or over 10 minutes the demo was connected; under 10 minutes it
        is a CANDIDATE no-show, because the recorder keeps running while the AE
        waits alone and 88 of 97 known no-shows cleared the old 5-minute gate.
        """
        try:
            return (is_demo(p)
                    and int(p.get("hs_meeting_recording_duration") or 0) >= DEMO_CONNECT_MS)
        except (TypeError, ValueError):
            return False

    print("\n[5/6] aggregate", file=sys.stderr)
    lead = defaultdict(lambda: {
        "dials": 0, "out_dials": 0, "in_dials": 0, "missed_inbound": 0,
        "connects": 0, "dm_connects": 0,
        # call_connects  = the TEAM's rule: an outbound dialer call >= 3 minutes.
        # connects       = HubSpot's rule: the disposition set. Both are kept, and
        #                  both are documented, because HubSpot's own automation
        #                  (hs_connected_count, workflow 1662944670, the SDR
        #                  pipeline) runs on the disposition and a reader comparing
        #                  this page to a HubSpot report must be able to see why
        #                  the two numbers differ.
        "call_connects": 0,
        # demo_connects  = demo-titled meetings whose recording ran >= 10 minutes.
        # demos          = ALL demo-titled meetings, unchanged.
        "demo_connects": 0,
        # hist[i] = outbound dials whose duration falls in DUR_BUCKETS[i].
        "hist": [0] * len(DUR_BUCKETS),
        "dial_talk_ms": 0, "conversations": 0,
        "meetings": 0, "demos": 0, "demos_performed": 0, "emails_out": 0, "emails_in": 0,
        "notes": 0, "tasks": 0, "meeting_recordings": 0,
        "first_touch": None, "first_outreach": None, "last_touch": None,
        "reps": set(), "teams": set(),
        "dispositions": defaultdict(int), "call_links": [],
        "per": defaultdict(lambda: defaultdict(int)),
        # PER-DAY ACTIVITY BUCKETS: "YYYY-MM-DD" -> {key: count}, only non-zero
        # keys, only days that saw activity. Every increment below sits on the
        # SAME line as the flat total it mirrors and is gated by the SAME
        # predicate (is_dial / is_missed_inbound / CONNECTED_DISPOSITIONS /
        # DECISION_MAKER_DISPOSITIONS / is_demo / is_demo_performed), so summing
        # one key across all days reproduces the flat 90-day total exactly.
        # That identity is asserted at the bottom of the aggregate step.
        # The flat totals stay: they are the 90-day figures and other code reads them.
        "days": defaultdict(lambda: defaultdict(int)),
        # PER-REP PER-DAY BUCKETS: rep -> "YYYY-MM-DD" -> {key: count}.
        # `per` above is the same split with no date on it, which is fine for a
        # 90-day page and useless for a period-switching one: the rep scorecard
        # and the two-seats cards would report each rep's FULL 90-day activity on
        # whichever contacts happened to be touched in the selected week. Every
        # increment below sits on the same line as its `per` counterpart and is
        # gated by the same predicate, so summing a key across days reproduces
        # per[rep][key] exactly. Asserted at the bottom of the aggregate step.
        "pd": defaultdict(lambda: defaultdict(lambda: defaultdict(int))),
    })

    # Per-rep counters aggregated from the ENGAGEMENT records themselves, not from
    # lead rows. A lead touched by two reps must not credit its full totals to both.
    rep_stat = defaultdict(lambda: defaultdict(int))
    rep_leads = defaultdict(set)

    def touch(cid, ts, owner, outreach=False):
        """Record an engagement against a lead.

        TWO clocks, deliberately. `first_touch` is the first activity of ANY
        kind and is what the lead table and the CSV display -- it keeps its old
        meaning. `first_outreach` is the first time the team actually REACHED
        OUT, and it is the only one the sourced test may use (VP decision,
        2026-09).

        Callers pass outreach=True for an outbound dial, an outbound email, a
        meeting, or an inbound dial somebody answered. Three mechanisms are
        deliberately excluded, because each of them let us claim we had sourced
        a practice nobody on the team had actually contacted:
          * NOTES and TASKS -- internal staff-to-staff records ("Enrollment
            Spreadsheet", "@Tia Bel This is for 4 locations"). Writing a note to
            a colleague is not outreach to the prospect.
          * INBOUND EMAIL with no outbound email at all -- the prospect wrote to
            us; we never wrote to them.
          * UNANSWERED INBOUND RINGS (is_missed_inbound) -- the prospect called
            and nobody picked up. Colesville Dental Center rang Gabrielle
            Nurod's line five times unanswered, duration 0, no disposition, and
            we were counting that as us having sourced them.
        """
        L = lead[cid]
        if ts:
            if L["first_touch"] is None or ts < L["first_touch"]:
                L["first_touch"] = ts
            if outreach and (L["first_outreach"] is None or ts < L["first_outreach"]):
                L["first_outreach"] = ts
            if L["last_touch"] is None or ts > L["last_touch"]:
                L["last_touch"] = ts
        if owner in TEAM:
            L["reps"].add(TEAM[owner])
            L["teams"].add(TEAM_OF[owner])

    # Engagements with no hs_timestamp cannot exist here - window_filter() selects
    # on hs_timestamp BETWEEN - but if one ever did it would break the
    # sum-of-days == flat-total identity silently. Send it to a scratch bucket
    # that is never emitted and count it, so it shows up instead of hiding.
    _no_ts = defaultdict(int)

    def dayb(L, ts):
        """The per-day bucket for this engagement.

        Day = the UTC calendar date of hs_timestamp, sliced exactly the way
        in_window() and the sourced test slice their dates, so bucket days and
        the 90-day window agree by construction.
        """
        if not ts:
            _no_ts["n"] += 1
            return defaultdict(int)
        return L["days"][ts[:10]]

    def repb(L, rep, ts):
        """The per-rep per-day bucket. Same day slicing as dayb()."""
        if not ts:
            _no_ts["n"] += 1
            return defaultdict(int)
        return L["pd"][rep][ts[:10]]

    for c in calls:
        p = c.get("properties", {})
        owner = p.get("hubspot_owner_id")
        rep = TEAM.get(owner)
        src, direction = p.get("hs_call_source"), p.get("hs_call_direction")
        dur = int(p.get("hs_call_duration") or 0)
        disp_ = p.get("hs_call_disposition")
        if rep:
            _missed = is_missed_inbound(p)
            if _missed:
                rep_stat[rep]["missed_inbound"] += 1
            if (src == "INTEGRATIONS_PLATFORM"
                    and direction in ("OUTBOUND", "INBOUND") and not _missed):
                rep_stat[rep]["in_dials" if direction == "INBOUND" else "out_dials"] += 1
                rep_stat[rep]["dials"] += 1
                if disp_ in CONNECTED_DISPOSITIONS:
                    rep_stat[rep]["connects"] += 1
                if disp_ in DECISION_MAKER_DISPOSITIONS:
                    rep_stat[rep]["dm_connects"] += 1
                if direction == "OUTBOUND" and dur >= CALL_CONNECT_MS:
                    rep_stat[rep]["call_connects"] += 1
                if direction == "OUTBOUND":
                    rep_stat[rep]["h_" + dur_bucket(dur)] += 1
                if dur >= 120000:
                    rep_stat[rep]["conversations"] += 1
                rep_stat[rep]["dial_talk_ms"] += dur
            else:
                rep_stat[rep]["meeting_recordings"] += 1
        missed = is_missed_inbound(p)
        is_dial = (src == "INTEGRATIONS_PLATFORM"
                   and direction in ("OUTBOUND", "INBOUND")
                   and not missed)
        # CALL CONNECT (team rule, Mel 2026-09-14): an OUTBOUND dialer call that
        # ran three minutes or longer. Outbound only - an inbound call somebody
        # answered is demand, not a connect the rep manufactured - and it is a
        # strict subset of out_dials, so it can never exceed the dial count.
        is_out_dial = is_dial and direction == "OUTBOUND"
        is_call_connect = is_out_dial and dur >= CALL_CONNECT_MS
        dbk = dur_bucket(dur) if is_out_dial else None
        for cid in amap["calls"].get(c["id"], []):
            L = lead[cid]
            B = dayb(L, p.get("hs_timestamp"))
            if rep:
                rep_leads[rep].add(cid)
            # is_dial means outbound, or inbound that somebody actually answered.
            # An unanswered inbound ring and a demo recording are both excluded,
            # so neither can start the outreach clock.
            touch(cid, p.get("hs_timestamp"), p.get("hubspot_owner_id"), outreach=is_dial)
            if missed:
                L["missed_inbound"] += 1
                B["mi"] += 1
            if rep:
                RB = repb(L, rep, p.get("hs_timestamp"))
                if is_dial:
                    L["per"][rep]["id" if direction == "INBOUND" else "d"] += 1
                    RB["id" if direction == "INBOUND" else "d"] += 1
                else:
                    L["per"][rep]["mr"] += 1
                    RB["mr"] += 1
                if is_dial and disp_ in CONNECTED_DISPOSITIONS:
                    L["per"][rep]["c"] += 1
                    RB["c"] += 1
                if is_dial and disp_ in DECISION_MAKER_DISPOSITIONS:
                    L["per"][rep]["dc"] += 1
                    RB["dc"] += 1
                if is_call_connect:
                    L["per"][rep]["cc"] += 1
                    RB["cc"] += 1
            # Motion split. A demo recording has no direction and is never a dial.
            if is_dial:
                L["in_dials" if direction == "INBOUND" else "out_dials"] += 1
                B["id" if direction == "INBOUND" else "d"] += 1
            if is_out_dial:
                # Duration histogram. Emitted as BUCKET COUNTS per day, never raw
                # durations, so the payload stays compact. Exactly one key fires
                # per outbound dial, so the seven keys sum to out_dials.
                L["hist"][DUR_KEYS.index(dbk)] += 1
                B[dbk] += 1
            if is_call_connect:
                L["call_connects"] += 1
                B["cc"] += 1
            if is_dial:
                L["dials"] += 1
                L["dial_talk_ms"] += dur
                disp = p.get("hs_call_disposition")
                if disp:
                    L["dispositions"][DISPOSITION.get(disp, disp)] += 1
                if disp in CONNECTED_DISPOSITIONS:
                    L["connects"] += 1
                    B["c"] += 1
                if disp in DECISION_MAKER_DISPOSITIONS:
                    L["dm_connects"] += 1
                    B["dc"] += 1
                if dur >= 120000:
                    L["conversations"] += 1
            else:
                # meeting recording surfacing as a CALL row
                L["meeting_recordings"] += 1
            if p.get("hs_call_has_transcript") == "true":
                L["call_links"].append(c["id"])

    for m in meetings:
        p = m.get("properties", {})
        rep = TEAM.get(p.get("hubspot_owner_id"))
        demo_f, perf_f = is_demo(p), is_demo_performed(p)
        conn_f = is_demo_connect(p)
        if rep:
            rep_stat[rep]["meetings"] += 1
            if demo_f:
                rep_stat[rep]["demos"] += 1
            if perf_f:
                rep_stat[rep]["demos_performed"] += 1
            if conn_f:
                rep_stat[rep]["demo_connects"] += 1
        for cid in amap["meetings"].get(m["id"], []):
            L = lead[cid]
            B = dayb(L, p.get("hs_timestamp"))
            if rep:
                rep_leads[rep].add(cid)
            touch(cid, p.get("hs_timestamp"), p.get("hubspot_owner_id"), outreach=True)
            if rep:
                RB = repb(L, rep, p.get("hs_timestamp"))
                L["per"][rep]["m"] += 1
                RB["m"] += 1
                if demo_f:
                    L["per"][rep]["dm"] += 1
                    RB["dm"] += 1
                if perf_f:
                    L["per"][rep]["dp"] += 1
                    RB["dp"] += 1
                if conn_f:
                    L["per"][rep]["dn"] += 1
                    RB["dn"] += 1
            L["meetings"] += 1
            B["m"] += 1
            if demo_f:
                L["demos"] += 1
                B["dm"] += 1
            if perf_f:
                L["demos_performed"] += 1
                B["dp"] += 1
            if conn_f:
                L["demo_connects"] += 1
                B["dn"] += 1

    for e in emails:
        p = e.get("properties", {})
        rep = TEAM.get(p.get("hubspot_owner_id"))
        inbound = (p.get("hs_email_direction") or "").upper().startswith("INCOMING")
        if rep:
            rep_stat[rep]["emails_in" if inbound else "emails_out"] += 1
        for cid in amap["emails"].get(e["id"], []):
            L = lead[cid]
            B = dayb(L, p.get("hs_timestamp"))
            if rep:
                rep_leads[rep].add(cid)
            # An email the PROSPECT sent us is not outreach we made.
            touch(cid, p.get("hs_timestamp"), p.get("hubspot_owner_id"),
                  outreach=not inbound)
            if rep:
                repb(L, rep, p.get("hs_timestamp"))["ei" if inbound else "eo"] += 1
                L["per"][rep]["ei" if inbound else "eo"] += 1
            if inbound:
                L["emails_in"] += 1
                B["ei"] += 1
            else:
                L["emails_out"] += 1
                B["eo"] += 1

    # Notes and tasks move first_touch but never first_outreach: they are
    # internal records, not contact with the prospect. outreach defaults to False.
    for n in notes:
        p = n.get("properties", {})
        for cid in amap["notes"].get(n["id"], []):
            touch(cid, p.get("hs_timestamp"), p.get("hubspot_owner_id"))
            lead[cid]["notes"] += 1
            dayb(lead[cid], p.get("hs_timestamp"))["n"] += 1

    for t in tasks:
        p = t.get("properties", {})
        for cid in amap["tasks"].get(t["id"], []):
            touch(cid, p.get("hs_timestamp"), p.get("hubspot_owner_id"))
            lead[cid]["tasks"] += 1
            dayb(lead[cid], p.get("hs_timestamp"))["t"] += 1

    def segment_of(props):
        d = (props.get("hs_object_source_detail_1") or "").strip().lower()
        label = (props.get("hs_object_source_label") or "").strip().upper()
        if d == "cli_lr" or props.get("clay_source_details"):
            return "Scrape (Clay)"
        if d == "zite":
            return "Web form (Zite)"
        if d == "referral rock":
            return "Referral (Referral Rock)"
        if d == "aloware cloud contact center":
            return "Dialer-created (Aloware)"
        if "contact us" in d:
            return "Web form (Contact us)"
        if d.endswith(".csv") or d.endswith(".xlsx") or label == "IMPORT":
            return "List import"
        if "form" in d:
            return "Web form (other)"
        if label == "CRM_UI":
            return "Manually created"
        if label == "CONVERSATIONS":
            return "Inbound chat/conversation"
        if not d and not label:
            return "Unknown"
        return f"Other ({d or label.title()})"

    rows = []
    for cid, L in lead.items():
        p = contacts.get(cid, {})
        co_ids = c2co.get(cid, [])
        assoc_co = (p.get("associatedcompanyid") or "").strip()
        best = assoc_co if assoc_co in companies else pick_company(co_ids)
        co = companies.get(best, {}) if best else {}
        # enrollment_date is stamped by workflow 1820099735 off the 06:31 CT nightly
        # ELI sync, so it lands one calendar day after the real enrollment.
        raw_enroll = co.get("enrollment_date") or ""
        enroll_dt = ""
        if raw_enroll:
            try:
                enroll_dt = (dt.date.fromisoformat(raw_enroll[:10]) - dt.timedelta(days=1)).isoformat()
            except ValueError:
                enroll_dt = raw_enroll[:10]
        enrolled_now = in_window(enroll_dt)
        # "Sourced" = the team REACHED OUT to this lead on or before the day its
        # practice enrolled. first_outreach, NOT first_touch: an internal note, an
        # inbound email we never answered, and an inbound ring nobody picked up all
        # move first_touch, and none of them is us sourcing anybody. On the
        # 2026-06-11..2026-09-08 window this drops 15 contacts and 10 practices
        # (144 -> 134 sourced practices). See touch() for the full reasoning.
        sourced = bool(enrolled_now and L["first_outreach"]
                       and L["first_outreach"][:10] <= enroll_dt[:10])
        fn, ln = (p.get("firstname") or "").strip(), (p.get("lastname") or "").strip()
        rows.append({
            "contact_id": cid,
            "name": (fn + " " + ln).strip() or "(no name)",
            "job_title": p.get("jobtitle") or "",
            "company": co.get("name") or p.get("company") or "",
            "company_id": best or "",
            "company_count": len(co_ids),
            "company_link_ok": len(co_ids) == 1,
            "enrollment_date": enroll_dt[:10] if enroll_dt else "",
            "enrolled_in_window": enrolled_now,
            "sourced": sourced,
            "provider_workflow": co.get("provider_workflow") or "",
            "provider_id": co.get("provider_unique_key") or "",
            # location_key = this company RECORD. practice_key = the BUSINESS behind
            # it, after joining records that share a Provider ID or a corroborated
            # name on any of Company name / Legal Business Name / Practice Name /
            # Doing Business As. Counting distinct location_key gives locations;
            # counting distinct practice_key gives practices. Both ship so the
            # browser can show Mel both figures without recomputing either.
            "location_key": best or "",
            "practice_key": PRACTICE_KEY.get(best, "") if best else "",
            "clay_source": p.get("clay_source_details") or "",
            "mkt_channel": p.get("marketing_acquisition_channel") or "",
            "sequence": p.get("hs_latest_sequence_enrolled") or "",
            "inbound_signal": p.get("hs_last_sales_activity_type") or "",
            "demo_booking_status": p.get("demo_booking_status") or "",
            "ae_demo_attended": p.get("ae_demo_attended") or "",
            "demo_won": (p.get("demo_closed_won_date") or "")[:10],
            "demo_lost": (p.get("demo_closed_lost_date") or "")[:10],
            "vertical": p.get("industry_vertical") or "",
            "unqualified_reason": p.get("unqualified_reason") or "",
            "ae_credited": co.get("ae_demo_converted_by") or "",
            "ae_eval_status": co.get("ae_evaluation_status") or "",
            "loan_apps": co.get("total_loan_applications") or "",
            "loan_activations": co.get("total_loan_activations") or "",
            "loan_volume": co.get("total_loan_volume") or "",
            "last_month_volume": co.get("last_month_loan_volume") or "",
            "contract_value": co.get("total_contract_value") or "",
            "contract_value_mtd": co.get("contract_value_month_to_date") or "",
            "city": p.get("city") or co.get("city") or "",
            "state": p.get("state") or co.get("state") or "",
            "email_masked": mask_email(p.get("email")),
            "segment": segment_of(p),
            "source_detail": p.get("hs_object_source_detail_1") or "",
            "lead_source": p.get("lead_source") or "",
            "lifecycle": p.get("lifecyclestage") or "",
            "lead_status": p.get("hs_lead_status") or "",
            "contact_owner": TEAM.get(p.get("hubspot_owner_id"), ""),
            "contact_owner_id": p.get("hubspot_owner_id") or "",
            "created": p.get("createdate") or "",
            "provid": p.get("provid_test") or "",
            "enrolled": bool(p.get("provid_test")),
            "reps": sorted(L["reps"]),
            "per": {k: dict(v) for k, v in L["per"].items()},
            # Per-day buckets. A day appears only if something happened on it, a
            # key only if its count is non-zero. A CALL row that is really a
            # meeting recording touches no bucket key, so its day is dropped here
            # rather than emitted as an empty object.
            "days": {d: dict(v) for d, v in sorted(L["days"].items()) if v},
            # The same split as "per", with a date on it. Same emptiness rule.
            "pd": {rep: {d: dict(v) for d, v in sorted(days.items()) if v}
                   for rep, days in sorted(L["pd"].items()) if days},
            "teams": sorted(L["teams"]),
            "dials": L["dials"],
            "out_dials": L["out_dials"],
            "in_dials": L["in_dials"],
            "missed_inbound": L["missed_inbound"],
            "connects": L["connects"],
            "dm_connects": L["dm_connects"],
            # Team rule (>= 3 min outbound). The disposition figure above stays.
            "call_connects": L["call_connects"],
            "conversations": L["conversations"],
            "talk_min": round(L["dial_talk_ms"] / 60000.0, 1),
            "meetings": L["meetings"],
            "demos": L["demos"],
            "demos_performed": L["demos_performed"],
            # Team rule (>= 10 min recording). demos is UNCHANGED; this splits it.
            "demo_connects": L["demo_connects"],
            "demos_under10": L["demos"] - L["demo_connects"],
            # Outbound-dial duration histogram, one count per DUR_BUCKETS entry.
            "hist": list(L["hist"]),
            "meeting_recordings": L["meeting_recordings"],
            "emails_out": L["emails_out"],
            "emails_in": L["emails_in"],
            "notes": L["notes"],
            "tasks": L["tasks"],
            "touches": (L["dials"] + L["meetings"] + L["emails_out"] + L["emails_in"]
                        + L["notes"] + L["tasks"]),
            "dispositions": dict(L["dispositions"]),
            "first_touch": L["first_touch"],
            # first_outreach is the OTHER clock (see touch()): the first time the
            # team actually reached out, which is the only one the sourced test may
            # use. It is emitted so the client can recompute "sourced in THIS
            # period" instead of trusting a flag computed against the 90-day window.
            "first_outreach": L["first_outreach"],
            "last_touch": L["last_touch"],
            "transcript_calls": L["call_links"][:5],
            "url": f"https://app.hubspot.com/contacts/2520274/record/0-1/{cid}",
        })

    # ---- bucket identity check ------------------------------------------
    # The whole point of the buckets is that they are the same events, resliced.
    # If summing a key across days ever stops matching its flat total, every
    # per-period number on the page is wrong, so fail loudly here rather than
    # ship a dashboard that quietly disagrees with itself.
    _BUCKET_OF = {"d": "out_dials", "id": "in_dials", "c": "connects",
                  "dc": "dm_connects", "m": "meetings", "dm": "demos",
                  "dp": "demos_performed", "eo": "emails_out", "ei": "emails_in",
                  "n": "notes", "t": "tasks", "mi": "missed_inbound",
                  # The two duration-rule keys ride the SAME check as everything
                  # else, so a period tab can never show a call-connect or
                  # demo-connect figure that disagrees with the window total.
                  "cc": "call_connects", "dn": "demo_connects"}
    _bad = []
    for r in rows:
        for k, flat in _BUCKET_OF.items():
            summed = sum(day.get(k, 0) for day in r["days"].values())
            if summed != r[flat]:
                _bad.append((r["contact_id"], k, summed, r[flat]))
        # Histogram: seven keys, checked against the seven-slot flat list, and
        # then against out_dials -- exactly one bucket fires per outbound dial.
        for i, k in enumerate(DUR_KEYS):
            summed = sum(day.get(k, 0) for day in r["days"].values())
            if summed != r["hist"][i]:
                _bad.append((r["contact_id"], k, summed, r["hist"][i]))
        if sum(r["hist"]) != r["out_dials"]:
            _bad.append((r["contact_id"], "hist_total", sum(r["hist"]), r["out_dials"]))
        # The 3-minute line falls on a bucket boundary, so the top four buckets
        # ARE the call connects. If this ever fails, the line drawn on the
        # distribution chart no longer matches the connect rule above it.
        if sum(r["hist"][3:]) != r["call_connects"]:
            _bad.append((r["contact_id"], "hist_ge3min", sum(r["hist"][3:]), r["call_connects"]))
        # Demo connects are a strict subset of demos -- the demo count does not move.
        if r["demo_connects"] > r["demos"]:
            _bad.append((r["contact_id"], "demo_connects>demos", r["demo_connects"], r["demos"]))
    if _bad:
        raise SystemExit("bucket/total mismatch on %d (contact,key) pairs, first 5: %s"
                         % (len(_bad), _bad[:5]))

    # Same check for the per-rep-per-day split against the dateless per-rep totals.
    # The rep scorecard and the two-seats cards read pd; if it ever stops summing
    # to per, those two sections disagree with the funnel above them.
    _badp, _triples = [], 0
    for r in rows:
        for rep, keys in r["per"].items():
            for k, flat in keys.items():
                _triples += 1
                summed = sum(day.get(k, 0) for day in r["pd"].get(rep, {}).values())
                if summed != flat:
                    _badp.append((r["contact_id"], rep, k, summed, flat))
    if _badp:
        raise SystemExit("pd/per mismatch on %d (contact,rep,key) triples, first 5: %s"
                         % (len(_badp), _badp[:5]))
    print("  rep-day buckets OK: %d rep-days, %d (contact,rep,key) triples match per"
          % (sum(len(d) for r in rows for d in r["pd"].values()), _triples), file=sys.stderr)
    _bkeys = sorted({k for r in rows for day in r["days"].values() for k in day})
    print("  buckets OK: %d contact-days, keys %s, %d engagements with no timestamp"
          % (sum(len(r["days"]) for r in rows), ",".join(_bkeys), _no_ts["n"]),
          file=sys.stderr)

    rows.sort(key=lambda r: (r["last_touch"] or ""), reverse=True)

    print("\n[6/6] write", file=sys.stderr)
    with open(os.path.join(DATA, "leads.json"), "w", encoding="utf-8") as f:
        json.dump(rows, f)

    summary = {
        "window": {"start": START, "end": END},
        "unowned_calls": _UNOWNED[0],
        "recovered_calls": _UNOWNED[1],
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "counts": {
            "calls": len(calls), "meetings": len(meetings), "emails": len(emails),
            "notes": len(notes), "tasks": len(tasks),
            "leads": len(rows), "companies": len(companies),
        },
        "unassociated": {
            k: sum(1 for r in v if not amap[k].get(r["id"]))
            for k, v in [("calls", calls), ("meetings", meetings), ("emails", emails)]
        },
        "by_rep": {},
        "by_segment": defaultdict(int),
    }
    for r in rows:
        summary["by_segment"][r["segment"]] += 1

    # ---- parent rollup ----------------------------------------------------
    # A group enrolls the PARENT record and each treating location separately. The
    # team only ever works a location, so the parent record never carries a touch.
    # VP decision (2026-09): a sourced child credits its parent too.
    #
    # The link is the COMPANY property parent_provider ("Parent Provider ID"): a
    # child holds its PARENT'S provider_unique_key, parents hold 0. This is HFD
    # hierarchy data off the ELI sync, NOT HubSpot's native parent/child
    # association -- that association exists in this portal (typeId 13 "Child
    # Company" / 14 "Parent Company") but is populated on only 4.5% of real pairs
    # and on NONE of the six pairs validated by hand. The "- Parent -" name suffix
    # is not usable either: 26.1% of real parents do not carry it (for example
    # "Dr Martin's Wellness Center - Corporate - 39957").
    def _parent_pid(cid):
        raw = str(companies.get(cid, {}).get("parent_provider") or "").strip()
        if not raw or raw in ("0", "0.0"):
            return ""
        try:
            return str(int(float(raw)))
        except ValueError:
            return ""

    def _enroll_adj(props):
        raw = props.get("enrollment_date") or ""
        if not raw:
            return ""
        try:
            return (dt.date.fromisoformat(raw[:10]) - dt.timedelta(days=1)).isoformat()
        except ValueError:
            return raw[:10]

    # Company grain, rolled off the contact rows: company -> reps who worked it.
    sourced_co_reps, enrolled_co_reps = defaultdict(set), defaultdict(set)
    for r in rows:
        if not r["company_id"]:
            continue
        if r["sourced"]:
            sourced_co_reps[r["company_id"]].update(r["reps"])
        if r["enrolled_in_window"]:
            enrolled_co_reps[r["company_id"]].update(r["reps"])

    want = {_parent_pid(c) for c in enrolled_co_reps} - {""}
    parents = search_companies_by_provider_ids(
        want, ["name", "enrollment_date", "provider_unique_key", "parent_provider",
               "legal_business_name", "practice_name", "doing_business_as"]) if want else {}
    pid_to_co = defaultdict(list)
    for pcid, pprops in parents.items():
        pid_to_co[str(pprops.get("provider_unique_key") or "").strip()].append(pcid)
    for k in pid_to_co:
        pid_to_co[k].sort()          # deterministic if a provider id ever maps to 2 records

    def _rollup(base_reps):
        """parent company -> {date, name, via: [child company ids]}, split into the
        parents that ALSO enrolled inside the window (countable) and those that did
        not (not countable). One hop only -- no grandparents: none of the credited
        parents carry a parent_provider of their own."""
        credited, skipped = {}, {}
        for child in sorted(base_reps):
            for pcid in pid_to_co.get(_parent_pid(child), []):
                if pcid in base_reps:
                    continue                      # already counted on its own merit
                d = _enroll_adj(parents[pcid])
                tgt = credited if in_window(d) else skipped
                tgt.setdefault(pcid, {"date": d, "name": parents[pcid].get("name") or "",
                                      "provider_id": parents[pcid].get("provider_unique_key") or "",
                                      "via": []})["via"].append(child)
        return credited, skipped

    parent_sourced, parent_skipped = _rollup(sourced_co_reps)
    parent_touched, _parent_touched_skipped = _rollup(enrolled_co_reps)

    # Sourced enrollments are credited at COMPANY grain, deduped per rep, so two
    # contacts at the same practice do not count as two enrollments.
    rep_sourced_co = defaultdict(set)
    rep_enrolled_co = defaultdict(set)
    for co_id, reps in sourced_co_reps.items():
        for rep in reps:
            rep_sourced_co[rep].add(co_id)
    for co_id, reps in enrolled_co_reps.items():
        for rep in reps:
            rep_enrolled_co[rep].add(co_id)
    # Credit each rolled-up parent to whichever reps worked the child that pulled
    # it in. Sets, so a parent that is ALSO sourced on its own merit counts once,
    # and a parent pulled in by two sourced children counts once.
    for pcid, info in parent_sourced.items():
        for child in info["via"]:
            for rep in sourced_co_reps[child]:
                rep_sourced_co[rep].add(pcid)
    for pcid, info in parent_touched.items():
        for child in info["via"]:
            for rep in enrolled_co_reps[child]:
                rep_enrolled_co[rep].add(pcid)

    for rep in TEAM.values():
        s = rep_stat[rep]
        summary["by_rep"][rep] = {
            "team": next((t for o, t in TEAM_OF.items() if TEAM[o] == rep), ""),
            "leads_touched": len(rep_leads[rep]),
            "dials": s["dials"],
            "out_dials": s["out_dials"],
            "in_dials": s["in_dials"],
            "missed_inbound": s["missed_inbound"],
            "connects": s["connects"],
            "dm_connects": s["dm_connects"],
            "call_connects": s["call_connects"],
            "dm_rate": round(s["dm_connects"] / s["dials"], 3) if s["dials"] else None,
            "connect_rate": round(s["connects"] / s["dials"], 3) if s["dials"] else None,
            "call_connect_rate": (round(s["call_connects"] / s["out_dials"], 3)
                                  if s["out_dials"] else None),
            "hist": [s["h_" + k] for k in DUR_KEYS],
            "conversations_2min": s["conversations"],
            "talk_hours": round(s["dial_talk_ms"] / 3600000.0, 1),
            "meetings": s["meetings"],
            "demos": s["demos"],
            "demos_performed": s["demos_performed"],
            "demo_connects": s["demo_connects"],
            "demos_under10": s["demos"] - s["demo_connects"],
            "meeting_recordings": s["meeting_recordings"],
            "emails_out": s["emails_out"],
            "emails_in": s["emails_in"],
            "enrolled_companies_touched": len(rep_enrolled_co[rep]),
            "sourced_enrollments": len(rep_sourced_co[rep]),
        }
    summary["totals_company_grain"] = {
        "distinct_enrolled_companies_touched": len(set().union(*rep_enrolled_co.values())) if rep_enrolled_co else 0,
        "distinct_sourced_enrollments": len(set().union(*rep_sourced_co.values())) if rep_sourced_co else 0,
        "distinct_enrolled_companies_touched_direct": len(enrolled_co_reps),
        "distinct_sourced_enrollments_direct": len(sourced_co_reps),
    }
    _co_name = {r["company_id"]: r["company"] for r in rows if r["company_id"]}
    summary["parent_rollup"] = {
        "rule": "a sourced CHILD credits its PARENT company too, but only if the parent "
                "also enrolled inside the window",
        "mechanism": "child COMPANY.parent_provider == parent COMPANY.provider_unique_key",
        "sourced_direct": len(sourced_co_reps),
        "sourced_rolled_up": len(sourced_co_reps) + len(parent_sourced),
        "touched_direct": len(enrolled_co_reps),
        "touched_rolled_up": len(enrolled_co_reps) + len(parent_touched),
        "parents_added": [
            {"company_id": pcid, "name": i["name"], "provider_id": i["provider_id"],
             "enrollment_date": i["date"],
             "via": [{"company_id": c, "name": _co_name.get(c, "")} for c in sorted(set(i["via"]))]}
            for pcid, i in sorted(parent_sourced.items(), key=lambda kv: (kv[1]["date"], kv[0]))],
        "parents_skipped_no_in_window_enrollment": [
            {"company_id": pcid, "name": i["name"], "provider_id": i["provider_id"],
             "enrollment_date": i["date"] or None,
             "via": [{"company_id": c, "name": _co_name.get(c, "")} for c in sorted(set(i["via"]))]}
            for pcid, i in sorted(parent_skipped.items(), key=lambda kv: kv[0])],
    }
    # ---- locations vs practices (Mel, 2026-09-14) -------------------------
    # "AEs are paid on total number of locations enrolled AND % of first 40-days
    #  funding. Seeing the total number of locations enrolled would be ideal (it
    #  would be great if we could see both)."
    # Two different questions, so two different numbers, both labelled in full:
    #   LOCATIONS ENROLLED  = every credited company record. That is each sourced
    #     practice record PLUS each parent group record the rollup credits, because
    #     a group that enrols a parent and three treating locations is four records
    #     on the comp plan. This is the larger figure and the one Mel asked for.
    #   PRACTICES ENROLLED  = the distinct BUSINESSES behind those records. Ed,
    #     2026-09-20: "Be sure to check legalname, practice name and dba when
    #     matching." So this is not a Provider ID count: records are joined when
    #     they share a Provider ID, or a corroborated name on any of Company
    #     name / Legal Business Name / Practice Name / Doing Business As.
    #     Always <= locations.
    # The gap between the two is the answer to Mel's comp question: a group that
    # enrols a parent and three treating locations pays on four locations but is
    # one practice.
    #
    # The index is rebuilt here over BOTH the worked company records and the
    # credited parent records, because `parents` is only fetched after the main
    # company pull and PRACTICE_KEY therefore does not cover it.
    _all_props = dict(parents)
    _grain_key, _grain_report = build_practice_index(
        set(companies) | set(parents), extra=_all_props)

    def _co_pid(cid):
        if cid in companies:
            return str(companies[cid].get("provider_unique_key") or "").strip()
        return str(parents.get(cid, {}).get("provider_unique_key") or "").strip()

    def _grain(direct_co, rolled_parents):
        recs = set(direct_co) | set(rolled_parents)
        # Practices counts the businesses behind EVERY credited record, parents
        # included. Counting only the direct records would put a parent group and
        # its child in different populations and could report more practices than
        # locations for a group that enrolled parent-first.
        keys = {_grain_key.get(c, c) for c in recs}
        # Like for like: the Provider ID comparison must run over the SAME record
        # set as the practice count, parents included. Comparing a parent-inclusive
        # practice count against a direct-only Provider ID count would make name
        # matching look as though it INCREASED the number of practices.
        pids = {_co_pid(c) or ("norecord:" + c) for c in recs}
        return {
            "locations": len(direct_co) + len(rolled_parents),
            "practices": len(keys),
            "practices_if_deduped_on_provider_id_only": len(pids),
            "direct_company_records": len(direct_co),
            "parent_records_credited": len(rolled_parents),
            "practice_records_without_provider_id":
                sum(1 for c in direct_co if not _co_pid(c)),
        }

    summary["practice_identity"] = {
        "rule": "company records are ONE practice when they share a Provider ID, or "
                "when a normalised name matches on any of Company name, Legal "
                "Business Name, Practice Name or Doing Business As",
        "asked_for_by": "Ed Smith, 2026-09-20: 'Be sure to check legalname, practice "
                        "name and dba when matching.'",
        "name_normalisation": "lowercase, '&' to 'and', punctuation folded to spaces, "
                              "entity suffixes and credentials stripped (Inc, LLC, "
                              "PLLC, PC, PA, DDS, DMD, MD, ...)",
        "not_evidence": "a name under 4 characters, or one whose every remaining token "
                        "is a category word (dental, family, care, center, smile, ...), "
                        "is ignored - it describes an industry, not a business",
        "corroboration_guard": "a shared name only joins records whose OWN Company name "
                               "contains it. Practice Name is a defaulted field in this "
                               "portal - 48 unrelated records carry 'Children's Choice "
                               "Dental Care Stockton' and 7 unrelated Brooklyn practices "
                               "carry 'Avenue D Dental' - so an uncorroborated name is "
                               "treated as a copied value, not as identity. Real brands "
                               "still join, because their locations are named after them "
                               "('Bayou Orthodontics - Harvey', '- Baton Rouge').",
        "not_parent_provider": "the parent link is deliberately NOT used. Amulet "
                               "Management LLC parents 48 records including Williams "
                               "Orthodontics (Gilbert AZ) and Jensen Orthodontics (Las "
                               "Cruces NM): one owner, not one practice. Joining on it "
                               "would collapse a DSO footprint to a single practice and "
                               "make the locations/practices gap meaningless.",
        "runaway_backstop": "a name that would still join more than %d records is "
                            "rejected outright; every rejection is listed below"
                            % NAME_SPAN_MAX,
        "over_all_company_records": _grain_report,
    }
    summary["enrollment_grain"] = {
        "locations_rule": "every credited COMPANY record: each sourced practice record "
                          "plus each parent group record credited by the parent rollup",
        "practices_rule": "the distinct BUSINESSES behind those records, joined on "
                          "Provider ID or on a corroborated Legal Business Name, "
                          "Practice Name, Doing Business As or Company name",
        "sourced": _grain(sourced_co_reps, parent_sourced),
        "touched": _grain(enrolled_co_reps, parent_touched),
    }

    # ---- demo no-shows (Ed's ruling, 2026-09-20) --------------------------
    # Ed: "The demo number should stay the same, but the no show number might
    # change given the less than 10 minute rule." Then: "I think we should mark
    # them as no shows for the ones under [10 minutes]. Laura is working on
    # finding attendance from meetings, but it's not backfilled yet."
    #
    # So the 10-minute bar does NOT move the Demos count - it SPLITS it, and the
    # under-10 side IS the no-show count. Not "candidate", not "possible". This
    # replaces the old no-show metric, which read the hand-set Demo Booking Status
    # radio: that field is manually maintained, blank on a large share of records,
    # and current-state, so a later edit silently rewrites history.
    #
    # The reconciliation below is kept as EVIDENCE, not as a competing headline.
    # It is the number Mel and Laura will want: of the demos now marked no-show,
    # how many the hand-set field already flagged No Show, how many it called
    # Booked or Occurred, and how many were blank. The disagreement is the case
    # for the duration rule.
    # Meeting grain. A meeting inherits a status from its associated contacts: if
    # ANY associated contact is flagged No Show the meeting counts as No Show,
    # otherwise the first non-blank status wins, otherwise it is blank.
    def _mtg_status(mid):
        cids = amap["meetings"].get(mid, [])
        if not cids:
            return "No contact linked"
        vals = [(contacts.get(c, {}).get("demo_booking_status") or "").strip() for c in cids]
        if any(v == "No Show" for v in vals):
            return "No Show"
        for v in vals:
            if v:
                return v
        return "Not set (blank)"

    _recon = {"under10": defaultdict(int), "connected10": defaultdict(int)}
    _n_demo_mtgs = _n_under = _n_conn = 0
    for m in meetings:
        mp = m.get("properties", {})
        if not is_demo(mp):
            continue
        _n_demo_mtgs += 1
        side = "connected10" if is_demo_connect(mp) else "under10"
        if side == "under10":
            _n_under += 1
        else:
            _n_conn += 1
        _recon[side][_mtg_status(m["id"])] += 1

    _old_noshow_field = sum(1 for r in rows if r.get("demo_booking_status") == "No Show")
    summary["demo_split"] = {
        "rule": "Demos is UNCHANGED (every demo-titled meeting). The 10-minute bar "
                "splits it: at or above 10 minutes is a demo connect, under 10 "
                "minutes IS a no-show.",
        "ruling": "Ed Smith, 2026-09-20: 'I think we should mark them as no shows for "
                  "the ones under [10 minutes].'",
        "demos": _n_demo_mtgs,
        "demo_connects_10min": _n_conn,
        "no_shows_under_10min": _n_under,
        "demos_performed_5min_old_gate": sum(v["demos_performed"] for v in summary["by_rep"].values()),
        "old_no_show_metric_demo_booking_status_contacts": _old_noshow_field,
        "no_shows_by_demo_booking_status": dict(sorted(_recon["under10"].items())),
        "demo_connects_by_demo_booking_status": dict(sorted(_recon["connected10"].items())),
        "interim_proxy": "Duration is an INTERIM PROXY for attendance, not ground "
                         "truth. Laura is building real attendance data from the "
                         "meeting records; it is not backfilled yet. When it lands it "
                         "should replace this rule.",
        "how_to_read": "The status split is the evidence, not a second answer. The "
                       "demos this rule marks no-show that the hand-set Demo Booking "
                       "Status field already flagged No Show are the two agreeing. The "
                       "ones it called Booked or Occurred are where the hand-set field "
                       "was overstating attendance. The blanks are where duration is "
                       "the only signal there is.",
    }

    summary["by_segment"] = dict(summary["by_segment"])

    with open(os.path.join(DATA, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # ---- provenance -------------------------------------------------------
    # Emitted from the same run that produced the numbers, so the documented
    # predicate and the value on the dashboard cannot drift apart. Every entry
    # is meant to be independently reproducible by hand.
    owners = ", ".join(sorted(TEAM))
    win = f"hs_timestamp >= {START} AND hs_timestamp < {END}"
    n_dial = sum(v["out_dials"] for v in summary["by_rep"].values())
    n_conn = sum(v["connects"] for v in summary["by_rep"].values())
    n_dm = sum(v["dm_connects"] for v in summary["by_rep"].values())
    n_demo = sum(v["demos"] for v in summary["by_rep"].values())
    n_perf = sum(v["demos_performed"] for v in summary["by_rep"].values())
    n_mtg = sum(v["meetings"] for v in summary["by_rep"].values())
    n_cc = sum(v["call_connects"] for v in summary["by_rep"].values())
    n_dn = sum(v["demo_connects"] for v in summary["by_rep"].values())
    n_u10 = n_demo - n_dn
    n_hist = [sum(v["hist"][i] for v in summary["by_rep"].values()) for i in range(len(DUR_KEYS))]
    _pct = lambda a, b: ("%.1f%%" % (100.0 * a / b)) if b else "n/a"
    _dist_txt = "; ".join("%s %d (%s)" % (DUR_BUCKETS[i][1], n_hist[i], _pct(n_hist[i], n_dial))
                          for i in range(len(DUR_KEYS)))
    _u10_txt = ", ".join("%s %d" % (k, v) for k, v in
                         summary["demo_split"]["no_shows_by_demo_booking_status"].items()) or "none"
    _ns_recon = summary["demo_split"]["no_shows_by_demo_booking_status"]
    _ns_agree = _ns_recon.get("No Show", 0)
    _ns_contra = _ns_recon.get("Booked", 0) + _ns_recon.get("Occurred", 0)
    _ns_blank = _ns_recon.get("Not set (blank)", 0) + _ns_recon.get("No contact linked", 0)
    _eg = summary["enrollment_grain"]["sourced"]

    sources = {
        "window": {"start": START, "end_exclusive": END,
                   "note": "90 complete days ending yesterday. Today is excluded so no figure sits on a partial day."},
        "generatedAtUtc": summary["generated_at_utc"],
        "team": {o: TEAM[o] for o in sorted(TEAM)},
        "metrics": [
            {"id": "contacts", "label": "Contacts touched", "value": len(rows),
             "system": "HubSpot CRM search API", "object": "CONTACT",
             "predicate": "Distinct contacts associated to any CALL / MEETING / EMAIL / NOTE / TASK "
                          f"owned by [{owners}] inside the window",
             "dateProperty": "hs_timestamp on the engagement", "grain": "one row per contact",
             "verify": "Sum of the Contacts column in the rep scorecard will exceed this - a contact "
                       "touched by two reps counts once here and once per rep there."},
            {"id": "dials", "label": "Outbound dials", "value": n_dial,
             "system": "HubSpot CRM search API", "object": "CALL",
             "predicate": "hs_call_source = 'INTEGRATIONS_PLATFORM' AND hs_call_direction = 'OUTBOUND'",
             "dateProperty": "hs_timestamp", "grain": "one row per call (engagement grain)",
             "verify": "HubSpot > Calls index > filter Call source = Integrations Platform, "
                       "Direction = Outbound, Activity date in range. Owner filter will UNDER-count: see "
                       "the unowned-calls note below."},
            {"id": "call_connects", "label": "Call connects (3+ minutes)", "value": n_cc,
             "system": "HubSpot CRM search API", "object": "CALL",
             "predicate": "Call source = Integrations Platform AND Direction = Outbound AND "
                          "Call duration >= 180000 ms (3 minutes)",
             "dateProperty": "Activity date (hs_timestamp)",
             "grain": "one row per outbound dial",
             "verify": "THIS IS THE TEAM'S DEFINITION, set by Mel Matthews on 2026-09-14: "
                       "'A call connect and a demo connect need to be different lengths IMO. "
                       "Call connect: >=3 minutes. Demo connect: >=10 minutes.' It is a strict "
                       "subset of Outbound dials, so it can never exceed them: %d of %d (%s). "
                       "Reproduce it in HubSpot: Calls index, Call source = Integrations Platform, "
                       "Direction = Outbound, Call duration is greater than or equal to 3 minutes, "
                       "Activity date in range. It does NOT match HubSpot's own connected count - "
                       "see the next row for why."
                       % (n_cc, n_dial, _pct(n_cc, n_dial))},
            {"id": "connects", "label": "Connects on call outcome (HubSpot's rule, secondary)",
             "value": n_conn,
             "system": "HubSpot CRM search API", "object": "CALL",
             "predicate": "a dial whose Call outcome is Connected (f240bbac-87c9-4f6e-bf70-924b57d47db7), "
                          "Meeting booked (2e7360c1-6b71-40e9-ab2b-30ae98a4678c) or "
                          "Left live message (a4c4c377-d246-4b32-a13b-75a56a4cd0ff)",
             "dateProperty": "Activity date (hs_timestamp)", "grain": "one row per dial",
             "verify": "KEPT ON PURPOSE as a second line, not as the headline. HubSpot's own "
                       "automation runs on the outcome, not on duration - the Connected call "
                       "count property, workflow 1662944670 and the SDR pipeline all read it - so "
                       "a reader comparing this dashboard to a HubSpot report needs both numbers "
                       "to see why they differ. Left live message is inside it on purpose: despite "
                       "the name it means a gatekeeper answered, and 116 of 116 sampled transcripts "
                       "had two speakers. The duration rule and the outcome rule are different "
                       "populations, not a corrected and an uncorrected version of one number."},
            {"id": "dm", "label": "Reached decision maker", "value": n_dm,
             "system": "HubSpot CRM search API", "object": "CALL",
             "predicate": "a dial dispositioned Connected or Meeting booked (excludes Left live message)",
             "dateProperty": "hs_timestamp", "grain": "one row per call",
             "verify": "Always <= Connects. The gap is the gatekeeper population."},
            {"id": "demos", "label": "Demos", "value": n_demo,
             "system": "HubSpot CRM search API", "object": "MEETING_EVENT",
             "predicate": "'demo' appears in hs_meeting_title (case-insensitive)",
             "dateProperty": "hs_timestamp", "grain": "one row per meeting",
             "verify": "This is Laura's definition from dashboard 21888050 (report 345792699). HubSpot's "
                       "CONTAINS is case-insensitive, so her three-variant list is one predicate. Do NOT "
                       "use hs_activity_type = 'Demo' - it is set on only about a third of demo meetings."},
            {"id": "demo_connects", "label": "Demo connects (10+ minutes)", "value": n_dn,
             "system": "HubSpot CRM search API", "object": "MEETING_EVENT",
             "predicate": "'demo' appears in the Meeting name (case-insensitive) AND "
                          "Meeting recording duration >= 600000 ms (10 minutes)",
             "dateProperty": "Activity date (hs_timestamp)", "grain": "one row per meeting",
             "verify": "Mel Matthews, 2026-09-14: demo connect = 10 minutes. This does NOT change "
                       "the Demos count above it - Demos is still every demo-titled meeting, "
                       "Laura's house definition. The 10-minute bar splits that count: %d of %d "
                       "demos (%s) cleared it. Reproduce it in HubSpot: Meetings index, Meeting "
                       "name contains demo, Meeting recording duration >= 10 minutes, Activity "
                       "date in range." % (n_dn, n_demo, _pct(n_dn, n_demo))},
            {"id": "perf", "label": "Demos performed on the retired 5-minute gate (prior definition)",
             "value": n_perf,
             "system": "HubSpot CRM search API", "object": "MEETING_EVENT",
             "predicate": "demo-titled AND Meeting recording duration > 300000 ms (5 minutes)",
             "dateProperty": "Activity date (hs_timestamp)", "grain": "one row per meeting",
             "verify": "RETIRED as a headline on 2026-09-20 and kept only as a documented prior "
                       "definition. The audit established that this gate counts no-shows as "
                       "performed - the recorder keeps running while the AE waits alone, and 88 of "
                       "97 known no-shows cleared 5 minutes. That is precisely the defect the "
                       "10-minute rule fixes. It is still carried so our number ties to Laura's "
                       "report 345792760 and so the move from a 5-minute to a 10-minute bar is "
                       "visible rather than silent. Do not use it to judge demo attendance."},
            {"id": "dur_dist", "label": "Outbound dials by call duration", "value": n_dial,
             "system": "HubSpot CRM search API", "object": "CALL",
             "predicate": "every outbound dialer call, bucketed on Call duration; buckets are "
                          "left-closed and right-open so each dial lands in exactly one",
             "dateProperty": "Activity date (hs_timestamp)", "grain": "one row per outbound dial",
             "verify": "The seven buckets sum to Outbound dials by construction, and the top four "
                       "(3 min and over) ARE the Call connects row - the 3-minute connect line "
                       "falls on a bucket boundary, so the marked line on the chart and the connect "
                       "rule cannot drift apart. On this window: %s." % _dist_txt},
            {"id": "meetings", "label": "Meetings", "value": n_mtg,
             "system": "HubSpot CRM search API", "object": "MEETING_EVENT",
             "predicate": f"hubspot_owner_id IN [{owners}]",
             "dateProperty": "hs_timestamp", "grain": "one row per meeting",
             "verify": "For these reps demos and meetings are nearly the same population."},
            {"id": "noshow", "label": "Demo no-shows (under 10 minutes)", "value": n_u10,
             "system": "HubSpot CRM search API", "object": "MEETING_EVENT",
             "predicate": "'demo' appears in the Meeting name (case-insensitive) AND Meeting "
                          "recording duration < 600000 ms (10 minutes). This is exactly Demos "
                          "minus Demo connects.",
             "dateProperty": "Activity date (hs_timestamp)", "grain": "one row per meeting",
             "verify": "Ed Smith ruled on 2026-09-20 that a demo whose recording ran under ten "
                       "minutes IS a no-show, so these %d are marked, not flagged as candidates. "
                       "Reproduce it in HubSpot: Meetings index, Meeting name contains demo, "
                       "Meeting recording duration less than 10 minutes, Activity date in range. "
                       "INTERIM PROXY, NOT GROUND TRUTH: duration stands in for attendance because "
                       "attendance is not recorded yet. Laura is building real attendance data from "
                       "the meeting records and it is not backfilled; when it lands it should "
                       "replace this rule. EVIDENCE FOR THE RULE: against the hand-set Demo Booking "
                       "Status field these %d break down as %s - %d the field already flagged No "
                       "Show, %d it called Booked or Occurred, %d blank. The %d it called Booked or "
                       "Occurred are where the hand-set field was overstating attendance."
                       % (n_u10, n_u10, _u10_txt, _ns_agree, _ns_contra, _ns_blank, _ns_contra)},
            {"id": "noshow_field_retired",
             "label": "No-shows on the retired Demo Booking Status field (prior definition)",
             "value": _old_noshow_field,
             "system": "HubSpot CRM search API", "object": "CONTACT",
             "predicate": "Demo Booking Status = 'No Show'",
             "dateProperty": "n/a - the field carries no timestamp",
             "grain": "one row per contact",
             "verify": "REPLACED on 2026-09-20 by the duration rule above and kept only as a "
                       "documented prior definition. Three reasons it was replaced: it is typed by "
                       "hand by the reps (232 of 232 writes are CRM_UI), it is blank on a large "
                       "share of records, and it is CURRENT STATE with no timestamp, so a later "
                       "edit silently rewrites history. It is also contact grain, not meeting "
                       "grain, so it is not comparable to the demo counts one for one. Laura's "
                       "automated detector, workflow 1870876825, is enabled but broken at 1.1%% "
                       "precision. Duration is measured; this was typed. Do not rank reps on it."},
            {"id": "enrolled", "label": "Sourced enrollments", "value": summary["totals_company_grain"]["distinct_sourced_enrollments"],
             "system": "HubSpot CRM search API", "object": "COMPANY",
             "predicate": ENROLLED_PREDICATE + " PLUS a company whose CHILD practice meets that test and "
                          "which itself enrolled inside the window - credited even though the team never "
                          "touched the parent record directly (VP decision, 2026-09).",
             "dateProperty": "Enrollment date on the practice, shifted back one day",
             "grain": "one distinct company",
             "verify": ENROLLED_WHY +
                       "The minus-one-day is real: the stamping workflow 1820099735 fires off the 06:31 CT "
                       "nightly ELI sync, so the raw value lands a day late (zero Mondays, 243 Saturdays in "
                       "the raw data). Read weekly or monthly, never daily - 45% arrives in catch-up batches. "
                       "Parent/child is COMPANY.parent_provider - the child holds the parent's Provider ID - "
                       "NOT HubSpot's native parent/child association, which is populated on only 4.5% of "
                       "real pairs here, and NOT the '- Parent -' name suffix, which 26.1% of real parents "
                       "do not carry. summary.parent_rollup lists every parent added, the child that pulled "
                       "it in, and the parents that could NOT be counted because they did not enroll in the "
                       "window."},
            {"id": "locations", "label": "Locations enrolled (sourced)",
             "value": _eg["locations"],
             "system": "HubSpot CRM search API", "object": "COMPANY",
             "predicate": "every credited company record: each sourced practice record (%d) "
                          "plus each parent group record the rollup credits (%d)"
                          % (_eg["direct_company_records"], _eg["parent_records_credited"]),
             "dateProperty": "Enrollment date on the record, shifted back one day",
             "grain": "one row per enrolled company record",
             "verify": "Mel Matthews, 2026-09-14: 'AEs are paid on total number of locations "
                       "enrolled AND %% of first 40-days funding. Seeing the total number of "
                       "locations enrolled would be ideal (it would be great if we could see "
                       "both).' This is the LARGER of the two: a group that enrols a parent "
                       "record and three treating locations is four records here. The parent "
                       "records are listed one by one in summary.parent_rollup.parents_added, "
                       "each with the sourced child that pulled it in. THIS ROW IS THE FULL "
                       "WINDOW AND INCLUDES THE PARENT RECORDS. The Locations enrolled figure on "
                       "the Combined card is smaller (%d) and always will be: a parent group "
                       "record carries no contacts of its own, so it cannot appear on a contact "
                       "row and cannot be re-counted inside a selected period. The card counts "
                       "the %d records the team actually worked."
                       % (_eg["direct_company_records"], _eg["direct_company_records"])},
            {"id": "practices", "label": "Practices enrolled (sourced)",
             "value": _eg["practices"],
             "system": "HubSpot CRM search API", "object": "COMPANY",
             "predicate": "the distinct BUSINESSES behind those same credited records. Two records "
                          "are one practice when they share a Provider ID, or when a normalised "
                          "name matches on any of Company name, Legal Business Name, Practice "
                          "Name or Doing Business As AND that name also appears in both records' "
                          "Company name",
             "dateProperty": "Enrollment date on the practice, shifted back one day",
             "grain": "one distinct practice (business), not one company record",
             "verify": "The SMALLER of the two and always <= Locations enrolled; the %d in the gap "
                       "are extra records for a business already counted. Ed Smith, 2026-09-20: "
                       "'Be sure to check legalname, practice name and dba when matching.' Name "
                       "matching lowercases, folds '&' and punctuation, and strips entity suffixes "
                       "and credentials (Inc, LLC, PLLC, PC, PA, DDS, DMD, MD), so 'Perla Dental "
                       "PC' and 'Perla Dental' are one name. A name is IGNORED when every token in "
                       "it is a category word (dental, family, care, center, smile), because that "
                       "describes an industry and not a business. A name must also be CORROBORATED "
                       "- it only joins records whose own Company name contains it - because "
                       "Practice Name is a defaulted field here: 48 unrelated records carry "
                       "'Children's Choice Dental Care Stockton'. Real brands still join, because "
                       "their locations are named after them ('Bayou Orthodontics - Harvey', "
                       "'- Baton Rouge'). Parent/child is deliberately NOT used: that is one owner, "
                       "not one practice, and it is what Locations already rolls up. Deduping on "
                       "Provider ID alone would give %d. Every record this joined is listed group "
                       "by group in summary.practice_identity, with the Provider IDs and names, so "
                       "each merge can be checked by hand. THIS ROW IS THE FULL WINDOW AND "
                       "INCLUDES THE PARENT RECORDS, for the same reason as the row above it, so "
                       "the Practices enrolled figure on the Combined card is smaller. Compare the "
                       "pair on the card against each other, and this pair against each other - "
                       "never one from the card against one from here."
                       % (_eg["locations"] - _eg["practices"],
                          _eg["practices_if_deduped_on_provider_id_only"])},
            {"id": "missed", "label": "Missed inbound calls",
             "value": sum(r.get("missed_inbound", 0) for r in rows),
             "system": "HubSpot CRM search API", "object": "CALL",
             "predicate": "hs_call_direction = 'INBOUND' AND hs_call_disposition is empty AND "
                          "hs_call_duration = 0",
             "dateProperty": "hs_timestamp", "grain": "one row per call",
             "verify": "An inbound ring nobody picked up. This is demand, not rep activity, so it is "
                       "deliberately excluded from dials and connects and reported on its own. Attributed "
                       "by the rep's own line number, since no name is written when nobody answers."},
            {"id": "segment", "label": "Segment", "value": len(summary["by_segment"]),
             "system": "HubSpot CRM search API", "object": "CONTACT",
             "predicate": "grouped on hs_object_source_detail_1, falling back to hs_object_source_label",
             "dateProperty": "n/a - set at record creation", "grain": "one row per contact",
             "verify": "Not lead_source, which is 96% empty on recent contacts. Scrape = 'CLI_LR' "
                       "(Laura's Clay pipeline). pb_last_scraped_at is a dead PhantomBuster field, 0% filled."},
            {"id": "signal", "label": "Inbound engagement signal",
             "value": sum(1 for r in rows if r.get("inbound_signal")),
             "system": "HubSpot CRM search API", "object": "CONTACT",
             "predicate": "hs_last_sales_activity_type is set",
             "dateProperty": "hs_last_sales_activity_date", "grain": "one row per contact",
             "verify": "HubSpot-maintained, inbound-only enum: EMAIL_REPLY, EMAIL_OPEN, EMAIL_CLICK, "
                       "MEETING_BOOKED, FORM_SUBMITTED, HUBSPOT_REVISIT."},
        ],
        # Shipped so the browser can re-count LOCATIONS inside the selected period
        # instead of quoting a window figure under a weekly tab. Each entry carries
        # the parent's own enrollment date and the sourced child company records
        # that earned it, which is exactly the rollup rule, re-applied per period.
        "parentRollup": [
            {"company_id": pcid, "name": i["name"], "enrollment_date": i["date"],
             "via": sorted(set(i["via"]))}
            for pcid, i in sorted(parent_sourced.items(), key=lambda kv: (kv[1]["date"], kv[0]))],
        "dataQuality": [
            {"id": "unowned", "label": "Dialer calls with no owner in HubSpot",
             "value": summary.get("unowned_calls", 0),
             "recovered": summary.get("recovered_calls", 0),
             "note": "HubSpot leaves hubspot_owner_id null on many Aloware calls. The body names the rep "
                     "and their line, so we parse `Line: Sales- <Rep>` and re-attribute. Any owner-filtered "
                     "report understates every rep who dials from their own line."},
            {"id": "orphan_calls", "label": "Calls with no contact association",
             "value": summary["unassociated"]["calls"],
             "note": "Included in team totals, absent from the contact list - they cannot land on a row."},
            {"id": "fanout", "label": "Contacts with no company / many companies",
             "value": sum(1 for r in rows if not r.get("company_id")),
             "note": "Primary company resolved via associatedcompanyid, which matches HubSpot's own "
                     "Primary association exactly. Caps every company-grain figure."},
        ],
    }
    with open(os.path.join(DATA, "sources.json"), "w", encoding="utf-8") as f:
        json.dump(sources, f, indent=2)

    print(json.dumps(summary, indent=2)[:2600])


if __name__ == "__main__":
    main()
