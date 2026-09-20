"""Concatenate every inline <script> block that is NOT type="application/json"
and hand it to node --check. Catches a syntax error in the page before it ships."""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
h = open(os.path.join(HERE, "dashboard_built.html"), encoding="utf-8").read()
blocks = []
for m in re.finditer(r"<script([^>]*)>(.*?)</script>", h, re.S | re.I):
    if "application/json" in (m.group(1) or "").lower():
        continue
    if re.search(r"\bsrc\s*=", m.group(1) or "", re.I):
        continue
    blocks.append(m.group(2))
js = "\n;\n".join(blocks)
out = os.path.join(HERE, "_jscheck.js")
open(out, "w", encoding="utf-8").write(js)
r = subprocess.run(["node", "--check", out], capture_output=True, text=True)
sys.stderr.write(r.stdout + r.stderr)
print("script blocks checked: %d | bytes %d | node --check %s"
      % (len(blocks), len(js), "PASS" if r.returncode == 0 else "FAIL"))
os.remove(out)
sys.exit(r.returncode)
