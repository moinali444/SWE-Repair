import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.repair_agent import detect_and_repair
from src.buggy_examples import BUG_EXAMPLES


def test_all_repairs():
    for example in BUG_EXAMPLES:
        result = detect_and_repair(example["code"])

        assert result["success"], example["id"]
        assert result["syntax_valid"], example["id"]
        assert result["repaired_code"] == example["expected"], example["id"]


def test_unmodified_code():
    code = "def multiply(a, b):\n    return a * b"

    result = detect_and_repair(code)

    assert result["repaired_code"] == code
    assert result["repairs"] == []