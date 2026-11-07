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
3. **Khusus Desain Antarmuka: Penambahan Fitur vs Redesign**:
   - **Penambahan Fitur pada Sistem Sehat**: Jika repositori sudah memiliki sistem token/komponen yang sehat dan sesuai domain, **ikuti dan perkuat sistem yang ada** tanpa bertanya.
   - **Permintaan Redesign / Ganti UI UX**: Jika pengguna meminta redesign, **JANGAN pertahankan token, variabel CSS (:root), atau wrapper layout lama yang mengunci tampilan menjadi kusam/generik**! Lakukan *Clean Cutover*: deteksi 5 Kunci Desain Sistem (`SYS-001` .. `SYS-005` di `purity-catalog.md`), hapus/ganti variabel root lama, buka kontainer layout pembatas, dan pasang fondasi visual baru yang kontekstual domain.
   - **Arah Gaya Belum Disebutkan**: Jika proyek benar-benar baru (*greenfield*) atau pengguna meminta *redesign total* namun belum menyebutkan arah gaya, tawarkan **3 arketipe visual yang sungguh kontras** sesuai domain produk (lihat `../maxilun-craft/SKILL.md` dan `../maxilun-craft/references/design-md/index.md`) — misal *Editorial Hangat* vs *Operasional Terang Presisi* vs *Minimalis Kontras Tinggi* — bukan tiga variasi dashboard gelap yang mirip.
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

### Kasus B: Keluhan "Tampilan Masih Generik AI, Ganti UI/UX, atau Redesign"
- **Pola Tambal Sulam & Terkunci (Ditolak)**: Hanya mengubah `border-radius` atau margin di leaf JSX sambil membiarkan variabel `:root` abu-abu generik, layout container sempit, dan wrapper lama tetap mengunci tampilan. Hasilnya UI/UX tetap "begitu-begitu saja".
- **Pola Rombak Struktural & Buka Kunci Bersih (Wajib)**:
  1. Identifikasi cacat struktur dan **Kunci Desain Sistem** yang mengunci UI (misal: token slate pucat di `globals.css`, wrapper `max-w-5xl` kaku di `layout.tsx`, tombol/kartu lama bersudut seragam, seluruh seksi rata tengah).
  2. Buka kunci fondasi: gantikan token `:root` dengan tangga warna OKLCH fisik domain produk, buka container layout agar ritme spasial bernapas, dan mutakhirkan komponen primitif ke formula konsentris.
  3. Tetapkan arah visual sesuai domain (misal: *Calm Clinical Operational* untuk klinik — permukaan terang bersih, kontras tinggi, fokus antrean & jadwal <3 langkah; atau rujukan konkret dari `../maxilun-craft/references/design-md/`), nyatakan prinsip yang dipakai dan ditolak (DDR), lalu bangun ulang komponen secara menyeluruh dan hapus kode styling lama yang usang (*clean cutover*).
