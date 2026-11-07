#!/usr/bin/env python3
"""
Maxilun Knowledge Graph — Code Intelligence Engine
===================================================

Command-line tool for scanning source code, extracting AST-based symbols
and relationships, querying symbol graphs, comparing architectural diffs,
and generating visual reports.

Usage:
  python cli.py scan [paths...] [--view] [--output <file>] [--no-cache] [--snapshot]
  python cli.py snapshot [path]
  python cli.py diff <target1> <target2> [--path <repo-path>]
  python cli.py query <operator> <symbol> [--json] [--path <repo-path>]
  python cli.py serve [--port <port>] [--host <host>] [--open]
  python cli.py export <path> <output>

Operators:
  defOf: <symbol>       Definition location & signature
  callsIn: <symbol>     Functions/methods calling this symbol
  callsOut: <symbol>    Symbols called by this function
  importersOf: <path>   Files importing this module
  implementsOf: <iface> Classes implementing interface
  extendsOf: <class>    Subclasses extending base class
  routesOf: <symbol>    Endpoints exposing handler
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Tuple, Optional, List
from collections import defaultdict, Counter

sys.path.insert(0, str(Path(__file__).parent))

from graph_builder import GraphBuilder
from server import MaxilunServer


def _generate_maxilun_report(graph, stats):
    nodes = graph.get('nodes', [])
    edges = graph.get('edges', [])
    communities = graph.get('communities', {}) or graph.get('clusters', {})
    community_labels = graph.get('community_labels', {})
    community_cohesions = graph.get('community_cohesions', {})
    meta = graph.get('metadata', {})

    node_by_id = {n.get('id'): n for n in nodes}
    in_degree = Counter()
    out_degree = Counter()
    for e in edges:
        src = e.get('source')
        tgt = e.get('target')
        out_degree[src] += 1
        in_degree[tgt] += 1

    top_inbound = sorted(in_degree.items(), key=lambda x: x[1], reverse=True)[:10]
    top_outbound = sorted(out_degree.items(), key=lambda x: x[1], reverse=True)[:10]

    lang_counts = Counter()
    for n in nodes:
        lang = n.get('language') or n.get('type') or 'other'
        lang_counts[lang] += 1

    ext_stats = meta.get('extraction_stats', {})
    exact_pct = ext_stats.get('exact_pct', 100.0)
    inferred_pct = ext_stats.get('inferred_pct', 0.0)
    cache_hits = meta.get('cache_hits', 0)
    cache_misses = meta.get('cache_misses', 0)
    unclass_count = meta.get('unclassified_count', 0)
    unclass_exts = meta.get('unclassified_top_extensions', {})

    lines = [
        f"# Maxilun Knowledge Graph — Architecture Report ({datetime.now().strftime('%Y-%m-%d')})",
        "",
        "Laporan pemetaan struktural basis kode yang dihasilkan secara deterministik oleh **Maxilun Knowledge Graph Engine**.",
        "",
        "## 1. Corpus & Extraction Check",
        "",
        f"- **Total Simbol / Node**: {len(nodes)}",
        f"- **Total Relasi / Edge**: {len(edges)}",
        f"- **Total Kluster Arsitektur**: {len(communities)}",
        f"- **Total Proyek Dipindai**: {stats.get('total_projects', 1)}",
        f"- **Tingkat Ekstraksi**: {exact_pct}% EXTRACTED · {inferred_pct}% INFERRED",
        f"- **Performa Cache**: {cache_hits} cache hits · {cache_misses} parsed fresh",
        f"- **Berkas Tidak Terklasifikasi**: {unclass_count} berkas non-kode (top: " +
        (", ".join(f"`{k}`: {v}" for k, v in unclass_exts.items()) if unclass_exts else "none") + ")",
        f"- **Komposisi Simbol**: " + ", ".join(f"`{k}`: {v}" for k, v in lang_counts.most_common(6)),
        "",
        "## 2. God Nodes (Simbol dengan Derajat Keterhubungan Tertinggi - High Blast Radius)",
        "",
        "Simbol dengan derajat ketergantungan paling masif (core bottlenecks). Modifikasi pada simbol ini memerlukan mitigasi risiko Type 1:",
        "",
        "| Peringkat | Simbol / Node | Total Derajat | Inbound | Outbound | File Sumber |",
        "|:---:|---|:---:|:---:|:---:|---|",
    ]

    ranked_god = sorted(nodes, key=lambda n: n.get('degree', in_degree[n['id']] + out_degree[n['id']]), reverse=True)[:10]
    for i, n in enumerate(ranked_god, 1):
        nid = n.get('id', '')
        label = n.get('label') or nid
        path = n.get('source_file') or n.get('path') or '-'
        in_d = in_degree[nid]
        out_d = out_degree[nid]
        tot_d = in_d + out_d
        lines.append(f"| {i} | `{label}` | **{tot_d}** | {in_d} | {out_d} | `{path}` |")

    lines.extend([
        "",
        "## 3. Hub Inti (Paling Banyak Dipanggil / Inbound)",
        "",
        "| Peringkat | Simbol / Target | Inbound Edges | File Sumber |",
        "|:---:|---|:---:|---|",
    ])
    for i, (nid, deg) in enumerate(top_inbound, 1):
        n = node_by_id.get(nid, {})
        label = n.get('label') or nid
        path = n.get('source_file') or n.get('path') or '-'
        lines.append(f"| {i} | `{label}` | **{deg}** | `{path}` |")

    lines.extend([
        "",
        "## 4. Titik Koordinasi (Highest Fan-Out)",
        "",
        "| Peringkat | Simbol Pengkoordinasi | Outbound Calls | File Sumber |",
        "|:---:|---|:---:|---|",
    ])
    for i, (nid, deg) in enumerate(top_outbound, 1):
        n = node_by_id.get(nid, {})
        label = n.get('label') or nid
        path = n.get('source_file') or n.get('path') or '-'
        lines.append(f"| {i} | `{label}` | **{deg}** | `{path}` |")

    if communities:
        lines.extend([
            "",
            "## 5. Kluster & Komunitas Arsitektur (dengan Cohesion Score)",
            "",
            "| ID | Label Komunitas | Anggota Node | Cohesion Score | Karakteristik Arsitektur |",
            "|:---:|---|:---:|:---:|---|",
        ])
        for cid, members in sorted(communities.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 999):
            clabel = community_labels.get(cid, f"Cluster {cid}")
            coh = community_cohesions.get(cid, 0.0)
            if coh >= 0.6:
                status = "Tinggi (Loose coupling, high cohesion)"
            elif coh >= 0.2:
                status = "Moderat (Interkoneksi sehat)"
            else:
                status = "Rendah (Penyebaran luas / cross-cutting)"
            lines.append(f"| **{cid}** | `{clabel}` | {len(members)} | `{coh}` | {status} |")

    lines.extend([
        "",
        "## 6. Cara Penggunaan Artefak Maxilun-Out",
        "",
        "1. **Buka Visualizer Offline**: Buka `lens.html` di browser apa pun untuk visualisasi 3D Galaxy & 2D Matrix.",
        "2. **Kueri Cepat Simbol**: Jalankan `python cli.py query <operator> <simbol>`.",
        "3. **Bandingkan Evolusi Graf**: Jalankan `python cli.py diff <snapshot1> <snapshot2>`.",
        "4. **Arsip Snapshot Baru**: Jalankan `python cli.py scan --snapshot`.",
        "",
        "---",
        "*Dihasilkan oleh Maxilun Knowledge Graph Engine v1.2.0*",
    ])
    return "\n".join(lines)


def _export_maxilun_out(target_root, graph, stats, snapshot=False):
    out_dir = Path(target_root) / 'maxilun-out'
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Save graph.json
    graph_json_path = out_dir / 'graph.json'
    with open(graph_json_path, 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)

    # 2. Save standalone lens.html
    lens_src = Path(__file__).parent / 'graph-viewer' / 'lens.html'
    if lens_src.is_file():
        try:
            lens_content = lens_src.read_text(encoding='utf-8')
            data_script = f"\n<script>\nwindow.MAXILUN_GRAPH_DATA = {json.dumps(graph, ensure_ascii=False)};\n</script>\n"
            injected = lens_content.replace('</head>', f'{data_script}</head>', 1)
            (out_dir / 'lens.html').write_text(injected, encoding='utf-8')
        except Exception:
            pass

    # 3. Save MAXILUN_REPORT.md
    report_content = _generate_maxilun_report(graph, stats)
    (out_dir / 'MAXILUN_REPORT.md').write_text(report_content, encoding='utf-8')

    # 4. Optional / Date snapshotting
    if snapshot:
        today_str = datetime.now().strftime("%Y-%m-%d")
        snap_dir = out_dir / 'snapshots' / today_str
        snap_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(graph_json_path, snap_dir / 'graph.json')
        (snap_dir / 'MAXILUN_REPORT.md').write_text(report_content, encoding='utf-8')

        manifest_src = Path(target_root) / '.maxilun' / 'manifest.json'
        if manifest_src.is_file():
            shutil.copy2(manifest_src, snap_dir / 'manifest.json')

    return out_dir


def _load_or_build_graph(graph_path=None, project_path="."):
    if graph_path and Path(graph_path).is_file():
        with open(graph_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    # 1. Native Maxilun output directory
    maxilun_out = Path(project_path) / 'maxilun-out' / 'graph.json'
    if maxilun_out.is_file():
        try:
            with open(maxilun_out, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass

    # 2. Internal dotfile cache
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
        stats = builder.get_stats()
        _export_maxilun_out(project_path, graph, stats)
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

    print("\n  Maxilun Knowledge Graph Scanner (v1.2.0)")
    print("  " + "=" * 45)

    use_cache = not getattr(args, 'no_cache', False)
    do_snapshot = getattr(args, 'snapshot', False)

    for i, path in enumerate(args.paths):
        resolved = str(Path(path).resolve())
        name = names[i] if i < len(names) and names[i] else None
        print(f"\n  Scanning: {resolved} {'[using incremental cache]' if use_cache else '[cache disabled]'}")
        graph = builder.scan_project(resolved, name, use_cache=use_cache)
        meta = graph.get('metadata', {})
        print(f"    Found : {meta.get('node_count', 0)} nodes, {meta.get('edge_count', 0)} edges, {meta.get('cluster_count', 0)} clusters")
        if use_cache:
            print(f"    Cache : {meta.get('cache_hits', 0)} hits, {meta.get('cache_misses', 0)} parsed fresh")

    merged = builder.merge_projects()
    stats = builder.get_stats()

    print(f"\n  Total   : {stats['total_projects']} project(s)")
    total_nodes = sum(p['nodes'] for p in stats['projects'].values())
    total_edges = sum(p['edges'] for p in stats['projects'].values())
    print(f"  Combined: {total_nodes} nodes, {total_edges} edges")

    if args.output:
        builder.save_graph(args.output)
        print(f"\n  Graph saved to: {args.output}")
    else:
        out_dir = _export_maxilun_out(args.paths[0], merged, stats, snapshot=do_snapshot)
        print(f"\n  Maxilun artifacts generated in: {out_dir}")
        print(f"    - {out_dir / 'graph.json'} (AST Knowledge Graph)")
        print(f"    - {out_dir / 'lens.html'} (Standalone 3D/2D Lens Visualizer)")
        print(f"    - {out_dir / 'MAXILUN_REPORT.md'} (Architecture & Hub Analysis Report)")
        if do_snapshot:
            today_str = datetime.now().strftime("%Y-%m-%d")
            print(f"    - {out_dir / 'snapshots' / today_str} (Archived Snapshot)")

        output_path = str(Path(args.paths[0]) / '.maxilun' / 'graph.json')
        builder.save_graph(output_path)
        print(f"  Internal cache saved to: {output_path}")

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


def cmd_snapshot(args):
    target_path = args.path or "."
    args.paths = [target_path]
    args.name = None
    args.view = False
    args.output = None
    args.no_cache = False
    args.snapshot = True
    return cmd_scan(args)


def _resolve_graph_target(target: str, base_path: str = ".") -> Tuple[Dict[str, Any], str]:
    p = Path(target)
    if p.is_file():
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f), str(p)

    cands = [
        Path(base_path) / 'maxilun-out' / 'snapshots' / target / 'graph.json',
        Path(base_path) / 'maxilun-out' / target / 'graph.json',
        Path(base_path) / 'graphify-out' / target / 'graph.json',
        Path(base_path) / target / 'graph.json',
    ]
    for cand in cands:
        if cand.is_file():
            with open(cand, 'r', encoding='utf-8') as f:
                return json.load(f), str(cand)

    raise FileNotFoundError(f"Cannot resolve graph for target '{target}'. Checked paths: {[str(c) for c in cands]}")


def cmd_diff(args):
    base_path = args.path or "."
    try:
        g1, name1 = _resolve_graph_target(args.target1, base_path)
        g2, name2 = _resolve_graph_target(args.target2, base_path)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    nodes1 = {n['id']: n for n in g1.get('nodes', [])}
    nodes2 = {n['id']: n for n in g2.get('nodes', [])}

    def _edge_key(e):
        src = e.get('source') or e.get('from')
        tgt = e.get('target') or e.get('to')
        rel = e.get('type') or e.get('relation') or e.get('label') or 'REL'
        return (src, tgt, rel)

    edges1 = {_edge_key(e) for e in g1.get('edges', []) + g1.get('links', [])}
    edges2 = {_edge_key(e) for e in g2.get('edges', []) + g2.get('links', [])}

    added_nodes = sorted(list(nodes2.keys() - nodes1.keys()))
    removed_nodes = sorted(list(nodes1.keys() - nodes2.keys()))
    added_edges = sorted(list(edges2 - edges1))
    removed_edges = sorted(list(edges1 - edges2))

    n_delta = len(nodes2) - len(nodes1)
    e_delta = len(edges2) - len(edges1)

    print("\n  Maxilun Architectural Graph Diff")
    print("  " + "=" * 45)
    print(f"  Target 1 (Base)    : {name1} ({len(nodes1)} nodes, {len(edges1)} edges)")
    print(f"  Target 2 (Compare) : {name2} ({len(nodes2)} nodes, {len(edges2)} edges)")
    print("  " + "-" * 45)
    print(f"  Node Delta         : {'+' if n_delta >= 0 else ''}{n_delta} (Added: {len(added_nodes)}, Removed: {len(removed_nodes)})")
    print(f"  Edge Delta         : {'+' if e_delta >= 0 else ''}{e_delta} (Added: {len(added_edges)}, Removed: {len(removed_edges)})")

    if added_nodes:
        print(f"\n  [+] Added Nodes ({len(added_nodes)}):")
        for nid in added_nodes[:8]:
            label = nodes2[nid].get('label') or nid
            print(f"      + {label} ({nid})")
        if len(added_nodes) > 8:
            print(f"      ... and {len(added_nodes) - 8} more")

    if removed_nodes:
        print(f"\n  [-] Removed Nodes ({len(removed_nodes)}):")
        for nid in removed_nodes[:8]:
            label = nodes1[nid].get('label') or nid
            print(f"      - {label} ({nid})")
        if len(removed_nodes) > 8:
            print(f"      ... and {len(removed_nodes) - 8} more")

    if added_edges:
        print(f"\n  [+] Added Edges ({len(added_edges)}):")
        for src, tgt, rel in added_edges[:8]:
            print(f"      + {src} --[{rel}]--> {tgt}")
        if len(added_edges) > 8:
            print(f"      ... and {len(added_edges) - 8} more")

    if removed_edges:
        print(f"\n  [-] Removed Edges ({len(removed_edges)}):")
        for src, tgt, rel in removed_edges[:8]:
            print(f"      - {src} --[{rel}]--> {tgt}")
        if len(removed_edges) > 8:
            print(f"      ... and {len(removed_edges) - 8} more")

    print()


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
                    'location': n.get('source_file') or n.get('path', 'unknown'),
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


def cmd_context(args):
    symbol = args.symbol.strip()
    graph = _load_or_build_graph(args.graph, args.path or ".")
    nodes = graph.get('nodes', [])
    edges = graph.get('edges', [])

    target_node = None
    for n in nodes:
        nid = n.get('id', '')
        lbl = n.get('label', '')
        if lbl == symbol or nid.endswith(f":{symbol}") or nid == symbol:
            target_node = n
            break

    loc = target_node.get('source_file') or target_node.get('path', 'unknown') if target_node else 'unknown'
    node_id = target_node.get('id', '') if target_node else ''

    callers = []
    for e in edges:
        if e.get('type') == 'CALLS':
            tgt = e.get('target', '')
            if tgt == node_id or tgt.endswith(f":{symbol}") or tgt == f"func:*:{symbol}":
                src = e.get('source', '')
                src_n = next((n for n in nodes if n['id'] == src), None)
                src_loc = src_n.get('source_file', src) if src_n else src
                callers.append(f"`{src_loc}` [{e.get('confidence', 'name-only')}]")

    callees = []
    if node_id:
        for e in edges:
            if e.get('type') == 'CALLS' and e.get('source') == node_id:
                tgt = e.get('target', '')
                tgt_n = next((n for n in nodes if n['id'] == tgt), None)
                tgt_lbl = tgt_n.get('label', tgt.split(':')[-1]) if tgt_n else tgt.split(':')[-1]
                callees.append(f"`{tgt_lbl}`")

    doc_refs = []
    for e in edges:
        if e.get('type') == 'REFERENCES' and (e.get('target') == node_id or symbol in e.get('target', '')):
            src = e.get('source', '')
            doc_refs.append(f"`{src}`")

    blast_level = "Type 1 (Irreversible / High-Blast)" if len(callers) > 10 else "Type 2 (Reversible / Moderate)" if len(callers) > 2 else "Type 2 (Low-Blast)"

    lines = [
        f"### Maxilun Impact Context: `{symbol}`",
        f"- **Definisi**: `{loc}` [exact]" if target_node else f"- **Definisi**: `Simbol tidak terdefinisi di graf lokal`",
        f"- **Inbound Callers** ({len(callers)}): " + (", ".join(callers[:8]) if callers else "None"),
        f"- **Outbound Calls** ({len(callees)}): " + (", ".join(callees[:8]) if callees else "None"),
        f"- **Related Specs / Docs**: " + (", ".join(doc_refs[:5]) if doc_refs else "None"),
        f"- **Klasifikasi Blast Radius**: `{blast_level}`"
    ]
    output = "\n".join(lines)
    print(output)
    return output

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
    scan_parser.add_argument('paths', nargs='*', default=['.'], help='Project path(s) to scan (default: current folder)')
    scan_parser.add_argument('--name', '-n', help='Name for the first project')
    scan_parser.add_argument('--view', '-v', action='store_true', help='Open visualizer in browser')
    scan_parser.add_argument('--port', '-p', type=int, default=8765, help='Server port (default: 8765)')
    scan_parser.add_argument('--output', '-o', help='Save graph JSON to file (default: .maxilun/graph.json)')
    scan_parser.add_argument('--no-cache', action='store_true', help='Bypass cache and force fresh scan')
    scan_parser.add_argument('--snapshot', action='store_true', help='Archive a date-stamped snapshot in maxilun-out/snapshots/YYYY-MM-DD/')

    # snapshot
    snapshot_parser = subparsers.add_parser('snapshot', help='Scan and archive a dated snapshot of the graph')
    snapshot_parser.add_argument('path', nargs='?', default='.', help='Project path to snapshot (default: current folder)')

    # diff
    diff_parser = subparsers.add_parser('diff', help='Compare two graph snapshots or files')
    diff_parser.add_argument('target1', help='Base target (date string YYYY-MM-DD or graph.json path)')
    diff_parser.add_argument('target2', help='Compare target (date string YYYY-MM-DD or graph.json path)')
    diff_parser.add_argument('--path', help='Project root path for snapshot resolution (default: .)')

    # query
    query_parser = subparsers.add_parser('query', help='Query symbols from knowledge graph')
    query_parser.add_argument('operator', help='Query operator (e.g. defOf:, callsIn:, importersOf:)')
    query_parser.add_argument('symbol', nargs='?', default='', help='Target symbol or file')
    query_parser.add_argument('--json', action='store_true', help='Output results as JSON')
    query_parser.add_argument('--graph', '-g', help='Path to graph JSON file')
    query_parser.add_argument('--path', help='Project path (default: .)')

    # context
    context_parser = subparsers.add_parser('context', help='Generate compressed blast-radius prompt context for LLMs')
    context_parser.add_argument('symbol', help='Target symbol to inspect')
    context_parser.add_argument('--graph', '-g', help='Path to graph JSON file')
    context_parser.add_argument('--path', help='Project path (default: .)')

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
    elif args.command == 'snapshot':
        cmd_snapshot(args)
    elif args.command == 'diff':
        cmd_diff(args)
    elif args.command == 'query':
        cmd_query(args)
    elif args.command == 'context':
        cmd_context(args)
    elif args.command == 'serve':
        cmd_serve(args)
    elif args.command == 'export':
        cmd_export(args)


if __name__ == '__main__':
    main()
