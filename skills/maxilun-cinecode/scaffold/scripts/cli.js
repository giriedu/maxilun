#!/usr/bin/env node

/**
 * Maxilun CineCode — Unified CLI
 * Single entry point for all cinecode commands
 */

const { render } = require('./render');
const { encode } = require('./encode');
const { startPreview } = require('./preview');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

const COMMANDS = {
  render: {
    description: 'Render video to PNG frame sequence',
    usage: 'cinecode render [--entry <file>] [--duration <frames>] [--fps <n>] [--output <dir>]',
  },
  encode: {
    description: 'Encode frame sequence to video (MP4/WebM/GIF)',
    usage: 'cinecode encode --frames <dir> [--output <file>] [--preset mp4-h264|webm-vp9|gif]',
  },
  preview: {
    description: 'Start live preview server with hot reload',
    usage: 'cinecode preview [--port <n>] [--entry <file>]',
  },
  validate: {
    description: 'Validate project structure and assets',
    usage: 'cinecode validate',
  },
  list: {
    description: 'List all compositions in project',
    usage: 'cinecode list',
  },
  still: {
    description: 'Export single frame as image',
    usage: 'cinecode still --frame <n> [--output <file>]',
  },
};

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help' || command === '-h') {
    printHelp();
    return;
  }

  if (!COMMANDS[command]) {
    console.error(`Unknown command: ${command}`);
    console.error(`Available: ${Object.keys(COMMANDS).join(', ')}`);
    process.exit(1);
  }

  const cmdArgs = parseArgs(args.slice(1));

  switch (command) {
    case 'render':
      await cmdRender(cmdArgs);
      break;
    case 'encode':
      await cmdEncode(cmdArgs);
      break;
    case 'preview':
      await cmdPreview(cmdArgs);
      break;
    case 'validate':
      await cmdValidate();
      break;
    case 'list':
      await cmdList();
      break;
    case 'still':
      await cmdStill(cmdArgs);
      break;
  }
}

async function cmdRender(args) {
  const result = await render({
    entry: args.entry,
    durationInFrames: args.duration ? parseInt(args.duration) : undefined,
    fps: args.fps ? parseInt(args.fps) : undefined,
    width: args.width ? parseInt(args.width) : undefined,
    height: args.height ? parseInt(args.height) : undefined,
    outputDir: args.output,
  });

  // Auto-encode if format specified
  if (args.format && args.format !== 'png-sequence') {
    console.log('\n[AUTO] Encoding frames to', args.format, '...');
    await encode({
      framesDir: result.framesDir,
      fps: result.config.fps,
      preset: args.format === 'mp4' ? 'mp4-h264' : args.format === 'webm' ? 'webm-vp9' : args.format,
      output: args.output ? path.join(path.dirname(args.output), `output.${args.format}`) : undefined,
    });
  }
}

async function cmdEncode(args) {
  if (!args.frames) {
    console.error('--frames <dir> is required');
    process.exit(1);
  }
  await encode({
    framesDir: args.frames,
    output: args.output,
    fps: args.fps ? parseInt(args.fps) : 30,
    preset: args.preset || 'mp4-h264',
    audioSrc: args.audio,
  });
}

async function cmdPreview(args) {
  await startPreview({
    port: args.port ? parseInt(args.port) : undefined,
    entry: args.entry,
    fps: args.fps ? parseInt(args.fps) : undefined,
    durationInFrames: args.duration ? parseInt(args.duration) : undefined,
  });
}

async function cmdValidate() {
  console.log('\n🔍 Validating CineCode project...\n');

  const checks = [];

  // Check entry point
  const entryCandidates = ['./src/compositions/MyVideo.tsx', './src/index.tsx', './src/App.tsx'];
  const entry = entryCandidates.find(c => fs.existsSync(c));
  checks.push({ name: 'Entry point', pass: !!entry, detail: entry || 'Not found' });

  // Check package.json
  const hasPkg = fs.existsSync('./package.json');
  checks.push({ name: 'package.json', pass: hasPkg, detail: hasPkg ? 'Found' : 'Missing' });

  // Check tsconfig
  const hasTs = fs.existsSync('./tsconfig.json');
  checks.push({ name: 'tsconfig.json', pass: hasTs, detail: hasTs ? 'Found' : 'Missing' });

  // Check types
  const hasTypes = fs.existsSync('./src/types.ts');
  checks.push({ name: 'Type definitions', pass: hasTypes, detail: hasTypes ? 'Found' : 'Missing' });

  // Check components dir
  const hasComponents = fs.existsSync('./src/components');
  checks.push({ name: 'Components directory', pass: hasComponents, detail: hasComponents ? 'Found' : 'Missing' });

  // Check dependencies
  if (hasPkg) {
    const pkg = JSON.parse(fs.readFileSync('./package.json', 'utf-8'));
    const deps = Object.keys(pkg.dependencies || {});
    const required = ['react', 'react-dom', 'esbuild', 'puppeteer'];
    const missing = required.filter(d => !deps.includes(d));
    checks.push({
      name: 'Required dependencies',
      pass: missing.length === 0,
      detail: missing.length === 0 ? 'All present' : `Missing: ${missing.join(', ')}`,
    });
  }

  // Print results
  let allPass = true;
  for (const check of checks) {
    const icon = check.pass ? '✅' : '❌';
    console.log(`${icon} ${check.name}: ${check.detail}`);
    if (!check.pass) allPass = false;
  }

  console.log(allPass ? '\n✅ Project validation passed!\n' : '\n❌ Validation failed. Fix issues above.\n');
  process.exit(allPass ? 0 : 1);
}

async function cmdList() {
  console.log('\n📋 Compositions in project:\n');

  const compDir = './src/compositions';
  if (!fs.existsSync(compDir)) {
    console.log('  No compositions directory found.');
    return;
  }

  const files = fs.readdirSync(compDir).filter(f => f.endsWith('.tsx') || f.endsWith('.ts'));
  if (files.length === 0) {
    console.log('  No composition files found.');
    return;
  }

  for (const file of files) {
    const content = fs.readFileSync(path.join(compDir, file), 'utf-8');
    // Extract exported component names
    const exports = content.match(/export\s+(?:const|function)\s+(\w+)/g) || [];
    const names = exports.map(e => e.replace(/export\s+(?:const|function)\s+/, ''));
    console.log(`  📄 ${file}`);
    names.forEach(n => console.log(`     └─ ${n}`));
  }
  console.log('');
}

async function cmdStill(args) {
  if (!args.frame) {
    console.error('--frame <n> is required');
    process.exit(1);
  }

  const frameNum = parseInt(args.frame);
  const output = args.output || `still-frame-${frameNum}.png`;

  console.log(`\n📸 Capturing frame ${frameNum}...\n`);

  // Render single frame
  const { bundleProject, generateHTML } = require('./render');
  const puppeteer = require('puppeteer');

  const entry = args.entry || findEntry();
  const bundlePath = await bundleProject(entry);

  const htmlPath = path.resolve('.cinecode/render.html');
  fs.mkdirSync(path.dirname(htmlPath), { recursive: true });
  const html = generateHTML(bundlePath, {
    width: 1920,
    height: 1080,
    fps: 30,
    durationInFrames: 300,
  });
  fs.writeFileSync(htmlPath, html);

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

  let browser;
  for (const execPath of executablePaths) {
    try {
      browser = await puppeteer.launch({
        headless: 'new',
        executablePath: execPath,
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
      });
      break;
    } catch {}
  }

  if (!browser) {
    throw new Error('No Chrome/Chromium/Edge found for still frame capture.');
  }

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });

  const fileUrl = pathToFileURL(htmlPath).href;
  await page.goto(fileUrl, { waitUntil: 'networkidle0' });
  await page.evaluate((f) => { window.__CINECODE_FRAME__ = f; }, frameNum);
  await new Promise(r => setTimeout(r, 100));

  await page.screenshot({ path: output, type: 'png' });
  await browser.close();

  console.log(`✅ Saved: ${output}\n`);
}

function findEntry() {
  const candidates = ['./src/compositions/MyVideo.tsx', './src/index.tsx', './src/App.tsx'];
  return candidates.find(c => fs.existsSync(c));
}

function parseArgs(args) {
  const result = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--') && args[i + 1]) {
      result[args[i].slice(2)] = args[++i];
    }
  }
  return result;
}

function printHelp() {
  console.log('\n╔══════════════════════════════════════╗');
  console.log('║   Maxilun CineCode CLI               ║');
  console.log('╚══════════════════════════════════════╝\n');
  console.log('Usage: cinecode <command> [options]\n');
  console.log('Commands:');
  for (const [name, info] of Object.entries(COMMANDS)) {
    console.log(`  ${name.padEnd(12)} ${info.description}`);
    console.log(`  ${''.padEnd(12)} ${info.usage}`);
    console.log('');
  }
}

main().catch(err => {
  console.error('\n❌ Error:', err.message);
  process.exit(1);
});
