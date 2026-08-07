#!/usr/bin/env python3
"""Write one timestamped branch-memory note and update the manifest."""

from __future__ import annotations

import argparse
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from resolve_branch_memory_dir import resolve, slugify
from update_manifest import rebuild


VALID_STATUSES = {"active", "superseded", "final", "deferred", "promoted"}
VALID_CONFIDENCE = {"unknown", "provisional", "supported", "verified", "reversed"}


def yaml_scalar(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_list(name: str, values: list[str]) -> list[str]:
    if not values:
        return [f"{name}: []"]
    return [f"{name}:"] + [f"  - {yaml_scalar(value)}" for value in values]


def default_body(summary: str) -> str:
    return "\n".join(
        [
            "# Memory",
            "",
            "## Current Decision",
            "",
            summary,
            "",
            "## Why It Came Up",
            "",
            "## Evidence So Far",
            "",
            "## Source Trace",
            "",
            "## Reviewer Relevance",
            "",
        ]
    )


def write_memory(args: argparse.Namespace) -> Path:
    if args.status not in VALID_STATUSES:
        raise SystemExit(f"Invalid status: {args.status}")
    if args.confidence not in VALID_CONFIDENCE:
        raise SystemExit(f"Invalid confidence: {args.confidence}")

    resolved = resolve(args.repo, mkdir=True)
    memory_dir = Path(resolved["memory_dir"])
    body = Path(args.body_file).read_text() if args.body_file else args.body or default_body(args.summary)
    body = body.strip() + "\n"
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    filename_slug = slugify(args.summary, "memory")[:64]
    filename_slug = re.sub(r"__+", "__", filename_slug)
    path = memory_dir / "memories" / f"{stamp}-{slugify(args.kind)}-{filename_slug}.md"
    counter = 2
    while path.exists():
        path = memory_dir / "memories" / f"{stamp}-{slugify(args.kind)}-{filename_slug}-{counter}.md"
        counter += 1

    thread_id = (
        args.thread_id
        or os.environ.get("CODEX_THREAD_ID")
        or os.environ.get("CLAUDE_SESSION_ID")
        or "unknown"
    )  # pass --thread-id on harnesses that export neither var
    lines = [
        "---",
        "type: branch-memory",
        f"repo: {yaml_scalar(resolved['repo_key'])}",
        f"branch: {yaml_scalar(resolved['branch'])}",
        f"thread_id: {yaml_scalar(thread_id)}",
        f"created_at: {yaml_scalar(now)}",
        f"updated_at: {yaml_scalar(now)}",
        f"status: {yaml_scalar(args.status)}",
        f"memory_kind: {yaml_scalar(args.kind)}",
        f"confidence: {yaml_scalar(args.confidence)}",
        f"summary: {yaml_scalar(args.summary)}",
        *yaml_list("tags", args.tag),
        *yaml_list("related_files", args.related_file),
        *yaml_list("source_refs", args.source_ref),
        *yaml_list("supersedes", args.supersedes),
        "---",
        "",
        body,
    ]
    path.write_text("\n".join(lines))
    rebuild(args.repo)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repo path, defaults to cwd")
    parser.add_argument("--kind", required=True, help="Memory kind, e.g. architecture-decision")
    parser.add_argument("--summary", required=True, help="One-line summary")
    parser.add_argument("--status", default="active", help="active|superseded|final|deferred|promoted")
    parser.add_argument("--confidence", default="provisional", help="unknown|provisional|supported|verified|reversed")
    parser.add_argument("--tag", action="append", default=[], help="Tag, may be repeated")
    parser.add_argument("--related-file", action="append", default=[], help="Related repo file, may be repeated")
    parser.add_argument("--source-ref", action="append", default=[], help="Decision source reference, may be repeated")
    parser.add_argument("--supersedes", action="append", default=[], help="Memory path/id this supersedes, may be repeated")
    parser.add_argument("--thread-id", default="", help="Thread/session id if known")
    parser.add_argument("--body", default="", help="Memory markdown body")
    parser.add_argument("--body-file", default="", help="Path to memory markdown body")
    args = parser.parse_args()
    path = write_memory(args)
    print(path)


if __name__ == "__main__":
    main()
