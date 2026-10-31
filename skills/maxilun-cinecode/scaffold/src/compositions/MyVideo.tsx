import React from 'react';
import { AbsoluteFill } from '../components/AbsoluteFill';
import { Sequence } from '../components/Sequence';
import { interpolate } from '../components/Interpolate';
import { useCurrentFrame } from '../hooks';

const ink = '#171715';
const paper = '#F1EEE6';
const signal = '#D6492F';

/** A reusable drawn path; its progress is local to the enclosing Sequence. */
const FlowPath: React.FC<{ d: string; startFrame: number; color?: string }> = ({
  d,
  startFrame,
  color = ink,
}) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [startFrame, startFrame + 24], [0, 1], 'clamp');
  return (
    <path
      d={d}
      pathLength={1000}
      fill="none"
      stroke={color}
      strokeWidth="3"
      strokeLinecap="round"
      strokeDasharray="1000"
      strokeDashoffset={1000 * (1 - progress)}
    />
  );
};

const FlowNode: React.FC<{ x: number; y: number; startFrame: number; label: string }> = ({
  x,
  y,
  startFrame,
  label,
}) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [startFrame, startFrame + 12], [0, 1], 'clamp');
  const scale = 0.35 + progress * 0.65;
  return (
    <g transform={`translate(${x} ${y}) scale(${scale})`}>
      <circle r="13" fill={signal} />
      <text
        x="0"
        y="42"
        textAnchor="middle"
        fill={ink}
        fontFamily="Arial, sans-serif"
        fontSize="22"
        fontWeight="700"
        letterSpacing="2"
      >
        {label}
      </text>
    </g>
  );
};

const OpeningShot: React.FC = () => {
  const frame = useCurrentFrame();
  const markWidth = interpolate(frame, [0, 18], [0, 220], 'clamp');
  const titleY = interpolate(frame, [8, 28], [34, 0], 'clamp');
  const titleOpacity = interpolate(frame, [8, 20], [0, 1], 'clamp');

  return (
    <AbsoluteFill style={{ backgroundColor: paper, color: ink, overflow: 'hidden' }}>
      <div style={{ position: 'absolute', left: 120, top: 120, width: markWidth, height: 12, background: signal }} />
      <div style={{ position: 'absolute', left: 120, top: 166, fontFamily: 'Arial, sans-serif', fontSize: 24, fontWeight: 700, letterSpacing: '0.12em' }}>
        SYSTEM STUDY / 01
      </div>
      <div
        style={{
          position: 'absolute',
          left: 112,
          top: 330 + titleY,
          opacity: titleOpacity,
          fontFamily: 'Arial, sans-serif',
          fontSize: 150,
          lineHeight: 0.88,
          fontWeight: 800,
          letterSpacing: '-0.075em',
        }}
      >
        ONE EVENT
        <br />
        THREE ROUTES
      </div>
      <div style={{ position: 'absolute', right: 120, bottom: 116, fontFamily: 'Arial, sans-serif', fontSize: 24, color: '#55534D' }}>
        ILLUSTRATIVE MOTION GRAPHIC
      </div>
      <div style={{ position: 'absolute', right: 120, top: 120, width: 210, height: 210, border: `2px solid ${ink}`, borderRadius: '50%' }} />
      <div style={{ position: 'absolute', right: 218, top: 218, width: 16, height: 16, borderRadius: '50%', background: signal }} />
    </AbsoluteFill>
  );
};

const MechanismShot: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: paper, color: ink, overflow: 'hidden' }}>
    <div style={{ position: 'absolute', left: 110, top: 94, fontFamily: 'Arial, sans-serif', fontSize: 24, fontWeight: 700, letterSpacing: '0.12em' }}>
      SYSTEM STUDY / 01 — ILLUSTRATIVE FLOW
    </div>
    <div style={{ position: 'absolute', left: 110, top: 172, fontFamily: 'Arial, sans-serif', fontSize: 82, lineHeight: 0.95, fontWeight: 800, letterSpacing: '-0.06em' }}>
      A signal
      <br />
      finds its path.
    </div>
    <svg
      viewBox="0 0 900 600"
      width="900"
      height="600"
      style={{ position: 'absolute', right: 90, top: 250, overflow: 'visible' }}
    >
      <FlowPath d="M80 300 H310" startFrame={4} />
      <FlowPath d="M310 300 C420 300 420 130 560 130 H780" startFrame={22} />
      <FlowPath d="M310 300 H780" startFrame={30} />
      <FlowPath d="M310 300 C420 300 420 470 560 470 H780" startFrame={38} />
      <FlowNode x={80} y={300} startFrame={0} label="EVENT" />
      <FlowNode x={310} y={300} startFrame={18} label="ROUTE" />
      <FlowNode x={780} y={130} startFrame={44} label="CAPTURE" />
      <FlowNode x={780} y={300} startFrame={50} label="TRANSFORM" />
      <FlowNode x={780} y={470} startFrame={56} label="RESPOND" />
    </svg>
    <div style={{ position: 'absolute', left: 110, bottom: 112, width: 560, height: 2, background: '#B8B3A8' }} />
    <div style={{ position: 'absolute', left: 110, bottom: 70, fontFamily: 'Arial, sans-serif', fontSize: 22, color: '#55534D' }}>
      Concept diagram — no product metrics
    </div>
  </AbsoluteFill>
);

const ClosingShot: React.FC = () => {
  const frame = useCurrentFrame();
  const reveal = interpolate(frame, [0, 22], [0, 1], 'clamp');
  const lineWidth = interpolate(frame, [12, 38], [0, 420], 'clamp');
  return (
    <AbsoluteFill style={{ backgroundColor: ink, color: paper, overflow: 'hidden' }}>
      <div style={{ position: 'absolute', left: 120, top: 108, fontFamily: 'Arial, sans-serif', fontSize: 24, fontWeight: 700, letterSpacing: '0.12em', color: '#C9C4B9' }}>
        SYSTEM STUDY / 01
      </div>
      <div style={{ position: 'absolute', left: 112, top: 315, opacity: reveal, transform: `translateY(${(1 - reveal) * 28}px)`, fontFamily: 'Arial, sans-serif', fontSize: 142, lineHeight: 0.9, fontWeight: 800, letterSpacing: '-0.075em' }}>
        MAKE THE
        <br />
        FLOW VISIBLE.
      </div>
      <div style={{ position: 'absolute', left: 120, bottom: 205, height: 10, width: lineWidth, background: signal }} />
      <div style={{ position: 'absolute', right: 130, bottom: 126, fontFamily: 'Arial, sans-serif', fontSize: 24, color: '#C9C4B9' }}>
        MOTION GRAPHICS / STUDY 01
      </div>
    </AbsoluteFill>
  );
};

export const MyVideo: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: paper }}>
    <Sequence from={0} durationInFrames={90} name="Opening: three routes">
      <OpeningShot />
    </Sequence>
    <Sequence from={90} durationInFrames={150} name="Mechanism: illustrative flow">
      <MechanismShot />
    </Sequence>
    <Sequence from={240} durationInFrames={120} name="Close: make the flow visible">
      <ClosingShot />
    </Sequence>
  </AbsoluteFill>
);
