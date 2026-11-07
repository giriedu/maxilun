# Maxilun Awwwards-Standard Craft Engine

<!-- metadata:
  version: "1.1.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine & Awwwards Jury Rubric Synthesis"
-->

Panduan rekayasa visual dan interaksi tingkat agensi (*agency-grade*) yang mengodifikasi sistem penilaian juri Awwwards (Site of the Day / Developer Award / Mobile Excellence) menjadi metode perancangan deterministik. Target: skor juri $\ge 7.0/10$.

---

## 1. Realitas Pembobotan Juri Awwwards (Memorize This)

Awwwards bukan gaya grafis—Awwwards adalah sistem penilaian kuantitatif terbobot:

| Kriteria | Bobot | Apa yang Sebenarnya Diukur Juri |
|---|---|---|
| **Design** | **40%** | Hierarki visual, disiplin tipografi, intensionalitas warna, ritme spasi, konsistensi detail pada *seluruh* halaman. |
| **Usability** | **30%** | Kecepatan render, kejelasan navigasi, ergonomi mobile, aksesibilitas, Core Web Vitals ($INP < 100\text{ms}, CLS < 0.05$). |
| **Creativity** | **20%** | Konsep orisinal, tepat **satu momen khas (*One Signature Moment*)** yang tak terlupakan. |
| **Content** | **10%** | Salinan teks asli, fotografi nyata, integrasi visual yang selaras dengan pesan subjek. |

> **Konsekuensi Kritis yang Mengendalikan Setiap Keputusan:**  
> 1. **Design (40%) + Creativity (20%) = 60%, tetapi Usability (30%) sendirian dapat membunuh skor Anda.** Situs yang memukau tetapi lambat dibuka (>3s) atau rusak pada iPhone tidak akan pernah mencapai skor 7.0. Usability adalah batasan desain awal, bukan fase QA di akhir.  
> 2. **Wajib tepat SATU Signature Moment, bukan dua puluh efek berserakan.** Efek yang tersebar acak terbaca sebagai kepanikan visual dan memotong nilai Design sekaligus Usability.

---

## 2. Protokol Satu Momen Khas (The Signature Moment Protocol)

Sebelum menulis baris kode pertama, rumuskan spesifikasi Momen Khas secara tertulis:

```markdown
### Signature Moment Specification
- **Nama Momen**: [Misal: Living Socket Inspector / Asymmetric Canvas Orbit]
- **Pemicu (Trigger)**: [Scroll progress / First load sequence / Hover pointer / Drag]
- **Fase Gerak**: Status A -> Transisi Terkoordinasi -> Status B (dengan timing eksak)
- **Durasi & Easing**: [300ms–800ms, kurva cubic-bezier seragam]
- **Interaksi Pengguna**: Apa yang dikendalikan pengguna dan bagaimana mereka menemukannya
- **Versi Layar Sentuh Mobile**: Adaptasi sentuhan langsung (swipe/tap), bukan versi yang dimatikan
- **Versi prefers-reduced-motion**: Transisi instan tanpa pergerakan yang memusingkan
- **Tiga Detik Pertama**: Apa yang langsung terbaca jelas sebelum pengguna mulai berinteraksi
```

---

## 3. Daftar Detail Mikro Bernilai Tinggi (The High-Craft Micro-Details)

Jurors mendaftarkan kualitas pengerjaan (*craftsmanship*) secara bawah sadar melalui detail-detail kecil:

### 3.1 Garis Bawah Tautan Berbalik Arah (ScaleX Flip Underline)
Garis bawah animasi 6-baris CSS yang langsung menandakan kualitas studio:
```css
.craft-link {
  position: relative;
  text-decoration: none;
}
.craft-link::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -0.15em;
  width: 100%;
  height: 1px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.craft-link:hover::after,
.craft-link:focus-visible::after {
  transform: scaleX(1);
  transform-origin: left;
}
```

### 3.2 Zoom Gambar di Dalam Masking Bersih
Hindari filter warna murahan; gunakan pembesaran halus di dalam kontainer `overflow: hidden`:
```css
.craft-media-frame {
  overflow: hidden;
  border-radius: var(--radius-md);
}
.craft-media-frame img,
.craft-media-frame video {
  transition: transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
  will-change: transform;
}
.craft-media-frame:hover img,
.craft-media-frame:hover video {
  transform: scale(1.05);
}
```

### 3.3 Penataan Warna Seleksi Teks Global
```css
::selection {
  background: var(--color-accent-solid);
  color: var(--color-accent-contrast);
}
```

### 3.4 Batas Konsistensi Halaman Dalam (Zero Homepage-Only Design)
Juri Awwwards selalu mengeklik tautan navigasi ke halaman dalam. Halaman dokumentasi, detail produk, atau 404 wajib dibangun dengan sistem token, tipografi, dan margin yang identik dengan beranda.

---

## 4. Evaluasi Mandiri Pra-Rilis Juri Awwwards (Self-Scoring Audit)

Sebelum menyerahkan situs, hitung estimasi skor juri secara mandiri:

| Dimensi Evaluasi | Indikator Lolos Skor $\ge 7.0$ | Gejala Pelanggaran (Membatasi Skor $< 6.5$) |
|---|---|---|
| **Design (40%)** | Grid terkalibrasi, skala tipografi berbasis peran, 1 aksi primer, hairline border 1px netral, foto/copy autentik. | Template smell, gradient pelangi pada judul, border neon menyala, jarak vertikal acak. |
| **Usability (30%)** | $LCP < 1.5\text{s}$, $INP < 100\text{ms}$, bebas kebocoran scroll 375px, keyboard fokus ring terlihat, navbar $\le 64\text{px}$. | Scroll-jacking membeku, menu mobile meluap, font input $<16\text{px}$, link mati. |
| **Creativity (20%)** | Satu signature moment yang kuat, artefak domain hidup (*The Living Engine*), mikro-interaksi taktil. | 20 efek animasi berserakan, kanvas 3D partikel fiktif tanpa kaitan fungsi, kapsul pill klise. |
| **Content (10%)** | Copywriting berorientasi tugas nyata, angka metrik terverifikasi, nol teks lorem ipsum atau emoji murahan. | Slogan brosur kosong (*"Revolutionize Your Experience"*), teks putus di tepi canvas, emoji tombol. |
