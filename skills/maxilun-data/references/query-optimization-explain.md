# Database Query Optimization & EXPLAIN ANALYZE Diagnostics

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-data/SKILL.md"
  origin: "Maxilun Data Engine"
-->

Panduan diagnostik kinerja kueri, pembacaan rencana eksekusi `EXPLAIN ANALYZE`, dan strategi perancangan indeks presisi.

---

## 1. Membaca Rencana Eksekusi (EXPLAIN ANALYZE)

Saat kueri berjalan lambat, jangan menambah indeks secara spekulatif. Jalankan `EXPLAIN (ANALYZE, BUFFERS)` dan periksa 4 titik pemeriksaan utama:

1. **Sequential Scan vs Index Scan**:
   - Jika tabel memiliki ribuan baris dan rencana menampilkan `Seq Scan`, periksa apakah filter `WHERE` atau klausul `JOIN` tidak tercakup oleh indeks yang ada.
2. **Perbedaan Perkiraan vs Realitas (Estimate vs Actual Rows)**:
   - Jika `rows=1` diperkirakan oleh perencana kueri tetapi baris nyata `actual rows=100000`, statistik tabel telah usang. Jalankan `ANALYZE nama_tabel;`.
3. **Penyortiran Memori vs Disk (Sort Method)**:
   - Periksa apakah operasi pengurutan (`ORDER BY`) menggunakan `quicksort Memory` atau `external merge Disk`. Penyortiran di disk menunjukkan perlunya penambahan indeks terurut atau peningkatan `work_mem`.
4. **Buffer Hit Ratio**:
   - Periksa `Buffers: shared hit=... read=...`. Angka `read` tinggi menandakan pembacaan fisik disk lambat yang perlu diredam dengan indeks yang lebih ramping.

---

## 2. Aturan Perancangan Indeks Komposit

Saat kueri memfilter multi-kolom (`WHERE tenant_id = ? AND status = ? ORDER BY created_at DESC`):

1. **Urutan Kolom Berdasarkan Kesetaraan Dulu (Equality First)**:
   - Tempatkan kolom dengan operator kesetaraan (`=`) di urutan paling kiri indeks.
   - Tempatkan kolom rentang (`<`, `>`, `BETWEEN`) atau pengurutan (`ORDER BY`) di urutan setelahnya.
   - Contoh Indeks Optimal: `(tenant_id, status, created_at DESC)`.
2. **Indeks Parsial (Partial Index)**:
   - Jika kueri hanya mencari baris dengan status spesifik (misal: antrean yang belum diproses):
   ```sql
   CREATE INDEX CONCURRENTLY idx_orders_unprocessed 
   ON orders (created_at) 
   WHERE status = 'PENDING';
   ```
   - Menghemat ukuran disk hingga 90% dibanding mengindeks seluruh tabel.

---

## 3. Optimasi Row-Level Security (RLS)

1. **Pemeriksaan Indeks pada Kolom Kebijakan**:
   - Kolom yang dipakai di ekspresi kebijakan RLS (`tenant_id` atau `user_id`) wajib memiliki indeks terpisah atau menjadi kolom utama di indeks komposit.
2. **Pencegahan Evaluasi Berulang**:
   - Bungkus fungsi pembacaan sesi di dalam ekspresi subkueri agar dieksekusi satu kali per kueri alih-alih dievaluasi per-baris tabel:
   ```sql
   -- Baik: dievaluasi sekali
   USING (tenant_id = (SELECT current_setting('app.current_tenant')::uuid))
   ```

---

## 4. Alur 5-Langkah Optimasi Kueri Sistemik

Jangan melakukan optimasi kueri secara coba-coba (*guesswork*). Ikuti alur 5-langkah deterministik berikut:

```
┌────────────────────────────────────────────────────────┐
│  1. Ukur Baseline: EXPLAIN (ANALYZE, BUFFERS)         │
│     (Catat execution time, actual rows, buffer read)   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  2. Evaluasi Selektivitas & Pangkas Scan Monolitik    │
│     (Hitung selektivitas predikat, singkirkan Seq Scan)│
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  3. Eliminasi Spill-to-Disk (Sorts & Hash Aggregates) │
│     (Deteksi external merge Disk, sesuaikan work_mem)  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  4. Rombak Pola Kueri & Indeks Covering (Rewrite)     │
│     (Subquery -> JOIN, Keyset Pagination, INCLUDE)    │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  5. Pembuktian Regresi Komparatif (Before vs After)    │
│     (Verifikasi penurunan buffers read & execution ms) │
└────────────────────────────────────────────────────────┘
```

### 4.1 Langkah 1: Pengukuran Baseline Rencana Eksekusi
Jalankan kueri lambat di lingkungan pementasan/transaksi aman:
```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, TIMING, SUMMARY)
SELECT o.id, o.total_amount, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'COMPLETED' AND o.created_at >= '2026-01-01'
ORDER BY o.created_at DESC LIMIT 50;
```
Catat tiga angka krusial:
- `Execution Time`: durasi eksekusi kueri aktual dalam milidetik.
- `Buffers: shared hit=... read=...`: rasio halaman memori (*hit*) vs I/O disk fisik (*read*).
- `Rows Removed by Filter`: jumlah baris yang dipindai tetapi dibuang percuma.

### 4.2 Langkah 2: Selektivitas Predikat & Indeks Presisi
- Jika `Rows Removed by Filter` tinggi pada scan indeks, urutan kolom indeks komposit keliru.
- Terapkan aturan mutlak: **Equality (`=`) $\to$ Range (`>`, `<`) $\to$ Sort (`ORDER BY`)**.
- Untuk status dengan distribusi timpang (misal 98% `COMPLETED` dan 2% `PENDING`), jangan membuat indeks untuk status mayoritas; buat **Partial Index** khusus predikat minoritas.

### 4.3 Langkah 3: Eliminasi Spill-to-Disk
- Cari peringatan: `Sort Method: external merge Disk: 18432kB` atau `spill to temp file`.
- Bahaya: Operasi pengurutan yang melebihi batas memori terpaksa menulis ke disk sementara, melipatgandakan latensi kueri 10x–50x.
- Solusi:
  1. Sediakan indeks yang urutannya persis dengan klausul `ORDER BY` agar database melakukan scan langsung tanpa pengurutan memori (*presorted index scan*).
  2. Jika pengurutan memang tak terhindarkan pada batch/laporan analitik, naikkan batas memori transaksi lokal:
     ```sql
     SET LOCAL work_mem = '64MB';
     ```

### 4.4 Langkah 4: Rombak Pola Kueri (Query Rewrite)
1. **Hapus Loop N+1**: Ganti kueri di dalam loop ORM dengan batch `WHERE parent_id = ANY($1)`.
2. **Paginasi Berbasis Kursor (Keyset Pagination)**: Dilarang menggunakan `OFFSET 100000` (database memindai dan membuang 100.000 baris pertama). Gunakan kursor Primary Key terurut:
   ```sql
   -- Gantikan: OFFSET 50000 LIMIT 20
   -- Dengan Keyset:
   WHERE created_at < $last_created_at OR (created_at = $last_created_at AND id < $last_id)
   ORDER BY created_at DESC, id DESC LIMIT 20;
   ```
3. **Index-Only Scan dengan Covering Index**:
   ```sql
   CREATE INDEX CONCURRENTLY idx_orders_covering
   ON orders (customer_id, status) INCLUDE (total_amount, created_at);
   ```

### 4.5 Langkah 5: Pembuktian Regresi Komparatif
Buktikan efektivitas perbaikan dengan membandingkan metrik sebelum dan sesudah:

| Metrik | Sebelum Optimasi | Sesudah Optimasi | Delta Perbaikan |
|---|---|---|---|
| **Metode Scan** | `Seq Scan on orders` | `Index Only Scan` | Eliminasi full scan |
| **Buffers Read (Disk I/O)** | `14.280 pages (111 MB)` | `0 pages (0 MB)` | 100% cache hit |
| **Sort Buffer** | `external merge Disk: 24MB` | `None (Index Presorted)` | Nol disk spill |
| **Execution Time** | `1.450 ms` | `3.2 ms` | **$\sim 450\times$ lebih cepat** |
