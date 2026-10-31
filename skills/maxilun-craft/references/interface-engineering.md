# Interface Engineering: Mathematical Precision & Production Design Rules

Panduan rekayasa antarmuka tingkat lanjut yang mengadaptasi prinsip *interface engineering* presisi tinggi untuk memusnahkan estetika generik dan cetakan template AI. Rujukan operasional untuk `maxilun-craft`, `maxilun-frontend`, dan `maxilun-verify`.

---

## 1. Presisi Visual & Poles Permukaan (UI Polish)

Nilai-nilai di bawah ini bersifat eksak, bukan rentang perkiraan.

### 1.1 Formula Radius Konsentris Eksak
Saat container induk dan elemen anak memiliki inset (padding) merata:
$$\text{radius}_{\text{outer}} = \text{radius}_{\text{inner}} + \text{padding} + \text{border}$$
$$\text{radius}_{\text{inner}} = \max(0, \text{radius}_{\text{outer}} - \text{padding} - \text{border})$$

Jika kartu luar menggunakan `rounded-2xl` (16px) dengan padding 8px, tombol atau input di dalamnya **wajib** menggunakan radius 8px (`16px - 8px = 8px`), bukan 16px seragam atau 0px tajam. Di atas padding 24px atau padding asimetris yang disengaja, kedua lapisan diperlakukan sebagai permukaan independen.

### 1.2 Bayangan Berlapis untuk Elevasi, Border untuk Struktur
- **Border**: Hanya untuk pembatas struktural (dividers, baris tabel, pemisah kolom, batas input formulir yang membutuhkan kontras non-teks 3:1 WCAG 1.4.11).
- **Elevasi**: Gantikan border tebal pembuat ilusi kedalaman dengan bayangan berlapis transparan (*layered transparent box-shadow*):
  ```css
  /* Elevasi kontak halus */
  box-shadow: 0 1px 2px oklch(0 0 0 / 0.05), 0 1px 3px oklch(0 0 0 / 0.08);
  /* Selalu sertakan border transparan agar mode forced-colors tetap menggambar tepi */
  border: 1px solid transparent;
  ```

### 1.3 Garis Tepi Gambar Hitam/Putih Murni (1px Inset Outline)
Beri outline `1px` inset `1px` pada media/gambar konten:
- Mode Terang: `oklch(0 0 0 / 0.1)`
- Mode Gelap: `oklch(1 0 0 / 0.1)`
- **Dilarang** menggunakan warna abu-abu netral bertinting atau warna aksen brand, karena akan menimbulkan efek *fringe* berwarna yang kotor pada tepi gambar. Lewati elemen vektor transparan (logo dan ilustrasi).

### 1.4 Mikro-Interaksi Taktil & Gerak
- **Skala Tekan Tombol**: Tombol aktif mengecil ke tepat `scale(0.96)` dalam durasi `150ms` kurva `ease-out`. Tombol disabled **tidak boleh** mengecil.
- **Transisi State vs Keyframe**: Gunakan CSS transition atau physics spring untuk perubahan status interaktif agar dapat berbalik arah saat kursor dilepas di tengah animasi. Keyframe hanya untuk animasi sekuens satu arah yang berjalan sekali saat mount.
- **Interaksi Frekuensi Tinggi Instan**: Pengetikan, hover baris tabel, dan perpindahan tab harus merespons instan (`<= 150ms`) pada properti `opacity` atau `background-color`. Jangan animasikan layout properties (`top`, `left`, `width`, `height`).
- **Gating Hover pada Pointer**: Seluruh efek hover wajib berada di bawah `@media (hover: hover)`. Pada layar sentuh, hover tanpa pelindung akan terkunci (*latched*) dan terbaca sebagai status terpilih palsu.
- **Scroll Containment**: Pasang `overscroll-behavior: contain` pada dialog modal, drawer, dan popover menu.

---

## 2. Standar Tipografi Matematis (Mathematical Typography)

### 2.1 Skala Tipografi Berbasis Peran
Definisikan ukuran dengan pasangan line-height dan font-weight yang konsisten:
- **Display**: `font-size: 40px–56px`, `line-height: 1.1–1.15`, `letter-spacing: -0.02em` s.d. `-0.04em`.
- **Heading 1–2**: `font-size: 24px–32px`, `line-height: 1.2–1.25`, `letter-spacing: -0.01em` s.d. `-0.02em`.
- **Heading 3–4**: `font-size: 18px–20px`, `line-height: 1.3–1.35`, `letter-spacing: -0.005em`.
- **Body Text**: `font-size: 15px–16px`, `line-height: 1.5–1.6`, `letter-spacing: 0`.
- **Technical/Micro Label**: `font-size: 11px–13px`, `line-height: 1.25`, uppercase label `letter-spacing: 0.05em`.

### 2.2 Batas Panjang Baris & Wrapping
- **Cap the Measure**: Batasi lebar baris teks bacaan pada **60–75 karakter** (`max-w-[65ch]`). Baris yang terlalu panjang membuat mata lelah saat kembali ke awal baris.
- **Text Wrapping**:
  - Pasang `text-wrap: balance` pada judul display dan headline pendek (maksimal 4 baris).
  - Pasang `text-wrap: pretty` pada paragraf naratif untuk mencegah kata tunggal menggantung di baris akhir (*widow*).
- **Disiplin Angka Tabular**: Pasang `font-variant-numeric: tabular-nums` pada seluruh harga, waktu, stopwatch, metrik KPI, dan kolom numerik tabel agar angka tidak bergetar (*layout jitter*) saat berganti nilai.
- **Batas Minimum Input Mobile 16px**: Font size pada elemen `<input>`, `<select>`, dan `<textarea>` pada perangkat layar kecil wajib minimal `16px` (`text-base sm:text-sm`) untuk mencegah iOS Safari melakukan auto-zoom paksa yang merusak layout.

### 2.3 Karakter Tipografi Asli
Simpan teks dalam karakter alami dan gunakan tanda baca tipografis nyata:
- Kutip lengkung: `“` dan `”` (bukan kutip lurus `"` `"`).
- Elipsis tunggal: `…` (bukan tiga titik biasa `...`).
- Tanda pisah: En dash `–` untuk rentang angka (`10–20 MB`), Em dash `—` untuk jeda klausa kalimat.
- Spasi non-breaking: `&nbsp;` di antara angka dan satuan (`10&nbsp;MB`, `24&nbsp;px`, `⌘&nbsp;K`).

---

## 3. Sistem Palet & Warna Semantik (Systematic Color Ramps)

### 3.1 Ramps, Bukan Warna Acak
Sistem warna dibangun atas tangga warna (*ramps*): satu tangga netral, satu tangga aksen utama, dan tangga status fungsional (success, warning, danger). Jangan membuat token untuk peran yang tidak pernah dirender di layar.

### 3.2 Pemisahan Primitif vs Semantik
- **Primitives** menamai nilai fisik: `--slate-900: oklch(20% 0.01 250)`. Dilarang dipanggil langsung di komponen UI.
- **Semantic Tokens** menamai tugas: `--color-surface-base: var(--slate-900)`. Komponen UI hanya boleh memanggil token semantik ini.

### 3.3 Aturan Satu Aksi Primer per Tampilan (One Primary Action Rule)
Ketika warna isi (*solid fill*) digunakan untuk menandakan aksi utama:
- **Tepat satu aksi primer** mendapatkan perlakuan warna aksen solid pada satu layar/viewport.
- Tombol pendamping wajib berstatus netral, outline, atau ghost.
- **Dilarang** meletakkan dua tombol pill berwarna kontras tebal berdampingan di hero section yang saling berebut perhatian pengunjung.

### 3.4 Pengukuran Kontras Nyata
Ukur kontras foreground terhadap warna background aktual yang dirender di belakangnya (bukan sekadar terhadap background halaman):
- Teks biasa (<18px regular): minimal `4.5:1` (WCAG AA).
- Teks besar (>=24px atau >=18.67px tebal): minimal `3:1`.
- Batas komponen kontrol & icon bermakna: minimal `3:1`.

---

## 4. Tata Letak & Ritme Spasial (Spatial Rhythm & Layout)

### 4.1 Aturan Spasi 2x (Group with Space, Not Lines)
Gunakan spasi untuk mengelompokkan elemen terlebih dahulu, kontras latar belakang kedua, dan garis pemisah hanya sebagai pilihan terakhir saat spasi tidak mencukupi:
- Jarak antar-grup elemen minimal **2 kali lipat** dari jarak antar-elemen di dalam grup yang sama.
- Jika elemen di dalam grup terpisah `8px`, jarak antar-kelompok adalah `16px` atau `24px`.

### 4.2 Keselarasan Tepi Bersama (Align to Shared Edges)
- Pilih sejumlah kecil garis tepi vertikal dan sejajarkan elemen ke garis tersebut.
- **Tolak Cetakan Senter-Total (Anti Center-Everything Cascade)**: Hindari menyusun seluruh halaman dengan tumpukan seragam yang semuanya rata tengah (Overline centered -> H2 centered -> Subtitle centered -> Card centered).
- Gunakan struktur asimetris, penyejajaran ke tepi kiri (*text-align: start*), atau Asymmetric Bento Grid (`2:1`, `1:2`) untuk menciptakan ritme visual berkarakter.

### 4.3 Properti Logis CSS (Logical Properties)
Gunakan properti logis untuk seluruh dimensi arah:
- `margin-inline-start`, `margin-inline-end`, `padding-block`, `inset-inline-start`, `text-align: start`.
- Hindari `width: 100vw` (akan memicu scroll horizontal karena memperhitungkan scrollbar desktop; gunakan `width: 100%`).
- Hindari `height: 100vh` pada container penuh di mobile (gunakan `height: 100dvh` agar tidak tertutup address bar browser).

---

## 5. Salinan Antarmuka & Bahasa Produk (Product Writing)

### 5.1 Inventarisasi Terminologi Domain
Sebelum menulis teks antarmuka:
- Buat daftar istilah baku: jangan gunakan "Proyek" di menu tetapi "Workspace" di notifikasi.
- Gunakan istilah teknis nyata sesuai domain operasional, bukan metafora fiksi ilmiah yang dibuat-buat (hindari menyebut WebSocket engine sebagai *"Arsitektur Ruang Virtual 3D"* atau *"Chamber 01"*).

### 5.2 Tombol Berorientasi Kata Kerja Konkret
- Tombol wajib diawali kata kerja aksi spesifik: *"Buka Sesi"*, *"Salin Perintah"*, *"Kirim Tagihan"*, *"Simpan Perubahan"*.
- Hindari tombol generik: *"OK"*, *"Explore"*, *"Learn More"*, *"Get Started"*, *"Click Here"*.

### 5.3 Error yang Solutif Tepat di Samping Kerusakan
Pesan error adalah panduan perbaikan yang diletakkan di samping input yang gagal:
- **Buruk**: *"Oops! Terjadi kesalahan."* atau *"Password tidak valid."*
- **Benar**: *"Password minimal 8 karakter dan mengandung 1 angka."*
- Jangan menyalahkan pengguna dan jangan gunakan tanda seru berlebihan.

### 5.4 Undo Lebih Unggul daripada Dialog Konfirmasi
Untuk tindakan yang dapat dibatalkan (arsip data, hapus ke tempat sampah), jalankan aksi seketika dan sediakan opsi **Undo** pada toast notifikasi selama 5–8 detik. Dialog konfirmasi modal hanya untuk aksi destruktif permanen yang tidak dapat dipulihkan.

---

## 6. Protokol Review Lintas-Disiplin & Tangga Severity

### 6.1 Tangga Keparahan (Severity Ladder)
- **HIGH**: Menghalangi tugas pengguna, memicu risiko kehilangan data, menyesatkan alur, atau melanggar salah satu dari 13 Escalation Triggers.
- **MEDIUM**: Mengurangi efisiensi, merusak hierarki visual, atau inkonsistensi sistem desain.
- **LOW**: Pemolesan kosmetik terisolasi.

### 6.2 Tiga Belas Pemicu Eskalasi Mutlak (13 Escalation Triggers — HIGH on Sight)
Jika salah satu dari 13 kondisi ini ditemukan, temuan otomatis berstatus **HIGH** dan **MEMBLOKIR (BLOCK)** rilis antarmuka:
1. Kontrol interaktif tanpa nama aksesibel (`aria-label` / `<label>`).
2. Kontrol yang dapat dijangkau keyboard tanpa cincin fokus terlihat (`:focus-visible`).
3. Jalur aksi yang bisa dijangkau pointer mouse tetapi tidak bisa dijangkau keyboard.
4. Animasi pergerakan, skala, atau media putar otomatis yang mengabaikan `prefers-reduced-motion`.
5. Konten atau kontrol yang terpotong, tumpang tindih, atau tidak terjangkau pada lebar 320px atau zoom 200%.
6. Rasio kontras teks atau kontrol interaktif gagal terhadap background rendered (<4.5:1 / <3:1).
7. Status atau makna sistem hanya dikomunikasikan melalui warna tunggal tanpa teks/ikon pendukung.
8. Tindakan destruktif tanpa konfirmasi jelas atau mekanisme pembatalan (*undo*).
9. Teks terpotong (*truncated*) tanpa akses untuk melihat nilai penuhnya (tooltip/expand).
10. Konten atau kontrol penting yang tersembunyi di luar batas scroll tanpa petunjuk visual (*peek cue*).
11. Pesan error tanpa petunjuk tindakan pemulihan bagi pengguna.
12. Warna semantik bahaya digunakan untuk tindakan non-destruktif.
13. Perubahan status hanya diindikasikan oleh animasi tanpa meninggalkan jejak visual statis (warna/ikon/label) saat animasi selesai.

---

## 7. Tabel Deteksi & Koreksi Sebelum Selesai (Before You Finish)

| Pola Terdeteksi | Koreksi Wajib |
|---|---|
| Card induk dan elemen anak memiliki `rounded-*` yang sama | Terapkan formula konsentris: $\text{radius}_{\text{anak}} = \text{radius}_{\text{induk}} - \text{padding}$ |
| Badge kapsul mengambang di atas judul hero (`• BADGE •`) | Hapus badge kapsul klise; masukkan konteks ke dalam eyebrow editorial atau judul |
| Seluruh seksi halaman tersusun senter (Overline -> H2 -> Card senter) | Ubah menjadi layout asimetris dengan penyejajaran tepi kiri atau bento grid `2:1` |
| Dua tombol pill berdampingan di hero section berebut perhatian | Terapkan aturan 1 aksi primer; jadikan tombol kedua sebagai tombol netral/link |
| Strip 4 kotak metrik KPI seragam dengan persentase statis | Gantikan dengan panel telemetri operasional atau antrean alur kerja nyata |
| Istilah fiksi ilmiah palsu (*"Chamber 01"*, *"Ruang Virtual 3D"*) | Gunakan istilah teknis nyata (*"Connection Socket"*, *"Session Store"*, *"Webhook Stream"*) |
| `transition: all` atau `transition-all` | Tuliskan properti spesifik: `transition-property: transform, opacity` |
| `:active` tanpa pengecualian `:disabled` | Tambahkan `:not(:disabled):active` atau `enabled:active:` |
| Kontrol interaktif dengan ukuran sentuh `< 44x44px` di mobile | Tambahkan padding atau pseudo-element target sentuh minimal 44x44px |
| Input formulir `< 16px` di perangkat mobile | Gunakan `text-base sm:text-sm` untuk mencegah zoom paksa iOS Safari |
| Komponen modal tanpa `overscroll-behavior: contain` | Tambahkan `overscroll-behavior: contain` |
