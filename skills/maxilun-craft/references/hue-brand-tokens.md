# Hue Brand-to-Token Ingestion Model & OKLCH Architecture

Adapted from Dominik Martin's Hue framework (`hueapp.io`, MIT License). Automates the translation of brand identity into a complete, mathematically balanced design system (`design-model.yaml` or `docs/DESIGN.md`) using perceptual OKLCH color spaces.

---

## 1. The Hue Ingestion Pipeline

When starting a project or inheriting an existing brand:
1. **Extract Origin**: Read brand URL, logo SVG colors, brand guidelines, or primary hex.
2. **Convert to OKLCH**: Map colors to Lightness ($L \in [0, 1]$), Chroma ($C \in [0, 0.4]$), and Hue ($H \in [0, 360]$).
3. **Generate 12-Step Semantic Scale**: Produce light and dark mode surfaces with perceptual luminance parity.
4. **Export Token Contract**: Write `design-model.yaml` or inject directly into `:root` / Tailwind `@theme`.

---

## 2. Structured `design-model.yaml` Schema

```yaml
version: "1.0.0"
brand:
  name: "Acme Analytics"
  archetype: "Technical Ledger"
  voice: ["authoritative", "precise", "restrained", "non-speculative"]

typography:
  display: "Geist, sans-serif"
  body: "Geist, sans-serif"
  mono: "JetBrains Mono, monospace"
  scale_ratio: 1.25 # Major Third
  base_size_px: 16

colors:
  neutral_hue: 260 # Cool slate tint
  accent_hue: 150  # Phosphor Emerald

  tokens:
    # Light Mode
    light:
      bg_canvas: "oklch(0.985 0.005 260)"
      surface_base: "oklch(1.00 0.000 0)"
      surface_raised: "oklch(0.96 0.008 260)"
      surface_sunken: "oklch(0.94 0.010 260)"
      border_subtle: "oklch(0.90 0.010 260)"
      border_strong: "oklch(0.75 0.015 260)"
      text_primary: "oklch(0.18 0.020 260)"
      text_secondary: "oklch(0.45 0.020 260)"
      text_muted: "oklch(0.62 0.015 260)"
      accent: "oklch(0.65 0.18 150)"
      accent_fg: "oklch(0.99 0.00 0)"

    # Dark Mode
    dark:
      bg_canvas: "oklch(0.12 0.010 260)"
      surface_base: "oklch(0.16 0.012 260)"
      surface_raised: "oklch(0.20 0.015 260)"
      surface_sunken: "oklch(0.09 0.008 260)"
      border_subtle: "oklch(0.24 0.015 260)"
      border_strong: "oklch(0.35 0.020 260)"
      text_primary: "oklch(0.95 0.005 260)"
      text_secondary: "oklch(0.72 0.010 260)"
      text_muted: "oklch(0.50 0.012 260)"
      accent: "oklch(0.75 0.18 150)"
      accent_fg: "oklch(0.10 0.02 150)"

geometry:
  radius_base_px: 4
  concentric_padding_px: 12
  # Outer radius = 4 + 12 = 16px

rhythm:
  base_unit_px: 4
```

---

## 3. Light & Dark Mode Semantic Parity

Never hardcode arbitrary dark colors like `#1a1a1a` or `bg-slate-900`. 
Always use semantic tokens matching their functional role:

| Semantic Token | Light Mode Usage | Dark Mode Usage |
|---|---|---|
| `--bg-canvas` | Page body background (Lightest) | Page body background (Deepest dark) |
| `--surface-base` | Primary content card surface | Primary content card surface |
| `--surface-raised` | Popover, modal, dropdown elevation | Popover, modal, dropdown elevation |
| `--border-subtle` | Hairline dividers, card outlines | Hairline dividers, card outlines |
| `--text-primary` | High-contrast headings and body | High-contrast headings and body |
| `--text-secondary` | Descriptive labels, metadata | Descriptive labels, metadata |
| `--accent` | Spotlight button, active tab | Spotlight button, active tab |
