import argparse
import json
import subprocess
import sys
from pathlib import Path
from abc import ABC, abstractmethod

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

class RepairGenerator(ABC):
    """Common interface for automated repair generators."""

    @abstractmethod
    def generate(self, task):
        """Return a unified diff patch as text."""
        raise NotImplementedError


class PatchFileGenerator(RepairGenerator):
    """Uses an existing patch for evaluator pipeline testing."""

    def __init__(self, patch_path):
        self.patch_path = Path(patch_path)

    def generate(self, task):
        if not self.patch_path.exists():
            raise FileNotFoundError(self.patch_path)
        return self.patch_path.read_text(encoding="utf-8")


def load_task(task_id, split="test"):
    dataset = DATA / f"{split}_full.jsonl"

    with dataset.open(encoding="utf-8") as f:
        for line in f:
            task = json.loads(line)
            if task["instance_id"] == task_id:
                return task

    raise ValueError(f"Task not found: {task_id}")


def run_pipeline(task_id, generator, split="test"):
    task = load_task(task_id, split)

    patch_text = generator.generate(task)
    if not patch_text.strip():
        raise ValueError("Generator returned an empty patch.")

    candidate_path = DATA / "pipeline_candidate.patch"
    candidate_path.write_text(patch_text, encoding="utf-8", newline="\n")

    command = [
        sys.executable,
        str(ROOT / "evaluate_repair.py"),
        "--task-id", task_id,
        "--patch", str(candidate_path),
        "--split", split
    ]

    print("Task:", task_id)
    print("Generator:", generator.__class__.__name__)
    print("Patch saved:", candidate_path)
    print("Launching Docker evaluator...")

    return subprocess.run(command, cwd=ROOT).returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--patch", required=True)
    parser.add_argument("--split", choices=["train", "test"], default="test")
    args = parser.parse_args()

    generator = PatchFileGenerator(args.patch)
    exit_code = run_pipeline(args.task_id, generator, args.split)

    print("\nPipeline process exit code:", exit_code)


if __name__ == "__main__":
    main()

