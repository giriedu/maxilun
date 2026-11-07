import re
import os
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple, Optional

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

    def scan_file(self, ts_file: Path, root: Path, project_files: Optional[Dict[str, Path]] = None) -> Dict[str, Any]:
        nodes = []
        edges = []
        if project_files is None:
            project_files = {}

        try:
            rel_path = str(ts_file.relative_to(root)).replace('\\', '/')
        except ValueError:
            rel_path = ts_file.name

        try:
            source = ts_file.read_text(encoding='utf-8', errors='replace')
        except Exception:
            return {'nodes': [], 'edges': []}

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

        # Functions (regular and arrow)
        for pat_name in ('function', 'arrow_function'):
            for match in self.PATTERNS[pat_name].finditer(source):
                func_name = match.group(1)
                if func_name in self.KEYWORDS:
                    continue
                line_no = source[:match.start()].count('\n') + 1
                func_id = f"func:{rel_path}:{func_name}"
                defined_symbols[func_name] = line_no

                snippet_end = min(line_no + 3, len(lines))
                nodes.append({
                    'id': func_id,
                    'label': func_name,
                    'type': 'function',
                    'source_file': f"{rel_path}:{line_no}",
                    'snippet': '\n'.join(lines[line_no - 1:snippet_end])
                })
                edges.append({'source': file_node_id, 'target': func_id, 'type': 'DEFINES'})
                func_ranges.append((line_no, line_no + 10, func_id))

        # Methods inside classes
        for match in self.PATTERNS['method'].finditer(source):
            method_name = match.group(1)
            if method_name in self.KEYWORDS:
                continue
            line_no = source[:match.start()].count('\n') + 1

            parent_class = None
            for cname, cstart, cend in class_blocks:
                if cstart <= line_no <= cend:
                    parent_class = cname
                    break

            if parent_class:
                method_id = f"func:{rel_path}:{parent_class}.{method_name}"
                label = f"{parent_class}.{method_name}"
                nodes.append({
                    'id': method_id,
                    'label': label,
                    'type': 'method',
                    'source_file': f"{rel_path}:{line_no}",
                    'snippet': '\n'.join(lines[line_no - 1:min(line_no + 3, len(lines))])
                })
                edges.append({'source': f"class:{rel_path}:{parent_class}", 'target': method_id, 'type': 'DEFINES'})
                func_ranges.append((line_no, line_no + 8, method_id))

        # Imports
        for match in self.PATTERNS['import'].finditer(source):
            import_path = match.group(1)
            if import_path.startswith('.'):
                target_file = self._resolve_js(ts_file, import_path, root, project_files)
                if target_file:
                    edges.append({'source': file_node_id, 'target': f"file:{target_file}", 'type': 'IMPORTS', 'confidence': 'exact'})
                    # Extract imported symbol names
                    import_stmt = match.group(0)
                    brace_match = re.search(r'\{([^}]+)\}', import_stmt)
                    if brace_match:
                        for sym in brace_match.group(1).split(','):
                            sym = sym.strip().split(' as ')[-1].strip()
                            if sym:
                                imported_symbols[sym] = target_file
            else:
                pkg_name = import_path.split('/')[0]
                if pkg_name.startswith('@') and '/' in import_path:
                    pkg_name = '/'.join(import_path.split('/')[:2])
                edges.append({'source': file_node_id, 'target': f"ext:{pkg_name}", 'type': 'IMPORTS', 'confidence': 'exact'})

        # Function calls
        for match in self.PATTERNS['call'].finditer(source):
            callee_name = match.group(1)
            if callee_name in self.KEYWORDS:
                continue
            line_no = source[:match.start()].count('\n') + 1

            # Skip self-call matching the function's own definition line
            if callee_name in defined_symbols and defined_symbols[callee_name] == line_no:
                continue

            caller_id = file_node_id
            for fstart, fend, fid in func_ranges:
                if fstart <= line_no <= fend:
                    caller_id = fid
                    break

            # Disallow self-call if caller is the exact function definition
            if caller_id == f"func:{rel_path}:{callee_name}":
                continue

            if callee_name in defined_symbols:
                target_id = f"func:{rel_path}:{callee_name}"
                conf = 'exact'
            elif callee_name in imported_symbols:
                target_file = imported_symbols[callee_name]
                target_id = f"func:{target_file}:{callee_name}"
                conf = 'exact'
            else:
                target_id = f"func:*:{callee_name}"
                conf = 'name-only'

            edges.append({'source': caller_id, 'target': target_id, 'type': 'CALLS', 'confidence': conf})

        return {'nodes': nodes, 'edges': edges}

    def scan(self, root_path: str) -> Dict[str, Any]:
        nodes = []
        edges = []
        root = Path(root_path).resolve()

        project_files = {}
        for ext in self.EXTENSIONS:
            for ts_file in root.rglob(f'*{ext}'):
                if self.should_skip(ts_file, root):
                    continue
                rel = str(ts_file.relative_to(root)).replace('\\', '/')
                project_files[rel] = ts_file

        for ts_file in project_files.values():
            res = self.scan_file(ts_file, root, project_files)
            nodes.extend(res.get('nodes', []))
            edges.extend(res.get('edges', []))

        return {'nodes': nodes, 'edges': edges}

    def _resolve_js(self, src_file: Path, spec: str, root: Path, project_files: Dict[str, Path]) -> str:
        base = (src_file.parent / spec).resolve()
        cands = [base] + [base.with_suffix(e) for e in self.EXTENSIONS] + [base / f"index{e}" for e in self.EXTENSIONS]
        for cand in cands:
            try:
                rel = str(cand.relative_to(root)).replace('\\', '/')
                if rel in project_files or cand.is_file():
                    return rel
            except ValueError:
                pass
        return ""
