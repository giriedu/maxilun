# Scroll Spines, View Transitions & Kinetic Micro-Interactions

<!-- metadata:
  version: "1.1.0"
  sync_target: "skills/maxilun-motion/SKILL.md"
  origin: "Maxilun Motion & Studio-Grade Kinetic Architecture"
-->

Panduan rekayasa tulang punggung scroll (*scroll spine*), transisi halaman halus (*View Transitions*), dan mikro-interaksi kinetik berkinerja tinggi (60 FPS GPU).

---

## 1. Aturan Satu Putaran (The One-Loop Rule)

Manipulasi DOM, smooth scroll (Lenis), dan kanvas 3D WebGL (Three.js) **wajib digerakkan oleh satu requestAnimationFrame loop bersama**. Dua putaran RAF independen memicu jeda 1 frame desinkronisasi antara kanvas dan DOM yang terlihat bergetar saat digulir.

```typescript
import Lenis from "lenis";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

// 1. Inisialisasi Lenis tanpa autoRaf mandiri
const lenis = new Lenis({
  duration: 1.1,               // 1.0–1.2s optimal; di atas 1.4s terasa seperti scroll-jacking
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  syncTouch: false,            // Jangan lawan inersia scroll native di mobile!
  autoRaf: false               // Wajib false agar dikendalikan oleh ticker GSAP
});

// 2. Sambungkan event scroll Lenis ke ScrollTrigger
lenis.on("scroll", ScrollTrigger.update);

// 3. Gabungkan seluruh render ke ticker tunggal GSAP
gsap.ticker.add((time) => {
  lenis.raf(time * 1000);      // GSAP memberi satuan detik, Lenis butuh milidetik
  renderWebGLScene?.();        // WebGL dirender tepat di tick yang sama setelah posisi scroll update
});

// 4. Cegah animasi melompat mengejar lag
gsap.ticker.lagSmoothing(0);

// 5. Matikan seketika di prefers-reduced-motion
if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  lenis.destroy();
}
```

---

## 2. Normalisasi Nilai Scrubbing (Scrubbed Value Architecture)

Jangan memasang 10 pemicu scroll independen pada satu seksi. Dorong **satu nilai progres ternormalisasi ($0.0 \to 1.0$)** dan turunkan seluruh transformasi dari nilai tersebut:

```typescript
ScrollTrigger.create({
  trigger: ".interactive-hero",
  start: "top top",
  end: "+=250%",
  pin: true,
  scrub: 0.6, // 0.4–0.8 memberikan inersia halus; true kaku 1:1
  onUpdate: (self) => {
    const progress = self.progress; // 0.0 s.d. 1.0
    
    // Pecah ke sub-range koreografi
    const scaleStage = gsap.utils.clamp(0, 1, (progress - 0.0) / 0.4);
    const cameraPan  = gsap.utils.clamp(0, 1, (progress - 0.4) / 0.6);
    
    applyVisualTransforms(scaleStage, cameraPan);
  }
});
```

---

## 3. Elemen Magnetik Kinetik (Magnetic Physics Interaction)

Tombol utama dan kontrol navigasi bereaksi mengikuti posisi kursor dengan tarikan magnetik dan pelepasan elastis:

```typescript
export function makeMagnetic(el: HTMLElement, strength: number = 0.35) {
  if (typeof window === "undefined" || window.matchMedia("(pointer: coarse)").matches) {
    return; // Dilarang aktif di perangkat layar sentuh mobile
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

## 4. Transisi Halaman Mulus (View Transitions API)

Gunakan standar View Transitions bawaan browser modern untuk morphing antar-halaman tanpa ketergantungan library router berat:

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
/* Aturan Transisi Lembut Antar-Halaman */
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

## 5. Umpan Balik Taktil Web Audio (Zero-Byte Synthesized Feedback)

Sintesis bunyi klik halus langsung dari API browser tanpa memuat berkas audio MP3/WAV eksternal (0 byte download):

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

  gain.gain.setValueAtTime(0.04, audioCtx.currentTime); // Gain sangat rendah, halus
  gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + durationMs / 1000);

  osc.connect(gain);
  gain.connect(audioCtx.destination);

  osc.start();
  osc.stop(audioCtx.currentTime + durationMs / 1000);
}
```
