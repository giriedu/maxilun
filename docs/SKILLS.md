# Daftar 18 Skill Maxilun (1 Orchestrator + 17 Spesialis)

Contract ownership dan routing lintas-skill ada di [SKILL-CONTRACTS.md](SKILL-CONTRACTS.md) dan [ROUTING-MATRIX.md](ROUTING-MATRIX.md). Aturan anti-slop publik ada di [ANTI-SLOP.md](ANTI-SLOP.md).

| No | Nama Skill | Fungsi Utama | Pemicu Khas |
|:---:|---|---|---|
| 1 | **maxilun** | Orchestrator. Menentukan hasil yang diminta, memilih spesialis, menjalankan discovery untuk brief kabur, mengoordinasikan wave, dan menegakkan gate bukti sebelum delivery. | `/maxilun`, `mode maxilun` |
| 2 | **maxilun-knowledge-graph** | Fondasi pencarian kode untuk perubahan struktural atau lintas-file: memetakan simbol, import, caller/callee, dan dependensi sebagai directed graph. Dilengkapi visualizer WebGL (Lens). Tugas trivial dapat memakai jalur cepat; pencarian langsung menjadi fallback jika tool graf tidak tersedia. | `/maxilun-knowledge-graph`, `/msal-graph`, `/msal-trace` |
| 3 | **maxilun-scaffold** | Project Context Scaffolder: generate 10 dokumen AI-readable (PRD, TECHSTACK, DESIGN, SECURITY, STYLEGUIDE, TASK, ARCHITECTURE, SKILLS, GLOSSARY, ONBOARDING) ke folder `docs/` sebelum coding dimulai. Update per milestone. | `/maxilun-scaffold`, `/msal-init`, `scaffold dokumen`, `buat docs project` |
| 4 | **maxilun-architect** | Arsitektur Sistem: C4 Model, Event Storming, kontrak API, batas modul, analisis dampak dependensi, dan penalaran mendalam (/msal-think). | `/maxilun-architect`, `/msal-think` |
| 5 | **maxilun-sentinel** | Keamanan Defensif: OWASP Top 10, autentikasi, otorisasi, threat modeling STRIDE, audit kriptografi (AES-GCM, timing-safe), validasi input, dan supply chain audit. | `/maxilun-sentinel`, `/msal-security`, `audit keamanan`, `enkripsi` |
| 6 | **maxilun-engineer** | Implementasi Kode: menulis kode bersih, TDD, perbaikan bug 5-WHY root-cause, refaktoring modular, dan verifikasi CEFR. | `/maxilun-engineer`, `tulis kode`, `fix bug` |
| 7 | **maxilun-data** | Database & Data Layer: desain skema, migrasi zero-downtime, ORM best practices, strategi indexing, pencegahan N+1, dan DB selection matrix. | `/maxilun-data`, `skema database`, `migrasi`, `indeks query`, `ORM` |
| 8 | **maxilun-frontend** | Rekayasa Frontend Modern: React Server Components, Next.js App Router, Server Actions, state management, type-safe full-stack, dan bundle optimization. | `/maxilun-frontend`, `RSC`, `Server Components`, `App Router`, `Next.js patterns` |
| 9 | **maxilun-verify** | Jaminan Kualitas: pengujian otomatis, Playwright E2E, visual regression, aksesibilitas WCAG, contract testing, lint, build check, dan proteksi regresi. | `/maxilun-verify`, `/msal-test`, `cek build` |
| 10 | **maxilun-insight** | Diagnostik & Profiling: audit performa, analisis akar masalah (root-cause), profiling CPU/memori/database, deteksi memory leak, dan distributed tracing. | `/maxilun-insight`, `/msal-audit`, `root cause` |
| 11 | **maxilun-deploy** | Cloud & Operasi: pipeline CI/CD, konfigurasi Docker multi-stage, manajemen environment, monitoring, deployment zero-downtime, dan disaster recovery. | `/maxilun-deploy`, `CI/CD`, `Docker`, `pipeline`, `monitoring`, `deployment` |
| 12 | **maxilun-docsmith** | Dokumentasi Teknis untuk Engineer: spesifikasi OpenAPI/AsyncAPI/TypeSpec, ADR arsitektur, runbook operasi, panduan migrasi, dan llms.txt. | `/maxilun-docsmith`, `/msal-docs`, `tulis README`, `dokumentasi API`, `ADR` |
| 13 | **maxilun-craft** | UI/UX & Sistem Desain: sistem token warna OKLCH, kontras rasio WCAG AAA, layout grid 4px, komponen produksi responsif, dan konsistensi visual. | `/maxilun-craft`, `/msal-ui`, `desain antarmuka` |
| 14 | **maxilun-motion** | Motion Design Web: animasi HTML/CSS/Canvas interaktif, export Lottie/SVG, physics-based motion, audio reactivity, kinetic typography, dan transisi mikro. | `/maxilun-motion`, `animasi`, `motion graphics`, `kinetic typography` |
| 15 | **maxilun-cinecode** | Programmatic Video: kreasi video berbasis kode (*video-as-code*), komponen React sebagai frame, rendering server-side headless, timeline audio sync, dan batch export MP4/WebM. | `/maxilun-cinecode`, `buat video dari kode`, `programmatic video`, `render video` |
| 16 | **maxilun-diagrams** | Visualisasi Arsitektur: pembuatan diagram arsitektur C4, sequence flow, Event Storming, data flow via format Mermaid dan SVG mandiri. | `/maxilun-diagrams`, `/msal-diagram`, `buat diagram` |
| 17 | **maxilun-content** | Copywriting Pengguna Akhir: landing page copy, microcopy antarmuka (CTA, error message, empty state), panduan brand voice, SEO copy, dan lokalisasi. | `/maxilun-content`, `/msal-copy`, `copywriting`, `microcopy`, `brand voice` |
| 18 | **maxilun-seo-audit** | Audit SEO Teknis: indexing, metadata semantik, canonical URL, structured data JSON-LD, internal linking, Core Web Vitals, dan integrasi llms.txt. | `/maxilun-seo-audit`, `/msal-seo`, `audit SEO` |

## Catatan Integrasi

- **Knowledge Graph sebagai Fondasi**: Gunakan `maxilun-knowledge-graph` untuk perubahan kode struktural atau lintas-file bila tersedia. Hasil `file:line` membantu mengarahkan inspeksi; tugas trivial boleh memakai jalur cepat dan pencarian langsung menjadi fallback bila indexer tidak tersedia.
- **Panduan domain docsmith vs content**: Gunakan `maxilun-docsmith` untuk dokumen yang dibaca engineer (API spec, README, ADR). Gunakan `maxilun-content` untuk teks yang dibaca pengguna akhir (landing page, tombol, pesan error).
- **SEO Audit**: Telah terintegrasi penuh sebagai spesialis resmi `maxilun-seo-audit`.
- **Archify**: Terintegrasi secara opsional melalui `maxilun-diagrams`. Maxilun tetap mandiri menghasilkan diagram Mermaid dan standalone SVG/HTML tanpa ketergantungan mutlak pada tool eksternal.

## Roadmap Skill (Belum Tersedia)

| Skill | Deskripsi | Status |
|---|---|---|
| **maxilun-ai** | AI/LLM feature development: prompt engineering, streaming responses, RAG pipeline, vector database, model selection, AI safety. | Direncanakan |
| **maxilun-mobile** | React Native, Flutter, Expo — mobile-native patterns, platform-specific UX, offline support, push notifications. | Direncanakan |
