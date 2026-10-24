---
version: alpha
name: Arc-Browser-Spatial-design-analysis
description: "Arc's spatial interface system frames web content inside an adaptive, user-tinted border frame with collapsible vertical command sidebars, pinned glass-morphic space tiles, and playful tactile micro-physics."

colors:
  canvas-frame: "#edeae2"
  surface-viewport: "#ffffff"
  surface-pill: "rgba(255, 255, 255, 0.65)"
  ink: "#1c1b18"
  ink-muted: "#6b6860"
  accent-cobalt: "#2b4eff"
  border-frame: "rgba(28, 27, 24, 0.08)"

typography:
  display-serif:
    fontFamily: "'Newsreader', Georgia, serif"
    fontSize: 48px
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: -1.0px
  ui-sans:
    fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, sans-serif"
    fontSize: 13.5px
    fontWeight: 500
    lineHeight: 1.35
    letterSpacing: -0.1px
---

# Arc Design System Analysis

## 1. Core Principles
- **Inset Framed Viewport**: The primary content viewport sits inset by `8px–10px` inside a tinted outer shell with `10px–12px` rounded corners and a subtle ambient shadow, creating a clean physical boundary between navigation chrome and workspace content.
- **Command-Bar-First Navigation**: Replaces static URL bars and multi-row toolbars with a single centered `Cmd+T / Cmd+L` floating command overlay.
