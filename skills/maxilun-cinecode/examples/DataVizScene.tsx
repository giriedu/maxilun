import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

interface DataPoint {
  label: string;
  value: number;
  displayValue?: string;
}

interface DataVizSceneProps {
  /** Supply verified values, or clearly label the composition as illustrative. */
  data: DataPoint[];
  title: string;
  sourceLabel: string;
}

const ink = '#171715';
const accent = '#D6492F';

export const DataVizScene: React.FC<DataVizSceneProps> = ({ data, title, sourceLabel }) => {
  const frame = useCurrentFrame();
  const maxValue = Math.max(1, ...data.map(({ value }) => Math.max(0, value)));
  const rows = data.map((point, index) => {
    const startFrame = index * 8;
    const progress = interpolate(frame, [startFrame, startFrame + 24], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });

    return { ...point, progress, widthPercent: (Math.max(0, point.value) / maxValue) * 100 };
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#F1EEE6',
        color: ink,
        padding: 96,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        fontFamily: 'Arial, sans-serif',
      }}
    >
      <h1 style={{ margin: '0 0 64px', maxWidth: 1400, fontSize: 88, lineHeight: 0.98, letterSpacing: '-0.06em' }}>
        {title}
      </h1>
      <div style={{ display: 'grid', gap: 28, maxWidth: 1450 }}>
        {rows.map(({ label, value, displayValue, progress, widthPercent }, index) => (
          <div key={`${label}-${index}`} style={{ display: 'grid', gridTemplateColumns: '260px 1fr 180px', alignItems: 'center', gap: 24 }}>
            <span style={{ fontSize: 30, fontWeight: 600 }}>{label}</span>
            <div style={{ height: 36, background: '#D7D2C8', overflow: 'hidden' }}>
              <div
                style={{
                  width: `${widthPercent * progress}%`,
                  height: '100%',
                  background: index === 0 ? accent : ink,
                }}
              />
            </div>
            <span style={{ fontSize: 30, fontVariantNumeric: 'tabular-nums', textAlign: 'right' }}>
              {displayValue ?? String(value)}
            </span>
          </div>
        ))}
      </div>
      <div style={{ position: 'absolute', left: 96, bottom: 72, fontSize: 22, color: '#55534D' }}>
        {sourceLabel}
      </div>
    </AbsoluteFill>
  );
};
