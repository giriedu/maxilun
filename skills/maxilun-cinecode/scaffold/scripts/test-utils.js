/**
 * Maxilun CineCode — Test Utilities
 * Provides renderFrame() helper for unit testing scenes
 */

const puppeteer = require('puppeteer');
const esbuild = require('esbuild');
const path = require('path');
const fs = require('fs');

let browserInstance = null;

async function getBrowser() {
  if (!browserInstance) {
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
        browserInstance = await puppeteer.launch({
          headless: 'new',
          executablePath: execPath,
          args: ['--no-sandbox', '--disable-setuid-sandbox'],
        });
        break;
      } catch {}
    }
  }
  return browserInstance;
}

async function closeBrowser() {
  if (browserInstance) {
    await browserInstance.close();
    browserInstance = null;
  }
}

/**
 * Render a single frame of a component and return screenshot buffer
 * @param {React.ComponentType} Component - React component to render
 * @param {Object} options - Render options
 * @returns {Promise<Buffer>} PNG screenshot buffer
 */
async function renderFrame(Component, options = {}) {
  const {
    frame = 0,
    fps = 30,
    width = 1920,
    height = 1080,
    props = {},
  } = options;

  // Create temporary entry file
  const tmpDir = '.cinecode/test';
  fs.mkdirSync(tmpDir, { recursive: true });

  const componentName = Component.name || 'TestComponent';
  const entryContent = `
    import React from 'react';
    import { createRoot } from 'react-dom/client';

    window.__CINECODE_FRAME__ = ${frame};
    window.__CINECODE_FPS__ = ${fps};
    window.__CINECODE_WIDTH__ = ${width};
    window.__CINECODE_HEIGHT__ = ${height};
    window.useCurrentFrame = () => ${frame};
    window.useVideoConfig = () => ({ fps: ${fps}, width: ${width}, height: ${height} });

    // Inline component for testing
    const ${componentName} = ${Component.toString()};

    const root = createRoot(document.getElementById('root'));
    root.render(React.createElement(${componentName}, ${JSON.stringify(props)}));
  `;

  const entryPath = path.join(tmpDir, 'test-entry.tsx');
  fs.writeFileSync(entryPath, entryContent);

  // Bundle
  await esbuild.build({
    entryPoints: [entryPath],
    bundle: true,
    platform: 'browser',
    format: 'esm',
    jsx: 'automatic',
    outfile: path.join(tmpDir, 'test-bundle.js'),
    logLevel: 'silent',
  });

  // Render in browser
  const browser = await getBrowser();
  const page = await browser.newPage();
  await page.setViewport({ width, height });

  const html = `<!DOCTYPE html><html><head><style>*{margin:0;padding:0}body{width:${width}px;height:${height}px;background:#000}#root{width:100%;height:100%}</style></head><body><div id="root"></div><script type="module">${fs.readFileSync(path.join(tmpDir, 'test-bundle.js'), 'utf-8')}</script></body></html>`;

  await page.setContent(html, { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 50));

  const screenshot = await page.screenshot({ type: 'png' });
  await page.close();

  return screenshot;
}

/**
 * Measure render time for performance budget testing
 */
async function measureFrameTime(Component, options = {}) {
  const start = Date.now();
  await renderFrame(Component, options);
  return Date.now() - start;
}

/**
 * Compare two screenshots pixel-by-pixel
 * Returns percentage of different pixels
 */
function compareScreenshots(buffer1, buffer2, threshold = 0.01) {
  // Simple byte comparison for now
  // In production, use pixelmatch or similar library
  if (buffer1.length !== buffer2.length) return 1.0;

  let diffBytes = 0;
  for (let i = 0; i < buffer1.length; i++) {
    if (Math.abs(buffer1[i] - buffer2[i]) > threshold * 255) {
      diffBytes++;
    }
  }

  return diffBytes / buffer1.length;
}

module.exports = {
  renderFrame,
  measureFrameTime,
  compareScreenshots,
  closeBrowser,
};
