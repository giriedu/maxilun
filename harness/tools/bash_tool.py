"""Maxilun Native Bash & Command Execution Tool.

Executes shell commands with strict timeouts and output capture.
Zero external dependencies.
"""

import subprocess
import time
from typing import Dict, Any


class BashTool:
    """Executes safe commands in local terminal environment."""

    @staticmethod
    def execute(command: str, timeout: int = 30) -> Dict[str, Any]:
        t0 = time.time()
        try:
            proc = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            duration_ms = (time.time() - t0) * 1000
            return {
                "command": command,
                "exit_code": proc.returncode,
                "stdout": proc.stdout[-5000:],  # cap output
                "stderr": proc.stderr[-5000:],
                "duration_ms": round(duration_ms, 2)
            }
        except subprocess.TimeoutExpired:
            duration_ms = (time.time() - t0) * 1000
            return {
                "command": command,
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds.",
                "duration_ms": round(duration_ms, 2)
            }
        except Exception as e:
            duration_ms = (time.time() - t0) * 1000
            return {
                "command": command,
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Command execution failed: {str(e)}",
                "duration_ms": round(duration_ms, 2)
            }
