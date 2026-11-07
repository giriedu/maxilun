# Root-Cause Convergence & Surgical Bug Fixing

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-engineer/SKILL.md"
  origin: "Maxilun Engineer Engine"
-->

Panduan pelacakan akar masalah (*root-cause convergence*) dan perbaikan bug presisi tanpa tambal sulam gejala luar.

---

## 1. Menemukan Titik Konvergensi Akar Masalah

Dilarang memperbaiki bug dengan menambahkan kondisi `if (data === null) return;` di lapisan antarmuka jika akar masalahnya adalah data korup di lapisan query basis data.

### Protokol 3 Langkah:
1. **Lacak Titik Asal Data (Upstream Tracing)**:
   - Gunakan pemetaan `callsIn:` dari `maxilun-knowledge-graph` untuk melacak dari titik error meletup mundur ke fungsi pemanggil pertama yang menghasilkan nilai tidak valid.
2. **Identifikasi Invarian yang Rusak**:
   - Tentukan kontrak apa yang dilanggar (misal: array kosong dianggap objek, zona waktu tidak terdefinisi, atau race condition transaksi simultan).
3. **Perbaiki Tepat pada Titik Konvergensi**:
   - Letakkan perbaikan di titik paling dalam di mana data pertama kali diciptakan atau divalidasi, sehingga seluruh konsumen downstream otomatis terlindungi tanpa perlu puluhan pengecekan defensif tambahan.

---

## 2. Invarian Uji Regresi Deterministik

Setiap perbaikan bug wajib disertai satu pengujian regresi:

1. **Uji Gagal Sebelum Perbaikan (Red)**:
   - Tulis pengujian unit atau integrasi yang mereproduksi error secara konsisten dengan masukan pemicu bug.
2. **Uji Lulus Setelah Perbaikan (Green)**:
   - Terapkan perbaikan bedah minimal dan pastikan pengujian tersebut berstatus lulus (*exit code 0*).
3. **Pencegahan Flaky Test**:
   - Dilarang menggunakan `sleep()` dengan durasi arbitrer. Gunakan mekanisme penungguan berbasis event (*await event / condition poll*) yang deterministik.
