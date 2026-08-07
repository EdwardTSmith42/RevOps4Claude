#!/usr/bin/env python3
"""Resolve the branch-scoped memory directory for the current repo."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def run_git(repo: Path, args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return None
    value = result.stdout.strip()
    return value or None


def slugify(value: str, fallback: str = "unknown") -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._/-]+", "-", value)
    value = value.replace("/", "__")
    value = re.sub(r"-{2,}", "-", value).strip("-._")
    return value or fallback


def repo_key_from_remote(remote: str | None, repo_root: Path) -> str:
    if not remote:
        return slugify(repo_root.name, "repo")
    cleaned = remote
    cleaned = cleaned.removesuffix(".git")
    cleaned = cleaned.replace("git@github.com:", "github.com/")
    cleaned = cleaned.replace("https://", "")
    cleaned = cleaned.replace("http://", "")
    cleaned = cleaned.replace("ssh://", "")
    return slugify(cleaned, "repo")


def resolve(repo: str | Path, mkdir: bool = False) -> dict[str, str]:
    start = Path(repo).expanduser().resolve()
    git_root = run_git(start, ["rev-parse", "--show-toplevel"])
    repo_root = Path(git_root).resolve() if git_root else start
    remote = run_git(repo_root, ["remote", "get-url", "origin"])
    branch = run_git(repo_root, ["branch", "--show-current"])
    if not branch:
        branch = run_git(repo_root, ["rev-parse", "--short", "HEAD"]) or "unknown"

    repo_key = repo_key_from_remote(remote, repo_root)
    branch_slug = slugify(branch, "unknown-branch")
    memory_home = os.environ.get("BRANCH_MEMORY_HOME")
    root = Path(memory_home).expanduser().resolve() if memory_home else repo_root / ".local" / "branch-memory"
    memory_dir = root / repo_key / branch_slug

    data = {
        "schema_version": "1",
        "repo_root": str(repo_root),
        "repo_key": repo_key,
        "remote": remote or "",
        "branch": branch,
        "branch_slug": branch_slug,
        "memory_root": str(root),
        "memory_dir": str(memory_dir),
    }

    if mkdir:
        (memory_dir / "memories").mkdir(parents=True, exist_ok=True)
        (memory_dir / "dream").mkdir(parents=True, exist_ok=True)
        branch_md = memory_dir / "branch.md"
        if not branch_md.exists():
            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            branch_md.write_text(
                "\n".join(
                    [
                        f"# Branch Memory: {branch}",
                        "",
                        "## Purpose",
                        "",
                        "_Capture branch-scoped decision context that is not obvious from the diff._",
                        "",
                        "## Current State",
                        "",
                        f"- Created: {now}",
                        f"- Repo: {repo_key}",
                        f"- Branch: {branch}",
                        "",
                        "## Important Memories",
                        "",
                        "## Dream Outputs",
                        "",
                        "## Open Questions",
                        "",
                    ]
                )
            )

    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repo path, defaults to cwd")
    parser.add_argument("--mkdir", action="store_true", help="Create the branch memory directories")
    args = parser.parse_args()
    print(json.dumps(resolve(args.repo, mkdir=args.mkdir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
