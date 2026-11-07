# Maxilun Well-Architected Framework (WAF) & Solution Discovery Playbook

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-architect/SKILL.md"
  origin: "Maxilun Architect Engine"
-->

Panduan perancangan arsitektur sistem holistik, protokol discovery kebutuhan bebas bias, resolusi kontradiksi teknis, dan evaluasi 6 pilar arsitektur rekayasa perangkat lunak.

---

## 1. Protokol Solution Discovery & Anti-Premature Design

Salah satu penyebab utama kegagalan arsitektur adalah melompat langsung ke pemilihan tumpukan teknologi (*technology stack*), alat, atau pemecahan layanan sebelum memahami karakteristik beban dan kendala domain.

### 1.1 Pemisahan Fase yang Ketat (*Strict Phase Separation*)

```
┌────────────────────────────────────────────────────────────────────────┐
│ Fase 1: Requirements Discovery & Trade-off Resolution                  │
│ (Fungsional, Non-Fungsional, Kondisi Eksisting, Resolusi Kontradiksi)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Persyaratan disepakati & bebas kontradiksi
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Fase 2: Dekomposisi Sistem & Arsitektur Solusi (6 Pilar WAF)          │
│ (Komponen Logis, Batas Modul, Kontrak API, Pilihan Teknologi)          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Rencana arsitektur divalidasi
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Fase 3: Validasi Solusi (Pre-Deployment Dry-Run & Runtime Checks)       │
│ (Topologi Statis, Policy Check, Canary Routing, Verification Script)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Bukti verifikasi sah
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Fase 4: Finalisasi Artefak ADR & Handoff Spesialis                     │
│ (ADR formal, OpenAPI 3.1, Fitness Functions di CI)                     │
└────────────────────────────────────────────────────────────────────────┘
```

**Aturan Emas**: Pada Fase 1 (Discovery), **DILARANG KERAS** merekomendasikan tumpukan produk, vendor cloud tertentu, atau rancangan mikroservis. Fokus sepenuhnya pada penggalian fakta:
1. **Persyaratan Fungsional**: Alur bisnis kritis, entitas domain inti, pemangku kepentingan, dan mutasi data utama.
2. **Persyaratan Non-Fungsional**:
   - *Ketersediaan & SLA*: Target uptime (99.9% vs 99.99%), target RTO (*Recovery Time Objective*) dan RPO (*Recovery Point Objective*).
   - *Latensi & Throughput*: Latensi batas atas $p95$/$p99$, estimasi RPS normal dan beban puncak (*sustained peak*).
   - *Keamanan & Kepatuhan*: Batas privasi data (GDPR/UU PDP, PCI-DSS), model tenant (multi-tenant shared vs isolated).
   - *Amplop Biaya*: Batasan anggaran komputasi, storage, dan tenaga operasional.
3. **Kondisi Eksisting (Brownfield)**: Infrastruktur yang sudah berjalan, bahasa pemrograman tim, dan basis data aktif.
4. **Dependensi Eksternal**: Layanan pihak ketiga, API mitra, dan karakteristik latensi/keandalannya.

---

## 2. Resolusi Ambiguitas & Kontradiksi Teknis

Ketika persyaratan pengguna mengandung tujuan yang saling bertentangan secara fundamental (misalnya: isolasi jaringan zero-trust tanpa akses publik sama sekali vs kebutuhan webhook real-time dari payment gateway publik; atau konsistensi ACID multi-region terdistribusi vs latensi tulis sub-milidetik):

1. **Identifikasi Kontradiksi Secara Eksplisit**: Sebutkan dua atau lebih persyaratan yang saling bertentangan secara teknis.
2. **Jelaskan Mengapa Tidak Dapat Terpenuhi Bersamaan**: Paparkan batas hukum fisika komputasi (misal Teorema CAP, batas kecepatan propagasi jaringan, atau trade-off keamanan).
3. **Sajikan Opsi Trade-off Terukur**:
   - Berikan maksimal 2–3 opsi kontras yang realistis beserta risiko masing-masing.
   - Sertakan **1 rekomendasi tegas** berlandaskan prinsip *Safety* dan *Simplicity*.
   - Minta persetujuan pengguna (Keputusan Type 1) sebelum melanjutkan ke perancangan struktur.

---

## 3. Enam Pilar Maxilun Well-Architected Framework (WAF)

Evaluasi setiap perancangan arsitektur terhadap 6 pilar rekayasa berikut:

### Pilar 1: Reliability & Fault Tolerance (Keandalan & Ketahanan)
- **Graceful Degradation**: Saat dependensi hilir (database sekunder, cache, broker, atau API pihak ketiga) mengalami pelambatan atau padam, sistem utama tetap melayani rute kritis dalam mode degradasi.
- **Circuit Breaker & Retry with Jitter**: Cegah badai koneksi (*thundering herd*). Terapkan batas waktu ketat (*timeout* $\le 2.5\text{s}$), backoff eksponensial dengan jitter acak, dan pemutus sirkuit.
- **Failover & RPO/RTO**: Pastikan basis data memiliki replika baca dan prosedur pemulihan PITR dengan bukti uji restore berkala.

### Pilar 2: Security & Trust Boundaries (Keamanan & Batas Kepercayaan)
- **Zero Trust Architecture**: Jangan mempercayai request semata-mata karena berasal dari jaringan internal. Autentikasi dan otorisasi wajib diverifikasi pada setiap batas layanan.
- **Cryptographic Sender-Constraining (DPoP)**: Untuk endpoint sensitif berisiko tinggi, gunakan token yang terikat secara kriptografis ke pasangan kunci klien (RFC 9449) guna mencegah eksfiltrasi dan replay serangan.
- **Least Privilege & RLS**: Akses data dibatasi di level database menggunakan Row-Level Security (RLS) PostgreSQL, memitigasi risiko IDOR pada lapisan aplikasi.

### Pilar 3: Performance & Capacity Envelope (Kinerja & Batas Kapasitas)
- **Amplop Kapasitas Kuantitatif**: Tetapkan angka eksplisit untuk RPS normal, kapasitas memori per instance, dan kuota connection pool database.
- **Pemrosesan Asinkron**: Alihkan tugas I/O berat (pembuatan laporan, pengiriman email/notifikasi, resize gambar) ke antrean latar belakang (*background workers*).
- **Backpressure & Concurrency Limits**: Lindungi layanan dari kehabisan memori (*OOM*) dengan menolak atau menahan request saat antrean worker melebihi batas ambang.

### Pilar 4: Cost Optimization & Anti-Waste (Efisiensi Biaya & Anti-Mubazir)
- **Modular Monolith Baseline**: Tolak mikroservis prematur. Satu aplikasi monolit modular menghemat 70–90% biaya jaringan egress, dependensi cluster orchestration, dan kompleksitas operasional.
- **Right-Sizing Komputasi**: Sesuaikan ukuran instance dengan profil memori aktual, manfaatkan auto-scaling berbasis antrean/metrik nyata, dan matikan lingkungan staging yang tidak aktif di luar jam kerja.
- **Storage Tiering**: Pindahkan log dan arsip historis yang jarang diakses ke penyimpanan objek berbiaya rendah dengan kebijakan lifecycle otomatis.

### Pilar 5: Operational Excellence & Fitness Functions (Kecakapan Operasional)
- **SRE SLO Alerting**: Pasang alert berbasis error budget menggunakan pola *Multi-Window Multi-Burn-Rate* (menghindari alert fatigue akibat lonjakan CPU sesaat).
- **Structured Logs & Distributed Tracing**: Setiap request membawa `traceId` konsisten dari edge ke database.
- **Architecture Fitness Functions**: Terjemahkan invarian arsitektur (arah dependensi modul, ketiadaan impor sirkular, kepatuhan batas modul) ke dalam pemeriksaan otomatis di CI pipeline.

### Pilar 6: Evolutionary Simplicity & Radical Minimalism (Kesederhanaan Evolusioner)
- **The Deletion Test**: Komponen atau modul dirancang sedemikian rupa sehingga dapat dihapus atau diganti tanpa merombak logika internal pemanggil (*caller*).
- **Two-Adapter Seam Rule**: Dilarang membuat interface/abstraksi spekulatif bila hanya ada satu implementasi konkret tanpa kebutuhan fake test memori.
- **Revisit Triggers Kuantitatif**: Tetapkan batas numerik konkret kapan struktur monolitik modular layak dipecah menjadi layanan independen (misal: penulisan tabel inti $>2.500\text{ TPS}$ konstan).

---

## 4. Siklus Validasi Solusi: Pre-Deployment & Runtime

Sebelum arsitektur dinyatakan siap rilis ke produksi, jalankan dua tahap pembuktian:

### 4.1 Validasi Pre-Deployment (Statis & Dry-Run)
1. **Pemeriksaan Topologi & Routing**: Verifikasi bahwa topologi jaringan tidak menyisakan endpoint privat yang terbuka ke publik.
2. **Dry-Run Konfigurasi**: Eksekusi perintah validasi sintaksis infrastruktur (misal `terraform plan` atau dry-run manifes) tanpa memodifikasi sumber daya aktif.
3. **Audit Kebijakan Keamanan**: Pastikan aturan firewall, kebijakan RLS, dan variabel environment rahasia terdefinisi lengkap tanpa nilai default placeholder.

### 4.2 Validasi Runtime (Post-Deployment)
1. **Canary & Health Check**: Lepaskan trafik bertahap ($5\% \to 25\% \to 100\%$) dan verifikasi kode status HTTP `200` pada probe `/health`.
2. **Synthetic Probing**: Jalankan pengujian sintetis dari luar jaringan untuk mengukur latensi round-trip aktual dan fungsionalitas rute kritis.
3. **Kesiapan Rollback**: Uji satu perintah rollback digest image versi sebelumnya dan buktikan pemulihan berhasil dalam waktu $\le 5$ menit.
