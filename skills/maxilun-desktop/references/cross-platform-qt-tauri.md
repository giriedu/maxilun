# Cross-Platform Desktop GUI, Tauri & Packaging Playbook

Architecture standards for cross-platform desktop applications (C++ Qt, Tauri/Rust), multi-thread GUI event loops, High-DPI awareness, and native installer packaging.

---

## 1. Qt6 C++ GUI Architecture & Threading

### QObject Ownership & Parent-Child Tree
1. **Deterministic Memory Management**:
   - Assign parents to every `QObject` (`QWidget`, `QTimer`, `QNetworkAccessManager`). When the parent is deleted, all children are freed automatically in reverse order of creation.
   - For standalone heap allocations without a parent, use `std::unique_ptr<T>` rather than raw pointers.

### Cross-Thread Signal and Slot Dispatch
Never touch QWidget UI methods directly from a background `QThread` or worker pool:

```cpp
// Correct: QueuedConnection marshals invocation to the GUI thread event loop
connect(worker, &WorkerThread::dataReady,
        uiController, &UIController::updateDisplay,
        Qt::QueuedConnection);

// Invariant: Custom types passed via QueuedConnection must be registered:
qRegisterMetaType<InvoiceRecord>("InvoiceRecord");
```

---

## 2. Tauri 2.0 (Rust + Webview) Architecture

Tauri provides lightweight native applications using the OS-provided webview instead of bundled Chromium:

### Safe Command Invocation
Declare typed commands in Rust and consume them through type-safe bindings:

```rust
// src-tauri/src/commands.rs
#[tauri::command]
pub async fn calculate_checksum(
    file_path: String,
    state: tauri::State<'_, AppState>,
) -> Result<String, String> {
    // Run disk I/O off the async runtime thread
    tokio::task::spawn_blocking(move || {
        compute_sha256(&file_path)
    })
    .await
    .map_err(|e| e.to_string())?
}
```

### Frontend State Invariant
- Never store authoritative state solely in the webview DOM. The Rust backend maintains application state; the frontend acts as a rendering projection.
- Keep event payloads lean (`<= 1MB`). Stream large binary datasets via file handles or chunks rather than base64 strings across the IPC bridge.

---

## 3. High-DPI Awareness & Window Ergonomics

1. **Per-Monitor V2 Awareness (Windows)**:
   - Configure application manifest with `<dpiAwareness>PerMonitorV2</dpiAwareness>`.
   - Never hardcode pixel coordinates. In Qt, rely on `QStyle::pixelMetric` and layout managers (`QHBoxLayout`, `QGridLayout`).
2. **macOS Retina & App Sandbox**:
   - Provide `@2x` and `@3x` asset scales in asset catalogs.
   - Set `isReleasedWhenClosed = false` on windows that preserve background state, and properly clean up window delegates.

---

## 4. Installer Packaging & Distribution Standards

| Platform | Recommended Format | Tooling | Invariant |
|---|---|---|---|
| **Windows** | MSI / InnoSetup | WiX Toolset v4, InnoSetup 6 | Must support clean uninstall without orphan registry keys. Sign with Authenticode. |
| **macOS** | DMG / PKG | create-dmg, `codesign`, `xcrun notarytool` | Must be notarized with Apple Developer certificate and hardened runtime enabled. |
| **Linux** | AppImage / Flatpak | appimagetool, flatpak-builder | Must bundle dependencies without relying on host glibc version above minimum target. |

```bash
# macOS codesign and notarization verification
codesign --deep --force --verify --verbose --options runtime \
  --sign "Developer ID Application: Company" "dist/MyApp.app"
xcrun notarytool submit "dist/MyApp.dmg" --keychain-profile "notarytool-profile" --wait
```
