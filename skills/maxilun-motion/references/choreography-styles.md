# Motion DNA, Style Signatures, Storyboard Hooks & Camera/Audio Choreography

Use this reference when designing motion direction, extracting *Motion DNA* from `maxilun-craft` tokens, building an opener/explainer storyboard, or handing a frame choreography spec to `maxilun-cinecode`.

---

## 1. Brand DNA → Motion DNA Pipeline (Integrated with `maxilun-craft`)

Take the visual tokens from the project, or pick 1–2 comparable references from `../maxilun-craft/references/design-md/index.md`, then map them to motion physics parameters:

| `maxilun-craft` Token | `maxilun-motion` Parameter | Production Conversion Rule |
|---|---|---|
| `--space-2` (`8px`) | `timing.fast` (`80ms - 120ms` / `3-4 frames @30fps`) | Micro-feedback (hover, focus, toggle) |
| `--space-4` (`16px`) | `timing.normal` (`160ms - 220ms` / `5-7 frames @30fps`) | Component state transitions, drawer, dropdown |
| `--space-8` (`32px`) | `timing.slow` (`320ms - 450ms` / `10-14 frames @30fps`) | Scene-to-scene transitions, hero reveal, modal |
| `typography.weight >= 700` | `kineticMode: "punch"` (`stiffness: 180, damping: 16`) | Assertive headline (for example the `stripe.md`, `nike.md`, `linear.app.md` style) |
| `typography.weight <= 400` | `kineticMode: "editorial-glide"` (`stiffness: 100, damping: 20`) | Soft editorial typography (for example the `apple.md`, `wired.md` style) |
| `borderRadius <= 4px` | `curvature: "architectural-snap"` (zero overshoot, `damping >= 22`) | Technical precision, strict grid |
| `borderRadius >= 12px` | `curvature: "elastic-spring"` (`stiffness: 130, damping: 14`) | Friendly, tactile consumer app |

### Motion DNA Profile Format (`motion-dna.json`)
```json
{
  "referenceSource": "../maxilun-craft/references/design-md/linear.app.md",
  "motionPersonality": "precision-kinetic",
  "timingMs": { "fast": 90, "normal": 180, "slow": 340, "dramatic": 600 },
  "framesAt30Fps": { "fast": 3, "normal": 6, "slow": 10, "dramatic": 18 },
  "springDefaults": { "stiffness": 170, "damping": 19, "mass": 1 },
  "accentColor": "oklch(58% 0.18 255)",
  "kineticMode": "punch",
  "reducedMotionVariant": "opacity-crossfade-120ms"
}
```

---

## 2. Matrix of 14 Motion Style Signatures

Use a signature as reference vocabulary, not as a mandatory preset. Pick one dominant influence when that helps unify the motion. Combine compatible influences, or ignore the matrix when the brief needs a different visual language. Consistency comes from art direction, motifs, timing, and transition rules, not from forcing one effect onto every shot.

| # | Style Signature | Physics & Easing Characteristics | Suited Domains | Closest `design-md` References |
|---|---|---|---|---|
| 1 | **Kinetic Minimal** | Snap-to-grid, zero overshoot (`damping: 24`), monochrome accents + 1 semantic color | B2B SaaS, Fintech, Issue Tracker | `linear.app.md`, `vercel.md`, `mercury.md` |
| 2 | **Fluid Organic** | Smooth continuous curves, organic morphing, no hard cuts | Wellness, Consumer Lifestyle, Health | `oura.md`, `airbnb.md` |
| 3 | **Architectural Depth** | Measured parallax depth planes, structural lines drawing the grid (`Trace`) | Architecture, Enterprise Infra, Hardware | `apple.md`, `spacex.md`, `dji.md` |
| 4 | **Tactile Card & Craft** | Staged folds, dynamic shadow on lift, responsive springs | Education, Visual Collaboration, Workspace | `notion.md`, `figma.md`, `miro.md` |
| 5 | **Data Flow Cascade** | Particles flowing along an SVG path (`MotionPath`), sequential node activation | Observability, Analytics, Database, AI | `sentry.md`, `posthog.md`, `clickhouse.md`, `supabase.md` |
| 6 | **Editorial Crisp** | Line-by-line reveal with a sharp mask, high-contrast transitions | Media, Journalism, Documentation | `wired.md`, `theverge.md`, `mintlify.md` |
| 7 | **Financial Precision** | `tabular-nums` digits rolling precisely (*odometer*), charts growing with a spring | Payment Gateway, Crypto, Banking | `stripe.md`, `wise.md`, `revolut.md` |
| 8 | **High-Velocity Sport** | Fast cuts on the beat, slanted/bold typography entering with high momentum | Automotive, Sports, Gaming | `nike.md`, `ferrari.md`, `bmw-m.md`, `playstation.md` |
| 9 | **Command-First Micro** | Feedback `< 100ms`, instant keyboard highlight, list morphing with no delay | IDE, CLI, Developer Productivity | `raycast.md`, `cursor.md`, `warp.md`, `superhuman.md` |
| 10 | **Cinematic Spotlight** | Slow dolly, lighting focused on a single subject, dark contrast | Luxury, Flagship Product Launch | `bugatti.md`, `lamborghini.md` |
| 11 | **Brutalist Slam** | 0ms hard cut combined with an extreme-contrast scale slam | Creative Agency, Event Campaign | `framer.md`, `webflow.md` |
| 12 | **Commerce Showcase** | Smooth product transitions, texture detail zoom, clear price badge | E-Commerce, Modern Retail | `shopify.md`, `starbucks.md` |
| 13 | **Narrative Scroll** | Timeline bound to scroll position (`ScrollTimeline`), subject persists across chapters | Product Landing Page, Annual Report | `apple.md`, `stripe.md` |
| 14 | **Audio-Synced Pulse** | Transitions and element scale locked to BPM/audio transients | Music, Social Video Promo, Teaser | `spotify.md` |

---

## 3. Catalog of 22 Opener & Promo Hook Concepts

These concepts are idea starters, not requirements or fixed durations. Choose, change, or ignore them based on the message, the platform, and the available footage. Do not use a KPI, a claim, or sample UI unless its source actually exists.

### A. Opener
1. **Logo Assembly** — Geometric elements converge on the center point using a spring simulation (`stiffness: 150, damping: 15`).
2. **Type Scramble Decode** — Random monospace characters decode into the main title within 24 frames.
3. **Portal Iris Wipe** — A circular mask grows from the primary focus element to open the scene.
4. **Depth Plane Plunge** — The camera moves forward (`dolly`) through 3 transparent UI layers toward the core screen.
5. **Signal Lock** — Random wave/data lines lock into a sharp metric chart.
6. **Grid Construct** — `1px` hairlines draw the layout structure before content appears (`Trace` + `Reveal`).
7. **Light Sweep** — A directed light sheen sweeps the product contour over a dark surface.
8. **Morph Entry** — A problem icon changes shape (`SVG path morph`) into the solution component.
9. **Stagger Cascade** — Data rows or feature cards activate in sequence with a `3 frame` (`100ms`) gap.
10. **Metric Counter Snap** — A KPI number rolls quickly from the old baseline to the new target value.

### B. Narrative & Explainer Hooks (Explainer Beats)
11. **Problem Friction Split** — The screen splits in two: the left side shows the slow manual flow (dim red), the right side shows the automated 1-click flow (sharp green).
12. **Before/After Slider Sweep** — A vertical line sweeps the screen and turns the old view into the new system.
13. **Architecture Node Activation** — A request travels from the User → API → DB nodes with a real `ms` latency indicator.
14. **Code-to-UI Live Compile** — Code lines are typed on the left (45 frames) and immediately render the production component on the right.
15. **Feature Unfold** — A compact card opens its detail layer spatially without switching context.
16. **Timeline March** — A progress stepper advances and drives the scene changes.
17. **Comparison Scale** — Horizontal bar charts grow side by side to compare time/cost load.
18. **Interactive Cursor Guided Tour** — A vector cursor moves along a natural curve, presses a button, and triggers a success toast.
19. **Security Shield Lock** — An incoming payload is validated and locked with an encryption indicator/green status.
20. **Social Proof Grid** — Verified metric quotes appear in turn at a calm rhythm.
21. **CTA Magnetic Focus** — All secondary elements dim (`opacity: 0.35`) while the primary action button gets full-contrast focus.
22. **Looping Seamless Outro** — The last frame connects back to the frame 0 composition for looped playback on social media.

---

## 4. Camera System, Text Kinetics & Audio Reactivity

### 4.1 Virtual Camera (Browser 3D / Canvas & `maxilun-cinecode`)
- **Motion Sickness Guard**: Allow at most **1 type of camera move** at a time (for example: `dolly` only or `pan` only; never combine `orbit + tilt + shake`).
- **Rack Focus**: Use depth blur only to move the viewer's attention from the background to the active component (`filter: blur(0px)` vs `blur(4px)`).

### 4.2 Text Kinetics
- **Granularity**:
  - *Per-Character*: Only for short titles (`<= 4 words`, for example numbers or code).
  - *Per-Word*: For headlines (`5 - 10 words`) with a `40ms` (`1-2 frame`) stagger.
  - *Per-Line*: For subheadlines or explanatory sentences, so the reader's eyes do not tire.
- **Accessibility invariant**: Text in the DOM must stay intact for screen readers (`aria-label` on the parent when letters are split into individual `<span>` elements).

### 4.3 Audio Sync & Beat Grid
- Compute the frame duration per beat for sync with `maxilun-cinecode`:
  $$\text{Frames per Beat} = \text{round}\left(\frac{\text{FPS} \times 60}{\text{BPM}}\right)$$
  *(Example: at `30 FPS` with `120 BPM` music, 1 beat = `15 frames`, 1 bar (4 beats) = `60 frames` / `2 seconds`)*
- When the edit does follow the music, use the beat/bar grid as a reference point and fit cuts to the action and narration. Do not lock every transition to the BPM; some passages need to hold still or leave the beat to create impact.
- **8 Audio-Reactive Visualization Modes**:
  1. *Waveform Ribbon* — An SVG/Canvas curve flows with the sound wave amplitude.
  2. *Circular Spectrum* — Radial frequency bars surround the logo or active voice indicator.
  3. *Particle Field* — Low-frequency energy (*bass*) controls the speed and density of Canvas particles.
  4. *Typography Pulse* — Weight (variable font `font-weight`) or text scale pulses exactly on beat transients.
  5. *Color Shift* — A measured OKLCH lightness/chroma shift follows the frequency bands (`bass`, `mid`, `treble`).
  6. *Geometry Morph* — Polygon vertices shift smoothly with the audio wave.
  7. *Grid Distortion* — The background grid bends in proportion to the decibel peak (*RMS amplitude*).
  8. *Spotlight Transient* — Stage lighting intensity rises while the vocalist/narrator speaks (*voice-over envelope*).
