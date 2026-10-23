import re
import os
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple

from .base_scanner import BaseScanner


class TypeScriptScanner(BaseScanner):
    EXTENSIONS = {'.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs'}

    PATTERNS = {
        'function': re.compile(
            r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*(?:<[^>]*>)?\s*\(([^)]*)\)',
            re.MULTILINE
        ),
        'arrow_function': re.compile(
            r'(?:export\s+)?(?:const|let|var)\s+(\w+)\s*(?::\s*[^=]+)?\s*=\s*(?:async\s+)?\(([^)]*)\)\s*(?::\s*[^=]+)?\s*=>',
            re.MULTILINE
        ),
        'class': re.compile(
            r'(?:export\s+)?(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w,\s]+))?',
            re.MULTILINE
        ),
        'interface': re.compile(
            r'(?:export\s+)?interface\s+(\w+)(?:\s+extends\s+([\w,\s]+))?',
            re.MULTILINE
        ),
        'method': re.compile(
            r'(?:(?:public|private|protected|static|async)\s+)*(\w+)\s*(?:<[^>]*>)?\s*\(([^)]*)\)\s*(?::\s*[^{]+)?\s*\{',
            re.MULTILINE
        ),
        'import': re.compile(
            r'(?:import\s+(?:(?:\{[^}]*\}|\*\s+as\s+\w+|\w+)(?:\s*,\s*(?:\{[^}]*\}|\*\s+as\s+\w+))?)\s+from\s+|require\(\s*)[\'"]([^\'"]+)[\'"]',
            re.MULTILINE
        ),
        'call': re.compile(
            r'(?<!\.)(\b\w+)\s*(?:<[^>]*>)?\s*\(',
            re.MULTILINE
        ),
        'type_alias': re.compile(
            r'(?:export\s+)?type\s+(\w+)\s*=\s*',
            re.MULTILINE
        ),
    }

    KEYWORDS = frozenset({
        'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'return',
        'throw', 'try', 'catch', 'finally', 'new', 'delete', 'typeof',
        'instanceof', 'void', 'in', 'of', 'await', 'yield', 'super',
        'this', 'null', 'undefined', 'true', 'false', 'NaN', 'Infinity',
        'console', 'require', 'import', 'export', 'default', 'from',
        'class', 'function', 'const', 'let', 'var', 'async', 'interface',
        'type', 'enum', 'abstract', 'implements', 'extends', 'public',
        'private', 'protected', 'static', 'readonly', 'declare', 'as',
        'get', 'set', 'constructor'
    })

    def scan(self, root_path: str) -> Dict[str, Any]:
        nodes = []
        edges = []
        root = Path(root_path).resolve()

        # Collect all project JS/TS files for import resolution
        project_files = {}
        for ext in self.EXTENSIONS:
            for ts_file in root.rglob(f'*{ext}'):
                if self.should_skip(ts_file, root):
                    continue
                rel = str(ts_file.relative_to(root)).replace('\\', '/')
                project_files[rel] = ts_file

        for rel_path, ts_file in project_files.items():
            try:
                source = ts_file.read_text(encoding='utf-8', errors='replace')
            except Exception:
                continue

            lines = source.splitlines()
            file_node_id = f"file:{rel_path}"
            nodes.append({
                'id': file_node_id,
                'label': ts_file.name,
                'type': 'module',
                'source_file': rel_path,
                'snippet': f'// {rel_path}\n// {len(lines)} lines'
            })

            func_ranges: List[Tuple[int, int, str]] = []
            defined_symbols: Dict[str, int] = {}  # symbol_name -> line_no
            imported_symbols: Dict[str, str] = {}  # symbol_name -> rel_path

            # Classes and interfaces
            class_blocks: List[Tuple[str, int, int]] = []  # (class_name, start_line, end_line)
            for match in self.PATTERNS['class'].finditer(source):
                class_name = match.group(1)
                extends = match.group(2)
                implements = match.group(3)
                line_no = source[:match.start()].count('\n') + 1
                class_id = f"class:{rel_path}:{class_name}"
                defined_symbols[class_name] = line_no

                snippet_end = min(line_no + 5, len(lines))
                nodes.append({
                    'id': class_id,
                    'label': class_name,
                    'type': 'class',
                    'source_file': f"{rel_path}:{line_no}",
                    'snippet': '\n'.join(lines[line_no - 1:snippet_end])
                })
                edges.append({'source': file_node_id, 'target': class_id, 'type': 'DEFINES'})

                if extends:
                    edges.append({'source': class_id, 'target': f"class:*:{extends.strip()}", 'type': 'EXTENDS'})
                if implements:
                    for iface in implements.split(','):
                        edges.append({'source': class_id, 'target': f"interface:*:{iface.strip()}", 'type': 'IMPLEMENTS'})

                # Approximate class body end (next class or EOF)
                class_blocks.append((class_name, line_no, len(lines)))

            for match in self.PATTERNS['interface'].finditer(source):
                iface_name = match.group(1)
                extends = match.group(2)
                line_no = source[:match.start()].count('\n') + 1
                iface_id = f"interface:{rel_path}:{iface_name}"
                defined_symbols[iface_name] = line_no

                snippet_end = min(line_no + 4, len(lines))
                nodes.append({
                    'id': iface_id,
                    'label': iface_name,
                    'type': 'interface',
                    'source_file': f"{rel_path}:{line_no}",
                    'snippet': '\n'.join(lines[line_no - 1:snippet_end])
                })
                edges.append({'source': file_node_id, 'target': iface_id, 'type': 'DEFINES'})

                if extends:
                    for parent in extends.split(','):
                        edges.append({'source': iface_id, 'target': f"interface:*:{parent.strip()}", 'type': 'EXTENDS'})

            # Top-level functions
            for match in self.PATTERNS['function'].finditer(source):
                func_name = match.group(1)
                line_no = source[:match.start()].count('\n') + 1
                func_id = f"func:{rel_path}:{func_name}"
                defined_symbols[func_name] = line_no

                is_async = 'async' in source[max(0, match.start() - 20):match.start()]
                snippet_end = min(line_no + 4, len(lines))
                nodes.append({
                    'id': func_id,
                    'label': func_name,
                    'type': 'async_function' if is_async else 'function',
                    'source_file': f"{rel_path}:{line_no}",
                    'snippet': '\n'.join(lines[line_no - 1:snippet_end])
                })
                edges.append({'source': file_node_id, 'target': func_id, 'type': 'DEFINES'})
                func_ranges.append((line_no, line_no + 5, func_id))

            # Arrow functions
            for match in self.PATTERNS['arrow_function'].finditer(source):
                func_name = match.group(1)
                line_no = source[:match.start()].count('\n') + 1
                func_id = f"func:{rel_path}:{func_name}"
                defined_symbols[func_name] = line_no

                is_async = 'async' in source[match.start():match.end()]
                snippet_end = min(line_no + 3, len(lines))
                nodes.append({
                    'id': func_id,
                    'label': func_name,
                    'type': 'async_function' if is_async else 'function',
                    'source_file': f"{rel_path}:{line_no}",
                    'snippet': '\n'.join(lines[line_no - 1:snippet_end])
                })
                edges.append({'source': file_node_id, 'target': func_id, 'type': 'DEFINES'})
                func_ranges.append((line_no, line_no + 5, func_id))

            # Imports: resolve relative imports to real local files
            for match in self.PATTERNS['import'].finditer(source):
                spec = match.group(1)
                if spec.startswith('.'):
                    resolved_rel = self._resolve_js(ts_file, spec, root, project_files)
                    if resolved_rel:
                        target_id = f"file:{resolved_rel}"
                        edges.append({'source': file_node_id, 'target': target_id, 'type': 'IMPORTS', 'confidence': 'exact'})
                    else:
                        clean_name = spec.split('/')[-1]
                        edges.append({'source': file_node_id, 'target': f"file:*:{clean_name}", 'type': 'IMPORTS', 'confidence': 'name-only'})
                else:
                    pkg_name = spec.split('/')[0]
                    if spec.startswith('@') and '/' in spec:
                        parts = spec.split('/')
                        pkg_name = f"{parts[0]}/{parts[1]}"
                    edges.append({'source': file_node_id, 'target': f"ext:{pkg_name}", 'type': 'IMPORTS', 'confidence': 'exact'})

            # Build line-based range for caller attribution
            func_ranges.sort(key=lambda x: x[0])
            total_lines = len(lines)
            for i in range(len(func_ranges)):
                start_l, _, fid = func_ranges[i]
                next_start = func_ranges[i + 1][0] if i + 1 < len(func_ranges) else total_lines + 1
                func_ranges[i] = (start_l, next_start - 1, fid)

            # Calls
            seen_calls = set()
            for call_match in self.PATTERNS['call'].finditer(source):
                callee_name = call_match.group(1)
                if callee_name in self.KEYWORDS:
                    continue

                call_line = source[:call_match.start()].count('\n') + 1

                # BUG FIX: If call is on the definition line of the function itself, ignore (it is the declaration)
                if callee_name in defined_symbols and defined_symbols[callee_name] == call_line:
                    continue

                caller_id = file_node_id
                for start_l, end_l, fid in func_ranges:
                    if start_l <= call_line <= end_l:
                        caller_id = fid
                        break

                # Resolve target if symbol is defined in same file
                if callee_name in defined_symbols:
                    target_id = f"func:{rel_path}:{callee_name}"
                    conf = "exact"
                else:
                    target_id = f"func:*:{callee_name}"
                    conf = "name-only"

                edge_key = f"{caller_id}->{target_id}:CALLS"
                if edge_key not in seen_calls:
                    seen_calls.add(edge_key)
                    edges.append({'source': caller_id, 'target': target_id, 'type': 'CALLS', 'confidence': conf})

        return {'nodes': nodes, 'edges': edges}

    def _resolve_js(self, src_file: Path, spec: str, root: Path, project_files: Dict[str, Path]) -> str:
        base = (src_file.parent / spec).resolve()
        cands = [base] + [base.with_suffix(e) for e in self.EXTENSIONS] + [base / f"index{e}" for e in self.EXTENSIONS]
        for cand in cands:
            try:
                rel = str(cand.relative_to(root)).replace('\\', '/')
                if rel in project_files:
                    return rel
            except ValueError:
                pass
        return ""
