# Evidence-First Discovery & Decision Triage Protocol

Digunakan hanya ketika permintaan memiliki ruang tafsir terbuka yang berdampak material pada arsitektur, kontrak data, atau identitas produk. Protokol ini menggantikan pola wawancara berantai satu-per-satu yang pasif dengan **investigasi repositori lebih dulu + klarifikasi terkelompok berbasis biaya keputusan**.

---

## 1. Urutan Triase Sebelum Bertanya

Sebelum mengajukan satu pun pertanyaan ke pengguna, jalankan 3 langkah ini secara internal:

1. **Periksa Bukti Repositori**:
   - Baca manifest (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`), struktur folder, skema DB, variabel environment contoh, token CSS/komponen yang sudah ada, dan `docs/` bila tersedia.
   - Fakta yang terlihat di repositori **dilarang keras ditanyakan ulang**.
2. **Ukur Biaya Membalik Keputusan (*Reversibility Check*)**:
   - **Type 2 (Murah dibalik)**: struktur komponen internal, penamaan lokal, tata letak satu halaman dengan sistem desain yang sudah ada, perbaikan performa/bug, atau endpoint CRUD standar.
   - **Type 1 (Mahal dibalik)**: pemecahan database/service, skema finansial/multi-tenant, perubahan *breaking* pada kontrak API publik, penghapusan fitur eksisting, atau penciptaan sistem identitas visual dari nol tanpa acuan sama sekali.
3. **Tentukan Tindakan**:
   - **Type 2 → Eksekusi langsung.** Pilih opsi paling standar dan kohesif dengan konvensi repo, tulis satu kalimat asumsi bila relevan, lalu selesaikan pekerjaannya.
   - **Type 1 → Maksimal 1 giliran klarifikasi terkelompok** (2–4 poin krusial yang benar-benar mengubah desain, lengkap dengan opsi konkret dan rekomendasi default).

---

## 2. Empat Dimensi yang Harus Jelas Sebelum Implementasi Besar

Jika keempat dimensi ini sudah terjawab dari prompt + pembacaan repo, **jangan jalankan sesi tanya-jawab**:

| Dimensi | Apa yang Dicari | Sumber Utama |
|---|---|---|
| **1. Outcome Pengguna** | Perubahan alur kerja nyata apa yang harus bisa dilakukan pengguna? | Prompt pengguna + rute/fitur eksisting |
| **2. Batasan Keras** | Stack, skema data, batas keamanan, target performa, kompatibilitas mundur | Manifest repo, konfigurasi CI, skema DB |
| **3. Batas Cakupan (Non-goals)** | Bagian berdekatan apa yang sengaja tidak disentuh di iterasi ini? | Prinsip YAGNI + cakupan eksplisit prompt |
| **4. Kriteria Terbukti** | Perintah tes, alur interaksi, atau metrik apa yang membuktikan tugas tuntas? | Suite tes repo + alur penerimaan fitur |

---

## 3. Aturan Klarifikasi Saat Benar-Benar Diperlukan (Type 1)

1. **Satu Giliran Terkelompok, Bukan Interogasi Cicilan**:
   - Jangan menahan pekerjaan selama 3–4 putaran tanya-jawab beruntun. Kelompokkan maksimal 2–3 keputusan kunci yang belum terjawab dalam satu pesan ringkas.
2. **Sajikan Opsi Berbeda Secara Substantif + Rekomendasi**:
   - Hindari pertanyaan kosong seperti *"Bisa jelaskan lebih detail?"* atau *"UI-nya mau seperti apa?"* tanpa jangkar.
   - Berikan 2–3 pilihan nyata beserta konsekuensi singkatnya, dan tandai mana yang direkomendasikan.
3. **Khusus Desain Antarmuka Baru Tanpa Sistem Desain Eksisting**:
   - Jika repositori sudah punya token warna/tipografi/komponen, **ikuti dan perkuat sistem yang ada** tanpa bertanya.
   - Jika proyek benar-benar baru (*greenfield*) atau pengguna meminta *redesign total* namun belum menyebutkan arah gaya, tawarkan **3 arketipe visual yang sungguh kontras** sesuai domain produk (lihat `../maxilun-craft/SKILL.md` dan `../maxilun-craft/references/design-md/index.md`) — misal *Editorial Hangat* vs *Operasional Terang Presisi* vs *Minimalis Kontras Tinggi* — bukan tiga variasi dashboard gelap yang mirip.
   - Jika pengguna menjawab *"terserah / rombak maksimal"*, pilih satu arah paling autentik bagi audiens produk tersebut, nyatakan pilihan + alasannya dalam 2–3 kalimat, dan langsung bangun secara menyeluruh.

---

## 4. Perbandingan Pola Buruk vs Pola Maxilun

### Kasus A: Fitur di Repositori yang Sudah Ada
**Prompt**: *"Tambahkan fitur jadwal reservasi pasien di aplikasi klinik ini."*

- **Pola Pasif (Ditolak)**: Berhenti bekerja dan mencicil 4 giliran pertanyaan (*"Siapa yang pakai?"*, *"Stack apa?"*, *"Non-goal apa?"*) disertai blok banner emoji kosong.
- **Pola Aktif Berbasis Bukti (Wajib)**:
  1. Baca repo: terdeteksi Next.js App Router, Prisma (`Patient`, `Doctor` sudah ada di `schema.prisma`), autentikasi staf resepsionis & portal pasien terpisah, serta palet terang bersih di `globals.css`.
  2. Hanya ada 1 keputusan Type 1 yang tidak tertulis di skema: aturan pembatalan/slot *double-booking* & sinkronisasi kalender eksternal.
  3. Jika tidak ada integrasi eksternal di `.env.example`, bangun langsung alur reservasi berbasis constraint unik database (`doctor_id, slot_start`) dengan asumsi eksplisit tanpa payment gateway eksternal, atau ajukan 1 klarifikasi fokus bila ditemukan stub Google Calendar separuh jalan.

### Kasus B: Keluhan "Tampilan Masih Generik AI, Ganti UI/UX"
- **Pola Tambal Sulam (Ditolak)**: Hanya mengubah `border-radius`, mengganti hex ungu ke biru, atau memaksa layout klinik menjadi dashboard gelap bergaya developer tool.
- **Pola Rombak Struktural (Wajib)**:
  1. Identifikasi cacat struktur saat ini (misal: seluruh seksi rata tengah seragam, 3 kartu fitur generik tanpa alur tugas utama, label tombol kabur).
  2. Jika pengguna meminta langsung dieksekusi, tetapkan arah visual yang sesuai domain klinik (misal: *Calm Clinical Operational* — permukaan terang bersih, kontras keterbacaan tinggi, fokus utama pada antrean hari ini & pemilihan jadwal <3 langkah), nyatakan referensi prinsip yang dipakai dan yang ditolak, lalu rombak total struktur komponennya.
