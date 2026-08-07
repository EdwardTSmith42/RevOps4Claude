import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "bin" / "skill-deploy"


class SkillDeployLinkTargetsTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.home = self.root / "home"
        self.vault = self.root / "vault"
        self.skill = self.vault / "skills" / "demo-skill"
        self.skill.mkdir(parents=True)
        self.home.mkdir()
        (self.skill / "SKILL.md").write_text(
            "---\nname: demo-skill\ndescription: Test skill.\n---\n"
        )

    def tearDown(self):
        self.tempdir.cleanup()

    def run_deploy(self, *args, extra_env=None):
        env = os.environ.copy()
        env.update({
            "HOME": str(self.home),
            "NO_COLOR": "1",
            "SKILL_VAULT_ROOT": str(self.vault),
        })
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            cwd=self.vault,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def assert_link_points_to_skill(self, path):
        self.assertTrue(path.is_symlink())
        self.assertEqual(path.resolve(), self.skill.resolve())

    def write_description(self, description):
        (self.skill / "SKILL.md").write_text(
            f"---\nname: demo-skill\ndescription: >-\n  {description}\n---\n"
        )

    def test_agents_is_default_target(self):
        result = self.run_deploy("link")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_link_points_to_skill(self.home / ".agents" / "skills" / "demo-skill")

    def test_codex_alias_uses_standard_target_and_preserves_legacy_directory(self):
        legacy = self.home / ".codex" / "skills"
        legacy.mkdir(parents=True)
        marker = legacy / "keep-me"
        marker.write_text("legacy")

        result = self.run_deploy("link", "--target", "codex")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("legacy alias", result.stdout)
        self.assert_link_points_to_skill(self.home / ".agents" / "skills" / "demo-skill")
        self.assertEqual(marker.read_text(), "legacy")

    def test_claude_target_remains_explicit(self):
        result = self.run_deploy("link", "--target", "claude")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_link_points_to_skill(self.home / ".claude" / "skills" / "demo-skill")
        self.assertFalse((self.home / ".agents" / "skills" / "demo-skill").exists())

    def test_all_creates_standard_and_claude_links(self):
        result = self.run_deploy("link", "--target", "all")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_link_points_to_skill(self.home / ".agents" / "skills" / "demo-skill")
        self.assert_link_points_to_skill(self.home / ".claude" / "skills" / "demo-skill")

    def test_real_path_conflict_is_not_overwritten(self):
        conflict = self.home / ".agents" / "skills" / "demo-skill"
        conflict.mkdir(parents=True)
        marker = conflict / "owned"
        marker.write_text("user")

        result = self.run_deploy("link", "--target", "agents")

        self.assertEqual(result.returncode, 1)
        self.assertFalse(conflict.is_symlink())
        self.assertEqual(marker.read_text(), "user")

    def test_unlink_removes_only_the_selected_symlink(self):
        self.assertEqual(self.run_deploy("link", "--target", "all").returncode, 0)

        result = self.run_deploy("unlink", "demo-skill", "--target", "agents")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.home / ".agents" / "skills" / "demo-skill").exists())
        self.assert_link_points_to_skill(self.home / ".claude" / "skills" / "demo-skill")

    def test_zip_accepts_description_at_1024_characters(self):
        (self.skill / "SKILL.md").write_text(
            "---\nname: demo-skill\ndescription: >-\n"
            f"  {'a' * 512}\n\n  {'b' * 511}\n---\n"
        )

        result = self.run_deploy("zip", "demo-skill")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.vault / "dist" / "demo-skill.zip").exists())

    def test_zip_rejects_description_over_1024_characters(self):
        self.write_description("a" * 1025)

        result = self.run_deploy("zip", "demo-skill")

        self.assertEqual(result.returncode, 1)
        self.assertIn("description is 1025 characters", result.stderr)
        self.assertIn("1 over the 1024-character maximum", result.stderr)
        self.assertFalse((self.vault / "dist" / "demo-skill.zip").exists())


    def test_output_survives_a_cp1252_console(self):
        # Windows consoles default to cp1252, which can't encode the arrows
        # this tool prints. The UTF-8 guard has been lost in two successive
        # rewrites of this file — this stays red if it goes missing a third time.
        result = self.run_deploy(
            "zip", "demo-skill", extra_env={"PYTHONIOENCODING": "cp1252"}
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("UnicodeEncodeError", result.stderr)
        self.assertIn("zipped", result.stdout)


if __name__ == "__main__":
    unittest.main()
