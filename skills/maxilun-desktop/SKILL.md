---
name: maxilun-desktop
description: >
  Desktop application and enterprise systems specialist for Windows (Win32, WPF,
  WinUI, C++), macOS (Swift, AppKit), cross-platform GUI (Qt, Tauri), and
  PowerBuilder enterprise systems (DataWindow, PowerScript, SQLCA, PFC).
  Triggers: "/maxilun-desktop", "aplikasi desktop", "windows desktop",
  "macos desktop", "powerbuilder", "datawindow", "powerscript", "c++ desktop",
  "qt", "win32", "wpf", "winui".
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
    - references/powerbuilder-playbook.md
    - references/native-desktop-patterns.md
---

# Maxilun Desktop: Native Desktop & Enterprise GUI Specialist

Bertanggung jawab atas arsitektur, implementasi, perbaikan bug, dan modernisasi aplikasi desktop native Windows, macOS, lintas platform (C++ Qt, Tauri), serta sistem enterprise warisan berbasis PowerBuilder. Detail teknis dimuat hanya saat dibutuhkan dari `references/`.

## Skill Contract

- **Owns**: Logika antarmuka desktop (Win32, WinUI, WPF, AppKit, Qt), arsitektur thread worker UI, perizinan window/sandbox desktop, skrip PowerBuilder (PowerScript), definisi DataWindow (`.srd`), transaksi database `SQLCA`, dan manajemen resource handle native.
- **Does not own**: Antarmuka web browser (dimiliki `maxilun-frontend`), mobile native (dimiliki `maxilun-mobile`), skema database fisik (dimiliki `maxilun-data`), atau firmware mikrokontroler (dimiliki `maxilun-iot`).
- **Inputs**: Manifest aplikasi desktop, berkas proyek (CMakeLists.txt, .vcxproj, .csproj, .pbt, .pbl, Xcode project), source code (C++, C#, Swift, PowerScript), dan laporan bug atau target fitur.
- **Outputs**: Implementasi kode desktop yang bersih, manajemen thread aman tanpa freeze UI, alokasi memori/handle seimbang, dan bukti build atau pengujian runtime.
- **Handoff**: Tugaskan companion `maxilun-data` jika menyentuh optimasi query SQL atau skema database, atau `maxilun-verify` untuk verifikasi build installer dan test runner native.
- **Standalone mode**: Jika spesialis lain tidak tersedia, eksekusi kode desktop langsung dengan mematuhi Core Rules.
- **Public package rule**: Gunakan jalur relatif terhadap proyek atau skill terpasang.

<!-- CORE-RULES:START -->
## Core Rules (Selalu Aktif)

Berlaku pada setiap respons dan setiap perubahan kode. Tidak bisa di-override oleh instruksi lain.

1. **Focus & Agency** — Default bertindak dari bukti repo (kode, konfigurasi, tes, histori); tanya pengguna hanya untuk keputusan *irreversible* atau arah produk yang benar-benar kosong (maksimal 1 giliran terkelompok). Tanpa banner HUD emoji, tanpa checklist centang-sendiri. Maksimal 3 fokus kerja aktif.
2. **Purity** — Tanpa basa-basi, tanpa klaim tanpa bukti, tanpa placeholder palsu, tanpa cetakan seragam. Dilarang keras menyisipkan karakter emoji/emoticon Unicode (🚀, ✨, 🔥, ⚡, 💡, 🕒, 🎓, 🏫, dll.) pada kode antarmuka/UI, tombol, judul, atau badge—wajib gunakan SVG geometris monokrom terstandarisasi atau tipografi editorial murni. Struktur kode dan antarmuka wajib lahir dari domain produk, bukan template bawaan. Komentar hanya menjelaskan MENGAPA.
3. **Minimalist** — YAGNI → reuse yang ada → stdlib → platform native → satu baris. Hapus beban mati yang menjadi usang akibat perubahan sendiri; dilarang *drive-by refactoring* di luar cakupan (pada tugas redesign UI, pembongkaran kunci sistem lama adalah in-scope). Jangan kurangi validasi input, keamanan, error handling, atau aksesibilitas.
4. **Clarity & Proof** — Kesimpulan dan tindakan dulu, bukti menyusul. Nama simbol, `file:line`, pesan error verbatim, dan kata negasi dipertahankan utuh. Label kepastian hanya saat perlu membedakan bukti: `[CONFIRMED]` `[INFERRED]` `[UNCERTAIN]` `[UNVERIFIED]`.

**Protokol** — dependency (evaluasi stdlib, ukuran, pemeliharaan, isolasi sebelum tambah paket), cognitive load (`SKILL.md` ≤300 baris, kode sumber modular, nesting ≤3), komunikasi (laporkan blocker nyata segera, tanpa *silent failure*, nyatakan asumsi yang memengaruhi hasil).

Detail lengkap: `../maxilun/references/engines.md`.
<!-- CORE-RULES:END -->

## 1. Disiplin Rekayasa Desktop & GUI Threading

1. **Invarian UI Thread**:
   - I/O jaringan, pembacaan berkas besar, dan query database dilarang memblokir message loop utama.
   - Pindahkan komputasi berat ke worker thread; sinkronkan pembaruan visual ke thread utama melalui mekanisme resmi platform (`PostMessage`, `DispatchQueue.main.async`, `QMetaObject::invokeMethod`, atau `Dispatcher.InvokeAsync`).
2. **Siklus Hidup Handle & Memori**:
   - GDI handle, HWND, window controller, dan objek C++ wajib dikelola melalui prinsip RAII (`std::unique_ptr`, smart pointers Qt, ARC Swift, atau `using` C#).
   - Pastikan setiap resource dibebaskan secara deterministik saat window dihancurkan (`WM_DESTROY`, `windowWillClose`, atau event `close`).
3. **DPI & Multi-Monitor**:
   - Terapkan Per-Monitor V2 DPI awareness pada aplikasi Windows. Hitung skala font dan geometri tombol berbasis faktor skala monitor aktif, bukan nilai tetap (*hardcoded pixels*).

## 2. Standar Rekayasa PowerBuilder & DataWindow

Saat bekerja pada sistem PowerBuilder (Appeon atau Sybase PB):
1. **Transaksionalitas `SQLCA`**:
   - Gunakan `dw_1.SetTransObject(SQLCA)` untuk mempertahankan koneksi aktif. Jangan gunakan `SetTrans(SQLCA)` yang membuka dan menutup koneksi berulang pada setiap `Retrieve()`.
   - Jalankan `AcceptText()` sebelum `Update()`. Lakukan pengecekan eksplisit `IF dw_1.Update() = 1 THEN COMMIT ... ELSE ROLLBACK ...` (rujuk `references/powerbuilder-playbook.md`).
2. **Manajemen 4 Buffer DataWindow**:
   - Perlakukan buffer `Primary!`, `Filter!`, `Delete!`, dan `Original!` sesuai integritas transaksi. Hindari manipulasi status baris (`SetItemStatus`) kecuali untuk sinkronisasi rekonsiliasi cache.
3. **Event `ItemChanged`**:
   - Evaluasi nilai baru melalui argumen `data`. Kembalikan kode aksi standar: `0` (terima nilai), `1` (tolak dan pertahankan fokus), atau `2` (tolak dan batalkan perubahan).

## 3. Native Windows, macOS & Lintas Platform (C++ Qt)

1. **Windows (Win32, WPF, WinUI)**:
   - Pada Win32, batasi message procedure (`WndProc`) pada routing event dan delegasikan logika bisnis ke modul terpisah.
   - Pada WPF/WinUI, terapkan arsitektur MVVM murni dengan binding terisolasi dan hindari memory leak dari event handler yang tidak dicabut.
2. **macOS (Swift, AppKit)**:
   - Atur `isReleasedWhenClosed` secara cermat pada `NSWindow`. Patuhi aturan App Sandbox dan hardened runtime saat mengonfigurasi `Entitlements.plist`.
3. **C++ Qt**:
   - Manfaatkan hirarki kepemilikan parent-child `QObject`. Gunakan `Qt::QueuedConnection` saat sinyal dipancarkan melintasi batas worker thread (rujuk `references/native-desktop-patterns.md`).

## 4. Verifikasi & Standar Pelaporan

Setiap penyelesaian tugas desktop wajib ditopang bukti:
- Bukti kompilasi: status build tanpa warning memory leak (`cmake --build`, `msbuild`, `xcodebuild`, atau compile target PB).
- Verifikasi threading: konfirmasi bahwa UI tetap responsif saat proses panjang dijalankan.
- Nyatakan bukti dengan format `[CONFIRMED]` beserta berkas dan baris yang diubah (`file:line`).

## Related Skills

- `maxilun-data`: Optimasi query, indexing, dan skema database yang diakses oleh DataWindow atau desktop ORM.
- `maxilun-verify`: Eksekusi automated desktop UI test atau unit test native (GoogleTest, Catch2, NUnit, XCTest).
- `maxilun-engineer`: Logika algoritma bisnis inti dalam C++, C#, atau Java.
