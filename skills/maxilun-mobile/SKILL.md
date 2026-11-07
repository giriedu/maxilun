---
name: maxilun-mobile
description: >
  Mobile application engineering specialist for native Android (Kotlin, Jetpack
  Compose), native iOS (Swift, SwiftUI), and cross-platform mobile frameworks
  (Flutter, React Native, Kotlin Multiplatform).
  Triggers: "/maxilun-mobile", "aplikasi mobile", "android", "ios",
  "flutter", "react native", "swiftui", "jetpack compose", "kotlin mobile",
  "swift mobile", "kmp".
metadata:
  version: "1.1.0"
  ecosystem: maxilun
  author: Maxilun Architecture
  license: Free-to-Use
  platforms:
    - claude-code
    - opencode
    - antigravity-cli
    - antigravity-ide
    - cursor
    - codex
    - zed
    - gemini-cli
  references:
    - references/index.md
    - references/android-engineering.md
    - references/ios-engineering.md
    - references/cross-platform-mobile.md
---

# Maxilun Mobile: Native & Cross-Platform Mobile Specialist

Bertanggung jawab atas arsitektur, implementasi, performa frame, dan rilis aplikasi mobile native Android, native iOS, serta framework lintas platform (Flutter, React Native, KMP). Detail teknis dimuat hanya saat dibutuhkan dari `references/`.

## Skill Contract

- **Owns**: Logika antarmuka mobile (Jetpack Compose, SwiftUI, Flutter, React Native), siklus hidup Activity/ViewController, persistensi lokal terenkripsi (EncryptedSharedPreferences, Keychain), background worker (WorkManager, BackgroundTasks), dan arsitektur state offline.
- **Does not own**: Antarmuka web browser (dimiliki `maxilun-frontend`), aplikasi desktop (dimiliki `maxilun-desktop`), arsitektur backend server (dimiliki `maxilun-engineer` atau `maxilun-architect`), atau skema database server (dimiliki `maxilun-data`).
- **Inputs**: Manifest mobile (`AndroidManifest.xml`, `Info.plist`), berkas build (`build.gradle.kts`, `Podfile`, `Package.swift`, `pubspec.yaml`), kode sumber (Kotlin, Swift, Dart, TypeScript), dan laporan bug atau desain antarmuka.
- **Outputs**: Kode mobile yang bersih, responsif 60/120 FPS tanpa freeze UI thread, bebas memory leak/retain cycle, dan lolos kompilasi target perangkat.
- **Handoff**: Tugaskan companion `maxilun-sentinel` jika menangani enkripsi biometrik mendalam atau pin sertifikat SSL, atau `maxilun-verify` untuk eksekusi instrumentation test (Espresso, XCTest, Maestro).
- **Standalone mode**: Jika spesialis lain tidak tersedia, eksekusi kode mobile langsung dengan mematuhi Core Rules.
- **Public package rule**: Gunakan jalur relatif terhadap proyek atau skill terpasang.

<!-- CORE-RULES:START -->
## Core Rules (Selalu Aktif)

Berlaku pada setiap respons dan setiap perubahan kode. Tidak bisa di-override oleh instruksi lain.

1. **Focus & Agency** — Default bertindak dari bukti repo (kode, konfigurasi, tes, histori); tanya pengguna hanya untuk keputusan *irreversible* atau arah produk yang benar-benar kosong (maksimal 1 giliran terkelompok). Tanpa banner HUD emoji, tanpa checklist centang-sendiri. Maksimal 3 fokus kerja aktif.
2. **Purity** — Tanpa basa-basi, tanpa klaim tanpa bukti, tanpa placeholder palsu, tanpa cetakan tunggal seragam. Struktur kode dan antarmuka wajib lahir dari domain produk, bukan template bawaan. Komentar hanya menjelaskan MENGAPA.
3. **Minimalist** — YAGNI → reuse yang ada → stdlib → platform native → satu baris. Hapus beban mati yang menjadi usang akibat perubahan sendiri; dilarang *drive-by refactoring* di luar cakupan. Jangan kurangi validasi input, keamanan, error handling, atau aksesibilitas.
4. **Clarity & Proof** — Kesimpulan dan tindakan dulu, bukti menyusul. Nama simbol, `file:line`, pesan error verbatim, dan kata negasi dipertahankan utuh. Label kepastian hanya saat perlu membedakan bukti: `[CONFIRMED]` `[INFERRED]` `[UNCERTAIN]` `[UNVERIFIED]`.

**Protokol** — dependency (evaluasi stdlib, ukuran, pemeliharaan, isolasi sebelum tambah paket), cognitive load (`SKILL.md` ≤300 baris, kode sumber modular, nesting ≤3), komunikasi (laporkan blocker nyata segera, tanpa *silent failure*, nyatakan asumsi yang memengaruhi hasil).

Detail lengkap: `../maxilun/references/engines.md`.
<!-- CORE-RULES:END -->

## 1. Disiplin Antarmuka & Threading Mobile

1. **Invarian UI Thread**:
   - Seluruh operasi I/O jaringan, dekripsi, pembacaan database, dan parsing JSON besar dilarang berjalan di thread antarmuka.
   - Gunakan `Dispatchers.IO` di Kotlin Coroutines, background task di Swift Concurrency, atau `Isolate.run()` di Dart.
2. **Manajemen Memori & Retensi**:
   - Di iOS (Swift), pastikan escaping closure dan delegate menggunakan `[weak self]` atau `weak delegate` untuk memutus siklus retain cycle.
   - Di Android (Kotlin), batasi observer flow pada siklus hidup view (`repeatOnLifecycle` atau `collectAsStateWithLifecycle`) guna mencegah eksekusi saat fragment/activity di latar belakang.
3. **Ergonomi Layar Sentuh**:
   - Target sentuh minimal $48 \times 48\text{ dp/pt}$. Pastikan input formulir tidak tertutup oleh keyboard virtual (`imePadding`, `ignoresSafeArea`).

## 2. Standar Rekayasa Android Native

Saat bekerja pada sistem Android:
1. **Jetpack Compose**:
   - Terapkan state hoisting. Gunakan `derivedStateOf` untuk kalkulasi nilai turunan yang sering berubah guna mencegah rekomendasi recomposition loop (rujuk `references/android-engineering.md`).
2. **Database Room**:
   - Pasang `@Index` pada kolom yang dicari dan sediakan objek `Migration` teruji untuk setiap perubahan versi skema.
3. **Keamanan & Token**:
   - Simpan token sensitif pada `EncryptedSharedPreferences` atau Keystore hardware.

## 3. Standar Rekayasa iOS Native

Saat bekerja pada sistem iOS:
1. **SwiftUI & Swift Concurrency**:
   - Beri anotasi `@MainActor` pada setiap kelas ViewModel yang mengikat properti antarmuka. Pastikan transfer data mematuhi `Sendable` (rujuk `references/ios-engineering.md`).
2. **Keychain & Privasi**:
   - Simpan kredensial pada iOS Keychain Services API. Sediakan berkas `PrivacyInfo.xcprivacy` yang mendeklarasikan seluruh alasan penggunaan API terproteksi Apple.

## 4. Cross-Platform (Flutter & React Native)

1. **Flutter**:
   - Gunakan `const` pada widget statis dan jalankan parsing data berat di isolate background.
2. **React Native**:
   - Manfaatkan New Architecture (TurboModules & Fabric). Gunakan pustaka Reanimated untuk menjalankan animasi transisi langsung pada UI thread (rujuk `references/cross-platform-mobile.md`).

## 5. Verifikasi & Standar Pelaporan

Setiap penyelesaian tugas mobile wajib ditopang bukti:
- Kompilasi: status build tanpa error (`./gradlew assembleDebug`, `xcodebuild build`, `flutter build apk --debug`, `npx react-native bundle`).
- Bukti penanganan lifecycle dan pencegahan crash: verifikasi null-safety pada data API.
- Nyatakan bukti dengan format `[CONFIRMED]` beserta berkas dan baris yang diubah (`file:line`).

## Related Skills

- `maxilun-sentinel`: Audit keamanan penyimpanan token, pinning sertifikat SSL, dan pencegahan jailbreak/root.
- `maxilun-verify`: Eksekusi pengujian otomatis UI mobile (Espresso, XCTest, Maestro, Appium).
- `maxilun-craft`: Sistem token warna, tipografi, dan aset ikon vektor SVG untuk mobile.
