"""Tests for classify_update.py — the three-way comparison behind update mode.

The bar here is doctrinal, not just functional: the update must never overwrite
something the user changed, never touch user-owned territory, and never guess
when it can't know. Each of those is a test below, because a silent regression
in any of them is the trust-poisoning failure the mode exists to prevent.
"""

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "classify_update.py"

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_NO_BASELINE = 2
EXIT_UP_TO_DATE = 3


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


class ClassifyUpdateTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        root = Path(self.tempdir.name)
        self.workspace = root / "workspace"
        self.release = root / "release"
        self.workspace.mkdir()
        self.release.mkdir()

    def tearDown(self):
        self.tempdir.cleanup()

    # ---- fixture helpers -------------------------------------------------

    def ownership(self, **overrides):
        base = {
            "system_owned": ["skills", "AGENTS.md"],
            "user_owned_never_touch": ["os-tracker", "os-inputs/_os-inbox.md"],
            "install_once_if_absent": ["os-inputs/_os-session-log.md"],
            "hybrid_review_required": ["AGENTS.md"],
        }
        base.update(overrides)
        return base

    def write(self, root: Path, rel_path: str, content: str) -> None:
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def write_manifest(self, root: Path, name: str, version: str, files: dict, **kw):
        (root / name).write_text(json.dumps({
            "manifest_version": 1,
            "pack_version": version,
            "ownership": kw.get("ownership", self.ownership()),
            "files": {p: sha256(c) for p, c in files.items()},
        }))

    def setup_pair(self, baseline_files, release_files, disk_files=None, **kw):
        """Baseline = what shipped. Release = what's new. Disk = what's there now."""
        self.write_manifest(self.workspace, ".os-manifest.json", "0.1.0", baseline_files, **kw)
        self.write_manifest(self.release, "os-manifest.json", "0.2.0", release_files, **kw)
        for rel_path, content in release_files.items():
            self.write(self.release, rel_path, content)
        disk = baseline_files if disk_files is None else disk_files
        for rel_path, content in disk.items():
            self.write(self.workspace, rel_path, content)

    def run_classify(self, *args, expect=EXIT_OK):
        result = subprocess.run(
            ["python3", str(SCRIPT), "--workspace", str(self.workspace),
             "--release", str(self.release), *args],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, expect, result.stderr)
        return result

    def classify(self):
        return json.loads(self.run_classify().stdout)

    def paths_in(self, report, bucket):
        return [e["path"] for e in report["buckets"][bucket]]

    # ---- the four core buckets ------------------------------------------

    def test_untouched_file_the_release_changed_updates_safely(self):
        self.setup_pair(
            baseline_files={"skills/a.md": "v1"},
            release_files={"skills/a.md": "v2"},
        )
        report = self.classify()
        self.assertEqual(self.paths_in(report, "safe_update"), ["skills/a.md"])
        self.assertFalse(report["needs_user_decision"])

    def test_user_modified_file_the_release_left_alone_is_kept(self):
        self.setup_pair(
            baseline_files={"skills/a.md": "v1"},
            release_files={"skills/a.md": "v1"},
            disk_files={"skills/a.md": "my own edit"},
        )
        report = self.classify()
        self.assertEqual(self.paths_in(report, "keep_theirs"), ["skills/a.md"])
        self.assertEqual(report["counts"]["conflict"], 0)
        self.assertFalse(report["needs_user_decision"])

    def test_both_changed_is_a_conflict_needing_a_decision(self):
        self.setup_pair(
            baseline_files={"skills/a.md": "v1"},
            release_files={"skills/a.md": "v2"},
            disk_files={"skills/a.md": "my own edit"},
        )
        report = self.classify()
        self.assertEqual(self.paths_in(report, "conflict"), ["skills/a.md"])
        self.assertEqual(report["counts"]["safe_update"], 0)
        self.assertTrue(report["needs_user_decision"])

    def test_untouched_and_unchanged_is_a_no_op(self):
        self.setup_pair(
            baseline_files={"skills/a.md": "v1"},
            release_files={"skills/a.md": "v1"},
        )
        report = self.classify()
        self.assertEqual(self.paths_in(report, "unchanged"), ["skills/a.md"])
        self.assertFalse(report["needs_user_decision"])

    # ---- edge buckets ----------------------------------------------------

    def test_file_new_in_the_release_is_added(self):
        self.setup_pair(
            baseline_files={"skills/a.md": "v1"},
            release_files={"skills/a.md": "v1", "skills/b.md": "brand new"},
        )
        self.assertEqual(self.paths_in(self.classify(), "new"), ["skills/b.md"])

    def test_file_retired_by_the_release_is_flagged_not_deleted(self):
        self.setup_pair(
            baseline_files={"skills/a.md": "v1", "skills/gone.md": "old"},
            release_files={"skills/a.md": "v1"},
        )
        report = self.classify()
        self.assertEqual(self.paths_in(report, "removed_upstream"), ["skills/gone.md"])
        self.assertTrue(report["needs_user_decision"])

    def test_retired_file_reports_whether_the_user_had_customized_it(self):
        # An untouched retirement needs no conversation; a customized one does.
        self.setup_pair(
            baseline_files={"skills/a.md": "v1", "skills/plain.md": "old", "skills/mine.md": "old"},
            release_files={"skills/a.md": "v1"},
            disk_files={"skills/a.md": "v1", "skills/plain.md": "old", "skills/mine.md": "my version"},
        )
        by_path = {e["path"]: e for e in self.classify()["buckets"]["removed_upstream"]}
        self.assertFalse(by_path["skills/plain.md"]["customized"])
        self.assertTrue(by_path["skills/mine.md"]["customized"])

    def test_retired_file_the_user_already_deleted_is_a_no_op(self):
        self.setup_pair(
            baseline_files={"skills/a.md": "v1", "skills/gone.md": "old"},
            release_files={"skills/a.md": "v1"},
            disk_files={"skills/a.md": "v1"},
        )
        report = self.classify()
        self.assertEqual(report["counts"]["removed_upstream"], 0)
        self.assertFalse(report["needs_user_decision"])

    # ---- the release arriving by another route ---------------------------

    def test_file_already_matching_the_release_is_not_a_conflict(self):
        # The signature of a release unpacked over the install. Reporting these
        # as conflicts manufactures decisions that don't exist.
        self.setup_pair(
            baseline_files={"skills/a.md": "v1"},
            release_files={"skills/a.md": "v2"},
            disk_files={"skills/a.md": "v2"},
        )
        report = self.classify()
        self.assertEqual(self.paths_in(report, "already_applied"), ["skills/a.md"])
        self.assertEqual(report["counts"]["conflict"], 0)
        self.assertFalse(report["needs_user_decision"])

    def test_wholesale_overwrite_is_called_out_not_reported_as_success(self):
        self.setup_pair(
            baseline_files={f"skills/s{i}.md": "v1" for i in range(6)},
            release_files={f"skills/s{i}.md": "v2" for i in range(6)},
            disk_files={f"skills/s{i}.md": "v2" for i in range(6)},
        )
        report = self.classify()
        self.assertEqual(report["counts"]["already_applied"], 6)
        self.assertTrue(report["likely_already_applied"])
        self.assertIn("unpacked over the install", self.run_classify("--format", "text").stdout)

    def test_a_single_already_applied_file_does_not_cry_overwrite(self):
        # One file matching the release amid real work is not the overwrite signature.
        self.setup_pair(
            baseline_files={f"skills/s{i}.md": "v1" for i in range(6)},
            release_files={f"skills/s{i}.md": "v2" for i in range(6)},
            disk_files={"skills/s0.md": "v2", **{f"skills/s{i}.md": "v1" for i in range(1, 6)}},
        )
        report = self.classify()
        self.assertEqual(report["counts"]["already_applied"], 1)
        self.assertEqual(report["counts"]["safe_update"], 5)
        self.assertFalse(report["likely_already_applied"])

    def test_genuine_conflicts_still_surface_alongside_already_applied_files(self):
        self.setup_pair(
            baseline_files={"skills/a.md": "v1", "skills/b.md": "v1"},
            release_files={"skills/a.md": "v2", "skills/b.md": "v2"},
            disk_files={"skills/a.md": "v2", "skills/b.md": "my own edit"},
        )
        report = self.classify()
        self.assertEqual(self.paths_in(report, "already_applied"), ["skills/a.md"])
        self.assertEqual(self.paths_in(report, "conflict"), ["skills/b.md"])
        self.assertTrue(report["needs_user_decision"])

    def test_file_the_user_deleted_is_asked_about_not_resurrected(self):
        self.setup_pair(
            baseline_files={"skills/a.md": "v1", "skills/deleted.md": "v1"},
            release_files={"skills/a.md": "v1", "skills/deleted.md": "v2"},
            disk_files={"skills/a.md": "v1"},
        )
        report = self.classify()
        self.assertEqual(self.paths_in(report, "missing_locally"), ["skills/deleted.md"])
        self.assertNotIn("skills/deleted.md", self.paths_in(report, "safe_update"))
        self.assertTrue(report["needs_user_decision"])

    def test_hybrid_files_are_flagged_so_the_conversation_is_not_a_surprise(self):
        self.setup_pair(
            baseline_files={"AGENTS.md": "v1"},
            release_files={"AGENTS.md": "v2"},
            disk_files={"AGENTS.md": "my tuned principles"},
        )
        conflict = self.classify()["buckets"]["conflict"]
        self.assertEqual(len(conflict), 1)
        self.assertTrue(conflict[0]["hybrid"])

    # ---- install-once ----------------------------------------------------

    def test_absent_starter_file_is_copied(self):
        self.setup_pair(
            baseline_files={"skills/a.md": "v1"},
            release_files={"skills/a.md": "v1", "os-inputs/_os-session-log.md": "starter"},
        )
        # The starter file ships in the release folder but isn't in the workspace.
        report = self.classify()
        self.assertEqual(self.paths_in(report, "install_once"), ["os-inputs/_os-session-log.md"])

    def test_existing_starter_file_is_left_entirely_alone(self):
        self.setup_pair(
            baseline_files={"skills/a.md": "v1"},
            release_files={"skills/a.md": "v1", "os-inputs/_os-session-log.md": "starter"},
        )
        self.write(self.workspace, "os-inputs/_os-session-log.md", "months of my notes")
        report = self.classify()
        self.assertEqual(report["counts"]["install_once"], 0)
        for bucket in report["buckets"].values():
            self.assertNotIn(
                "os-inputs/_os-session-log.md", [e["path"] for e in bucket]
            )

    # ---- the invariants --------------------------------------------------

    def test_user_owned_territory_is_never_classified_even_if_the_manifest_lists_it(self):
        # A malformed or malicious manifest listing user data must not pull it in.
        self.setup_pair(
            baseline_files={"skills/a.md": "v1", "os-tracker/my-tasks.md": "mine"},
            release_files={"skills/a.md": "v2", "os-tracker/my-tasks.md": "theirs"},
            disk_files={"skills/a.md": "v1", "os-tracker/my-tasks.md": "mine"},
        )
        report = self.classify()
        for name, bucket in report["buckets"].items():
            if name == "skipped_user_owned":
                continue
            self.assertNotIn("os-tracker/my-tasks.md", [e["path"] for e in bucket])
        self.assertEqual(self.paths_in(report, "skipped_user_owned"), ["os-tracker/my-tasks.md"])

    def test_user_owned_zone_added_by_the_new_release_is_honored_immediately(self):
        # Protection is the union of both manifests, so a newly protected area
        # is safe on the very update that introduces it.
        self.write_manifest(
            self.workspace, ".os-manifest.json", "0.1.0",
            {"skills/a.md": "v1", "os-vault/secret.md": "mine"},
            ownership=self.ownership(user_owned_never_touch=["os-tracker"]),
        )
        self.write_manifest(
            self.release, "os-manifest.json", "0.2.0",
            {"skills/a.md": "v2", "os-vault/secret.md": "theirs"},
            ownership=self.ownership(user_owned_never_touch=["os-tracker", "os-vault"]),
        )
        for rel_path, content in {"skills/a.md": "v2", "os-vault/secret.md": "theirs"}.items():
            self.write(self.release, rel_path, content)
        for rel_path, content in {"skills/a.md": "v1", "os-vault/secret.md": "mine"}.items():
            self.write(self.workspace, rel_path, content)
        report = self.classify()
        self.assertEqual(self.paths_in(report, "skipped_user_owned"), ["os-vault/secret.md"])

    def test_missing_baseline_refuses_to_classify(self):
        self.write_manifest(self.release, "os-manifest.json", "0.2.0", {"skills/a.md": "v2"})
        result = self.run_classify(expect=EXIT_NO_BASELINE)
        self.assertIn("no baseline", result.stderr)
        self.assertIn("bulk-overwrite", result.stderr)

    def test_same_version_stops_before_doing_anything(self):
        self.write_manifest(self.workspace, ".os-manifest.json", "0.2.0", {"skills/a.md": "v1"})
        self.write_manifest(self.release, "os-manifest.json", "0.2.0", {"skills/a.md": "v1"})
        result = self.run_classify(expect=EXIT_UP_TO_DATE)
        self.assertIn("0.2.0", result.stderr)

    def test_unzipping_over_the_install_is_caught_and_explained(self):
        self.write_manifest(self.workspace, ".os-manifest.json", "0.1.0", {"skills/a.md": "v1"})
        self.write_manifest(self.workspace, "os-manifest.json", "0.2.0", {"skills/a.md": "v2"})
        result = subprocess.run(
            ["python3", str(SCRIPT), "--workspace", str(self.workspace),
             "--release", str(self.workspace)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, EXIT_ERROR)
        self.assertIn("destroys the baseline", result.stderr)

    # ---- release integrity ----------------------------------------------

    def test_file_missing_from_the_release_folder_is_caught(self):
        self.setup_pair(
            baseline_files={"skills/a.md": "v1"},
            release_files={"skills/a.md": "v2", "skills/b.md": "new"},
        )
        (self.release / "skills" / "b.md").unlink()
        report = self.classify()
        self.assertEqual(self.paths_in(report, "release_incomplete"), ["skills/b.md"])
        self.assertTrue(report["needs_user_decision"])

    def test_corrupt_release_file_is_caught_before_it_can_be_applied(self):
        self.setup_pair(
            baseline_files={"skills/a.md": "v1"},
            release_files={"skills/a.md": "v2"},
        )
        (self.release / "skills" / "a.md").write_text("truncated")
        report = self.classify()
        self.assertEqual(self.paths_in(report, "release_incomplete"), ["skills/a.md"])
        self.assertEqual(report["counts"]["safe_update"], 0)

    # ---- finding the release root ---------------------------------------

    def test_extraction_directory_is_accepted_not_just_the_release_root(self):
        # The pack unzips into one top-level folder, so pointing at the directory
        # it was extracted into is the natural move. It should just work.
        self.setup_pair(
            baseline_files={"skills/a.md": "v1"},
            release_files={"skills/a.md": "v2"},
        )
        extracted = Path(self.tempdir.name) / "extracted"
        (extracted / "personal-os").mkdir(parents=True)
        for item in self.release.iterdir():
            target = extracted / "personal-os" / item.name
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                for sub in item.rglob("*"):
                    if sub.is_file():
                        dest = target / sub.relative_to(item)
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        dest.write_bytes(sub.read_bytes())
            else:
                target.write_bytes(item.read_bytes())
        self.release = extracted
        report = self.classify()
        self.assertEqual(self.paths_in(report, "safe_update"), ["skills/a.md"])

    def test_two_candidate_releases_are_ambiguous_and_refuse_to_guess(self):
        self.write_manifest(self.workspace, ".os-manifest.json", "0.1.0", {"skills/a.md": "v1"})
        self.write(self.workspace, "skills/a.md", "v1")
        for name, version in (("personal-os-0.2.0", "0.2.0"), ("personal-os-0.3.0", "0.3.0")):
            sub = self.release / name
            sub.mkdir(parents=True)
            self.write_manifest(sub, "os-manifest.json", version, {"skills/a.md": "v2"})
        result = self.run_classify(expect=EXIT_ERROR)
        self.assertIn("more than one release", result.stderr)
        self.assertIn("personal-os-0.2.0", result.stderr)

    # ---- reporting -------------------------------------------------------

    def test_text_format_leads_with_counts_not_paths(self):
        self.setup_pair(
            baseline_files={"skills/a.md": "v1", "skills/b.md": "v1"},
            release_files={"skills/a.md": "v2", "skills/b.md": "v2"},
            disk_files={"skills/a.md": "v1", "skills/b.md": "mine"},
        )
        out = self.run_classify("--format", "text").stdout
        self.assertIn("0.1.0 → 0.2.0", out)
        self.assertIn("1 files update safely", out)
        self.assertIn("Needs attention:", out)
        self.assertIn("skills/b.md", out)

    def test_whats_new_is_reported_when_present_and_null_when_not(self):
        self.setup_pair(
            baseline_files={"skills/a.md": "v1"},
            release_files={"skills/a.md": "v2"},
        )
        self.assertIsNone(self.classify()["whats_new"])
        (self.release / "WHATS-NEW.md").write_text("# What's new")
        self.assertIsNotNone(self.classify()["whats_new"])

    def test_text_report_survives_a_cp1252_console(self):
        # The text report's first line prints an arrow between versions.
        # Windows consoles default to cp1252, which can't encode it; without
        # the UTF-8 guard the classification succeeds but the print crashes,
        # and exit 1 sends the user to the wrong diagnosis. The guard has been
        # lost in two successive rewrites — this stays red if it happens again.
        import os

        self.setup_pair(
            baseline_files={"skills/a.md": "v1"},
            release_files={"skills/a.md": "v2"},
        )
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "cp1252"
        result = subprocess.run(
            ["python3", str(SCRIPT), "--workspace", str(self.workspace),
             "--release", str(self.release), "--format", "text"],
            text=True, capture_output=True, check=False, env=env,
        )
        self.assertEqual(result.returncode, EXIT_OK, result.stderr)
        self.assertNotIn("UnicodeEncodeError", result.stderr)


if __name__ == "__main__":
    unittest.main()
