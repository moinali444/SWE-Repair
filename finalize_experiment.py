import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"
REPORTS = ROOT / "reports"

RESULTS.mkdir(exist_ok=True)
REPORTS.mkdir(exist_ok=True)


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"WARNING: Could not read {path.name}: {exc}")
        return None


def load_jsonl(path):
    records = []
    if not path.exists():
        return records

    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    print("WARNING: Invalid JSON line in", path.name)

    return records


def dataset_statistics():
    train = load_jsonl(DATA / "train_full.jsonl")
    test = load_jsonl(DATA / "test_full.jsonl")

    train_repos = {
        x.get("repo") for x in train if x.get("repo")
    }
    test_repos = {
        x.get("repo") for x in test if x.get("repo")
    }

    overlap = train_repos.intersection(test_repos)

    return {
        "train_records": len(train),
        "test_records": len(test),
        "total_records": len(train) + len(test),
        "train_repositories": len(train_repos),
        "test_repositories": len(test_repos),
        "repository_overlap_count": len(overlap),
        "repository_overlap": sorted(overlap),
        "repository_disjoint_split": len(overlap) == 0,
        "train_file_exists": (DATA / "train_full.jsonl").exists(),
        "test_file_exists": (DATA / "test_full.jsonl").exists()
    }


def patch_statistics():
    report = {}

    for name in ["train_full.jsonl", "test_full.jsonl"]:
        records = load_jsonl(DATA / name)
        valid = 0
        invalid = 0

        for record in records:
            patch = record.get("output", "")

            if (
                isinstance(patch, str)
                and "diff --git " in patch
                and ("@@ " in patch or "@@ -" in patch)
            ):
                valid += 1
            else:
                invalid += 1

        report[name] = {
            "total": len(records),
            "basic_diff_structure_valid": valid,
            "invalid": invalid
        }

    return report


def collect_experiments():
    experiments = []

    for path in sorted(RESULTS.glob("repair_eval_*.json")):
        data = load_json(path)

        if data:
            experiments.append({
                "file": path.name,
                "task_id": data.get("task_id", data.get("instance_id")),
                "status": data.get("status"),
                "candidate_type": data.get("candidate_type", "unspecified"),
                "tests_passed": data.get("tests_passed"),
                "tests_failed": data.get("tests_failed"),
                "execution_time_seconds": data.get(
                    "execution_time_seconds"
                ),
                "model_generated": data.get("model_generated", False),
                "pass_at_1_model_result": data.get(
                    "pass_at_1_model_result"
                ),
                "evaluation_interpretation": data.get(
                    "evaluation_interpretation", ""
                )
            })

    return experiments


def project_file_audit():
    required = [
        "main.py",
        "README.md",
        "evaluate_repair.py",
        "generate_repair.py",
        "src/repair_agent.py",
        "src/repair_pipeline.py",
        "src/qwen_adapter.py",
        "src/patch_utils.py",
        "data/train_full.jsonl",
        "data/test_full.jsonl",
        "results/benchmark_validation.json"
    ]

    return {
        item: (ROOT / item).exists()
        for item in required
    }


def main():
    dataset = dataset_statistics()
    patches = patch_statistics()
    experiments = collect_experiments()
    files = project_file_audit()

    benchmark = load_json(RESULTS / "benchmark_validation.json")

    audit = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project": "SWE-Repair",
        "dataset": dataset,
        "patch_validation": patches,
        "experiments": experiments,
        "benchmark_validation": benchmark,
        "required_files": files,
        "model_inference_completed": False,
        "lora_training_completed": False,
        "ai_generated_benchmark_score_available": False,
        "notes": [
            "SWE-smith output patches represent injected bug changes.",
            "The inverse patch experiment is an oracle/reference validation.",
            "The oracle experiment is not an AI-generated repair.",
            "Qwen adapter code has been created and unit-tested.",
            "Actual Qwen inference and LoRA training remain pending.",
            "Patch structure validation does not prove patch correctness."
        ]
    }

    audit_path = RESULTS / "final_project_audit.json"

    audit_path.write_text(
        json.dumps(audit, indent=2),
        encoding="utf-8"
    )

    lines = [
        "# SWE-Repair — Experimental Results and Project Audit",
        "",
        f"Generated: {audit['generated_at']}",
        "",
        "## 1. Dataset",
        "",
        f"- Training records: {dataset['train_records']}",
        f"- Testing records: {dataset['test_records']}",
        f"- Total records: {dataset['total_records']}",
        f"- Training repositories: {dataset['train_repositories']}",
        f"- Testing repositories: {dataset['test_repositories']}",
        f"- Repository overlap: {dataset['repository_overlap_count']}",
        f"- Repository-disjoint split: {dataset['repository_disjoint_split']}",
        "",
        "## 2. Patch format validation",
        ""
    ]

    for filename, stats in patches.items():
        lines.extend([
            f"### {filename}",
            f"- Total: {stats['total']}",
            f"- Basic diff structure valid: {stats['basic_diff_structure_valid']}",
            f"- Invalid: {stats['invalid']}",
            ""
        ])

    lines.extend([
        "## 3. Docker benchmark validation",
        ""
    ])

    if benchmark:
        lines.extend([
            f"- Task: {benchmark.get('task_id', 'Not recorded')}",
            f"- Clean baseline: {benchmark.get('clean_baseline', {})}",
            f"- Bug-patched execution: {benchmark.get('after_dataset_bug_patch', {})}",
            "- Interpretation: The injected bug reproduced the expected test failures.",
            ""
        ])
    else:
        lines.extend([
            "- Benchmark validation JSON not found.",
            ""
        ])

    lines.extend([
        "## 4. Repair experiments",
        ""
    ])

    if experiments:
        for exp in experiments:
            lines.extend([
                f"### {exp['file']}",
                f"- Task: {exp['task_id']}",
                f"- Status: {exp['status']}",
                f"- Candidate type: {exp['candidate_type']}",
                f"- Tests passed: {exp['tests_passed']}",
                f"- Tests failed: {exp['tests_failed']}",
                f"- Model generated: {exp['model_generated']}",
                f"- Model Pass@1: {exp['pass_at_1_model_result']}",
                f"- Interpretation: {exp['evaluation_interpretation']}",
                ""
            ])
    else:
        lines.extend(["No repair evaluation JSON files found.", ""])

    lines.extend([
        "## 5. AI model status",
        "",
        "- Qwen adapter implementation: created and unit-tested.",
        "- Actual Qwen inference: not completed.",
        "- LoRA fine-tuning: not completed.",
        "- AI-generated benchmark Pass@1: not available.",
        "",
        "## 6. Required project files",
        ""
    ])

    for filename, exists in files.items():
        lines.append(
            f"- [{'x' if exists else ' '}] `{filename}`"
        )

    lines.extend([
        "",
        "## 7. Limitations",
        "",
        "The current validated repair experiment uses an oracle inverse "
        "of the SWE-smith injected bug patch. It demonstrates that the "
        "Docker-based evaluation pipeline can reproduce failures and "
        "verify a repair. It is not a Qwen-generated result.",
        "",
        "The Qwen adapter is an implementation interface. Model weights "
        "have not been loaded, inference has not been completed, and "
        "LoRA training has not been performed.",
        "",
        "Patch-format checks verify basic unified-diff structure only. "
        "They do not establish semantic correctness.",
        "",
        "## 8. Conclusion",
        "",
        "The project has a prepared SWE-smith dataset, repository-based "
        "train/test separation, patch validation, Docker-based bug "
        "reproduction, an automated repair evaluator, an oracle repair "
        "validation experiment, and a tested Qwen adapter interface.",
        "Actual AI-model training and benchmark evaluation remain future work.",
        ""
    ])

    report_path = REPORTS / "experimental_results.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")

    print("\n========== PROJECT AUDIT ==========")
    print("Dataset records:", dataset["total_records"])
    print("Train:", dataset["train_records"])
    print("Test:", dataset["test_records"])
    print("Repository overlap:", dataset["repository_overlap_count"])
    print("Repair experiments:", len(experiments))
    print("Model inference: NOT COMPLETED")
    print("LoRA training: NOT COMPLETED")

    print("\nRequired files:")
    for filename, exists in files.items():
        print(("OK  " if exists else "MISSING  ") + filename)

    print("\nCreated:")
    print(audit_path)
    print(report_path)


if __name__ == "__main__":
    main()
