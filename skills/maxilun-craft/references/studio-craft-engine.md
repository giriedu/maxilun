# Maxilun Studio Craft Engine

<!-- metadata:
  version: "1.1.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine & Studio Jury Rubric Synthesis"
-->

Visual and interaction engineering guide at agency level. It codifies the scoring system of design award juries (Site of the Day / Developer Award / Mobile Excellence) into Maxilun's deterministic design method. Target: jury score $\ge 7.0/10$.

---

## 1. How a Studio Design Jury Weights Its Score (Memorize This)

The studio standard is not a graphic style. It is a weighted quantitative scoring system:

| Criterion | Weight | What the Jury Actually Measures |
|---|---|---|
| **Design** | **40%** | Visual hierarchy, typographic discipline, color intentionality, spacing rhythm, detail consistency across *every* page. |
| **Usability** | **30%** | Render speed, navigation clarity, mobile ergonomics, accessibility, Core Web Vitals (stretch target $INP < 100\text{ms}, CLS < 0.05$; the blocking gate is in `interaction-telemetry-benchmarks.md`: $INP \le 200\text{ms}, CLS = 0$). |
| **Creativity** | **20%** | Original concept, exactly **one memorable signature moment (*One Signature Moment*)**. |
| **Content** | **10%** | Original copy, real photography, visual integration that matches the subject's message. |

> **Critical Consequences That Drive Every Decision:**  
> 1. **Design (40%) + Creativity (20%) = 60%, but Usability (30%) alone can kill your score.** A striking site that opens slowly (>3s) or breaks on iPhone never reaches 7.0. Usability is an initial design constraint, not a QA phase at the end.  
> 2. **Build exactly ONE Signature Moment, not twenty scattered effects.** Randomly scattered effects read as visual panic and cut both the Design and the Usability score.

---

## 2. The Signature Moment Protocol

Before writing the first line of code, write the Signature Moment specification:

```markdown
### Signature Moment Specification
- **Moment Name**: [Example: Living Socket Inspector / Asymmetric Canvas Orbit]
- **Trigger**: [Scroll progress / First load sequence / Hover pointer / Drag]
- **Motion Phases**: State A -> Coordinated Transition -> State B (with exact timing)
- **Duration & Easing**: [300ms–800ms, one uniform cubic-bezier curve]
- **User Interaction**: What the user controls and how they discover it
- **Mobile Touch Version**: Direct touch adaptation (swipe/tap), not a disabled version
- **prefers-reduced-motion Version**: Instant transition without disorienting movement
- **First Three Seconds**: What reads clearly before the user starts interacting
```

---

## 3. The High-Craft Micro-Details

Jurors register craftsmanship subconsciously through small details. All of these primitives ship in the ready-to-use stylesheet `assets/craft-primitives.css`.
### 3.1 ScaleX Flip Underline (Link Underline That Reverses Direction)
An animated CSS underline that signals studio quality at once:
```css
.craft-link {
  position: relative;
  text-decoration: none;
}
.craft-link::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -0.15em;
  width: 100%;
  height: 1px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1);
}
.craft-link:hover::after,
.craft-link:focus-visible::after {
  transform: scaleX(1);
  transform-origin: left;
}
```

### 3.2 Image Zoom Inside a Clean Mask
Avoid cheap color filters; use a subtle zoom inside an `overflow: hidden` container:
```css
.craft-media-frame {
  overflow: hidden;
  border-radius: var(--radius-md);
}
.craft-media-frame img,
.craft-media-frame video {
  transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1);
  will-change: transform;
}
.craft-media-frame:hover img,
.craft-media-frame:hover video {
  transform: scale(1.05);
}
```

### 3.3 Global Text Selection Color
```css
::selection {
  background: var(--color-accent-solid);
  color: var(--color-accent-contrast);
}
```

### 3.4 Inner-Page Consistency Limit (Zero Homepage-Only Design)
Jurors and professional users always click navigation links through to inner pages. Build documentation pages, product detail pages, and the 404 page with the same token system, typography, and margins as the homepage.

---

## 4. Pre-Release Studio Jury Self-Scoring Audit

Before handing over the site, estimate the jury score yourself:

| Evaluation Dimension | Indicators That Pass at Score $\ge 7.0$ | Violation Symptoms (Cap the Score at $< 6.5$) |
|---|---|---|
| **Design (40%)** | Calibrated grid, role-based type scale, 1 primary action, neutral 1px hairline border, authentic photos/copy. | Template smell, rainbow gradient on headings, glowing neon borders, random vertical spacing. |
| **Usability (30%)** | Stretch targets $LCP < 1.5\text{s}$, $INP < 100\text{ms}$ (blocking gate: $LCP \le 2.5\text{s}$, $INP \le 200\text{ms}$), no scroll leak at 375px, visible keyboard focus ring, navbar $\le 64\text{px}$. | Frozen scroll-jacking, overflowing mobile menu, input font $<16\text{px}$, dead links. |
| **Creativity (20%)** | One strong signature moment, a living domain artifact (*The Living Engine*), tactile micro-interactions. | 20 scattered animation effects, fictional 3D particle canvas unrelated to function, cliché pill capsule. |
| **Content (10%)** | Copywriting oriented to real tasks, verified metric numbers, zero lorem ipsum text or cheap emoji. | Empty brochure slogans (*"Revolutionize Your Experience"*), text cut off at the canvas edge, emoji on buttons. |
