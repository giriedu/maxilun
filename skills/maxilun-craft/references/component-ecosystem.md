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

*Adheres strictly to the 4-State Matrix, zero layout shift (CLS = 0), and seamless mobile-to-desktop responsiveness.*
