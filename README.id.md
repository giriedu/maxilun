# Maxilun

<div align="center">

<img src="assets/banner.jpg" alt="Maxilun — 18 Skill: 1 Orchestrator + 17 Spesialis · Zero AI Slop · Empat Engine" width="100%">

<br/>

[![CI](https://github.com/giriedu/maxilun/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/giriedu/maxilun/actions/workflows/validate-skills.yml)
[![Version](https://img.shields.io/badge/version-2.3.0-7c3aed?style=flat-square)](CHANGELOG.md)
[![Skills](https://img.shields.io/badge/skills-18_skills-06b6d4?style=flat-square)](docs/SKILLS.md)
[![License](https://img.shields.io/badge/license-Source_Available-22c55e?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/runs_on-Claude_·_Cursor_·_Codex_·_Antigravity_·_Zed_·_Termul-white?style=flat-square)](#platform-support)
[![skills.sh](https://skills.sh/b/giriedu/maxilun?style=flat-square)](https://skills.sh/giriedu/maxilun)

<br/>

[English](README.md) · **Bahasa Indonesia**

</div>

---

**Maxilun** adalah ekosistem 18 skill AI untuk tim rekayasa perangkat lunak: satu orchestrator dan 17 spesialis. Setiap skill membawa blok **Core Rules** yang sama, sehingga empat engine kualitas ikut terpasang bersama skill, bukan tertinggal di folder terpisah. Orchestrator menambahkan routing berbasis hasil, protokol discovery untuk brief kabur, koordinasi wave, dan gate delivery berbasis bukti. Materi mendalam (detail engine, katalog anti-slop, higienitas kode, discovery) ada di `references/` dalam skill orchestrator dan hanya dimuat saat dibutuhkan.

## Instalasi Cepat

```bash
npx skills add giriedu/maxilun
```

> Pantau dan jelajahi 18 skill Maxilun di [skills.sh/giriedu/maxilun](https://skills.sh/giriedu/maxilun).  
> **Mode Non-interaktif (semua skill)**: `npx skills add giriedu/maxilun -y` (tambahkan `-g` untuk instalasi global).  
> **Catatan Windows**: Jika symlink dibatasi hak akses Windows, tambahkan opsi `--copy` (`npx skills add giriedu/maxilun --copy -y`) atau jalankan script PowerShell di [docs/INSTALL.md](docs/INSTALL.md).

---

## 18 Skill: 1 Orchestrator + 17 Spesialis

Disusun berdasarkan siklus rekayasa perangkat lunak dari fondasi arsitektur hingga eksekusi kreatif:

| # | Skill | Fungsi Rekayasa | Pemicu Utama |
|:--:|---|---|---|
| 1 | `maxilun` | Orchestrator — routing berbasis hasil, protokol discovery, koordinasi wave, gate bukti | `/maxilun`, `mode maxilun` |
| 2 | `maxilun-knowledge-graph` | Fondasi Penemuan Kode — AST parser mendalam & WebGL visualizer (Lens) | `/maxilun-graph`, `/msal-trace` |
| 3 | `maxilun-scaffold` | Project Context Scaffolder — 10 dokumen konteks siap-baca AI di `docs/` dengan archetype domain & referensi UI | `/maxilun-scaffold`, `/msal-init` |
| 4 | `maxilun-architect` | Arsitektur Sistem — C4 model, Event Storming, ADRs, penalaran `/maxilun-think` | `/maxilun-think`, `/maxilun-architect` |
| 5 | `maxilun-sentinel` | Keamanan Defensif — OWASP Top 10, STRIDE threat modeling, kriptografi, secrets | `/maxilun-sentinel`, `/msal-security` |
| 6 | `maxilun-engineer` | Implementasi Kode — TDD, pemecahan bug 5-WHY, refaktoring modular | `/maxilun-engineer` |
| 7 | `maxilun-data` | Lapisan Database — desain skema, migrasi zero-downtime, optimasi query | `/maxilun-data` |
| 8 | `maxilun-frontend` | Rekayasa Frontend — React Server Components, Next.js App Router, Server Actions | `/maxilun-frontend` |
| 9 | `maxilun-verify` | Jaminan Kualitas — E2E (Playwright), visual regression, a11y, contract testing | `/maxilun-verify`, `/msal-test` |
| 10 | `maxilun-insight` | Diagnostik Performa — profiling CPU/memori/database, distributed tracing | `/maxilun-insight`, `/msal-audit` |
| 11 | `maxilun-deploy` | Operasi & Cloud — pipeline CI/CD, Docker multi-stage, rollout zero-downtime | `/maxilun-deploy` |
| 12 | `maxilun-docsmith` | Spesifikasi & Dokumentasi Teknis — Feature PRD/RFC, OpenAPI 3.1/AsyncAPI, ADR, runbook, `llms.txt` | `/maxilun-docsmith`, `/msal-docs` |
| 13 | `maxilun-craft` | Desain Sistem & UI/UX — palet warna OKLCH, kepatuhan WCAG AAA, grid 4px | `/maxilun-craft`, `/msal-ui` |
| 14 | `maxilun-motion` | Desain motion — animasi browser interaktif, aset Lottie/SVG, kinetic typography | `/maxilun-motion` |
| 15 | `maxilun-cinecode` | Render video final — MP4/WebM/GIF berbasis kode/data, pipeline batch | `/maxilun-cinecode` |
| 16 | `maxilun-diagrams` | Visualisasi Sistem — diagram alur, sequence, C4 diagram via Mermaid/SVG | `/maxilun-diagram`, `/maxilun-diagrams` |
| 17 | `maxilun-content` | Copywriting Pengguna — landing page, microcopy UI, brand voice, lokalisasi | `/maxilun-content`, `/msal-copy` |
| 18 | `maxilun-seo-audit` | Audit SEO Teknis — Core Web Vitals, JSON-LD structured data, crawler readiness | `/maxilun-seo`, `/maxilun-seo-audit` |

---

## Empat Engine Kualitas yang Selalu Aktif

Digunakan di seluruh 18 skill:

| Mesin | Fungsi Utama |
|---|---|
| **Focus Engine** | Executive HUD, dekomposisi tugas hierarkis, pelacakan subtask persisten |
| **Purity Engine** | Meninjau output generik, klaim tanpa bukti, dan placeholder kosong |
| **Minimalist Engineering** | Tangga kesederhanaan, perbaikan akar masalah, hapus sebelum menambah |
| **Clarity Engine** | Penandaan kepastian teknis eksplisit: `[CONFIRMED]`, `[INFERRED]`, `[UNCERTAIN]`, `[UNVERIFIED]` |

Tiga protokol pendukung:

| Protokol | Panduan |
|---|---|
| **Dependency Decision Framework** | Evaluasi stdlib, ukuran bundle, dan pemeliharaan sebelum menambah dependency |
| **Cognitive Load Reduction** | Naming sebagai dokumentasi, panduan ukuran file dan nesting, explicit over implicit |
| **Proactive Communication** | Laporkan blocker, hindari silent failure, nyatakan asumsi dan perubahan scope |

---

## Fondasi Knowledge Graph

Gunakan `maxilun-knowledge-graph` untuk perubahan kode struktural atau lintas-file ketika tool graf tersedia. Perubahan teks kecil dan terisolasi boleh memakai jalur cepat; jika tool graf tidak tersedia, gunakan pencarian repo langsung dan nyatakan fallback tersebut:

- **Python AST Scanner** — pemetaan sintaksis tingkat tinggi berbasis pohon sintaks nyata (bukan regex rapuh)
- **TypeScript Scanner** — atribusi dependensi pemanggilan baris-ke-baris (*line-accurate CALLS*)
- **Generic Polyglot Scanner** — mendukung Go, Rust, Java, C#, Ruby, PHP, Swift, C/C++
- **Maxilun Lens** — visualizer visual interaktif WebGL 3D & 2D Matrix dengan pelacakan jalur BFS (*Path Trace*)

```bash
# Jalankan langsung dari dalam sesi AI Anda:
/maxilun-graph
```

---

## Dukungan Platform AI

| Platform AI | Status Dukungan | Catatan |
|---|---|---|
| Claude Code | ✅ Dukungan Penuh | `.claude/skills/` |
| Antigravity IDE / CLI | ✅ Dukungan Penuh | `.agents/skills/` |
| Cursor | ✅ Dukungan Penuh | `.cursor/skills/` |
| OpenCode / Codex | ✅ Dukungan Penuh | `.config/opencode/` & `.codex/` |
| Zed Editor | ✅ Dukungan Penuh | `.agents/skills/` (`npx skills add -a zed`) |
| Termul (`termul.dev`) | ✅ Dukungan Penuh | Workspace terminal manager untuk agen AI |

---

## Dokumentasi Teknis

| Berkas Panduan | Cakupan Informasi |
|---|---|
| [docs/INSTALL.md](docs/INSTALL.md) | Panduan instalasi multi-platform lengkap & integrasi CLI |
| [docs/SKILLS.md](docs/SKILLS.md) | Detail mendalam, peran teknis, dan pemicu 18 spesialis |
| [docs/ENGINES.md](docs/ENGINES.md) | Empat engine kualitas dan tiga protokol operasi |
| [docs/EXAMPLES.md](docs/EXAMPLES.md) | Contoh skenario rekayasa nyata & orkestrasi Wave Pattern |
| [docs/SKILL-CONTRACTS.md](docs/SKILL-CONTRACTS.md) | Ownership, mode standalone, input, output, dan handoff setiap skill |
| [docs/ROUTING-MATRIX.md](docs/ROUTING-MATRIX.md) | Routing primary owner dan batas trigger yang bertabrakan |
| [docs/ANTI-SLOP.md](docs/ANTI-SLOP.md) | Anti-slop distribution-safe dan gate berbasis bukti |
| [docs/RELEASE.md](docs/RELEASE.md) | Alur rilis GitHub Release otomatis & pembaruan metadata |
| [CHANGELOG.md](CHANGELOG.md) | Riwayat pembaruan versi ekosistem |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Standar kontribusi & pengujian test-suite |

---

## Lisensi

Didistribusikan di bawah **Maxilun Source Available License v2.0 (MSAL-2.0)** — bebas digunakan, dimodifikasi, dan di-deploy untuk kebutuhan internal, riset, maupun komersial. Redistribusi langsung sebagai produk kompetitif berbayar memerlukan izin tertulis. Lihat detail lengkap di [LICENSE](LICENSE).
