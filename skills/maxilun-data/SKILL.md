---
name: maxilun-data
description: >
  Database & data layer specialist for schema design, zero-downtime migrations,
  ORM and query boundaries, indexing strategy, EXPLAIN analysis, database selection,
  and multi-tenant RLS isolation across PostgreSQL, SQLite/libSQL, MySQL, Redis,
  and ClickHouse. Triggers: "/maxilun-data", "skema database", "migrasi",
  "indeks query", "ORM", "optimasi database", "desain tabel", or any data layer task.
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
    - references/zero-downtime-migrations.md
    - references/query-optimization-explain.md
---

# Maxilun Data: Database & Data Layer Engineering

Bertanggung jawab atas rekayasa lapisan data: desain skema relasional yang menjaga integritas di tingkat database, migrasi *Expand-Contract* tanpa henti layanan, eliminasi pola kueri `N+1`, strategi indeks berbasis bukti `EXPLAIN`, pemilihan mesin penyimpanan sesuai profil beban kerja, serta isolasi data *multi-tenant*.

## Skill Contract

- **Owns**: database schemas, DDL/DML migrations, indexing plans, ORM/query-builder boundaries, transaction scoping, query optimization, and database-level tenant isolation (RLS).
- **Does not own**: service-boundary decomposition (`maxilun-architect`), application auth/encryption policy (`maxilun-sentinel`), general runtime profiling outside data access (`maxilun-insight`), or infrastructure provisioning (`maxilun-deploy`).
- **Inputs**: domain entities and invariants, read/write access patterns, existing schema and migrations (`maxilun-knowledge-graph`), query plans, and uptime/consistency constraints.
- **Outputs**: normalized or evidence-backed schemas, reversible/zero-downtime migration steps, measured index/query remedies, and explicit rollback plans.
- **Handoff**: align bounded contexts and partitioning strategy with `maxilun-architect`, review PII/IDOR/encryption controls with `maxilun-sentinel`, diagnose systemic contention with `maxilun-insight`, implement repository/ORM code with `maxilun-engineer`, and prove migration/query regressions with `maxilun-verify`.

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

## 1. Desain Skema, Konvensi Brownfield/Greenfield & Audit

Periksa migrasi eksisting serta artefak `maxilun-knowledge-graph` (`maxilun-out/graph.json` atau `.maxilun/graph.json`) terlebih dahulu untuk memetakan model ORM, pemanggil repositori, dan konvensi database yang sedang berjalan.

- **Brownfield Dahulu**: Pada skema eksisting, patuhi secara konsisten penamaan tabel/kolom (`snake_case` vs `camelCase`), tipe Primary Key, dan alat migrasi repositori—dilarang mencampur dua konvensi di satu database.
- **Standar Greenfield**: Gunakan tabel `snake_case` jamak (`payment_transactions`), kolom `snake_case` tunggal, waktu UTC bertipe `TIMESTAMPTZ` berakhiran `_at`, dan Primary Key **`UUIDv7`** (terurut waktu, aman diekspos publik tanpa fragmentasi halaman B-tree `UUIDv4`) atau **`BIGINT GENERATED ALWAYS AS IDENTITY`** (kompak untuk join internal berkecepatan tinggi; hindari `SERIAL` lama).
- **Normalisasi & Constraint Database**: Mulai dari **3NF** dan tegakkan `NOT NULL`, `FOREIGN KEY`, `UNIQUE`, serta `CHECK` langsung di mesin database. Denormalisasi atau *materialized view* hanya dibenarkan bila terukur oleh profil beban baca dan memiliki mekanisme sinkronisasi eksplisit.
- **Audit Trail yang Aman bagi Sistem & Hard-Delete**: Jangan memaksakan `created_by UUID NOT NULL REFERENCES users(id)` bila baris dapat ditulis oleh *webhook*, *cron worker*, antrean sistem, atau bila akun pengguna dapat dihapus permanen:

```sql
created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
actor_type TEXT NOT NULL DEFAULT 'user', -- 'user' | 'system' | 'webhook'
actor_id   TEXT                          -- atau UUID NULL REFERENCES users(id) ON DELETE SET NULL
```

  Untuk tabel *ledger* atau *event log append-only*, simpan `created_at` saja tanpa `updated_at` dan larang `UPDATE`/`DELETE`.
- **Soft Delete sebagai Opt-In Domain (Bukan Dogma Universal)**: Tambahkan `deleted_at TIMESTAMPTZ NULL` **hanya** bila produk memang membutuhkan fitur *trash/restore* pengguna. Bila diaktifkan, wajib pasang *partial unique index* (`CREATE UNIQUE INDEX users_email_active_idx ON users (email) WHERE deleted_at IS NULL`), saring kueri baca default secara konsisten, dan sediakan prosedur *hard-delete*/anonimisasi nyata untuk kewajiban penghapusan data pribadi (GDPR/UU PDP).

## 2. Migrasi Zero-Downtime, Expand-Contract & Backfill

Jangan pernah melakukan `RENAME COLUMN`, mengubah tipe kolom yang memicu penulisan ulang tabel penuh, atau menahan *lock* eksklusif lama pada produksi aktif. Jalankan satu alur **Expand-Contract** terpadu:

1. **Expand (DDL Non-Blocking)**:
   - Tambah kolom baru sebagai *nullable* atau dengan `DEFAULT` konstanta statis (metadata-only di PostgreSQL 11+; hindari fungsi volatil ber-rewrite pada versi lama).
   - Bangun indeks di luar transaksi dengan `CREATE INDEX CONCURRENTLY`.
   - Pasang `FOREIGN KEY` atau `CHECK` baru pada tabel besar menggunakan `ADD CONSTRAINT ... NOT VALID`, lalu jalankan `VALIDATE CONSTRAINT` pada migrasi terpisah:

```sql
-- Langkah 1: pasang constraint instan tanpa memindai baris lama
ALTER TABLE orders ADD CONSTRAINT orders_customer_fk
  FOREIGN KEY (customer_id) REFERENCES customers(id) NOT VALID;
-- Langkah 2 (migrasi terpisah): validasi dengan SHARE UPDATE EXCLUSIVE ringan
ALTER TABLE orders VALIDATE CONSTRAINT orders_customer_fk;
```

2. **Dual-Write & Cursor Backfill**:
   - Deploy kode yang menulis ke representasi lama sekaligus baru.
   - Isi data historis secara idempoten dalam potongan berbasis *cursor* Primary Key (`WHERE id > $last_id ORDER BY id LIMIT 2000`, jangan pernah memakai `OFFSET` besar), setel `SET LOCAL lock_timeout = '2s'` dan `statement_timeout`, serta beri jeda sesuai metrik lag replika.
3. **Switch Reads & Contract**:
   - Alihkan pembacaan aplikasi ke kolom/tabel baru, pantau periode observasi hingga dipastikan nol *fallback*, hapus referensi kode lama, lalu lepas kolom/tabel usang (`DROP COLUMN`). Dokumentasikan eksplisit setiap langkah pembersihan yang *irreversible* beserta rencana pemulihannya.

## 3. Bentuk Query, Batas ORM & Eliminasi N+1

- **Eliminasi Loop `N+1` Tak Terbatas**: Jangan memakai angka batas kueri sembarang (seperti batas kaku 10 kueri); berantas pola di mana jumlah kueri bertambah mengikuti panjang daftar hasil (`O(N)`). Ganti kueri di dalam loop dengan `JOIN` eksplisit, pemuatan batch `WHERE parent_id = ANY($1)` (`include`/`with`/DataLoader), atau agregasi CTE tunggal. Pilih kolom spesifik daripada `SELECT *` pada tabel lebar atau kolom `JSONB` besar.
- **Batas Transaksi & Mutasi Massal**: Jaga transaksi sependek mungkin—dilarang memanggil HTTP pihak ketiga, mengirim email, atau mengeksekusi pekerjaan lambat di dalam transaksi terbuka. Setel `statement_timeout` eksplisit, gunakan `SELECT ... FOR UPDATE` atau *optimistic locking* (`WHERE version = $v`) untuk mutasi konkuren, dan gunakan multi-row `VALUES`, `UNNEST`, atau `COPY` untuk tulis massal.
- **Connection Pooling**: Ukur ukuran pool (`PgBouncer`, driver serverless HTTP/WS, atau pool aplikasi) berdasarkan kapasitas nyata `max_connections`, jumlah replika aplikasi, dan inti CPU database sambil menyisakan kuota koneksi admin dan migrasi.

## 4. Strategi Indexing & Bukti EXPLAIN

Jalankan **Alur 5-Langkah Optimasi Kueri Sistemik** di `references/query-optimization-explain.md` (§4: Baseline EXPLAIN $\to$ Scan Pruning $\to$ Spill-to-Disk Elimination $\to$ Query Rewrite & Covering Index $\to$ Comparative Proof). Ukur rencana kueri sebelum menambah indeks menggunakan `EXPLAIN` (dan `EXPLAIN (ANALYZE, BUFFERS)` hanya pada kueri baca atau di dalam staging/transaksi uji yang aman—jangan menjalankan mutasi produksi langsung dengan `EXPLAIN ANALYZE`):

| Sinyal pada `EXPLAIN (ANALYZE, BUFFERS)` | Diagnosis & Tindakan Rekayasa |
|---|---|
| *Estimated rows* meleset jauh (`>10x`) dari *actual rows* | Statistik tabel basi atau korelasi antar-kolom tinggi → jalankan `ANALYZE` atau `CREATE STATISTICS` |
| *Rows Removed by Filter* sangat besar pada Seq/Index Scan | Selektivitas indeks kurang tepat → susun indeks komposit **Equality (`=`) → Range (`>`,`<`) → Sort (`ORDER BY`)** |
| *Heap Fetches* tinggi pada jalur baca panas | Tambahkan kolom proyeksi ke **Covering Index (`INCLUDE (...)`)** dan pastikan *autovacuum* sehat |
| Predikat miring (mis. hanya `status = 'pending'` 2% baris) | Buat **Partial Index** (`WHERE status = 'pending'`) agar ukuran indeks kecil dan tulis tetap ringan |
| Pencarian di dalam `JSONB`, array, teks, atau deret waktu besar | Gunakan **GIN** untuk `JSONB`/`tsvector`/array dan **BRIN** untuk tabel *append-only* terurut waktu |

Pantau `pg_stat_user_indexes` secara berkala dan hapus indeks tak terpakai yang hanya memperbesar amplifikasi tulis (`INSERT`/`UPDATE`).

## 5. Pemilihan Database, Caching & Isolasi Multi-Tenant

| Mesin Penyimpanan | Profil Beban Kerja Utama | Catatan Arsitektural |
|---|---|---|
| **PostgreSQL** | Default utama OLTP relasional, ACID, `JSONB`, `tsvector`, `PostGIS`, `pgvector` | Pilihan pertama kecuali ada kendala topologi spesifik |
| **SQLite / libSQL** | Aplikasi *embedded*/CLI, *local-first*, baca dominan satu node, atau DB-per-tenant di edge | Aktifkan `PRAGMA journal_mode = WAL;` dan `busy_timeout`; penulis tunggal per file |
| **MySQL** | Ekosistem aplikasi mapan di atas InnoDB atau kluster sharding Vitess | Pertahankan konsistensi charset `utf8mb4` dan isolasi transaksi InnoDB |
| **Redis / Valkey** | Cache efemeral, *rate limiter*, *distributed lock*, sesi/antrean pendek | Bukan sumber kebenaran tunggal tanpa DB primer; cegah *cache stampede* dengan *single-flight* lock |
| **ClickHouse / DuckDB** | Analitik OLAP kolomnar, agregasi log/event masif, pelaporan historis | Pisahkan beban agregasi berat dari database transaksi OLTP |

### Isolasi Multi-Tenancy (PostgreSQL RLS) & Data Uji
Selaraskan model isolasi (*Shared Schema + `tenant_id`*, *Schema-per-Tenant*, atau *DB-per-Tenant*) dengan `maxilun-architect` dan `maxilun-sentinel`. Pada *Shared Schema*, tempatkan `tenant_id` sebagai kolom terdepan indeks komposit dan aktifkan **Row-Level Security** di mesin database:

```sql
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON invoices FOR ALL
  USING (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid);
-- Setel di dalam setiap transaksi request terverifikasi: SET LOCAL app.current_tenant_id = '<uuid>';
```

Gunakan *seed* referensi yang idempoten dan *test fixtures* deterministik berbasis data sintetis penuh (dilarang menyalin PII produksi).

## Related Skills

- **maxilun-architect**: Batas *bounded context*, topologi partisi/multi-tenant, dan pola *Transactional Outbox*
- **maxilun-engineer**: Implementasi repositori, model ORM, skrip migrasi, dan integrasi transaksi aplikasi
- **maxilun-insight**: Investigasi kontensi *lock*, kebocoran *connection pool*, dan anomali latensi produksi
- **maxilun-sentinel**: Pencegahan IDOR, kontrol akses RLS, enkripsi data sensitif, dan kepatuhan retensi PII
- **maxilun-knowledge-graph**: Penelusuran pemanggil model, skema, dan kueri lintas modul sebelum perubahan tabel
- **maxilun-verify**: Pengujian maju-mundur migrasi, validasi constraint, dan pembuktian regresi lapisan data
