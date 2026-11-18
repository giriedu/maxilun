# Audio Direction and Remotion Timeline

Use this guide when a video brief includes music, narration, sound effects, or audio sync. Do not add a soundtrack by default if the user did not ask for one or supply an audio direction.

## 1. Plan the audio before editing

- Record the intended mood, energy curve, narration priority, language, and any music/SFX references from the brief.
- Use supplied or user-approved audio assets. If a music-generation service is available and the user asks for generated music, prepare a prompt from the brief instead of imposing a default genre, BPM, or instrumentation.
- Note the source and license/usage constraints for every external or generated track.
- Make the narration understandable at normal listening volume. Ducking, EQ, compression, and loudness targets depend on the source material and destination; do not claim broadcast compliance without measuring the final mix.

## 2. Put audio on the Remotion timeline

Use the installed Remotion API. In current versions, `<Audio>` and `<Video>` are provided by `@remotion/media`; use `staticFile()` from `remotion` for project assets in `public/`. Check current docs if the installed version differs.

```tsx
import { Audio } from '@remotion/media';
import { interpolate, staticFile, useCurrentFrame } from 'remotion';

export const MusicBed: React.FC = () => {
  const frame = useCurrentFrame();
  const volume = interpolate(frame, [0, 18, 240, 270], [0, 0.2, 0.2, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return <Audio src={staticFile('music-bed.mp3')} volume={volume} />;
};
```

### Automatic Audio Ducking Pattern
Use this standalone helper function to lower the background music volume automatically while speech intervals are active:

```tsx
export interface VoiceInterval {
  startFrame: number;
  endFrame: number;
}

export function computeAudioDuckingGain(
  frame: number,
  speechIntervals: VoiceInterval[],
  options: { duckedGainDb?: number; attackFrames?: number; releaseFrames?: number } = {}
): number {
  const { duckedGainDb = -14, attackFrames = 12, releaseFrames = 18 } = options;
  const duckedGain = Math.pow(10, duckedGainDb / 20);
  let minGain = 1.0;
  for (const interval of speechIntervals) {
    if (frame >= interval.startFrame && frame <= interval.endFrame) return duckedGain;
    if (frame >= interval.startFrame - attackFrames && frame < interval.startFrame) {
      const p = (frame - (interval.startFrame - attackFrames)) / attackFrames;
      const gain = 1.0 - p * (1.0 - duckedGain);
      if (gain < minGain) minGain = gain;
    }
    if (frame > interval.endFrame && frame <= interval.endFrame + releaseFrames) {
      const p = (frame - interval.endFrame) / releaseFrames;
      const gain = duckedGain + p * (1.0 - duckedGain);
      if (gain < minGain) minGain = gain;
    }
  }
  return minGain;
}

// Usage in timeline:
export const DuckedSoundtrack: React.FC = () => {
  const frame = useCurrentFrame();
  const speechIntervals = [
    { startFrame: 30, endFrame: 120 },
    { startFrame: 150, endFrame: 240 },
  ];
  const volume = computeAudioDuckingGain(frame, speechIntervals, { duckedGainDb: -14, attackFrames: 12, releaseFrames: 18 });

  return <Audio src={staticFile('soundtrack.mp3')} volume={volume} />;
};
```
For edits that need explicit timeline placement, use `<Sequence>` or the audio component's documented timing props. Calculate every sync point from the actual clip, frame rate, and edit; do not assume a default tempo.

## 3. Beat and narration sync

When a music track has a known BPM and stable beat grid, a rough frame interval is `fps * 60 / BPM`. Confirm the grid against the actual waveform/audio because intros, pickup beats, tempo changes, and edits can shift downbeats. Major cuts can follow the beat when that strengthens the story; narration-led scenes may intentionally cut off-beat.

For voice-over, align captions to the final narration timing. Use silence and pauses deliberately. Do not synthesize or invent narration unless the user asks for it.

## 4. Preview and export

Use Remotion Studio (`npm run dev`) to preview visual timing and audio together. Do not use the legacy `scripts/preview.js` server. Export only when requested, using the installed Remotion CLI and a format suitable for the target platform. Inspect the final audio mix and sync after rendering when a render is part of the task.

## Official references

- [Remotion video and audio](https://www.remotion.dev/docs/videos)
- [Remotion audio component](https://www.remotion.dev/docs/media/audio)
- [Remotion audio controls](https://www.remotion.dev/docs/using-audio)
