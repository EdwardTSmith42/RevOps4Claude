#!/usr/bin/env python3
"""Rebuild manifest.json for a branch-memory directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from resolve_branch_memory_dir import resolve


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(errors="replace")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(match.group(1))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def file_record(path: Path, base: Path) -> dict[str, Any]:
    fm = parse_frontmatter(path)
    stat = path.stat()
    record = {
        "path": str(path.relative_to(base)),
        "sha256": sha256_file(path),
        "bytes": stat.st_size,
        "mtime": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(timespec="seconds"),
    }
    for key in ("summary", "status", "memory_kind", "confidence", "created_at", "updated_at", "tags", "source_refs"):
        if key in fm:
            record[key] = fm[key]
    return record


def rebuild(repo: str | Path) -> dict[str, Any]:
    resolved = resolve(repo, mkdir=True)
    memory_dir = Path(resolved["memory_dir"])
    manifest_path = memory_dir / "manifest.json"
    existing: dict[str, Any] = {}
    if manifest_path.exists():
        try:
            existing = json.loads(manifest_path.read_text())
        except json.JSONDecodeError:
            existing = {}

    memories = sorted((memory_dir / "memories").glob("*.md"))
    dream_outputs = sorted((memory_dir / "dream").glob("*.md"))
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    manifest = {
        "schema_version": 1,
        "created_at": existing.get("created_at", now),
        "updated_at": now,
        "repo_root": resolved["repo_root"],
        "repo_key": resolved["repo_key"],
        "remote": resolved["remote"],
        "branch": resolved["branch"],
        "branch_slug": resolved["branch_slug"],
        "memory_dir": resolved["memory_dir"],
        "memories": [file_record(path, memory_dir) for path in memories],
        "dream_outputs": [file_record(path, memory_dir) for path in dream_outputs],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repo path, defaults to cwd")
    args = parser.parse_args()
    manifest = rebuild(args.repo)
    print(json.dumps({"manifest": manifest["memory_dir"] + "/manifest.json", "memories": len(manifest["memories"]), "dream_outputs": len(manifest["dream_outputs"])}, indent=2))


if __name__ == "__main__":
    main()
