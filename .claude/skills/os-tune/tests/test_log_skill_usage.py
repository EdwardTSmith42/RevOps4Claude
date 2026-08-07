"""Tests for log_skill_usage.py — the optional skill-invocation hook.

The hook runs inside the user's turn, so the invariant that matters most isn't
correctness of the row, it's that nothing it does can break the turn. Every
malformed-input test below asserts exit 0 and no crash. A logging side-effect
that fails loudly is worse than no logging at all.
"""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "log_skill_usage.py"


class LogSkillUsageTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.log = Path(self.tempdir.name) / "nested" / "skill-usage.jsonl"

    def tearDown(self):
        self.tempdir.cleanup()

    def run_hook(self, payload, cwd=None):
        env = os.environ.copy()
        env["OS_SKILL_USAGE_LOG"] = str(self.log)
        raw = payload if isinstance(payload, str) else json.dumps(payload)
        result = subprocess.run(
            ["python3", str(SCRIPT)], input=raw, text=True,
            capture_output=True, env=env, cwd=cwd or self.tempdir.name, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def rows(self):
        if not self.log.is_file():
            return []
        return [json.loads(l) for l in self.log.read_text().splitlines() if l.strip()]

    # ---- the happy path ---------------------------------------------------

    def test_writes_one_row_per_invocation(self):
        self.run_hook({"tool_input": {"skill": "os-editing", "args": "humanize the draft"},
                       "tool_use_id": "toolu_1"})
        rows = self.rows()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["skill"], "os-editing")
        self.assertEqual(rows[0]["args_preview"], "humanize the draft")
        self.assertEqual(rows[0]["tool_use_id"], "toolu_1")
        self.assertTrue(rows[0]["ts"].endswith("Z"))

    def test_appends_rather_than_overwrites(self):
        self.run_hook({"tool_input": {"skill": "a"}})
        self.run_hook({"tool_input": {"skill": "b"}})
        self.assertEqual([r["skill"] for r in self.rows()], ["a", "b"])

    def test_creates_the_log_directory(self):
        self.assertFalse(self.log.parent.exists())
        self.run_hook({"tool_input": {"skill": "os-tune"}})
        self.assertTrue(self.log.is_file())

    def test_records_the_working_directory(self):
        # cwd is how the log gets partitioned by project later.
        self.run_hook({"tool_input": {"skill": "os-tune"}}, cwd=self.tempdir.name)
        self.assertEqual(self.rows()[0]["cwd"], str(Path(self.tempdir.name).resolve()))

    def test_long_args_are_truncated(self):
        self.run_hook({"tool_input": {"skill": "x", "args": "y" * 500}})
        self.assertEqual(len(self.rows()[0]["args_preview"]), 200)

    def test_alternate_payload_key_spellings_are_accepted(self):
        self.run_hook({"toolInput": {"skill_name": "os-gold", "arguments": "mine this"},
                       "toolUseId": "t2"})
        row = self.rows()[0]
        self.assertEqual((row["skill"], row["args_preview"], row["tool_use_id"]),
                         ("os-gold", "mine this", "t2"))

    def test_missing_args_still_logs_the_skill(self):
        # 27% of real invocations carry no args; the skill name alone is signal.
        self.run_hook({"tool_input": {"skill": "dev-checkpoint"}})
        self.assertEqual(self.rows()[0]["args_preview"], "")

    def test_unicode_survives_the_round_trip(self):
        self.run_hook({"tool_input": {"skill": "os-writing", "args": "draft — with an em dash ✓"}})
        self.assertIn("—", self.rows()[0]["args_preview"])

    # ---- nothing may break the turn ---------------------------------------

    def test_malformed_json_writes_nothing_and_exits_clean(self):
        self.run_hook("{not json at all")
        self.assertEqual(self.rows(), [])

    def test_empty_stdin_writes_nothing(self):
        self.run_hook("")
        self.assertEqual(self.rows(), [])

    def test_payload_without_a_skill_name_writes_nothing(self):
        # An empty row would quietly poison frequency counts; better to write
        # nothing and let the log's staleness be the visible signal.
        self.run_hook({"tool_input": {"args": "no skill here"}})
        self.assertEqual(self.rows(), [])

    def test_payload_with_no_tool_input_writes_nothing(self):
        self.run_hook({"something_else": True})
        self.assertEqual(self.rows(), [])

    def test_non_dict_tool_input_writes_nothing(self):
        self.run_hook({"tool_input": "a string, unexpectedly"})
        self.assertEqual(self.rows(), [])

    def test_non_string_skill_value_does_not_crash(self):
        self.run_hook({"tool_input": {"skill": {"nested": "object"}}})
        self.assertEqual(self.rows(), [])

    def test_unwritable_log_path_fails_silently(self):
        env = os.environ.copy()
        env["OS_SKILL_USAGE_LOG"] = "/proc/nonexistent/cannot-write.jsonl"
        result = subprocess.run(
            ["python3", str(SCRIPT)], input=json.dumps({"tool_input": {"skill": "x"}}),
            text=True, capture_output=True, env=env, check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_hook_is_silent_on_success(self):
        # Anything printed would land in the user's transcript.
        result = self.run_hook({"tool_input": {"skill": "os-tune"}})
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
