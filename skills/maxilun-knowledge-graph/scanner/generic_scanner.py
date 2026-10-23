import re
from pathlib import Path
from typing import Dict, Any

from .base_scanner import BaseScanner


class GenericScanner(BaseScanner):
    EXTENSIONS = {'.go', '.rs', '.java', '.kt', '.cs', '.rb', '.php', '.swift', '.c', '.cpp', '.h', '.hpp'}

    PATTERNS = {
        'function': re.compile(
            r'(?:pub(?:lic)?\s+|priv(?:ate)?\s+|prot(?:ected)?\s+|static\s+|async\s+|fn\s+|func\s+|def\s+|fun\s+|void\s+|int\s+|string\s+)?'
            r'(?:fn|func|function|def|fun|void|int|string|bool)\s+(\w+)\s*\(',
            re.MULTILINE
        ),
        'class': re.compile(
            r'(?:pub(?:lic)?\s+|abstract\s+|sealed\s+|open\s+)?(?:class|struct|enum)\s+(\w+)',
            re.MULTILINE
        ),
        'import_go': re.compile(r'^\s*(?:import\s+(?:"([^"]+)"|(\w+))|"([^"]+)")', re.MULTILINE),
        'import_rust': re.compile(r'^\s*use\s+([\w:]+(?:::\{[^}]*\})?)', re.MULTILINE),
        'import_java': re.compile(r'^\s*import\s+([\w.]+)\s*;', re.MULTILINE),
        'import_cs': re.compile(r'^\s*using\s+([\w.]+)\s*;', re.MULTILINE),
        'import_rb': re.compile(r'^\s*(?:require|require_relative)\s+[\'"]([^\'"]+)[\'"]', re.MULTILINE),
        'import_php': re.compile(r'^\s*(?:use|require_once|include_once)\s+([\w\\]+)\s*;', re.MULTILINE),
        'import_c': re.compile(r'^\s*#include\s+[<"]([^>"]+)[>"]', re.MULTILINE),
        'import_swift': re.compile(r'^\s*import\s+(\w+)', re.MULTILINE),
    }

    LANG_IMPORT_MAP = {
        '.go': 'import_go', '.rs': 'import_rust', '.java': 'import_java',
        '.kt': 'import_java', '.cs': 'import_cs', '.rb': 'import_rb',
        '.php': 'import_php', '.swift': 'import_swift',
        '.c': 'import_c', '.cpp': 'import_c', '.h': 'import_c', '.hpp': 'import_c',
    }

    SKIP_DIRS = frozenset({
        'vendor', 'target', 'build', 'dist', 'node_modules', '__pycache__',
        '.git', '.svn', '.hg', '.tox', '.eggs', '*.egg-info',
    })

    def _should_skip(self, parts):
        for part in parts:
            if part.startswith('.'):
                return True
            if part in self.SKIP_DIRS:
                return True
        return False

    def scan(self, root_path: str) -> Dict[str, Any]:
        nodes = []
        edges = []
        root = Path(root_path).resolve()

        for ext in self.EXTENSIONS:
            for src_file in root.rglob(f'*{ext}'):
                if self.should_skip(src_file, root):
                    continue

                rel_path = str(src_file.relative_to(root))
                try:
                    source = src_file.read_text(encoding='utf-8', errors='replace')
                except Exception:
                    continue

                lines = source.splitlines()
                file_node_id = f"file:{rel_path}"
                nodes.append({
                    'id': file_node_id,
                    'label': src_file.name,
                    'type': 'module',
                    'source_file': rel_path,
                    'snippet': f'// {rel_path}\n// {len(lines)} lines'
                })

                for match in self.PATTERNS['class'].finditer(source):
                    class_name = match.group(1)
                    line_no = source[:match.start()].count('\n') + 1
                    class_id = f"class:{rel_path}:{class_name}"

                    snippet_end = min(line_no + 4, len(lines))
                    nodes.append({
                        'id': class_id,
                        'label': class_name,
                        'type': 'class',
                        'source_file': f"{rel_path}:{line_no}",
                        'snippet': '\n'.join(lines[line_no - 1:snippet_end])
                    })
                    edges.append({'source': file_node_id, 'target': class_id, 'type': 'DEFINES'})

                func_names = []
                for match in self.PATTERNS['function'].finditer(source):
                    func_name = match.group(1)
                    line_no = source[:match.start()].count('\n') + 1
                    func_id = f"func:{rel_path}:{func_name}"
                    func_names.append(func_name)

                    snippet_end = min(line_no + 3, len(lines))
                    nodes.append({
                        'id': func_id,
                        'label': func_name,
                        'type': 'function',
                        'source_file': f"{rel_path}:{line_no}",
                        'snippet': '\n'.join(lines[line_no - 1:snippet_end])
                    })
                    edges.append({'source': file_node_id, 'target': func_id, 'type': 'DEFINES'})

                # Best-effort CALLS: grep for known func names appearing as calls
                # Only cross-reference within discovered function names to reduce noise
                call_pattern = re.compile(
                    r'(?<![\w.])(' + '|'.join(re.escape(n) for n in func_names) + r')\s*\(',
                    re.MULTILINE
                ) if func_names else None

                if call_pattern:
                    seen_calls = set()
                    for call_match in call_pattern.finditer(source):
                        callee_name = call_match.group(1)
                        call_line = source[:call_match.start()].count('\n') + 1
                        edge_key = f"{file_node_id}->func:*:{callee_name}:CALLS:{call_line}"
                        if edge_key not in seen_calls:
                            seen_calls.add(edge_key)
                            edges.append({'source': file_node_id, 'target': f"func:*:{callee_name}", 'type': 'CALLS'})

                import_key = self.LANG_IMPORT_MAP.get(ext)
                if import_key and import_key in self.PATTERNS:
                    for match in self.PATTERNS[import_key].finditer(source):
                        module_path = next((g for g in match.groups() if g), None)
                        if module_path:
                            module_name = module_path.split('/')[-1].split('.')[0].split('::')[0]
                            edges.append({'source': file_node_id, 'target': f"ext:{module_name}", 'type': 'IMPORTS'})

        return {'nodes': nodes, 'edges': edges}
