import type { VideoProject, Composition } from './types';

export const project: VideoProject = {
  id: 'my-video',
  fps: 30,
  width: 1920,
  height: 1080,
  durationInFrames: 450,
  compositions: [],
  metadata: {
    title: 'My CineCode Video',
    author: 'Maxilun User',
    description: 'Generated with maxilun-cinecode',
  },
};
