# Cross-Platform Mobile Engineering (Flutter, React Native, KMP)

Panduan rekayasa aplikasi mobile lintas platform dengan penekanan pada performa native, arsitektur state yang deterministik, dan komunikasi jembatan sistem.

## 1. Flutter & Dart Engineering

### 1.1 Optimasi Pohon Widget & State
- **Konstruktor `const`**: Sematkan `const` pada setiap widget yang tidak bergantung pada variabel dinamis untuk memangkas alokasi siklus rebuild.
- **Isolate untuk Komputasi & JSON Parsing**:
  Gunakan `compute()` atau `Isolate.run()` saat mem-parsing JSON berukuran besar atau melakukan kompresi gambar agar frame rate tetap terjaga di 60/120 FPS:
  ```dart
  Future<List<Item>> parseItems(String rawJson) async {
    return await Isolate.run(() => parseJsonInBackground(rawJson));
  }
  ```
- **Platform Channels**: Validasi tipe data pada `MethodChannel`. Kembalikan error terstruktur melalui `PlatformException` saat integrasi native gagal.

---

## 2. React Native (New Architecture & Hermes)

- **Fabric & TurboModules**: Migrasikan modul native ke C++ JSI / TurboModules untuk menghilangkan overhead serialisasi JSON asynchronous pada jembatan legacy.
- **Animasi di UI Thread**: Gunakan `react-native-reanimated` dan `react-native-gesture-handler`. Jalankan transisi gestur langsung di thread UI tanpa melewati JS thread.
- **Manajemen List**: Gunakan `@shopify/flash-list` alih-alih `FlatList` konvensional untuk daftaran data berulang guna memastikan daur ulang view yang instan.

---

## 3. Kotlin Multiplatform (KMP)

- **Batas Logika Bersama**: Bagikan domain logic, repository, validasi, dan klien jaringan (`Ktor`) serta database (`SQLDelight`). Biarkan layer presentasi tetap native (Compose di Android, SwiftUI di iOS).
- **Deklarasi `expect` / `actual`**: Batasi penggunaan `expect`/`actual` hanya pada titik yang benar-benar membutuhkan API platform unik (UUID generator, secure storage, sensor).
