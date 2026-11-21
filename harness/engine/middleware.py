"""Maxilun Active Runtime Middleware Pipeline.

Intercepts the agent loop at key execution boundaries:
- Pre-flight Knowledge Graph caller discovery before edits
- Security guard against destructive shell commands and bypass flags
- Purity Gate correction loop before yielding to user
- Decision reversibility enforcement (Type 1 vs Type 2)
Zero external dependencies.
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from ..purity_validator import PurityValidator
from ..router import MaxilunRouter
from ..tools.kg_tool import KnowledgeGraphTool

class MiddlewarePipeline:
    """Manages pre-tool, post-response, and reversibility hooks during agent execution."""

    DANGEROUS_COMMAND_PATTERNS = [
        (r"\brm\s+-[rRfF]*\s+/(?:\s|$|\*)", "Destructive root filesystem deletion ('rm -rf /')"),
        (r"\bdel\s+/[fFqsS]*\s+[a-zA-Z]:\\", "Destructive Windows disk deletion ('del /s /q')"),
        (r"\bformat\s+[a-zA-Z]:", "Disk formatting command"),
        (r"\bmkfs\b", "Filesystem creation command"),
        (r"\bgit\s+push\b[^\n]*\s+(?:--force|-f)\b", "Force-pushing to git remote bypasses safety history"),
        (r"\bgit\s+commit\b[^\n]*\s+(?:--no-verify|-n)\b", "Bypassing pre-commit verification hooks is prohibited"),
        (r"\b(?:curl|wget)\b[^\n]*\|\s*(?:bash|sh|powershell|pwsh)\b", "Piping untrusted remote network script directly to shell interpreter"),
        (r"\bcat\b[^\n]*\.(?:env|id_rsa|id_ed25519)\b[^\n]*\|\s*(?:curl|nc|wget)\b", "Attempted credential / secret exfiltration over network"),
    ]

    def __init__(self, repo_root):
        self.root = repo_root
        self.validator = PurityValidator()
        self.router = MaxilunRouter()
        self.kg = KnowledgeGraphTool(repo_root)

    def check_command_security(self, command: str) -> Optional[str]:
        """Validates shell command against dangerous patterns."""
        if not command:
            return None
        for pattern, reason in self.DANGEROUS_COMMAND_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return f"[BLOCKED]: Prohibited command execution: {reason}."
        return None

    def before_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Optional[str]:
        """Pre-flight check before modifying files or executing shell commands."""
        if tool_name in ("execute_bash", "bash", "run_command"):
            cmd = arguments.get("command", "")
            sec_err = self.check_command_security(cmd)
            if sec_err:
                return sec_err

        if tool_name in ("edit_file", "write_file"):
            target_path = arguments.get("path", "")
            target_name = Path(target_path).name.lower()
            if target_name in (".env", "id_rsa", "id_ed25519"):
                return f"[BLOCKED]: Modification of sensitive credential file '{target_name}' is guarded."

            # If editing code files, ensure caller blast radius is known
            if target_path.endswith((".ts", ".tsx", ".py", ".go")):
                filename = Path(target_path).name
                kg_res = self.kg.query("importersOf", filename)
                if kg_res and kg_res.get("match_count", 0) > 0:
                    importers = [m.get("importer") for m in kg_res.get("results", [])[:3]]
                    return f"[PRE-FLIGHT NOTICE]: Target '{filename}' is imported by {len(importers)} files: {', '.join(importers)}. Ensure caller compatibility."
        return None

    def post_model_response(self, text: str) -> Optional[str]:
        """Validates output against Purity Gate; returns corrective prompt if slop detected."""
        res = self.validator.validate_text(text)
        if not res.passed:
            errors = [f"[{v.rule_id}] {v.message}" for v in res.violations if v.severity == "ERROR"]
            if errors:
                return (
                    "MAXILUN PURITY GATE REJECTION: Your previous response violates Maxilun Core Rules:\n"
                    + "\n".join(f"- {e}" for e in errors)
                    + "\n\nCorrection instruction: Revise your answer immediately. Remove all buzzwords, HUD banners, or fake checklists, and ensure all engineering invariants (4 UI states, constant-time compare, etc.) are strictly met."
                )
        return None

    def check_reversibility(self, prompt: str) -> int:
        """Determines if the prompt is Type 1 (Irreversible) or Type 2 (Reversible)."""
        decision = self.router.route(prompt)
        return decision.decision_type
