
import json
import subprocess
from pathlib import Path

DATA_FILE = Path("data/test.jsonl")
RESULT_FILE = Path("results/dataset_evaluation.json")

def run_git(repo_path, *args):
    return subprocess.run(
        ["git", "-C", str(repo_path), *args],
        capture_output=True,
        text=True
    )

def main():
    results = []

    with DATA_FILE.open(encoding="utf-8") as file:
        tasks = [json.loads(line) for line in file if line.strip()]

    for index, task in enumerate(tasks, start=1):
        instance_id = task.get("instance_id", "unknown")
        patch = task.get("output", "")

        # Check patch format
        valid_format = (
            patch.startswith("diff --git ")
            and "+++ " in patch
            and "--- " in patch
        )

        results.append({
            "instance_id": instance_id,
            "valid_patch_format": valid_format,
            "repository": "Not yet cloned",
            "patch_applicable": None,
            "status": "format_valid" if valid_format else "invalid_format"
        })

        print(
            f"[{index}/{len(tasks)}] {instance_id}: "
            f"{'Valid format' if valid_format else 'Invalid format'}"
        )

    RESULT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with RESULT_FILE.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    valid_count = sum(r["valid_patch_format"] for r in results)

    print("\nDataset evaluation summary")
    print("--------------------------")
    print("Total tasks:", len(results))
    print("Valid patch formats:", valid_count)
    print("Invalid patch formats:", len(results) - valid_count)
    print("Repository application: Not evaluated yet")
    print("Results saved to:", RESULT_FILE)

if __name__ == "__main__":
    main()
