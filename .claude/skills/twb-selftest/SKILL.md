---
name: twb-selftest
description: Use when about to deliver, publish, or hand off any programmatically generated or modified Tableau workbook (.twb/.twbx), or when Tableau Desktop rejects a file with D2E8DA72, 2805CF18, "no declaration found for element", "not allowed for content model", or "Unable to complete action" load errors.
---

# TWB Self-Test Before Delivery

## Overview

Tableau's workbook schema is compiled into Desktop; no public XSD exists. Hand-rolled structural checks always lag the real grammar, so the only authoritative validation is Tableau Desktop opening the file. This skill gates delivery behind two layers: a static lint and a scripted Desktop open test.

**Iron rule: a generated or modified TWB is NOT done until the Desktop smoke test passes on this machine. Static lint passing is not done. "It validated" is not done.**

Origin (baseline failure, 2026-06-10): a workbook passed a thorough hand-rolled validator and was delivered; Desktop rejected it with D2E8DA72 (`single-value-per-nest-shelf-sorts` not declared). The fix then failed AGAIN with 2805CF18 (dashboard filter zones without dashboard-level datasource-dependencies). The smoke test caught the second bug before the user did. Two consecutive escapes from static-only checking is the proof this gate is mandatory.

## The Gate (run both, in order)

```powershell
# Layer 1: static lint (~1s). Catches all KNOWN Desktop rejection classes.
python C:\Users\esmith\.claude\skills\twb-selftest\twb_lint.py "C:\path\book.twb"

# Layer 2: authoritative. Launches Desktop, watches for the error dialog via UI
# automation, kills the process after. Needs no credentials: load errors fire
# before sign-in. ALWAYS pass -ExpectText with a real sheet/dashboard name from
# the workbook; PASS then requires the workbook's own UI to render (a bare
# window title "Tableau" can be the start page, not your file).
powershell -ExecutionPolicy Bypass -File C:\Users\esmith\.claude\skills\twb-selftest\twb_desktop_smoketest.ps1 `
    -Path "C:\path\book.twb" -ExpectText "Some Sheet Name"
```

Exit codes: 0 pass, 1 Desktop showed a load error (dialog text printed), 2 inconclusive. Full UI text blob is written to `%TEMP%\twb_smoketest_last.txt` for post-mortem. The smoke test only watches and kills Tableau processes it spawned; a user's open instance is untouched (but warn the user a Tableau window will flash up, and avoid racing a single-instance handoff by checking `Get-Process tableau` first).

### Live Custom SQL workbooks stall the standard smoke test (2026-07-07)

A workbook with a live Custom SQL relation shows the **"Custom SQL Warning"** dialog ("This document contains one or more custom SQL connections... Do you want to connect?") immediately after parse. The standard smoke test cannot answer it, so `-ExpectText` times out with exit 2 even on a good file. Facts:

- Reaching that dialog IS a positive parse signal: load errors (D2E8DA72 / 2805CF18) fire before it. Check `%TEMP%\twb_smoketest_last.txt` for the dialog text.
- Answering **No does NOT mean "open without connecting"** -- Desktop abandons the workbook and lands on the start page. Answer **Yes**; if credentials are saved Desktop connects, otherwise cancel the sign-in and the workbook shell still renders (tabs, dashboard scaffold, filter cards) with a "Dashboard Unavailable / Edit Connection" panel, which is enough to verify structure.
- Scripted version: `twb_smoketest_customsql.ps1 -Path <twb> -Answer Yes` (this folder). It answers the prompt via UIAutomation, dismisses sign-in/connect-failure dialogs, PASSes when the sheet-tab text renders, and captures the window via `twb_window_capture.ps1`.

## Layer 3 (when the change is visual or numeric): screenshot + extract reconciliation

```powershell
# Launch and KEEP open (saved Tableau Cloud credentials auto-connect, data renders in ~60-100s),
# then capture the window even if it landed on another virtual desktop:
powershell -File C:\Users\esmith\.claude\skills\twb-selftest\twb_window_capture.ps1 -ProcId <pid>
# -> %TEMP%\rsl_window_capture.png ; crop/upscale regions with PIL, Read the PNGs, then taskkill /T /F.
```

- PrintWindow with PW_RENDERFULLCONTENT captures cross-virtual-desktop with zero user disruption; a full-desktop Screenshot tool misses windows on the inactive desktop (and shows the user's personal screen).
- A fixed-size dashboard taller than the window only shows the top fold; verify below-the-fold sheets numerically instead of scrolling.
- **Numeric reconciliation:** published datasources are often WINDOWED extracts (v.HfdV3 = rolling 3-year contract window). KPI verification numbers computed on the full warehouse will NOT match the workbook; query the extract itself via the Tableau MCP `query-datasource` tool (it accepts custom calculations INCLUDING `{FIXED ...}` LODs - but it has no context-filter semantics, so within-filter LOD numbers cannot be reproduced there; use warehouse SQL with the extract's date floor for those). Find the window by querying MIN/MAX and a by-month profile of the date field.

## Calibrating lint rules (when Desktop teaches you something new)

- A rule may be an ERROR only if backed by an observed Desktop rejection (quote the error code and message in a comment next to the rule).
- Everything else is a WARNING. Desktop-saved workbooks legally interleave deps columns/instances, reuse zone ids inside `<devicelayouts>`, put worksheet windows after dashboard windows, and interleave `filter` with `*-sort` elements in `<view>`.
- **Negative control:** after adding any rule, run the lint on a known-good Desktop-saved workbook (e.g. `TableauExamples\bing_bong_extracted\Bing Bong 2026 is Here!.twb`). If it fails, the rule is a convention, not schema. A linter that fails working files gets ignored, then the real bugs ship.
- Regression fixtures live in `C:\Users\esmith\temp\twb_selftest_fixtures\` (`broken_single_value_sort.twb` must always FAIL both layers). Add a fixture for every new Desktop rejection you encounter.

## Quick reference

| Situation | Action |
|---|---|
| Built/modified a TWB, about to deliver | Lint, then smoke test with `-ExpectText`, then deliver |
| Lint passes, smoke test fails | Real bug. Read the captured dialog, fix, add a lint rule + fixture |
| Smoke test inconclusive (exit 2) | Check `%TEMP%\twb_smoketest_last.txt`; close stray Tableau instances; retry |
| New Desktop error code seen | Fix file, save broken copy as fixture, encode rule as ERROR with the message quoted |
| Lint fails a Desktop-saved file | Your rule is wrong, demote to warning |

## Rationalizations

| Excuse | Reality |
|---|---|
| "Static validation passed, it's fine" | That exact reasoning shipped a broken file. Twice in one day. |
| "The smoke test takes a minute" | The user round-trip on a broken delivery takes an hour and your credibility. |
| "I only changed one attribute" | 2805CF18 is a semantic error; one missing declaration triggers it. |
| "Desktop isn't on this machine" | Then say so in the delivery: the file is UNVERIFIED. Do not imply it was tested. |
| "It opened fine last build" | Every rebuild is a new file. Re-run the gate. |

## Red flags - STOP and run the gate

- About to SendUserFile / publish / attach a .twb you have not smoke-tested in its current byte-for-byte form
- Adding "verified" or "validated" to a delivery message with only static checks done
- Tempted to skip `-ExpectText` because the plain PASS came back quicker
