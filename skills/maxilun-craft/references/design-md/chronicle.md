---
version: alpha
name: Chronicle-Interactive-Storytelling-design-analysis
description: "Chronicle's interactive presentation and storytelling format uses pitch-black theatrical staging (#070708), high-contrast display typography, bento-grid interactive widget blocks, and keyboard-first focus dimming."

colors:
  canvas: "#070708"
  surface-bento: "#121214"
  surface-active: "#1a1a1e"
  border-subtle: "#242429"
  primary-accent: "#a855f7"
  ink: "#ffffff"
  ink-dimmed: "#52525b"

typography:
  display-hero:
    fontFamily: "'Labil Grotesk', 'Inter', system-ui, sans-serif"
    fontSize: 64px
    fontWeight: 600
    lineHeight: 1.04
    letterSpacing: -2.0px
  bento-body:
    fontFamily: "'Inter', system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: -0.1px
---

# Chronicle Design System Analysis

## 1. Core Principles
- **Spotlight Focus Dimming**: When one card or metric block on the canvas is focused/hovered, sibling blocks smoothly dim to `opacity: 0.35`, directing 100% of viewer attention without popups or clutter.
- **Tactile Bento Blocks**: Content is organized into tight `16px`-gap asymmetric bento grids where every block is an interactive widget (live chart, expandable quote, or status timeline).
