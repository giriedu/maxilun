# Daftar 24 Skill Maxilun (1 Orchestrator + 23 Spesialis)

Kontrak kepemilikan dan aturan kohesi routing lintas-skill ada di [SKILL-CONTRACTS.md](SKILL-CONTRACTS.md) dan [ROUTING-MATRIX.md](ROUTING-MATRIX.md). Aturan Purity Gate publik ada di [PURITY-GATE.md](PURITY-GATE.md).

| No | Nama Skill | Fungsi Utama | Pemicu Khas |
|:---:|---|---|---|
| 1 | **maxilun** | Orchestrator: triase keputusan berbasis reversibilitas, penunjukan satu pemilik kohesif per permukaan kerja, koordinasi wave lintas-domain, dan gate bukti nyata tanpa seremoni HUD. | `/maxilun`, `mode maxilun` |
| 2 | **maxilun-knowledge-graph** | Fondasi pemetaan kode struktural: memetakan simbol, import, caller/callee (`defOf:`, `callsIn:`) via AST scanner Python/TS/Polyglot dan visualizer WebGL (Lens). | `/maxilun-knowledge-graph`, `/maxilun-graph`, `/msal-trace` |
| 3 | **maxilun-scaffold** | Project Context Scaffolder: membangkitkan dokumen konteks `docs/` berbasis bukti repositori lebih dulu, menyesuaikan cakupan antara produk ber-UI vs API/CLI headless. | `/maxilun-scaffold`, `/maxilun-init`, `/msal-init` |
| 4 | **maxilun-architect** | Arsitektur Sistem: batas modul dalam (*Deep Modules*), kontrak API/event, migrasi *Strangler/Expand-Contract*, isolasi multi-tenant, evaluasi mode kegagalan, dan ADR dengan pemicu tinjau ulang terukur. | `/maxilun-architect`, `/maxilun-think`, `/msal-think` |
| 5 | **maxilun-sentinel** | Keamanan Defensif: autentikasi/otorisasi modern, OWASP Top 10, threat modeling STRIDE, kriptografi aman (`timingSafeEqual`, Argon2id), dan audit supply chain. | `/maxilun-sentinel`, `/msal-security`, `audit keamanan` |
| 6 | **maxilun-engineer** | Implementasi Kode: perbaikan akar masalah di titik konvergensi, TDD proporsional, refaktoring terukur tanpa *drive-by diff*, dan pembersihan kode usang hasil cutover. | `/maxilun-engineer`, `tulis kode`, `fix bug` |
| 7 | **maxilun-data** | Database & Data Layer: desain skema kontekstual, migrasi *expand-contract* zero-downtime, optimasi query `EXPLAIN (ANALYZE, BUFFERS)`, pencegahan N+1, dan PostgreSQL RLS. | `/maxilun-data`, `skema database`, `migrasi`, `ORM` |
| 8 | **maxilun-frontend** | Rekayasa Frontend Modern: Next.js 15 App Router, batas React 19 Server/Client Components, async request APIs, caching eksplisit, dan Server Actions aman. | `/maxilun-frontend`, `RSC`, `App Router`, `Server Actions` |
| 9 | **maxilun-verify** | Pembuktian Kualitas: verifikasi bertingkat proporsional (typecheck, unit/integrasi, E2E Playwright, aksesibilitas WCAG, regresi visual) berbasis bukti perintah nyata. | `/maxilun-verify`, `/msal-test`, `cek build` |
| 10 | **maxilun-insight** | Diagnostik & Audit Codebase: pencarian akar masalah berbasis bukti, profiling CPU/memori/DB, penelusuran radius dampak via graf, dan daftar pangkas (*cut-list*) berprioritas. | `/maxilun-insight`, `/msal-audit`, `root cause` |
| 11 | **maxilun-deploy** | Cloud & Operasi: pipeline CI/CD bersih, container Docker multi-stage non-root, validasi environment fail-fast, rollout zero-downtime, dan uji pemulihan backup. | `/maxilun-deploy`, `CI/CD`, `Docker`, `deploy` |
| 12 | **maxilun-docsmith** | Spesifikasi & Dokumentasi Engineer: Feature PRD/RFC kontekstual, kontrak OpenAPI 3.1 + RFC 9457, README teknis, ADR, runbook insiden, dan `llms.txt`. | `/maxilun-docsmith`, `/msal-docs`, `tulis RFC`, `ADR` |
| 13 | **maxilun-craft** | Sistem Desain & UI/UX Kontekstual: arsitektur antarmuka autentik sesuai domain produk, protokol pembongkaran kunci desain lama (clean cutover), token OKLCH, 6 state data, kepatuhan WCAG, logo SVG matematis, dan Brand Guidelines PDF. | `/maxilun-craft`, `/msal-ui`, `desain UI`, `redesign` |
| 14 | **maxilun-motion** | Desain Gerak & 3D Web: koreografi pegas kontekstual, interaksi SVG/Lottie, scene 3D/WebGL penuh, serta fallback `prefers-reduced-motion`. | `/maxilun-motion`, `animasi web`, `Three.js`, `WebGL` |
| 15 | **maxilun-cinecode** | Programmatic Video: komposisi frame React/Remotion deterministik, sinkronisasi audio, dan pipeline render MP4/WebM/GIF headless via FFmpeg. | `/maxilun-cinecode`, `video programatik`, `render video` |
| 16 | **maxilun-diagrams** | Visualisasi Sistem: diagram alur, sequence, ER, dan state machine berlabel aktif via Mermaid serta ekspor SVG/HTML mandiri. | `/maxilun-diagrams`, `/msal-diagram`, `buat diagram` |
| 17 | **maxilun-content** | Copywriting Produk: teks antarmuka berorientasi tugas, pemulihan error kontekstual, lokalisasi tepat sasaran, dan naskah beat video ringkas. | `/maxilun-content`, `/msal-copy`, `copywriting` |
| 18 | **maxilun-seo-audit** | Audit SEO Teknis: crawlability, canonical, metadata sesuai search intent, structured data JSON-LD akurat, dan Core Web Vitals. | `/maxilun-seo-audit`, `/msal-seo`, `audit SEO` |
| 19 | **maxilun-desktop** | Rekayasa Desktop & Enterprise: Windows native (Win32, WPF, WinUI), macOS (AppKit, Swift), lintas platform (C++ Qt, Tauri), dan sistem enterprise PowerBuilder (PowerScript, DataWindow, SQLCA, PFC). | `/maxilun-desktop`, `aplikasi desktop`, `powerbuilder`, `win32`, `qt` |
| 20 | **maxilun-mobile** | Rekayasa Mobile Native & Lintas Platform: Android native (Kotlin, Jetpack Compose), iOS native (Swift, SwiftUI), Flutter, React Native, KMP, arsitektur offline-first, dan izin OS. | `/maxilun-mobile`, `aplikasi mobile`, `android`, `ios`, `flutter` |
| 21 | **maxilun-iot** | Sistem Embedded & IoT: mikrokontroler (ESP32, STM32, Arduino, Raspberry Pi), FreeRTOS, zero-heap ISR, driver bus (I2C, SPI, UART, GPIO), protokol telemetri MQTT, BLE, Modbus, dan OTA. | `/maxilun-iot`, `iot`, `embedded`, `esp32`, `arduino`, `firmware` |
| 22 | **maxilun-network** | Rekayasa Jaringan & RouterOS: konfigurasi router MikroTik RouterOS (v6 & v7, WinBox/CLI), firewall stateful default-drop, QoS/PCQ bandwidth shaping, bridge VLAN, WireGuard, dan Linux networking. | `/maxilun-network`, `mikrotik`, `routeros`, `firewall`, `wireguard` |
| 23 | **maxilun-ai** | Rekayasa Aplikasi LLM & RAG: arsitektur hybrid retrieval (dense vector + BM25), chunking semantik, reranking, evaluasi regresi prompt, LLM-as-a-judge, optimasi context caching, dan function calling schemas. | `/maxilun-ai`, `/msal-ai`, `rag`, `embedding`, `prompt eval` |
| 24 | **maxilun-game** | Rekayasa Game Studio & Multi-Engine: arsitektur engine (Godot GDScript/GDExtension, Unreal Engine C++/GAS, Unity C#/DOTS), sinkronisasi fisika, authoritative netcode, spesifikasi GDD, dan otomasi test game (gdUnit4, NUnit, Unreal Automation). | `/maxilun-game`, `/maxilun-gamestudio`, `game dev`, `godot`, `unreal`, `unity`, `gdd` |

## Prinsip Integrasi Inti

- **Satu Pemilik Kohesif**: Hindari memecah satu halaman atau satu endpoint ke banyak spesialis tanpa batas kapabilitas nyata.
- **Investigasi Repo Sebelum Bertanya**: Gunakan `maxilun-knowledge-graph` dan pembacaan konfigurasi proyek untuk mengambil keputusan teknis secara mandiri; tanyakan hanya keputusan yang mahal dibalik.
- **Anti-Monokultur Desain**: `maxilun-craft` memanfaatkan 100 analisis brand nyata di `skills/maxilun-craft/references/design-md/` untuk menyesuaikan struktur dengan domain produk, bukan menyeragamkan semua proyek ke satu template SaaS.
- **Batas Instruksi Ramping (`≤300` Baris)**: Seluruh 24 berkas `SKILL.md` dijaga tetap padat di bawah 300 baris agar jendela konteks model tetap tajam, dengan referensi mendalam dimuat sesuai kebutuhan.
