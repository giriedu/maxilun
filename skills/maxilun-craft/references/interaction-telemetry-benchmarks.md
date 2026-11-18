# Interaction Telemetry Benchmarks: Quantitative UX Instrumentation

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine"
-->

Measure user-experience performance quantitatively (*interaction telemetry benchmarks*). Do not judge design quality on visual aesthetics alone. Judge it on measured telemetry: interaction latency, layout stability, and task completion efficiency.

---

## 1. Web Vitals Thresholds (Frontend Telemetry)

Every web interface implementation must stay within these core metric limits:

| Metric | Parameter Name | Performance Target | Enforcement Mechanism in Code |
|---|---|---|---|
| **INP** | *Interaction to Next Paint* | $\le 200\text{ms}$ | Avoid heavy computation in event handlers; use `startTransition` in React for non-urgent updates. |
| **CLS** | *Cumulative Layout Shift* | **$= 0$ (Absolute Zero)** | Lock the size of images and dynamic containers with `aspect-ratio` or explicit dimensions; use proportional 1:1 skeletons. |
| **LCP** | *Largest Contentful Paint* | $\le 2.5\text{s}$ | Prioritize local font loading and modern media compression (AVIF/WebP) with the `fetchpriority="high"` attribute. |
| **TBT** | *Total Blocking Time* | $\le 150\text{ms}$ | Split large JavaScript bundles with *code splitting* and minimize third-party script execution. |

---

## 2. Mobile Frame Budget

In native iOS and Android applications:

1. **60 FPS / 120 FPS ProMotion Target**:
   - On a $60\text{Hz}$ display, render one frame in at most **$16.6\text{ms}$**.
   - On a $120\text{Hz}$ display (ProMotion / High Refresh Rate), render one frame in at most **$8.3\text{ms}$**.
2. **UI Thread Isolation**:
   - Run large JSON parsing, local database queries, and file decryption off the main thread (*background worker* / IO coroutine / Swift concurrency Task).
   - Frame failures (*jank* or frame drops) during fast list scrolling must be zero.

---

## 3. Product-Analytics Telemetry Goals (Post-Release Telemetry)

These indicators measure real user behavior via product analytics tools (PostHog, Amplitude, custom telemetry) after release. They are operational product goals, distinct from the deterministic, code-verifiable gates in §1:
1. ***Task Completion Rate* (TCR)**:
   - Target: $\ge 90\%$ of users who start the task flow finish the final confirmation without a dead end or a repeated error.
2. ***Time-To-Task* (TTT)**:
   - Compare how long users need to complete a form or a booking before and after the design change. The redesign succeeds when TTT drops by at least 20%.
3. ***Error Recovery Velocity***:
   - The average time from the user receiving an error message to fixing the input and continuing (target $\le 10$ seconds, achieved through clear inline recovery messages).
4. ***Form Drop-off Rate***:
   - Track which form fields users abandon most often. Evaluate every high drop-off field for removal or simplification.
