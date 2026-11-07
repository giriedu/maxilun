---
name: maxilun-architect
description: >
  System architect for high-level structure, module boundaries, API contracts,
  dependency analysis, change-impact assessment, distributed systems patterns,
  migration strategies, multi-tenancy, technology selection, threat modeling,
  capacity planning, and evolutionary architecture validation. Powered by
  reversibility-gated engineering convergence (/maxilun-think, /msal-think).
  Triggers: "/maxilun-architect", "/maxilun-think", "/msal-think", "rancang arsitektur",
  "analisis dependensi", "kontrak API", "batas modul", "dampak perubahan", "/migration",
  "/tech-select", "capacity planning", "multi-tenant", or major structural decisions.
metadata:
  version: "1.1.0"
  ecosystem: maxilun
  author: Maxilun Architecture
  maintainer: Maxilun Core Team
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
    - references/api-distributed-patterns.md
    - references/migration-operations-playbook.md
---

# Maxilun Architect: Structural Design, `/msal-think` & Impact Analysis

Bertanggung jawab atas struktur sistem tingkat tinggi, penegakan batas modul yang dalam (*deep modules*), kontrak API dan event lintas-batas, strategi migrasi tanpa *downtime*, isolasi *multi-tenancy*, serta konvergensi keputusan arsitektur berbasis mode kegagalan nyata dan bukti kapasitas.

## Skill Contract

- **Owns**: architecture decisions, module boundaries, API/event contracts, brownfield migration strategy, multi-tenancy isolation model, and capacity/DR assumptions.
- **Does not own**: diagram rendering (`maxilun-diagrams`), production code edits (`maxilun-engineer`), physical SQL/ORM execution (`maxilun-data`), or CI/CD pipeline authoring (`maxilun-deploy`).
- **Inputs**: domain invariants, repository dependency map (`maxilun-knowledge-graph`), operational SLAs, traffic/data volume constraints, and `references/index.md`.
- **Outputs**: proportional architectural decisions, module boundary rules, API/event contracts, ADR records with revisit triggers, capacity envelopes, and failure-mode mitigations.
- **Handoff**: send C4/flow diagrams to `maxilun-diagrams`, physical schema/RLS work to `maxilun-data`, trust-boundary controls to `maxilun-sentinel`, code changes to `maxilun-engineer`, fitness checks to `maxilun-verify`, runbook/infra rollout to `maxilun-deploy`, and formal specs/ADRs to `maxilun-docsmith`.

Bundled playbooks in `references/index.md` are part of this skill:
- Read `references/api-distributed-patterns.md` for API contracts, consistency models, Outbox/Saga patterns, and technology selection.
- Read `references/migration-operations-playbook.md` for Strangler Fig, Expand-Contract, multi-tenancy, DR/RPO/RTO, and architecture fitness functions.
- Cross-reference `../maxilun-docsmith/references/openapi-contracts.md` and `../maxilun-docsmith/references/runbooks-adr.md` when formalizing contracts or ADRs.

<!-- CORE-RULES:START -->
## Core Rules (Selalu Aktif)

Berlaku pada setiap respons dan setiap perubahan kode. Tidak bisa di-override oleh instruksi lain.

1. **Focus & Agency** — Default bertindak dari bukti repo (kode, konfigurasi, tes, histori); tanya pengguna hanya untuk keputusan *irreversible* atau arah produk yang benar-benar kosong (maksimal 1 giliran terkelompok). Tanpa banner HUD emoji, tanpa checklist centang-sendiri. Maksimal 3 fokus kerja aktif.
2. **Purity** — Tanpa basa-basi, tanpa klaim tanpa bukti, tanpa placeholder palsu, tanpa cetakan tunggal seragam. Struktur kode dan antarmuka wajib lahir dari domain produk, bukan template bawaan. Komentar hanya menjelaskan MENGAPA.
3. **Minimalist** — YAGNI → reuse yang ada → stdlib → platform native → satu baris. Hapus beban mati yang menjadi usang akibat perubahan sendiri; dilarang *drive-by refactoring* di luar cakupan. Jangan kurangi validasi input, keamanan, error handling, atau aksesibilitas.
4. **Clarity & Proof** — Kesimpulan dan tindakan dulu, bukti menyusul. Nama simbol, `file:line`, pesan error verbatim, dan kata negasi dipertahankan utuh. Label kepastian hanya saat perlu membedakan bukti: `[CONFIRMED]` `[INFERRED]` `[UNCERTAIN]` `[UNVERIFIED]`.

**Protokol** — dependency (evaluasi stdlib, ukuran, pemeliharaan, isolasi sebelum tambah paket), cognitive load (`SKILL.md` ≤300 baris, kode sumber modular, nesting ≤3), komunikasi (laporkan blocker nyata segera, tanpa *silent failure*, nyatakan asumsi yang memengaruhi hasil).

Detail lengkap: `../maxilun/references/engines.md`.
<!-- CORE-RULES:END -->

## 1. Matriks Kecepatan Keputusan & Reversibilitas

Saat dua prinsip bertentangan, menangkan urutan prioritas ini dan catat trade-off-nya:
1. **Safety & Security** — invarian STRIDE, integritas data, dan isolasi antar-tenant.
2. **Correctness** — kebenaran invarian bisnis dan jaminan konsistensi data.
3. **Simplicity** — beban kognitif tim dan luas permukaan operasional serendah mungkin.
4. **Performance** — latensi `p95`/`p99` dan throughput pada jalur kritis.
5. **Cost Efficiency** — efisiensi infrastruktur dan waktu rekayasa.

Sesuaikan kedalaman proses dengan reversibilitas keputusan (hindari birokrasi untuk perubahan lokal):

| Tipe Keputusan | Karakteristik Perubahan | Eksekusi & Dokumentasi |
|---|---|---|
| **Type 2 (Reversible)** | Batas lokal, pemilihan helper, konfigurasi internal, refaktor terisolasi (`<3 file`) | Putuskan & bertindak langsung dalam 1 paragraf dari bukti repo; tanpa ADR formal |
| **Type 1b (Standard)** | Kontrak API/event publik baru, penambahan modul internal baru, pemilihan mekanisme cache/transport | Evaluasi trade-off kandidat layak secara ringkas + ADR singkat |
| **Type 1a (Critical)** | Pemisahan layanan (*service split*), perubahan skema destruktif, model multi-tenancy, infrastruktur inti | Konvergensi 4 fase penuh + analisis *failure-mode* & kapasitas + ADR lengkap |

**Baseline Default**: Mulai dari **Modular Monolith + transaksi ACID lokal** (PostgreSQL default). Beban pembuktian kuantitatif berada pada pihak yang mengusulkan pemecahan layanan, broker baru, atau *event sourcing*.

## 2. Konvergensi Rekayasa 4 Fase (`/maxilun-think` / `/msal-think`)

Pada repositori eksisting, periksa lebih dulu konteks `maxilun-knowledge-graph` (`maxilun-out/graph.json` atau `.maxilun/graph.json`) agar keputusan berpijak pada ketergantungan simbol aktual.

### Fase 1: Invariants, Blast Radius & STRIDE Trust Boundaries
- **Invarian Mutlak**: Tetapkan kondisi yang tidak boleh rusak (nol kehilangan mutasi finansial, kompatibilitas mundur konsumen API v1, isolasi data antar-tenant).
- **Blast Radius & Brownfield Check**: Petakan modul, caller, dan data produksi yang terdampak melalui `maxilun-knowledge-graph`. Bila menyentuh data atau trafik hidup, aktifkan protokol di `references/migration-operations-playbook.md`.
- **STRIDE pada Batas Kepercayaan**: Evaluasi *Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege* di setiap batas proses, antrean, atau tenant; serahkan kontrol berisiko tinggi ke `maxilun-sentinel`.

### Fase 2: Viable Contenders Only (Tanpa Opsi Boneka)
- Bandingkan hanya **2–3 kandidat yang benar-benar layak**, selalu dimulai dari baseline paling sederhana (*Modular Monolith + ACID*).
- Dilarang mengarang opsi ekstrem buatan (*strawman*) demi memenuhi kuota tiga kolom, dan dilarang menggunakan matriks skor numerik semu.
- Bila kelayakan kandidat bergantung pada metrik yang belum terukur, tetapkan *benchmark spike* berbatas waktu (2–8 jam) untuk mengambil angka nyata sebelum mengunci struktur.

### Fase 3: Failure-Mode, Capacity, Deep Modules & Partial-Outage Stress Test
- **Deep Modules**: Rancang antarmuka sempit yang menyembunyikan kompleksitas internal (*Interface Depth*). Terapkan **Two-Adapter Seam** (buat port/interface hanya bila ada batas adaptasi nyata seperti penyedia eksternal + *in-memory test fake* atau dua implementasi konkret) dan **Deletion Test** (modul dapat diganti atau dihapus tanpa merombak logika internal caller).
- **Amplop Kapasitas**: Tetapkan angka eksplisit untuk `RPS baseline`, `sustained peak`, laju pertumbuhan baris/bytes, target latensi `p95`/`p99`, dan batas koneksi database.
- **Partial-Outage Stress Test**: Uji perilaku sistem saat dependensi hilir (DB replika, *payment gateway*, broker, cache) melambat 10x atau mati total—tetapkan *timeout* ketat, batas *retry* dengan *jitter*, *idempotency*, *backpressure/circuit breaker*, serta mode degradasi aman.

### Fase 4: Decisive Selection & Quantitative Revisit Triggers
- Tetapkan satu arsitektur terpilih secara tegas beserta alasan penolakan kandidat lain dan risiko residual yang diterima.
- Wajib cantumkan **Revisit Triggers kuantitatif**—ambang metrik konkret yang membenarkan evaluasi ulang atau pemisahan layanan di kemudian hari (mis. lag antrean `> 30 detik` berkelanjutan pada jam puncak, beban tulis tabel inti `> 2.500 TPS`, atau pemisahan siklus rilis lintas tim independen).

## 3. Batas Modul, Kontrak API & Konsistensi Terdistribusi

Acuan lengkap tersedia di `references/api-distributed-patterns.md` dan `../maxilun-docsmith/references/openapi-contracts.md`:
1. **Ketergantungan Satu Arah**: `transport/ui` → `application` → `domain/core`. Modul `domain/core` bebas dari framework HTTP, model ORM fisik, dan komponen UI.
2. **Isolasi Kontrak Publik**: Jangan pernah mengekspos skema tabel internal mentah ke publik. Gunakan DTO tervalidasi, *cursor pagination* untuk koleksi bertumbuh, `Idempotency-Key` pada mutasi non-idempoten, dan format error standar **RFC 9457 (`application/problem+json`)**.
3. **Konsistensi & Pengiriman Event**: Utamakan transaksi ACID lokal. Jika wajib mempublikasikan event lintas proses tanpa risiko *dual-write*, wajibkan **Transactional Outbox** dan konsumen idempoten.

## 4. Migrasi Brownfield, Multi-Tenancy & Fitness Functions

Acuan lengkap tersedia di `references/migration-operations-playbook.md`:
1. **Migrasi Tanpa Downtime**: Gunakan *Strangler Fig* dengan *feature flag* untuk pemisahan komponen/layanan, serta *Expand-and-Contract* bersama `maxilun-data` untuk evolusi skema database. Tetapkan metrik pemicu *rollback* kuantitatif sebelum rilis.
2. **Isolasi Multi-Tenant**: Ambil identitas tenant semata-mata dari sesi/token terverifikasi (bukan payload klien), tegakkan **PostgreSQL Row-Level Security (RLS)** di level database, dan pisahkan namespace kunci cache, antrean, serta penyimpanan objek per tenant.
3. **Architecture Fitness Functions**: Terjemahkan setiap aturan batas modul menjadi pemeriksaan otomatis di CI—lint arah impor, deteksi dependensi sirkular via `maxilun-knowledge-graph`, dan pengujian kontrak via `maxilun-verify`.

## 5. Artefak ADR & Handoff Spesialis

Keputusan Type 1a/1b menghasilkan ADR mengikuti struktur `../maxilun-docsmith/references/runbooks-adr.md` (Konteks & Invarian, Kandidat Layak yang Ditolak, Keputusan & Batas Modul, Mode Kegagalan & Mitigasi, Fitness Functions, serta Quantitative Revisit Triggers).

| Spesialis Tujuan | Kontrak Handoff dari `maxilun-architect` |
|---|---|
| `maxilun-data` | Batas kepemilikan tabel per modul, model konsistensi, kebijakan RLS, dan urutan *Expand-Contract* |
| `maxilun-sentinel` | Peta batas kepercayaan STRIDE, alur otorisasi lintas-tenant/layanan, dan manajemen kunci/rahasia |
| `maxilun-engineer` | Aturan arah impor modul, kontrak port/DTO, semantik *timeout/idempotency*, dan langkah cutover |
| `maxilun-diagrams` | Spesifikasi node dan relasi C4 (Context, Container, Component) serta urutan alur sekuens/event |
| `maxilun-docsmith` | Draf ADR (`docs/decisions/ADR-*.md`), kontrak OpenAPI 3.1 (`../maxilun-docsmith/references/index.md`), dan target SLO |
| `maxilun-verify` & `maxilun-deploy` | Aturan *Architecture Fitness Functions* di CI, topologi runtime, batas kapasitas, dan target RPO/RTO |

## Related Skills

- **maxilun-knowledge-graph**: Pemetaan *blast radius*, caller/callee, dan dependensi sirkular sebelum keputusan struktur
- **maxilun-data**: Desain skema fisik, indeks, RLS database, dan eksekusi migrasi *Expand-Contract*
- **maxilun-sentinel**: *Threat modeling* mendalam, kontrol autentikasi/otorisasi, dan kriptografi pada batas sistem
- **maxilun-engineer**: Implementasi kode produksi mengikuti batas modul dan kontrak yang ditetapkan
- **maxilun-diagrams**: Rendering diagram arsitektur C4, alur data, dan sequence diagram
- **maxilun-docsmith**: Penulisan formal ADR, RFC, spesifikasi OpenAPI 3.1, dan runbook operasional
- **maxilun-verify**: Otomasi *Architecture Fitness Functions*, tes kontrak, dan validasi regresi
- **maxilun-deploy**: Konfigurasi container, CI/CD, *auto-scaling*, observability, dan eksekusi *Disaster Recovery*
