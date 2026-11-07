#!/usr/bin/env python3
"""
Maxilun Pre-Commit Purity Hook Installer
=======================================

Installs a lightweight, deterministic git pre-commit hook that runs
the Maxilun UI Purity Gate on staged files before commit.
"""

import os
import sys
from pathlib import Path
from typing import Optional


HOOK_SCRIPT = """#!/bin/sh
# Maxilun Pre-Commit Purity Gate
# Rejects commits containing AI design tells (gradients, emojis, uncalibrated hex)

echo ""
echo "  🔒 Maxilun Pre-Commit Purity Gate running..."

if command -v python3 >/dev/null 2>&1; then
    PY_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PY_CMD="python"
elif command -v py >/dev/null 2>&1; then
    PY_CMD="py"
else
    echo "  ⚠️ Python not found, skipping Maxilun pre-commit check."
    exit 0
fi

# Audit staged UI surface files
STATUS=0
STAGED_UI=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(html|jsx|tsx|css|vue|svelte)$')
if [ -n "$STAGED_UI" ]; then
    for file in $STAGED_UI; do
        if [ -f "$file" ]; then
            $PY_CMD scripts/ui-purity-linter.py "$file"
            if [ $? -ne 0 ]; then
                STATUS=1
                break
            fi
        fi
    done
fi
if [ $STATUS -ne 0 ]; then
    echo ""
    echo "  ❌ Commit rejected: Maxilun UI Purity violations detected."
    echo "  👉 Run 'python scripts/ui-purity-linter.py --fix' to auto-remediate."
    echo "  👉 Run 'git commit --no-verify' only in emergency overrides."
    echo ""
    exit 1
fi

echo "  ✅ Maxilun Pre-Commit Gate: Zero AI design tells detected."
echo ""
exit 0
"""


def install_hook(repo_root: Optional[Path] = None) -> bool:
    root = repo_root or Path(__file__).resolve().parent.parent
    git_dir = root / ".git"

    if not git_dir.is_dir():
        print(f"Error: No .git directory found at '{root}'. Run 'git init' first.", file=sys.stderr)
        return False

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_file = hooks_dir / "pre-commit"

    try:
        hook_file.write_text(HOOK_SCRIPT, encoding="utf-8")
        # Chmod +x on platforms supporting chmod
        try:
            current_mode = hook_file.stat().st_mode
            hook_file.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        except Exception:
            pass

        print(f"✅ Maxilun pre-commit purity hook installed successfully in: {hook_file}")
        return True
    except Exception as e:
        print(f"❌ Failed to install pre-commit hook: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
    success = install_hook(target)
    sys.exit(0 if success else 1)
