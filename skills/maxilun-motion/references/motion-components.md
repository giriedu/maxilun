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

## 3. Composable Primitives & CineCode Frame Helpers

Saat membangun animasi yang dapat dipakai baik di browser interaktif maupun di dalam komposisi frame `maxilun-cinecode`, pisahkan **fungsi matematika kurva** dari **manipulasi DOM**:

```typescript
export interface SpringParams {
  stiffness: number; // default: 150
  damping: number;   // default: 16
  mass: number;      // default: 1
}

/**
 * Evaluasi nilai spring secara deterministik pada waktu t (detik).
 * Aman dipakai untuk requestAnimationFrame (browser) maupun frame/fps (CineCode).
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

## 4. Katalog 12 Komponen Motion & Batas Komposisi

| Komponen | Fungsi Utama | Properti GPU yang Dianimasikan | Fallback `prefers-reduced-motion` |
|---|---|---|---|
| `Reveal` | Kemunculan elemen dengan mask/arah | `opacity`, `transform: translate3d()` | Crossfade `opacity` 120ms tanpa geser |
| `Cascade` | Aktivasi berurutan anak list/grid | `opacity`, `transform: translateY()` | Tampilkan serentak tanpa stagger delay |
| `Spring` | Transisi posisi/skala berbasis fisika | `transform: translate3d() scale()` | Snap langsung ke posisi akhir |
| `Trace` | Menggambar garis `stroke-dashoffset` SVG | `stroke-dashoffset`, `opacity` | Render path SVG penuh secara statis |
| `Morph` | Interpolasi bentuk SVG path (`d`) | Atribut SVG `d` / `opacity` | Crossfade antara bentuk awal dan akhir |
| `Scramble` | Dekode karakter teks monospace | `textContent` (dengan `aria-label` utuh) | Tampilkan teks akhir secara langsung |
| `Orbit` | Gerak melingkar/elips mengelilingi pusat | `transform: rotate() translate3d()` | Posisi statis pada sudut akhir |
| `Pulse` | Penekanan ritmis pada indikator aktif | `transform: scale()`, `opacity` | Warna border/badge statis kontras tinggi |
| `Breathe` | Gerak mikro kontinu yang sangat halus | `opacity`, `transform: scale(1..1.02)` | Dinonaktifkan sepenuhnya (`none`) |
| `Wave` | Propagasi gelombang sinus antar-elemen | `transform: translateY()` | Rata pada baseline normal |
| `Drag` | Mengikuti pointer dengan inersia & friksi | `transform: translate3d()` | Posisi mengikuti pointer 1:1 tanpa momentum |
| `Scatter` | Penyebaran/pengumpulan partikel | Canvas 2D / WebGL buffer | Ilustrasi statis posisi akhir |

**Aturan Komposisi Anti-Slop**:
1. Maksimal **3 primitif per elemen** dan maksimal **2 grup animasi simultan** dalam satu viewport agar fokus mata pengguna tidak pecah.
2. Dilarang menganimasikan `top`, `left`, `width`, `height`, atau `box-shadow` secara terus-menerus pada thread utama; gunakan `transform` dan `opacity`.
3. Untuk ekspor **Lottie JSON** dan **Animated SVG**, pastikan semua path sudah dikonversi ke kurva bezier standar tanpa filter CSS non-standar yang gagal dirender di iOS/Android.
