import ast
from pathlib import Path


REPAIR_RULES = [
    {
        "name": "Assignment used instead of comparison",
        "buggy": "if n = 0:",
        "fixed": "if n == 0:",
    },
    {
        "name": "Incorrect final list index",
        "buggy": "return numbers[len(numbers)]",
        "fixed": "return numbers[len(numbers) - 1]",
    },
    {
        "name": "Incorrect addition operator",
        "buggy": "return a - b",
        "fixed": "return a + b",
    },
]


def detect_and_repair(code):
    repaired_code = code
    applied_repairs = []

    for rule in REPAIR_RULES:
        if rule["buggy"] in repaired_code:
            repaired_code = repaired_code.replace(
                rule["buggy"], rule["fixed"]
            )
            applied_repairs.append(rule["name"])

    try:
        ast.parse(repaired_code)
        syntax_valid = True
    except SyntaxError:
        syntax_valid = False

    return {
        "original_code": code,
        "repaired_code": repaired_code,
        "repairs": applied_repairs,
        "syntax_valid": syntax_valid,
        "success": bool(applied_repairs) and syntax_valid,
    }


def repair_file(input_path, output_path):
    code = Path(input_path).read_text(encoding="utf-8")
    result = detect_and_repair(code)

    if result["syntax_valid"]:
        Path(output_path).write_text(
            result["repaired_code"], encoding="utf-8"
        )

    return result