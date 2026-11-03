"""Maxilun Native Knowledge Graph In-Process Tool.

Connects the harness runtime directly to maxilun-knowledge-graph scanners.
Zero external dependencies.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List


class KnowledgeGraphTool:
    """Direct in-process binding to Maxilun Knowledge Graph AST Scanners."""

    def __init__(self, repo_root: Path):
        self.root = repo_root
        self.kg_dir = self.root / "skills" / "maxilun-knowledge-graph"
        if not self.kg_dir.exists():
            self.kg_dir = self.root / ".agents" / "skills" / "maxilun-knowledge-graph"
        if str(self.kg_dir) not in sys.path and self.kg_dir.exists():
            sys.path.insert(0, str(self.kg_dir))

        self.builder = None
        self._cached_graph = None

    def _get_builder(self):
        if self.builder is None:
            try:
                from graph_builder import GraphBuilder
                self.builder = GraphBuilder()
            except ImportError:
                return None
        return self.builder

    def scan(self, target_path: str = ".") -> Dict[str, Any]:
        builder = self._get_builder()
        if not builder:
            return {"error": "Knowledge Graph scanner module not found."}

        target = Path(target_path) if Path(target_path).is_absolute() else self.root / target_path
        self._cached_graph = builder.scan_project(str(target))
        nodes = self._cached_graph.get("nodes", [])
        edges = self._cached_graph.get("edges", [])

        return {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "sample_nodes": [n.get("id") for n in nodes[:5]],
            "sample_edges": [f"{e.get('source')} -> {e.get('target')} ({e.get('type')})" for e in edges[:5]]
        }

    def query(self, operator: str, symbol: str, target_path: str = ".") -> Dict[str, Any]:
        if not self._cached_graph:
            self.scan(target_path)

        if not self._cached_graph:
            return {"error": "Knowledge Graph scan unavailable."}

        op = operator.rstrip(":")
        nodes = self._cached_graph.get("nodes", [])
        edges = self._cached_graph.get("edges", [])
        matches = []

        if op == "defOf":
            for n in nodes:
                if n.get("label") == symbol or symbol in n.get("id", ""):
                    matches.append({
                        "id": n.get("id"),
                        "type": n.get("type"),
                        "source_file": n.get("source_file"),
                        "snippet": n.get("snippet", "")[:150]
                    })
        elif op == "callsIn":
            for e in edges:
                if e.get("type") == "CALLS" and symbol in e.get("target", ""):
                    matches.append({
                        "caller": e.get("source"),
                        "callee": e.get("target"),
                        "type": e.get("type"),
                        "confidence": e.get("confidence", "exact")
                    })
        elif op == "callsOut":
            for e in edges:
                if e.get("type") == "CALLS" and symbol in e.get("source", ""):
                    matches.append({
                        "caller": e.get("source"),
                        "callee": e.get("target"),
                        "type": e.get("type")
                    })
        elif op == "importersOf":
            for e in edges:
                if e.get("type") == "IMPORTS" and symbol in e.get("target", ""):
                    matches.append({
                        "importer": e.get("source"),
                        "imported": e.get("target")
                    })
        else:
            return {"error": f"Unsupported Knowledge Graph operator: '{operator}' (use defOf, callsIn, callsOut, importersOf)"}

        return {
            "operator": op,
            "symbol": symbol,
            "match_count": len(matches),
            "results": matches
        }
