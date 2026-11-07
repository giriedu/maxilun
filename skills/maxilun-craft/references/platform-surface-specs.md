# Platform Surface Specifications: Native iOS & Android Ergonomics

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine"
-->

Panduan spesifikasi rekayasa antarmuka native untuk platform seluler iOS dan Android. Memastikan aplikasi dibangun mengikuti konvensi platform sesungguhnya dan menolak mentalitas membungkus tampilan web mentah ke dalam layar ponsel.

---

## 1. Prinsip Utama: The Interface IS the Object

Alih-alih menyusun aplikasi sebagai deretan ubin statistik (*dashboard stat tiles*) yang monoton:

1. **Satu Objek Pengendali Inti**:
   - Pusatkan setiap layar pada satu representasi fisik interaktif yang mewakili fungsi utama aplikasi:
     - Aplikasi pelacak tidur: Jam malam melingkar yang dapat digeser untuk mengatur target tidur.
     - Aplikasi keuangan: Satu grafik aliran dana berkesinambungan yang merespons usapan jari.
     - Aplikasi penginapan butik: Bingkai arsitektur lengkung (*arch mask*) yang membingkai suasana tempat sebelum angka harga.
2. **Elemen Sekunder Mengorbit**:
   - Seluruh filter, tombol tindakan, dan data rincian disusun secara tenang di sekitar objek inti tersebut tanpa berebut hierarki pandang.

---

## 2. Spesifikasi Native iOS (SwiftUI & UIKit)

1. **Disiplin Safe Area**:
   - Konten interaktif, tombol, dan formulir wajib berada di dalam batas Safe Area (`safeAreaPadding()`).
   - Hanya gambar latar belakang dekoratif dan media visual yang diizinkan melintasi batas Safe Area (`ignoresSafeArea()`).
2. **Material Translusen (Liquid Glass)**:
   - Gunakan material sistem bawaan (`.ultraThinMaterial`, `.regularMaterial`) untuk bilah navigasi atas dan bilah tab bawah, sehingga konten di balik bilah tetap memberikan kedalaman spasial saat digulir.
3. **Kepatuhan Dynamic Type**:
   - Dilarang mengunci ukuran teks dengan angka mutlak tanpa skala. Gunakan gaya teks semantik (`.title`, `.headline`, `.body`, `.caption`) agar ukuran huruf otomatis beradaptasi saat pengguna mengubah preferensi ukuran teks di pengaturan iOS.
4. **Target Sentuh Minimum $44\text{pt}$**:
   - Setiap kontrol klik wajib memiliki ukuran kotak sentuh minimal $44 \times 44\text{pt}$.
5. **Navigasi Sistem Native**:
   - Utamakan penggunaan `NavigationStack` native agar gestur usap untuk kembali (*interactive swipe-back gesture*) bekerja secara alami tanpa glitch visual.

---

## 3. Spesifikasi Native Android (Jetpack Compose & Material 3 Expressive)

1. **Tonal Elevation (Bukan Drop Shadow Tebal)**:
   - Material 3 mengekspresikan kedalaman spasial menggunakan tingkatan warna permukaan tonal (`surfaceContainerLowest`, `surfaceContainerLow`, `surfaceContainer`, `surfaceContainerHigh`), bukan bayangan gelap hitam pekat yang kotor.
2. **Target Sentuh Minimum $48\text{dp}$**:
   - Setiap elemen tombol atau area interaksi sentuh wajib memenuhi standar minimal $48 \times 48\text{dp}$ untuk mengakomodasi berbagai ukuran ujung jari pengguna.
3. **Dukungan Gestur Predictive Back**:
   - Integrasikan API navigasi Android modern yang mendukung pratinjau animasi kembali (*predictive back animation*) sebelum pengguna melepas jari dari tepi layar.
4. **Penanganan Keyboard Virtual Otomatis**:
   - Seluruh formulir input wajib menerapkan penyesuaian bantalan keyboard (`WindowInsets.ime` atau `imePadding()`) agar kolom yang sedang diketik tidak tertutup oleh keyboard virtual perangkat.

---

## 4. Matriks Ringkas Komparasi Platform

| Parameter Desain | Standar iOS (SwiftUI) | Standar Android (Material 3) |
|---|---|---|
| **Target Sentuh Minimum** | $44 \times 44\text{pt}$ | $48 \times 48\text{dp}$ |
| **Material Navigasi** | `.ultraThinMaterial` translusen | Tonal surface tint (warna aksen beropasitas halus) |
| **Pemisah Kedalaman** | Garis batas hairline $1\text{px}$ / blur latar | Perbedaan saturasi/luminansi level kontainer |
| **Ukuran Teks Input** | Minimal $16\text{pt}$ (mencegah auto-zoom) | Minimal $16\text{sp}$ |
| **Gestur Navigasi Utama** | Usap tepi kiri (*edge swipe-back*) | Gestur tepi adaptif (*Predictive Back*) |
| **Aksi Mengambang** | Bilah bawah mengambang atau bar toolbar | Floating Action Button (FAB) terstandarisasi |
