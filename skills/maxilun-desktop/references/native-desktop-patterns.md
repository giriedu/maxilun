# Native Desktop Engineering Patterns (Windows, macOS, C++, Qt)

Production desktop application architecture for Windows (Win32, WPF, WinUI, C++), macOS (Swift, AppKit, Cocoa), and cross-platform toolkits (C++ Qt, Tauri).

## 1. Windows Desktop Engineering

### 1.1 Win32 C++ Patterns & Window Lifecycle
- **Message loop & responsiveness**:
  Never run I/O or intensive computation on the main UI thread. Use `std::thread` or a worker thread pool, then send the result to the UI thread with `PostMessage(hWnd, WM_APP_..., wParam, lParam)`. Do not call UI components directly from a worker thread.
- **DPI awareness (Per-Monitor V2)**:
  Declare DPI awareness in the application manifest to prevent blurry rendering on multi-monitor setups:
  ```xml
  <application xmlns="urn:schemas-microsoft-com:asm.v3">
    <windowsSettings>
      <dpiAwareness xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">PerMonitorV2, PerMonitor</dpiAwareness>
    </windowsSettings>
  </application>
  ```
- **GDI resources & handles**:
  Pair every `CreateCompatibleDC`, `SelectObject`, and `CreateFont` with `DeleteDC`, restoring the previous object, and `DeleteObject`. A GDI handle leak that passes the 10,000 limit hangs the application immediately.

### 1.2 WPF & WinUI 3 (C# / .NET)
- Apply strict MVVM. Use `CommunityToolkit.Mvvm` (`[ObservableProperty]`, `[RelayCommand]`).
- Release event listeners when the window/view closes (`WeakEventManager` or an explicit unregister in `Unloaded`) so the view is not retained indefinitely.
- Use UI virtualization (`VirtualizingStackPanel.IsVirtualizing="True"`) for large data collections.

---

## 2. macOS Desktop Engineering (Swift, AppKit, Cocoa)

### 2.1 Window Management & Lifecycle
- **`NSWindowController` & `NSViewController`**:
  Separate window ownership from view ownership. Set `isReleasedWhenClosed = false` when an ARC-managed controller owns the window, to avoid a use-after-free crash.
- **Menu bar & status item**:
  Use `NSStatusItem` with a dynamic menu. Update visual state only on the main thread (`DispatchQueue.main.async` or `@MainActor`).
- **App Sandbox & notarization**:
  Keep `Entitlements.plist` minimal. Enable hardened runtime before submitting for notarization with `notarytool`:
  ```bash
  xcrun notarytool submit app.zip --keychain-profile "AC_PASSWORD" --wait
  xcrun stapler staple "App.app"
  ```

---

## 3. C++ Qt Architecture (Widgets & QML)

### 3.1 Object Ownership Model (`QObject`)
- Use the `QObject` parent-child ownership tree. A child is deleted automatically when its parent is destroyed.
- Take care with `QPointer` and `deleteLater()` when deleting objects across thread event loops.

### 3.2 Cross-Thread Signals & Slots
- When connecting a signal from a worker thread to the UI thread, use the `Qt::QueuedConnection` connection type (the automatic default when a signal crosses a thread boundary).
- Register signal parameters with the Qt meta-type system (`qRegisterMetaType<T>()`) when they use custom non-primitive types.

### 3.3 Modern CMake Structure for Desktop
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
