# AI-Ready Documentation (`llms.txt`, `llms-full.txt`) & High-Density README Reference

Gunakan referensi ini saat menyusun `README.md`, `/llms.txt`, dan `/llms-full.txt` agar dapat dikonsumsi manusia dalam `< 60 detik` sekaligus hemat token bagi agen AI/LLM.

---

## 1. Arsitektur `llms.txt` & `llms-full.txt`

Mengikuti spesifikasi standar `llms.txt` (dan terintegrasi dengan audit `maxilun-seo-audit`):
- **`/llms.txt` (Indeks Peta Konteks)**: Berisi H1 nama proyek, blockquote 1 kalimat fungsi sistem, diikuti daftar tautan markdown yang dikelompokkan berdasarkan prioritas. Setiap tautan wajib memiliki deskripsi 1 kalimat tentang **kapan agen harus membaca file tersebut**.
- **`/llms-full.txt` (Bundel Konteks Tunggal)**: Menggabungkan isi dokumen inti (`PRD.md`, `ARCHITECTURE.md`, `TECHSTACK.md`, kontrak API utama) tanpa duplikasi navigasi, tanpa badge dekoratif, dan tanpa HTML yang tidak perlu.

### Template `/llms.txt` Produksi

```markdown
# [Nama Proyek]

> [Satu kalimat padat: apa yang dilakukan sistem ini, stack utamanya, dan batas domainnya.]

## Quick Context Rules (Baca Sebelum Edit Kode)
- Stack: [Contoh: Next.js 15 App Router, TypeScript strict, PostgreSQL 16 + Drizzle ORM]
- Moneter & Angka: Semua nominal uang disimpan dalam satuan terkecil (`BIGINT` IDR), jangan gunakan `float`.
- Validasi & Auth: Semua mutasi melewati validasi Zod di server dan pemeriksaan kepemilikan tenant (`tenant_id`).

## Core Project Documents (`docs/`)
- [Product Requirements (PRD)](docs/PRD.md): Tujuan produk, persona pengguna, fitur MVP, non-goals, dan metrik keberhasilan.
- [System Architecture](docs/ARCHITECTURE.md): Diagram C4, batas modul (module boundaries), alur data, dan daftar ADR.
- [Tech Stack & Env](docs/TECHSTACK.md): Versi runtime, kebijakan dependensi, dan tabel environment variables wajib.
- [Design System & Tokens](docs/DESIGN.md): Token warna OKLCH, skala tipografi, grid 4px, dan aturan 4 state UI (`maxilun-craft`).
- [Security & Threat Model](docs/SECURITY.md): Matriks STRIDE, kebijakan sesi/JWT, RBAC, dan perlindungan PII (`maxilun-sentinel`).
- [Coding Styleguide](docs/STYLEGUIDE.md): Konvensi penamaan, struktur import, pola error handling, dan daftar larangan keras.

## API & Operations
- [OpenAPI Specification](docs/openapi.yaml): Kontrak endpoint REST, skema payload, dan struktur error RFC 9457.
- [Operational Runbook](docs/runbooks/core-service.md): Prosedur healthcheck, triase alert produksi, dan langkah rollback aman.
- [Onboarding Guide](docs/ONBOARDING.md): Urutan setup lokal, migrasi database, dan verifikasi test suite.
```

---

## 2. Standar High-Density `README.md`

`README.md` di root repositori harus bebas dari basa-basi pemasaran. Struktur wajib:

1. **Judul + Satu Kalimat Fungsional**: Apa yang dilakukan repositori ini dan untuk siapa.
2. **Arsitektur & Peta Direktori Ringkas**: Pohon folder yang menjelaskan tanggung jawab tiap direktori utama.
3. **Quickstart (Copy-Paste Ready)**: Perintah berurutan dari clone, install, setup `.env`, migrasi DB, hingga server menyala di bawah 60 detik.
4. **Tabel Environment Variables**: Nama variabel, wajib/opsional, contoh nilai aman, dan fungsinya.
5. **Perintah Verifikasi & Build**: Perintah eksak untuk `typecheck`, `lint`, `test`, dan `build`.
6. **Tautan ke `docs/`**: Mengarahkan pembaca dan agen AI ke `docs/PRD.md`, `docs/ARCHITECTURE.md`, dan `/llms.txt`.

### Checklist Kualitas Dokumentasi (Delivery Gate `maxilun-docsmith`)
- [ ] Semua perintah CLI di dalam dokumen telah dicocokkan dengan `package.json` / `Makefile` / `pyproject.toml` aktual di repositori (`[CONFIRMED]`).
- [ ] Semua nama environment variable di tabel dokumentasi cocok dengan `.env.example` dan pembacaan `process.env` / `os.environ` di kode.
- [ ] Tidak ada klaim performa atau keamanan tanpa angka/mekanisme nyata.
- [ ] Jika dokumen memuat spesifikasi fitur/PRD dengan komponen UI, matriks 4 state UI dan catatan referensi desain (`../maxilun-craft/references/design-md/index.md`) sudah disertakan.
