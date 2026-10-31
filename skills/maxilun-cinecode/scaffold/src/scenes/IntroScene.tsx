import React from 'react';
import { AbsoluteFill } from '../components/AbsoluteFill';
import { KineticHeadline, MaskedSlideText } from '../components/KineticTypography';
import { ArchitecturalFrame } from '../components/MotionShapes';
import { CameraRig } from '../components/Effects';

interface IntroSceneProps {
  title?: string;
  tagline?: string;
}

export const IntroScene: React.FC<IntroSceneProps> = ({
  title = 'Maxilun CineCode',
  tagline = 'SYSTEM STUDY / 01',
}) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#F1EEE6',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
      }}
    >
      <CameraRig fromScale={1.03} toScale={1.0} fromX={10} toX={0}>
        <ArchitecturalFrame
          width={840}
          height={320}
          startFrame={0}
          color="rgba(23, 23, 21, 0.22)"
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '36px 48px',
          }}
        >
          <KineticHeadline
            text={title}
            startFrame={5}
            staggerFrames={3}
            fontSize={96}
            color="#171715"
            highlightWords={['CineCode']}
            highlightColor="#D6492F"
          />

          <div style={{ marginTop: 20 }}>
            <MaskedSlideText startFrame={25} durationInFrames={20}>
              <div
                style={{
                  fontFamily: "'JetBrains Mono', monospace",
                  fontSize: 24,
                  fontWeight: 600,
                  color: '#55534D',
                  letterSpacing: '0.12em',
                  textTransform: 'uppercase',
                }}
              >
                {tagline}
              </div>
            </MaskedSlideText>
          </div>
        </ArchitecturalFrame>
      </CameraRig>

    </AbsoluteFill>
  );
};
