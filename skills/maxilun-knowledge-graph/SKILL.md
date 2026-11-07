---
name: maxilun-knowledge-graph
description: >
  Code discovery foundation. Maps symbols, imports, caller/callee edges, and blast
  radius as a directed graph before structural or multi-file changes. Uses direct
  inspection for trivial isolated edits and clean search/read fallback when graph
  tooling is unavailable. Triggers: "/maxilun-knowledge-graph", "/msal-trace",
  "/msal-graph", "cari kode", "di mana fungsi", "petakan dependensi", "siapa panggil",
  "relasi modul", "analisis impor", codebase lookup, navigation, pre-edit mapping.
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
    - references/ast-graph-specifications.md
---

# Maxilun Knowledge Graph

Fondasi penemuan kode dan analisis dampak perubahan untuk ekosistem Maxilun. Memperlakukan repositori sebagai graf terarah (*directed graph* dengan node berkas/simbol dan edge `IMPORTS`, `CALLS`, `IMPLEMENTS`, `EXTENDS`, `EXPOSES`) agar spesialis menemukan koordinat `file:line` dan seluruh pemanggil terdampak secara presisi tanpa membaca berkas penuh tanpa arah.

## Skill Contract

- **Owns**: symbol and file discovery, caller/callee tracing, module import relationships, circular dependency detection, and structural blast-radius maps.
- **Does not own**: architectural trade-off decisions (`maxilun-architect`), code modifications (`maxilun-engineer`), or runtime bug root-cause claims without execution evidence (`maxilun-insight`).
- **Inputs**: target symbol, route, module path, or planned structural change.
- **Outputs**: verified `file:line` coordinates, inbound/outbound edges, resolution precision tags (`[exact]`, `[name-only]`, `[DIRECT]`), and unresolved dynamic lookup boundaries.
- **Handoff**: return the factual impact map directly to the requesting specialist (`maxilun-engineer`, `maxilun-architect`, `maxilun-data`, `maxilun-frontend`, `maxilun-insight`, `maxilun-verify`); never edit target source files during discovery.

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

## 1. Cakupan Bahasa & Akurasi Scanner

Mesin pemindai di `<skill-dir>/scanner/` memetakan kode secara bertingkat sesuai bahasa repositori:

| Tingkat Pemindai | Bahasa yang Didukung | Ekstraksi Struktural |
|---|---|---|
| **Deep AST / Structural** (`python_scanner.py`, `typescript_scanner.py`) | Python (`.py`), TypeScript/JavaScript (`.ts`, `.tsx`, `.js`, `.jsx`) | Definisi fungsi/method/class, impor relatif & paket, `EXTENDS`/`IMPLEMENTS`, rute `EXPOSES`, serta edge panggilan `CALLS` |
| **Polyglot Generic + Tier 2** (`generic_scanner.py` + LSP/`grep`) | Go, Rust, Java, Kotlin, C#, Ruby, PHP, Swift, C/C++ | Deklarasi fungsi/class/struct/enum dan `IMPORTS`; padukan dengan LSP atau `grep` simbol Tier 2 untuk verifikasi situs panggilan `CALLS` |

## 2. Kontrak Fondasi

1. **Peta Sebelum Perubahan Struktural**: Sebelum mengubah tanda tangan fungsi, kontrak API, skema bersama, atau relasi lintas-modul, petakan definisi dan pemanggil simbol yang terdampak terlebih dahulu.
2. **Koordinat Graf sebagai Acuan Eksekusi**: Situs `file:line` yang terkonfirmasi menjadi titik baca rentang dan titik edit langsung bagi spesialis eksekutor tanpa membaca ulang berkas penuh.
3. **Berhenti Saat Bukti Lengkap**: Hentikan penelusuran segera setelah definisi simbol dan seluruh situs panggilan/impor yang relevan terkonfirmasi.
4. **Jalur Cepat Tugas Trivial**: Lewati pemindaian graf penuh untuk perbaikan salah ketik, teks statis, atau perubahan lokal satu baris yang tidak menggeser kontrak lintas-berkas.

## 3. Tangga Pencarian

Jalankan urutan paling ringan yang menuntaskan pemetaan tanpa kerja ganda:
1. **Tier 0 — Memori Sesi & Cache Aktif**: Gunakan peta simbol yang sudah terkonfirmasi di sesi ini, atau baca langsung cache `maxilun-out/graph.json` maupun `.maxilun/graph.json` bila sudah ada di repositori tanpa memindai ulang dari nol.
2. **Tier 1 — CLI Knowledge Graph & Indeks Bahasa**:
   - Panggil `cli.py` relatif terhadap direktori tempat skill ini terpasang (`<skill-dir>`):
     - Bangun artefak lengkap (`maxilun-out/graph.json`, `maxilun-out/lens.html`, `maxilun-out/MAXILUN_REPORT.md`): `python <skill-dir>/cli.py scan <repo-path>` (atau simpan khusus ke `.maxilun/graph.json` menggunakan `-o`).
     - Kueri simbol terhadap cache atau path target: `python <skill-dir>/cli.py query <operator> <simbol> --path <repo-path>`.
   - Manfaatkan pula LSP lingkungan atau CodeGraph MCP bila tersedia.
3. **Tier 2 — Pencarian Simbol Terstruktur**: Jalankan `glob` dan `grep` terfokus per nama simbol/impor secara paralel (bukan kata kunci kabur) untuk memastikan kandidat ambigu atau registrasi dinamis.
4. **Tier 3 — Baca Rentang Baris**: Baca hanya rentang baris di sekitar `file:line` yang ditemukan guna memverifikasi argumen dan konteks lokal.

**Invalidasi Cache**: Lakukan scan ulang hanya ketika berkas baru ditambah/dihapus/dipindahkan, simbol publik diganti namanya, refaktor lintas banyak berkas mengubah arah impor, atau pengguna secara eksplisit meminta pembaruan graf.

## 4. Tata Bahasa Query Simbol (Symbol Query Grammar)

Ekspresikan kueri relasi menggunakan operator presisi berikut:

| Operator | Makna Relasi | Contoh Eksekusi CLI |
|---|---|---|
| `defOf:` | Lokasi deklarasi & tanda tangan simbol | `python <skill-dir>/cli.py query defOf: validateToken` |
| `callsIn:` | Seluruh pemanggil simbol (*inbound callers*) | `python <skill-dir>/cli.py query callsIn: processPayment` |
| `callsOut:` | Simbol lain yang dipanggil oleh target | `python <skill-dir>/cli.py query callsOut: checkoutHandler` |
| `importersOf:` | Berkas yang mengimpor modul/path target | `python <skill-dir>/cli.py query importersOf: src/config/keys.ts` |
| `implementsOf:` | Class yang mengimplementasikan interface | `python <skill-dir>/cli.py query implementsOf: PaymentGateway` |
| `extendsOf:` | Subclass yang mewarisi class dasar | `python <skill-dir>/cli.py query extendsOf: BaseRepository` |
| `routesOf:` | Endpoint rute yang mengekspos handler | `python <skill-dir>/cli.py query routesOf: usersController` |

- **Skala Kueri Proporsional**: Jalankan kueri mengikuti *fan-out* nyata simbol yang ditelusuri (paralelkan pencarian simbol independen tanpa batas angka kueri sembarang, namun hindari pengulangan kueri identik).
- **Label Presisi Resolusi**: Tandai `[exact]` bila edge terkonfirmasi lewat path impor atau deklarasi unik, dan `[name-only]` bila pencocokan berbasis nama memiliki lebih dari satu kandidat sehingga wajib dipastikan via bacaan rentang Tier 2/3.

## 5. Penelusuran Dampak & Deteksi Siklus

- **Inbound Blast Radius**: Sebelum mengubah nama, parameter, tipe kembalian, atau semantik error simbol, kumpulkan seluruh pemanggil produksi (`callsIn:`), berkas pengimpor/re-export (`importersOf:`), serta berkas tes terkait. Periksa kemungkinan pemanggilan dinamis (event bus, refleksi, DI container, dynamic `import()`).
- **Outbound Side Effects**: Telusuri `callsOut:` untuk mengidentifikasi mutasi database, panggilan jaringan eksternal, publikasi antrean, atau state bersama yang tersentuh.
- **Deteksi Siklus Impor**: Ungkap ketergantungan melingkar langsung maupun transitif (`A -> B -> A`) yang berpotensi memicu referensi `undefined` saat inisialisasi modul, lalu serahkan opsi pemisahan kontrak ke `maxilun-architect` atau `maxilun-engineer`.

## 6. Pelaporan Faktual Lokasi Simbol

Laporkan hasil penelusuran secara ringkas dan faktual dalam format `file:line` tanpa kotak atau ikon emoji:

```text
# Pencarian simbol langsung
validateToken -> src/auth/jwt.ts:42 [exact]
callsIn (3): src/middleware/authGuard.ts:18, src/routes/users.ts:25, tests/auth.test.ts:40

# Peta dampak refactor lintas-berkas
Target   : validateToken(token, opts) di src/auth/jwt.ts:42 [exact]
Inbound  : src/middleware/authGuard.ts:18 [exact], src/routes/users.ts:25 [exact], tests/auth.test.ts:40 [exact]
Outbound : crypto.subtle (stdlib), src/config/keys.ts:12 [exact]
Dampak   : 2 berkas produksi, 1 berkas tes, 0 re-export publik di luar src/auth/
```

## 7. Mode Adaptif Tanpa Indexer

Uji ketersediaan `python` dan artefak graf sekali pada awal sesi. Bila `cli.py`, cache `graph.json`, maupun LSP tidak tersedia di lingkungan target, langsung gunakan kombinasi `glob`, `grep` simbol presisi, dan `read` rentang baris tanpa menarasikan kegagalan alat, serta tandai hasil pelacakan manual dengan `[DIRECT]`.

## 8. Visualisasi Graf

Untuk penjelajahan visual interaktif WebGL 3D Galaxy & 2D Force-Directed Matrix (`maxilun-out/lens.html` serta laporan arsitektur `maxilun-out/MAXILUN_REPORT.md`), ikuti panduan di [LENS.md](./LENS.md). Muat [LENS.md](./LENS.md) hanya saat pengguna secara eksplisit meminta `/graph`, `/msal-graph`, atau visualisasi graf.

## Related Skills

- **maxilun-engineer**: Eksekusi perubahan kode dan migrasi seluruh caller berdasarkan peta `file:line`
- **maxilun-architect**: Evaluasi batas modul, pemutusan siklus dependensi, dan analisis *blast radius* arsitektural
- **maxilun-insight**: Korelasi peta pemanggil statis dengan jejak *stack trace* dan diagnosis performa runtime
- **maxilun-data**: Penelusuran pemakaian model ORM, repositori, dan kueri sebelum migrasi skema
- **maxilun-frontend**: Pemetaan pohon komponen Next.js/React dan penyebaran batas `'use client'`
- **maxilun-verify**: Penentuan cakupan tes regresi berdasarkan modul yang masuk dalam radius dampak
