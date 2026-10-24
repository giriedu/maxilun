# Production Component, Mobile Interaction & Iterative Workflow Reference

Gunakan referensi ini bersama `maxilun-craft` saat merancang atau mengimplementasikan komponen produksi, interaksi perangkat sentuh (mobile), `PRODUCT.md` / `DESIGN.md`, atau menjalankan 24 perintah desain iteratif.

---

## 1. Struktur `PRODUCT.md` & Surface Briefs

### 1.1 `PRODUCT.md` (Single Source of Product Truth)
```markdown
# [Product Name] — Product Context

## Identity & Audience
- **Name & Tagline**: [Nama produk + proposisi nilai <= 8 kata]
- **Primary Audience**: [Role spesifik, konteks kerja, perangkat utama]
- **Anti-Audience**: [Siapa yang sengaja BUKAN target produk ini]

## Core Problem & Metrics
- **Problem Solved**: [Masalah konkret yang dipecahkan beserta bukti kuantitatif]
- **Success Metrics**: [KPI utama: task completion time, error rate, conversion]

## Operating & Voice Constraints
- **Platform & Stack**: [Web / Mobile / Desktop, batas bundle & latensi]
- **Accessibility**: [Minimal WCAG AA 4.5:1, keyboard-first / touch-first]
- **Voice & Tone**: [Calm Operational / Authoritative / Friendly — natural, bebas jargon]
```

### 1.2 Surface Briefs (`.maxilun/surfaces/*.md`)
Pisahkan arah visual per halaman/rute dari `PRODUCT.md` agar kebenaran produk tetap stabil sementara eksplorasi visual dapat disesuaikan per permukaan (misal: *Landing Page* vs *Operational Dashboard* vs *Checkout Modal*).

---

## 2. Katalog 24 Perintah Desain Iteratif (`/maxilun-craft <cmd>`)

Perintah berikut adalah pola prompt terarah untuk agen:

| Kategori | Perintah | Fungsi Spesifik |
|---|---|---|
| **Core Workflow** | `init`, `shape`, `build`, `polish`, `audit`, `critique`, `document`, `extract` | Inisialisasi konteks, perencanaan struktur UX, implementasi, pemolesan akhir, audit kualitas/aksesibilitas, dan ekstraksi token ke `DESIGN.md` |
| **Refinement** | `bolder`, `quieter`, `distill`, `harden`, `clarify`, `typeset`, `colorize`, `layout` | Memperkuat kontras/hierarki, menenangkan tampilan ramai, memangkas elemen tak perlu, menambah edge-case/error state, memperbaiki copy, tipografi, warna semantik, dan ritme grid 4px |
| **Enhancement** | `animate`, `delight`, `overdrive`, `onboard`, `adapt`, `optimize` | Menambahkan micro-interaction (`maxilun-motion`), empty state & first-run flow, adaptasi responsif lintas-viewport, dan optimasi performa render |
| **Advanced & Review** | `direction`, `images`, `review`, `app`, `frame`, `live`, `generate`, `detect` | Memilih 1 dari 20 Art Directions, mencari gambar lisensi terbuka beserta kredit, self-review 3 lebar layar (`375px`, `768px`, `1440px`), rute khusus dashboard/app, dan pemeriksaan frame |

---

## 3. Sistem 20 Art Directions (Anti-Generic Visual Direction)

Saat membangun antarmuka baru, pilih **1 arah artistik yang sesuai dengan konteks produk** (atau padukan dengan 1–2 file dari `references/design-md/index.md`):

| # | Art Direction | Karakteristik Visual Utama | Cocok Untuk Domain |
|---|---|---|---|
| 1 | **Editorial Magazine** | Tipografi display tajam, grid asimetris, ruang kosong terarah | Media, publikasi, laporan riset, dokumentasi |
| 2 | **Swiss International** | Grid matematis ketat, sans-serif objektif, palet terbatas, garis hairline | Fintech, korporat, layanan profesional, B2B |
| 3 | **Neo-Brutalist** | Border tegas (`1.5px-2px`), kontras ekstrem, kejujuran struktural | Studio kreatif, kampanye produk, komunitas dev |
| 4 | **Japanese Minimalist** | *Ma* (ruang negatif bermakna), keseimbangan tenang, warna alam | Kesehatan, gaya hidup, arsitektur, produk premium |
| 5 | **Retro-Futurism** | Geometri tegas, aksen fosfor terukur, tipografi teknis | Gaming, audio/musik, event teknologi |
| 6 | **Organic Modern** | Sudut hangat, palet bumi (*earth tones* OKLCH), kontras lembut | Keberlanjutan, F&B, kesehatan mental, edukasi anak |
| 7 | **Industrial Technical** | Monospace presisi, label fungsional ber-indeks, skema bak cetak biru | Developer tools, cloud infra, hardware, IoT |
| 8 | **Art Deco Revival** | Simetri struktural, aksen emas/tembaga hangat, kontras gelap-terang | Perhotelan, fashion, acara eksklusif |
| 9 | **Scandinavian Functional** | Permukaan terang hangat, bayangan sangat halus, keterbacaan maksimum | E-commerce rumah tangga, produktivitas keluarga |
| 10 | **Cyber-Telemetry Dense** | Permukaan gelap pekat, indikator status semantik tajam, grafik rapat | Keamanan siber, observabilitas, perdagangan kripto |
| 11 | **Vintage Editorial Print** | Serif berkarakter, latar krem kertas (`canvas-cream`), pemisah garis klasik | Penerbitan buku, kopi/artisan, arsip sejarah |
| 12 | **Single-Layer Translucent** | Maksimal 1 lapis blur kontekstual pada header/modal di atas permukaan solid | Aplikasi desktop/OS modern, command palette |
| 13 | **Bauhaus Geometric** | Warna primer terkalibrasi, bentuk dasar fungsional, keseimbangan dinamis | Sekolah desain, alat kolaborasi kreatif |
| 14 | **Vibrant Commerce** | Fotografi produk dominan, badge harga/diskon faktual, CTA kontras tinggi | Retail modern, pengiriman makanan, marketplace |
| 15 | **Monochrome Typography** | Satu keluarga warna, skala ukuran huruf sebagai pembentuk hierarki tunggal | Portofolio arsitek, firma hukum, penulisan |
| 16 | **Calm Atmospheric** | Transisi nada permukaan lembut untuk memandu fokus pernapasan/tugas | Aplikasi fokus, kesehatan, pembaca buku |
| 17 | **Data-Dense Operational** | Padding kompak (`4px-8px`), `tabular-nums` rata kanan, panel tenang tanpa shadow | ERP, kasir/POS, admin finansial, monitoring |
| 18 | **Illustrated Guided Flow** | Vektor fungsional yang menjelaskan langkah kerja secara bertahap | Onboarding produk, edukasi interaktif |
| 19 | **High-Contrast Luxury** | Hitam pekat / putih bersih, margin ekstra lega, tipografi proporsional | Otomotif flagship, properti, jam tangan |
| 20 | **Tactile Micro-Responsive** | Tombol dan kontrol dengan umpan balik pegas instan (`< 150ms`) | Aplikasi utilitas harian, manajemen tugas |

---

## 4. Pola Komponen Produksi (Production Component Specifications)

### 4.1 Form Validation UX
- **Inline Error dengan `aria-describedby`**: Tampilkan pesan error tepat di bawah field terkait (`<div role="alert" id="err-email">`), bukan hanya toast global.
- **Timing Validasi (`Blur` lalu `Input`)**: Jangan memunculkan error merah saat pengguna baru mengetik huruf pertama. Validasi saat `blur`; setelah error muncul, validasi ulang secara real-time saat `input` agar error segera hilang ketika diperbaiki.
- **Submit State**: Nonaktifkan tombol submit **hanya** saat request jaringan sedang berlangsung (`aria-busy="true"` + spinner inline).

### 4.2 Data Tables & Responsive Collapse
- **Angka & Alignment**: Kolom teks rata kiri; kolom nominal uang, persentase, dan kuantitas wajib **rata kanan** dengan `font-variant-numeric: tabular-nums`.
- **Sorting & Filtering**: Gunakan `aria-sort="ascending|descending"` pada `<th>`, debounce pencarian teks `250ms–300ms`, dan tampilkan jumlah hasil filter beserta tombol `"Reset Filter"` pada keadaan kosong.
- **Mobile Collapse (`< 768px`)**: Jangan biarkan tabel 8 kolom meluber tanpa kendali. Ubah baris menjadi tumpukan kartu terstruktur dengan pasangan *Label : Nilai* atau bekukan kolom identitas pertama (*sticky first column*).

### 4.3 Modal, Dialog, Command Palette & Toast
- **Modal (`<dialog>` native)**: Wajib mengunci fokus (*focus trap*) di dalam modal, mengunci scroll `<body>`, menutup saat menekan `Escape`, dan mengembalikan fokus ke tombol pemicu saat ditutup. Jika form di dalam modal sudah diubah (*dirty*), minta konfirmasi sebelum menutup.
- **Command Palette (`Cmd/Ctrl + K`)**: Navigasi penuh dengan `ArrowUp`/`ArrowDown`, `Enter` untuk eksekusi, pengelompokan hasil per kategori, dan highlight karakter yang cocok.
- **Toast System**: Maksimal 3 toast tampil bersamaan; gunakan `aria-live="polite"` untuk status sukses dan `aria-live="assertive"` untuk error; hentikan hitung mundur (*pause timer*) saat pointer hover atau fokus keyboard berada di dalam toast.

### 4.4 File Upload & Multi-Step Wizard
- **File Upload**: Validasi ukuran dan MIME type di sisi client sebelum unggah (dengan pesan spesifik: *"File laporan.pdf (8.4MB) melebihi batas 5MB"*), tampilkan progres per berkas, dan sediakan tombol *Retry* untuk berkas yang gagal jaringan.
- **Multi-Step Wizard**: Gunakan `aria-current="step"` pada langkah aktif, validasi per langkah sebelum lanjut, dan simpan draft input di `sessionStorage`/state agar tidak hilang saat halaman ter-refresh.

---

## 5. Pola Interaksi Mobile & PWA (Touch-First Rules)

1. **Target Sentuh & Input iOS**: Semua kontrol interaktif minimal `44x44px` dengan jarak antar-target minimal `8px`. Font size pada `<input>`, `<select>`, dan `<textarea>` wajib `>= 16px` untuk mencegah auto-zoom paksa di iOS Safari.
2. **Semantic Keyboards**: Pasang `inputmode="numeric"` untuk kode OTP/PIN, `inputmode="decimal"` untuk nominal harga, `type="tel"` untuk telepon, dan atribut `autocomplete` yang tepat (`email`, `current-password`, `one-time-code`).
3. **Bottom Sheet & Safe Area**: Gunakan `visualViewport` API agar input di dalam bottom sheet tidak tertutup keyboard virtual, dan tambahkan `padding-bottom: env(safe-area-inset-bottom)` pada semua navigasi bawah / tombol sticky.
4. **Swipe Actions Accessibility**: Setiap aksi geser (*swipe-to-delete/archive*) wajib memiliki alternatif tombol terlihat atau menu konteks untuk pengguna pembesaran layar / motorik terbatas, ditambah *Undo Toast* selama 5 detik untuk aksi destruktif.

---

## 6. Protokol Self-Review 3 Breakpoint & Format Audit

Saat menjalankan review visual (baik melalui inspeksi kode maupun browser tool jika tersedia):
1. Uji pada **3 lebar layar wajib**: `375px` (Mobile), `768px` (Tablet), dan `1440px` (Desktop).
2. Periksa **Frame Quality**: judul utama jelas di layar pertama (*above the fold*), margin kiri/kanan seimbang, tidak ada ruang kosong tak sengaja, dan kontras lolos di tema Terang maupun Gelap (`color-scheme: dark` + inline script pencegah *Flash of Wrong Theme*).
3. Laporkan temuan secara konkret dengan format `file:line`, kode aturan (`CLR-001`, `CMP-004`, `TYPO-001`), dan perbaikan langsung pada token/CSS.
