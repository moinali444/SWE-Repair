import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent

sys.path.insert(0, str(ROOT / "src"))

from qwen_adapter import QwenRepairAdapter
from patch_utils import validate_patch_text, save_patch


def load_task(task_id, split):
    dataset = ROOT / "data" / f"{split}_full.jsonl"

    if not dataset.exists():
        raise FileNotFoundError(dataset)

    with dataset.open(encoding="utf-8") as file:
        for line in file:
            task = json.loads(line)

            if task["instance_id"] == task_id:
                return task

    raise ValueError("Task not found: " + task_id)


def main():
    parser = argparse.ArgumentParser(
        description="Generate SWE-smith repairs using Qwen"
    )

    parser.add_argument("--task-id", required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--context", default="")
    parser.add_argument("--max-new-tokens", type=int, default=1200)

    args = parser.parse_args()

    task = load_task(args.task_id, args.split)

    context = ""

    if args.context:
        context_path = Path(args.context)

        if not context_path.exists():
            raise FileNotFoundError(context_path)

        context = context_path.read_text(encoding="utf-8")

    adapter = QwenRepairAdapter(
        max_new_tokens=args.max_new_tokens
    )

    print("Task:", task["instance_id"])
    print("Repository:", task["repo"])
    print("Model:", adapter.model_name)
    print("Generating candidate repair...")

    patch = adapter.generate(task, context)

    valid, message = validate_patch_text(patch)

    if not valid:
        raise SystemExit("Patch validation failed: " + message)

    safe_id = "".join(
        c if c.isalnum() or c in "-_." else "_"
        for c in args.task_id
    )

    output_path = ROOT / "data" / f"qwen_repair_{safe_id}.patch"

    save_patch(patch, output_path)

    metadata = {
        "task_id": task["instance_id"],
        "model": adapter.model_name,
        "candidate_type": "qwen_generated",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "patch_file": str(output_path),
        "basic_patch_validation": message,
        "model_inference_attempted": True,
        "test_evaluation_performed": False
    }

    metadata_path = ROOT / "results" / f"qwen_generation_{safe_id}.json"

    metadata_path.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8"
    )

    print("\n===== GENERATION COMPLETE =====")
    print("Patch:", output_path)
    print("Metadata:", metadata_path)
    print("Validation:", message)


if __name__ == "__main__":
    main()
