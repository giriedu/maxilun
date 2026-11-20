"""Maxilun Git Pre-Commit Hook & CI Workflow Installer.

Automates continuous enforcement of Maxilun Purity Gate:
- Installs a pre-commit hook (in the hooks dir git actually uses) to block AI slop before commit.
  The hook pins this checkout's harness CLI and Python interpreter by absolute path and
  skips with a note if either goes missing. A foreign pre-commit hook is backed up, never
  overwritten or deleted.
- Generates a GitHub Actions workflow for automated PR quality gating. Steps are only emitted
  for Maxilun files present in the target repository (the full workflow targets the Maxilun repo).
"""
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

HARNESS_CLI = Path(__file__).resolve().parent / "cli.py"


class HookInstaller:
    """Manages installation and removal of Git hooks and CI configurations."""

    MARKER = "# Maxilun-managed pre-commit hook"
    LEGACY_MARKERS = (MARKER, "# Maxilun Purity Gate Pre-Commit Hook", "# Maxilun Pre-Commit Purity Gate")
    BACKUP_NAME = "pre-commit.pre-maxilun"

    HOOK_SCRIPT = r"""#!/bin/sh
# Maxilun-managed pre-commit hook
# Maxilun Purity Gate: blocks AI slop, banned buzzwords, ceremonial theater, and security invariants.

PY=@PYTHON@
CLI=@CLI@

if [ ! -x "$PY" ] && ! command -v "$PY" >/dev/null 2>&1; then
    echo "Maxilun: Python not found at $PY, skipping Purity Gate."
    exit 0
fi
if [ ! -f "$CLI" ]; then
    echo "Maxilun: harness CLI not found at $CLI, skipping Purity Gate."
    echo "Re-run 'python harness/cli.py install-hook' from your Maxilun checkout to repair the hook."
    exit 0
fi

echo "Running Maxilun Purity Gate on staged files..."

git diff --cached --name-only --diff-filter=ACM | grep -E '\.(ts|tsx|js|jsx|py|md|sql)$' | {
    FAILED=0
    while IFS= read -r FILE; do
        [ -f "$FILE" ] || continue
        if ! OUTPUT=$("$PY" "$CLI" check "$FILE" 2>&1); then
            echo ""
            echo "Purity Gate violation detected in: $FILE"
            echo "$OUTPUT"
            FAILED=1
        fi
    done
    exit $FAILED
}
if [ $? -ne 0 ]; then
    echo ""
    echo "Commit aborted by Maxilun Purity Gate."
    echo "Fix violations above, or run '$PY $CLI check <file>'."
    exit 1
fi

echo "Maxilun Purity Gate passed for all staged files."
exit 0
"""

    # (file that must exist in the target repo, workflow step)
    CI_STEPS = (
        ("scripts/test-suite.py", """      - name: Run Maxilun Test Suite
        run: python scripts/test-suite.py
"""),
        ("harness/cli.py", """      - name: Run Maxilun Benchmark Suite
        run: python harness/cli.py bench --json -o benchmark_report.json

      - name: Run Purity Gate on repository
        run: python harness/cli.py check .
"""),
    )

    CI_HEADER = """name: Maxilun Purity & Benchmark Gate

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  purity-gate:
    name: Maxilun Engineering Verification
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
"""

    @staticmethod
    def _sh_path(path: str) -> str:
        return shlex.quote(path.replace("\\", "/"))

    @classmethod
    def render_hook(cls) -> str:
        return (cls.HOOK_SCRIPT
                .replace("@PYTHON@", cls._sh_path(sys.executable))
                .replace("@CLI@", cls._sh_path(str(HARNESS_CLI))))

    @staticmethod
    def resolve_hooks_dir(root: Path) -> Path:
        """Return the hooks dir git actually uses (honours worktrees, core.hooksPath)."""
        out = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--git-path", "hooks"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        hooks_dir = Path(out)
        return hooks_dir if hooks_dir.is_absolute() else (root / hooks_dir).resolve()

    @classmethod
    def is_maxilun_hook(cls, hook_file: Path) -> bool:
        lines = hook_file.read_text(encoding="utf-8", errors="replace").splitlines()
        return any(line.strip() in cls.LEGACY_MARKERS for line in lines[:5])

    @classmethod
    def _hook_file(cls, repo_root: Optional[Path]) -> Optional[Path]:
        root = (repo_root or Path.cwd()).resolve()
        try:
            return cls.resolve_hooks_dir(root) / "pre-commit"
        except (OSError, subprocess.CalledProcessError) as e:
            print(f"Error: '{root}' is not a usable Git repository ({e}).", file=sys.stderr)
            return None

    @classmethod
    def install_git_hook(cls, repo_root: Optional[Path] = None) -> bool:
        hook_file = cls._hook_file(repo_root)
        if hook_file is None:
            return False
        hook_file.parent.mkdir(parents=True, exist_ok=True)

        if hook_file.exists() and not cls.is_maxilun_hook(hook_file):
            backup = hook_file.with_name(cls.BACKUP_NAME)
            if backup.exists():
                backup = hook_file.with_name(f"{cls.BACKUP_NAME}-{time.strftime('%Y%m%d-%H%M%S')}")
            hook_file.rename(backup)
            print(f"Existing non-Maxilun pre-commit hook moved to: {backup}")

        hook_file.write_text(cls.render_hook(), encoding="utf-8", newline="\n")
        os.chmod(hook_file, 0o755)
        print(f"✅ Maxilun Git pre-commit hook installed to: {hook_file}")
        return True

    @classmethod
    def uninstall_git_hook(cls, repo_root: Optional[Path] = None) -> bool:
        hook_file = cls._hook_file(repo_root)
        if hook_file is None:
            return False
        if not hook_file.exists():
            print("Notice: No pre-commit hook found to remove.")
            return False
        if not cls.is_maxilun_hook(hook_file):
            print(f"Notice: {hook_file} was not installed by Maxilun; leaving it untouched.")
            return False

        hook_file.unlink()
        print(f"✅ Maxilun Git pre-commit hook removed: {hook_file}")
        backup = hook_file.with_name(cls.BACKUP_NAME)
        if backup.exists():
            backup.rename(hook_file)
            print(f"Restored previous pre-commit hook from: {backup}")
        return True

    @classmethod
    def generate_ci_workflow(cls, repo_root: Optional[Path] = None) -> bool:
        root = (repo_root or Path.cwd()).resolve()
        steps = [step for required, step in cls.CI_STEPS if (root / required).is_file()]
        if not steps:
            print(
                f"Error: '{root}' contains none of the Maxilun files the workflow runs "
                f"({', '.join(r for r, _ in cls.CI_STEPS)}). generate-ci targets the Maxilun repository.",
                file=sys.stderr,
            )
            return False

        wf_dir = root / ".github" / "workflows"
        wf_dir.mkdir(parents=True, exist_ok=True)
        wf_file = wf_dir / "maxilun-harness.yml"
        wf_file.write_text(cls.CI_HEADER + "\n" + "\n".join(steps), encoding="utf-8")
        print(f"✅ Maxilun CI workflow generated: {wf_file}")
        return True
