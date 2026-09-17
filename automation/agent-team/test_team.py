import argparse
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import team


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.run = Path(self.temp.name)
        self.args = argparse.Namespace(rounds=2)
        self.plan = dict(status="ready", summary="plan", steps=["implement"],
                         acceptance_criteria=["works"], files_to_inspect=[], blockers=[])

    def status(self):
        return json.loads((self.run / "status.json").read_text())["status"]

    def test_review_feedback_reaches_executor(self):
        fix = dict(verdict="changes_requested", summary="missing check",
                   required_fixes=["Verify empty input"], evidence=[])
        ok = dict(verdict="approved", summary="done", required_fixes=[], evidence=["file inspected"])
        with patch.object(team, "claude", side_effect=[self.plan, fix, ok]), \
                patch.object(team, "codex", return_value="implemented") as execute:
            self.assertEqual(team.workflow("task", self.run, self.args), 0)
            self.assertEqual(execute.call_count, 2)
            self.assertIn("Verify empty input", execute.call_args_list[1].args[0])
            self.assertEqual(self.status(), "approved")

    def test_blocked_plan_never_executes(self):
        self.plan["blockers"] = ["Missing source"]
        with patch.object(team, "claude", return_value=self.plan), patch.object(team, "codex") as execute:
            self.assertEqual(team.workflow("task", self.run, self.args), 2)
            execute.assert_not_called()
            self.assertEqual(self.status(), "blocked")

    def test_round_limit_is_not_approval(self):
        fix = dict(verdict="changes_requested", summary="still broken", required_fixes=["fix"], evidence=[])
        with patch.object(team, "claude", side_effect=[self.plan, fix, fix]), \
                patch.object(team, "codex", return_value="implemented"):
            self.assertEqual(team.workflow("task", self.run, self.args), 2)
            self.assertEqual(self.status(), "needs_attention")

    def test_bad_schema_fails_closed(self):
        with self.assertRaises(ValueError):
            team.validate({"verdict": "approved"}, team.REVIEW)
        with self.assertRaises(ValueError):
            team.validate(dict(verdict="maybe", summary="", required_fixes=[], evidence=[]), team.REVIEW)


if __name__ == "__main__":
    unittest.main()
