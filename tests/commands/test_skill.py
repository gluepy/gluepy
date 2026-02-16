import os
import shutil
import tempfile
from unittest import TestCase, mock
from click.testing import CliRunner
from gluepy.commands import cli


class SkillCommandTestCase(TestCase):
    def setUp(self):
        self._orig_cwd = os.getcwd()
        self._tmpdir = tempfile.mkdtemp()
        os.chdir(self._tmpdir)
        return super().setUp()

    def tearDown(self):
        os.chdir(self._orig_cwd)
        shutil.rmtree(self._tmpdir)
        return super().tearDown()

    def test_skill_github(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["skill", "github"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(
            os.path.exists(
                os.path.join(".github", "skills", "gluepy", "SKILL.md")
            )
        )

    def test_skill_claude(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["skill", "claude"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(
            os.path.exists(
                os.path.join(".claude", "skills", "gluepy", "SKILL.md")
            )
        )

    def test_skill_cursor(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["skill", "cursor"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(
            os.path.exists(
                os.path.join(".cursor", "skills", "gluepy", "SKILL.md")
            )
        )

    def test_skill_creates_directories(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["skill", "github"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(os.path.isdir(os.path.join(".github", "skills", "gluepy")))
        self.assertTrue(
            os.path.isdir(
                os.path.join(".github", "skills", "gluepy", "references")
            )
        )

    def test_skill_creates_reference_files(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["skill", "github"])
        self.assertEqual(result.exit_code, 0)
        ref_dir = os.path.join(".github", "skills", "gluepy", "references")
        for ref_file in ["context.md", "storage.md", "dags.md", "settings.md", "data.md"]:
            self.assertTrue(
                os.path.exists(os.path.join(ref_dir, ref_file)),
                f"Reference file '{ref_file}' not found",
            )
