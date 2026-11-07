# Zero-Downtime Database Migrations: The Expand-Contract Pattern

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-data/SKILL.md"
  origin: "Maxilun Data Engine"
-->

Panduan rekayasa perubahan skema basis data produksi tanpa henti layanan (*zero-downtime migrations*) menggunakan pola bertahap *Expand-Contract*.

---

## 1. Empat Fase Pola Expand-Contract

Dilarang melakukan *breaking change* skema (seperti me-rename kolom atau memindahkan relasi) dalam satu langkah transaksi DDL. Gunakan alur 4 fase:

```text
[Fase 1: Expand] ──> [Fase 2: Dual Write] ──> [Fase 3: Backfill] ──> [Fase 4: Contract]
```

1. **Fase 1: Expand (Peluasan Skema)**:
   - Tambahkan kolom atau tabel baru yang dapat bernilai `NULL` tanpa memodifikasi kolom lama.
   - Contoh: Menambahkan kolom `phone_e164` di samping kolom lama `phone_number`.
2. **Fase 2: Dual Write (Penulisan Ganda)**:
   - Kode aplikasi diperbarui untuk menulis ke kedua kolom (kolom lama dan kolom baru), tetapi masih membaca dari kolom lama.
3. **Fase 3: Backfill (Pengisian Data Historis)**:
   - Jalankan proses background worker ber-batch (misal: 1.000 baris per batch dengan jeda $50\text{ms}$) untuk menyalin data dari kolom lama ke kolom baru.
   - Jangan menjalankan update jutaan baris sekaligus dalam satu transaksi raksasa karena akan mengunci tabel secara eksklusif.
4. **Fase 4: Contract (Penyusutan Skema)**:
   - Alihkan pembacaan aplikasi sepenuhnya ke kolom baru.
   - Setelah stabil dalam observasi produksi, hapus kolom lama atau jadikan `deprecated` via migrasi terpisah.

---

## 2. Invarian Operasi DDL Aman (PostgreSQL / MySQL)

1. **Batas Waktu Penguncian (Lock Timeout)**:
   - Pasang `lock_timeout = '3s'` sebelum mengeksekusi DDL agar migrasi otomatis gagal daripada memblokir antrean kueri produksi:
   ```sql
   SET lock_timeout = '3s';
   ALTER TABLE orders ADD COLUMN status_code VARCHAR(32);
   ```
2. **Pembuatan Indeks Tanpa Penguncian Tabel**:
   - Di PostgreSQL, selalu gunakan `CREATE INDEX CONCURRENTLY`.
   - Di MySQL/InnoDB, gunakan `ALGORITHM=INPLACE, LOCK=NONE`.
3. **Penambahan Kolom dengan Nilai Default**:
   - Di PostgreSQL 11+, penambahan kolom dengan nilai konstan `DEFAULT` tidak menulis ulang tabel (*zero rewrite*). Pada versi lama, tambahkan kolom sebagai `NULL` terlebih dahulu, baru isi secara bertahap.
