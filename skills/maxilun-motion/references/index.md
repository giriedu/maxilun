# Motion Reference Corpus

This directory is a bundled reference library for `maxilun-motion`. It covers native CSS/WAAPI/GSAP/Canvas motion primitives (`references/motion-components.md`), Brand DNA-to-Motion DNA extraction, 14 motion style signatures, 22 opener/promo hooks, kinetic typography, camera choreography, audio reactivity (`references/choreography-styles.md`), and direct token derivation from `../maxilun-craft/references/design-md/index.md`.

## Index of Bundled References

| File | Purpose | When to Read |
|---|---|---|
| `references/motion-components.md` | Native CSS custom properties, spring physics approximations, Web Animations API (WAAPI) primitives, and GSAP/Canvas composition APIs | Always read before implementing interactive browser animations, micro-interactions, or SVG/Lottie motion |
| `references/choreography-styles.md` | Brand DNA → Motion DNA mapping, 14 Motion Style Signatures, 22 Opener/Promo Hooks, 9 Explainer Styles, Camera & Multi-Scene Graph, Text Kinetics, and Audio Reactivity | Read when planning motion direction, storyboard choreography, kinetic typography, or handing off a motion spec to `maxilun-cinecode` |
| `references/3d-scenes.md` | Scene contract, renderer selection, complete 3D world structure, accessible interaction, loading/fallback, and performance gates | Read when the requested website/app includes a full navigable or interactive 3D environment |
| `references/visual-reference-workflow.md` | Reference inspection, art-direction synthesis, motion planning, and preview-based visual review | Read when the user supplies websites/screenshots or asks for a polished reference-led motion experience |
| `../maxilun-craft/references/design-md/index.md` | 100 Production Design Systems (Stripe, Linear, Vercel, GitHub, Apple, Nike, etc.) | Read when deriving motion timing, spring stiffness, and color accents from a comparable product reference |

## Motion & Video Coordination Contract

1. **Interactive Web / Lottie / SVG / Full 3D Scene Deliverable**: `maxilun-motion` is the primary owner. For full 3D scenes, read `references/3d-scenes.md`; derive visual and motion direction from project tokens or `../maxilun-craft/references/design-md/index.md`, and include reduced-motion, loading, and renderer-failure paths.
2. **Rendered Video Deliverable (MP4 / WebM / GIF)**: `maxilun-cinecode` is the primary owner (`../maxilun-cinecode/references/index.md`). When `maxilun-motion` is invoked as a companion for a video project, output a **Shot Choreography Spec** (frame/timing ranges, spring profile where useful, camera direction, and text timing) for implementation with the installed Remotion APIs.
