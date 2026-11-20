# Three-Layer UX Architecture & Interface Audit Matrix

A rigorous, objective 3-layer UX and interface quality audit system. Grounded in LobeHub's production interface architecture and Maxilun's design standards.

---

## 1. The Three UX Audit Layers

Every interface surface—whether landing page, dashboard, modal, or form—is audited across three sequential layers:

```text
Layer 1: Static Architecture & Semantic Purity (Structure, Semantics, Color Contrast)
   ↓
Layer 2: Visual Engineering & Concentric Geometry (Spacing, Radii, Asymmetry, Typography)
   ↓
Layer 3: Dynamic Ergonomics & Micro-States (6-State Matrix, Skeletons, Mobile 375px)
```

---

## 2. Layer 1: Static Architecture & Semantic Purity

Audit against raw DOM structure and token hygiene before styling is evaluated:

| Checkpoint | Requirement | Failure Mode |
|---|---|---|
| **Semantic Heading Tree** | Exactly one `h1` per page; strictly nested `h2`, `h3` without skipped levels. | Jumping from `h1` to `h4` for font size. |
| **Monochrome Icons Only** | Single SVG icon set (Lucide, Radix, Phosphor). | Emoji characters used as interface icons (`CMP-003`). |
| **WCAG AA Contrast** | Normal text $\ge 4.5:1$, large text $\ge 3:1$, UI controls $\ge 3:1$. | Low-contrast grey text (`#94a3b8` on `#0f172a`). |
| **Landmark Landmarks** | Distinct `header`, `nav`, `main`, `footer`, and `aside` regions. | Nested `<div>` soup without landmarks. |
| **Token System Integrity** | All colors, spacing, and typography derived from CSS variables / OKLCH tokens. | Raw hex colors hardcoded in component styles. |

---

## 3. Layer 2: Visual Engineering & Concentric Geometry

Audit spatial harmony and layout topology:

### Concentric Border Radii Rule
Nested rounded corners must share a common geometric center. When child padding exists:
$$r_{\text{inner}} = r_{\text{outer}} - \text{padding}$$
- *Example*: If card outer radius is `16px` and padding is `12px`, the inner child element radius MUST be $16 - 12 = 4\text{px}$. Using identical `16px` for both looks sloppy and misaligned.

### Asymmetric Layout Topologies (Ban on 3-Card Triads `LAY-008`)
- Banned: Three equal-width cards sitting side-by-side with identical icon, header, and paragraph.
- Required: Declare an intentional topology from `design-archetypes.md`:
  - **Bento 2:1**: Primary spotlight cell ($66\%$ width) paired with stacked secondary cells.
  - **Tabular Ledger**: High-density numerical or data rows with monospaced data alignment.
  - **Master-Detail**: Persistent left list/sidebar paired with deep inspect pane.
  - **Spotlight Pairing**: 60/40 visual vs control pane.

---

## 4. Layer 3: Dynamic Ergonomics & Micro-States

Audit user interaction, state transitions, and responsive behavior:

### 6-State Component Matrix
Every interactive element (button, input, select, row) must declare 6 distinct visual states:
1. **Default**: Calibrated rest appearance.
2. **Hover**: Subtle contrast elevation or background tint ($\Delta L \approx 4-6\%$).
3. **Active (Pressed)**: Downward translation (`scale(0.98)` or inset shadow).
4. **Focus-Visible**: High-contrast outline with 2px offset for keyboard navigation.
5. **Disabled**: Reduced opacity ($40-50\%$), `cursor: not-allowed`, no hover effects.
6. **Loading / Pending**: Animated skeleton or spinner replacing action verb, preventing double submission.

### Mobile 375px Viewport Audit
- **Zero Horizontal Overflow**: No element may exceed `100vw` or cause horizontal scroll on a standard 375px mobile viewport.
- **Minimum Touch Targets**: All interactive targets must be $\ge 44 \times 44\text{px}$ (or padded to meet it).
- **Sticky Navigation Clearance**: Fixed bottom bars or headers must not obscure interactive form inputs.
