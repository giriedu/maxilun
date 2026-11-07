# Production Component, Mobile Interaction & Iterative Workflow Reference

Referensi pendamping `maxilun-craft` untuk struktur konteks produk (`PRODUCT.md`), pemilihan arah artistik lintas-domain, spesifikasi komponen produksi, ergonomi perangkat sentuh, dan pemeriksaan lintas-viewport.

---

## 1. Konteks Produk & Pemisahan Permukaan (`PRODUCT.md`)

Ketika membangun produk dari awal, rumuskan identitas fungsional sebelum memilih estetika:
- **Audiens Utama & Anti-Audiens**: Siapa pemakai harian di lapangan, di perangkat apa (kasir tablet, ponsel lapangan, monitor lebar analis), dan siapa yang sengaja bukan sasaran.
- **Tugas Inti & Metrik Keberhasilan**: Tindakan utama apa yang harus tuntas cepat tanpa salah klik.
- **Pemisahan Permukaan**: Halaman publik (*landing/editorial*) boleh memiliki ekspresi tipografi dan ruang kosong lebih berani dibanding layar kerja operasional dalam (*workspace/ledger*) yang mengutamakan kepadatan dan kecepatan pemindaian.

---

## 2. Perintah Iterasi Desain Terarah (`/maxilun-craft <aksi>`)

| Kelompok | Kata Kerja | Sasaran Perubahan |
|---|---|---|
| **Struktur** | `init`, `shape`, `layout`, `app` | Menetapkan konteks produk, arsitektur informasi domain, hierarki tata letak, dan alur ruang kerja aplikasi |
| **Karakter** | `direction`, `typeset`, `colorize`, `bolder`, `quieter` | Memilih arah artistik, menajamkan skala tipografi, menyusun tangga warna OKLCH kontekstual, menaikkan atau menenangkan kontras |
| **Ketahanan** | `distill`, `harden`, `clarify`, `adapt` | Memangkas dekorasi mubazir, melengkapi 4 state data & edge-case teks panjang, memperbaiki microcopy, serta merapikan responsivitas |
| **Audit** | `audit`, `critique`, `polish`, `review` | Memeriksa kontras WCAG, radius konsentris, *Escalation Triggers*, dan konsistensi lintas 3 lebar layar |

---

## 3. Spektrum 20 Art Directions (Anti-Monokultur)

Pilih arah yang benar-benar selaras dengan subjek produk — jangan menjatuhkan semua proyek ke satu gaya:

| # | Art Direction | Ciri Struktural & Permukaan | Domain yang Tepat |
|---|---|---|---|
| 1 | **Editorial Magazine** | Tipografi display berkarakter, kolom asimetris, pemisah garis tipis | Media, berita, laporan riset, esai |
| 2 | **Swiss International** | Grid matematis objektif, sans-serif tegas, palet terukur | Keuangan, hukum, korporat B2B, arsitektur |
| 3 | **Neo-Brutalist** | Garis batas tegas (`1.5–2px`), kontras blok warna berani, jujur struktural | Kampanye kreatif, studio independen, acara budaya |
| 4 | **Japanese Minimalist** | Ruang negatif bermakna (*Ma*), nada bumi tenang, fokus satu objek | Kesehatan, perhotelan butik, kerajinan premium |
| 5 | **Retro-Futurism** | Geometri teknis tajam, aksen fosfor terkendali di atas bidang gelap | Audio/musik, perangkat keras kreatif, gim |
| 6 | **Organic Warmth** | Permukaan krem/batu hangat, sudut lembut terukur, kontras ramah mata | Edukasi, psikologi/klinik ramah pasien, kuliner, F&B |
| 7 | **Industrial Technical** | Indeks bernomor, label monospaced fungsional, tata letak skematik | Cloud infra, IoT, manufaktur, developer CLI |
| 8 | **Art Deco Prestige** | Proporsi simetris anggun, aksen logam hangat, tipografi klasik-modern | Perhotelan bintang lima, jam tangan, busana |
| 9 | **Scandinavian Functional** | Permukaan terang jernih, kayu/abu hangat lembut, keterbacaan tinggi | Ritel rumah tangga, produktivitas keluarga |
| 10 | **Telemetry Dense** | Permukaan gelap fokus data, indikator status semantik + ikon, grafik rapat | SOC keamanan siber, perdagangan real-time, NOC |
| 11 | **Print Archive** | Serif bacaan tajam, latar kertas alami, catatan tepi bernomor | Penerbit buku, perpustakaan, jurnal akademik |
| 12 | **Layered OS Surface** | Satu lapis panel translusen fungsional di atas bidang kerja solid | Aplikasi desktop/produktivitas lintas-platform |
| 13 | **Bauhaus Functional** | Bentuk geometri primer yang menandai fungsi navigasi berbeda | Pendidikan desain, alat kolaborasi visual |
| 14 | **Commerce Showcase** | Media produk tajam mendominasi, harga/varian faktual, alur beli instan | Marketplace, pemesanan makanan, ritel langsung |
| 15 | **Monochrome Type-Led** | Skala dan bobot huruf menjadi pembentuk hierarki utama tanpa ramai warna | Portofolio desain, galeri fotografi, penulisan |
| 16 | **Calm Clinical** | Permukaan bersih bebas bising visual, hierarki jadwal/tindakan jelas | Klinik medis, apotek, rekam kesehatan |
| 17 | **Operational Ledger** | Tabel padat (`4–8px` sel), `tabular-nums` rata kanan, nol dekorasi | Akuntansi, ERP, kasir POS, manajemen gudang |
| 18 | **Guided Step Flow** | Progres bertahap jelas dengan pratinjau hasil langsung di samping input | Onboarding kompleks, pengajuan pajak/asuransi |
| 19 | **Flagship Media** | Ruang lega dramatis, fokus penuh pada rekayasa produk fisik | Otomotif, elektronik konsumen unggulan, properti |
| 20 | **Tactile Utility** | Kontrol pegas responsif `<150ms`, status instan tanpa perpindahan halaman | Kalkulator teknis, konverter, alat kerja harian |

### Contoh Kontras 3 Opsi Saat Arah Visual Belum Ditentukan
Jika harus menawarkan pilihan arah ke pengguna, sodorkan **3 kutub yang berbeda nyata** (bukan 3 kembaran gelap):
- *Contoh Produk Klinik/Reservasi*: **(A) Calm Clinical** (`oura.md` / `cal.md` — terang jernih, fokus slot waktu) vs **(B) Organic Warmth** (`airbnb.md` — hangat, ramah pasien) vs **(C) Swiss Precision** (`wise.md` — grid tegas, kepadatan jadwal staf).
- *Contoh Produk SaaS/Data*: **(A) Crisp Light Ledger** (`stripe.md` / `midday.md`) vs **(B) Editorial Knowledge Workspace** (`claude.md` / `notion.md`) vs **(C) Dark Technical Telemetry** (`tailscale.md` / `linear.app.md`).

---

## 4. Spesifikasi Pola Komponen Produksi

### 4.1 Arsitektur Navigasi Kontekstual (Pilih Sesuai Kedalaman Produk)
Jangan memasang satu jenis header ke semua situs. Pilih pola yang sesuai dengan model mental pengguna:
1. **Focused Content / Task Header** (Landing, Media, Toko, Booking): merek di kiri, 3–5 tujuan domain nyata, dan tepat satu tombol aksi primer kontekstual. Jangan menaruh badge `Cmd+K` palsu pada situs yang tidak berorientasi perintah keyboard.
2. **Operational Sidebar Rail** (ERP, B2B, Admin, Klinik Staf): lebar `240–260px` (dapat dilipat ke ikon + tooltip), dikelompokkan menurut alur kerja domain nyata (mis. `Antrean Pasien`, `Rekam Medis`, `Tagihan` — bukan ember generik tanpa konteks), dengan `aria-current="page"` dan angka antrean `tabular-nums` bila faktual.
3. **Command-Driven Workspace** (DevTools, IDE, Analitik Keyboard-First): bilah kompak dengan pemicu palet perintah (`⌘K` / `Ctrl+K`) yang benar-benar berfungsi penuh dengan navigasi panah dan `Escape`.
4. **Thumb-Zone Mobile Navigation (`< 768px`)**: gunakan **Bottom Tab Bar (3–4 tujuan inti)** setinggi `56–64px` + `env(safe-area-inset-bottom)` untuk aplikasi berulang, atau **Bottom Sheet Drawer** untuk menu sekunder — hindari daftar teks layar penuh yang memutus orientasi pengguna.

### 4.2 Komposisi Tata Letak Pengganti Template Klise
Hindari pola *hero rata-tengah + 3 kartu fitur identik + 4 kotak KPI palsu* yang membuat hero *"biasa saja tapi jadi aneh"* akibat ditambal dekorasi pelangi dan kanvas 3D palsu. Terapkan 4 arketipe hero produksi nyata:
1. **The Interactive Split Engine (Developer Tools, API Gateways, B2B Infrastructure)**:
   - Rasio 55/45 atau 50/50 penyejajaran teks awal (*text-align: start*).
   - Kiri: Display typeface solid tegas + 2 kalimat proposisi nilai riil + 1 tombol aksi solid primer + blok copy perintah instalasi (`$ npx aetherlink@latest` atau `$ docker run ...`).
   - Kanan: **The Living Engine** — komponen kerja operasional nyata (bukan ilustrasi / bukan 3D particle mesh). Misal pada gateway pesan: live WhatsApp QR terminal pairing + live WebSocket JSON event stream (`messages.upsert`, latensi p95 `18ms`).
2. **The Task-First Hero (Fintech, Booking, Travel, Utilitas Kerja)**:
   - Antarmuka tugas langsung menjadi pahlawan paruh atas layar (misal: widget konversi mata uang riil dengan kurs live atau pemilih tanggal & kamar terpadu alih-alih foto dekoratif).
3. **The Editorial Masthead (Media, Riset, Publikasi, AI Naratif)**:
   - Kolom baca proporsional (`60–70ch`), kontras skala serif/sans tajam, ringkasan eksekutif langsung terbaca, dan stempel waktu baca faktual.
4. **Functional Asymmetric Grid (`2:1` / `1:2`)**:
   - Gunakan hanya ketika panel utama memang menampung komponen kerja berdimensi besar dan panel pendamping menampung kontrol sekunder.
5. **4-Level Surface Ladder**:
   - Bedakan bidang lewat nada permukaan halus (`Canvas` → `Surface` dengan garis `1px` atau spasi → `Elevated` dengan bayangan kontak tipis → `Overlay` untuk dialog/sheet), bukan menumpuk bayangan tebal di semua kotak.

### 4.3 Validasi Form, Tabel Data, Dialog & Toast
- **Form UX**: validasi saat `blur`, lalu perbarui instan saat `input` begitu pengguna memperbaiki nilai; hubungkan pesan perbaikan spesifik via `aria-describedby`; aktifkan indikator sibuk (`aria-busy="true"`) saat pengiriman berlangsung.
- **Tabel Data**: teks rata kiri, nominal/angka rata kanan dengan `tabular-nums`, `aria-sort` pada kolom urut, debounce filter `250–300ms`, dan transformasi terstruktur pada layar sempit (kolom identitas lekat atau kartu pasangan label-nilai).
- **Dialog & Toast**: gunakan `<dialog>` dengan *focus trap*, penguncian scroll latar (`overscroll-behavior: contain`), penutupan `Escape`, dan pengembalian fokus ke pemicu. Batasi maksimal 3 toast bersamaan (`aria-live="polite"`), jeda timer saat di-hover/fokus, dan sediakan tombol *Undo* untuk aksi reversibel.

---

## 5. Ergonomi Mobile & Pemeriksaan 3 Lebar Layar

1. **Input & Keyboard Semantik Mobile**: font `<input>`/`<select>`/`<textarea>` minimal `16px`, target sentuh `≥ 44×44px` dengan jeda `≥ 8px`, serta `inputmode` dan `autocomplete` yang sesuai (`numeric`, `decimal`, `tel`, `one-time-code`).
2. **Aksi Geser Aksesibel**: setiap aksi *swipe* wajib memiliki padanan tombol/menu yang dapat diakses keyboard dan pembaca layar.
3. **Pemeriksaan Ketat 3 Lebar Layar (`375px`, `768px`, `1440px`) & Zero Canvas Leak**:
   - *Uji Kebocoran Layar Ponsel 375px (`document.documentElement.scrollWidth <= window.innerWidth`)*:
     - Dilarang `100vw` atau `w-screen` (penyebab #1 scrollbar horizontal samping bocor). Gunakan `w-full`.
     - Dilarang padding horizontal berlebihan: gunakan `px-4 sm:px-6` (bukan `px-12` atau `px-20` di mobile).
     - Seluruh flex/grid child wajib menyertakan `min-w-0` agar pemotongan teks (`truncate`) dan `break-words` berfungsi tanpa mendorong kontainer melebar.
   - *Ukuran Navbar Mobile (Maksimal 64px)*:
     - Header mobile wajib kompak `56px–64px` (`h-14 sm:h-16`).
     - Tautan menu teks desktop disembunyikan di `< 768px` (`hidden md:flex`).
     - Tombol CTA navbar desktop disembunyikan atau diringkas menjadi satu ikon agar tidak menabrak logo di layar sempit.
   - *Disiplin Fluid Heading & Anti-Typo Overflow*:
     - Judul display wajib memakai skala responsif bertahap (`text-2xl sm:text-4xl lg:text-6xl`) atau `clamp()` dan diberi `break-words`.
     - Monospace, URL, token, dan hash wajib `break-all` atau dimasukkan ke dalam wrapper berbatas dengan `overflow-x-auto`.
