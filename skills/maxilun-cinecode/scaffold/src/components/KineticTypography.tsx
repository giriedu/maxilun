import React from 'react';
import { useCurrentFrame, useVideoConfig } from '../hooks';
import { useSpring } from './Spring';
import { interpolate } from './Interpolate';

export interface KineticHeadlineProps {
  text: string;
  startFrame?: number;
  staggerFrames?: number;
  fontSize?: number;
  fontWeight?: number | string;
  color?: string;
  highlightWords?: string[];
  highlightColor?: string;
  fontFamily?: string;
  stiffness?: number;
  damping?: number;
  mass?: number;
}

export const KineticHeadline: React.FC<KineticHeadlineProps> = ({
  text,
  startFrame = 0,
  staggerFrames = 4,
  fontSize = 64,
  fontWeight = 800,
  color = '#ffffff',
  highlightWords = [],
  highlightColor = '#22d3ee',
  fontFamily = "'Inter', system-ui, -apple-system, sans-serif",
  stiffness = 180,
  damping = 15,
  mass = 0.8,
}) => {
  const frame = useCurrentFrame();
  const words = text.split(' ');

  return (
    <div
      style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: `${Math.round(fontSize * 0.22)}px ${Math.round(fontSize * 0.28)}px`,
        alignItems: 'baseline',
      }}
    >
      {words.map((word, idx) => {
        const wordStart = startFrame + idx * staggerFrames;
        const elapsed = Math.max(0, frame - wordStart);
        const isActive = frame >= wordStart;

        // Custom spring interpolation per word
        const progress = useSpring(0, 1, {
          stiffness,
          damping,
          mass,
          startFrame: wordStart,
        });

        const translateY = isActive ? interpolate(progress, [0, 1], [fontSize * 0.5, 0]) : fontSize * 0.5;
        const opacity = isActive ? interpolate(progress, [0, 1], [0, 1]) : 0;
        const cleanWord = word.replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, '').toLowerCase();
        const isHighlight = highlightWords.some(h => cleanWord === h.toLowerCase() || word.toLowerCase().includes(h.toLowerCase()));

        return (
          <span
            key={idx}
            style={{
              overflow: 'hidden',
              display: 'inline-block',
              padding: '2px 0',
            }}
          >
            <span
              style={{
                display: 'inline-block',
                transform: `translateY(${translateY}px)`,
                opacity,
                fontFamily,
                fontWeight,
                fontSize: `${fontSize}px`,
                letterSpacing: '-0.03em',
                lineHeight: 1.15,
                color: isHighlight ? highlightColor : color,
                textShadow: isHighlight
                  ? `0 0 35px ${highlightColor}44`
                  : 'none',
              }}
            >
              {word}
            </span>
          </span>
        );
      })}
    </div>
  );
};

export interface MaskedSlideTextProps {
  children: React.ReactNode;
  startFrame?: number;
  durationInFrames?: number;
  direction?: 'up' | 'down';
  style?: React.CSSProperties;
}

export const MaskedSlideText: React.FC<MaskedSlideTextProps> = ({
  children,
  startFrame = 0,
  durationInFrames = 20,
  direction = 'up',
  style,
}) => {
  const frame = useCurrentFrame();
  const progress = interpolate(
    frame,
    [startFrame, startFrame + durationInFrames],
    [0, 1],
    'clamp'
  );

  const initialY = direction === 'up' ? 100 : -100;
  const translateY = interpolate(progress, [0, 1], [initialY, 0], 'clamp');
  const opacity = interpolate(progress, [0, 0.4], [0, 1], 'clamp');

  return (
    <div style={{ overflow: 'hidden', display: 'inline-block', ...style }}>
      <div
        style={{
          transform: `translateY(${translateY}%)`,
          opacity,
          willChange: 'transform, opacity',
        }}
      >
        {children}
      </div>
    </div>
  );
};

export interface CounterOdometerProps {
  fromValue?: number;
  toValue: number;
  startFrame?: number;
  durationInFrames?: number;
  prefix?: string;
  suffix?: string;
  decimals?: number;
  fontSize?: number;
  color?: string;
  fontFamily?: string;
}

export const CounterOdometer: React.FC<CounterOdometerProps> = ({
  fromValue = 0,
  toValue,
  startFrame = 0,
  durationInFrames = 45,
  prefix = '',
  suffix = '',
  decimals = 0,
  fontSize = 56,
  color = '#ffffff',
  fontFamily = "'Outfit', 'Bahnschrift', sans-serif",
}) => {
  const frame = useCurrentFrame();
  const progress = interpolate(
    frame,
    [startFrame, startFrame + durationInFrames],
    [0, 1],
    'clamp'
  );

  // Smooth ease-out cubic
  const easeOut = 1 - Math.pow(1 - progress, 3);
  const currentVal = fromValue + (toValue - fromValue) * easeOut;
  const formattedNumber = decimals > 0 ? currentVal.toFixed(decimals) : Math.round(currentVal).toLocaleString();

  return (
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'baseline',
        fontFamily,
        fontVariantNumeric: 'tabular-nums',
        fontSize: `${fontSize}px`,
        fontWeight: 800,
        color,
        letterSpacing: '-0.02em',
      }}
    >
      {prefix && <span style={{ fontSize: `${Math.round(fontSize * 0.7)}px`, marginRight: '4px', opacity: 0.85 }}>{prefix}</span>}
      <span>{formattedNumber}</span>
      {suffix && <span style={{ fontSize: `${Math.round(fontSize * 0.7)}px`, marginLeft: '4px', opacity: 0.85 }}>{suffix}</span>}
    </div>
  );
};
