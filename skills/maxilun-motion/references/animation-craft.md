# Modern Animation Craft & Fluid Motion Engineering

> **Status**: Reference Document  
> **Specialist**: `maxilun-motion` & `maxilun-craft`  
> **Source Attribution**: Synthesized from modern animation craft principles (MIT License, see `CREDITS.md`)

This document codifies the technical invariants, physics curves, and performance guardrails required to build software that feels organic, responsive, and tactile.

---

## 1. The 60 FPS Composite-Only Invariant

Smooth animation requires respecting the browser rendering pipeline. Animations must execute exclusively on the GPU compositor thread without triggering CPU Layout (Reflow) or Paint passes.

### Safe Properties (Composite-Only)
- **`transform`**: `translateX`, `translateY`, `translateZ`, `scale`, `rotate`.
- **`opacity`**: Clean alpha blending.

### Prohibited Animation Targets
- **Layout Properties**: Never animate `width`, `height`, `top`, `left`, `right`, `bottom`, `margin`, or `padding`. Use `transform: scale()` or CSS Subgrid / Grid-template-row transitions instead.
- **Heavy Paint Properties**: Avoid continuously animating `box-shadow`, `filter`, or `backdrop-filter`. Pre-render the elevated state on a pseudo-element (`::after`) and animate its `opacity`.

---

## 2. Natural Physics & Spring Dynamics

Real physical objects possess mass, friction, and momentum. Artificial linear transitions and aggressive ease-in curves create an unpolished, mechanical feel.

### The Easing Rules of Thumb
1. **Entering Elements (Popovers, Modals, Menus)**: Must enter with initial velocity and decelerate gracefully into position.
   - Standard Curve: `cubic-bezier(0.16, 1, 0.3, 1)` (Expo Out / Fast Deceleration)
   - Spring Equivalent: `stiffness: 260, damping: 20, mass: 1`
2. **Exiting Elements**: Must depart swiftly without lingering.
   - Standard Curve: `cubic-bezier(0.7, 0, 0.84, 0)` (Expo In / Fast Acceleration Out)
3. **Tactile Micro-Interactions (Buttons, Toggles)**:
   - Duration: 120ms – 150ms.
   - Scale-down on press: `scale(0.97)` to `scale(0.98)` with instant 100ms rebound.

---

## 3. Reverse Motion Vocabulary

Use this mapping to translate descriptive user feedback into exact mechanical tokens:

| Descriptive Request | Mechanical Motion Blueprint | Exact Formula / Token |
| :--- | :--- | :--- |
| *"Make it feel snappy & bouncy"* | Moderate damping spring with slight overshoot. | `stiffness: 300, damping: 22, mass: 0.8` |
| *"Make the modal feel weighty & premium"* | Critically damped motion with zero oscillation. | `duration: 240ms, easing: cubic-bezier(0.16, 1, 0.3, 1)` |
| *"The accordion jumps jarringly"* | CSS Grid row expansion technique. | Container: `grid-template-rows: 0fr -> 1fr`, Inner: `overflow: hidden; min-h: 0` |
| *"The tooltip feels sticky"* | Instantaneous appearance with delayed exit. | Entry: 100ms delay, 120ms fade; Exit: 0ms delay, 80ms fade |

---

## 4. Stacked Notification & Toast Architecture

When orchestrating multi-layer feedback components (such as Sonner-style stacked toast alerts):

1. **Stacking Dynamics**:
   - Maximum 3 items visible simultaneously in the resting stack.
   - Depth illusion via programmatic Y-offset translation (`translateY(calc(var(--index) * -12px))`) and scale attenuation (`scale(calc(1 - var(--index) * 0.05))`).
2. **Hover Expansion**:
   - On cursor hover over the stack, smooth spring transitions unstack the notifications into a vertical list so individual alerts can be read and dismissed.
3. **Gesture Dismissal**:
   - Touch/drag dismissals must track touch coordinates 1:1, calculating release velocity to determine whether to snap back or fling off-canvas.

---

## 5. Interruptibility & Accessibility

- **Interruptibility**: Animations must never lock the interface. If a user cancels or redirects an action mid-flight, the active transition must blend smoothly toward the new target without visual snapping or stutter.
- **Accessibility Invariant (`prefers-reduced-motion`)**:
  Every animated element must provide a fallback for users with vestibular sensitivities:
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, ::before, ::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }
  ```

