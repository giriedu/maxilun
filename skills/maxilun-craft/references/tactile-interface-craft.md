# Tactile Interface Craft, Stress Testing & Variants

Small-detail engineering standards for `maxilun-craft`, `maxilun-motion`, `maxilun-ui-designer`, and `maxilun-ui-reviewer`.

## 1. Interruptible Motion & Transitions
- **CSS Transitions for interactive state** (`hover`, `toggle`, `drawer`, `accordion`): Transitions interpolate toward the latest target and retarget cleanly mid-flight when a user reverses intent.
- **CSS Keyframes only for staged one-shot sequences** (initial mount, loading shimmer): Never use keyframe animations on interactive toggles where mid-flight reversal causes a jump.
- **Tactile scale & compositor safety**: Animate only `transform` and `opacity`; apply subtle `scale(0.96)` press feedback under `@media (hover: hover)` and disable non-essential motion under `@media (prefers-reduced-motion: reduce)`.

## 2. Optical Alignment, Hit Areas & Surfaces
- **Expanded invisible hit targets**: Keep visual icon buttons crisp (`24px`–`32px`) while expanding their clickable hit area to `>= 44x44px` (`48dp` mobile) via padding or a pseudo-element (`::after { inset: -8px; }`).
- **Icon optical balance**: Center play triangles `+1px`–`+2px` right; match icon stroke weight to adjacent typography weight and keep one monochrome `stroke="currentColor"` SVG family (resolve icons with `scripts/icon_lookup.py` rather than guessing SVG paths).
- **Typography micro-polish**: Apply `font-variant-numeric: tabular-nums` on numbers/prices/timers, `text-wrap: balance` on headings, and `text-wrap: pretty` on body paragraphs.
- **Surfaces & borders**: Prefer crisp `1px` hairline borders (`oklch` low-contrast neutral) or subtle multi-layered shadows over heavy single-blur drop shadows; enforce concentric inner radius $R_{inner} = \max(0, R_{outer} - padding - border)$.

## 3. Component Stress-Testing & State Machine Completeness
Before signing off on any component, verify:
- **Extreme content**: 1-character labels, 120-character overflowing titles (`min-w-0` + `truncate` or `break-words`), missing optional fields, and `0` / negative / 9-digit numbers.
- **Viewport & zoom floor**: Nothing clips, overlaps, or leaks horizontal scroll at `320px`–`375px` width or `200%` browser zoom.
- **Full state matrix**: Every interactive flow defines `Idle`, `Loading (CLS=0)`, `Populated`, `Empty + Primary CTA`, `Pending (double-submit guarded)`, and `Error + Recovery CTA`, with zero color-only status indicators.

## 4. Single-Axis Variant Exploration
When exploring multiple UI directions for the same brief:
- Vary **one primary axis** per set (Structure, Density, Emphasis, Typography, or Voice) — never three tint swaps of the same layout.
- Every candidate must clear the accessibility floor first: accessible names, `:focus-visible` ring, keyboard reachability, contrast (`>= 4.5:1` text / `>= 3:1` UI), and `320px` layout integrity.

