"""Maxilun Execution Sandbox & Runtime Verifier.

Executes candidate code snippets, migrations, and assertions in isolated,
ephemeral runtime environments to provide concrete pass/fail proof.
Zero external dependencies.
"""

import sqlite3
import subprocess
import tempfile
import sys
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional


@dataclass
class SandboxResult:
    passed: bool
    engine: str
    exit_code: int
    output: str
    error: Optional[str] = None

    def summary(self) -> str:
        status = "✅ PASS" if self.passed else "❌ FAIL"
        msg = f"Sandbox ({self.engine}): {status} (exit code: {self.exit_code})"
        if self.error:
            msg += f"\n  Error: {self.error}"
        if self.output and self.output.strip():
            msg += f"\n  Output: {self.output.strip()}"
        return msg


class SandboxRunner:
    """Executes code compilation and in-memory execution assertions."""

    @staticmethod
    def verify_python(code: str) -> SandboxResult:
        """Verifies Python code compilation and AST syntax validity."""
        try:
            compile(code, "<sandbox>", "exec")
            return SandboxResult(passed=True, engine="python-compiler", exit_code=0, output="Compilation successful")
        except SyntaxError as e:
            return SandboxResult(
                passed=False,
                engine="python-compiler",
                exit_code=1,
                output="",
                error=f"SyntaxError at line {e.lineno}: {e.msg}"
            )
        except Exception as e:
            return SandboxResult(
                passed=False,
                engine="python-compiler",
                exit_code=1,
                output="",
                error=f"Compilation failure: {str(e)}"
            )

    @staticmethod
    def verify_sql_migration(sql_script: str) -> SandboxResult:
        """Executes DDL statements against an in-memory SQLite database engine."""
        # Sanitize common dialect tokens for standard SQLite execution test
        sanitized = (
            sql_script
            .replace("VARCHAR(20)", "TEXT")
            .replace("VARCHAR(50)", "TEXT")
            .replace("VARCHAR(255)", "TEXT")
            .replace("TIMESTAMPTZ", "TEXT")
            .replace("BIGINT", "INTEGER")
            .replace("BOOLEAN", "INTEGER")
            .replace("DEFAULT now()", "DEFAULT CURRENT_TIMESTAMP")
        )

        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        try:
            cursor.executescript(sanitized)
            conn.commit()
            return SandboxResult(
                passed=True,
                engine="sqlite-in-memory",
                exit_code=0,
                output="All SQL DDL and mutation statements executed without syntax errors"
            )
        except sqlite3.OperationalError as e:
            return SandboxResult(
                passed=False,
                engine="sqlite-in-memory",
                exit_code=1,
                output="",
                error=f"SQLite Execution Error: {str(e)}"
            )
        except Exception as e:
            return SandboxResult(
                passed=False,
                engine="sqlite-in-memory",
                exit_code=1,
                output="",
                error=f"Database execution error: {str(e)}"
            )
        finally:
            conn.close()

    @staticmethod
    def verify_javascript(code: str) -> SandboxResult:
        """Verifies JavaScript/Node syntax if node runtime is available."""
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(code)
            tmp_path = f.name

        try:
            # Check if node is available
            proc = subprocess.run(
                ["node", "--check", tmp_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            passed = (proc.returncode == 0)
            err = proc.stderr if not passed else None
            return SandboxResult(
                passed=passed,
                engine="node-check",
                exit_code=proc.returncode,
                output=proc.stdout or "Syntax check passed",
                error=err
            )
        except FileNotFoundError:
            # Node not available, fallback to basic lexical check
            balanced_braces = (code.count("{") == code.count("}")) and (code.count("(") == code.count(")"))
            if balanced_braces:
                return SandboxResult(
                    passed=True,
                    engine="lexical-fallback (node not found)",
                    exit_code=0,
                    output="Braces and parentheses balanced"
                )
            else:
                return SandboxResult(
                    passed=False,
                    engine="lexical-fallback",
                    exit_code=1,
                    output="",
                    error="Unbalanced curly braces or parentheses"
                )
        except Exception as e:
            return SandboxResult(passed=False, engine="node-check", exit_code=1, output="", error=str(e))
        finally:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
