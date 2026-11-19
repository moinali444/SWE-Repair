import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from qwen_adapter import QwenRepairAdapter
from patch_utils import validate_patch_text


class RepairComponentTests(unittest.TestCase):

    def test_prompt_generation(self):
        adapter = QwenRepairAdapter()

        task = {
            "repo": "example/project",
            "problem_statement": "Fix a version parsing bug.",
            "FAIL_TO_PASS": ["tests/test_version.py"]
        }

        prompt = adapter.build_prompt(task)

        self.assertIn("version parsing bug", prompt)
        self.assertIn("tests/test_version.py", prompt)
        self.assertIn("unified Git diff", prompt)

    def test_empty_patch_rejected(self):
        valid, message = validate_patch_text("")

        self.assertFalse(valid)

    def test_missing_git_header_rejected(self):
        valid, message = validate_patch_text("@@ -1 +1 @@")

        self.assertFalse(valid)

    def test_valid_diff_header(self):
        patch = (
            "diff --git a/example.py b/example.py\n"
            "--- a/example.py\n"
            "+++ b/example.py\n"
            "@@ -1 +1 @@\n"
            "-old\n"
            "+new\n"
        )

        valid, message = validate_patch_text(patch)

        self.assertTrue(valid)


if __name__ == "__main__":
    unittest.main()
