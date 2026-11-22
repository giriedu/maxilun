# Hero Section Archetypes: First-Fold Conversion & Art Direction

> **Status**: Reference Document  
> **Specialist**: `maxilun-craft` & `maxilun-content`  
> **Source Attribution**: Synthesized from First Fold architectures (see `CREDITS.md`)

The First Fold (the viewport area visible without scrolling) dictates over 80% of landing page engagement and conversion. Generic hero layouts (centered headline, gray subtext, two generic buttons) fail the 3-second comprehension test. This guide establishes industry-specific hero architectures and high-conversion structural rules.

---

## 1. The 5-Element Hero Anatomy

Every high-performing hero section must compose these five structural layers:

```
[1. Announcement Badge / Context Eyebrow]
[2. Hook Headline (Max 8-10 Words, -0.04em Tracking)]
[3. Concrete Subheadline (Outcome-Driven, 2 Sentences Max)]
[4. Action Cluster: Primary Spotlight CTA + Secondary Link + Micro-Guarantee]
[5. Interactive Centerpiece (Living Workbench / 3D Tilt Preview)]
────────────────────────────────────────────────────────────────
[Trust Bar: Monochrome Logo Strip / Verified Metric Ticker]
```

### The Three-Second Conversion Rules
1. **Pass the "So What?" Test**: Within 3 seconds, a first-time visitor must immediately understand what the product does, for whom, and what friction it removes.
2. **Zero Jargon**: Ban empty buzzwords ("revolutionary", "seamless", "synergy", "supercharge"). State literal capabilities in plain user language.
3. **One Focal Spotlight**: Exactly one visual anchor must claim attention first. The eye must flow naturally: Headline $\rightarrow$ Interactive Centerpiece $\rightarrow$ Primary CTA.

---

## 2. Industry-Specific Hero Archetypes

### A. AI & Autonomous Developer Tools
- **Visual Motif**: Dark atmospheric deep space, interactive prompt-to-result simulation, real terminal window with syntax highlighting.
- **Centerpiece**: An interactive sandbox where visitors can type or click presets to see immediate simulated output.
- **Typographic Pair**: `Syne` or `Clash Display` headline paired with `Geist Mono` terminal code.

### B. High-Velocity SaaS & B2B Platforms
- **Visual Motif**: Asymmetric 2-column split (60% content / 40% interactive dashboard preview).
- **Centerpiece**: A live interactive preview card featuring a draggable timeline, interactive filter chip, or live status metric.
- **Trust Elements**: Verified customer metrics with right-aligned `tabular-nums` (e.g. "99.99% uptime · 4.2M daily events").

### C. E-Commerce & Tangible Hardware
- **Visual Motif**: High-definition spatial photography, subtle perspective tilt on hover, material switcher.
- **Centerpiece**: A floating 3D perspective product canvas with interactive color swatches that smoothly crossfade textures.
- **Action Cluster**: Prominent "Order Now" button with instantaneous stock availability indicator dot (green pulse).

### D. FinTech, Crypto & High-Throughput Trading
- **Visual Motif**: Technical ledger aesthetic, hairline borders (`1px solid var(--border)`), high-density data matrices.
- **Centerpiece**: Live interactive SVG sparkline chart with crosshair scrubbing and instant currency conversion.
- **Trust Elements**: Regulatory compliance badges and SOC2 / ISO verification shields.

### E. CyberSecurity & Cloud Operations
- **Visual Motif**: Matrix radar canvas, live network heartbeat, zero-trust telemetry indicators.
- **Centerpiece**: An interactive vulnerability/health scanner visualizer showing real-time ping waves.

---

## 3. High-Converting Hero Code Blueprint (Next.js & Tailwind)

```tsx
"use client";

import * as React from "react";
import { ArrowRight, ShieldCheck } from "lucide-react";

export function SaaSWorkbenchHero() {
  return (
    <section className="relative overflow-hidden pt-24 pb-20 md:pt-32 md:pb-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
          {/* Left Column: Value Proposition */}
          <div className="lg:col-span-6 flex flex-col items-start text-left">
            {/* Announcement Badge */}
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-neutral-800 bg-neutral-900/60 text-xs font-mono text-neutral-400 mb-6">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              v2.4 Released with Real-time Sync
            </div>

            {/* Headline */}
            <h1 className="text-4xl sm:text-6xl font-bold tracking-tight text-neutral-100 text-balance mb-6">
              Continuous infrastructure audits without the noise.
            </h1>

            {/* Subheadline */}
            <p className="text-base sm:text-lg text-neutral-400 max-w-xl text-pretty mb-8">
              Automatically track caller blast radius, detect runtime memory leaks, and prove zero regressions before every production deployment.
            </p>

            {/* Action Cluster */}
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full sm:w-auto mb-6">
              <button className="px-6 py-3 rounded-xl bg-neutral-100 text-neutral-950 font-semibold text-sm hover:bg-white transition-all shadow-md hover:shadow-neutral-200/20 active:scale-[0.98]">
                Start Free 14-Day Trial
              </button>
              <button className="inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl border border-neutral-800 bg-neutral-900/50 text-neutral-300 font-medium text-sm hover:bg-neutral-800/80 transition-all">
                Live Interactive Sandbox <ArrowRight className="w-4 h-4" />
              </button>
            </div>

            {/* Micro-Social Proof */}
            <div className="flex items-center gap-2 text-xs text-neutral-500 font-mono">
              <ShieldCheck className="w-4 h-4 text-emerald-500/80" />
              <span>SOC2 Type II Certified · Zero setup friction</span>
            </div>
          </div>

          {/* Right Column: Interactive Centerpiece Preview */}
          <div className="lg:col-span-6 relative">
            <div className="relative rounded-2xl border border-neutral-800 bg-neutral-900/80 p-4 shadow-2xl backdrop-blur-xl">
              <div className="flex items-center justify-between pb-3 border-b border-neutral-800/60 mb-4">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-neutral-700" />
                  <span className="w-3 h-3 rounded-full bg-neutral-700" />
                  <span className="w-3 h-3 rounded-full bg-neutral-700" />
                </div>
                <span className="text-xs font-mono text-neutral-500">live-telemetry.ts</span>
              </div>
              <div className="h-64 sm:h-80 rounded-lg bg-neutral-950/60 border border-neutral-800/40 p-4 font-mono text-xs text-neutral-300 overflow-hidden flex flex-col justify-between">
                <div className="space-y-2">
                  <div className="text-emerald-400">✓ Graph AST parsed: 2,410 symbols</div>
                  <div className="text-neutral-400">→ Traced caller radius: 0 cycles detected</div>
                  <div className="text-neutral-500">→ Latency: 12ms | Memory: 42MB | Thread Pool: 4/4</div>
                </div>
                <div className="pt-4 border-t border-neutral-900 flex justify-between text-neutral-500">
                  <span>Status: Operational</span>
                  <span className="text-emerald-400">Coverage: 98.4%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
```

