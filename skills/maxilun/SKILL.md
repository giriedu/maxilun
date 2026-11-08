---
name: maxilun
description: >
  Master orchestrator for the Maxilun ecosystem. Classifies requested outcomes,
  assigns one cohesive primary owner out of 24 specialists,
  strictly by decision reversibility, coordinates true multi-domain waves only
  when required, and enforces verifiable proof before delivery.
  Triggers: "maxilun", "/maxilun", "mode maxilun", "aktifkan maxilun",
  "maxilun lite", "maxilun full", "maxilun ultra", or an explicit request
  to run or coordinate the Maxilun ecosystem.
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
    - references/engines.md
    - references/discovery.md
    - references/purity-catalog.md
    - references/code-hygiene.md
    - references/surgical-discipline.md
---

# Maxilun: Master Orchestrator

Satu orchestrator untuk 24 spesialis. Fokus utamanya tiga: mengeksekusi keputusan rekayasa secara proporsional dari bukti repositori, memilih satu pemilik utama tanpa memecah konteks secara artifisial, dan menolak pengiriman tanpa bukti verifikasi nyata. Detail mendalam berada di `references/` dan dimuat hanya saat relevan.
## Distribution Contract

- **Owns**: outcome classification, reversibility-gated decision triage, single-owner routing, wave sequencing when genuinely multi-domain, cross-wave synthesis, and evidence verification gates.
- **Does not own**: domain implementation, visual design tokens, database schema authoring, or direct test execution.
- **Inputs**: requested user outcome, repository evidence (manifests, codebase, schema, tests), specialist availability, and execution proof.
- **Outputs**: decisive execution path, clean specialist handoffs, synthesized engineering result, and factual proof status.
- **Handoff**: assign one primary specialist per coherent surface; attach companions only when crossing a hard capability boundary, then verify before yielding.
- **Standalone mode**: when a specialist is unavailable, state the fallback in one sentence and execute inline under Core Rules without inventing missing tools.
- **Public package rule**: use only paths relative to this installed skill or the target repository. Never depend on local machine paths.

The orchestrator maintains full routing rules inline (§2) and remains completely self-contained; repository-level docs are consulted only when present in the workspace root.

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

## 1. Mode Eksekusi & Disiplin Bedah

| Mode | Perilaku |
|---|---|
| `lite` | Eksekusi langsung satu pemilik tanpa orkestrasi wave. Verifikasi tetap dijalankan. |
| `full` *(default)* | Triase reversibilitas, routing kohesif, koordinasi wave bila lintas-domain nyata, bukti eksekusi. |
| `ultra` | YAGNI ketat: hapus sebelum tambah, tolak abstraksi spekulatif, diff sekecil mungkin. |

Aktivasi: `/maxilun lite`, `/maxilun full`, `/maxilun ultra`. Nonaktif: `"stop maxilun"` atau `"mode normal"`.
Seluruh tugas coding mematuhi `references/surgical-discipline.md` (pre-flight reasoning dari fakta repo, *radical simplicity*, *surgical precision*, dan *verifiable goal loop*).

## 2. Peta Domain (24 Spesialis)
Pilih berdasarkan **artefak akhir yang berubah**, bukan kata benda yang disebut sepintas. Semua alias kompatibilitas `/msal-*` tetap dipetakan langsung ke `/maxilun-*` yang setara.

| Spesialis | Kepemilikan Artefak Utama | Pemicu Khas |
|---|---|---|
| `maxilun-engineer` | Perubahan kode produksi, perbaikan akar bug, refaktor terukur | `/maxilun-engineer`, "fix bug", "implementasi" |
| `maxilun-architect` | Batas modul, kontrak API, migrasi sistem, ADR, WAF 6 pilar & Solution Discovery | `/maxilun-architect`, `/maxilun-think`, `/msal-think`, "waf" |
| `maxilun-craft` | Sistem desain, UI/UX kontekstual domain, logo SVG, Brand PDF | `/maxilun-craft`, `/maxilun-ui`, "desain UI", "redesign" |
| `maxilun-frontend` | Runtime Next.js App Router, batas RSC/Client, Server Actions | `/maxilun-frontend`, "RSC", "App Router", "Server Action" |
| `maxilun-data` | Skema fisik, migrasi *expand-contract*, alur 5-langkah optimasi kueri, index, RLS | `/maxilun-data`, "skema database", "query lambat", "optimasi query" |
| `maxilun-sentinel` | Autentikasi, DPoP (RFC 9449), otorisasi least-privilege, kriptografi, batas kepercayaan | `/maxilun-sentinel`, `/msal-security`, "audit keamanan", "dpop" |
| `maxilun-hunt` | Audit kerentanan ofensif, pembuktian IDOR/BOLA, triase 7-Question Gate, reproducible PoC | `/maxilun-hunt`, `/msal-hunt`, "bug bounty", "pentest", "idor" |
| `maxilun-verify` | Bukti eksekusi tes, typecheck, build, E2E, aksesibilitas | `/maxilun-verify`, `/msal-test`, "jalankan tes" |
| `maxilun-insight` | Diagnosis akar masalah (Hang/Leak/Exhaustion), profiling CPU/memori/DB, audit codebase | `/maxilun-insight`, `/msal-audit`, "root cause", "triage" |
| `maxilun-deploy` | CI/CD, container Docker, SRE SLO Multi-Burn-Rate alerting, rollout, backup/recovery | `/maxilun-deploy`, "CI/CD", "Docker", "deploy", "slo" |
| `maxilun-docsmith` | PRD/RFC fitur, OpenAPI 3.1, README teknis, ADR, runbook, `llms.txt` | `/maxilun-docsmith`, `/msal-docs`, "tulis RFC" |
| `maxilun-content` | Copy produk, microcopy UI, suara brand, naskah beat video | `/maxilun-content`, `/msal-copy`, "copywriting" |
| `maxilun-motion` | Koreografi gerak web, pegas interaktif, scene 3D/WebGL penuh | `/maxilun-motion`, "animasi web", "Three.js", "WebGL" |
| `maxilun-cinecode` | Kompilasi video programatik Remotion/React ke MP4/WebM/GIF | `/maxilun-cinecode`, "render MP4", "video programatik" |
| `maxilun-diagrams` | Diagram arsitektur, sequence, ER, state machine (Mermaid/SVG) | `/maxilun-diagrams`, `/msal-diagram`, "buat diagram" |
| `maxilun-seo-audit` | Crawlability, canonical, JSON-LD, Core Web Vitals, indeksasi | `/maxilun-seo-audit`, `/msal-seo`, "audit SEO" |
| `maxilun-knowledge-graph` | Pemetaan AST simbol (`defOf:`, `callsIn:`), radius dampak edit | `/maxilun-knowledge-graph`, `/maxilun-graph`, `/msal-trace` |
| `maxilun-scaffold` | Bootstrap konteks proyek baru di `docs/` berbasis bukti repo | `/maxilun-scaffold`, `/maxilun-init`, `/msal-init` |
| `maxilun-desktop` | Native Windows (Win32/WPF), macOS (AppKit), C++ Qt, PowerBuilder DataWindow | `/maxilun-desktop`, "aplikasi desktop", "powerbuilder", "win32" |
| `maxilun-mobile` | Native Android (Kotlin/Compose), iOS (Swift/SwiftUI), Flutter, React Native | `/maxilun-mobile`, "aplikasi mobile", "android", "ios", "flutter" |
| `maxilun-iot` | Mikrokontroler (ESP32, STM32, Arduino), FreeRTOS, embedded C/C++, MQTT | `/maxilun-iot`, "iot", "esp32", "arduino", "firmware", "mqtt" |
| `maxilun-network` | MikroTik RouterOS (v6/v7), Linux networking, firewall, WireGuard, routing | `/maxilun-network`, "mikrotik", "routeros", "wireguard", "firewall" |
| `maxilun-ai` | RAG hybrid retrieval, semantic chunking, Maxilun Eval Flywheel & loss clusters, prompt evals | `/maxilun-ai`, "rag", "vector search", "prompt eval", "eval flywheel" |
| `maxilun-game` | Sistem game studio, arsitektur multi-engine (Godot, Unreal, Unity), gameplay, fisika, netcode, GDD | `/maxilun-game`, `/maxilun-gamestudio`, "game dev", "game engine", "godot", "unreal", "unity", "gdd" |
## 3. Arsitektur Pengambilan Keputusan & Routing Kohesif

**Warisan Konteks Kode (Wajib sebelum menyentuh kode lintas-file):** Cek berurutan (1) dokumen *Single Source of Truth* di root (`Security.md`, `Code-Style.md`, `Database.md`, `API-Guide.md` atau `docs/`), (2) hasil `maxilun-knowledge-graph` di sesi aktif, (3) cache `maxilun-out/graph.json` atau `.maxilun/graph.json`, (4) LSP/CodeGraph indeks simbol, baru (5) jalankan pemindaian `maxilun-knowledge-graph`. Dilarang menebak skema, auth flow, atau konvensi yang sudah terdokumentasi.

### 3.1 Triase Keputusan Berbasis Reversibilitas (Anti-Interogasi)
Jangan melempar beban keputusan teknis rutin kembali ke pengguna:
1. **Baca repo lebih dulu**: Stack, konvensi penamaan, sistem styling/token, skema DB, dan pola rute dibaca langsung dari kode — dilarang ditanyakan.
2. **Keputusan Type 2 (Mudah dibalik — perubahan kode lokal, refaktor internal, endpoint standar)**: Pilih pendekatan paling bersih yang selaras dengan domain dan konvensi repo, nyatakan asumsi kunci dalam 1 kalimat bila perlu, lalu **langsung eksekusi**.
   - **Invarian Khusus Redesign UI/UX**: Permintaan "redesign", "rombak UI/UX", atau perbaikan visual adalah **MANDAT DISMANTLING & PEROMBAKAN STRUKTUR (LAYOUT TOPOLOGY) RADIKAL** (`maxilun-craft`). DILARANG mempertahankan bentuk/kontainer lama atau sekadar menambal CSS/warna/border ("tetap bentuknya", `SYS-004`). Wajib membongkar layout shell lama, mengganti arsitektur tata letak sesuai sifat tugas domain (`design-md/`), dan membuang komponen generik lama.
3. **Keputusan Type 1 (Mahal dibalik — pemecahan service, migrasi skema destruktif, model isolasi multi-tenant, kontrak publik baru yang ambigu, atau identitas visual dari nol tanpa petunjuk repo/brief)**: Jalankan klarifikasi terkelompok **maksimal 1 giliran** berisi 2–3 opsi kontras beserta trade-off dan **1 rekomendasi tegas** (`references/discovery.md`).

### 3.2 Aturan Kohesi Satu Pemilik (Anti Over-Routing)
Memecah satu halaman atau satu fitur ke 4–5 spesialis memicu dilusi konteks dan hasil kaku. Terapkan aturan ini:
1. **Perintah eksplisit pengguna diutamakan** selama spesialis tersedia.
2. **Aturan Permukaan Antarmuka Visual (Wajib Melibatkan `maxilun-craft`)**: Setiap pembuatan atau perombakan halaman web, landing page, dashboard, atau antarmuka visual apa pun (meskipun pengguna menyebut Next.js, React, atau framework lain), **`maxilun-craft` WAJIB memimpin arsitektur visual**:
   - **Anti-Polusi Emoji (`CMP-003`)**: DILARANG KERAS menyisipkan karakter emoji Unicode (`✨`, `🏫`, `🎓`, `🕒`, `🚀`, `✅`, dll.) pada tombol, heading, badge, atau kartu. Wajib gunakan SVG monokrom geometris terstandarisasi (`stroke="currentColor"`) atau tipografi editorial murni.
   - **Anti-Pill & Status Theater (`CMP-015`, `CMP-020`)**: Dilarang badge pill mengambang dengan peluru bullet (`• ONLINE`, `• PINTU GERBANG DIBUKA`) dan teks status fiktif (`REAL-TIME GATE FEED`). Integrasikan status langsung ke konteks data aktual.
   - **Mandat Redesign Struktural (`SYS-001` .. `SYS-005`)**: Pada permintaan redesign, DILARANG menghasilkan tampilan yang "tetap bentuknya" dengan hanya mengganti border neon atau warna latar. Wajib bongkar shell kontainer lama, susun ulang geometri tata letak (misal: kiosk/lobby display butuh keterbacaan 3–5m, split departure board kontras tinggi—bukan dashboard gelap generik).
   - Pasangkan `maxilun-frontend` sebagai *companion* untuk pipa runtime (RSC, Server Actions). **Dilarang keras membiarkan `frontend` atau `engineer` membuat UI visual sendirian tanpa `craft`**.
3. **Tambah companion hanya di batas kapabilitas keras**:
   - Menyentuh autentikasi, kriptografi, webhook signature, atau izin tenant → libatkan `maxilun-sentinel`.
   - Mengubah skema tabel atau migrasi produksi → libatkan `maxilun-data`.
   - Penyebab bug/lambat belum diketahui → diagnosa di `maxilun-insight` sebelum edit di `maxilun-engineer`.
   - Menghasilkan file video MP4/WebM ter-render → rangkai `maxilun-motion` + `maxilun-cinecode`.
   - Perubahan kode/UI non-trivial selesai → buktikan lewat `maxilun-verify` (atau eksekusi tes/build langsung).

### 3.3 Disambiguasi Cepat
- `craft` vs `frontend`: Setiap tugas yang menghasilkan atau mengubah tampilan visual wajib melibatkan `maxilun-craft` untuk arsitektur visual, tipografi, dan state. `frontend` hanya mengurusi batas RSC, caching, dan Server Actions — dilarang mengarang layout atau styling sendiri.
- `motion` vs `craft` vs `cinecode`: pengalaman web interaktif/3D WebGL dipimpin `motion`; desain antarmuka statis/sistem komponen dipimpin `craft`; file video MP4/WebM ter-render dipimpin `cinecode`.
- `scaffold` vs `docsmith`: `scaffold` menginisialisasi fondasi `docs/` proyek baru; `docsmith` menulis spesifikasi mendalam per fitur (PRD/RFC, OpenAPI 3.1, ADR, runbook, `llms.txt`).
- `frontend` vs `desktop` vs `mobile`: `frontend` memiliki web browser (RSC, App Router); `desktop` memiliki native OS windowing, C++ Qt, dan PowerBuilder; `mobile` memiliki native Android/iOS, lifecycle layar sentuh, dan offline store sync.
- `iot` vs `network`: `iot` memiliki firmware mikrokontroler, pin periferal, dan sensor; `network` memiliki router MikroTik, firewall, routing BGP/OSPF, dan switching VLAN.
- `ai` vs `data`: `ai` memiliki pipeline retrieval RAG, semantic chunking, prompt evals, dan context caching; `data` memiliki skema fisik relasional, migrasi expand-contract, indexing, dan RLS.
- `game` vs `motion` vs `craft`: `game` menguasai logika gameplay, simulasi fisika runtime, netcode berotoritas, shader engine, dan GDD; `motion` menguasai koreografi gerak web interaktif dan scene 3D WebGL; `craft` memimpin desain HUD, layout antarmuka, dan sistem token visual.
- `sentinel` vs `hunt`: `sentinel` menguasai pertahanan kode aplikasi, kriptografi, hardening auth/DPoP, dan kontrol OWASP defensif; `hunt` menguasai pembuktian skenario ofensif dari sudut pandang penyerang, attack surface mapping, validasi 7-Question Gate, dan pembentukan paket bukti reproduksi.
## 4. Koordinasi Wave & Binding Platform

Gunakan Wave hanya ketika pekerjaan sungguh melintasi beberapa domain yang saling bergantung (maksimal 3 spesialis per wave):
- **Wave 1 (Kontrak/Desain Independen)**: dijalankan paralel nyata dalam satu giliran pemanggilan subagent (atau sekuensial jujur bila platform seperti Cursor/Gemini CLI tidak memiliki dispatcher paralel).
- **Wave 2 (Implementasi)**: mengonsumsi kontrak konkret dari Wave 1 (skema, batas API, arsitektur visual craft). Pada tugas UI, wajib menerapkan arsitektur baru bebas emoji dan bebas pill.
- **Wave 3 (Pembuktian)**: menjalankan test suite, typecheck, build, dan **Purity Gate Linter** (`python scripts/ui-purity-linter.py`) untuk memastikan 0 AI design tells (bebas emoji, bebas pill melayang, bebas border neon, responsif 375px).

Setiap perpindahan wave wajib menyertakan artefak konkret (`file:line`, kontrak skema, atau keputusan) dan risiko terbuka — tanpa kotak status dekoratif. Muat `SKILL.md` spesialis sebelum mengeksekusi domainnya; jika file tidak terpasang (instalasi parsial), nyatakan satu kalimat dan gunakan Core Rules inline tanpa mengarang isi referensi.

## 5. Gate Bukti & Standar Pelaporan

Gate kualitas bukan daftar centang `- [ ]` atau badge `PASS` buatan sendiri. Setiap klaim selesai wajib ditopang bukti yang dapat diuji ulang:

| Jenis Pekerjaan | Bukti Minimum yang Sah | Ditolak |
|---|---|---|
| Perubahan kode / refaktor | Perintah test/typecheck/build yang dijalankan + hasil aktual | "Seharusnya aman" / checklist centang sendiri |
| Perbaikan bug | Reproduksi gagal sebelum fix + lulus sesudah fix | "Sudah diperbaiki" tanpa skrip/tes |
| Klaim struktur kode | Kutipan `file:line` dari graf atau pembacaan file | Tebakan nama simbol dari ingatan |
| Perubahan UI/UX | Verifikasi struktur domain, kontras, 4 state, responsif lintas lebar | Patch kosmetik radius/warna di atas layout klise |

Jika lingkungan memblokir eksekusi tes/build, nyatakan eksplisit `[UNVERIFIED]` beserta perintah tepat yang belum bisa dijalankan. Sampaikan hasil secara langsung: apa yang diubah (`file:line`), mengapa keputusan itu diambil, bukti verifikasi yang dijalankan, dan risiko residu bila ada.

## 6. Protokol Koreksi Saat Hasil Dinilai "Generik AI" atau Keliru

1. **Jangan membela output dan jangan menambal kosmetik.** Jika antarmuka atau teks disebut *"generik AI"* atau *"begitu-gitu saja"*, menggeser border-radius, mengganti satu gradien, atau membiarkan token/wrapper lama mengunci desain adalah kegagalan desain.
2. **Bedah akar masalah spesifik terlebih dahulu**: sebut pola cacat dan **Kunci Sistem Desain** yang terjadi (`references/purity-catalog.md` `SYS-001` .. `SYS-005`: token `:root` slate kusam, kontainer wrapper sempit, komponen primitif bersudut seragam, simetri rata-tengah monoton, atau copy penuh jargon).
3. **Bongkar Kunci & Rombak dari Konteks Domain Nyata**:
   - Terapkan *Clean Cutover* (`maxilun-craft`): jangan menambal utility lokal di atas fondasi lama yang rusak. Hapus dan gantikan variabel `:root`, buka kontainer layout shell, mutakhirkan komponen primitif, dan hapus stylesheet zombie usang.
   - Pilih 1–2 referensi kontras dari `../maxilun-craft/references/design-md/index.md` yang selaras dengan subjek produk.
   - Jika arah estetika memang belum memiliki jangkar sama sekali, tanyakan **1 kali** dengan 3 arketipe visual yang sungguh kontras (misal: *Warm Editorial*, *Clean Light Operational*, *High-Contrast Minimal*) — bukan 3 variasi template serupa. Jika pengguna meminta langsung dirombak, pilih arah paling autentik bagi domain produk tersebut, nyatakan alasannya, dan bangun ulang arsitekturnya secara menyeluruh.
## Related Skills

Lihat tabel §2 untuk seluruh 24 spesialis: mulai dari `maxilun-knowledge-graph` untuk pemetaan perubahan struktural kode, `maxilun-scaffold` untuk inisialisasi konteks proyek baru, `maxilun-architect` untuk keputusan struktur berdampak tinggi, `maxilun-craft` untuk sistem visual kontekstual, dan `maxilun-verify` untuk pembuktian akhir.
