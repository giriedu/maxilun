---
version: alpha
name: Perplexity-Answer-Engine-design-analysis
description: "Perplexity's answer-engine interface blends editorial serif headlines with warm stone-ivory reading surfaces (#fcfcf9), inline numbered source citations, compact source-domain cards, and distraction-free long-form synthesis."

colors:
  canvas: "#fcfcf9"
  surface-sidebar: "#f3f3ee"
  surface-card: "#f5f5f0"
  canvas-dark: "#191a1a"
  surface-dark: "#202222"
  border-hairline: "#e5e5de"
  border-dark: "#2d2f2f"
  primary-teal: "#20808d"
  primary-teal-dark: "#2fb8c6"
  ink: "#13343b"
  ink-body: "#212529"
  ink-muted: "#64645e"

typography:
  editorial-title:
    fontFamily: "'Instrument Serif', Georgia, serif"
    fontSize: 36px
    fontWeight: 400
    lineHeight: 1.18
    letterSpacing: -0.5px
  body-reading:
    fontFamily: "'FK Grotesk', 'Inter', system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.65
    letterSpacing: 0
  citation-pill:
    fontFamily: "ui-monospace, SFMono-Regular, monospace"
    fontSize: 11px
    fontWeight: 600
    lineHeight: 1.0
    letterSpacing: 0
---

# Perplexity Design System Analysis

## 1. Core Principles
- **Editorial Research Calm**: Warm ivory paper (`#fcfcf9`) paired with deep पेट्रोल-teal ink (`#13343b` / `#20808d`) reduces eye strain during deep reading and research sessions.
- **Inline Numbered Citation Badges**: Claims in prose are immediately followed by a compact `18x18px` rounded pill (`[1]`, `[2]`) in `#e5e5de` that highlights the corresponding source card on hover.
- ** Constrained Reading Column**: Answer prose is strictly locked to `65ch–70ch` max-width, with horizontal source-card strips and follow-up question rows anchored cleanly to the same column grid.
