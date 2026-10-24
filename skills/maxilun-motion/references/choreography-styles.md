# Motion DNA, Style Signatures, Storyboard Hooks & Camera/Audio Choreography

Gunakan referensi ini saat merancang arah gerak (*motion direction*), mengekstrak *Motion DNA* dari token `maxilun-craft`, menyusun storyboard opener/explainer, atau menyerahkan spesifikasi koreografi frame ke `maxilun-cinecode`.

---

## 1. Pipeline Brand DNA → Motion DNA (Terintegrasi `maxilun-craft`)

Ambil token visual dari proyek atau pilih 1–2 referensi yang setara dari `../maxilun-craft/references/design-md/index.md`, lalu petakan ke parameter fisika gerak:

| Token `maxilun-craft` | Parameter `maxilun-motion` | Aturan Konversi Produksi |
|---|---|---|
| `--space-2` (`8px`) | `timing.fast` (`80ms - 120ms` / `3-4 frames @30fps`) | Micro-feedback (hover, focus, toggle) |
| `--space-4` (`16px`) | `timing.normal` (`160ms - 220ms` / `5-7 frames @30fps`) | Transisi state komponen, drawer, dropdown |
| `--space-8` (`32px`) | `timing.slow` (`320ms - 450ms` / `10-14 frames @30fps`) | Transisi antar-scene, reveal hero, modal |
| `typography.weight >= 700` | `kineticMode: "punch"` (`stiffness: 180, damping: 16`) | Headline tegas (misal gaya `stripe.md`, `nike.md`, `linear.app.md`) |
| `typography.weight <= 400` | `kineticMode: "editorial-glide"` (`stiffness: 100, damping: 20`) | Tipografi editorial halus (misal gaya `apple.md`, `wired.md`) |
| `borderRadius <= 4px` | `curvature: "architectural-snap"` (zero overshoot, `damping >= 22`) | Presisi teknikal, grid ketat |
| `borderRadius >= 12px` | `curvature: "elastic-spring"` (`stiffness: 130, damping: 14`) | Consumer app yang ramah dan taktil |

### Format Profil Motion DNA (`motion-dna.json`)
```json
{
  "referenceSource": "../maxilun-craft/references/design-md/linear.app.md",
  "motionPersonality": "precision-kinetic",
  "timingMs": { "fast": 90, "normal": 180, "slow": 340, "dramatic": 600 },
  "framesAt30Fps": { "fast": 3, "normal": 6, "slow": 10, "dramatic": 18 },
  "springDefaults": { "stiffness": 170, "damping": 19, "mass": 1 },
  "accentColor": "oklch(58% 0.18 255)",
  "kineticMode": "punch",
  "reducedMotionVariant": "opacity-crossfade-120ms"
}
```

---

## 2. Matriks 14 Style Signature Motion

Pilih **tepat satu** signature utama agar gerakan di seluruh halaman atau video konsisten (tidak menjadi *motion soup*):

| # | Style Signature | Karakteristik Фиsika & Easing | Cocok Untuk Domain | Referensi `design-md` Terdekat |
|---|---|---|---|---|
| 1 | **Kinetic Minimal** | Snap-to-grid, zero overshoot (`damping: 24`), aksen monokrom + 1 warna semantik | B2B SaaS, Fintech, Issue Tracker | `linear.app.md`, `vercel.md`, `mercury.md` |
| 2 | **Fluid Organic** | Kurva kontinu halus, morphing organik, tanpa hard cut | Wellness, Consumer Lifestyle, Health | `oura.md`, `airbnb.md` |
| 3 | **Architectural Depth** | Bidang kedalaman paralaks terukur, garis struktural menggambar grid (`Trace`) | Arsitektur, Enterprise Infra, Hardware | `apple.md`, `spacex.md`, `dji.md` |
| 4 | **Tactile Card & Craft** | Lipatan bertahap, bayangan dinamis saat diangkat, pegas responsif | Edukasi, Kolaborasi Visual, Workspace | `notion.md`, `figma.md`, `miro.md` |
| 5 | **Data Flow Cascade** | Aliran partikel sepanjang jalur SVG (`MotionPath`), aktivasi node berurutan | Observability, Analytics, Database, AI | `sentry.md`, `posthog.md`, `clickhouse.md`, `supabase.md` |
| 6 | **Editorial Crisp** | Reveal per baris dengan mask tajam, transisi kontras tinggi | Media, Jurnalisme, Dokumentasi | `wired.md`, `theverge.md`, `mintlify.md` |
| 7 | **Financial Precision** | Angka `tabular-nums` berputar presisi (*odometer*), grafik tumbuh dengan spring | Payment Gateway, Crypto, Perbankan | `stripe.md`, `wise.md`, `revolut.md` |
| 8 | **High-Velocity Sport** | Cut cepat pada beat, tipografi miring/tebal masuk dengan momentum tinggi | Otomotif, Olahraga, Gaming | `nike.md`, `ferrari.md`, `bmw-m.md`, `playstation.md` |
| 9 | **Command-First Micro** | Feedback `< 100ms`, keyboard highlight instan, list morphing tanpa delay | IDE, CLI, Developer Productivity | `raycast.md`, `cursor.md`, `warp.md`, `superhuman.md` |
| 10 | **Cinematic Spotlight** | Dolly lambat, pencahayaan terfokus pada subjek tunggal, kontras gelap | Luxury, Peluncuran Produk Flagship | `bugatti.md`, `lamborghini.md` |
| 11 | **Brutalist Slam** | Hard cut 0ms dikombinasikan dengan scale slam ber-kontras ekstrem | Agensi Kreatif, Kampanye Event | `framer.md`, `webflow.md` |
| 12 | **Commerce Showcase** | Transisi produk mulus, zoom detail tekstur, badge harga jelas | E-Commerce, Retail Modern | `shopify.md`, `starbucks.md` |
| 13 | **Narrative Scroll** | Timeline terikat posisi scroll (`ScrollTimeline`), subjek persisten antar-bab | Landing Page Produk, Laporan Tahunan | `apple.md`, `stripe.md` |
| 14 | **Audio-Synced Pulse** | Transisi dan skala elemen terkunci pada BPM/transien audio | Musik, Promo Video Sosial, Teaser | `spotify.md` |

---

## 3. Katalog 22 Konsep Opener & Promo Hook (3–5 Detik Pertama)

### A. Opener (Frame 0 – Frame 90 @ 30fps)
1. **Logo Assembly** — Elemen geometri menyatu ke titik tengah menggunakan simulasi spring (`stiffness: 150, damping: 15`).
2. **Type Scramble Decode** — Karakter acak monospace terdekode menjadi judul utama dalam 24 frame.
3. **Portal Iris Wipe** — Mask lingkaran membesar dari elemen fokus utama membuka scene.
4. **Depth Plane Plunge** — Kamera bergerak maju (`dolly`) menembus 3 lapisan UI transparan menuju layar inti.
5. **Signal Lock** — Garis gelombang/data acak terkunci menjadi grafik metrik yang tajam.
6. **Grid Construct** — Garis hairline `1px` menggambar struktur tata letak sebelum konten muncul (`Trace` + `Reveal`).
7. **Light Sweep** — Kilau cahaya terarah menyapu kontur produk di atas permukaan gelap.
8. **Morph Entry** — Ikon masalah berubah bentuk (`SVG path morph`) menjadi komponen solusi.
9. **Stagger Cascade** — Baris data atau kartu fitur aktif berurutan dengan jeda `3 frame` (`100ms`).
10. **Metric Counter Snap** — Angka KPI berputar cepat dari baseline lama ke angka target baru.

### B. Hook Narasi & Penjelas (Explainer Beats)
11. **Problem Friction Split** — Layar terbelah dua: sisi kiri menampilkan alur manual yang lambat (merah redup), sisi kanan menampilkan alur otomatis 1-klik (hijau tajam).
12. **Before/After Slider Sweep** — Garis vertikal menyapu layar mengubah tampilan lama menjadi sistem baru.
13. **Architecture Node Activation** — Request bergerak dari node User → API → DB dengan indikator latensi `ms` nyata.
14. **Code-to-UI Live Compile** — Baris kode diketik di kiri (45 frame), langsung me-render komponen produksi di kanan.
15. **Feature Unfold** — Kartu ringkas membuka lapisan detail secara spasial tanpa berpindah konteks.
16. **Timeline March** — Stepper progres berjalan mendorong pergantian scene.
17. **Comparison Scale** — Grafik batang horizontal tumbuh berdampingan membandingkan beban waktu/biaya.
18. **Interactive Cursor Guided Tour** — Kursor vektor bergerak dengan kurva alami, menekan tombol, dan memicu toast sukses.
19. **Security Shield Lock** — Payload masuk divalidasi dan dikunci dengan indikator enkripsi/status hijau.
20. **Social Proof Grid** — Kutipan metrik terverifikasi muncul bergantian dengan ritme tenang.
21. **CTA Magnetic Focus** — Seluruh elemen sekunder meredup (`opacity: 0.35`) sementara tombol aksi utama mendapat fokus kontras penuh.
22. **Looping Seamless Outro** — Frame terakhir kembali menyambung ke komposisi frame 0 untuk pemutaran berulang di media sosial.

---

## 4. Sistem Kamera, Text Kinetics & Audio Reactivity

### 4.1 Kamera Virtual (Browser 3D / Canvas & `maxilun-cinecode`)
- **Aturan Anti-Mual (Motion Sickness Guard)**: Batasi maksimal **1 jenis gerakan kamera** pada satu waktu (misal: `dolly` saja atau `pan` saja; jangan menggabungkan `orbit + tilt + shake`).
- **Rack Focus**: Gunakan blur kedalaman hanya untuk memindahkan perhatian penonton dari latar ke komponen aktif (`filter: blur(0px)` vs `blur(4px)`).

### 4.2 Text Kinetics (Tipografi Bergerak)
- **Granularitas**:
  - *Per-Character*: Hanya untuk judul pendek (`<= 4 kata`, misal angka atau kode).
  - *Per-Word*: Untuk headline (`5 - 10 kata`) dengan stagger `40ms` (`1-2 frame`).
  - *Per-Line*: Untuk subheadline atau kalimat penjelas agar mata pembaca tidak lelah.
- **Invarian Aksesibilitas**: Teks di dalam DOM harus tetap utuh untuk screen reader (`aria-label` pada induk jika huruf dipecah ke dalam `<span>` individual).

### 4.3 Sinkronisasi Audio & Beat Grid
- Hitung durasi frame per ketukan (beat) untuk sinkronisasi dengan `maxilun-cinecode`:
  $$\text{Frames per Beat} = \text{round}\left(\frac{\text{FPS} \times 60}{\text{BPM}}\right)$$
  *(Contoh: pada `30 FPS` dan musik `120 BPM`, 1 ketukan = `15 frame`, 1 bar (4 ketukan) = `60 frame` / `2 detik`)*
- Tempatkan semua transisi scene utama pada kelipatan bar (`frame 0, 60, 120, 180, ...`) agar potongan visual terasa menyatu dengan ritme audio.
