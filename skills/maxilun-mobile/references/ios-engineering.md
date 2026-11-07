# iOS Native Engineering Playbook (Swift, SwiftUI, UIKit, SPM)

Panduan rekayasa aplikasi iOS native produksi berbasis Swift modern, SwiftUI deklaratif, konkurensi aman, dan kepatuhan App Store.

## 1. Arsitektur SwiftUI & Swift Concurrency

### 1.1 Konkurensi Modern (`async/await` & `@MainActor`)
- **Isolasi UI Thread**: Setiap view model atau presenter yang memodifikasi state antarmuka wajib dianotasi `@MainActor`.
- **Protokol `Sendable`**: Pastikan model data yang ditransfer lintas task konkurensi mematuhi aturan `Sendable` untuk mencegah *data races*.
- **Pola View Model Modern**:
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

## 2. Manajemen Memori & Pencegahan Retain Cycles

- **Klausul `[weak self]`**: Selalu gunakan `[weak self]` pada escaping closure, listener delegat, atau Combine subscriber yang berpotensi mempertahankan instance controller/view.
- **Audit Deinitialization**: Pasangkan `deinit { print("\(Self.self) deallocated") }` pada pengujian manual untuk membuktikan pembebasan memori saat controller ditutup.
- **Delegat Lemah (*Weak Delegates*)**: Setiap protokol delegat wajib dideklarasikan `weak`:
  ```swift
  protocol OrderStatusDelegate: AnyObject {
      func orderDidComplete(_ order: Order)
  }
  ```

---

## 3. Persistensi & Keamanan Data (Keychain)

- **Keychain Services**: Token otentikasi, sertifikat privat, dan data sensitif wajib disimpan di iOS Keychain dengan atribut `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly`. Dilarang menyimpan token di `UserDefaults`.
- **SwiftData / CoreData**: Jalankan operasi batch insert atau fetch besar pada konteks background terpisah (`ModelContext` terisolasi) agar UI tidak stuttering.

---

## 4. Kepatuhan Privasi & Rilis (Privacy Manifest)

- **`PrivacyInfo.xcprivacy`**: Cantumkan seluruh deklarasi API dengan alasan yang disetujui Apple (NSPrivacyAccessedAPITypeDiskSpace, SystemBootTime, dll.) dan pelacak domain jaringan pihak ketiga.
- **Fastlane & Notarisasi**: Otomatiskan penandatanganan sertifikat dengan match, pengujian unit via `scan`, dan distribusi TestFlight via `gym` + `pilot`.
