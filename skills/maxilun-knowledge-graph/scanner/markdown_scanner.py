import re
from pathlib import Path
from typing import Dict, List, Any, Set

from .base_scanner import BaseScanner


class MarkdownScanner(BaseScanner):
    """
    Scans Markdown documentation (.md) to extract document structure (pages, headings)
    and infer references between documentation and code symbols.
    """

    EXTENSIONS = {'.md', '.markdown'}

    HEADING_RE = re.compile(r'^(#{1,6})\s+(.+)$')
    CODE_REF_RE = re.compile(r'`([A-Za-z_][A-Za-z0-9_\.:]{2,}(?:\(\))?)`')

    IGNORED_WORDS = frozenset({
        'true', 'false', 'null', 'undefined', 'none', 'nil',
        'get', 'post', 'put', 'patch', 'delete', 'options', 'head',
        'http', 'https', 'json', 'yaml', 'yml', 'bash', 'sh', 'python',
        'string', 'number', 'boolean', 'array', 'object', 'any', 'void',
        'npm', 'yarn', 'pnpm', 'bun', 'pip', 'cargo', 'git'
    })

    def scan_file(self, src_file: Path, root: Path) -> Dict[str, Any]:
        nodes = []
        edges = []
        try:
            rel = str(src_file.relative_to(root)).replace('\\', '/')
        except ValueError:
            rel = src_file.name

        doc_id = f"doc:{rel}"
        nodes.append({
            'id': doc_id,
            'type': 'document',
            'label': src_file.name,
            'name': src_file.stem,
            'path': rel,
            'file_type': 'document',
            'node_kind': 'page',
            'source_file': rel,
            'line': 1
        })

        try:
            lines = src_file.read_text(encoding='utf-8', errors='replace').splitlines()
        except Exception:
            return {'nodes': nodes, 'edges': edges}

        current_parent_id = doc_id
        seen_refs_per_section: Set[str] = set()

        for line_idx, line in enumerate(lines, start=1):
            h_match = self.HEADING_RE.match(line.strip())
            if h_match:
                title = h_match.group(2).strip()
                slug = re.sub(r'[^a-zA-Z0-9_\-]+', '-', title.lower()).strip('-')
                heading_id = f"heading:{rel}#{slug or f'line{line_idx}'}"
                nodes.append({
                    'id': heading_id,
                    'type': 'heading',
                    'label': title,
                    'path': rel,
                    'file_type': 'document',
                    'node_kind': 'heading',
                    'source_file': rel,
                    'line': line_idx
                })
                edges.append({
                    'source': doc_id,
                    'target': heading_id,
                    'type': 'CONTAINS',
                    'confidence': 'exact'
                })
                current_parent_id = heading_id
                seen_refs_per_section = set()
                continue

            # Find backtick code references
            for ref_match in self.CODE_REF_RE.finditer(line):
                sym = ref_match.group(1).rstrip('()').strip()
                if not sym or sym.lower() in self.IGNORED_WORDS:
                    continue
                if sym.isdigit():
                    continue

                if sym in seen_refs_per_section:
                    continue
                seen_refs_per_section.add(sym)

                # Wildcard symbol reference target
                target = f"func:*:{sym}" if '.' not in sym else f"class:*:{sym}"
                edges.append({
                    'source': current_parent_id,
                    'target': target,
                    'type': 'REFERENCES',
                    'confidence': 'inferred',
                    'confidence_score': 0.85,
                    'context': 'doc_reference',
                    'source_file': rel,
                    'line': line_idx
                })

        return {'nodes': nodes, 'edges': edges}

    def scan(self, root_path: str) -> Dict[str, Any]:
        nodes = []
        edges = []
        root = Path(root_path).resolve()

        for ext in self.EXTENSIONS:
            for src_file in root.rglob(f'*{ext}'):
                if self.should_skip(src_file, root):
                    continue
                res = self.scan_file(src_file, root)
                nodes.extend(res.get('nodes', []))
                edges.extend(res.get('edges', []))

        return {'nodes': nodes, 'edges': edges}
