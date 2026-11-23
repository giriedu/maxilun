# Component & Registry Ecosystem Vault

> **Status**: Reference Document  
> **Specialist**: `maxilun-craft` & `maxilun-frontend`  
> **Source Attribution**: Curated from `awesome-shadcn-ui` (MIT License, see `CREDITS.md`)

This vault catalogs high-utility, domain-specialized UI components and registries built on the modern headless foundation (Radix UI / Base UI, Tailwind CSS, Class Variance Authority). Use these battle-tested patterns to construct bespoke interfaces instead of re-inventing complex headless primitives.

---

## 1. Architectural Invariants for Component Adoption

When adopting or adapting components from this ecosystem into a production Maxilun application:

1. **Copy-Paste and Own**:
   - Prefer directly embedding component source code (`components/ui/...`) over adding opaque third-party npm wrappers whenever possible.
   - Maintain total ownership of styling, accessibility, and refactoring lifecycle.

2. **RSC vs. Client Island Boundaries**:
   - Interactive components (`fancy-multi-select`, `adapttable`, `credenza`, `audiocn`) must be scoped as leaf Client Islands with `'use client'`.
   - Data fetching and layout orchestration remain in React Server Components (RSC). Pass plain serializable DTOs to islands.

3. **Purity & Quality Gate Enforcement**:
   - **`CMP-003` (Zero Emojis)**: Replace any emojis in community examples with monochrome SVG icons (`stroke="currentColor"`) from Lucide or the project's icon set.
   - **`LAY-008` (Anti-Monotony)**: Never place community cards into rigid, symmetrical 3-column grids. Embed components into asymmetric Bento layouts, operational ledgers, or split workspaces.
   - **Matte Precision**: Replace garish purple-cyan gradients with semantic tokens from `design-model.yaml` (OKLCH scales).

4. **Security & Supply-Chain Hardening (`maxilun-sentinel`)**:
   - Inspect third-party registry JSON/schema files before installing (`npx shadcn@latest add <registry-url>`).
   - Validate that components rendering user-generated markup (diff viewers, rich text) pass DOMPurify / sanitize-html gates.

---

## 2. Specialized Component Catalog by Domain

### A. Adaptive Overlays & Responsive Modals
*Standard dialogs fail on mobile viewports; adaptive overlays switch geometry based on screen size.*

| Component | Architecture & Purpose | Key Capabilities |
| :--- | :--- | :--- |
| **`credenza`** | Responsive Modal Primitive | Renders Radix `Dialog` on desktop (`min-width: 768px`) and Vaul `Drawer` (bottom sheet) on mobile. Zero duplicate state logic. |
| **`drop-drawer`** | Responsive Action Menu | Operates as a `DropdownMenu` on desktop and slides up as a gesture-dismissible `Drawer` on mobile touchscreens. |
| **`confirm-dialog`** | Promise-Based Action Gate | Async verification dialog for destructive operations with integrated loading states and keyboard shortcuts (`Enter`/`Esc`). |

### B. Complex Forms, Inputs & Autocomplete
*High-density input patterns designed for operational efficiency.*

| Component | Architecture & Purpose | Key Capabilities |
| :--- | :--- | :--- |
| **`auto-form`** | Schema-Driven Form Generation | Automatically constructs fully typed React Hook Form layouts directly from Zod schemas with validation, errors, and custom fields. |
| **`fancy-multi-select`** | Tagged Selection Primitive | Keyboard-first multi-select with inline badge removable pills, debounced search, and zero layout shift (campsite/cal.com pattern). |
| **`fancy-area`** | Mention-Enabled Textarea | Textarea with popover autocomplete for `@user` mentions, `#issue` references, and slash commands. |
| **`fancy-box`** | Labeled Filtering Combobox | Popover combobox with multi-category badges and color-coded tags inspired by GitHub PR issue label selectors. |
| **`emblor`** | Tag Input with Validation | Accessible tag management input with delimiter customization, drag-and-drop reordering, and max-tag constraints. |
| **`downshift-shadcn-combobox`** | Accessible Autocomplete | Production-grade autocomplete built with Downshift, supporting complex item objects, virtual lists, and WCAG AAA screen reader states. |
| **`async-select`** | Remote Search Dropdown | Select component with built-in debounced remote API fetching, abort controller cancellation, and loading skeletons. |

### C. Data Grids, Virtualization & Code Diffs
*Enterprise data presentation with high throughput and instant responsiveness.*

| Component | Architecture & Purpose | Key Capabilities |
| :--- | :--- | :--- |
| **`adapttable`** | High-Density Data Grid | TanStack Table preset with URL-synced state (`nuqs`), declarative filter chips, column reordering, and TanStack Virtual row virtualization. |
| **`@pierre/diffs`** | Code Comparison Engine | Syntax-highlighted split and unified diff rendering powered by Shiki, supporting line annotations and expand/collapse hunks. |
| **`crypto-charts`** | Financial Sparkline & Candlestick | Real-time SVG time-series charts with hover crosshairs, volume overlays, and `tabular-nums` tooltips. |

### D. Time, Date & Range Pickers
*Precise temporal selection with zero timezone ambiguity.*

| Component | Architecture & Purpose | Key Capabilities |
| :--- | :--- | :--- |
| **`date-time-range-picker`** | Multi-Month Range Selection | Dual-calendar picker with explicit IANA timezone dropdown, quick-preset shortcuts (Today, Last 7D, MTD, QTD), and comparison mode. |
| **`date-range-picker-for-shadcn`**| Compact Date Range Selector | Streamlined popover calendar with preset chips, keyboard input mask, and responsive single/dual month toggle. |
| **`datetime-picker`** | Timestamp Control | Granular date and time picker supporting 12/24-hour modes, second-level precision, and disabled boundary ranges. |

### E. AI Chat, Voice & Media Interfaces
*Modern agentic interfaces and tactile media controls.*

| Component | Architecture & Purpose | Key Capabilities |
| :--- | :--- | :--- |
| **`assistant-ui`** | AI Conversational Interface | Streaming chat interface with markdown rendering, generative tool call representations, thread history, and branch navigation. |
| **`agents-ui`** | Voice Agent Workspace | Voice interaction UI primitives (audio visualizers, live audio level bars, mic status indicators) built by LiveKit for React. |
| **`audiocn`** | Audio Production Primitives | React audio controls: logarithmic decibel meters, rotary knobs, vertical faders, channel strips, and tactile sound pads. |
| **`audio-ui`** | Playback & Waveform Suite | Accessible HTML5 audio wrapper with interactive canvas waveform scrubbing, chapter markers, and variable playback speeds. |

### F. Micro-Interactions, Layouts & Loaders
*Tactile feedback mechanisms maintaining the 60 FPS performance budget.*

| Component | Architecture & Purpose | Key Capabilities |
| :--- | :--- | :--- |
| **`dotmatrix`** | High-Craft Minimalist Loaders | 55+ SVG/CSS loaders and spinners (dot matrix, pulse rings, progress beams) with zero external script runtime. |
| **`drag-to-resize-sidebar`** | Persisted Layout Splitter | Multi-panel split container with smooth pointer tracking, collapse threshold snapping, and `localStorage` state persistence. |
| **`dnd-dashboard`** | Drop-to-Swap Grid | Flexible dashboard widget canvas using Swapy for smooth layout swaps without heavy drag-and-drop bundle overhead. |
| **`componentry`** | Micro-Interactive Triggers | Smooth spring-driven button states, ripple-free click responses, and expandable disclosure panels. |

---

## 3. Curated Component Registries & CLI Installation

When using the official CLI to scaffold components directly:

```bash
# Add base component from official registry
npx shadcn@latest add <component-name>

# Add community registry items directly via URL or namespaced registry
npx shadcn@latest add "https://raw.githubusercontent.com/<owner>/<repo>/main/registry/<item>.json"
```

### Verified Community Registries
- **`kibo-ui`**: Enterprise-grade components (advanced data tables, complex filter builders, nested trees).
- **`cult-ui`**: Tactile micro-interactions, interactive background canvases, and physics-driven spring buttons.
- **`origin-ui`**: Extended input primitives, phone number inputs with country flags, and password strength meters.
- **`shadcn-phone-input`**: International phone input with E.164 formatting and ISO 3166-1 alpha-2 flags.
- **`shadcn-timeline`**: Vertical and horizontal chronological event streams with status badges.

---

## 4. Integration Recipe: Scaffolding a Responsive Detail Drawer

When building a high-density master-detail view:

```tsx
"use client";

import * as React from "react";
import { useMediaQuery } from "@/hooks/use-media-query";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Drawer,
  DrawerContent,
  DrawerHeader,
  DrawerTitle,
} from "@/components/ui/drawer";

interface DetailViewProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  children: React.ReactNode;
}

export function DetailView({ open, onOpenChange, title, children }: DetailViewProps) {
  const isDesktop = useMediaQuery("(min-width: 768px)");

  if (isDesktop) {
    return (
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent className="sm:max-w-[640px]">
          <DialogHeader>
            <DialogTitle className="text-lg font-semibold tracking-tight">{title}</DialogTitle>
          </DialogHeader>
          <div className="py-2">{children}</div>
        </DialogContent>
      </Dialog>
    );
  }

  return (
    <Drawer open={open} onOpenChange={onOpenChange}>
      <DrawerContent className="p-4">
        <DrawerHeader className="text-left px-0">
          <DrawerTitle className="text-lg font-semibold tracking-tight">{title}</DrawerTitle>
        </DrawerHeader>
        <div className="py-2 overflow-y-auto max-h-[75vh]">{children}</div>
      </DrawerContent>
    </Drawer>
  );
}
```

*Adheres strictly to the 4-State Matrix, zero layout shift (CLS = 0), and smooth mobile-to-desktop responsiveness.*

---

## 3. Curated UI/UX Inspiration & Production Component Vault

This section catalogs 8 premier inspiration libraries and architectural design systems, mapping their core aesthetic patterns into Maxilun's strict Purity Gate:

### A. `jiro.build` — AI-Ready Component Blueprints (1,500+ Verified Layouts)
- **Core Archetype**: Production-ready source code across Next.js, Tailwind CSS, and headless primitives.
- **Architectural Heuristic**: Provides pre-vetted responsive wireframe trees and verified React blocks. When composing screens, use `jiro.build` structural hierarchies to avoid blank-canvas hallucination while replacing generic styling with project-specific OKLCH brand tokens.
- **Maxilun Invariant**: Strip community emojis (`CMP-003`) and convert floating KPI pill strips into dense, asymmetric tabular ledgers with right-aligned `tabular-nums`.

### B. `header.design` — Masthead & Navigation Architectures
- **Core Archetype**: Curated header compositions across enterprise software, developer tools, and editorial platforms.
- **Architectural Heuristic**:
  - **Operational Status Masthead**: Header integrating real-time telemetry (node status, environment indicator dot, sync timestamp) with negative tracking display typography.
  - **Sticky Translucent Backdrop**: Header pinning with `backdrop-blur-md bg-neutral-950/80` and `border-b border-neutral-800/80` to preserve scroll context without obscuring viewport real estate.
  - **Purity Gate Invariant (`HDR-001`)**: Forbid generic dummy breadcrumbs (`Dashboard / Analytics / Overview`) and centered pill stacks. Enforce clear two-level hierarchy: Workspace Switcher + Primary Nav on top, Contextual Action Deck below.

### C. `transitions.dev` — Fluid UI Layout Transitions
- **Core Archetype**: Tactile cross-screen and state transitions without jarring layout snaps or content jumps.
- **Architectural Heuristic**:
  - **FLIP Layout Morphing**: Apply Framer Motion `layoutId` or CSS View Transitions for smooth geometric expansion (e.g., list item expanding into full-width detail view).
  - **Zero CLS State Transitions**: Container bounds are pre-allocated so asynchronous content resolution causes zero cumulative layout shift.
  - **Reduced Motion Fallback**: Every layout transition strictly provides `@media (prefers-reduced-motion: reduce)` opacity cross-fades.

### D. `obsidianui.dev` — Obsidian Dark-Mode & Tactical Aesthetics
- **Core Archetype**: Deep obsidian dark palettes (`#08090C`, `#0E1015`), subtle reactive borders, and technical high-contrast clarity.
- **Architectural Heuristic**:
  - **Border Beam & Ray Highlights**: Subtle rotating gradient stroke (`border-neutral-800` accented by a moving hairline specular highlight) applied only to the primary focus anchor.
  - **Matte Precision**: Replace garish purple-cyan gradients with deep monochromatic slate, obsidian black, and functional emerald/amber status dots.

### E. `ui.aceternity.com` — High-Impact Animated React Primitives
- **Core Archetype**: Kinetic visual components (3D Pin, Spotlight Card Hover, Tracing Beam, Grid Backgrounds).
- **Architectural Heuristic**:
  - **One Signature Moment Rule**: Limit to exactly ONE signature motion element per viewport (e.g. an interactive Spotlight Card on the hero centerpiece or a Tracing Beam timeline).
  - **Compositor Safety**: Restrict motion execution strictly to GPU-accelerated properties (`transform`, `opacity`). Never animate `width`, `height`, `margin`, or `padding`.

### F. `60fps.design` — Tactile Kinetic Mobile & Desktop Micro-Interactions
- **Core Archetype**: High-refresh-rate interaction curves, fluid drawer swipe dismissals, and gesture physics.
- **Architectural Heuristic**:
  - **Analytical Damped Springs**: Use physical spring constants ($k = 300$, $\zeta = 0.85$) instead of artificial `linear` or ease-in-out bezier curves for touch feedback.
  - **Inertial Momentum**: Drag gestures respect release velocity, snapping to sheet snap-points without bouncy oscillations.

### G. `mobbin.com` — Production-Tested Mobile & Web User Flows
- **Core Archetype**: Exhaustive capture of real-world leader user journeys (checkout, multi-step onboarding, settings, paywalls).
- **Architectural Heuristic**:
  - **Progressive Disclosure**: Break complex multi-field configurations into 3–4 focused steps with persistent back navigation and inline field validation.
  - **Tap Ergonomics**: Interactive targets strictly maintain $\ge 44 \times 44$ px touch bounding boxes on mobile screens (`375px` viewport audit).

### H. `styles.refero.design` — AI Agent & Autonomous Interface Patterns
- **Core Archetype**: Advanced UI patterns tailored specifically for AI-native workflows and agent operations.
- **Architectural Heuristic**:
  - **Split Workbench Canvas**: Dual-pane workspace (left: streaming agent thought ledger, tool execution tree, and verification gates; right: live interactive document/canvas preview).
  - **Human-In-The-Loop Decision Cards**: Non-blocking interactive decision cards presenting concrete options (`[Accept A]`, `[Review B]`) rather than open-ended conversational prompts.
  - **Collapsible Tool Traces**: Detailed terminal logs, AST queries, and command outputs default to compact collapsible drawers with instant copy buttons and exit code badges.

