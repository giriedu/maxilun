import React from 'react';
import { useCurrentFrame } from '../hooks';
import { interpolate } from './Interpolate';
import { useSpring } from './Spring';

export interface SvgTraceProps {
  pathD: string;
  width?: number;
  height?: number;
  viewBox?: string;
  strokeColor?: string;
  strokeWidth?: number;
  startFrame?: number;
  durationInFrames?: number;
  fillColor?: string;
  fillStartFrame?: number;
  pathLengthEstimate?: number;
}

export const SvgTrace: React.FC<SvgTraceProps> = ({
  pathD,
  width = 120,
  height = 120,
  viewBox = '0 0 100 100',
  strokeColor = '#22d3ee',
  strokeWidth = 3,
  startFrame = 0,
  durationInFrames = 30,
  fillColor = 'transparent',
  fillStartFrame,
  pathLengthEstimate = 400,
}) => {
  const frame = useCurrentFrame();
  const drawProgress = interpolate(
    frame,
    [startFrame, startFrame + durationInFrames],
    [0, 1],
    'clamp'
  );

  const dashOffset = pathLengthEstimate * (1 - drawProgress);
  const fillProgress = fillStartFrame !== undefined
    ? interpolate(frame, [fillStartFrame, fillStartFrame + 20], [0, 1], 'clamp')
    : 0;

  return (
    <svg
      width={width}
      height={height}
      viewBox={viewBox}
      style={{ overflow: 'visible', display: 'block' }}
    >
      <path
        d={pathD}
        fill={fillColor === 'transparent' ? 'none' : fillColor}
        fillOpacity={fillProgress}
        stroke={strokeColor}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeDasharray={pathLengthEstimate}
        strokeDashoffset={dashOffset}
      />
    </svg>
  );
};

export interface ParticleBurstProps {
  particleCount?: number;
  startFrame?: number;
  durationInFrames?: number;
  radius?: number;
  color?: string;
  accentColor?: string;
  size?: number;
}

export const ParticleBurst: React.FC<ParticleBurstProps> = ({
  particleCount = 18,
  startFrame = 0,
  durationInFrames = 25,
  radius = 120,
  color = '#22d3ee',
  accentColor = '#818cf8',
  size = 4,
}) => {
  const frame = useCurrentFrame();
  if (frame < startFrame || frame > startFrame + durationInFrames) {
    return null;
  }

  const progress = interpolate(
    frame,
    [startFrame, startFrame + durationInFrames],
    [0, 1],
    'clamp'
  );

  // Smooth outward deceleration
  const easeOut = 1 - Math.pow(1 - progress, 2);
  const opacity = interpolate(progress, [0, 0.2, 0.7, 1], [0, 1, 0.8, 0], 'clamp');

  const particles = Array.from({ length: particleCount }, (_, i) => {
    const angle = (i / particleCount) * Math.PI * 2;
    const dist = radius * easeOut * (0.8 + (i % 3) * 0.2);
    const x = Math.cos(angle) * dist;
    const y = Math.sin(angle) * dist;
    const particleColor = i % 2 === 0 ? color : accentColor;
    const pSize = size * (1 - progress * 0.4);

    return (
      <div
        key={i}
        style={{
          position: 'absolute',
          left: `calc(50% + ${x}px)`,
          top: `calc(50% + ${y}px)`,
          width: pSize,
          height: pSize,
          borderRadius: '50%',
          backgroundColor: particleColor,
          opacity,
          boxShadow: `0 0 12px ${particleColor}`,
          transform: 'translate(-50%, -50%)',
        }}
      />
    );
  });

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        pointerEvents: 'none',
      }}
    >
      {particles}
    </div>
  );
};

export interface ArchitecturalFrameProps {
  width?: number | string;
  height?: number | string;
  color?: string;
  startFrame?: number;
  children?: React.ReactNode;
  style?: React.CSSProperties;
}

/**
 * Replaces generic full-screen blueprint grids with refined architectural
 * corner brackets and subtle technical crosshairs (Purity Craft Standard).
 */
export const ArchitecturalFrame: React.FC<ArchitecturalFrameProps> = ({
  width = '100%',
  height = '100%',
  color = 'rgba(255, 255, 255, 0.15)',
  startFrame = 0,
  children,
  style,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [startFrame, startFrame + 15], [0, 1], 'clamp');
  const bracketSize = 16;
  const strokeW = 1.5;

  return (
    <div
      style={{
        position: 'relative',
        width,
        height,
        opacity,
        ...style,
      }}
    >
      {/* Top Left Bracket */}
      <svg
        style={{ position: 'absolute', top: 0, left: 0 }}
        width={bracketSize}
        height={bracketSize}
      >
        <path
          d={`M 0,${bracketSize} L 0,0 L ${bracketSize},0`}
          fill="none"
          stroke={color}
          strokeWidth={strokeW}
        />
      </svg>

      {/* Top Right Bracket */}
      <svg
        style={{ position: 'absolute', top: 0, right: 0 }}
        width={bracketSize}
        height={bracketSize}
      >
        <path
          d={`M 0,0 L ${bracketSize},0 L ${bracketSize},${bracketSize}`}
          fill="none"
          stroke={color}
          strokeWidth={strokeW}
        />
      </svg>

      {/* Bottom Left Bracket */}
      <svg
        style={{ position: 'absolute', bottom: 0, left: 0 }}
        width={bracketSize}
        height={bracketSize}
      >
        <path
          d={`M 0,0 L 0,${bracketSize} L ${bracketSize},${bracketSize}`}
          fill="none"
          stroke={color}
          strokeWidth={strokeW}
        />
      </svg>

      {/* Bottom Right Bracket */}
      <svg
        style={{ position: 'absolute', bottom: 0, right: 0 }}
        width={bracketSize}
        height={bracketSize}
      >
        <path
          d={`M 0,${bracketSize} L ${bracketSize},${bracketSize} L ${bracketSize},0`}
          fill="none"
          stroke={color}
          strokeWidth={strokeW}
        />
      </svg>

      {children}
    </div>
  );
};
