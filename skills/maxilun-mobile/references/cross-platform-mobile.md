# Cross-Platform Mobile Engineering (Flutter, React Native, KMP)

Engineering guide for cross-platform mobile apps, focused on native performance, deterministic state architecture, and platform bridge communication.

## 1. Flutter & Dart Engineering

### 1.1 Widget Tree & State Optimization
- **`const` constructors**: Mark every widget that does not depend on dynamic variables as `const` to cut allocations during rebuilds.
- **Isolates for computation & JSON parsing**:
  Use `compute()` or `Isolate.run()` when parsing large JSON or compressing images, so the frame rate holds at 60/120 FPS:
  ```dart
  Future<List<Item>> parseItems(String rawJson) async {
    return await Isolate.run(() => parseJsonInBackground(rawJson));
  }
  ```
- **Platform channels**: Validate data types on every `MethodChannel`. Return a structured error through `PlatformException` when a native integration fails.

---

## 2. React Native (New Architecture & Hermes)

- **Fabric & TurboModules**: Migrate native modules to C++ JSI / TurboModules to remove the asynchronous JSON serialization overhead of the legacy bridge.
- **Animations on the UI thread**: Use `react-native-reanimated` and `react-native-gesture-handler`. Run gesture transitions directly on the UI thread without going through the JS thread.
- **List management**: Use `@shopify/flash-list` instead of the conventional `FlatList` for repeating data lists, so views are recycled immediately.

---

## 3. Kotlin Multiplatform (KMP)

- **Shared logic boundary**: Share domain logic, repositories, validation, the network client (`Ktor`), and the database (`SQLDelight`). Keep the presentation layer native (Compose on Android, SwiftUI on iOS).
- **`expect` / `actual` declarations**: Limit `expect`/`actual` to points that truly need a platform-specific API (UUID generator, secure storage, sensors).
