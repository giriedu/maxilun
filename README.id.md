# Maxilun

<div align="center">

<img src="assets/banner.jpg" alt="Maxilun — 18 Specialist Skills · Zero AI Slop · Four Always-On Engines and Three Operating Protocols" width="100%">

<br/>

[![CI](https://github.com/giriedu/maxilun/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/giriedu/maxilun/actions/workflows/validate-skills.yml)
[![Version](https://img.shields.io/badge/version-1.0.0-7c3aed?style=flat-square)](CHANGELOG.md)
[![Skills](https://img.shields.io/badge/skills-18_specialists-06b6d4?style=flat-square)](docs/SKILLS.md)
[![License](https://img.shields.io/badge/license-Source_Available-22c55e?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/runs_on-Claude_·_Cursor_·_Codex_·_Antigravity_·_Zed_·_Termul-white?style=flat-square)](#platform-support)
[![skills.sh](https://skills.sh/b/giriedu/maxilun?style=flat-square)](https://skills.sh/giriedu/maxilun)

<br/>

[English](README.md) · **Bahasa Indonesia**

</div>

---

**Maxilun** adalah ekosistem 18 skill AI spesialis tingkat produksi untuk tim rekayasa perangkat lunak. Maxilun menggabungkan fondasi Knowledge Graph, empat engine kualitas yang selalu aktif, tiga protokol kerja, orkestrator, dan panduan pemeriksaan kualitas.

## Instalasi Cepat

```bash
npx skills add giriedu/maxilun
```

> Pantau dan jelajahi 18 skill Maxilun di [skills.sh/giriedu/maxilun](https://skills.sh/giriedu/maxilun).  
> **Mode Non-interaktif (semua skill)**: `npx skills add giriedu/maxilun -y` (tambahkan `-g` untuk instalasi global).  
> **Catatan Windows**: Jika symlink dibatasi hak akses Windows, tambahkan opsi `--copy` (`npx skills add giriedu/maxilun --copy -y`) atau jalankan script PowerShell di [docs/INSTALL.md](docs/INSTALL.md).

---

## 18 Skill Spesialis

Disusun berdasarkan siklus rekayasa perangkat lunak dari fondasi arsitektur hingga eksekusi kreatif:

| # | Skill | Fungsi Rekayasa | Pemicu Utama |
|:--:|---|---|---|
| 1 | `maxilun` | Master Orchestrator — confidence routing, koordinasi wave antar-spesialis | `/maxilun`, `/msal` |
| 2 | `msal-knowledge-graph` | Fondasi Penemuan Kode — AST parser mendalam & WebGL visualizer (Lens) | `/msal-graph`, `/msal-trace` |
| 3 | `msal-scaffold` | Project Context Scaffolder — 10 dokumen konteks siap-baca AI di `docs/` | `/msal-scaffold`, `/msal-init` |
| 4 | `msal-architect` | Arsitektur Sistem — C4 model, Event Storming, ADRs, penalaran `/msal-think` | `/msal-think`, `/msal-architect` |
| 5 | `msal-sentinel` | Keamanan Defensif — OWASP Top 10, STRIDE threat modeling, kriptografi, secrets | `/msal-sentinel`, `/msal-security` |
| 6 | `msal-engineer` | Implementasi Kode — TDD, pemecahan bug 5-WHY, refaktoring modular | `/msal-engineer` |
| 7 | `msal-data` | Lapisan Database — desain skema, migrasi zero-downtime, optimasi query | `/msal-data` |
| 8 | `msal-frontend` | Rekayasa Frontend — React Server Components, Next.js App Router, Server Actions | `/msal-frontend` |
| 9 | `msal-verify` | Jaminan Kualitas — E2E (Playwright), visual regression, a11y, contract testing | `/msal-verify`, `/msal-test` |
| 10 | `msal-insight` | Diagnostik Performa — profiling CPU/memori/database, distributed tracing | `/msal-insight`, `/msal-audit` |
| 11 | `msal-deploy` | Operasi & Cloud — pipeline CI/CD, Docker multi-stage, rollout zero-downtime | `/msal-deploy` |
| 12 | `msal-docsmith` | Dokumentasi Teknis — OpenAPI/AsyncAPI, ADR, runbook, llms.txt | `/msal-docsmith`, `/msal-docs` |
| 13 | `msal-craft` | Desain Sistem & UI/UX — palet warna OKLCH, kepatuhan WCAG AAA, grid 4px | `/msal-craft`, `/msal-ui` |
| 14 | `msal-motion` | Desain Animasi — animasi web interaktif, kinetic typography, interaksi fisika | `/msal-motion` |
| 15 | `msal-cinecode` | Programmatic Video — komponen React sebagai frame, rendering batch MP4/WebM | `/msal-cinecode` |
| 16 | `msal-diagrams` | Visualisasi Sistem — diagram alur, sequence, C4 diagram via Mermaid/SVG | `/msal-diagram`, `/msal-diagrams` |
| 17 | `msal-content` | Copywriting Pengguna — landing page, microcopy UI, brand voice, lokalisasi | `/msal-content`, `/msal-copy` |
| 18 | `msal-seo-audit` | Audit SEO Teknis — Core Web Vitals, JSON-LD structured data, crawler readiness | `/msal-seo`, `/msal-seo-audit` |

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

`msal-knowledge-graph` adalah pintu gerbang wajib yang dijalankan sebelum AI memodifikasi kode repositori:

- **Python AST Scanner** — pemetaan sintaksis tingkat tinggi berbasis pohon sintaks nyata (bukan regex rapuh)
- **TypeScript Scanner** — atribusi dependensi pemanggilan baris-ke-baris (*line-accurate CALLS*)
- **Generic Polyglot Scanner** — mendukung Go, Rust, Java, C#, Ruby, PHP, Swift, C/C++
- **Maxilun Lens** — visualizer visual interaktif WebGL 3D & 2D Matrix dengan pelacakan jalur BFS (*Path Trace*)

```bash
# Jalankan langsung dari dalam sesi AI Anda:
/msal-graph
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
| [docs/RELEASE.md](docs/RELEASE.md) | Alur rilis GitHub Release otomatis & pembaruan metadata |
| [CHANGELOG.md](CHANGELOG.md) | Riwayat pembaruan versi ekosistem |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Standar kontribusi & pengujian test-suite |

---

## Lisensi

Didistribusikan di bawah **Maxilun Source Available License v2.0 (MSAL-2.0)** — bebas digunakan, dimodifikasi, dan di-deploy untuk kebutuhan internal, riset, maupun komersial. Redistribusi langsung sebagai produk kompetitif berbayar memerlukan izin tertulis. Lihat detail lengkap di [LICENSE](LICENSE).
