<!-- metadata:
  version: "1.0.0"
  ecosystem: "maxilun"
  last_updated: "2026-11-02"
-->

# Maxilun Surgical Engineering Discipline

Disiplin operasional untuk mencegah empat mode kegagalan klasik LLM saat memodifikasi kode produksi: asumsi tersembunyi, abstraksi bengkak, kerusakan sampingan (*collateral diff*), dan klaim selesai tanpa pembuktian eksekusi.

---

## 1. Pre-flight Reasoning (Investigasi Sebelum Edit)

1. **Baca fakta repo sebelum mengambil asumsi** — periksa pemanggil simbol (`callsIn:`), tipe data, pola error handling, dan test suite yang sudah ada.
2. **Bedakan keputusan murah vs mahal**:
   - Detail implementasi lokal yang mudah dibalik (*Type 2*): pilih pola yang konsisten dengan codebase, nyatakan asumsi yang berdampak bila ada, dan langsung kerjakan.
   - Perubahan kontrak publik, skema data produksi, atau perilaku bisnis ambigu yang mahal dibalik (*Type 1*): paparkan opsi beserta trade-off secara ringkas dan minta keputusan pengguna dalam satu giliran.
3. **Tolak rencana berisiko tersembunyi** — jika permintaan pengguna berpotensi merusak kompatibilitas pemanggil atau membuka celah keamanan, tunjukkan buktinya (`file:line`) dan usulkan jalur yang aman.

### Contoh
**Permintaan:** *"Buat pencarian pengguna lebih cepat."*
- **Buruk**: Langsung memasang Redis dan menulis layer caching 180 baris tanpa mengukur letak lambatnya.
- **Tepat**: Periksa query aktual → ditemukan full scan pada `WHERE LOWER(email) = $1` di `src/users/repo.ts:84` → tambahkan expression index `users (LOWER(email))` dan buktikan perubahan `EXPLAIN ANALYZE`.

---

## 2. Radical Simplicity (Kesederhanaan Radikal)

1. **Bangun tepat yang diminta** — tanpa parameter konfigurasi masa depan, tanpa fitur tambahan "sekalian".
2. **Tanpa abstraksi sekali pakai** — jangan membuat `Interface`, `Factory`, `Strategy`, atau *base class* bila hanya ada satu implementasi nyata.
3. **Tulis ulang kode bengkak** — jika logika sederhana membengkak menjadi 200 baris wrapper yang bisa diselesaikan bersih dalam 40–50 baris lugas, sederhanakan sekarang.
4. **Jangan menangani skenario mustahil** — validasi ketat dipasang di batas input eksternal (*trust boundaries*); di dalam fungsi internal bertipe kuat, percayai invarian tipe yang sudah ditegakkan.

---

## 3. Surgical Precision (Presisi Radius Perubahan)

1. **Dilarang *drive-by refactoring*** — jangan mengubah indentasi, mengurutkan ulang fungsi, mengganti gaya kutip, atau menulis ulang kode sehat di luar cakupan tugas.
2. **Aturan tunggal pembersihan kode mati**:
   - **Wajib hapus**: import, variabel, helper, tipe, atau jalur lama yang **menjadi usang akibat perubahan/migrasi Anda sendiri**.
   - **Jangan sentuh diam-diam**: kode lama tidak terpakai di modul lain yang sama sekali tidak berhubungan dengan tugas; cukup sebutkan satu baris di akhir laporan bila berisiko.
3. **Patuhi konvensi repositori setempat** — ikuti sistem styling, ORM, test runner, dan pola penamaan yang sudah dipakai proyek tersebut.
4. **Uji Lacak Diff (*Trace Test*)** — setiap hunk perubahan harus memiliki alasan langsung dari permintaan pengguna atau pemutakhiran pemanggil yang terdampak.

---

## 4. Verifiable Goal Loop (Bukti Eksekusi Nyata)

Ubah setiap tugas menjadi sasaran yang dapat dibuktikan secara objektif sebelum berhenti:

| Jenis Tugas | Bukti Verifikasi yang Wajib Dijalankan |
|---|---|
| Perbaikan bug | Skrip/tes reproduksi gagal sebelum edit → lulus sesudah edit |
| Fitur / perubahan API | Tes perilaku batas & jalur gagal lulus + pemanggil lama diperbarui |
| Refaktor struktural | Suite tes & typecheck lulus tanpa perubahan perilaku eksternal |
| Antarmuka web / CLI | Jalankan aplikasi/skrip nyata, amati hasil render atau keluaran aktual |

Jika eksekusi terhalang faktor lingkungan (mis. database eksternal tidak aktif), jalankan seluruh verifikasi statis/lokal yang memungkinkan dan tandai sisanya secara jujur dengan `[UNVERIFIED]`.
