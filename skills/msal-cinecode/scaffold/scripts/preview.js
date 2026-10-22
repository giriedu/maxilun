#!/usr/bin/env node

/**
 * Maxilun CineCode — Preview Server with Hot Reload
 * Phase 3: Live browser preview with frame scrubbing and auto-rebuild
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { WebSocketServer } = require('ws');
const esbuild = require('esbuild');
const chokidar = require('chokidar');

const DEFAULT_PORT = 3123;

async function startPreview(options = {}) {
  const {
    port = DEFAULT_PORT,
    entry,
    fps = 30,
    width = 1920,
    height = 1080,
    durationInFrames = 450,
  } = options;

  // Auto-detect entry
  const entryPoint = entry || findEntry();
  if (!entryPoint) {
    throw new Error('No entry point found. Create src/compositions/MyVideo.tsx or specify --entry.');
  }

  console.log('\n╔══════════════════════════════════════╗');
  console.log('║   Maxilun CineCode Preview Server    ║');
  console.log('╚══════════════════════════════════════╝\n');
  console.log(`[PREVIEW] Entry: ${entryPoint}`);
  console.log(`[PREVIEW] Duration: ${durationInFrames} frames (${(durationInFrames / fps).toFixed(1)}s at ${fps}fps)`);
  console.log(`[PREVIEW] Resolution: ${width}x${height}`);

  // Ensure .cinecode directory exists
  if (!fs.existsSync('.cinecode')) fs.mkdirSync('.cinecode', { recursive: true });

  const resolvedEntryPoint = path.resolve(entryPoint).replace(/\\/g, '/');
  const previewRunnerPath = path.resolve('.cinecode', 'preview-runner.js');
  fs.writeFileSync(previewRunnerPath, `
import React from 'react';
import { createRoot } from 'react-dom/client';
import * as CompModule from '${resolvedEntryPoint}';

const Comp = CompModule.default || CompModule.MyVideo || Object.values(CompModule)[0];
window.__mountCinecode = function(container) {
  if (Comp && container) {
    const root = createRoot(container);
    root.render(React.createElement(Comp));
    return root;
  }
};
`);

  // Initial bundle
  let bundleError = null;
  async function rebuild() {
    try {
      await esbuild.build({
        entryPoints: [previewRunnerPath],
        bundle: true,
        platform: 'browser',
        format: 'esm',
        target: 'es2022',
        jsx: 'automatic',
        outfile: '.cinecode/preview-bundle.js',
        define: { 'process.env.NODE_ENV': '"development"' },
        logLevel: 'silent',
      });
      bundleError = null;
      console.log('[PREVIEW] ✓ Bundle rebuilt');
      return true;
    } catch (err) {
      bundleError = err.message;
      console.error('[PREVIEW] ✗ Bundle error:', err.message.split('\n')[0]);
      return false;
    }
  }

  await rebuild();

  // File watcher for hot reload
  const watchDirs = ['src'].filter(d => fs.existsSync(d));
  if (watchDirs.length > 0) {
    const watcher = chokidar.watch(watchDirs, { ignoreInitial: true });
    let debounceTimer = null;

    watcher.on('all', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(async () => {
        const success = await rebuild();
        if (success) {
          // Notify all connected WebSocket clients
          wss.clients.forEach(client => {
            if (client.readyState === 1) {
              client.send(JSON.stringify({ type: 'reload' }));
            }
          });
        }
      }, 200);
    });

    console.log(`[PREVIEW] Watching: ${watchDirs.join(', ')}`);
  }

  // HTTP Server
  const server = http.createServer((req, res) => {
    if (req.url === '/' || req.url === '/index.html') {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(generatePreviewHTML(fps, width, height, durationInFrames, bundleError));
    } else if (req.url === '/bundle.js') {
      try {
        const bundle = fs.readFileSync('.cinecode/preview-bundle.js', 'utf-8');
        res.writeHead(200, { 'Content-Type': 'application/javascript' });
        res.end(bundle);
      } catch {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Bundle not ready. Check console for errors.');
      }
    } else {
      res.writeHead(404);
      res.end('Not found');
    }
  });

  // WebSocket for hot reload
  const wss = new WebSocketServer({ server });
  wss.on('connection', (ws) => {
    console.log('[PREVIEW] Client connected');
    ws.on('close', () => console.log('[PREVIEW] Client disconnected'));
  });

  server.listen(port, () => {
    console.log(`\n🎬 Preview ready: http://localhost:${port}`);
    console.log('   Press Ctrl+C to stop\n');
  });

  return { server, wss };
}

function findEntry() {
  const candidates = [
    './src/compositions/MyVideo.tsx',
    './src/index.tsx',
    './src/App.tsx',
  ];
  return candidates.find(c => fs.existsSync(c));
}

function generatePreviewHTML(fps, width, height, durationInFrames, bundleError) {
  const scale = 0.5; // Preview at 50% scale
  const previewWidth = Math.round(width * scale);
  const previewHeight = Math.round(height * scale);

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>CineCode Preview</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #111; color: #eee; font-family: system-ui, sans-serif; display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding: 20px; }
    #viewport { width: ${previewWidth}px; height: ${previewHeight}px; position: relative; overflow: hidden; background: #000; border: 1px solid #333; margin-bottom: 16px; }
    #viewport iframe { width: ${width}px; height: ${height}px; border: none; transform: scale(${scale}); transform-origin: top left; }
    #controls { display: flex; align-items: center; gap: 12px; padding: 12px 20px; background: #222; border-radius: 8px; }
    button { background: #444; color: #fff; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-size: 14px; }
    button:hover { background: #555; }
    button.active { background: #7c3aed; }
    input[type=range] { width: 300px; }
    #info { font-size: 13px; color: #888; margin-top: 8px; }
    #error { color: #f87171; background: #2d1b1b; padding: 12px; border-radius: 4px; margin-bottom: 16px; max-width: ${previewWidth}px; white-space: pre-wrap; font-size: 12px; display: none; }
  </style>
</head>
<body>
  <div id="error">${bundleError || ''}</div>
  <div id="viewport">
    <iframe id="frame" srcdoc=""></iframe>
  </div>
  <div id="controls">
    <button id="playBtn">▶ Play</button>
    <input type="range" id="scrubber" min="0" max="${durationInFrames - 1}" value="0">
    <span id="frameLabel">0 / ${durationInFrames}</span>
    <span id="timeLabel">0:00.0</span>
  </div>
  <div id="info">${width}×${height} @ ${fps}fps | ${(durationInFrames / fps).toFixed(1)}s total | Preview @ ${Math.round(scale * 100)}%</div>

  <script>
    const fps = ${fps};
    const totalFrames = ${durationInFrames};
    let currentFrame = 0;
    let playing = false;
    let animId = null;
    let lastTime = 0;

    const iframe = document.getElementById('frame');
    const scrubber = document.getElementById('scrubber');
    const frameLabel = document.getElementById('frameLabel');
    const timeLabel = document.getElementById('timeLabel');
    const playBtn = document.getElementById('playBtn');
    const errorDiv = document.getElementById('error');

    ${bundleError ? `errorDiv.style.display = 'block';` : ''}

    function getFrameHTML(frame) {
      return `<!DOCTYPE html><html><head><style>*{margin:0;padding:0;box-sizing:border-box}body{width:${width}px;height:${height}px;overflow:hidden;background:#000}#root{width:100%;height:100%;position:relative}</style></head><body><div id="root"></div><script type="module">
        window.__CINECODE_FRAME__=\${frame};window.__CINECODE_FPS__=\${fps};window.__CINECODE_WIDTH__=\${width};window.__CINECODE_HEIGHT__=\${height};window.__CINECODE_DURATION__=\${totalFrames};
        window.useCurrentFrame=()=>window.__CINECODE_FRAME__;
        window.useVideoConfig=()=>({fps:\${fps},width:\${width},height:\${height},durationInFrames:\${totalFrames}});
        import('/bundle.js').then(()=>{
          const rootEl = document.getElementById('root');
          if (typeof window.__mountCinecode === 'function') {
            window.__mountCinecode(rootEl);
          }
        }).catch(e=>{
          const el = document.getElementById('root');
          if (el) el.textContent = e.message;
        });
      </script></body></html>\`;
    }

    function updateFrame(frame) {
      currentFrame = Math.max(0, Math.min(frame, totalFrames - 1));
      scrubber.value = currentFrame;
      frameLabel.textContent = currentFrame + ' / ' + totalFrames;
      const seconds = currentFrame / fps;
      const mins = Math.floor(seconds / 60);
      const secs = (seconds % 60).toFixed(1);
      timeLabel.textContent = mins + ':' + secs.padStart(4, '0');
      iframe.srcdoc = getFrameHTML(currentFrame);
    }

    function playLoop(timestamp) {
      if (!playing) return;
      if (timestamp - lastTime >= 1000 / fps) {
        lastTime = timestamp;
        currentFrame++;
        if (currentFrame >= totalFrames) currentFrame = 0;
        updateFrame(currentFrame);
      }
      animId = requestAnimationFrame(playLoop);
    }

    playBtn.addEventListener('click', () => {
      playing = !playing;
      playBtn.textContent = playing ? '⏸ Pause' : '▶ Play';
      playBtn.classList.toggle('active', playing);
      if (playing) { lastTime = performance.now(); animId = requestAnimationFrame(playLoop); }
      else cancelAnimationFrame(animId);
    });

    scrubber.addEventListener('input', () => {
      updateFrame(parseInt(scrubber.value));
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.code === 'Space') { e.preventDefault(); playBtn.click(); }
      if (e.code === 'ArrowLeft') updateFrame(currentFrame - 1);
      if (e.code === 'ArrowRight') updateFrame(currentFrame + 1);
      if (e.code === 'Home') updateFrame(0);
      if (e.code === 'End') updateFrame(totalFrames - 1);
    });

    // WebSocket hot reload
    const ws = new WebSocket('ws://' + location.host);
    ws.onmessage = (msg) => {
      const data = JSON.parse(msg.data);
      if (data.type === 'reload') updateFrame(currentFrame);
    };

    // Initial render
    updateFrame(0);
  </script>
</body>
</html>`;
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--port' && args[i + 1]) options.port = parseInt(args[++i]);
    if (args[i] === '--entry' && args[i + 1]) options.entry = args[++i];
    if (args[i] === '--fps' && args[i + 1]) options.fps = parseInt(args[++i]);
    if (args[i] === '--duration' && args[i + 1]) options.durationInFrames = parseInt(args[++i]);
  }

  startPreview(options).catch(err => {
    console.error('❌ Preview failed:', err.message);
    process.exit(1);
  });
}

module.exports = { startPreview };
