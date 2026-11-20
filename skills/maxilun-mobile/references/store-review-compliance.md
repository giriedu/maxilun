# Store Review Compliance: Rejection Prevention for App Store and Google Play

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun-mobile/SKILL.md"
  origin: "Maxilun Mobile Engine"
-->

Use this file before any build goes to App Store Connect or the Play Console, or when a review rejection arrives. It maps the recurring rejection classes to the exact file, config key, or console form that decides them, and turns each one into a gate that can be checked from the repository or the built artifact instead of from memory. Store policies move every year: treat every deadline or version number here as "verify against the live policy page on the day of submission", and record the date you checked.

---

## 1. Operating Rules

1. **The artifact is the truth, not the source tree.** Review sees the merged manifest, the final `Info.plist`, and the linked SDKs. Library merges add permissions and plugins add API usage the app code never mentions. Inspect the build output (`.ipa`, `.aab`), not only the project files.
2. **Declarations must match behavior in both directions.** Under-declaring (collecting data not disclosed) is a policy violation; over-declaring (permissions or entitlements the app never uses) is also a rejection class on both stores. The gate is equality, not "at least".
3. **One owner per declaration.** Privacy manifest, purpose strings, Data safety form, and privacy policy must describe the same data flows. Keep a single data inventory (data type, purpose, SDK or endpoint, linked to user, used for tracking) in the repo and derive every store form from it.
4. **Evidence gate.** A compliance claim is `[CONFIRMED]` only with the command output or file:line that proves it. Console-only forms (Data safety, App Privacy labels, permission declarations) are `[UNVERIFIED]` until someone with console access confirms the submitted values match the inventory.
5. **Policy facts expire.** Never hardcode "current target API level" or "minimum Xcode" in CI without a dated comment and an owner; stale thresholds produce false passes.

---

## 2. Rejection Classes: Apple App Store

Section numbers below refer to the public App Store Review Guidelines.

| Class | Guideline | What decides it | Typical failure |
|---|---|---|---|
| Incomplete app, crashes, placeholder content | 2.1 | Build on a clean device, reviewer path | Login wall without demo credentials; staging backend; "coming soon" screens |
| Inaccurate metadata | 2.3 | Screenshots, description, keywords, What's New | Screenshots of features not in the build; competitor or other-platform names; promised future features |
| Non-public API, downloaded executable code | 2.5.1, 2.5.2 | Linked symbols, OTA update scope | Private selectors in a dependency; OTA bundle that changes the app's primary purpose |
| In-app purchase for digital goods | 3.1.1 | Purchase flow, external links | Card form or web checkout for digital content outside an approved entitlement; no restore mechanism for non-consumables or subscriptions |
| Subscription clarity | 3.1.2 | Paywall screen | Price per period, trial length, and auto-renew terms not visible before the purchase button |
| Minimum functionality, web wrappers | 4.2 | Native value beyond a website | Single `WKWebView` pointing at the marketing site |
| Login service parity | 4.8 | Sign-in screen | Third-party social login offered without an equivalent privacy-focused option (limited data, private email relay, no ad tracking) |
| Data collection and purpose strings | 5.1.1 | `Info.plist`, permission timing | Missing or vague usage description; permission requested at launch instead of in context; data required that the feature does not need |
| Account deletion | 5.1.1(v) | Settings screen | App creates accounts but offers only "deactivate" or "email support"; deletion hidden behind a website with no in-app path |
| Tracking and sharing | 5.1.2 | ATT prompt, SDK behavior | IDFA or cross-app tracking before `ATTrackingManager` authorization; tracking domains contacted after denial |

### 2.1 Privacy manifest and required-reason APIs
- `PrivacyInfo.xcprivacy` must exist in the app target and in every third-party SDK that touches covered data or APIs. A missing reason for a used API produces an automated `ITMS-91053` email at upload time.
- Required-reason API categories: file timestamps, system boot time, disk space, active keyboards, and `UserDefaults`. Each entry in `NSPrivacyAccessedAPITypes` pairs an `NSPrivacyAccessedAPIType` with one or more approved reason codes in `NSPrivacyAccessedAPITypeReasons`. Pick the code whose documented meaning matches the real use; a mismatched code is a false declaration, not a formality.
- `NSPrivacyTracking` must be `true` if any tracking happens, and `NSPrivacyTrackingDomains` must list every domain used for it, because the system blocks those domains when the user denies tracking. Test the denied path: the app must still work.
- `NSPrivacyCollectedDataTypes` must agree with the App Privacy label in App Store Connect.
- Cross-platform builds: Flutter plugins, React Native native modules, and Capacitor plugins ship their own manifests or none at all. Audit the aggregated privacy report (Xcode Organizer, "Generate Privacy Report") of the archive, not the plugin README.

### 2.2 Purpose strings
- Every protected resource the binary can request needs its key: `NSCameraUsageDescription`, `NSMicrophoneUsageDescription`, `NSPhotoLibraryUsageDescription`, `NSPhotoLibraryAddUsageDescription`, `NSLocationWhenInUseUsageDescription`, `NSLocationAlwaysAndWhenInUseUsageDescription`, `NSContactsUsageDescription`, `NSBluetoothAlwaysUsageDescription`, `NSFaceIDUsageDescription`, `NSUserTrackingUsageDescription`. A missing key crashes the app on access and fails upload validation (`ITMS-90683`).
- A string passes review when it names the feature and the user benefit: "Scan receipts to fill in expense amounts" passes; "This app needs camera access" does not.
- Localize the strings in `InfoPlist.strings` for every shipped locale; an English-only string in a localized app reads as a defect.
- Remove keys for capabilities the app dropped; a stale key invites the reviewer to ask where the feature is.

### 2.3 Payments decision table

| Selling | iOS path |
|---|---|
| Digital content, features, subscriptions consumed in the app | StoreKit in-app purchase, with restore |
| Physical goods or services consumed outside the app | Any payment processor; IAP not allowed |
| Reader content bought elsewhere (media, books, accounts) | Account login allowed; external link only with the dedicated entitlement and its storefront rules |
| External purchase links or alternative processors | Only under storefront-specific entitlements; terms differ by region and have changed through litigation and regulation. Gate the link by storefront at runtime and re-read the current terms before each release |
| Person-to-person tips, donations to approved nonprofits | Check the specific clause; defaults differ from general digital goods |

### 2.4 Review readiness
- Demo account with seeded data, not expiring before review ends, in App Review Information; plus notes for any hardware, region, or feature flag the reviewer needs.
- Production backend reachable from the reviewer's region; no IP allowlists or VPN-only endpoints.
- `ITSAppUsesNonExemptEncryption` set in `Info.plist` so every upload does not stall on the export compliance question.
- Entitlements file (`*.entitlements`) contains only capabilities with a shipped feature behind them.
- Build with the Xcode and SDK version currently required for uploads; Apple raises the floor periodically.

---

## 3. Rejection Classes: Google Play

| Class | What decides it | Typical failure |
|---|---|---|
| Target API level | `targetSdk` in the merged manifest | Update rejected at upload because the target is older than the yearly requirement (new apps and updates must target within roughly one year of the latest major Android release) |
| Data safety mismatch | Console Data safety form vs SDK behavior | Analytics, crash, or ad SDK collects device identifiers that the form says are not collected |
| Account deletion | Console account deletion URL plus in-app path | App allows account creation but provides no web link where users can request deletion without reinstalling |
| Prominent disclosure | In-app screen before the runtime prompt | Personal or sensitive data collected without an in-app disclosure that states what, why, and how it is used |
| Background location | `ACCESS_BACKGROUND_LOCATION`, console declaration, demo video | Background location used for a feature that works in the foreground, or no disclosure video |
| Restricted permissions | Merged manifest | `QUERY_ALL_PACKAGES`, `MANAGE_EXTERNAL_STORAGE`, SMS and call log groups, `READ_MEDIA_IMAGES`/`READ_MEDIA_VIDEO` for one-off picks, `USE_EXACT_ALARM` without a qualifying core use |
| Foreground service types | `foregroundServiceType` on each `<service>`, console declaration | Android 14+ target without declared types, or a type that does not match the work performed |
| Play Billing | Billing library version, purchase flow | Digital goods sold outside Play Billing where not permitted; billing library version past its deprecation date |
| Misleading listing | Store listing, icon, screenshots | Keyword stuffing, ranking claims, imitation of another app's branding |
| Release hygiene | Built artifact | `android:debuggable="true"`, missing 64-bit native libraries, native libraries not aligned for 16 KB page sizes when targeting recent Android versions |
| Testing gate for new personal accounts | Console testing track | Production access requested before the required closed test (minimum testers over a minimum continuous period) has run |

### 3.1 Permission discipline
- Prefer the platform alternative that needs no permission: Photo Picker over media read permissions, Contact Picker intents over `READ_CONTACTS`, `<queries>` with explicit packages or intent filters over `QUERY_ALL_PACKAGES`, Storage Access Framework over all-files access, coarse location over fine where the feature allows.
- Strip permissions contributed by libraries you do not need in the app manifest with `tools:node="remove"`, then confirm in the merged manifest.
- Each dangerous permission gets an in-context rationale screen before the system dialog, and the feature degrades gracefully on denial.

### 3.2 Data safety as an inventory export
- Maintain the data inventory (section 1, rule 3) per SDK version. When an SDK upgrade changes collection behavior, the PR that bumps it must update the inventory; the console form is then updated from the inventory in the same release.
- "Data encrypted in transit" and "users can request deletion" are claims; back them with the network security config (no cleartext) and the deletion endpoint.

---

## 4. Cross-Store Classes

- **Privacy policy URL** reachable (HTTP 200, no login), linked in both consoles and inside the app, and naming the same data types as the manifests and forms.
- **User-generated content**: report, block, content filtering, and published contact info before launch, on both stores.
- **Kids and families audience**: no behavioral advertising SDKs, no third-party analytics that collect identifiers, a parental gate before external links or purchases. Choose the audience deliberately; a "13+" declaration does not cancel a kid-appealing listing.
- **Subscriptions**: cancellation path at least as easy as signup, regional withdrawal or cancellation rules honored, no dark-pattern trial disclosure.
- **Loot boxes and randomized paid items**: disclose odds before purchase.
- **Hidden or dormant features**: remote flags may toggle features, but not unlock functionality the reviewer could not see or that changes the app's category.
- **OTA updates (React Native, Expo, Capacitor)**: allowed for interpreted JS bug fixes and content; not for shipping new native capabilities or changing the app's purpose. Document the OTA policy in review notes when the reviewer could notice behavior changing.

---

## 5. Pre-Submission Gates

Each gate names the input it inspects and a machine-checkable pass condition. Run on the release artifact in CI; console-only items stay manual with a named owner.

| Gate | Input | Pass condition |
|---|---|---|
| Purpose strings | Built `Info.plist` | Every framework-implied usage key present, non-empty, longer than a template sentence |
| Privacy manifest | `PrivacyInfo.xcprivacy` in app and each embedded framework | File present; every required-reason API symbol found in the binary has a matching category entry |
| Tracking consistency | Manifest plus SDK list | `NSPrivacyTracking` true iff any tracking SDK linked; domains listed |
| Entitlements | `codesign -d --entitlements :- App.app` | Only allowlisted capabilities |
| Export compliance | `Info.plist` | `ITSAppUsesNonExemptEncryption` present |
| Target SDK | Merged manifest from `bundletool dump manifest` | `targetSdkVersion` meets the dated threshold in the repo config |
| Permission allowlist | Merged manifest | Permission set equals the reviewed allowlist; diffs fail the build until reviewed |
| Release flags | Merged manifest, `build.gradle(.kts)` | Not debuggable; cleartext disabled or scoped; minify enabled for release |
| Native ABI and alignment | AAB contents | `arm64-v8a` present for every native library; alignment check passes |
| Account deletion | App routes plus web URL | In-app deletion entry reachable from settings; web URL returns 200 |
| Metadata | Store listing export (fastlane `metadata/` or equivalent) | No other-platform names, no placeholder text, every URL reachable |
| Review notes | Release checklist | Demo account valid through review window; notes cover gated features |

### 5.1 Example gate: iOS purpose strings from the built app
```python
# ci/check_usage_strings.py -- run against the .app inside the archive
import plistlib, subprocess, sys, pathlib

FRAMEWORK_KEYS = {
    "AVFoundation": ["NSCameraUsageDescription", "NSMicrophoneUsageDescription"],
    "CoreLocation": ["NSLocationWhenInUseUsageDescription"],
    "Contacts": ["NSContactsUsageDescription"],
    "AppTrackingTransparency": ["NSUserTrackingUsageDescription"],
}

app = pathlib.Path(sys.argv[1])
info = plistlib.loads((app / "Info.plist").read_bytes())
binary = app / info["CFBundleExecutable"]
linked = subprocess.run(["otool", "-L", str(binary)], capture_output=True, text=True).stdout

failures = []
for framework, keys in FRAMEWORK_KEYS.items():
    if f"/{framework}.framework/" not in linked:
        continue
    for key in keys:
        text = str(info.get(key, "")).strip()
        if len(text) < 25:
            failures.append(f"{key}: missing or too vague for linked {framework}")

print("\n".join(failures) or "usage strings: ok")
sys.exit(1 if failures else 0)
```
Linking a framework does not prove a permission is requested (AVFoundation is linked for playback too), so treat a hit as "review required" and allow a reviewed exception file rather than adding fake strings.

### 5.2 Example gate: Android permission allowlist on the merged manifest
```python
# ci/check_permissions.py <merged AndroidManifest.xml> <allowlist.txt>
import sys, xml.etree.ElementTree as ET

ANDROID = "{http://schemas.android.com/apk/res/android}"
root = ET.parse(sys.argv[1]).getroot()
declared = {p.get(ANDROID + "name") for p in root.iter("uses-permission")}
allowed = {l.strip() for l in open(sys.argv[2]) if l.strip() and not l.startswith("#")}

added, removed = declared - allowed, allowed - declared
for p in sorted(added):
    print(f"NEW permission not reviewed: {p}")
for p in sorted(removed):
    print(f"allowlist entry no longer declared (update Data safety?): {p}")
sys.exit(1 if added else 0)
```
The allowlist lives next to the data inventory; changing it requires the same reviewer who owns the Data safety form.

---

## 6. CI Placement

- **On every PR touching manifests, Gradle, Podfile, `pubspec.yaml`, or `package.json`**: permission allowlist diff, entitlements diff, SDK inventory diff. Cheap and catches library-merged changes early.
- **On release builds only**: artifact-level gates (privacy report, ABI, alignment, debuggable, export flag) because they need the signed output.
- **Weekly, not per build**: reachability of privacy policy, support, and deletion URLs; dated thresholds approaching expiry (flag 60 days before a known store deadline).
- Fail closed on parse errors: a gate that could not read its input is a failure, never a silent pass.
- No hook that silently blocks the submit command with an environment-variable override as the only escape; failures go to the CI report with the file and the fix.

---

## 7. Responding to a Rejection

1. Copy the cited guideline and the reviewer's exact wording into the ticket; do not paraphrase.
2. Reproduce on the reviewer's device class and OS version with the build number they reviewed.
3. Fix the cause in the artifact, add the matching gate from section 5 so it cannot regress, then reply in Resolution Center (Apple) or the policy status page (Play) with what changed and where to find it.
4. Appeal only when the build demonstrably complies; cite the screen and steps. An appeal is not a substitute for a missing disclosure.

---

## 8. Handoffs

- Token storage, certificate pinning, and data-at-rest encryption claims behind the privacy forms: `maxilun-sentinel`.
- Running the gates and instrumentation tests before release: `maxilun-verify`.
- Store listing copy, screenshot captions, and purpose-string wording: `maxilun-content`.
- Release pipelines that host these gates (fastlane lanes, Gradle tasks, CI runners): `maxilun-deploy`.
