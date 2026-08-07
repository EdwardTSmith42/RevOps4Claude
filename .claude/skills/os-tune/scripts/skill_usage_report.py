#!/usr/bin/env python3
"""Report skill-usage patterns from the harness's invocation log.

Answers three questions for a checkpoint: what am I actually using, what's
sitting idle, and which declared modes never fire. The third is the one worth
having — a mode that never fires is usually a trigger-wording problem, not a
dead feature.

Mode resolution is the subtle part. The log records the skill name and the
free-form args the caller passed; it has no mode field, because the harness
doesn't have one to give. Modes are a Personal OS convention living inside
that prose. So mode is resolved here by matching each skill's *declared*
modes against its args — and a skill that declares no modes reports as
single-mode rather than as missing data. Guessing from the first word doesn't
work: real args start with prose ("Re-review the update path...").

Usage:
    python3 <skill-dir>/scripts/skill_usage_report.py [--days 30]
        [--log <path>] [--skills-dir <path>] [--format text|json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Ordered by trustworthiness: the hook-written log is mechanical and complete;
# the workspace log depends on an agent remembering to append to it.
def _default_logs() -> list[Path]:
    return [
        Path.home() / ".claude" / "skill-usage.jsonl",
        find_workspace_root() / "os-inputs" / "_os-skill-usage.log",
    ]
DEFAULT_SKILL_DIRS = [
    Path.home() / ".agents" / "skills",
    Path.home() / ".claude" / "skills",
]



def find_workspace_root(start: Path | None = None) -> Path:
    """Walk up for the workspace root so relative defaults don't depend on cwd.

    These scripts are run by an agent whose working directory is whatever the
    session happened to start in. A bare relative default silently resolves
    against the wrong place — the report reads a log that isn't there, and
    distill writes a fresh state file, losing the record of which threads were
    already processed along with the user's project exclusions.
    """
    here = (start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / "_os-map.md").is_file() or (candidate / "os-inputs").is_dir():
            return candidate
    return here

def pick_existing(candidates: list[Path]) -> Path | None:
    for path in candidates:
        if path.exists():
            return path
    return None


def declared_modes(skill_dir: Path) -> set[str]:
    """Modes a skill declares — from modes/*.md, falling back to frontmatter."""
    modes = {p.stem for p in (skill_dir / "modes").glob("*.md")}
    if modes:
        return modes
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return set()
    text = skill_md.read_text(errors="replace")
    front = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not front:
        return set()
    return set(re.findall(r"^\s*-\s+name:\s*([a-z0-9-]+)\s*$", front.group(1), re.MULTILINE))


def resolve_mode(args: str, modes: set[str], explicit: str | None = None) -> str | None:
    """Which mode did this invocation use? None if it names none.

    An explicit `mode` field wins outright. Logs differ: a harness hook records
    only the skill and the raw args, because harnesses have no concept of a
    mode; a workspace log written by an agent usually records mode directly.
    Inferring from args when the answer is already stated would throw away the
    better source and report live modes as never-fired.
    """
    if explicit and explicit.strip():
        return explicit.strip()
    if not modes or not args:
        return None
    lowered = args.lower()
    # Longest first so "multi-layer-extract" wins over a hypothetical "extract".
    for mode in sorted(modes, key=len, reverse=True):
        if re.search(rf"(?<![a-z0-9-]){re.escape(mode)}(?![a-z0-9-])", lowered):
            return mode
    return None


def load_entries(log: Path, since: datetime) -> list[dict]:
    entries = []
    for line in log.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = entry.get("ts")
        if not ts:
            continue
        try:
            when = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            continue
        if when.tzinfo is None:
            # Writers differ: the harness hook stamps UTC with a trailing Z,
            # while a workspace log written by an agent often omits the zone.
            # Treat a bare timestamp as UTC rather than crashing on the compare.
            when = when.replace(tzinfo=timezone.utc)
        if when >= since:
            entries.append(entry)
    return entries


def build_report(log: Path, skills_dir: Path, days: int) -> dict:
    since = datetime.now(timezone.utc) - timedelta(days=days)
    entries = load_entries(log, since)

    modes_by_skill = {
        d.name: declared_modes(d)
        for d in sorted(skills_dir.iterdir())
        if d.is_dir() and not d.name.startswith("_")
    }

    invocations = Counter()
    fired: dict[str, set[str]] = {}
    unresolved = Counter()
    for entry in entries:
        skill = entry.get("skill")
        if not skill:
            continue
        invocations[skill] += 1
        known = modes_by_skill.get(skill, set())
        mode = resolve_mode(
            entry.get("args_preview") or entry.get("args") or "", known, entry.get("mode")
        )
        if mode:
            fired.setdefault(skill, set()).add(mode)
        elif known:
            # Declares modes but this call named none — a real signal that the
            # skill is being invoked without routing, distinct from single-mode.
            unresolved[skill] += 1

    never_fired = sorted(
        f"{skill}:{mode}"
        for skill, known in modes_by_skill.items()
        for mode in known - fired.get(skill, set())
    )
    idle = sorted(s for s in modes_by_skill if s not in invocations)

    return {
        "log": str(log),
        "skills_dir": str(skills_dir),
        "window_days": days,
        "total_invocations": sum(invocations.values()),
        "top_skills": invocations.most_common(10),
        "modes_fired": {s: sorted(m) for s, m in sorted(fired.items())},
        "invoked_without_naming_a_mode": unresolved.most_common(10),
        "modes_never_fired": never_fired,
        "idle_skills": idle,
    }


def render(report: dict) -> str:
    out = [
        f"Skill usage — last {report['window_days']}d "
        f"({report['total_invocations']} invocations)",
        f"  log: {report['log']}",
        "",
        "## Most used",
    ]
    out += [f"  {n:4}  {s}" for s, n in report["top_skills"]] or ["  (none)"]

    out += ["", "## Modes that fired"]
    out += [f"  {s}: {', '.join(m)}" for s, m in report["modes_fired"].items()] or ["  (none)"]

    if report["invoked_without_naming_a_mode"]:
        out += ["", "## Invoked without naming a mode (routing may be implicit)"]
        out += [f"  {n:4}  {s}" for s, n in report["invoked_without_naming_a_mode"]]

    out += ["", "## Modes defined but never fired (trigger-gap candidates)"]
    out += [f"  {m}" for m in report["modes_never_fired"]] or ["  (none)"]

    out += ["", "## Skills idle in window"]
    out += [f"  {s}" for s in report["idle_skills"]] or ["  (none)"]
    out += ["", "Recently-added skills look identical to dead ones here — check dates before cutting."]
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description="Report skill-usage patterns for a checkpoint.")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--log", help="invocation log (JSONL); defaults to the harness hook log")
    ap.add_argument("--skills-dir", help="installed skills directory")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    log = Path(args.log).expanduser() if args.log else pick_existing(_default_logs())
    if not log or not log.is_file():
        sys.exit(
            "error: no skill-usage log found. Looked for "
            f"{', '.join(str(p) for p in _default_logs())}. "
            "If your harness logs invocations elsewhere, pass --log."
        )
    skills_dir = Path(args.skills_dir).expanduser() if args.skills_dir else pick_existing(DEFAULT_SKILL_DIRS)
    if not skills_dir or not skills_dir.is_dir():
        sys.exit(
            "error: no skills directory found. Looked for "
            f"{', '.join(str(p) for p in DEFAULT_SKILL_DIRS)}. Pass --skills-dir."
        )

    report = build_report(log, skills_dir, args.days)
    print(json.dumps(report, indent=2) if args.format == "json" else render(report))


if __name__ == "__main__":
    main()
