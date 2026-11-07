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
- **Koreografi Scroll Reveal Progresif (Blur Fade-In & Gentle Rise)**: Untuk seksi landing page dan kartu naratif, terapkan pola `ScrollBlurReveal` (`../maxilun-motion/references/motion-components.md`): elemen di luar layar memiliki `opacity: 0; filter: blur(10px); transform: translateY(28px)`, lalu saat scroll masuk viewport bertransisi halus ke `opacity: 1; filter: blur(0); transform: translateY(0)`. Bersihkan `filter` setelah animasi selesai dan selalu hormati `@media (prefers-reduced-motion: reduce)`.

### 1.5 Standar Kontainer Kartu Produksi (Anti-Neon Outline & Anti-Status Theater)
- **Neutral Hairline Border, Bukan Garis Neon**: Border kontainer kartu wajib netral 1px dengan opasitas rendah (`oklch(1 0 0 / 0.08)` pada dark mode, `oklch(0 0 0 / 0.08)` pada light mode). **Dilarang keras membungkus keliling kartu dengan border berwarna saturasi tinggi/neon** (`border-cyan-500`, `border-purple-500`). Warna aksen hanya boleh digunakan sebagai titik status atau indikator aktif kecil, bukan garis pagar keliling kartu!
- **Tolak Radial Glow Blobs di Belakang Kartu**: Dilarang memasang lingkaran blur besar (`blur-3xl bg-cyan-500/20`) di balik kartu untuk menciptakan kesan "menyala". Kedalaman kartu harus lahir dari perbedaan nada permukaan (`Surface` vs `Elevated`) dan bayangan kontak halus.
- **Tolak Telemetri & Status Teater Palsu**: Dilarang menempelkan label fiktif seperti `// 60 FPS`, `• ONLINE`, `• PING: 0.1ms`, `SYSTEM NORMAL` secara statis tanpa sumber data streaming nyata (`CMP-020`). Jika menampilkan status soket/koneksi, wajib mencerminkan state asli (`CONNECTED`, `CONNECTING`, `DISCONNECTED`) dengan teks + ikon semantik pendamping.

### 1.6 Larangan Polusi Emoticon/Emoji pada Antarmuka (`CMP-003`)
- **Dilarang Keras**: Menyusupkan karakter emoji Unicode (`🚀`, `✨`, `🔥`, `⚡`, `💡`, `🎉`, `⭐`, `✅`, `❌`, `⚠️`, `👉`, `💎`, `🌟`, `🤖`, `💬`, dll.) ke dalam:
  1. Tombol atau tautan navigasi (`<button>⚡ Submit</button>`).
  2. Judul heading atau subjudul (`<h3>⚡ Fast Performance</h3>`).
  3. Badge, tag, atau chip hero (`<span>✨ New Feature</span>`).
  4. Kartu fitur atau daftar checklist (`<li>✅ 99.9% Uptime</li>`).
  5. Sel status tabel atau pesan toast notifikasi.
- **Standar Vektor Wajib**:
  - Gantikan dengan ikon vektor SVG monokrom geometris (`stroke="currentColor"` / `fill="currentColor"`) dari library standar (Lucide, Radix, Heroicons) atau SVG inline terkalibrasi.
  - Untuk checklist: gunakan SVG path checkmark `<svg class="w-4 h-4 text-emerald-500" ...><path d="M5 13l4 4L19 7" .../></svg>`.
  - Seluruh ikon wajib lulus *1-Bit Monochrome Test*: tetap jelas dan terbaca saat diubah menjadi hitam-putih murni 1-bit tanpa warna atau bayangan.

### 1.7 Invarian Simetri Tema Ganda & Sinkronisasi Canvas (`CLR-009` & `MOT-005`)
- **Zero Dark-Trap Lock**: Setiap komponen dengan background kustom gelap (misal kartu CTA dengan radial gradient gelap `#030509` atau container terminal) **wajib mendefinisikan aturan pembalik simetris** pada `[data-theme="light"]`. Dilarang keras membiarkan teks mewarisi `var(--text)` gelap di atas latar belakang gelap.
- **Protokol Sinkronisasi Canvas (Canvas Theme Sync)**: Elemen HTML5 `<canvas>` 2D/3D tidak mewarisi variabel CSS secara otomatis. Seluruh fungsi gambar canvas (`fillText`, `strokeText`, `strokeStyle`) **wajib mendeteksi tema aktif** secara dinamis:
  ```javascript
  const isLight = document.documentElement.getAttribute('data-theme') === 'light';
  ctx.fillStyle = isLight ? '#090d16' : '#f1f5f9';
  ctx.strokeStyle = isLight ? 'rgba(0, 0, 0, 0.2)' : 'rgba(255, 255, 255, 0.22)';
  ```
- **Simetri Mockup Pihak Ketiga**: Mockup antarmuka nyata (seperti WhatsApp chat atau mobile frame) wajib memiliki varian terang otentik (`#efeae2` wallpaper, `#d9fdd3` outgoing bubble, teks `#111b21`) saat aplikasi beralih ke tema terang.

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


### 2.4 Anti-Gradien Teks & Pemilihan Karakter Typeface
- **Larangan Keras Gradien Teks**: Dilarang keras menggunakan efek gradien teks pelangi (`bg-clip-text text-transparent bg-gradient-to-r ...`) pada headline hero. Judul wajib menggunakan tinta solid dengan kontras tinggi ($\ge 4.5:1$, pada tema gelap $\ge 7:1$). Gradien teks adalah tanda tangan template AI generik murahan yang menutupi kelemahan tipografi.
- **Pemisahan 3 Lapisan Font (Font Layering)**:
  1. *Display / Headline Face*: Typeface berkarakter struktural kuat (misal: *Geist*, *Cabinet Grotesk*, *Instrument Sans*, *Plus Jakarta Sans*, atau *Manuka* untuk editorial tegas) dengan tracking negatif rapat (`-0.02em` s.d. `-0.04em`).
  2. *Technical / Protocol Monospace*: Monospace tajam (misal: *JetBrains Mono*, *Geist Mono*, *Fira Code*) untuk spesifikasi protokol, WebSocket state, JSON payload, token ID, dan stempel waktu.
  3. *Functional Sans*: Sans netral untuk paragraf, navigasi, dan tombol dengan line-height proporsional (`1.5–1.6`).
- **Eliminasi Kapsul Hero Pill (`CMP-015`)**: Dilarang mencetak kapsul pill oval (`rounded-full`) dengan peluru `•` (`• SIGNAL PROTOCOL TCP • ...`) di atas H1. Jika membutuhkan penanda kategori, gunakan teks murni tanpa kapsul (eyebrow editorial kecil, huruf kapital berjarak, tanpa border kotak) atau leburkan langsung ke dalam kalimat judul.

### 2.5 Disiplin Anti-Overflow Tipografi & Skala Fluid Mobile (`TYPO-009`)
- **Fluid Heading Scaling**: Dilarang menggunakan ukuran teks display statis besar (mis. `text-5xl` atau `text-6xl`) tanpa breakpoint mobile. Pada layar ponsel $\le 375\text{px}$, kata panjang seperti *"Infrastruktur"* atau *"Communication"* akan langsung patah kasar atau terpotong keluar melebihi canvas! Wajib gunakan skala breakpoint bertahap (`text-2xl sm:text-4xl md:text-5xl lg:text-6xl`) atau CSS clamp: `font-size: clamp(1.875rem, 1.25rem + 3.125vw, 3.75rem);`.
- **Word Wrapping & Breakage**: Wajib pasang `break-words` atau `overflow-wrap: anywhere` pada judul hero dan heading komponen.
- **Monospace, Token & URL Overflow**: Seluruh string panjang yang tidak memiliki spasi alami (JID WhatsApp, token hash, URL endpoint, cURL command) **wajib** diberi kelas `break-all` atau dibungkus dalam kontainer berbatas dengan scroll horizontal terisolasi `overflow-x-auto`.
- **Flex & Grid Child Truncation Invariant**: Setiap flex/grid child yang menampung teks terpotong (`truncate` / `text-ellipsis`) **wajib menyertakan `min-w-0`** (`min-width: 0`). Tanpa `min-w-0`, spesifikasi CSS flexbox akan mempertahankan lebar konten teks asli dan mendorong kontainer melebihi canvas layar!
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
- Pilih struktur yang mengikuti sifat konten: penyejajaran ke tepi awal (*text-align: start*), komposisi split dengan artefak produk hidup, tabel perbandingan, urutan editorial, atau grid asimetris (`2:1`, `1:2`) ketika setiap panel memiliki bobot fungsi berbeda.

### 4.3 Properti Logis CSS (Logical Properties)
Gunakan properti logis untuk seluruh dimensi arah:
- `margin-inline-start`, `margin-inline-end`, `padding-block`, `inset-inline-start`, `text-align: start`.
- Hindari `width: 100vw` (akan memicu scroll horizontal karena memperhitungkan scrollbar desktop; gunakan `width: 100%`).
- Hindari `height: 100vh` pada container penuh di mobile (gunakan `height: 100dvh` agar tidak tertutup address bar browser).


### 4.4 Rekayasa Hero Section Kelas Dunia (The Living Hero vs "Biasa Saja Jadi Aneh")
- **Diagnosa Sindrom "Biasa Saja Jadi Aneh"**: Model AI menghasilkan hero yang membosankan (*biasa saja*) karena memakai tumpukan senter malas (Pill $\to$ H1 $\to$ Subtitle $\to$ 2 Tombol). Kemudian karena merasa kosong, AI menambalnya dengan dekorasi aneh: teks gradien pelangi, glow neon, dan kanvas partikel 3D hampa (*jadi aneh*).
- **Aturan Eksekusi Hero Produksi**:
  1. **Asymmetric Split Hero (50/50 atau 55/45)**: Wajib untuk seluruh produk developer, alat kerja, API gateway, dan B2B. Sisi kiri penyejajaran teks awal (*text-align: start*), judul display solid, dan tepat 1 tombol aksi primer.
  2. **The Living Engine (Bukan Gambar Kartun / Gimmick 3D)**: Sisi kanan hero menampung objek kerja nyata yang dapat berinteraksi:
     - *Messaging Gateway*: Terminal pairing WhatsApp nyata + live WebSocket JSON event stream dengan event `messages.upsert` dan latensi p95.
     - *Cloud / Developer Tools*: Tab switchable cURL / TypeScript SDK + output respons JSON nyata.
     - *Fintech / Ledger*: Kartu kalkulasi biaya / transaksi interaktif.
  3. **Eyebrow Editorial Murni**: Metadata kategori tampil sebagai teks murni tanpa kapsul rounded-full, tanpa border, tanpa peluru bullet `•` (`font-mono text-xs uppercase tracking-wider text-muted`).
  4. **Salinan Instalasi Cepat (One-Click CLI)**: Di samping tombol aksi primer, sertakan blok salin perintah terminal kompak (`$ npx aetherlink@latest` atau `$ docker run ...`) alih-alih tombol kedua yang berebut perhatian.

### 4.5 Standar Navbar Responsif & Ergonomi Mobile (Anti-Navbar Bloat `LAY-015` & `LAY-016`)
- **Tinggi Navbar Mobile Ketat ($\le 64\text{px}$)**: Tinggi navbar pada viewport mobile wajib berada di rentang **56px–64px** (`h-14 sm:h-16`). Navbar mobile yang membengkak $> 64\text{px}$ memakan paruh atas layar secara rakus.
- **Komposisi Navbar Mobile 2-Elemen**: Pada layar ponsel (`< 768px`), navbar hanya boleh menampilkan tepat 2 elemen:
  1. *Kiri*: Logo atau nama merek ringkas.
  2. *Kanan*: Tepat 1 pemicu menu (tombol hamburger atau 1 aksi ringkas).
  - Tautan menu teks desktop **wajib disembunyikan** di mobile (`hidden md:flex`), dilarang dibiarkan meluap atau bertumpuk menjadi dua baris.
  - Tombol CTA desktop ("Mulai Uji Coba", "Akses Console") disembunyikan di mobile atau disederhanakan menjadi ikon ringkas tanpa teks panjang.
- **Drawer Mobile & Scroll Lock**: Menu drawer mobile wajib memiliki:
  - *Scroll Containment*: `overscroll-behavior: contain` pada backdrop dan drawer agar halaman di belakangnya tidak ikut bergulir (*background scroll chaining*).
  - *Accessibility*: `aria-expanded="true/false"`, penutupan tombol `Escape`, dan pengembalian fokus ke pemicu hamburger.
- **Zero Horizontal Scrollbar (`LAY-016`)**:
  - Dilarang keras memakai `width: 100vw` (selalu gunakan `width: 100%` agar tidak menghitung lebar scrollbar desktop).
  - Padding kontainer horizontal di mobile dibatasi maksimal `px-4 sm:px-6` (dilarang `px-12` atau `px-16` di mobile).
  - Setiap kontainer kartu dan layout wajib memiliki `max-w-full`.
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
| Gradien teks pelangi pada judul (`bg-clip-text text-transparent`) | Ganti dengan warna tinta solid berdaya kontras tinggi ($\ge 7:1$ pada tema gelap) |
| Kapsul pill tagline dengan peluru (`• TAG 1 • TAG 2 •`) di atas H1 | Hapus kapsul; gunakan eyebrow editorial teks murni tanpa border atau leburkan ke judul |
| Kanvas 3D partikel/mesh palsu pada produk gateway/backend API | Ganti dengan konsol operasional hidup (live WebSocket stream, status pairing QR, inspektor JSON) |

---

## 8. Protokol Pembongkaran Kunci Sistem Desain pada Redesign (Dismantling Legacy Design System Locks)

Ketika pengguna meminta **redesign**, kegagalan terbesar model AI adalah *The Legacy Design Lock Trap*: model mendeteksi adanya variabel/layout lama yang kusam, tetapi takut menghapusnya dan hanya menambal utility lokal di file komponen. Akibatnya, UI/UX tetap "begitu-begitu saja" karena fondasi visualnya tidak pernah diganti.

### 8.1 Taksonomi 5 Kunci Sistem Desain (Design Locks)

1. **Token & Variable Lock (`SYS-001`)**:
   - *Bentuk*: Variabel `:root`, CSS custom properties, atau Tailwind `@theme` yang mematok warna ke palet slate generik (`#3b82f6`, `--background: #f8fafc`, `--border: #e2e8f0`).
   - *Dampak*: Menjebak antarmuka dalam estetika dingin membosankan tanpa karakter domain.
   - *Tindakan Wajib*: Hapus token lama di root stylesheet (`globals.css` / `theme.css`); definisikan ulang tangga warna OKLCH material fisik domain produk (`--hue-neutral`, `--hue-accent`, `color-scheme`).

2. **Shell & Layout Wrapper Lock (`SYS-002`)**:
   - *Bentuk*: Pembungkus global di `layout.tsx`, `App.tsx`, atau `index.html` seperti `<div className="container mx-auto max-w-7xl px-4 py-8">` atau background hardcoded di `<body>`.
   - *Dampak*: Mencekik komposisi tata letak baru, memaksa seluruh konten masuk ke dalam kontainer sempit yang kaku.
   - *Tindakan Wajib*: Buka kontainer wrapper; sediakan layout kanvas yang fleksibel untuk hierarki tugas paruh atas, *split artifact*, atau *operational ledger*.

3. **Component Primitive Lock (`SYS-003`)**:
   - *Bentuk*: Komponen bersama lama (`<Card>`, `<Button>`, `<Input>`) yang memaksakan border pucat `1px solid #e2e8f0`, radius seragam tanpa konsentrisitas, atau padding flat.
   - *Dampak*: Setiap elemen baru yang dirender otomatis mewarisi gaya usang lama.
   - *Tindakan Wajib*: Mutakhirkan primitif komponen ke formula radius konsentris eksak, elevasi berlapis transparan (*layered box-shadow*), dan aturan 1 aksi primer.

4. **Typography Lock (`SYS-004`)**:
   - *Bentuk*: Font family dipatok ke sans sistem polos atau Inter tanpa peran display berkarakter, tanpa batas measure `60–75ch`, dan angka bergetar tanpa `tabular-nums`.
   - *Dampak*: Hierarki baca datar dan kelelahan visual bagi pengguna.
   - *Tindakan Wajib*: Pasangkan typeface display berkarakter domain + functional sans, pasang `text-wrap: balance` pada judul, dan wajib `font-variant-numeric: tabular-nums` pada angka.

5. **Zombie Style Lock & Tabrakan Styling (`SYS-005`)**:
   - *Bentuk*: File CSS lama, CSS modules tak terpakai, kelas utilitas lama, atau selector bertingkat yang saling menimpa secara acak.
   - *Dampak*: Konflik visual, flicker, atau aturan baru kalah spesifisitas.
   - *Tindakan Wajib*: Lakukan *Clean Cutover*—hapus tuntas kode styling lama yang menjadi usang akibat redesign. Dilarang meninggalkan zombie CSS shims.

### 8.2 Protokol Eksekusi 4 Tahap Clean Cutover

| Tahap | Tindakan Konkret | File Target Khas |
|---|---|---|
| **1. Scan & Isolate** | Petakan variabel `:root`, wrapper `layout.tsx`, dan primitif komponen yang mengunci tampilan saat ini. | `globals.css`, `tailwind.config.*`, `layout.tsx` |
| **2. Root Token Replacement** | Gantikan token warna, radius, dan tipografi di root dengan sistem OKLCH kontekstual domain produk. | `src/app/globals.css`, `src/styles/theme.css` |
| **3. Shell Emancipation** | Buka kontainer wrapper yang kaku, hapus background hardcoded lama pada body/html, pasang arsitektur layout tugas. | `src/app/layout.tsx`, `src/App.tsx` |
| **4. Primitive Upgrade & Purge** | Mutakhirkan komponen tombol/kartu/input dan hapus seluruh kode styling lama yang usang (*clean purge*). | `src/components/ui/*`, modul CSS lama |

### 8.3 Anti-Pola Tambal Sulam (The Band-Aid Redesign Trap)

- **Dilarang**: Menambahkan `!important` atau inline style overrides (`style={{ backgroundColor: ... }}`) pada komponen anak untuk mengakali token root lama yang kusam.
- **Dilarang**: Mendesain ulang kartu di dalam halaman tetapi membiarkan background halaman tetap abu-abu kusam `#f8fafc` dari root layout lama.
- **Wajib**: Jika sistem desain lama membelenggu tampilan, **bongkar kuncinya di sumbernya (root & shell)**, bukan menutupinya dengan tambalan lokal.

---

## 9. Rekayasa Dashboard Produksi & Eliminasi Slop Dashboard (Enterprise Dashboard Standards)

Dashboard adalah area yang paling rentan terhadap polusi AI slop karena generator otomatis cenderung mengulang template klise yang sama: 4 kartu metrik statis, Bento gelap salah domain, status dot tanpa teks, dan tombol penuh emoji.

### 9.1 Eliminasi 5 Slop Dashboard Klasik

1. **Pembersihan Strip 4 KPI Mengambang (`LAY-009` / `LAY-012`)**:
   - *Slop*: 4 kotak identik di baris atas dengan angka fiktif dan badge `+12.5%` tanpa konteks rentang waktu.
   - *Solusi Enterprise*: Gunakan **Operational Status Rail** satu baris terukur dengan pemilih rentang waktu nyata (`1h` / `24h` / `7d`), angka `tabular-nums` rata kanan, dan sparkline SVG proporsional.

2. **Arsitektur Layout Berbasis Sifat Tugas, Bukan Bento Gelap Seragam (`LAY-013`)**:
   - *ERP, Akuntansi, Kasir, Logistik*: Wajib gunakan **Operational Ledger** (tabel padat, baris `40px–48px`, font sans netral, kontras tinggi). Dilarang memakai tema cyberpunk/dark mode neon.
   - *Observabilitas, Cloud, DevTools*: Gunakan **Master-Detail Inspector** (panel entitas di kiri, telemetri dan log aktif di kanan).
   - *Klinik & Reservasi*: Gunakan **Timeline / Calendar Slot Matrix** (fokus slot waktu dan antrean pasien).

3. **Disiplin 4 State pada Setiap Panel & Tabel Dashboard**:
   - Dilarang hanya menampilkan dashboard dalam kondisi data statis ideal.
   - Setiap panel dan tabel wajib memiliki implementasi konkret untuk 4 status:
     1. *Loading State*: Skeleton geometri 1:1 proporsional ($\text{CLS}=0$), dilarang spinner kosong mengambang di tengah layar.
     2. *Empty State*: Alasan faktual mengapa belum ada data + tombol aksi pertama yang jelas (misal: *"Belum ada transaksi hari ini · [Buat Transaksi Baru]"*).
     3. *Populated State*: Data riil dengan angka `tabular-nums` rata kanan dan teks panjang yang aman dari overflow (`truncate` + `min-w-0`).
     4. *Error State*: Pesan kegagalan inline yang solutif + tombol *Coba Lagi* (*Retry*).

4. **Status Indikator Aksesibel (Anti-Color-Only Dot `CLR-004`)**:
   - Titik hijau/kuning/merah dilarang berdiri sendirian. Wajib selalu didampingi teks semantik status (`Active`, `Syncing`, `Degraded`, `Offline`) dan ikon pendukung.

5. **Pembersihan Emoji pada Kontrol Dashboard (`CMP-003`)**:
   - Dilarang keras memakai emoji (`🚀`, `✨`, `🔥`, `📊`, `💳`, `⚡`) pada tombol, tab navigasi, atau chip filter dashboard. Wajib gunakan ikon SVG monokrom geometris terstandarisasi.
