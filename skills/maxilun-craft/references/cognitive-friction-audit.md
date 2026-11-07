# Cognitive Friction Audit: Empirical Usability Invariants

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine"
-->

Panduan pelaksanaan audit beban kognitif dan evaluasi heuristik antarmuka berbasis bukti kode konkret (*file:line*). Menghindari audit teoretis generik dengan memeriksa 10 invarian keterpakaian empiris langsung pada struktur DOM, komponen, dan interaksi.

---

## 1. Sepuluh Invarian Keterpakaian Empiris

1. **Visibilitas Status Sistem Real-Time**:
   - Setiap operasi yang memakan waktu $> 150\text{ms}$ wajib menampilkan umpan balik visual (status pending, indikator proses deterministik).
   - Pengguna dilarang berada dalam kondisi menebak apakah klik tombol mereka sudah terdaftar oleh sistem atau belum.
2. **Kesesuaian dengan Objek Dunia Nyata**:
   - Kosakata antarmuka memakai nama benda dan alur kerja asli domain pengguna (misal: faktur, nomor resi, slot reservasi), bukan istilah teknis internal developer (*database_id*, *payload*, *record_entity*).
3. **Kebebasan Kendali Pengguna (Jalur Batal Eksplisit)**:
   - Setiap dialog modal, drawer geser, atau alur bertahap wajib menyediakan tombol penutup (*escape hatch*) yang jelas dan dapat diakses via tombol `Esc` keyboard.
4. **Konsistensi Token & Pola Antarmuka**:
   - Seluruh status sejenis (sukses, perhatian, galat) wajib menggunakan warna semantik dan ikonografi yang sama di seluruh layar tanpa variasi arbitrer.
5. **Pencegahan Galat Sebelum Terjadi (Error Prevention)**:
   - Matikan kemungkinan salah input sejak awal (misal: nonaktifkan tanggal masa lalu pada pemesanan masa depan, pasang masking angka pada nomor kartu, sediakan validasi langsung saat pengguna selesai mengetik).
6. **Pengenalan Lebih Utama dari Mengingat (Recognition over Recall)**:
   - Tampilkan informasi kontekstual penting (seperti ringkasan pesanan, harga per malam, atau ID transaksi) tetap terlihat selama alur konfirmasi tanpa mengharuskan pengguna kembali ke layar sebelumnya.
7. **Ergonomi Akselerator Kontekstual**:
   - Sediakan shortcut keyboard hanya pada aplikasi berbasis kerja keyboard cepat (editor, terminal, pengarsipan data), dan dilarang memaksakan shortcut palsu di halaman promosi publik.
8. **Minimalisme Subtraktif & Kejelasan Sinyal**:
   - Singkirkan setiap elemen dekoratif yang tidak berkontribusi pada pemahaman konten atau pengambilan keputusan pengguna.
9. **Diagnostik Galat Dekat Titik Gagal**:
   - Pesan kegagalan wajib memandu langkah pemulihan langsung, bukan sekadar menampilkan kode kesalahan HTTP mentah (*"500 Internal Error"*).
10. **Bantuan Tepat Waktu Tanpa Mengganggu Alur**:
    - Petunjuk bantuan disajikan sebagai teks tooltip mikro atau tautan kontekstual di samping label input yang membutuhkan penjelasan teknis.

---

## 2. Ergonomi Fisik: Hukum Fitts & Zona Ibu Jari (Thumb Zone)

Saat merancang antarmuka mobile atau layar sentuh tablet:

1. **Aturan Area Jangkauan**:
   - Tindakan primer paling sering dipakai (navigasi utama, tombol lanjut alur, filter cepat) wajib ditempatkan di sepertiga bawah layar (*natural thumb zone*).
   - Tindakan destruktif atau jarang dipakai diletakkan di area atas yang membutuhkan usaha jangkauan sengaja.
2. **Target Sentuh Minimum Terukur**:
   - Kontrol antarmuka mobile wajib memiliki area klik efektif minimal $44 \times 44\text{pt}$ (iOS) atau $48 \times 48\text{dp}$ (Android), meskipun ikon visual di dalamnya berukuran lebih kecil (gunakan invisible hit-box padding).
3. **Pemisahan Jarak Antar Tombol**:
   - Kontrol yang berdampingan wajib memiliki jarak aman minimal $8\text{px}$ untuk mencegah salah sentuh (*accidental activation*).

---

## 3. Format Pelaporan Audit Kognitif

Setiap temuan audit keterpakaian dilaporkan dalam format berbasis bukti berikut:

```markdown
### [AUDIT-HEURISTIK] file:line — Deskripsi Singkat Masalah
- **Kode Invarian**: [INV-01 s/d INV-10]
- **Tingkat Friksi**: [Tinggi / Sedang / Rendah]
- **Bukti Kode**: `file:line` potongan kode yang melanggar
- **Dampak Kognitif**: [1-2 kalimat menjelaskan kebingungan pengguna atau potensi salah klik]
- **Rekomendasi Perbaikan**: [Diff atau spesifikasi penyesuaian konkret]
```
