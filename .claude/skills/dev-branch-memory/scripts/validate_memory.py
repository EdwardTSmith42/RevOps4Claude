#!/usr/bin/env python3
"""Validate branch-memory markdown frontmatter."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "type",
    "repo",
    "branch",
    "thread_id",
    "created_at",
    "updated_at",
    "status",
    "memory_kind",
    "confidence",
    "summary",
    "tags",
    "related_files",
    "source_refs",
    "supersedes",
}
VALID_STATUSES = {"active", "superseded", "final", "deferred", "promoted"}
VALID_CONFIDENCE = {"unknown", "provisional", "supported", "verified", "reversed"}
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(errors="replace")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter")
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise ValueError("PyYAML is required for validation") from exc
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return data


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        fm = parse_frontmatter(path)
    except ValueError as exc:
        return [f"{path}: {exc}"]

    missing = sorted(REQUIRED_FIELDS - set(fm))
    if missing:
        errors.append(f"{path}: missing required fields: {', '.join(missing)}")
    if fm.get("type") != "branch-memory":
        errors.append(f"{path}: type must be branch-memory")
    if fm.get("status") not in VALID_STATUSES:
        errors.append(f"{path}: invalid status {fm.get('status')!r}")
    if fm.get("confidence") not in VALID_CONFIDENCE:
        errors.append(f"{path}: invalid confidence {fm.get('confidence')!r}")
    for key in ("tags", "related_files", "source_refs", "supersedes"):
        if key in fm and not isinstance(fm[key], list):
            errors.append(f"{path}: {key} must be a list")
    if not str(fm.get("summary", "")).strip():
        errors.append(f"{path}: summary must be non-empty")
    return errors


def candidate_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if (path / "memories").exists():
        return sorted((path / "memories").glob("*.md"))
    return sorted(path.glob("*.md"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Memory file or branch-memory directory")
    args = parser.parse_args()
    files = candidate_files(Path(args.path).expanduser().resolve())
    if not files:
        print("No memory files found")
        return
    errors: list[str] = []
    for file_path in files:
        errors.extend(validate_file(file_path))
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print(f"Validated {len(files)} branch memory file(s)")


if __name__ == "__main__":
    main()
