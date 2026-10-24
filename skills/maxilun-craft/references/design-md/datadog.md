---
version: alpha
name: Datadog-Observability-design-analysis
description: "Datadog's high-density observability and APM system is engineered for extreme telemetry volume: synchronized multi-chart time-series crosshairs, semantic severity color coding, compact 4px-padded log tables, flamegraphs, and zero wasted whitespace."

colors:
  primary: "#632ca6"
  primary-light: "#7c3aed"
  canvas: "#f9fafb"
  surface-panel: "#ffffff"
  canvas-dark: "#0f1117"
  surface-dark: "#171a24"
  border-panel: "#e2e8f0"
  border-dark: "#262b38"
  ink: "#111827"
  ink-muted: "#64748b"
  sev-critical: "#ef4444"
  sev-warning: "#f59e0b"
  sev-ok: "#10b981"
  sev-nodata: "#94a3b8"
  series-1: "#3b82f6"
  series-2: "#8b5cf6"
  series-3: "#06b6d4"
  series-4: "#f97316"

typography:
  panel-title:
    fontFamily: "system-ui, -apple-system, sans-serif"
    fontSize: 13px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: 0.1px
  metric-hero:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: 28px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.6px
  log-row:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0
---

# Datadog Design System Analysis

## 1. Core Principles
- **Maximum Signal per Viewport**: Dashboard widgets use a tight `13px` panel header, `8px` internal padding, and `1px` flat borders (`#e2e8f0` / `#262b38`) with zero drop-shadows so 12–16 live charts fit cleanly on a 1080p monitor.
- **Left-Edge Severity Bars**: Log rows and alert cards indicate status via a `3px` solid vertical bar on the far left edge (`#ef4444` critical, `#f59e0b` warn, `#10b981` ok) rather than painting the entire row background.
- **Time-Scrubber Synchronization**: A unified global time-range picker (`Past 15m`, `Past 1h`, `UTC`) sits in the top bar; hovering any chart draws a synchronized vertical hairline across all sibling charts.
