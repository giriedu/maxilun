# CineCode Composition API, Audio/Data Binding & Render Presets Reference

Gunakan referensi ini saat menulis komponen frame React/TypeScript, menyusun timeline `<Sequence>`, mengikat data dinamis, atau mengonfigurasi encoder FFmpeg di `maxilun-cinecode`.

---

## 1. Aturan Emas Determinisme Frame (Non-Negotiable)

Di dalam `maxilun-cinecode`, setiap frame dirender secara berurutan oleh headless browser / canvas renderer lalu di-pipe ke FFmpeg:
1. **Murni Fungsi `frame`**: Seluruh posisi, skala, opasitas, dan teks harus dihitung dari `const frame = useCurrentFrame()` dan `const { fps, width, height } = useVideoConfig()`.
2. **DILARANG memakai `transition` CSS atau `setTimeout`**: Properti CSS `transition: all 0.3s` tidak sinkron dengan kecepatan capture per-frame. Selalu set `transition: 'none'` dan hitung nilai per frame menggunakan `interpolate()` atau `<Spring>`.
3. **Preload Seluruh Aset**: Font, gambar, dan data JSON wajib selesai dimuat sebelum frame diambil agar tidak muncul frame kedip kosong (*flash of unstyled text/image*).

---

## 2. Core Interfaces & Komponen Primitif (`scaffold/src/`)

### 2.1 Struktur Proyek & Komposisi (`types.ts`)
```typescript
export interface VideoProject {
  id: string;
  fps: number;              // Standar: 30 atau 60
  width: number;            // Standar: 1920 (16:9), 1080 (9:16 atau 1:1)
  height: number;
  durationInFrames: number;
  compositions: Composition[];
  audio?: AudioTrack[];
  metadata: ProjectMetadata;
}

export interface CompositionProps {
  frame: number;
  fps: number;
  width: number;
  height: number;
  [key: string]: unknown;
}
```

### 2.2 Primitif Layout, Waktu & Animasi
| Komponen / Fungsi | Peran | Contoh Pemakaian Deterministik |
|---|---|---|
| `<AbsoluteFill>` | Container full-frame (`position: absolute; inset: 0; display: flex`) | Layering latar belakang, konten utama, dan overlay HUD/subtitle |
| `<Sequence from={f} durationInFrames={d}>` | Menggeser konteks `useCurrentFrame()` anak sehingga dimulai dari `0` pada frame `from` | Memecah video menjadi `IntroScene`, `DemoScene`, `MetricsScene`, `OutroScene` |
| `interpolate(frame, [inMin, inMax], [outMin, outMax], 'clamp')` | Memetakan rentang frame ke opasitas, posisi `px`, atau sudut rotasi | `const opacity = interpolate(frame, [0, 15], [0, 1], 'clamp');` |
| `<Spring frame={f} fps={fps} config={{ stiffness, damping, mass }}>` | Simulasi pegas teredam analitik yang mulus tanpa keyframe manual | Kemunculan kartu UI, pergerakan kursor, atau pop-in badge metrik |
| `<Audio src="..." startFrom={0} volume={(f) => ...} />` | Track musik latar atau voice-over dengan kurva fade-in/fade-out per frame | Ducking volume BGM dari `0.35` ke `0.12` saat narator berbicara |
| `<Subtitle segments={[...]} />` | Overlay teks takarir beserta ekspor sidecar `.srt` / `.vtt` | Aksesibilitas wajib untuk video dengan narasi suara |
| `<SceneTransition type="iris\|wipe-right\|wipe-up\|zoom-through\|fade">` | Transisi masuk/keluar scene berbasis `clip-path` & `scale` deterministik (`Effects.tsx`) | Membuka scene baru dengan *Portal Iris Wipe* atau *Zoom-Through* |
| `<CameraRig fromScale={1} toScale={1.06} fromX={0} toX={-24}>` | Rig kamera 2.5D virtual (`dolly`, `pan`, `tilt`) per frame (`Effects.tsx`) | Gerakan kamera sinematik halus tanpa memicu mabuk visual |
| `<RackFocusBlur fromBlurPx={8} toBlurPx={0}>` | Efek kedalaman bidang (*depth-of-field rack focus*) deterministik (`Effects.tsx`) | Memindahkan fokus mata penonton dari latar ke kartu UI utama |
| `<ColorGrade contrast={1.04} saturate={1.05} vignetteOpacity={0.28}>` | Koreksi warna studio + *radial vignette* halus (`Effects.tsx`) | Menjaga atmosfer warna sinematik yang konsisten di seluruh video |
| `<FilmGrainOverlay frame={frame} opacity={0.04} />` | Tekstur *fractal noise* SVG dengan `seed` per frame (`Effects.tsx`) | Mencegah *color banding* pada latar gelap saat di-encode ke MP4 H.264 |
| `<KineticScrambleText text="..." frame={frame} durationInFrames={24} />` | Efek dekode karakter monospace deterministik per frame (`Effects.tsx`) | Reveal judul teknologi, metrik angka, atau perintah CLI |
| `<VideoClip src="./footage.mp4" startFrom={0} trimStartSeconds={2.5} />` | Menyematkan, memotong (*trim*), dan menyinkronkan file video lokal frame-demi-frame (`VideoClip.tsx`) | Menampilkan rekaman layar/footage produk di dalam bingkai UI atau layar penuh dengan overlay motion |

---

## 3. Pola Komposisi Multi-Scene & Dynamic Data Binding

```tsx
import React from 'react';
import { AbsoluteFill } from '../scaffold/src/components/AbsoluteFill';
import { Sequence } from '../scaffold/src/components/Sequence';
import { interpolate } from '../scaffold/src/components/Interpolate';
import { Subtitle } from '../scaffold/src/components/Subtitle';
import { useCurrentFrame, useVideoConfig } from '../scaffold/src/hooks';

export interface ReleaseVideoProps {
  productName: string;
  headline: string;
  p95BeforeMs: number;
  p95AfterMs: number;
  ctaCommand: string;
}

export const ReleaseVideo: React.FC<ReleaseVideoProps> = ({
  productName,
  headline,
  p95BeforeMs,
  p95AfterMs,
  ctaCommand,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: '#090d16', color: '#f8fafc', fontFamily: 'Inter, system-ui, sans-serif' }}>
      {/* Scene 1: Hook (Frame 0 - 90 / 0s - 3s @30fps) */}
      <Sequence from={0} durationInFrames={90} name="01-hook">
        <HookScene productName={productName} headline={headline} />
      </Sequence>

      {/* Scene 2: Metric Proof (Frame 90 - 240 / 3s - 8s @30fps) */}
      <Sequence from={90} durationInFrames={150} name="02-metric-proof">
        <MetricComparisonScene beforeMs={p95BeforeMs} afterMs={p95AfterMs} fps={fps} />
      </Sequence>

      {/* Scene 3: Terminal CTA (Frame 240 - 330 / 8s - 11s @30fps) */}
      <Sequence from={240} durationInFrames={90} name="03-cta">
        <TerminalCtaScene command={ctaCommand} />
      </Sequence>

      <Subtitle
        segments={[
          { start: 0, end: 90, text: headline },
          { start: 90, end: 240, text: `p95 latency dropped from ${p95BeforeMs}ms to ${p95AfterMs}ms.` },
          { start: 240, end: 330, text: `Run ${ctaCommand} to start.` },
        ]}
      />
    </AbsoluteFill>
  );
};
```

---

## 4. Preset Render & Konfigurasi Encoder FFmpeg

| Nama Preset | Resolusi | Aspect | FPS | Codec & Pixel Format | Target Distribusi |
|---|---|---|---|---|---|
| `presentation` | `1920x1080` | `16:9` | `30` / `60` | MP4 H.264 (`libx264`, `-pix_fmt yuv420p`, `-crf 18`) | Website Hero, YouTube, Product Hunt, Presentasi |
| `social-vertical` | `1080x1920` | `9:16` | `30` / `60` | MP4 H.264 (`libx264`, `-pix_fmt yuv420p`, `-crf 19`) | Reels, TikTok, YouTube Shorts |
| `social-square` | `1080x1080` | `1:1` | `30` | MP4 H.264 (`libx264`, `-pix_fmt yuv420p`, `-crf 19`) | Feed X/Twitter, LinkedIn, Instagram |
| `web-optimized` | `1280x720` | `16:9` | `30` | WebM VP9 (`libvpx-vp9`, `-b:v 0 -crf 28`) | Embed dokumentasi ringan |
| `transparent` | `1920x1080` | `16:9` | `30` | WebM VP9 dengan Alpha (`yuva420p`) | Overlay komponen di atas halaman web |
| `high-quality` | `3840x2160` | `16:9` | `60` | MP4 H.265 (`libx265`, `-crf 16`) | Master arsip / layar pameran 4K |

---

## 6. Mengedit & Menambahkan Motion Overlay pada File Video di Folder Lokal

Jika pengguna sudah memiliki file video di dalam folder proyek (misal `./assets/raw-recording.mp4` atau `./demo.mp4`) dan ingin menambahkan desain motion (headline pegas, callout zoom, lower-third, grafik metrik, atau takarir), tersedia **2 metode produksi**:

### Metode A: Komposisi di Dalam Scene via `<VideoClip>` (Mendukung Zoom Kamera, Split-Screen & Bingkai Mockup)
Gunakan `<VideoClip>` di dalam komposisi React. Renderer `render.js` secara otomatis menunggu event `seeked` pada `<video>` di setiap frame sebelum mengambil gambar, sehingga video lokal dan animasi React 100% sinkron tanpa drop frame:

```tsx
import React from 'react';
import { AbsoluteFill } from '../scaffold/src/components/AbsoluteFill';
import { VideoClip } from '../scaffold/src/components/VideoClip';
import { CameraRig, ColorGrade, KineticScrambleText } from '../scaffold/src/components/Effects';
import { useCurrentFrame } from '../scaffold/src/hooks';

export const AnnotatedDemoVideo: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ backgroundColor: '#090d16' }}>
      <ColorGrade contrast={1.05} vignetteOpacity={0.25}>
        {/* Zoom kamera halus ke arah rekaman video lokal pada frame 30..90 */}
        <CameraRig frame={frame} startFrame={30} endFrame={90} fromScale={0.88} toScale={1.0}>
          <VideoClip
            src="./assets/screen-recording.mp4"
            trimStartSeconds={1.5}
            borderRadius={16}
            style={{ boxShadow: '0 24px 64px rgba(0,0,0,0.6)' }}
          />
        </CameraRig>
      </ColorGrade>

      {/* Layer Motion Design Overlay di atas video */}
      <div style={{ position: 'absolute', top: 56, left: 80 }}>
        <KineticScrambleText
          text="LATENSI TURUN 10X: 38ms"
          frame={frame}
          durationInFrames={20}
          style={{ fontSize: 48, fontWeight: 700, color: '#38bdf8' }}
        />
      </div>
    </AbsoluteFill>
  );
};
```

### Metode B: Transparent Motion Overlay langsung via FFmpeg `--bg-video` (Zero Re-Decode Blur)
Jika ingin kualitas piksel video asli 100% utuh beserta suara aslinya, dan hanya menempelkan layer desain motion transparan (lower-third, HUD, callout badge, subtitle) di atasnya:

```bash
# 1. Render komponen motion dengan latar belakang transparan (--transparent)
node scripts/render.js --entry ./src/compositions/MotionOverlay.tsx --duration 300 --transparent --output ./out

# 2. Gabungkan (composite) frame motion transparan langsung di atas video lokal + pertahankan audio asli
node scripts/encode.js --frames ./out/frames --bg-video ./assets/input-video.mp4 --output ./out/final-edited.mp4
```

---

## 5. Pengujian Unit & Snapshot per Frame (`Vitest`)

Setiap scene wajib dapat diuji pada frame kunci (`frame 0`, `mid-animation`, `settled frame`) sebelum menjalankan render penuh:

```typescript
import { describe, it, expect } from 'vitest';
import { interpolate } from '../scaffold/src/components/Interpolate';

describe('Deterministic Frame Math', () => {
  it('clamps progress strictly between 0 and 1', () => {
    expect(interpolate(-10, [0, 30], [0, 1], 'clamp')).toBe(0);
    expect(interpolate(15, [0, 30], [0, 1], 'clamp')).toBeCloseTo(0.5);
    expect(interpolate(45, [0, 30], [0, 1], 'clamp')).toBe(1);
  });
});
```
