---
version: alpha
name: PlanetScale-Database-Platform-design-analysis
description: "PlanetScale's database platform design blends ultra-clean monochrome precision with electric orange-amber accents (#f97316), schema diff viewers, branching topology graphs, and sub-millisecond query insight tables."

colors:
  primary: "#f97316"
  canvas-dark: "#090a0f"
  surface-dark: "#11131a"
  surface-elevated: "#181b24"
  border-hairline: "#232734"
  ink-dark: "#f8fafc"
  ink-muted: "#94a3b8"
  diff-add-bg: "rgba(16, 185, 129, 0.14)"
  diff-add-text: "#34d399"
  diff-del-bg: "rgba(239, 68, 68, 0.14)"
  diff-del-text: "#f87171"

typography:
  display:
    fontFamily: "'Inter', system-ui, sans-serif"
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -1.5px
  sql-mono:
    fontFamily: "'JetBrains Mono', ui-monospace, monospace"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: 0
---

# PlanetScale Design System Analysis

## 1. Core Principles
- **Git-for-Databases Visual Language**: Database branches (`main` vs `deploy-request #42`) are visualized with clean SVG commit-graph rails, DDL schema diffs (`ALTER TABLE` additions in emerald, drops in coral), and zero-downtime migration progress steppers.
- **Monochrome Restraint**: 95% of the interface is neutral obsidian/slate (`#090a0f` / `#11131a`) with `1px` borders (`#232734`), reserving chromatic color strictly for query latency anomalies and primary deploy actions.
