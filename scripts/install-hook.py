#!/usr/bin/env python3
"""
Maxilun Pre-Commit Purity Hook Installer
=======================================

Installs a lightweight, deterministic git pre-commit hook that runs
the Maxilun UI Purity Gate on staged files before commit.

The hook pins the absolute path of this checkout's linter and of the Python
interpreter running this installer, so it works from any repository. If either
disappears later, the hook prints a note and lets the commit through.

An existing pre-commit hook that Maxilun did not write is never overwritten:
it is moved to ``pre-commit.pre-maxilun`` first.
"""

import os
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

MARKER = "# Maxilun-managed pre-commit hook"
LEGACY_MARKERS = (MARKER, "# Maxilun Pre-Commit Purity Gate", "# Maxilun Purity Gate Pre-Commit Hook")
LINTER = Path(__file__).resolve().parent / "ui-purity-linter.py"

HOOK_SCRIPT = r"""#!/bin/sh
# Maxilun-managed pre-commit hook
# Maxilun Pre-Commit Purity Gate: rejects commits containing AI design tells
# (gradients, emojis, uncalibrated hex) in staged UI files.

PY=@PYTHON@
LINTER=@LINTER@

if [ ! -x "$PY" ] && ! command -v "$PY" >/dev/null 2>&1; then
    echo "  Maxilun: Python not found at $PY, skipping pre-commit purity check."
    exit 0
fi
if [ ! -f "$LINTER" ]; then
    echo "  Maxilun: linter not found at $LINTER, skipping pre-commit purity check."
    echo "  Re-run scripts/install-hook.py from your Maxilun checkout to repair the hook."
    exit 0
fi

echo ""
echo "  Maxilun Pre-Commit Purity Gate running..."

git diff --cached --name-only --diff-filter=ACM | grep -E '\.(html|jsx|tsx|css|vue|svelte)$' | {
    while IFS= read -r file; do
        if [ -f "$file" ] && ! "$PY" "$LINTER" "$file"; then
            exit 1
        fi
    done
    exit 0
}
if [ $? -ne 0 ]; then
    echo ""
    echo "  Commit rejected: Maxilun UI Purity violations detected."
    echo "  Run '$PY $LINTER --fix <file>' to auto-remediate."
    echo "  Run 'git commit --no-verify' only in emergency overrides."
    echo ""
    exit 1
fi

echo "  Maxilun Pre-Commit Gate: zero AI design tells detected."
echo ""
exit 0
"""


def _sh_path(path: str) -> str:
    return shlex.quote(path.replace("\\", "/"))


def render_hook() -> str:
    return HOOK_SCRIPT.replace("@PYTHON@", _sh_path(sys.executable)).replace("@LINTER@", _sh_path(str(LINTER)))


def resolve_hooks_dir(root: Path) -> Path:
    """Return the hooks dir git actually uses (honours worktrees, core.hooksPath)."""
    out = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--git-path", "hooks"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    hooks_dir = Path(out)
    return hooks_dir if hooks_dir.is_absolute() else (root / hooks_dir).resolve()


def is_maxilun_hook(hook_file: Path) -> bool:
    try:
        lines = hook_file.read_text(encoding="utf-8", errors="replace").splitlines()
    except FileNotFoundError:
        return False
    return any(line.strip() in LEGACY_MARKERS for line in lines[:5])


def backup_foreign_hook(hook_file: Path) -> Path:
    backup = hook_file.with_name("pre-commit.pre-maxilun")
    if backup.exists():
        backup = hook_file.with_name(f"pre-commit.pre-maxilun-{time.strftime('%Y%m%d-%H%M%S')}")
    hook_file.rename(backup)
    return backup


def install_hook(repo_root: Optional[Path] = None) -> bool:
    root = (repo_root or Path.cwd()).resolve()
    try:
        hooks_dir = resolve_hooks_dir(root)
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"Error: '{root}' is not a usable git repository ({e}).", file=sys.stderr)
        return False

    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_file = hooks_dir / "pre-commit"
    if hook_file.exists() and not is_maxilun_hook(hook_file):
        backup = backup_foreign_hook(hook_file)
        print(f"Existing non-Maxilun pre-commit hook moved to: {backup}")

    hook_file.write_text(render_hook(), encoding="utf-8", newline="\n")
    os.chmod(hook_file, 0o755)
    print(f"Maxilun pre-commit purity hook installed in: {hook_file}")
    return True


if __name__ == "__main__":
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
    sys.exit(0 if install_hook(target) else 1)
