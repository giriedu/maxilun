"""Maxilun Native Knowledge Graph In-Process Tool.

Connects the harness runtime directly to maxilun-knowledge-graph scanners.
Zero external dependencies.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

HARNESS_REPO = Path(__file__).resolve().parents[2]


class KnowledgeGraphTool:
    """Direct in-process binding to Maxilun Knowledge Graph AST Scanners."""

    def __init__(
        self,
        repo_root: Path,
        cached_graph: Optional[Dict[str, Any]] = None,
        cached_root: Optional[str] = None,
    ):
        self.root = Path(repo_root).resolve()
        # Prefer verified harness KG implementation before workspace copies to prevent sys.path hijacking.
        builtin_kg = HARNESS_REPO / "skills" / "maxilun-knowledge-graph"
        candidates = [builtin_kg] + [
            self.root / base / "maxilun-knowledge-graph"
            for base in ("skills", Path(".agents") / "skills", Path(".claude") / "skills")
        ]
        self.kg_dir = next((c for c in candidates if c.exists()), builtin_kg)
        if str(self.kg_dir) not in sys.path and self.kg_dir.exists():
            sys.path.insert(0, str(self.kg_dir))

        self.builder = None
        self._cached_graph = cached_graph
        self._cached_root = cached_root if cached_graph is not None else None

    def invalidate(self) -> None:
        """Clears the in-memory graph cache after workspace mutations."""
        self._cached_graph = None
        self._cached_root = None

    def _resolve_target(self, target_path: str = ".") -> Path:
        raw = Path(target_path or ".")
        resolved = (raw if raw.is_absolute() else self.root / raw).resolve()
        if resolved != self.root and self.root not in resolved.parents:
            raise PermissionError(f"KG target path '{target_path}' is outside the workspace root.")
        return resolved

    def _get_builder(self):
        if self.builder is None:
            try:
                from graph_builder import GraphBuilder
                self.builder = GraphBuilder()
            except ImportError:
                return None
        return self.builder

    def _load_or_scan(self, target_path: str = ".") -> Optional[Dict[str, Any]]:
        target = self._resolve_target(target_path)
        key = str(target)
        if self._cached_graph is not None and self._cached_root == key:
            return self._cached_graph

        for cache_file in (target / "maxilun-out" / "graph.json", target / ".maxilun" / "graph.json"):
            if cache_file.is_file():
                try:
                    data = json.loads(cache_file.read_text(encoding="utf-8", errors="replace"))
                    if isinstance(data, dict) and isinstance(data.get("nodes"), list):
                        self._cached_graph = data
                        self._cached_root = key
                        return data
                except OSError:
                    pass
                except ValueError:
                    pass

        builder = self._get_builder()
        if not builder:
            return None
        self._cached_graph = builder.scan_project(key)
        self._cached_root = key
        return self._cached_graph

    def scan(self, target_path: str = ".") -> Dict[str, Any]:
        try:
            target = self._resolve_target(target_path)
        except PermissionError as exc:
            return {"error": str(exc)}
        builder = self._get_builder()
        if not builder:
            return {"error": "Knowledge Graph scanner module not found."}

        key = str(target)
        self._cached_graph = builder.scan_project(key)
        self._cached_root = key
        nodes = self._cached_graph.get("nodes", [])
        edges = self._cached_graph.get("edges", [])

        return {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "sample_nodes": [n.get("id") for n in nodes[:5]],
            "sample_edges": [f"{e.get('source')} -> {e.get('target')} ({e.get('type')})" for e in edges[:5]]
        }

    def locate(
        self,
        question: str,
        target_path: str = ".",
        also: str = "",
        top: int = 5,
        lines: int = 14,
        budget: int = 6000,
        include_hits: bool = False,
    ) -> Dict[str, Any]:
        """Question, stack trace, or symbol -> ranked file:line ranges with verbatim excerpts."""
        try:
            target = self._resolve_target(target_path)
            graph = self._load_or_scan(target_path)
        except PermissionError as exc:
            return {"error": str(exc)}
        if not graph:
            return {"error": "Knowledge Graph scanner module not found."}
        try:
            from locate import locate as run_locate, render
        except ImportError:
            return {"error": "Knowledge Graph locate module not found."}
        extra = [a.strip() for a in also.split(",") if a.strip()]
        result = run_locate(
            question,
            root=str(target),
            graph=graph,
            top=top,
            lines=lines,
            budget=budget,
            also=extra,
        )
        out: Dict[str, Any] = {
            "confidence": result["confidence"],
            "missing_terms": result["missing_terms"],
            "report": render(result),
        }
        if include_hits:
            out["hits"] = [
                {
                    "file": h.get("file", ""),
                    "range": h.get("range", []),
                    "symbol": h.get("symbol", ""),
                    "type": h.get("type", ""),
                    "score": h.get("score", 0.0),
                    "callers": h.get("callers", []),
                    "callees": h.get("callees", []),
                }
                for h in result.get("hits", [])
            ]
        return out

    def query(self, operator: str, symbol: str, target_path: str = ".") -> Dict[str, Any]:
        op = operator.rstrip(":")
        if op not in ("defOf", "callsIn", "callsOut", "importersOf"):
            return {"error": f"Unsupported Knowledge Graph operator: '{operator}' (use defOf, callsIn, callsOut, importersOf)"}

        sym = (symbol or "").strip()
        if not sym:
            return {"operator": op, "symbol": symbol, "match_count": 0, "results": []}

        try:
            graph = self._load_or_scan(target_path)
        except PermissionError as exc:
            return {"error": str(exc)}
        if not graph:
            return {"error": "Knowledge Graph scan unavailable."}

        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])
        exact_matches: List[Dict[str, Any]] = []
        partial_matches: List[Dict[str, Any]] = []

        if op == "defOf":
            for n in nodes:
                node_id = n.get("id", "")
                label = n.get("label", "")
                leaf = node_id.split(":")[-1]
                is_exact = (label == sym or leaf == sym)
                if is_exact or sym in node_id:
                    item = {
                        "id": node_id,
                        "type": n.get("type"),
                        "source_file": n.get("source_file"),
                        "line": n.get("line"),
                        "snippet": n.get("snippet", "")[:150],
                    }
                    (exact_matches if is_exact else partial_matches).append(item)
        elif op in ("callsIn", "callsOut"):
            field = "target" if op == "callsIn" else "source"
            for e in edges:
                if e.get("type") != "CALLS":
                    continue
                val = e.get(field, "")
                leaf = val.split(":")[-1]
                is_exact = (val == sym or leaf == sym)
                if is_exact or sym in val:
                    item = {
                        "caller": e.get("source"),
                        "callee": e.get("target"),
                        "type": e.get("type"),
                        "confidence": e.get("confidence", "exact"),
                    }
                    (exact_matches if is_exact else partial_matches).append(item)
        elif op == "importersOf":
            sym_norm = sym.replace("\\", "/")
            while sym_norm.startswith("./"):
                sym_norm = sym_norm[2:]
            sym_stem = sym_norm.rsplit(".", 1)[0] if "." in sym_norm.rsplit("/", 1)[-1] else sym_norm
            stem_leaf = sym_stem.rsplit("/", 1)[-1]
            for e in edges:
                if e.get("type") != "IMPORTS":
                    continue
                target_val = str(e.get("target", "")).replace("\\", "/")
                leaf = target_val.split("/")[-1]
                mod_leaf = leaf.split(":")[-1]
                is_exact = (
                    target_val == sym_norm
                    or leaf == sym_norm
                    or mod_leaf in (sym_norm, sym_stem, stem_leaf)
                )
                if is_exact or sym_norm in target_val:
                    item = {
                        "importer": e.get("source"),
                        "imported": e.get("target"),
                    }
                    (exact_matches if is_exact else partial_matches).append(item)

        matches = exact_matches + partial_matches
        return {
            "operator": op,
            "symbol": symbol,
            "match_count": len(matches),
            "results": matches[:30],
        }
