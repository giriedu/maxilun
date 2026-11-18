#!/usr/bin/env python3
"""
Maxilun Locate — question-to-coordinates retrieval
===================================================

Turns a plain-language question, a stack trace, or a symbol name into a short
ranked list of `file:start-end` ranges with verbatim excerpts and graph leads,
in one response. The caller reads those ranges and nothing else.

Ranking is lexical and local (BM25 over symbol-bounded chunks, boosted by the
knowledge graph). No model, no network, no dependency outside the stdlib. The
calling agent supplies the semantics: it phrases the question with the words
the code is likely to use and passes extra candidates through `also`.
"""

import hashlib
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent))

try:
    from scanner.base_scanner import BaseScanner
except Exception:  # scanner package missing in a partial install
    BaseScanner = None

INDEX_VERSION = 4
INDEX_REL = Path('.maxilun') / 'cache' / 'locate-index.json'

SKIP_DIRS = {
    '.git', '.svn', '.hg', 'node_modules', 'dist', 'build', '.next', '__pycache__',
    '.venv', 'venv', 'vendor', '.maxilun', 'coverage', '.turbo', '.cache', 'target',
    '.idea', '.vscode', 'maxilun-out', 'graphify-out', 'out', 'bin', 'obj',
}

TEXT_EXT = {
    '.py', '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.go', '.rs', '.java', '.kt', '.kts',
    '.cs', '.rb', '.php', '.swift', '.c', '.h', '.cc', '.cpp', '.hpp', '.m', '.mm', '.dart',
    '.vue', '.svelte', '.astro', '.html', '.htm', '.css', '.scss', '.sass', '.less',
    '.sql', '.prisma', '.graphql', '.gql', '.proto', '.sh', '.ps1', '.bat', '.gs',
    '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.xml', '.xaml', '.gradle',
    '.md', '.mdx', '.txt', '.rst', '.rsc', '.tf', '.lua', '.gd', '.sru', '.srw', '.srd',
}
BARE_NAMES = {'dockerfile', 'makefile', 'procfile', 'jenkinsfile'}

# Secrets never enter the index or an excerpt.
SENSITIVE = re.compile(
    r'(^\.env|\.pem$|\.key$|\.p12$|\.pfx$|\.keystore$|id_rsa|id_ed25519|secret|credential|\.htpasswd)',
    re.IGNORECASE)
NOISE = re.compile(
    r'(\.min\.(js|css)$|\.map$|\.lock$|-lock\.(json|yaml)$|^pnpm-lock|^yarn\.lock$|^composer\.lock$)',
    re.IGNORECASE)
TEST_PATH = re.compile(r'(^|/)(tests?|__tests__|spec|e2e|fixtures?)(/|$)|\.(test|spec)\.|_test\.|(^|/)test[-_]',
                       re.IGNORECASE)

MAX_FILE_BYTES = 400_000
MAX_CHUNK_LINES = 60
WINDOW_LINES = 40

STOPWORDS = set("""
a an the and or of to in on at for from with by is are was be been it this that these those as
how what where which who when why does do did can could should would will i we you they there
find show me code file files function method class get all any into about using use used via
yang dan atau di ke dari untuk dengan pada adalah ini itu apa mana siapa kapan kenapa mengapa
bagaimana gimana dimana saya kita kami anda ada tidak bisa akan sudah belum juga jadi agar supaya
cari carikan tolong lihat fungsi kode berkas bagian semua setiap saat ketika lalu nya
""".split())

# Indonesian question words mapped to the English terms source code tends to use.
# Deliberately small: the calling agent adds project-specific terms through `also`.
ID_EN = {
    'masuk': ['login', 'signin', 'auth'], 'keluar': ['logout', 'signout'], 'daftar': ['register', 'signup', 'list'],
    'pengguna': ['user'], 'sandi': ['password'], 'kata': ['password'], 'akun': ['account'],
    'hapus': ['delete', 'remove', 'destroy'], 'simpan': ['save', 'store', 'persist'],
    'ubah': ['update', 'edit', 'change'], 'perbarui': ['update', 'refresh'], 'tambah': ['add', 'create', 'insert'],
    'buat': ['create', 'make', 'generate'], 'ambil': ['get', 'fetch', 'load'], 'kirim': ['send', 'submit', 'post'],
    'unggah': ['upload'], 'unduh': ['download'], 'cetak': ['print', 'export', 'pdf'],
    'bayar': ['payment', 'pay', 'checkout'], 'pembayaran': ['payment', 'billing', 'invoice'],
    'tagihan': ['invoice', 'bill'], 'harga': ['price', 'cost'], 'pesanan': ['order'], 'keranjang': ['cart'],
    'laporan': ['report'], 'surat': ['letter', 'document'], 'sertifikat': ['certificate'],
    'siswa': ['student'], 'murid': ['student'], 'guru': ['teacher'], 'kelas': ['class', 'classroom'],
    'sekolah': ['school'], 'nilai': ['grade', 'score', 'value'], 'jadwal': ['schedule'],
    'validasi': ['validate', 'validation'], 'izin': ['permission', 'authorize'], 'peran': ['role'],
    'hak': ['permission', 'access'], 'akses': ['access', 'permission'], 'kunci': ['key', 'lock', 'token'],
    'galat': ['error', 'exception'], 'kesalahan': ['error', 'exception'], 'gagal': ['fail', 'error'],
    'pesan': ['message', 'notification'], 'notifikasi': ['notification', 'notify'],
    'tampilan': ['view', 'ui', 'layout', 'render'], 'halaman': ['page', 'route'], 'tombol': ['button'],
    'formulir': ['form'], 'isian': ['form', 'input', 'field'], 'tabel': ['table'], 'kolom': ['column', 'field'],
    'baris': ['row', 'line'], 'pencarian': ['search', 'filter', 'query'], 'saring': ['filter'],
    'urut': ['sort', 'order'], 'unggahan': ['upload'], 'gambar': ['image', 'photo'],
    'basis': ['database'], 'data': ['data'], 'skema': ['schema'], 'migrasi': ['migration', 'migrate'],
    'pengaturan': ['settings', 'config'], 'konfigurasi': ['config', 'settings'],
    'rute': ['route', 'router'], 'antarmuka': ['interface', 'ui'], 'sesi': ['session'],
    'tembolok': ['cache'], 'antrean': ['queue'], 'antrian': ['queue'], 'tes': ['test'], 'uji': ['test'],
    'lambat': ['slow', 'performance', 'timeout'], 'cadangan': ['backup'], 'dasbor': ['dashboard'],
    'cek': ['check', 'verify'], 'periksa': ['check', 'verify', 'validate'], 'hitung': ['calculate', 'count', 'compute'],
    'tampil': ['show', 'render', 'display'], 'muat': ['load'], 'baca': ['read'], 'tulis': ['write'],
    'ganti': ['replace', 'change'], 'pilih': ['select', 'choose'], 'gabung': ['merge', 'join'],
    'salin': ['copy'], 'pindah': ['move'], 'tutup': ['close'], 'buka': ['open'], 'jalan': ['run', 'execute'],
    'mulai': ['start', 'init'], 'henti': ['stop'], 'ulang': ['retry', 'repeat'], 'tunggu': ['wait'],
}

ID_PREFIX = ('memper', 'meng', 'meny', 'mem', 'men', 'me', 'di', 'ber', 'ter', 'per', 'pe')
ID_SUFFIX = ('kan', 'nya', 'an', 'i')


def _id_roots(tok: str) -> List[str]:
    """Candidate Indonesian roots for dictionary lookup only (dicek -> cek, menghapus -> hapus)."""
    roots = [tok]
    for pre in ID_PREFIX:
        if tok.startswith(pre) and len(tok) - len(pre) >= 3:
            roots.append(tok[len(pre):])
    for root in list(roots):
        for suf in ID_SUFFIX:
            if root.endswith(suf) and len(root) - len(suf) >= 3:
                roots.append(root[:-len(suf)])
    return roots

DOC_EXT = ('.md', '.mdx', '.txt', '.rst')

IDENT = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')
CAMEL = re.compile(r'[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|\d+')
TRACE_FRAMES = [
    re.compile(r'File "([^"]+)", line (\d+)'),
    re.compile(r'([\w./\\@-]+\.[A-Za-z]{1,5})[:(](\d+)'),
]


def _stem(tok: str) -> str:
    if len(tok) > 5 and tok.endswith('ing'):
        return tok[:-3]
    if len(tok) > 4 and tok.endswith('ies'):
        return tok[:-3] + 'y'
    if len(tok) > 4 and tok.endswith('ed'):
        return tok[:-2]
    if len(tok) > 3 and tok.endswith('s') and not tok.endswith('ss'):
        return tok[:-1]
    return tok


STOPWORDS |= {_stem(w) for w in STOPWORDS}


def tokenize(text: str) -> List[str]:
    """Identifier-aware tokens: whole identifier plus its camelCase/snake_case parts."""
    out: List[str] = []
    for ident in IDENT.findall(text):
        whole = ident.lower().strip('_')
        if len(whole) < 2:
            continue
        parts = [p.lower() for seg in ident.split('_') for p in CAMEL.findall(seg)]
        parts = [p for p in parts if len(p) > 1 and not p.isdigit()]
        if len(parts) > 1:
            out.append(whole.replace('_', ''))
            out.extend(_stem(p) for p in parts)
        else:
            out.append(_stem(whole))
    return out


def _query_terms(question: str, also: Iterable[str]) -> Tuple[Dict[str, float], List[str]]:
    """Weighted query terms. Original words weigh 1.0, mapped translations 0.6."""
    weights: Dict[str, float] = {}
    raw_idents = [w for w in IDENT.findall(question) if len(w) > 2]
    for tok in tokenize(question):
        if tok in STOPWORDS:
            continue
        weights[tok] = max(weights.get(tok, 0.0), 1.0)
        for root in _id_roots(tok):
            for en in ID_EN.get(root, []):
                st = _stem(en)
                weights[st] = max(weights.get(st, 0.0), 0.6)
    for extra in also:
        for tok in tokenize(extra):
            weights[tok] = max(weights.get(tok, 0.0), 1.0)
        raw_idents.extend(w for w in IDENT.findall(extra) if len(w) > 2)
    return weights, raw_idents


def _node_location(node: Dict[str, Any]) -> Tuple[str, int]:
    src = str(node.get('source_file') or node.get('path') or '').replace('\\', '/')
    line = node.get('line')
    head, sep, tail = src.rpartition(':')
    if sep and tail.isdigit():
        return head, int(tail)
    return src, int(line) if isinstance(line, int) else 0


def _boundaries(graph: Dict[str, Any]) -> Dict[str, List[Tuple[int, str, str, str]]]:
    """Per file: sorted (start_line, label, type, node_id) taken from graph symbols."""
    per_file: Dict[str, List[Tuple[int, str, str, str]]] = defaultdict(list)
    for node in graph.get('nodes', []):
        if node.get('type') in ('module', 'document', None):
            continue
        rel, line = _node_location(node)
        if rel and line > 0:
            per_file[rel].append((line, str(node.get('label', '')), str(node.get('type', '')), str(node.get('id', ''))))
    for rel in per_file:
        per_file[rel].sort()
    return per_file


def _iter_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]
        for name in filenames:
            if name.startswith('.') or SENSITIVE.search(name) or NOISE.search(name):
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext in TEXT_EXT or name.lower() in BARE_NAMES:
                yield Path(dirpath) / name


def _chunk_file(lines: List[str], marks: List[Tuple[int, str, str, str]]) -> List[List[Any]]:
    """Symbol-bounded chunks; long or symbol-less spans fall back to fixed windows."""
    total = len(lines)
    spans: List[Tuple[int, int, str, str, str]] = []
    marks = [m for m in marks if m[0] <= total]
    if marks and marks[0][0] > 1:
        spans.append((1, marks[0][0] - 1, '', 'preamble', ''))
    for idx, (start, label, kind, node_id) in enumerate(marks):
        end = marks[idx + 1][0] - 1 if idx + 1 < len(marks) else total
        spans.append((start, max(start, end), label, kind, node_id))
    if not spans:
        spans.append((1, total, '', 'file', ''))

    chunks: List[List[Any]] = []
    for start, end, label, kind, node_id in spans:
        cursor = start
        while cursor <= end:
            if cursor > start:  # later windows of a long span are context, not the declaration
                kind, node_id = 'cont', ''
            stop = end if end - cursor < MAX_CHUNK_LINES else cursor + WINDOW_LINES - 1
            body = '\n'.join(lines[cursor - 1:stop])
            if body.strip():
                tf = Counter(t for t in tokenize(body) if t not in STOPWORDS)
                if tf:
                    chunks.append([cursor, stop, label, kind, node_id, dict(tf)])
            cursor = stop + 1
    return chunks


def build_index(root: Path, graph: Dict[str, Any]) -> Dict[str, Any]:
    """Incremental chunk index. Only files whose mtime, size, or symbol map changed are re-read."""
    index_path = root / INDEX_REL
    cached: Dict[str, Any] = {}
    gitignore = root / '.gitignore'
    stamp = gitignore.stat().st_mtime_ns if gitignore.is_file() else 0
    try:
        loaded = json.loads(index_path.read_text(encoding='utf-8'))
        if loaded.get('version') == INDEX_VERSION and loaded.get('gitignore') == stamp:
            cached = loaded.get('files', {})
    except Exception:
        cached = {}

    marks_by_file = _boundaries(graph)
    scanner = BaseScanner() if BaseScanner else None
    files: Dict[str, Any] = {}
    dirty = False

    for path in _iter_files(root):
        try:
            stat = path.stat()
        except OSError:
            continue
        if stat.st_size > MAX_FILE_BYTES or stat.st_size == 0:
            continue
        rel = str(path.relative_to(root)).replace('\\', '/')
        marks = marks_by_file.get(rel, [])
        sig = hashlib.sha1(repr([m[0] for m in marks]).encode()).hexdigest()[:12]
        old = cached.get(rel)
        if old and old.get('m') == stat.st_mtime_ns and old.get('s') == stat.st_size and old.get('b') == sig:
            files[rel] = old
            continue
        dirty = True
        if scanner and scanner._is_gitignored(path, root):
            files[rel] = {'m': stat.st_mtime_ns, 's': stat.st_size, 'b': sig, 'c': []}
            continue
        try:
            text = path.read_text(encoding='utf-8', errors='replace')
        except OSError:
            continue
        if '\x00' in text[:2000]:
            continue
        files[rel] = {'m': stat.st_mtime_ns, 's': stat.st_size, 'b': sig,
                      'c': _chunk_file(text.splitlines(), marks)}

    if dirty or len(files) != len(cached):
        try:
            index_path.parent.mkdir(parents=True, exist_ok=True)
            index_path.write_text(
                json.dumps({'version': INDEX_VERSION, 'gitignore': stamp, 'files': files}, separators=(',', ':')),
                encoding='utf-8')
        except OSError:
            pass  # read-only checkout: the index simply stays in memory
    return files


def _trace_frames(question: str, files: Dict[str, Any]) -> List[Tuple[str, int]]:
    frames: List[Tuple[str, int]] = []
    for pattern in TRACE_FRAMES:
        for raw, line in pattern.findall(question):
            cand = raw.replace('\\', '/').lstrip('./')
            match = cand if cand in files else next(
                (rel for rel in files if rel.endswith('/' + cand) or cand.endswith('/' + rel)
                 or rel.rsplit('/', 1)[-1] == cand.rsplit('/', 1)[-1]), None)
            if match and (match, int(line)) not in frames:
                frames.append((match, int(line)))
    return frames


def _excerpt(root: Path, rel: str, start: int, end: int, terms: Iterable[str], max_lines: int,
             focus: Optional[int] = None) -> Tuple[int, List[str]]:
    """Verbatim lines read from disk now, centred on the densest match (or the trace line)."""
    try:
        lines = (root / rel).read_text(encoding='utf-8', errors='replace').splitlines()
    except OSError:
        return start, []
    end = min(end, len(lines))
    if end - start + 1 <= max_lines:
        return start, lines[start - 1:end]
    termset = set(terms)
    hits = [sum(1 for t in set(tokenize(lines[i - 1])) if t in termset) for i in range(start, end + 1)]
    if focus and start <= focus <= end:
        best = max(start, min(focus - max_lines // 2, end - max_lines + 1))
    else:
        running = sum(hits[:max_lines])
        best_sum, best = running, start
        for offset in range(1, len(hits) - max_lines + 1):
            running += hits[offset + max_lines - 1] - hits[offset - 1]
            if running > best_sum:
                best_sum, best = running, start + offset
    return best, lines[best - 1:best - 1 + max_lines]


def locate(question: str, root: str = '.', graph: Optional[Dict[str, Any]] = None, top: int = 5,
           lines: int = 14, budget: int = 6000, also: Optional[List[str]] = None,
           include_tests: bool = False) -> Dict[str, Any]:
    root_path = Path(root).resolve()
    graph = graph or {}
    files = build_index(root_path, graph)
    weights, raw_idents = _query_terms(question, also or [])
    wants_tests = include_tests or any(t in weights for t in ('test', 'spec', 'fixture'))
    wants_docs = any(t in weights for t in ('doc', 'docs', 'readme', 'spec', 'dokumentasi', 'guide', 'changelog'))

    flat: List[Tuple[str, List[Any]]] = [(rel, ch) for rel, meta in files.items() for ch in meta.get('c', [])]
    n_chunks = max(len(flat), 1)
    avg_len = sum(sum(ch[5].values()) for _, ch in flat) / n_chunks or 1.0
    df: Counter = Counter()
    for _, ch in flat:
        for term in weights:
            if term in ch[5]:
                df[term] += 1

    exact = {w.lower() for w in raw_idents}
    scored: List[Dict[str, Any]] = []
    by_node: Dict[str, int] = {}
    for rel, ch in flat:
        start, end, label, kind, node_id, tf = ch
        length = sum(tf.values())
        label_toks = set(tokenize(label))
        path_toks = set(tokenize(rel))
        score, matched = 0.0, []
        for term, weight in weights.items():
            freq = tf.get(term, 0)
            in_label, in_path = term in label_toks, term in path_toks
            if not (freq or in_label or in_path):
                continue
            idf = math.log(1 + (n_chunks - df[term] + 0.5) / (df[term] + 0.5))
            bm = freq * 2.2 / (freq + 1.2 * (0.25 + 0.75 * length / avg_len)) if freq else 0.0
            score += weight * idf * (bm + (2.5 if in_label else 0.0) + (1.2 if in_path else 0.0))
            matched.append(term)
        if not matched:
            continue
        leaf = label.rsplit('.', 1)[-1].lower()
        if label and kind != 'cont' and (label.lower() in exact or leaf in exact):
            score += 12.0
            matched.append('=' + label)
        primary = [t for t, w in weights.items() if w >= 1.0] or list(weights)
        covered = sum(1 for t in primary if t in matched) / max(len(primary), 1)
        score *= 0.45 + 0.55 * covered
        if not wants_tests and TEST_PATH.search(rel):
            score *= 0.55
        if not wants_docs and rel.endswith(DOC_EXT):
            score *= 0.7
        if kind == 'preamble':
            score *= 0.8
        entry = {'file': rel, 'start': start, 'end': end, 'symbol': label, 'type': kind, 'node': node_id,
                 'score': score, 'matched': matched, 'coverage': covered, 'via': []}
        if node_id:
            by_node.setdefault(node_id, len(scored))
        scored.append(entry)

    # Graph expansion: neighbours of the strongest symbols inherit a fraction of their score.
    callers: Dict[str, List[str]] = defaultdict(list)
    callees: Dict[str, List[str]] = defaultdict(list)
    for edge in graph.get('edges', []):
        if edge.get('type') in ('CALLS', 'EXTENDS', 'IMPLEMENTS'):
            callers[edge.get('target', '')].append(edge.get('source', ''))
            callees[edge.get('source', '')].append(edge.get('target', ''))
    for seed in sorted(scored, key=lambda e: -e['score'])[:8]:
        if not seed['node']:
            continue
        for other in callers.get(seed['node'], []) + callees.get(seed['node'], []):
            idx = by_node.get(other)
            if idx is not None and scored[idx] is not seed:
                scored[idx]['score'] += 0.15 * seed['score']
                scored[idx]['via'].append(seed['symbol'])

    # Stack-trace frames are evidence, not guesses: pin them above lexical hits.
    pinned: List[Dict[str, Any]] = []
    for rel, line in _trace_frames(question, files):
        chunk = next((ch for ch in files[rel].get('c', []) if ch[0] <= line <= ch[1]), None)
        if chunk:
            pinned.append({'file': rel, 'start': chunk[0], 'end': chunk[1], 'symbol': chunk[2], 'type': chunk[3],
                           'node': chunk[4], 'score': 1e6 - len(pinned), 'matched': [f'trace:{line}'],
                           'coverage': 1.0, 'via': [], 'focus': line})

    ranked = pinned + sorted(scored, key=lambda e: -e['score'])
    per_file: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    order: List[str] = []
    for entry in ranked:
        bucket = per_file[entry['file']]
        if any(b['start'] == entry['start'] for b in bucket):
            continue
        if not bucket:
            order.append(entry['file'])
        if not bucket or (len(bucket) < 2 and entry['score'] >= 0.5 * bucket[0]['score']):
            bucket.append(entry)
        if len(order) > top:
            break

    node_index = {n.get('id'): n for n in graph.get('nodes', [])}

    def _where(node_id: str) -> str:
        node = node_index.get(node_id)
        if not node:
            return node_id.split(':')[-1]
        rel, line = _node_location(node)
        return f"{rel}:{line}" if line else rel

    hits: List[Dict[str, Any]] = []
    spent = 0
    for rel in order[:top]:
        for entry in per_file[rel]:
            first, body = (entry['start'], [])
            if spent < budget:
                first, body = _excerpt(root_path, rel, entry['start'], entry['end'], weights, lines, entry.get('focus'))
                spent += sum(len(b) + 8 for b in body)
            hits.append({
                'file': rel, 'range': [entry['start'], entry['end']], 'symbol': entry['symbol'],
                'type': entry['type'], 'score': round(min(entry['score'], 999.0), 2),
                'matched': sorted(set(entry['matched'])), 'via': sorted(set(entry['via']))[:3],
                'excerpt_start': first, 'excerpt': body,
                'callers': [_where(c) for c in callers.get(entry['node'], [])[:4]] if entry['node'] else [],
                'callers_total': len(callers.get(entry['node'], [])) if entry['node'] else 0,
                'callees': [c.split(':')[-1] for c in callees.get(entry['node'], [])[:5]] if entry['node'] else [],
            })

    primary = [t for t, w in weights.items() if w >= 1.0]
    seen_terms = {t for h in hits for t in h['matched']}
    missing = [t for t in primary if t not in seen_terms]
    best = ranked[0] if ranked else None
    if pinned or (best and (best['coverage'] >= 0.6 or any(m.startswith('=') for m in best['matched']))):
        confidence = 'strong'
    elif best and best['coverage'] >= 0.34:
        confidence = 'partial'
    else:
        confidence = 'weak'

    return {
        'question': question, 'confidence': confidence if hits else 'none',
        'terms': sorted(weights), 'missing_terms': missing,
        'indexed_files': len(files), 'indexed_chunks': len(flat), 'hits': hits,
    }


def render(result: Dict[str, Any]) -> str:
    hits = result['hits']
    out = [f"locate [{result['confidence']}] {len(hits)} range(s) in "
           f"{len({h['file'] for h in hits})} file(s) "
           f"(index: {result['indexed_files']} files, {result['indexed_chunks']} chunks)"]
    if not hits:
        out.append(f"No match for terms: {', '.join(result['terms']) or '(none)'}.")
        out.append("Next: rephrase with identifiers the code would use (--also a,b,c), or run a Tier 2 symbol grep.")
        return '\n'.join(out)

    out.append('')
    out.append('Read plan (read these ranges only):')
    for rank, hit in enumerate(hits, 1):
        if hit['type'] == 'cont':
            name = f"  (inside {hit['symbol']})" if hit['symbol'] else ''
        else:
            name = f"  {hit['symbol']} [{hit['type']}]" if hit['symbol'] else f"  [{hit['type']}]"
        out.append(f"  {rank}. {hit['file']}:{hit['range'][0]}-{hit['range'][1]}{name}  score {hit['score']}")

    for rank, hit in enumerate(hits, 1):
        out.append('')
        why = ', '.join(hit['matched'][:8])
        via = f"; linked to {', '.join(hit['via'])}" if hit['via'] else ''
        out.append(f"--- {rank}. {hit['file']}:{hit['range'][0]}-{hit['range'][1]}  matched: {why}{via}")
        for offset, line in enumerate(hit['excerpt']):
            out.append(f"{hit['excerpt_start'] + offset:>5}| {line}")
        if not hit['excerpt']:
            out.append('      (excerpt omitted: output budget reached; range-read if needed)')
        elif hit['excerpt_start'] + len(hit['excerpt']) - 1 < hit['range'][1]:
            out.append(f"      ... range continues to line {hit['range'][1]}")
        if hit['callers_total']:
            more = f" (+{hit['callers_total'] - len(hit['callers'])} more)" if hit['callers_total'] > len(hit['callers']) else ''
            out.append(f"      callers: {', '.join(hit['callers'])}{more}")
        if hit['callees']:
            out.append(f"      calls: {', '.join(hit['callees'])}")

    out.append('')
    if result['missing_terms']:
        out.append(f"No hit for: {', '.join(result['missing_terms'])}. "
                   f"If they matter, retry once with code-side synonyms via --also.")
    if result['confidence'] == 'weak':
        out.append("Weak match: treat the list as leads, confirm with one symbol grep before editing.")
    return '\n'.join(out).rstrip()
