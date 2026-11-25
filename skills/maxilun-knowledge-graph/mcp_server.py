"""Zero-dependency stdio MCP Server for Maxilun Knowledge Graph.

Exposes kg_locate, kg_query, and kg_scan as native MCP tools for
Antigravity IDE, Claude Code, Cursor, and any MCP-compatible client.
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

KG_DIR = Path(__file__).resolve().parent
if str(KG_DIR) not in sys.path:
    sys.path.insert(0, str(KG_DIR))

from graph_builder import GraphBuilder
from locate import locate as run_locate, render as render_locate


TOOLS = [
    {
        "name": "kg_locate",
        "description": (
            "Locate code, schemas, docs, or assets by natural-language question, symbol, "
            "or stack trace. Returns a ranked file:start-end Read plan with verbatim excerpts "
            "and caller/callee leads without reading files one by one."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "Question, behaviour, error/stack trace, or symbol to find"},
                "path": {"type": "string", "description": "Repository root path (default: '.')", "default": "."},
                "also": {"type": "string", "description": "Comma-separated identifier hints (e.g. 'calculateTotal,tax')", "default": ""},
                "top": {"type": "integer", "description": "Max ranked hits to return (default: 5)", "default": 5},
                "refresh": {"type": "boolean", "description": "Incrementally re-scan changed files before locating (default: false)", "default": False},
            },
            "required": ["question"],
        },
    },
    {
        "name": "kg_query",
        "description": (
            "Query Knowledge Graph relationships for a known symbol or file: "
            "defOf, callsIn, callsOut, importersOf, implementsOf, extendsOf, routesOf."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "operator": {
                    "type": "string",
                    "enum": ["defOf", "callsIn", "callsOut", "importersOf", "implementsOf", "extendsOf", "routesOf"],
                    "description": "Relationship operator",
                },
                "symbol": {"type": "string", "description": "Target symbol or module path"},
                "path": {"type": "string", "description": "Repository root path (default: '.')", "default": "."},
                "refresh": {"type": "boolean", "description": "Incrementally re-scan changed files before querying (default: false)", "default": False},
            },
            "required": ["operator", "symbol"],
        },
    },
    {
        "name": "kg_scan",
        "description": (
            "Build or incrementally refresh the Knowledge Graph (code AST, Markdown, SQL/Prisma/Infra, "
            "and PDF/SVG/Image assets) and write maxilun-out/graph.json."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Repository root path (default: '.')", "default": "."},
                "use_cache": {"type": "boolean", "description": "Use incremental AST cache (default: true)", "default": True},
            },
        },
    },
    {
        "name": "kg_diff_impact",
        "description": (
            "Analyze git diff (staged + unstaged) against the Knowledge Graph to list changed files "
            "and their affected importers/callers blast radius."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Repository root path (default: '.')", "default": "."},
                "refresh": {"type": "boolean", "description": "Incrementally re-scan before computing impact (default: true)", "default": True},
            },
        },
    },
]

_GRAPH_CACHE: Dict[str, Tuple[float, Dict[str, Any]]] = {}


def _resolve_root(raw_path: str) -> Path:
    p = Path(raw_path or ".").expanduser()
    return p.resolve() if p.is_absolute() else (Path.cwd() / p).resolve()


def _parse_file_line(node: Dict[str, Any]) -> Tuple[Optional[str], Optional[int]]:
    raw = str(node.get("source_file") or "")
    line = node.get("line")
    if not raw:
        return None, int(line) if isinstance(line, int) else None
    m = re.match(r"^(.*):(\d+)$", raw)
    if m:
        fpath = m.group(1).replace("\\", "/")
        return fpath, int(line) if isinstance(line, int) else int(m.group(2))
    return raw.replace("\\", "/"), int(line) if isinstance(line, int) else None


def _get_or_scan(root: Path, force: bool = False, use_cache: bool = True) -> Dict[str, Any]:
    key = str(root)
    graph_files = [root / "maxilun-out" / "graph.json", root / ".maxilun" / "graph.json"]
    if not force:
        for gf in graph_files:
            if gf.is_file():
                try:
                    mtime = gf.stat().st_mtime
                    cached = _GRAPH_CACHE.get(key)
                    if cached and cached[0] >= mtime:
                        return cached[1]
                    data = json.loads(gf.read_text(encoding="utf-8", errors="replace"))
                    if isinstance(data, dict) and "nodes" in data:
                        _GRAPH_CACHE[key] = (mtime, data)
                        return data
                except Exception:
                    pass
        if key in _GRAPH_CACHE and not any(gf.is_file() for gf in graph_files):
            return _GRAPH_CACHE[key][1]
    gb = GraphBuilder()
    graph = gb.scan_project(key, use_cache=use_cache)
    out_dir = root / "maxilun-out"
    out_dir.mkdir(parents=True, exist_ok=True)
    gf_out = out_dir / "graph.json"
    gb.save_graph(str(gf_out), merged=True)
    try:
        mtime = gf_out.stat().st_mtime
    except OSError:
        mtime = 0.0
    _GRAPH_CACHE[key] = (mtime, graph)
    return graph


def _handle_tool(name: str, args: Dict[str, Any]) -> str:
    root = _resolve_root(args.get("path", "."))
    if not root.exists():
        raise FileNotFoundError(f"Path does not exist: {root}")

    if name == "kg_scan":
        use_cache = bool(args.get("use_cache", True))
        graph = _get_or_scan(root, force=True, use_cache=use_cache)
        return json.dumps({
            "root": str(root),
            "total_nodes": len(graph.get("nodes", [])),
            "total_edges": len(graph.get("edges", [])),
            "graph_file": str(root / "maxilun-out" / "graph.json"),
        }, indent=2)

    graph = _get_or_scan(root, force=bool(args.get("refresh", False)), use_cache=True)
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    node_locs = {n["id"]: _parse_file_line(n) for n in nodes if n.get("id")}

    if name == "kg_locate":
        question = args["question"]
        also_raw = args.get("also", "")
        extra = [a.strip() for a in also_raw.split(",") if a.strip()]
        top = int(args.get("top", 5))
        res = run_locate(question, root=str(root), graph=graph, top=top, also=extra)
        return render_locate(res)

    if name == "kg_query":
        op = args["operator"].rstrip(":")
        symbol = str(args["symbol"]).replace("\\", "/")
        matches = []
        if op == "defOf":
            for n in nodes:
                nid = str(n.get("id", "")).replace("\\", "/")
                if n.get("label") == symbol or symbol in nid:
                    nfile, nline = _parse_file_line(n)
                    matches.append({
                        "id": n.get("id"),
                        "type": n.get("type"),
                        "file": nfile,
                        "line": nline,
                    })
        else:
            edge_map = {
                "callsIn": ("CALLS", "target", "source"),
                "callsOut": ("CALLS", "source", "target"),
                "importersOf": ("IMPORTS", "target", "source"),
                "implementsOf": ("IMPLEMENTS", "target", "source"),
                "extendsOf": ("EXTENDS", "target", "source"),
                "routesOf": ("EXPOSES", "source", "target"),
            }
            if op in edge_map:
                etype, match_field, other_field = edge_map[op]
                for e in edges:
                    mval = str(e.get(match_field, "")).replace("\\", "/")
                    if e.get("type") == etype and symbol in mval:
                        src_file, src_line = node_locs.get(e.get("source"), (None, None))
                        ef = e.get("source_file") or src_file
                        el = e.get("line") if isinstance(e.get("line"), int) else src_line
                        matches.append({
                            "match": e.get(match_field),
                            "related": e.get(other_field),
                            "type": etype,
                            "confidence": e.get("confidence", "exact"),
                            "file": ef,
                            "line": el,
                        })
        payload: Dict[str, Any] = {"operator": op, "symbol": symbol, "count": len(matches), "matches": matches[:50]}
        if op == "routesOf" and not matches:
            payload["note"] = "No EXPOSES route edges in graph; use kg_locate with endpoint/router terms for HTTP route lookup."
        return json.dumps(payload, indent=2)

    if name == "kg_diff_impact":
        changed = []
        for cmd in (["git", "diff", "--name-only"], ["git", "diff", "--cached", "--name-only"]):
            try:
                out = subprocess.check_output(cmd, cwd=str(root), text=True, stderr=subprocess.DEVNULL)
                for line in out.splitlines():
                    f = line.strip().replace("\\", "/")
                    if f and f not in changed:
                        changed.append(f)
            except Exception:
                pass

        impacted = {}
        for f in changed:
            stem = Path(f).stem
            no_ext = f.rsplit(".", 1)[0] if "." in Path(f).name else f
            importers = set()
            callers = set()
            for e in edges:
                etype = e.get("type")
                src_file, src_line = node_locs.get(e.get("source"), (None, None))
                ef = str(e.get("source_file") or src_file or "").replace("\\", "/")
                if etype == "IMPORTS":
                    tval = str(e.get("target", "")).replace("\\", "/")
                    if tval.endswith(f) or tval.endswith(no_ext) or Path(tval).stem == stem and ("/" in tval and f.endswith(tval) or tval == stem):
                        importers.add(ef or str(e.get("source")))
                elif etype == "CALLS":
                    if ef == f or ef.endswith("/" + f) or f"file:{f}" in str(e.get("source", "")) or f":{f}:" in str(e.get("source", "")):
                        loc = f"{ef}:{src_line}" if (ef and src_line) else (ef or str(e.get("source")))
                        target_sym = str(e.get("target", ""))
                        callers.add(f"{loc} -> {target_sym}" if target_sym else loc)
            impacted[f] = {"importers": sorted(importers)[:20], "outbound_calls": sorted(callers)[:20]}

        return json.dumps({"changed_files": changed, "impact": impacted}, indent=2)

    raise ValueError(f"Unknown tool: {name}")


def main() -> None:
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        req_id = req.get("id")
        method = req.get("method", "")
        params = req.get("params") or {}

        # Notifications have no id and expect no response
        if req_id is None:
            continue

        try:
            if method == "initialize":
                result = {
                    "protocolVersion": params.get("protocolVersion", "2024-11-05"),
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "maxilun-kg", "version": "1.3.0"},
                }
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": TOOLS}
            elif method == "tools/call":
                tname = params.get("name", "")
                targs = params.get("arguments") or {}
                try:
                    text = _handle_tool(tname, targs)
                    result = {"content": [{"type": "text", "text": text}], "isError": False}
                except Exception as exc:
                    result = {"content": [{"type": "text", "text": f"Error: {exc}"}], "isError": True}
            else:
                resp = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
                continue

            resp = {"jsonrpc": "2.0", "id": req_id, "result": result}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as exc:
            resp = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32603, "message": str(exc)}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()

