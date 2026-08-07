#!/usr/bin/env python3
"""Append one line per skill invocation. Meant to be run by the harness, not by you.

Optional. Personal OS works without it — `reflect` reads the memories under
`os-memory/`, which carry the stronger signal anyway. What this adds is
frequency: which skills you lean on, which ones you never reach for, which
modes never fire. That turns "you keep asking for this" into "you keep asking
for this and the skill you already have keeps needing the same correction."

The reason it's a harness hook rather than something the AI writes: asking an
agent to log its own work at the end of every turn was the original design,
and it produced zero entries in three months. A hook can't forget.

Wiring (Claude Code) — a `PostToolUse` hook matching the Skill tool:

    {"hooks": {"PostToolUse": [{"matcher": "Skill", "hooks": [
      {"type": "command",
       "command": "python3 <skills-dir>/os-tune/scripts/log_skill_usage.py",
       "timeout": 10}]}]}}

Other harnesses: any post-tool event that can run a command and pass the tool
payload on stdin works the same way. See `references/usage-logging-setup.md`.

Log path defaults to `~/.claude/skill-usage.jsonl`; override with
`OS_SKILL_USAGE_LOG`. Deliberately outside the workspace so it captures skill
use across every project rather than only the one you happen to be in.

**This never fails loudly.** Any error exits 0 with nothing written. A logging
side-effect must never break the user's turn — that trade is not close.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ARGS_PREVIEW_CHARS = 200


def log_path() -> Path:
    return Path(os.environ.get("OS_SKILL_USAGE_LOG", Path.home() / ".claude" / "skill-usage.jsonl")).expanduser()


def first_str(source: dict, *keys: str) -> str:
    """First key present with a usable scalar value."""
    for key in keys:
        value = source.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, (int, float)):
            return str(value)
    return ""


def build_entry(payload: dict) -> dict | None:
    tool_input = payload.get("tool_input") or payload.get("toolInput") or {}
    if not isinstance(tool_input, dict):
        return None

    skill = first_str(tool_input, "skill", "skill_name", "name")
    if not skill:
        # No identifiable skill means the payload shape changed upstream.
        # Writing an empty row would quietly poison the frequency counts, so
        # write nothing and let the log's staleness be the signal instead.
        return None

    args = first_str(tool_input, "args", "arguments", "input")
    return {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "skill": skill,
        # Truncated on purpose: the opening words carry the request; the rest is
        # detail the transcript still holds. Keeps lines scannable by eye.
        "args_preview": args[:ARGS_PREVIEW_CHARS],
        "cwd": str(Path.cwd()),
        "tool_use_id": first_str(payload, "tool_use_id", "toolUseId"),
    }


def main() -> None:
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return
        entry = build_entry(json.loads(raw))
        if entry is None:
            return
        path = log_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        # Single append of a single line: concurrent sessions interleave rows
        # rather than corrupting each other.
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


if __name__ == "__main__":
    main()
    sys.exit(0)
