"""Tests for skill_usage_report.py — mode resolution from free-form args.

The bug this replaced reported every mode in every skill as "never fired",
because it read a `mode` field the log has never contained. The tests that
matter here are the ones that keep a false "dead mode" verdict from coming
back: a mode that fired must never be listed as never-fired, and a skill with
no declared modes must not be treated as missing data.
"""

import json
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "skill_usage_report.py"


def now_iso(days_ago: int = 0) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")


class SkillUsageReportTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.skills = self.root / "skills"
        self.skills.mkdir()
        self.log = self.root / "usage.jsonl"

    def tearDown(self):
        self.tempdir.cleanup()

    def add_skill(self, name, modes=(), frontmatter_modes=()):
        d = self.skills / name
        d.mkdir(parents=True)
        front = "---\nname: %s\n" % name
        if frontmatter_modes:
            front += "modes:\n" + "".join(f"  - name: {m}\n    job: x\n" for m in frontmatter_modes)
        (d / "SKILL.md").write_text(front + "---\n\n# %s\n" % name)
        for m in modes:
            (d / "modes").mkdir(exist_ok=True)
            (d / "modes" / f"{m}.md").write_text(f"# {m}\n")

    def write_log(self, rows):
        self.log.write_text("".join(json.dumps(r) + "\n" for r in rows))

    def report(self, *args):
        result = subprocess.run(
            ["python3", str(SCRIPT), "--log", str(self.log),
             "--skills-dir", str(self.skills), "--format", "json", *args],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    # ---- mode resolution -------------------------------------------------

    def test_mode_named_in_args_is_resolved(self):
        self.add_skill("dev-plan", modes=["scope", "architecture", "prd"])
        self.write_log([{"ts": now_iso(1), "skill": "dev-plan",
                         "args_preview": "architecture — boundaries for the new service"}])
        r = self.report()
        self.assertEqual(r["modes_fired"], {"dev-plan": ["architecture"]})
        self.assertNotIn("dev-plan:architecture", r["modes_never_fired"])
        self.assertIn("dev-plan:prd", r["modes_never_fired"])

    def test_prose_args_do_not_produce_a_false_mode(self):
        # The old heuristic took the first word; real args start with prose.
        self.add_skill("dev-review", modes=["ship-gate", "digest"])
        self.write_log([{"ts": now_iso(1), "skill": "dev-review",
                         "args_preview": "Re-review the update path before we ship"}])
        r = self.report()
        self.assertEqual(r["modes_fired"], {})
        self.assertEqual(r["invoked_without_naming_a_mode"], [["dev-review", 1]])

    def test_skill_with_no_declared_modes_is_not_counted_as_missing_data(self):
        self.add_skill("dev-fresh-eyes")
        self.write_log([{"ts": now_iso(1), "skill": "dev-fresh-eyes",
                         "args_preview": "Pressure-test this plan"}])
        r = self.report()
        self.assertEqual(r["invoked_without_naming_a_mode"], [])
        self.assertEqual(r["modes_never_fired"], [])

    def test_longer_mode_name_wins_over_a_shorter_substring(self):
        self.add_skill("os-content-mining", modes=["extract", "multi-layer-extract"])
        self.write_log([{"ts": now_iso(1), "skill": "os-content-mining",
                         "args_preview": "multi-layer-extract on the talk transcript"}])
        self.assertEqual(self.report()["modes_fired"], {"os-content-mining": ["multi-layer-extract"]})

    def test_mode_must_match_on_a_word_boundary(self):
        self.add_skill("os-editing", modes=["shorten"])
        self.write_log([{"ts": now_iso(1), "skill": "os-editing",
                         "args_preview": "unshortened draft needs a pass"}])
        self.assertEqual(self.report()["modes_fired"], {})

    def test_modes_are_read_from_frontmatter_when_there_is_no_modes_dir(self):
        self.add_skill("os-capture", frontmatter_modes=["route", "process"])
        self.write_log([{"ts": now_iso(1), "skill": "os-capture",
                         "args_preview": "process the inbox backlog"}])
        r = self.report()
        self.assertEqual(r["modes_fired"], {"os-capture": ["process"]})
        self.assertIn("os-capture:route", r["modes_never_fired"])

    def test_an_explicit_mode_field_wins_over_inferring_from_args(self):
        # Two log shapes exist. A harness hook records skill + raw args and no
        # mode, because harnesses have no concept of one. A workspace log
        # written by an agent records mode directly. Inferring when the answer
        # is already stated reports live modes as never-fired.
        self.add_skill("os-editing", modes=["humanize", "shorten"])
        self.write_log([{"ts": now_iso(1), "skill": "os-editing", "mode": "humanize",
                         "ctx": "pass over a draft", "outcome": "applied"}])
        r = self.report()
        self.assertEqual(r["modes_fired"], {"os-editing": ["humanize"]})
        self.assertNotIn("os-editing:humanize", r["modes_never_fired"])
        self.assertIn("os-editing:shorten", r["modes_never_fired"])

    def test_explicit_mode_beats_a_conflicting_word_in_the_args(self):
        self.add_skill("os-editing", modes=["humanize", "shorten"])
        self.write_log([{"ts": now_iso(1), "skill": "os-editing", "mode": "humanize",
                         "args_preview": "shorten this if you can"}])
        self.assertEqual(self.report()["modes_fired"], {"os-editing": ["humanize"]})

    def test_timestamps_without_a_timezone_do_not_crash(self):
        # The workspace log omits the zone; the hook log stamps a trailing Z.
        # Comparing the two shapes raised TypeError and killed the whole report.
        self.add_skill("os-editing", modes=["humanize"])
        naive = now_iso(1).rstrip("Z")
        self.write_log([{"ts": naive, "skill": "os-editing", "mode": "humanize"}])
        r = self.report()
        self.assertEqual(r["total_invocations"], 1)
        self.assertEqual(r["modes_fired"], {"os-editing": ["humanize"]})

    def test_mixed_timestamp_shapes_in_one_log_both_count(self):
        self.add_skill("os-editing", modes=["humanize"])
        self.write_log([
            {"ts": now_iso(1), "skill": "os-editing", "mode": "humanize"},
            {"ts": now_iso(2).rstrip("Z"), "skill": "os-editing", "mode": "humanize"},
        ])
        self.assertEqual(self.report()["total_invocations"], 2)

    # ---- windowing and idle detection ------------------------------------

    def test_entries_outside_the_window_are_excluded(self):
        self.add_skill("dev-plan", modes=["scope"])
        self.write_log([{"ts": now_iso(90), "skill": "dev-plan", "args_preview": "scope it"}])
        r = self.report("--days", "30")
        self.assertEqual(r["total_invocations"], 0)
        self.assertIn("dev-plan", r["idle_skills"])

    def test_installed_but_uninvoked_skill_is_idle(self):
        self.add_skill("dev-plan", modes=["scope"])
        self.add_skill("os-writing")
        self.write_log([{"ts": now_iso(1), "skill": "dev-plan", "args_preview": "scope it"}])
        r = self.report()
        self.assertEqual(r["idle_skills"], ["os-writing"])

    def test_comment_and_malformed_lines_are_skipped(self):
        self.add_skill("dev-plan", modes=["scope"])
        self.log.write_text(
            "# header comment\n"
            "not json at all\n"
            + json.dumps({"ts": now_iso(1), "skill": "dev-plan", "args_preview": "scope it"}) + "\n"
            + json.dumps({"skill": "dev-plan"}) + "\n"  # no ts
        )
        self.assertEqual(self.report()["total_invocations"], 1)

    def test_missing_log_fails_with_an_actionable_message(self):
        self.add_skill("dev-plan", modes=["scope"])
        result = subprocess.run(
            ["python3", str(SCRIPT), "--log", str(self.root / "nope.jsonl"),
             "--skills-dir", str(self.skills)],
            text=True, capture_output=True, check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--log", result.stderr)


if __name__ == "__main__":
    unittest.main()
