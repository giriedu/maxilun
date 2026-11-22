# Bento Dashboard Recipes: Production Asymmetric Grid Standards

Operational blueprint for `maxilun-craft`, `maxilun-frontend`, and `maxilun-ui-designer`. Replaces generic AI dashboard slop (the symmetrical 4/5-card KPI strip `LAY-017`, the white-box admin monoculture `LAY-014`, and decorative pill badge proliferation `CMP-022`) with battle-tested, high-craft Asymmetric Bento Grids.

---

## 1. Anatomy of an Anti-Symmetric Bento Grid

```
+-------------------------------------------------------------------------+
| DOMAIN MASTHEAD (School/Org Name, Active Term, Real Sync Heartbeat Dot) |
+------------------------------------+------------------------------------+
| SPOTLIGHT HERO CARD (8 cols)       | QUICK ACTION & STATUS DECK (4 cols)|
| - Primary Operational Chart (SVG)   | - Borderless Action List           |
| - Filterable Metric Range          | - System Health & Node Metrics     |
| - High-contrast Tabular Header     | - Compact Sparkline Tracker        |
+------------------------------------+------------------------------------+
| REAL-TIME ACTIVITY LEDGER (8 cols) | ASYMMETRIC METRIC POD (4 cols)     |
| - Borderless row list              | - Stacked primary numbers          |
| - Tabular timestamps               | - Contextual delta (vs reference)  |
| - Monospace IDs, no card-in-card   | - Zero decorative pill capsules    |
+------------------------------------+------------------------------------+
```

### The 5 Structural Invariants
1. **Asymmetric 8:4 or 7:5 Ratio**: Never slice the top row into 4 or 5 identical cards (`grid-cols-4` or `grid-cols-5`). The primary metric/trend receives a dominant 8-column Spotlight anchor with real visual data (AreaChart/BarChart).
2. **Zero Decorative Pill Proliferation (`CMP-022`)**: Ban scattering 10+ `rounded-full` pills across the viewport (`[LIVE]`, `[HOST]`, `[AI]`, `[VALID]`). Status is conveyed by plain monochrome typography or a single `w-1.5 h-1.5` green/amber dot with text label.
3. **Deep Surface Hierarchy (Anti-White Box `LAY-014`)**: Do not dump white `#ffffff` boxes on `#f8fafc`. Use a calibrated 3-step surface ramp (`bg-surface-base`, `bg-surface-elevated`, `bg-surface-subtle`) with `1px` neutral hairline borders (`oklch(0 0 0 / 0.08)` or `oklch(1 0 0 / 0.08)`).
4. **Tabular Numerals & Monospace Metadata**: Every metric, percentage, score, and timestamp must carry `tabular-nums font-mono` to prevent layout shaking during live stream updates.
5. **No Card Inside a Card**: Use spatial rhythm ($2\times$ spacing) and subtle border dividers instead of nesting card containers.

---

## 2. Complete React + Tailwind Component Recipe

```tsx
import React, { useState } from 'react';

// Types
interface ActivityItem {
  id: string;
  candidateName: string;
  examTitle: string;
  timestamp: string;
  score: number;
  status: 'submitted' | 'in_progress' | 'flagged';
}

interface MetricSummary {
  label: string;
  value: string;
  reference: string;
  delta: string;
  trend: 'up' | 'neutral' | 'down';
}

export function EduCoreDashboardView() {
  const [selectedRange, setSelectedRange] = useState<'today' | '7d' | '30d'>('7d');

  // Authentic mock data
  const activities: ActivityItem[] = [
    { id: 'SES-9482', candidateName: 'Ahmad Dahlan', examTitle: 'Matematika Peminatan XII', timestamp: '10:42:15', score: 88, status: 'submitted' },
    { id: 'SES-9481', candidateName: 'Siti Nurhaliza', examTitle: 'Biologi Asesmen Akhir', timestamp: '10:41:02', score: 74, status: 'submitted' },
    { id: 'SES-9480', candidateName: 'Budi Santoso', examTitle: 'Fisika Kuantum Dasar', timestamp: '10:39:48', score: 92, status: 'submitted' },
    { id: 'SES-9479', candidateName: 'Dewi Lestari', examTitle: 'Bahasa Indonesia Literasi', timestamp: '10:35:10', score: 68, status: 'flagged' },
    { id: 'SES-9478', candidateName: 'Eko Prasetyo', examTitle: 'Kimia Larutan Penyangga', timestamp: '10:30:22', score: 81, status: 'submitted' },
  ];

  const metrics: MetricSummary[] = [
    { label: 'Peserta Ujian Aktif', value: '1,420', reference: 'Kapasitas 1,600', delta: '+12%', trend: 'up' },
    { label: 'Rata-Rata Daya Serap', value: '78.4', reference: 'KKTP Minimal 75.0', delta: '+3.4 pt', trend: 'up' },
    { label: 'Integritas Ujian CBT', value: '99.8%', reference: '3 anomali ditinjau', delta: 'Stabil', trend: 'neutral' },
  ];

  return (
    <div className="w-full max-w-[1440px] mx-auto p-4 sm:p-6 lg:p-8 space-y-6 bg-stone-900 text-stone-100 min-h-screen">
      
      {/* 1. DOMAIN MASTHEAD (No fake breadcrumbs HDR-001, no floating pills CMP-015) */}
      <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-6 border-b border-stone-800">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-xs font-mono uppercase tracking-wider text-stone-400">SMA Negeri 1 EduCore Jakarta &bull; Node ID: CBT-JKT-01</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight text-stone-100 mt-1">
            Pusat Kendali Asesmen & Administrasi
          </h1>
          <p className="text-sm text-stone-400 mt-0.5">
            Tahun Ajaran 2024/2025 Genap &bull; Penilaian Berbasis Komputer & Bank Soal Kurikulum Merdeka
          </p>
        </div>

        {/* Primary Action + Context Controls */}
        <div className="flex items-center gap-3">
          <div className="inline-flex rounded-lg bg-stone-800 p-0.5 border border-stone-700">
            {(['today', '7d', '30d'] as const).map((rng) => (
              <button
                key={rng}
                onClick={() => setSelectedRange(rng)}
                className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                  selectedRange === rng
                    ? 'bg-stone-700 text-stone-100 shadow-sm'
                    : 'text-stone-400 hover:text-stone-200'
                }`}
              >
                {rng === 'today' ? 'Hari Ini' : rng === '7d' ? '7 Hari' : '30 Hari'}
              </button>
            ))}
          </div>

          <button className="px-4 py-2 text-xs font-medium rounded-lg bg-emerald-600 hover:bg-emerald-500 text-stone-950 font-semibold transition-colors">
            + Buat Jadwal Asesmen
          </button>
        </div>
      </header>

      {/* 2. THE ASYMMETRIC BENTO GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* === CARD 1: THE SPOTLIGHT HERO (8 cols) === */}
        <section className="lg:col-span-8 rounded-xl bg-stone-800/60 border border-stone-800 p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-start justify-between">
              <div>
                <span className="text-xs font-mono uppercase text-stone-400">Throughput Ujian Real-Time</span>
                <div className="flex items-baseline gap-3 mt-1">
                  <span className="text-4xl font-semibold font-mono tabular-nums text-stone-100">8,429</span>
                  <span className="text-xs font-mono text-emerald-400 font-medium">+14.2% dibanding sesi kemarin</span>
                </div>
              </div>
              <div className="text-right">
                <span className="text-xs font-mono text-stone-400">Latensi P95 Server</span>
                <p className="text-sm font-mono tabular-nums text-stone-200 font-medium">18ms &bull; HTTP/2 Keepalive</p>
              </div>
            </div>

            {/* REAL SVG AREACHART (No fake canvas, no neon glow CMP-019) */}
            <div className="mt-8 h-48 w-full relative">
              <svg viewBox="0 0 600 160" className="w-full h-full overflow-visible" preserveAspectRatio="none">
                <defs>
                  <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#10b981" stopOpacity="0.25" />
                    <stop offset="100%" stopColor="#10b981" stopOpacity="0.0" />
                  </linearGradient>
                </defs>
                {/* Horizontal reference grid lines */}
                <line x1="0" y1="40" x2="600" y2="40" stroke="#292524" strokeDasharray="3 3" />
                <line x1="0" y1="80" x2="600" y2="80" stroke="#292524" strokeDasharray="3 3" />
                <line x1="0" y1="120" x2="600" y2="120" stroke="#292524" strokeDasharray="3 3" />
                
                {/* Area fill */}
                <path
                  d="M0,140 Q60,110 120,125 T240,70 T360,95 T480,45 T600,60 L600,160 L0,160 Z"
                  fill="url(#areaGradient)"
                />
                {/* Main stroke line */}
                <path
                  d="M0,140 Q60,110 120,125 T240,70 T360,95 T480,45 T600,60"
                  fill="none"
                  stroke="#10b981"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
                {/* Interactive Anchor Points */}
                <circle cx="240" cy="70" r="3.5" fill="#10b981" />
                <circle cx="480" cy="45" r="3.5" fill="#10b981" />
              </svg>
            </div>
          </div>

          <div className="flex items-center justify-between pt-4 mt-4 border-t border-stone-800 text-xs font-mono text-stone-400">
            <span>Sesi 01 (07:30)</span>
            <span>Sesi 02 (10:00 - Puncak)</span>
            <span>Sesi 03 (13:00)</span>
            <span>Sesi 04 (15:30)</span>
          </div>
        </section>

        {/* === CARD 2: QUICK ACTION & OPERATIONAL DECK (4 cols) === */}
        <section className="lg:col-span-4 rounded-xl bg-stone-800/60 border border-stone-800 p-6 flex flex-col justify-between">
          <div>
            <h2 className="text-sm font-semibold text-stone-200 tracking-tight">Tindakan Cepat & Telemetri</h2>
            <p className="text-xs text-stone-400 mt-0.5">Operasional pengawas ruang ujian</p>

            <ul className="mt-4 space-y-2">
              {[
                { label: 'Sinkronisasi Lembar Jawaban', desc: '48 paket antrean lokal', action: 'Kirim' },
                { label: 'Rilis Kunci Token Sesi 02', desc: 'Valid untuk 40 menit', action: 'Buka' },
                { label: 'Cetak Berita Acara Ujian', desc: '14 ruang asesmen', action: 'Unduh' },
              ].map((act, i) => (
                <li key={i} className="flex items-center justify-between p-3 rounded-lg bg-stone-900/60 border border-stone-800/80 hover:border-stone-700 transition-colors">
                  <div>
                    <span className="text-xs font-medium text-stone-200 block">{act.label}</span>
                    <span className="text-[11px] font-mono text-stone-400">{act.desc}</span>
                  </div>
                  <button className="px-2.5 py-1 text-xs font-mono rounded bg-stone-800 hover:bg-stone-700 text-stone-300 border border-stone-700 transition-colors">
                    {act.action}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Node Health Status */}
          <div className="mt-6 pt-4 border-t border-stone-800 flex items-center justify-between text-xs font-mono">
            <span className="text-stone-400">Node Sync: Normal</span>
            <span className="text-emerald-400 tabular-nums">0 Sesi Gagal</span>
          </div>
        </section>

        {/* === CARD 3: REAL-TIME ACTIVITY LEDGER (8 cols) === */}
        <section className="lg:col-span-8 rounded-xl bg-stone-800/60 border border-stone-800 p-6">
          <div className="flex items-center justify-between pb-4 border-b border-stone-800">
            <div>
              <h2 className="text-sm font-semibold text-stone-200 tracking-tight">Log Aktivitas Peserta Ujian</h2>
              <p className="text-xs text-stone-400 mt-0.5">Aliran pengiriman lembar jawaban sesi aktif</p>
            </div>
            <span className="text-xs font-mono text-stone-400">Real-Time Polling &bull; 5 detik</span>
          </div>

          {/* Borderless Ledger Rows (Anti Card-in-Card LAY-001) */}
          <div className="divide-y divide-stone-800/80 mt-2">
            {activities.map((act) => (
              <div key={act.id} className="py-3 flex items-center justify-between text-xs hover:bg-stone-800/40 px-2 rounded transition-colors">
                <div className="flex items-center gap-3">
                  <span className="font-mono text-stone-400 text-[11px]">{act.id}</span>
                  <div>
                    <span className="font-medium text-stone-200">{act.candidateName}</span>
                    <span className="text-stone-400 ml-2 hidden sm:inline">&bull; {act.examTitle}</span>
                  </div>
                </div>

                <div className="flex items-center gap-6">
                  <span className="font-mono tabular-nums text-stone-400 hidden md:inline">{act.timestamp}</span>
                  <div className="text-right">
                    <span className="font-mono tabular-nums font-semibold text-stone-100">{act.score}</span>
                    <span className="text-[10px] text-stone-400 block sm:inline sm:ml-1">/ 100</span>
                  </div>
                  <span
                    className={`text-[11px] font-mono font-medium ${
                      act.status === 'submitted'
                        ? 'text-emerald-400'
                        : act.status === 'flagged'
                        ? 'text-amber-400'
                        : 'text-stone-400'
                    }`}
                  >
                    {act.status === 'submitted' ? 'Valid' : act.status === 'flagged' ? 'Anomali' : 'Berjalan'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* === CARD 4: ASYMMETRIC METRIC SUMMARY POD (4 cols) === */}
        <section className="lg:col-span-4 rounded-xl bg-stone-800/60 border border-stone-800 p-6 flex flex-col justify-between">
          <div>
            <h2 className="text-sm font-semibold text-stone-200 tracking-tight">Ringkasan Metrik Kunci</h2>
            <p className="text-xs text-stone-400 mt-0.5">Indikator kinerja pedagogis</p>

            <div className="mt-4 space-y-4">
              {metrics.map((m, idx) => (
                <div key={idx} className="p-4 rounded-lg bg-stone-900/60 border border-stone-800/80">
                  <span className="text-xs text-stone-400 block">{m.label}</span>
                  <div className="flex items-baseline justify-between mt-1">
                    <span className="text-2xl font-semibold font-mono tabular-nums text-stone-100">{m.value}</span>
                    <span className="text-xs font-mono font-medium text-emerald-400">{m.delta}</span>
                  </div>
                  <span className="text-[11px] font-mono text-stone-400 mt-1 block">{m.reference}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-4 border-t border-stone-800 mt-4 text-[11px] font-mono text-stone-400">
            Sumber Data: Kurikulum Merdeka Engine v1.3
          </div>
        </section>

      </div>
    </div>
  );
}
```

---

## 3. Light-Mode Technical Swiss Ledger Variant

When designing light-theme dashboards for school administration, health clinics, or enterprise legal portals, never use raw `#ffffff` boxes on `#f1f5f9`. Deploy the **Technical Swiss Ledger Archetype**:

```html
<!-- Light-Theme Swiss Technical Ledger Shell -->
<div class="w-full bg-[#fcfbf9] text-[#1c1917] p-8 font-sans">
  <!-- Masthead -->
  <header class="flex justify-between items-baseline border-b border-[#e7e5e4] pb-4 mb-8">
    <div>
      <span class="text-xs font-mono uppercase tracking-widest text-[#78716c]">Arsip & Evaluasi Asesmen</span>
      <h1 class="text-2xl font-serif text-[#1c1917] mt-1">SMA Negeri 1 EduCore Jakarta</h1>
    </div>
    <div class="text-xs font-mono tabular-nums text-[#78716c]">
      2024/2025 &bull; Semester Genap
    </div>
  </header>

  <!-- 8:4 Grid -->
  <div class="grid grid-cols-12 gap-8">
    <div class="col-span-12 lg:col-span-8 space-y-6">
      <!-- Spotlight Table (Not generic cards) -->
      <div class="border border-[#e7e5e4] bg-[#fafaf9] rounded-lg p-6">
        <h2 class="text-base font-medium text-[#1c1917] mb-4">Distribusi Capaian Kompetensi (KKTP: 75.0)</h2>
        <!-- Ledger Table with tabular-nums -->
        <table class="w-full text-xs font-mono">
          <thead>
            <tr class="border-b border-[#e7e5e4] text-[#78716c] text-left">
              <th class="pb-2 font-normal">Mata Pelajaran</th>
              <th class="pb-2 font-normal text-right">Peserta</th>
              <th class="pb-2 font-normal text-right">Rata-Rata</th>
              <th class="pb-2 font-normal text-right">Ketuntasan</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-[#f5f5f4]">
            <tr>
              <td class="py-2.5 font-sans font-medium">Matematika Peminatan</td>
              <td class="py-2.5 text-right tabular-nums">318</td>
              <td class="py-2.5 text-right tabular-nums font-semibold">81.4</td>
              <td class="py-2.5 text-right tabular-nums text-emerald-700">92.4%</td>
            </tr>
            <tr>
              <td class="py-2.5 font-sans font-medium">Fisika Dasar</td>
              <td class="py-2.5 text-right tabular-nums">312</td>
              <td class="py-2.5 text-right tabular-nums font-semibold">76.8</td>
              <td class="py-2.5 text-right tabular-nums text-emerald-700">84.2%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Asymmetric Rail -->
    <div class="col-span-12 lg:col-span-4 border border-[#e7e5e4] bg-[#fafaf9] rounded-lg p-6">
      <h3 class="text-xs font-mono uppercase tracking-wider text-[#78716c]">Antrean Pengawas Aktif</h3>
      <!-- Rail List -->
      <ul class="divide-y divide-[#e7e5e4] mt-4 text-xs">
        <li class="py-3 flex justify-between">
          <span>Ruang CBT Lab 01</span>
          <span class="font-mono text-emerald-700">Terhubung</span>
        </li>
        <li class="py-3 flex justify-between">
          <span>Ruang CBT Lab 02</span>
          <span class="font-mono text-emerald-700">Terhubung</span>
        </li>
      </ul>
    </div>
  </div>
</div>
```

---

## 4. Mechanical Review Checklist for Dashboards
- [ ] Are KPI metrics presented in an asymmetric grid ($8:4$ or $7:5$) rather than a symmetrical $4/5$ card strip?
- [ ] Is there an AreaChart, BarChart, or Operational Table taking up the primary Spotlight area?
- [ ] Are all numbers, timestamps, and percentages formatted with `tabular-nums`?
- [ ] Are decorative pill badges (`rounded-full`) restricted to $\le 2$ functional status tags per screen?
- [ ] Is the masthead free of fake breadcrumbs (`HDR-001`) and floating pill tagline capsules (`CMP-015`)?

