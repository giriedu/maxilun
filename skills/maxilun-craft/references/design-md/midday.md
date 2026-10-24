---
version: alpha
name: Midday-Financial-OS-design-analysis
description: "Midday's financial operating system for founders pairs ultra-minimalist monochrome architectural grids (#0c0c0c dark / #fbfbfa light), dotted matrix charts, monospace invoice ledgers, and AI-assisted receipt vault matching."

colors:
  canvas-dark: "#0c0c0c"
  surface-dark: "#121212"
  border-dark: "#222222"
  canvas-light: "#fbfbfa"
  surface-light: "#ffffff"
  border-light: "#e6e6e4"
  ink-dark: "#f5f5f3"
  ink-muted: "#737373"
  status-matched: "#22c55e"

typography:
  ledger-mono:
    fontFamily: "'Geist Mono', 'JetBrains Mono', ui-monospace, monospace"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.45
    letterSpacing: 0
  heading-sans:
    fontFamily: "'Geist', 'Inter', system-ui, sans-serif"
    fontSize: 24px
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: -0.5px
---

# Midday Design System Analysis

## 1. Core Principles
- **Monospace Financial Clarity**: Runway months, burn rate, VAT totals, and transaction rows are set in crisp monospace (`Geist Mono` / `tabular-nums`) inside exposed `1px` grid cells with zero rounded-card fluff (`0px–4px` sharp corners).
- **Direct Command & Filter Bar**: A single unified search/filter bar at the top of the transaction ledger replaces multi-level navigation trails and breadcrumbs.
