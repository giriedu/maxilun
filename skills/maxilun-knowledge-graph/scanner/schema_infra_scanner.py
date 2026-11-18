import re
from pathlib import Path
from typing import Dict, Any, Set

from .base_scanner import BaseScanner


class SchemaInfraScanner(BaseScanner):
    """
    Scans SQL schemas, Prisma models, and infrastructure/config files
    (.sql, .prisma, .yaml, .yml, .toml, .tf, .json) to extract tables,
    models, services, foreign-key relations, and file references.
    Zero external dependencies.
    """

    EXTENSIONS = {'.sql', '.prisma', '.yaml', '.yml', '.toml', '.tf', '.json'}

    SQL_TABLE_RE = re.compile(
        r'^\s*CREATE\s+(?:OR\s+REPLACE\s+)?(?:TABLE|VIEW|MATERIALIZED\s+VIEW)\s+(?:IF\s+NOT\s+EXISTS\s+)?([`"\[]?[A-Za-z0-9_.]+[`"\]]?)',
        re.IGNORECASE,
    )
    SQL_FK_RE = re.compile(
        r'\bREFERENCES\s+([`"\[]?[A-Za-z0-9_.]+[`"\]]?)',
        re.IGNORECASE,
    )
    SQL_POLICY_RE = re.compile(
        r'^\s*CREATE\s+POLICY\s+([`"\[]?[A-Za-z0-9_]+[`"\]]?)\s+ON\s+([`"\[]?[A-Za-z0-9_.]+[`"\]]?)',
        re.IGNORECASE,
    )
    PRISMA_MODEL_RE = re.compile(r'^\s*(?:model|enum)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{')
    TF_RESOURCE_RE = re.compile(r'^\s*(?:resource|data|module)\s+"([^"]+)"(?:\s+"([^"]+)")?')
    YAML_TOP_KEY_RE = re.compile(r'^([A-Za-z0-9_.-]+):\s*(?:#.*)?$')
    PATH_REF_RE = re.compile(r'([A-Za-z0-9_./-]+\.(?:py|ts|tsx|js|jsx|sql|sh|ps1|md|json|yaml|yml))')

    @staticmethod
    def _clean_ident(raw: str) -> str:
        return raw.strip().strip('`"[]')

    def scan_file(self, src_file: Path, root: Path) -> Dict[str, Any]:
        nodes = []
        edges = []
        try:
            rel = str(src_file.relative_to(root)).replace('\\', '/')
        except ValueError:
            rel = src_file.name

        ext = src_file.suffix.lower()
        file_id = f"schema:{rel}"
        is_sql_or_prisma = ext in ('.sql', '.prisma')
        nodes.append({
            'id': file_id,
            'type': 'file',
            'label': src_file.name,
            'name': src_file.stem,
            'path': rel,
            'file_type': 'schema' if is_sql_or_prisma else 'infra',
            'node_kind': 'schema' if is_sql_or_prisma else 'config',
            'source_file': rel,
            'line': 1,
        })

        try:
            # Skip huge generated lockfiles or minified JSON > 512 KB
            if src_file.stat().st_size > 512 * 1024:
                return {'nodes': nodes, 'edges': edges}
            lines = src_file.read_text(encoding='utf-8', errors='replace').splitlines()
        except Exception:
            return {'nodes': nodes, 'edges': edges}

        current_entity_id = file_id
        seen_edges: Set[tuple] = set()

        for line_idx, line in enumerate(lines, start=1):
            if ext == '.sql':
                m_tbl = self.SQL_TABLE_RE.match(line)
                if m_tbl:
                    tbl = self._clean_ident(m_tbl.group(1))
                    tbl_id = f"table:{rel}:{tbl}"
                    nodes.append({
                        'id': tbl_id,
                        'type': 'class',
                        'label': tbl,
                        'name': tbl,
                        'path': rel,
                        'file_type': 'schema',
                        'node_kind': 'table',
                        'source_file': rel,
                        'line': line_idx,
                    })
                    edges.append({'source': file_id, 'target': tbl_id, 'type': 'CONTAINS', 'confidence': 'exact'})
                    current_entity_id = tbl_id
                    continue

                m_pol = self.SQL_POLICY_RE.match(line)
                if m_pol:
                    pol = self._clean_ident(m_pol.group(1))
                    on_tbl = self._clean_ident(m_pol.group(2))
                    edges.append({
                        'source': file_id,
                        'target': f"table:*:{on_tbl}",
                        'type': 'REFERENCES',
                        'confidence': 'inferred',
                        'context': f'rls_policy:{pol}',
                        'source_file': rel,
                        'line': line_idx,
                    })

                for m_fk in self.SQL_FK_RE.finditer(line):
                    tgt_tbl = self._clean_ident(m_fk.group(1))
                    key = (current_entity_id, tgt_tbl)
                    if key not in seen_edges:
                        seen_edges.add(key)
                        edges.append({
                            'source': current_entity_id,
                            'target': f"table:*:{tgt_tbl}",
                            'type': 'REFERENCES',
                            'confidence': 'exact',
                            'context': 'foreign_key',
                            'source_file': rel,
                            'line': line_idx,
                        })

            elif ext == '.prisma':
                m_mod = self.PRISMA_MODEL_RE.match(line)
                if m_mod:
                    mod = m_mod.group(1)
                    mod_id = f"table:{rel}:{mod}"
                    nodes.append({
                        'id': mod_id,
                        'type': 'class',
                        'label': mod,
                        'name': mod,
                        'path': rel,
                        'file_type': 'schema',
                        'node_kind': 'model',
                        'source_file': rel,
                        'line': line_idx,
                    })
                    edges.append({'source': file_id, 'target': mod_id, 'type': 'CONTAINS', 'confidence': 'exact'})
                    current_entity_id = mod_id

            elif ext == '.tf':
                m_tf = self.TF_RESOURCE_RE.match(line)
                if m_tf:
                    r_name = f"{m_tf.group(1)}.{m_tf.group(2)}" if m_tf.group(2) else m_tf.group(1)
                    r_id = f"infra:{rel}:{r_name}"
                    nodes.append({
                        'id': r_id,
                        'type': 'class',
                        'label': r_name,
                        'name': r_name,
                        'path': rel,
                        'file_type': 'infra',
                        'node_kind': 'resource',
                        'source_file': rel,
                        'line': line_idx,
                    })
                    edges.append({'source': file_id, 'target': r_id, 'type': 'CONTAINS', 'confidence': 'exact'})

            elif ext in ('.yaml', '.yml'):
                m_y = self.YAML_TOP_KEY_RE.match(line)
                if m_y:
                    k = m_y.group(1)
                    k_id = f"infra:{rel}:{k}"
                    nodes.append({
                        'id': k_id,
                        'type': 'heading',
                        'label': k,
                        'path': rel,
                        'file_type': 'infra',
                        'node_kind': 'config_section',
                        'source_file': rel,
                        'line': line_idx,
                    })
                    edges.append({'source': file_id, 'target': k_id, 'type': 'CONTAINS', 'confidence': 'exact'})

            # Link file references inside infra/config files
            for m_ref in self.PATH_REF_RE.finditer(line):
                ref_path = m_ref.group(1).lstrip('./')
                if ref_path == rel or ref_path.startswith('http'):
                    continue
                key = (file_id, ref_path)
                if key not in seen_edges:
                    seen_edges.add(key)
                    edges.append({
                        'source': file_id,
                        'target': f"file:{ref_path}",
                        'type': 'REFERENCES',
                        'confidence': 'inferred',
                        'context': 'config_path_ref',
                        'source_file': rel,
                        'line': line_idx,
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
