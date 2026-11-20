# Measured Design Gates

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine"
-->

`scripts/slopscan.py` reads source; it cannot see what a cascade, a theme switch, a hover rule, or a long name does to the page. This reference defines gates that open the rendered page and measure it, so a claim in the §9 report ("contrast passes", "nothing overflows", "the toggle works") is a number someone observed, not a sentence the agent wrote. Each gate states what to measure, the threshold, and how to measure it with nothing more than a browser and `page.evaluate` (or the DevTools console). Rules already owned elsewhere are not restated: the 4.5:1 / 3:1 contrast floor and 44px touch target live in SKILL.md §4, the state matrix in `ux-audit-matrix.md`, reduced-motion CSS in `motion.md`. This file only adds how to prove them on rendered output, plus the gates Maxilun had no rule for.

---

## 1. Gate Discipline

A gate that can only say yes is worse than no gate: it converts an unknown into a false pass.

| Rule | Requirement | Failure it prevents |
|---|---|---|
| Three exits | `0` measured and passed, `1` measured and failed, `2` could not measure. Exit 2 is reported `[UNVERIFIED]`, never folded into pass. | A machine without a browser printing "skipped" and a green summary. |
| Must reject its fixture | Every gate is run once against `evals/fixtures/slop-landing.html` (or a purpose-built broken page) and must fail it before its pass on real work counts. | A gate silently broken by a refactor that now passes everything. |
| Thresholds are tokens | Numeric limits live in the token block (`--gate-media-max-block: 60vh`), read by the gate at run time. | Editing the gate's source to make it pass. |
| Opt-outs live in the page, with a reason | An exemption is an attribute or comment in the markup that carries a sentence of justification (`data-gate-exempt="target-size: map pins use a spacing exception"`). A bare flag is rejected. | Quietly switching a gate off from the command line. |
| Measure vs heuristic | Geometry and computed-style facts block. Taste heuristics (ratios, counts) report only. | Teaching people to ignore a gate that guesses. |
| Both themes | Every colour gate runs in light and in dark (`emulateMedia({ colorScheme })` or the app's theme attribute). | A secondary button reads well in light yet drops to 1.1:1 in dark, because its component tokens were never mapped to the dark palette. |
| Receipts | Each run records gate, file, SHA-256 of the file at measurement time, exit code, printed numbers, timestamp. A number is quotable only while the file still hashes the same. | A remembered ratio quoted after the stylesheet changed. |

Freeze transitions before any colour or geometry read (`*, *::before, *::after { transition: none !important; animation-play-state: paused !important; }` injected as a style tag), otherwise the gate measures a mid-tween frame.

## 2. Contrast on the Composited Background, per State

**Measure.** For every visible text node and every control boundary: the computed foreground against the background the eye actually sees, which is the alpha composite of every ancestor background up to an opaque one.

**Threshold.** SKILL.md §4.4 floors, in default, hover, focus-visible, and active states; disabled controls exempt; loading controls NOT exempt (they are still readable content).

**Method.**

```js
function effectiveBg(el) {
  const layers = [];
  for (let n = el; n; n = n.parentElement) {
    const cs = getComputedStyle(n);
    if (cs.backgroundImage !== 'none') return null;      // gradient or image: not measurable
    const c = parse(cs.backgroundColor);                  // {r,g,b,a}
    if (c.a > 0) layers.push(c);
    if (c.a === 1) break;
  }
  return layers.reverse().reduce(over, { r: 255, g: 255, b: 255, a: 1 });
}
```

- `null` (text over a gradient or photo) is a failure for body text unless a solid scrim token sits between the text and the image. "White on a gradient" has no single measurable ratio, so it has no claim to pass.
- States: hover via `locator.hover()`, focus via keyboard `Tab` (not `.focus()`, which may skip `:focus-visible`), active via `mouse.down()` held during the read. Read each control on a fresh load so one hover does not bleed into the next read.
- Report as `element  state  ratio  [fg on bg]`, e.g. `button.secondary  hover  2.9:1  [rgb(...) on rgb(...)]`.

## 3. Token by Intent

A blue Delete passes every contrast check and is still a defect. Source grep cannot catch it because a class name does not reveal the colour it resolves to.

**Measure.** For each control, its label (accessible name) and its computed accent (background-color, or border/text colour for outline variants). Resolve the theme's accent and danger custom properties from `:root` in the same run.

**Signals and thresholds.**

| Signal | Condition | Verdict |
|---|---|---|
| Wrong intent | Destructive label painted with the accent hue (hue distance under 30 degrees) | Fail |
| Inverted | Affirmative label (save, confirm, continue, `simpan`, `kirim`, `lanjut`) painted with the danger hue | Fail |
| Inconsistent | Same destructive label rendered with hues more than 30 degrees apart on one screen (red trigger, blue confirm) | Fail |
| Untokenised page | No resolvable danger token and a destructive label filled with a saturated colour (HSL saturation over 40%) outside the red band (roughly 345 to 20 degrees) | Fail |
| Quiet destructive | Neutral or ghost destructive control | Pass: declining to be red is allowed; wearing the accent is not |

Destructive vocabulary must cover the UI language: delete, remove, revoke, discard, cancel subscription, close account, `hapus`, `buang`, `cabut akses`, `batalkan langganan`, `tutup akun`. Extend the list per product; a gate that does not know the product's wording for "destroy" will pass it.

## 4. Interactive Truth

**Measure.** Every enabled, visible control that declares a state contract: `aria-pressed`, `aria-expanded`, `aria-checked`, `aria-selected`, `aria-sort`, or a stateful role (`switch`, `tab`, `option`, `menuitemcheckbox`, `menuitemradio`).

**Method.** On a fresh load, attach a `MutationObserver` to `document` (attributes, childList, subtree), snapshot the control's computed style and the styles of its descendants, click it, wait two animation frames, then compare.

| Outcome | Verdict |
|---|---|
| No mutation anywhere, no focus move | Fail: dead contract. The header says it sorts and sorts nothing. |
| State attribute flipped, but control and descendants are style-identical and text-identical | Fail: invisible state. A screen reader hears the change, a sighted user sees nothing. |
| Plain button, no contract, no observable effect | Advisory only; harness pages legitimately ship inert demo buttons. |

A control that is a deliberate rendering of a state (a states harness showing a toggle in both positions) carries `data-demo-state` written by hand. The gate never infers that exemption.

## 5. Keyboard Is Driven, Not Inspected

**Measure.** Press `Tab` until focus cycles (cap at controls x 2), recording `document.activeElement` each time.

| Check | Failure |
|---|---|
| Reachable | An operable control without `tabindex="-1"` never receives focus. A `div` with a click handler fails here even though it passes every colour gate. |
| Operable | A focused custom control with a state attribute does not change it on `Enter` or `Space`. |
| Composite entry | A `tablist`, `listbox`, `menu`, `grid`, `tree`, `radiogroup`, or `toolbar` has no tabbable item, container, or owner. |
| Roving focus | Inside a composite, `ArrowRight`/`ArrowDown` moves neither focus nor `aria-activedescendant`. |
| Dialog | With a modal open: Tab never leaves it, it has an accessible name, `Escape` closes it, focus returns to the trigger. `<dialog>` opened with `showModal()` counts as modal without extra ARIA. |
| Trigger missing | The gate was told to open a dialog and found no trigger: exit 2, not 0. Nothing was opened, so nothing was proven. |

## 6. Target Size with the Real Exceptions

**Threshold.** 24 x 24 CSS px everywhere (WCAG 2.2 SC 2.5.8); 44 x 44 at viewports of 480px and below to honour the SKILL.md touch rule.

**Method.** `getBoundingClientRect()` on every operable target at each width. Before failing a small target, apply the three exceptions the criterion allows:

1. **Spacing**: passes if a circle of the threshold diameter centred on it intersects no other target's circle (centre-to-centre distance at least the threshold).
2. **Inline**: a link inside a run of text, where enlarging it would break the line box.
3. **Label union**: a checkbox or radio is measured as the union of its box and its associated `<label>`, which is part of the hit area.

Disabled controls are skipped: not operable, not targets.

## 7. Overflow That Hides

Happy-path copy fits by luck. These checks run on a stressed copy of the page.

**Stress set** (injected into a clone, never shipped): a 60-character email, a 40-character unbroken word (a long compound or a pasted token), a 13-digit figure in the locale format (`1.250.000.000.000`), a name three times the sample length, every list at 0, 1, and 50 items.

| Check | Threshold | Method |
|---|---|---|
| Page scroll | `documentElement.scrollWidth <= innerWidth` at 280, 320, 360, 768, 1440, and again at a 125% root font size | First remove `overflow-x: hidden/clip` from `html` and `body`. A root clip hides overflow from the measurement while still cutting content off. Clips on inner boxes (carousels) are design choices and stay. |
| Silent clip | Fail when `scrollWidth > clientWidth + 1` on an element with `overflow: hidden/clip` and `text-overflow` is not `ellipsis` | An ellipsis admits truncation; a silent cut does not. |
| Control overlap | Fail when two control rects overlap by more than a quarter of the smaller one's area | Long content pushed one control on top of another; part of it is untappable. |

The 125% pass approximates both a user's larger default text size and a platform whose fallback font is wider than the one on the developer's machine.

## 8. Mobile-First Proof

Counting `min-width` against `max-width` queries proves nothing. Strip the queries and look.

```js
for (const sheet of document.styleSheets) {
  let rules; try { rules = sheet.cssRules; } catch { return 'unreadable'; }   // exit 2
  for (let i = rules.length - 1; i >= 0; i--)
    if (rules[i] instanceof CSSMediaRule || rules[i].constructor.name === 'CSSContainerRule')
      sheet.deleteRule(i);
}
```

Render at 320px after stripping. The base styles must already be the phone layout: no page overflow (§7), no target under 24px (§6), no paragraph wider than 75 characters measured in its own font. A stylesheet the CSSOM refuses to expose (a linked sheet on `file://` is treated as cross-origin by Chromium) means the gate could not look: serve the page over local HTTP or exit 2. Treating an unreadable sheet as "no media queries, passes" is the exact blind spot to avoid.

## 9. Reduced-Motion Parity

Render twice: `reducedMotion: 'no-preference'` and `reducedMotion: 'reduce'`.

| Signal | Condition under `reduce` | Verdict |
|---|---|---|
| No policy | Page has animations or transform/size transitions and no reduce branch at all | Fail |
| Not reduced | `getAnimations()` still running, or a transform/position/size transition longer than 100ms | Fail. Opacity and colour transitions pass: a fade is the sanctioned substitute. |
| Content lost | An element visible without `reduce` has `opacity: 0`, `visibility: hidden`, or a zero box under `reduce` | Fail, highest severity. The reveal-on-enter pattern starts content invisible and lets the animation reveal it; kill the animation and the content never appears. |

Compare visibility element by element using a stable path (tag plus index chain), after waiting long enough for entrance animations in the first render to finish.

## 10. Screen Economy

The viewport is scarce, most of all on a phone, and large bright areas cost battery on OLED. Thresholds below are Maxilun's chosen defaults, exposed as tokens so a product can move them on purpose.

| Gate | Threshold and reason | Method |
|---|---|---|
| Media height | Image, video, or background-image block at most 60% of viewport height, so at least 40% remains for the heading and the action | `getBoundingClientRect().height / innerHeight` |
| Hollow box | A box covering 35% or more of the viewport must have the union bounding box of its visible children cover at least 30% of its content box | Union of child rects vs the box minus padding. Measure space used, not ink: well-leaded text never covers a third of its box in ink, so an ink ratio would punish good spacing. |
| Endless decoration | `iterations: Infinity` animations fail unless inside or beside an element with `aria-busy="true"` or a live region | `document.getAnimations()` and `effect.getTiming().iterations` |
| First screen earns itself | A product screen shows a readable heading and an enabled primary action inside the initial viewport at 360 x 640 | Rect top below `innerHeight`. Component harness pages opt out with `data-harness` on `<body>`. |
| Layout-shift readiness | Every `<img>` has intrinsic `width`/`height` or an `aspect-ratio`; images below the first viewport carry `loading="lazy"` | Attribute and computed-style read |

## 11. Spacing Geometry

| Gate | Threshold | Method |
|---|---|---|
| Ragged row | Boxed siblings whose tops align within 1px must have bottoms aligned within 1px | Group by top; skip items spanning several grid rows (a deliberate lead tile). Usually an `align-items: start` someone added. |
| Touching | A control, badge, or boxed card at least 8px (two steps on the 4 base) from its nearest sibling, at every width including 320 where rows wrap | Measure text by its glyphs (`Range.getBoundingClientRect()` over the text node), not its padded box, so the gap read is the gap the eye sees. Exception: a label and the control it names may be 4px apart. |

Not gated, left to eyes: "one relationship, one gap" and "one gutter". Two elements can carry the same class while being unrelated, and card padding moves text off a gutter the card itself sits on. Automating either produces false failures on good pages.

## 12. Token Closure Census

The rendered counterpart of the token lock (SKILL.md §2 step 4). Resolve every custom property on `:root`, then census computed values across `body *`.

| Property family | Pass condition |
|---|---|
| Colour (`color`, `background-color`, `border-*-color`, `fill`, `stroke`) | Every value is a resolved token, or a token at a stated alpha |
| Font size | At most six distinct values, all on the type scale |
| Font weight | At most three distinct values |
| Radius | Every value is the declared radius, a concentric derivative (outer minus padding, per `interface-engineering.md` §1.1), `0`, or full pill on tags and toggles |
| Box shadow | At most two distinct non-`none` values (the two elevation levels) |
| Accent spend | Count of elements painted with the accent hue; report the count and the elements. Advisory: SKILL.md §4.4 says "a handful", the reviewer decides. |

A value outside the set points at a hardcoded literal that slopscan missed (inline style written by script, third-party widget, framework default). Fix the set or remove the literal, as SKILL.md §2 step 4 requires.

## 13. Line Breaking for Scripts and Locales

Break opportunities are chosen by the browser's dictionary, not by the reader's sense of a unit.

- **Number and unit split.** Fail when a line ends with a currency or prefix (`Rp`, `No.`, `NISN`) and the next starts with its number, or a line ends with a number and the next starts with its unit or counter word (`siswa`, `kg`, `%`). Method: wrap each word in a `Range`, compare `top` of consecutive words. Fix: a non-breaking space or a `white-space: nowrap` span, including in strings built by script.
- **Stacked-mark leading.** Thai, Lao, Devanagari, and Arabic with vowel marks need room above and below each line. Measure `actualBoundingBoxAscent` and `actualBoundingBoxDescent` with canvas `measureText()` on a stress string set in the page's loaded font; fail when line-height in px is below ascent plus descent. These scripts typically need line-height near 1.45 for display sizes, and never negative letter-spacing.
- **RTL mirror.** Set `dir="rtl"` on `<html>` and rerun §7. Overflow that appears only mirrored points at physical `left/right` properties where logical ones belong (`interface-engineering.md` §4.3).

## 14. What Gates Cannot Prove

Passing every gate proves correctness, never taste. After the gates are green, run one adversarial pass whose job is to argue for rejection while looking at the rendered states, not the code. Cues that no gate catches:

- An empty state indistinguishable from a page that failed to load.
- A theme or mode toggle whose label and icon do not change with its state.
- A success toast announcing a change the list under it does not show.
- A loading control wearing the disabled dimming, so it reads as "not allowed" instead of "working".
- A screen that passes everything and would still fit a competitor (SKILL.md §7 Swap).

Report gate results as receipts (gate, file hash, exit, numbers) and the critique as findings with severity. Never merge them into one score: a high gate count must not launder a weak design.
