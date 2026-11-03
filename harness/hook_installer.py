"""Maxilun Git Pre-Commit Hook & CI Workflow Installer.

Automates continuous enforcement of Maxilun Purity Gate:
- Installs local .git/hooks/pre-commit to block AI slop before commit
- Generates GitHub Actions workflow for automated PR quality gating
"""
import os
import sys
from pathlib import Path
from typing import Optional

class HookInstaller:
    """Manages installation and removal of Git hooks and CI configurations."""

    HOOK_SCRIPT = """#!/usr/bin/env bash
# Maxilun Purity Gate Pre-Commit Hook
# Blocks AI slop, banned buzzwords, ceremonial theater, and security invariants.

echo "🌑 Running Maxilun Purity Gate on staged files..."

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\\.(ts|tsx|js|jsx|py|md|sql)$')

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

FAILED=0
for FILE in $STAGED_FILES; do
    if [ -f "$FILE" ]; then
        OUTPUT=$(python harness/cli.py check "$FILE" 2>&1)
        EXIT_CODE=$?
        if [ $EXIT_CODE -ne 0 ]; then
            echo ""
            echo "❌ Purity Gate violation detected in: $FILE"
            echo "$OUTPUT"
            FAILED=1
        fi
    fi
done

if [ $FAILED -ne 0 ]; then
    echo ""
    echo "⚠️  Commit aborted by Maxilun Purity Gate."
    echo "   Fix violations above, or run 'python harness/cli.py check <file>'."
    exit 1
fi

echo "✅ Maxilun Purity Gate passed for all staged files."
exit 0
"""

    CI_WORKFLOW = """name: Maxilun Purity & Benchmark Gate

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

      - name: Run Maxilun 18-Skill Test Suite
        run: python scripts/test-suite.py

      - name: Run Maxilun Benchmark Suite
        run: python harness/cli.py bench --json -o benchmark_report.json

      - name: Run Purity Gate on repository
        run: python harness/cli.py check .
"""

    @classmethod
    def install_git_hook(cls, repo_root: Optional[Path] = None) -> bool:
        root = repo_root or Path.cwd()
        git_dir = root / ".git"
        if not git_dir.exists():
            print(f"Error: '{root}' is not a Git repository (.git folder not found).", file=sys.stderr)
            return False

        hooks_dir = git_dir / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)
        hook_file = hooks_dir / "pre-commit"

        hook_file.write_text(cls.HOOK_SCRIPT, encoding="utf-8")

        # Set executable permission on Unix/macOS
        if sys.platform != "win32":
            try:
                os.chmod(hook_file, 0o755)
            except Exception:
                pass

        print(f"✅ Maxilun Git pre-commit hook installed to: {hook_file}")
        return True

    @classmethod
    def uninstall_git_hook(cls, repo_root: Optional[Path] = None) -> bool:
        root = repo_root or Path.cwd()
        hook_file = root / ".git" / "hooks" / "pre-commit"
        if hook_file.exists():
            hook_file.unlink()
            print(f"✅ Maxilun Git pre-commit hook removed: {hook_file}")
            return True
        else:
            print("Notice: No pre-commit hook found to remove.")
            return False

    @classmethod
    def generate_ci_workflow(cls, repo_root: Optional[Path] = None) -> bool:
        root = repo_root or Path.cwd()
        wf_dir = root / ".github" / "workflows"
        wf_dir.mkdir(parents=True, exist_ok=True)
        wf_file = wf_dir / "maxilun-harness.yml"

        wf_file.write_text(cls.CI_WORKFLOW, encoding="utf-8")
        print(f"✅ Maxilun CI workflow generated: {wf_file}")
        return True
