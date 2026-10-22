#!/usr/bin/env python3
"""Peta repo cepat tanpa dependensi: bahasa, titik masuk, dan file yang paling banyak diimpor.

Pakai: python3 repomap.py [path] [--top N]
Hanya impor relatif/lokal yang dihitung. Impor dinamis tidak terdeteksi.
"""
import ast, os, re, sys
from collections import Counter, defaultdict

SKIP = {".git", "node_modules", "dist", "build", ".next", "__pycache__", ".venv", "venv", "vendor", ".maxilun", "coverage"}
JS_EXT = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}
JS_IMPORT = re.compile(r"""(?:import\s[^'"]*?from\s*|import\s*|require\(\s*|export\s[^'"]*?from\s*)['"]([^'"]+)['"]""")
ENTRY_NAMES = {"main.py", "app.py", "manage.py", "index.js", "index.ts", "main.ts", "main.js", "server.js", "App.jsx", "App.tsx", "main.go", "Code.gs", "package.json", "pyproject.toml", "Dockerfile"}


def walk(root):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP and not x.startswith(".")]
        for f in files:
            yield os.path.join(d, f)


def resolve_js(src, spec, files):
    if not spec.startswith("."):
        return None
    base = os.path.normpath(os.path.join(os.path.dirname(src), spec))
    for cand in [base] + [base + e for e in JS_EXT] + [os.path.join(base, "index" + e) for e in JS_EXT]:
        if cand in files:
            return cand


def resolve_py(src, node, root, files):
    names = []
    if isinstance(node, ast.ImportFrom):
        base = os.path.dirname(src) if node.level else root
        for _ in range(max(node.level - 1, 0)):
            base = os.path.dirname(base)
        mod = (node.module or "").replace(".", os.sep)
        names.append(os.path.join(base, mod))
        names += [os.path.join(base, mod, a.name) for a in node.names]
    else:
        names += [os.path.join(root, a.name.replace(".", os.sep)) for a in node.names]
    out = []
    for n in names:
        for cand in (n + ".py", os.path.join(n, "__init__.py")):
            if os.path.normpath(cand) in files:
                out.append(os.path.normpath(cand))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 10
    if "--top" in sys.argv and args and args[-1] == str(top):
        args.pop()
    root = os.path.normpath(args[0] if args else ".")
    files = {os.path.normpath(f) for f in walk(root)}
    ext = Counter(os.path.splitext(f)[1] or "(tanpa ekstensi)" for f in files)
    deps = defaultdict(set)
    for f in files:
        e = os.path.splitext(f)[1]
        try:
            text = open(f, encoding="utf-8", errors="ignore").read() if e in JS_EXT | {".py"} else ""
        except OSError:
            continue
        if e in JS_EXT:
            for spec in JS_IMPORT.findall(text):
                t = resolve_js(f, spec, files)
                if t:
                    deps[f].add(t)
        elif e == ".py":
            try:
                for n in ast.walk(ast.parse(text)):
                    if isinstance(n, (ast.Import, ast.ImportFrom)):
                        deps[f].update(resolve_py(f, n, root, files))
            except SyntaxError:
                pass
    indeg = Counter(t for ts in deps.values() for t in ts)
    print(f"# Peta: {root}\n\nFile: {len(files)}")
    print("Ekstensi: " + ", ".join(f"{k} {v}" for k, v in ext.most_common(8)))
    entries = sorted(f for f in files if os.path.basename(f) in ENTRY_NAMES)
    print("\n## Titik masuk / konfigurasi")
    print("\n".join(f"- {e}" for e in entries[:15]) or "- (tidak terdeteksi)")
    print(f"\n## Paling banyak diimpor (hub, {top} teratas)")
    print("\n".join(f"- {f} ({n} pengimpor)" for f, n in indeg.most_common(top)) or "- (tidak ada impor lokal terdeteksi)")
    print("\n## Folder teratas")
    tops = Counter(os.path.relpath(f, root).split(os.sep)[0] for f in files if os.sep in os.path.relpath(f, root))
    print("\n".join(f"- {d}/ ({n} file)" for d, n in tops.most_common(10)))
    print("\nCatatan: hanya impor statis lokal (js/ts/py). Impor dinamis, refleksi, dan string rute perlu dicek manual.")


if __name__ == "__main__":
    main()
