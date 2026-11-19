
import json
from pathlib import Path

train_path = Path("data/train.jsonl")
test_path = Path("data/test.jsonl")

def load_data(path):
    with path.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]

train_data = load_data(train_path)
test_data = load_data(test_path)

print("========== SWE-REPAIR DATASET REPORT ==========")
print("Training examples:", len(train_data))
print("Testing examples:", len(test_data))

print("\nTraining data checks:")
print("Missing instructions:", sum(not x.get("instruction") for x in train_data))
print("Missing inputs:", sum(not x.get("input") for x in train_data))
print("Missing patches:", sum(not x.get("output") for x in train_data))

print("\nTesting data checks:")
print("Missing inputs:", sum(not x.get("input") for x in test_data))
print("Missing patches:", sum(not x.get("output") for x in test_data))

print("\nSample task:")
print("ID:", train_data[0]["instance_id"])
print("Repository:", train_data[0]["input"].splitlines()[0])
print("Patch length:", len(train_data[0]["output"]))

print("\nDataset inspection completed.")
