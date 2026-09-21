import argparse
import collections
import datetime as dt
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
STAGE = os.path.join(DATA, "transcripts_new")
CACHE = os.path.join(DATA, "transcript_cache.jsonl")
STATE = os.path.join(DATA, "vom_state.json")
DELTA = os.path.join(DATA, "vom_delta.json")
VOM = os.path.join(DATA, "voice_of_market.json")
VOM_SLIM = os.path.join(DATA, "vom_slim.json")
RAW_CALLS = os.path.join(DATA, "raw_calls.jsonl")
HS = os.environ.get("HUBSPOT_CLI", r"C:/Users/esmith/.hubspot/bin/hubspot.exe")

OWN = {"84616314", "96412056", "88456783", "96412059", "96412054", "80632115"}
DISPO = {"9d9162e7-6cf3-4944-bf63-4dff82258764": "Busy",
         "f240bbac-87c9-4f6e-bf70-924b57d47db7": "Connected",
         "a4c4c377-d246-4b32-a13b-75a56a4cd0ff": "Left live message",
         "b2cf5968-551e-4856-9783-52b3da59a7d0": "Left voicemail",
         "2e7360c1-6b71-40e9-ab2b-30ae98a4678c": "Meeting booked",
         "73a0d17f-1163-4015-bdd5-ec830791da20": "No answer",
         "17b47fee-58de-441e-a44c-c6300d46f273": "Wrong number"}
MIN_SPEECH = 120
STAGE_CAP = 250
TREND_RECENT_DAYS = 7

PRIV = ("PRIVACY: raw business-call text. Speaker labels de-identified; IN-TEXT personal names, "
        "practice staff names and health/financial details are NOT redacted. Downstream output "
        "must de-identify: role descriptors only, quotes <= 25 words. Never reproduce passages "
        "wholesale.")


def load_state():
    if os.path.exists(STATE):
        try:
            s = json.load(open(STATE, encoding="utf-8"))
            s.setdefault("mined_ids", [])
            s.setdefault("last_mined_ts", "")
            s.setdefault("last_mined_call_id", "")
            s.setdefault("runs", [])
            return s
        except Exception:
            pass
    return {"mined_ids": [], "last_mined_ts": "", "last_mined_call_id": "", "runs": []}


def save_state(s):
    tmp = STATE + ".tmp"
    json.dump(s, open(tmp, "w", encoding="utf-8"), indent=1)
    os.replace(tmp, STATE)


def strip_html(s):
    s = re.sub(r"<br\s*/?>|</p>|</h\d>|</li>|</tr>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"[ \t]+", " ", html.unescape(s)).strip()


def speech_chars(t):
    return sum(len(w) for w in re.findall(r"\S+", t) if re.search(r"[A-Za-z]", w))


def render(rec):
    utts = [u for u in (rec.get("utterances") or []) if (u.get("text") or "").strip()]
    if not utts:
        return [], False, rec.get("transcriptSource"), ""
    lab, ctr = {}, collections.Counter()
    for u in utts:
        sp = u.get("speaker") or {}
        role = (sp.get("role") or "").upper()
        key = (role, sp.get("integrationId") or sp.get("name") or "?")
        if key not in lab:
            base = "REP" if role == "AGENT" else "PROSPECT" if role == "VISITOR" else "SPEAKER"
            ctr[base] += 1
            lab[key] = base if (base != "SPEAKER" and ctr[base] == 1) else "%s_%d" % (base, ctr[base])
    lines = []
    for u in utts:
        sp = u.get("speaker") or {}
        key = ((sp.get("role") or "").upper(), sp.get("integrationId") or sp.get("name") or "?")
        lines.append("%s: %s" % (lab[key], (u.get("text") or "").strip()))
    raw = "\n".join((u.get("text") or "").strip() for u in utts)
    return lines, len(set(lab.values())) > 1, rec.get("transcriptSource"), raw


def read_cache():
    cache = {}
    if os.path.exists(CACHE):
        for l in open(CACHE, encoding="utf-8"):
            try:
                x = json.loads(l)
                cache[x["id"]] = x.get("rec")
            except Exception:
                pass
    return cache


def fetch_transcripts(ids, log):
    have = set(read_cache())
    todo = [c for c in ids if c not in have]
    if not todo:
        log("transcript cache already covers all %d calls" % len(ids))
        return
    if not (os.path.exists(HS) or shutil.which(HS) or shutil.which("hubspot")):
        raise SystemExit(
            "the HubSpot CLI is not on this machine (looked for %s), so %d new calls cannot have "
            "their transcripts fetched. This step needs a runner that has the CLI installed and "
            "authenticated. Re-run with --skip-transcripts to publish without new themes, or "
            "point HUBSPOT_CLI at the binary." % (HS, len(todo)))
    env = dict(os.environ)

    def parse(s):
        i = s.find("{")
        return json.loads(s[i:]) if i >= 0 else None

    def fetch(cid):
        for _ in range(3):
            try:
                p = subprocess.run([HS, "activities", "transcript", "get", cid, "--format", "json"],
                                   capture_output=True, text=True, encoding="utf-8",
                                   errors="replace", env=env, timeout=120)
                d = parse(p.stdout)
            except Exception:
                d = None
            if d and d.get("ok"):
                return {"id": cid, "ok": True, "rec": (d.get("data") or [None])[0]}
            time.sleep(1.5)
        return {"id": cid, "ok": False, "rec": None}

    n = fails = 0
    with open(CACHE, "a", encoding="utf-8") as f, ThreadPoolExecutor(max_workers=6) as ex:
        for res in ex.map(fetch, todo):
            f.write(json.dumps(res) + "\n")
            n += 1
            if not res["ok"]:
                fails += 1
    log("fetched %d new transcripts (%d failed)" % (n, fails))


def build_records(call_rows, cache):
    recs = []
    for r in call_rows:
        p = r.get("properties", {})
        cid = r["id"]
        rec = cache.get(cid)
        lines, diar, tsrc, src, raw = [], False, None, "NONE", ""
        if rec:
            lines, diar, tsrc, raw = render(rec)
            if lines:
                src = "TRANSCRIPT"
        for prop, tag in (("hs_call_summary", "AI_SUMMARY"), ("hs_call_body", "CALL_BODY")):
            if speech_chars(raw) < MIN_SPEECH and (p.get(prop) or "").strip():
                alt = strip_html(p[prop])
                if speech_chars(alt) > speech_chars(raw):
                    lines, raw, src, diar = [alt], alt, tag, False
        body = "\n".join(lines)
        recs.append(dict(id=cid, date=p.get("hs_timestamp") or "",
                         ownerId=str(p.get("hubspot_owner_id")),
                         durationSec=round(int(p.get("hs_call_duration") or 0) / 1000),
                         disposition=DISPO.get(p.get("hs_call_disposition"),
                                               p.get("hs_call_disposition") or "none"),
                         hasTranscript=(p.get("hs_call_has_transcript") or "").lower() == "true",
                         source=src, transcriptSource=tsrc or "NA", diarized=diar,
                         direction=p.get("hs_call_direction") or "NA",
                         utterances=len(lines) if src == "TRANSCRIPT" else 0,
                         chars=len(body), speech=speech_chars(raw), body=body))
    return recs


def stage(full, log, since=None, bootstrap_days=30):
    state = load_state()
    mined = set(state["mined_ids"])
    if not os.path.exists(RAW_CALLS):
        raise SystemExit("data/raw_calls.jsonl missing - extract.py has not run")
    rows = []
    for l in open(RAW_CALLS, encoding="utf-8"):
        try:
            r = json.loads(l)
        except Exception:
            continue
        p = r.get("properties", {})
        if str(p.get("hubspot_owner_id")) in OWN:
            rows.append(r)
    corpus_total = len(rows)

    def ts(r):
        return (r.get("properties", {}).get("hs_timestamp") or "")[:10]

    if full:
        candidates = rows
        cutoff = min([ts(r) for r in rows] or [""])
        log("--full: re-mining the entire %d-call corpus from %s" % (corpus_total, cutoff))
    else:
        cutoff = since or state.get("last_call_ts") or ""
        if not cutoff:
            newest = max([ts(r) for r in rows] or [""])
            if newest:
                cutoff = str(dt.date.fromisoformat(newest) - dt.timedelta(days=bootstrap_days))
            log("no prior state - bootstrapping from %s (%d days)" % (cutoff, bootstrap_days))
        candidates = [r for r in rows if r["id"] not in mined and ts(r) >= cutoff]
        log("incremental: %d of %d corpus calls are new since %s"
            % (len(candidates), corpus_total, cutoff or "the beginning"))
    newest_seen = max([ts(r) for r in candidates] or [cutoff or ""])

    want = [r["id"] for r in candidates
            if (r["properties"].get("hs_call_has_transcript") or "").lower() == "true"]
    fetch_transcripts(want, log)
    cache = read_cache()
    recs = build_records(candidates, cache)
    usable = [r for r in recs if r["speech"] >= MIN_SPEECH]
    thin = [r for r in recs if r["speech"] < MIN_SPEECH]
    usable.sort(key=lambda r: (r["date"], r["durationSec"]), reverse=True)
    sel = usable[:STAGE_CAP]
    deferred = usable[STAGE_CAP:]

    if os.path.isdir(STAGE):
        shutil.rmtree(STAGE)
    os.makedirs(STAGE)
    man = []
    for r in sel:
        hdr = ("callId=%s | date=%s | ownerId=%s | durationSec=%d | disposition=%s | source=%s "
               "| transcriptSource=%s | diarized=%s | direction=%s"
               % (r["id"], r["date"], r["ownerId"], r["durationSec"], r["disposition"],
                  r["source"], r["transcriptSource"], "yes" if r["diarized"] else "no",
                  r["direction"]))
        fp = os.path.join(STAGE, "%s.txt" % r["id"])
        open(fp, "w", encoding="utf-8").write(hdr + "\n" + PRIV + "\n\n" + r["body"] + "\n")
        man.append({"id": r["id"], "date": r["date"], "ownerId": r["ownerId"],
                    "durationSec": r["durationSec"], "disposition": r["disposition"],
                    "file": fp.replace("\\", "/"), "source": r["source"],
                    "speechChars": r["speech"]})
    with open(os.path.join(DATA, "transcripts_new_manifest.jsonl"), "w", encoding="utf-8") as f:
        for d in man:
            f.write(json.dumps(d) + "\n")

    skipped_ids = [r["id"] for r in thin]
    info = {"mode": "full" if full else "incremental",
            "corpusTotal": corpus_total,
            "cutoff": cutoff,
            "newestCallDate": newest_seen,
            "candidates": len(candidates),
            "usable": len(usable),
            "unusable": len(thin),
            "staged": len(sel),
            "deferredOverCap": len(deferred),
            "stagedDir": STAGE.replace("\\", "/"),
            "skippedIds": skipped_ids,
            "deferredIds": [r["id"] for r in deferred],
            "sources": dict(collections.Counter(d["source"] for d in man)),
            "perOwner": dict(collections.Counter(d["ownerId"] for d in man))}
    json.dump(info, open(os.path.join(DATA, "transcripts_stage.json"), "w", encoding="utf-8"), indent=1)
    log("staged %d call files in %s (usable %d, unusable %d, deferred over cap %d)"
        % (len(sel), STAGE, len(usable), len(thin), len(deferred)))
    return info


def _key(t):
    return (t.get("category") or "", (t.get("label") or "").strip().lower())


# The slim projection is what build.py actually embeds into the page, so any field
# the dashboard reads MUST be listed here. exampleCallIds was missing, which is why
# the Voice of the Market "Calls" column rendered a dash: the ids existed in
# voice_of_market.json and never reached the browser.
CALL_ID_CAP = 10          # HubSpot call links rendered per theme
SLIM_THEME_KEYS = ("category", "label", "description", "mentions30d", "mentions7d",
                   "trend", "distinctReps", "routeTo", "quotes", "exampleCallIds")


def write_slim(full):
    """Project voice_of_market.json down to vom_slim.json. Single source of truth for
    the whitelist, callable without a delta so an existing corpus can be re-projected
    (see --reslim)."""
    themes = full.get("themes") or []
    slim = {"corpusStats": full.get("corpusStats", {}),
            "themes": [{k: t.get(k) for k in SLIM_THEME_KEYS} for t in themes],
            "executiveRead": full.get("executiveRead", []),
            "dataQualityCaveats": full.get("dataQualityCaveats", []),
            "changedSinceLastRun": full.get("changedSinceLastRun", [])}
    tmp = VOM_SLIM + ".tmp"
    json.dump(slim, open(tmp, "w", encoding="utf-8"), separators=(",", ":"))
    os.replace(tmp, VOM_SLIM)
    return sum(1 for t in slim["themes"] if t.get("exampleCallIds"))


def merge(log, today=None):
    if not os.path.exists(DELTA):
        return None
    today = today or dt.date.today()
    delta = json.load(open(DELTA, encoding="utf-8"))
    base = json.load(open(VOM, encoding="utf-8")) if os.path.exists(VOM) else {"themes": []}
    state = load_state()

    by = {_key(t): t for t in base.get("themes", [])}
    added, updated = 0, 0
    for d in delta.get("themes", []):
        k = _key(d)
        inc = int(d.get("newMentions") or d.get("mentions30d") or 0)
        rec = int(d.get("newMentionsRecent") or d.get("mentions7d") or 0)
        if k in by:
            t = by[k]
            t["mentions30d"] = int(t.get("mentions30d") or 0) + inc
            t["mentions7d"] = rec
            if d.get("description"):
                t["description"] = d["description"]
            if d.get("routeTo"):
                t["routeTo"] = d["routeTo"]
            for q in (d.get("quotes") or []):
                if q not in t.setdefault("quotes", []):
                    t["quotes"].append(q)
            t["quotes"] = t["quotes"][:4]
            for c in (d.get("exampleCallIds") or []):
                if c not in t.setdefault("exampleCallIds", []):
                    t["exampleCallIds"].append(c)
            t["exampleCallIds"] = t["exampleCallIds"][-CALL_ID_CAP:]
            t["lastSeen"] = str(today)
            updated += 1
        else:
            t = {"category": d.get("category") or "OTHER",
                 "label": d.get("label") or "",
                 "description": d.get("description") or "",
                 "mentions30d": inc,
                 "mentions7d": rec,
                 "trend": "NEW",
                 "distinctReps": int(d.get("distinctReps") or 0),
                 "routeTo": d.get("routeTo") or "",
                 "quotes": (d.get("quotes") or [])[:4],
                 "exampleCallIds": (d.get("exampleCallIds") or [])[:CALL_ID_CAP],
                 "firstSeen": str(today),
                 "lastSeen": str(today)}
            by[k] = t
            added += 1

    themes = list(by.values())
    tot = sum(int(t.get("mentions30d") or 0) for t in themes) or 1
    totr = sum(int(t.get("mentions7d") or 0) for t in themes) or 1
    for t in themes:
        share = int(t.get("mentions30d") or 0) / tot
        share_r = int(t.get("mentions7d") or 0) / totr
        if t.get("trend") == "NEW" and t.get("firstSeen") == str(today):
            continue
        if share_r > share * 1.25:
            t["trend"] = "RISING"
        elif share_r < share * 0.75:
            t["trend"] = "FADING"
        else:
            t["trend"] = "STEADY"
    themes.sort(key=lambda t: -int(t.get("mentions30d") or 0))

    stats = base.get("corpusStats") or {}
    stage_info = {}
    sp = os.path.join(DATA, "transcripts_stage.json")
    if os.path.exists(sp):
        stage_info = json.load(open(sp, encoding="utf-8"))
    mined_now = delta.get("callsAnalyzed") or stage_info.get("staged") or 0
    if stage_info.get("mode") == "full":
        stats["callsAnalyzed"] = mined_now
    else:
        stats["callsAnalyzed"] = int(stats.get("callsAnalyzed") or 0) + int(mined_now)
    stats["canonicalThemes"] = len(themes)
    stats["windowEnd"] = str(today)
    stats.setdefault("windowStart", base.get("corpusStats", {}).get("windowStart", ""))
    stats["lastIncrementOn"] = str(today)
    stats["lastIncrementCalls"] = int(mined_now)
    stats["mode"] = stage_info.get("mode", "incremental")

    out = dict(base)
    out["corpusStats"] = stats
    out["themes"] = themes
    if delta.get("executiveRead"):
        out["executiveRead"] = delta["executiveRead"]
    if delta.get("changedSinceLastRun"):
        out["changedSinceLastRun"] = delta["changedSinceLastRun"]
    if delta.get("dataQualityCaveats"):
        out["dataQualityCaveats"] = delta["dataQualityCaveats"]

    tmp = VOM + ".tmp"
    json.dump(out, open(tmp, "w", encoding="utf-8"), indent=1)
    os.replace(tmp, VOM)

    write_slim(out)

    newly = list(stage_info.get("skippedIds") or [])
    for fn in os.listdir(STAGE) if os.path.isdir(STAGE) else []:
        if fn.endswith(".txt"):
            newly.append(fn[:-4])
    mined = set(state["mined_ids"]) | set(newly)
    state["mined_ids"] = sorted(mined)
    if newly:
        state["last_mined_call_id"] = sorted(newly)[-1]
    state["last_mined_ts"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    state["runs"] = (state["runs"] + [{"on": str(today), "mode": stats["mode"],
                                       "calls": int(mined_now), "themesAdded": added,
                                       "themesUpdated": updated}])[-30:]
    save_state(state)

    shutil.move(DELTA, os.path.join(DATA, "vom_delta.applied.json"))
    log("merged delta: %d themes updated, %d added, %d themes total, %d calls now mined"
        % (updated, added, len(themes), len(state["mined_ids"])))
    return {"themesUpdated": updated, "themesAdded": added, "themes": len(themes),
            "callsMinedTotal": len(state["mined_ids"]), "callsThisRun": int(mined_now)}


def seed_state(log):
    state = load_state()
    ids, newest = set(state["mined_ids"]), state.get("last_call_ts") or ""
    for fn in ("transcripts_manifest.jsonl", "skipped_calls.jsonl"):
        p = os.path.join(DATA, fn)
        if not os.path.exists(p):
            continue
        n = 0
        for l in open(p, encoding="utf-8"):
            try:
                d = json.loads(l)
            except Exception:
                continue
            ids.add(d["id"])
            newest = max(newest, (d.get("date") or "")[:10])
            n += 1
        log("seeded %d ids from %s" % (n, fn))
    state["mined_ids"] = sorted(ids)
    state["last_call_ts"] = newest
    state["last_mined_ts"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    state["seededFrom"] = "the 2026-09-08 build_corpus3 run"
    save_state(state)
    return {"minedIds": len(ids), "watermark": newest}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true",
                    help="re-mine the entire corpus instead of only unmined calls")
    ap.add_argument("--since", default=None,
                    help="stage calls on or after this date instead of the stored watermark")
    ap.add_argument("--bootstrap-days", type=int, default=30)
    ap.add_argument("--seed-state", action="store_true",
                    help="mark the calls already mined by the 0908 corpus run as mined, so the "
                         "first incremental run does not re-mine three months of history")
    ap.add_argument("--stage-only", action="store_true")
    ap.add_argument("--merge-only", action="store_true")
    ap.add_argument("--reslim", action="store_true",
                    help="re-project data/voice_of_market.json into vom_slim.json with the "
                         "current whitelist and exit; no mining, no state change")
    a = ap.parse_args()

    if a.reslim:
        full = json.load(open(VOM, encoding="utf-8"))
        n = write_slim(full)
        print(json.dumps({"reslim": {"themes": len(full.get("themes") or []),
                                     "withCallIds": n, "wrote": os.path.basename(VOM_SLIM)}}))
        return 0

    def log(m):
        print("  " + m, file=sys.stderr)

    if a.seed_state:
        print(json.dumps(seed_state(log), indent=1))
        return 0

    res = {}
    if not a.stage_only:
        m = merge(log)
        if m:
            res["merge"] = m
        elif a.merge_only:
            log("no data/vom_delta.json to merge")
    if not a.merge_only:
        res["stage"] = stage(a.full, log, a.since, a.bootstrap_days)
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
