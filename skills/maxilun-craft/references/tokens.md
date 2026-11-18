# Tokens

How to derive a token set from the Brief. These are formulas and ranges, not
a house style: two products run through them should come out different.
If the project already has a sound token set, keep it and repair its usage.

Contents: output shape · spacing · type · neutrals · accent · status ·
radius · elevation · sizes

## Output shape

Write one block and use nothing else in components.

```css
:root {
  /* space */   --s-1: 4px; --s-2: 8px; --s-3: 12px; --s-4: 16px;
                --s-6: 24px; --s-8: 32px; --s-12: 48px; --s-16: 64px; --s-24: 96px;
  /* type */    --font-ui: ...; --font-num: ...;
                --t-xs: ...; --t-sm: ...; --t-md: ...; --t-lg: ...; --t-xl: ...; --t-2xl: ...;
  /* neutral */ --bg: ...; --surface: ...; --sunken: ...; --line: ...;
                --text: ...; --text-2: ...; --text-3: ...;
  /* accent */  --accent: ...; --accent-ink: ...; --accent-soft: ...;
  /* status */  --ok: ...; --warn: ...; --bad: ...; --info: ...;
  /* shape */   --r: ...; --r-lg: ...; --shadow: ...;
  /* motion */  --d-1: 120ms; --d-2: 200ms; --d-3: 320ms;
                --ease-enter: cubic-bezier(.2,0,0,1); --ease-exit: cubic-bezier(.4,0,1,1);
}
```

In Tailwind, put the same values into the theme (`@theme` in v4, or
`theme.extend` in v3) and stop using arbitrary `[...]` values. In Google Apps
Script or plain HTML, the `:root` block goes in the page's `<style>`.

## Spacing

Scale: 4 8 12 16 24 32 48 64 96. Pick by Density from the Brief.

| | Airy | Regular | Dense |
|---|---|---|---|
| Inside a control (padding-inline) | 16 | 12 | 8 |
| Between label and field | 8 | 8 | 4 |
| Between sibling items | 16 | 12 | 8 |
| Card / panel padding | 32 | 24 | 16 |
| Between groups | 48 | 32 | 24 |
| Between page sections | 96 | 64 | 48 |
| Control height | 44 | 36–40 | 28–32 |
| Table row height | 56 | 44 | 32–36 |
| Page gutter (desktop / phone) | 48 / 20 | 32 / 16 | 24 / 12 |

Touch surfaces keep 44px targets even when Dense: grow the hit area, not the
visual.

## Type

1. **Base size** by Density: Dense 13–14, Regular 15–16, Airy 17–18.
2. **Ratio**: tools 1.2, mixed 1.25, marketing 1.333. Sizes are base × ratioⁿ,
   rounded to whole pixels. Keep at most six.
3. **Line height**: running text 1.5–1.6, UI labels 1.3–1.4, headings
   1.15–1.25, display 1.0–1.1. Multiply out and snap to the 4px grid.
4. **Weights**: 400 text, 500 or 600 for labels and headings. One of them,
   not both. A third weight is reserved and used at most once per screen.
5. **Tracking**: 0 on body. Slightly negative (−0.01 to −0.02em) only above
   ~24px. Never negative on small text.
6. **Figures**: `font-variant-numeric: tabular-nums` wherever numbers stack.

Choosing a family: start from the Voice, and write the reason next to it.

| The Voice leans | Look among | Because |
|---|---|---|
| Institutional, trustworthy, public service | Public Sans, Source Sans 3, IBM Plex Sans, Noto Sans | Built for forms and long reading; wide language coverage |
| Local, friendly, Indonesian context | Plus Jakarta Sans, Nunito Sans, Figtree | Open shapes, warm without being childish |
| Dense data, operators, tables | system-ui stack, Inter (if chosen on purpose), IBM Plex Sans + Plex Mono | Holds up at 12–14px, true tabular figures |
| Technical, exact | Geist, JetBrains Mono for figures, Commit Mono | Mechanical rhythm reads as precision |
| Editorial, considered | a text serif for headings (Newsreader, Literata, Source Serif 4) over a plain sans | Two voices create hierarchy without weight |
| Bold, youthful, event | Bricolage Grotesque, Space Grotesk, Unbounded (display only) | Character in the headline, calm sans for everything else |
| Accessibility first | Atkinson Hyperlegible, Lexend | Letterforms designed to be told apart |

Rules: one UI family, optionally one partner (mono for figures or a display
face for headings). Load only the weights used. If offline use or load speed
matters (school networks, Apps Script), the system stack is the honest
choice: `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`.

## Neutrals

Build the ramp in OKLCH so steps are perceptually even. Take the hue `H`
from the Origin (the brand colour's hue, or the hue of the domain material:
paper ≈ 85, slate ≈ 250, leaf ≈ 150, clay ≈ 45). Chroma `C` stays tiny:
0.004–0.010 for apps, up to 0.020 for marketing pages. A ramp with `C = 0`
is pure grey and is the "nobody decided" answer.

| Role | Light L | Dark L |
|---|---|---|
| `--sunken` (wells, table header) | 0.965 | 0.130 |
| `--bg` | 0.985 | 0.160 |
| `--surface` | 1.000 | 0.195 |
| raised (hover, active row) | 0.955 | 0.235 |
| `--line` | 0.900 | 0.300 |
| `--text-3` (meta, captions) | 0.550 | 0.640 |
| `--text-2` | 0.420 | 0.760 |
| `--text` | 0.200 | 0.940 |

```css
--bg: oklch(0.985 0.006 85);   /* example: paper-tinted */
--text: oklch(0.20 0.010 85);
```

Provide hex fallbacks if old browsers matter. Body text uses `--text` or
`--text-2`; `--text-3` is for meta only. In dark themes do not use pure
black or pure white, and lift elevation by lightness, not by shadow.

## Accent

- A real brand colour is the accent. Otherwise take a hue from the Origin
  that is at least 60° away from the neutral hue so it reads as a decision.
- Shape it for use: on light themes `L 0.50–0.58, C 0.12–0.19`; on dark
  themes `L 0.70–0.78, C 0.10–0.15`.
- `--accent-ink` is the text colour on top of the accent. Verify 4.5:1 with
  the contrast command; if it fails, darken the accent rather than shrinking
  the text.
- `--accent-soft` is the accent at very low chroma and high lightness
  (light theme `L 0.95, C 0.03`) for selected rows and quiet highlights.
- The blue-to-violet family is what models reach for unasked. Use it only
  when the brand truly is that colour.
- One accent. If the product needs category colours (subjects, classes,
  statuses), that is a separate small categorical set used only as dots,
  thin bars or chart series, never as surface fills.

## Status

Same lightness and chroma as the accent so they sit together, hues about:
ok 150, warn 75, bad 25, info 245. Each gets a soft tint for backgrounds.
Status always travels with a word or an icon.

## Radius

One decision from the Voice: `0` (formal, print-like), `4` (exact, dense),
`8` (neutral, friendly), `12` (soft, consumer). Then:

- controls `--r`
- containers `--r-lg = --r + 4`
- nested element radius = parent radius − parent padding (minimum 2)
- full pills only for things that are literally tags or toggles

## Elevation

Two levels beyond the page: resting surfaces and floating things (menus,
dialogs, toasts). Resting surfaces use a hairline **or** a faint shadow,
chosen once for the whole product. Floating things use one neutral shadow:

```css
--shadow: 0 1px 2px oklch(0 0 0 / .06), 0 8px 24px oklch(0 0 0 / .10);
```

No coloured shadows. No shadow on dark themes except under floating things.

## Sizes

- Icons 16 in dense UI, 20 otherwise, stroke 1.5–1.75, one family
  (use the project's; otherwise Lucide, Phosphor or Tabler, pick one).
- Sidebar 224–272. Top bar 48–64. Content cap 1200–1440 for apps,
  running text 60–72ch.
- Dialog widths 400 / 560 / 720. Toast width ≤ 400.
- Focus ring: 2px, offset 2px, accent or text colour, never removed.
