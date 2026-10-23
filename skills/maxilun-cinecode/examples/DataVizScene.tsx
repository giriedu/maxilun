import React from 'react';
import { AbsoluteFill } from '../scaffold/src/components/AbsoluteFill';
import { interpolate } from '../scaffold/src/components/Interpolate';

interface DataPoint {
  label: string;
  value: number;
}

interface DataVizSceneProps {
  data: DataPoint[];
  frame: number;
}

export const DataVizScene: React.FC<DataVizSceneProps> = ({ data, frame }) => {
  const maxBarWidth = 600;
  const barHeight = 60;
  const gap = 20;
  const maxValue = Math.max(...data.map(d => d.value));

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#111',
        padding: '80px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        gap: `${gap}px`,
      }}
    >
      {data.map((point, i) => {
        // Animate bars growing from 0 to full width over 30 frames per bar
        const startFrame = i * 10;
        const progress = interpolate(
          frame - startFrame,
          [0, 30],
          [0, 1],
          'clamp'
        );

        const barWidth = (point.value / maxValue) * maxBarWidth * progress;

        return (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
            <span
              style={{
                color: '#fff',
                fontSize: '24px',
                fontFamily: 'system-ui',
                width: '200px',
                textAlign: 'right',
              }}
            >
              {point.label}
            </span>
            <div
              style={{
                width: `${barWidth}px`,
                height: `${barHeight}px`,
                backgroundColor: `hsl(${220 + i * 30}, 70%, 50%)`,
                borderRadius: '4px',
                transition: 'none',
              }}
            />
            <span
              style={{
                color: '#aaa',
                fontSize: '20px',
                fontFamily: 'monospace',
              }}
            >
              {Math.round(point.value * progress)}
            </span>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
