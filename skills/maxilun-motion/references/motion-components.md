# Maxilun Motion: Reference & Component Implementations

Dokumen referensi implementasi primitif animasi native (CSS Keyframes, Web Animations API, dan GSAP/Canvas).

## 1. Primitif Native (Zero Dependencies)

Untuk sebagian besar UI web, gunakan CSS Variables + CSS Transitions / Animations atau Web Animations API (WAAPI) bawaan browser.

### Spring Simulation via CSS Custom Property & Easing
```css
/* Spring-like curve tanpa library pihak ketiga */
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

## 2. Advanced Multi-Scene Motion (GSAP / Canvas)

Untuk kinetic typography, video sequencing, dan audio-reactive scene:
- Pasang via npm: `pnpm add gsap` (atau unduh `gsap.min.js` lokal ke folder `assets/` untuk eksekusi offline).
- Hindari ketergantungan CDN runtime di lingkungan produksi atau intranet terisolasi.
