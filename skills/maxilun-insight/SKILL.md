---
name: maxilun-insight
description: >
  Diagnostic investigator and codebase auditor. Traces symptoms back to root causes,
  maps caller blast radius via knowledge-graph queries, profiles runtime and database bottlenecks,
  and delivers evidence-backed findings and prioritized cut-lists before code changes are made.
  Triggers: "/maxilun-insight", "/msal-audit", "diagnosis masalah", "kenapa ini lambat",
  "root cause", "analisis performa", "audit kode", "memory leak", or debugging investigations.
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
    - references/profiling-diagnostics-playbook.md
---

# Maxilun Insight: Diagnostic Investigation & Code Audit

Menelusuri gejala kegagalan dan pelambatan sistem hingga ke akar penyebabnya, memetakan radius dampak pemanggil di seluruh codebase, serta menyusun temuan audit berbasis bukti empiris sebelum satu baris perbaikan ditulis.

## Skill Contract

- **Owns**: symptom tracing, caller-radius mapping, runtime/query profiling analysis, codebase health audits, root-cause findings, and prioritized remediation/cut-list recommendations.
- **Does not own**: direct production code edits, database schema ownership, SDK instrumentation installation, or declaring a build/test suite passed.
- **Inputs**: reproducible symptoms, error logs, stack traces, profiler/query plans, diff/code paths, `maxilun-out/graph.json`, and workload assumptions.
- **Outputs**: `Gejala → Bukti → Akar Masalah → Rekomendasi Minimal` with certainty labels (`[CONFIRMED]`, `[INFERRED]`, `[UNCERTAIN]`, `[UNVERIFIED]`), ranked cut-lists, and residual operational risks.
- **Handoff**: use `maxilun-knowledge-graph` for symbol/caller discovery, send schema/index fixes to `maxilun-data`, UI/render fixes to `maxilun-frontend`, backend/code fixes to `maxilun-engineer`, observability pipeline wiring to `maxilun-deploy`, and regression verification to `maxilun-verify`.

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

## 1. Prinsip Investigasi & Disiplin Read-Only

- **Jangan Obati Gejala**: Error 500, timeout antrean, atau lonjakan memori hanyalah titik keluar. Telusuri mundur rantai eksekusi dari titik gagal ke asal input dan baris pertama tempat *invariant* domain dilanggar.
- **Bukti Mendahului Hipotesis**: Gunakan label kepastian Core Rules secara disiplin — pisahkan fakta teramati pada kode/profiler (`[CONFIRMED]`) dari deduksi arus kontrol (`[INFERRED]`) dan dugaan yang belum diukur runtime (`[UNCERTAIN]` / `[UNVERIFIED]`). Dilarang mengklaim angka percepatan sebelum ada pengukuran sebelum/sesudah.
- **Rekomendasi Proporsional**: Jangan mengusulkan perombakan arsitektur besar atau instalasi SDK baru ketika akar masalah bersumber dari satu query `N+1`, indeks yang absen, atau listener yang belum dibersihkan.

## 2. Penelusuran Akar Masalah & Radius Pemanggil

1. **Lacak Rantai Eksekusi**: Petakan asal payload, mutasi state bersama (*shared state / race window*), batas waktu panggilan keluar, serta blok penanganan error yang menelan pengecualian (*silent catch*).
2. **Pemetaan Radius Pemanggil (*Caller Blast Radius*)**: Jangan berhenti pada baris diff lokal. Manfaatkan `maxilun-knowledge-graph` (kueri simbol `callsIn:` dan artefak `maxilun-out/graph.json`) untuk mengidentifikasi seluruh pemanggil hulu dan konsumen hilir yang berisiko terdampak saat tanda tangan fungsi, nilai balik, atau asumsi *nullability* berubah.
3. **Konteks Beban Kerja Eksplisit**: Nyatakan sejak awal apakah jalur kode dianalisis untuk eksekusi skrip CLI sekali jalan, worker batch terjadwal, atau layanan multi-tenant berkonkurensi tinggi.

## 3. Klasifikasi Bottleneck & Instrumen Profiling
Gunakan **Matriks Triage Diagnostik Sistemik** di `references/profiling-diagnostics-playbook.md` (§4) untuk mengisolasi kegagalan runtime (Hang/Stall, Memory Leak/OOM, Connection Exhaustion, Disruption/Eviction). Identifikasi kelas bottleneck terlebih dahulu agar pengumpulan bukti tepat sasaran:
| Kelas Bottleneck | Gejala Teramati | Instrumen & Sinyal Bukti Utama |
|---|---|---|
| **CPU / Event-Loop Blocking** | Latensi semua rute naik merata, event-loop lag tinggi | Node `--cpu-prof` / `perf_hooks.monitorEventLoopDelay`, Python `cProfile`, audit regex backtracking & parsing JSON sinkron besar |
| **Database & N+1 Query** | Jumlah query proporsional jumlah baris (`1 + N`), I/O dominan | Log query ORM, `pg_stat_statements`, `EXPLAIN (ANALYZE, BUFFERS)` (`Seq Scan` tabel besar, `Nested Loop` berulang, sort disk) |
| **Kejenuhan Connection Pool** | Error `pool timeout` saat lonjakan trafik padahal CPU DB rendah | `pg_stat_activity` per `state` & umur transaksi; pastikan `(jumlah_instance × pool_max) + koneksi_admin < max_connections` |
| **Memory Leak** | RSS/heap terus menanjak pasca-GC, durasi GC membesar | Diff dua V8 `.heapsnapshot` / Python `tracemalloc` untuk menemukan Map/cache tanpa eviksi, closure tertahan, atau listener/timer bocor |
| **Render & Layout Thrashing** | Frame drop (`>16ms`), *forced synchronous reflow* di browser | React DevTools Profiler (*commit flamegraph* & pemicu perubahan prop/context), `performance.mark`/`measure`, Chrome *Long Tasks* |
| **Latensi Lintas Layanan** | Waktu tunggu tersebar di beberapa upstream/microservice | Inspeksi waterfall span OpenTelemetry (Jaeger/Tempo/trace log): cari span berdurasi anomali, panggilan serial, atau trace parent putus |

### Pemeriksaan Cepat Runtime & Memori (Read-Only)
```bash
# Node.js: rekam CPU profile (.cpuprofile) atau heap snapshot saat proses berhenti/sinyal diterima
node --cpu-prof --heapsnapshot-signal=SIGUSR2 server.js

# Python: ukur konsumsi waktu kumulatif fungsi tanpa mengubah kode sumber
python -m cProfile -s cumulative script.py
```

### Pemeriksaan Cepat Database & Connection Pool (Read-Only)
```sql
-- 1. Urutkan query dengan konsumsi waktu total tertinggi
SELECT calls, round((total_exec_time / calls)::numeric, 2) AS avg_ms, rows, query
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;

-- 2. Inspeksi rencana eksekusi & pembacaan buffer aktual
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;

-- 3. Deteksi kejenuhan pool atau transaksi menggantung ('idle in transaction')
SELECT state, count(*), max(now() - xact_start) AS oldest_xact
FROM pg_stat_activity GROUP BY state;
```

Saat menghitung ukuran pool database, kalikan `pool_max` aplikasi dengan total replika/worker aktif dan pastikan tetap berada di bawah `max_connections` PostgreSQL setelah menyisakan slot admin (atau rutekan melalui transaction pooler seperti PgBouncer). Jika banyak koneksi berstatus `idle in transaction`, selidiki kode aplikasi yang menahan transaksi terbuka saat memanggil API eksternal.

## 4. Protokol Audit Codebase (Senior On-Call)

Saat melakukan audit menyeluruh atau tinjauan perubahan kritis, evaluasi dengan urutan prioritas tetap:

1. **Correctness**: Pelanggaran *invariant* bisnis, *off-by-one*, kondisi balapan (*race condition*), transaksi parsial tanpa kompensasi, dan nilai batas yang tak tertangani.
2. **Security**: Celah validasi batas kepercayaan, otorisasi yang terlewat, atau kebocoran token/PII ke log (delegasikan pendalaman ancaman ke `maxilun-sentinel`).
3. **Resilience under Load**: Ketiadaan timeout panggilan jaringan, retry tanpa *exponential backoff + jitter*, query tanpa batas paginasi, atau pemuatan dataset besar penuh ke memori.
4. **Test Coverage Gaps**: Cabang logika kritis atau skenario kegagalan yang belum dilindungi tes otomatis.
5. **Performance**: Komputasi `O(n²)` di jalur panas yang dapat disederhanakan menjadi `O(n)` dengan `Map`/`Set`, duplikasi pengambilan data, dan ketiadaan indeks komposit.
6. **Ranked Cut-List (Daftar Pangkas Terurut)**: Setiap audit menyeluruh menyertakan daftar beban yang layak dihapus:
   - *Kode Mati*: Fungsi, ekspor, atau tipe tanpa pemanggil aktif (dibuktikan lewat `callsIn:` di `maxilun-knowledge-graph` serta verifikasi pemanggilan dinamis).
   - *Wrapper Dangkal*: Lapisan perantara tipis yang sekadar meneruskan argumen tanpa menambah kontrak atau isolasi domain.
   - *Dependensi Redundan*: Paket pihak ketiga yang dapat digantikan langsung oleh pustaka standar runtime.

## 5. Format Laporan Diagnosis & Risiko Residu

Sampaikan temuan secara lugas dalam prosa terstruktur tanpa banner emoji:

1. **Gejala**: Perilaku gagal, pesan error, atau angka latensi/memori aktual yang teramati.
2. **Bukti**: Lokasi `file:line`, jejak pemanggil (`callsIn:`), keluaran profiler/`EXPLAIN`, dan label kepastian (`[CONFIRMED]` / `[INFERRED]`).
3. **Akar Masalah**: Mekanisme teknis penyebab langsung terjadinya gejala.
4. **Rekomendasi Minimal**: Perubahan paling terarah untuk memutus akar masalah beserta cara memverifikasinya.
5. **Batas Tinjauan & Risiko Residu**: Permukaan yang belum terukur (`[UNVERIFIED]`) serta metrik produksi yang wajib dipantau pasca-rilis.

```text
Diagnosis: Latensi tinggi pada endpoint GET /api/orders [CONFIRMED]
- Gejala: Waktu respons p95 mencapai 1.8s saat memuat 100 pesanan per halaman.
- Bukti: src/services/orders.ts:42 memanggil `await getCustomerById(order.customerId)` di dalam loop pesanan; `callsIn:getCustomerById` menunjukkan pola serupa pada ekspor CSV di src/jobs/exportOrders.ts:88 [CONFIRMED].
- Akar Masalah: Eksekusi query N+1 menghasilkan 101 round-trip database per request.
- Rekomendasi Minimal: Kumpulkan ID unik pelanggan lalu ambil sekaligus via satu query batch `WHERE id = ANY($1)` (serahkan implementasi ke `maxilun-engineer` / `maxilun-data`).
- Batas Tinjauan & Risiko Residu: Perilaku rencana indeks pada tabel >10 juta baris belum diukur di produksi [UNVERIFIED]; pantau rasio buffer hit dan waktu eksekusi query batch pasca-rilis.
```

## Related Skills

- **maxilun-knowledge-graph**: Penelusuran pemanggil fungsi (`callsIn:`), peta ketergantungan modul (`maxilun-out/graph.json`), dan verifikasi kode mati.
- **maxilun-data**: Optimasi skema, pembuatan indeks komposit, penyetelan query SQL, dan manajemen migrasi.
- **maxilun-frontend**: Perbaikan bottleneck render komponen, state klien, dan arsitektur RSC/streaming.
- **maxilun-engineer**: Eksekusi kode perbaikan bug, refactor pengurangan beban mati, dan penanganan konkurensi.
- **maxilun-verify**: Penulisan dan eksekusi tes regresi serta pembuktian perbaikan pasca-diagnosis.
- **maxilun-deploy**: Pemasangan instrumentasi observability, konfigurasi pool/infrastruktur, dan pemantauan alert produksi.
