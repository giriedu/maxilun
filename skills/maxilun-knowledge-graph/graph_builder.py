import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from collections import defaultdict, Counter

from scanner import BaseScanner, PythonScanner, TypeScriptScanner, GenericScanner, MarkdownScanner, SchemaInfraScanner, AssetScanner
from cache_manager import CacheManager


class GraphBuilder:
    SCANNERS = [PythonScanner(), TypeScriptScanner(), GenericScanner(), MarkdownScanner(), SchemaInfraScanner(), AssetScanner()]

    def __init__(self):
        self.projects: Dict[str, Dict[str, Any]] = {}

    def scan_project(self, path: str, name: Optional[str] = None, use_cache: bool = True) -> Dict[str, Any]:
        root = Path(path).resolve()
        project_name = name or root.name

        all_nodes = []
        all_edges = []
        cache_hits = 0
        cache_misses = 0

        # Build extension -> scanner lookup
        ext_to_scanner = {}
        for scanner in self.SCANNERS:
            for ext in getattr(scanner, 'EXTENSIONS', set()):
                ext_to_scanner[ext] = scanner

        cache_mgr = CacheManager(str(root)) if use_cache else None
        active_rel_paths: Set[str] = set()

        if use_cache and cache_mgr:
            # 1. Discover all candidate files
            candidate_files = []
            for ext, scanner in ext_to_scanner.items():
                for fpath in root.rglob(f"*{ext}"):
                    if scanner.should_skip(fpath, root):
                        continue
                    try:
                        rel = str(fpath.relative_to(root)).replace('\\', '/')
                    except ValueError:
                        rel = fpath.name
                    active_rel_paths.add(rel)
                    candidate_files.append((rel, fpath, scanner))

            # 2. Extract or load from AST cache
            for rel, fpath, scanner in candidate_files:
                cached_ast, sha256_hash = cache_mgr.get_file_ast(rel, fpath)
                if cached_ast is not None:
                    all_nodes.extend(cached_ast.get('nodes', []))
                    all_edges.extend(cached_ast.get('edges', []))
                    cache_hits += 1
                else:
                    try:
                        if hasattr(scanner, 'scan_file'):
                            res = scanner.scan_file(fpath, root)
                        else:
                            res = {'nodes': [], 'edges': []}
                    except Exception:
                        res = {'nodes': [], 'edges': []}

                    cache_mgr.save_file_ast(rel, fpath, sha256_hash, res)
                    all_nodes.extend(res.get('nodes', []))
                    all_edges.extend(res.get('edges', []))
                    cache_misses += 1

            cache_mgr.prune_stale_entries(active_rel_paths)
            cache_mgr.persist()

        else:
            for scanner in self.SCANNERS:
                result = scanner.scan(str(root))
                all_nodes.extend(result.get('nodes', []))
                all_edges.extend(result.get('edges', []))

        # Deduplicate nodes by ID
        seen_ids = set()
        unique_nodes = []
        for node in all_nodes:
            if node['id'] not in seen_ids:
                seen_ids.add(node['id'])
                node['project'] = project_name
                unique_nodes.append(node)

        # Resolve wildcard edges (func:*:, class:*:, interface:*:, file:*:)
        unique_edges = self._resolve_symbol_edges(unique_nodes, all_edges)

        # Compute in/out degree and total degree for all nodes
        in_deg = Counter()
        out_deg = Counter()
        for e in unique_edges:
            out_deg[e.get('source')] += 1
            in_deg[e.get('target')] += 1

        for node in unique_nodes:
            nid = node['id']
            node['in_degree'] = in_deg[nid]
            node['out_degree'] = out_deg[nid]
            node['degree'] = in_deg[nid] + out_deg[nid]

        # Community detection with stability and cohesion
        communities = self._detect_communities(unique_nodes, unique_edges, root)

        # Assign community ID to each node
        node_comm_map = {}
        for cid, members in communities['communities'].items():
            for mid in members:
                node_comm_map[mid] = int(cid)
        for node in unique_nodes:
            if node['id'] in node_comm_map:
                node['community'] = node_comm_map[node['id']]
                node['community_name'] = communities['labels'].get(str(node_comm_map[node['id']]), '')

        # Calculate extraction statistics
        exact_edges = sum(1 for e in unique_edges if e.get('confidence') == 'exact')
        inferred_edges = sum(1 for e in unique_edges if e.get('confidence') in ('name-only', 'inferred'))
        total_e = len(unique_edges) or 1

        # Discover unclassified files
        unclassified = self._find_unclassified_files(root, active_rel_paths)

        # Top God Nodes (high degree centrality)
        god_nodes = sorted(
            [n for n in unique_nodes if n.get('degree', 0) > 0],
            key=lambda x: x.get('degree', 0),
            reverse=True
        )[:15]

        graph_data = {
            'name': project_name,
            'nodes': unique_nodes,
            'edges': unique_edges,
            'communities': communities['communities'],
            'community_labels': communities['labels'],
            'community_cohesions': communities.get('cohesions', {}),
            'metadata': {
                'path': str(root),
                'node_count': len(unique_nodes),
                'edge_count': len(unique_edges),
                'cluster_count': len(communities['communities']),
                'cache_hits': cache_hits,
                'cache_misses': cache_misses,
                'extraction_stats': {
                    'exact_count': exact_edges,
                    'exact_pct': round((exact_edges / total_e) * 100, 1),
                    'inferred_count': inferred_edges,
                    'inferred_pct': round((inferred_edges / total_e) * 100, 1),
                },
                'god_nodes': [
                    {'id': n['id'], 'label': n.get('label') or n['id'], 'degree': n.get('degree', 0), 'path': n.get('source_file') or n.get('path', '')}
                    for n in god_nodes
                ],
                'unclassified_count': len(unclassified),
                'unclassified_top_extensions': dict(Counter(f.suffix for f in unclassified if f.suffix).most_common(5))
            }
        }

        self.projects[project_name] = graph_data
        return graph_data

    def _find_unclassified_files(self, root: Path, active_rel_paths: Set[str]) -> List[Path]:
        unclassified = []
        skip_dirs = BaseScanner.COMMON_SKIP_DIRS
        base_scanner = BaseScanner()
        try:
            for p in root.rglob('*'):
                if p.is_dir() or base_scanner.should_skip(p, root):
                    continue
                try:
                    rel = str(p.relative_to(root)).replace('\\', '/')
                except ValueError:
                    rel = p.name
                if rel not in active_rel_paths:
                    unclassified.append(p)
        except Exception:
            pass
        return unclassified

    def _resolve_symbol_edges(self, nodes: List[Dict], edges: List[Dict]) -> List[Dict]:
        """
        Maps wildcard targets (func:*:name, class:*:name, interface:*:name, file:*:name) to concrete node IDs.
        Tags resolved edges with confidence: exact, name-only, or inferred.
        """
        valid_ids = {n['id'] for n in nodes}
        symbol_map = defaultdict(list)
        for n in nodes:
            label = n.get('label', '')
            if label:
                symbol_map[label].append(n['id'])
                if '.' in label:
                    symbol_map[label.split('.')[-1]].append(n['id'])

        unique_edges = []
        seen_edges = set()

        file_imports = defaultdict(set)
        for e in edges:
            if e.get('type') == 'IMPORTS' and e['source'] in valid_ids and e['target'] in valid_ids:
                file_imports[e['source']].add(e['target'])

        for edge in edges:
            src = edge.get('source', '')
            tgt = edge.get('target', '')
            etype = edge.get('type', '')
            conf = edge.get('confidence', 'exact')

            if src not in valid_ids:
                continue

            # Attempt wildcard resolution
            if any(tgt.startswith(p) for p in ('func:*:', 'class:*:', 'interface:*:')):
                sym_name = tgt.split(':')[-1]
                cands = symbol_map.get(sym_name, [])
                if len(cands) == 1:
                    tgt = cands[0]
                    conf = 'exact' if edge.get('confidence') != 'inferred' else 'inferred'
                elif len(cands) > 1:
                    caller_file = f"file:{src.split(':')[1]}" if ':' in src else src
                    same_file = [c for c in cands if caller_file in c]
                    imported = [c for c in cands if any(imp in c for imp in file_imports.get(caller_file, set()))]

                    if len(same_file) == 1:
                        tgt = same_file[0]
                        conf = 'exact' if edge.get('confidence') != 'inferred' else 'inferred'
                    elif len(imported) == 1:
                        tgt = imported[0]
                        conf = 'exact' if edge.get('confidence') != 'inferred' else 'inferred'
                    else:
                        conf = 'name-only'
                        edge['candidates'] = cands
                else:
                    conf = 'name-only'

            elif tgt.startswith('file:*:'):
                f_name = tgt.split(':')[-1]
                file_cands = [n['id'] for n in nodes if n.get('type') in ('module', 'document') and n.get('label') == f_name]
                if len(file_cands) == 1:
                    tgt = file_cands[0]
                    conf = 'exact'
                else:
                    conf = 'name-only'

            if tgt not in valid_ids and not tgt.startswith('ext:'):
                continue

            edge_key = (src, tgt, etype)
            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                resolved_edge = dict(edge)
                resolved_edge['source'] = src
                resolved_edge['target'] = tgt
                resolved_edge['confidence'] = conf
                unique_edges.append(resolved_edge)

        return unique_edges

    def _detect_communities(self, nodes: List[Dict], edges: List[Dict], root: Optional[Path] = None) -> Dict[str, Any]:
        """
        Detects communities across modules using label propagation.
        Stabilizes community IDs and labels across runs using member signatures.
        Computes cohesion score for each community.
        """
        file_nodes = [n for n in nodes if n.get('type') in ('module', 'document')]
        file_nodes.sort(key=lambda n: n['id'])
        file_ids = {fn['id'] for fn in file_nodes}

        # Map each symbol to its owning file
        node_to_file = {}
        for n in nodes:
            nid = n['id']
            if n.get('type') in ('module', 'document'):
                node_to_file[nid] = nid
            else:
                src_file = (n.get('source_file') or n.get('path', '')).split(':')[0]
                node_to_file[nid] = f"file:{src_file}" if not src_file.startswith('doc:') else src_file

        file_adj = defaultdict(set)
        for edge in edges:
            src = edge.get('source', '')
            tgt = edge.get('target', '')
            src_file = node_to_file.get(src)
            tgt_file = node_to_file.get(tgt)

            if src_file and tgt_file and src_file != tgt_file and src_file in file_ids and tgt_file in file_ids:
                file_adj[src_file].add(tgt_file)
                file_adj[tgt_file].add(src_file)

        labels = {fn['id']: fn['id'] for fn in file_nodes}

        for _iteration in range(10):
            changed = False
            for fn in file_nodes:
                fid = fn['id']
                neighbors = file_adj.get(fid, set())
                if not neighbors:
                    continue
                label_counts = defaultdict(int)
                for nb in neighbors:
                    label_counts[labels[nb]] += 1
                best_label = max(label_counts, key=label_counts.get)
                if labels[fid] != best_label:
                    labels[fid] = best_label
                    changed = True
            if not changed:
                break

        # Group file nodes by community
        file_clusters = defaultdict(list)
        for fn in file_nodes:
            file_clusters[labels[fn['id']]].append(fn['id'])

        raw_communities = []
        raw_labels = []

        for root_label, fids in file_clusters.items():
            members = []
            for fid in fids:
                members.append(fid)
                members.extend([n['id'] for n in nodes if node_to_file.get(n['id']) == fid and n['id'] != fid])

            label_parts = [
                fid.replace('file:', '').replace('doc:', '').replace('schema:', '').replace('asset:', '').split('/')[-1].split('.')[0]
                for fid in fids[:3]
            ]
            comm_label = ' / '.join(label_parts) if label_parts else "Cluster"
            raw_communities.append(members)
            raw_labels.append(comm_label)

        unvisited = [n['id'] for n in nodes if not any(n['id'] in mem for mem in raw_communities)]
        if unvisited:
            raw_communities.append(unvisited)
            raw_labels.append("External / Shared")

        # Stabilize community IDs using signature caching
        sig_file = (root / ".maxilun" / "community_signatures.json") if root else None
        prev_signatures = {}
        prev_labels = {}
        if sig_file and sig_file.is_file():
            try:
                with open(sig_file, "r", encoding="utf-8") as f:
                    sig_data = json.load(f)
                    prev_signatures = sig_data.get("signatures", {})
                    prev_labels = sig_data.get("labels", {})
            except Exception:
                pass

        final_communities: Dict[str, List[str]] = {}
        final_labels: Dict[str, str] = {}
        final_cohesions: Dict[str, float] = {}
        new_signatures: Dict[str, str] = {}

        used_cids: Set[int] = set()

        for idx, members in enumerate(raw_communities):
            curr_sig = hashlib.sha256(",".join(sorted(members)).encode()).hexdigest()[:16]
            matched_cid = None

            # 1. Exact signature match
            for prev_cid, prev_sig in prev_signatures.items():
                if prev_sig == curr_sig and int(prev_cid) not in used_cids:
                    matched_cid = int(prev_cid)
                    break

            # 2. Allocate cid
            if matched_cid is None:
                next_cid = 0
                while next_cid in used_cids:
                    next_cid += 1
                matched_cid = next_cid

            used_cids.add(matched_cid)
            cid_str = str(matched_cid)
            final_communities[cid_str] = members
            final_labels[cid_str] = prev_labels.get(cid_str, raw_labels[idx])
            new_signatures[cid_str] = curr_sig

            # Calculate cohesion score
            member_set = set(members)
            int_e = 0
            ext_e = 0
            for e in edges:
                s_in = e.get('source') in member_set
                t_in = e.get('target') in member_set
                if s_in and t_in:
                    int_e += 1
                elif s_in or t_in:
                    ext_e += 1
            cohesion = round(int_e / (int_e + ext_e), 3) if (int_e + ext_e) > 0 else 0.0
            final_cohesions[cid_str] = cohesion

        # Persist updated signatures
        if sig_file:
            try:
                sig_file.parent.mkdir(parents=True, exist_ok=True)
                with open(sig_file, "w", encoding="utf-8") as f:
                    json.dump({"signatures": new_signatures, "labels": final_labels}, f, indent=2)
            except Exception:
                pass

        return {
            'communities': final_communities,
            'labels': final_labels,
            'cohesions': final_cohesions
        }

    def merge_projects(self) -> Dict[str, Any]:
        if len(self.projects) == 0:
            return {'name': 'Empty', 'nodes': [], 'edges': [], 'communities': {}, 'community_labels': {}}

        if len(self.projects) == 1:
            return list(self.projects.values())[0]

        all_nodes = []
        all_edges = []
        merged_communities = {}
        merged_labels = {}
        merged_cohesions = {}
        comm_offset = 0

        for proj_name, proj_graph in self.projects.items():
            proj_comm_offset = comm_offset
            node_id_map = {
                node['id']: f"{proj_name}:{node['id']}"
                for node in proj_graph.get('nodes', [])
            }

            for node in proj_graph.get('nodes', []):
                merged_node = dict(node)
                merged_node['id'] = node_id_map[node['id']]
                merged_node['project'] = node.get('project') or proj_name
                if 'community' in merged_node:
                    merged_node['community'] = int(merged_node['community']) + proj_comm_offset
                all_nodes.append(merged_node)

            for edge in proj_graph.get('edges', []):
                merged_edge = dict(edge)
                if merged_edge.get('source') in node_id_map:
                    merged_edge['source'] = node_id_map[merged_edge['source']]
                if merged_edge.get('target') in node_id_map:
                    merged_edge['target'] = node_id_map[merged_edge['target']]
                all_edges.append(merged_edge)

            for cid, members in proj_graph.get('communities', {}).items():
                new_cid = str(int(cid) + proj_comm_offset)
                merged_communities[new_cid] = [node_id_map.get(member, member) for member in members]
                original_label = proj_graph.get('community_labels', {}).get(cid, f"Cluster {cid}")
                merged_labels[new_cid] = f"{proj_name}: {original_label}"
                merged_cohesions[new_cid] = proj_graph.get('community_cohesions', {}).get(cid, 0.0)

            comm_offset += len(proj_graph.get('communities', {}))

        return {
            'name': 'Multi-Project Graph',
            'nodes': all_nodes,
            'edges': all_edges,
            'communities': merged_communities,
            'community_labels': merged_labels,
            'community_cohesions': merged_cohesions,
            'metadata': {
                'project_count': len(self.projects),
                'projects': list(self.projects.keys()),
                'total_nodes': len(all_nodes),
                'total_edges': len(all_edges)
            }
        }

    def save_graph(self, output_path: str, merged: bool = True):
        graph = self.merge_projects() if merged else list(self.projects.values())[0] if self.projects else {}
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph, f, indent=2, ensure_ascii=False)
        return graph

    def get_stats(self) -> Dict[str, Any]:
        stats = {'projects': {}}
        for name, graph in self.projects.items():
            meta = graph.get('metadata', {})
            stats['projects'][name] = {
                'nodes': meta.get('node_count', len(graph.get('nodes', []))),
                'edges': meta.get('edge_count', len(graph.get('edges', []))),
                'clusters': meta.get('cluster_count', len(graph.get('communities', {})))
            }
        stats['total_projects'] = len(self.projects)
        return stats
