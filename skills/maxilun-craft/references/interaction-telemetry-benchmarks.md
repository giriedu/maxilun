# Interaction Telemetry Benchmarks: Quantitative UX Instrumentation

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine"
-->

Panduan pengukuran kuantitatif kinerja pengalaman pengguna (*interaction telemetry benchmarks*). Kualitas desain tidak dinilai hanya dari estetika visual, melainkan melalui bukti telemetri terukur pada latensi interaksi, stabilitas tata letak, dan efisiensi penyelesaian tugas.

---

## 1. Ambang Batas Web Vitals (Frontend Telemetry)

Setiap implementasi antarmuka berbasis web wajib mematuhi batas metrik inti berikut:

| Metrik | Nama Parameter | Target Kinerja | Mekanisme Penegakan di Kode |
|---|---|---|---|
| **INP** | *Interaction to Next Paint* | $\le 200\text{ms}$ | Hindari komputasi berat di event handler; gunakan `startTransition` di React untuk pembaruan non-mendesak. |
| **CLS** | *Cumulative Layout Shift* | **$= 0$ (Nol Mutlak)** | Kunci ukuran elemen gambar dan wadah dinamis menggunakan `aspect-ratio` atau dimensi eksplisit; pakai skeleton proporsional 1:1. |
| **LCP** | *Largest Contentful Paint* | $\le 2.5\text{s}$ | Utamakan pemuatan font lokal dan kompresi media modern (AVIF/WebP) dengan atribut `fetchpriority="high"`. |
| **FID/TBT** | *Total Blocking Time* | $\le 150\text{ms}$ | Pecah bundle JavaScript berukuran besar dengan *code splitting* dan minimalkan eksekusi script pihak ketiga. |

---

## 2. Anggaran Frame Perangkat Bergerak (Mobile Frame Budget)

Pada aplikasi native iOS dan Android:

1. **Target 60 FPS / 120 FPS ProMotion**:
   - Batas waktu render satu frame pada layar $60\text{Hz}$ adalah maksimal **$16.6\text{ms}$**.
   - Batas waktu render satu frame pada layar $120\text{Hz}$ (ProMotion / High Refresh Rate) adalah maksimal **$8.3\text{ms}$**.
2. **Isolasi UI Thread**:
   - Parsing JSON berukuran besar, kueri database lokal, dan dekripsi berkas wajib berjalan di luar main thread (*background worker* / coroutine IO / Swift concurrency Task).
   - Indikator kegagalan frame (*jank* atau frame drop) saat daftar digulir cepat wajib bernilai nol.

---

## 3. Metrik Efisiensi Interaksi Pengguna (Task Telemetry)

Ukur keberhasilan alur desain antarmuka menggunakan empat indikator kuantitatif:

1. **Tingkat Keberhasilan Tugas (*Task Completion Rate* / TCR)**:
   - Target $\ge 90\%$ dari pengguna yang memulai alur tugas berhasil menyelesaikan konfirmasi akhir tanpa mengalami kebuntuan atau galat berulang.
2. **Waktu Penyelesaian Tugas (*Time-To-Task* / TTT)**:
   - Bandingkan durasi waktu yang dibutuhkan pengguna untuk menyelesaikan formulir atau pemesanan sebelum dan sesudah perubahan desain. Redesign dinilai berhasil jika TTT terpangkas minimal 20%.
3. **Kecepatan Pemulihan Galat (*Error Recovery Velocity*)**:
   - Waktu rata-rata yang dibutuhkan pengguna dari saat menerima pesan galat hingga berhasil memperbaiki input dan melanjutkan proses (target $\le 10$ detik berkat pesan pemulihan inline yang jelas).
4. **Rasio Pembatalan Formulir (*Form Drop-off Rate*)**:
   - Pantau titik bidang formulir mana yang paling sering ditinggalkan pengguna. Bidang yang memiliki drop-off tinggi wajib dievaluasi untuk dihapus atau disederhanakan.
