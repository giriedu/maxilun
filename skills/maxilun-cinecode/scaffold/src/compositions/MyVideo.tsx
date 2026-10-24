import React from 'react';
import { AbsoluteFill } from '../components/AbsoluteFill';
import { Sequence } from '../components/Sequence';
import { IntroScene } from '../scenes/IntroScene';
import { SceneTransition, ColorGrade } from '../components/Effects';
import { KineticHeadline, MaskedSlideText, CounterOdometer } from '../components/KineticTypography';
import { ProgressRing, AnimatedBarChart } from '../components/DataMotion';
import { LogoReveal } from '../components/LogoReveal';

export const MyVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#090a10', color: '#ffffff' }}>
      <ColorGrade contrast={1.03} saturate={1.04} vignetteOpacity={0.24}>
        {/* Scene 1: Kinetic Intro (f0 - f90 / 3.0s) */}
        <Sequence from={0} durationInFrames={90} name="Scene 1: Kinetic Intro">
          <IntroScene title="Maxilun CineCode" tagline="Programmatic Studio Engine" />
        </Sequence>

        {/* Scene 2: High-Velocity Metrics Showcase (f90 - f240 / 5.0s) */}
        <Sequence from={90} durationInFrames={150} name="Scene 2: Data Metrics">
          <SceneTransition type="wipe-right">
            <AbsoluteFill
              style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                padding: '96px 120px',
              }}
            >
              <div>
                <KineticHeadline
                  text="Deterministic Frame Synthesis"
                  startFrame={10}
                  fontSize={56}
                  highlightWords={['Synthesis']}
                  highlightColor="#10b981"
                />
                <div style={{ marginTop: 12 }}>
                  <MaskedSlideText startFrame={22} durationInFrames={18}>
                    <p style={{ color: 'rgba(255,255,255,0.7)', fontSize: 22, margin: 0 }}>
                      Zero frame drift. Closed-form spring physics across every render target.
                    </p>
                  </MaskedSlideText>
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 64, alignItems: 'center' }}>
                <ProgressRing
                  value={98}
                  startFrame={30}
                  size={180}
                  strokeWidth={14}
                  color="#10b981"
                  label="Render Determinism"
                />

                <div>
                  <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 13, color: 'rgba(255,255,255,0.6)', marginBottom: 8 }}>
                    BENCHMARK RENDER SPEED
                  </div>
                  <CounterOdometer
                    fromValue={0}
                    toValue={120}
                    startFrame={35}
                    suffix=" FPS"
                    fontSize={64}
                    color="#22d3ee"
                  />
                  <div style={{ marginTop: 16 }}>
                    <AnimatedBarChart
                      startFrame={45}
                      height={140}
                      data={[
                        { label: 'Puppeteer', value: 75, formattedValue: '75 fps' },
                        { label: 'Remotion', value: 90, formattedValue: '90 fps' },
                        { label: 'CineCode Native', value: 100, formattedValue: '120 fps', color: '#10b981' },
                      ]}
                    />
                  </div>
                </div>
              </div>
            </AbsoluteFill>
          </SceneTransition>
        </Sequence>

        {/* Scene 3: Clean Outro with Logo Reveal (f240 - f360 / 4.0s) */}
        <Sequence from={240} durationInFrames={120} name="Scene 3: Logo Reveal">
          <SceneTransition type="zoom-through">
            <AbsoluteFill style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <LogoReveal
                brandName="MAXILUN"
                tagline="Biro Desain Identitas & Sistem Web Resmi"
              />
            </AbsoluteFill>
          </SceneTransition>
        </Sequence>
      </ColorGrade>
    </AbsoluteFill>
  );
};
