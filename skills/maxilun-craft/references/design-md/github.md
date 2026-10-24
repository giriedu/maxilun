---
version: alpha
name: GitHub-Primer-design-analysis
description: "GitHub's Primer design system balances dense developer workflows (pull diffs, commit graphs, actions logs, issue trackers) with high-contrast semantic clarity. Built on crisp 1px structural borders (#d0d7de light / #30363d dark), functional status pills, monospace SHA/code tokens, and a strict 4px/8px spatial grid that prioritizes scannability over ornament."

colors:
  canvas: "#ffffff"
  surface-subtle: "#f6f8fa"
  surface-inset: "#eff2f5"
  canvas-dark: "#0d1117"
  surface-dark: "#161b22"
  surface-dark-elevated: "#21262d"
  border-default: "#d0d7de"
  border-muted: "#d8dee4"
  border-dark: "#30363d"
  ink: "#1f2328"
  ink-muted: "#656d76"
  ink-dark: "#e6edf3"
  ink-dark-muted: "#7d8590"
  primary-action: "#1f883d"
  primary-action-hover: "#1a7f37"
  accent-blue: "#0969da"
  accent-blue-dark: "#2f81f7"
  status-open: "#1a7f37"
  status-merged: "#8250df"
  status-closed: "#cf222e"
  status-draft: "#6e7781"

typography:
  display-lg:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: -0.96px
  heading-lg:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: -0.24px
  heading-md:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
    fontSize: 20px
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: 0
  body-md:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0
  code-sm:
    fontFamily: "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.45
    letterSpacing: 0

rounded:
  sm: 6px
  md: 8px
  lg: 12px
  pill: 9999px

spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
---

# GitHub (Primer) Design System Analysis

## 1. Core Principles
- **14px Workhorse Body Type**: Unlike marketing pages that default to 16px–18px, dense engineering interfaces (file trees, PR reviews, CI logs) use `14px` (`line-height: 1.5`) as the primary UI body scale to maximize horizontal and vertical information density.
- **6px Functional Radius**: Inputs, buttons, code blocks, and boxed tables standardize on `6px` (`--radius-sm`) with a crisp `1px solid` border (`#d0d7de` light / `#30363d` dark) and subtle inset shadows.
- **Semantic State Vocabulary**: Every lifecycle state has an unambiguous color + icon pair: Open/Passing (`#1a7f37` green), Merged/Done (`#8250df` purple), Closed/Failed (`#cf222e` red), Pending/Warning (`#9a6700` amber), and Draft (`#6e7781` neutral).

## 2. Key Component Patterns
- **Split Boxed Tables**: A `surface-subtle` header bar (`#f6f8fa`) with counts/filters sits directly attached to `1px` bordered row items below (`border-top: 1px solid` per row), avoiding separate floating cards for list items.
- **Inline Monospace Chips**: Commit hashes, branch names, and file paths render in `12px` monospace inside a `rgba(175,184,193,0.2)` background pill (`padding: 2px 6px`, `border-radius: 6px`).
- **Context Switcher over Trail Clutter**: Navigation uses a single compact repository/branch dropdown popover (`Cmd+K` compatible) rather than multi-line decorative trails.
