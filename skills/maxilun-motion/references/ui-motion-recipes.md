# UI Motion Recipes & Micro-Interaction Vault

> **Status**: Reference Document  
> **Specialist**: `maxilun-motion` & `maxilun-craft`  
> **Source Attribution**: Synthesized from curated micro-interaction patterns (see `CREDITS.md`)

This vault provides battle-tested, high-craft animation recipes designed to eliminate static, lifeless interfaces. Every recipe complies with the 60 FPS GPU compositor invariant, executes with zero layout shift (CLS = 0), and respects user accessibility settings.

---

## 1. Navigation: Sliding Pill Tab Bar

Replacing static tab underlines with an organic sliding background pill transforms navigation feel:

```tsx
"use client";

import * as React from "react";
import { motion } from "framer-motion";

interface Tab {
  id: string;
  label: string;
}

export function SlidingPillNav({ tabs, activeId, onChange }: { tabs: Tab[]; activeId: string; onChange: (id: string) => void }) {
  return (
    <nav className="inline-flex items-center gap-1 p-1.5 rounded-full bg-neutral-900/80 border border-neutral-800 backdrop-blur-md">
      {tabs.map((tab) => {
        const isActive = tab.id === activeId;
        return (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            className={`relative px-4 py-2 text-xs font-medium transition-colors duration-150 rounded-full ${
              isActive ? "text-neutral-100" : "text-neutral-400 hover:text-neutral-200"
            }`}
          >
            {isActive && (
              <motion.div
                layoutId="active-pill"
                transition={{ type: "spring", stiffness: 380, damping: 30 }}
                className="absolute inset-0 rounded-full bg-neutral-800 shadow-sm border border-neutral-700/60"
              />
            )}
            <span className="relative z-10">{tab.label}</span>
          </button>
        );
      })}
    </nav>
  );
}
```

---

## 2. Interactive Tactile Buttons

### A. Hold-to-Confirm Button (Destructive Actions)
Prevents accidental deletion while delivering visceral, satisfying physical confirmation:

```tsx
"use client";

import * as React from "react";

export function HoldToConfirmButton({ onConfirm, label = "Hold to Delete" }: { onConfirm: () => void; label?: string }) {
  const [progress, setProgress] = React.useState(0);
  const timerRef = React.useRef<NodeJS.Timeout | null>(null);

  const startHold = () => {
    const startTime = Date.now();
    const duration = 1200; // 1.2s hold duration
    timerRef.current = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const p = Math.min(100, (elapsed / duration) * 100);
      setProgress(p);
      if (p >= 100) {
        clearInterval(timerRef.current!);
        onConfirm();
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
      className="relative overflow-hidden px-5 py-2.5 rounded-lg border border-red-500/30 bg-red-950/20 text-red-400 text-xs font-semibold tracking-wide active:scale-[0.98] transition-transform select-none"
    >
      <div
        className="absolute inset-0 bg-red-600/30 transition-all duration-75 ease-linear pointer-events-none"
        style={{ width: `${progress}%` }}
      />
      <span className="relative z-10">{progress > 0 ? `Holding... ${Math.round(progress)}%` : label}</span>
    </button>
  );
}
```

### B. Magnetic Pointer Pull
Subtle attraction toward the cursor signals interactive luxury:

```tsx
"use client";

import * as React from "react";
import { motion, useMotionValue, useSpring } from "framer-motion";

export function MagneticButton({ children, onClick }: { children: React.ReactNode; onClick?: () => void }) {
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const springX = useSpring(x, { stiffness: 250, damping: 18 });
  const springY = useSpring(y, { stiffness: 250, damping: 18 });

  const handleMouseMove = (e: React.MouseEvent<HTMLButtonElement>) => {
    const { clientX, clientY, currentTarget } = e;
    const { left, top, width, height } = currentTarget.getBoundingClientRect();
    const centerX = left + width / 2;
    const centerY = top + height / 2;
    x.set((clientX - centerX) * 0.35); // 35% pull strength
    y.set((clientY - centerY) * 0.35);
  };

  const handleMouseLeave = () => {
    x.set(0);
    y.set(0);
  };

  return (
    <motion.button
      style={{ x: springX, y: springY }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      onClick={onClick}
      className="relative px-6 py-3 rounded-full bg-neutral-100 text-neutral-900 font-medium text-sm shadow-md hover:shadow-lg transition-shadow"
    >
      {children}
    </motion.button>
  );
}
```

---

## 3. Form Feedback: Damped Error Shake

When validation fails, an organic physical shake instantly alerts the user without intrusive popup alerts:

```css
@keyframes damped-shake {
  0% { transform: translateX(0); }
  20% { transform: translateX(-6px); }
  40% { transform: translateX(6px); }
  60% { transform: translateX(-4px); }
  80% { transform: translateX(4px); }
  100% { transform: translateX(0); }
}

.animate-shake {
  animation: damped-shake 320ms cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
}
```

---

## 4. Cards: 3D Perspective Tilt with Specular Sheen

Cards that respond to 3D mouse parallax feel like tangible objects rather than flat digital rectangles:

```tsx
"use client";

import * as React from "react";

export function PerspectiveCard({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  const cardRef = React.useRef<HTMLDivElement>(null);
  const [coords, setCoords] = React.useState({ x: 0, y: 0, rx: 0, ry: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const px = e.clientX - rect.left;
    const py = e.clientY - rect.top;
    const rx = ((py - rect.height / 2) / (rect.height / 2)) * -8; // max 8 deg tilt
    const ry = ((px - rect.width / 2) / (rect.width / 2)) * 8;
    setCoords({ x: px, y: py, rx, ry });
  };

  const handleMouseLeave = () => {
    setCoords({ x: 0, y: 0, rx: 0, ry: 0 });
  };

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        transform: `perspective(1000px) rotateX(${coords.rx}deg) rotateY(${coords.ry}deg)`,
        transition: coords.rx === 0 ? "transform 400ms cubic-bezier(0.16, 1, 0.3, 1)" : "none",
      }}
      className={`relative overflow-hidden rounded-2xl border border-neutral-800 bg-neutral-900/60 p-6 will-change-transform ${className}`}
    >
      {/* Dynamic Specular Sheen */}
      <div
        className="pointer-events-none absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        style={{
          background: `radial-gradient(400px circle at ${coords.x}px ${coords.y}px, rgba(255,255,255,0.06), transparent 70%)`,
        }}
      />
      {children}
    </div>
  );
}
```

---

## 5. Delight: Animated SVG Checkmark Draw

Instant visual closure upon completing an action:

```tsx
export function CheckDraw({ size = 24, className = "text-emerald-400" }: { size?: number; className?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" className={className}>
      <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" className="opacity-20" />
      <path
        d="M8 12.5L10.5 15L16 9.5"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        style={{
          strokeDasharray: 20,
          strokeDashoffset: 0,
          animation: "check-draw 400ms cubic-bezier(0.16, 1, 0.3, 1) forwards",
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
```
