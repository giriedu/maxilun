#!/usr/bin/env node

/**
 * Maxilun CineCode — Core Render Pipeline
 * Phase 1: esbuild bundle + Puppeteer frame capture
 */

const esbuild = require('esbuild');
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
const { mkdir } = require('fs/promises');
const { pathToFileURL } = require('url');

const DEFAULT_CONFIG = {
  fps: 30,
  width: 1920,
  height: 1080,
  outputDir: './out',
  format: 'png-sequence', // png-sequence | mp4 | webm (mp4/webm require ffmpeg in Phase 2)
};

async function bundleProject(entryPoint) {
  console.log('[BUNDLE] Compiling TypeScript/React project...');

  const result = await esbuild.build({
    entryPoints: [entryPoint],
    bundle: true,
    platform: 'browser',
    format: 'esm',
    target: 'es2022',
    jsx: 'automatic',
    outfile: '.cinecode/bundle.js',
    external: [],
    define: {
      'process.env.NODE_ENV': '"production"',
    },
    logLevel: 'warning',
  });

  if (result.errors.length > 0) {
    throw new Error(`Bundle failed: ${result.errors.map(e => e.text).join('\n')}`);
  }

  console.log('[BUNDLE] ✓ Compiled successfully');
  return path.resolve('.cinecode/bundle.js');
}

function generateHTML(bundlePath, config) {
  const propsJSON = JSON.stringify(config.props || {});
  const fileUrl = pathToFileURL(bundlePath).href;
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { width: ${config.width}px; height: ${config.height}px; overflow: hidden; background: #000; }
    #root { width: 100%; height: 100%; position: relative; }
  </style>
</head>
<body>
  <div id="root"></div>
  <script type="module">
    import React from 'react';
    import { createRoot } from 'react-dom/client';

    // Injected by render pipeline
    window.__CINECODE_FRAME__ = 0;
    window.__CINECODE_FPS__ = ${config.fps};
    window.__CINECODE_WIDTH__ = ${config.width};
    window.__CINECODE_HEIGHT__ = ${config.height};
    window.__CINECODE_PROPS__ = ${propsJSON};

    // Frame hook shim
    window.useCurrentFrame = () => window.__CINECODE_FRAME__;
    window.useVideoConfig = () => ({
      fps: window.__CINECODE_FPS__,
      width: window.__CINECODE_WIDTH__,
      height: window.__CINECODE_HEIGHT__,
      durationInFrames: window.__CINECODE_DURATION__,
    });

    // Load bundled composition
    const module = await import('${fileUrl}');
    const Composition = module.default || module.MyVideo || Object.values(module)[0];

    if (!Composition) {
      document.getElementById('root').innerHTML = '<h1 style="color:red;padding:40px">No composition found. Export a default component or named "MyVideo".</h1>';
      throw new Error('No composition exported');
    }

    const root = createRoot(document.getElementById('root'));
    root.render(React.createElement(Composition, window.__CINECODE_PROPS__));
  </script>
</body>
</html>`;
}

async function captureFrames(config) {
  const framesDir = path.join(config.outputDir, 'frames');
  await mkdir(framesDir, { recursive: true });

  console.log(`[CAPTURE] Starting frame capture: ${config.durationInFrames} frames at ${config.fps}fps`);
  console.log(`[CAPTURE] Resolution: ${config.width}x${config.height}`);
  console.log(`[CAPTURE] Output: ${framesDir}`);

  // Try multiple browser paths (Puppeteer bundled → system Chrome → Edge)
  const executablePaths = [
    undefined, // Puppeteer's bundled Chromium
    process.env.CHROME_PATH,
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium-browser',
  ].filter(Boolean);

  let browser;
  let usedPath = null;
  for (const execPath of executablePaths) {
    try {
      browser = await puppeteer.launch({
        headless: 'new',
        executablePath: execPath,
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-gpu',
          `--window-size=${config.width},${config.height}`,
        ],
      });
      usedPath = execPath || 'bundled Chromium';
      break;
    } catch (err) {
      continue;
    }
  }

  if (!browser) {
    throw new Error(
      'No Chrome/Chromium/Edge found. Install one or run:\n' +
      '  npx puppeteer browsers install chrome\n' +
      'Or set CHROME_PATH environment variable.'
    );
  }

  console.log(`[CAPTURE] Using browser: ${usedPath}`);

  const page = await browser.newPage();
  await page.setViewport({ width: config.width, height: config.height, deviceScaleFactor: 1 });

  // Generate and load HTML
  const htmlPath = path.resolve('.cinecode/render.html');
  const bundlePath = path.resolve('.cinecode/bundle.js');
  const html = generateHTML(bundlePath, config);
  fs.writeFileSync(htmlPath, html);

  const fileUrl = pathToFileURL(htmlPath).href;
  await page.goto(fileUrl, { waitUntil: 'networkidle0' });

  // Set duration
  await page.evaluate((duration) => {
    window.__CINECODE_DURATION__ = duration;
  }, config.durationInFrames);

  const startTime = Date.now();
  let lastReportTime = startTime;

  for (let frame = 0; frame < config.durationInFrames; frame++) {
    // Set current frame
    await page.evaluate((f) => {
      window.__CINECODE_FRAME__ = f;
      // Trigger React re-render by dispatching custom event
      window.dispatchEvent(new CustomEvent('cinecode:frame', { detail: { frame: f } }));
    }, frame);

    // Wait for render to settle
    await page.waitForFunction(() => document.readyState === 'complete', { timeout: 5000 });

    // Small delay to allow React to process
    await new Promise(resolve => setTimeout(resolve, 16));

    // Capture screenshot
    const framePath = path.join(framesDir, `frame-${String(frame).padStart(6, '0')}.png`);
    await page.screenshot({
      path: framePath,
      type: 'png',
      omitBackground: false,
    });

    // Progress reporting every 5 seconds
    const now = Date.now();
    if (now - lastReportTime > 5000) {
      const elapsed = (now - startTime) / 1000;
      const fps = (frame + 1) / elapsed;
      const remaining = (config.durationInFrames - frame - 1) / fps;
      console.log(`[CAPTURE] Frame ${frame + 1}/${config.durationInFrames} (${((frame + 1) / config.durationInFrames * 100).toFixed(1)}%) — ${fps.toFixed(1)} fps — ETA: ${remaining.toFixed(0)}s`);
      lastReportTime = now;
    }
  }

  await browser.close();

  const totalTime = (Date.now() - startTime) / 1000;
  console.log(`[CAPTURE] ✓ Completed ${config.durationInFrames} frames in ${totalTime.toFixed(1)}s (${(config.durationInFrames / totalTime).toFixed(1)} fps)`);

  return framesDir;
}

async function render(options = {}) {
  const config = { ...DEFAULT_CONFIG, ...options };

  // Validate
  if (!config.entry) {
    // Auto-detect entry point
    const candidates = [
      './src/compositions/MyVideo.tsx',
      './src/index.tsx',
      './src/App.tsx',
    ];
    config.entry = candidates.find(c => fs.existsSync(c));
    if (!config.entry) {
      throw new Error(`No entry point found. Searched: ${candidates.join(', ')}. Specify --entry explicitly.`);
    }
  }

  if (!config.durationInFrames) {
    throw new Error('durationInFrames is required. Add to project config or pass --duration.');
  }

  console.log('\n╔══════════════════════════════════════╗');
  console.log('║   Maxilun CineCode Render Pipeline   ║');
  console.log('╚══════════════════════════════════════╝\n');

  // Phase 1: Bundle
  await bundleProject(config.entry);

  // Phase 2: Capture frames
  const framesDir = await captureFrames(config);

  console.log('\n✅ Render complete!');
  console.log(`   Frames: ${framesDir}`);
  console.log(`   Next: Run encode step to convert frames → video (Phase 2)\n`);

  return { framesDir, config };
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--entry' && args[i + 1]) options.entry = args[++i];
    if (args[i] === '--duration' && args[i + 1]) options.durationInFrames = parseInt(args[++i]);
    if (args[i] === '--fps' && args[i + 1]) options.fps = parseInt(args[++i]);
    if (args[i] === '--width' && args[i + 1]) options.width = parseInt(args[++i]);
    if (args[i] === '--height' && args[i + 1]) options.height = parseInt(args[++i]);
    if (args[i] === '--output' && args[i + 1]) options.outputDir = args[++i];
  }

  render(options)
    .then(() => process.exit(0))
    .catch(err => {
      console.error('\n❌ Render failed:', err.message);
      process.exit(1);
    });
}

module.exports = { render, bundleProject, captureFrames, generateHTML };
