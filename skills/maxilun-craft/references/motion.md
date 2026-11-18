# Motion

Motion is the last layer. A screen that needs animation to feel finished is
not finished. Add it when the static screen already works.

Contents: the three questions · budget · tokens · CSS recipes ·
when to use the Motion library · library recipes · performance · checklist

## The three questions

An animation stays only if it answers one of these for the user:

1. **Where did this come from / where did it go?** Menus, dialogs, drawers,
   toasts, list items being added or removed, a card expanding into a page.
2. **What just changed?** A value updating, a row reordering, a filter
   narrowing a list, a tab switching.
3. **Did my action register?** Press feedback, a toggle moving, a save
   confirming, a drag following the finger.

Decoration (floating shapes, looping gradients, scroll-triggered fades on
every section, counters that count for no reason) answers none and goes.

## Budget

- **Frequency rule.** Seen once a visit: up to 320ms and may be expressive.
  Seen many times a session: 120–200ms. Seen constantly (typing, table
  hover, keyboard navigation, tab switching in a work tool): none.
- **Distance.** Elements travel 4–16px, not across the screen. Scale changes
  stay within 0.96–1.0. Large things move less and slower than small things.
- **Leaving is faster than entering**, about two thirds of the duration.
- **Stagger** at most 30–40ms per item and 300ms in total; cap the count,
  let the rest appear together.
- **One entrance per view.** The main content may fade and rise once on
  first load. Not each card, not each section on scroll.
- **Loops** only for something truly ongoing: a spinner for unknown-length
  work, a pulse on a genuinely live indicator.
- **Bounce** belongs to things that are dragged, thrown or playful by Brief.
  Menus, dialogs and forms settle without overshoot.

## Tokens

```css
:root {
  --d-1: 120ms;  /* feedback: hover, press, toggle */
  --d-2: 200ms;  /* small things entering: menu, tooltip, toast */
  --d-3: 320ms;  /* large things: dialog, drawer, page section */
  --ease-enter: cubic-bezier(.2, 0, 0, 1);   /* fast start, soft landing */
  --ease-exit:  cubic-bezier(.4, 0, 1, 1);   /* accelerates away */
  --ease-move:  cubic-bezier(.4, 0, .2, 1);  /* on-screen A to B */
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: .01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Reduced motion does not mean no feedback: keep opacity and colour changes,
drop movement and scale.

## CSS recipes (use these first)

```css
/* Feedback */
.btn { transition: background-color var(--d-1) var(--ease-move),
                   transform var(--d-1) var(--ease-move); }
.btn:active { transform: scale(.98); }

/* Enter from nothing, no JS (modern browsers) */
.menu { transition: opacity var(--d-2) var(--ease-enter),
                    transform var(--d-2) var(--ease-enter),
                    display var(--d-2) allow-discrete;
        transform-origin: top left; }
.menu[hidden] { opacity: 0; transform: translateY(-4px) scale(.98); }
@starting-style { .menu { opacity: 0; transform: translateY(-4px) scale(.98); } }

/* Height open/close without animating height */
.reveal { display: grid; grid-template-rows: 0fr;
          transition: grid-template-rows var(--d-2) var(--ease-move); }
.reveal[data-open="true"] { grid-template-rows: 1fr; }
.reveal > * { overflow: hidden; }

/* Page-to-page continuity */
@view-transition { navigation: auto; }
```

Grow menus and popovers from the control that opened them
(`transform-origin` at the trigger), not from their centre.

## When to use the Motion library

`motion` (motion.dev, formerly Framer Motion) is worth its bytes when CSS
cannot do the job cleanly:

| Need | CSS enough? | Library |
|---|---|---|
| Hover, press, colour, simple enter | Yes | No |
| Element animates **out** before unmounting (React/Vue) | Awkward | `AnimatePresence` |
| Size, position or order changes (reorder, expand, shared element) | No | `layout`, `layoutId` |
| Drag, swipe to dismiss, pinch | No | gestures |
| Value tied to scroll progress | Partly (`animation-timeline`) | `useScroll`, `scroll()` |
| Interruptible motion that keeps velocity | No | springs |
| Sequenced timeline across elements | Painful | `animate()` sequences |

Do not add it to a project just to fade a card in. In plain HTML or Apps
Script pages, the vanilla build is enough and loads from a CDN; pin the
version.

Install: `npm install motion`. React imports come from `motion/react`,
vanilla from `motion`. The API below is stable across recent major versions;
if something does not behave as written, check motion.dev/docs for the
installed version instead of guessing.

## Library recipes

**Global setup (React).** One place decides duration, easing and
reduced-motion for the whole app.

```jsx
import { MotionConfig } from "motion/react"

<MotionConfig reducedMotion="user"
              transition={{ duration: 0.2, ease: [0.2, 0, 0, 1] }}>
  <App />
</MotionConfig>
```

**Exit animation.** The reason most projects need the library at all.

```jsx
import { AnimatePresence, motion } from "motion/react"

<AnimatePresence>
  {open && (
    <motion.div
      key="dialog"
      initial={{ opacity: 0, y: 8, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: 4, transition: { duration: 0.13 } }}
    />
  )}
</AnimatePresence>
```

**List that adds, removes and reorders.**

```jsx
<AnimatePresence initial={false} mode="popLayout">
  {rows.map(r => (
    <motion.li key={r.id} layout
      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} />
  ))}
</AnimatePresence>
```

**Shared element** (the tab indicator, a card becoming a detail view).

```jsx
{tabs.map(t => (
  <button key={t.id} onClick={() => setActive(t.id)}>
    {t.label}
    {active === t.id && <motion.span layoutId="tab-underline" className="underline" />}
  </button>
))}
```

**Spring for things under the finger.** Describe springs by how long they
look and how much they bounce; keep bounce at 0 for utility UI.

```jsx
<motion.div drag="x" dragConstraints={{ left: 0, right: 0 }} dragElastic={0.2}
  transition={{ type: "spring", visualDuration: 0.3, bounce: 0 }} />
```

**Vanilla, no framework** (plain HTML, Apps Script web app).

```html
<script type="module">
  import { animate, stagger, inView }
    from "https://cdn.jsdelivr.net/npm/motion@<pinned-version>/+esm"

  const still = matchMedia("(prefers-reduced-motion: reduce)").matches
  if (!still) {
    // the single entrance for the first view
    animate(".page > *", { opacity: [0, 1], y: [8, 0] },
            { duration: 0.24, delay: stagger(0.03), ease: [0.2, 0, 0, 1] })
  }
  // number that actually changed
  function tweenNumber(el, from, to) {
    animate(from, to, { duration: 0.3,
      onUpdate: v => el.textContent = Math.round(v).toLocaleString("id-ID") })
  }
</script>
```

**Bundle size (React).** For large apps, load features lazily with
`LazyMotion` and the `m` component from `motion/react-m`.

## Performance

- Animate `transform` and `opacity`. `filter: blur` only on small elements
  and briefly. Never `width`, `height`, `top`, `left`, `margin`, `padding`,
  `box-shadow` spread; use `layout`, the grid-rows trick or a scale.
- Do not read layout (`getBoundingClientRect`, `offsetHeight`) inside an
  animation loop.
- `will-change` only on the element, only while it animates.
- Test on a slow phone or with CPU throttling at 4×. If it stutters there,
  shorten or remove it.

## Checklist

- [ ] Every animation answers one of the three questions
- [ ] Durations and curves come from tokens; no `transition: all`
- [ ] Exit is shorter than enter
- [ ] No loop on anything that is not live or loading
- [ ] No bounce on menus, dialogs, forms
- [ ] Reduced-motion handled globally and verified
- [ ] High-frequency interactions are instant
- [ ] Library added only for a need in the table above
