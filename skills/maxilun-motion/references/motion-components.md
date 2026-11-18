# Maxilun Motion: Reference & Component Implementations

Implementation reference for native animation primitives (CSS Keyframes, Web Animations API, and GSAP/Canvas).

## 1. Native Primitives (Zero Dependencies)

For most web UI, use CSS Variables + CSS Transitions / Animations or the browser's built-in Web Animations API (WAAPI).

### Spring Simulation via CSS Custom Property & Easing
```css
/* Spring-like curve without a third-party library */
:root {
  --ease-spring-snappy: cubic-bezier(0.175, 0.885, 0.32, 1.275);
  --ease-spring-gentle: cubic-bezier(0.25, 1, 0.5, 1);
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --motion-duration-fast: 150ms;
  --motion-duration-normal: 250ms;
  --motion-duration-slow: 400ms;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```
### Action Frequency & Timing Matrix (Emil Kowalski Matrix)

1. **Daily frequency rule**:
   - **High-frequency actions (≥100x/day)**: keyboard shortcuts (`Cmd+K`), table row selection, keyboard tabbing, account switching. **Duration: 0ms (INSTANT)**. Never animate these actions, because the animation adds interaction friction.
   - **Standard interactions**: tooltip, popover, dropdown menu, selector: **120ms – 180ms**.
   - **Structural & sheet**: modal dialog, bottom sheet drawer, collapsible panel: **200ms – 250ms**.
2. **Easing rule**:
   - **No `ease-in` for interactive UI**: an animation that starts slowly feels sluggish.
   - **Use high-tension `ease-out`**: `cubic-bezier(0.23, 1, 0.32, 1)` or `cubic-bezier(0.16, 1, 0.3, 1)`.
   - Popovers and dropdowns must grow from their trigger point (`transform-origin: top left/right`), not from the center of the screen.

### The 12 Animation Principles Adapted to Web Micro-Interactions

| Animation Principle | Web Micro-Interaction Use | CSS / Timing Spec |
|---|---|---|
| **Squash & Stretch** | Button compresses while pressed (`:active`) | `transform: scale(0.97); transition: transform 60ms ease-out;` |
| **Anticipation** | Subtle lift on hover before the click | `transform: translateY(-1px); box-shadow: 0 2px 6px rgba(0,0,0,0.08);` |
| **Follow Through** | Checkbox tick draws after the box fills | `transition: stroke-dashoffset 180ms ease-out 50ms;` |
| **Arc Motion** | Toggle switch thumb travels along a curve | `cubic-bezier(0.34, 1.56, 0.64, 1)` over 180ms |
| **Timing Bounds** | Cap micro-interaction duration at 300ms | 50–100ms (instant), 100–200ms (standard), 200–300ms (complex) |


### Reveal Primitive (WAAPI)
```typescript
export function reveal(element: HTMLElement, options: { direction?: 'up' | 'down' | 'fade', duration?: number } = {}) {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    element.style.opacity = '1';
    return element.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 1 });
  }

  const { direction = 'up', duration = 300 } = options;
  const yOffset = direction === 'up' ? 16 : direction === 'down' ? -16 : 0;

  return element.animate([
    { opacity: 0, transform: `translateY(${yOffset}px)` },
    { opacity: 1, transform: 'translateY(0)' }
  ], {
    duration,
    easing: 'cubic-bezier(0.16, 1, 0.3, 1)',
    fill: 'forwards'
  });
}
```

### Cascade / Stagger Primitive
```typescript
export function cascade(elements: HTMLElement[], staggerMs: number = 50, durationMs: number = 300) {
  elements.forEach((el, index) => {
    setTimeout(() => {
      reveal(el, { duration: durationMs });
    }, index * staggerMs);
  });
}
```

### Scroll-Driven Blur-Reveal & Progressive Focus Primitive
A scroll pattern in which each section/card stays hidden and blurred while off-screen, then sharpens, fades in, and rises slightly as it enters the viewport.

#### 1. Native CSS Implementation (Zero-JS Scroll-Timeline)
```css
/* Uses CSS Scroll-Driven Animations in modern browsers */
@keyframes scrollBlurReveal {
  from {
    opacity: 0;
    filter: blur(12px);
    transform: translateY(32px) scale(0.98);
  }
  to {
    opacity: 1;
    filter: blur(0px);
    transform: translateY(0) scale(1);
  }
}

.scroll-blur-section {
  animation: scrollBlurReveal 700ms cubic-bezier(0.16, 1, 0.3, 1) both;
  animation-timeline: view();
  animation-range: entry 10% cover 30%;
  will-change: transform, opacity, filter;
}

/* Fallback and mandatory accessibility reset */
@media (prefers-reduced-motion: reduce) {
  .scroll-blur-section {
    animation: none !important;
    opacity: 1 !important;
    filter: none !important;
    transform: none !important;
  }
}
```

#### 2. Universal Implementation via IntersectionObserver (Lightweight, No External Library)
```typescript
/**
 * Initialize scroll reveal with a blur fade-in and gentle rise.
 * Clears filter: blur automatically when finished so text stays pixel-crisp.
 */
export function initScrollBlurReveal(selector: string = '[data-scroll-reveal]') {
  if (typeof window === 'undefined') return;

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll(selector).forEach(el => {
      el.classList.add('is-revealed');
    });
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const target = entry.target as HTMLElement;
        target.classList.add('is-revealed');
        // Clear the filter after the transition ends to keep subpixel text sharp
        setTimeout(() => {
          target.style.filter = 'none';
          target.style.willChange = 'auto';
        }, 800);
        observer.unobserve(target); // Reveal once (one-shot)
      }
    });
  }, {
    rootMargin: '0px 0px -60px 0px',
    threshold: 0.15
  });

  document.querySelectorAll(selector).forEach(el => observer.observe(el));
}
```

```css
/* CSS class for the universal observer */
[data-scroll-reveal] {
  opacity: 0;
  filter: blur(10px);
  transform: translateY(28px) scale(0.985);
  transition:
    opacity 700ms cubic-bezier(0.16, 1, 0.3, 1),
    filter 700ms cubic-bezier(0.16, 1, 0.3, 1),
    transform 700ms cubic-bezier(0.16, 1, 0.3, 1);
  will-change: transform, opacity, filter;
}

[data-scroll-reveal].is-revealed {
  opacity: 1;
  filter: blur(0px);
  transform: translateY(0px) scale(1);
}

/* Automatic stagger for child components */
[data-scroll-reveal] > *:nth-child(1) { transition-delay: 50ms; }
[data-scroll-reveal] > *:nth-child(2) { transition-delay: 120ms; }
[data-scroll-reveal] > *:nth-child(3) { transition-delay: 190ms; }
[data-scroll-reveal] > *:nth-child(4) { transition-delay: 260ms; }

@media (prefers-reduced-motion: reduce) {
  [data-scroll-reveal] {
    opacity: 1 !important;
    filter: none !important;
    transform: none !important;
    transition: none !important;
  }
}
```

## 2. Advanced Multi-Scene Motion (GSAP / Canvas)

For kinetic typography, video sequencing, and audio-reactive scenes:
- Install via the package manager: `pnpm add gsap` (or download `gsap.min.js` into the `assets/` folder for offline execution).
- Avoid a runtime CDN dependency in production or isolated intranet environments.

## 3. Composable Primitives & CineCode Frame Helpers

When an animation must work both in the interactive browser and inside `maxilun-cinecode` frame compositions, separate the **curve math function** from the **DOM manipulation**:

```typescript
export interface SpringParams {
  stiffness: number; // default: 150
  damping: number;   // default: 16
  mass: number;      // default: 1
}

/**
 * Evaluate the spring value deterministically at time t (seconds).
 * Safe for requestAnimationFrame (browser) as well as frame/fps (CineCode).
 */
export function evaluateSpring(tSeconds: number, params: SpringParams = { stiffness: 150, damping: 16, mass: 1 }): number {
  if (tSeconds <= 0) return 0;
  const { stiffness, damping, mass } = params;
  const omega0 = Math.sqrt(stiffness / mass);
  const zeta = damping / (2 * Math.sqrt(stiffness * mass));

  if (zeta < 1) {
    const omegaD = omega0 * Math.sqrt(1 - zeta * zeta);
    const envelope = Math.exp(-zeta * omega0 * tSeconds);
    return 1 - envelope * (Math.cos(omegaD * tSeconds) + ((zeta * omega0) / omegaD) * Math.sin(omegaD * tSeconds));
  }
  // Critically damped or overdamped (zero overshoot)
  return 1 - (1 + omega0 * tSeconds) * Math.exp(-omega0 * tSeconds);
}
```

## 4. Catalog of 12 Motion Components & Composition Limits

| Component | Primary Function | Animated GPU Properties | `prefers-reduced-motion` Fallback |
|---|---|---|---|
| `Reveal` | Element entrance with a mask/direction | `opacity`, `transform: translate3d()` | 120ms `opacity` crossfade without movement |
| `Cascade` | Sequential activation of list/grid children | `opacity`, `transform: translateY()` | Show all at once without stagger delay |
| `Spring` | Physics-based position/scale transition | `transform: translate3d() scale()` | Snap directly to the final position |
| `Trace` | Draws an SVG `stroke-dashoffset` line | `stroke-dashoffset`, `opacity` | Render the full SVG path statically |
| `Morph` | Interpolates an SVG path shape (`d`) | SVG `d` attribute / `opacity` | Crossfade between the start and end shape |
| `Scramble` | Decodes monospace text characters | `textContent` (with intact `aria-label`) | Show the final text immediately |
| `Orbit` | Circular/elliptical motion around a center | `transform: rotate() translate3d()` | Static position at the final angle |
| `Pulse` | Rhythmic emphasis on an active indicator | `transform: scale()`, `opacity` | Static high-contrast border/badge color |
| `Breathe` | Very subtle continuous micro-motion | `opacity`, `transform: scale(1..1.02)` | Fully disabled (`none`) |
| `Wave` | Sine wave propagating across elements | `transform: translateY()` | Flat on the normal baseline |
| `Drag` | Follows the pointer with inertia & friction | `transform: translate3d()` | Position follows the pointer 1:1 without momentum |
| `Scatter` | Particles disperse/gather | Canvas 2D / WebGL buffer | Static illustration of the final positions |

**Purity Composition Rules**:
1. At most **3 primitives per element** and at most **2 simultaneous animation groups** in one viewport, so the user's attention does not split.
2. Never animate `top`, `left`, `width`, `height`, or `box-shadow` continuously on the main thread; use `transform` and `opacity`.
3. For **Lottie JSON** and **Animated SVG** export, convert every path to standard bezier curves and remove non-standard CSS filters that fail to render on iOS/Android.

## 5. Visual Effects Engine, Text Kinetics & Compositor Filters

### 5.1 Catalog of 10 Text Kinetics Effects
| Text Effect | Technical Mechanism | Control Parameters | When to Use |
|---|---|---|---|
| `Scramble` | Random monospace characters decode into the target text | `speed`, `charset`, `resolveOrder` | Reveal of technical titles, KPI numbers, CLI code, or hashes |
| `Elastic` | Per-word/letter position bounces gently with `evaluateSpring()` | `stiffness`, `damping`, `staggerMs` | Energetic, tactile product hero headline |
| `MaskReveal` | Text rises from behind an `overflow: hidden` container, line by line | `yOffsetPx`, `durationMs`, `staggerMs` | Clean editorial reveal (Stripe / Linear / Apple style) |
| `Typewriter` | Characters appear in sequence + blinking block cursor | `charIntervalMs`, `cursorChar` | Simulated terminal input, AI prompt, or live coding |
| `HighlightSweep` | Accent background sweeps across keywords (`scaleX(0 -> 1)`) | `color`, `direction`, `durationMs` | Emphasize 1–2 business-value keywords inside a sentence |
| `Wave` | Sine phase shift (`Math.sin(t + i * phase)`) across characters | `amplitudePx`, `frequencyHz`, `phase` | Active processing indicator or music/audio state |
| `SplitReunite` | Characters split along the X/Y axis, then rejoin | `distancePx`, `axis`, `returnDelayMs` | Dramatic chapter/scene change transition |
| `GradientFlow` | Flowing `background-clip: text` color at a measured angle | `stops`, `angleDeg`, `durationMs` | Emphasize one word in a dark, high-contrast title |
| `GlitchClean` | Brief `clip-path` shift (`120ms`), then locks sharp | `slices`, `offsetPx`, `durationMs` | Cybersecurity, system anomaly, or retro-tech themes |
| `CounterOdometer` | Number interpolation with `font-variant-numeric: tabular-nums` | `fromValue`, `toValue`, `decimals` | Animated financial metrics, `ms` latency, and growth |

### 5.2 Catalog of Camera, Layer & Post-Processing Effects (Browser & Video)
| Visual Effect | Native Implementation (CSS / SVG / Canvas) | Purity & Performance Rule |
|---|---|---|
| **Iris / Portal Wipe** | `clip-path: circle(0% at 50% 50%)` → `circle(150% at 50% 50%)` | Use to open a new scene from the click point/primary focus |
| **Rack Focus Blur** | `filter: blur(0px)` ↔ `blur(6px)` + `opacity` | Focus only 1 active layer; limit simultaneous blurred elements to `<= 2` |
| **Film Grain / Noise** | SVG `<feTurbulence type="fractalNoise" baseFrequency="0.8">` overlay (`opacity: 0.04`) | Adds organic texture to dark surfaces and prevents color banding |
| **Light Sweep / Sheen** | Skewed pseudo-element `translateX(-120% -> 220%)` inside `overflow: hidden` | Trigger once only, when an important card/badge enters or is hovered |
| **Parallax Depth Planes** | 3 layers (`--layer-bg: 0.2x`, `--layer-mid: 0.6x`, `--layer-fg: 1.0x`) via `translate3d` | Must switch off automatically when `prefers-reduced-motion: reduce` is active |
| **Chromatic Impact** | Brief `text-shadow` / RGB channel split (`<= 150ms`) on the peak beat | Only for the *High-Velocity* / *Audio-Synced* styles; never left on continuously |

### 5.3 Bundled Interactive Starter Templates (`assets/`)
- `assets/starter-opener.html`: responsive `1920x1080` stage canvas with 5 layers (`bg`, `mid`, `fg`, `text`, `overlay`), a virtual camera rig, and Brand DNA CSS variable injection.
- `assets/starter-explainer.html`: multi-scene explainer template with camera transitions and timeline controls.

## 6. Native CSS Scroll-Driven Animations (Zero JS Runtime)

Use the modern `animation-timeline: scroll()` and `view-timeline` standards for page-scroll animation that runs 100% on the compositor thread with no JavaScript event listeners:

### 6.1 Page Scroll Progress Bar
```css
.scroll-progress-bar {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: var(--primary, #5e6ad2);
  transform-origin: 0% 50%;
  animation: grow-progress auto linear;
  animation-timeline: scroll(root block);
  z-index: 1000;
}

@keyframes grow-progress {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
```

### 6.2 View-Timeline Reveal & Staggered Viewport Entrance
```css
.reveal-on-scroll {
  animation: reveal-fade-up auto ease-out both;
  animation-timeline: view();
  animation-range: entry 15% cover 40%;
}

@keyframes reveal-fade-up {
  from {
    opacity: 0;
    transform: translateY(24px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Fallback for older browsers and accessibility */
@supports not (animation-timeline: scroll()) {
  .reveal-on-scroll { opacity: 1; transform: none; }
}

@media (prefers-reduced-motion: reduce) {
  .scroll-progress-bar, .reveal-on-scroll {
    animation: none !important;
  }
}
```
