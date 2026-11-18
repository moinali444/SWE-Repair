import json
import time
from pathlib import Path

from src.repair_agent import detect_and_repair
from src.buggy_examples import BUG_EXAMPLES


def main():
    results = []
    successful = 0

    print("=" * 55)
    print("       SWE-REPAIR: AUTOMATED PYTHON CODE REPAIR")
    print("=" * 55)

    for example in BUG_EXAMPLES:
        start = time.perf_counter()

        result = detect_and_repair(example["code"])

        elapsed = time.perf_counter() - start

        passed = (
            result["success"]
            and result["repaired_code"] == example["expected"]
        )

        successful += int(passed)

        record = {
            "bug_id": example["id"],
            "description": example["description"],
            "detected_repairs": result["repairs"],
            "syntax_valid": result["syntax_valid"],
            "test_passed": passed,
            "execution_time_seconds": round(elapsed, 6),
        }

        results.append(record)

        print(f"\n{example['id']}: {example['description']}")
        print("Status:", "SUCCESS" if passed else "FAILED")
        print("Repair:", result["repairs"])
        print("Time:", round(elapsed, 6), "seconds")

    accuracy = successful / len(BUG_EXAMPLES) * 100

    output = {
        "project": "SWE-Repair",
        "total_examples": len(BUG_EXAMPLES),
        "successful_repairs": successful,
        "failed_repairs": len(BUG_EXAMPLES) - successful,
        "repair_success_rate_percent": accuracy,
        "results": results,
    }

    Path("results/evaluation_results.json").write_text(
        json.dumps(output, indent=4),
        encoding="utf-8",
    )

    print("\n" + "=" * 55)
    print(f"Repair success rate: {accuracy:.2f}%")
    print("Results saved to results/evaluation_results.json")
    print("=" * 55)


if __name__ == "__main__":
    main()