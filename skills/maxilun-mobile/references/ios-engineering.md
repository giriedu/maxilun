# iOS Native Engineering Playbook (Swift, SwiftUI, UIKit, SPM)

Engineering guide for production native iOS apps: modern Swift, declarative SwiftUI, safe concurrency, and App Store compliance.

## 1. SwiftUI Architecture & Swift Concurrency

### 1.1 Modern Concurrency (`async/await` & `@MainActor`)
- **UI thread isolation**: Annotate every view model or presenter that modifies UI state with `@MainActor`.
- **`Sendable` protocol**: Make data models that cross concurrency tasks conform to `Sendable` to prevent data races.
- **Modern view model pattern**:
  ```swift
  import SwiftUI

  @MainActor
  @Observable
  final class UserProfileViewModel {
      private(set) var state: ViewState = .idle
      private let userService: UserServiceProtocol

      init(userService: UserServiceProtocol) {
          self.userService = userService
      }

      func loadProfile(userId: String) async {
          state = .loading
          do {
              let profile = try await userService.fetchProfile(id: userId)
              state = .success(profile)
          } catch {
              state = .failure(error.localizedDescription)
          }
      }
  }
  ```

---

## 2. Memory Management & Retain Cycle Prevention

- **`[weak self]` clause**: Always use `[weak self]` in escaping closures, delegate listeners, or Combine subscribers that could retain a controller/view instance.
- **Deinitialization audit**: Add `deinit { print("\(Self.self) deallocated") }` during manual testing to prove memory is released when the controller closes.
- **Weak delegates**: Declare every delegate protocol so it can be held `weak`:
  ```swift
  protocol OrderStatusDelegate: AnyObject {
      func orderDidComplete(_ order: Order)
  }
  ```

---

## 3. Persistence & Data Security (Keychain)

- **Keychain Services**: Store authentication tokens, private certificates, and sensitive data in the iOS Keychain with the `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` attribute. Never store a token in `UserDefaults`.
- **SwiftData / CoreData**: Run batch inserts or large fetches on a separate background context (an isolated `ModelContext`) so the UI does not stutter.

---

## 4. Privacy Compliance & Release (Privacy Manifest)

- **`PrivacyInfo.xcprivacy`**: List every API declaration with an Apple-approved reason (NSPrivacyAccessedAPITypeDiskSpace, SystemBootTime, etc.) and the third-party network tracking domains.
- **Fastlane & notarization**: Automate certificate signing with match, unit tests with `scan`, and TestFlight distribution with `gym` + `pilot`.
