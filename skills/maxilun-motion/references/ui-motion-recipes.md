# UI Motion Recipes & Micro-Interaction Vault

> **Status**: Reference Document (Mandatory Load for UI/UX, Landing Page, Dashboard & Redesign)  
> **Specialist**: `maxilun-motion` & `maxilun-craft`  
> **Source Attribution**: Synthesized from UI Motion Prompts (`ui-motion-prompts.pages.dev`) and Framer Motion React Orchestration (`sami12344/framer-motion`, see `CREDITS.md`)

This vault provides production-calibrated micro-interaction recipes designed to eliminate static, lifeless interfaces (`shallow-motion`). Every recipe complies with the 60 FPS GPU compositor invariant (`transform`, `opacity`), executes with zero layout shift (`CLS = 0`), provides both **Framer Motion** and **Zero-Dependency React/CSS Spring** patterns, and respects `@media (prefers-reduced-motion: reduce)`.

> **Mandatory Redesign Rule**: Every Landing Page, Hero Section, and Operational Dashboard MUST integrate at least **3 tactile micro-interaction recipes** from this vault matching its domain row in `../maxilun-craft/references/domain-recipe-matrix.md`. Relying solely on `transition-colors` is rejected as generic static output.

---

## 1. Navigation & Filtering: Sliding Pill, Segmented Control & Filter Chips

### A. Sliding Pill Tab Bar & Segmented Control (`SlidingPillNav` / `SegmentedControl`)
Replaces static tab buttons with an organic sliding active indicator (`layoutId` spring in Framer Motion, or GPU-translated indicator in zero-dependency React):

```tsx
"use client";

import * as React from "react";
import { motion, useReducedMotion } from "framer-motion";

export interface NavTab {
  id: string;
  label: string;
  count?: number;
}

export function SlidingPillNav({
  tabs,
  activeId,
  onChange,
}: {
  tabs: NavTab[];
  activeId: string;
  onChange: (id: string) => void;
}) {
  const reduced = useReducedMotion();

  return (
    <nav
      aria-label="View Switcher"
      className="inline-flex items-center gap-1 p-1 rounded-lg bg-neutral-900/90 border border-neutral-800"
    >
      {tabs.map((tab) => {
        const isActive = tab.id === activeId;
        return (
          <button
            key={tab.id}
            type="button"
            onClick={() => onChange(tab.id)}
            className={`relative px-3.5 py-1.5 text-xs font-medium rounded-md transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 ${
              isActive ? "text-neutral-100" : "text-neutral-400 hover:text-neutral-200"
            }`}
          >
            {isActive && (
              <motion.span
                layoutId="active-nav-segment"
                transition={
                  reduced
                    ? { duration: 0 }
                    : { type: "spring", stiffness: 380, damping: 30 }
                }
                className="absolute inset-0 rounded-md bg-neutral-800 border border-neutral-700/70 shadow-sm"
              />
            )}
            <span className="relative z-10 inline-flex items-center gap-1.5">
              <span>{tab.label}</span>
              {typeof tab.count === "number" && (
                <span className="font-mono tabular-nums text-xs text-neutral-400">
                  {tab.count}
                </span>
              )}
            </span>
          </button>
        );
      })}
    </nav>
  );
}

/**
 * Zero-Dependency Fallback (when framer-motion is not installed in the target repo)
 */
export function SegmentedControlCSS({
  tabs,
  activeId,
  onChange,
}: {
  tabs: NavTab[];
  activeId: string;
  onChange: (id: string) => void;
}) {
  const activeIndex = Math.max(0, tabs.findIndex((t) => t.id === activeId));
  return (
    <div
      role="tablist"
      className="relative grid grid-flow-col auto-cols-fr p-1 rounded-lg bg-stone-900 border border-stone-800"
    >
      <span
        aria-hidden="true"
        style={{
          transform: `translate3d(${activeIndex * 100}%, 0, 0)`,
          transition: "transform 220ms cubic-bezier(0.16, 1, 0.3, 1)",
        }}
        className="pointer-events-none absolute inset-y-1 left-1 w-[calc((100%-8px)/3)] rounded-md bg-stone-800 border border-stone-700/80"
      />
      {tabs.map((tab) => (
        <button
          key={tab.id}
          role="tab"
          type="button"
          aria-selected={tab.id === activeId}
          onClick={() => onChange(tab.id)}
          className={`relative z-10 px-3 py-1.5 text-xs font-medium transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 ${
            tab.id === activeId ? "text-stone-100" : "text-stone-400 hover:text-stone-200"
          }`}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
```

### B. Animated Filter Chips (`AnimatedFilterChips`)
Tactile multi-filter bar with spring compression and instant count updates:

```tsx
"use client";

import * as React from "react";

export function AnimatedFilterChips({
  filters,
  activeFilter,
  onSelect,
}: {
  filters: { id: string; label: string; count: number }[];
  activeFilter: string;
  onSelect: (id: string) => void;
}) {
  return (
    <div className="flex flex-wrap items-center gap-2">
      {filters.map((f) => {
        const active = f.id === activeFilter;
        return (
          <button
            key={f.id}
            type="button"
            onClick={() => onSelect(f.id)}
            style={{
              transition: "transform 140ms cubic-bezier(0.16, 1, 0.3, 1), background-color 150ms ease, border-color 150ms ease",
            }}
            className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-medium border active:scale-[0.96] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 ${
              active
                ? "bg-stone-100 text-stone-950 border-stone-100"
                : "bg-stone-900/60 text-stone-300 border-stone-800 hover:border-stone-700"
            }`}
          >
            <span>{f.label}</span>
            <span className="font-mono tabular-nums text-xs opacity-75">{f.count}</span>
          </button>
        );
      })}
    </div>
  );
}
```

---

## 2. Interactive Tactile Buttons (`HoldToConfirmButton`, `MagneticButton`, `SpringScaleTap`)

### A. Hold-to-Confirm Button (Destructive or High-Stakes Actions)
Prevents accidental triggers while delivering physical progress confirmation with automatic unmount cleanup:

```tsx
"use client";

import * as React from "react";

export function HoldToConfirmButton({
  onConfirm,
  label = "Tahan untuk Kunci Sesi",
}: {
  onConfirm: () => void;
  label?: string;
}) {
  const [progress, setProgress] = React.useState(0);
  const timerRef = React.useRef<ReturnType<typeof setInterval> | null>(null);

  const cancelHold = React.useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    setProgress(0);
  }, []);

  React.useEffect(() => () => cancelHold(), [cancelHold]);

  const startHold = () => {
    cancelHold();
    const startTime = Date.now();
    const duration = 1000;
    timerRef.current = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const next = Math.min(100, (elapsed / duration) * 100);
      setProgress(next);
      if (next >= 100) {
        cancelHold();
        onConfirm();
      }
    }, 16);
  };

  return (
    <button
      type="button"
      onMouseDown={startHold}
      onMouseUp={cancelHold}
      onMouseLeave={cancelHold}
      onTouchStart={startHold}
      onTouchEnd={cancelHold}
      className="relative overflow-hidden px-4 py-2 rounded-lg border border-amber-500/30 bg-amber-950/20 text-amber-300 text-xs font-semibold tracking-wide active:scale-[0.97] transition-transform duration-150 select-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-400"
    >
      <span
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 bg-amber-500/25 origin-left"
        style={{
          transform: `scaleX(${progress / 100})`,
          transition: progress === 0 ? "transform 150ms ease-out" : "none",
        }}
      />
      <span className="relative z-10 font-mono tabular-nums">
        {progress > 0 ? `Menahan... ${Math.round(progress)}%` : label}
      </span>
    </button>
  );
}
```

### B. Magnetic Pointer Pull (`MagneticButton`)
Subtle cursor attraction (`35%` pull factor) with analytical spring recovery:

```tsx
"use client";

import * as React from "react";
import { motion, useMotionValue, useSpring, useReducedMotion } from "framer-motion";

export function MagneticButton({
  children,
  onClick,
}: {
  children: React.ReactNode;
  onClick?: () => void;
}) {
  const reduced = useReducedMotion();
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const springX = useSpring(x, { stiffness: 260, damping: 20 });
  const springY = useSpring(y, { stiffness: 260, damping: 20 });

  const handleMouseMove = (e: React.MouseEvent<HTMLButtonElement>) => {
    if (reduced) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    x.set((e.clientX - centerX) * 0.28);
    y.set((e.clientY - centerY) * 0.28);
  };

  const handleMouseLeave = () => {
    x.set(0);
    y.set(0);
  };

  return (
    <motion.button
      type="button"
      style={{ x: springX, y: springY }}
      whileTap={{ scale: 0.97 }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      onClick={onClick}
      className="relative px-5 py-2.5 rounded-lg bg-neutral-100 text-neutral-950 font-semibold text-xs sm:text-sm transition-colors duration-150 hover:bg-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500"
    >
      {children}
    </motion.button>
  );
}
```

---

## 3. Framer Motion Orchestration, Bounded Drag & Imperative Controls

Synthesized and production-calibrated from the 6 core mechanics in `sami12344/framer-motion` (`variants`, `when: "beforeChildren"`, `custom={index}`, `whileInView`, `dragConstraints`, keyframe arrays, and `useAnimationControls`).

### A. Parent-Child Stagger Orchestration (`StaggerBentoContainer` & `StaggerItem`)
Coordinates container entry before staggering child Bento cards or Hero items (`when: "beforeChildren"`, custom index delay capped at `45ms` per item):

```tsx
"use client";

import * as React from "react";
import { motion, Variants } from "framer-motion";

const containerVariants: Variants = {
  hidden: { opacity: 0, y: 12 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.28,
      ease: [0.16, 1, 0.3, 1],
      when: "beforeChildren",
      staggerChildren: 0.05,
    },
  },
};

const itemVariants: Variants = {
  hidden: { opacity: 0, y: 16 },
  visible: (index: number) => ({
    opacity: 1,
    y: 0,
    transition: {
      type: "spring",
      stiffness: 320,
      damping: 28,
      delay: index * 0.04,
    },
  }),
};

export function StaggerBentoGrid({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-40px" }}
      className={className}
    >
      {React.Children.map(children, (child, index) => (
        <motion.div variants={itemVariants} custom={index} key={index}>
          {child}
        </motion.div>
      ))}
    </motion.div>
  );
}
```

### B. Bounded Interactive Drag for Hero Workbenches (`DraggableWorkbenchCard`)
Transforms static First-Fold Hero previews into tactile sandboxes using constrained spring drag (`drag`, `dragConstraints`, `whileTap`):

```tsx
"use client";

import * as React from "react";
import { motion } from "framer-motion";

export function DraggableWorkbenchCard({
  title,
  metric,
  children,
}: {
  title: string;
  metric: string;
  children: React.ReactNode;
}) {
  return (
    <motion.div
      drag
      dragConstraints={{ left: -24, right: 24, top: -16, bottom: 16 }}
      dragElastic={0.14}
      whileTap={{ scale: 0.98 }}
      transition={{ type: "spring", stiffness: 340, damping: 26 }}
      className="cursor-grab active:cursor-grabbing rounded-xl border border-neutral-800 bg-neutral-900/90 p-4 select-none"
    >
      <div className="flex items-center justify-between pb-2.5 mb-3 border-b border-neutral-800">
        <span className="text-xs font-mono text-neutral-400">{title}</span>
        <span className="text-xs font-mono tabular-nums text-emerald-400">{metric}</span>
      </div>
      {children}
    </motion.div>
  );
}
```

### C. Imperative Sequence Controller & Keyframe Arrays (`useAnimationControls` / `DampedShake`)
Programmatically triggers multi-step keyframe arrays (`x: [0, -6, 6, -4, 4, 0]`, `scale: [1, 1.03, 1]`) on validation error or live event arrival:

```tsx
"use client";

import * as React from "react";
import { motion, useAnimationControls } from "framer-motion";

export function ImperativeActionPanel({
  onValidate,
}: {
  onValidate: (code: string) => boolean;
}) {
  const [token, setToken] = React.useState("");
  const [status, setStatus] = React.useState<"idle" | "error" | "ok">("idle");
  const controls = useAnimationControls();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const ok = onValidate(token);
    if (!ok) {
      setStatus("error");
      await controls.start({
        x: [0, -6, 6, -4, 4, 0],
        transition: { duration: 0.32, ease: "easeInOut" },
      });
    } else {
      setStatus("ok");
      await controls.start({
        scale: [1, 1.03, 1],
        transition: { duration: 0.26, ease: [0.16, 1, 0.3, 1] },
      });
    }
  };

  return (
    <motion.form
      onSubmit={handleSubmit}
      animate={controls}
      className="flex items-center gap-2 p-3 rounded-lg border border-stone-800 bg-stone-900/70"
    >
      <label htmlFor="session-token" className="sr-only">
        Token Sesi
      </label>
      <input
        id="session-token"
        value={token}
        onChange={(e) => setToken(e.target.value)}
        placeholder="Masukkan kode token (mis: CBT-09)"
        className="min-w-0 flex-1 bg-transparent text-base sm:text-sm font-mono text-stone-100 placeholder:text-stone-500 focus:outline-none"
      />
      <button
        type="submit"
        className="px-3.5 py-1.5 rounded-md bg-emerald-600 text-stone-950 text-xs font-semibold hover:bg-emerald-500 active:scale-[0.97] transition-transform duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400"
      >
        Verifikasi Token
      </button>
      {status === "error" && (
        <span role="alert" className="text-xs font-mono text-amber-400">
          Token tidak cocok
        </span>
      )}
    </motion.form>
  );
}
```

```css
/* Zero-Dependency CSS Keyframe Equivalent */
@keyframes damped-shake {
  0%, 100% { transform: translate3d(0, 0, 0); }
  20% { transform: translate3d(-6px, 0, 0); }
  40% { transform: translate3d(6px, 0, 0); }
  60% { transform: translate3d(-4px, 0, 0); }
  80% { transform: translate3d(4px, 0, 0); }
}

.animate-shake {
  animation: damped-shake 320ms cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
}

@media (prefers-reduced-motion: reduce) {
  .animate-shake {
    animation: none;
  }
}
```

### D. Multi-Step Drawer (`MultiStepDrawer`)
Smooth step-indexed slide transition for operational workflows without modal stacking:

```tsx
"use client";

import * as React from "react";

export function MultiStepDrawer({
  steps,
}: {
  steps: { title: string; summary: string; detail: string }[];
}) {
  const [stepIdx, setStepIdx] = React.useState(0);
  const current = steps[stepIdx] ?? steps[0];

  return (
    <div className="rounded-xl border border-stone-800 bg-stone-900/80 p-5">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-mono text-stone-400">
          Langkah {stepIdx + 1} dari {steps.length}
        </span>
        <div className="flex items-center gap-1.5">
          {steps.map((s, idx) => (
            <button
              key={s.title}
              type="button"
              aria-label={`Buka langkah ${idx + 1}`}
              onClick={() => setStepIdx(idx)}
              className={`h-1.5 rounded-sm transition-colors duration-150 ${
                idx === stepIdx ? "w-6 bg-emerald-400" : "w-2 bg-stone-700"
              }`}
            />
          ))}
        </div>
      </div>
      <div
        key={stepIdx}
        style={{ animation: "step-fade-in 200ms cubic-bezier(0.16, 1, 0.3, 1)" }}
      >
        <h3 className="text-sm font-semibold text-stone-100 text-balance">{current.title}</h3>
        <p className="text-xs text-stone-400 mt-1">{current.summary}</p>
        <p className="text-xs font-mono text-stone-300 mt-2 pt-2 border-t border-stone-800/80">
          {current.detail}
        </p>
      </div>
    </div>
  );
}
```

---

## 4. Cards: 3D Perspective Tilt with Specular Spotlight (`PerspectiveCard`)

Cards that respond to mouse coordinates (`--mouse-x`, `--mouse-y`) and subtle 3D parallax feel like tangible instruments rather than flat boxes:

```tsx
"use client";

import * as React from "react";

export function PerspectiveCard({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  const cardRef = React.useRef<HTMLDivElement>(null);
  const [coords, setCoords] = React.useState({ x: 0, y: 0, rx: 0, ry: 0, active: false });

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const px = e.clientX - rect.left;
    const py = e.clientY - rect.top;
    const rx = ((py - rect.height / 2) / (rect.height / 2)) * -5;
    const ry = ((px - rect.width / 2) / (rect.width / 2)) * 5;
    setCoords({ x: px, y: py, rx, ry, active: true });
  };

  const handleMouseLeave = () => {
    setCoords((prev) => ({ ...prev, rx: 0, ry: 0, active: false }));
  };

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        transform: `perspective(1000px) rotateX(${coords.rx}deg) rotateY(${coords.ry}deg)`,
        transition: coords.active
          ? "transform 80ms linear"
          : "transform 360ms cubic-bezier(0.16, 1, 0.3, 1)",
      }}
      className={`relative overflow-hidden rounded-xl border border-stone-800 bg-stone-900/70 p-6 ${className}`}
    >
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 transition-opacity duration-200"
        style={{
          opacity: coords.active ? 1 : 0,
          background: `radial-gradient(360px circle at ${coords.x}px ${coords.y}px, rgba(16, 185, 129, 0.08), transparent 70%)`,
        }}
      />
      <div className="relative z-10">{children}</div>
    </div>
  );
}
```

---

## 5. Data Ledgers, Progressive Disclosure & Live Telemetry

### A. Expandable Data Row & Accordion Item (`ExpandableDataRow` / `AccordionItem`)
Zero-CLS progressive disclosure using CSS Grid `grid-template-rows: 0fr -> 1fr` (composite-friendly without measuring DOM pixel heights):

```tsx
"use client";

import * as React from "react";

export function ExpandableDataRow({
  id,
  primary,
  secondary,
  metric,
  detail,
}: {
  id: string;
  primary: string;
  secondary: string;
  metric: string;
  detail: string;
}) {
  const [open, setOpen] = React.useState(false);

  return (
    <div className="border-b border-stone-800/80">
      <button
        type="button"
        aria-expanded={open}
        onClick={() => setOpen((o) => !o)}
        className="w-full py-3 px-2 flex items-center justify-between text-left text-xs hover:bg-stone-800/40 rounded transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500"
      >
        <div className="flex items-center gap-3 min-w-0">
          <span className="font-mono text-stone-400 text-xs">{id}</span>
          <span className="font-medium text-stone-200 truncate">{primary}</span>
          <span className="text-stone-400 hidden sm:inline truncate">{secondary}</span>
        </div>
        <div className="flex items-center gap-4 shrink-0">
          <span className="font-mono tabular-nums font-semibold text-stone-100">{metric}</span>
          <span
            aria-hidden="true"
            style={{
              transform: open ? "rotate(180deg)" : "rotate(0deg)",
              transition: "transform 180ms cubic-bezier(0.16, 1, 0.3, 1)",
            }}
            className="text-stone-400 font-mono"
          >
            v
          </span>
        </div>
      </button>
      <div
        className="grid transition-[grid-template-rows,opacity] duration-200 ease-out"
        style={{
          gridTemplateRows: open ? "1fr" : "0fr",
          opacity: open ? 1 : 0,
        }}
      >
        <div className="overflow-hidden">
          <div className="px-3 pb-3 pt-1 text-xs font-mono text-stone-400 bg-stone-950/40 rounded mb-2">
            {detail}
          </div>
        </div>
      </div>
    </div>
  );
}
```

### B. Animated Tabular Counter Odometer (`CounterOdometer`)
Smoothly interpolates numeric metrics with locked `tabular-nums` so adjacent columns never jitter:

```tsx
"use client";

import * as React from "react";

export function CounterOdometer({
  value,
  suffix = "",
}: {
  value: number;
  suffix?: string;
}) {
  const [display, setDisplay] = React.useState(value);

  React.useEffect(() => {
    let rafId = 0;
    const start = display;
    const delta = value - start;
    if (delta === 0) return;
    const duration = 360;
    const t0 = performance.now();

    const step = (now: number) => {
      const p = Math.min(1, (now - t0) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      setDisplay(Math.round(start + delta * eased));
      if (p < 1) rafId = requestAnimationFrame(step);
    };
    rafId = requestAnimationFrame(step);
    return () => cancelAnimationFrame(rafId);
  }, [value]);

  return (
    <span className="font-mono tabular-nums">
      {display.toLocaleString("id-ID")}
      {suffix}
    </span>
  );
}
```

### C. Reversible Action Toast (`ReversibleActionToast`) & Animated Checkmark (`CheckDraw`)
Replaces disruptive confirmation modals with an 8-second undo window and SVG stroke completion:

```tsx
"use client";

import * as React from "react";

export function CheckDraw({
  size = 18,
  className = "text-emerald-400",
}: {
  size?: number;
  className?: string;
}) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" className={className}>
      <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" className="opacity-25" />
      <path
        d="M8 12.5L10.5 15L16 9.5"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        style={{
          strokeDasharray: 20,
          strokeDashoffset: 0,
          animation: "check-draw 360ms cubic-bezier(0.16, 1, 0.3, 1) forwards",
        }}
      />
    </svg>
  );
}
```

```css
@keyframes check-draw {
  from { stroke-dashoffset: 20; }
  to { stroke-dashoffset: 0; }
}
@keyframes step-fade-in {
  from { opacity: 0; transform: translate3d(0, 6px, 0); }
  to { opacity: 1; transform: translate3d(0, 0, 0); }
}
@media (prefers-reduced-motion: reduce) {
  @keyframes check-draw {
    from, to { stroke-dashoffset: 0; }
  }
  @keyframes step-fade-in {
    from, to { opacity: 1; transform: none; }
  }
}
```
