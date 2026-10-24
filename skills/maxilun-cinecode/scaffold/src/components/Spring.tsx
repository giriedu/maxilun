/**
 * Maxilun CineCode — Spring Animation Component
 * Physics-based animation dengan configurable stiffness, damping, mass
 */

import React, { useMemo } from 'react';
import { useCurrentFrame, useVideoConfig } from '../hooks';

interface SpringConfig {
  stiffness?: number;  // Default: 100
  damping?: number;    // Default: 10
  mass?: number;       // Default: 1
  overshootClamping?: boolean;
}

interface SpringProps {
  from: number;
  to: number;
  config?: SpringConfig;
  startFrame?: number;
  children: (value: number) => React.ReactNode;
}

// Pre-compute spring physics
function computeSpring(
  frame: number,
  from: number,
  to: number,
  config: Required<SpringConfig>,
  fps: number = 30
): number {
  const { stiffness, damping, mass } = config;

  // Damped harmonic oscillator
  const w0 = Math.sqrt(stiffness / mass);
  const zeta = damping / (2 * Math.sqrt(stiffness * mass));

  const t = frame / (fps || 30); // Convert frames to seconds

  let value: number;

  if (zeta < 1) {
    // Underdamped
    const wd = w0 * Math.sqrt(1 - zeta * zeta);
    const A = from - to;
    value = to + A * Math.exp(-zeta * w0 * t) * Math.cos(wd * t);
  } else if (zeta === 1) {
    // Critically damped
    const A = from - to;
    value = to + A * (1 + w0 * t) * Math.exp(-w0 * t);
  } else {
    // Overdamped
    const r1 = -w0 * (zeta - Math.sqrt(zeta * zeta - 1));
    const r2 = -w0 * (zeta + Math.sqrt(zeta * zeta - 1));
    const A = from - to;
    value = to + A * (r2 * Math.exp(r1 * t) - r1 * Math.exp(r2 * t)) / (r2 - r1);
  }

  if (config.overshootClamping) {
    if (from < to) value = Math.min(value, to);
    else value = Math.max(value, to);
  }

  return value;
}

export const Spring: React.FC<SpringProps> = ({
  from,
  to,
  config = {},
  startFrame = 0,
  children,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fullConfig: Required<SpringConfig> = {
    stiffness: config.stiffness ?? 100,
    damping: config.damping ?? 10,
    mass: config.mass ?? 1,
    overshootClamping: config.overshootClamping ?? false,
  };

  const value = useMemo(() => {
    const elapsed = Math.max(0, frame - startFrame);
    return computeSpring(elapsed, from, to, fullConfig, fps);
  }, [frame, from, to, startFrame, fps, fullConfig.stiffness, fullConfig.damping, fullConfig.mass, fullConfig.overshootClamping]);

  return <>{children(value)}</>;
};

/**
 * Hook version for use outside JSX
 */
export function useSpring(from: number, to: number, config?: SpringConfig & { startFrame?: number }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const startFrame = config?.startFrame ?? 0;

  const fullConfig: Required<SpringConfig> = {
    stiffness: config?.stiffness ?? 100,
    damping: config?.damping ?? 10,
    mass: config?.mass ?? 1,
    overshootClamping: config?.overshootClamping ?? false,
  };

  const elapsed = Math.max(0, frame - startFrame);
  return computeSpring(elapsed, from, to, fullConfig, fps);
}
