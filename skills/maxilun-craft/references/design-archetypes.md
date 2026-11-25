# Design Archetypes Matrix & Nuclear Redesign Protocol

A model that is not given an explicit archetype falls back to the internet average:
dark slate-900 or zinc-900, blue/purple accents, centered cards, and floating pills.
This playbook defines 6 contrasting, production visual identities with copy-pasteable
OKLCH tokens, typography pairings, surface elevations, and structural layouts.

Every UI build or redesign task MUST explicitly declare ONE archetype before writing code:
`[ARCHETYPE SELECTED: <Archetype Name>]`

**Font delivery rule.** The `<link>` snippets below name the font pairing; they are not the delivery method. Use the project's existing loader first (`next/font`, `@fontsource/*`, self-hosted `woff2` with `font-display: swap`). New projects self-host the files. A third-party font CDN link is acceptable only for a throwaway prototype or a single-file preview the user asked for, because it adds a network dependency and sends every visitor's IP to the font host.

---

## 1. The 6 Contrasting Visual Archetypes

### Archetype 1: Technical Ledger / High-Density Data
*Best for*: Developer dashboards, trading terminals, administrative ledgers, operations tools.
*Anti-Average*: Zero rounded pills, zero floating cards, strict tabular alignment, hairline borders.

```html
<!-- Font Import: JetBrains Mono + Geist -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

```css
:root {
  /* Surface: Deep Ink Charcoal / Dark Carbon */
  --bg: oklch(0.12 0.01 260);
  --surface: oklch(0.16 0.012 260);
  --sunken: oklch(0.09 0.008 260);
  --line: oklch(0.24 0.015 260);

  /* Typography: Technical Mono & Dense Grotesque */
  --font-ui: "Geist", system-ui, -apple-system, sans-serif;
  --font-mono: "JetBrains Mono", monospace;
  --font-num: var(--font-mono);

  /* Accent: Phosphor Emerald or Signal Amber (single accent) */
  --accent: oklch(0.75 0.18 150);
  --accent-ink: oklch(0.10 0.02 150);
  --accent-soft: oklch(0.20 0.04 150);

  /* Status */
  --ok: oklch(0.75 0.18 150);
  --warn: oklch(0.80 0.16 80);
  --bad: oklch(0.65 0.22 25);

  /* Geometry: Strict Hairlines & Razor Radii */
  --r: 2px;
  --r-lg: 4px;
  --shadow: none;
}
```
*Layout Topology*: Master-detail split pane with fixed left telemetry rail, sticky tabular data table with right-aligned `tabular-nums`, and persistent status indicators.

---

### Archetype 2: Warm Editorial / Heritage Craft
*Best for*: Long-form reading, documentation portals, publishing, university/school portals, essays.
*Anti-Average*: Warm fibrous paper surface, serif display typography, asymmetrical editorial balance, zero SaaS cards.

```html
<!-- Font Import: Newsreader Serif Display + Plus Jakarta Sans Body -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
```

```css
:root {
  /* Surface: Warm Unbleached Fibrous Paper */
  --bg: oklch(0.975 0.012 85);
  --surface: oklch(1.000 0.000 0);
  --sunken: oklch(0.940 0.015 85);
  --line: oklch(0.880 0.020 85);

  /* Typography: High-Contrast Serif Headings + Calm Sans Body */
  --font-ui: "Plus Jakarta Sans", system-ui, sans-serif;
  --font-display: "Newsreader", Georgia, serif;
  --font-num: var(--font-ui);

  /* Text: Warm Lead Ink */
  --text: oklch(0.20 0.015 60);
  --text-2: oklch(0.42 0.018 60);
  --text-3: oklch(0.58 0.015 60);

  /* Accent: Antique Terracotta / Warm Copper */
  --accent: oklch(0.55 0.16 45);
  --accent-ink: oklch(0.98 0.01 45);
  --accent-soft: oklch(0.94 0.04 45);

  /* Geometry: Bookbinder Geometry & Quiet Margins */
  --r: 4px;
  --r-lg: 6px;
  --shadow: 0 1px 3px oklch(0.2 0.02 60 / 0.06);
}
```
*Layout Topology*: Off-center magazine layout, wide readable text columns (60-70ch), drop-caps, hairline rules instead of card boxes.

---

### Archetype 3: Swiss High-Contrast Minimalist
*Best for*: Modern software showcases, developer portfolio, architectural products, design tools.
*Anti-Average*: Pure 1-bit monochrome contrast, tight negative tracking, zero drop shadows, structural grid bleed.

```html
<!-- Font Import: Space Grotesk Display + Inter/System Body -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
```

```css
:root {
  /* Surface: Stark Binary Contrast */
  --bg: oklch(0.99 0.000 0);
  --surface: oklch(0.96 0.000 0);
  --sunken: oklch(0.92 0.000 0);
  --line: oklch(0.15 0.000 0);

  /* Typography: Heavy Swiss Grotesque (-0.04em tracking) */
  --font-ui: "Inter", system-ui, sans-serif;
  --font-display: "Space Grotesk", sans-serif;
  --font-num: var(--font-ui);

  /* Text: Absolute Pitch Black */
  --text: oklch(0.08 0.000 0);
  --text-2: oklch(0.35 0.000 0);
  --text-3: oklch(0.60 0.000 0);

  /* Accent: Laser Signal Red or Pure Black */
  --accent: oklch(0.58 0.24 25);
  --accent-ink: oklch(0.99 0.00 0);
  --accent-soft: oklch(0.95 0.03 25);

  /* Geometry: Zero Corner Radius & Razor Hairlines */
  --r: 0px;
  --r-lg: 0px;
  --shadow: none;
}
```
*Layout Topology*: Asymmetrical full-bleed grid lines extending to viewport edges, ultra-large typographic statements, coordinate labels in corners.

---

### Archetype 4: Cybernetic Command Deck
*Best for*: Network consoles, security operations centers, IoT control panels, CLI telemetry.
*Anti-Average*: Void black backdrop, phosphor status indicators, visible keyboard shortcuts, command strip.

```html
<!-- Font Import: JetBrains Mono + Geist -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

```css
:root {
  /* Surface: Void Deep Space Black with Metallic Plates */
  --bg: oklch(0.08 0.005 260);
  --surface: oklch(0.14 0.010 260);
  --sunken: oklch(0.05 0.003 260);
  --line: oklch(0.22 0.015 260);

  /* Typography: Monospace Headers & Compact Matrix */
  --font-ui: "Geist", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", monospace;
  --font-num: var(--font-mono);

  /* Accent: Phosphor Electric Cyan */
  --accent: oklch(0.78 0.16 210);
  --accent-ink: oklch(0.08 0.02 210);
  --accent-soft: oklch(0.20 0.05 210);

  /* Status */
  --ok: oklch(0.78 0.18 145);
  --warn: oklch(0.82 0.16 75);
  --bad: oklch(0.65 0.22 25);

  /* Geometry: Chamfered Corners & Hard Boundaries */
  --r: 3px;
  --r-lg: 6px;
  --shadow: none;
}
```
*Layout Topology*: Top diagnostic telemetry bar (`kbd` hotkeys visible), split dual-pane interactive command deck, real-time log stream.

---

### Archetype 5: Neo-Brutalist Clean Functional
*Best for*: Creator tools, education apps, interactive forms, marketing landing pages with personality.
*Anti-Average*: Thick 2px solid black boundaries, zero-blur hard drop-shadows, high-contrast block accents.

```html
<!-- Font Import: Bricolage Grotesque Display + Space Grotesk Body -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
```

```css
:root {
  /* Surface: Crisp Paper Chalk */
  --bg: oklch(0.99 0.000 0);
  --surface: oklch(1.00 0.000 0);
  --sunken: oklch(0.95 0.010 90);
  --line: oklch(0.00 0.000 0);

  /* Typography: Punchy Bold Display + Clean Sans */
  --font-ui: "Space Grotesk", system-ui, sans-serif;
  --font-display: "Bricolage Grotesque", sans-serif;
  --font-num: var(--font-ui);

  /* Text: True Pure Black */
  --text: oklch(0.00 0.000 0);
  --text-2: oklch(0.30 0.000 0);
  --text-3: oklch(0.50 0.000 0);

  /* Accent: Electric Canary Yellow or Cobalt */
  --accent: oklch(0.88 0.18 95);
  --accent-ink: oklch(0.00 0.00 0);
  --accent-soft: oklch(0.96 0.06 95);

  /* Geometry: Hard Edges with 4px Zero-Blur Shadow */
  --r: 0px;
  --r-lg: 4px;
  --shadow: 4px 4px 0px oklch(0 0 0);
}
```
*Layout Topology*: Bold asymmetric content blocks, solid 2px black grid dividing lines, prominent bordered CTAs with hard press transforms.

---

### Archetype 6: Nordic Living / Soft Tactile Organic
*Best for*: Wellness platforms, lifestyle, educational tools, collaborative workspace.
*Anti-Average*: Sage and stone muted palette, gentle organic curves, humanized spacing, tactile inner bevels.

```html
<!-- Font Import: Figtree + Plus Jakarta Sans -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet">
```

```css
:root {
  /* Surface: Muted Stone & Natural Linen */
  --bg: oklch(0.960 0.008 120);
  --surface: oklch(0.985 0.005 120);
  --sunken: oklch(0.925 0.010 120);
  --line: oklch(0.870 0.012 120);

  /* Typography: Humanist Sans */
  --font-ui: "Plus Jakarta Sans", system-ui, sans-serif;
  --font-display: "Figtree", sans-serif;
  --font-num: var(--font-ui);

  /* Text: Muted Charcoal Leaf */
  --text: oklch(0.22 0.015 120);
  --text-2: oklch(0.44 0.018 120);
  --text-3: oklch(0.60 0.012 120);

  /* Accent: Muted Moss Green or Warm Ochre */
  --accent: oklch(0.62 0.12 140);
  --accent-ink: oklch(0.99 0.00 0);
  --accent-soft: oklch(0.94 0.03 140);

  /* Geometry: Generous Organic Radii */
  --r: 12px;
  --r-lg: 20px;
  --shadow: 0 4px 16px oklch(0.2 0.01 120 / 0.06);
}
```
*Layout Topology*: Spacious fluid flow, pill-grouped secondary actions, generous whitespace rhythm, tranquil breathing space.

---

## 2. Nuclear Redesign Protocol (Mandatory Structural Dismantling)

When a prompt asks for a "redesign", "redesain", "rombak", "revamp", or "overhaul":
Applying cosmetic class replacements (e.g. changing button background color or card border)
while leaving the old layout wrapper and card grid intact is the **Patchwork Failure (`SYS-004`)**.
It is strictly banned.

### Step-by-Step Dismantling Workflow

1. **Delete the Legacy Layout Skeleton (`SYS-002`)**:
   - Locate the outer container: e.g. `<div className="container mx-auto max-w-7xl px-4 py-12">`.
   - Tear down the wrapper: do not keep the generic 3-card grid or centered hero.
   - Strip obsolete styling rules and hardcoded palette tokens (`SYS-001`).

2. **Declare the Visual Archetype**:
   - Output `[ARCHETYPE SELECTED: <Archetype>]` at the top of your handoff.
   - Inject the chosen archetype's font stylesheet and `:root` CSS custom properties.

3. **Re-architect the Spatial Topology**:
   - Replace generic centered boxes with a domain-authentic geometry:
     - Dashboard -> Asymmetric Split-Rail or Dense Tabular Ledger.
     - Landing -> Composed Asymmetric Hero with full-bleed typographic anchor.
     - Document/Tool -> Master-Detail Workspace with sticky sidebar context.

4. **Re-author Semantic Components from Scratch**:
   - Rebuild the DOM structure with semantic tags (`<header>`, `<main>`, `<aside>`, `<nav>`).
   - Group by proximity and meaning before applying any borders.
   - Enforce concentric inner radii: $R_{inner} = \max(0, R_{outer} - padding - border)$.
   - Enforce zero emojis (`CMP-003`) and zero floating hero pills (`CMP-015`).

5. **Independent Gatekeeper Verification**:
   - Run `python skills/maxilun-craft/scripts/slopscan.py <paths>`.
   - Verify exit code 0. If patchwork remnants are detected, reject and re-author.

---

## 3. High-Craft Card Architecture (Dismantling 3-Card Monotony `LAY-008`)

The most common signature of AI-generated interfaces is the **Symmetrical 3-Card Triad**:
three identical equal-width boxes (`grid-cols-1 md:grid-cols-3`), each containing a round icon in a tinted square,
a bold title, two lines of generic text, and a "Learn more ->" link.
This pattern treats unequal data equally and announces a template.

### Banned Anti-Pattern (`LAY-008` / `LAY-TEL-02`)
```html
<!-- REJECTED: Monotonous 3-card triad with identical visual weight -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
  <div class="p-6 rounded-xl border border-slate-800 bg-slate-900/50">...</div>
  <div class="p-6 rounded-xl border border-slate-800 bg-slate-900/50">...</div>
  <div class="p-6 rounded-xl border border-slate-800 bg-slate-900/50">...</div>
</div>
```

### Approved Layout Topologies

#### Topology A: Asymmetrical Bento Grid (2:1 or 1:2 Hierarchy)
Gives the primary task or key artifact the dominant visual area, with supporting controls beside it.
```html
<div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
  <!-- Anchor Card: Spans 2 columns, holds primary work artifact -->
  <div class="lg:col-span-2 p-6 rounded-[var(--r-lg)] border border-[var(--line)] bg-[var(--surface)] flex flex-col justify-between">
    <div>
      <span class="text-xs font-mono text-[var(--accent)] uppercase tracking-wider">Live Workspace</span>
      <h3 class="text-xl font-semibold tracking-tight text-[var(--text)] mt-1 text-balance">Primary Operational Stream</h3>
      <p class="text-sm text-[var(--text-2)] mt-2 max-w-prose">Full-bleed interactive view with live data telemetry.</p>
    </div>
    <div class="mt-6 border border-[var(--line)] rounded-[var(--r)] bg-[var(--sunken)] p-4 font-mono text-xs">
      <!-- Live artifact or data visualization -->
    </div>
  </div>

  <!-- Supporting Rail Card: Spans 1 column, holds secondary actions -->
  <div class="p-5 rounded-[var(--r-lg)] border border-[var(--line)] bg-[var(--surface)] flex flex-col justify-between">
    <div>
      <h4 class="text-sm font-medium text-[var(--text)]">Recent Event Log</h4>
      <div class="mt-4 space-y-3 font-mono text-xs">
        <div class="flex justify-between py-1 border-b border-[var(--line)]/50">
          <span class="text-[var(--text-2)]">auth.verify</span>
          <span class="text-[var(--ok)] tabular-nums">12ms</span>
        </div>
      </div>
    </div>
    <button class="mt-4 w-full py-2 px-3 text-xs font-medium rounded-[var(--r)] border border-[var(--line)] hover:bg-[var(--sunken)]">
      View audit trail
    </button>
  </div>
</div>
```

#### Topology B: Operational List / Tabular Ledger (Cardless High-Density)
Replaces bulky cards with clean, high-density row ledgers separated by hairlines.
```html
<div class="border border-[var(--line)] rounded-[var(--r-lg)] bg-[var(--surface)] overflow-hidden">
  <div class="px-5 py-3 border-b border-[var(--line)] bg-[var(--sunken)] flex justify-between items-center text-xs font-mono">
    <span class="text-[var(--text-2)] uppercase">Active Nodes</span>
    <span class="text-[var(--text-3)]">12 of 12 healthy</span>
  </div>
  <div class="divide-y divide-[var(--line)]/60">
    <div class="px-5 py-3 flex items-center justify-between hover:bg-[var(--sunken)] transition-colors">
      <div class="flex items-center gap-3">
        <span class="w-2 h-2 rounded-full bg-[var(--ok)]"></span>
        <span class="font-mono text-sm font-medium text-[var(--text)]">prod-us-east-01</span>
      </div>
      <div class="flex items-center gap-6 font-mono text-xs">
        <span class="text-[var(--text-2)] tabular-nums">CPU 42%</span>
        <span class="text-[var(--text-2)] tabular-nums">p95 18ms</span>
        <span class="text-[var(--text-3)]">99.98%</span>
      </div>
    </div>
  </div>
</div>
```

#### Topology C: Hierarchical Spotlight Pairing
When cards are necessary, exactly ONE card carries the Spotlight budget (accent hairline, distinct elevation), while sibling cards remain quiet and subordinate.

---

## 4. Domain-Authentic Headers vs Breadcrumb Slop (`HDR-001` / `CMP-TEL-05`)

Generic AI templates routinely stamp fake breadcrumb trails (`Dashboard / Analytics / Overview` or `Home > Products`)
or floating capsule pill badges right above titles. This creates visual clutter without providing navigation utility.

### Banned Anti-Pattern (`HDR-001` / `CMP-015`)
<!-- maxilun-example:bad -->
```html
<!-- REJECTED: Breadcrumb slop on flat top-level page -->
<div class="text-xs text-slate-400 uppercase tracking-widest mb-1">Dashboard / Analytics / Overview</div>
<h1 class="text-3xl font-bold">Overview</h1>

<!-- REJECTED: Floating bullet capsule pill badge -->
<div class="rounded-full px-3 py-1 bg-blue-500/10 text-blue-400 text-xs inline-flex mb-3">
  • REAL-TIME • TELEMETRY • V2.0
</div>
```
<!-- /maxilun-example:bad -->

### Approved Domain-Authentic Header Patterns

#### Pattern 1: Operational Status Masthead (Dashboards & Apps)
Anchors the view with entity name, live status indicator dot, active filters, and primary action verbs.
```html
<header class="py-4 px-6 border-b border-[var(--line)] bg-[var(--surface)] flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
  <div class="flex items-center gap-3">
    <h1 class="text-lg font-semibold tracking-tight text-[var(--text)] text-balance">Laporan Transaksi Harian</h1>
    <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-xs font-mono bg-[var(--ok)]/10 text-[var(--ok)]">
      <span class="w-1.5 h-1.5 rounded-full bg-[var(--ok)]"></span>
      Terkoneksi
    </span>
  </div>
  <div class="flex items-center gap-2">
    <span class="text-xs font-mono text-[var(--text-3)] mr-2 tabular-nums">Sinkronisasi: 2 mnt lalu</span>
    <button class="py-1.5 px-3 text-xs font-medium rounded-[var(--r)] border border-[var(--line)] text-[var(--text)] hover:bg-[var(--sunken)]">
      Filter
    </button>
    <button class="py-1.5 px-3 text-xs font-medium rounded-[var(--r)] bg-[var(--accent)] text-[var(--accent-ink)] hover:opacity-90">
      Ekspor CSV
    </button>
  </div>
</header>
```

#### Pattern 2: Editorial Publication Masthead (Publications, Portals, Docs)
Uses hairline metadata rules, high-contrast serif headlines, and horizontal category anchors.
```html
<header class="pt-8 pb-6 border-b border-[var(--line)]">
  <div class="flex justify-between items-baseline text-xs font-mono text-[var(--text-3)] pb-2 border-b border-[var(--line)]/40 mb-4">
    <span>Edisi 14 • 19 November 2026</span>
    <span>Warta Akademik Terpadu</span>
  </div>
  <h1 class="font-['Newsreader',serif] text-4xl sm:text-5xl font-medium tracking-tight text-[var(--text)] text-balance">
    Transformasi Pembelajaran Berbasis Bukti
  </h1>
  <p class="mt-3 text-base sm:text-lg text-[var(--text-2)] max-w-[65ch]">
    Dokumentasi komprehensif metrik keterlibatan siswa dan evaluasi formatif semester berjalan.
  </p>
</header>
```

#### Pattern 3: Clean Hero Masthead (Landing Pages & Portfolios)
Combines clean brand logo with semantic navigation and exactly ONE primary action. Zero fake breadcrumbs.

---

## 5. Multi-Agent UI Collaboration Lifecycle

To eradicate single-agent monologue and generic averaging, UI design and implementation
mandatorily flows across 3 specialized agents:

```
[maxilun-ui-designer] (Wave 1: Contracts & Tokens)
        │
        ▼ (Handoff: Archetype, Web Font <link>, :root Tokens, Bento/Ledger Topology, Masthead Pattern)
[maxilun-coder-frontend] (Wave 2: Structural Implementation)
        │
        ▼ (Handoff: Modified files, Deleted legacy wrappers, Semantic markup)
[maxilun-ui-reviewer] (Wave 3: Independent Gatekeeper)
        │
        ├─► PASS (Exit code 0, 0 errors, slopscan clean) -> Yield to user
        └─► FAIL -> Loop back exact file:line defects to Wave 2 for immediate remedy
```

### The Structured UI Handoff Packet Format
Every transition between agents MUST carry this structured packet:
```text
[UI ARCHITECTURE PACKET]
ARCHETYPE: <Technical Ledger | Warm Editorial | Swiss High-Contrast | Cybernetic Deck | Neo-Brutalist | Nordic Living>
FONTS: <font pairing, font-family rule, and delivery: project loader or self-hosted woff2 (CDN link only for a requested prototype)>
TOKENS: <:root CSS custom properties block>
CARD_TOPOLOGY: <Asymmetric Bento | Operational List Ledger | Master-Detail | Spotlight Pairing> (Strictly No 3-Card Triads LAY-008)
MASTHEAD: <Status Masthead | Editorial Masthead | Clean Hero> (Strictly No Breadcrumbs HDR-001)
INVARIANTS: Zero emojis (CMP-003), No floating pills (CMP-015), Responsive 375px (no horizontal overflow)
```
