#!/usr/bin/env python3
"""Deterministic n8n Workflow JSON Validator & Mermaid Converter.

Validates n8n workflow files against schema invariants:
  - Valid JSON object structure with 'nodes' (list) and 'connections' (dict)
  - Every node has valid 'id', 'name', 'type', 'typeVersion'
  - Validates connection integrity (no dangling edges, existing nodes)
  - Enforces SEC-N8N-001: Zero hardcoded credentials/secrets in node parameters
  - Emits Mermaid flowchart diagram for immediate visual inspection
Zero external dependencies.
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple

SUSPICIOUS_SECRET_PATTERNS = [
    r"(?i)api[_-]?key\s*[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{20,}",
    r"(?i)bearer\s+[A-Za-z0-9_\-\.]{25,}",
    r"(?i)ghp_[A-Za-z0-9]{30,}",
    r"(?i)sk_live_[A-Za-z0-9]{24,}",
    r"(?i)password\s*[\"']?\s*[:=]\s*[\"'](?!\$env\.)[^\s\"']{6,}[\"']",
]


class N8nWorkflowValidator:
    """Validates n8n workflow JSON structure and security invariants."""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self, workflow_data: Dict[str, Any]) -> bool:
        self.errors.clear()
        self.warnings.clear()

        if not isinstance(workflow_data, dict):
            self.errors.append("Workflow root must be a JSON object.")
            return False

        nodes = workflow_data.get("nodes")
        if not isinstance(nodes, list) or len(nodes) == 0:
            self.errors.append("Workflow must contain a non-empty 'nodes' list.")
            return False

        connections = workflow_data.get("connections")
        if not isinstance(connections, dict):
            self.errors.append("Workflow must contain a 'connections' dictionary.")
            return False

        node_names = set()
        node_ids = set()

        for idx, node in enumerate(nodes):
            if not isinstance(node, dict):
                self.errors.append(f"Node at index {idx} is not an object.")
                continue

            name = node.get("name")
            nid = node.get("id")
            ntype = node.get("type")
            tver = node.get("typeVersion")

            if not name or not isinstance(name, str):
                self.errors.append(f"Node at index {idx} missing valid 'name'.")
            else:
                if name in node_names:
                    self.errors.append(f"Duplicate node name: '{name}'.")
                node_names.add(name)

            if not nid:
                self.errors.append(f"Node '{name or idx}' missing 'id'.")
            else:
                node_ids.add(nid)

            if not ntype or not isinstance(ntype, str):
                self.errors.append(f"Node '{name or idx}' missing 'type'.")

            if tver is None:
                self.warnings.append(f"Node '{name or idx}' missing 'typeVersion'.")

            # Check for hardcoded secrets in parameters (SEC-N8N-001)
            params = node.get("parameters", {})
            param_str = json.dumps(params)
            for pat in SUSPICIOUS_SECRET_PATTERNS:
                if re.search(pat, param_str):
                    self.errors.append(f"SEC-N8N-001: Potential hardcoded secret in parameters of node '{name}'. Use n8n credentials vault or $env.")

        # Validate connection integrity
        for source_name, conn_group in connections.items():
            if source_name not in node_names:
                self.errors.append(f"Connection source '{source_name}' does not exist in nodes list.")
                continue

            if not isinstance(conn_group, dict):
                continue

            for output_type, output_branches in conn_group.items():
                if not isinstance(output_branches, list):
                    continue
                for branch_idx, branch in enumerate(output_branches):
                    if not isinstance(branch, list):
                        continue
                    for edge in branch:
                        if not isinstance(edge, dict):
                            continue
                        target_name = edge.get("node")
                        if target_name not in node_names:
                            self.errors.append(f"Connection from '{source_name}' points to non-existent target node '{target_name}'.")

        # Check for error handling
        has_error_handler = any(
            "error" in n.get("type", "").lower() or "error" in n.get("name", "").lower()
            for n in nodes
        )
        if not has_error_handler and len(nodes) > 3:
            self.warnings.append("REL-N8N-002: Workflow has >3 nodes but no Error Trigger or error handling node detected.")

        return len(self.errors) == 0

    def to_mermaid(self, workflow_data: Dict[str, Any]) -> str:
        """Converts n8n workflow graph into Mermaid flowchart."""
        nodes = workflow_data.get("nodes", [])
        connections = workflow_data.get("connections", {})

        lines = ["flowchart LR"]
        node_id_map = {}

        for idx, n in enumerate(nodes):
            name = n.get("name", f"Node_{idx}")
            safe_id = f"N_{re.sub(r'[^A-Za-z0-9_]', '_', name)}"
            node_id_map[name] = safe_id
            ntype = n.get("type", "").split(".")[-1]
            lines.append(f"    {safe_id}[\"{name}<br/><i>({ntype})</i>\"]")

        for source_name, conn_group in connections.items():
            src_id = node_id_map.get(source_name)
            if not src_id or not isinstance(conn_group, dict):
                continue
            for out_type, branches in conn_group.items():
                if not isinstance(branches, list):
                    continue
                for branch in branches:
                    if not isinstance(branch, list):
                        continue
                    for edge in branch:
                        tgt_name = edge.get("node")
                        tgt_id = node_id_map.get(tgt_name)
                        if tgt_id:
                            lines.append(f"    {src_id} --> {tgt_id}")

        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python n8n_validate.py <workflow.json> [--mermaid]")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"❌ File not found: {path}")
        sys.exit(1)

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Invalid JSON format: {e}")
        sys.exit(1)

    validator = N8nWorkflowValidator()
    valid = validator.validate(data)

    print(f"\n🔍 n8n Workflow Validation Report: {path.name}")
    print("=" * 60)

    if validator.errors:
        print(f"❌ Found {len(validator.errors)} Error(s):")
        for err in validator.errors:
            print(f"  • {err}")

    if validator.warnings:
        print(f"⚠️  Found {len(validator.warnings)} Warning(s):")
        for warn in validator.warnings:
            print(f"  • {warn}")

    if valid:
        print("✅ Workflow passed all n8n v1 schema & security invariant checks.")
        if "--mermaid" in sys.argv:
            print("\nMermaid Flowchart:")
            print("```mermaid")
            print(validator.to_mermaid(data))
            print("```")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
