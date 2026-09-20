"""Build the artifact: slim the lead rows, then inject them into dashboard.html."""
import json, os
from collections import Counter

from sourced_rule import ENROLLED_PREDICATE, ENROLLED_WHY

HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, "data", "leads.json"), encoding="utf-8"))


def group(seg, clay):
    if clay or seg.startswith("Scrape"):
        return "Scrape (Clay)"
    if seg.startswith("Web form") or seg.startswith("Other (Form"):
        return "Inbound form"
    if seg.startswith("Referral"):
        return "Referral"
    if seg.startswith("List import"):
        return "List import"
    if seg.startswith("Dialer"):
        return "Dialer-created"
    if "livestorm" in seg.lower():
        return "Webinar"
    if seg.startswith("Inbound chat"):
        return "Inbound chat"
    if seg.startswith("Manually"):
        return "Manually created"
    return "Other"


# Friendly labels for the inbound-engagement enum (hs_last_sales_activity_type).
SIGNAL = {
    "EMAIL_REPLY": "Replied to email",
    "EMAIL_OPEN": "Opened email",
    "EMAIL_CLICK": "Clicked email",
    "MEETING_BOOKED": "Booked a meeting",
    "FORM_SUBMITTED": "Submitted a form",
    "HUBSPOT_REVISIT": "Revisited site",
    "PRESENTATION_REVISIT": "Reopened a deck",
    "INCOMING_EMAIL": "Emailed us",
    "CALL": "Called in",
}

# company_id  -> lets the browser dedupe sourced enrollments to practice grain,
#                so the cards match revenue.json's company-grain sourcedProviders.
# mkt_channel -> lets the browser test the paid-acquisition cohort on the
#                attribution fields (with lead_source, already kept below).
KEEP = ["contact_id", "company_id", "name", "job_title", "company", "city", "state",
        "lead_source", "mkt_channel",
        "lead_status", "lifecycle", "contact_owner", "created", "reps", "teams", "dials",
        "connects", "dm_connects", "conversations", "talk_min", "meetings", "demos", "demos_performed",
        # THE DURATION RULE (Mel 2026-09-14, approved by Ed 2026-09-20).
        # call_connects  = outbound dial >= 3 min. demo_connects = demo meeting
        # whose recording ran >= 10 min. demos is UNCHANGED and still ships.
        # hist           = the seven outbound-dial duration buckets, as COUNTS
        #                  per contact; the per-day copy rides in "days".
        # connects (the disposition figure) stays in KEEP on purpose - it is the
        # secondary line the page shows next to HubSpot's own reports.
        "call_connects", "demo_connects", "demos_under10", "hist",
        # provider_id   -> still shipped: it is the key the revenue SQL joins on.
        # location_key  -> the COMPANY RECORD. Counting distinct location_key is
        #                  "locations enrolled", the figure Mel's comp plan pays on.
        # practice_key  -> the BUSINESS behind that record, after extract.py joins
        #                  records sharing a Provider ID, a parent link, or a name on
        #                  Company name / Legal Business Name / Practice Name /
        #                  Doing Business As (Ed, 2026-09-20). Counting distinct
        #                  practice_key is "practices enrolled". Both ship so the
        #                  browser can show Mel both without recomputing either.
        "provider_id", "location_key", "practice_key",
        "emails_out", "emails_in", "notes", "tasks", "touches", "first_touch", "last_touch",
        # days        -> the per-day activity buckets, so the period control can
        #                RECOUNT activity inside the selected period instead of
        #                showing each contact's full 90-day totals.
        # first_outreach -> the outreach clock the sourced rule runs on, date-stamped
        #                so "sourced in THIS period" is computable client-side.
        # enrollment_date is already kept below and is already the shifted-back date.
        # pd -> the SAME per-rep split as `per`, with a date on it, so the rep
        #       scorecard and the two-seats cards can re-window instead of
        #       reporting 90-day rep totals under a "This week" tab.
        "days", "pd", "first_outreach",
        "enrolled_in_window", "sourced", "enrollment_date", "company_count",
        "provider_workflow", "url", "clay_source", "sequence", "per",
        # missed_inbound: the 'mi' bucket key mirrors it, and the browser-side
        # self-check compares every bucket key against its flat total. Without the
        # flat field shipped, that check compares against undefined and fails on a
        # missing column rather than on a real disagreement.
        "out_dials", "in_dials", "missed_inbound",
        "dm_connects", "demo_booking_status", "ae_demo_attended",
        "demo_won", "demo_lost", "vertical", "unqualified_reason", "ae_credited",
        "ae_eval_status", "loan_apps", "loan_activations", "loan_volume",
        "last_month_volume", "contract_value", "contract_value_mtd"]

# ---- sourced: guard rail, no longer a recomputation -------------------------
# HISTORY: this block used to RE-DERIVE the tightened sourced rule, because
# data/leads.json predated extract.py's switch to first_outreach and the window
# was frozen for the audit. That is over. The 2026-09-13 extract run applies the
# strict dated rule itself (first_outreach on or before the enrollment date), so
# this block now finds nothing to change and prints 167 -> 167 contacts,
# 157 -> 157 practices, zero dropped ids.
#
# It is kept for two reasons, not out of inertia:
#   1. It is the tripwire. If a future leads.json is ever produced by an older
#      extract.py, or by one whose outreach predicate has drifted, this prints a
#      non-zero drop instead of letting a loose flag reach the page silently.
#   2. It owns data/sourced_pids.txt - the provider cohort the revenue SQL runs
#      against - so the cohort is always regenerated from the SAME flag the page
#      renders. A hand-typed list once silently included practices that should
#      have been excluded; deriving the file here is what stops that recurring.
#
# It can only ever REMOVE a contact from the sourced set, never add one, so it
# cannot loosen the rule even if it does fire.
def real_outreach(r):
    """An outbound dial, an outbound email, a meeting, or an ANSWERED inbound dial.
    in_dials already excludes unanswered inbound rings, and meeting recordings that
    surface in the CALL object are counted as meeting_recordings, never as dials."""
    return bool((r.get("out_dials") or 0) or (r.get("emails_out") or 0)
                or (r.get("meetings") or 0) or (r.get("in_dials") or 0))


# THREE different grains, never mixed:
#   _pids      Provider IDs. What the revenue SQL joins on. Not a practice count.
#   _locations company RECORDS. What the comp plan pays on.
#   _practices distinct BUSINESSES, using extract.py's practice_key, which already
#              joined records sharing a Provider ID, a parent link, or a name on
#              Legal Business Name / Practice Name / Doing Business As / Company
#              name (Ed, 2026-09-20). Falls back to the location when a row has no
#              key at all, so a keyless row is never silently dropped from a count.
def _pids(pred):
    return {r.get("provider_id") for r in rows if pred(r) and r.get("provider_id")}


def _locations(pred):
    return {r.get("location_key") or ("contact:" + str(r.get("contact_id")))
            for r in rows if pred(r)}


def _practices(pred):
    return {r.get("practice_key") or r.get("location_key")
            or ("contact:" + str(r.get("contact_id")))
            for r in rows if pred(r)}


SOURCED = lambda r: r.get("sourced")
_was_contacts = sum(1 for r in rows if r.get("sourced"))
_was_practices = _practices(SOURCED)
for r in rows:
    if r.get("sourced") and not real_outreach(r):
        r["sourced"] = False
_now_contacts = sum(1 for r in rows if r.get("sourced"))
_now_practices = _practices(SOURCED)
_now_locations = _locations(SOURCED)
_now_pids = _pids(SOURCED)

# The provider cohort the revenue SQL runs against. PROVIDER IDs, not practice
# keys: the warehouse joins ContractProviderKey to provider_unique_key and knows
# nothing about our practice grouping. Regenerated from the same recomputed
# sourced flag so the cohort and the page can never drift apart again.
PIDS = os.path.join(HERE, "data", "sourced_pids.txt")
open(PIDS, "w", encoding="utf-8").write(
    ",".join("'%s'" % p for p in sorted(_now_pids)))

slim = []
for r in rows:
    d = {k: r.get(k) for k in KEEP}
    d["seg"] = group(r.get("segment") or "", r.get("clay_source"))
    d["sig"] = SIGNAL.get(r.get("inbound_signal") or "", "")
    for f in ("first_touch", "first_outreach", "last_touch", "created"):
        if d.get(f):
            d[f] = d[f][:10]
    slim.append(d)

out = os.path.join(HERE, "data", "leads_slim.json")
json.dump(slim, open(out, "w", encoding="utf-8"), separators=(",", ":"))

html = open(os.path.join(HERE, "dashboard.html"), encoding="utf-8").read()

# The artifact wrapper owns <head>, so the page cannot declare its own charset.
# Escape every non-ASCII character instead - HTML entities in the markup, and
# JS unicode escapes inside the script block - so the page renders correctly no
# matter how the host decides to decode it.
_split = html.index('<script id="leads"')
_esc_js = chr(92) + "u%04X"
html = ("".join(c if ord(c) < 128 else "&#x%04X;" % ord(c) for c in html[:_split])
        + "".join(c if ord(c) < 128 else _esc_js % ord(c) for c in html[_split:]))
assert all(ord(c) < 128 for c in html), "template still has non-ASCII"

data = open(out, encoding="utf-8").read()
vom = open(os.path.join(HERE, "data", "vom_slim.json"), encoding="utf-8").read()
rev = open(os.path.join(HERE, "data", "revenue.json"), encoding="utf-8").read()
# data/sources.json was written by the extract run that produced leads.json, so its
# "Sourced enrollments" row still carries the OLD count and the OLD predicate. Rewrite
# it from the recomputation above, otherwise the most-read row of the data dictionary
# would contradict every number on the page. The next extract run regenerates it from
# the same shared wording in sourced_rule.py.
SRC = os.path.join(HERE, "data", "sources.json")
srcdoc = json.load(open(SRC, encoding="utf-8"))
for _m in srcdoc.get("metrics", []):
    if _m.get("id") == "enrolled":
        _m["value"] = len(_now_practices)
        _m["predicate"] = ENROLLED_PREDICATE
        _m["dateProperty"] = "Enrollment date on the practice, shifted back one day"
        _v = _m.get("verify", "")
        _m["verify"] = _v if _v.startswith(ENROLLED_WHY) else ENROLLED_WHY + _v
json.dump(srcdoc, open(SRC, "w", encoding="utf-8"), indent=2)
src = open(SRC, encoding="utf-8").read()
# data/deals.json is produced by the pull_deals.py -> resolve_deals.py ->
# build_deals.py chain, NOT by extract.py: Deals are owner-scoped and not
# date-bounded, so they do not ride the rolling 90-day window and re-running
# extract.py neither refreshes nor invalidates them.
deals = open(os.path.join(HERE, "data", "deals.json"), encoding="utf-8").read()
assert "/*__DEALS__*/" in html, "deals marker missing from template"
assert "/*__DATA__*/" in html, "data marker missing from template"
built = os.path.join(HERE, "dashboard_built.html")
open(built, "w", encoding="utf-8").write(
    html.replace("/*__DATA__*/", data).replace("/*__VOM__*/", vom).replace("/*__REV__*/", rev).replace("/*__SRC__*/", src).replace("/*__DEALS__*/", deals))

print(f"rows {len(slim)} | payload {os.path.getsize(out)/1048576:.2f} MB "
      f"| built {os.path.getsize(built)/1048576:.2f} MB")
print(f"sourced (real-outreach guard): contacts {_was_contacts} -> {_now_contacts}, "
      f"practices {len(_was_practices)} -> {len(_now_practices)}"
      + ("  [no-op, as expected]" if _was_contacts == _now_contacts else "  [!! FIRED - leads.json "
         "was produced by an extract whose sourced rule disagrees with this one]"))
print("dropped practices:", ", ".join(sorted(_was_practices - _now_practices)) or "(none)")
print(f"sourced provider cohort written to data/sourced_pids.txt: {len(_now_pids)} provider ids")
print(f"sourced enrollment grain (contact rows, so NO parent group records): "
      f"{len(_now_locations)} locations (company records), "
      f"{len(_now_practices)} practices (distinct businesses)")
assert len(_now_practices) <= len(_now_locations), \
    "practices exceed locations - the practice_key join is broken"
print("segments:", dict(Counter(r["seg"] for r in slim).most_common()))
print("inbound signals:", dict(Counter(r["sig"] for r in slim if r["sig"]).most_common(8)))
print("demos:", sum(r["demos"] for r in slim), "performed:", sum(r["demos_performed"] for r in slim))
_ccs = sum(r["call_connects"] for r in slim)
_ods = sum(r["out_dials"] for r in slim)
_dns = sum(r["demo_connects"] for r in slim)
_dms = sum(r["demos"] for r in slim)
_h = [sum(r["hist"][i] for r in slim) for i in range(7)]
print("call connects (>=3 min): %d of %d outbound dials (contact grain)" % (_ccs, _ods))
print("demo connects (>=10 min): %d of %d demos, under 10 min %d" % (_dns, _dms, _dms - _dns))
print("duration histogram (contact grain):", _h, "sum", sum(_h), "3min+", sum(_h[3:]))
assert sum(_h) == _ods, "histogram does not sum to outbound dials"
assert sum(_h[3:]) == _ccs, "the 3-minute line does not match the call-connect rule"
assert _dns <= _dms, "demo connects exceed demos - the demo count must not move"
