import React from 'react';
import { AbsoluteFill } from '../components/AbsoluteFill';
import { Sequence } from '../components/Sequence';
import { IntroScene } from '../scenes/IntroScene';

export const MyVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a' }}>
      {/* Intro: 0-90 frames (3 seconds at 30fps) */}
      <Sequence from={0} durationInFrames={90} name="intro">
        <IntroScene title="Maxilun CineCode" />
      </Sequence>

      {/* Main content placeholder: 90-390 frames (10 seconds) */}
      <Sequence from={90} durationInFrames={300} name="main">
        <AbsoluteFill
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <p style={{ color: '#888', fontSize: '40px' }}>Main Content</p>
        </AbsoluteFill>
      </Sequence>

      {/* Outro: 390-450 frames (2 seconds) */}
      <Sequence from={390} durationInFrames={60} name="outro">
        <AbsoluteFill
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <p style={{ color: '#666', fontSize: '32px' }}>Get Started → maxilun.com</p>
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};
