#!/usr/bin/env node

/**
 * Maxilun CineCode — FFmpeg Encoder
 * Phase 2: Convert PNG frame sequence → MP4/WebM/GIF
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const ENCODE_PRESETS = {
  'mp4-h264': {
    format: 'mp4',
    codec: 'libx264',
    pixelFormat: 'yuv420p',
    preset: 'medium',
    crf: 23,
    extraArgs: ['-movflags', '+faststart'],
  },
  'mp4-h265': {
    format: 'mp4',
    codec: 'libx265',
    pixelFormat: 'yuv420p',
    preset: 'medium',
    crf: 28,
    extraArgs: ['-tag:v', 'hvc1'],
  },
  'webm-vp9': {
    format: 'webm',
    codec: 'libvpx-vp9',
    pixelFormat: 'yuv420p',
    bitrate: '2M',
    extraArgs: ['-b:v', '2M', '-minrate', '1M', '-maxrate', '4M'],
  },
  'gif': {
    format: 'gif',
    codec: null, // Uses palettegen/paletteuse filter chain
    extraArgs: [],
  },
};

function findFFmpeg() {
  // Check common locations
  const candidates = [
    'ffmpeg',
    '/usr/bin/ffmpeg',
    '/usr/local/bin/ffmpeg',
    'C:\\ffmpeg\\bin\\ffmpeg.exe',
    process.env.FFMPEG_PATH,
  ].filter(Boolean);

  for (const candidate of candidates) {
    try {
      const result = require('child_process').spawnSync(candidate, ['-version'], { encoding: 'utf-8' });
      if (result.status === 0) return candidate;
    } catch {}
  }

  // Try @ffmpeg-installer/ffmpeg
  try {
    const ffmpegPath = require('@ffmpeg-installer/ffmpeg').path;
    if (fs.existsSync(ffmpegPath)) return ffmpegPath;
  } catch {}

  return null;
}

async function encode(options) {
  const {
    framesDir,
    output,
    fps = 30,
    preset = 'mp4-h264',
    width,
    height,
    audioSrc,
  } = options;

  const ffmpegPath = findFFmpeg();
  if (!ffmpegPath) {
    throw new Error(
      'FFmpeg not found. Install via:\n' +
      '  npm install @ffmpeg-installer/ffmpeg\n' +
      '  or install system ffmpeg: https://ffmpeg.org/download.html'
    );
  }

  const presetConfig = ENCODE_PRESETS[preset];
  if (!presetConfig) {
    throw new Error(`Unknown preset: ${preset}. Available: ${Object.keys(ENCODE_PRESETS).join(', ')}`);
  }

  const outputFile = output || path.join(path.dirname(framesDir), `output.${presetConfig.format}`);
  const framePattern = path.join(framesDir, 'frame-%06d.png');

  console.log('\n[ENCODE] Starting video encoding...');
  console.log(`[ENCODE] Input: ${framesDir}`);
  console.log(`[ENCODE] Output: ${outputFile}`);
  console.log(`[ENCODE] Preset: ${preset} (${presetConfig.codec || 'palette'})`);
  console.log(`[ENCODE] FPS: ${fps}`);

  let args = [];

  // Input
  args.push('-framerate', String(fps));
  args.push('-i', framePattern);

  // Audio (optional)
  if (audioSrc && fs.existsSync(audioSrc)) {
    args.push('-i', audioSrc);
    args.push('-map', '0:v');
    args.push('-map', '1:a?');
    args.push('-shortest');
    console.log(`[ENCODE] Audio: ${audioSrc}`);
  }

  // Codec-specific args
  if (preset === 'gif') {
    // GIF requires two-pass palette generation
    const palettePath = path.join(path.dirname(outputFile), '.palette.png');

    // Pass 1: Generate palette
    console.log('[ENCODE] Pass 1/2: Generating color palette...');
    await runFFmpeg(ffmpegPath, [
      '-i', framePattern,
      '-vf', `fps=${fps},scale=${width || -1}:${height || -1}:flags=lanczos,palettegen`,
      '-y', palettePath,
    ]);

    // Pass 2: Encode with palette
    console.log('[ENCODE] Pass 2/2: Encoding GIF...');
    args = [
      '-framerate', String(fps),
      '-i', framePattern,
      '-i', palettePath,
      '-lavfi', `fps=${fps},scale=${width || -1}:${height || -1}:flags=lanczos[x];[x][1:v]paletteuse`,
      '-y', outputFile,
    ];
  } else {
    // Video codec args
    args.push('-c:v', presetConfig.codec);

    if (presetConfig.pixelFormat) {
      args.push('-pix_fmt', presetConfig.pixelFormat);
    }

    if (presetConfig.preset) {
      args.push('-preset', presetConfig.preset);
    }

    if (presetConfig.crf) {
      args.push('-crf', String(presetConfig.crf));
    }

    if (presetConfig.extraArgs) {
      args.push(...presetConfig.extraArgs);
    }

    // Scale if specified
    if (width && height) {
      args.push('-vf', `scale=${width}:${height}`);
    }

    args.push('-y', outputFile);
  }

  await runFFmpeg(ffmpegPath, args);

  // Verify output
  const stats = fs.statSync(outputFile);
  const sizeMB = (stats.size / (1024 * 1024)).toFixed(2);

  console.log(`\n✅ Encoding complete!`);
  console.log(`   Output: ${outputFile}`);
  console.log(`   Size: ${sizeMB} MB`);

  // Cleanup palette file if GIF
  if (preset === 'gif') {
    const palettePath = path.join(path.dirname(outputFile), '.palette.png');
    if (fs.existsSync(palettePath)) fs.unlinkSync(palettePath);
  }

  return outputFile;
}

function runFFmpeg(ffmpegPath, args) {
  return new Promise((resolve, reject) => {
    const proc = spawn(ffmpegPath, args, { stdio: ['ignore', 'pipe', 'pipe'] });

    let stderr = '';
    proc.stderr.on('data', (data) => {
      stderr += data.toString();
      // Parse progress from ffmpeg stderr
      const progressMatch = data.toString().match(/frame=\s*(\d+)/);
      if (progressMatch) {
        process.stdout.write(`\r[ENCODE] Processing frame ${progressMatch[1]}...`);
      }
    });

    proc.on('close', (code) => {
      process.stdout.write('\n');
      if (code !== 0) {
        reject(new Error(`FFmpeg exited with code ${code}:\n${stderr.slice(-500)}`));
      } else {
        resolve();
      }
    });

    proc.on('error', (err) => {
      reject(new Error(`Failed to start FFmpeg: ${err.message}`));
    });
  });
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--frames' && args[i + 1]) options.framesDir = args[++i];
    if (args[i] === '--output' && args[i + 1]) options.output = args[++i];
    if (args[i] === '--fps' && args[i + 1]) options.fps = parseInt(args[++i]);
    if (args[i] === '--preset' && args[i + 1]) options.preset = args[++i];
    if (args[i] === '--width' && args[i + 1]) options.width = parseInt(args[++i]);
    if (args[i] === '--height' && args[i + 1]) options.height = parseInt(args[++i]);
    if (args[i] === '--audio' && args[i + 1]) options.audioSrc = args[++i];
  }

  if (!options.framesDir) {
    console.error('Usage: node encode.js --frames <dir> [--output <file>] [--preset mp4-h264|mp4-h265|webm-vp9|gif] [--fps 30] [--audio <file>]');
    process.exit(1);
  }

  encode(options)
    .then(() => process.exit(0))
    .catch(err => {
      console.error('\n❌ Encoding failed:', err.message);
      process.exit(1);
    });
}

module.exports = { encode, findFFmpeg, ENCODE_PRESETS };
