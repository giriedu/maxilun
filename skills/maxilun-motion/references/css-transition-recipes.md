# CSS Transition Recipes: Swaps, Digits, Size Changes & Entry/Exit

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun-motion/SKILL.md"
  origin: "Maxilun Motion Engine"
-->

Native-CSS recipes for the small state changes that make an interface feel responsive: text and icon swaps, numbers that change, containers that change size, and elements that enter or leave the DOM. Each recipe states when to use it, the timing choice, the interruption behavior, and the reduced-motion fallback. Tokens (`--d-1`, `--d-2`, `--d-3`, `--ease-enter`, `--ease-exit`, `--ease-move`) come from `../maxilun-craft/references/motion.md`; the basic menu `@starting-style` and `grid-template-rows` reveal snippets live there and are not repeated here.

---

## 1. Pick the Recipe From the Change, Not From Taste

| What changed | Recipe | Section |
|---|---|---|
| A label's text, nothing shared ("Processing" to "Done") | Stacked cross-swap with blur + small rise | 3 |
| A label's text, shared start or end ("Save" to "Saved") | Shared-affix morph, only the differing part swaps | 4 |
| Two icons in one slot | Cross-swap with scale instead of rise | 3 |
| A number that updates rarely and matters (balance, score) | Per-digit swap with spring settle | 5 |
| A number that updates every few seconds (live stats) | Per-digit quiet cross-fade, direction-aware | 5 |
| A container's height opens from or closes to zero | `interpolate-size` or grid rows | 6 |
| A container resizes because its content changed | View Transition on the element, or measured width/height | 6 |
| An element is inserted or removed | `@starting-style` + `allow-discrete` exit | 7 |
| A small badge appears on a trigger | Scale-pop from `@starting-style` | 7 |
| Several lines enter together | Capped stagger via an index custom property | 8 |

If the value changes faster than the transition can finish (typing, scrubbing, sub-second polling), use no transition: the motion would only lag the data.

## 2. Timing, Easing and Interruption Rules

| Recipe class | Duration | Easing | Notes |
|---|---|---|---|
| Text / icon swap | 120-180 ms per side, overlapped | `--ease-move` | Exit and enter run at the same time, not back-to-back |
| Quiet digit change | 300-450 ms | `--ease-enter` | Distance about 0.15em, no overshoot |
| Emphasized digit change | 450-650 ms | spring via `linear()` | Overshoot no more than ~3% scale |
| Size change | 200-320 ms | `--ease-enter` | Larger boxes take the longer end |
| Enter from nothing | `--d-2` | `--ease-enter` | Exit is about 2/3 of enter, `--ease-exit` |
| Badge pop | 250-400 ms | spring via `linear()` | Starts at scale 0.6, never 0 (avoids a sub-pixel speck) |

- **Transitions retarget, keyframe animations restart.** A CSS `transition` interrupted mid-flight continues from the current value toward the new target. A keyframe `animation` jumps back to its first keyframe. Use transitions for reversible state (open/closed, hover), keyframes for one-shot events (a digit arriving).
- **Sequence with animation events, not timers.** `setTimeout(fn, parsedCssDuration)` breaks when someone writes `0.2s` instead of `200ms`, when reduced motion zeroes durations, and when the tab is throttled. Use `Promise.all(el.getAnimations().map((a) => a.finished))`, which resolves immediately when there are no running animations.
- **Distances in `em` for text.** A 4 px rise is huge on a 12 px caption and invisible on a 48 px figure; `0.15em` scales with the type.
- **Spring without a library.** `linear()` takes a list of output stops and approximates any curve, including overshoot:

```css
:root {
  /* settles with one ~4% overshoot; author new stops by sampling a damped spring, keep 10-20 points */
  --ease-spring-settle: linear(0, 0.24 9%, 0.62 19%, 0.9 29%, 1.035 39%, 1.045 46%, 1.02 57%, 1 70%, 0.997 84%, 1);
}
```

Hand-baking twenty keyframe percentages per property to fake a spring is unmaintainable; one `linear()` token is reusable across recipes. Provide a `cubic-bezier` fallback with `@supports not (transition-timing-function: linear(0, 1))` for old engines.

## 3. Stacked Cross-Swap (Text or Icon)

Old and new content occupy the same grid cell, so they animate at the same time and the box never collapses to zero between them.

```css
.swap { display: inline-grid; vertical-align: bottom; }
.swap > * { grid-area: 1 / 1; }
.swap[data-ready] > [data-state="in"]  { animation: swap-in  var(--swap-d, 160ms) var(--ease-move) both; }
.swap[data-ready] > [data-state="out"] { animation: swap-out var(--swap-d, 160ms) var(--ease-move) both; }

@keyframes swap-in  { from { opacity: 0; transform: translateY(0.3em);  filter: blur(1.5px); } }
@keyframes swap-out { to   { opacity: 0; transform: translateY(-0.3em); filter: blur(1.5px); } }

/* icon variant: scale reads better than travel inside a fixed square */
.swap--icon[data-ready] > [data-state="in"]  { animation-name: icon-in; }
.swap--icon[data-ready] > [data-state="out"] { animation-name: icon-out; }
@keyframes icon-in  { from { opacity: 0; transform: scale(0.7); filter: blur(1.5px); } }
@keyframes icon-out { to   { opacity: 0; transform: scale(0.7); filter: blur(1.5px); } }

@media (prefers-reduced-motion: reduce) {
  @keyframes swap-in  { from { opacity: 0; } }
  @keyframes swap-out { to   { opacity: 0; } }
  @keyframes icon-in  { from { opacity: 0; } }
  @keyframes icon-out { to   { opacity: 0; } }
}
```

```js
export async function swapContent(host, nextNode) {
  const leaving = host.querySelector('[data-state="in"]');
  if (leaving) {
    host.dataset.ready = '';                      // the very first render stays still; only real swaps animate
    leaving.dataset.state = 'out';
    leaving.setAttribute('aria-hidden', 'true');
  }
  nextNode.dataset.state = 'in';
  host.append(nextNode);
  if (!leaving) return;
  await Promise.all(leaving.getAnimations().map((a) => a.finished.catch(() => {})));
  leaving.remove();                               // rapid swaps stack safely: each call removes only its own node
}
```

- Reduced motion keeps a short opacity cross-fade instead of `animation: none`, so the change is still perceptible and `finished` promises still resolve.
- Blur stays at 1-2 px and only on short spans: `filter` forces a repaint of the element each frame, which is cheap for one word and expensive for a paragraph. Elements end at the implicit `filter: none` so text renders crisp at rest.
- The grid cell takes the wider of the two contents during the swap; if the label sits in a button whose width should ease, combine with section 6 measured width.

## 4. Shared-Affix Morph

When old and new labels share a prefix or suffix, keep the shared letters still and swap only the middle. The eye reads "Save" to "Saved" as one word gaining a letter instead of a new word.

```js
export function splitAffixes(prev, next) {
  let head = 0;
  while (head < prev.length && head < next.length && prev[head] === next[head]) head++;
  let tail = 0;
  while (tail < prev.length - head && tail < next.length - head &&
         prev.at(-1 - tail) === next.at(-1 - tail)) tail++;
  return {
    head: next.slice(0, head),
    oldMid: prev.slice(head, prev.length - tail),
    newMid: next.slice(head, next.length - tail),
    tail: next.slice(next.length - tail),
  };
}
```

Render `head`, a `.swap` (section 3) containing the old and new middle, then `tail`. Rules: only use this when the shared part is at least 3 characters or half the shorter label, otherwise the half-matched result looks broken ("Pending" to "Paid" sharing only "P"); split on grapheme clusters (`Intl.Segmenter`) rather than UTF-16 indexes for any non-ASCII copy; set `aria-label` on the button to the full new label because the visual pieces are fragmented.

## 5. Digit Changes

Split the formatted number into per-character cells and animate only the cells whose character changed.

```js
const fmt = new Intl.NumberFormat(undefined, { maximumFractionDigits: 2 });

export function renderNumber(host, prevValue, nextValue) {
  const prev = fmt.format(prevValue), next = fmt.format(nextValue);
  host.style.setProperty('--dir', nextValue >= prevValue ? '1' : '-1');
  host.querySelector('.sr-value').textContent = next;  // the screen reader reads one clean value
  const cells = host.querySelector('.digits');
  cells.replaceChildren(...[...next].map((ch, i) => {
    const cell = document.createElement('span');
    cell.textContent = ch;
    // align from the right so 999 -> 1,000 compares ones with ones
    const changed = prev.at(i - next.length) !== ch;
    if (changed) cell.className = 'digit-changed';
    cell.style.setProperty('--i', String(next.length - 1 - i)); // rightmost digit leads
    return cell;
  }));
}
```

```css
.number { font-variant-numeric: tabular-nums; }
.number .digits { display: inline-flex; }
.number .digits > * { display: inline-block; }
.digit-changed { animation: digit-quiet 380ms var(--ease-enter) both; animation-delay: calc(min(var(--i), 3) * 30ms); }
.number--emphasis .digit-changed { animation: digit-pop 560ms var(--ease-spring-settle) both; }

@keyframes digit-quiet { from { opacity: 0; transform: translateY(calc(0.15em * var(--dir))); } }
@keyframes digit-pop   { from { opacity: 0; transform: translateY(calc(0.45em * var(--dir))) scale(0.8); filter: blur(1px); } }

@media (prefers-reduced-motion: reduce) {
  .digit-changed, .number--emphasis .digit-changed { animation: digit-fade 160ms linear both; }
  @keyframes digit-fade { from { opacity: 0.2; } }
}
```

- `tabular-nums` is mandatory: proportional digits change width and make the whole number jitter sideways.
- Direction carries meaning: values going up rise, values going down fall. Do not color them unless the domain says up is good (a rising error count is bad).
- Mark the `.digits` container `aria-hidden="true"` and keep the full value in a visually-hidden `.sr-value`; announce it through a live region only when the user needs to know about the change.
- Polling dashboards use the quiet variant; the emphasized variant is for user-caused events (a payment applied, points earned). An emphasized number that changes every 3 s becomes noise.

## 6. Size Changes

| Situation | Native approach | Fallback |
|---|---|---|
| Height 0 to content height (disclosure, accordion) | `interpolate-size: allow-keywords` on `:root`, transition `height` between `0` and `auto` | `grid-template-rows: 0fr` to `1fr` (craft motion.md) |
| `<details>` open/close | `::details-content` with `content-visibility` + `allow-discrete` and `height` | instant toggle |
| Card resizes because its content changed | `document.startViewTransition()` with a `view-transition-name` on the card | measured width/height (below) |
| Button width follows its label | measured width transition | none: let it snap |

`interpolate-size` lets a transition run between a length and an intrinsic keyword such as `auto`; it does not animate `auto` to `auto` when the content inside changes. That case needs a View Transition or measurement.

```css
:root { interpolate-size: allow-keywords; }
.disclosure-body { height: 0; overflow: clip; transition: height var(--d-2) var(--ease-enter); }
.disclosure[data-open] .disclosure-body { height: auto; }

/* content-driven resize through a View Transition */
.result-card { view-transition-name: result-card; }
::view-transition-group(result-card) { animation-duration: 260ms; animation-timing-function: var(--ease-enter); overflow: clip; }
::view-transition-old(result-card),
::view-transition-new(result-card) { height: 100%; object-fit: none; object-position: left top; } /* no squashed text */
@media (prefers-reduced-motion: reduce) {
  ::view-transition-group(result-card) { animation-duration: 0s; }
}
```

```js
export async function resizeWithMeasure(box, mutate) {
  const from = box.getBoundingClientRect();
  mutate();                                         // DOM update that changes the natural size
  const to = box.getBoundingClientRect();
  if (from.width === to.width && from.height === to.height) return;
  const anim = box.animate(
    [{ width: `${from.width}px`, height: `${from.height}px` }, { width: `${to.width}px`, height: `${to.height}px` }],
    { duration: 240, easing: 'cubic-bezier(.2, 0, 0, 1)' });
  await anim.finished.catch(() => {});               // no fill: the box returns to its natural auto size
}
```

- Width/height animation runs layout each frame. That is acceptable for one small component for 200-300 ms, never for a looping animation or a list of dozens (SKILL.md §5.2). `will-change: width, height` gives no compositor benefit; do not add it.
- During a document View Transition the page shows snapshots; keep it under ~300 ms and never start one on hover or keystroke.
- Skip `resizeWithMeasure` when `prefers-reduced-motion: reduce` matches; snap to the new size.

## 7. Entry and Exit Without JavaScript Timers

```css
.toast {
  transition: opacity var(--d-2) var(--ease-enter), transform var(--d-2) var(--ease-enter),
              overlay var(--d-2) allow-discrete, display var(--d-2) allow-discrete;
}
.toast:not(:popover-open) {                         /* exit state, used when closing */
  opacity: 0; transform: translateY(0.5rem);
  transition-duration: calc(var(--d-2) * 0.66); transition-timing-function: var(--ease-exit);
}
@starting-style { .toast:popover-open { opacity: 0; transform: translateY(0.75rem); } }

.badge { transition: scale 320ms var(--ease-spring-settle), opacity 120ms linear; }
@starting-style { .badge { scale: 0.6; opacity: 0; } }

@media (prefers-reduced-motion: reduce) {
  .toast:not(:popover-open) { transform: none; }
  @starting-style { .toast:popover-open { transform: none; } .badge { scale: 1; } }
}
```

- `overlay` keeps a popover or modal dialog in the top layer until its exit transition ends; without it the element drops out of the top layer at frame one and the exit is clipped.
- `@starting-style` only applies on the first style resolution after insertion or `display: none` to visible; inserting a node that is already visible animates, re-rendering an existing one does not. For framework lists keyed by id that is the desired behavior.
- Use the individual `scale`/`translate` properties for the pop so a later `transform` on hover does not cancel it.
- Unsupported engines simply show the end state: the content appears without motion, which is an acceptable fallback.

## 8. Capped Stagger

```css
.reveal-line { animation: line-in var(--d-3) var(--ease-enter) both; animation-delay: calc(min(var(--i, 0), 5) * 35ms); }
@keyframes line-in { from { opacity: 0; translate: 0 0.4em; } }
@media (prefers-reduced-motion: reduce) { .reveal-line { animation: none; } }
```

Set `--i` inline per item (`style="--i: 2"`); where the engine supports `sibling-index()` it can replace the inline index, but keep `--i` as the baseline. The `min()` cap keeps total stagger under ~200 ms no matter how many lines arrive (craft budget: 30-40 ms per item, 300 ms total). Stagger once per view, on first appearance; never re-stagger on re-render or filter.

## 9. Rejected Patterns

| Pattern | Problem | Maxilun standard |
|---|---|---|
| `transition: none !important` as the only reduced-motion rule | Removes feedback along with movement; state changes become invisible | Keep opacity/color change, drop travel and scale |
| Exit then enter sequenced with `setTimeout` | Double duration, breaks with unit changes and throttled tabs | Overlapped swap, `getAnimations().finished` |
| Twenty baked keyframe stops per property to fake a spring | Unreadable, untunable | One `linear()` easing token |
| `will-change` on width/height | No compositor gain; wastes memory | Animate layout briefly or use View Transitions |
| Blur on whole paragraphs or long lists | Per-frame repaint cost | Blur <= 2 px on short spans only |
| A paid or vendored transition kit for a handful of swaps | Dependency and license weight for ~40 lines of CSS | Native CSS + small WAAPI helper (Core Rule 3) |
| Timer-cycled "thinking" status text | Fake progress; screen readers re-announce every cycle | Labels from real events, see `references/agent-state-indicators.md` |

## 10. Verification

- [ ] Each recipe chosen from the section 1 table by the kind of change, not by look.
- [ ] Rapid repeated triggers (click 5x in 1 s) leave no stale nodes and end in the correct final state.
- [ ] Reduced motion: every change still perceptible (opacity or color), no travel, no scale.
- [ ] Numbers use `tabular-nums`; screen readers read one complete value.
- [ ] No layout-property animation loops; size animations finish under ~320 ms.
- [ ] Unsupported-engine path (no `linear()`, no `@starting-style`, no View Transitions) checked once and shows correct end states.
