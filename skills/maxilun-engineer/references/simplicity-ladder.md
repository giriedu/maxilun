# The Simplicity Ladder: Operationalizing Minimalist Code

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-engineer/SKILL.md"
  origin: "Maxilun Engineer Engine"
-->

Panduan penerapan *Simplicity Ladder* (Tangga Kesederhanaan) dalam penulisan logika produksi dan refactoring terukur.

---

## 1. Lima Tingkatan Tangga Kesederhanaan

Sebelum menambahkan kelas, abstraksi baru, atau pustaka pihak ketiga, evaluasi solusi mulai dari tingkatan paling bawah:

```text
[Tingkat 5: Dependensi Pihak Ketiga Baru] ── (Opsi Terakhir, wajib justifikasi)
      ▲
[Tingkat 4: Abstraksi Modular / Polimorfisme]
      ▲
[Tingkat 3: Fungsi Bantu Murni (Pure Helper Function)]
      ▲
[Tingkat 2: Fitur Bawaan Bahasa / Stdlib]
      ▲
[Tingkat 1: Nol Kode Baru / Manfaatkan Kode yang Ada]
```

1. **Tingkat 1 — Manfaatkan Kode Eksisting**:
   - Periksa apakah repositori sudah memiliki fungsi pembantu (*helper*), utilitas, atau method yang menyelesaikan masalah ini. Dilarang menduplikasi utilitas serupa dengan nama berbeda.
2. **Tingkat 2 — Manfaatkan Fitur Standar Bahasa (Stdlib)**:
   - Gunakan fungsi bawaan bahasa (seperti `structuredClone` di JavaScript, `array_map` / `match` di PHP, `itertools` di Python, `slices` di Go).
3. **Tingkat 3 — Fungsi Murni Tunggal**:
   - Tulis satu fungsi lokal murni tanpa *side-effect* yang menerima input dan mengembalikan output secara deterministik.
4. **Tingkat 4 — Pola Desain Berorientasi Objek Terbatas**:
   - Gunakan kelas atau antarmuka hanya jika perilaku memiliki beberapa variasi polimorfik nyata.
5. **Tingkat 5 — Dependensi Eksternal Baru**:
   - Menambah paket di `package.json`, `composer.json`, atau `go.mod` adalah opsi paling akhir. Evaluasi ukuran paket, frekuensi rilis, dan potensi celah keamanan sebelum menambahkannya.

---

## 2. Invarian Komentar Kode

1. **Jelaskan MENGAPA, Bukan APA**:
   - Komentar yang menjelaskan alur kode yang jelas terbaca (*"menaikkan nilai counter"* atau *"memeriksa apakah user ada"*) wajib dihapus.
   - Tulis komentar hanya untuk keputusan arsitektur yang tidak lazim, batasan spesifikasi eksternal, atau penanganan celah perangkat keras/browser tertentu.
2. **Hapus Kode Usang Sendiri**:
   - Saat Anda merefaktor fungsi, hapus seluruh impor yang tidak lagi terpakai, variabel sisa, dan jalur cabang mati yang ditinggalkan oleh perubahan Anda.
