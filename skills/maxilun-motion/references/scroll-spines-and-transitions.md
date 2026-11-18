# Scroll Spines, View Transitions & Kinetic Micro-Interactions

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun-motion/SKILL.md"
  origin: "Maxilun Motion & Kinetic Architecture"
-->

Engineering guide for the scroll spine, View Transitions between pages, and kinetic micro-interactions that run on the GPU at a 60 FPS target.

---

## 1. The One-Loop Rule

Drive DOM manipulation, smooth scroll (Lenis), and the WebGL 3D canvas (Three.js) from **one shared requestAnimationFrame loop**. Two independent RAF loops put the canvas and the DOM one frame out of sync, which shows as jitter while scrolling.

```typescript
import Lenis from "lenis";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

// 1. Initialize Lenis without its own autoRaf
const lenis = new Lenis({
  duration: 1.1,               // 1.0–1.2s is optimal; above 1.4s feels like scroll-jacking
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  syncTouch: false,            // Do not fight native scroll inertia on mobile
  autoRaf: false               // Must be false so the GSAP ticker drives it
});

// 2. Connect the Lenis scroll event to ScrollTrigger
lenis.on("scroll", ScrollTrigger.update);

// 3. Merge all rendering into the single GSAP ticker
gsap.ticker.add((time) => {
  lenis.raf(time * 1000);      // GSAP provides seconds, Lenis needs milliseconds
  renderWebGLScene?.();        // WebGL renders in the same tick, after the scroll position updates
});

// 4. Prevent animation from jumping to catch up with lag
gsap.ticker.lagSmoothing(0);

// 5. Disable immediately under prefers-reduced-motion
if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  lenis.destroy();
}
```

---

## 2. Scrubbed Value Architecture

Do not attach 10 independent scroll triggers to one section. Publish **one normalized progress value ($0.0 \to 1.0$)** and derive every transform from it:

```typescript
ScrollTrigger.create({
  trigger: ".interactive-hero",
  start: "top top",
  end: "+=250%",
  pin: true,
  scrub: 0.6, // 0.4–0.8 gives smooth inertia; true is a rigid 1:1
  onUpdate: (self) => {
    const progress = self.progress; // 0.0 to 1.0
    
    // Split into choreography sub-ranges
    const scaleStage = gsap.utils.clamp(0, 1, (progress - 0.0) / 0.4);
    const cameraPan  = gsap.utils.clamp(0, 1, (progress - 0.4) / 0.6);
    
    applyVisualTransforms(scaleStage, cameraPan);
  }
});
```

---

## 3. Magnetic Physics Interaction

Primary buttons and navigation controls follow the cursor with a magnetic pull and an elastic release:

```typescript
export function makeMagnetic(el: HTMLElement, strength: number = 0.35) {
  if (typeof window === "undefined" || window.matchMedia("(pointer: coarse)").matches) {
    return; // Never active on mobile touch devices
  }

  const state = { x: 0, y: 0 };
  
  el.addEventListener("pointermove", (e: PointerEvent) => {
    const rect = el.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    gsap.to(state, {
      x: (e.clientX - centerX) * strength,
      y: (e.clientY - centerY) * strength,
      duration: 0.35,
      ease: "power3.out",
      onUpdate: () => gsap.set(el, { x: state.x, y: state.y })
    });
  });

  el.addEventListener("pointerleave", () => {
    gsap.to(state, {
      x: 0,
      y: 0,
      duration: 0.65,
      ease: "elastic.out(1, 0.4)",
      onUpdate: () => gsap.set(el, { x: state.x, y: state.y })
    });
  });
}
```

---

## 4. Smooth Page Transitions (View Transitions API)

Use the browser-native View Transitions standard to morph between pages without a heavy router library:

```typescript
export function navigateWithTransition(url: string, updateDOM: () => Promise<void> | void) {
  if (!document.startViewTransition || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    updateDOM();
    return;
  }

  document.startViewTransition(async () => {
    await updateDOM();
  });
}
```

```css
/* Soft transition rules between pages */
::view-transition-old(root) {
  animation: 250ms cubic-bezier(0.16, 1, 0.3, 1) both fade-out;
}
::view-transition-new(root) {
  animation: 350ms cubic-bezier(0.16, 1, 0.3, 1) both fade-in;
}

@keyframes fade-out {
  from { opacity: 1; filter: blur(0); }
  to { opacity: 0; filter: blur(4px); }
}
@keyframes fade-in {
  from { opacity: 0; filter: blur(4px); transform: translateY(12px); }
  to { opacity: 1; filter: blur(0); transform: translateY(0); }
}
```

---

## 5. Web Audio Tactile Feedback (Zero-Byte Synthesized Feedback)

Synthesize a soft click directly from the browser API without loading an external MP3/WAV file (0 bytes downloaded):

```typescript
let audioCtx: AudioContext | null = null;

export function playTactileClick(frequency: number = 800, durationMs: number = 25) {
  if (typeof window === "undefined" || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }

  if (!audioCtx) {
    audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
  }
  if (audioCtx.state === "suspended") {
    audioCtx.resume();
  }

  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();

  osc.type = "sine";
  osc.frequency.setValueAtTime(frequency, audioCtx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(120, audioCtx.currentTime + durationMs / 1000);

  gain.gain.setValueAtTime(0.04, audioCtx.currentTime); // Very low gain, soft
  gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + durationMs / 1000);

  osc.connect(gain);
  gain.connect(audioCtx.destination);

  osc.start();
  osc.stop(audioCtx.currentTime + durationMs / 1000);
}
```
