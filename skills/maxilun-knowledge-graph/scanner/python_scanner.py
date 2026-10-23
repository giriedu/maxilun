import ast
import os
from pathlib import Path
from typing import Dict, List, Any, Set, Optional

from .base_scanner import BaseScanner

PYTHON_BUILTINS = frozenset({
    'abs', 'aiter', 'all', 'anext', 'any', 'ascii', 'bin', 'bool', 'breakpoint',
    'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex',
    'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter',
    'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash',
    'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter',
    'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next',
    'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'range',
    'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted',
    'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip'
})


class PythonScanner(BaseScanner):
    EXTENSIONS = {'.py'}

    def scan(self, root_path: str) -> Dict[str, Any]:
        nodes = []
        edges = []
        root = Path(root_path).resolve()

        # Collect all python files in project for import resolution
        project_files = {}
        for py_file in root.rglob('*.py'):
            if self.should_skip(py_file, root):
                continue
            rel = str(py_file.relative_to(root)).replace('\\', '/')
            project_files[rel] = py_file

        for rel_path, py_file in project_files.items():
            try:
                source = py_file.read_text(encoding='utf-8', errors='replace')
                tree = ast.parse(source, filename=str(py_file))
            except SyntaxError:
                continue

            file_node_id = f"file:{rel_path}"
            nodes.append({
                'id': file_node_id,
                'label': py_file.name,
                'type': 'module',
                'source_file': rel_path,
                'snippet': f'# {rel_path}\n# {len(source.splitlines())} lines'
            })

            parent_map = self._build_parent_map(tree)
            func_ranges = []
            file_symbols = set()
            imported_symbols = {}  # name -> target file rel_path

            # First pass: classes, methods, top-level functions, imports
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_id = f"class:{rel_path}:{node.name}"
                    file_symbols.add(node.name)
                    snippet_lines = source.splitlines()[node.lineno - 1:min(node.lineno + 5, len(source.splitlines()))]
                    nodes.append({
                        'id': class_id,
                        'label': node.name,
                        'type': 'class',
                        'source_file': f"{rel_path}:{node.lineno}",
                        'snippet': '\n'.join(snippet_lines)
                    })
                    edges.append({'source': file_node_id, 'target': class_id, 'type': 'DEFINES'})

                    for base in node.bases:
                        base_name = self._get_name(base)
                        if base_name:
                            edges.append({'source': class_id, 'target': f"class:*:{base_name}", 'type': 'EXTENDS'})

                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            method_id = f"func:{rel_path}:{node.name}.{item.name}"
                            method_label = f"{node.name}.{item.name}"
                            file_symbols.add(item.name)
                            file_symbols.add(method_label)
                            nodes.append({
                                'id': method_id,
                                'label': method_label,
                                'type': 'method',
                                'source_file': f"{rel_path}:{item.lineno}",
                                'snippet': '\n'.join(source.splitlines()[item.lineno - 1:min(item.lineno + 3, len(source.splitlines()))])
                            })
                            edges.append({'source': class_id, 'target': method_id, 'type': 'DEFINES'})
                            func_ranges.append((item.lineno, item.end_lineno or item.lineno, method_id))

                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    parent = parent_map.get(node)
                    # Skip if enclosed in ClassDef (already handled above as method)
                    if isinstance(parent, ast.ClassDef):
                        continue

                    func_id = f"func:{rel_path}:{node.name}"
                    file_symbols.add(node.name)
                    snippet_lines = source.splitlines()[node.lineno - 1:min(node.lineno + 4, len(source.splitlines()))]
                    nodes.append({
                        'id': func_id,
                        'label': node.name,
                        'type': 'async_function' if isinstance(node, ast.AsyncFunctionDef) else 'function',
                        'source_file': f"{rel_path}:{node.lineno}",
                        'snippet': '\n'.join(snippet_lines)
                    })
                    edges.append({'source': file_node_id, 'target': func_id, 'type': 'DEFINES'})
                    func_ranges.append((node.lineno, node.end_lineno or node.lineno, func_id))

                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    resolved_files, ext_modules = self._resolve_py_import(py_file, node, root, project_files)
                    for target_rel in resolved_files:
                        target_file_id = f"file:{target_rel}"
                        edges.append({'source': file_node_id, 'target': target_file_id, 'type': 'IMPORTS', 'confidence': 'exact'})
                        if isinstance(node, ast.ImportFrom):
                            for alias in node.names:
                                imported_symbols[alias.asname or alias.name] = target_rel

                    for ext_mod in ext_modules:
                        edges.append({'source': file_node_id, 'target': f"ext:{ext_mod}", 'type': 'IMPORTS', 'confidence': 'exact'})

                elif isinstance(node, ast.Call):
                    callee_name = self._get_call_name(node)
                    if not callee_name or callee_name in PYTHON_BUILTINS:
                        continue

                    caller_id = self._find_enclosing_fast(parent_map, node, rel_path, func_ranges)
                    
                    # Resolve callee target
                    if callee_name in file_symbols:
                        target_id = f"func:{rel_path}:{callee_name}"
                        conf = "exact"
                    elif callee_name in imported_symbols:
                        target_rel = imported_symbols[callee_name]
                        target_id = f"func:{target_rel}:{callee_name}"
                        conf = "exact"
                    else:
                        target_id = f"func:*:{callee_name}"
                        conf = "name-only"

                    edges.append({
                        'source': caller_id,
                        'target': target_id,
                        'type': 'CALLS',
                        'confidence': conf
                    })

        return {'nodes': nodes, 'edges': edges}

    def _resolve_py_import(self, src_file: Path, node: ast.AST, root: Path, project_files: Dict[str, Path]):
        resolved_files = set()
        ext_modules = set()

        if isinstance(node, ast.ImportFrom):
            level = node.level or 0
            if level > 0:
                # Relative import e.g. from .b import helper, from ..utils import helper
                base = src_file.parent
                for _ in range(level - 1):
                    base = base.parent
                mod_subpath = (node.module or '').replace('.', os.sep)
                target_base = (base / mod_subpath).resolve()
            else:
                mod_subpath = (node.module or '').replace('.', os.sep)
                target_base = (root / mod_subpath).resolve()

            # Check if target is a file or package
            cands = [
                target_base.with_suffix('.py'),
                target_base / '__init__.py'
            ]
            matched = False
            for cand in cands:
                try:
                    rel = str(cand.relative_to(root)).replace('\\', '/')
                    if rel in project_files:
                        resolved_files.add(rel)
                        matched = True
                        break
                except ValueError:
                    pass

            if not matched:
                if level == 0 and node.module:
                    top_pkg = node.module.split('.')[0]
                    ext_modules.add(top_pkg)

        elif isinstance(node, ast.Import):
            for alias in node.names:
                mod_path = alias.name.replace('.', os.sep)
                target_base = (root / mod_path).resolve()
                cands = [target_base.with_suffix('.py'), target_base / '__init__.py']
                matched = False
                for cand in cands:
                    try:
                        rel = str(cand.relative_to(root)).replace('\\', '/')
                        if rel in project_files:
                            resolved_files.add(rel)
                            matched = True
                            break
                    except ValueError:
                        pass
                if not matched:
                    top_pkg = alias.name.split('.')[0]
                    ext_modules.add(top_pkg)

        return resolved_files, ext_modules

    def _build_parent_map(self, tree: ast.AST) -> Dict[ast.AST, ast.AST]:
        parent_map = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parent_map[child] = node
        return parent_map

    def _get_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return node.attr
        return ''

    def _get_call_name(self, node: ast.Call) -> str:
        if isinstance(node.func, ast.Name):
            return node.func.id
        if isinstance(node.func, ast.Attribute):
            return node.func.attr
        return ''

    def _find_enclosing_fast(self, parent_map, target_node, rel_path, func_ranges):
        current = target_node
        while current in parent_map:
            current = parent_map[current]
            if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef)):
                enclosing_class = parent_map.get(current)
                if isinstance(enclosing_class, ast.ClassDef):
                    return f"func:{rel_path}:{enclosing_class.name}.{current.name}"
                return f"func:{rel_path}:{current.name}"
        return f"file:{rel_path}"
