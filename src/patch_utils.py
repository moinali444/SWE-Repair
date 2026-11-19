import subprocess
import tempfile
from pathlib import Path

def validate_patch_text(patch):
    if not patch or not patch.strip():
        return False, "Empty patch"

    if "diff --git " not in patch:
        return False, "Missing Git diff header"

    if not ("@@ " in patch or "@@ -" in patch):
        return False, "Missing unified diff hunk"

    if "\x00" in patch:
        return False, "Null byte detected"

    return True, "Basic patch structure valid"


def validate_patch_with_git(patch):
    valid, message = validate_patch_text(patch)

    if not valid:
        return False, message

    with tempfile.TemporaryDirectory() as directory:
        patch_file = Path(directory) / "candidate.patch"
        patch_file.write_text(patch, encoding="utf-8", newline="\n")

        result = subprocess.run(
            ["git", "apply", "--stat", str(patch_file)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return False, result.stderr.strip()

        return True, "Git accepted patch format"


def save_patch(patch, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)

    destination.write_text(
        patch,
        encoding="utf-8",
        newline="\n"
    )

    return destination
