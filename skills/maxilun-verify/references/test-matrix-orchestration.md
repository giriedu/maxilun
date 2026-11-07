# Test Matrix Orchestration: Deterministic Verification Engineering

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-verify/SKILL.md"
  origin: "Maxilun Verify Engine"
-->

Panduan orkestrasi matriks pengujian deterministik, pengujian integrasi berbasis kontainer, dan eliminasi tes rapuh (*flaky tests*).

---

## 1. Piramida Matriks Pengujian Terukur

Piramida pengujian diatur berdasarkan rasio kecepatan eksekusi dan tingkat isolasi:

```text
       [End-to-End Playwright (Kritis Saja, < 10%)]
                        ▲
          [Pengujian Integrasi & Kontrak API (20-30%)]
                        ▲
           [Pengujian Unit & State Deterministik (60-70%)]
```

1. **Pengujian Unit (Unit Tests)**:
   - Menguji fungsi murni, state machine, dan transformasi data.
   - Wajib berjalan dalam memori tanpa I/O jaringan atau disk nyata ($< 5\text{ms}$ per tes).
2. **Pengujian Integrasi & Kontrak (Integration / Contract Tests)**:
   - Menguji interaksi antara handler kode dengan basis data nyata atau antrean pesan.
   - Gunakan basis data sementara (*ephemeral database* / Testcontainers) daripada mock palsu yang menyembunyikan inkonsistensi tipe SQL.
3. **Pengujian End-to-End (E2E)**:
   - Gunakan Playwright untuk menguji alur kerja utama pengguna (*critical user journeys*): pendaftaran akun, alur transaksi pembayaran, dan pengiriman formulir.
   - Jalankan dalam mode headless dengan perekaman jejak (*trace recording*) aktif hanya saat terjadi kegagalan.

---

## 2. Invarian Anti-Flakiness

1. **Dilarang Penungguan Waktu Arbitrer (`sleep`)**:
   - Seluruh asersi wajib menggunakan penungguan berbasis status eksplisit (misal: `waitForSelector`, `await expect(...).toBeVisible()`).
2. **Isolasi State Antar-Pengujian**:
   - Setiap kasus uji wajib memiliki data awal bersih (*clean fixture*). Dilarang mengandalkan efek samping atau mutasi yang ditinggalkan oleh kasus uji sebelumnya.
3. **Penyimpanan Screenshot & Trace Kegagalan**:
   - Simpan tangkapan layar dan log konsol browser hanya untuk tes yang gagal agar tidak membebani ruang penyimpanan artefak CI/CD.
