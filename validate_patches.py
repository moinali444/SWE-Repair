
import json
from pathlib import Path

def validate(path):
    total = 0
    valid = 0
    invalid = []

    with open(path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, 1):
            if not line.strip():
                continue

            total += 1
            record = json.loads(line)
            patch = record.get("output", "")

            if "diff --git " in patch and "--- " in patch and "+++ " in patch:
                valid += 1
            else:
                invalid.append(line_number)

    print(f"\nFile: {path}")
    print("Total patches:", total)
    print("Valid diff patches:", valid)
    print("Invalid patches:", len(invalid))

    if invalid:
        print("Invalid line numbers:", invalid[:10])

validate("data/train.jsonl")
validate("data/test.jsonl")
