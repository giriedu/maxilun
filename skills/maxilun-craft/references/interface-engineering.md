# Interface Engineering: Mathematical Precision & Production Design Rules

Advanced interface engineering guide. It applies high-precision *interface engineering* principles to remove generic aesthetics and AI template molds. Operational reference for `maxilun-craft`, `maxilun-frontend`, and `maxilun-verify`.

---

## 1. Visual Precision & Surface Polish (UI Polish)

The values below are exact, not approximate ranges.

### 1.1 Exact Concentric Radius Formula
When a parent container and its child element have an even inset (padding):
$$\text{radius}_{\text{outer}} = \text{radius}_{\text{inner}} + \text{padding} + \text{border}$$
$$\text{radius}_{\text{inner}} = \max(0, \text{radius}_{\text{outer}} - \text{padding} - \text{border})$$

If the outer card uses `rounded-2xl` (16px) with 8px padding, the button or input inside it **must** use an 8px radius (`16px - 8px = 8px`), not a uniform 16px or a sharp 0px. Above 24px padding, or with deliberately asymmetric padding, treat the two layers as independent surfaces.

### 1.2 Layered Shadows for Elevation, Borders for Structure
- **Border**: Only for structural separators (dividers, table rows, column separators, form input boundaries that need 3:1 non-text contrast per WCAG 1.4.11).
- **Elevation**: Replace thick borders that fake depth with a *layered transparent box-shadow*:
  ```css
  /* Subtle contact elevation */
  box-shadow: 0 1px 2px oklch(0 0 0 / 0.05), 0 1px 3px oklch(0 0 0 / 0.08);
  /* Always include a transparent border so forced-colors mode still draws the edge */
  border: 1px solid transparent;
  ```

### 1.3 Pure Black/White Image Edge Line (1px Inset Outline)
Give content media/images a `1px` outline inset by `1px`:
- Light mode: `oklch(0 0 0 / 0.1)`
- Dark mode: `oklch(1 0 0 / 0.1)`
- **Do not** use a tinted neutral gray or the brand accent color. It creates a dirty colored *fringe* on the image edge. Skip transparent vector elements (logos and illustrations).

### 1.4 Tactile Micro-Interactions & Motion
- **Button Press Scale**: An active button shrinks to exactly `scale(0.96)` over `150ms` with an `ease-out` curve. A disabled button **must not** shrink.
- **State Transitions vs Keyframes**: Use a CSS transition or a physics spring for interactive state changes, so the motion can reverse when the cursor leaves mid-animation. Use keyframes only for one-way sequence animations that run once on mount.
- **Instant High-Frequency Interactions**: Typing, table row hover, and tab switching must respond instantly (`<= 150ms`) on the `opacity` or `background-color` property. Do not animate layout properties (`top`, `left`, `width`, `height`).
- **Gate Hover on Pointer**: Put every hover effect under `@media (hover: hover)`. On touch screens an unguarded hover gets stuck (*latched*) and reads as a false selected state.
- **Scroll Containment**: Set `overscroll-behavior: contain` on modal dialogs, drawers, and menu popovers.
- **Progressive Scroll Reveal Choreography (Blur Fade-In & Gentle Rise)**: For landing page sections and narrative cards, apply the `ScrollBlurReveal` pattern (`../maxilun-motion/references/motion-components.md`). Off-screen elements have `opacity: 0; filter: blur(10px); transform: translateY(28px)`. When they scroll into the viewport they transition smoothly to `opacity: 1; filter: blur(0); transform: translateY(0)`. Clear `filter` after the animation ends and always respect `@media (prefers-reduced-motion: reduce)`.

### 1.5 Production Card Container Standard (Anti-Neon Outline & Anti-Status Theater)
- **Neutral Hairline Border, Not a Neon Line (`CMP-018`)**: A card container border must be neutral, 1px, low opacity (`oklch(1 0 0 / 0.08)` in dark mode, `oklch(0 0 0 / 0.08)` in light mode). **Never wrap the card perimeter in a high-saturation/neon border** (`border-cyan-500`, `border-purple-500`). Use the accent color only as a status dot or a small active indicator, never as a fence line around the card.
- **Reject Radial Glow Blobs Behind Cards (`CMP-019`)**: Do not place a large blurred circle (`blur-3xl bg-cyan-500/20`) behind a card to make it look "lit". Card depth must come from the surface tone difference (`Surface` vs `Elevated`) and a subtle contact shadow.
- **Reject Fake Telemetry & Status Theater**: Do not attach static fictional labels such as `// 60 FPS`, `• ONLINE`, `• PING: 0.1ms`, `SYSTEM NORMAL` without a real streaming data source (`CMP-020`). When you show socket/connection status, reflect the real state (`CONNECTED`, `CONNECTING`, `DISCONNECTED`) with text + a matching semantic icon.
- **Ban on Pastel Rounded Icon Square Boxes (`CMP-021`)**: Do not place an icon inside a soft pastel rounded box (`bg-blue-50 text-blue-600 rounded-lg p-2.5`, `bg-indigo-50`, etc.) as a decorative badge or empty state visual. This is a generic AI template hallmark. Use clean monochrome `text-foreground` / `text-muted-foreground` SVG vector icon, or render on a calibrated neutral surface step (`bg-surface-elevated border border-border`).

### 1.6 Ban on Emoticon/Emoji Pollution in the Interface (`CMP-003`)
- **Strictly Forbidden**: Inserting Unicode emoji characters (`🚀`, `✨`, `🔥`, `⚡`, `💡`, `🎉`, `⭐`, `✅`, `❌`, `⚠️`, `👉`, `💎`, `🌟`, `🤖`, `💬`, etc.) into:
  1. Buttons or navigation links (`<button>⚡ Submit</button>`).
  2. Headings or subheadings (`<h3>⚡ Fast Performance</h3>`).
  3. Hero badges, tags, or chips (`<span>✨ New Feature</span>`).
  4. Feature cards or checklist items (`<li>✅ 99.9% Uptime</li>`).
  5. Table status cells or toast notification messages.
- **Required Vector Standard**:
  - Replace them with geometric monochrome SVG vector icons (`stroke="currentColor"` / `fill="currentColor"`) from a standard library (Lucide, Radix, Heroicons) or calibrated inline SVG.
  - For checklists: use the SVG checkmark path `<svg class="w-4 h-4 text-emerald-500" ...><path d="M5 13l4 4L19 7" .../></svg>`.
  - Every icon must pass the *1-Bit Monochrome Test*: it stays clear and legible when converted to pure 1-bit black and white without color or shadow.

### 1.7 Dual-Theme Symmetry Invariant & Canvas Sync (`CLR-009` & `MOT-005`)
- **Zero Dark-Trap Lock**: Every component with a custom dark background (for example a CTA card with a dark `#030509` radial gradient, or a terminal container) **must define a symmetric inverse rule** under `[data-theme="light"]`. Never let text inherit a dark `var(--text)` on top of a dark background.
- **Canvas Theme Sync Protocol**: HTML5 2D/3D `<canvas>` elements do not inherit CSS variables automatically. Every canvas drawing call (`fillText`, `strokeText`, `strokeStyle`) **must detect the active theme** dynamically:
  ```javascript
  const isLight = document.documentElement.getAttribute('data-theme') === 'light';
  ctx.fillStyle = isLight ? '#090d16' : '#f1f5f9';
  ctx.strokeStyle = isLight ? 'rgba(0, 0, 0, 0.2)' : 'rgba(255, 255, 255, 0.22)';
  ```
- **Third-Party Mockup Symmetry**: Mockups of real interfaces (such as a WhatsApp chat or a mobile frame) must have an authentic light variant (`#efeae2` wallpaper, `#d9fdd3` outgoing bubble, `#111b21` text) when the app switches to the light theme.

---

## 2. Mathematical Typography Standard

### 2.1 Role-Based Type Scale
Define sizes with consistent line-height and font-weight pairs:
- **Display**: `font-size: 40px–56px`, `line-height: 1.1–1.15`, `letter-spacing: -0.02em` to `-0.04em`.
- **Heading 1–2**: `font-size: 24px–32px`, `line-height: 1.2–1.25`, `letter-spacing: -0.01em` to `-0.02em`.
- **Heading 3–4**: `font-size: 18px–20px`, `line-height: 1.3–1.35`, `letter-spacing: -0.005em`.
- **Body Text**: `font-size: 15px–16px`, `line-height: 1.5–1.6`, `letter-spacing: 0`.
- **Technical/Micro Label**: `font-size: 11px–13px`, `line-height: 1.25`, sentence case in secondary text role (no wide-tracked all-caps).

### 2.2 Line Length Limit & Wrapping
- **Cap the Measure**: Limit the line width of reading text to **60–75 characters** (`max-w-[65ch]`). Lines that are too long tire the eye on the return to the start of the next line.
- **Text Wrapping**:
  - Set `text-wrap: balance` on display titles and short headlines (at most 4 lines).
  - Set `text-wrap: pretty` on narrative paragraphs to prevent a single word hanging on the last line (*widow*).
- **Tabular Number Discipline**: Set `font-variant-numeric: tabular-nums` on every price, time, stopwatch, KPI metric, and numeric table column so digits do not shake (*layout jitter*) when values change.
- **16px Minimum for Mobile Inputs**: Font size on `<input>`, `<select>`, and `<textarea>` elements on small-screen devices must be at least `16px` (`text-base sm:text-sm`). This prevents iOS Safari from forcing an auto-zoom that breaks the layout.

### 2.3 True Typographic Characters
Store text in natural characters and use real typographic punctuation:
- Curly quotes: `“` and `”` (not straight quotes `"` `"`).
- Single ellipsis: `…` (not three plain dots `...`).
- Dashes: en dash `–` for number ranges (`10–20 MB`), em dash `—` for a clause break in a sentence.
- Non-breaking space: `&nbsp;` between a number and its unit (`10&nbsp;MB`, `24&nbsp;px`, `⌘&nbsp;K`).


### 2.4 Anti-Text-Gradient & Typeface Character Selection
- **Hard Ban on Text Gradients**: Never use a rainbow text gradient effect (`bg-clip-text text-transparent bg-gradient-to-r ...`) on a hero headline. Titles must use solid ink with high contrast ($\ge 4.5:1$, on dark themes $\ge 7:1$). A text gradient is the signature of a cheap generic AI template and it hides weak typography.
- **3-Layer Font Separation (Font Layering)**:
  1. *Display / Headline Face*: A typeface with strong structural character (for example: *Geist*, *Cabinet Grotesk*, *Instrument Sans*, *Plus Jakarta Sans*, or *Manuka* for firm editorial) with tight negative tracking (`-0.02em` to `-0.04em`).
  2. *Technical / Protocol Monospace*: A sharp monospace (for example: *JetBrains Mono*, *Geist Mono*, *Fira Code*) for protocol specifications, WebSocket state, JSON payloads, token IDs, and timestamps.
  3. *Functional Sans*: A neutral sans for paragraphs, navigation, and buttons with proportional line-height (`1.5–1.6`).
- **Eliminate the Hero Pill Capsule (`CMP-015`)**: Do not print an oval pill capsule (`rounded-full`) with `•` bullets (`• SIGNAL PROTOCOL TCP • ...`) above the H1. If you need a category marker, use plain text without a capsule (a small editorial eyebrow, spaced capitals, no box border) or merge it directly into the title sentence.

### 2.5 Typographic Anti-Overflow Discipline & Fluid Mobile Scale (`TYPO-009`)
- **Fluid Heading Scaling**: Do not use a large static display text size (e.g. `text-5xl` or `text-6xl`) without a mobile breakpoint. On phone screens $\le 375\text{px}$, long words such as *"Infrastructure"* or *"Communication"* break roughly or get cut off beyond the canvas. Use a stepped breakpoint scale (`text-2xl sm:text-4xl md:text-5xl lg:text-6xl`) or CSS clamp: `font-size: clamp(1.875rem, 1.25rem + 3.125vw, 3.75rem);`.
- **Word Wrapping & Breakage**: Set `break-words` or `overflow-wrap: anywhere` on hero titles and component headings.
- **Monospace, Token & URL Overflow**: Every long string without natural spaces (WhatsApp JID, token hash, endpoint URL, cURL command) **must** carry the `break-all` class or sit inside a bounded container with isolated horizontal scroll, `overflow-x-auto`.
- **Flex & Grid Child Truncation Invariant**: Every flex/grid child that holds truncated text (`truncate` / `text-ellipsis`) **must include `min-w-0`** (`min-width: 0`). Without `min-w-0`, the CSS flexbox specification keeps the original text content width and pushes the container past the screen canvas.
---

## 3. Palette System & Semantic Color (Systematic Color Ramps)

### 3.1 Ramps, Not Random Colors
Build the color system on *ramps*: one neutral ramp, one main accent ramp, and functional status ramps (success, warning, danger). Do not create tokens for roles that are never rendered on screen.

### 3.2 Primitive vs Semantic Separation
- **Primitives** name physical values: `--slate-900: oklch(20% 0.01 250)`. Never call them directly in UI components.
- **Semantic Tokens** name jobs: `--color-surface-base: var(--slate-900)`. UI components may call only these semantic tokens.

### 3.3 One Primary Action Rule (One Primary Action per View)
When a *solid fill* color signals the main action:
- **Exactly one primary action** gets the solid accent color treatment on a single screen/viewport.
- Companion buttons must be neutral, outline, or ghost.
- **Do not** place two bold, contrasting pill buttons side by side in the hero section, where they compete for the visitor's attention.

### 3.4 Real Contrast Measurement
Measure foreground contrast against the actual background color rendered behind it (not only against the page background):
- Normal text (<18px regular): at least `4.5:1` (WCAG AA).
- Large text (>=24px or >=18.67px bold): at least `3:1`.
- Control component boundaries & meaningful icons: at least `3:1`.

---

## 4. Spatial Rhythm & Layout

### 4.1 2x Spacing Rule (Group with Space, Not Lines)
Group elements with spacing first, background contrast second, and divider lines only as the last resort when spacing is not enough:
- The gap between element groups is at least **2 times** the gap between elements inside the same group.
- If elements inside a group are `8px` apart, the gap between groups is `16px` or `24px`.

### 4.2 Align to Shared Edges
- Choose a small number of vertical edge lines and align elements to them.
- **Reject the Center-Everything Mold (Anti Center-Everything Cascade)**: Avoid composing the whole page as a uniform stack where everything is centered (Overline centered -> H2 centered -> Subtitle centered -> Card centered).
- Choose a structure that follows the nature of the content: start-edge alignment (*text-align: start*), a split composition with a living product artifact, a comparison table, an editorial sequence, or an asymmetric grid (`2:1`, `1:2`) when each panel carries a different functional weight.

### 4.3 CSS Logical Properties
Use logical properties for every directional dimension:
- `margin-inline-start`, `margin-inline-end`, `padding-block`, `inset-inline-start`, `text-align: start`.
- Avoid `width: 100vw` (it triggers horizontal scroll because it counts the desktop scrollbar; use `width: 100%`).
- Avoid `height: 100vh` on full-height containers on mobile (use `height: 100dvh` so the browser address bar does not cover content).


### 4.4 Production Hero Section Engineering (The Living Hero vs "Plain Turned Strange")
- **Diagnosis of the "Plain Turned Strange" Syndrome**: An AI model produces a boring (*plain*) hero because it uses the lazy centered stack (Pill $\to$ H1 $\to$ Subtitle $\to$ 2 Buttons). The result feels empty, so the model patches it with odd decoration: rainbow gradient text, neon glow, and an empty 3D particle canvas (*turned strange*).
- **Production Hero Execution Rules**:
  1. **Layout derived from the craft Brief**: Do not default to one hero shape. For developer products, work tools, API gateways, and B2B, the Brief commonly resolves to an asymmetric split (50/50 or 55/45). In that case the left side has start-aligned text (*text-align: start*), a solid display title, and exactly 1 primary action button.
  2. **The Living Engine (Not a Cartoon Image / 3D Gimmick)**: The right side of the hero holds a real working object the user can interact with:
     - *Messaging Gateway*: A real WhatsApp pairing terminal + live WebSocket JSON event stream with the `messages.upsert` event and p95 latency.
     - *Cloud / Developer Tools*: Switchable cURL / TypeScript SDK tabs + real JSON response output.
     - *Fintech / Ledger*: An interactive fee / transaction calculation card.
  3. **Pure Editorial Eyebrow**: Category metadata appears as plain text without a rounded-full capsule, without a border, without `•` bullets (`font-mono text-xs uppercase tracking-wider text-muted`).
  4. **Quick Install Copy (One-Click CLI)**: Beside the primary action button, include a compact terminal command copy block (`$ npx aetherlink@latest` or `$ docker run ...`) instead of a second button that competes for attention.

### 4.5 Responsive Navbar Standard & Mobile Ergonomics (Anti-Navbar Bloat `LAY-015` & `LAY-016`)
- **Strict Mobile Navbar Height ($\le 64\text{px}$)**: Navbar height on a mobile viewport must stay within **56px–64px** (`h-14 sm:h-16`). A mobile navbar swollen to $> 64\text{px}$ eats the upper half of the screen.
- **2-Element Mobile Navbar Composition**: On phone screens (`< 768px`), the navbar may show exactly 2 elements:
  1. *Left*: Logo or short brand name.
  2. *Right*: Exactly 1 menu trigger (hamburger button or 1 short action).
  - Desktop text menu links **must be hidden** on mobile (`hidden md:flex`). Never let them overflow or stack into two rows.
  - Hide desktop CTA buttons ("Start Trial", "Open Console") on mobile or reduce them to a compact icon without long text.
- **Mobile Drawer & Scroll Lock**: The mobile drawer menu must have:
  - *Scroll Containment*: `overscroll-behavior: contain` on the backdrop and the drawer so the page behind does not scroll along (*background scroll chaining*).
  - *Accessibility*: `aria-expanded="true/false"`, close on the `Escape` key, and focus return to the hamburger trigger.
- **Zero Horizontal Scrollbar (`LAY-016`)**:
  - Never use `width: 100vw` (always use `width: 100%` so the desktop scrollbar width is not counted).
  - Horizontal container padding on mobile is capped at `px-4 sm:px-6` (`px-12` and `px-16` are forbidden on mobile).
  - Every card and layout container must have `max-w-full`.

### 4.6 Anti-Symmetrical Dashboard Metric Strip & Anti-Pill Proliferation Mandate (`LAY-017` / `CMP-022`)
- **Ban Symmetrical 4-5 KPI Metric Strips (`LAY-017`)**: Slicing the dashboard into 4 or 5 identical small boxes (`grid-cols-4` or `grid-cols-5`) with a number and an invented delta is the primary hallmark of generic dashboard slop. Dashboards MUST use an Asymmetric Bento Grid (8:4 or 7:5 anchor ratio) with a real visual data chart (AreaChart/BarChart) in the 8-col Spotlight card and an operational work queue or tabular ledger in the companion container (`references/bento-dashboard-recipes.md`).
- **Ban Pill Badge Proliferation & Pill Overload (`CMP-022`)**: Scattering `rounded-full` pill capsules across the screen for every status label, mode, tag, or button (`[LIVE]`, `[HOST]`, `[AI]`, `[VALID]`, `[NORMAL]`), turning the interface into a noisy pill matrix. Maximum 2 functional status pills per screen. Status should be expressed by plain typography, tabular numerals, subtle borderless tags, or a single 6px active dot indicator.
---

## 5. Interface Copy & Product Language (Product Writing)

### 5.1 Domain Terminology Inventory
Before writing interface text:
- Make a list of standard terms: do not use "Project" in the menu but "Workspace" in notifications.
- Use real technical terms that fit the operational domain, not invented science-fiction metaphors (avoid calling a WebSocket engine a *"3D Virtual Space Architecture"* or *"Chamber 01"*).

### 5.2 Buttons Led by a Concrete Verb
- Start every button with a specific action verb: *"Open Session"*, *"Copy Command"*, *"Send Invoice"*, *"Save Changes"*.
- Avoid generic buttons: *"OK"*, *"Explore"*, *"Learn More"*, *"Get Started"*, *"Click Here"*.

### 5.3 Errors That Solve, Right Beside the Failure
An error message is a repair guide placed beside the input that failed:
- **Bad**: *"Oops! Something went wrong."* or *"Invalid password."*
- **Correct**: *"Password must be at least 8 characters and contain 1 number."*
- Do not blame the user and do not overuse exclamation marks.

### 5.4 Undo Beats a Confirmation Dialog
For reversible actions (archive data, delete to trash), run the action immediately and offer an **Undo** option in a toast notification for 5–8 seconds. Use a modal confirmation dialog only for permanently destructive actions that cannot be recovered.

---

## 6. Cross-Discipline Review Protocol & Severity Ladder

### 6.1 Severity Ladder
- **HIGH**: Blocks the user's task, creates a data-loss risk, misleads the flow, or violates any of the 13 Escalation Triggers.
- **MEDIUM**: Reduces efficiency, damages the visual hierarchy, or is inconsistent with the design system.
- **LOW**: Isolated cosmetic polish.

### 6.2 Thirteen Absolute Escalation Triggers (13 Escalation Triggers — HIGH on Sight)
If any of these 13 conditions is found, the finding is automatically **HIGH** and **BLOCKS (BLOCK)** the interface release:
1. An interactive control without an accessible name (`aria-label` / `<label>`).
2. A keyboard-reachable control without a visible focus ring (`:focus-visible`).
3. An action path reachable by mouse pointer but not by keyboard.
4. Movement or scale animation, or autoplay media, that ignores `prefers-reduced-motion`.
5. Content or controls that are cut off, overlapping, or unreachable at 320px width or 200% zoom.
6. Text or interactive control contrast ratio that fails against the rendered background (<4.5:1 / <3:1).
7. System status or meaning communicated through color alone, without supporting text/icon.
8. A destructive action without clear confirmation or an *undo* mechanism.
9. *Truncated* text without a way to see its full value (tooltip/expand).
10. Important content or controls hidden beyond the scroll boundary without a visual hint (*peek cue*).
11. An error message without a recovery action hint for the user.
12. The semantic danger color used for a non-destructive action.
13. A state change indicated only by animation, leaving no static visual trace (color/icon/label) once the animation ends.

---

## 7. Detection & Correction Table Before You Finish

| Detected Pattern | Required Correction |
|---|---|
| Parent card and child element share the same `rounded-*` | Apply the concentric formula: $\text{radius}_{\text{child}} = \text{radius}_{\text{parent}} - \text{padding}$ |
| Capsule badge floating above the hero title (`• BADGE •`) | Remove the cliché capsule badge; move the context into an editorial eyebrow or the title |
| Every page section is centered (Overline -> H2 -> centered Card) | Change to a layout derived from the craft Brief, such as start-edge alignment or a `2:1` grid |
| Two pill buttons side by side in the hero section competing for attention | Apply the 1 primary action rule; make the second button a neutral button/link |
| Strip of 4 uniform KPI metric boxes with static percentages | Replace with an operational telemetry panel or a real workflow queue |
| Symmetrical 4- or 5-card metric strip (`grid-cols-4` / `5`) | Deploy an Asymmetric Bento Grid (8:4 anchor) with real SVG AreaChart (`LAY-017`) |
| Pill badge proliferation / pill overload (`rounded-full` > 2) | Use plain typography, tabular-nums, or a single active status dot (`CMP-022`) |
| Fake science-fiction terms (*"Chamber 01"*, *"3D Virtual Space"*) | Use real technical terms (*"Connection Socket"*, *"Session Store"*, *"Webhook Stream"*) |
| `transition: all` or `transition-all` | Write the specific properties: `transition-property: transform, opacity` |
| `:active` without a `:disabled` exclusion | Add `:not(:disabled):active` or `enabled:active:` |
| Interactive control with touch size `< 44x44px` on mobile | Add padding or a pseudo-element touch target of at least 44x44px |
| Form input `< 16px` on mobile devices | Use `text-base sm:text-sm` to prevent forced zoom in iOS Safari |
| Modal component without `overscroll-behavior: contain` | Add `overscroll-behavior: contain` |
| Rainbow text gradient on a title (`bg-clip-text text-transparent`) | Replace with a solid high-contrast ink color ($\ge 7:1$ on dark themes) |
| Tagline pill capsule with bullets (`• TAG 1 • TAG 2 •`) above the H1 | Remove the capsule; use a plain-text editorial eyebrow without border or merge it into the title |
| Fake 3D particle/mesh canvas on a gateway/backend API product | Replace with a live operational console (live WebSocket stream, QR pairing status, JSON inspector) |

---

## 8. Protocol for Dismantling Design System Locks in a Redesign (Dismantling Legacy Design System Locks)

When the user asks for a **redesign**, the biggest AI model failure is *The Legacy Design Lock Trap*. The model detects dull old variables/layout but is afraid to delete them, so it only patches local utilities in component files. The UI/UX stays "the same as before" because its visual foundation is never replaced.

### 8.1 Taxonomy of the 5 Design System Locks (Design Locks)

1. **Token & Variable Lock (`SYS-001`)**:
   - *Form*: `:root` variables, CSS custom properties, or a Tailwind `@theme` that pin color to a generic slate palette (`#3b82f6`, `--background: #f8fafc`, `--border: #e2e8f0`).
   - *Impact*: Traps the interface in a cold, boring aesthetic with no domain character.
   - *Required Action*: Delete the old tokens in the root stylesheet (`globals.css` / `theme.css`); redefine an OKLCH color ramp from the physical materials of the product domain (`--hue-neutral`, `--hue-accent`, `color-scheme`).

2. **Shell & Layout Wrapper Lock (`SYS-002`)**:
   - *Form*: A global wrapper in `layout.tsx`, `App.tsx`, or `index.html` such as `<div className="container mx-auto max-w-7xl px-4 py-8">`, or a hardcoded background on `<body>`.
   - *Impact*: Chokes the new layout composition and forces all content into a narrow, rigid container.
   - *Required Action*: Open the wrapper container; provide a flexible canvas layout for an upper-half task hierarchy, a *split artifact*, or an *operational ledger*.

3. **Component Primitive Lock (`SYS-003`)**:
   - *Form*: Old shared components (`<Card>`, `<Button>`, `<Input>`) that force a pale `1px solid #e2e8f0` border, a uniform radius without concentricity, or flat padding.
   - *Impact*: Every newly rendered element automatically inherits the obsolete style.
   - *Required Action*: Update the component primitives to the exact concentric radius formula, transparent layered elevation (*layered box-shadow*), and the 1 primary action rule.

4. **Typography Lock (`SYS-004`)**:
   - *Form*: Font family pinned to a plain system sans or Inter with no display role with character, no `60–75ch` measure limit, and shaking digits without `tabular-nums`.
   - *Impact*: Flat reading hierarchy and visual fatigue for users.
   - *Required Action*: Pair a display typeface with domain character + a functional sans, set `text-wrap: balance` on titles, and require `font-variant-numeric: tabular-nums` on numbers.

5. **Zombie Style Lock & Styling Collisions (`SYS-005`)**:
   - *Form*: Old CSS files, unused CSS modules, old utility classes, or nested selectors that override each other at random.
   - *Impact*: Visual conflicts, flicker, or new rules losing on specificity.
   - *Required Action*: Do a *Clean Cutover*: fully delete the old styling code that the redesign made obsolete. Never leave zombie CSS shims behind.

### 8.2 4-Stage Clean Cutover Execution Protocol

| Stage | Concrete Action | Typical Target Files |
|---|---|---|
| **1. Scan & Isolate** | Map the `:root` variables, the `layout.tsx` wrapper, and the component primitives that lock the current look. | `globals.css`, `tailwind.config.*`, `layout.tsx` |
| **2. Root Token Replacement** | Replace the color, radius, and typography tokens at the root with a contextual OKLCH system for the product domain. | `src/app/globals.css`, `src/styles/theme.css` |
| **3. Shell Emancipation** | Open the rigid wrapper container, delete old hardcoded backgrounds on body/html, install the task layout architecture. | `src/app/layout.tsx`, `src/App.tsx` |
| **4. Primitive Upgrade & Purge** | Update the button/card/input components and delete all obsolete old styling code (*clean purge*). | `src/components/ui/*`, old CSS modules |

### 8.3 Patchwork Anti-Pattern (The Band-Aid Redesign Trap)

- **Forbidden**: Adding `!important` or inline style overrides (`style={{ backgroundColor: ... }}`) on child components to work around dull old root tokens.
- **Forbidden**: Redesigning the cards inside a page while leaving the page background at the dull gray `#f8fafc` from the old root layout.
- **Required**: If the old design system shackles the look, **dismantle the lock at its source (root & shell)**. Do not cover it with local patches.

---

## 9. Production Dashboard Engineering & Dashboard Slop Elimination (Enterprise Dashboard Standards)

Dashboards are the area most exposed to AI slop pollution. Automatic generators tend to repeat the same cliché template: 4 static metric cards, a dark Bento from the wrong domain, status dots without text, and emoji-filled buttons.

### 9.1 Eliminating the 5 Classic Dashboard Slops

1. **Clear Out the Floating 4-KPI Strip (`LAY-009` / `LAY-012`)**:
   - *Slop*: 4 identical boxes in the top row with fictional numbers and a `+12.5%` badge without time-range context.
   - *Enterprise Solution*: Use a measured single-row **Operational Status Rail** with a real time-range selector (`1h` / `24h` / `7d`), right-aligned `tabular-nums` figures, and a proportional SVG sparkline.

2. **Layout Architecture Based on the Nature of the Task, Not a Uniform Dark Bento (`LAY-013`)**:
   - *ERP, Accounting, Cashier, Logistics*: Use an **Operational Ledger** (dense table, `40px–48px` rows, neutral sans font, high contrast). Cyberpunk/neon dark mode themes are forbidden.
   - *Observability, Cloud, DevTools*: Use a **Master-Detail Inspector** (entity panel on the left, live telemetry and logs on the right).
   - *Clinic & Reservation*: Use a **Timeline / Calendar Slot Matrix** (focus on time slots and the patient queue).

3. **4-State Discipline on Every Dashboard Panel & Table**:
   - Do not show the dashboard only in its ideal static-data condition.
   - Every panel and table must have a concrete implementation of the 4 states:
     1. *Loading State*: Proportional 1:1 geometric skeleton ($\text{CLS}=0$); an empty spinner floating mid-screen is forbidden.
     2. *Empty State*: A factual reason why there is no data yet + a clear first-action button (for example: *"No transactions yet today · [Create New Transaction]"*).
     3. *Populated State*: Real data with right-aligned `tabular-nums` figures and long text that is safe from overflow (`truncate` + `min-w-0`).
     4. *Error State*: An inline failure message that offers a fix + a *Retry* button.

4. **Accessible Status Indicators (Anti-Color-Only Dot `CLR-004`)**:
   - A green/yellow/red dot must never stand alone. Always pair it with semantic status text (`Active`, `Syncing`, `Degraded`, `Offline`) and a supporting icon.

5. **Clear Emoji from Dashboard Controls (`CMP-003`)**:
   - Never use emoji (`🚀`, `✨`, `🔥`, `📊`, `💳`, `⚡`) on dashboard buttons, navigation tabs, or filter chips. Use standardized geometric monochrome SVG icons.

6. **Eradicate Sterile White-Box Admin Monoculture (`LAY-014`)**:
   - *Slop*: A generic template of floating white rounded card boxes (`bg-white border-gray-200 rounded-xl`) stacked haphazardly onto a light-gray shell background (`bg-gray-50`/`bg-slate-50`), turning an application into an uninspired, off-the-shelf admin template.
   - *Enterprise Solution*: Ground the interface in a declared domain archetype (e.g., Technical Ledger, Warm Swiss Editorial, Deep Space Obsidian). Differentiate structural zones with background step hierarchy, unified border rhythm, or subtle tonal surface transitions instead of generic white card boxes.

7. **Vertical Slice Protocol for Multi-Module Redesigns**:
   - On massive multi-screen revamp mandates, never perform superficial styling patches across dozens of files simultaneously.
   - Re-architect the Root Layout Shell (Sidebar, Header, Main Canvas tokens) and ONE primary workspace view to 100% production completeness first, verify with user, then systematically propagate to secondary views.
