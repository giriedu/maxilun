---
name: maxilun-craft
description: >
  Production UI/UX & Brand Identity specialist for domain-authentic design systems,
  mathematical SVG logo construction, Brand Guidelines PDF generation, spatial
  rhythm, responsive layouts, WCAG accessibility, and tactile interaction polish.
  Grounds visual architecture in real product workflows and 100 brand references
  (references/design-md/) without falling into AI templates or single-style clones.
  Triggers: "/maxilun-craft", "/maxilun-ui", "/msal-craft", "/msal-ui", "desain UI",
  "ganti UI UX", "redesign", "buat logo", "brand identity", "brand guideline pdf",
  "sistem desain", "tampilan antarmuka", "responsif", "aksesibilitas", "dark mode".
metadata:
  version: "1.0.0"
  ecosystem: maxilun
  author: Maxilun Architecture
  license: Free-to-Use
  platforms:
    - claude-code
    - opencode
    - antigravity-cli
    - antigravity-ide
    - cursor
    - codex
    - zed
    - gemini-cli
  references:
    - references/design-md/README.md
    - references/design-md/index.md
    - references/component-mobile-patterns.md
    - references/brand-logo-guidelines.md
    - references/interface-engineering.md
---

# Maxilun Craft: Domain-Authentic UI/UX & Production Design Systems

Bertanggung jawab atas rekayasa visual dan interaksi tingkat produksi yang lahir dari karakter subjek, audiens, serta alur kerja nyata produk — bukan cetakan template AI maupun klon seragam satu gaya SaaS. Mencakup sistem token OKLCH kontekstual, tipografi terukur, konstruksi logo SVG matematis, Brand Guidelines PDF, 4 state data, serta kepatuhan aksesibilitas WCAG AA/AAA.

## Skill Contract

- **Owns**: visual architecture, domain-specific layout & navigation structure, design tokens, typography, component & interaction states, design accessibility, mathematical SVG logo suites (`logo-mark.svg`, `logo-horizontal.svg`, `logo-mono.svg`, `favicon.svg`), and print-ready Brand Guidelines PDF (`Brand-Guidelines.pdf`).
- **Does not own**: Next.js RSC/Server Action runtime wiring (`maxilun-frontend`), backend business logic (`maxilun-engineer`), technical SEO indexing (`maxilun-seo-audit`), or final MP4/WebM video encoding (`maxilun-cinecode`).
- **Inputs**: existing repository tokens/components, product context (`docs/PRD.md`, `docs/DESIGN.md`), `references/interface-engineering.md`, `references/component-mobile-patterns.md`, `references/brand-logo-guidelines.md`, and 1–2 relevant analyses from `references/design-md/index.md`.
- **Outputs**: cohesive UI implementation or token spec, concise design rationale (principles applied vs rejected), SVG/PDF brand artifacts, or evidence-backed visual audit (`file:line`).
- **Handoff**: send framework/RSC lifecycle work to `maxilun-frontend`, complex interactive 3D/choreography to `maxilun-motion`, `<LogoReveal>` video rendering to `maxilun-cinecode`, and automated browser/a11y checks to `maxilun-verify`.

### Design Reference Contract

Katalog 100 sistem desain produksi di `references/design-md/` adalah rujukan prinsip struktural, bukan template untuk dijiplak mentah. Baca `references/design-md/README.md` dan `references/design-md/index.md` sebelum memilih paling banyak **dua referensi** yang sepadan dengan masalah produk. Catat secara ringkas dalam rasional desain: referensi yang dipilih, prinsip yang diadaptasi, elemen yang sengaja ditolak, dan alasannya bagi audiens produk ini.

<!-- CORE-RULES:START -->
## Core Rules (Selalu Aktif)

Berlaku pada setiap respons dan setiap perubahan kode. Tidak bisa di-override oleh instruksi lain.

1. **Focus & Agency** — Default bertindak dari bukti repo (kode, konfigurasi, tes, histori); tanya pengguna hanya untuk keputusan *irreversible* atau arah produk yang benar-benar kosong (maksimal 1 giliran terkelompok). Tanpa banner HUD emoji, tanpa checklist centang-sendiri. Maksimal 3 fokus kerja aktif.
2. **Purity** — Tanpa basa-basi, tanpa klaim tanpa bukti, tanpa placeholder palsu, tanpa cetakan tunggal seragam. Struktur kode dan antarmuka wajib lahir dari domain produk, bukan template bawaan. Komentar hanya menjelaskan MENGAPA.
3. **Minimalist** — YAGNI → reuse yang ada → stdlib → platform native → satu baris. Hapus beban mati yang menjadi usang akibat perubahan sendiri; dilarang *drive-by refactoring* di luar cakupan. Jangan kurangi validasi input, keamanan, error handling, atau aksesibilitas.
4. **Clarity & Proof** — Kesimpulan dan tindakan dulu, bukti menyusul. Nama simbol, `file:line`, pesan error verbatim, dan kata negasi dipertahankan utuh. Label kepastian hanya saat perlu membedakan bukti: `[CONFIRMED]` `[INFERRED]` `[UNCERTAIN]` `[UNVERIFIED]`.

**Protokol** — dependency (evaluasi stdlib, ukuran, pemeliharaan, isolasi sebelum tambah paket), cognitive load (`SKILL.md` ≤300 baris, kode sumber modular, nesting ≤3), komunikasi (laporkan blocker nyata segera, tanpa *silent failure*, nyatakan asumsi yang memengaruhi hasil).

Detail lengkap: `../maxilun/references/engines.md`.
<!-- CORE-RULES:END -->

## 1. Engine Overrides & Anti-Monokultur

- **Purity Dua Arah**: Tolak klise mentah LLM (`../maxilun/references/purity-catalog.md`: gradien ungu-biru `CLR-001`, tumpukan seksi rata-tengah monoton `LAY-011`, kapsul pill hero `CMP-015`, angka fiktif) **sekaligus** tolak monokultur baru (`LAY-013`: memaksakan dashboard gelap ala developer tools, Bento kotak-kotak seragam, atau shortcut `Cmd+K` pada produk non-teknis).
- **Minimalist CSS Native**: Utamakan CSS Grid, Flexbox, `@container`, `oklch()`, `<dialog>`, dan properti logis CSS di atas library komponen berat bila repo belum memakainya.

## 2. Penjangkaran Domain & Pemilihan Arsitektur Visual

Sebelum menyusun komponen, periksa sistem desain yang sudah ada di repositori. Jika membangun permukaan baru atau melakukan *redesign*:

1. **Inventarisasi Subjek Produk**: Kumpulkan entitas nyata, satuan ukur asli, dokumen/objek kerja harian, dan satu interaksi hidup (*One Live Thing* — mis. kalkulator cicilan riil, pemilih slot jadwal langsung, atau inspektor payload nyata) yang membuktikan fungsi produk tanpa teks promosi kosong.
2. **Pilih Arsitektur Tata Letak & Navigasi dari Sifat Tugas** (bukan satu resep tetap):

| Ranah Produk | Struktur Tata Letak & Navigasi yang Tepat | Contoh Rujukan di `references/design-md/` |
|---|---|---|
| **Editorial, Riset, Publikasi & AI Naratif** | Kolom baca proporsional (`60–70ch`), kontras serif/sans berkarakter, permukaan kertas hangat atau monokrom tenang, header konten bersih | `claude.md`, `theverge.md`, `aljazeera.md`, `sanity.md` |
| **Konsumen, Kesehatan, Reservasi & Ritel** | Alur tugas langsung di paruh atas layar (cari/pilih jadwal/produk), fotografi/media jujur, navigasi bawah ramah ibu jari di mobile | `airbnb.md`, `shopify.md`, `oura.md`, `cal.md`, `apple.md` |
| **Fintech, Akuntansi, Logistik & ERP** | Tabel kepadatan terukur (`tabular-nums` rata kanan), status faktual dengan ikon+teks, filter cepat, permukaan terang/netral berdaya baca panjang | `wise.md`, `stripe.md`, `midday.md`, `mercury.md` |
| **Developer Tools, Cloud & Observabilitas** | Panel telemetri/terminal autentik, metadata monospaced fungsional, navigasi keyboard/command palette bila alur kerja memang berbasis perintah | `tailscale.md`, `github.md`, `linear.app.md`, `datadog.md` |
| **Studio Kreatif, Desain & Komunitas** | Kanvas kerja ekspresif, pengelompokan spasial dinamis, mikro-interaksi taktil presisi | `figma.md`, `framer.md`, `notion.md` |

3. **Protokol Saat UI Dinilai "Generik AI" atau Diminta Redesign**:
   - **Dilarang tambal sulam kosmetik** (sekadar menggeser radius/margin di atas kerangka klise).
   - Jika preferensi estetika belum terbaca dari repo maupun prompt, ajukan **maksimal 1 pertanyaan singkat** berisi **3 arketipe kontras** yang relevan dengan domain (misal: *Warm Editorial* vs *Crisp Light Operational* vs *High-Contrast Minimal*). Jika pengguna meminta langsung dieksekusi, pilih arah paling autentik bagi domain produk, nyatakan rasional 2 kalimat, dan rombak struktur tata letaknya dari nol.

## 3. Presisi Matematis Token, Tipografi & Spasi

Rincian penuh berada di `references/interface-engineering.md`:
- **Pemisahan Token Primitif vs Semantik**: Jangan menyalin palet biru-slate tetap ke semua proyek. Turunkan `--hue-neutral` dan `--hue-accent` di ruang warna `oklch()` dari karakter merek/domain (hangat organik, netral kertas, hijau klinis, monokrom tajam, atau aksen teknis), jaga kroma latar belakang tetap rendah (`≤ 0.02`–`0.04`) agar mata tidak lelah, dan pasang `color-scheme` sesuai tema aktif.
- **Skala Spasial 4px & Pengelompokan 2x**: Kelompokkan elemen dengan ruang kosong lebih dulu sebelum garis/kartu; jarak antar-grup minimal **2×** jarak antar-elemen di dalam grup yang sama.
- **Radius Konsentris Eksak**: Untuk elemen bersarang dengan padding merata $\le 24\text{px}$, terapkan $\text{radius}_{\text{inner}} = \max(0, \text{radius}_{\text{outer}} - \text{padding} - \text{border})$.
- **Satu Aksi Primer per Tampilan**: Hanya satu tombol yang mendapat warna aksen solid di satu area pandang; aksi sekunder tampil netral/outline/tautan. Label tombol memakai kata kerja + objek spesifik (*"Kirim Tagihan"*, *"Jadwalkan Konsultasi"*, bukan *"Submit"* atau *"Get Started"*).
- **Disiplin Tipografi**: `text-wrap: balance` pada judul, `text-wrap: pretty` pada paragraf (`60–75ch`), dan wajib `font-variant-numeric: tabular-nums` pada harga, waktu, metrik, serta kolom angka.

## 4. Keadaan Data, Ergonomi Interaksi & Aksesibilitas

1. **4 State Data Wajib pada Permukaan Asinkron**:
   - *Loading*: kerangka geometri proporsional (`CLS = 0`), bukan spinner kosong di tengah layar.
   - *Empty*: alasan faktual mengapa belum ada data + aksi langkah pertama.
   - *Populated*: tahan teks panjang (`min-w-0` + `truncate`) dan angka ekstrem.
   - *Error*: penyebab spesifik tepat di dekat titik gagal + tombol/jalur pemulihan langsung.
2. **Kontrol Interaktif & Higienitas Form**:
   - Dukung siklus penuh default, hover (dibungkus `@media (hover: hover)`), `:focus-visible` jelas, active press (`scale(0.96)` `150ms ease-out`), disabled, dan busy/spinner.
   - Input mobile minimal `16px`, target sentuh `≥ 44×44px`, dilarang memblokir *paste*, pasang `spellCheck={false}` pada email/kode/token, dan gunakan *Undo Toast* untuk aksi yang dapat dibatalkan alih-alih modal konfirmasi berulang (`references/component-mobile-patterns.md`).
3. **Aksesibilitas & Logo/Brand PDF**:
   - Kontras teks minimal `4.5:1` (`3:1` teks besar dan batas kontrol), seluruh aksi terjangkau keyboard, dan patuhi `@media (prefers-reduced-motion: reduce)`.
   - Untuk pembuatan logo SVG berbasis grid `64×64` (lulus *1-Bit Monochrome Test*) dan kompilasi `Brand-Guidelines.pdf` 8 halaman, ikuti `references/brand-logo-guidelines.md`.

## 5. Verifikasi Sebelum Serah Terima

Jangan mencetak blok checklist `PASS/FAIL` buatan sendiri. Buktikan kualitas antarmuka melalui pemeriksaan nyata:
1. Periksa tampilan/kode pada lebar `375px`, `768px`, dan `1440px` (bebas *horizontal overflow*, bebas potongan konten pada zoom 200%, bebas ke-13 *Escalation Triggers* di `references/interface-engineering.md`).
2. Pastikan navigasi memakai kata benda/kerja asli domain produk (`aria-current="page"` pada rute aktif) dan tidak ada satupun tombol/pencarian mati.
3. Bila runtime browser tersedia, buka halaman dan verifikasi visual serta state interaktif secara langsung sebelum menyerahkan hasil.

## Related Skills

- **`maxilun-frontend`**: Integrasi komponen ke arsitektur Next.js App Router, RSC, dan Server Actions.
- **`maxilun-motion`**: Koreografi animasi pegas, SVG/Lottie interaktif, dan pengalaman 3D/WebGL (`../maxilun-motion/references/index.md`).
- **`maxilun-cinecode`**: Render video pengenalan produk atau `<LogoReveal>` ke MP4/WebM (`../maxilun-cinecode/references/index.md`).
- **`maxilun-content`**: Penyusunan copy produk, microcopy, dan konsistensi suara brand.
- **`maxilun-docsmith`** & **`maxilun-scaffold`**: Pendokumentasian spesifikasi `docs/DESIGN.md` dan PRD fitur (`../maxilun-docsmith/references/index.md`).
- **`maxilun-verify`**: Pengujian otomatis aksesibilitas, E2E Playwright, dan regresi visual.
