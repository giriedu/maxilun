"""Maxilun Active Runtime Middleware Pipeline.

Intercepts the agent loop at key execution boundaries:
- Pre-flight Knowledge Graph caller discovery before edits
- Purity Gate correction loop before yielding to user
- Decision reversibility enforcement (Type 1 vs Type 2)
Zero external dependencies.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from ..purity_validator import PurityValidator
from ..router import MaxilunRouter
from ..tools.kg_tool import KnowledgeGraphTool

class MiddlewarePipeline:
    """Manages pre-tool, post-response, and reversibility hooks during agent execution."""

    def __init__(self, repo_root):
        self.root = repo_root
        self.validator = PurityValidator()
        self.router = MaxilunRouter()
        self.kg = KnowledgeGraphTool(repo_root)

    def before_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Optional[str]:
        """Pre-flight check before modifying files."""
        if tool_name in ("edit_file", "write_file"):
            target_path = arguments.get("path", "")
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
