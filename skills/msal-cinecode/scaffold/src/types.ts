export interface VideoProject {
  id: string;
  fps: number;
  width: number;
  height: number;
  durationInFrames: number;
  compositions: Composition[];
  audio?: AudioTrack[];
  metadata: ProjectMetadata;
}

export interface Composition {
  id: string;
  component: React.ComponentType<CompositionProps>;
  durationInFrames: number;
  fps: number;
  width: number;
  height: number;
  defaultProps?: Record<string, unknown>;
}

export interface CompositionProps {
  frame: number;
  fps: number;
  width: number;
  height: number;
  [key: string]: unknown;
}

export interface Sequence {
  id: string;
  from: number;
  durationInFrames: number;
  component: React.ComponentType<unknown>;
  props?: Record<string, unknown>;
  name?: string;
}

export interface AudioTrack {
  src: string;
  startFrom: number;
  endAt?: number;
  volume?: number | ((frame: number) => number);
  playbackRate?: number;
}

export interface ProjectMetadata {
  title: string;
  author: string;
  description: string;
  tags?: string[];
}

export interface RenderConfig {
  outputFormat: 'mp4' | 'webm' | 'gif' | 'png-sequence';
  fps: number;
  width: number;
  height: number;
  quality: 'low' | 'medium' | 'high' | 'lossless';
  concurrency: number;
  memoryLimitMB: number;
}
