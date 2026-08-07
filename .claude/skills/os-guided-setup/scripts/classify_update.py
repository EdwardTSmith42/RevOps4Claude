#!/usr/bin/env python3
"""Classify a Personal OS update: what's safe, what's the user's, what needs a decision.

The three-way comparison behind `os-guided-setup` update mode. For every
system-owned file it compares three fingerprints — what originally shipped
(the workspace's `.os-manifest.json` baseline), what's on disk now, and what
the new release carries — and sorts each file into exactly one bucket.

This script decides nothing and writes nothing. It reports. Applying the safe
buckets and holding the conflict conversation stay with the agent, which is
the split that matters: hashing is deterministic work a script does reliably,
and judging what two competing edits *mean* is not.

Usage:
    python3 <skill-dir>/scripts/classify_update.py \
        --workspace <the existing install> \
        --release <the unzipped new release — never the install itself>

    --format json   (default) machine-readable report
    --format text   short human-readable summary

Exit codes:
    0  classified — report on stdout
    1  hard error (bad paths, unreadable manifest) — message on stderr
    2  no baseline in the workspace; classification is impossible.
       Route to the skill's "When there's no baseline" section.
    3  already up to date — nothing to do
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

# Windows consoles default to cp1252, which can't encode the arrows this
# report prints; force UTF-8 where the runtime allows it. Without this the
# classification succeeds but the print crashes, and the exit code sends the
# user to the wrong diagnosis.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

BASELINE_NAME = ".os-manifest.json"
RELEASE_NAME = "os-manifest.json"

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_NO_BASELINE = 2
EXIT_UP_TO_DATE = 3


def die(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(EXIT_ERROR)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        die(f"{label} not found at {path}")
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        die(f"{label} at {path} is not valid JSON ({exc})")
    if not isinstance(data.get("files"), dict):
        die(f"{label} at {path} has no 'files' map — it may be truncated or hand-edited")
    return data


def user_owned_prefixes(manifest: dict[str, Any]) -> list[str]:
    """Paths the update must never read, write, or reason about."""
    ownership = manifest.get("ownership", {})
    return [p.rstrip("/") for p in ownership.get("user_owned_never_touch", [])]


def is_user_owned(rel_path: str, prefixes: list[str]) -> bool:
    return any(rel_path == p or rel_path.startswith(p + "/") for p in prefixes)


def resolve_release_root(release: Path) -> Path:
    """Accept the directory a release was unzipped into, not only the release root.

    The pack unpacks into a single top-level folder, so pointing at the extraction
    directory is the natural mistake and a pure nuisance to hit. Descend only when
    exactly one immediate subdirectory carries a manifest — two candidates is real
    ambiguity about which release is meant, and guessing there could update someone
    to the wrong version.
    """
    if (release / RELEASE_NAME).is_file():
        return release
    try:
        candidates = [
            d for d in sorted(release.iterdir())
            if d.is_dir() and (d / RELEASE_NAME).is_file()
        ]
    except OSError as exc:
        die(f"cannot read {release} ({exc})")
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        listed = "\n".join(f"  {d.name}" for d in candidates)
        die(
            f"{release} holds more than one release; point at the one you mean:\n{listed}"
        )
    return release  # nothing found — let the manifest error name the exact path


def classify(workspace: Path, release: Path) -> dict[str, Any]:
    baseline_path = workspace / BASELINE_NAME
    if not baseline_path.is_file():
        print(
            f"error: no baseline at {baseline_path} — this install predates the "
            "manifest, so whether a file was customized cannot be determined. "
            "Do not bulk-overwrite; see the skill's 'When there's no baseline' section.",
            file=sys.stderr,
        )
        sys.exit(EXIT_NO_BASELINE)

    baseline = load_manifest(baseline_path, "workspace baseline")
    incoming = load_manifest(release / RELEASE_NAME, "release manifest")

    from_version = baseline.get("pack_version", "unknown")
    to_version = incoming.get("pack_version", "unknown")
    if from_version == to_version:
        print(
            f"Already running {to_version} — nothing to update.",
            file=sys.stderr,
        )
        sys.exit(EXIT_UP_TO_DATE)

    # Ownership is the first gate, before any comparison. Union both manifests'
    # user-owned zones so a release that adds a protected area protects it
    # immediately, and one that drops an area still shields the existing data.
    protected = sorted(set(user_owned_prefixes(baseline)) | set(user_owned_prefixes(incoming)))

    ownership = incoming.get("ownership", {})
    hybrid = set(ownership.get("hybrid_review_required", []))
    install_once = ownership.get("install_once_if_absent", [])

    baseline_files: dict[str, str] = baseline["files"]
    release_files: dict[str, str] = incoming["files"]

    buckets: dict[str, list[dict[str, Any]]] = {
        "safe_update": [],       # untouched + release changed it → apply silently
        "keep_theirs": [],       # user modified + release didn't → say nothing
        "conflict": [],          # user modified + release changed it → ask
        "already_applied": [],   # disk already matches the new release → nothing to do
        "new": [],               # new in this release → add
        "removed_upstream": [],  # baseline had it, release dropped it → ask
        "missing_locally": [],   # baseline had it, not on disk → ask, don't resurrect
        "unchanged": [],         # nothing to do
        "install_once": [],      # starter file absent → copy
        "release_incomplete": [], # listed in the release manifest but not in the folder
        "skipped_user_owned": [], # defense in depth; should always be empty
    }

    install_once_set = set(install_once)

    for rel_path in sorted(set(baseline_files) | set(release_files)):
        if is_user_owned(rel_path, protected):
            buckets["skipped_user_owned"].append({"path": rel_path})
            continue
        # Starter files are never classified, even if a manifest lists them among
        # the hashed files. Comparison implies a file the system may rewrite, and
        # once one of these exists it belongs to the user. Handled below instead.
        if rel_path in install_once_set:
            continue

        base_hash = baseline_files.get(rel_path)
        new_hash = release_files.get(rel_path)
        local = workspace / rel_path
        disk_hash = sha256(local) if local.is_file() else None

        entry: dict[str, Any] = {"path": rel_path}
        if rel_path in hybrid:
            # Shipped and expected to be customized. Flagged so the agent frames
            # the conversation as routine rather than surprising.
            entry["hybrid"] = True

        # A file the release claims to carry but didn't deliver intact means a
        # partial or corrupted unzip — catch it before anything is applied,
        # because every bucket below is only as trustworthy as the source.
        if new_hash is not None:
            source = release / rel_path
            if not source.is_file():
                buckets["release_incomplete"].append({**entry, "reason": "missing from release folder"})
                continue
            if sha256(source) != new_hash:
                buckets["release_incomplete"].append({**entry, "reason": "does not match the release manifest"})
                continue

        if base_hash is None:
            buckets["new"].append(entry)
        elif new_hash is None:
            # The release retired this file. Whether that's a question depends
            # entirely on whether the user had made it theirs.
            if disk_hash is None:
                buckets["unchanged"].append(entry)  # already gone; nothing to do
            else:
                entry["customized"] = disk_hash != base_hash
                buckets["removed_upstream"].append(entry)
        elif disk_hash is None:
            buckets["missing_locally"].append(entry)
        elif disk_hash == base_hash:
            buckets["safe_update" if new_hash != base_hash else "unchanged"].append(entry)
        elif disk_hash == new_hash:
            # On disk it already matches the new release, but not the baseline.
            # A user cannot plausibly hand-edit a file into byte-identical
            # future-release content, so this is the release arriving by some
            # route other than this update — most often the new zip unpacked
            # over the install, sometimes an earlier update that didn't finish.
            # Calling it a conflict would manufacture a decision that doesn't
            # exist and bury the real ones.
            buckets["already_applied"].append(entry)
        else:
            buckets["conflict" if new_hash != base_hash else "keep_theirs"].append(entry)

    # Starter files: copied only if absent. Once the workspace has one it's the
    # user's forever, so a present file is never compared, never flagged, never
    # touched — which is why this runs outside the classification loop above.
    for rel_path in install_once:
        if not (workspace / rel_path).is_file() and (release / rel_path).is_file():
            buckets["install_once"].append({"path": rel_path})

    # When most of what the release changed is already sitting on disk, the
    # release reached this workspace some other way. Worth saying out loud:
    # if it arrived by unpacking over the install, any customization in those
    # files is already gone, and no amount of careful classification here can
    # bring it back. Better to name that than to report a tidy success.
    release_changed = (
        len(buckets["safe_update"]) + len(buckets["conflict"]) + len(buckets["already_applied"])
    )
    already = len(buckets["already_applied"])
    likely_already_applied = bool(already) and already * 2 >= release_changed

    whats_new = release / "WHATS-NEW.md"
    return {
        "status": "classified",
        "likely_already_applied": likely_already_applied,
        "from_version": from_version,
        "to_version": to_version,
        "workspace": str(workspace),
        "release": str(release),
        # Absent on older releases. Say so rather than inventing a summary.
        "whats_new": str(whats_new) if whats_new.is_file() else None,
        "needs_user_decision": bool(
            buckets["conflict"]
            or buckets["removed_upstream"]
            or buckets["missing_locally"]
            or buckets["release_incomplete"]
        ),
        "counts": {name: len(items) for name, items in buckets.items()},
        "buckets": buckets,
    }


def render_text(report: dict[str, Any]) -> str:
    c = report["counts"]
    lines = [
        f"Personal OS {report['from_version']} → {report['to_version']}",
        "",
        f"  {c['safe_update']} files update safely",
        f"  {c['new']} new in this release",
        f"  {c['keep_theirs']} of your customizations kept as-is",
        f"  {c['unchanged']} unchanged",
    ]
    if c["install_once"]:
        lines.append(f"  {c['install_once']} starter files to add")
    if c["already_applied"]:
        lines.append(f"  {c['already_applied']} already match this release")

    if report["likely_already_applied"]:
        lines.append("")
        lines.append(
            "Most of what this release changes is already on disk. The new version "
            "most likely got unpacked over the install (or an earlier update stopped "
            "partway). Nothing here needs deciding — but if it was unpacked over the "
            "top, any customizations in those files are already gone, and a snapshot "
            "is the only way back."
        )

    attention = [
        ("conflict", "need a decision (you changed it, so did the release)"),
        ("removed_upstream", "retired in this release"),
        ("missing_locally", "in the baseline but not on disk"),
        ("release_incomplete", "listed in the release but missing from the folder"),
    ]
    flagged = [(name, label) for name, label in attention if c[name]]
    if flagged:
        lines.append("")
        lines.append("Needs attention:")
        for name, label in flagged:
            lines.append(f"  {c[name]} {label}")
            for entry in report["buckets"][name]:
                if entry.get("hybrid"):
                    mark = " (expected to be customized)"
                elif entry.get("customized"):
                    mark = " (you customized this one)"
                elif entry.get("customized") is False:
                    mark = " (untouched — safe to remove)"
                else:
                    mark = ""
                lines.append(f"      {entry['path']}{mark}")

    if c["skipped_user_owned"]:
        lines.append("")
        lines.append(
            f"  note: {c['skipped_user_owned']} manifest entries fell inside user-owned "
            "territory and were skipped. This should be empty — worth reporting."
        )
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Classify a Personal OS update against the install-time baseline."
    )
    ap.add_argument(
        "--workspace",
        default=".",
        help=f"existing install root (must contain {BASELINE_NAME}); defaults to cwd",
    )
    ap.add_argument(
        "--release",
        required=True,
        help=f"unzipped new release root (must contain {RELEASE_NAME}); never the workspace itself",
    )
    ap.add_argument("--format", choices=["json", "text"], default="json")
    args = ap.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    release = Path(args.release).expanduser().resolve()

    if not workspace.is_dir():
        die(f"workspace {workspace} is not a directory")
    if not release.is_dir():
        die(
            f"release {release} is not a directory — if the download is still a .zip, "
            "unzip it somewhere separate first (never over the workspace)"
        )
    if workspace == release:
        die(
            "workspace and release are the same directory. The new release was "
            "unzipped over the install, which destroys the baseline needed to tell "
            "your changes from the release's. Restore from a snapshot, or treat this "
            "as an install with no baseline."
        )

    report = classify(workspace, resolve_release_root(release))
    print(render_text(report) if args.format == "text" else json.dumps(report, indent=2))
    sys.exit(EXIT_OK)


if __name__ == "__main__":
    main()
