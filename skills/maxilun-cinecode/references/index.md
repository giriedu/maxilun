# CineCode Reference Corpus

This directory is a bundled reference library for `maxilun-cinecode`. It documents the programmatic video architecture, React frame primitives (`<AbsoluteFill>`, `<Sequence>`, `<Spring>`, `<Audio>`, `<Subtitle>`, `interpolate`), FFmpeg encoding presets, unit/snapshot testing (`references/composition-api.md`), and the multi-specialist **Maxilun Motion Video Pipeline** (`references/video-production-pipeline.md`) that combines `maxilun-craft`, `maxilun-motion`, `maxilun-content`, and `maxilun-cinecode`.

## Index of Bundled References

| File | Purpose | When to Read |
|---|---|---|
| `references/composition-api.md` | Complete API reference for `<AbsoluteFill>`, `<Sequence>`, `<Series>`, `<Spring>`, `interpolate`, `<Audio>`, `<Subtitle>`, dynamic data binding, FFmpeg render presets, and Vitest frame unit tests | Always read before building or editing a CineCode video composition or render pipeline |
| `references/video-production-pipeline.md` | Multi-skill production blueprint: how to combine `maxilun-craft` (`../maxilun-craft/references/design-md/index.md`), `maxilun-motion` (`../maxilun-motion/references/choreography-styles.md`), `maxilun-content`, and `maxilun-cinecode` for studio-grade product videos, launch teasers, and data reports | Read whenever generating a complete promo/demo/explainer video to maximize visual, kinetic, and narrative quality |
| `../maxilun-motion/references/choreography-styles.md` | 14 Motion Style Signatures, 22 Opener/Promo Hooks, Beat Grid Math, and Spring DNA | Read when translating motion choreography into frame-accurate `<Sequence>` and `<Spring>` code |
| `../maxilun-craft/references/design-md/index.md` | 100 Production Design Systems (Stripe, Linear, Vercel, GitHub, Apple, Nike, etc.) | Read to style video scenes with authentic typography scales, `tabular-nums`, and OKLCH/hex palettes |

## Evidence & Render Contract

1. Every frame in `maxilun-cinecode` MUST be a pure, deterministic function of `frame` and `fps` (`useCurrentFrame()`, `useVideoConfig()`). Never use `setTimeout`, `requestAnimationFrame`, or CSS `transition` inside a rendered video component (they cause non-deterministic frame capture).
2. Ground scene visual tokens in `../maxilun-craft/references/design-md/index.md` and motion curves in `../maxilun-motion/references/choreography-styles.md`.
3. Validate frame 0, mid-transition frames, and final CTA frames before full MP4/WebM encoding.
