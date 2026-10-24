import React from 'react';
import { useCurrentFrame } from '../hooks';
import { interpolate } from './Interpolate';
import { useSpring } from './Spring';

export interface ProgressRingProps {
  value: number; // 0 - 100
  size?: number;
  strokeWidth?: number;
  startFrame?: number;
  durationInFrames?: number;
  color?: string;
  bgColor?: string;
  label?: string;
  showPercentage?: boolean;
}

export const ProgressRing: React.FC<ProgressRingProps> = ({
  value,
  size = 140,
  strokeWidth = 10,
  startFrame = 0,
  durationInFrames = 40,
  color = '#22d3ee',
  bgColor = 'rgba(255, 255, 255, 0.08)',
  label,
  showPercentage = true,
}) => {
  const frame = useCurrentFrame();
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;

  const progress = interpolate(
    frame,
    [startFrame, startFrame + durationInFrames],
    [0, 1],
    'clamp'
  );

  // Ease out cubic
  const eased = 1 - Math.pow(1 - progress, 3);
  const currentVal = Math.round(value * eased);
  const strokeDashoffset = circumference - (currentVal / 100) * circumference;

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div style={{ position: 'relative', width: size, height: size }}>
        <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={bgColor}
            strokeWidth={strokeWidth}
          />
          {/* Animated active arc */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            style={{
              filter: `drop-shadow(0 0 10px ${color}88)`,
            }}
          />
        </svg>

        {showPercentage && (
          <div
            style={{
              position: 'absolute',
              inset: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontFamily: "'Outfit', 'Bahnschrift', sans-serif",
              fontSize: `${Math.round(size * 0.24)}px`,
              fontWeight: 800,
              color: '#ffffff',
              fontVariantNumeric: 'tabular-nums',
            }}
          >
            {currentVal}%
          </div>
        )}
      </div>

      {label && (
        <div
          style={{
            marginTop: 12,
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 12,
            fontWeight: 700,
            color: 'rgba(255, 255, 255, 0.7)',
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
          }}
        >
          {label}
        </div>
      )}
    </div>
  );
};

export interface BarData {
  label: string;
  value: number; // 0 - 100
  formattedValue?: string;
  color?: string;
}

export interface AnimatedBarChartProps {
  data: BarData[];
  startFrame?: number;
  staggerFrames?: number;
  height?: number;
  barColor?: string;
}

export const AnimatedBarChart: React.FC<AnimatedBarChartProps> = ({
  data,
  startFrame = 0,
  staggerFrames = 6,
  height = 200,
  barColor = '#22d3ee',
}) => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'flex-end',
        gap: 20,
        height,
        padding: '16px 8px',
      }}
    >
      {data.map((item, idx) => {
        const itemStart = startFrame + idx * staggerFrames;
        const progress = interpolate(
          frame,
          [itemStart, itemStart + 25],
          [0, 1],
          'clamp'
        );
        const eased = 1 - Math.pow(1 - progress, 3);
        const barHeight = Math.max(4, Math.round((item.value / 100) * (height - 50) * eased));
        const color = item.color || barColor;

        return (
          <div
            key={idx}
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              flex: 1,
              gap: 8,
            }}
          >
            <div
              style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: 12,
                fontWeight: 700,
                color: '#ffffff',
                fontVariantNumeric: 'tabular-nums',
                opacity: progress,
              }}
            >
              {item.formattedValue || `${Math.round(item.value * eased)}%`}
            </div>

            <div
              style={{
                width: '100%',
                maxWidth: 48,
                height: barHeight,
                backgroundColor: color,
                borderRadius: '4px 4px 0 0',
                boxShadow: `0 0 16px ${color}44`,
                transition: 'none',
              }}
            />

            <div
              style={{
                fontFamily: "'Inter', sans-serif",
                fontSize: 12,
                color: 'rgba(255, 255, 255, 0.65)',
                textAlign: 'center',
                marginTop: 4,
              }}
            >
              {item.label}
            </div>
          </div>
        );
      })}
    </div>
  );
};
