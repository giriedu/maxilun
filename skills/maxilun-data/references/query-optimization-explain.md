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
