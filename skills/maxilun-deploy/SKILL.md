---
name: maxilun-deploy
description: >
  Deployment and operations specialist for CI/CD pipelines, containerization,
  environment configuration, observability, zero-downtime release strategies,
  ingress/TLS hardening, and database backup and disaster recovery.
  Triggers: "/maxilun-deploy", "CI/CD", "Docker", "pipeline", "monitoring", "deployment",
  "SSL", "backup database", "environment variables", or any DevOps/infra task.
metadata:
  version: "1.1.0"
  ecosystem: maxilun
  author: Maxilun Architecture
  license: Free-to-Use
  platforms:
    - claude-code
    - opencode
    - antigravity-cli
    - antigravity-ide
    - cursor
    - codex
    - zed
    - gemini-cli
  references:
    - references/index.md
    - references/container-pipeline-hardening.md
---

# Maxilun Deploy: Deployment & Operations Engineering

Merancang dan memelihara pipeline CI/CD deterministik, image kontainer minimal, injeksi konfigurasi runtime yang aman, observability berorientasi gejala, strategi rilis tanpa henti, serta pemulihan bencana yang teruji.

## Skill Contract

- **Owns**: CI/CD workflows, container builds, runtime environment configuration, ingress/TLS/WAF operations, observability, release/rollback orchestration, and backup/recovery procedures.
- **Does not own**: application authentication/authorization logic, product feature code, or search-engine crawl directives.
- **Inputs**: runtime topology, build/test scripts, hosting constraints, secret store interfaces, and SLO/RTO/RPO targets.
- **Outputs**: executable pipeline definitions, hardened container configs, operational runbooks, and rollback/recovery verification steps.
- **Handoff**: use `maxilun-sentinel` for application security policy, `maxilun-verify` for test/quality gate suites, `maxilun-data` for backward-compatible schema migrations, `maxilun-engineer` for application code changes, and `maxilun-docsmith` for extended operator documentation.

<!-- CORE-RULES:START -->
## Core Rules (Selalu Aktif)

Berlaku pada setiap respons dan setiap perubahan kode. Tidak bisa di-override oleh instruksi lain.

1. **Focus & Agency** — Default bertindak dari bukti repo (kode, konfigurasi, tes, histori); tanya pengguna hanya untuk keputusan *irreversible* atau arah produk yang benar-benar kosong (maksimal 1 giliran terkelompok). Tanpa banner HUD emoji, tanpa checklist centang-sendiri. Maksimal 3 fokus kerja aktif.
2. **Purity** — Tanpa basa-basi, tanpa klaim tanpa bukti, tanpa placeholder palsu, tanpa cetakan seragam. Dilarang keras menyisipkan karakter emoji/emoticon Unicode (🚀, ✨, 🔥, ⚡, 💡, 🕒, 🎓, 🏫, dll.) pada kode antarmuka/UI, tombol, judul, atau badge—wajib gunakan SVG geometris monokrom terstandarisasi atau tipografi editorial murni. Struktur kode dan antarmuka wajib lahir dari domain produk, bukan template bawaan. Komentar hanya menjelaskan MENGAPA.
3. **Minimalist** — YAGNI → reuse yang ada → stdlib → platform native → satu baris. Hapus beban mati yang menjadi usang akibat perubahan sendiri; dilarang *drive-by refactoring* di luar cakupan (pada tugas redesign UI, pembongkaran kunci sistem lama adalah in-scope). Jangan kurangi validasi input, keamanan, error handling, atau aksesibilitas.
4. **Clarity & Proof** — Kesimpulan dan tindakan dulu, bukti menyusul. Nama simbol, `file:line`, pesan error verbatim, dan kata negasi dipertahankan utuh. Label kepastian hanya saat perlu membedakan bukti: `[CONFIRMED]` `[INFERRED]` `[UNCERTAIN]` `[UNVERIFIED]`.

**Protokol** — dependency (evaluasi stdlib, ukuran, pemeliharaan, isolasi sebelum tambah paket), cognitive load (`SKILL.md` ≤300 baris, kode sumber modular, nesting ≤3), komunikasi (laporkan blocker nyata segera, tanpa *silent failure*, nyatakan asumsi yang memengaruhi hasil).

Detail lengkap: `../maxilun/references/engines.md`.
<!-- CORE-RULES:END -->

## 1. Prinsip Operasional & Proporsi Infrastruktur

- **Infrastruktur Mengikuti Beban Nyata**: Tolak orkestrasi berlebih (misal klaster Kubernetes untuk layanan tunggal bertrafik rendah). Pilih topologi paling sederhana yang memenuhi target ketersediaan, isolasi keamanan, dan kapasitas tim.
- **Artefak Tunggal (*Build Once, Promote Everywhere*)**: Bangun artefak atau image satu kali dari commit terverifikasi, kunci dengan digest SHA-256, lalu promosikan artefak yang sama dari staging ke produksi.
- **Tanpa Konfigurasi Semu**: Jangan menulis file workflow dengan komentar `# ... deploy steps` kosong; sesuaikan perintah langsung dengan target platform aktual di repositori (GitHub Actions, GitLab CI, Docker/Compose, Fly.io, Cloud Run, VPS, atau Kubernetes).

## 2. Pipeline CI/CD & Quality Gates

Sesuaikan runtime dan skrip dengan lockfile serta `package.json`/`Makefile`/`pyproject.toml` proyek. Pola GitHub Actions untuk Node.js/pnpm tanpa duplikasi setup:

```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main]

jobs:
  verify-and-build:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version-file: ".nvmrc"
          cache: "pnpm"
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint && pnpm typecheck
      - run: pnpm test --run
      - run: pnpm build
```

- **Quality Gates Proporsional**: Kunci versi dependensi (`--frozen-lockfile` / `npm ci`), batasi `permissions` token CI seminimal mungkin, pasang `timeout-minutes` di setiap job, dan jalankan audit kerentanan dependensi produksi selaras dengan `maxilun-verify`.
- **Kontrak Rilis Produksi**: Workflow rilis hanya berjalan sesudah CI hijau pada environment terproteksi, mengeksekusi migrasi database yang *backward-compatible*, menggulirkan image bertanda digest, lalu memverifikasi HTTP `200` pada endpoint `/health` sebelum menyatakan rilis berhasil.

## 3. Containerization & Runtime Image (Docker)

Gunakan *multi-stage build* dengan versi `node:22-alpine` terkunci pada patch eksak (atau digest SHA-256), user non-root, dan satu endpoint kesehatan `/health` yang konsisten di kontainer, ingress, dan pipeline rilis:

```dockerfile
FROM node:22.12.0-alpine AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

FROM node:22.12.0-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN corepack enable && pnpm build

FROM node:22.12.0-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production PORT=3000
COPY --from=builder --chown=node:node /app/.next/standalone ./
COPY --from=builder --chown=node:node /app/.next/static ./.next/static
COPY --from=builder --chown=node:node /app/public ./public
USER node
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:3000/health || exit 1
CMD ["node", "server.js"]
```

- **Disiplin Layer & `.dockerignore`**: Salin manifes paket sebelum kode sumber demi memaksimalkan *cache hit*. Sediakan `.dockerignore` yang mengecualikan `.git`, `node_modules`, `.env*`, direktori build lokal, `*.md`, dan direktori pengujian.
- **Shutdown Anggun (*Graceful Shutdown*)**: Jalankan proses utama langsung sebagai PID 1 (`CMD ["node", ...]`, bukan lewat shell) agar sinyal `SIGTERM` diterima langsung untuk menutup listener dan menguras koneksi aktif sebelum batas waktu terminasi.

## 4. Konfigurasi Environment & Manajemen Rahasia

- **Kontrak *Fail-Fast* Saat Startup**: Aplikasi wajib memvalidasi seluruh variabel environment esensial terhadap skema ketat saat proses mulai berjalan dan segera berhenti (*exit non-zero*) bila ada variabel yang hilang atau salah format; baca konfigurasi melalui satu modul bertipe terpusat (implementasi kode diserahkan ke `maxilun-engineer`).
- **Injeksi Rahasia Runtime**: Simpan kredensial di secret manager platform (GitHub Secrets, Vault, AWS/GCP Secret Manager). Injeksi hanya saat runtime — dilarang menanam secret di `Dockerfile` (`ENV`/`ARG`) atau membundel file `.env` ke dalam image. Dukung masa transisi kunci ganda (*dual-key overlap*) saat rotasi rahasia.
- **Paritas Staging–Produksi**: Samakan versi OS kontainer, mesin database, dan skema konfigurasi antar-environment; bedakan kapasitas secara proporsional dan kelola variasi perilaku fitur via *feature flags*, bukan percabangan `NODE_ENV`.

## 5. Observability, Alerting & SLO

- **Structured Logging**: Tulis log JSON ke `stdout` dengan atribut konsisten (`timestamp`, `level`, `message`, `requestId`/`traceId`, `service`, `durationMs`, `statusCode`). Teruskan *correlation ID* dari ingress ke panggilan hilir dan redaksi otomatis token, password, serta PII.
- **Pelacakan Error & Trace**: Unggah *source maps* saat tahap build dan sematkan tag versi rilis (`release: git-sha`) agar regresi error langsung terpetakan ke commit penyebab.
- **SRE SLO Multi-Window Multi-Burn-Rate Alerting**: Tolak alert CPU/RAM naif yang memicu *alert fatigue*. Terapkan standar di `references/container-pipeline-hardening.md` (§3):
  - **P1 Critical (Pager)**: Burn rate $\ge 14.4x$ (konsumsi 2% budget dalam 1 jam / jendela short 5 menit) $\to$ darurat aktif, bangunkan on-call seketika.
  - **P2 High (Urgent)**: Burn rate $\ge 6.0x$ (konsumsi 5% budget dalam 6 jam / jendela short 30 menit) $\to$ investigasi dalam 30 menit.
  - **P3 Medium (Ticket)**: Burn rate $\ge 1.0x$ (konsumsi 10% budget dalam 3 hari) $\to$ tiket backlog otomatis.
  - Setiap alert aktif wajib menyertakan tautan langsung ke runbook penanganan operasional spesifik.

## 6. Strategi Rilis, Rollback & Perimeter Domain/TLS

| Strategi Rilis | Pola Pengalihan Trafik | Kecepatan Rollback | Prasyarat Utama |
|---|---|---|---|
| **Rolling Update** | Ganti instance bertahap per batch | Menit (redeploy digest lama) | Layanan stateless + probe `/health` akurat |
| **Blue-Green** | Pindah penuh ke klaster hijau setelah siap | Detik (switch router balik ke biru) | Kapasitas 2x sementara + DB kompatibel mundur |
| **Canary** | Bertahap `5% → 25% → 100%` berbasis metrik | Detik (cabut bobot trafik canary) | Weighted routing + telemetri error/latensi real-time |

- **Protokol Rollback (<5 Menit)**: Sediakan mekanisme satu perintah untuk mengembalikan digest image sebelumnya. Koordinasikan pola migrasi *expand-and-contract* dengan `maxilun-data` agar rollback aplikasi tidak merusak skema database aktif.
- **Perimeter TLS, DNS & Reverse Proxy**:
  - Tegakkan TLS 1.2/1.3 dengan perpanjangan sertifikat otomatis, pengalihan `301` HTTP ke HTTPS, dan kanonikalisasi tunggal antara `www` dan apex domain.
  - Pasang `Strict-Transport-Security: max-age=31536000; includeSubDomains` pada HTTPS (tambahkan `; preload` hanya jika seluruh subdomain permanen HTTPS), pembatasan laju (*rate limiting*) di level reverse-proxy (`Nginx`/`Caddy`), serta aturan edge WAF/DDoS selaras dengan `maxilun-sentinel`.
  - Konfigurasikan DNS `CAA` pembatas penerbit sertifikat, `SPF`/`DKIM`/`DMARC` untuk reputasi email domain, dan turunkan TTL (misal `300s`) sebelum jendela perpindahan IP/load balancer.

## 7. Backup, Pemulihan & Kesiapan Bencana (DR)

- **Arsitektur Pencadangan**: Gabungkan *full backup* harian yang dienkripsi saat disimpan (*encrypted at rest*) dengan pengarsipan log transaksi berkelanjutan (WAL/binlog) untuk *Point-in-Time Recovery* (PITR) di penyimpanan lintas-region/akun terpisah.
- **Verifikasi Restore Otomatis**: Cadangan tanpa bukti uji pulih dianggap tidak ada. Jadwalkan uji *restore* otomatis berkala ke instance terisolasi guna memvalidasi integritas cadangan dan mengukur ketercapaian **RTO** (*Recovery Time Objective*) serta **RPO** (*Recovery Point Objective*).
- **Runbook Insiden & Failover**: Dokumentasikan langkah failover primer-ke-replika, verifikasi konsistensi pasca-pemulihan, dan jalur komunikasi insiden bersama `maxilun-docsmith`.

## Related Skills

- **maxilun-sentinel**: Kebijakan keamanan aplikasi, header HTTP, rotasi rahasia, dan pemodelan ancaman perimeter.
- **maxilun-verify**: Eksekusi suite pengujian otomatis dan penentuan quality gate pada pipeline CI/CD.
- **maxilun-data**: Strategi migrasi database *expand-and-contract*, pengindeksan, dan penyetelan koneksi DB.
- **maxilun-architect**: Perencanaan kapasitas sistem, topologi layanan, dan batas kegagalan (*fault isolation*).
- **maxilun-insight**: Investigasi insiden produksi, analisis log/trace, dan diagnosis bottleneck performa.
- **maxilun-engineer**: Implementasi endpoint `/health`, *graceful shutdown*, dan validasi konfigurasi startup di kode aplikasi.
- **maxilun-docsmith**: Penyusunan runbook operasional, post-mortem insiden, dan dokumentasi arsitektur rilis.
