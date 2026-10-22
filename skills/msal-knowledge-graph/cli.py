#!/usr/bin/env python3
"""
Maxilun Knowledge Graph CLI

Usage:
    python cli.py scan <path> [<path2> ...] [--name NAME] [--view] [-o <output.json>]
    python cli.py query <operator> <symbol> [--json] [--graph <graph.json>] [--path <path>]
    python cli.py serve [--port PORT] [--open] [--graph <graph.json>]
    python cli.py export <path> <output.json>

Supported Query Operators:
    defOf: <symbol>         - Find definition location (file:line) and signature
    callsIn: <symbol>       - Find all callers of symbol (file:line)
    callsOut: <symbol>      - Find all symbols called by symbol
    importersOf: <target>   - Find files that import target module/file
    implementsOf: <iface>   - Find classes that implement interface
    extendsOf: <class>      - Find subclasses that extend class
    routesOf: <handler>     - Find routes exposing handler

Examples:
    python cli.py scan . -o .maxilun/graph.json
    python cli.py query defOf: validateToken
    python cli.py query callsIn: processPayment --json
    python cli.py query importersOf: src/config/keys.ts
"""

import argparse
import sys
import os
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from graph_builder import GraphBuilder
from server import MaxilunServer


def _load_or_build_graph(graph_path=None, project_path="."):
    if graph_path and Path(graph_path).is_file():
        with open(graph_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    default_cache = Path(project_path) / '.maxilun' / 'graph.json'
    if default_cache.is_file():
        try:
            with open(default_cache, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass

    # Build fresh graph
    builder = GraphBuilder()
    resolved_path = str(Path(project_path).resolve())
    graph = builder.scan_project(resolved_path)
    try:
        default_cache.parent.mkdir(parents=True, exist_ok=True)
        with open(default_cache, 'w', encoding='utf-8') as f:
            json.dump(graph, f, indent=2, ensure_ascii=False)
    except Exception:
        pass
    return graph


def cmd_scan(args):
    builder = GraphBuilder()

    names = []
    if args.name:
        names = [args.name] + [None] * (len(args.paths) - 1)

    print("\n  Maxilun Knowledge Graph Scanner")
    print("  " + "=" * 40)

    for i, path in enumerate(args.paths):
        resolved = str(Path(path).resolve())
        name = names[i] if i < len(names) and names[i] else None
        print(f"\n  Scanning: {resolved}")
        graph = builder.scan_project(resolved, name)
        meta = graph.get('metadata', {})
        print(f"    Found: {meta.get('node_count', 0)} nodes, {meta.get('edge_count', 0)} edges, {meta.get('cluster_count', 0)} clusters")

    merged = builder.merge_projects()
    stats = builder.get_stats()

    print(f"\n  Total: {stats['total_projects']} project(s)")
    total_nodes = sum(p['nodes'] for p in stats['projects'].values())
    total_edges = sum(p['edges'] for p in stats['projects'].values())
    print(f"  Combined: {total_nodes} nodes, {total_edges} edges")

    output_path = args.output or str(Path(args.paths[0]) / '.maxilun' / 'graph.json')
    builder.save_graph(output_path)
    print(f"\n  Graph cached to: {output_path}")

    if args.view:
        server = MaxilunServer(port=args.port or 8765)
        server.builder = builder
        server.current_graph = merged
        url = server.start(open_browser=True)
        print(f"\n  Press Ctrl+C to stop server...")
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server.stop()

    return merged


def cmd_query(args):
    raw_op = args.operator.strip()
    symbol = args.symbol.strip() if args.symbol else ""

    # Support "defOf: symbol" as single argument
    if not symbol and ':' in raw_op:
        parts = raw_op.split(':', 1)
        op = parts[0].strip()
        symbol = parts[1].strip()
    else:
        op = raw_op.rstrip(':')

    graph = _load_or_build_graph(args.graph, args.path or ".")
    nodes = graph.get('nodes', [])
    edges = graph.get('edges', [])

    results = []

    if op in ('defOf', 'def'):
        for n in nodes:
            label = n.get('label', '')
            nid = n.get('id', '')
            if label == symbol or nid.endswith(f":{symbol}") or nid == symbol:
                results.append({
                    'id': n['id'],
                    'label': label,
                    'type': n.get('type', 'symbol'),
                    'location': n.get('source_file', 'unknown'),
                    'confidence': 'exact'
                })

    elif op in ('callsIn', 'callersOf', 'calls_in'):
        # Find who calls symbol
        for e in edges:
            if e.get('type') == 'CALLS':
                tgt = e.get('target', '')
                matched = (tgt == symbol or tgt.endswith(f":{symbol}") or
                           tgt.endswith(f".{symbol}") or f":{symbol}." in tgt or
                           tgt == f"func:*:{symbol}")
                if not matched and 'candidates' in e:
                    matched = any(c.endswith(f":{symbol}") or c.endswith(f".{symbol}") for c in e['candidates'])

                if matched:
                    caller_id = e.get('source', '')
                    caller_node = next((n for n in nodes if n['id'] == caller_id), None)
                    loc = caller_node.get('source_file', caller_id) if caller_node else caller_id
                    results.append({
                        'caller_id': caller_id,
                        'caller_label': caller_node.get('label', caller_id) if caller_node else caller_id,
                        'location': loc,
                        'confidence': e.get('confidence', 'name-only')
                    })

    elif op in ('callsOut', 'calleesOf', 'calls_out'):
        # Find what symbol calls
        for e in edges:
            if e.get('type') == 'CALLS':
                src = e.get('source', '')
                if (src == symbol or src.endswith(f":{symbol}") or
                        src.endswith(f".{symbol}") or symbol in src):
                    tgt = e.get('target', '')
                    tgt_node = next((n for n in nodes if n['id'] == tgt), None)
                    loc = tgt_node.get('source_file', tgt) if tgt_node else tgt
                    results.append({
                        'callee_id': tgt,
                        'callee_label': tgt_node.get('label', tgt.split(':')[-1]) if tgt_node else tgt.split(':')[-1],
                        'location': loc,
                        'confidence': e.get('confidence', 'name-only')
                    })

    elif op in ('importersOf', 'importers'):
        for e in edges:
            if e.get('type') == 'IMPORTS':
                tgt = e.get('target', '')
                clean_sym = symbol.replace('\\', '/')
                if clean_sym in tgt or tgt.endswith(f":{clean_sym}") or tgt == f"ext:{clean_sym}":
                    src = e.get('source', '')
                    src_node = next((n for n in nodes if n['id'] == src), None)
                    loc = src_node.get('source_file', src) if src_node else src
                    results.append({
                        'importer_id': src,
                        'location': loc,
                        'confidence': e.get('confidence', 'exact')
                    })

    elif op in ('implementsOf', 'implements'):
        for e in edges:
            if e.get('type') == 'IMPLEMENTS':
                tgt = e.get('target', '')
                if symbol in tgt:
                    src = e.get('source', '')
                    src_node = next((n for n in nodes if n['id'] == src), None)
                    loc = src_node.get('source_file', src) if src_node else src
                    results.append({
                        'implementor_id': src,
                        'location': loc,
                        'confidence': 'exact'
                    })

    elif op in ('extendsOf', 'subclassesOf', 'extends'):
        for e in edges:
            if e.get('type') == 'EXTENDS':
                tgt = e.get('target', '')
                if symbol in tgt:
                    src = e.get('source', '')
                    src_node = next((n for n in nodes if n['id'] == src), None)
                    loc = src_node.get('source_file', src) if src_node else src
                    results.append({
                        'subclass_id': src,
                        'location': loc,
                        'confidence': 'exact'
                    })

    elif op in ('routesOf', 'routes'):
        for n in nodes:
            if n.get('type') == 'route' or 'route' in n.get('id', ''):
                if symbol in n.get('id', '') or symbol in n.get('snippet', ''):
                    results.append({
                        'id': n['id'],
                        'label': n.get('label', ''),
                        'location': n.get('source_file', 'unknown')
                    })
    else:
        print(f"Error: Unknown operator '{op}'. Supported: defOf, callsIn, callsOut, importersOf, implementsOf, extendsOf, routesOf", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps({
            'operator': op,
            'symbol': symbol,
            'count': len(results),
            'results': results
        }, indent=2, ensure_ascii=False))
    else:
        if not results:
            print(f"No results found for {op}: {symbol}")
            sys.exit(0)

        print(f"\n  Found {len(results)} match(es) for {op}: {symbol}")
        print("  " + "-" * 40)
        for r in results:
            loc = r.get('location', '')
            label = r.get('label') or r.get('caller_label') or r.get('callee_label') or r.get('id', '')
            conf = f" [{r['confidence']}]" if 'confidence' in r else ""
            print(f"  - {loc} ({label}){conf}")
        print()


def cmd_serve(args):
    server = MaxilunServer(port=args.port, host=args.host)

    if args.graph:
        with open(args.graph, 'r', encoding='utf-8') as f:
            server.current_graph = json.load(f)
        print(f"  Loaded graph from: {args.graph}")
    else:
        server.current_graph = _load_or_build_graph()

    url = server.start(open_browser=args.open)
    print(f"\n  Press Ctrl+C to stop...")
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()


def cmd_export(args):
    builder = GraphBuilder()
    builder.scan_project(str(Path(args.path).resolve()))
    graph = builder.save_graph(args.output)
    print(f"  Exported {len(graph.get('nodes', []))} nodes, {len(graph.get('edges', []))} edges to {args.output}")


def main():
    parser = argparse.ArgumentParser(
        prog='maxilun',
        description='Maxilun Knowledge Graph — Code Intelligence Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # scan
    scan_parser = subparsers.add_parser('scan', help='Scan codebase and build knowledge graph')
    scan_parser.add_argument('paths', nargs='+', help='Project path(s) to scan')
    scan_parser.add_argument('--name', '-n', help='Name for the first project')
    scan_parser.add_argument('--view', '-v', action='store_true', help='Open visualizer in browser')
    scan_parser.add_argument('--port', '-p', type=int, default=8765, help='Server port (default: 8765)')
    scan_parser.add_argument('--output', '-o', help='Save graph JSON to file (default: .maxilun/graph.json)')

    # query
    query_parser = subparsers.add_parser('query', help='Query symbols from knowledge graph')
    query_parser.add_argument('operator', help='Query operator (e.g. defOf:, callsIn:, importersOf:)')
    query_parser.add_argument('symbol', nargs='?', default='', help='Target symbol or file')
    query_parser.add_argument('--json', action='store_true', help='Output results as JSON')
    query_parser.add_argument('--graph', '-g', help='Path to graph JSON file')
    query_parser.add_argument('--path', help='Project path (default: .)')

    # serve
    serve_parser = subparsers.add_parser('serve', help='Start visualizer server')
    serve_parser.add_argument('--port', '-p', type=int, default=8765, help='Server port (default: 8765)')
    serve_parser.add_argument('--host', default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    serve_parser.add_argument('--open', '-o', action='store_true', help='Auto-open browser')
    serve_parser.add_argument('--graph', '-g', help='Load existing graph JSON file')

    # export
    export_parser = subparsers.add_parser('export', help='Export graph to JSON file')
    export_parser.add_argument('path', help='Project path to scan')
    export_parser.add_argument('output', help='Output JSON file path')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'scan':
        cmd_scan(args)
    elif args.command == 'query':
        cmd_query(args)
    elif args.command == 'serve':
        cmd_serve(args)
    elif args.command == 'export':
        cmd_export(args)


if __name__ == '__main__':
    main()
