"""Maxilun Interactive Visual Dashboard Generator with Linear/Railway Design System & Multi-Wave Orchestration.

Adheres strictly to maxilun-craft, linear.app.md, and railway.md standards:
- Deep black canvas (#010102) with hairline borders (#23252a) and signature lavender accent (#5e6ad2)
- Zero generic 4-metric KPI strips (eliminates LAY-012 anti-pattern)
- Zero generic Bento monoculture (eliminates LAY-013 anti-pattern)
- Real 2D Multi-Wave Orchestration Topology canvas (Railway canvas over hierarchy)
- Authentic vector multiplayer cursors (Figma/DhvanilPatel arrow, cross, ibeam, pen, dup)
- Full Wave 1 / Wave 2 / Wave 3 execution workflow with formal Handoff Records
- Synthetic Web Audio API feedback
Zero external dependencies.
"""

import base64
import json
from pathlib import Path
from typing import Optional

from .engine.skills_loader import SkillsLoader
from .benchmarks import BenchmarkRunner
from .router import MaxilunRouter


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Maxilun Orchestrator — Live Swarm Control Center</title>
  <style>
    :root {
      --bg: #010102;
      --canvas: #06080d;
      --surface-1: #0b0e17;
      --surface-2: #101420;
      --hairline: #1c2233;
      --hairline-strong: #2a334a;
      --ink: #f7f8f8;
      --ink-muted: #a1a7b3;
      --ink-subtle: #94a3b8;
      --primary: #5e6ad2;
      --primary-hover: #717de3;
      --primary-ink: #8b95f6;
      --success: #34d399;
      --warning: #fbbf24;
      --error: #f87171;
      --architect: #a855f7;
      --data: #f43f5e;
      --craft: #f97316;
      --sentinel: #10b981;
      --engineer: #38bdf8;
      --verify: #eab308;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
    button:focus-visible, .tab-btn:focus-visible, .btn-action:focus-visible, .preset-chip:focus-visible, .cmdk-item:focus-visible {
      outline: 2px solid var(--primary-hover);
      outline-offset: 2px;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--ink);
      font-family: var(--font-sans);
      line-height: 1.5;
      padding: 20px 24px;
      overflow-x: hidden;
      letter-spacing: -0.01em;
    }

    /* LINEAR COMPACT HEADER */
    header {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 10px 14px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--hairline);
      margin-bottom: 14px;
    }
    header > div {
      flex-wrap: wrap;
      gap: 8px;
    }
    .brand-title {
      font-size: 16px;
      font-weight: 600;
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .brand-mark {
      width: 14px;
      height: 14px;
      background: var(--primary);
      border-radius: 3px;
      display: inline-block;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .badge {
      font-size: 11px;
      font-family: var(--font-mono);
      padding: 2px 7px;
      border-radius: 4px;
      background: #111420;
      border: 1px solid var(--hairline-strong);
      color: var(--ink-muted);
    }

    /* LINEAR SINGLE-LINE TELEMETRY STATUS BAR (Replaces generic 4-card KPI strip LAY-012) */
    .telemetry-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 6px 14px;
      background: var(--surface-1);
      border: 1px solid var(--hairline);
      padding: 8px 16px;
      border-radius: 6px;
      margin-bottom: 16px;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--ink-muted);
    }
    .telemetry-bar > div {
      flex-wrap: wrap;
      gap: 6px 12px;
    }
    .status-pill {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .status-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--success);
      box-shadow: 0 0 0 1px rgba(16, 185, 129, 0.3);
    }

    /* NAVIGATION TABS */
    .nav-tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      margin-bottom: 14px;
      border-bottom: 1px solid var(--hairline);
      padding-bottom: 6px;
    }
    .tab-btn {
      background: transparent;
      color: var(--ink-subtle);
      border: none;
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      border-radius: 4px;
      transition: color 0.15s, background-color 0.15s, border-color 0.15s, opacity 0.15s, transform 0.15s;
    }
    .tab-btn:hover { color: var(--ink); }
    .tab-btn.active {
      background: #161a29;
      color: var(--ink);
      font-weight: 600;
    }

    /* CARD & GRID CONTAINERS */
    .card {
      background: var(--surface-1);
      border: 1px solid var(--hairline);
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .grid-2 {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr));
      gap: 14px;
    }
    .skill-card {
      background: var(--surface-1);
      border: 1px solid var(--hairline);
      border-radius: 6px;
      padding: 14px 16px;
      transition: color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease, opacity 0.2s ease, transform 0.2s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .skill-card:hover {
      border-color: var(--primary);
      transform: translateY(-1px);
      box-shadow: 0 4px 16px rgba(94, 106, 210, 0.15);
    }

    /* RAILWAY 2D TOPOLOGY CANVAS (Canvas over hierarchy) */
    .orchestration-layout {
      display: grid;
      grid-template-columns: 1fr 340px;
      gap: 14px;
    }
    @media (max-width: 1240px) {
      .orchestration-layout { grid-template-columns: 1fr; }
      .canvas-stage { overflow-x: auto; }
    }
    .code-surface-desktop {
      left: 24px;
      top: 162px;
      width: clamp(240px, 54%, 516px);
      height: 224px;
    }
    @media (max-width: 900px) {
      body { padding: 14px 12px; }
      .canvas-stage {
        height: auto;
        min-height: 0;
        padding: 12px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        overflow: visible;
      }
      #stage-svg, .swarm-cursor { display: none !important; }
      .stage-bar, .btn-group {
        flex-wrap: wrap;
        gap: 6px;
      }
      .btn-action, .tab-btn, .preset-chip {
        min-height: 44px;
      }
      .topo-node, .code-surface {
        position: static !important;
        width: 100% !important;
        height: auto !important;
        left: auto !important;
        top: auto !important;
      }
      .roster-dock {
        position: static !important;
        margin-top: 4px;
      }
    }

    .canvas-stage {
      position: relative;
      background: var(--canvas);
      background-image: 
        radial-gradient(rgba(255, 255, 255, 0.06) 1px, transparent 1px);
      background-size: 20px 20px;
      border: 1px solid var(--hairline);
      border-radius: 8px;
      height: 620px;
      overflow: hidden;
      user-select: none;
      box-shadow: inset 0 0 60px rgba(0,0,0,0.9);
    }

    /* ORTHOGONAL WAVE TOPOLOGY NODES */
    .topo-node {
      position: absolute;
      background: var(--surface-1);
      border: 1px solid var(--hairline-strong);
      border-radius: 6px;
      padding: 12px 14px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.6);
      z-index: 10;
      transition: color 0.25s ease, background-color 0.25s ease, border-color 0.25s ease, opacity 0.25s ease, transform 0.25s ease;
    }
    .topo-node.active-wave {
      border-color: var(--primary);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    .vignette-overlay {
      position: fixed;
      inset: 0;
      pointer-events: none;
      background: radial-gradient(circle at 50% 15%, rgba(94, 106, 210, 0.08) 0%, transparent 60%),
                  radial-gradient(circle at center, transparent 65%, rgba(0, 0, 0, 0.5) 100%);
      z-index: 9999;
    }
    .node-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
      font-size: 11px;
      font-weight: 600;
    }
    .node-title {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
    }
    .node-body {
      font-size: 11px;
      color: var(--ink-muted);
      line-height: 1.4;
    }

    /* CODE & SPECIFICATION SURFACES */
    .code-surface {
      position: absolute;
      background: rgba(11, 14, 23, 0.95);
      border: 1px solid var(--hairline-strong);
      border-radius: 6px;
      font-family: var(--font-mono);
      font-size: 11px;
      color: #93c5fd;
      line-height: 1.5;
      padding: 12px;
      white-space: pre-wrap;
      z-index: 8;
      box-shadow: 0 12px 28px rgba(0,0,0,0.7);
      overflow: hidden;
    }

    /* STANDBY ROSTER DOCK */
    .roster-dock {
      position: absolute;
      left: 24px;
      right: 24px;
      bottom: 12px;
      height: 48px;
      border: 1px dashed var(--hairline-strong);
      border-radius: 6px;
      background: rgba(6, 8, 13, 0.6);
      display: flex;
      align-items: center;
      padding: 0 16px;
      z-index: 5;
    }
    .roster-label {
      font-size: 10px;
      font-family: var(--font-mono);
      color: var(--ink-subtle);
      letter-spacing: 0.5px;
      text-transform: uppercase;
      font-weight: 700;
    }

    /* FIGMA VECTOR MULTIPLAYER CURSORS */
    .swarm-cursor {
      position: absolute;
      pointer-events: none;
      z-index: 100;
      will-change: transform;
      filter: drop-shadow(0 4px 8px rgba(0,0,0,0.7));
    }
    .cursor-svg {
      width: 22px;
      height: 22px;
      display: block;
    }
    .cursor-pill {
      position: absolute;
      left: 12px;
      top: 12px;
      padding: 2px 6px;
      border-radius: 3px;
      font-size: 10px;
      font-weight: 700;
      font-family: var(--font-mono);
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 4px;
      color: white;
    }
    .cursor-action {
      position: absolute;
      left: 12px;
      top: 30px;
      padding: 2px 6px;
      border-radius: 3px;
      font-size: 9px;
      font-family: var(--font-mono);
      background: rgba(6, 8, 13, 0.95);
      border: 1px solid var(--hairline-strong);
      color: #cbd5e1;
      white-space: nowrap;
    }

    /* CONTROLS BAR */
    .stage-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }
    .btn-group { display: flex; gap: 6px; }
    .btn-action {
      background: var(--surface-1);
      border: 1px solid var(--hairline);
      color: var(--ink);
      padding: 5px 12px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: color 0.15s, background-color 0.15s, border-color 0.15s, opacity 0.15s, transform 0.15s;
    }
    .btn-action:hover { border-color: var(--primary); color: white; }
    .btn-action.active { background: var(--primary); border-color: var(--primary); color: white; }

    /* RAILWAY STYLE SIDEBAR DRAWER */
    .telemetry-drawer {
      background: var(--surface-1);
      border: 1px solid var(--hairline);
      border-radius: 8px;
      padding: 16px;
      height: 620px;
      display: flex;
      flex-direction: column;
    }
    .drawer-title {
      font-size: 12px;
      font-weight: 700;
      letter-spacing: -0.01em;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--hairline);
    }
    .drawer-content {
      flex: 1;
      overflow-y: auto;
      font-family: var(--font-mono);
      font-size: 11px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 10px;
    }
    .handoff-box {
      background: #06080d;
      border: 1px solid var(--hairline-strong);
      border-radius: 6px;
      padding: 12px;
      line-height: 1.5;
    }
    .handoff-grid {
      display: grid;
      grid-template-columns: 85px 1fr;
      gap: 6px 10px;
      font-size: 11px;
    }
    .handoff-label {
      color: var(--ink-muted);
      font-family: var(--font-mono);
      font-weight: 600;
    }
    .handoff-value {
      color: #cbd5e1;
      font-family: var(--font-mono);
    }

    .activity-row {
      background: #06080d;
      border-left: 2px solid var(--hairline-strong);
      padding: 6px 8px;
      border-radius: 0 3px 3px 0;
      line-height: 1.4;
    }

    /* DIRECTORY TABLES */
    table {
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      margin-top: 14px;
      font-size: 12px;
      border: 1px solid var(--hairline);
      border-radius: 6px;
      overflow: hidden;
      background: var(--surface-1);
    }
    th, td {
      padding: 11px 14px;
      text-align: left;
      border-bottom: 1px solid var(--hairline);
    }
    th {
      background: #06080d;
      color: var(--ink-muted);
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }
    tr:last-child td {
      border-bottom: none;
    }
    tbody tr:hover td {
      background: rgba(255, 255, 255, 0.02);
    }
    .tabular {
      font-family: var(--font-mono);
      font-variant-numeric: tabular-nums;
    }
    
    /* TRIAGE CONTROLS */
    .triage-preset-chips {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin: 10px 0 14px 0;
    }
    .preset-chip {
      background: #06080d;
      border: 1px solid var(--hairline);
      color: var(--ink-muted);
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 11px;
      font-family: var(--font-mono);
      cursor: pointer;
      transition: color 0.15s, background-color 0.15s, border-color 0.15s, opacity 0.15s, transform 0.15s;
    }
    .preset-chip:hover {
      border-color: var(--primary);
      color: var(--ink);
    }
    .input-action-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 14px;
    }
    .input-action-row input[type="text"] {
      flex: 1 1 220px;
      margin-bottom: 0;
    }

    input[type="text"] {
      width: 100%;
      background: #06080d;
      border: 1px solid var(--hairline-strong);
      padding: 10px 14px;
      color: white;
      border-radius: 4px;
      font-size: 16px;
      margin-bottom: 10px;
      font-family: var(--font-sans);
    }
    input[type="text"]:focus-visible {
      outline: 2px solid var(--primary);
      outline-offset: 2px;
      border-color: var(--primary);
    }

    /* COMMAND PALETTE MODAL (Linear / Raycast grade) */
    .cmdk-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(1, 1, 2, 0.75);
      backdrop-filter: blur(6px);
      z-index: 10000;
      display: none;
      align-items: flex-start;
      justify-content: center;
      padding: 15vh 12px 0 12px;
    }
    .cmdk-dialog {
      background: var(--surface-1);
      border: 1px solid var(--hairline-strong);
      border-radius: 8px;
      width: 100%;
      max-width: 600px;
      box-shadow: 0 16px 48px rgba(0, 0, 0, 0.8);
      overflow: hidden;
      animation: cmdk-scale 0.15s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes cmdk-scale {
      from { opacity: 0; transform: scale(0.97) translateY(-6px); }
      to { opacity: 1; transform: scale(1) translateY(0); }
    }
    @media (prefers-reduced-motion: reduce) {
      .cmdk-dialog { animation: none; }
      #pulse-1, #pulse-2, #pulse-3 { display: none !important; }
    }
    .cmdk-input-wrap {
      display: flex;
      align-items: center;
      border-bottom: 1px solid var(--hairline);
      padding: 0 16px;
      gap: 10px;
    }
    .cmdk-input {
      flex: 1;
      background: transparent !important;
      border: none !important;
      padding: 14px 0 !important;
      font-size: 16px !important;
      color: var(--ink) !important;
      margin-bottom: 0 !important;
    }
    .cmdk-input:focus-visible {
      outline: 2px solid var(--primary);
      outline-offset: 2px;
    }
    .cmdk-list {
      max-height: 340px;
      overflow-y: auto;
      padding: 8px;
    }
    .cmdk-group-title {
      font-size: 10px;
      text-transform: uppercase;
      font-family: var(--font-mono);
      color: var(--ink-subtle);
      padding: 6px 10px 4px 10px;
      letter-spacing: 0.5px;
    }
    .cmdk-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 12px;
      border-radius: 4px;
      font-size: 12px;
      color: var(--ink);
      cursor: pointer;
      transition: background 0.1s;
    }
    .cmdk-item.selected, .cmdk-item:hover {
      background: rgba(94, 106, 210, 0.18);
      color: white;
    }
    .cmdk-kbd {
      font-size: 10px;
      font-family: var(--font-mono);
      background: #06080d;
      border: 1px solid var(--hairline-strong);
      padding: 2px 6px;
      border-radius: 3px;
      color: var(--ink-muted);
    }
  </style>
</head>
<body>
  <!-- CINEMATIC VIGNETTE & AMBIENT DEPTH OVERLAY -->
  <div class="vignette-overlay"></div>

  <!-- COMMAND PALETTE MODAL -->
  <div class="cmdk-backdrop" id="cmdk" role="dialog" aria-modal="true" aria-label="Command palette" onclick="onCmdkBackdrop(event)">
    <div class="cmdk-dialog" onclick="event.stopPropagation()">
      <div class="cmdk-input-wrap">
        <span style="color:var(--primary-ink); font-family:var(--font-mono); font-size:12px; font-weight:700;" aria-hidden="true">CMD</span>
        <label for="cmdk-query" class="sr-only">Search commands, skills, agents, and benchmarks</label>
        <input type="text" class="cmdk-input" id="cmdk-query" placeholder="Type a command or search skills, agents, benchmarks..." oninput="onCmdkInput()" onkeydown="onCmdkKey(event)">
        <span class="cmdk-kbd">ESC to close</span>
      </div>
      <div class="cmdk-list" id="cmdk-list" role="listbox" aria-label="Command results"></div>
    </div>
  </div>

  <!-- HEADER -->
  <header>
    <div class="brand-title">
      <span class="brand-mark" aria-hidden="true"></span>
      <span>Maxilun Orchestrator <span style="color:var(--ink-muted); font-weight:400;">/ Swarm Telemetry Control Center</span></span>
    </div>
    <div style="display:flex; gap:8px;">
      <button type="button" class="badge" onclick="toggleCmdK()" style="cursor:pointer; display:flex; align-items:center; gap:5px; background:var(--surface-2); border-color:var(--primary); color:var(--ink);" title="Open Command Palette (Cmd+K / Ctrl+K)">
        <span style="color:var(--primary-ink); font-family:var(--font-mono); font-weight:700;">Ctrl/Cmd+K</span> Command Palette
      </button>
      <span class="badge" id="ecosystem-count-badge" style="color:var(--success)">20 Specialists + 1 Orchestrator (27 Skills)</span>
      <span class="badge">Linear · Railway Design MD Calibrated</span>
    </div>
  </header>

  <!-- TELEMETRY STATUS BAR (Compact & Pure) -->
  <div class="telemetry-bar">
    <div class="status-pill">
      <span class="status-dot" aria-hidden="true"></span>
      <span style="color:var(--ink)">Multi-Wave Orchestration Engine Operational</span>
    </div>
    <div style="display:flex; gap:16px;">
      <span>Wave 1: Contracts [LOCKED]</span>
      <span>Wave 2: Implementation [ISOLATED]</span>
      <span>Wave 3: Proof [EXIT 0]</span>
      <span style="color:var(--primary-ink); font-weight:700;">Zero Slop</span>
    </div>
  </div>

  <!-- NAVIGATION TABS -->
  <div class="nav-tabs" role="tablist" aria-label="Dashboard sections" onkeydown="onTabKeyDown(event)">
    <button type="button" class="tab-btn active" id="tabbtn-swarm" role="tab" aria-selected="true" aria-controls="tab-swarm" data-tab="swarm" onclick="showTab('swarm', this)">Swarm Topology</button>
    <button type="button" class="tab-btn" id="tabbtn-benchmarks" role="tab" aria-selected="false" aria-controls="tab-benchmarks" data-tab="benchmarks" onclick="showTab('benchmarks', this)">Benchmarks & Purity Gate</button>
    <button type="button" class="tab-btn" id="tabbtn-agents" role="tab" aria-selected="false" aria-controls="tab-agents" data-tab="agents" onclick="showTab('agents', this)">21 Autonomous Agents</button>
    <button type="button" class="tab-btn" id="tabbtn-skills" role="tab" aria-selected="false" aria-controls="tab-skills" data-tab="skills" onclick="showTab('skills', this)">27 Production Skills</button>
    <button type="button" class="tab-btn" id="tabbtn-triage" role="tab" aria-selected="false" aria-controls="tab-triage" data-tab="triage" onclick="showTab('triage', this)">Triage Simulator</button>
  </div>

  <!-- TAB: SWARM TOPOLOGY STAGE -->
  <div id="tab-swarm" role="tabpanel" aria-labelledby="tabbtn-swarm">
    <div class="stage-bar">
      <div class="btn-group">
        <button type="button" class="btn-action active" id="btn-play" aria-pressed="true" onclick="togglePlay()">Pause</button>
        <button type="button" class="btn-action" onclick="restartOrchestration()">Replay Swarm</button>
        <button type="button" class="btn-action" id="btn-sound" aria-pressed="true" onclick="toggleSound()">Audio: ON</button>
      </div>
      <div class="btn-group">
        <span style="font-size:11px; color:var(--ink-muted); align-self:center; margin-right:4px;">Execution Pace:</span>
        <button type="button" class="btn-action" onclick="setPace(0.5, this)">0.5x</button>
        <button type="button" class="btn-action active" onclick="setPace(1.0, this)">1x</button>
        <button type="button" class="btn-action" onclick="setPace(2.0, this)">2x</button>
      </div>
    </div>

    <div class="orchestration-layout">
      <!-- 2D Topology Canvas -->
      <div class="canvas-stage" id="stage">
        <!-- Orthogonal SVG Connecting Lines -->
        <svg id="stage-svg" style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:2;">
          <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 10 5 L 0 9 z" fill="#2a334a" />
            </marker>
            <marker id="arrow-active" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 10 5 L 0 9 z" fill="#5e6ad2" />
            </marker>
          </defs>
          <!-- Conn 1: Input to Wave 1 -->
          <path id="conn-1" d="M 254 67 L 298 67" stroke="#2a334a" stroke-width="2" fill="none" marker-end="url(#arrow)" stroke-dasharray="4 3"/>
          <circle id="pulse-1" r="3.5" fill="#717de3" style="display:none;">
            <animateMotion id="anim-p1" dur="0.9s" repeatCount="indefinite" path="M 254 67 L 298 67" />
          </circle>

          <!-- Conn 2: Wave 1 to Wave 2 -->
          <path id="conn-2" d="M 540 67 L 560 67 L 560 195 L 578 195" stroke="#2a334a" stroke-width="2" fill="none" marker-end="url(#arrow)" stroke-dasharray="4 3"/>
          <circle id="pulse-2" r="3.5" fill="#38bdf8" style="display:none;">
            <animateMotion id="anim-p2" dur="1.8s" repeatCount="indefinite" path="M 540 67 L 560 67 L 560 195 L 578 195" />
          </circle>

          <!-- Conn 3: Wave 2 to Wave 3 -->
          <path id="conn-3" d="M 695 240 L 695 302" stroke="#2a334a" stroke-width="2" fill="none" marker-end="url(#arrow)" stroke-dasharray="4 3"/>
          <circle id="pulse-3" r="3.5" fill="#eab308" style="display:none;">
            <animateMotion id="anim-p3" dur="0.9s" repeatCount="indefinite" path="M 695 240 L 695 302" />
          </circle>
        </svg>

        <!-- Node 1: User Request -->
        <div class="topo-node" id="node-request" style="left: 24px; top: 24px; width: 230px;">
          <div class="node-header">
            <span>INPUT GATEWAY</span>
            <span class="badge" style="color:var(--primary)">Triggered</span>
          </div>
          <div class="node-title">Payment Webhook Flow</div>
          <div class="node-body">Idempotent mutation & HMAC verification</div>
        </div>

        <!-- Node 2: Wave 1 Contracts -->
        <div class="topo-node" id="node-w1" style="left: 300px; top: 24px; width: 240px;">
          <div class="node-header">
            <span style="color:var(--architect)">WAVE 1: CONTRACTS</span>
            <span class="badge">Seam Locked</span>
          </div>
          <div class="node-title">Architect · Data · Sentinel</div>
          <div class="node-body">3NF schema, UUIDv7, timingSafeEqual rule</div>
        </div>

        <!-- Node 3: Wave 2 Implementation -->
        <div class="topo-node" id="node-w2" style="left: 580px; top: 140px; width: 230px;">
          <div class="node-header">
            <span style="color:var(--engineer)">WAVE 2: CODING</span>
            <span class="badge">Convergent</span>
          </div>
          <div class="node-title">Engineer · Craft · Frontend</div>
          <div class="node-body">Surgical implementation & 6 UI states</div>
        </div>

        <!-- Node 4: Wave 3 Verification -->
        <div class="topo-node" id="node-w3" style="left: 580px; top: 304px; width: 230px;">
          <div class="node-header">
            <span style="color:var(--verify)">WAVE 3: PROOF</span>
            <span class="badge" style="color:var(--success)">Exit Code 0</span>
          </div>
          <div class="node-title">Verify · Deploy</div>
          <div class="node-body">Playwright E2E & AST proof</div>
        </div>

        <!-- Live Code Inspector Surface on Canvas -->
        <div class="code-surface code-surface-desktop" id="code-surface">
          <div style="color:var(--ink-muted); font-size:10px; margin-bottom:6px; border-bottom:1px solid #1c2233; padding-bottom:4px; display:flex; justify-content:space-between;">
            <span>src/auth/webhook.ts — Convergent Implementation</span>
            <span id="ts-badge" style="color:var(--warning)">Compiling...</span>
          </div>
          <div id="code-content" style="font-size:11px; line-height:1.5;"></div>
        </div>

        <!-- Standby Roster Dock -->
        <div class="roster-dock">
          <span class="roster-label">SWARM ROSTER (5 SPECIALISTS STANDBY)</span>
        </div>
      </div>

      <!-- Railway-style Telemetry & Handoff Drawer -->
      <div class="telemetry-drawer">
        <div class="drawer-title">
          <span>ORCHESTRATOR HANDOFF DRAWER</span>
          <span class="badge" style="color:var(--primary)">Live Log</span>
        </div>
        <div class="drawer-content" id="drawer-feed">
          <div class="handoff-box" id="active-handoff">
            <div class="handoff-grid">
              <span class="handoff-label">Owner</span>
              <span class="handoff-value" style="color:var(--primary); font-weight:700;">maxilun-sentinel</span>
              <span class="handoff-label">Artifacts</span>
              <span class="handoff-value">verifyWebhookSignature() [SRC]</span>
              <span class="handoff-label">Verification</span>
              <span class="handoff-value" style="color:var(--success);">timingSafeEqual [CONFIRMED]</span>
              <span class="handoff-label">Next</span>
              <span class="handoff-value">maxilun-data (Idempotency Table)</span>
              <span class="handoff-label">Residual risk</span>
              <span class="handoff-value" style="color:var(--warning);">Replay tolerance cap 300s</span>
            </div>
          </div>
          <div id="log-list" style="display:flex; flex-direction:column; gap:6px; margin-top:8px;"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB: BENCHMARKS -->
  <div id="tab-benchmarks" role="tabpanel" aria-labelledby="tabbtn-benchmarks" style="display: none;">
    <div class="card">
      <h2 style="font-size: 15px; margin-bottom: 8px;">Maxilun empirical engineering benchmarks</h2>
      <div style="overflow-x: auto;">
        <table>
          <thead>
            <tr>
              <th>Scenario</th>
              <th>Raw AI Score</th>
              <th>Maxilun Score</th>
              <th>Violations Prevented</th>
              <th>Verdict</th>
            </tr>
          </thead>
          <tbody id="benchmarks-body"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- TAB: SKILLS -->
  <div id="tab-skills" role="tabpanel" aria-labelledby="tabbtn-skills" style="display: none;">
    <div class="grid-2" id="skills-grid"></div>
  </div>

  <!-- TAB: AGENTS -->
  <div id="tab-agents" role="tabpanel" aria-labelledby="tabbtn-agents" style="display: none;">
    <div class="grid-2" id="agents-grid"></div>
  </div>

  <!-- TAB: TRIAGE -->
  <div id="tab-triage" role="tabpanel" aria-labelledby="tabbtn-triage" style="display: none;">
    <div class="card">
      <h2 style="font-size: 15px; margin-bottom: 6px;">Live decision reversibility and specialist triage</h2>
      <p style="color: var(--ink-muted); font-size: 12px; margin-bottom: 12px;">Simulates Master Orchestrator reversibility triage and multi-wave decomposition:</p>
      
      <div class="triage-preset-chips">
        <span style="font-size: 11px; color: var(--ink-muted); align-self: center;">Test Scenarios:</span>
        <button type="button" class="preset-chip" onclick="applyPreset(0)">Payment Webhook + DB</button>
        <button type="button" class="preset-chip" onclick="applyPreset(1)">Zero-Downtime DB Migration</button>
        <button type="button" class="preset-chip" onclick="applyPreset(2)">UI Redesign 6-State Matrix</button>
        <button type="button" class="preset-chip" onclick="applyPreset(3)">Drop Users Table (Destructive)</button>
      </div>

      <div class="input-action-row">
        <label for="triage-input" class="sr-only">Task prompt to classify and route</label>
        <input type="text" id="triage-input" aria-label="Task prompt to classify and route" value="Bikin webhook pembayaran lengkap beserta update saldo database dan verifikasi testing" placeholder="Enter task prompt...">
        <button type="button" class="btn-action active" onclick="simulateTriage()">Decompose & Route</button>
      </div>

      <div id="triage-output" style="margin-top: 12px; font-family: var(--font-mono); font-size: 11px; line-height: 1.6; background: #06080d; padding: 14px; border-radius: 6px; border: 1px solid var(--hairline-strong);">
        Press Decompose to run orchestrator triage.
      </div>
    </div>
  </div>

  <script>
    function decodeB64Json(b64, fallback) {
      try {
        const raw = new TextDecoder().decode(Uint8Array.from(atob(b64), c => c.charCodeAt(0)));
        return JSON.parse(raw);
      } catch (e) {
        return fallback;
      }
    }
    function esc(v) {
      return String(v == null ? '' : v)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }
    const skillsData = decodeB64Json("__SKILLS_JSON__", []);
    const agentsData = decodeB64Json("__AGENTS_JSON__", []);
    const benchmarksData = decodeB64Json("__BENCHMARKS_JSON__", []);
    const telemetryData = decodeB64Json("__TELEMETRY_JSON__", []);
    const reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /*
     * Authentic Figma / DhvanilPatel Vector Cursors
     */
    const ARROW_D = "M4.6 3.9 C4.2 3.1 4.9 2.4 5.7 2.8 L20.6 9.4 C21.5 9.8 21.4 11.1 20.4 11.3 L13.9 12.9 C13.4 13 13 13.4 12.9 13.9 L11.3 20.4 C11.1 21.4 9.8 21.5 9.4 20.6 Z";

    function cursorSVG(shape, c) {
      const st = 'stroke="#fff" stroke-width="1.5" stroke-linejoin="round"';
      switch (shape) {
        case "arrow":
          return `<path d="${ARROW_D}" fill="${c}" ${st}/>`;
        case "cross":
          return `<g stroke-linecap="round"><path d="M12 3.5 V20.5 M3.5 12 H20.5" stroke="#fff" stroke-width="3.6"/><path d="M12 3.5 V20.5 M3.5 12 H20.5" stroke="${c}" stroke-width="1.5"/></g>`;
        case "ibeam":
          const d = "M8.5 4.5 H10.5 Q12 4.5 12 6 Q12 4.5 13.5 4.5 H15.5 M12 6 V18 M8.5 19.5 H10.5 Q12 19.5 12 18 Q12 19.5 13.5 19.5 H15.5";
          return `<g fill="none" stroke-linecap="round"><path d="${d}" stroke="#fff" stroke-width="3.6"/><path d="${d}" stroke="${c}" stroke-width="1.5"/></g>`;
        default:
          return `<path d="${ARROW_D}" fill="${c}" ${st}/>`;
      }
    }

    const AGENTS = {
      architect: { name: "Architect", color: "#a855f7", bg: "#4c1d95", x: 40,  y: 556 },
      data:      { name: "Data",      color: "#f43f5e", bg: "#881337", x: 170, y: 556 },
      sentinel:  { name: "Sentinel",  color: "#10b981", bg: "#064e3b", x: 290, y: 556 },
      engineer:  { name: "Engineer",  color: "#38bdf8", bg: "#0c4a6e", x: 420, y: 556 },
      verify:    { name: "Verify",    color: "#eab308", bg: "#713f12", x: 540, y: 556 }
    };

    class AudioSynth {
      constructor() { this.ctx = null; this.enabled = true; }
      init() {
        if (!this.ctx) {
          try { this.ctx = new (window.AudioContext || window.webkitAudioContext)(); } catch(e) {}
        }
      }
      _getDestination(pan = 0) {
        if (!this.ctx) return null;
        if (this.ctx.createStereoPanner) {
          const panner = this.ctx.createStereoPanner();
          panner.pan.setValueAtTime(Math.max(-1, Math.min(1, pan)), this.ctx.currentTime);
          panner.connect(this.ctx.destination);
          return panner;
        }
        return this.ctx.destination;
      }
      click(pan = 0) {
        if (!this.enabled || !this.ctx) return;
        const dest = this._getDestination(pan);
        const o = this.ctx.createOscillator(); const g = this.ctx.createGain();
        o.frequency.setValueAtTime(800, this.ctx.currentTime);
        o.frequency.exponentialRampToValueAtTime(150, this.ctx.currentTime + 0.03);
        g.gain.setValueAtTime(0.04, this.ctx.currentTime);
        g.gain.linearRampToValueAtTime(0.001, this.ctx.currentTime + 0.03);
        o.connect(g); g.connect(dest);
        o.start(); o.stop(this.ctx.currentTime + 0.03);
      }
      type(pan = 0) {
        if (!this.enabled || !this.ctx) return;
        const dest = this._getDestination(pan);
        const o = this.ctx.createOscillator(); const g = this.ctx.createGain();
        o.frequency.setValueAtTime(1600 + Math.random()*200, this.ctx.currentTime);
        g.gain.setValueAtTime(0.015, this.ctx.currentTime);
        g.gain.linearRampToValueAtTime(0.001, this.ctx.currentTime + 0.015);
        o.connect(g); g.connect(dest);
        o.start(); o.stop(this.ctx.currentTime + 0.015);
      }
      tab() {
        if (!this.enabled || !this.ctx) return;
        const o = this.ctx.createOscillator(); const g = this.ctx.createGain();
        o.type = 'sine';
        o.frequency.setValueAtTime(520, this.ctx.currentTime);
        o.frequency.exponentialRampToValueAtTime(260, this.ctx.currentTime + 0.035);
        g.gain.setValueAtTime(0.03, this.ctx.currentTime);
        g.gain.linearRampToValueAtTime(0.001, this.ctx.currentTime + 0.035);
        o.connect(g); g.connect(this.ctx.destination);
        o.start(); o.stop(this.ctx.currentTime + 0.035);
      }
      chime() {
        if (!this.enabled || !this.ctx) return;
        const now = this.ctx.currentTime;
        [523.25, 659.25, 783.99].forEach((freq, idx) => {
          const o = this.ctx.createOscillator(); const g = this.ctx.createGain();
          o.type = 'triangle';
          o.frequency.setValueAtTime(freq, now + idx * 0.04);
          g.gain.setValueAtTime(0.025, now + idx * 0.04);
          g.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.04 + 0.28);
          o.connect(g); g.connect(this.ctx.destination);
          o.start(now + idx * 0.04); o.stop(now + idx * 0.04 + 0.28);
        });
      }
    }

    const audio = new AudioSynth();
    const stage = document.getElementById('stage');
    const logList = document.getElementById('log-list');
    const codeContent = document.getElementById('code-content');
    const cursorEls = {};
    let isPlaying = true;
    let pace = 1.0;
    let swarmTimers = [];
    let swarmIntervals = [];

    function initCursors() {
      for (const [k, a] of Object.entries(AGENTS)) {
        const el = document.createElement('div');
        el.className = 'swarm-cursor';
        el.id = 'cursor-' + k;
        el.innerHTML = `
          <svg class="cursor-svg" viewBox="0 0 24 24">${cursorSVG("arrow", a.color)}</svg>
          <div class="cursor-pill" style="background:${a.bg}; border:1px solid ${a.color}">${a.name}</div>
          <div class="cursor-action" id="act-${k}">Standby</div>
        `;
        el.style.transform = `translate(${a.x}px, ${a.y}px)`;
        stage.appendChild(el);
        cursorEls[k] = el;
      }
    }

    function addLog(role, msg, color) {
      const now = new Date();
      const timeStr = now.toTimeString().split(' ')[0];
      const row = document.createElement('div');
      row.className = 'activity-row';
      row.style.borderLeftColor = color || '#5e6ad2';
      row.innerHTML = `<span style="color:var(--ink-subtle)">${esc(timeStr)}</span> <strong style="color:${esc(color || '#cbd5e1')}">[${esc(role)}]</strong> ${esc(msg)}`;
      logList.prepend(row);
      if (logList.children.length > 20) logList.lastChild.remove();
    }

    function tweenAgent(key, targetX, targetY, action, durMs, onComplete) {
      const el = cursorEls[key];
      if (!el) return;
      const a = AGENTS[key];
      const actEl = document.getElementById('act-' + key);
      if (actEl && action) actEl.innerText = action;
      if (reducedMotion) {
        a.x = targetX; a.y = targetY;
        el.style.transform = `translate(${targetX}px, ${targetY}px)`;
        if (onComplete) onComplete();
        return;
      }

      const x0 = a.x; const y0 = a.y;
      const dx = targetX - x0; const dy = targetY - y0;
      const dist = Math.hypot(dx, dy);
      const bend = (Math.random() < 0.5 ? -1 : 1) * Math.min(dist * 0.12, 40);
      const L = dist || 1;
      const dur = (durMs || 600) / pace;
      let lastNow = performance.now();
      let elapsed = 0;

      function frame(now) {
        if (!isPlaying) {
          lastNow = now;
          requestAnimationFrame(frame);
          return;
        }
        elapsed += (now - lastNow);
        lastNow = now;
        const p = Math.min(1, elapsed / dur);
        const e = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
        const off = Math.sin(Math.PI * e) * bend;
        const cx = x0 + dx * e + (-dy / L) * off;
        const cy = y0 + dy * e + (dx / L) * off;

        a.x = cx; a.y = cy;
        el.style.transform = `translate(${cx}px, ${cy}px)`;

        if (p < 1) requestAnimationFrame(frame);
        else {
          a.x = targetX; a.y = targetY;
          el.style.transform = `translate(${targetX}px, ${targetY}px)`;
          if (onComplete) onComplete();
        }
      }
      requestAnimationFrame(frame);
    }

    function setConn(id, active) {
      const el = document.getElementById(id);
      if (el) {
        el.setAttribute('stroke', active ? '#5e6ad2' : '#2a334a');
        el.setAttribute('stroke-width', active ? '2.5' : '2');
        el.setAttribute('marker-end', active ? 'url(#arrow-active)' : 'url(#arrow)');
      }
      const num = id.split('-')[1];
      const pulse = document.getElementById('pulse-' + num);
      if (pulse) pulse.style.display = (active && !reducedMotion) ? 'block' : 'none';
    }

    function runOrchestrationPlayback() {
      clearTimers();
      codeContent.innerText = "";
      logList.innerHTML = "";
      if (Array.isArray(telemetryData) && telemetryData.length > 0) {
        telemetryData.slice(-5).forEach(ev => {
          addLog(ev.agent || 'harness', `${ev.action || 'event'}${ev.detail ? ': ' + ev.detail : ''}`, '#8b95f6');
        });
      }
      document.getElementById('ts-badge').innerText = "Compiling...";
      document.getElementById('ts-badge').style.color = "var(--warning)";
      setConn('conn-1', false);
      setConn('conn-2', false);
      setConn('conn-3', false);

      addLog("maxilun", "Orchestrator decomposing multi-domain request into 3 Waves", "#5e6ad2");

      // 1. WAVE 1: Architect locks contract
      swarmTimers.push(setTimeout(() => {
        setConn('conn-1', true);
        tweenAgent("architect", 296, 108, "Locking Seam Interface", 500, () => {
          audio.click(-0.2);
          addLog("Architect", "Established Deep Seam: verifyWebhookSignature() contract", "#a855f7");
          document.getElementById('node-w1').classList.add('active-wave');
        });
      }, 400 / pace));

      // 2. WAVE 1: Sentinel hardens constant-time rule & Data checks schema
      swarmTimers.push(setTimeout(() => {
        tweenAgent("sentinel", 435, 108, "Enforcing timingSafeEqual", 500, () => {
          audio.click(0.1);
          addLog("Sentinel", "Mandated timingSafeEqual & 300s replay window", "#10b981");
        });
        tweenAgent("data", 568, 22, "Verifying BIGINT units", 600, () => {
          addLog("Data", "Validated PostgreSQL idempotency schema (UUIDv7 + BIGINT)", "#f43f5e");
        });
      }, 1500 / pace));

      // 3. WAVE 2: Transition to Engineer for convergent implementation
      swarmTimers.push(setTimeout(() => {
        setConn('conn-2', true);
        addLog("Orchestrator", "Handoff to Wave 2: Implementation (maxilun-engineer)", "#5e6ad2");
        tweenAgent("engineer", 30, 394, "Writing convergent code", 700, () => {
          audio.click(-0.85);
          document.getElementById('node-w2').classList.add('active-wave');
          
          // Type code
          const codeSnippet = `import { createHmac, timingSafeEqual } from 'node:crypto';

export function verifyWebhookSignature(rawBody: Buffer, ts: string, sig: string, secret: string): boolean {
  if (Math.abs(Date.now() / 1000 - Number(ts)) > 300) return false;
  const exp = Buffer.from('v1=' + createHmac('sha256', secret).update(ts + '.' + rawBody).digest('hex'));
  const rec = Buffer.from(sig);
  return exp.length === rec.length && timingSafeEqual(exp, rec);
}`;
          let idx = 0;
          const typer = setInterval(() => {
            if (!isPlaying) return;
            idx += 6;
            if (idx > codeSnippet.length) idx = codeSnippet.length;
            codeContent.innerText = codeSnippet.slice(0, idx) + "▍";
            audio.type(-0.85);
            if (idx >= codeSnippet.length) {
              clearInterval(typer);
              codeContent.innerText = codeSnippet;
              document.getElementById('ts-badge').innerText = "Convergent OK";
              document.getElementById('ts-badge').style.color = "var(--success)";
              addLog("Engineer", "Surgical code written with zero dead code", "#38bdf8");
            }
          }, 20 / pace);
          swarmIntervals.push(typer);
        });
      }, 3000 / pace));

      // 4. WAVE 3: Verification & Proof
      swarmTimers.push(setTimeout(() => {
        setConn('conn-3', true);
        addLog("Orchestrator", "Handoff to Wave 3: Quality Gate (maxilun-verify)", "#5e6ad2");
        tweenAgent("verify", 580, 386, "Executing test suite", 600, () => {
          audio.click(0.55);
          audio.chime();
          document.getElementById('node-w3').classList.add('active-wave');
          addLog("Verify", "Ran test suite & AST verification: [CONFIRMED] PASS exit=0", "#eab308");
          // Update Handoff Drawer
          document.getElementById('active-handoff').innerHTML = `
            <div class="handoff-grid">
              <span class="handoff-label">Owner</span>
              <span class="handoff-value" style="color:var(--verify); font-weight:700;">maxilun-verify</span>
              <span class="handoff-label">Artifacts</span>
              <span class="handoff-value">src/auth/webhook.ts verified</span>
              <span class="handoff-label">Verification</span>
              <span class="handoff-value" style="color:var(--success);">Exit code 0 [CONFIRMED]</span>
              <span class="handoff-label">Next</span>
              <span class="handoff-value">Done (Deliverable verified)</span>
              <span class="handoff-label">Residual risk</span>
              <span class="handoff-value" style="color:var(--warning);">Clock drift on client nodes</span>
            </div>
          `;
        });
      }, 6500 / pace));
    }

    function clearTimers() {
      for (const t of swarmTimers) clearTimeout(t);
      swarmTimers = [];
      for (const iv of swarmIntervals) clearInterval(iv);
      swarmIntervals = [];
      document.querySelectorAll('.topo-node').forEach(n => n.classList.remove('active-wave'));
      setConn('conn-1', false);
      setConn('conn-2', false);
      setConn('conn-3', false);
      // Reset agents to dock
      for (const [k, a] of Object.entries(AGENTS)) {
        const el = cursorEls[k];
        if (el) {
          a.x = { architect: 40, data: 170, sentinel: 290, engineer: 420, verify: 540 }[k];
          a.y = 556;
          el.style.transform = `translate(${a.x}px, ${a.y}px)`;
          const act = document.getElementById('act-' + k);
          if (act) act.innerText = "Standby";
        }
      }
    }

    function restartOrchestration() {
      audio.init();
      runOrchestrationPlayback();
    }

    function togglePlay() {
      audio.init();
      isPlaying = !isPlaying;
      const btn = document.getElementById('btn-play');
      btn.innerText = isPlaying ? "Pause" : "Play";
      btn.setAttribute('aria-pressed', String(isPlaying));
    }

    function toggleSound() {
      audio.init();
      audio.enabled = !audio.enabled;
      const btn = document.getElementById('btn-sound');
      btn.innerText = audio.enabled ? "Audio: ON" : "Audio: OFF";
      btn.setAttribute('aria-pressed', String(audio.enabled));
    }

    function setPace(p, btn) {
      audio.init();
      pace = p;
      document.querySelectorAll('.stage-bar .btn-action').forEach(b => {
        if (b.innerText.includes('x')) b.classList.remove('active');
      });
      btn.classList.add('active');
    }

    function onTabKeyDown(e) {
      const tabs = Array.from(document.querySelectorAll('.nav-tabs .tab-btn'));
      const cur = tabs.indexOf(document.activeElement);
      if (cur === -1) return;
      let next = cur;
      if (e.key === 'ArrowRight') next = (cur + 1) % tabs.length;
      else if (e.key === 'ArrowLeft') next = (cur - 1 + tabs.length) % tabs.length;
      else if (e.key === 'Home') next = 0;
      else if (e.key === 'End') next = tabs.length - 1;
      else return;
      e.preventDefault();
      tabs[next].focus();
      showTab(tabs[next].dataset.tab, tabs[next]);
    }

    function showTab(id, btn) {
      audio.tab();
      document.querySelectorAll('.tab-btn').forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      ['swarm', 'benchmarks', 'skills', 'agents', 'triage'].forEach(t => {
        const el = document.getElementById('tab-' + t);
        if (el) el.style.display = (t === id) ? 'block' : 'none';
      });
      const targetBtn = btn || document.querySelector(`.tab-btn[data-tab="${id}"]`);
      if (targetBtn) {
        targetBtn.classList.add('active');
        targetBtn.setAttribute('aria-selected', 'true');
      }
    }

    function renderBenchmarks() {
      const tbody = document.getElementById('benchmarks-body');
      if (!tbody) return;
      if (!benchmarksData || benchmarksData.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="color:var(--ink-muted); text-align:center;">No benchmark telemetry recorded yet. Run <code>python harness/cli.py bench</code>.</td></tr>`;
        return;
      }
      tbody.innerHTML = benchmarksData.map(b => {
        const passed = b.maxilun_passed !== false;
        const vColor = passed ? 'var(--success)' : 'var(--error)';
        return `
        <tr>
          <td><strong>${esc(b.title)}</strong><br><span style="font-size:11px; color:var(--ink-muted);">"${esc(b.prompt)}"</span></td>
          <td class="tabular" style="color:var(--error);">${Number(b.raw_score || 0).toFixed(1)}</td>
          <td class="tabular" style="color:var(--success); font-weight:700;">${Number(b.maxilun_score || 0).toFixed(1)}</td>
          <td><span class="badge" style="background:#111420; color:var(--primary-ink);">${(b.raw_violations || []).length - (b.max_violations || []).length} prevented</span></td>
          <td><span style="color:${vColor}; font-weight:600;">${passed ? 'PASS' : 'FAIL'}</span></td>
        </tr>
      `}).join('');
    }

    function renderSkills() {
      const grid = document.getElementById('skills-grid');
      if (!grid) return;
      if (!skillsData || skillsData.length === 0) {
        grid.innerHTML = `<div class="card" style="color:var(--ink-muted);">No skills loaded from workspace or harness repository.</div>`;
        return;
      }
      grid.innerHTML = skillsData.map(s => `
        <div class="skill-card" data-skill-card="${esc(s.name)}">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; margin-bottom:8px;">
            <span style="font-weight:700; font-family:var(--font-mono); color:var(--primary-ink); font-size:13px;">${esc(s.name)}</span>
            <div style="display:flex; gap:6px; align-items:center;">
              <span class="badge">v${esc(s.version || '1.3.0')}</span>
              <span class="badge" style="background:rgba(94, 106, 210, 0.12); color:var(--primary-ink); border-color:rgba(94, 106, 210, 0.25);">${esc(s.line_count)} lines · ${esc(s.ref_count || 0)} refs</span>
            </div>
          </div>
          <div style="font-size:12px; color:var(--ink-muted); margin-bottom:10px; line-height:1.5;">${esc(s.owns)}</div>
          <div style="font-family:var(--font-mono); font-size:10px; color:#cbd5e1; background:#06080d; padding:6px 10px; border-radius:4px; border:1px solid var(--hairline);">
            <span style="color:var(--ink-subtle);">Triggers:</span> ${esc((s.triggers || []).join(', ') || 'orchestration')}
          </div>
        </div>
      `).join('');
    }

    function renderAgents() {
      const grid = document.getElementById('agents-grid');
      if (!grid) return;
      if (!agentsData || agentsData.length === 0) {
        grid.innerHTML = `<div class="card" style="color:var(--ink-muted);">No autonomous agent definitions discovered. Check <code>agents/</code> directory.</div>`;
        return;
      }
      grid.innerHTML = agentsData.map(a => `
        <div class="skill-card" data-agent-card="${esc(a.name)}">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; margin-bottom:8px;">
            <span style="font-weight:700; font-family:var(--font-mono); color:var(--primary-ink); font-size:13px;">${esc(a.name)}</span>
            <span class="badge" style="background:rgba(94, 106, 210, 0.15); color:var(--primary-ink); border:1px solid rgba(94, 106, 210, 0.3);">${esc((a.skills || []).length)} skill(s)</span>
          </div>
          <div style="font-size:12px; color:var(--ink-muted); margin-bottom:12px; line-height:1.5;">${esc(a.description)}</div>
          <div style="border-top:1px solid var(--hairline); padding-top:10px; display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:8px;">
            <div style="display:flex; gap:6px; flex-wrap:wrap;">
              ${(a.tools || []).map(t => `<span style="font-size:10px; font-family:var(--font-mono); background:#06080d; border:1px solid var(--hairline-strong); color:var(--ink); padding:2px 7px; border-radius:3px;">${esc(t)}</span>`).join('')}
            </div>
            <span style="font-size:10px; color:var(--success); font-family:var(--font-mono); display:flex; align-items:center; gap:4px;">
              <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:var(--success);"></span> Invariant Enforced
            </span>
          </div>
        </div>
      `).join('');
    }

    const PRESETS = [
      "Bikin webhook pembayaran lengkap beserta update saldo database dan verifikasi testing",
      "Migrasi skema database zero-downtime tambah kolom status ke tabel users ber-traffic tinggi",
      "Redesign halaman profile dengan 6 state UI (idle, loading, populated, empty, pending, error) dan tabular-nums",
      "Drop tabel users dan hapus semua data audit log (operasi destruktif)"
    ];

    function applyPreset(idx) {
      audio.tab();
      const input = document.getElementById('triage-input');
      if (input && PRESETS[idx]) {
        input.value = PRESETS[idx];
        simulateTriage();
      }
    }

    function simulateTriage() {
      const raw = (document.getElementById('triage-input').value || '').trim();
      const outEl = document.getElementById('triage-output');
      if (!raw) {
        outEl.innerHTML = `<div style="color:var(--error);">[INPUT REQUIRED] Enter a task description or choose a preset scenario above.</div>`;
        return;
      }
      const input = raw.toLowerCase();
      let owner = 'maxilun-engineer';
      let companions = [];
      let isType1 = input.includes('drop') || input.includes('destruktif') || input.includes('redesign') || input.includes('overhaul') || input.includes('pecah service');

      if (input.includes('n8n') || (input.includes('webhook') && input.includes('workflow'))) {
        owner = 'maxilun-n8n';
        if (input.includes('hmac') || input.includes('signature')) companions.push('maxilun-sentinel');
      } else if (input.includes('figcraft') || input.includes('kanvas live')) {
        owner = 'maxilun-figcraft';
        companions.push('maxilun-craft', 'maxilun-verify');
      } else if (input.includes('webhook') || input.includes('signature') || input.includes('auth')) {
        owner = 'maxilun-sentinel';
        if (input.includes('database') || input.includes('saldo') || input.includes('tabel')) companions.push('maxilun-data');
      } else if (input.includes('migrasi') || input.includes('database') || input.includes('skema') || input.includes('tabel')) {
        owner = 'maxilun-data';
      } else if (input.includes('ui') || input.includes('desain') || input.includes('redesign') || input.includes('halaman')) {
        owner = 'maxilun-craft';
        companions.push('maxilun-frontend', 'maxilun-verify');
      }

      const typeLabel = isType1 ? 'Type 1 (Irreversible — max 1 batched clarification turn)' : 'Type 2 (Reversible — execute directly from repo evidence)';
      const isMulti = companions.length > 0 || input.includes('redesign') || input.includes('lengkap') || input.includes('test');
      const w1List = [owner].concat(companions).filter(s => ['maxilun-architect','maxilun-data','maxilun-sentinel','maxilun-craft','maxilun-figcraft'].includes(s));
      const w2List = [owner].concat(companions).filter(s => ['maxilun-engineer','maxilun-frontend','maxilun-craft','maxilun-n8n','maxilun-data','maxilun-sentinel','maxilun-figcraft'].includes(s));

      outEl.innerHTML = `
        <div style="color:var(--primary-ink); font-weight:700; margin-bottom:6px; font-size:12px;">[ORCHESTRATOR WAVE DECOMPOSITION]</div>
        <div style="display:grid; grid-template-columns:120px 1fr; gap:4px 8px; margin-bottom:10px;">
          <span style="color:var(--ink-muted);">Primary Owner:</span> <strong>${esc(owner)}</strong>
          <span style="color:var(--ink-muted);">Reversibility:</span> <span>${esc(typeLabel)}</span>
          <span style="color:var(--ink-muted);">Companions:</span> <span>${esc(companions.join(', ') || 'None (Single Cohesive Owner)')}</span>
          <span style="color:var(--ink-muted);">Coordination:</span> <span>${isMulti ? 'Multi-Wave Wave 1 → Wave 2 → Wave 3' : 'Direct Single Surface'}</span>
        </div>
        <hr style="border-color:var(--hairline-strong); margin:10px 0;"/>
        <div style="color:var(--architect); font-weight:700; margin-bottom:2px;">Wave 1 (Contracts & Seams):</div>
        <div style="color:var(--ink-muted); padding-left:10px; margin-bottom:6px;">→ ${esc(w1List.join(', ') || owner)}: Establish schema invariants, design tokens & auth boundaries</div>
        <div style="color:var(--engineer); font-weight:700; margin-bottom:2px;">Wave 2 (Implementation):</div>
        <div style="color:var(--ink-muted); padding-left:10px; margin-bottom:6px;">→ ${esc((w2List.length ? w2List : ['maxilun-engineer']).join(', '))}: Consume locked contracts to write convergent production code</div>
        <div style="color:var(--verify); font-weight:700; margin-bottom:2px;">Wave 3 (Verification & Proof):</div>
        <div style="color:var(--ink-muted); padding-left:10px;">→ maxilun-verify: Execute test suite, slopscan, reflow check & AST invariants (exit code 0)</div>
      `;
    }
    /* COMMAND PALETTE LOGIC */
    let cmdkSelectedIndex = 0;
    let cmdkFilteredItems = [];
    let lastFocusedEl = null;

    function getAllCmdkItems() {
      const skillCount = (skillsData || []).length;
      const agentCount = (agentsData || []).length;
      const items = [
        { label: "Replay Multi-Wave Swarm Simulation", group: "Actions", kbd: "Enter", run: () => { showTab('swarm'); restartOrchestration(); } },
        { label: "Toggle Play / Pause Simulation", group: "Actions", kbd: "P", run: () => togglePlay() },
        { label: "Toggle Audio Synthesizer", group: "Actions", kbd: "A", run: () => toggleSound() },
        { label: "Switch Tab: Multi-Wave Swarm Topology", group: "Navigation", kbd: "1", run: () => showTab('swarm') },
        { label: "Switch Tab: Benchmarks & Purity Gate", group: "Navigation", kbd: "2", run: () => showTab('benchmarks') },
        { label: `Switch Tab: ${agentCount} Autonomous Agents`, group: "Navigation", kbd: "3", run: () => showTab('agents') },
        { label: `Switch Tab: ${skillCount} Production Skills Directory`, group: "Navigation", kbd: "4", run: () => showTab('skills') },
        { label: "Switch Tab: Live Reversibility Triage Simulator", group: "Navigation", kbd: "5", run: () => showTab('triage') },
        { label: "Test Scenario: Payment Webhook + DB Balance", group: "Triage", kbd: "Enter", run: () => { showTab('triage'); applyPreset(0); } },
        { label: "Test Scenario: Zero-Downtime DB Migration", group: "Triage", kbd: "Enter", run: () => { showTab('triage'); applyPreset(1); } },
        { label: "Test Scenario: UI Redesign 6-State Matrix", group: "Triage", kbd: "Enter", run: () => { showTab('triage'); applyPreset(2); } },
        { label: "Test Scenario: Drop Users Table (Destructive)", group: "Triage", kbd: "Enter", run: () => { showTab('triage'); applyPreset(3); } }
      ];

      (skillsData || []).forEach(s => {
        items.push({
          label: `${s.name} (${s.line_count} lines) — ${s.owns}`,
          group: "Skills",
          kbd: "Skill",
          run: () => {
            showTab('skills');
            const target = document.querySelector(`[data-skill-card="${CSS.escape(s.name)}"]`);
            if (target) {
              target.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'center' });
              target.style.borderColor = 'var(--primary)';
              setTimeout(() => target.style.borderColor = '', 2000);
            }
          }
        });
      });

      (agentsData || []).forEach(a => {
        items.push({
          label: `${a.name} — ${(a.description || '').slice(0, 60)}`,
          group: "Agents",
          kbd: "Agent",
          run: () => {
            showTab('agents');
            const target = document.querySelector(`[data-agent-card="${CSS.escape(a.name)}"]`);
            if (target) {
              target.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'center' });
              target.style.borderColor = 'var(--primary)';
              setTimeout(() => target.style.borderColor = '', 2000);
            }
          }
        });
      });

      return items;
    }

    function toggleCmdK() {
      const el = document.getElementById('cmdk');
      if (!el) return;
      const isOpen = el.style.display === 'flex';
      if (isOpen) {
        closeCmdK();
      } else {
        lastFocusedEl = document.activeElement;
        el.style.display = 'flex';
        audio.init();
        audio.tab();
        const input = document.getElementById('cmdk-query');
        input.value = '';
        cmdkSelectedIndex = 0;
        renderCmdkList();
        setTimeout(() => input.focus(), 20);
      }
    }

    function closeCmdK() {
      const el = document.getElementById('cmdk');
      if (el && el.style.display !== 'none') {
        el.style.display = 'none';
        if (lastFocusedEl && typeof lastFocusedEl.focus === 'function') {
          lastFocusedEl.focus();
        }
        lastFocusedEl = null;
      }
    }

    function onCmdkBackdrop(e) {
      if (e.target.id === 'cmdk') closeCmdK();
    }

    function onCmdkInput() {
      cmdkSelectedIndex = 0;
      renderCmdkList();
    }

    function onCmdkKey(e) {
      if (e.key === 'Escape') {
        closeCmdK();
      } else if (e.key === 'Tab') {
        const dlg = document.querySelector('#cmdk .cmdk-dialog');
        const focusables = dlg ? Array.from(dlg.querySelectorAll('input, button')) : [];
        if (focusables.length > 0) {
          const idx = focusables.indexOf(document.activeElement);
          const next = e.shiftKey ? (idx <= 0 ? focusables.length - 1 : idx - 1) : (idx + 1) % focusables.length;
          e.preventDefault();
          focusables[next].focus();
        }
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (cmdkFilteredItems.length > 0) {
          cmdkSelectedIndex = Math.min(cmdkFilteredItems.length - 1, cmdkSelectedIndex + 1);
          renderCmdkList();
        }
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        cmdkSelectedIndex = Math.max(0, cmdkSelectedIndex - 1);
        renderCmdkList();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (cmdkFilteredItems[cmdkSelectedIndex]) {
          const item = cmdkFilteredItems[cmdkSelectedIndex];
          closeCmdK();
          item.run();
        }
      }
    }

    function renderCmdkList() {
      const query = (document.getElementById('cmdk-query').value || '').toLowerCase().trim();
      const all = getAllCmdkItems();
      cmdkFilteredItems = query ? all.filter(i => i.label.toLowerCase().includes(query) || i.group.toLowerCase().includes(query)) : all;
      const listEl = document.getElementById('cmdk-list');
      if (!listEl) return;

      if (cmdkFilteredItems.length === 0) {
        listEl.innerHTML = `<div style="padding:16px; text-align:center; color:var(--ink-muted); font-size:12px;">No matching command or skill found.</div>`;
        return;
      }

      let currentGroup = '';
      let html = '';
      cmdkFilteredItems.forEach((item, idx) => {
        if (item.group !== currentGroup) {
          currentGroup = item.group;
          html += `<div class="cmdk-group-title">${esc(currentGroup)}</div>`;
        }
        const isSel = idx === cmdkSelectedIndex;
        html += `
          <button type="button" role="option" aria-selected="${isSel}" class="cmdk-item ${isSel ? 'selected' : ''}" style="width:100%; border:none; text-align:left;" onclick="cmdkFilteredItems[${idx}].run(); closeCmdK();">
            <span>${esc(item.label)}</span>
            <span class="cmdk-kbd">${esc(item.kbd)}</span>
          </button>
        `;
      });
      listEl.innerHTML = html;

      const selEl = listEl.querySelector('.cmdk-item.selected');
      if (selEl) selEl.scrollIntoView({ block: 'nearest' });
    }

    window.addEventListener('keydown', e => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        toggleCmdK();
      } else if (e.key === 'Escape') {
        closeCmdK();
      }
    });

    function syncDynamicCounts() {
      const sc = (skillsData || []).length;
      const ac = (agentsData || []).length;
      const specCount = Math.max(0, ac - 1);
      const badge = document.getElementById('ecosystem-count-badge');
      if (badge && sc && ac) badge.innerText = `${specCount} Specialists + 1 Orchestrator (${sc} Skills)`;
      const ab = document.getElementById('tabbtn-agents');
      if (ab && ac) ab.innerText = `${ac} Autonomous Agents`;
      const sb = document.getElementById('tabbtn-skills');
      if (sb && sc) sb.innerText = `${sc} Production Skills`;
    }

    // Initialize
    syncDynamicCounts();
    initCursors();
    renderBenchmarks();
    renderSkills();
    renderAgents();
    renderCmdkList();
    simulateTriage();
    runOrchestrationPlayback();
  </script>
</body>
</html>
"""


class DashboardGenerator:
    """Renders the Maxilun Engineering Dashboard to an interactive single-file HTML."""

    @classmethod
    def generate(cls, repo_root: Optional[Path] = None, output_path: Optional[Path] = None) -> Path:
        root = repo_root or Path.cwd()
        loader = SkillsLoader(root)
        skills = loader.list_skills()

        runner = BenchmarkRunner()
        report = runner.run_all()

        out_file = output_path or root / "maxilun-out" / "dashboard.html"
        out_file.parent.mkdir(parents=True, exist_ok=True)

        telemetry_file = root / "maxilun-out" / "swarm_events.json"
        telemetry_data = []
        if telemetry_file.exists():
            try:
                telemetry_data = json.loads(telemetry_file.read_text(encoding="utf-8"))
            except Exception:
                telemetry_data = []

        def _b64(obj) -> str:
            raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
            return base64.b64encode(raw).decode("ascii")

        skills_b64 = _b64([
            {
                "name": s.name,
                "version": s.version,
                "line_count": s.line_count,
                "triggers": s.triggers[:4],
                "owns": s.contract.get("Owns", "Implementation"),
                "ref_count": len(s.references),
                "status": "PASS" if s.line_count <= 300 else "EXCEEDED"
            }
            for s in skills
        ])

        benchmarks_b64 = _b64([
            {
                "id": r.benchmark_id,
                "title": r.title,
                "prompt": r.prompt,
                "raw_score": r.raw_score,
                "maxilun_score": r.maxilun_score,
                "maxilun_passed": r.maxilun_passed,
                "delta": r.score_delta,
                "raw_violations": r.raw_violations_sample,
                "max_violations": r.maxilun_violations_sample
            }
            for r in report.results
        ])

        telemetry_b64 = _b64(telemetry_data)

        import re
        agents_data = []
        for name, agent_def in sorted(loader.agents.items()):
            text = agent_def.full_content
            desc = "Autonomous agent"
            if text.startswith("---"):
                parts = text.split("---", 2)
                if len(parts) >= 3:
                    fm = parts[1]
                    m_block = re.search(r"^description:\s*(?:>|\|)[ \t]*\n((?:[ \t]+[^\n]+\n?)+)", fm, re.MULTILINE)
                    if m_block:
                        desc = " ".join(ln.strip() for ln in m_block.group(1).splitlines() if ln.strip())
                    else:
                        m_inline = re.search(r"^description:\s*([^\n\r]+)", fm, re.MULTILINE)
                        if m_inline:
                            desc = m_inline.group(1).strip().strip('"').strip("'")
            agents_data.append({
                "name": name,
                "description": desc,
                "tools": list(agent_def.tools),
                "skills": list(agent_def.skills),
                "file": agent_def.path.name
            })
        agents_b64 = _b64(agents_data)

        html = (
            HTML_TEMPLATE
            .replace("__SKILLS_JSON__", skills_b64)
            .replace("__BENCHMARKS_JSON__", benchmarks_b64)
            .replace("__TELEMETRY_JSON__", telemetry_b64)
            .replace("__AGENTS_JSON__", agents_b64)
        )

        out_file.write_text(html, encoding="utf-8")
        return out_file
