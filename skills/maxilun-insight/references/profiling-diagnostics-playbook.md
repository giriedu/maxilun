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

---

## 4. Matriks Triage Diagnostik Sistemik (Hangs, Leaks, Exhaustion, Disruption)

Saat sistem mengalami anomali runtime di lingkungan pengujian maupun produksi, gunakan matriks triage terstruktur untuk mengisolasi akar penyebab dalam 4 kelas kegagalan:

| Kelas Kegagalan | Sinyal Teramati | Mekanisme Akar Penyebab | Instrumen Bukti & Verifikasi |
|---|---|---|---|
| **1. Hang & Process Stall** | Event-loop lag tinggi, proses tidak merespon `/health` padahal CPU rendah, thread pool beku | Mutex/row lock deadlock, panggilan I/O sinkron di loop async, transaksi database `idle in transaction` tanpa timeout, atau distributed lock tanpa auto-expiry | Node `perf_hooks.monitorEventLoopDelay()`, Python `py-spy dump`, Go `pprof/goroutine` (deteksi goroutine leak), `pg_stat_activity` (filter `state = 'idle in transaction'`) |
| **2. Memory Leak & OOM Killer** | RSS memori menanjak monoton pasca-GC, jeda stop-the-world GC membesar, proses mati mendadak dengan exit code `137` | Map/cache memori tanpa eviksi LRU/TTL, closure menahan referensi objek besar, event listener tanpa `removeEventListener`, stream tanpa backpressure | Diff 3 heap snapshot V8/Python `tracemalloc`, inspeksi `dmesg -T \| grep -i oom`, bandingkan ukuran `Retained Size` objek |
| **3. Connection & Resource Exhaustion** | Error `pool timeout`, `EMFILE / too many open files`, ribuan soket menggantung di `TIME_WAIT` | Koneksi database tidak dilepas di blok `finally`, response stream HTTP client tidak ditutup, atau koneksi keluar dibuat baru per request tanpa keep-alive | `lsof -p <pid> \| wc -l` (hitung file descriptor), `netstat -ant \| grep TIME_WAIT \| wc -l`, kueri jumlah koneksi aktif vs `max_connections` |
| **4. Disruption & Unclean Shutdown** | Terputus `502 Bad Gateway` atau `ECONNRESET` saat deploy/restart, data mutasi terpotong | Kontainer dibungkus shell sehingga `SIGTERM` tidak sampai ke proses aplikasi (PID 1), handler shutdown tidak menolak request baru sambil menguras in-flight jobs, grace period terlalu pendek | Verifikasi `PID 1` di kontainer (`ps aux`), audit handler sinyal `SIGTERM`/`SIGINT`, dan uji coba simulasi `kill -15 <pid>` di staging |

### 4.1 Protokol 5 Langkah Triage Cepat
1. **Cek Exit Code**: Apakah proses mati dengan `137` (OOM), `143` (SIGTERM timeout), atau `1` (uncaught exception)?
2. **Identifikasi Sinyal I/O vs CPU**: Apakah CPU saturasi 100% (komputasi intensif/loop) atau 0–5% (deadlock/I/O wait)?
3. **Periksa File Descriptors & Socket**: Apakah FD mendekati `ulimit -n` sistem?
4. **Cek Transaksi Menggantung**: Apakah ada transaksi terbuka lebih dari 5 detik di database?
5. **Formulasikan Rekomendasi Terukur**: Terapkan perbaikan minimal (misal: pasang `statement_timeout = '3s'`, bungkus stream dengan `pipeline()`, atau tambahkan graceful draining).
