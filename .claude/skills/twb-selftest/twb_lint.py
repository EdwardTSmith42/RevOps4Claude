#!/usr/bin/env python
"""Generic structural lint for generated/modified Tableau .twb files.

Encodes every Desktop schema rule (D2E8DA72 class) learned the hard way.
Read-only: parses, never re-serializes. Usage:

    python twb_lint.py "C:\\path\\to\\workbook.twb"

Exit 0 = pass, 1 = findings (printed). This is layer 1; the authoritative
check is twb_desktop_smoketest.ps1 (actually opening the file in Desktop).
"""
import re
import sys
import xml.etree.ElementTree as ET

# Authoritative <view> content model, Tableau 2026.1 base schema.
# Source: Desktop error D2E8DA72 (2026-06-10): element 'single-value-per-nest-
# shelf-sorts' is not allowed for content model '(datasources?,mapsources?,
# datasource-dependencies*,filter,((computed-sort)|(manual-sort)|(natural-sort)
# |(alphabetic-sort)),perspectives,shelf-sorts,slices?,aggregation)'
VIEW_ORDER = [
    "datasources", "mapsources", "datasource-dependencies", "filter",
    "computed-sort", "manual-sort", "natural-sort", "alphabetic-sort",
    "perspectives", "shelf-sorts", "slices", "aggregation",
]
# table children, known-valid prefix order (gotchas 54/55)
TABLE_ORDER = ["view", "style", "panes", "mark-layout", "rows", "cols"]

# attributes gated by document-format-change-manifest entries (gotcha 65)
MANIFEST_GATED = [
    ("enable-sort-zone-taborder", "AccessibleZoneTabOrder"),
    ("auto-generated", "AutoCreateAndUpdateDSDPhoneLayouts"),
    # D2E8DA72 (2026-06-10, AM Business Review build): relative-date filter
    # with period-type-v2= in a 2021.2-era-manifest file fails to load; the
    # attribute is gated by ISO8601PeriodTypes. Old grammar: period-type=.
    ("period-type-v2", "ISO8601PeriodTypes"),
]

# ELEMENTS gated by manifest entries. Same D2E8DA72 class as gated attributes:
# the tag is legal only when the manifest carries the entry. Verified by
# bisection 2026-06-10: identical <computed-sort> XML fails to load without
# <SortTagCleanup /> in the manifest and loads with it; every reference
# workbook containing <computed-sort> carries SortTagCleanup.
# single-value-per-nest-shelf-sorts is the same story with
# SingleValuePerNestSorting (Sales Territory Performance carries entry +
# element and loads; a generated old-manifest file with the element was
# rejected).
ELEMENT_MANIFEST_GATED = [
    ("computed-sort", "SortTagCleanup"),
    ("single-value-per-nest-shelf-sorts", "SingleValuePerNestSorting"),
]


def lint(path):
    errors = []
    warnings = []

    raw = open(path, encoding="utf-8").read()
    raw_nocdata = re.sub(r"<!\[CDATA\[.*?\]\]>", "", raw, flags=re.DOTALL)

    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        return [f"XML parse error: {e}"], []

    # ---- root order ----
    order = [c.tag for c in root]
    for a, b in [("datasources", "worksheets"), ("worksheets", "dashboards"),
                 ("dashboards", "windows")]:
        if a in order and b in order and order.index(a) > order.index(b):
            errors.append(f"root: <{a}> after <{b}>")

    manifest = root.find("document-format-change-manifest")
    manifest_entries = {c.tag.split("...")[-1] for c in manifest} if manifest is not None else set()

    # ---- manifest-gated attributes ----
    for attr, entry in MANIFEST_GATED:
        if f"{attr}=" in raw_nocdata and entry not in manifest_entries:
            errors.append(
                f"attribute '{attr}' used but manifest lacks <{entry} /> (D2E8DA72 'not declared')")

    # ---- datasource rules ----
    for ds in root.iter("datasource"):
        tags = [c.tag for c in ds]
        if "aliases" in tags and "column" in tags and tags.index("aliases") > tags.index("column"):
            errors.append(f"datasource {ds.get('name')}: <aliases> after first <column>")
        if "column" in tags and "column-instance" in tags:
            if max(i for i, t in enumerate(tags) if t == "column") > \
               min(i for i, t in enumerate(tags) if t == "column-instance"):
                errors.append(f"datasource {ds.get('name')}: <column> after <column-instance>")
        for col in ds.findall("column"):
            nm = col.get("name")
            if col.find("format") is not None:
                errors.append(f"column {nm}: <format> child not allowed (use worksheet style-rule)")
            ctags = [c.tag for c in col]
            if "calculation" in ctags and "desc" in ctags and \
               ctags.index("calculation") > ctags.index("desc"):
                errors.append(f"column {nm}: <calculation> must precede <desc>")
            if col.get("param-domain-type") and not col.get("value"):
                errors.append(f"parameter column {nm}: missing value= attribute ('value - empty text')")

    # ---- Custom SQL relations ----
    for rel in root.iter("relation"):
        if rel.get("type") == "text" and rel.text:
            sql = rel.text
            brackets = re.findall(r"<[^>]+>", sql)
            if brackets:
                errors.append(
                    f"Custom SQL has angle-bracket pattern(s) Tableau reads as parameter refs: {brackets[:3]}")
            if re.match(r"\s*WITH\b", sql, re.IGNORECASE):
                errors.append("Custom SQL starts with WITH/CTE (fails as derived table)")

    # ---- worksheets ----
    sheet_names = []
    for ws in root.iter("worksheet"):
        nm = ws.get("name")
        sheet_names.append(nm)
        table = ws.find("table")
        if table is None:
            errors.append(f"{nm}: no <table>")
            continue
        ttags = [c.tag for c in table]
        for req in ("view", "style", "panes", "rows", "cols"):
            if req not in ttags:
                errors.append(f"{nm}: missing <{req}> in table")
        known = [t for t in ttags if t in TABLE_ORDER]
        if known != sorted(known, key=TABLE_ORDER.index):
            errors.append(f"{nm}: table children out of order: {known}")

        view = table.find("view")
        if view is None:
            continue
        vtags = [c.tag for c in view]
        # ERROR: element not declared in the 2026.1 base view model (proven D2E8DA72).
        # Manifest-gated elements are legal only with their manifest entry present.
        gated_elements = dict(ELEMENT_MANIFEST_GATED)
        for t in vtags:
            if t in gated_elements:
                if gated_elements[t] not in manifest_entries:
                    errors.append(
                        f"{nm}: <{t}> requires manifest entry <{gated_elements[t]} /> "
                        f"(D2E8DA72 'not declared', observed 2026-06-10)")
            elif t not in VIEW_ORDER:
                errors.append(
                    f"{nm}: <{t}> not declared in 2026.1 view content model (D2E8DA72). "
                    f"Allowed: {VIEW_ORDER}")
        # Only minimal ordering is schema-fatal. Desktop-saved files (Bing Bong) legally
        # interleave filter and *-sort elements, so do NOT enforce the full sequence.
        if "datasources" in vtags and vtags.index("datasources") != 0:
            errors.append(f"{nm}: <datasources> is not the first view child")
        if "aggregation" in vtags and vtags.index("aggregation") != len(vtags) - 1:
            warnings.append(f"{nm}: <aggregation> is not the last view child")
        if "slices" in vtags and "filter" in vtags:
            if vtags.index("slices") < max(i for i, t in enumerate(vtags) if t == "filter"):
                errors.append(f"{nm}: a <filter> appears after <slices>")

        # dependency integrity
        for deps in view.findall("datasource-dependencies"):
            dtags = [c.tag for c in deps]
            if "column" in dtags and "column-instance" in dtags:
                if max(i for i, t in enumerate(dtags) if t == "column") > \
                   min(i for i, t in enumerate(dtags) if t == "column-instance"):
                    # Desktop emits interleaved deps in saved files; convention only.
                    warnings.append(f"{nm}: deps <column> after <column-instance> (convention)")
            dep_cols = {c.get("name", "").strip("[]") for c in deps.findall("column")}
            for ci in deps.findall("column-instance"):
                src = (ci.get("column") or "").strip("[]")
                if src and src not in dep_cols:
                    errors.append(f"{nm}: instance {ci.get('name')} references undeclared column [{src}]")

        # shelf / encoding refs must be declared instances (per datasource)
        inst_by_ds = {}
        for deps in view.findall("datasource-dependencies"):
            dsn = deps.get("datasource")
            inst_by_ds.setdefault(dsn, set())
            for ci in deps.findall("column-instance"):
                inst_by_ds[dsn].add(ci.get("name", "").strip("[]"))
            for cc in deps.findall("column"):
                inst_by_ds[dsn].add(cc.get("name", "").strip("[]"))
        ref_re = re.compile(r"\[([^\]]+)\]\.\[([^\]]+)\]")

        def check_ref(text, where):
            for dsn, ref in ref_re.findall(text or ""):
                if dsn == "Parameters" or ref in (":Measure Names", "Multiple Values"):
                    continue
                if ref.startswith("Action (") or ref.startswith("none:Action"):
                    continue
                if dsn in inst_by_ds and ref not in inst_by_ds[dsn]:
                    errors.append(f"{nm}: {where} ref [{ref}] not declared in deps of {dsn}")

        for shelf in ("rows", "cols"):
            el = table.find(shelf)
            if el is not None:
                if el.text and ":Measure Values]" in el.text:
                    errors.append(f"{nm}: <{shelf}> uses fake field ':Measure Values'")
                check_ref(el.text, shelf)
        for pane in table.findall("panes/pane"):
            enc = pane.find("encodings")
            if enc is not None:
                if enc.find("detail") is not None:
                    errors.append(f"{nm}: <detail> in encodings (use <lod>)")
                for e in enc:
                    check_ref(e.get("column", ""), f"encoding <{e.tag}>")
        for f in view.findall("filter"):
            check_ref(f.get("column", ""), "filter")

    # ---- dashboards ----
    for dashes in root.iter("dashboards"):
        for dash in dashes.findall("dashboard"):
            dname = dash.get("name")
            # zone-id uniqueness applies within the MAIN <zones> block only;
            # devicelayouts legitimately reuse the same ids (Desktop-saved output).
            main_zones = dash.find("zones")
            if main_zones is not None:
                ids = [z.get("id") for z in main_zones.iter("zone")]
                if len(ids) != len(set(ids)):
                    errors.append(f"dashboard {dname}: duplicate zone ids in main <zones>")
            for z in dash.iter("zone"):
                if z.get("type-v2") is None and z.get("name") and z.get("name") not in sheet_names:
                    errors.append(
                        f"dashboard {dname}: zone references unknown sheet {z.get('name')}")
            dl = dash.find("devicelayouts")
            if dl is not None and len(dl) == 0:
                errors.append(f"dashboard {dname}: empty <devicelayouts> (must be absent or populated)")
            # 2805CF18 class (2026-06-10): filter/paramctrl zones require the dashboard
            # itself to declare the datasource AND the referenced field in dashboard-level
            # <datasources> + <datasource-dependencies>, like Desktop-saved output does.
            dash_inst = {}
            for deps in dash.findall("datasource-dependencies"):
                dsn = deps.get("datasource")
                dash_inst.setdefault(dsn, set())
                for c in deps.findall("column"):
                    dash_inst[dsn].add(c.get("name", "").strip("[]"))
                for ci in deps.findall("column-instance"):
                    dash_inst[dsn].add(ci.get("name", "").strip("[]"))
            dash_ds_decl = {d.get("name") for d in dash.findall("datasources/datasource")}
            zone_ref_re = re.compile(r"\[([^\]]+)\]\.\[([^\]]+)\]")
            for z in dash.iter("zone"):
                if z.get("type-v2") in ("filter", "paramctrl"):
                    param = z.get("param", "")
                    m = zone_ref_re.match(param)
                    if not m:
                        continue
                    dsn, ref = m.group(1), m.group(2)
                    if dsn == "Parameters":
                        continue
                    if dsn not in dash_ds_decl:
                        errors.append(
                            f"dashboard {dname}: {z.get('type-v2')} zone uses datasource {dsn} "
                            f"but dashboard has no <datasources> entry for it (2805CF18 risk)")
                    if dsn not in dash_inst or ref not in dash_inst[dsn]:
                        errors.append(
                            f"dashboard {dname}: {z.get('type-v2')} zone param [{ref}] not declared "
                            f"in dashboard-level datasource-dependencies (2805CF18 risk)")

    # ---- windows ----
    windows = root.find("windows")
    if windows is not None:
        wlist = windows.findall("window")
        if wlist and any(w.get("class") == "dashboard" for w in wlist) and \
           wlist[-1].get("class") != "dashboard":
            # convention for generated files; Desktop-saved files violate it and load fine
            warnings.append("windows: dashboard window is not last (convention)")
        for w in wlist:
            for strip in w.iter("strip"):
                if not (strip.get("size") or "").isdigit():
                    errors.append(f"window {w.get('name')}: non-integer strip size")

    return errors, warnings


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    errs, warns = lint(sys.argv[1])
    for w in warns:
        print("WARN:", w)
    if errs:
        print(f"FAIL: {len(errs)} finding(s) in {sys.argv[1]}")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    print(f"PASS (static lint): {sys.argv[1]}")
    print("Static lint is NOT proof Desktop will open it. Run twb_desktop_smoketest.ps1 next.")
