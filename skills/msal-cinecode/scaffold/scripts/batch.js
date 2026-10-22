#!/usr/bin/env node

/**
 * Maxilun CineCode — Batch Renderer
 * Phase 6: Data-driven multi-variant video generation
 */

const { render } = require('./render');
const { encode } = require('./encode');
const fs = require('fs');
const path = require('path');

async function batch(options) {
  const {
    template,
    dataFile,
    outputDir = './out/batch',
    format = 'mp4-h264',
    fps = 30,
    concurrency = 2,
  } = options;

  // Load data
  let variants = [];
  if (dataFile.endsWith('.json')) {
    variants = JSON.parse(fs.readFileSync(dataFile, 'utf-8'));
  } else if (dataFile.endsWith('.csv')) {
    variants = parseCSV(fs.readFileSync(dataFile, 'utf-8'));
  } else {
    throw new Error(`Unsupported data format: ${dataFile}. Use .json or .csv`);
  }

  if (!Array.isArray(variants)) {
    variants = [variants];
  }

  console.log('\n╔══════════════════════════════════════╗');
  console.log('║   Maxilun CineCode Batch Renderer    ║');
  console.log('╚══════════════════════════════════════╝\n');
  console.log(`[BATCH] Template: ${template}`);
  console.log(`[BATCH] Variants: ${variants.length}`);
  console.log(`[BATCH] Format: ${format}`);
  console.log(`[BATCH] Concurrency: ${concurrency}`);
  console.log(`[BATCH] Output: ${outputDir}\n`);

  fs.mkdirSync(outputDir, { recursive: true });

  const results = [];
  const startTime = Date.now();

  // Process in batches for concurrency control
  for (let i = 0; i < variants.length; i += concurrency) {
    const batch = variants.slice(i, i + concurrency);
    const promises = batch.map(async (variant, idx) => {
      const variantIndex = i + idx;
      const variantId = variant.id || `variant-${variantIndex}`;
      const variantOutputDir = path.join(outputDir, variantId);

      console.log(`[BATCH] Rendering variant ${variantIndex + 1}/${variants.length}: ${variantId}`);

      try {
        // Render frames
        const result = await render({
          entry: template,
          durationInFrames: variant.durationInFrames || 150,
          fps,
          outputDir: variantOutputDir,
          props: variant,
        });

        // Encode
        const outputFile = await encode({
          framesDir: result.framesDir,
          fps,
          preset: format,
          output: path.join(variantOutputDir, `${variantId}.${getExt(format)}`),
        });

        console.log(`[BATCH] ✓ ${variantId} complete`);
        return { id: variantId, status: 'success', output: outputFile };
      } catch (err) {
        console.error(`[BATCH] ✗ ${variantId} failed:`, err.message);
        return { id: variantId, status: 'error', error: err.message };
      }
    });

    const batchResults = await Promise.all(promises);
    results.push(...batchResults);
  }

  const totalTime = ((Date.now() - startTime) / 1000).toFixed(1);
  const successCount = results.filter(r => r.status === 'success').length;
  const failCount = results.filter(r => r.status === 'error').length;

  console.log(`\n${'='.repeat(50)}`);
  console.log(`✅ Batch complete: ${successCount}/${variants.length} succeeded, ${failCount} failed`);
  console.log(`   Total time: ${totalTime}s`);
  console.log(`   Output: ${outputDir}`);

  if (failCount > 0) {
    console.log('\n❌ Failed variants:');
    results.filter(r => r.status === 'error').forEach(r => {
      console.log(`   - ${r.id}: ${r.error}`);
    });
  }

  // Write manifest
  const manifest = {
    generatedAt: new Date().toISOString(),
    template,
    totalVariants: variants.length,
    successCount,
    failCount,
    totalTime,
    results,
  };
  fs.writeFileSync(path.join(outputDir, 'manifest.json'), JSON.stringify(manifest, null, 2));

  return manifest;
}

function parseCSV(content) {
  const lines = content.trim().split('\n');
  const headers = lines[0].split(',').map(h => h.trim());
  return lines.slice(1).map(line => {
    const values = line.split(',').map(v => v.trim());
    const obj = {};
    headers.forEach((h, i) => { obj[h] = values[i]; });
    return obj;
  });
}

function getExt(preset) {
  if (preset.startsWith('mp4')) return 'mp4';
  if (preset.startsWith('webm')) return 'webm';
  if (preset === 'gif') return 'gif';
  return 'mp4';
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--template' && args[i + 1]) options.template = args[++i];
    if (args[i] === '--data' && args[i + 1]) options.dataFile = args[++i];
    if (args[i] === '--output' && args[i + 1]) options.outputDir = args[++i];
    if (args[i] === '--format' && args[i + 1]) options.format = args[++i];
    if (args[i] === '--fps' && args[i + 1]) options.fps = parseInt(args[++i]);
    if (args[i] === '--concurrency' && args[i + 1]) options.concurrency = parseInt(args[++i]);
  }

  if (!options.template || !options.dataFile) {
    console.error('Usage: cinecode batch --template <file> --data <json|csv> [--output <dir>] [--format mp4-h264]');
    process.exit(1);
  }

  batch(options)
    .then(() => process.exit(0))
    .catch(err => {
      console.error('\n❌ Batch failed:', err.message);
      process.exit(1);
    });
}

module.exports = { batch };
