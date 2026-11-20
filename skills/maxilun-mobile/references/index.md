# Maxilun Mobile References Index

Index of references for native and cross-platform mobile engineering.

## Domain Reference Files

1. **`android-engineering.md`**:
   Kotlin, Jetpack Compose, ViewModel StateFlow, Room database migrations, WorkManager background jobs, Android 13+ runtime permissions, and R8/ProGuard configuration.
2. **`ios-engineering.md`**:
   Modern Swift, SwiftUI, `@MainActor` & Task concurrency, retain cycle elimination (`[weak self]`), Keychain Services integration, and Privacy Manifest compliance.
3. **`cross-platform-mobile.md`**:
   Flutter Dart isolates & widget tree optimization, React Native New Architecture (Fabric/TurboModules), and Kotlin Multiplatform (KMP) shared logic architecture.
4. **`store-review-compliance.md`**:
   App Store and Google Play rejection classes (privacy manifest and required-reason APIs, purpose strings, account deletion, payments, sign-in parity, Data safety, target SDK, background location) as artifact-level pre-submission gates with CI timing and a rejection-response loop.

## Loading Guide
- Native Android project → read `references/android-engineering.md`.
- Native iOS project → read `references/ios-engineering.md`.
- Flutter, React Native, or KMP project → read `references/cross-platform-mobile.md`.
- Preparing any store submission or answering a review rejection → read `references/store-review-compliance.md`.
