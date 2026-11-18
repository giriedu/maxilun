# Tells

What makes a screen read as machine-averaged. `slopscan.py` finds the ones
marked ⌕ automatically. The rest need you to look. Each tell has the reason
it happens and the decision that replaces it.

## A. Surface

| Tell | Why it appears | Replace with |
|---|---|---|
| ⌕ Hue-to-hue gradient on backgrounds, buttons, cards | Stands in for a brand that was never defined | A flat surface from the ramp; accent only on the Spotlight |
| ⌕ Gradient-filled text | Fastest way to make a heading feel "designed" | Solid text; hierarchy from size |
| ⌕ Glow, coloured shadow, neon border | Fakes depth and importance | Surface step + hairline; two elevation levels |
| ⌕ Frosted glass on many panels | Trend reflex | One solid surface; blur only behind a floating layer if at all |
| Blurred colour blobs, mesh, grid lines behind content | Fills emptiness | Leave the space empty, or put real content there |
| Dark navy + violet as the automatic "dark mode" | Most common dark palette in training data | Dark ramp derived from the Origin hue |
| Every panel a rounded card with border *and* shadow | Component library defaults stacked | Border or shadow, chosen once; fewer boxes |

## B. Structure

| Tell | Why | Replace with |
|---|---|---|
| Row of three or four identical stat cards, then two identical charts | Default dashboard skeleton | Rank against the Job: one dominant region, smaller supporting ones of different kinds |
| Card inside card inside card | Each component wraps itself | Flatten; group with space and a single container |
| Everything centred in a narrow column | Landing-page reflex applied to apps | Real app proportions; left-aligned reading edge |
| Hero = badge, headline, subtext, two buttons, screenshot, all centred | The canonical template | Composition decided by the content: split, full-bleed product view, or text only |
| Three feature cards with icon + title + one vague line | Fills a section without saying anything | Fewer, concrete claims with evidence; or delete the section |
| Sections that all have the same height and padding | Loop output | Vary by importance |
| Mobile is the desktop scaled down | No separate decision made | Re-rank for the narrow screen |

## C. Type

| Tell | Why | Replace with |
|---|---|---|
| ⌕ Headings at 800–900 weight | Weight used as the only hierarchy tool | 500–600, larger size, more space above |
| ⌕ ALL-CAPS micro labels with wide tracking | "Looks like a design system" | Sentence case in the secondary text role |
| ⌕ More than six font sizes on a screen | Sizes typed ad hoc | Scale from tokens |
| ⌕ The framework's default family, unexamined | Nobody chose | Confirm with a reason or replace |
| Centre-aligned paragraphs | Symmetry reflex | Left-aligned; centre only one or two short lines |
| Mixed number formats, proportional figures in columns | Mock data pasted in | One format, tabular figures |

## D. Colour

| Tell | Why | Replace with |
|---|---|---|
| ⌕ Many unrelated hues, each card or icon its own colour | "Colourful = friendly" | One accent; categorical colour only as small marks |
| ⌕ Dozens of near-identical greys or tints | Values typed by feel | Ramp roles |
| Accent on everything clickable and every heading | No emphasis budget | Accent on primary action, selection, Spotlight |
| Icon in a pastel rounded square on every card | Copied pattern | Icon in text colour, or no icon |
| Low-contrast grey text on grey | "Subtle" | Check the ratio |
| Pure grey ramp with one saturated blue button | The cleaned-up average | Tint the ramp and take the accent from the Origin |

## E. Components

| Tell | Why | Replace with |
|---|---|---|
| ⌕ Emoji as icons, bullets or status | Cheapest icon available | One line-icon family, or words |
| ⌕ Everything fully rounded | Pill reflex | One radius decision; nested radius math |
| Badges everywhere (New, Pro, Beta, AI) | Fake liveliness | Remove; one quiet label only if it changes a decision |
| Sparkline or mini chart in every stat | Fills the card | Number, label, comparison |
| Charts with a different colour per bar | Library default palette | One accent series, the rest neutral |
| Tables with zebra + borders + hover + icons per cell | All options on | One separator style, quiet header |
| Placeholder used as the label | Saves space | Visible label above the field |
| No empty, loading or error state | Only the happy path was imagined | Design all four states |
| Avatar stacks, star rows, "Trusted by" logos with no source | Social proof by template | Ask; remove if not real |

## F. Words

| Tell | Why | Replace with |
|---|---|---|
| ⌕ Greeting headline (`Welcome back, …` / `Selamat datang kembali, …`) | Friendly by default | The name of the page or period |
| ⌕ Hype verbs: supercharge, unlock, seamless, effortless, elevate, revolutionise; `solusi terbaik`, `tingkatkan produktivitas`, `revolusioner` | Marketing average | What it does, for whom, in the user's words |
| ⌕ Exclamation marks in interface text | Enthusiasm filler | Plain statement |
| `Lorem ipsum`, `John Doe`, `123,456`, `example@email.com` | Placeholder never replaced | Plausible local data |
| Buttons named `Submit`, `OK`, `Click here` | Generic verb | Verb + object |
| Formal-and-casual mix (`Anda` in one place, `kamu` in another) | Generated in pieces | One register for the whole product |
| English labels in an Indonesian product (or the reverse) | Template leftovers | One language |

## G. Motion

| Tell | Why | Replace with |
|---|---|---|
| ⌕ `transition: all` | Catch-all | Named properties |
| ⌕ Infinite pulse, ping, bounce, float, shimmer on things that are not live | "Feels alive" | Static; loop only for real progress or live status |
| ⌕ Hover scale on cards | Default interaction | Surface or border step |
| Every section fades up on scroll | Library demo copied | One entrance for the first view at most |
| Overshooting springs on menus and dialogs | Fun default | Critically damped; no bounce on utility UI |
| Animated counters on every number | Looks dynamic | Tween only a number that actually changed |
| ⌕ No reduced-motion handling | Forgotten | Global guard |

## H. The tidy average

Not slop, but what is left when decoration is removed and nothing is decided.
Check after every Repair.

- Neutral grey, default sans, one blue button, could be any SaaS.
- A headline where the product name is the only specific word.
- A layout identical to the last project's.
- A Brief whose Voice words would fit a bank, a game and a clinic.

If any of these is true, go back to Origin and Refusals and push them.
