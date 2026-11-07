# Native Desktop Engineering Patterns (Windows, macOS, C++, Qt)

Arsitektur aplikasi desktop tingkat produksi untuk Windows (Win32, WPF, WinUI, C++), macOS (Swift, AppKit, Cocoa), dan lintas platform (C++ Qt, Tauri).

## 1. Windows Desktop Engineering

### 1.1 Pola Win32 C++ & Manajemen Siklus Window
- **Message Loop & Responsivitas**:
  Pekerjaan I/O atau komputasi intensif dilarang berjalan di thread antarmuka utama (UI thread). Gunakan `std::thread` atau thread pool worker, lalu kirim hasil ke UI thread melalui `PostMessage(hWnd, WM_APP_..., wParam, lParam)` — jangan panggil komponen UI langsung dari worker thread.
- **DPI Awareness (Per-Monitor V2)**:
  Wajib mendeklarasikan DPI awareness pada manifest aplikasi untuk mencegah visual blur pada setup multi-monitor:
  ```xml
  <application xmlns="urn:schemas-microsoft-com:asm.v3">
    <windowsSettings>
      <dpiAwareness xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">PerMonitorV2, PerMonitor</dpiAwareness>
    </windowsSettings>
  </application>
  ```
- **Alokasi Sumber Daya GDI & Handle**:
  Setiap `CreateCompatibleDC`, `SelectObject`, dan `CreateFont` wajib dipasangkan dengan `DeleteDC`, pemulihan objek lama, dan `DeleteObject`. Kebocoran GDI handle melampaui limit 10.000 memicu aplikasi hang seketika.

### 1.2 WPF & WinUI 3 (C# / .NET)
- Terapkan pola MVVM ketat. Gunakan `CommunityToolkit.Mvvm` (`[ObservableProperty]`, `[RelayCommand]`).
- Bebaskan event listener saat window/view ditutup (`WeakEventManager` atau unregister eksplisit di `Unloaded`) guna mencegah retensi memori tak berujung.
- Gunakan virtualisasi antarmuka (`VirtualizingStackPanel.IsVirtualizing="True"`) pada koleksi data besar.

---

## 2. macOS Desktop Engineering (Swift, AppKit, Cocoa)

### 2.1 Manajemen Window & Siklus Hidup
- **`NSWindowController` & `NSViewController`**:
  Pisahkan kepemilikan window dengan view. Pastikan `isReleasedWhenClosed = false` jika window dikelola oleh ARC controller untuk menghindari crash akses pointer bebas (*use-after-free*).
- **Menu Bar & Status Item**:
  Gunakan `NSStatusItem` dengan menu dinamis. Perbarui state visual hanya di thread utama (`DispatchQueue.main.async` atau `@MainActor`).
- **App Sandbox & Notarisasi**:
  Konfigurasikan `Entitlements.plist` minimal. Hardened runtime wajib aktif sebelum submit notarization via `notarytool`:
  ```bash
  xcrun notarytool submit app.zip --keychain-profile "AC_PASSWORD" --wait
  xcrun stapler staple "App.app"
  ```

---

## 3. C++ Qt Architecture (Widgets & QML)

### 3.1 Model Kepemilikan Objek (`QObject`)
- Manfaatkan pohon kepemilikan parent-child `QObject`. Child otomatis dihapus saat parent dihancurkan.
- Hati-hati dengan `QPointer` dan `deleteLater()` saat menghapus objek lintas event loop thread.

### 3.2 Sinyal & Slot Lintas Thread
- Saat menghubungkan sinyal dari worker thread ke UI thread, gunakan tipe koneksi `Qt::QueuedConnection` (default otomatis jika sinyal melintasi batas thread).
- Parameter sinyal wajib terdaftar dalam sistem meta-tipe Qt (`qRegisterMetaType<T>()`) jika menggunakan tipe data kustom non-primitif.

### 3.3 Struktur CMake Modern untuk Desktop
```cmake
cmake_minimum_required(VERSION 3.20)
project(DesktopApp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets)
qt_standard_project_setup()

add_executable(DesktopApp src/main.cpp src/mainwindow.cpp)
target_link_libraries(DesktopApp PRIVATE Qt6::Core Qt6::Gui Qt6::Widgets)
```
