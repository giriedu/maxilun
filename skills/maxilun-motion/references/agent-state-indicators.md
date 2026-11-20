# Agent State Indicators: Thinking, Working, Streaming & Error Motion

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun-motion/SKILL.md"
  origin: "Maxilun Motion Engine"
-->

Design and engineering rules for the small animated marks that tell a user what an AI agent is doing right now: the state model behind them, a Canvas 2D rendering loop that stays cheap at any count, per-size tuning, reduced-motion and offscreen behavior, and how the state reaches assistive technology. Use it together with `references/motion-components.md` (primitives) and `references/css-transition-recipes.md` (label swaps and streamed text).

---

## 1. Purpose Gate: The Indicator Mirrors Real State

An agent indicator passes the SKILL.md §5.1 gate only through function 1 (it communicates a status change). That has three consequences:

1. **Every visual state maps to a real backend state.** No timer-driven fake narration ("Analyzing...", "Almost there...") that cycles regardless of what the agent is doing. If the backend does not report a step, show one generic working state.
2. **The indicator stops the moment the work stops.** A loop that keeps running after a response finished or failed teaches users to ignore it.
3. **The verb vocabulary stays small.** Users learn 3-5 distinct shapes; a catalog of nine look-alike verbs carries no information. Distinguish states by what the user should do next, not by flavor.

| Expected wait | Indicator form | Rule |
|---|---|---|
| < 300 ms | none | Showing anything creates a flash; let the result appear |
| 300 ms - 1 s | indicator, appears after a show-delay | Delay ~300 ms so fast responses never flash it |
| 1 - 10 s | indeterminate animated mark + one-line status | Status text names the real step when the backend reports it |
| > 10 s | mark + step label + elapsed time or step count | Add a cancel control; motion alone does not reassure past ~10 s |
| Known fraction | determinate progress (bar, ring, step N of M) | Never use an indeterminate loop when the fraction is known |

## 2. The State Machine

Model the indicator as an explicit finite state machine fed by backend events. Do not derive it from booleans spread across components (`isLoading && !error && !done` breeds impossible combinations).

| State | Meaning | Visual | Announced |
|---|---|---|---|
| `idle` | nothing in flight | hidden or static resting mark | no |
| `pending` | request sent, no first byte yet | hidden during show-delay, then working mark | after show-delay only |
| `working` | agent reasoning or calling a tool | animated mark + step label | on entry and on step change |
| `streaming` | tokens arriving | mark shrinks or hides; text itself is the progress | on entry only |
| `awaiting-input` | blocked on the user (approval, question) | static mark, accent color, focusable action | yes, assertive only if blocking |
| `done` | finished successfully | short settle (<= 400 ms), then `idle` | brief "Response complete" |
| `error` | failed | static error mark + message + retry | yes, as an alert |
| `cancelled` | user stopped it | immediate stop, no exit flourish | "Stopped" |

Transition rules:

- **Show-delay and minimum-visible time.** Enter the visible working state only after ~300 ms of `pending`; once visible, keep it for at least ~500 ms. Both together remove the flicker of an indicator that appears for one frame.
- **Terminal states are not animated loops.** `error`, `done`, `cancelled`, and `awaiting-input` render a still frame. A spinning error mark reads as "still trying".
- **Step changes swap the label, not the mark.** Keep the mark continuous across `working` steps (same clock, no restart) and use the label swap recipe in `references/css-transition-recipes.md`.
- **Ignore stale events.** Tag each run with an id; drop events whose id is not the current run, or a late "step" event from a cancelled request resurrects the indicator.

```ts
type AgentPhase = 'idle' | 'pending' | 'working' | 'streaming' | 'awaiting-input' | 'done' | 'error' | 'cancelled';

type AgentEvent =
  | { type: 'start'; runId: string }
  | { type: 'step'; runId: string; label: string }
  | { type: 'token'; runId: string }
  | { type: 'needs-input'; runId: string; prompt: string }
  | { type: 'finish'; runId: string }
  | { type: 'fail'; runId: string; message: string }
  | { type: 'cancel'; runId: string };

interface AgentStatus { phase: AgentPhase; runId: string | null; label: string; detail?: string }

export function reduceStatus(s: AgentStatus, e: AgentEvent): AgentStatus {
  if (e.type === 'start') return { phase: 'pending', runId: e.runId, label: 'Working' };
  if (e.runId !== s.runId) return s; // stale event from an older run
  switch (e.type) {
    case 'step': return s.phase === 'pending' || s.phase === 'working' ? { ...s, phase: 'working', label: e.label } : s;
    case 'token': return s.phase === 'streaming' ? s : { ...s, phase: 'streaming', label: 'Writing response' };
    case 'needs-input': return { ...s, phase: 'awaiting-input', label: 'Waiting for you', detail: e.prompt };
    case 'finish': return { ...s, phase: 'done', label: 'Response complete' };
    case 'fail': return { ...s, phase: 'error', label: 'Something went wrong', detail: e.message };
    case 'cancel': return { ...s, phase: 'cancelled', label: 'Stopped' };
  }
}
```

The show-delay and minimum-visible timers live in the view layer that consumes this reducer, not in the reducer, so the reducer stays pure and unit-testable.

## 3. Rendering Architecture: Geometry Separate From Paint

Split each animated mark into two functions:

1. **Geometry**: `(t, size, params) -> Mark[]`, a pure function of time. It returns a finished, ordered list of draw instructions (center, radius, ink value 0..1, alpha) with nothing left to interpret.
2. **Paint**: iterates that list and issues `arc` + `fill` calls. It knows the theme color and nothing about motion.

Why this split pays off:

- **Deterministic and testable.** Because geometry depends only on `t`, a test can evaluate it at fixed timestamps and compare numbers (positions, radii) against stored vectors. Numeric comparison is stable across GPUs and font hinting; pixel snapshots are not.
- **Portable.** The same list can be painted by Canvas 2D, a native canvas, or an SVG fallback without re-deriving motion.
- **Reduced motion is free.** A static frame is just `geometry(t0)` for a chosen representative `t0`.

Determinism rules: never call `Math.random()` inside geometry; derive per-dot variation from a hash of the dot index. Use a monotonic clock (`performance.now()`), not `Date.now()`, which jumps with system clock changes.

## 4. Canvas Setup and Device Pixel Ratio

A canvas has two sizes: its CSS box and its backing store. Draw in CSS pixels and let one transform map them to device pixels.

```ts
const MAX_DPR = 2; // above 2 the extra pixels are invisible at indicator sizes but cost fill-rate

export function fitCanvas(canvas: HTMLCanvasElement, cssSize: number): CanvasRenderingContext2D {
  const dpr = Math.min(MAX_DPR, window.devicePixelRatio || 1);
  const px = Math.round(cssSize * dpr);
  if (canvas.width !== px) { canvas.width = px; canvas.height = px; } // assigning resets state, so only on change
  canvas.style.width = canvas.style.height = `${cssSize}px`;
  const ctx = canvas.getContext('2d', { alpha: true })!;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0); // every later draw call uses CSS pixels
  return ctx;
}
```

- **Re-fit when DPR changes** (window dragged to another monitor, browser zoom): watch a `matchMedia` query for `(resolution: <current dpr>dppx)` and re-run `fitCanvas` on `change`, then re-register for the new value.
- **Snap the CSS size to whole pixels.** A 20.5 px box gives a fractional backing store and blurry dots.
- **Clear with `clearRect` in CSS units after `setTransform`**, not by reassigning `width` every frame (that reallocates the buffer).
- **No `ctx.filter`, no `shadowBlur` in the loop.** Filter support on the 2D context is not uniform across engines, and shadow blur is one of the most expensive 2D operations. Express depth with dot radius and ink value instead (section 6).

## 5. One Shared Ticker, Paused When Not Visible

Ten indicators in a chat transcript must not mean ten `requestAnimationFrame` loops. Run one ticker; each indicator subscribes while it is visible.

```ts
type Draw = (tSeconds: number) => void;
const subscribers = new Set<Draw>();
let rafId = 0;

function tick(now: number) {
  const t = now / 1000; // shared clock: every mark stays in phase, and resumes in phase
  subscribers.forEach((draw) => draw(t));
  rafId = subscribers.size ? requestAnimationFrame(tick) : 0;
}

function subscribe(draw: Draw) {
  subscribers.add(draw);
  if (!rafId && document.visibilityState === 'visible') rafId = requestAnimationFrame(tick);
  return () => subscribers.delete(draw);
}

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'hidden') { cancelAnimationFrame(rafId); rafId = 0; }
  else if (subscribers.size && !rafId) rafId = requestAnimationFrame(tick);
});

export function mountIndicator(canvas: HTMLCanvasElement, draw: Draw, reducedMotion: MediaQueryList) {
  let unsubscribe: (() => void) | null = null;
  let onScreen = false;
  const sync = () => {
    const shouldRun = onScreen && !reducedMotion.matches;
    if (shouldRun && !unsubscribe) unsubscribe = subscribe(draw);
    if (!shouldRun && unsubscribe) { unsubscribe(); unsubscribe = null; }
    if (!shouldRun) draw(REST_T); // paint one still frame so the slot is never empty
  };
  const io = new IntersectionObserver(([entry]) => { onScreen = entry.isIntersecting; sync(); });
  io.observe(canvas);
  reducedMotion.addEventListener('change', sync);
  return () => { io.disconnect(); reducedMotion.removeEventListener('change', sync); unsubscribe?.(); };
}
const REST_T = 0.75; // a representative pose chosen by eye, not t = 0 (often a degenerate pose)
```

Rules:

- **Shared absolute time, not per-instance elapsed time.** Phase stays continuous after pause/resume and identical marks on one screen move together instead of drifting into visual noise.
- **Offscreen = zero cost.** `IntersectionObserver` stops subscriptions for marks scrolled out of the transcript; `visibilitychange` stops the whole ticker on hidden tabs (browsers throttle rAF there, but explicit stop also stops geometry work).
- **Cleanup is mandatory** (SKILL.md §5.2): every mount returns a disposer that disconnects observers and unsubscribes.
- **Frame budget.** Target < 0.5 ms of script per indicator per frame on a mid-range phone. Above ~300 marks per indicator, precompute static lattice positions once and only rotate them per frame.

## 6. Per-Size Tuning: Separate Designs, Not a Scale Factor

An indicator drawn for 64 px and shrunk to 16 px turns into grey mush: dots fall below one device pixel and motion amplitude drops below what the eye tracks. Ship a small set of size buckets, each tuned on its own.

| Parameter | Large (avatar scale, 48-72 px) | Small (inline text scale, 14-24 px) | Why |
|---|---|---|---|
| Mark count | full density | roughly 1/4 to 1/3 | fewer, larger marks stay distinguishable |
| Mark radius | baseline | relatively larger (sub-linear scale) | keeps each dot at or above ~1 CSS px |
| Angular speed | baseline | 1.3x to 2x | small travel distance needs more speed to read as motion |
| Depth range | full size and ink contrast | compressed | tiny depth differences alias into flicker |

Sub-linear radius scaling keeps small marks legible without a hand table for every size:

```ts
// referenceSize: the size the radii were designed at; exponent < 1 shrinks radii slower than the box.
const radiusFor = (base: number, size: number, referenceSize = 64, exponent = 0.6) =>
  Math.max(0.6, base * (size / referenceSize) ** exponent);
```

- Snap requested sizes to the nearest bucket; do not interpolate presets between buckets (in-between sizes get the worst of both).
- Inline indicators sit on the text baseline and size in `em`-derived whole pixels so they match the label's cap height.
- Review each bucket at 1x and 2x DPR on a real screen; a mark that only works at 2x fails on most office monitors.

## 7. Depth, Ink and Theme Without Filters

- **Depth cue = radius + ink.** Near marks are larger and higher contrast; far marks are smaller and closer to the background. Sort far to near and paint in that order; no blending modes needed.
- **Ink as a 0..1 value, color at paint time.** Geometry outputs ink; paint maps it between background and foreground. On dark themes the mapping inverts so near marks are bright.
- **Take color from CSS, not from theme sniffing.** Read the canvas element's computed `color` (it inherits `currentColor` from the surrounding text) at mount and when the theme changes. Walking every ancestor for `data-theme` or watching the whole document subtree with a `MutationObserver` per instance is expensive and couples the indicator to one theming convention.

```ts
function inkToRgba(ink: number, fg: [number, number, number], alpha: number) {
  const k = Math.min(1, Math.max(0, ink)); // 0 = background-like, 1 = full foreground
  return `rgba(${fg[0]},${fg[1]},${fg[2]},${(alpha * (0.25 + 0.75 * k)).toFixed(3)})`;
}
```

Alpha-based ink keeps the mark correct on any background, including tinted message bubbles, with one foreground color.

## 8. Reduced Motion

- Under `prefers-reduced-motion: reduce`, render one still representative frame (section 5, `REST_T`) and **keep every state change**: label text, color, and terminal icons still update. Reduced motion removes movement, not information.
- Listen for live `change` events on the media query; a user toggling the OS setting mid-session gets the static frame without reload.
- Do not replace the loop with a slower loop or an opacity pulse; a pulsing mark is still continuous motion.
- Streaming text under reduced motion appends instantly, with no per-word fade.

## 9. Accessible Status: The Canvas Is Decoration, the Text Is the Status

A canvas with `role="img"` and a label is announced once when encountered and never again, so it cannot report state changes. Structure instead:

```html
<div class="agent-status">
  <canvas class="agent-status__mark" aria-hidden="true"></canvas>
  <span class="agent-status__label" aria-hidden="true">Searching the repository</span>
  <span class="visually-hidden" role="status" aria-live="polite" aria-atomic="true"></span>
</div>
<div class="agent-response" aria-busy="true"><!-- streamed content --></div>
```

- **The live region exists before it is used.** Insert the `role="status"` element at mount, empty; then write text into it. Regions created together with their first message are often not announced.
- **Announce transitions, not frames.** Write to the live region only on phase entry and on step-label change, and throttle step announcements to at most one per ~2 s. Never announce per token.
- **Errors use `role="alert"`** (assertive) with the message and the retry control nearby; `awaiting-input` moves focus to the required control only when the user is not typing elsewhere.
- **`aria-busy="true"` on the response container while streaming**, cleared on `done`/`error`/`cancelled`, so screen readers can read the finished response as a whole instead of fragments.
- **Plain words, no decorative characters.** "Searching the repository", not a label ending in an ellipsis glyph that some screen readers read aloud as "dot dot dot".
- **Visible text stays visible.** The visual label is `aria-hidden` only because the live region carries the same words; never let the canvas be the only cue.

## 10. Streaming Output Motion

- The text itself is the progress indicator once tokens flow; shrink or hide the working mark when `streaming` starts.
- Batch DOM writes to one per animation frame; appending per token causes layout thrash on long answers.
- If streamed words fade in, use opacity only (optionally a sub-1 px blur on short spans), at most ~200 ms per word, and stop the effect beyond the visible viewport. Never delay text that has already arrived to make the animation look smoother; latency theater fails the purpose gate.
- Keep the caret or end-marker static or blink at <= 2 Hz; it is not a loading spinner.

## 11. Verification Checklist

Evidence each item before handoff (route measurement to `maxilun-verify`):

- [ ] Every visual state traces to a backend event; no timer-cycled fake steps.
- [ ] Show-delay (~300 ms) and minimum-visible (~500 ms) prevent flicker on fast and slow responses.
- [ ] Terminal states (`done`, `error`, `cancelled`, `awaiting-input`) render still frames.
- [ ] One rAF loop total; zero rAF callbacks when the tab is hidden or all marks are offscreen (check with a Performance recording).
- [ ] Backing store equals CSS size x capped DPR; marks stay crisp after moving the window between monitors.
- [ ] Each size bucket reviewed at 1x and 2x DPR; smallest dot >= ~1 CSS px.
- [ ] Geometry tests compare numeric marks at fixed `t` values, not screenshots.
- [ ] Reduced motion: still frame, labels and terminal states still update, live toggle works.
- [ ] Screen reader hears phase changes and step changes once each, errors assertively, never per token.
- [ ] No flash > 3 per second (SKILL.md §5.2); no `ctx.filter` or `shadowBlur` in the loop.

## 12. Rejected Patterns

| Pattern | Problem | Maxilun standard |
|---|---|---|
| Nine or more decorative state verbs | Users cannot learn them; shapes carry no decision | 3-5 states tied to next user action |
| `role="img"` canvas as the only status carrier | Announced once, changes are silent | Hidden canvas + persistent live region |
| One rAF loop per instance | Linear cost growth in long transcripts | Single shared ticker with subscriptions |
| Per-instance document-wide `MutationObserver` for theme | Fires on every class change anywhere | Inherit `currentColor` from CSS |
| Scaling one design to every size | Sub-pixel dots, invisible motion at small sizes | Tuned size buckets |
| Glow via `shadowBlur` / `ctx.filter` | Expensive, inconsistent across engines | Radius + ink depth cue |
| A third-party indicator package for one spinner | Dependency weight for ~150 lines of code | Native Canvas 2D first (Core Rule 3) |
