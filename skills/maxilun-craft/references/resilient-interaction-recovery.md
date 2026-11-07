# Resilient Interaction Recovery: Fault-Tolerant UX Patterns

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine"
-->

Panduan rekayasa penanganan galat dan pemulihan interaksi tahan gangguan (*resilient interaction recovery*). Antarmuka produksi memperlakukan kegagalan jaringan, validasi, dan transaksi sebagai bagian normal dari siklus hidup aplikasi, bukan anomali yang ditutup dialog peringatan kosong.

---

## 1. Prinsip Kedekatan Titik Galat (Inline Proximity)

1. **Dilarang Modal Peringatan Global untuk Galat Lokal**:
   - Galat pengisian formulir, kegagalan unggah berkas tunggal, atau validasi field wajib ditampilkan langsung di bawah atau di samping kontrol bersangkutan.
   - Dialog modal hanya diizinkan untuk kegagalan tingkat sistem fatal yang memutus seluruh sesi kerja (misal: token autentikasi kedaluwarsa permanen).
2. **Anatomi Pesan Galat yang Lengkap**:
   Pesan galat yang sah wajib memenuhi rumus tiga bagian:
   - **Apa yang terjadi**: Fakta objektif (misal: *"Nomor telepon kurang 2 digit"*).
   - **Mengapa gagal**: Batasan sistem yang tidak terpenuhi (*"Format standar memerlukan minimal 10 digit"*).
   - **Jalur perbaikan langsung**: Aksi perbaikan konkret tanpa perlu memuat ulang halaman (*"Tambahkan kode area"* atau tombol *"Coba kirim ulang"*).

---

## 2. Pola Transaksi Undo vs Kelelahan Modal Konfirmasi

Dialog pop-up *"Apakah Anda yakin ingin menghapus data ini?"* menimbulkan kelelahan kognitif (*confirmation modal fatigue*) dan sering diklik otomatis tanpa dibaca.

Gantikan dengan pola **Reversible Mutation (Undo Toast)**:

```text
[Data dihapus dari daftar seketika]
        │
        ▼ (Tampilkan baris status mengambang 6 detik)
┌────────────────────────────────────────────────────────┐
│  1 kontak dipindahkan ke tempat sampah.   [ Batal ]    │
└────────────────────────────────────────────────────────┘
```

### Invarian Undo Toast:
1. **Durasi Terukur**: Baris notifikasi tampil selama 5 hingga 8 detik sebelum transaksi difinalisasi di server.
2. **Aksi Batal Seketika**: Mengklik tombol *"Batal"* (*Undo*) langsung mengembalikan elemen ke posisi semula dalam daftar tanpa refetch jaringan penuh.
3. **Pengecualian Mutasi Permanen**: Dialog konfirmasi eksplisit hanya dipakai jika aksi bersifat destruktif permanen dan tidak dapat dibatalkan (misal: menghapus repositori produksi atau menghapus akun secara permanen).

---

## 3. Invarian Perlindungan Data Masukan (Data Preservation)

1. **Dilarang Mengosongkan Formulir Saat Pengiriman Gagal**:
   - Jika proses `submit` gagal karena respons status non-200 atau jaringan terputus, seluruh data yang sudah diketik pengguna wajib tetap utuh di dalam field masing-masing.
   - Tandai field yang tidak valid dengan garis tepi merah semantik dan indikator ikon, tetapi pertahankan teks input pengguna agar mereka tidak perlu mengetik ulang dari awal.
2. **Penyimpanan Draf Lokal Otomatis**:
   - Untuk formulir panjang (> 4 field), simpan perubahan sementara ke penyimpanan lokal (`sessionStorage` atau IndexedDB) sehingga input aman dari ketidaksengajaan menutup tab atau browser crash.
3. **Rollback Mutasi Optimistik**:
   - Jika antarmuka memperbarui status secara optimistik (misal: mencentang checkbox selesai), lalu server menolak permintaan, kembalikan status visual ke kondisi awal secara halus disertai notifikasi inline singkat tentang alasan penolakan.

---

## 4. Penanganan Mode Terdegradasi & Partisi Jaringan

1. **Deteksi Konektivitas Aktif**:
   - Manfaatkan event `navigator.onLine` dan pemantauan `fetch` timeout untuk menampilkan indikator koneksi pasif di bilah status (*offline badge*), tanpa memblokir pembacaan konten yang sudah ter-cache.
2. **Antrean Aksi Tertunda (Offline Queue)**:
   - Tindakan pengguna saat koneksi terputus disimpan ke dalam antrean lokal dan otomatis disinkronisasi saat koneksi pulih (*automatic replay*).
