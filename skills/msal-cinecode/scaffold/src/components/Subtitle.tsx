/**
 * Maxilun CineCode — Subtitle Component
 * Timed caption overlay with accessibility compliance
 */

import React from 'react';
import { useCurrentFrame } from '../hooks';

interface SubtitleSegment {
  start: number;      // Start frame
  end: number;        // End frame
  text: string;
}

interface SubtitleProps {
  segments: SubtitleSegment[];
  style?: React.CSSProperties;
  position?: 'top' | 'center' | 'bottom';
  fontSize?: number;
  backgroundColor?: string;
  textColor?: string;
  padding?: string;
  borderRadius?: number;
}

export const Subtitle: React.FC<SubtitleProps> = ({
  segments,
  style,
  position = 'bottom',
  fontSize = 32,
  backgroundColor = 'rgba(0, 0, 0, 0.75)',
  textColor = '#ffffff',
  padding = '12px 24px',
  borderRadius = 8,
}) => {
  const frame = useCurrentFrame();

  // Find active segment
  const activeSegment = segments.find(s => frame >= s.start && frame < s.end);

  if (!activeSegment) return null;

  const positionStyles: Record<string, React.CSSProperties> = {
    top: { top: '10%', left: '50%', transform: 'translateX(-50%)' },
    center: { top: '50%', left: '50%', transform: 'translate(-50%, -50%)' },
    bottom: { bottom: '10%', left: '50%', transform: 'translateX(-50%)' },
  };

  return (
    <div
      role="region"
      aria-live="polite"
      aria-label="Subtitle"
      style={{
        position: 'absolute',
        ...positionStyles[position],
        backgroundColor,
        color: textColor,
        fontSize: `${fontSize}px`,
        fontFamily: 'system-ui, -apple-system, sans-serif',
        fontWeight: 500,
        padding,
        borderRadius: `${borderRadius}px`,
        maxWidth: '80%',
        textAlign: 'center',
        lineHeight: 1.4,
        zIndex: 1000,
        pointerEvents: 'none',
        ...style,
      }}
    >
      {activeSegment.text}
    </div>
  );
};

/**
 * Generate SRT subtitle file content from segments
 */
export function generateSRT(segments: SubtitleSegment[], fps: number = 30): string {
  return segments.map((seg, i) => {
    const start = formatSRTTime(seg.start / fps);
    const end = formatSRTTime(seg.end / fps);
    return `${i + 1}\n${start} --> ${end}\n${seg.text}\n`;
  }).join('\n');
}

/**
 * Generate WebVTT subtitle file content from segments
 */
export function generateVTT(segments: SubtitleSegment[], fps: number = 30): string {
  const header = 'WEBVTT\n\n';
  const cues = segments.map((seg, i) => {
    const start = formatVTTTime(seg.start / fps);
    const end = formatVTTTime(seg.end / fps);
    return `${i + 1}\n${start} --> ${end}\n${seg.text}\n`;
  }).join('\n');
  return header + cues;
}

function formatSRTTime(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  const ms = Math.floor((seconds % 1) * 1000);
  return `${pad(h)}:${pad(m)}:${pad(s)},${pad(ms, 3)}`;
}

function formatVTTTime(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  const ms = Math.floor((seconds % 1) * 1000);
  return `${pad(h)}:${pad(m)}:${pad(s)}.${pad(ms, 3)}`;
}

function pad(n: number, len: number = 2): string {
  return String(n).padStart(len, '0');
}
