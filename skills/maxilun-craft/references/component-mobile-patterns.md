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

### 4.0 Sistem Arsitektur Navigasi & Menu Produksi (Navigation & Menu Architecture)

Menu dan bilah navigasi adalah jangkar struktural utama antarmuka. Model AI dilarang menghasilkan menu generik tanpa konteks bisnis atau navigasi mobile yang tidak ergonomis.

#### 1. Aturan Information Architecture (IA) Berbasis Domain
- **Larangan Ember Generik**: Dilarang menggunakan label navigasi template (`Dashboard`, `Features`, `Pricing`, `About`, `Contact`, `Analytics`, `Settings`) tanpa entitas bisnis nyata.
- **Derivasi Berbasis Verba & Objek**: Petakan menu langsung dari objek domain dan alur kerja pengguna:
  - *SaaS Finansial/Invoice*: `Antrean Tagihan`, `Buku Piutang`, `Rekonsiliasi Bank`, `Direktori Klien`.
  - *Developer Platform*: `Cluster Overview`, `Service Mesh`, `Incident Stream`, `Access Policies`.
  - *Klinik/Kesehatan*: `Antrean Pasien`, `Rekam Medis`, `Jadwal Dokter`, `Apotek Farmasi`.
- **Hierarki 3 Lapisan Navigasi**:
  1. *Primary Destinations (3–5 rute)*: Alur kerja 80% pengguna harian.
  2. *Secondary & Filter Actions*: Pencarian terindeks, filter status, batch export.
  3. *Utility & Account Anchor*: Workspace/organization switcher, pusat notifikasi faktual, preferensi profil.

#### 2. Empat Pola Navigasi Produksi Baku

##### Pola A: Command-Driven Header (SaaS & Web Modern)
- **Shell & Pinned Header**: Tinggi `56px–64px`, sticky di puncak layar dengan `backdrop-filter: blur(12px)` di atas permukaan semi-transparan (`oklch` alpha `0.85`), dipisah oleh garis bawah hairline `1px` (`var(--border-hairline)`).
- **Cluster Kiri (Brand Anchor)**: Logo identitas + badge pemilih workspace / status lingkungan (`Production` / `Staging`).
- **Cluster Tengah (Primary Links)**: Item menu horizontal dengan spasi `var(--space-1)` hingga `var(--space-2)`. Rute aktif ditandai dengan **Sliding Pill Highlight** (`var(--surface-card)` dengan bayangan halus) atau hairline border bawah, bukan sekadar mengubah warna teks menjadi biru.
- **Cluster Kanan (Action & Utilities)**:
  - Tombol pemicu Command Palette dengan visual shortcut badge: `Cmd+K` atau `Ctrl+K` (`<kbd>` dengan styling border hairline).
  - Lonceng notifikasi dengan hitungan angka tertunda nyata (`tabular-nums`), bukan badge titik merah tanpa fungsi.
  - Avatar profil dengan trigger popover menu akun (nama, email terpotong rapi, aksi logout/switch role).

##### Pola B: Operational Sidebar Rail (B2B, ERP & DevTools)
- **Dimensi & Struktur**: Lebar tetap `240px–260px` di desktop, berlatar `var(--surface-base)` dengan pembatas vertikal `1px` ke arah kanvas kerja. Dapat di-collapse menjadi *Icon Rail* `60px–64px` dengan tooltip kontekstual.
- **Puncak (Context Switcher)**: Dropdown pemilih organisasi/tim dengan inisial avatar + chevron indikator dan shortcut cepat (`⌘K`).
- **Seksi Menu Terkelompok**: Setiap kelompok diawali judul seksi teknis huruf kapital kecil (`text-xs font-semibold tracking-wider text-muted`, misal: `OPERATIONS`, `SECURITY`, `SYSTEM`).
- **Anatomi Item Menu**:
  - Ikon 18px dari keluarga tunggal dengan stroke konsisten (`1.5px–2px`).
  - Label teks dengan `line-height: 1.25` dan penanganan overflow (`truncate`).
  - Badge kuantitas dinamis di sisi kanan (misal: antrean pending `12` dengan `tabular-nums`).
  - Hint pintasan keyboard (`⌘1`, `⌘2`, `⌘3`) untuk akses cepat.
- **Bawah (User & Environment Dock)**: Area pengguna tertambat di dasar sidebar dengan indikator status kehadiran sistem, versi rilis, dan tombol menu preferensi.

##### Pola C: Ergonomic Mobile Navigation & Action Drawer
- **Ergonomi Zona Ibu Jari (Thumb Zone)**:
  - Pada layar `< 768px`, navigasi utama berpindah ke **Bottom Tab Bar (3–4 Item)** di bagian bawah layar. Tinggi `56px–64px` ditambah `padding-bottom: env(safe-area-inset-bottom)`.
  - Item tab bar memuat ikon 22px + label teks ringkas `11px–12px`. Target sentuh minimal `48x48px`.
- **Sheet Drawer untuk Sub-Navigasi**:
  - Dilarang merender dropdown hamburger layar penuh kaku yang memblokir konteks.
  - Navigasi sekunder dibuka via **Bottom Sheet Drawer** dengan drag-handle visual di atas, mendukung interaksi geser ke bawah (*swipe-to-dismiss*), dan otomatis memperhitungkan `visualViewport`.

##### Pola D: Contextual Mega-Menu / Category Flyout
- Untuk katalog atau dokumentasi besar: dropdown multi-kolom yang mengelompokkan link per kategori tematik.
- Setiap item link memuat: Judul link tebal + 1 baris deskripsi fungsional (`<= 8 kata`) + ikon pembantu.
- Kolom pendukung di sisi kanan: *Featured Card* (template unggulan, update rilis terbaru, atau kalkulator interaktif), bukan ruang kosong.
- Wajib bebas jebakan kursor (*cursor diagonal protection*) dan segera tertutup saat menekan `Escape`.

#### 3. Aksesibilitas & Mekanika Interaksi Navigasi
- **Penanda Rute Aktif**: Item aktif wajib memiliki atribut `aria-current="page"`.
- **Kontrak Keyboard**:
  - Navigasi menu utama mendukung perpindahan dengan tombol `Tab` dan panah (`ArrowRight`/`ArrowLeft` pada header, `ArrowDown`/`ArrowUp` pada sidebar).
  - Menekan `Escape` pada dropdown/drawer wajib menutup menu dan mengembalikan fokus keyboard ke tombol pemicu (*trigger button*).
- **State Indikator**: Status hover, focus-visible, dan active harus memiliki transisi halus (`150ms–200ms ease-out`) hanya pada `background-color`, `transform`, atau `opacity`.

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

### 4.5 Pola Tata Letak Otentik & Anti-Cetakan (Anti-Generic Layout Archetypes)

Model AI dilarang menggunakan cetakan tata letak klise yang membuat situs tampak generik dan membosankan.

#### 1. Larangan Tiga Cetakan Klise Utama
- **Larangan 3-Kartu Simetris**: Dilarang menggunakan tata letak `grid-cols-3` berulang dengan 3 kartu identik berisi ikon lingkaran di atas, judul, dan 2 baris teks abu-abu.
- **Larangan 4-Kotak Metrik Seragam**: Dilarang membuka dashboard dengan strip 4 kotak kecil simetris yang memuat angka statis dan badge hijau persentase palsu (`+12.5%`).
- **Larangan Centered Hero Dual-Button**: Dilarang menyusun hero section dengan judul rata tengah, subteks panjang rata tengah, dan dua tombol pill simetris berdampingan yang berebut fokus.

#### 2. Tiga Arsitektur Tata Letak Pengganti Produksi

##### A. Asymmetric Bento Grid (Hierarki Berbasis Fungsi)
- Gunakan rasio spasial asimetris (`2:1`, `1:2`, atau `2:3`) di mana ukuran kartu ditentukan oleh kedalaman fungsinya:
  - **Kartu Primer (Hero Card, 60–66% lebar)**: Memuat elemen interaktif aktif — simulator perhitungan live, visualisasi alur kode nyata, atau pemutar data telemetri interaktif.
  - **Kartu Sekunder (Companion Cards, 33–40% lebar)**: Memuat ringkasan status operasional, log audit terkini, atau kontrol sakelar cepat.
- Setiap kartu di dalam bento grid wajib memiliki perlakuan visual dan konten yang berbeda (bukan 3 variasi dari elemen yang sama).

##### B. The Surface & Elevation Ladder (Kedalaman Struktural)
Gantikan bayangan tebal seragam dan border berat dengan 4 tingkatan permukaan semantik:
1. **Level 0 (Canvas Floor)**: Latar belakang aplikasi (`oklch(98.5% ...)` untuk tema terang, `oklch(14% ...)` untuk tema gelap).
2. **Level 1 (Surface Panel)**: Kontainer kerja utama yang dipisahkan oleh garis hairline `1px solid var(--border-hairline)`, tanpa bayangan.
3. **Level 2 (Elevated Card & Interactive)**: Kartu yang dapat ditekan atau di-hover, menggunakan pencerahan mikro pada nada permukaan (`oklch` lightness `+2%`) dan bayangan kontak sangat halus (`0 1px 2px rgba(0,0,0,0.05)`).
4. **Level 3 (Overlay & Modal)**: Dialog, popover, command palette yang melayang di atas kanvas dengan backdrop scrim translusen.

##### C. Typographic Tension & Densitas Visual
- **Kontras Skala Ekstrem**: Pasangkan display headline tajam (tracking rapat `-0.02em` hingga `-0.04em`, line-height `1.15`) dengan label mikro teknis (font monospace atau sans-serif kapital, tracking longgar `+0.05em`, `font-size: 11px–12px`).
- **Ritme Densitas Kontras**: Ciptakan ketegangan visual antara zona baca editorial yang tenang dan lega (*low-density reading zone*) dengan zona kerja data yang rapat (*high-density operational panel* dengan `tabular-nums` dan padding `8px–12px`).
##### D. Standar Formula Inner Radius Konsentris
- **Formula Matematika**:
  `radius_inner = max(0, radius_outer - padding)`
- *Implementasi Nyata*: Jika card luar memiliki radius `16px` dan padding `8px`, maka elemen tombol atau input di dalamnya wajib memiliki radius `8px` (`16 - 8 = 8px`), bukan `16px` seragam ataupun `0px`.

### 4.6 Standar 8-State Feedback Interaktif & Form Hygiene (WIG Compliance)

Setiap elemen kontrol interaktif primer (Button, Input, Dropdown) wajib mengimplementasikan **8 state interaktif terukur**:
```
[1. Default] ──► [2. Hover] ──► [3. Focus-Visible] ──► [4. Active/Press (scale 0.97)]
     │                                                               │
     ▼                                                               ▼
[5. Disabled] ◄── [6. Loading/Spinner] ◄── [7. Error] ◄── [8. Success]
```

#### Aturan Form & Input Hygiene (WIG)
1. **Larangan Blokir Paste**: Dilarang keras menonaktifkan fungsi tempel (`onPaste` dengan `preventDefault()`). Pengguna wajib dapat menempel password, token, dan data form.
2. **Spellcheck Disiplin**: Matikan spellcheck (`spellCheck={false}`) untuk input email, username, kode lisensi, dan token teknis guna menghilangkan garis bawah merah yang merusak visual.
3. **Label Interaktif & Hit Target**: Setiap input wajib memiliki `<label>` terkait (via `htmlFor` atau nesting). Pada checkbox dan radio, label dan kotak seleksi harus berbagi satu target klik terpadu tanpa zona mati.
4. **Truncation Guard**: Setiap flex container yang menampung teks terpotong (`truncate` / `text-overflow: ellipsis`) wajib menambahkan `min-w-0` agar flex child tidak meluap ke luar kontainer.
5. **Scroll Containment**: Pasang `overscroll-behavior: contain` pada modal, drawer, dan dropdown menu agar scroll di dalam modal tidak merambat ke halaman utama.
6. **Micro-Typography Web**:
   - Gunakan elipsis unicode `…` (bukan tiga titik biasa `...`).
   - Gunakan `text-wrap: balance` atau `text-pretty` pada display titles dan headings untuk mencegah satu kata menggantung di baris akhir (*widow*).
   - Pasang non-breaking space `&nbsp;` pada pintasan keyboard (`⌘&nbsp;K`) dan besaran angka bersatuan (`10&nbsp;MB`, `24&nbsp;px`).

### 4.7 Prinsip "One Live Thing" & Protokol Inventarisasi Subjek

1. **Inventarisasi Subjek Nyata (Subject Inventory)**:
   Sebelum merancang antarmuka, telusuri 8–12 fakta unik milik produk/klien yang tidak dimiliki kompetitor:
   - Makna nama produk, asal lokasi/kota, bahan/material fisik (kayu, silikon, kertas, tembaga).
   - Angka konkret di dalam model bisnis (durasi proses, kapasitas, tahun, harga jujur).
   - Batasan operasional nyata (misal: rilis batch mingguan, reservasi terjadwal).
   - Benda cetak atau analog yang ada di dunianya (tiket, manifest, bagan, buku kas).
2. **Prinsip "One Live Thing"**:
   Setiap halaman web yang didesain dilarang hanya berupa kartu statis. Wajib ada **satu interaksi hidup** di mana pengunjung dapat memanipulasi parameter nyata:
   - *Fintech*: Simulator kalkulasi dividen / pelunasan pinjaman secara real-time.
   - *DevTools*: Playground interaktif pengujian regex atau curl preview generator.
   - *Produk Fisik*: Selektor material/tekstur interaktif yang mengubah visual seketika.
   - Syarat: Berfungsi instan, ramah sentuhan ibu jari di mobile, dan memiliki fallback graceful tanpa JavaScript.

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
