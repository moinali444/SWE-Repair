import json
from pathlib import Path

data = Path("data")

metadata = {}
with (data / "original_metadata.jsonl").open(encoding="utf-8") as f:
    for line in f:
        if line.strip():
            row = json.loads(line)
            metadata[row["instance_id"]] = row

for split in ["train", "test"]:
    source = data / f"{split}.jsonl"
    output = data / f"{split}_full.jsonl"

    count = 0
    with source.open(encoding="utf-8") as fin, output.open("w", encoding="utf-8") as fout:
        for line in fin:
            if not line.strip():
                continue

            task = json.loads(line)
            original = metadata.get(task["instance_id"])

            if original is None:
                raise ValueError(f"Missing metadata: {task['instance_id']}")

            task.update({
                "repo": original["repo"],
                "image_name": original["image_name"],
                "FAIL_TO_PASS": original["FAIL_TO_PASS"],
                "PASS_TO_PASS": original["PASS_TO_PASS"]
            })

            fout.write(json.dumps(task, ensure_ascii=False) + "\n")
            count += 1

    print(f"{split}: {count} complete records -> {output}")

print("\nUnique repositories:", len({r["repo"] for r in metadata.values()}))
print("Unique Docker images:", len({r["image_name"] for r in metadata.values()}))
print("All selected records enriched successfully.")
