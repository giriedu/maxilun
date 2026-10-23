import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict

from scanner import PythonScanner, TypeScriptScanner, GenericScanner


class GraphBuilder:
    SCANNERS = [PythonScanner(), TypeScriptScanner(), GenericScanner()]

    def __init__(self):
        self.projects: Dict[str, Dict[str, Any]] = {}

    def scan_project(self, path: str, name: Optional[str] = None) -> Dict[str, Any]:
        root = Path(path).resolve()
        project_name = name or root.name

        all_nodes = []
        all_edges = []

        for scanner in self.SCANNERS:
            result = scanner.scan(str(root))
            all_nodes.extend(result.get('nodes', []))
            all_edges.extend(result.get('edges', []))

        seen_ids = set()
        unique_nodes = []
        for node in all_nodes:
            if node['id'] not in seen_ids:
                seen_ids.add(node['id'])
                node['project'] = project_name
                unique_nodes.append(node)

        # Resolve wildcard edges (func:*:, class:*:, interface:*:, file:*:)
        unique_edges = self._resolve_symbol_edges(unique_nodes, all_edges)

        communities = self._detect_communities(unique_nodes, unique_edges)

        # Assign community ID to each node
        node_comm_map = {}
        for cid, members in communities['communities'].items():
            for mid in members:
                node_comm_map[mid] = int(cid)
        for node in unique_nodes:
            if node['id'] in node_comm_map:
                node['community'] = node_comm_map[node['id']]

        graph_data = {
            'name': project_name,
            'nodes': unique_nodes,
            'edges': unique_edges,
            'communities': communities['communities'],
            'community_labels': communities['labels'],
            'metadata': {
                'path': str(root),
                'node_count': len(unique_nodes),
                'edge_count': len(unique_edges),
                'cluster_count': len(communities['communities'])
            }
        }

        self.projects[project_name] = graph_data
        return graph_data

    def _resolve_symbol_edges(self, nodes: List[Dict], edges: List[Dict]) -> List[Dict]:
        """
        Maps wildcard targets (func:*:name, class:*:name, file:*:name) to concrete node IDs.
        Tags resolved edges with confidence: exact or name-only.
        """
        valid_ids = {n['id'] for n in nodes}
        symbol_map = defaultdict(list)
        for n in nodes:
            label = n.get('label', '')
            if label:
                symbol_map[label].append(n['id'])
                if '.' in label:
                    symbol_map[label.split('.')[-1]].append(n['id'])

        wildcard_prefixes = ('func:*:', 'class:*:', 'interface:*:', 'ext:', 'file:*:')
        unique_edges = []
        seen_edges = set()

        # Build file import map for caller disambiguation
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
                    conf = 'exact'
                elif len(cands) > 1:
                    # Disambiguation: check caller's file and imports
                    caller_file = f"file:{src.split(':')[1]}" if ':' in src else src
                    same_file = [c for c in cands if caller_file in c]
                    imported = [c for c in cands if any(imp in c for imp in file_imports.get(caller_file, set()))]

                    if len(same_file) == 1:
                        tgt = same_file[0]
                        conf = 'exact'
                    elif len(imported) == 1:
                        tgt = imported[0]
                        conf = 'exact'
                    else:
                        conf = 'name-only'
                        edge['candidates'] = cands
                else:
                    conf = 'name-only'

            elif tgt.startswith('file:*:'):
                mod_name = tgt.split(':')[-1]
                cands = [n['id'] for n in nodes if n.get('type') == 'module' and (n.get('label', '').startswith(mod_name) or mod_name in n['id'])]
                if len(cands) == 1:
                    tgt = cands[0]
                    conf = 'exact'
                elif len(cands) > 1:
                    conf = 'name-only'
                    edge['candidates'] = cands
                else:
                    conf = 'name-only'

            key = f"{src}->{tgt}:{etype}"
            if key in seen_edges:
                continue

            tgt_valid = (tgt in valid_ids or any(tgt.startswith(p) for p in wildcard_prefixes))
            if tgt_valid:
                seen_edges.add(key)
                resolved_edge = dict(edge)
                resolved_edge['source'] = src
                resolved_edge['target'] = tgt
                resolved_edge['confidence'] = conf
                unique_edges.append(resolved_edge)

        return unique_edges

    def _detect_communities(self, nodes: List[Dict], edges: List[Dict]) -> Dict[str, Any]:
        """
        Detects communities across modules using label propagation.
        Connects files not just by IMPORTS, but also by cross-file function calls.
        """
        file_nodes = [n for n in nodes if n.get('type') == 'module']
        file_nodes.sort(key=lambda n: n['id'])
        file_ids = {fn['id'] for fn in file_nodes}

        # Map each symbol to its owning file
        node_to_file = {}
        for n in nodes:
            nid = n['id']
            if n.get('type') == 'module':
                node_to_file[nid] = nid
            else:
                src_file = n.get('source_file', '').split(':')[0]
                node_to_file[nid] = f"file:{src_file}"

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

        result_communities = {}
        result_labels = {}
        comm_id = 0

        for root_label, fids in file_clusters.items():
            cid_str = str(comm_id)
            # Members include the files and all symbols declared within those files
            members = []
            for fid in fids:
                members.append(fid)
                members.extend([n['id'] for n in nodes if node_to_file.get(n['id']) == fid and n['id'] != fid])

            result_communities[cid_str] = members
            label_parts = [fid.replace('file:', '').split('/')[-1].split('.')[0] for fid in fids[:3]]
            result_labels[cid_str] = ' / '.join(label_parts) if label_parts else f"Cluster {comm_id}"
            comm_id += 1

        unvisited = [n['id'] for n in nodes if not any(n['id'] in mem for mem in result_communities.values())]
        if unvisited:
            result_communities[str(comm_id)] = unvisited
            result_labels[str(comm_id)] = "External / Shared"

        return {'communities': result_communities, 'labels': result_labels}

    def merge_projects(self) -> Dict[str, Any]:
        if len(self.projects) == 0:
            return {'name': 'Empty', 'nodes': [], 'edges': [], 'communities': {}, 'community_labels': {}}

        if len(self.projects) == 1:
            return list(self.projects.values())[0]

        all_nodes = []
        all_edges = []
        merged_communities = {}
        merged_labels = {}
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

            comm_offset += len(proj_graph.get('communities', {}))

        return {
            'name': 'Multi-Project Graph',
            'nodes': all_nodes,
            'edges': all_edges,
            'communities': merged_communities,
            'community_labels': merged_labels,
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
