import re
from pathlib import Path
from typing import Dict, Any

from .base_scanner import BaseScanner


class AssetScanner(BaseScanner):
    """
    Indexes multi-modal non-code assets (PDFs, diagrams, images) into the
    knowledge graph so documentation, specs, and visual assets are discoverable
    alongside source code. Zero external dependencies.
    """

    EXTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif'}

    SVG_TEXT_RE = re.compile(r'<(?:title|desc|text)[^>]*>([^<]{2,80})</(?:title|desc|text)>', re.IGNORECASE)
    PDF_TITLE_RE = re.compile(rb'/Title\s*\(([^)]{2,120})\)')

    def scan_file(self, src_file: Path, root: Path) -> Dict[str, Any]:
        nodes = []
        edges = []
        try:
            rel = str(src_file.relative_to(root)).replace('\\', '/')
        except ValueError:
            rel = src_file.name

        ext = src_file.suffix.lower()
        asset_id = f"asset:{rel}"
        kind = 'pdf' if ext == '.pdf' else ('diagram' if ext == '.svg' else 'image')

        try:
            size_bytes = src_file.stat().st_size
        except OSError:
            size_bytes = 0

        title = src_file.stem
        extracted_labels = []

        if ext == '.svg' and size_bytes <= 512 * 1024:
            try:
                text = src_file.read_text(encoding='utf-8', errors='replace')
                for m in self.SVG_TEXT_RE.finditer(text):
                    lbl = m.group(1).strip()
                    if lbl and lbl not in extracted_labels:
                        extracted_labels.append(lbl)
                    if len(extracted_labels) >= 8:
                        break
            except Exception:
                pass
        elif ext == '.pdf' and size_bytes <= 5 * 1024 * 1024:
            try:
                raw = src_file.read_bytes()[:65536]
                m_title = self.PDF_TITLE_RE.search(raw)
                if m_title:
                    decoded = m_title.group(1).decode('latin-1', errors='replace').strip()
                    if decoded:
                        title = decoded
            except Exception:
                pass

        nodes.append({
            'id': asset_id,
            'type': 'document',
            'label': src_file.name,
            'name': title,
            'path': rel,
            'file_type': 'asset',
            'node_kind': kind,
            'size_bytes': size_bytes,
            'metadata_labels': extracted_labels,
            'source_file': rel,
            'line': 1,
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
