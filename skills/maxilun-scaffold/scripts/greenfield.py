#!/usr/bin/env python3
"""greenfield.py - Deterministic starter code generator for Maxilun Scaffold.

Generates complete, runnable, slop-free greenfield applications across 3 stacks
and 3 distinct domain archetypes (edtech, saas, ledger):
  1. nextjs: Next.js 15 App Router + React 19 + Tailwind CSS + Lucide
  2. vite-php: Decoupled React Vite SPA + PHP 8+ REST API (PDO SQLite in WAL mode)
  3. gas: Google Apps Script Web App (Code.gs + index.html + local_preview.html)

Includes Domain-to-Recipe auto-binding (first-fold hero + ui-motion recipes)
and instant realistic seed data.
"""
import argparse
import os
import sys
from pathlib import Path

# --- CORE CONFIG TEMPLATES ---

NEXTJS_PACKAGE_JSON = """{
  "name": "{name}",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "framer-motion": "^11.0.0",
    "lucide-react": "^0.460.0",
    "next": "15.0.0",
    "react": "19.0.0",
    "react-dom": "19.0.0"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "postcss": "^8",
    "tailwindcss": "^3.4.1",
    "typescript": "^5"
  }
}
"""

NEXTJS_TAILWIND_CONFIG = """import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        surface: "var(--surface)",
        "surface-elevated": "var(--surface-elevated)",
        border: "var(--border)",
        accent: "var(--accent)",
        "accent-foreground": "var(--accent-foreground)",
        muted: "var(--muted)",
        success: "var(--success)",
        warning: "var(--warning)",
        danger: "var(--danger)",
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [],
};
export default config;
"""

NEXTJS_GLOBALS_CSS = """@tailwind base;
@tailwind components;
@tailwind utilities;

/* PLACEHOLDER tokens so the starter runs. maxilun-craft replaces this whole block
   from the Craft Brief before any screen ships; shipping them unchanged makes every
   Maxilun app look the same. */
:root {
  --background: oklch(0.12 0.01 260);
  --foreground: oklch(0.95 0.005 260);
  --surface: oklch(0.16 0.012 260);
  --surface-elevated: oklch(0.20 0.015 260);
  --border: oklch(1 0 0 / 0.08);
  --accent: oklch(0.65 0.20 250);
  --accent-foreground: oklch(0.98 0 0);
  --muted: oklch(0.60 0.02 260);
  --success: oklch(0.68 0.16 150);
  --warning: oklch(0.75 0.18 75);
  --danger: oklch(0.62 0.22 25);
  --radius: 0.5rem;
}

body {
  background-color: var(--background);
  color: var(--foreground);
  font-feature-settings: "cv02", "cv03", "cv04", "cv11";
  -webkit-font-smoothing: antialiased;
}

@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
"""

NEXTJS_LAYOUT = """import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "{title}",
  description: "High-craft precision operational workspace.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="id">
      <body className="min-h-screen bg-background text-foreground antialiased selection:bg-accent/20 selection:text-accent">
        {children}
      </body>
    </html>
  );
}
"""

# --- MOTION PRIMITIVES ---

SLIDING_PILL_NAV = """"use client";

import * as React from "react";
import { motion } from "framer-motion";

export interface TabItem {
  id: string;
  label: string;
}

export function SlidingPillNav({
  tabs,
  activeId,
  onChange,
}: {
  tabs: TabItem[];
  activeId: string;
  onChange: (id: string) => void;
}) {
  return (
    <nav className="inline-flex items-center gap-1 p-1 rounded-lg bg-surface border border-border">
      {tabs.map((tab) => {
        const isActive = tab.id === activeId;
        return (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            className={`relative px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
              isActive ? "text-foreground" : "text-muted hover:text-foreground"
            }`}
          >
            {isActive && (
              <motion.div
                layoutId="active-pill"
                transition={{ type: "spring", stiffness: 380, damping: 30 }}
                className="absolute inset-0 rounded-md bg-surface-elevated shadow-sm border border-border/80"
              />
            )}
            <span className="relative z-10">{tab.label}</span>
          </button>
        );
      })}
    </nav>
  );
}
"""

HOLD_TO_CONFIRM_BTN = """"use client";

import * as React from "react";

export function HoldToConfirmButton({
  onConfirm,
  label = "Tekan dan Tahan untuk Konfirmasi",
}: {
  onConfirm: () => void;
  label?: string;
}) {
  const [progress, setProgress] = React.useState(0);
  const timerRef = React.useRef<NodeJS.Timeout | null>(null);

  const startHold = () => {
    const startTime = Date.now();
    const duration = 1000;
    timerRef.current = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const p = Math.min(100, (elapsed / duration) * 100);
      setProgress(p);
      if (p >= 100) {
        if (timerRef.current) clearInterval(timerRef.current);
        onConfirm();
        setProgress(0);
      }
    }, 16);
  };

  const cancelHold = () => {
    if (timerRef.current) clearInterval(timerRef.current);
    setProgress(0);
  };

  return (
    <button
      onMouseDown={startHold}
      onMouseUp={cancelHold}
      onMouseLeave={cancelHold}
      onTouchStart={startHold}
      onTouchEnd={cancelHold}
      className="relative overflow-hidden h-10 px-5 rounded-lg bg-surface border border-border text-xs font-medium text-foreground select-none"
    >
      <div
        className="absolute left-0 top-0 bottom-0 bg-accent/20 transition-all"
        style={{ width: `${progress}%` }}
      />
      <span className="relative z-10">{progress > 0 ? `Menahan... ${Math.round(progress)}%` : label}</span>
    </button>
  );
}
"""

# --- DOMAIN SPECIFICATIONS ---

DOMAINS = {
    "edtech": {
        "title": "Portal Asesmen & Akademik EduCore",
        "tag": "Tahun Ajaran 2026/2027 · Semester Gasal",
        "h1": "Pusat Asesmen & Manajemen Akademik Presisi.",
        "desc": "Platform terpadu evaluasi belajar, butir instrumen soal berbasis taksonomi, dan pemantauan capaian kompetensi peserta didik secara real-time.",
        "cta1": "Buka Ruang Ujian CBT",
        "cta2": "Bank Soal Asesmen",
        "metric_label": "Peserta Terdaftar",
        "metric_value": "15 Siswa",
        "table_heading": "Daftar Peserta Asesmen Aktif",
        "table_sub": "Data terverifikasi semester berjalan dengan status kehadiran live.",
        "cols": ["NISN", "Nama Peserta Didik", "Rombongan Belajar", "Kehadiran", "Status"],
        "data_ts": """export interface Item { id: string; col1: string; col2: string; col3: string; col4: number; status: string; }
export const SEED_DATA: Item[] = [
  { id: "1", col1: "0082341001", col2: "Ahmad Fauzi", col3: "X-A (Fase E)", col4: 98.4, status: "Terverifikasi" },
  { id: "2", col1: "0082341002", col2: "Siti Rahma Nurhaliza", col3: "X-A (Fase E)", col4: 100.0, status: "Terverifikasi" },
  { id: "3", col1: "0082341003", col2: "Budi Santoso", col3: "X-B (Fase E)", col4: 94.2, status: "Terverifikasi" },
  { id: "4", col1: "0082341004", col2: "Dewi Lestari", col3: "XI-MIPA 1", col4: 96.8, status: "Terverifikasi" },
  { id: "5", col1: "0082341005", col2: "Rizky Pratama", col3: "XI-MIPA 2", col4: 91.5, status: "Terverifikasi" }
];"""
    },
    "saas": {
        "title": "Autonomous Systems Control Plane",
        "tag": "Cluster Telemetry · Region ap-southeast-3",
        "h1": "High-Throughput Operational Control Plane.",
        "desc": "Distributed workflow orchestration, real-time telemetry tracing, and automated policy verification across cloud clusters.",
        "cta1": "Launch Workbench",
        "cta2": "View Cluster Topology",
        "metric_label": "Active Nodes",
        "metric_value": "48 Workers",
        "table_heading": "Cluster Workspace Registry",
        "table_sub": "Live node status and p95 inference latency across active execution pools.",
        "cols": ["Worker ID", "Cluster Node", "Assigned Domain", "p95 Latency", "Health"],
        "data_ts": """export interface Item { id: string; col1: string; col2: string; col3: string; col4: number; status: string; }
export const SEED_DATA: Item[] = [
  { id: "1", col1: "node-01a", col2: "api-gateway-prod", col3: "Ingress / Edge", col4: 4.2, status: "Healthy" },
  { id: "2", col1: "node-02b", col2: "model-router-v3", col3: "Inference Stream", col4: 12.8, status: "Healthy" },
  { id: "3", col1: "node-03c", col2: "db-replica-sg", col3: "Data Outbox", col4: 2.1, status: "Healthy" },
  { id: "4", col1: "node-04d", col2: "agent-coordinator", col3: "Swarm Bus", col4: 8.5, status: "Healthy" }
];"""
    },
    "ledger": {
        "title": "Enterprise Settlement & Cashier Ledger",
        "tag": "Fiscal Year 2026 · Daily Clearing Cycle",
        "h1": "High-Density Financial Settlement Matrix.",
        "desc": "Double-entry transactional ledger, automated multi-channel payment reconciliation, and real-time cashier balance journal.",
        "cta1": "Open Cashier Journal",
        "cta2": "Export Audit Proof",
        "metric_label": "Settled Today",
        "metric_value": "Rp 42.850.000",
        "table_heading": "Reconciled Transaction Journal",
        "table_sub": "Audited journal entries with cryptographic receipt signature verification.",
        "cols": ["Journal Ref", "Counterparty / Account", "Category", "Amount (IDR)", "Audit Status"],
        "data_ts": """export interface Item { id: string; col1: string; col2: string; col3: string; col4: number; status: string; }
export const SEED_DATA: Item[] = [
  { id: "1", col1: "JRN-8801", col2: "BCA Virtual Account", col3: "SPP Semester Gasal", col4: 1250000, status: "Settled" },
  { id: "2", col1: "JRN-8802", col2: "Mandiri Bill Payment", col3: "Registrasi Ujian CBT", col4: 350000, status: "Settled" },
  { id: "3", col1: "JRN-8803", col2: "QRIS Dinamis POS", col3: "Kantin Digital", col4: 45000, status: "Settled" },
  { id: "4", col1: "JRN-8804", col2: "BNI Direct Transfer", col3: "Laboratorium Komputer", col4: 2500000, status: "Settled" }
];"""
    }
}


def generate_page_tsx(d: dict) -> str:
    template = """\"use client\";

import * as React from "react";
import { ArrowRight, Clock, ShieldCheck } from "lucide-react";
import { SlidingPillNav } from "@/components/ui/SlidingPillNav";
import { HoldToConfirmButton } from "@/components/ui/HoldToConfirmButton";
import { SEED_DATA } from "@/lib/data";

export default function HomePage() {
  const [activeTab, setActiveTab] = React.useState("all");

  const tabs = [
    { id: "all", label: "Semua Entitas" },
    { id: "verified", label: "Terverifikasi" },
    { id: "review", label: "Menunggu Audit" },
  ];

  return (
    <main className="min-h-screen flex flex-col">
      <header className="border-b border-border/80 bg-surface/50 backdrop-blur-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <span className="font-semibold text-sm tracking-tight">{TITLE}</span>
            <span className="text-xs text-muted font-mono px-2 py-0.5 rounded bg-surface-elevated border border-border">v1.0</span>
          </div>
          <div className="flex items-center gap-3 text-xs text-muted">
            <span className="font-mono tabular-nums">{METRIC_LABEL}: {METRIC_VALUE}</span>
            <span className="w-1 h-1 rounded-full bg-border" />
            <span className="text-emerald-400 font-medium">Sistem Normal</span>
          </div>
        </div>
      </header>

      <section className="relative overflow-hidden border-b border-border/80 bg-surface/30 py-16 sm:py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          <div className="lg:col-span-7 flex flex-col items-start text-left">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-elevated border border-border text-xs text-muted mb-6">
              <span className="w-2 h-2 rounded-full bg-accent" />
              <span>{TAG}</span>
            </div>
            <h1 className="text-3xl sm:text-5xl font-bold tracking-tight text-foreground text-balance leading-[1.1]">
              {H1}
            </h1>
            <p className="mt-6 text-base sm:text-lg text-muted max-w-xl text-pretty leading-relaxed">
              {DESC}
            </p>
            <div className="mt-8 flex flex-wrap items-center gap-4">
              <button className="h-11 px-6 rounded-lg bg-accent text-accent-foreground font-medium text-sm flex items-center gap-2 hover:opacity-90 transition-opacity shadow-sm">
                <span>{CTA1}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
              <HoldToConfirmButton onConfirm={() => alert("Tindakan terkonfirmasi.")} label="{CTA2}" />
            </div>
          </div>

          <div className="lg:col-span-5 w-full">
            <div className="rounded-2xl border border-border bg-surface p-6 shadow-xl">
              <div className="flex items-center justify-between pb-4 border-b border-border mb-4">
                <div className="flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4 text-accent" />
                  <span className="text-xs font-semibold text-foreground">Status Operasional Aktif</span>
                </div>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Live</span>
              </div>
              <div className="space-y-3">
                <div className="p-3 rounded-lg bg-surface-elevated border border-border flex items-center justify-between">
                  <span className="text-xs text-muted">Beban Pemrosesan</span>
                  <span className="text-xs font-mono tabular-nums text-foreground">12.4% Optimal</span>
                </div>
                <div className="p-3 rounded-lg bg-surface-elevated border border-border flex items-center justify-between">
                  <span className="text-xs text-muted">Integritas Transaksi</span>
                  <span className="text-xs font-mono tabular-nums text-emerald-400">100% Lolos Audit</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-4 sm:px-6 py-12 w-full">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-lg font-semibold tracking-tight text-foreground">{TABLE_HEADING}</h2>
            <p className="text-xs text-muted mt-0.5">{TABLE_SUB}</p>
          </div>
          <SlidingPillNav tabs={tabs} activeId={activeTab} onChange={setActiveTab} />
        </div>

        <div className="rounded-xl border border-border bg-surface overflow-hidden">
          <table className="w-full text-left text-sm">
            <thead className="bg-surface-elevated/50 border-b border-border text-xs text-muted">
              <tr>
                <th className="py-3 px-4 font-medium">{COL0}</th>
                <th className="py-3 px-4 font-medium">{COL1}</th>
                <th className="py-3 px-4 font-medium">{COL2}</th>
                <th className="py-3 px-4 font-medium text-right">{COL3}</th>
                <th className="py-3 px-4 font-medium text-right">{COL4}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/60">
              {SEED_DATA.map((row) => (
                <tr key={row.id} className="hover:bg-surface-elevated/30 transition-colors">
                  <td className="py-3 px-4 font-mono text-xs text-muted">{row.col1}</td>
                  <td className="py-3 px-4 font-medium text-foreground">{row.col2}</td>
                  <td className="py-3 px-4 text-xs text-muted">{row.col3}</td>
                  <td className="py-3 px-4 text-xs font-mono tabular-nums text-right text-foreground">
                    {typeof row.col4 === "number" ? row.col4.toLocaleString("id-ID") : row.col4}
                  </td>
                  <td className="py-3 px-4 text-right">
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                      {row.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
"""
    return (
        template.replace("{TITLE}", d["title"])
        .replace("{METRIC_LABEL}", d["metric_label"])
        .replace("{METRIC_VALUE}", d["metric_value"])
        .replace("{TAG}", d["tag"])
        .replace("{H1}", d["h1"])
        .replace("{DESC}", d["desc"])
        .replace("{CTA1}", d["cta1"])
        .replace("{CTA2}", d["cta2"])
        .replace("{TABLE_HEADING}", d["table_heading"])
        .replace("{TABLE_SUB}", d["table_sub"])
        .replace("{COL0}", d["cols"][0])
        .replace("{COL1}", d["cols"][1])
        .replace("{COL2}", d["cols"][2])
        .replace("{COL3}", d["cols"][3])
        .replace("{COL4}", d["cols"][4])
    )


# --- PHP TEMPLATES ---

PHP_INDEX = """<?php
declare(strict_types=1);

header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization");
header("Content-Type: application/json; charset=UTF-8");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

require_once __DIR__ . '/config/db.php';

$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$path = preg_replace('#^/api#', '', $path);
$method = $_SERVER['REQUEST_METHOD'];

function jsonResponse(mixed $data, int $status = 200): void {
    http_response_code($status);
    echo json_encode(['status' => $status, 'data' => $data], JSON_UNESCAPED_UNICODE);
    exit;
}

if ($path === '/items' && $method === 'GET') {
    $db = getDB();
    $stmt = $db->query("SELECT * FROM items ORDER BY id ASC");
    jsonResponse($stmt->fetchAll(PDO::FETCH_ASSOC));
} elseif ($path === '/health' && $method === 'GET') {
    jsonResponse(['status' => 'operational', 'engine' => 'PHP 8+ WAL SQLite', 'p95_latency_ms' => 3.8]);
} else {
    jsonResponse(['error' => 'Endpoint not found'], 404);
}
"""

PHP_DB = """<?php
declare(strict_types=1);

function getDB(): PDO {
    static $pdo = null;
    if ($pdo === null) {
        $dbPath = __DIR__ . '/../database.sqlite';
        $pdo = new PDO("sqlite:" . $dbPath);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // WAL mode for high concurrency
        $pdo->exec("PRAGMA journal_mode = WAL; PRAGMA busy_timeout = 5000;");

        // Auto-migration
        $pdo->exec("
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                metric REAL NOT NULL DEFAULT 0.0,
                status TEXT NOT NULL DEFAULT 'Active',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ");

        // Seed if empty
        $count = (int)$pdo->query("SELECT COUNT(*) FROM items")->fetchColumn();
        if ($count === 0) {
            $stmt = $pdo->prepare("INSERT INTO items (code, name, category, metric, status) VALUES (?, ?, ?, ?, ?)");
            $seeds = [
                ['REC-001', 'Ahmad Fauzi / Settlement Alpha', 'Primary', 98.4, 'Verified'],
                ['REC-002', 'Siti Rahma / Node Cluster Beta', 'Secondary', 100.0, 'Verified'],
                ['REC-003', 'Budi Santoso / Clearing Gamma', 'Operational', 94.2, 'Verified']
            ];
            foreach ($seeds as $s) {
                $stmt->execute($s);
            }
        }
    }
    return $pdo;
}
"""

# --- GAS TEMPLATES ---

GAS_CODE_GS = """function doGet(e) {
  return HtmlService.createTemplateFromFile('index')
    .evaluate()
    .setTitle('{title}')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function apiGetItems() {
  return {
    success: true,
    data: [
      { code: "REC-001", name: "Alpha Entity", category: "Core", metric: 98.4, status: "Active" },
      { code: "REC-002", name: "Beta Entity", category: "Auxiliary", metric: 100.0, status: "Active" },
      { code: "REC-003", name: "Gamma Entity", category: "Ledger", metric: 94.2, status: "Active" }
    ]
  };
}
"""

GAS_INDEX_HTML = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    // PLACEHOLDER theme so the starter runs: maxilun-craft replaces it from the Craft Brief.
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            background: '#090a0f',
            surface: '#12151e',
            'surface-elevated': '#1a1f2c',
            border: 'rgba(255, 255, 255, 0.08)',
            accent: '#3b82f6',
            muted: '#94a3b8'
          }
        }
      }
    }
  </script>
  <style>
    @media (prefers-reduced-motion: reduce) {
      *, ::before, ::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
    }
    :focus-visible { outline: 2px solid #3b82f6; outline-offset: 2px; }
  </style>
</head>
<body class="bg-background text-neutral-100 min-h-screen font-sans antialiased">
  <header class="border-b border-border/80 bg-surface/50 backdrop-blur-md sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
        <span class="font-semibold text-sm tracking-tight">{title}</span>
        <span class="text-xs text-muted font-mono px-2 py-0.5 rounded bg-surface-elevated border border-border">GAS WebApp</span>
      </div>
      <div class="text-xs text-muted font-mono">100% Serverless Google Sheets</div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 py-12">
    <div class="rounded-2xl border border-border bg-surface p-8 mb-8">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-elevated border border-border text-xs text-muted mb-4">
        <span class="w-2 h-2 rounded-full bg-accent"></span>
        <span>Semester Gasal 2026/2027</span>
      </div>
      <h1 class="text-3xl sm:text-4xl font-bold tracking-tight text-white mb-4">Portal Operasional Terpadu</h1>
      <p class="text-muted text-sm sm:text-base max-w-2xl leading-relaxed">
        Aplikasi terhubung langsung dengan basis data Google Spreadsheet instansi.
      </p>
    </div>

    <div class="rounded-xl border border-border bg-surface overflow-hidden">
      <div class="p-4 border-b border-border flex items-center justify-between">
        <h2 class="text-sm font-semibold text-white">Daftar Data Terverifikasi</h2>
        <span class="text-xs text-muted font-mono">Live Sync</span>
      </div>
      <div id="data-table" class="p-4 text-xs text-muted">Memuat data...</div>
    </div>
  </main>

  <script>
    function renderItems(items) {
      var html = '<table class="w-full text-left">';
      html += '<thead class="border-b border-border text-muted pb-2"><tr><th class="py-2">Kode</th><th>Nama Entitas</th><th>Kategori</th><th class="text-right">Metrik</th><th class="text-right">Status</th></tr></thead><tbody class="divide-y divide-border/60">';
      items.forEach(function(s) {
        html += '<tr class="hover:bg-surface-elevated/40"><td class="py-2.5 font-mono">' + s.code + '</td><td class="font-medium text-white">' + s.name + '</td><td>' + s.category + '</td><td class="text-right font-mono">' + s.metric + '</td><td class="text-right"><span class="text-emerald-400 font-medium">' + s.status + '</span></td></tr>';
      });
      html += '</tbody></table>';
      document.getElementById('data-table').innerHTML = html;
    }

    if (typeof google !== 'undefined' && google.script && google.script.run) {
      google.script.run.withSuccessHandler(function(res) {
        if (res && res.success) renderItems(res.data);
      }).apiGetItems();
    } else {
      setTimeout(function() {
        renderItems([
          { code: "REC-001", name: "Ahmad Fauzi", category: "Core", metric: 98.4, status: "Terverifikasi" },
          { code: "REC-002", name: "Siti Rahma", category: "Core", metric: 100.0, status: "Terverifikasi" },
          { code: "REC-003", name: "Budi Santoso", category: "Auxiliary", metric: 94.2, status: "Terverifikasi" }
        ]);
      }, 100);
    }
  </script>
</body>
</html>
"""

GAS_LOCAL_PREVIEW = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>Offline Preview Runner</title>
</head>
<body style="margin: 0; padding: 0; background: #090a0f;">
  <iframe src="index.html" style="width: 100vw; height: 100vh; border: none;"></iframe>
</body>
</html>
"""

GAS_MANIFEST = """{
  "timeZone": "Asia/Jakarta",
  "dependencies": {},
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "webapp": {
    "executeAs": "USER_DEPLOYING",
    "access": "ANYONE"
  }
}
"""


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")


def scaffold_nextjs(target: Path, name: str, title: str, domain: str = "edtech"):
    d = DOMAINS.get(domain, DOMAINS["edtech"])
    display_title = title if title and title != "EduCore Platform" else d["title"]

    write_file(target / "package.json", NEXTJS_PACKAGE_JSON.replace("{name}", name))
    write_file(target / "tailwind.config.ts", NEXTJS_TAILWIND_CONFIG)
    write_file(target / "app" / "globals.css", NEXTJS_GLOBALS_CSS)
    write_file(target / "app" / "layout.tsx", NEXTJS_LAYOUT.replace("{title}", display_title))
    write_file(target / "app" / "page.tsx", generate_page_tsx(d))
    write_file(target / "lib" / "data.ts", d["data_ts"])

    # Physical Motion Primitives
    write_file(target / "components" / "ui" / "SlidingPillNav.tsx", SLIDING_PILL_NAV)
    write_file(target / "components" / "ui" / "HoldToConfirmButton.tsx", HOLD_TO_CONFIRM_BTN)


def scaffold_vite_php(target: Path, name: str, title: str, domain: str = "edtech"):
    d = DOMAINS.get(domain, DOMAINS["edtech"])
    display_title = title if title and title != "EduCore Platform" else d["title"]

    # Frontend
    fe = target / "frontend"
    write_file(fe / "package.json", NEXTJS_PACKAGE_JSON.replace("{name}", f"{name}-frontend"))
    page_tsx = generate_page_tsx(d).replace("@/components", "./components").replace("@/lib", "./lib")
    write_file(fe / "src" / "App.tsx", page_tsx)
    write_file(fe / "src" / "index.css", NEXTJS_GLOBALS_CSS)
    write_file(fe / "src" / "lib" / "data.ts", d["data_ts"])
    write_file(fe / "src" / "components" / "ui" / "SlidingPillNav.tsx", SLIDING_PILL_NAV)
    write_file(fe / "src" / "components" / "ui" / "HoldToConfirmButton.tsx", HOLD_TO_CONFIRM_BTN)

    # Backend
    api = target / "api"
    write_file(api / "index.php", PHP_INDEX)
    write_file(api / "config" / "db.php", PHP_DB)


def scaffold_gas(target: Path, name: str, title: str, domain: str = "edtech"):
    d = DOMAINS.get(domain, DOMAINS["edtech"])
    display_title = title if title and title != "EduCore Platform" else d["title"]

    write_file(target / "Code.gs", GAS_CODE_GS.replace("{title}", display_title))
    write_file(target / "index.html", GAS_INDEX_HTML.replace("{title}", display_title))
    write_file(target / "local_preview.html", GAS_LOCAL_PREVIEW)
    write_file(target / "appsscript.json", GAS_MANIFEST)


def main():
    parser = argparse.ArgumentParser(description="Maxilun Greenfield Project Scaffold Generator")
    parser.add_argument("target", nargs="?", default=".", help="Target project root directory")
    parser.add_argument("--stack", choices=["nextjs", "vite-php", "gas"], default="nextjs", help="Technology stack")
    parser.add_argument("--domain", choices=["edtech", "saas", "ledger"], default="edtech", help="Domain archetype")
    parser.add_argument("--name", default="my-app", help="Project slug name")
    parser.add_argument("--title", default="EduCore Platform", help="Human-readable project title")
    args = parser.parse_args()

    target_dir = Path(args.target).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"🚀 Maxilun Greenfield Generator: Initializing '{args.name}' ({args.stack} · domain: {args.domain})...")

    if args.stack == "nextjs":
        scaffold_nextjs(target_dir, args.name, args.title, domain=args.domain)
    elif args.stack == "vite-php":
        scaffold_vite_php(target_dir, args.name, args.title, domain=args.domain)
    elif args.stack == "gas":
        scaffold_gas(target_dir, args.name, args.title, domain=args.domain)

    print(f"✅ Greenfield project structure generated successfully at: {target_dir}")
    print("\nNext Steps:")
    if args.stack == "nextjs":
        print(f"  cd {target_dir.name} && npm install && npm run dev")
    elif args.stack == "vite-php":
        print("  Terminal 1: php -S localhost:8000 -t api")
        print(f"  Terminal 2: cd frontend && npm install && npm run dev")
    elif args.stack == "gas":
        print("  1. Double-click local_preview.html to test offline in browser")
        print("  2. Deploy Code.gs & index.html to script.google.com")
    print("\nDesign is NOT done: the colours, hero, and layout are placeholders shared by every starter.")
    print("  Run maxilun-craft next: write the Brief, replace the token block and hero, and look at the result with")
    print("  python <maxilun-craft>/scripts/render.py <page-or-url>")


if __name__ == "__main__":
    main()
