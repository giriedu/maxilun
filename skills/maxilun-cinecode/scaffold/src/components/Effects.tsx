import React from 'react';
import { useCurrentFrame } from '../hooks';
import { interpolate } from './Interpolate';

export interface SceneTransitionProps {
  frame?: number;
  durationInFrames?: number;
  type?: 'fade' | 'wipe-right' | 'wipe-up' | 'iris' | 'zoom-through';
  children: React.ReactNode;
}

/**
 * Deterministic frame-driven scene entrance transition.
 */
export const SceneTransition: React.FC<SceneTransitionProps> = ({
  frame,
  durationInFrames = 18,
  type = 'fade',
  children,
}) => {
  const currentFrame = useCurrentFrame();
  const progress = interpolate(frame ?? currentFrame, [0, durationInFrames], [0, 1], 'clamp');

  let style: React.CSSProperties = { position: 'absolute', inset: 0 };

  switch (type) {
    case 'fade':
      style.opacity = progress;
      break;
    case 'wipe-right':
      style.clipPath = `inset(0 ${(1 - progress) * 100}% 0 0)`;
      break;
    case 'wipe-up':
      style.clipPath = `inset(${(1 - progress) * 100}% 0 0 0)`;
      break;
    case 'iris':
      style.clipPath = `circle(${progress * 150}% at 50% 50%)`;
      break;
    case 'zoom-through':
      style.opacity = progress;
      style.transform = `scale(${0.92 + progress * 0.08})`;
      break;
  }

  return <div style={style}>{children}</div>;
};

export interface CameraRigProps {
  frame?: number;
  startFrame?: number;
  endFrame?: number;
  fromScale?: number;
  toScale?: number;
  fromX?: number;
  toX?: number;
  fromY?: number;
  toY?: number;
  children: React.ReactNode;
}

/**
 * Deterministic 2.5D virtual camera rig (dolly, pan, tilt).
 */
export const CameraRig: React.FC<CameraRigProps> = ({
  frame,
  startFrame = 0,
  endFrame = 90,
  fromScale = 1,
  toScale = 1.06,
  fromX = 0,
  toX = 0,
  fromY = 0,
  toY = 0,
  children,
}) => {
  const currentFrame = useCurrentFrame();
  const activeFrame = frame ?? currentFrame;
  const scale = interpolate(activeFrame, [startFrame, endFrame], [fromScale, toScale], 'clamp');
  const x = interpolate(activeFrame, [startFrame, endFrame], [fromX, toX], 'clamp');
  const y = interpolate(activeFrame, [startFrame, endFrame], [fromY, toY], 'clamp');

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        transform: `translate3d(${x}px, ${y}px, 0) scale(${scale})`,
        transformOrigin: 'center center',
      }}
    >
      {children}
    </div>
  );
};

export interface RackFocusBlurProps {
  frame: number;
  startFrame: number;
  endFrame: number;
  fromBlurPx: number;
  toBlurPx: number;
  children: React.ReactNode;
}

/**
 * Deterministic depth-of-field rack focus blur wrapper.
 */
export const RackFocusBlur: React.FC<RackFocusBlurProps> = ({
  frame,
  startFrame,
  endFrame,
  fromBlurPx,
  toBlurPx,
  children,
}) => {
  const blur = interpolate(frame, [startFrame, endFrame], [fromBlurPx, toBlurPx], 'clamp');
  return (
    <div style={{ position: 'absolute', inset: 0, filter: `blur(${blur.toFixed(2)}px)` }}>
      {children}
    </div>
  );
};

export interface ColorGradeProps {
  contrast?: number;
  brightness?: number;
  saturate?: number;
  hueRotateDeg?: number;
  vignetteOpacity?: number;
  children: React.ReactNode;
}

/**
 * Studio color-grading & subtle vignette container for video scenes.
 */
export const ColorGrade: React.FC<ColorGradeProps> = ({
  contrast = 1.04,
  brightness = 1.0,
  saturate = 1.05,
  hueRotateDeg = 0,
  vignetteOpacity = 0.28,
  children,
}) => {
  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        filter: `contrast(${contrast}) brightness(${brightness}) saturate(${saturate}) hue-rotate(${hueRotateDeg}deg)`,
      }}
    >
      {children}
      {vignetteOpacity > 0 && (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            pointerEvents: 'none',
            background: `radial-gradient(circle at center, transparent 58%, rgba(0, 0, 0, ${vignetteOpacity}) 100%)`,
          }}
        />
      )}
    </div>
  );
};

export interface FilmGrainOverlayProps {
  frame: number;
  opacity?: number;
}

/**
 * Deterministic per-frame SVG fractal noise film grain overlay (prevents dark gradient banding in MP4).
 */
export const FilmGrainOverlay: React.FC<FilmGrainOverlayProps> = ({ frame, opacity = 0.04 }) => {
  const seed = (frame * 17) % 997;
  return (
    <svg
      width="100%"
      height="100%"
      style={{ position: 'absolute', inset: 0, pointerEvents: 'none', opacity, mixBlendMode: 'overlay' }}
    >
      <filter id={`grain-${seed}`}>
        <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="3" seed={seed} stitchTiles="stitch" />
      </filter>
      <rect width="100%" height="100%" filter={`url(#grain-${seed})`} />
    </svg>
  );
};

export interface KineticScrambleTextProps {
  text: string;
  frame: number;
  startFrame?: number;
  durationInFrames?: number;
  charset?: string;
  style?: React.CSSProperties;
}

/**
 * Deterministic frame-indexed character scramble decode effect for headlines, metrics, and CLI commands.
 */
export const KineticScrambleText: React.FC<KineticScrambleTextProps> = ({
  text,
  frame,
  startFrame = 0,
  durationInFrames = 24,
  charset = '01ABCDEF#$%&*+-<>',
  style,
}) => {
  const progress = interpolate(frame, [startFrame, startFrame + durationInFrames], [0, 1], 'clamp');
  const resolvedCount = Math.floor(progress * text.length);

  const displayed = text
    .split('')
    .map((char, idx) => {
      if (char === ' ' || idx < resolvedCount) return char;
      const hash = (idx * 31 + frame * 13) % charset.length;
      return charset[hash];
    })
    .join('');

  return (
    <span aria-label={text} style={style}>
      {displayed}
    </span>
  );
};

export interface VoiceInterval {
  startFrame: number;
  endFrame: number;
}

/**
 * Deterministic audio ducking curve helper.
 * Calculates volume gain (0.0 to 1.0) with logarithmic attack/release ramps
 * to automatically duck background soundtracks underneath voice-over / speech intervals.
 */
export function computeAudioDuckingGain(
  frame: number,
  speechIntervals: VoiceInterval[],
  options: {
    duckedGainDb?: number; // default -14 dB (~0.20 linear gain)
    attackFrames?: number; // fade down duration (default 12 frames)
    releaseFrames?: number; // fade up duration (default 18 frames)
  } = {}
): number {
  const { duckedGainDb = -14, attackFrames = 12, releaseFrames = 18 } = options;
  const duckedGain = Math.pow(10, duckedGainDb / 20);

  let minGain = 1.0;
  for (const interval of speechIntervals) {
    if (frame >= interval.startFrame && frame <= interval.endFrame) {
      return duckedGain;
    }
    // Attack ramp (fade down before speech begins)
    if (frame >= interval.startFrame - attackFrames && frame < interval.startFrame) {
      const p = (frame - (interval.startFrame - attackFrames)) / attackFrames;
      const gain = 1.0 - p * (1.0 - duckedGain);
      if (gain < minGain) minGain = gain;
    }
    // Release ramp (fade up after speech ends)
    if (frame > interval.endFrame && frame <= interval.endFrame + releaseFrames) {
      const p = (frame - interval.endFrame) / releaseFrames;
      const gain = duckedGain + p * (1.0 - duckedGain);
      if (gain < minGain) minGain = gain;
    }
  }
  return minGain;
}
