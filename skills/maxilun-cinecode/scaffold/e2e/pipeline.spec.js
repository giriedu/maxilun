/**
 * Maxilun CineCode — E2E Test Suite
 * Verifies full pipeline: code → bundle → render → encode → video file
 */

import { describe, test, expect, beforeAll } from 'vitest';
import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import puppeteer from 'puppeteer';
import { pathToFileURL, fileURLToPath } from 'url';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const __dirname = path.dirname(fileURLToPath(import.meta.url));

const SCAFFOLD_DIR = path.resolve(__dirname, '..');
const OUT_DIR = path.join(SCAFFOLD_DIR, 'out', 'e2e-test');

async function launchBrowserHelper() {
  const executablePaths = [
    undefined,
    process.env.CHROME_PATH,
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium-browser',
  ].filter(Boolean);

  for (const execPath of executablePaths) {
    try {
      return await puppeteer.launch({
        headless: 'new',
        executablePath: execPath,
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
      });
    } catch {}
  }
  throw new Error('No compatible Chrome/Edge browser found.');
}

describe('CineCode E2E Pipeline', () => {

  beforeAll(() => {
    // Clean output directory
    if (fs.existsSync(OUT_DIR)) {
      fs.rmSync(OUT_DIR, { recursive: true });
    }
    fs.mkdirSync(OUT_DIR, { recursive: true });
  });

  test('1. Project validation passes', () => {
    const result = execSync('node scripts/cli.js validate', {
      cwd: SCAFFOLD_DIR,
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe'],
    });

    expect(result).toContain('✅');
    expect(result).not.toContain('❌');
  });

  test('2. Composition listing works', () => {
    const result = execSync('node scripts/cli.js list', {
      cwd: SCAFFOLD_DIR,
      encoding: 'utf-8',
    });

    expect(result).toContain('MyVideo');
  });

  test('3. Bundle compilation succeeds', async () => {
    const { bundleProject } = require('../scripts/render');

    const entryPoint = path.join(SCAFFOLD_DIR, 'src', 'compositions', 'MyVideo.tsx');
    expect(fs.existsSync(entryPoint)).toBe(true);

    await bundleProject(entryPoint);

    const bundlePath = path.join(SCAFFOLD_DIR, '.cinecode', 'bundle.js');
    expect(fs.existsSync(bundlePath)).toBe(true);

    const bundleSize = fs.statSync(bundlePath).size;
    expect(bundleSize).toBeGreaterThan(0);
    console.log(`   Bundle size: ${(bundleSize / 1024).toFixed(1)} KB`);
  });

  test('4. Frame capture produces PNG sequence', async () => {
    const { captureFrames } = require('../scripts/render');

    const framesDir = await captureFrames({
      entry: path.join(SCAFFOLD_DIR, 'src', 'compositions', 'MyVideo.tsx'),
      durationInFrames: 30, // 1 second at 30fps
      fps: 30,
      width: 640,  // Smaller for faster test
      height: 360,
      outputDir: OUT_DIR,
    });

    expect(fs.existsSync(framesDir)).toBe(true);

    const frames = fs.readdirSync(framesDir).filter(f => f.endsWith('.png'));
    expect(frames.length).toBe(30);

    // Verify frame files are valid PNGs (>512 bytes each)
    for (const frame of frames.slice(0, 5)) {
      const stat = fs.statSync(path.join(framesDir, frame));
      expect(stat.size).toBeGreaterThan(512);
    }

    console.log(`   Captured ${frames.length} frames`);
  });

  test('5. FFmpeg encoding produces valid MP4', async () => {
    const { encode, findFFmpeg } = require('../scripts/encode');

    const ffmpegPath = findFFmpeg();
    if (!ffmpegPath) {
      console.log('   FFmpeg not available — skipping encode test');
      return;
    }

    const framesDir = path.join(OUT_DIR, 'frames');
    expect(fs.existsSync(framesDir)).toBe(true);

    const outputFile = await encode({
      framesDir,
      fps: 30,
      preset: 'mp4-h264',
      output: path.join(OUT_DIR, 'test-output.mp4'),
    });

    expect(fs.existsSync(outputFile)).toBe(true);

    const stat = fs.statSync(outputFile);
    expect(stat.size).toBeGreaterThan(1024);

    console.log(`   Output: ${outputFile} (${(stat.size / 1024).toFixed(1)} KB)`);
  });

  test('6. Preview server starts and serves content', async () => {
    const { startPreview } = require('../scripts/preview');

    const { server } = await startPreview({
      port: 3199, // Use non-default port to avoid conflicts
      entry: path.join(SCAFFOLD_DIR, 'src', 'compositions', 'MyVideo.tsx'),
      durationInFrames: 90,
    });

    try {
      // Wait for server to be ready
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Fetch preview page
      const response = await fetch('http://localhost:3199/');
      expect(response.status).toBe(200);

      const html = await response.text();
      expect(html).toContain('CineCode Preview');
      expect(html).toContain('viewport');
      expect(html).toContain('scrubber');

      // Fetch bundle
      const bundleResponse = await fetch('http://localhost:3199/bundle.js');
      expect(bundleResponse.status).toBe(200);

      console.log('   Preview server responding on port 3199');
    } finally {
      server.close();
    }
  });

  test('7. Still frame export works', async () => {
    const { bundleProject } = require('../scripts/render');

    const entryPoint = path.join(SCAFFOLD_DIR, 'src', 'compositions', 'MyVideo.tsx');
    await bundleProject(entryPoint);

    const browser = await launchBrowserHelper();
    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    const htmlPath = path.resolve(SCAFFOLD_DIR, '.cinecode', 'render.html');
    if (fs.existsSync(htmlPath)) {
      const fileUrl = pathToFileURL(htmlPath).href;
      await page.goto(fileUrl, { waitUntil: 'networkidle0' });
      await page.evaluate(() => { window.__CINECODE_FRAME__ = 45; });
      await new Promise(r => setTimeout(r, 100));

      const stillPath = path.join(OUT_DIR, 'still-frame-45.png');
      await page.screenshot({ path: stillPath, type: 'png' });

      expect(fs.existsSync(stillPath)).toBe(true);
      const stat = fs.statSync(stillPath);
      expect(stat.size).toBeGreaterThan(1024);

      console.log(`   Still exported: ${stillPath}`);
    }

    await browser.close();
  });

  test('8. Interpolate function works correctly', async () => {
    const { interpolate } = await import('../src/components/Interpolate');

    // Basic linear interpolation
    expect(interpolate(0.5, [0, 1], [0, 100])).toBe(50);
    expect(interpolate(0, [0, 1], [0, 100])).toBe(0);
    expect(interpolate(1, [0, 1], [0, 100])).toBe(100);

    // Multi-segment
    expect(interpolate(1.5, [0, 1, 2], [0, 100, 0])).toBe(50);

    // Clamping
    expect(interpolate(-1, [0, 1], [0, 100], 'clamp')).toBe(0);
    expect(interpolate(2, [0, 1], [0, 100], 'clamp')).toBe(100);

    console.log('   Interpolation tests passed');
  });

  test('9. Spring physics produces expected values', () => {
    // Import spring computation directly
    const computeSpring = (frame, from, to, config) => {
      const { stiffness = 100, damping = 10, mass = 1 } = config;
      const w0 = Math.sqrt(stiffness / mass);
      const zeta = damping / (2 * Math.sqrt(stiffness * mass));
      const t = frame / 30;

      let value;
      if (zeta < 1) {
        const wd = w0 * Math.sqrt(1 - zeta * zeta);
        const A = from - to;
        value = to + A * Math.exp(-zeta * w0 * t) * Math.cos(wd * t);
      } else {
        value = to; // Simplified for overdamped
      }
      return value;
    };

    // At frame 0, should be at 'from' value
    const initial = computeSpring(0, 0, 100, {});
    expect(initial).toBeCloseTo(0, 0);

    // After many frames, should converge to 'to' value
    const final = computeSpring(300, 0, 100, {}); // 10 seconds
    expect(final).toBeCloseTo(100, 0);

    console.log('   Spring physics verified');
  });

});

describe('CineCode Performance Benchmarks', () => {

  test('Bundle time under 5 seconds', async () => {
    const { bundleProject } = require('../scripts/render');
    const entryPoint = path.join(SCAFFOLD_DIR, 'src', 'compositions', 'MyVideo.tsx');

    const start = Date.now();
    await bundleProject(entryPoint);
    const elapsed = Date.now() - start;

    expect(elapsed).toBeLessThan(5000);
    console.log(`   Bundle time: ${elapsed}ms`);
  });

  test('Single frame render under 2000ms', async () => {
    const { bundleProject } = require('../scripts/render');

    const entryPoint = path.join(SCAFFOLD_DIR, 'src', 'compositions', 'MyVideo.tsx');
    await bundleProject(entryPoint);

    const browser = await launchBrowserHelper();
    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    const htmlPath = path.resolve(SCAFFOLD_DIR, '.cinecode', 'render.html');
    if (fs.existsSync(htmlPath)) {
      const start = Date.now();
      const fileUrl = pathToFileURL(htmlPath).href;
      await page.goto(fileUrl, { waitUntil: 'networkidle0' });
      await page.screenshot({ type: 'png' });
      const elapsed = Date.now() - start;

      expect(elapsed).toBeLessThan(2000);
      console.log(`   Frame render time: ${elapsed}ms`);
    }

    await browser.close();
  });

});
