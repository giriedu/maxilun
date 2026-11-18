# Interactive Choreography & Advanced Motion Playbook

Production guide for scroll orchestration, spring physics, gesture-driven animation, and page transitions in modern browsers.

---

## 1. GSAP ScrollTrigger: Production-Scale Architecture

Use GSAP ScrollTrigger for scroll-driven animation that needs precise pinning, scrubbing, and multi-element orchestration.

### A. Lifecycle-Safe Pattern in React (`gsap.context`)
Wrap every initialization in `gsap.context()` to prevent memory leaks:

```tsx
import { useLayoutEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export function FeatureShowcase() {
  const containerRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    // gsap.context scopes selectors and guarantees complete cleanup
    const ctx = gsap.context((self) => {
      const cards = self.selector?.('.feature-card');

      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: containerRef.current,
          start: 'top top',
          end: '+=200%',
          pin: true,
          scrub: 1,
          anticipatePin: 1
        }
      });

      tl.from(cards, {
        y: 80,
        opacity: 0,
        stagger: 0.2,
        ease: 'power2.out'
      });
    }, containerRef);

    return () => ctx.revert(); // Remove every ScrollTrigger when the component unmounts
  }, []);

  return (
    <div ref={containerRef} className="min-h-screen bg-stone-950 p-12">
      <div className="feature-card">Feature 1</div>
      <div className="feature-card">Feature 2</div>
    </div>
  );
}
```

### B. Responsive Isolation Across Screens (`ScrollTrigger.matchMedia`)
Do not force desktop horizontal pinning onto small phone screens:

```javascript
ScrollTrigger.matchMedia({
  // Desktop: enable horizontal scrub and pinning
  '(min-width: 1024px)': function() {
    gsap.to('.horizontal-track', {
      xPercent: -100 * (panels.length - 1),
      ease: 'none',
      scrollTrigger: {
        trigger: '.horizontal-container',
        pin: true,
        scrub: 1,
        end: () => '+=' + document.querySelector('.horizontal-track').offsetWidth
      }
    });
  },

  // Mobile: native vertical flow without pinning
  '(max-width: 1023px)': function() {
    gsap.from('.horizontal-track > div', {
      opacity: 0,
      y: 40,
      stagger: 0.15,
      scrollTrigger: {
        trigger: '.horizontal-container',
        start: 'top 80%'
      }
    });
  }
});
```

---

## 2. Framer Motion (Motion): Interface Transitions & Semantic Layout

Use Framer Motion for shared element transitions and gesture physics.

### A. Shared Element Transition via `layoutId`
Move an element from a list to its detail view without a reload or visual jump:
```tsx
import { motion, AnimatePresence } from 'framer-motion';

export function CardItem({ item, isSelected, onSelect }: CardItemProps) {
  return (
    <motion.div
      layoutId={`card-container-${item.id}`}
      onClick={onSelect}
      className="p-6 bg-stone-900 border border-stone-800 rounded-xl cursor-pointer"
      whileHover={{ y: -4 }}
      transition={{ type: 'spring', stiffness: 350, damping: 25 }}
    >
      <motion.div layoutId={`card-badge-${item.id}`} className="text-xs font-mono text-emerald-400">
        {item.category}
      </motion.div>
      <motion.h3 layoutId={`card-title-${item.id}`} className="text-xl font-bold text-stone-100">
        {item.title}
      </motion.h3>
    </motion.div>
  );
}
```

### B. Drag Gesture & Critically Damped Spring (Zero Overshoot on High-Frequency)
```tsx
<motion.div
  drag="x"
  dragConstraints={{ left: -100, right: 100 }}
  dragElastic={0.2}
  whileTap={{ scale: 0.98 }}
  transition={{
    type: 'spring',
    stiffness: 400, // Instant response
    damping: 35,    // Critical damping suppresses excess oscillation
    mass: 1
  }}
  className="w-full bg-stone-900 p-4 rounded-lg select-none"
>
  Drag for quick actions
</motion.div>
```

---

## 3. Rive & Lottie Runtimes: State-Machine Vector Graphics

Use state-machine vector animation when a graphic must react directly to pointer input without the cost of a full canvas:

- **Rive Runtime**:
  - Use `useRive` with state machine inputs:
  - `Boolean` for toggle states (for example: Night / Day mode).
  - `Number` for continuous scroll/cursor tracking (0.0 .. 100.0).
  - `Trigger` for one-shot actions (success/failure button click).
- **Lottie Optimization**:
  - Trim hidden paths in Adobe After Effects before exporting JSON.
  - Prefer the compressed `.lottie` / dotLottie format (saves 70% of the raw JSON size).
  - Stop loop playback when the element leaves the viewport via `IntersectionObserver`.

---

## 4. Smooth Page Transitions (Barba.js & View Transitions API)

Transition between pages without triggering a white-flash reload:

### Modern Native Approach (View Transitions API):
```javascript
// Navigate with a native transition and no extra dependency
export function navigateWithTransition(url) {
  if (!document.startViewTransition) {
    window.location.href = url;
    return;
  }

  document.startViewTransition(async () => {
    const res = await fetch(url);
    const html = await res.text();
    const newDoc = new DOMParser().parseFromString(html, 'text/html');

    document.querySelector('#app-root').replaceWith(newDoc.querySelector('#app-root'));
    document.title = newDoc.title;
  });
}
```

### CSS View Transition Companion:
```css
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 250ms;
  animation-timing-function: cubic-bezier(0.16, 1, 0.3, 1);
}

@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(root),
  ::view-transition-new(root) {
    animation: none;
  }
}
```
