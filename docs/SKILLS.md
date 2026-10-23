# Daftar 18 Skill Spesialis Maxilun

| No | Nama Skill | Fungsi Utama | Pemicu Khas |
|:---:|---|---|---|
| 1 | **maxilun** | Master Orchestrator. Memahami permintaan, menentukan mode kerja, memilih spesialis, mengatur alur eksekusi, dan merangkum hasil. | `/maxilun`, `/msal`, `mode maxilun` |
| 2 | **msal-knowledge-graph** | Fondasi pencarian kode untuk perubahan struktural atau lintas-file: memetakan simbol, import, caller/callee, dan dependensi sebagai directed graph. Dilengkapi visualizer WebGL (Lens). Tugas trivial dapat memakai jalur cepat; pencarian langsung menjadi fallback jika tool graf tidak tersedia. | `/msal-knowledge-graph`, `/msal-graph`, `/msal-trace` |
| 3 | **msal-scaffold** | Project Context Scaffolder: generate 10 dokumen AI-readable (PRD, TECHSTACK, DESIGN, SECURITY, STYLEGUIDE, TASK, ARCHITECTURE, SKILLS, GLOSSARY, ONBOARDING) ke folder `docs/` sebelum coding dimulai. Update per milestone. | `/msal-scaffold`, `/msal-init`, `scaffold dokumen`, `buat docs project` |
| 4 | **msal-architect** | Arsitektur Sistem: C4 Model, Event Storming, kontrak API, batas modul, analisis dampak dependensi, dan penalaran mendalam (/msal-think). | `/msal-architect`, `/msal-think` |
| 5 | **msal-sentinel** | Keamanan Defensif: OWASP Top 10, autentikasi, otorisasi, threat modeling STRIDE, audit kriptografi (AES-GCM, timing-safe), validasi input, dan supply chain audit. | `/msal-sentinel`, `/msal-security`, `audit keamanan`, `enkripsi` |
| 6 | **msal-engineer** | Implementasi Kode: menulis kode bersih, TDD, perbaikan bug 5-WHY root-cause, refaktoring modular, dan verifikasi CEFR. | `/msal-engineer`, `tulis kode`, `fix bug` |
| 7 | **msal-data** | Database & Data Layer: desain skema, migrasi zero-downtime, ORM best practices, strategi indexing, pencegahan N+1, dan DB selection matrix. | `/msal-data`, `skema database`, `migrasi`, `indeks query`, `ORM` |
| 8 | **msal-frontend** | Rekayasa Frontend Modern: React Server Components, Next.js App Router, Server Actions, state management, type-safe full-stack, dan bundle optimization. | `/msal-frontend`, `RSC`, `Server Components`, `App Router`, `Next.js patterns` |
| 9 | **msal-verify** | Jaminan Kualitas: pengujian otomatis, Playwright E2E, visual regression, aksesibilitas WCAG, contract testing, lint, build check, dan proteksi regresi. | `/msal-verify`, `/msal-test`, `cek build` |
| 10 | **msal-insight** | Diagnostik & Profiling: audit performa, analisis akar masalah (root-cause), profiling CPU/memori/database, deteksi memory leak, dan distributed tracing. | `/msal-insight`, `/msal-audit`, `root cause` |
| 11 | **msal-deploy** | Cloud & Operasi: pipeline CI/CD, konfigurasi Docker multi-stage, manajemen environment, monitoring, deployment zero-downtime, dan disaster recovery. | `/msal-deploy`, `CI/CD`, `Docker`, `pipeline`, `monitoring`, `deployment` |
| 12 | **msal-docsmith** | Dokumentasi Teknis untuk Engineer: spesifikasi OpenAPI/AsyncAPI/TypeSpec, ADR arsitektur, runbook operasi, panduan migrasi, dan llms.txt. | `/msal-docsmith`, `/msal-docs`, `tulis README`, `dokumentasi API`, `ADR` |
| 13 | **msal-craft** | UI/UX & Sistem Desain: sistem token warna OKLCH, kontras rasio WCAG AAA, layout grid 4px, komponen produksi responsif, dan konsistensi visual. | `/msal-craft`, `/msal-ui`, `desain antarmuka` |
| 14 | **msal-motion** | Motion Design Web: animasi HTML/CSS/Canvas interaktif, export Lottie/SVG, physics-based motion, audio reactivity, kinetic typography, dan transisi mikro. | `/msal-motion`, `animasi`, `motion graphics`, `kinetic typography` |
| 15 | **msal-cinecode** | Programmatic Video: kreasi video berbasis kode (*video-as-code*), komponen React sebagai frame, rendering server-side headless, timeline audio sync, dan batch export MP4/WebM. | `/msal-cinecode`, `buat video dari kode`, `programmatic video`, `render video` |
| 16 | **msal-diagrams** | Visualisasi Arsitektur: pembuatan diagram arsitektur C4, sequence flow, Event Storming, data flow via format Mermaid dan SVG mandiri. | `/msal-diagrams`, `/msal-diagram`, `buat diagram` |
| 17 | **msal-content** | Copywriting Pengguna Akhir: landing page copy, microcopy antarmuka (CTA, error message, empty state), panduan brand voice, SEO copy, dan lokalisasi. | `/msal-content`, `/msal-copy`, `copywriting`, `microcopy`, `brand voice` |
| 18 | **msal-seo-audit** | Audit SEO Teknis: indexing, metadata semantik, canonical URL, structured data JSON-LD, internal linking, Core Web Vitals, dan integrasi llms.txt. | `/msal-seo-audit`, `/msal-seo`, `audit SEO` |

## Catatan Integrasi

- **Knowledge Graph sebagai Fondasi**: Gunakan `msal-knowledge-graph` untuk perubahan kode struktural atau lintas-file bila tersedia. Hasil `file:line` membantu mengarahkan inspeksi; tugas trivial boleh memakai jalur cepat dan pencarian langsung menjadi fallback bila indexer tidak tersedia.
- **Panduan domain docsmith vs content**: Gunakan `msal-docsmith` untuk dokumen yang dibaca engineer (API spec, README, ADR). Gunakan `msal-content` untuk teks yang dibaca pengguna akhir (landing page, tombol, pesan error).
- **SEO Audit**: Telah terintegrasi penuh sebagai spesialis resmi `msal-seo-audit`.
- **Archify**: Terintegrasi secara opsional melalui `msal-diagrams`. Maxilun tetap mandiri menghasilkan diagram Mermaid dan standalone SVG/HTML tanpa ketergantungan mutlak pada tool eksternal.

## Roadmap Skill (Belum Tersedia)

| Skill | Deskripsi | Status |
|---|---|---|
| **maxilun-ai** | AI/LLM feature development: prompt engineering, streaming responses, RAG pipeline, vector database, model selection, AI safety. | Direncanakan |
| **maxilun-mobile** | React Native, Flutter, Expo — mobile-native patterns, platform-specific UX, offline support, push notifications. | Direncanakan |
