#!/usr/bin/env python3
"""Find and extract the user's own words from archived agent threads.

The input side of `os-tune/distill`. Harnesses record full session transcripts
but usually delete them on a rolling window, so the signal in them is
perishable — this pulls out the durable part before it expires, and the agent
turns that into memories under `os-memory/`.

What it extracts is deliberately narrow: **the user's turns only.** Not the
assistant's replies, not tool results. What someone asked for, in their own
words, repeated across weeks, is the thing that reveals a missing skill. Two
filters matter more than they look:

- Subagent transcripts are excluded. Their "user" turns are prompts the
  assistant wrote to itself, and on a real machine they outnumber genuine
  human turns — clustering them surfaces the assistant's habits as if they
  were the user's.
- System-injected blocks (reminders, command wrappers, tool results) are
  excluded for the same reason: nobody typed them.

State lives beside the memories so a run never reprocesses a thread. That is
what keeps this cheap enough to run weekly.

Usage:
    python3 <skill-dir>/scripts/distill_threads.py scan   [--days 60] [--json]
    python3 <skill-dir>/scripts/distill_threads.py extract [--limit 5] [--max-turns 80]
    python3 <skill-dir>/scripts/distill_threads.py mark --thread <id> [--memories 2]
    python3 <skill-dir>/scripts/distill_threads.py exclude --project <name>

Exit codes: 0 ok · 1 error · 3 nothing pending
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator

DEFAULT_TRANSCRIPTS = [
    Path.home() / ".claude" / "projects",   # Claude Code
    Path.home() / ".codex" / "sessions",    # Codex, when present
]
def _default_state() -> Path:
    return find_workspace_root() / "os-memory" / "_distill-state.json"


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

EXIT_OK, EXIT_ERROR, EXIT_NOTHING = 0, 1, 3

# Text that arrives in the user role but nobody typed: harness reminders,
# slash-command plumbing, skill bodies, resume boilerplate, and interrupt
# markers. Derived by frequency-counting real transcripts rather than guessed —
# every entry here was observed leaking into extraction. Prefix-matched.
#
# Deliberately NOT filtered: short turns. "commit push" looks like noise and is
# actually one of the strongest signals there is — a two-word request repeated
# many times is exactly the shape that deserves a skill.
INJECTED_PREFIXES = (
    "<system-reminder",
    "<command-",
    "<local-command",
    "<user-prompt",
    "<task-notification",
    "Base directory for this skill:",
    "This session is being continued from a previous conversation",
    "[Request interrupted by user]",
    "Continue from where you left off.",
)


def die(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(EXIT_ERROR)


def load_state(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"processed": {}, "excluded_projects": [], "last_run": None}
    try:
        state = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        die(f"state file {path} is not valid JSON ({exc})")
    state.setdefault("processed", {})
    state.setdefault("excluded_projects", [])
    state.setdefault("last_run", None)
    return state


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True))


def is_user_text(entry: dict) -> str | None:
    """The text of a genuine human turn, or None for anything else."""
    if entry.get("type") != "user":
        return None
    message = entry.get("message") or {}
    content = message.get("content")
    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        # A tool result is delivered in the user role but nobody typed it.
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
            return None
        text = " ".join(b.get("text", "") for b in content if isinstance(b, dict))
    else:
        return None
    text = text.strip()
    if not text or text.startswith(INJECTED_PREFIXES):
        return None
    return text


def thread_files(root: Path) -> Iterator[Path]:
    for path in sorted(root.rglob("*.jsonl")):
        # Subagent transcripts hold assistant-authored prompts, not user speech.
        if "subagents" in path.parts:
            continue
        yield path


def read_thread(path: Path, max_turns: int | None = None) -> dict[str, Any]:
    turns: list[dict[str, str]] = []
    stamps: list[str] = []
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = entry.get("timestamp") or entry.get("ts")
        if ts:
            stamps.append(ts)
        text = is_user_text(entry)
        if text:
            turns.append({"ts": ts or "", "text": text})
    if max_turns is not None and len(turns) > max_turns:
        # Keep both ends: the opening states intent, the close carries decisions.
        head, tail = max_turns * 2 // 3, max_turns - (max_turns * 2 // 3)
        turns = turns[:head] + turns[-tail:] if tail else turns[:head]
    return {
        "thread_id": path.stem,
        "path": str(path),
        "first_ts": min(stamps) if stamps else None,
        "last_ts": max(stamps) if stamps else None,
        "turn_count": len(turns),
        "turns": turns,
    }


def project_of(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    return rel.parts[0] if len(rel.parts) > 1 else "(root)"


def normalize_project(name: str) -> str:
    """Compare project names ignoring leading dashes.

    Claude Code encodes a project's path into its directory name, which leaves
    a leading `-` (`-Users-work-myrepo`). Passed as `--project -Users-...` that
    reads as a flag and the command dies. Normalizing both sides lets the user
    write the name with or without the dashes and have it work either way.
    """
    return name.lstrip("-").lower()


def is_excluded(project: str, excluded: list[str]) -> bool:
    return normalize_project(project) in {normalize_project(e) for e in excluded}


def pending(root: Path, state: dict, days: int) -> list[dict[str, Any]]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    out = []
    for path in thread_files(root):
        project = project_of(path, root)
        if is_excluded(project, state["excluded_projects"]):
            continue
        if path.stem in state["processed"]:
            continue
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        except OSError:
            continue
        if mtime < cutoff:
            continue
        out.append({
            "thread_id": path.stem,
            "project": project,
            "path": str(path),
            "modified": mtime.isoformat(),
            "size_kb": round(path.stat().st_size / 1024, 1),
        })
    out.sort(key=lambda t: t["modified"])   # oldest first — closest to expiry
    return out


def resolve_root(arg: str | None) -> Path:
    if arg:
        root = Path(arg).expanduser()
        if not root.is_dir():
            die(f"transcripts directory {root} not found")
        return root
    for candidate in DEFAULT_TRANSCRIPTS:
        if candidate.is_dir():
            return candidate
    die(
        "no transcript directory found. Looked for "
        f"{', '.join(str(p) for p in DEFAULT_TRANSCRIPTS)}. "
        "If your harness stores sessions elsewhere, pass --transcripts-dir."
    )
    raise AssertionError  # unreachable; die() exits


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract the user's own turns from archived threads.")
    ap.add_argument("command", choices=["scan", "extract", "mark", "exclude"])
    ap.add_argument("--transcripts-dir")
    ap.add_argument("--state", default=str(_default_state()))
    ap.add_argument("--days", type=int, default=60, help="only consider threads touched in this window")
    ap.add_argument("--limit", type=int, default=5, help="extract: threads per run")
    ap.add_argument("--max-turns", type=int, default=80, help="extract: cap turns per thread")
    ap.add_argument("--thread", help="mark: thread id")
    ap.add_argument("--memories", type=int, default=0, help="mark: how many memories it produced")
    ap.add_argument("--project", help="exclude: project directory name")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    state_path = Path(args.state).expanduser()
    state = load_state(state_path)

    if args.command == "exclude":
        if not args.project:
            die("--project required")
        if not is_excluded(args.project, state["excluded_projects"]):
            state["excluded_projects"].append(args.project)
            state["excluded_projects"].sort()
            save_state(state_path, state)
        print(f"excluded: {', '.join(state['excluded_projects'])}")
        return

    if args.command == "mark":
        if not args.thread:
            die("--thread required")
        state["processed"][args.thread] = {
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "memories": args.memories,
        }
        state["last_run"] = state["processed"][args.thread]["at"]
        save_state(state_path, state)
        print(f"marked {args.thread} ({args.memories} memories)")
        return

    root = resolve_root(args.transcripts_dir)
    todo = pending(root, state, args.days)

    if args.command == "scan":
        report = {
            "transcripts_dir": str(root),
            "window_days": args.days,
            "pending": len(todo),
            "processed": len(state["processed"]),
            "excluded_projects": state["excluded_projects"],
            "last_run": state["last_run"],
            "oldest_pending": todo[0] if todo else None,
            "threads": todo,
        }
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"{len(todo)} threads pending in {root} (last {args.days}d)")
            print(f"  already distilled: {len(state['processed'])}")
            if state["excluded_projects"]:
                print(f"  excluded projects: {', '.join(state['excluded_projects'])}")
            if todo:
                print(f"  oldest pending:    {todo[0]['modified'][:10]}  {todo[0]['project']}")
        sys.exit(EXIT_OK if todo else EXIT_NOTHING)

    # extract
    if not todo:
        print("nothing pending", file=sys.stderr)
        sys.exit(EXIT_NOTHING)
    batch = [read_thread(Path(t["path"]), args.max_turns) for t in todo[: args.limit]]
    for thread, meta in zip(batch, todo):
        thread["project"] = meta["project"]
    print(json.dumps({
        "transcripts_dir": str(root),
        "extracted": len(batch),
        "remaining": max(0, len(todo) - len(batch)),
        "threads": batch,
    }, indent=2))


if __name__ == "__main__":
    main()
