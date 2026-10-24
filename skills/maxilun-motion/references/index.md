# Motion Reference Corpus

This directory is a bundled reference library for `maxilun-motion`. It covers native CSS/WAAPI/GSAP/Canvas motion primitives (`references/motion-components.md`), Brand DNA-to-Motion DNA extraction, 14 motion style signatures, 22 opener/promo hooks, kinetic typography, camera choreography, audio reactivity (`references/choreography-styles.md`), and direct token derivation from `../maxilun-craft/references/design-md/index.md`.

## Index of Bundled References

| File | Purpose | When to Read |
|---|---|---|
| `references/motion-components.md` | Native CSS custom properties, spring physics approximations, Web Animations API (WAAPI) primitives, and GSAP/Canvas composition APIs | Always read before implementing interactive browser animations, micro-interactions, or SVG/Lottie motion |
| `references/choreography-styles.md` | Brand DNA → Motion DNA mapping, 14 Motion Style Signatures, 22 Opener/Promo Hooks, 9 Explainer Styles, Camera & Multi-Scene Graph, Text Kinetics, and Audio Reactivity | Read when planning motion direction, storyboard choreography, kinetic typography, or handing off a motion spec to `maxilun-cinecode` |
| `../maxilun-craft/references/design-md/index.md` | 100 Production Design Systems (Stripe, Linear, Vercel, GitHub, Apple, Nike, etc.) | Read when deriving motion timing, spring stiffness, and color accents from a comparable product reference |

## Motion & Video Synergy Contract

1. **Interactive Web / Lottie / SVG Deliverable**: `maxilun-motion` is the primary owner. Derive timing and spring curves from project tokens or `../maxilun-craft/references/design-md/index.md`, and always include `@media (prefers-reduced-motion: reduce)` fallbacks.
2. **Rendered Video Deliverable (MP4 / WebM / GIF)**: `maxilun-cinecode` is the primary owner (`../maxilun-cinecode/references/index.md`). When `maxilun-motion` is invoked as a companion for a video project, output a **Deterministic Frame Choreography Spec** (frame numbers, spring stiffness/damping/mass, camera vectors, and text kinetic stagger in frames) that maps directly into CineCode `<Sequence>`, `<Spring>`, and `interpolate()`.
