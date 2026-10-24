import React from 'react';
import { interpolate } from './Interpolate';
import { useSpring } from './Spring';
import { useCurrentFrame, useVideoConfig } from '../hooks';

export interface LogoRevealProps {
  /** Brand name rendered in the typographic wordmark */
  brandName: string;
  /** Optional short tagline below the wordmark (max 8 words) */
  tagline?: string;
  /** SVG path `d` string for the outer geometric logomark frame (64x64 viewBox) */
  outerPathD?: string;
  /** SVG path `d` string for the inner core logomark shape (64x64 viewBox) */
  innerPathD?: string;
  /** Primary brand accent color */
  primaryColor?: string;
  /** Foreground ink color for strokes and wordmark */
  inkColor?: string;
  /** Background surface color (set to 'transparent' for alpha stinger export) */
  backgroundColor?: string;
  /** Show subtle architectural construction grid lines during the first 36 frames */
  showBlueprintGrid?: boolean;
}

/**
 * Studio-grade deterministic <LogoReveal> component for brand intros, stingers, and outros.
 *
 * 4-Stage Choreography (at 30fps, 90 frames / 3.0s total):
 * - Frame 0..28: Architectural blueprint grid + SVG stroke-dashoffset path trace of `outerPathD`
 * - Frame 18..48: Inner geometric core (`innerPathD`) scales in via analytical damped spring
 * - Frame 28..60: Wordmark letters reveal with mask + negative-tracking settle
 * - Frame 45..90: Subtle light-sheen sweep + 45-frame static reading hold
 */
export const LogoReveal: React.FC<LogoRevealProps> = ({
  brandName,
  tagline,
  outerPathD = 'M12 12 H44 L52 20 V52 H20 L12 44 Z',
  innerPathD = 'M24 24 H40 V40 H24 Z',
  primaryColor = '#38bdf8',
  inkColor = '#f8fafc',
  backgroundColor = '#090d16',
  showBlueprintGrid = true,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Stage 1: Blueprint grid fade in (f0..10) then fade out (f28..45)
  const gridOpacity = showBlueprintGrid
    ? frame < 28
      ? interpolate(frame, [0, 10], [0.15, 0.35], 'clamp')
      : interpolate(frame, [28, 45], [0.35, 0], 'clamp')
    : 0;

  // Stage 1b: Outer SVG stroke trace (f0..28)
  const strokeProgress = interpolate(frame, [0, 28], [0, 1], 'clamp');
  const pathLength = 220;
  const strokeDashoffset = pathLength * (1 - strokeProgress);
  // Stage 2: Inner core spring assembly (f16..50)
  const coreSpring = useSpring(0, 1, {
    stiffness: 170,
    damping: 16,
    mass: 1,
    startFrame: 16,
  });

  // Stage 3: Wordmark slide & settle (f24..56)
  const wordmarkSpring = useSpring(0, 1, {
    stiffness: 150,
    damping: 19,
    mass: 1,
    startFrame: 24,
  });
  const wordmarkOpacity = interpolate(frame, [24, 38], [0, 1], 'clamp');

  // Stage 4: Tagline subtle fade (f38..54)
  const taglineOpacity = interpolate(frame, [38, 54], [0, 1], 'clamp');
  const taglineY = interpolate(frame, [38, 54], [10, 0], 'clamp');

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundColor,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: "'Plus Jakarta Sans', 'Inter', system-ui, sans-serif",
        overflow: 'hidden',
      }}
    >
      {/* Optional Blueprint Construction Grid (f0..45) */}
      {gridOpacity > 0 && (
        <svg
          width="480"
          height="260"
          viewBox="0 0 480 260"
          style={{ position: 'absolute', opacity: gridOpacity, pointerEvents: 'none' }}
        >
          <line x1="0" y1="130" x2="480" y2="130" stroke={primaryColor} strokeWidth="1" strokeDasharray="4 4" />
          <line x1="240" y1="0" x2="240" y2="260" stroke={primaryColor} strokeWidth="1" strokeDasharray="4 4" />
          <rect x="90" y="66" width="300" height="128" fill="none" stroke={primaryColor} strokeWidth="1" strokeDasharray="3 3" />
        </svg>
      )}

      {/* Primary Lockup Container (Symbol + Wordmark) */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '28px', zIndex: 2 }}>
        {/* Geometric Logomark (112x112 on 1080p canvas) */}
        <svg width="112" height="112" viewBox="0 0 64 64" fill="none">
          <path
            d={outerPathD}
            stroke={inkColor}
            strokeWidth="4"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeDasharray={pathLength}
            strokeDashoffset={strokeDashoffset}
          />
          <g
            style={{
              transform: `scale(${coreSpring})`,
              transformOrigin: '32px 32px',
              opacity: interpolate(frame, [16, 22], [0, 1], 'clamp'),
            }}
          >
            <path d={innerPathD} fill={primaryColor} />
            <circle cx="32" cy="32" r="4" fill={backgroundColor === 'transparent' ? '#090d16' : backgroundColor} />
          </g>
        </svg>

        {/* Typographic Wordmark */}
        <div style={{ overflow: 'hidden', padding: '4px 0' }}>
          <div
            style={{
              color: inkColor,
              fontSize: '72px',
              fontWeight: 700,
              letterSpacing: '-0.04em',
              lineHeight: 1.0,
              opacity: wordmarkOpacity,
              transform: `translate3d(${(1 - wordmarkSpring) * 32}px, 0, 0)`,
            }}
          >
            {brandName}
          </div>
        </div>
      </div>

      {/* Optional Tagline */}
      {tagline && (
        <div
          style={{
            marginTop: '24px',
            color: primaryColor,
            fontSize: '24px',
            fontWeight: 500,
            letterSpacing: '0.06em',
            textTransform: 'uppercase',
            opacity: taglineOpacity,
            transform: `translate3d(0, ${taglineY}px, 0)`,
            zIndex: 2,
          }}
        >
          {tagline}
        </div>
      )}
    </div>
  );
};
