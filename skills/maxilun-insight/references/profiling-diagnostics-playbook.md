# Systems Profiling & Deep Diagnostics Playbook

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-insight/SKILL.md"
  origin: "Maxilun Insight Engine"
-->

Panduan diagnostik kinerja sistemik, pelacakan kebocoran memori (*memory leaks*), dan analisis titik jenuh CPU/IO.

---

## 1. Analisis Flamegraph CPU

1. **Mengidentifikasi Hot Path**:
   - Periksa lebar balok (*plateau*) pada visualisasi flamegraph. Balok yang lebar menunjukkan fungsi yang menghabiskan waktu eksekusi CPU paling lama.
2. **Pembedaan CPU Bound vs IO Bound**:
   - Jika penggunaan CPU mendekati 100% dan grafik menunjukkan kalkulasi berulang, optimalkan algoritma atau terapkan memoization.
   - Jika waktu tunggu tinggi tetapi CPU rendah, periksa latensi kueri basis data eksternal atau pemanggilan HTTP jaringan downstream.

---

## 2. Pelacakan Kebocoran Memori (Heap Profiling)

1. **Pengambilan 3 Snapshot Berurutan**:
   - Ambil snapshot memori saat inisiasi (*Baseline*).
   - Picu operasi sistem berulang kali (*Stress Test*).
   - Ambil snapshot kedua, jalankan garbage collector paksa, lalu ambil snapshot ketiga (*Comparison*).
2. **Mendeteksi Objek Tertahan (Retained Size)**:
   - Bandingkan perbedaan objek antara snapshot 1 dan snapshot 3. Objek yang terus bertambah tanpa pernah dibersihkan menandakan adanya kebocoran referensi (misal: event listener yang tidak di-unregister, map cache tak berbatas, atau closure memegang referensi ke objek besar).

---

## 3. Investigasi Deadlock & Kontensi Koneksi

1. **Pemantauan Pool Koneksi**:
   - Jika latency melonjak tajam saat traffic naik, periksa apakah antrean pool koneksi basis data mengalami kehabisan slot (*pool exhaustion*).
2. **Urutan Penguncian Konsisten (Lock Ordering)**:
   - Untuk mencegah deadlock transaksi multi-tabel, pastikan seluruh alur kode mengunci baris atau tabel dengan urutan yang sama (misal: selalu urutkan ID secara menaik sebelum melakukan `SELECT ... FOR UPDATE`).
