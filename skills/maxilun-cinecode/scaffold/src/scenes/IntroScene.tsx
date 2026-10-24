import React from 'react';
import { AbsoluteFill } from '../components/AbsoluteFill';
import { KineticHeadline, MaskedSlideText } from '../components/KineticTypography';
import { ArchitecturalFrame, ParticleBurst } from '../components/MotionShapes';
import { CameraRig, FilmGrainOverlay } from '../components/Effects';
import { useCurrentFrame } from '../hooks';

interface IntroSceneProps {
  title?: string;
  tagline?: string;
}

export const IntroScene: React.FC<IntroSceneProps> = ({
  title = 'Maxilun CineCode',
  tagline = 'Deterministic Programmatic Video Studio',
}) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#090a10',
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
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '36px 48px',
          }}
        >
          <ParticleBurst startFrame={10} particleCount={20} radius={140} color="#22d3ee" accentColor="#818cf8" />

          <KineticHeadline
            text={title}
            startFrame={5}
            staggerFrames={5}
            fontSize={72}
            highlightWords={['CineCode']}
            highlightColor="#22d3ee"
          />

          <div style={{ marginTop: 20 }}>
            <MaskedSlideText startFrame={25} durationInFrames={20}>
              <div
                style={{
                  fontFamily: "'JetBrains Mono', monospace",
                  fontSize: 18,
                  fontWeight: 600,
                  color: 'rgba(255, 255, 255, 0.7)',
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

      <FilmGrainOverlay frame={frame} opacity={0.03} />
    </AbsoluteFill>
  );
};
