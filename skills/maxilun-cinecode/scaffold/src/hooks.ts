/**
 * Maxilun CineCode — React Hooks
 * Proper implementations (bukan hanya window shim)
 */

import { useState, useEffect, useMemo } from 'react';

declare global {
  interface Window {
    __CINECODE_FRAME__?: number;
    __CINECODE_FPS__?: number;
    __CINECODE_WIDTH__?: number;
    __CINECODE_HEIGHT__?: number;
    __CINECODE_DURATION__?: number;
    __CINECODE_PROPS__?: Record<string, unknown>;
  }
}

export interface CineCodeContextConfig {
  frame?: number;
  fps?: number;
  width?: number;
  height?: number;
  durationInFrames?: number;
}

export interface VideoConfig {
  fps: number;
  width: number;
  height: number;
  durationInFrames: number;
}

// Global frame state (set by renderer)
let globalFrame = 0;
let globalFps = 30;
let globalWidth = 1920;
let globalHeight = 1080;
let globalDuration = 450;
const listeners = new Set<() => void>();

export function setCineCodeContext(ctx: CineCodeContextConfig) {
  if (ctx.frame !== undefined) globalFrame = ctx.frame;
  if (ctx.fps !== undefined) globalFps = ctx.fps;
  if (ctx.width !== undefined) globalWidth = ctx.width;
  if (ctx.height !== undefined) globalHeight = ctx.height;
  if (ctx.durationInFrames !== undefined) globalDuration = ctx.durationInFrames;
  listeners.forEach(fn => fn());
}

// Initialize from window globals (renderer sets these)
if (typeof window !== 'undefined') {
  if (window.__CINECODE_FRAME__ !== undefined) globalFrame = window.__CINECODE_FRAME__;
  if (window.__CINECODE_FPS__ !== undefined) globalFps = window.__CINECODE_FPS__;
  if (window.__CINECODE_WIDTH__ !== undefined) globalWidth = window.__CINECODE_WIDTH__;
  if (window.__CINECODE_HEIGHT__ !== undefined) globalHeight = window.__CINECODE_HEIGHT__;
  if (window.__CINECODE_DURATION__ !== undefined) globalDuration = window.__CINECODE_DURATION__;

  // Listen for frame updates from renderer
  window.addEventListener('cinecode:frame', (e: Event) => {
    const customEvent = e as CustomEvent<{ frame: number }>;
    if (customEvent.detail && typeof customEvent.detail.frame === 'number') {
      setCineCodeContext({ frame: customEvent.detail.frame });
    }
  });
}

/**
 * Returns current frame number (0-indexed)
 */
export function useCurrentFrame(): number {
  const [frame, setFrame] = useState(globalFrame);

  useEffect(() => {
    const handler = () => setFrame(globalFrame);
    listeners.add(handler);
    return () => {
      listeners.delete(handler);
    };
  }, []);

  return frame;
}

/**
 * Returns video configuration
 */
export function useVideoConfig(): VideoConfig {
  return useMemo(() => ({
    fps: globalFps,
    width: globalWidth,
    height: globalHeight,
    durationInFrames: globalDuration,
  }), []);
}

/**
 * Calculate progress (0-1) within a time range
 */
export function useProgress(from: number, durationInFrames: number): number {
  const frame = useCurrentFrame();
  if (frame < from) return 0;
  if (frame >= from + durationInFrames) return 1;
  return (frame - from) / durationInFrames;
}

/**
 * Delay value until specific frame
 */
export function useDelay<T>(value: T, delayFrames: number): T | undefined {
  const frame = useCurrentFrame();
  return frame >= delayFrames ? value : undefined;
}

/**
 * Loop a value within frame range
 */
export function useLoop(durationInFrames: number): number {
  const frame = useCurrentFrame();
  return (frame % durationInFrames) / durationInFrames;
}
