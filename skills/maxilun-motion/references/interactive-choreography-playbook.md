# Interactive Choreography & Advanced Motion Playbook

Panduan produksi orkestrasi scroll, pegas fisika, animasi berbasis gestur, dan transisi antar-halaman (*page transitions*) di peramban web modern.

---

## 1. GSAP ScrollTrigger: Arsitektur Skala Produksi

GSAP ScrollTrigger adalah standar industri untuk animasi berbasis scroll yang membutuhkan *pinning* presisi, *scrubbing*, dan orkestrasi multi-elemen.

### A. Pola Aman Siklus Hidup di React (`gsap.context`)
Hindari kebocoran memori dengan selalu membungkus inisialisasi di dalam `gsap.context()`:

```tsx
import { useLayoutEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export function FeatureShowcase() {
  const containerRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    // gsap.context mengisolasi selektor dan memastikan cleanup tuntas
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

    return () => ctx.revert(); // Bersihkan seluruh ScrollTrigger saat komponen unmount
  }, []);

  return (
    <div ref={containerRef} className="min-h-screen bg-stone-950 p-12">
      <div className="feature-card">Fitur 1</div>
      <div className="feature-card">Fitur 2</div>
    </div>
  );
}
```

### B. Isolasi Responsif Lintas Layar (`ScrollTrigger.matchMedia`)
Dilarang memaksakan animasi pinning horizontal desktop pada layar ponsel kecil:

```javascript
ScrollTrigger.matchMedia({
  // Desktop: Aktifkan horizontal scrub dan pinning
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

  // Mobile: Aliran vertikal native tanpa pinning
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

## 2. Framer Motion (Motion): Transisi Antarmuka & Layout Semantik

Framer Motion unggul dalam transisi antar-elemen (shared element transitions) dan fisika gestur.

### A. Shared Element Transition via `layoutId`
Memindahkan elemen dari daftar ke tampilan detail tanpa reload atau lompatan visual:
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

### B. Gestur Seret & Pegas Fisika Kritis (Zero Overshoot on High-Frequency)
```tsx
<motion.div
  drag="x"
  dragConstraints={{ left: -100, right: 100 }}
  dragElastic={0.2}
  whileTap={{ scale: 0.98 }}
  transition={{
    type: 'spring',
    stiffness: 400, // Responsif instan
    damping: 35,    // Redaman kritis untuk mematikan osilasi berlebih
    mass: 1
  }}
  className="w-full bg-stone-900 p-4 rounded-lg select-none"
>
  Geser untuk tindakan cepat
</motion.div>
```

---

## 3. Rive & Lottie Runtimes: Grafik Vektor State-Machine

Gunakan animasi vektor berbasis state machine ketika grafik harus bereaksi langsung terhadap input kursor pengguna tanpa overhead komputasi canvas penuh:

- **Rive Runtime**:
  - Gunakan `useRive` dengan state machine input:
  - `Boolean` untuk toggle state (misal: Mode Malam / Siang).
  - `Number` untuk tracking scroll/kursor kontinu (0.0 .. 100.0).
  - `Trigger` untuk aksi satu kali (klik tombol sukses/gagal).
- **Lottie Optimization**:
  - Pangkas path tersembunyi di Adobe After Effects sebelum mengekspor JSON.
  - Prioritaskan format `.lottie` / dotLottie terkompresi (menghemat 70% ukuran JSON mentah).
  - Hentikan pemutaran loop saat elemen keluar dari viewport via `IntersectionObserver`.

---

## 4. Transisi Halaman Mulus (Barba.js & View Transitions API)

Transisi antar-halaman tanpa memicu *white-flash reload*:

### Pendekatan Native Modern (View Transitions API):
```javascript
// Navigasi dengan transisi native tanpa dependensi tambahan
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
