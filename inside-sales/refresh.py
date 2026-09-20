import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
PY = sys.executable
LOG = os.path.join(DATA, "refresh_log.json")

MAX_DRIFT = 0.60
MAX_BUILT_MB = 15.0
PERIOD_KEYS = ("thisWeek", "lastWeek", "mtd", "lastMonth", "last90")


class Gate(Exception):
    pass


class Step(object):
    def __init__(self, name):
        self.name = name
        self.t0 = time.time()
        self.rec = {"step": name, "status": "RUNNING", "counts": {}, "notes": []}
        print("[%s] START" % name, flush=True)

    def note(self, m):
        self.rec["notes"].append(m)
        print("    %s" % m, flush=True)

    def ok(self, **counts):
        self.rec["counts"].update(counts)
        self.rec["status"] = "OK"
        self.rec["seconds"] = round(time.time() - self.t0, 1)
        print("[%s] OK   %.1fs  %s" % (self.name, self.rec["seconds"],
                                       fmt_counts(self.rec["counts"])), flush=True)
        return self.rec

    def skip(self, why):
        self.rec["status"] = "SKIPPED"
        self.rec["seconds"] = round(time.time() - self.t0, 1)
        self.rec["notes"].append(why)
        print("[%s] SKIP %s" % (self.name, why), flush=True)
        return self.rec

    def staged(self, **counts):
        self.rec["counts"].update(counts)
        self.rec["status"] = "STAGED"
        self.rec["seconds"] = round(time.time() - self.t0, 1)
        print("[%s] STAGED %.1fs  %s" % (self.name, self.rec["seconds"],
                                         fmt_counts(self.rec["counts"])), flush=True)
        return self.rec

    def fail(self, why):
        self.rec["status"] = "FAIL"
        self.rec["seconds"] = round(time.time() - self.t0, 1)
        self.rec["error"] = why
        print("[%s] FAIL %.1fs  %s" % (self.name, self.rec["seconds"], why), flush=True)
        return self.rec


def fmt_counts(c):
    return " ".join("%s=%s" % (k, v) for k, v in c.items())


def sh(args, step, timeout=5400):
    p = subprocess.run([PY] + args, cwd=HERE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    tail = (p.stderr or "").strip().splitlines()
    for line in tail[-12:]:
        step.note(line)
    if p.returncode != 0:
        raise Gate("%s exited %d: %s" % (" ".join(args), p.returncode,
                                         (tail[-1] if tail else (p.stdout or "")[-300:])))
    return p.stdout


def read_json(p, what):
    if not os.path.exists(p):
        raise Gate("%s is missing (%s)" % (os.path.relpath(p, HERE), what))
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception as e:
        raise Gate("%s is not valid JSON: %s" % (os.path.relpath(p, HERE), e))


def read_pids():
    p = os.path.join(DATA, "sourced_pids.txt")
    if not os.path.exists(p):
        return []
    raw = open(p, encoding="utf-8").read().strip()
    return [x.strip().strip("'") for x in raw.split(",") if x.strip()]


def prior_counts():
    p = os.path.join(DATA, "summary.json")
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8")).get("counts")
    except Exception:
        return None


def gate_extract(step, prev):
    s = read_json(os.path.join(DATA, "summary.json"), "extract output")
    c = s.get("counts") or {}
    leads = int(c.get("leads") or 0)
    if leads <= 0:
        raise Gate("extract produced 0 contacts")
    drift = None
    if prev and prev.get("leads"):
        drift = (leads - prev["leads"]) / float(prev["leads"])
        if abs(drift) > MAX_DRIFT:
            raise Gate("contact count moved %+.0f%% (%d -> %d), past the +/-%d%% gate. That is "
                       "how a broken pull or a silently truncated search presents. Nothing was "
                       "published." % (drift * 100, prev["leads"], leads, MAX_DRIFT * 100))
        step.note("contact count %d -> %d (%+.1f%%), inside the gate" %
                  (prev["leads"], leads, drift * 100))
    else:
        step.note("no previous summary.json - drift gate skipped on this first run")
    w = s.get("window") or {}
    step.note("window %s .. %s" % (w.get("start"), w.get("end")))
    return {"contacts": leads, "companies": c.get("companies"), "calls": c.get("calls"),
            "meetings": c.get("meetings"), "emails": c.get("emails"),
            "driftPct": round(drift * 100, 1) if drift is not None else None,
            "window": [w.get("start"), w.get("end")]}


def gate_revenue(step):
    r = read_json(os.path.join(DATA, "revenue.json"), "revenue output")
    p = r.get("periods") or {}
    missing = [k for k in PERIOD_KEYS if k not in p]
    if missing:
        raise Gate("revenue.json is missing period bucket(s): %s" % ", ".join(missing))
    if p["last90"].get("value") is None:
        raise Gate("revenue.json last90 value is null")
    for k in PERIOD_KEYS:
        if p[k].get("value") is None:
            raise Gate("revenue.json %s value is null" % k)
    if not r.get("caveats"):
        raise Gate("revenue.json lost its caveats block")
    cancel = [c for c in r["caveats"] if "cancel" in c.lower()]
    if not cancel:
        raise Gate("revenue.json no longer carries the cancellation-restatement caveat")
    for m in (r.get("monthly") or []):
        if m.get("providers") is None:
            raise Gate("monthly series has a null provider count for %s; the page prints it "
                       "verbatim and would render 'null providers'" % m.get("m"))
    step.note("asOf %s, cohort %s providers" % (r.get("asOf"), r.get("sourcedProviders")))
    return {"last90": p["last90"]["value"], "thisWeek": p["thisWeek"]["value"],
            "contracts90": p["last90"].get("contracts"),
            "cohort": r.get("sourcedProviders"), "asOf": r.get("asOf")}


def gate_build(step):
    built = os.path.join(HERE, "dashboard_built.html")
    if not os.path.exists(built):
        raise Gate("dashboard_built.html was not produced")
    h = open(built, encoding="utf-8").read()
    bad = sum(1 for ch in h if ord(ch) > 127)
    if bad:
        raise Gate("dashboard_built.html holds %d non-ASCII characters; the artifact wrapper "
                   "owns <head> so the page cannot declare a charset" % bad)
    mb = os.path.getsize(built) / 1048576.0
    if mb > MAX_BUILT_MB:
        raise Gate("dashboard_built.html is %.2f MB, past the %.0f MB gate (artifact ceiling "
                   "is 16 MB)" % (mb, MAX_BUILT_MB))
    for marker in ("/*__DATA__*/", "/*__REV__*/", "/*__VOM__*/", "/*__SRC__*/", "/*__DEALS__*/"):
        if marker in h:
            raise Gate("marker %s was never substituted - a payload is missing" % marker)
    step.note("%.2f MB, 0 non-ASCII" % mb)
    return {"builtMB": round(mb, 2), "nonAscii": 0}


def main():
    ap = argparse.ArgumentParser(description="Refresh the inside-sales dashboard end to end.")
    ap.add_argument("--skip-transcripts", action="store_true",
                    help="skip the transcript step entirely; the page keeps the themes it has")
    ap.add_argument("--skip-extract", action="store_true")
    ap.add_argument("--skip-revenue", action="store_true")
    ap.add_argument("--full-transcripts", action="store_true",
                    help="re-mine the whole corpus instead of only unmined calls (weekly)")
    ap.add_argument("--skip-deals", action="store_true",
                    help="skip the Deals chain; the page keeps the deals it has")
    a = ap.parse_args()

    started = dt.datetime.now()
    log = {"startedAt": started.isoformat(timespec="seconds"), "steps": [],
           "argv": sys.argv[1:], "status": "RUNNING"}

    def flush():
        log["finishedAt"] = dt.datetime.now().isoformat(timespec="seconds")
        log["seconds"] = round((dt.datetime.now() - started).total_seconds(), 1)
        tmp = LOG + ".tmp"
        json.dump(log, open(tmp, "w", encoding="utf-8"), indent=1)
        os.replace(tmp, LOG)

    prev = prior_counts()
    prev_pids = read_pids()

    try:
        s = Step("extract")
        if a.skip_extract:
            log["steps"].append(s.skip("--skip-extract"))
        else:
            sh(["extract.py"], s)
            log["steps"].append(s.ok(**gate_extract(s, prev)))
            log["window"] = log["steps"][-1]["counts"].get("window")

        s = Step("cohort")
        sh(["build.py"], s)
        pids = read_pids()
        if not pids:
            raise Gate("build.py produced an empty data/sourced_pids.txt, so the revenue step "
                       "has no cohort to query")
        if prev_pids is not None and prev_pids:
            move = abs(len(pids) - len(prev_pids)) / float(len(prev_pids))
            if move > MAX_DRIFT:
                raise Gate("sourced cohort moved %+.0f%% (%d -> %d providers) - the revenue "
                           "figures would not be comparable to yesterday's"
                           % ((len(pids) - len(prev_pids)) / float(len(prev_pids)) * 100,
                              len(prev_pids), len(pids)))
            s.note("cohort %d -> %d providers, %d added, %d dropped"
                   % (len(prev_pids), len(pids), len(set(pids) - set(prev_pids)),
                      len(set(prev_pids) - set(pids))))
        log["steps"].append(s.ok(cohort=len(pids)))

        s = Step("revenue")
        if a.skip_revenue:
            s.note("--skip-revenue: gating the existing data/revenue.json instead")
        else:
            sh(["tableau_revenue.py"], s)
        c = gate_revenue(s)
        if a.skip_revenue:
            c["refreshed"] = False
        log["steps"].append(s.ok(**c))

        # Deals are owner-scoped, not date-bounded, so extract.py does not touch
        # them - they come from their own three-script chain. Without this step the
        # Deals section silently freezes at whatever generatedAtUtc happened to be
        # committed while every other number on the page rolls forward, which is a
        # worse failure than an empty table because it looks current.
        s = Step("deals")
        if a.skip_deals:
            log["steps"].append(s.skip("--skip-deals"))
        else:
            for script in ("pull_deals.py", "resolve_deals.py", "build_deals.py"):
                sh([script], s)
            dj = os.path.join(DATA, "deals.json")
            if not os.path.exists(dj):
                raise Gate("the deals chain did not produce data/deals.json")
            d = json.load(open(dj, encoding="utf-8"))
            rows = d.get("deals") or []
            if not rows:
                raise Gate("data/deals.json has no deals; the page would render an empty "
                           "Deals section as though the AEs have no open opportunities")
            gen = (d.get("generatedAtUtc") or "")[:10]
            today = dt.date.today().isoformat()
            if gen != today:
                raise Gate("data/deals.json is stamped %s, not today (%s) - the chain ran but "
                           "did not rewrite the file" % (gen or "(none)", today))
            resolved = sum(1 for r in rows if r.get("providerIds"))
            log["steps"].append(s.ok(deals=len(rows), resolved=resolved,
                                     unlinked=len(rows) - resolved, generatedAtUtc=d.get("generatedAtUtc")))

        s = Step("transcripts")
        if a.skip_transcripts:
            log["steps"].append(s.skip("--skip-transcripts"))
        else:
            args = ["mine_transcripts.py"]
            if a.full_transcripts:
                args.append("--full")
            out = sh(args, s)
            res = json.loads(out) if out.strip() else {}
            st = res.get("stage") or {}
            mg = res.get("merge") or {}
            counts = {"staged": st.get("staged", 0), "corpus": st.get("corpusTotal", 0),
                      "mode": st.get("mode", "incremental")}
            if mg:
                counts.update({"themes": mg.get("themes"), "themesAdded": mg.get("themesAdded"),
                               "themesUpdated": mg.get("themesUpdated")})
            if st.get("staged"):
                s.note("NEXT: read the files in data/transcripts_new, write data/vom_delta.json, "
                       "then re-run: python refresh.py --skip-extract --skip-revenue")
                log["steps"].append(s.staged(**counts))
                log["pendingMine"] = {"staged": st.get("staged"),
                                      "dir": st.get("stagedDir"),
                                      "manifest": "data/transcripts_new_manifest.jsonl"}
            else:
                log["steps"].append(s.ok(**counts))

        s = Step("build")
        sh(["build.py"], s)
        if read_pids() != pids:
            raise Gate("the sourced cohort changed between the cohort step and the final build; "
                       "the revenue figures on the page would be cut from a different set of "
                       "practices than the activity figures")
        log["steps"].append(s.ok(**gate_build(s)))

        log["status"] = "OK"
        pend = log.get("pendingMine")
        if pend:
            log["status"] = "OK_PENDING_MINE"
        flush()
        print("\nREFRESH %s in %.0fs" % (log["status"], log["seconds"]))
        if pend:
            print("  %d new calls staged in %s - mine them, then re-run with "
                  "--skip-extract --skip-revenue" % (pend["staged"], pend["dir"]))
        print("  log: data/refresh_log.json")
        # Exit 2, not 0: staged-but-unmined is NOT success. 0 means the dashboard is
        # fully refreshed; 1 means it failed and nothing should publish; 2 means the
        # page is publishable but transcripts still need a mining pass. A caller that
        # only tests "exit == 0" would otherwise report success forever while the
        # themes silently never update.
        return 2 if pend else 0

    except Gate as e:
        if log["steps"] and log["steps"][-1].get("status") == "RUNNING":
            log["steps"][-1]["status"] = "FAIL"
            log["steps"][-1]["error"] = str(e)
        else:
            log["steps"].append({"step": "gate", "status": "FAIL", "error": str(e)})
        log["status"] = "FAIL"
        log["error"] = str(e)
        flush()
        print("\nREFRESH FAILED: %s" % e, file=sys.stderr)
        print("Nothing was published. See data/refresh_log.json.", file=sys.stderr)
        return 1
    except Exception as e:
        log["status"] = "FAIL"
        log["error"] = "%s: %s" % (type(e).__name__, e)
        flush()
        print("\nREFRESH CRASHED: %s" % log["error"], file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
