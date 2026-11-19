import argparse
import json
import shlex
import subprocess
import time
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"

def main():
    parser = argparse.ArgumentParser(description="SWE-smith Docker repair evaluator")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--patch", required=True)
    parser.add_argument("--split", choices=["train", "test"], default="test")
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()

    dataset = DATA / f"{args.split}_full.jsonl"
    patch_source = Path(args.patch).resolve()

    if not dataset.exists() or not patch_source.exists():
        raise SystemExit("Dataset or candidate patch file not found.")

    task = None
    with dataset.open(encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            if item["instance_id"] == args.task_id:
                task = item
                break

    if task is None:
        raise SystemExit("Task ID not found.")

    tests = task.get("FAIL_TO_PASS", [])
    if not tests:
        raise SystemExit("No FAIL_TO_PASS tests found.")

    image = task["image_name"]
    bug_patch = DATA / "bug_injection_patch.patch"
    candidate = DATA / "candidate_patch.patch"

    bug_patch.write_text(task["output"], encoding="utf-8", newline="\n")
    candidate.write_bytes(patch_source.read_bytes())

    test_command = " ".join(shlex.quote(t) for t in tests)

    script = (
        "cd /testbed || exit 90; "
        "python -m pip install -q pytest beautifulsoup4 || exit 91; "
        "echo BUG_PATCH_CHECK; "
        "git apply --check /swe-data/bug_injection_patch.patch || exit 10; "
        "git apply /swe-data/bug_injection_patch.patch || exit 11; "
        "echo BUG_PATCH_APPLIED; "
        "echo REPAIR_PATCH_CHECK; "
        "git apply --check /swe-data/candidate_patch.patch || exit 20; "
        "git apply /swe-data/candidate_patch.patch || exit 21; "
        "echo REPAIR_PATCH_APPLIED; "
        "echo TESTS_STARTED; "
        "python -m pytest -v " + test_command + "; "
        "code=$?; echo PYTEST_EXIT_CODE=$code; exit $code"
    )

    command = [
        "docker", "run", "--rm",
        "--mount", f"type=bind,source={DATA},target=/swe-data,readonly",
        "--entrypoint", "bash", image, "-lc", script
    ]

    print("Task:", task["instance_id"])
    print("Starting bug injection, repair application, and test evaluation...")

    start = time.perf_counter()
    try:
        run = subprocess.run(
            command, capture_output=True, text=True, timeout=args.timeout
        )
        elapsed = round(time.perf_counter() - start, 3)
        output = run.stdout + "\n" + run.stderr
        code = run.returncode

        if "REPAIR_PATCH_CHECK" not in output:
            status = "bug_patch_or_setup_error"
        elif "TESTS_STARTED" not in output:
            status = "repair_patch_not_applicable"
        elif code == 0:
            status = "passed"
        else:
            status = "tests_failed"

    except subprocess.TimeoutExpired as exc:
        elapsed = round(time.perf_counter() - start, 3)
        output = str(exc)
        code = None
        status = "timeout"

    result = {
        "task_id": task["instance_id"],
        "repository": task["repo"],
        "docker_image": image,
        "required_tests": tests,
        "candidate_patch": str(patch_source),
        "status": status,
        "docker_exit_code": code,
        "execution_time_seconds": elapsed,
        "evaluated_at_utc": datetime.now(timezone.utc).isoformat(),
        "model_generated": False,
        "output": output[-20000:]
    }

    RESULTS.mkdir(exist_ok=True)
    safe_id = "".join(c if c.isalnum() or c in "-_." else "_" for c in args.task_id)
    result_path = RESULTS / f"repair_eval_{safe_id}.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("\n===== REPAIR EVALUATION =====")
    print("Status:", status)
    print("Docker exit code:", code)
    print("Execution time:", elapsed, "seconds")
    print("Saved:", result_path)
    print(output[-10000:])

if __name__ == "__main__":
    main()
