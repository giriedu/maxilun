---
version: alpha
name: Discord-RealTime-Community-design-analysis
description: "Discord's multi-pane real-time communication design system is built on a 4-tier dark slate elevation hierarchy (#1e1f22 → #2b2d31 → #313338 → #383a40), blurple interactive accents (#5865f2), presence status badges, and ultra-fast keyboard channel switching."

colors:
  primary: "#5865f2"
  primary-hover: "#4752c4"
  surface-server-rail: "#1e1f22"
  surface-channel-sidebar: "#2b2d31"
  canvas-chat: "#313338"
  surface-message-hover: "#2e3035"
  surface-input: "#383a40"
  ink: "#f2f3f5"
  ink-muted: "#949ba4"
  ink-channel: "#80848e"
  status-online: "#23a55a"
  status-idle: "#f0b232"
  status-dnd: "#f23f43"

typography:
  channel-header:
    fontFamily: "'gg sans', 'Noto Sans', system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: 0
  message-body:
    fontFamily: "'gg sans', 'Noto Sans', system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.375
    letterSpacing: 0
---

# Discord Design System Analysis

## 1. Core Principles
- **4-Step Luminance Elevation Without Borders**: Instead of drawing `1px` lines between every panel, Discord separates the `72px` server rail (`#1e1f22`), `240px` channel list (`#2b2d31`), main chat stream (`#313338`), and composer input (`#383a40`) purely through calibrated dark-slate luminance steps.
- **Morphing Pill Indicators**: Server icons morph from `24px` circle (`border-radius: 50%`) to `16px` squircle (`border-radius: 16px`) on hover/active, paired with a left-edge white pill that scales height (`8px → 20px → 40px`) based on unread/hover/selected state.
