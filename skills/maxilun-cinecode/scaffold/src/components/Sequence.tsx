import React, { createContext, useContext } from 'react';
import { FrameOffsetContext, useCurrentFrame } from '../hooks';

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
  const parentOffset = useContext(FrameOffsetContext);

  if (frame < from || frame >= from + durationInFrames) {
    return null;
  }

  return (
    <FrameOffsetContext.Provider value={parentOffset + from}>
      <SequenceContext.Provider value={{ from, durationInFrames }}>
        <>{children}</>
      </SequenceContext.Provider>
    </FrameOffsetContext.Provider>
  );
};
