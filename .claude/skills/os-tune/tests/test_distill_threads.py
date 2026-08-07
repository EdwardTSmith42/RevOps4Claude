"""Tests for distill_threads.py — extracting the user's own words from threads.

Every filter here exists because something leaked during a real run against
real transcripts. The tests pin those cases so the leak can't come back: if
assistant-authored or harness-injected text reaches the extract output, the
pattern detection downstream clusters the machine's habits as if they were
the user's, which is worse than finding no pattern at all.
"""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "distill_threads.py"
EXIT_OK, EXIT_ERROR, EXIT_NOTHING = 0, 1, 3


def user(text):
    return {"type": "user", "timestamp": "2026-08-01T10:00:00Z",
            "message": {"role": "user", "content": text}}


def assistant(text):
    return {"type": "assistant", "timestamp": "2026-08-01T10:00:01Z",
            "message": {"role": "assistant", "content": [{"type": "text", "text": text}]}}


def tool_result(text):
    return {"type": "user", "timestamp": "2026-08-01T10:00:02Z",
            "message": {"role": "user",
                        "content": [{"type": "tool_result", "tool_use_id": "x", "content": text}]}}


class DistillThreadsTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.transcripts = self.root / "projects"
        self.transcripts.mkdir()
        self.state = self.root / "state.json"

    def tearDown(self):
        self.tempdir.cleanup()

    def write_thread(self, project, thread_id, records, subagent=False):
        d = self.transcripts / project
        if subagent:
            d = d / thread_id / "subagents"
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"{thread_id if not subagent else 'agent-1'}.jsonl"
        path.write_text("".join(json.dumps(r) + "\n" for r in records))
        return path

    def run_cmd(self, *args, expect=EXIT_OK):
        result = subprocess.run(
            ["python3", str(SCRIPT), *args,
             "--transcripts-dir", str(self.transcripts), "--state", str(self.state)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, expect, result.stderr)
        return result

    def extract(self, *args):
        return json.loads(self.run_cmd("extract", *args).stdout)

    def all_turns(self, payload):
        return [t["text"] for th in payload["threads"] for t in th["turns"]]

    # ---- what counts as the user speaking ---------------------------------

    def test_user_turns_are_extracted(self):
        self.write_thread("proj", "t1", [user("draft the release email"), assistant("ok")])
        self.assertEqual(self.all_turns(self.extract()), ["draft the release email"])

    def test_assistant_turns_are_never_extracted(self):
        self.write_thread("proj", "t1", [assistant("Here is my analysis"), user("thanks")])
        self.assertEqual(self.all_turns(self.extract()), ["thanks"])

    def test_tool_results_are_not_user_speech(self):
        self.write_thread("proj", "t1", [tool_result("file contents here"), user("real ask")])
        self.assertEqual(self.all_turns(self.extract()), ["real ask"])

    def test_subagent_transcripts_are_excluded_entirely(self):
        # These outnumber real turns on a working machine; including them would
        # surface the assistant's own habits as if they were the user's.
        self.write_thread("proj", "t1", [user("the real request")])
        self.write_thread("proj", "t1", [user("Review this diff for bugs")], subagent=True)
        payload = self.extract()
        self.assertEqual(self.all_turns(payload), ["the real request"])

    def test_harness_injected_text_is_filtered(self):
        injected = [
            "<system-reminder>do the thing</system-reminder>",
            "<command-name>/model</command-name>",
            "<local-command-stdout>Compacted</local-command-stdout>",
            "<task-notification><task-id>x</task-id></task-notification>",
            "Base directory for this skill: /Users/x/.claude/skills/foo",
            "This session is being continued from a previous conversation that ran out of context.",
            "[Request interrupted by user]",
            "Continue from where you left off.",
        ]
        self.write_thread("proj", "t1", [user(t) for t in injected] + [user("my actual ask")])
        self.assertEqual(self.all_turns(self.extract()), ["my actual ask"])

    def test_short_turns_are_kept(self):
        # "commit push" repeated is a strong skill signal, not noise.
        self.write_thread("proj", "t1", [user("commit push"), user("say OK")])
        self.assertEqual(self.all_turns(self.extract()), ["commit push", "say OK"])

    # ---- state and idempotency -------------------------------------------

    def test_marked_threads_are_not_reprocessed(self):
        self.write_thread("proj", "t1", [user("first")])
        self.write_thread("proj", "t2", [user("second")])
        self.assertEqual(len(self.extract()["threads"]), 2)
        self.run_cmd("mark", "--thread", "t1", "--memories", "2")
        remaining = self.extract()
        self.assertEqual([t["thread_id"] for t in remaining["threads"]], ["t2"])

    def test_scan_reports_nothing_pending_once_all_marked(self):
        self.write_thread("proj", "t1", [user("only one")])
        self.run_cmd("mark", "--thread", "t1")
        self.run_cmd("scan", expect=EXIT_NOTHING)

    def test_extract_exits_distinctly_when_nothing_pending(self):
        self.write_thread("proj", "t1", [user("x")])
        self.run_cmd("mark", "--thread", "t1")
        self.run_cmd("extract", expect=EXIT_NOTHING)

    # ---- project scoping --------------------------------------------------

    def test_excluded_project_is_skipped(self):
        self.write_thread("client-work", "t1", [user("client thing")])
        self.write_thread("mine", "t2", [user("my thing")])
        self.run_cmd("exclude", "--project", "client-work")
        self.assertEqual(self.all_turns(self.extract()), ["my thing"])

    def test_project_name_matches_with_or_without_leading_dashes(self):
        # Claude Code encodes paths into dir names, so real names start with "-",
        # which argparse reads as a flag unless the user knows to strip it.
        self.write_thread("-Users-work-client", "t1", [user("client thing")])
        self.write_thread("mine", "t2", [user("my thing")])
        self.run_cmd("exclude", "--project", "Users-work-client")
        self.assertEqual(self.all_turns(self.extract()), ["my thing"])

    def test_exclusions_persist_across_runs(self):
        self.write_thread("client-work", "t1", [user("client thing")])
        self.run_cmd("exclude", "--project", "client-work")
        state = json.loads(self.state.read_text())
        self.assertEqual(state["excluded_projects"], ["client-work"])

    # ---- windowing and batching ------------------------------------------

    def test_limit_batches_threads_and_reports_the_remainder(self):
        for i in range(4):
            self.write_thread("proj", f"t{i}", [user(f"ask {i}")])
        payload = self.extract("--limit", "2")
        self.assertEqual(payload["extracted"], 2)
        self.assertEqual(payload["remaining"], 2)

    def test_max_turns_caps_a_long_thread_keeping_both_ends(self):
        records = [user(f"turn {i}") for i in range(30)]
        self.write_thread("proj", "t1", records)
        turns = self.all_turns(self.extract("--max-turns", "6"))
        self.assertEqual(len(turns), 6)
        self.assertIn("turn 0", turns)      # opening intent
        self.assertIn("turn 29", turns)     # closing decisions

    def test_oldest_threads_come_first(self):
        # Oldest is closest to the harness's retention cliff.
        import os, time
        p1 = self.write_thread("proj", "new", [user("newer")])
        p2 = self.write_thread("proj", "old", [user("older")])
        old = time.time() - 5 * 86400
        os.utime(p2, (old, old))
        self.assertEqual([t["thread_id"] for t in self.extract()["threads"]], ["old", "new"])

    def test_threads_outside_the_window_are_ignored(self):
        import os, time
        p = self.write_thread("proj", "ancient", [user("long ago")])
        old = time.time() - 200 * 86400
        os.utime(p, (old, old))
        self.run_cmd("scan", "--days", "60", expect=EXIT_NOTHING)

    # ---- failure modes ----------------------------------------------------

    def test_missing_transcripts_dir_is_an_actionable_error(self):
        result = subprocess.run(
            ["python3", str(SCRIPT), "scan",
             "--transcripts-dir", str(self.root / "nope"), "--state", str(self.state)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, EXIT_ERROR)
        self.assertIn("not found", result.stderr)

    def test_malformed_lines_do_not_abort_a_thread(self):
        path = self.write_thread("proj", "t1", [user("good one")])
        path.write_text("not json\n" + path.read_text())
        self.assertEqual(self.all_turns(self.extract()), ["good one"])


if __name__ == "__main__":
    unittest.main()
