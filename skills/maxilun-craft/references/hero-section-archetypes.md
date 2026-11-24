# Hero Section Archetypes: First-Fold Conversion & Art Direction

> **Status**: Reference Document (Mandatory Load for Landing Page, First-Fold & UI Redesign)  
> **Specialists**: `maxilun-craft`, `maxilun-motion`, & `maxilun-content`  
> **Source Attribution**: Synthesized from First Fold architectures (`first-fold.pages.dev`) and Framer Motion React Orchestration (`sami12344/framer-motion`, see `CREDITS.md`)

The First Fold (the viewport area visible without scrolling) dictates over 80% of landing page and portal engagement. Generic AI hero layouts—centered headline (`LAY-018`), floating `rounded-full` pill tagline capsule (`CMP-015`), gray subtext, and twin competing solid buttons (`LAY-010`)—fail the 3-second comprehension test. This guide binds every product domain to an asymmetric, interactive First-Fold Hero architecture.

---

## 1. The 5-Element Hero Anatomy (Slop-Free Invariant)

Every First-Fold hero section must compose these five structural layers in an **asymmetric start-aligned or 7:5 / 6:6 split layout** (never a monotonous centered stack `LAY-018`):

```
[1. Unbordered Editorial Eyebrow + Semantic Status Dot (NO rounded-full pill capsule CMP-015)]
[2. Hook Headline (Max 8-10 Words, -0.03em Tracking, text-wrap: balance)]
[3. Concrete Subheadline (Outcome-Driven, 2 Sentences Max, max-w-[60ch])]
[4. Action Cluster: ONE Primary Solid CTA + Secondary Outline/Link Action (LAY-010)]
[5. Interactive Centerpiece (Living Workbench / Live Academic Ledger / 3D Perspective Preview)]
──────────────────────────────────────────────────────────────────────────────────────────────
[Verified Operational Strip: Tabular Metrics (tabular-nums) or Authentic Institutional Context]
```

### The Three-Second Conversion Rules
1. **Pass the "So What?" Test**: Within 3 seconds, a visitor must immediately see what the system operates on, for whom, and can interact with the centerpiece right in the first fold.
2. **Zero Jargon & Zero Pill Taglines (`CMP-015`)**: Never stamp a bordered `rounded-full` pill badge above the `<h1>`. Use an unbordered monospace/editorial eyebrow (`flex items-center gap-2 text-xs font-mono`).
3. **Living Interactive Centerpiece**: The right column (or lower workbench deck) MUST contain stateful micro-interactions from `../../maxilun-motion/references/ui-motion-recipes.md` (e.g. `SlidingPillNav`, `DraggableWorkbenchCard`, `PerspectiveCard`, or live filterable rows), never a dead static box.

---

## 2. Canonical Domain Hero Archetypes (`domain-recipe-matrix.md` Binding)

Every project or redesign MUST declare and implement one of these 5 canonical IDs:

### `HERO-EDTECH-01`: Asymmetric Split-Screen Live Academic Ledger
- **Target Domain**: EdTech, School Portals, CBT Exam Systems, Academic LMS, University Administration.
- **Visual Motif**: Warm Academic Editorial (`oklch(0.97 0.01 75)` warm paper or deep stone-900 workbench), unbordered institutional eyebrow (`NPSN / Node ID`), serif/display headline paired with monospace `tabular-nums`.
- **Interactive Centerpiece**: Live Academic & CBT Session Workbench right in the first fold—featuring a **Sliding Pill Session Switcher** (`Sesi Aktif`, `Cek NISN`, `Rekap KKTP`), interactive student/exam filtering, and expandable row details.

### `HERO-SAAS-02`: Asymmetric Command Workbench
- **Target Domain**: B2B SaaS, Multi-Tenant Operations, HRIS, ERP, Project Workbenches.
- **Visual Motif**: Asymmetric 12-column split (6 columns value proposition / 6 columns interactive dual-pane telemetry workbench) on an Obsidian or Technical Stone surface ramp.
- **Interactive Centerpiece**: Interactive telemetry card with **Framer Motion `when: "beforeChildren"` staggered metrics**, bounded draggable inspector pod (`dragConstraints`), and live range switcher.

### `HERO-LEDGER-03`: High-Density Tabular Masthead
- **Target Domain**: Administrative Portals, Financial Ledgers, Cashier / POS, Treasury, Public Sector Data.
- **Visual Motif**: Technical Swiss Ledger aesthetic (`1px solid var(--border)` hairline grid, zero decorative cards, high-contrast neutral ink on crisp paper).
- **Interactive Centerpiece**: Live reconciliation matrix with `AnimatedFilterChips`, instant `CounterOdometer` totals (`tabular-nums`), and keyboard-accessible row inspection.

### `HERO-COMMERCE-04`: Tangible Showcase Deck
- **Target Domain**: E-Commerce, School Store, Equipment Booking, Hardware Catalogs.
- **Visual Motif**: Tactile studio surface with high-contrast spot accent and physical depth.
- **Interactive Centerpiece**: `PerspectiveCard` 3D tilt showcase with mouse-following specular spotlight (`--mouse-x`, `--mouse-y`), interactive variant/package selector, and instant stock availability dot.

### `HERO-DEVTOOLS-05`: Dark Atmospheric Terminal Sandbox
- **Target Domain**: Developer Tools, AI Agent Workbenches, API Gateways, Infrastructure CLI/SDKs.
- **Visual Motif**: Deep charcoal (`oklch(0.11 0.01 265)`), razor-sharp monospace metadata tracks, zero fake 3D particle meshes (`CMP-016`).
- **Interactive Centerpiece**: Interactive command/prompt preset switcher that streams deterministic AST/execution trace lines with `tabular-nums` latency metrics.

---

## 3. Blueprint A (`HERO-EDTECH-01`): Split-Screen Live Academic & CBT Ledger Hero

Zero-dependency React + Tailwind blueprint (with CSS spring micro-interactions, sliding tab indicator, interactive session lookup, and cursor spotlight—passes `slopscan.py` with 0 errors):

```tsx
"use client";

import * as React from "react";

interface ExamSessionRow {
  code: string;
  subject: string;
  grade: string;
  participants: number;
  completionRate: string;
  room: string;
}

const SESSIONS: Record<"pagi" | "siang" | "susulan", ExamSessionRow[]> = {
  pagi: [
    { code: "CBT-MAT-12A", subject: "Matematika Peminatan", grade: "XII MIPA 1", participants: 36, completionRate: "94.4%", room: "Lab CBT 01" },
    { code: "CBT-FIS-11B", subject: "Fisika Mekanika", grade: "XI MIPA 2", participants: 34, completionRate: "88.2%", room: "Lab CBT 02" },
    { code: "CBT-BIN-10A", subject: "Literasi Bahasa Indonesia", grade: "X Reguler A", participants: 35, completionRate: "100%", room: "Lab CBT 03" },
  ],
  siang: [
    { code: "CBT-BIO-12B", subject: "Biologi Molekuler", grade: "XII MIPA 2", participants: 35, completionRate: "91.4%", room: "Lab CBT 01" },
    { code: "CBT-EKO-11A", subject: "Ekonomi Makro & Akuntansi", grade: "XI IPS 1", participants: 32, completionRate: "87.5%", room: "Lab CBT 02" },
  ],
  susulan: [
    { code: "CBT-KIM-12S", subject: "Kimia Larutan Penyangga", grade: "XII MIPA Gabungan", participants: 8, completionRate: "100%", room: "Ruang Pengawas" },
  ],
};

export function EdTechAcademicLedgerHero() {
  const [activeTab, setActiveTab] = React.useState<"pagi" | "siang" | "susulan">("pagi");
  const [selectedCode, setSelectedCode] = React.useState<string>("CBT-MAT-12A");
  const [spotlight, setSpotlight] = React.useState({ x: 240, y: 120, active: false });

  const tabs: { id: "pagi" | "siang" | "susulan"; label: string; time: string }[] = [
    { id: "pagi", label: "Sesi 01 Pagi", time: "07:30 WIB" },
    { id: "siang", label: "Sesi 02 Siang", time: "10:30 WIB" },
    { id: "susulan", label: "Sesi Susulan", time: "13:30 WIB" },
  ];
  const activeIdx = tabs.findIndex((t) => t.id === activeTab);
  const rows = SESSIONS[activeTab];

  return (
    <section className="relative overflow-hidden bg-stone-950 text-stone-100 py-16 md:py-24 border-b border-stone-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-8 items-start">
          {/* Left Column (6 cols): Editorial Value Proposition */}
          <div className="lg:col-span-6 flex flex-col items-start text-left">
            {/* 1. Unbordered Editorial Eyebrow (No rounded-full pill CMP-015) */}
            <div className="flex items-center gap-2.5 text-xs font-mono text-stone-400 mb-4">
              <span className="w-2 h-2 rounded-sm bg-emerald-500" />
              <span>NPSN 20102941 &bull; Semester Genap 2026/2027 &bull; Sinkron Dapodik</span>
            </div>

            {/* 2. Hook Headline */}
            <h1 className="text-3xl sm:text-5xl lg:text-6xl font-semibold tracking-tight text-stone-100 text-balance leading-[1.08] mb-5">
              Kendali asesmen sekolah dan buku induk dalam satu meja kerja.
            </h1>

            {/* 3. Concrete Subheadline */}
            <p className="text-base sm:text-lg text-stone-300 max-w-[58ch] mb-8">
              Pantau lembar jawaban CBT secara langsung, validasi capaian KKTP per rombel, dan cetak rapor Kurikulum Merdeka tanpa berpindah aplikasi.
            </p>

            {/* 4. Action Cluster (One Primary Solid CTA + One Secondary Outline CTA) */}
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full sm:w-auto mb-8">
              <button
                type="button"
                className="px-6 py-3 rounded-lg bg-emerald-600 text-stone-950 font-semibold text-sm hover:bg-emerald-500 active:scale-[0.97] transition-transform duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400"
              >
                Buka Ruang Pengawas CBT
              </button>
              <button
                type="button"
                className="px-5 py-3 rounded-lg border border-stone-800 bg-stone-900/70 text-stone-200 font-medium text-sm hover:border-stone-700 active:scale-[0.98] transition-transform duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-stone-500"
              >
                Periksa Jadwal &amp; Token Rombel
              </button>
            </div>

            {/* Verified Institutional Metrics Strip */}
            <dl className="grid grid-cols-3 gap-6 pt-6 border-t border-stone-800/90 w-full">
              <div>
                <dt className="text-xs font-mono text-stone-400">Peserta Terdaftar</dt>
                <dd className="text-xl sm:text-2xl font-mono tabular-nums font-semibold text-stone-100 mt-1">
                  1.420
                </dd>
              </div>
              <div>
                <dt className="text-xs font-mono text-stone-400">Rombel Aktif</dt>
                <dd className="text-xl sm:text-2xl font-mono tabular-nums font-semibold text-stone-100 mt-1">
                  42 Kelas
                </dd>
              </div>
              <div>
                <dt className="text-xs font-mono text-stone-400">Latensi Lokal</dt>
                <dd className="text-xl sm:text-2xl font-mono tabular-nums font-semibold text-emerald-400 mt-1">
                  14 ms
                </dd>
              </div>
            </dl>
          </div>

          {/* Right Column (6 cols): Living Interactive Academic Ledger Centerpiece */}
          <div className="lg:col-span-6">
            <div
              onMouseMove={(e) => {
                const rect = e.currentTarget.getBoundingClientRect();
                setSpotlight({
                  x: e.clientX - rect.left,
                  y: e.clientY - rect.top,
                  active: true,
                });
              }}
              onMouseLeave={() => setSpotlight((s) => ({ ...s, active: false }))}
              className="relative overflow-hidden rounded-xl border border-stone-800 bg-stone-900/80 p-5"
            >
              {/* Specular Cursor Spotlight */}
              <div
                aria-hidden="true"
                className="pointer-events-none absolute inset-0 transition-opacity duration-200"
                style={{
                  opacity: spotlight.active ? 1 : 0,
                  background: `radial-gradient(380px circle at ${spotlight.x}px ${spotlight.y}px, rgba(16, 185, 129, 0.08), transparent 70%)`,
                }}
              />

              <div className="relative z-10">
                {/* Workbench Header */}
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pb-4 border-b border-stone-800">
                  <div>
                    <span className="text-xs font-mono text-stone-400 block">
                      Monitor Sesi Ujian Langsung
                    </span>
                    <h2 className="text-sm font-semibold text-stone-100">
                      Status Sinkronisasi Ruang CBT
                    </h2>
                  </div>

                  {/* Micro-Interaction 1: Sliding Segmented Control */}
                  <div
                    role="tablist"
                    aria-label="Pilih Sesi Ujian"
                    className="relative grid grid-cols-3 p-1 rounded-lg bg-stone-950 border border-stone-800"
                  >
                    <span
                      aria-hidden="true"
                      style={{
                        transform: `translate3d(${activeIdx * 100}%, 0, 0)`,
                        transition: "transform 220ms cubic-bezier(0.16, 1, 0.3, 1)",
                      }}
                      className="pointer-events-none absolute inset-y-1 left-1 w-[calc((100%-8px)/3)] rounded-md bg-stone-800 border border-stone-700"
                    />
                    {tabs.map((tab) => (
                      <button
                        key={tab.id}
                        role="tab"
                        type="button"
                        aria-selected={activeTab === tab.id}
                        onClick={() => {
                          setActiveTab(tab.id);
                          setSelectedCode(SESSIONS[tab.id][0].code);
                        }}
                        className={`relative z-10 px-2.5 py-1 text-xs font-medium transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 ${
                          activeTab === tab.id ? "text-stone-100" : "text-stone-400 hover:text-stone-200"
                        }`}
                      >
                        {tab.label}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Micro-Interaction 2: Interactive Session Ledger Rows */}
                <div className="divide-y divide-stone-800/80 my-3">
                  {rows.map((row) => {
                    const isSelected = row.code === selectedCode;
                    return (
                      <button
                        key={row.code}
                        type="button"
                        onClick={() => setSelectedCode(row.code)}
                        className={`w-full py-3 px-3 text-left rounded-lg transition-colors duration-150 flex items-center justify-between gap-3 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 ${
                          isSelected ? "bg-stone-800/70" : "hover:bg-stone-800/30"
                        }`}
                      >
                        <div className="min-w-0">
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-mono text-emerald-400">{row.code}</span>
                            <span className="text-xs font-mono text-stone-400">&bull; {row.room}</span>
                          </div>
                          <p className="text-sm font-medium text-stone-100 truncate mt-0.5">
                            {row.subject} ({row.grade})
                          </p>
                        </div>
                        <div className="text-right shrink-0">
                          <span className="text-sm font-mono tabular-nums font-semibold text-stone-100 block">
                            {row.completionRate}
                          </span>
                          <span className="text-xs font-mono tabular-nums text-stone-400">
                            {row.participants} peserta
                          </span>
                        </div>
                      </button>
                    );
                  })}
                </div>

                {/* Micro-Interaction 3: Live Inspector Footer */}
                <div className="pt-3 border-t border-stone-800 flex items-center justify-between text-xs font-mono text-stone-400">
                  <span>Kode Aktif: {selectedCode}</span>
                  <span className="text-emerald-400 tabular-nums">
                    Pengawas Terhubung &bull; 0 Anomali
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
```

---

## 4. Blueprint B (`HERO-SAAS-02`): Framer Motion Orchestrated Command Workbench Hero

Integrates the 6 Framer Motion mechanics synthesized from `sami12344/framer-motion` (`variants` with `when: "beforeChildren"` parent-child stagger, `custom={index}`, bounded `dragConstraints` on the interactive centerpiece pod, `layoutId` sliding mode switcher, and `useReducedMotion()` guard):

```tsx
"use client";

import * as React from "react";
import { motion, useReducedMotion, Variants } from "framer-motion";

const heroContainerVariants: Variants = {
  hidden: { opacity: 0, y: 14 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.3,
      ease: [0.16, 1, 0.3, 1],
      when: "beforeChildren",
      staggerChildren: 0.06,
    },
  },
};

const heroChildVariants: Variants = {
  hidden: { opacity: 0, y: 12 },
  visible: (index: number) => ({
    opacity: 1,
    y: 0,
    transition: {
      type: "spring",
      stiffness: 340,
      damping: 28,
      delay: index * 0.04,
    },
  }),
};

export function SaaSWorkbenchHero() {
  const reduced = useReducedMotion();
  const [mode, setMode] = React.useState<"trace" | "latency" | "policy">("trace");

  return (
    <section className="relative overflow-hidden pt-20 pb-20 md:pt-28 md:pb-24 bg-neutral-950 text-neutral-100 border-b border-neutral-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          variants={heroContainerVariants}
          initial={reduced ? "visible" : "hidden"}
          animate="visible"
          className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center"
        >
          {/* Left Column: Staggered Value Proposition */}
          <div className="lg:col-span-6 flex flex-col items-start text-left">
            <motion.div
              variants={heroChildVariants}
              custom={0}
              className="flex items-center gap-2 text-xs font-mono text-neutral-400 mb-5"
            >
              <span className="w-2 h-2 rounded-sm bg-emerald-400" />
              <span>Release v2.4 &bull; Zero-Downtime Expand-Contract Engine</span>
            </motion.div>

            <motion.h1
              variants={heroChildVariants}
              custom={1}
              className="text-3xl sm:text-5xl lg:text-6xl font-semibold tracking-tight text-neutral-100 text-balance mb-5"
            >
              Audit struktur produksi tanpa membebani latensi layanan.
            </motion.h1>

            <motion.p
              variants={heroChildVariants}
              custom={2}
              className="text-base sm:text-lg text-neutral-300 max-w-[58ch] mb-8"
            >
              Lacak blast radius pemanggil fungsi lewat grafik AST, deteksi kebocoran memori sebelum rilis, dan verifikasi setiap perubahan secara deterministik.
            </motion.p>

            <motion.div
              variants={heroChildVariants}
              custom={3}
              className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full sm:w-auto mb-6"
            >
              <motion.button
                type="button"
                whileTap={{ scale: 0.97 }}
                className="px-6 py-3 rounded-lg bg-neutral-100 text-neutral-950 font-semibold text-sm hover:bg-white transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400"
              >
                Jalankan Inspeksi Repositori
              </motion.button>
              <motion.button
                type="button"
                whileTap={{ scale: 0.98 }}
                className="px-5 py-3 rounded-lg border border-neutral-800 bg-neutral-900/60 text-neutral-200 font-medium text-sm hover:border-neutral-700 transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-500"
              >
                Buka Dokumentasi Kontrak API
              </motion.button>
            </motion.div>
          </div>

          {/* Right Column: Interactive Centerpiece with layoutId Switcher & Bounded Drag */}
          <motion.div variants={heroChildVariants} custom={4} className="lg:col-span-6">
            <div className="rounded-xl border border-neutral-800 bg-neutral-900/80 p-5">
              <div className="flex items-center justify-between pb-3 border-b border-neutral-800 mb-4">
                <span className="text-xs font-mono text-neutral-400">live-telemetry.ts</span>
                <div className="inline-flex p-1 rounded-lg bg-neutral-950 border border-neutral-800">
                  {(["trace", "latency", "policy"] as const).map((item) => (
                    <button
                      key={item}
                      type="button"
                      onClick={() => setMode(item)}
                      className={`relative px-3 py-1 text-xs font-mono rounded-md transition-colors duration-150 ${
                        mode === item ? "text-neutral-100" : "text-neutral-400 hover:text-neutral-200"
                      }`}
                    >
                      {mode === item && (
                        <motion.span
                          layoutId="hero-mode-pill"
                          transition={{ type: "spring", stiffness: 380, damping: 30 }}
                          className="absolute inset-0 rounded-md bg-neutral-800 border border-neutral-700"
                        />
                      )}
                      <span className="relative z-10">{item}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Draggable Interactive Telemetry Pod */}
              <motion.div
                drag={!reduced}
                dragConstraints={{ left: -16, right: 16, top: -12, bottom: 12 }}
                dragElastic={0.12}
                whileTap={{ scale: 0.99 }}
                className="cursor-grab active:cursor-grabbing rounded-lg bg-neutral-950/80 border border-neutral-800/80 p-4 font-mono text-xs text-neutral-300 space-y-2.5 select-none"
              >
                <div className="flex items-center justify-between text-emerald-400">
                  <span>Graph AST parsed (drag to inspect)</span>
                  <span className="tabular-nums">2.410 symbols</span>
                </div>
                <div className="flex items-center justify-between text-neutral-300">
                  <span>Mode aktif: {mode.toUpperCase()}</span>
                  <span className="tabular-nums">0 cycles detected</span>
                </div>
                <div className="flex items-center justify-between text-neutral-400 pt-2 border-t border-neutral-900">
                  <span>P95 Latency: 12 ms</span>
                  <span className="text-emerald-400 tabular-nums">Coverage: 98.4%</span>
                </div>
              </motion.div>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
```
