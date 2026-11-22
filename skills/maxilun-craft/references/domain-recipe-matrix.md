# Domain-to-Recipe Matrix: First-Fold Archetypes & UI Motion Binding

> **Status**: Reference Document  
> **Specialists**: `maxilun-craft`, `maxilun-motion`, & `maxilun-scaffold`  
> **Purpose**: Eliminates guesswork by directly binding domain categories to high-impact Hero Archetypes (`references/hero-section-archetypes.md`), fluid motion recipes (`../maxilun-motion/references/ui-motion-recipes.md`), typography pairings, and authentic seed data.

---

## 1. Domain-to-Recipe Mapping Matrix

| Domain Category | First-Fold Archetype (`hero-section-archetypes.md`) | Micro-Interaction Recipes (`ui-motion-recipes.md`) | Typographic Pairing (`design-archetypes.md`) | Hallmark Theme (`hallmark-themes.md`) | Day-1 Realistic Seed Invariant |
|---|---|---|---|---|---|
| **1. EdTech / School / CBT / LMS** | `HERO-EDTECH-01`: Asymmetric Split-Screen Live Academic Ledger (Ticker status, quick student lookup, announcement ribbon) | `SlidingPillNav` (Section 1), `AccordionItem` (Section 5), `HoldToConfirmButton` (Section 2.A) | `Plus Jakarta Sans` (Display/UI) + `Newsreader` (Editorial) | Theme 12: *Warm Academic Editorial* (`oklch(0.97 0.01 75)` warm paper / deep walnut) | 15 Indonesian student records (NISN, class X-A / XI-IPA, grades, schedule, CBT packages) |
| **2. B2B SaaS / Operational Dashboard** | `HERO-SAAS-02`: Asymmetric Command Workbench (Dual-pane telemetry, live status dot, keyboard shortcut launcher) | `MagneticButton` (Section 2.B), `MultiStepDrawer` (Section 3), `ExpandableDataRow` (Section 5) | `Geist Sans` + `JetBrains Mono` (tabular-nums) | Theme 01: *Obsidian Command Deck* (`oklch(0.12 0.01 260)` deep space / hairline border) | 20 workspace members, tenant roles (Admin, Teacher, Operator), API latency telemetry |
| **3. Administrative / Financial / Cashier** | `HERO-LEDGER-03`: High-Density Tabular Masthead (Zero cards, border-separated data matrix, audit trail) | `SegmentedControl` (Section 1), `AnimatedFilterChips` (Section 1.B), `ReversibleActionToast` | `Space Grotesk` + `Inter` (tabular figures) | Theme 08: *Technical Swiss Ledger* (High-contrast neutral black & crisp paper white) | 30 financial transactions (`BIGINT` IDR / cents), invoice status, reconciliation log |
| **4. E-Commerce / School Store / Booking** | `HERO-COMMERCE-04`: Tangible Showcase Deck (Interactive 3D perspective card tilt, floating price tag, quick cart drawer) | `InteractivePerspectiveCard` (Section 4), `CartFlyAnimation`, `SpringScaleTap` | `Syne` or `Clash Display` + `Inter` | Theme 24: *Tactile Studio Minimal* (Muted stone surfaces with vivid spot accent) | 12 product items (school uniforms, textbook bundles, exam tokens), stock quantities |
| **5. Developer Tools / AI Agent Workbenches** | `HERO-DEVTOOLS-05`: Dark Atmospheric Terminal Sandbox (Live prompt-to-response split, syntax-highlighted code block) | `LiveConsoleStream`, `TokenPillShuffle`, `ShimmerWaveSkeleton` | `Geist Sans` + `Geist Mono` | Theme 03: *Deep Space Terminal* (Rich charcoal `oklch(0.10 0.01 270)`) | 10 execution trace events, model parameters (temperature, max_tokens), latency p95 |

---

## 2. Integration Protocol During Scaffolding

When a new project is bootstrapped via `maxilun-scaffold` / `greenfield.py`:
1. **Identify the Domain**: Map the user's prompt (e.g. "website sekolah", "portal ujian CBT", "sistem absensi") to one of the 5 Domain Categories above.
2. **Inject the Matching Hero Component**:
   - Write the Hero component into `src/components/hero/FirstFoldHero.tsx` (or `index.html` for GAS) using the code blueprint from `references/hero-section-archetypes.md`.
   - Never generate a bare generic centered hero (`LAY-TEL-01`).
3. **Inject the UI Motion Primitives**:
   - Write the designated motion primitives into `src/components/ui/` from `../maxilun-motion/references/ui-motion-recipes.md`.
   - For React/Next.js: use `framer-motion` or CSS spring variables.
   - For GAS/vanilla HTML: use lightweight zero-dependency CSS keyframe animations.
4. **Seed Realistic Domain Data**:
   - Populate the initial state with the Day-1 Realistic Seed Invariant. The app must never render an empty, dead UI upon first launch.
5. **Enforce Mechanical Purity**:
   - Run `slopscan.py` on the generated files to ensure zero emoji icons (`CMP-003`), zero pastel rounded boxes (`CMP-021`), and zero white-box monoculture (`LAY-014`).
