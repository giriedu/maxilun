# GitHub Release Guide

## Cara Buat Release Baru

### Metode Otomatis (Recommended)

Release dibuat otomatis saat tag `v*.*.*` di-push ke repo:

```bash
# Pastikan semua perubahan sudah di-commit dan push ke main
git add .
git commit -m "chore: release v1.0.0"
git push origin main

# Buat dan push tag — ini yang men-trigger workflow release.yml
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions akan:
1. Ambil section `## [1.0.0]` dari `CHANGELOG.md`
2. Buat GitHub Release dengan judul "Maxilun v1.0.0"
3. Isi body release dari CHANGELOG section tersebut
4. Publish otomatis (bukan draft)

### Metode Manual (via GitHub UI)

1. Buka: https://github.com/giriedu/maxilun/releases/new
2. Tag: pilih atau buat `v1.0.0`
3. Title: `Maxilun v1.0.0`
4. Body: copy dari `CHANGELOG.md` section `## [1.0.0]`
5. Klik "Publish release"

---

## Update "About" di GitHub Repository

GitHub "About" (deskripsi di sidebar) **tidak bisa diset via file** — harus manual:

1. Buka: https://github.com/giriedu/maxilun
2. Klik ikon ⚙️ (gear) di sebelah kanan "About"
3. Isi form:
   - **Description**: `AI engineering co-pilot — 18 specialist skills, knowledge graph foundation, zero AI slop`
   - **Website**: `https://skills.sh/giriedu/maxilun`
   - **Topics**: `ai-skills`, `claude-code`, `antigravity`, `cursor`, `codex`, `zed`, `termul`, `knowledge-graph`, `purity-engine`, `nextjs`, `project-scaffold`
4. Klik "Save changes"

---

## Riwayat Release

| Tag | Tanggal | Highlights |
|---|---|---|
| v1.0.0 | 2026-10-22 | First stable release — 18 specialist skills, MSAL namespace, Knowledge Graph, 4 engines |
