# Task Flow Choreography: User Mental Pathways & Friction Reduction

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine"
-->

Panduan koreografi alur tugas pengguna (*task flow choreography*) untuk meminimalkan beban kognitif dan memotong titik gesekan navigasi. Menghilangkan ketergantungan pada diagram alur abstrak dan berfokus pada efisiensi transisi layar nyata dalam menyelesaikan tugas utama.

---

## 1. Dekonstruksi Jalur Mental Pengguna (User Mental Pathways)

Setiap tugas pengguna dalam aplikasi terdiri dari 4 tahapan mental diskrit:

```text
[Orientasi Konteks] ──> [Evaluasi Pilihan] ──> [Konfirmasi Aksi] ──> [Verifikasi Hasil]
```

1. **Orientasi Konteks (< 2 detik)**:
   - Pengguna memahami di mana mereka berada dan apa tujuan halaman saat ini.
   - Wajib menampilkan judul yang jelas dalam format *sentence case* dan identifikasi entitas kerja utama.
2. **Evaluasi Pilihan**:
   - Membatasi opsi yang disajikan pada satu waktu (Hukum Hick).
   - Tampilkan parameter paling menentukan terlebih dahulu (misal: harga, ketersediaan tanggal, atau status pesanan) sebelum menyajikan opsi pengaturan sekunder.
3. **Konfirmasi Aksi**:
   - Tombol tindakan primer wajib menggunakan label spesifik berbentuk kata kerja + objek (misal: *"Konfirmasi Reservasi"*, *"Kirim Laporan"*).
   - Hindari tombol dengan label generik (*"Submit"*, *"OK"*, *"Next"*).
4. **Verifikasi Hasil**:
   - Tampilkan bukti visual bahwa aksi telah berhasil dicatat oleh sistem (perubahan status seketika, ringkasan bukti transaksi, atau nomor referensi).

---

## 2. Mengeliminasi Pantulan Layar (Screen Bounce)

Pantulan layar (*screen bounce*) terjadi saat pengguna dipaksa berpindah layar penuh hanya untuk memasukkan sepotong kecil data, lalu kembali lagi ke layar awal.

Gantikan dengan pola **In-Place Choreography**:

| Kasus Interaksi | Pola Konvensional (Banyak Pantulan) | Pola Koreografi Maxilun (Tanpa Pantulan) |
|---|---|---|
| **Filter & Pengurutan Data** | Pindah ke halaman filter terpisah. | Gunakan panel laci (*bottom sheet*) atau filter inline langsung di atas tabel data. |
| **Penyuntingan Baris Tunggal** | Pindah ke formulir edit layar penuh. | Terapkan penyuntingan inline (*click-to-edit*) atau drawer samping non-intrusif. |
| **Pratinjau Rincian Item** | Pindah ke rute baru, lalu menekan tombol kembali. | Terapkan pratinjau split (*master-detail pane*) di desktop atau ekspansi akordeon di mobile. |

---

## 3. Disiplin Pengungkapan Bertahap (Progressive Disclosure)

1. **Aturan 80/20**:
   - Tampilkan 80% parameter umum yang dibutuhkan mayoritas pengguna secara langsung di permukaan utama.
   - Sembunyikan 20% konfigurasi tingkat lanjut (*advanced settings*) di balik kontrol pengungkapan bertahap (*disclosure toggle* atau tab sekunder).
2. **Konteks Bertahan**:
   - Saat pengguna membuka rincian opsi lanjutan, pastikan ringkasan parameter utama sebelumnya tetap terlihat sebagai jangkar pembanding.

---

## 4. Eksekusi Subtraction Pass dalam Alur Kerja

Gunakan daftar periksa subtraksi ini sebelum memfinalisasi alur tugas:

1. **Pemeriksaan Redundansi**: Apakah ada teks instruksi yang sebenarnya sudah jelas dari label input itu sendiri? (Jika ya, hapus teks instruksi tersebut).
2. **Pemeriksaan Garis Batas**: Apakah pemisahan visual bisa dicapai cukup dengan spasi 2x (*spatial rhythm*) alih-alih menambahkan garis pembatas atau kartu baru? (Jika ya, hapus garis/kartu tersebut).
3. **Pemeriksaan Klik**: Apakah ada langkah dalam alur yang bisa digabungkan tanpa membebani pemahaman pengguna? (Jika ya, pangkas jumlah langkahnya).
