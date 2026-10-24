# Soundtrack Scoring, Beat Grid Alignment & Audio Ducking Pipeline

Gunakan referensi ini saat memproduksi musik latar asli (AI music generation via Suno/Udio), menyelaraskan birama musik dengan frame video, menghitung kurva audio ducking, atau mengonfigurasi dev server preview real-time di `maxilun-cinecode`.

---

## 1. Komposisi Musik Latar Deterministik Berbasis Storyboard

Musik latar video promosi berfungsi memperkuat emosi narasi, bukan sekadar mengisi kekosongan:

### Formula Prompt AI Music (Suno / Udio API)
```text
[Genre]: Cinematic Ambient Synthwave / Minimalist Tech Pulse
[Tempo]: 120 BPM
[Instrumentation]: Warm analog synthesizers, deep sub-bass pulse, crisp digital percussion, subtle arpeggio
[Mood]: Confident, authoritative, engineering precision, no lyrics (pure instrumental)
[Structure]: 
- Intro (0s - 5s): Sub-bass swell and light rhythmic pulse
- Build (5s - 15s): Layered arpeggios establishing momentum
- Peak (15s - 25s): Full rhythmic drive without overpowering vocal frequencies
- Outro (25s - 30s): Clean acoustic decay on sustained root chord
```

---

## 2. Perhitungan Beat Grid Video

Untuk menyinkronkan pergantian scene atau transisi visual pada ketukan musik:

$$\text{Frames Per Beat} = \text{round}\left(\frac{\text{FPS} \times 60}{\text{BPM}}\right)$$

| FPS | BPM | Frames / Beat | Durasi Per Beat | Penanda Birama 4/4 (1 Bar) |
|---|---|---|---|---|
| `30` | `120` | `15 frames` | `0.50 detik` | Setiap `60 frames` (`2.0s`) |
| `30` | `100` | `18 frames` | `0.60 detik` | Setiap `72 frames` (`2.4s`) |
| `30` | `90` | `20 frames` | `0.67 detik` | Setiap `80 frames` (`2.67s`) |
| `60` | `120` | `30 frames` | `0.50 detik` | Setiap `120 frames` (`2.0s`) |

Kunci transisi scene (misal `<SceneTransition>`) tepat pada ketukan ke-1 birama (*downbeat*) untuk dampak visual yang memuaskan.

---

## 3. Kurva Volume & Otomasi Audio Ducking

Saat suara narator (*voice-over*) aktif, volume musik latar wajib diturunkan secara mulus (*ducking*) agar vokal terdengar jernih tanpa tabrakan frekuensi:

```typescript
export function computeBgmVolume(frame: number, voiceActiveRanges: Array<[number, number]>): number {
  const baseVolume = 0.40;   // Volume musik saat tidak ada vokal
  const duckedVolume = 0.12; // Volume musik saat vokal sedang berbicara
  const fadeFrames = 8;      // Durasi transisi fade (8 frame = ~260ms @30fps)

  for (const [start, end] of voiceActiveRanges) {
    if (frame >= start - fadeFrames && frame <= end + fadeFrames) {
      if (frame < start) {
        // Fade down
        const progress = (frame - (start - fadeFrames)) / fadeFrames;
        return baseVolume - progress * (baseVolume - duckedVolume);
      } else if (frame > end) {
        // Fade up
        const progress = (frame - end) / fadeFrames;
        return duckedVolume + progress * (baseVolume - duckedVolume);
      } else {
        return duckedVolume;
      }
    }
  }

  return baseVolume;
}
```

### Standar Loudness Broadcast
- **Voice-over**: `-16 LUFS` (terkompresi lembut, EQ high-pass di `80Hz`, cut di `300Hz`).
- **Background Music**: `-24 LUFS` normal, `-32 LUFS` saat ducking.
- **Combined Final Master**: `-14 LUFS` dengan true peak limit `-1.0 dBFS`.

---

## 4. Alur Kerja Preview Real-Time (Motion Dev Server)

Untuk menghindari proses render ulang MP4 yang memakan waktu saat mengatur kurva pegas dan timing:

1. **Jalankan Dev Server**:
   ```bash
   node scripts/preview.js --port 3000
   ```
2. **Fitur Dev Server**:
   - Timeline scrubber interaktif dengan zoom frame presisi.
   - Hot module reload (HMR) instan saat berkas scene diubah.
   - Audio playback yang tersinkronisasi dengan posisi kursor timeline.
   - Pengecekan safe-area untuk preset `16:9` (`1920x1080`) dan `9:16` (`1080x1920`).
