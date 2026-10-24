# GitHub Release Guide

## Cara Buat Release Baru

### Metode Otomatis (Recommended)

Release dibuat otomatis saat tag `v*.*.*` di-push ke repo:

```bash
# Ganti nilai ini untuk rilis yang sedang dibuat; CHANGELOG.md harus memiliki section yang sama.
RELEASE_VERSION=1.0.0

# Pastikan semua perubahan sudah di-commit dan push ke main
git add .
git commit -m "chore: release v${RELEASE_VERSION}"
git push origin main

# Buat dan push tag — ini yang men-trigger workflow release.yml
git tag "v${RELEASE_VERSION}"
git push origin "v${RELEASE_VERSION}"
```

GitHub Actions akan:
1. Ambil section `## [RELEASE_VERSION]` yang cocok dengan tag dari `CHANGELOG.md`
2. Buat GitHub Release dengan judul yang memakai tag tersebut
3. Isi body release dari CHANGELOG section tersebut
4. Publish otomatis (bukan draft)

### Metode Manual (via GitHub UI)

1. Buka: https://github.com/giriedu/maxilun/releases/new
2. Tag: pilih atau buat tag versi yang akan dirilis, misalnya `v1.0.0`
3. Title: gunakan nama produk dan tag tersebut
4. Body: salin section versi yang sama dari `CHANGELOG.md`
5. Klik "Publish release"

---

## Update "About" di GitHub Repository

GitHub "About" (deskripsi di sidebar) **tidak bisa diset via file** — harus manual:

1. Buka: https://github.com/giriedu/maxilun
2. Klik ikon ⚙️ (gear) di sebelah kanan "About"
3. Isi form:
   - **Description**: `AI engineering co-pilot — 18 specialist skills, 100 UI design references, graph code discovery, programmatic motion video & evidence-based orchestration`
   - **Website**: `https://skills.sh/giriedu/maxilun`
   - **Topics**: `ai-skills`, `claude-code`, `antigravity`, `cursor`, `codex`, `zed`, `termul`, `knowledge-graph`, `purity-engine`, `motion-design`, `programmatic-video`, `design-system`, `openapi`, `project-scaffold`
4. Klik "Save changes"

---

## Riwayat Release

| Tag | Tanggal | Highlights |
|---|---|---|
| v1.0.0 | 2026-10-24 | Initial production release — 18 specialists, 100 brand design corpus, motion video studio pipeline, Knowledge Graph, Purity Gate & evidence-based orchestration |
