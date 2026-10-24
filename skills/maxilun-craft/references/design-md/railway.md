---
version: alpha
name: Railway-Cloud-Canvas-design-analysis
description: "Railway's infrastructure deployment canvas replaces multi-level nested menus and breadcrumbs with a unified infinite 2D service-topology canvas: dark plum-slate surfaces (#13111c), orthogonal dependency connectors, and live deployment log drawers."

colors:
  canvas: "#13111c"
  surface-node: "#1b1828"
  surface-drawer: "#171522"
  border-node: "#2d2842"
  primary-violet: "#8b5cf6"
  status-deployed: "#10b981"
  status-building: "#f59e0b"
  status-crashed: "#ef4444"
  ink: "#f5f3ff"
  ink-muted: "#9ca3af"

typography:
  node-title:
    fontFamily: "'Inter', system-ui, sans-serif"
    fontSize: 15px
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: -0.2px
  log-mono:
    fontFamily: "'JetBrains Mono', ui-monospace, monospace"
    fontSize: 12.5px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0
---

# Railway Design System Analysis

## 1. Core Principles
- **Canvas Over Hierarchy**: Instead of burying services, databases, volumes, and cron jobs inside 4 levels of sidebar navigation and breadcrumbs, Railway renders the entire project architecture on an interactive 2D dot-grid canvas (`#13111c`). Clicking any service node slides open a right-hand detail drawer (`#171522`) in place.
