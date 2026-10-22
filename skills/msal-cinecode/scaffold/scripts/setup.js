#!/usr/bin/env node

/**
 * Maxilun CineCode — Setup & Verification Script
 * Ensures all dependencies and runtime requirements are met
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

async function setup() {
  console.log('\n╔══════════════════════════════════════╗');
  console.log('║   Maxilun CineCode Setup             ║');
  console.log('╚══════════════════════════════════════╝\n');

  const checks = [];

  // 1. Check Node.js version
  const nodeVersion = process.version;
  const nodeMajor = parseInt(nodeVersion.slice(1).split('.')[0]);
  checks.push({
    name: 'Node.js version',
    pass: nodeMajor >= 18,
    detail: `${nodeVersion} ${nodeMajor >= 18 ? '✓' : '(need ≥18)'}`,
  });

  // 2. Check npm dependencies
  console.log('[SETUP] Checking dependencies...');
  const requiredDeps = ['react', 'react-dom', 'esbuild', 'puppeteer', 'ws', 'chokidar'];
  for (const dep of requiredDeps) {
    const depPath = path.join(__dirname, '..', 'node_modules', dep);
    checks.push({
      name: `Dependency: ${dep}`,
      pass: fs.existsSync(depPath),
      detail: fs.existsSync(depPath) ? 'Installed' : 'MISSING — run: npm install',
    });
  }

  // 3. Check Puppeteer Chromium
  console.log('[SETUP] Verifying Puppeteer Chromium...');
  try {
    const puppeteer = require('puppeteer');
    const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
    await browser.close();
    checks.push({ name: 'Puppeteer Chromium', pass: true, detail: 'Browser launchable ✓' });
  } catch (err) {
    checks.push({
      name: 'Puppeteer Chromium',
      pass: false,
      detail: `FAILED: ${err.message.split('\n')[0]}\n  Fix: npx puppeteer browsers install chrome`,
    });
  }

  // 4. Check FFmpeg
  console.log('[SETUP] Checking FFmpeg...');
  let ffmpegFound = false;
  try {
    execSync('ffmpeg -version', { stdio: 'ignore' });
    ffmpegFound = true;
    checks.push({ name: 'FFmpeg (system)', pass: true, detail: 'Available ✓' });
  } catch {
    // Try @ffmpeg-installer/ffmpeg
    try {
      const ffmpegPath = require('@ffmpeg-installer/ffmpeg').path;
      if (fs.existsSync(ffmpegPath)) {
        ffmpegFound = true;
        checks.push({ name: 'FFmpeg (@ffmpeg-installer)', pass: true, detail: `${ffmpegPath} ✓` });
      }
    } catch {
      checks.push({
        name: 'FFmpeg',
        pass: false,
        detail: 'NOT FOUND\n  Fix: npm install @ffmpeg-installer/ffmpeg\n  Or: https://ffmpeg.org/download.html',
      });
    }
  }

  // 5. Check esbuild binary
  console.log('[SETUP] Verifying esbuild binary...');
  try {
    const esbuild = require('esbuild');
    await esbuild.build({
      stdin: { contents: 'console.log("test")', loader: 'js' },
      write: false,
      logLevel: 'silent',
    });
    checks.push({ name: 'esbuild binary', pass: true, detail: 'Working ✓' });
  } catch (err) {
    checks.push({
      name: 'esbuild binary',
      pass: false,
      detail: `FAILED: ${err.message.split('\n')[0]}`,
    });
  }

  // 6. Check project structure
  console.log('[SETUP] Validating project structure...');
  const requiredFiles = [
    'src/types.ts',
    'src/components/AbsoluteFill.tsx',
    'src/components/Sequence.tsx',
    'scripts/render.js',
    'scripts/encode.js',
    'scripts/cli.js',
  ];
  for (const file of requiredFiles) {
    const fullPath = path.join(__dirname, '..', file);
    checks.push({
      name: `File: ${file}`,
      pass: fs.existsSync(fullPath),
      detail: fs.existsSync(fullPath) ? 'Exists ✓' : 'MISSING',
    });
  }

  // Print results
  console.log('\n' + '='.repeat(60));
  console.log('SETUP VERIFICATION RESULTS');
  console.log('='.repeat(60) + '\n');

  let allPass = true;
  for (const check of checks) {
    const icon = check.pass ? '✅' : '❌';
    console.log(`${icon} ${check.name}`);
    if (!check.pass) {
      console.log(`   ${check.detail}`);
      allPass = false;
    }
  }

  console.log('\n' + '='.repeat(60));
  if (allPass) {
    console.log('✅ ALL CHECKS PASSED — CineCode is ready to use!');
    console.log('\nQuick start:');
    console.log('  node scripts/cli.js preview    # Start live preview');
    console.log('  node scripts/cli.js render     # Render frames');
    console.log('  node scripts/cli.js validate   # Validate project');
  } else {
    console.log('❌ SOME CHECKS FAILED — Fix issues above before using CineCode');
  }
  console.log('='.repeat(60) + '\n');

  return allPass;
}

// Run if called directly
if (require.main === module) {
  setup()
    .then(pass => process.exit(pass ? 0 : 1))
    .catch(err => {
      console.error('Setup error:', err);
      process.exit(1);
    });
}

module.exports = { setup };
