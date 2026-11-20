"""Maxilun Native Bash & Command Execution Tool.

Executes shell commands in the workspace root with clamped timeouts and output capture.
Zero external dependencies.
"""

import subprocess
import time
from pathlib import Path
from typing import Dict, Any, Optional

MAX_TIMEOUT = 600


class BashTool:
    """Executes commands in the workspace root."""

    def __init__(self, root: Optional[Path] = None):
        self.root = Path(root or Path.cwd()).resolve()

    def execute(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        # Model-supplied timeouts are clamped so one call cannot hang the loop indefinitely.
        try:
            timeout = max(1, min(int(timeout), MAX_TIMEOUT))
        except (TypeError, ValueError):
            timeout = 30
        t0 = time.time()
        try:
            proc = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout, cwd=self.root)
            return {
                "command": command,
                "exit_code": proc.returncode,
                "stdout": proc.stdout[-5000:],
                "stderr": proc.stderr[-5000:],
                "duration_ms": round((time.time() - t0) * 1000, 2)
            }
        except subprocess.TimeoutExpired:
            stderr = f"Command timed out after {timeout} seconds."
        except Exception as e:
            stderr = f"Command execution failed: {str(e)}"
        return {
            "command": command,
            "exit_code": -1,
            "stdout": "",
            "stderr": stderr,
            "duration_ms": round((time.time() - t0) * 1000, 2)
        }
