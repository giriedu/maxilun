# Design Archetypes Matrix & Nuclear Redesign Protocol

A model that is not given an explicit archetype falls back to the internet average:
dark slate-900 or zinc-900, blue/purple accents, centered cards, and floating pills.
This playbook defines 6 contrasting, production visual identities with copy-pasteable
OKLCH tokens, typography pairings, surface elevations, and structural layouts.

Every UI build or redesign task MUST explicitly declare ONE archetype before writing code:
`[ARCHETYPE SELECTED: <Archetype Name>]`

---

## 1. The 6 Contrasting Visual Archetypes

### Archetype 1: Technical Ledger / High-Density Data
*Best for*: Developer dashboards, trading terminals, administrative ledgers, operations tools.
*Anti-Average*: Zero rounded pills, zero floating cards, strict tabular alignment, hairline borders.

```css
:root {
  /* Surface: Deep Ink Charcoal / Dark Carbon */
  --bg: oklch(0.12 0.01 260);
  --surface: oklch(0.16 0.012 260);
  --sunken: oklch(0.09 0.008 260);
  --line: oklch(0.24 0.015 260);

  /* Typography: Technical Mono & Dense Grotesque */
  --font-ui: "Geist", system-ui, -apple-system, sans-serif;
  --font-mono: "Commit Mono", "JetBrains Mono", monospace;
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

```css
:root {
  /* Surface: Warm Unbleached Fibrous Paper */
  --bg: oklch(0.975 0.012 85);
  --surface: oklch(1.000 0.000 0);
  --sunken: oklch(0.940 0.015 85);
  --line: oklch(0.880 0.020 85);

  /* Typography: High-Contrast Serif Headings + Calm Sans Body */
  --font-ui: "Plus Jakarta Sans", system-ui, sans-serif;
  --font-display: "Newsreader", "Fraunces", Georgia, serif;
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

```css
:root {
  /* Surface: Stark Binary Contrast */
  --bg: oklch(0.99 0.000 0);
  --surface: oklch(0.96 0.000 0);
  --sunken: oklch(0.92 0.000 0);
  --line: oklch(0.15 0.000 0);

  /* Typography: Heavy Swiss Grotesque (-0.04em tracking) */
  --font-ui: "Space Grotesk", "Geist", system-ui, sans-serif;
  --font-display: var(--font-ui);
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

```css
:root {
  /* Surface: Crisp Paper Chalk */
  --bg: oklch(0.99 0.000 0);
  --surface: oklch(1.00 0.000 0);
  --sunken: oklch(0.95 0.010 90);
  --line: oklch(0.00 0.000 0);

  /* Typography: Punchy Bold Display + Clean Sans */
  --font-ui: "Space Grotesk", "Plus Jakarta Sans", sans-serif;
  --font-display: var(--font-ui);
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

```css
:root {
  /* Surface: Muted Stone & Natural Linen */
  --bg: oklch(0.960 0.008 120);
  --surface: oklch(0.985 0.005 120);
  --sunken: oklch(0.925 0.010 120);
  --line: oklch(0.870 0.012 120);

  /* Typography: Humanist Sans */
  --font-ui: "Figtree", "Plus Jakarta Sans", system-ui, sans-serif;
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
   - Inject the chosen archetype's `:root` CSS custom properties or Tailwind theme variables.

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
