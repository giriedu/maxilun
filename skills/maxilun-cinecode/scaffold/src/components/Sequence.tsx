import React, { createContext, useContext } from 'react';
import { useCurrentFrame } from '../hooks';

interface SequenceProps {
  from: number;
  durationInFrames: number;
  name?: string;
  children: React.ReactNode;
}

export const SequenceContext = createContext<{ from: number; durationInFrames: number } | null>(null);

export const useSequence = () => useContext(SequenceContext);

export const Sequence: React.FC<SequenceProps> = ({ from, durationInFrames, children }) => {
  const frame = useCurrentFrame();

  if (frame < from || frame >= from + durationInFrames) {
    return null;
  }

  return (
    <SequenceContext.Provider value={{ from, durationInFrames }}>
      <>{children}</>
    </SequenceContext.Provider>
  );
};
