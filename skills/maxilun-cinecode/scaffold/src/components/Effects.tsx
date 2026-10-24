import React from 'react';
import { interpolate } from './Interpolate';

export interface SceneTransitionProps {
  frame: number;
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
  const progress = interpolate(frame, [0, durationInFrames], [0, 1], 'clamp');

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
  frame: number;
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
  const scale = interpolate(frame, [startFrame, endFrame], [fromScale, toScale], 'clamp');
  const x = interpolate(frame, [startFrame, endFrame], [fromX, toX], 'clamp');
  const y = interpolate(frame, [startFrame, endFrame], [fromY, toY], 'clamp');

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
