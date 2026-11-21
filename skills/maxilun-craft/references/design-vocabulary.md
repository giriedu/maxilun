# Design Vocabulary & Granular Direction Playbook

Instead of vague instructions like "make it modern" or "make it pop", Maxilun Craft gives users and agents a deterministic, shared design vocabulary to adjust visual intensity, spatial rhythm, and typography without breaking tokens.

---

## 1. Directional Tuning Commands

Use these terms to steer an interface's aesthetic weight and visual volume:

### `/maxilun craft bolder` (Intensify Presence)
When an interface feels timid, flat, or lacks authoritative hierarchy:
* **Contrast**: Elevate primary surface contrast against background (deepen darks or brighten pure whites).
* **Typography**: Increase header scale ratio (e.g., from 1.25 Major Third to 1.333 Perfect Fourth); step up heading weights (font-semibold to font-bold).
* **Action Priority**: Enhance primary button prominence: solid saturated accent fill, 1px inset highlight, stronger shadow elevation.
* **Borders**: Darken/sharpen hairline dividers (`oklch(0.28 ...)` vs faint `oklch(0.20 ...)`).
* **Spotlight**: Expand the spatial footprint of the key metric or hero visual.

### `/maxilun craft quieter` (Reduce Visual Noise)
When an interface feels overwhelming, cluttered, or shouting:
* **Borders**: Replace high-contrast card borders with pure whitespace separation ($2\times$ gap rule).
* **Typography**: Subdue secondary and tertiary labels to muted text roles (`text-neutral-500` / `var(--text-muted)`).
* **Color Discipline**: Strip decorative accents from icons, pills, or minor badges; reserve the accent strictly for the single primary action.
* **Surface Steps**: Flatten multi-tiered cards down to a unified, quiet background plane.

### `/maxilun craft typeset` (Typographic Precision)
When text hierarchy feels generic or sloppy:
* **Sentence Case Enforcement**: Strip all Title Case from buttons, table headers, and modal headings.
* **Balanced Headlines**: Add `text-wrap: balance` to every H1, H2, and modal title to eliminate orphaned words.
* **Tabular Figures**: Add `tabular-nums` (`font-variant-numeric: tabular-nums`) to all prices, counts, timestamps, and data tables.
* **Tracking Audit**: Remove wide letter-spacing (`tracking-widest`) from standard headings; restrict tracking only to uppercase technical codes or micro-unit tags.
* **Measure**: Constrain body text width to $50\text{--}75$ characters (`max-w-prose` / `max-w-xl`).

### `/maxilun craft polish` (Tactile Micro-Interactions)
When interactions feel stiff, robotic, or unresponsive:
* **Press Scale**: Add tactile active state scale: `active:scale-[0.97]` over `120ms` ease-out.
* **Concentric Radii**: Ensure all nested children obey $R_{outer} = R_{inner} + padding + border$.
* **Focus Rings**: Replace blurry browser outlines with sharp, high-contrast 2px focus-visible rings offset by 2px (`focus-visible:ring-2 focus-visible:ring-offset-2`).
* **Hover Transitions**: Restrict hover animations to GPU-accelerated `opacity` and `transform` at `150ms\text{--}200ms`.

### `/maxilun craft harden` (Stress-Testing & Edge Cases)
When an interface looks good on a mock desktop but breaks in the real world:
* **Extreme Viewports**: Verify layout on 320px (minimum mobile reflow), 375px (standard mobile), and 1440px (wide desktop). Zero horizontal overflow allowed.
* **Text Stress**: Test UI containers with $3\times$ longer text strings; ensure flex children carry `min-w-0` and truncation is intentional.
* **Empty States**: Ensure every list, table, or chart renders a dedicated, helpful Empty State with a clear primary action.
* **Accessibility Floor**: Confirm 4.5:1 text contrast ratio and keyboard tab navigation focus paths.

### `/maxilun craft shape` (Spatial Layout Topology)
When a page defaults to a monotonous top-to-bottom card cascade:
* **Break Monotony (`LAY-008`)**: Ban the 3-column symmetrical card grid.
* **Asymmetric Bento (2:1)**: Anchor the dominant metric or preview on a large 2-span card, flanking supporting actions in a 1-span rail.
* **Tabular Ledger**: Convert scattered metric cards into a unified, high-density table ledger with aligned columns.
* **Domain Mastheads (`HDR-001`)**: Replace floating breadcrumb trails with authentic domain header bands.

### `/maxilun craft critique` (Automated Heuristics Review)
Runs the Purity Gate and usability heuristics without editing files, returning ranked findings:
* **P0 (Blocker)**: Broken responsive reflow, inaccessible contrast (< 3:1), missing core action.
* **P1 (Slop & Invariant Violations)**: AI emojis used as UI icons (`CMP-003`), generic 3-card layout (`LAY-008`), title case abuse (`TYP-TEL-02`).
* **P2 (Craft Refinements)**: Concentric radius mismatch, missing tabular numbers on currency, sluggish animation duration.
