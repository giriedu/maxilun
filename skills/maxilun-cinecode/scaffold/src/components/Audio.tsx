/**
 * Maxilun CineCode — Audio Component
 * Embeds audio tracks with volume control and time offset
 */

import React from 'react';
import { useCurrentFrame, useVideoConfig } from '../hooks';

interface AudioProps {
  src: string;
  startFrom?: number;
  endAt?: number;
  volume?: number | ((frame: number) => number);
  playbackRate?: number;
  muted?: boolean;
}

export const Audio: React.FC<AudioProps> = ({
  src,
  startFrom = 0,
  endAt,
  volume = 1,
  playbackRate = 1,
  muted = false,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Calculate if audio should be playing
  const isPlaying = frame >= startFrom && (endAt === undefined || frame < endAt);

  // Calculate current volume
  const currentVolume = typeof volume === 'function' ? volume(frame - startFrom) : volume;

  // In actual render, this would be handled by the renderer's audio mixing pipeline
  // For preview, we render an HTML5 audio element
  if (typeof window !== 'undefined' && isPlaying) {
    const currentTime = ((frame - startFrom) / (fps || 30)) * playbackRate;

    return (
      <audio
        src={src}
        autoPlay
        muted={muted}
        data-cinecode-audio="true"
        data-start-frame={startFrom}
        data-end-frame={endAt}
        data-volume={currentVolume}
        style={{ display: 'none' }}
        ref={(el) => {
          if (el) {
            el.currentTime = currentTime;
            el.volume = Math.max(0, Math.min(1, currentVolume));
            el.playbackRate = playbackRate;
          }
        }}
      />
    );
  }

  return null;
};

/**
 * Text-to-Speech component (placeholder for Phase 2 TTS integration)
 */
interface TextToSpeechProps {
  text: string;
  voice?: string;
  rate?: number;
  pitch?: number;
  startFrom?: number;
}

export const TextToSpeech: React.FC<TextToSpeechProps> = ({
  text,
  voice = 'en-US-Neural',
  rate = 1,
  startFrom = 0,
}) => {
  // TTS requires external service integration
  // This is a placeholder that renders nothing during frame capture
  // Audio will be generated separately and mixed in encode phase
  return null;
};
