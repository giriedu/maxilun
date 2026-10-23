import React from 'react';
import { AbsoluteFill } from '../components/AbsoluteFill';

interface IntroSceneProps {
  title: string;
}

export const IntroScene: React.FC<IntroSceneProps> = ({ title }) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0a0a0a',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <h1
        style={{
          color: '#ffffff',
          fontSize: '80px',
          fontFamily: 'system-ui, sans-serif',
          fontWeight: 700,
          margin: 0,
        }}
      >
        {title}
      </h1>
    </AbsoluteFill>
  );
};
