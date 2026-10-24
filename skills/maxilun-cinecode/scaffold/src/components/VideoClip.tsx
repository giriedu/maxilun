import React, { useEffect, useRef } from 'react';
import { useCurrentFrame, useVideoConfig } from '../hooks';

export interface VideoClipProps {
  /** Local file path or URL to the source video in the project folder */
  src: string;
  /** Frame in the composition where this clip starts playing */
  startFrom?: number;
  /** Trim offset (in seconds) inside the source video file */
  trimStartSeconds?: number;
  /** Playback speed multiplier (default: 1) */
  playbackRate?: number;
  /** CSS object-fit mode (default: 'cover') */
  fit?: 'cover' | 'contain' | 'fill';
  /** Optional device frame / container border radius */
  borderRadius?: number;
  /** Optional custom styles (scale, shadow, position) */
  style?: React.CSSProperties;
}

/**
 * Frame-synchronized <VideoClip> component for embedding and editing existing
 * video files inside a CineCode composition.
 *
 * On every frame `f`, it seeks the underlying HTML5 <video> element to the exact
 * timestamp `trimStartSeconds + ((f - startFrom) / fps) * playbackRate` and
 * registers a readiness promise in `window.__CINECODE_PENDING_PROMISES__` so the
 * headless frame renderer waits for `seeked` before capturing the PNG frame.
 */
export const VideoClip: React.FC<VideoClipProps> = ({
  src,
  startFrom = 0,
  trimStartSeconds = 0,
  playbackRate = 1,
  fit = 'cover',
  borderRadius = 0,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const videoRef = useRef<HTMLVideoElement | null>(null);

  const relativeFrame = Math.max(0, frame - startFrom);
  const targetTimeSeconds = trimStartSeconds + (relativeFrame / fps) * playbackRate;

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const { promise: seekPromise, resolve } = Promise.withResolvers<void>();

    const applySeek = () => {
      if (Math.abs(video.currentTime - targetTimeSeconds) < 0.005) {
        resolve();
        return;
      }
      const onSeeked = () => {
        video.removeEventListener('seeked', onSeeked);
        resolve();
      };
      video.addEventListener('seeked', onSeeked, { once: true });
      try {
        video.currentTime = targetTimeSeconds;
      } catch {
        resolve();
      }
    };

    if (video.readyState >= 1) {
      applySeek();
    } else {
      video.addEventListener('loadedmetadata', applySeek, { once: true });
      video.addEventListener('error', () => resolve(), { once: true });
    }

    if (typeof window !== 'undefined') {
      const win = window as unknown as { __CINECODE_PENDING_PROMISES__?: Promise<unknown>[] };
      if (!win.__CINECODE_PENDING_PROMISES__) {
        win.__CINECODE_PENDING_PROMISES__ = [];
      }
      win.__CINECODE_PENDING_PROMISES__.push(seekPromise);
    }
  }, [targetTimeSeconds]);

  return (
    <video
      ref={videoRef}
      src={src}
      muted
      playsInline
      preload="auto"
      style={{
        width: '100%',
        height: '100%',
        objectFit: fit,
        borderRadius: borderRadius ? `${borderRadius}px` : undefined,
        display: 'block',
        ...style,
      }}
    />
  );
};
