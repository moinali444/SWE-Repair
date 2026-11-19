import json
from pathlib import Path
from datasets import load_dataset

data_dir = Path("data")

targets = {}
for filename in ["train.jsonl", "test.jsonl"]:
    with (data_dir / filename).open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                task = json.loads(line)
                targets[task["instance_id"]] = True

print("Selected task IDs:", len(targets))
print("Streaming original SWE-smith dataset...")

ds = load_dataset(
    "SWE-bench/SWE-smith-py",
    split="train",
    streaming=True
)

found = {}
for index, row in enumerate(ds, start=1):
    task_id = row["instance_id"]

    if task_id in targets:
        found[task_id] = row
        print(f"[{len(found)}/{len(targets)}] Found: {task_id}")

    if len(found) == len(targets):
        break

output = data_dir / "original_metadata.jsonl"
with output.open("w", encoding="utf-8") as f:
    for task_id in targets:
        if task_id in found:
            f.write(json.dumps(found[task_id], ensure_ascii=False) + "\n")

print("\nRecovery complete.")
print("Matched:", len(found), "/", len(targets))
print("Missing:", len(targets) - len(found))
print("Saved to:", output)
