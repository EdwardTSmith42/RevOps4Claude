import datetime as dt
import json
import os
import sys
import time

from extract import DATA, START, START_MS, TEAM, TEAM_OF, post

PROPS = ["hs_timestamp", "hs_meeting_title", "hs_meeting_outcome", "hubspot_owner_id",
         "hs_meeting_start_time", "hs_meeting_end_time", "hs_meeting_recording_duration"]


def is_demo(p):
    return "demo" in (p.get("hs_meeting_title") or "").lower()


def search(filters):
    out, after = [], None
    while True:
        payload = {"filterGroups": [{"filters": filters}], "properties": PROPS, "limit": 100,
                   "sorts": [{"propertyName": "hs_meeting_start_time", "direction": "ASCENDING"}]}
        if after:
            payload["after"] = after
        d = post("/crm/v3/objects/meetings/search", payload)
        out.extend(d.get("results", []))
        after = d.get("paging", {}).get("next", {}).get("after")
        if not after:
            return out
        if len(out) >= 9900:
            sys.exit("demo calendar hit the 10k search cap - split the pull before trusting it")


def main():
    now = dt.datetime.now(dt.timezone.utc)
    now_ms = int(now.timestamp() * 1000)
    today = dt.date.today().isoformat()
    rows = search([
        {"propertyName": "hubspot_owner_id", "operator": "IN", "values": list(TEAM)},
        {"propertyName": "hs_meeting_start_time", "operator": "GTE", "value": str(START_MS)},
    ])
    demos, canceled, future = [], 0, 0
    for m in rows:
        p = m.get("properties", {})
        if not is_demo(p):
            continue
        start = p.get("hs_meeting_start_time") or p.get("hs_timestamp") or ""
        if not start:
            continue
        outcome = p.get("hs_meeting_outcome") or ""
        if outcome == "CANCELED":
            canceled += 1
            continue
        try:
            rec = int(p.get("hs_meeting_recording_duration") or 0)
        except (TypeError, ValueError):
            rec = 0
        rep = TEAM.get(p.get("hubspot_owner_id"))
        start_ms = int(dt.datetime.strptime(start[:19], "%Y-%m-%dT%H:%M:%S")
                       .replace(tzinfo=dt.timezone.utc).timestamp() * 1000)
        is_future = start_ms >= now_ms
        future += is_future
        demos.append({
            "id": m["id"],
            "d": start[:10],
            "start": start[:16],
            "rep": rep,
            "seat": TEAM_OF.get(p.get("hubspot_owner_id")),
            "outcome": outcome,
            "rec": rec,
            "future": is_future,
        })
    out = {
        "asOf": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "asOfDate": today,
        "windowStart": START,
        "rule": {
            "demo": "'demo' appears in the Meeting name (case-insensitive)",
            "held": "Meeting recording duration >= 600000 ms (10 minutes)",
            "upcoming": "Meeting start time at or after the pull time, Meeting outcome is not Canceled",
            "owner": "Meeting owner is one of the six Inside Sales / SDR reps",
        },
        "counts": {"meetings_pulled": len(rows), "demos": len(demos), "canceled_dropped": canceled,
                   "future": future, "past": len(demos) - future},
        "meetings": demos,
    }
    path = os.path.join(DATA, "demo_calendar.json")
    json.dump(out, open(path, "w", encoding="utf-8"), separators=(",", ":"))
    print("demo calendar: %d meetings pulled, %d demo-titled, %d canceled dropped, %d past, %d upcoming"
          % (len(rows), len(demos), canceled, len(demos) - future, future), file=sys.stderr)
    print(json.dumps(out["counts"]))


if __name__ == "__main__":
    main()
