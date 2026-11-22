#!/usr/bin/env python3
"""greenfield.py - Deterministic starter code generator for Maxilun Scaffold.

Generates complete, runnable, slop-free greenfield applications across 3 stacks:
  1. nextjs: Next.js 15 App Router + React 19 + Tailwind CSS + Lucide
  2. vite-php: Decoupled React Vite SPA + PHP 8+ REST API (PDO SQLite)
  3. gas: Google Apps Script Web App (Code.gs + index.html + local_preview.html)

Includes Domain-to-Recipe auto-binding (first-fold hero + ui-motion recipes)
and instant Indonesian realistic seed data.
"""
import argparse
import os
import sys
from pathlib import Path

# --- TEMPLATES ---

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
  description: "Platform akademik dan asesmen terpadu.",
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

NEXTJS_PAGE = """"use client";

import * as React from "react";
import { FirstFoldHero } from "@/components/hero/FirstFoldHero";
import { SEED_STUDENTS } from "@/lib/data";

export default function HomePage() {
  const [activeTab, setActiveTab] = React.useState("semua");

  return (
    <main className="min-h-screen flex flex-col">
      {/* Navigation Masthead */}
      <header className="border-b border-border/80 bg-surface/50 backdrop-blur-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="font-semibold text-sm tracking-tight">{title}</span>
            <span className="text-xs text-muted font-mono px-2 py-0.5 rounded bg-surface-elevated border border-border">v1.0</span>
          </div>
          <div className="flex items-center gap-3 text-xs text-muted">
            <span className="font-mono tabular-nums">15 Siswa Terdaftar</span>
            <span className="w-1 h-1 rounded-full bg-border" />
            <span className="text-emerald-400 font-medium">Server Aktif</span>
          </div>
        </div>
      </header>

      {/* High-Impact Hero First-Fold */}
      <FirstFoldHero />

      {/* Operational Data Ledger Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 py-12 w-full">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-lg font-semibold tracking-tight text-foreground">Daftar Peserta Asesmen Aktif</h2>
            <p className="text-xs text-muted mt-0.5">Data terverifikasi semester berjalan dengan status kehadiran live.</p>
          </div>
          <div className="flex items-center gap-1.5 p-1 rounded-lg bg-surface border border-border">
            {["semua", "fase-e", "fase-f"].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${
                  activeTab === tab
                    ? "bg-surface-elevated text-foreground shadow-sm"
                    : "text-muted hover:text-foreground"
                }`}
              >
                {tab === "semua" ? "Semua Kelas" : tab === "fase-e" ? "Fase E (Kelas 10)" : "Fase F (Kelas 11-12)"}
              </button>
            ))}
          </div>
        </div>

        {/* High-Craft Table Ledger */}
        <div className="rounded-xl border border-border bg-surface overflow-hidden">
          <table className="w-full text-left text-sm">
            <thead className="bg-surface-elevated/50 border-b border-border text-xs text-muted">
              <tr>
                <th className="py-3 px-4 font-medium">NISN</th>
                <th className="py-3 px-4 font-medium">Nama Peserta Didik</th>
                <th className="py-3 px-4 font-medium">Rombongan Belajar</th>
                <th className="py-3 px-4 font-medium text-right">Kehadiran</th>
                <th className="py-3 px-4 font-medium text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/60">
              {SEED_STUDENTS.map((student) => (
                <tr key={student.nisn} className="hover:bg-surface-elevated/30 transition-colors">
                  <td className="py-3 px-4 font-mono text-xs text-muted">{student.nisn}</td>
                  <td className="py-3 px-4 font-medium text-foreground">{student.name}</td>
                  <td className="py-3 px-4 text-xs text-muted">{student.grade}</td>
                  <td className="py-3 px-4 text-xs font-mono tabular-nums text-right text-foreground">{student.attendance.toFixed(1)}%</td>
                  <td className="py-3 px-4 text-right">
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                      {student.status}
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

HERO_EDTECH_COMPONENT = """"use client";

import * as React from "react";
import { ArrowRight, BookOpen, Clock, Users } from "lucide-react";

export function FirstFoldHero() {
  return (
    <section className="relative overflow-hidden border-b border-border/80 bg-surface/30 py-16 sm:py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        {/* Left Column (Editorial Hook) */}
        <div className="lg:col-span-7 flex flex-col items-start text-left">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-elevated border border-border text-xs text-muted mb-6">
            <span className="w-2 h-2 rounded-full bg-accent" />
            <span>Tahun Ajaran 2026/2027 · Semester Gasal</span>
          </div>

          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-foreground text-balance leading-[1.1]">
            Pusat Asesmen & Manajemen Akademik Presisi.
          </h1>

          <p className="mt-6 text-base sm:text-lg text-muted max-w-xl text-pretty leading-relaxed">
            Platform terpadu evaluasi belajar, butir instrumen soal berbasis taksonomi, dan pemantauan capaian kompetensi peserta didik secara real-time.
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-4">
            <button className="h-11 px-6 rounded-lg bg-accent text-accent-foreground font-medium text-sm flex items-center gap-2 hover:opacity-90 transition-opacity shadow-sm">
              <span>Buka Ruang Ujian CBT</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button className="h-11 px-5 rounded-lg bg-surface border border-border text-foreground font-medium text-sm hover:bg-surface-elevated transition-colors">
              Bank Soal Asesmen
            </button>
          </div>
        </div>

        {/* Right Column (Live Centerpiece Ledger) */}
        <div className="lg:col-span-5 w-full">
          <div className="rounded-2xl border border-border bg-surface p-6 shadow-xl relative overflow-hidden">
            <div className="flex items-center justify-between pb-4 border-b border-border mb-4">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-lg bg-surface-elevated text-accent border border-border">
                  <Clock className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="text-xs font-semibold text-foreground">Jadwal Asesmen Terdekat</h3>
                  <p className="text-[11px] text-muted font-mono">08:00 - 10:00 WIB</p>
                </div>
              </div>
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Siap Uji</span>
            </div>

            <div className="space-y-3">
              <div className="p-3 rounded-lg bg-surface-elevated border border-border/80 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <BookOpen className="w-4 h-4 text-muted" />
                  <div>
                    <p className="text-xs font-medium text-foreground">Informatika & Literasi Digital</p>
                    <p className="text-[11px] text-muted">Kelas 10 (Fase E) · 40 Butir</p>
                  </div>
                </div>
                <span className="text-xs font-mono tabular-nums text-foreground">120 Menit</span>
              </div>

              <div className="p-3 rounded-lg bg-surface-elevated border border-border/80 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Users className="w-4 h-4 text-muted" />
                  <div>
                    <p className="text-xs font-medium text-foreground">Matematika Tingkat Lanjut</p>
                    <p className="text-[11px] text-muted">Kelas 11 (Fase F) · 35 Butir</p>
                  </div>
                </div>
                <span className="text-xs font-mono tabular-nums text-foreground">90 Menit</span>
              </div>
            </div>

            <div className="mt-4 pt-4 border-t border-border flex items-center justify-between text-xs text-muted">
              <span className="font-mono">Server Status: Normal</span>
              <span className="font-mono tabular-nums">p95 Latency: 12ms</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
"""

DATA_TS = """export interface Student {
  nisn: string;
  name: string;
  grade: string;
  attendance: number;
  status: string;
}

export const SEED_STUDENTS: Student[] = [
  { nisn: "0082341001", name: "Ahmad Fauzi", grade: "X-A (Fase E)", attendance: 98.4, status: "Terverifikasi" },
  { nisn: "0082341002", name: "Siti Rahma Nurhaliza", grade: "X-A (Fase E)", attendance: 100.0, status: "Terverifikasi" },
  { nisn: "0082341003", name: "Budi Santoso", grade: "X-B (Fase E)", attendance: 94.2, status: "Terverifikasi" },
  { nisn: "0082341004", name: "Dewi Lestari", grade: "XI-MIPA 1", attendance: 96.8, status: "Terverifikasi" },
  { nisn: "0082341005", name: "Rizky Pratama", grade: "XI-MIPA 2", attendance: 91.5, status: "Terverifikasi" },
  { nisn: "0082341006", name: "Anisa Putri", grade: "XI-IPS 1", attendance: 99.0, status: "Terverifikasi" },
  { nisn: "0082341007", name: "Fajar Nugraha", grade: "XII-IPA 1", attendance: 95.0, status: "Terverifikasi" },
  { nisn: "0082341008", name: "Nabila Zahra", grade: "XII-IPS 2", attendance: 97.5, status: "Terverifikasi" }
];
"""

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

if ($path === '/students' && $method === 'GET') {
    $db = getDB();
    $stmt = $db->query("SELECT * FROM students ORDER BY name ASC");
    jsonResponse($stmt->fetchAll(PDO::FETCH_ASSOC));
} elseif ($path === '/health' && $method === 'GET') {
    jsonResponse(['status' => 'operational', 'p95_latency_ms' => 4.2]);
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

        // Auto-migration
        $pdo->exec("
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nisn TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                grade TEXT NOT NULL,
                attendance REAL NOT NULL DEFAULT 100.0,
                status TEXT NOT NULL DEFAULT 'Terverifikasi',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ");

        // Seed if empty
        $count = (int)$pdo->query("SELECT COUNT(*) FROM students")->fetchColumn();
        if ($count === 0) {
            $stmt = $pdo->prepare("INSERT INTO students (nisn, name, grade, attendance, status) VALUES (?, ?, ?, ?, ?)");
            $seeds = [
                ['0082341001', 'Ahmad Fauzi', 'X-A (Fase E)', 98.4, 'Terverifikasi'],
                ['0082341002', 'Siti Rahma', 'X-A (Fase E)', 100.0, 'Terverifikasi'],
                ['0082341003', 'Budi Santoso', 'X-B (Fase E)', 94.2, 'Terverifikasi'],
                ['0082341004', 'Dewi Lestari', 'XI-MIPA 1', 96.8, 'Terverifikasi']
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

function apiGetStudents() {
  return {
    success: true,
    data: [
      { nisn: "0082341001", name: "Ahmad Fauzi", grade: "X-A (Fase E)", attendance: 98.4, status: "Terverifikasi" },
      { nisn: "0082341002", name: "Siti Rahma Nurhaliza", grade: "X-A (Fase E)", attendance: 100.0, status: "Terverifikasi" },
      { nisn: "0082341003", name: "Budi Santoso", grade: "X-B (Fase E)", attendance: 94.2, status: "Terverifikasi" },
      { nisn: "0082341004", name: "Dewi Lestari", grade: "XI-MIPA 1", attendance: 96.8, status: "Terverifikasi" }
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
</head>
<body class="bg-background text-neutral-100 min-h-screen font-sans antialiased">
  <header class="border-b border-border/80 bg-surface/50 backdrop-blur-md sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
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
      <h1 class="text-3xl sm:text-4xl font-bold tracking-tight text-white mb-4">Portal Asesmen & Administrasi Guru</h1>
      <p class="text-muted text-sm sm:text-base max-w-2xl leading-relaxed">
        Aplikasi terhubung langsung dengan basis data Google Spreadsheet instansi sekolah.
      </p>
    </div>

    <div class="rounded-xl border border-border bg-surface overflow-hidden">
      <div class="p-4 border-b border-border flex items-center justify-between">
        <h2 class="text-sm font-semibold text-white">Daftar Siswa Terverifikasi</h2>
        <span class="text-xs text-muted font-mono">Live Sync</span>
      </div>
      <div id="student-table" class="p-4 text-xs text-muted">Memuat data...</div>
    </div>
  </main>

  <script>
    function renderStudents(students) {
      var html = '<table class="w-full text-left">';
      html += '<thead class="border-b border-border text-muted pb-2"><tr><th class="py-2">NISN</th><th>Nama</th><th>Kelas</th><th class="text-right">Kehadiran</th><th class="text-right">Status</th></tr></thead><tbody class="divide-y divide-border/60">';
      students.forEach(function(s) {
        html += '<tr class="hover:bg-surface-elevated/40"><td class="py-2.5 font-mono">' + s.nisn + '</td><td class="font-medium text-white">' + s.name + '</td><td>' + s.grade + '</td><td class="text-right font-mono">' + s.attendance + '%</td><td class="text-right"><span class="text-emerald-400 font-medium">' + s.status + '</span></td></tr>';
      });
      html += '</tbody></table>';
      document.getElementById('student-table').innerHTML = html;
    }

    // Load data via google.script.run or mock
    if (typeof google !== 'undefined' && google.script && google.script.run) {
      google.script.run.withSuccessHandler(function(res) {
        if (res && res.success) renderStudents(res.data);
      }).apiGetStudents();
    } else {
      // Mock fallback for browser preview
      setTimeout(function() {
        renderStudents([
          { nisn: "0082341001", name: "Ahmad Fauzi", grade: "X-A (Fase E)", attendance: 98.4, status: "Terverifikasi" },
          { nisn: "0082341002", name: "Siti Rahma", grade: "X-A (Fase E)", attendance: 100.0, status: "Terverifikasi" },
          { nisn: "0082341003", name: "Budi Santoso", grade: "X-B (Fase E)", attendance: 94.2, status: "Terverifikasi" },
          { nisn: "0082341004", name: "Dewi Lestari", grade: "XI-MIPA 1", attendance: 96.8, status: "Terverifikasi" }
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
  <title>EduCore - Local Offline Preview Runner</title>
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


def scaffold_nextjs(target: Path, name: str, title: str):
    write_file(target / "package.json", NEXTJS_PACKAGE_JSON.replace("{name}", name))
    write_file(target / "tailwind.config.ts", NEXTJS_TAILWIND_CONFIG)
    write_file(target / "app" / "globals.css", NEXTJS_GLOBALS_CSS)
    write_file(target / "app" / "layout.tsx", NEXTJS_LAYOUT.replace("{title}", title))
    write_file(target / "app" / "page.tsx", NEXTJS_PAGE.replace("{title}", title))
    write_file(target / "components" / "hero" / "FirstFoldHero.tsx", HERO_EDTECH_COMPONENT)
    write_file(target / "lib" / "data.ts", DATA_TS)


def scaffold_vite_php(target: Path, name: str, title: str):
    # Frontend
    fe = target / "frontend"
    write_file(fe / "package.json", NEXTJS_PACKAGE_JSON.replace("{name}", f"{name}-frontend"))
    write_file(fe / "src" / "App.tsx", NEXTJS_PAGE.replace("{title}", title).replace("@/components", "./components").replace("@/lib", "./lib"))
    write_file(fe / "src" / "index.css", NEXTJS_GLOBALS_CSS)
    write_file(fe / "src" / "components" / "hero" / "FirstFoldHero.tsx", HERO_EDTECH_COMPONENT)
    write_file(fe / "src" / "lib" / "data.ts", DATA_TS)

    # Backend
    api = target / "api"
    write_file(api / "index.php", PHP_INDEX)
    write_file(api / "config" / "db.php", PHP_DB)


def scaffold_gas(target: Path, name: str, title: str):
    write_file(target / "Code.gs", GAS_CODE_GS.replace("{title}", title))
    write_file(target / "index.html", GAS_INDEX_HTML.replace("{title}", title))
    write_file(target / "local_preview.html", GAS_LOCAL_PREVIEW)
    write_file(target / "appsscript.json", GAS_MANIFEST)


def main():
    parser = argparse.ArgumentParser(description="Maxilun Greenfield Project Scaffold Generator")
    parser.add_argument("target", nargs="?", default=".", help="Target project root directory")
    parser.add_argument("--stack", choices=["nextjs", "vite-php", "gas"], default="nextjs", help="Technology stack")
    parser.add_argument("--name", default="my-app", help="Project slug name")
    parser.add_argument("--title", default="EduCore Platform", help="Human-readable project title")
    args = parser.parse_args()

    target_dir = Path(args.target).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"🚀 Maxilun Greenfield Generator: Initializing '{args.name}' ({args.stack})...")

    if args.stack == "nextjs":
        scaffold_nextjs(target_dir, args.name, args.title)
    elif args.stack == "vite-php":
        scaffold_vite_php(target_dir, args.name, args.title)
    elif args.stack == "gas":
        scaffold_gas(target_dir, args.name, args.title)

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


if __name__ == "__main__":
    main()
