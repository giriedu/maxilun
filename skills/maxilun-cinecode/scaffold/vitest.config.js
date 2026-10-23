import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['e2e/**/*.spec.js'],
    testTimeout: 60000, // 60s for render operations
    hookTimeout: 30000,
    reporters: ['verbose'],
  },
});
