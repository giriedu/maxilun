# Platform Surface Specifications: Native iOS & Android Ergonomics

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine"
-->

Native interface engineering specifications for the iOS and Android mobile platforms. Build apps on the real conventions of each platform. Do not wrap a raw web view inside a phone screen.

---

## 1. Core Principle: The Interface IS the Object

Do not compose the app as a monotonous row of statistic tiles (*dashboard stat tiles*). Instead:

1. **One Core Control Object**:
   - Center every screen on one interactive physical representation of the app's main function:
     - Sleep tracker app: a circular night clock the user drags to set the sleep target.
     - Finance app: one continuous cash-flow chart that responds to finger swipes.
     - Boutique lodging app: an arched architectural frame (*arch mask*) that frames the atmosphere of the place before the price figure.
2. **Secondary Elements Orbit**:
   - Arrange all filters, action buttons, and detail data quietly around that core object. They must not compete with it for visual hierarchy.

---

## 2. Native iOS Specifications (SwiftUI & UIKit)

1. **Safe Area Discipline**:
   - Keep interactive content, buttons, and forms inside the Safe Area bounds (`safeAreaPadding()`).
   - Only decorative background images and visual media may cross the Safe Area bounds (`ignoresSafeArea()`).
2. **Translucent Material (Liquid Glass)**:
   - Use built-in system materials (`.ultraThinMaterial`, `.regularMaterial`) for the top navigation bar and the bottom tab bar, so content behind the bars keeps spatial depth while scrolling.
3. **Dynamic Type Compliance**:
   - Do not lock text size to an absolute number without scaling. Use semantic text styles (`.title`, `.headline`, `.body`, `.caption`) so type adapts automatically when the user changes the text-size preference in iOS settings.
4. **Minimum Touch Target $44\text{pt}$**:
   - Give every tappable control a touch box of at least $44 \times 44\text{pt}$.
5. **Native System Navigation**:
   - Prefer the native `NavigationStack` so the *interactive swipe-back gesture* works naturally without visual glitches.

---

## 3. Native Android Specifications (Jetpack Compose & Material 3 Expressive)

1. **Tonal Elevation (Not Heavy Drop Shadows)**:
   - Material 3 expresses spatial depth through tonal surface color levels (`surfaceContainerLowest`, `surfaceContainerLow`, `surfaceContainer`, `surfaceContainerHigh`), not through dirty, pitch-black shadows.
2. **Minimum Touch Target $48\text{dp}$**:
   - Give every button or touch interaction area at least $48 \times 48\text{dp}$ to accommodate different fingertip sizes.
3. **Predictive Back Gesture Support**:
   - Integrate the modern Android navigation API that supports the *predictive back animation* preview before the user lifts the finger from the screen edge.
4. **Automatic Virtual Keyboard Handling**:
   - Apply keyboard inset padding (`WindowInsets.ime` or `imePadding()`) to every input form so the device's virtual keyboard never covers the field being typed in.

---

## 4. Platform Comparison Quick Matrix

| Design Parameter | iOS Standard (SwiftUI) | Android Standard (Material 3) |
|---|---|---|
| **Minimum Touch Target** | $44 \times 44\text{pt}$ | $48 \times 48\text{dp}$ |
| **Navigation Material** | Translucent `.ultraThinMaterial` | Tonal surface tint (accent color at subtle opacity) |
| **Depth Separator** | $1\text{px}$ hairline border / background blur | Saturation/luminance difference between container levels |
| **Input Text Size** | At least $16\text{pt}$ (prevents auto-zoom) | At least $16\text{sp}$ |
| **Primary Navigation Gesture** | Left edge swipe (*edge swipe-back*) | Adaptive edge gesture (*Predictive Back*) |
| **Floating Action** | Floating bottom bar or toolbar | Standardized Floating Action Button (FAB) |
