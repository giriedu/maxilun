---
version: alpha
name: Neon-Serverless-Postgres-design-analysis
description: "Neon's serverless Postgres design system features pitch-black technical surfaces (#0a0b0d), high-luminance phosphor green accents (#00e599), interactive autoscaling compute gauges, and branching tree visualizations."

colors:
  canvas: "#0a0b0d"
  surface-1: "#121418"
  surface-2: "#181b20"
  border-hairline: "#262930"
  primary: "#00e599"
  on-primary: "#090a0c"
  ink: "#f3f4f6"
  ink-muted: "#9ca3af"

typography:
  display:
    fontFamily: "'Inter', system-ui, sans-serif"
    fontSize: 56px
    fontWeight: 600
    lineHeight: 1.06
    letterSpacing: -1.8px
  mono:
    fontFamily: "'JetBrains Mono', monospace"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0
---

# Neon Design System Analysis

## 1. Core Principles
- **Phosphor Green Precision**: A single high-energy accent (`#00e599`) is used for active database branches, compute autoscaling curves (`0.25 → 4 CU`), and primary CTAs with dark `#090a0c` text for crisp legibility.
- **Instant Connection String Drawer**: The primary dashboard view exposes pooled vs. direct connection strings with framework-specific tabs (`Drizzle`, `Prisma`, `Next.js`, `psql`) and masked password toggle.
