# Maxilun Purity Catalog

<!-- metadata:
  version: "1.3.0"
  last_updated: "2026-11-02"
  sync_target: "scripts/test-suite.py:BANNED_WORDS"
  origin: "Maxilun Purity Engine"
-->

Catalog of generic patterns to reject across three domains of the Maxilun ecosystem: **Content/Text**, **Interface Design**, and **Code/Interaction**. Use it for evaluation in the context of the product. It is not a blind scanner that rejects a legitimate pattern without looking at its function.

> **Test Suite Sync**: The banned buzzword vocabulary in Section A.5 is aligned with `BANNED_WORDS` in `scripts/test-suite.py`.
>
> **Detection**: Mechanical detection of the visual tells is done by `python ../maxilun-craft/scripts/slopscan.py <path>` (relative to the installed maxilun skill folder). Judgement-only tells are listed in `../maxilun-craft/references/tells.md`.

---

## A. Cliché Patterns in Content & Text

Rewrite the text when it shows one or more of these signs:

1. **Generic with no domain anchor (*Identity Swap Failure*)** — the sentence can be moved to a competitor's product or another industry without changing a word. Name the work object, a real metric, or the user's specific task flow.
2. **Low signal ratio** — many opening sentences but few facts or decisions. One sentence = one new piece of functional information.
3. **Superlative claims without evidence** — promising inflated results with no mechanism or verified number.
4. **Invented statistics or testimonials** — delete numbers such as `"99.9% accuracy"` or `"10,000+ teams trust us"` that have no real source.
5. **Banned Buzzword Vocabulary (`BANNED_WORDS`)** — must not be used as a positive claim:
   - English: `delve`, `tapestry`, `synergy`, `holistic`, `leverage`, `seamlessly`, `robust`, `cutting-edge`, `game-changer`, `revolutionary`, `supercharge`, `dive in`, `elevate`, `empower`, `unlock`, `transformative`, `next-level`, `state-of-the-art`, `best-in-class`, `paradigm shift`.
   - Indonesian: `menyelami`, `merajut harmoni`, `sinergi`, `holistik`, `memanfaatkan secara mulus`, `solusi mutakhir/terdepan`, `pengubah permainan`, `revolusioner`, `meningkatkan ke level berikutnya`, `mari selami`, `memberdayakan`, `membuka potensi`, `transformatif`, `kelas dunia`, `pergeseran paradigma`.
6. **Empty brochure slogans** — stock phrases such as *"Revolutionize Your Workflow"*, *"Unlock Your Potential"*, and, in Indonesian copy, *"Di era digital yang serba cepat"* ("In today's fast-paced digital era") or *"Solusi all-in-one terpercaya"* ("The trusted all-in-one solution").

---

## B. Visual Cliché Patterns & Interface Design Monoculture

Core principle: **reject raw LLM clichés and reject single-mold monoculture as well.** Interface design must come from the character of the subject, the audience, and the product's primary task.

### B1. Typography
1. **Flat hierarchy & uniform generic sans font (`TYPO-001`)** — one plain generic sans font (default Inter with no calibration) used for every level with no role distinction (display vs body vs technical metadata). Pair a display typeface with strong character for headings (`tracking: -0.02em` to `-0.04em`) + a functional monospace for protocol/payload specifications + a measured sans for body text.
2. **Weak text contrast (`TYPO-002` / `CLR-002`)** — pale gray text on a colored surface with a ratio `< 4.5:1`.
3. **Uncalibrated black/gray on a light theme (`TYPO-003`)** — pure `#000000` text on a glaring white background that tires the eye over long reading. *(Legitimate exceptions: high-contrast dark canvases such as `#010102`/`#000000` in references like `linear.app.md` or `vercel.md`, and `1px` media edge lines at alpha `oklch(0 0 0 / 0.1)`).*
4. **Extreme line length (`TYPO-004`)** — reading paragraphs wider than `> 75ch` with no reading-width limit (`max-w-[65ch]`).
5. **Mobile inputs `< 16px` (`TYPO-007`)** — triggers forced auto-zoom on iOS Safari.
6. **Rainbow text gradient on headings (`TYPO-008` / `CLR-008`)** — coloring heading words with a multicolor gradient (`bg-gradient-to-r ... bg-clip-text text-transparent`) to hide dull typography. STRICTLY PROHIBITED. Headings must use solid ink with high contrast ($\ge 4.5:1$, dark theme $\ge 7:1$). Visual authority comes from letterform (*typeface character*), weight contrast, and size scale, not from a cheap gradient effect.
7. **Giant display text with no mobile scale (`TYPO-009`)** — a large static font size (`text-5xl` / `text-6xl` with no responsiveness) or long text (URL, JID, token hash) without `break-words`/`min-w-0`, which pushes long words past the screen canvas at widths $\le 360\text{px}$ (and the `320px` reflow check). Apply fluid scaling (`text-2xl sm:text-4xl lg:text-6xl`) and `break-words`.

### B2. Color & Surface
6. **Default decorative purple-blue gradient (`CLR-001`)** — a `#667eea → #764ba2` gradient or random neon glow with no brand/status meaning.
7. **Oversaturated background (`CLR-005`)** — the main work surface uses high chroma (`chroma > 0.05` in OKLCH) that hurts content readability.
8. **Status conveyed by color alone (`CLR-004`)** — red/green with no accompanying icon or text label.
9. **Bolted-on dark mode (`CLR-007`)** — naively inverting colors with no surface token system and no `color-scheme: dark`.
10. **Dual-Theme Contrast Trap / Black-on-Black Light Mode (`CLR-009`)** — a component with a hardcoded dark background (`#030509` / dark radial-gradient) and no `[data-theme="light"]` theme-inversion rule. When the theme switches to light, the text inherits the dark `var(--text)` (`#090d16`), producing black text on a black background (contrast $< 1.5:1$). Every custom component must have symmetric rules for both themes.
11. **Canvas Out of Sync with Theme / Invisible Canvas Text (`MOT-005`)** — an HTML5 `<canvas>` element renders text or lines in a hardcoded color (`#ffffff` / `#060910`) without checking the active theme (`document.documentElement.dataset.theme`). When the theme flips, canvas text becomes white on white or black on black. Read the active theme state dynamically on every render frame.
### B3. Layout & New Monoculture Hazards
10. **Monotonous center-aligned stack (`LAY-011`)** — the whole page repeats the pattern *centered uppercase overline → centered H2 → centered 2-line subtext → symmetric cards* from top to bottom.
11. **Three symmetric cards with no differentiation (`LAY-008` / `LAY-TEL-02`)** — a `grid-cols-3` of 3 identical boxes with a round icon on top and 2 filler sentences. Replace it according to the nature of the content: an Asymmetric Bento Grid (2:1 anchor layout), an Operational List Ledger with borderless rows and right-aligned `tabular-nums`, or a Master-Detail Workspace.
12. **SaaS Bento Monoculture / Misplaced `Cmd+K` (`LAY-013`)** — copying the dark developer-tools dashboard aesthetic as-is (dark Bento, cold blue-slate palette, `Cmd+K` shortcut badge, monospaced technical labels) for a non-technical product such as a health clinic, food business, education, editorial media, or consumer retail.
13. **Decorative strip of 4 KPI boxes (`LAY-009` / `LAY-012`)** — four static number cards at the top of the page with an invented green percentage (`+12.5%`) and no time context, filter, or follow-up action.
14. **Hero with two twin primary buttons (`LAY-010` / `CMP-017`)** — two solid/pill buttons competing for the main focus. Set exactly one primary action per view; the companion action appears neutral/secondary.
15. **Nested card wrapping (`LAY-001` / `LAY-002`)** — a card inside a card inside a card. Group with spacing first (`2x` the distance between groups compared with inside a group) before adding boxes or lines.
16. **Oversized navbar & overflowing menu on mobile (`LAY-015`)** — mobile navbar height $> 64\text{px}$, desktop links not hidden (`hidden md:flex`), a desktop CTA button covering the logo on touch screens, or a menu drawer without background scroll lock (`overscroll-behavior: contain`).
17. **Mobile horizontal scroll leak (`LAY-016`)** — using `width: 100vw` or `w-screen` (which counts the desktop scrollbar and so leaks on mobile), a fixed width without `max-w-full`, or `px-12`/`px-20` padding on a narrow viewport.

### B4. Components & Navigation
16. **Breadcrumb Header Slop on Flat Surfaces (`HDR-001` / `CMP-001` / `CMP-011`)** — showing fake breadcrumb trails like `Dashboard / Analytics / Overview` or `Home > Products` on a landing page, top-level dashboard, or shallow app. Use a domain masthead with live status dot or an editorial masthead; reserve breadcrumbs strictly for deep taxonomies (`≥ 3` levels).
17. **Decorative tagline pill capsule above the H1 (`CMP-015`)** — a floating badge `• SIGNAL PROTOCOL TCP • MULTI-DEVICE ... •` shaped as an oval pill capsule (`rounded-full`) with `•` bullets above the main heading. This is *the primary signature of an AI template*. STRICTLY PROHIBITED. If technical context or a category must be shown, use plain sentence-case text in the secondary text role (no capsule, no border, no isolated pill background), or fold the context into the headline.
18. **Sci-fi gimmicks & fake 3D canvas (`CMP-016`)** — showing a 3D canvas of floating particles, wireframe cubes, or invented terms (*"3D MESH TOPOLOGY // 60 FPS"*, *"Fire 3D Packet ⚡"*, *"Chamber 01"*) on a backend, API gateway, or messaging infrastructure product. For developer/infrastructure products, the live work artifact (**The Live Artifact**) **MUST be a real operational console**: a live WebSocket stream with real events (`messages.upsert`), real WhatsApp QR pairing status, factual p95 latency, and interactive cURL / REST SDK code blocks.
19. **Marketing badges with no facts (`CMP-002`)** & **Emoji/Emoticon Pollution in Interfaces (`CMP-003`)** — inserting Unicode emoji characters (`🚀`, `✨`, `🔥`, `⚡`, `💡`, `🎉`, `⭐`, `✅`, `❌`, `⚠️`, `👉`, `💎`, `🌟`, `🤖`, `💬`, etc.) as button icons, heading prefixes (`<h3>⚡ Performance</h3>`), feature card icons, checklist bullets (`<li>✅ 99.9%</li>`), hero badges, or table status cells. This is *the most visible signature of AI laziness*: it breaks line-height, renders differently across operating systems (iOS vs Windows), and breaks screen readers. STRICTLY PROHIBITED. Use standardized geometric monochrome SVG vector icons (`stroke="currentColor"` / `fill="currentColor"`) that pass the *1-Bit Monochrome Test*.
20. **Uniform radius ignoring nested geometry (`CMP-004`)** — container and child use the same radius without accounting for concentric padding.
21. **Dead navigation/control elements (`CMP-005` / `CMP-012`)** — a search box, bell icon, filter, or button that does nothing when clicked.
22. **Generic navigation labels with no domain context (`CMP-010`)** — the sidebar only says *Menu 1, Analytics, Reports* without naming the actual business entities.
23. **Saturated neon border on cards (`CMP-018`)** — wrapping a card's perimeter in a high-saturation border (`border-cyan-500`, `border-purple-500`, etc.) with a glowing halo. STRICTLY PROHIBITED. Card containers must use a neutral hairline border `1px solid var(--border)` (`oklch(1 0 0 / 0.08)` in dark mode). Accent color is only for small active-dot indicators.
24. **Radial glow blob behind cards (`CMP-019`)** — placing a large blurred circle (`blur-3xl bg-cyan-500/20`) behind a card to fake a glowing look. Replace it with the *4-Level Surface Ladder* and a thin transparent contact shadow.
25. **Fake telemetry & status theater (`CMP-020`)** — attaching fictional decorative badges (`// 60 FPS`, `• PING: 0.1ms`, `SYSTEM NORMAL`) with no real data source. Show real operational telemetry with a filter or an action.

### B5. Motion & Accessibility
23. **Animating layout properties (`ANI-002`)** — animating `width`, `height`, `top`, `left`, which triggers reflow; use `transform` and `opacity`.
24. **Ignoring `prefers-reduced-motion` (`ANI-003`)** or **autoplaying media with no controls (`ANI-005`)**.
25. **Basic accessibility violations (`A11Y-001..007`)** — a control with no accessible name, an input with no `<label>`, `:focus-visible` removed, or a mobile touch target `< 44x44px` (`LAY-004`).

### B6. Design System Locks & Patchwork Redesign Traps
26. **Obsolete Token & Variable Lock (`SYS-001`)** — keeping old CSS color/spacing tokens (for example: generic slate `#3b82f6`, background `#f8fafc`, `--radius: 0.5rem`) when the user asks for a redesign, so the new interface stays confined to the old dull aesthetic. Replace them at root level (`globals.css` / theme) with OKLCH values from the product's physical domain.
27. **Shell & Layout Wrapper Lock (`SYS-002`)** — leaving the root container (`max-w-7xl mx-auto px-4`, hardcoded `bg-gray-50` on body) to choke the new composition. Rework the container so the $2\times$ spatial rhythm has room.
28. **Zombie Primitive Component Lock (`SYS-003`)** — still using the old `<Card>` or `<Button>` wrapper that forces a flat pale border and uniform radius with no concentric formula. Update the component primitives to the interface engineering standard.
29. **Patchwork Redesign Trap (`SYS-004`)** — editing only leaf JSX or adding inline overrides (`!important` / `style={{...}}`) on top of a broken design system foundation, which produces a UI that looks the same as before.
30. **Two-System Styling Collision (`SYS-005`)** — stacking new styling classes without deleting the conflicting old CSS, leaving zombie classes and layout glitches. Perform a *Clean Cutover* (fully delete the old styling code).

### B7. Studio Score Killers
31. **Twenty Effects With No Signature Moment (`JURY-001`)** — stacking dozens of random micro-animations with no single main interaction (*One Signature Moment*). Reviewers read the noise of effects as a lack of visual confidence.
32. **Scroll-Jacking / Frozen Scroll (`JURY-002`)** — fighting mouse-wheel inertia, disabling keyboard keys (`Space`/`PageDown`), or turning off natural scroll inertia on mobile touch devices.
33. **GPU Memory Leak From Permanent will-change (`JURY-003`)** — leaving `will-change: transform, opacity` active permanently in CSS/JS instead of resetting it to `auto` after the animation ends, which exhausts mobile GPU VRAM.
34. **Preloader Covering Ready Content (`JURY-004`)** — an intro screen that holds the user for 3–5 seconds although the HTML content is already ready behind it, which damages the LCP metric.
35. **Homepage-Only Design (`JURY-005`)** — the homepage is polished while inner pages (about, detail, 404, documentation) are left untidy, like a different project. Professional users always test inner pages.
---

## C. Contextual Check Code Summary

Use these reference codes to report design/code audit results precisely (`file:line` + ID + concrete fix):

| Category | ID Range | Main Evaluation Focus |
|---|---|---|
| Typography | `TYPO-001` .. `TYPO-009` | Role-based scale hierarchy, no rainbow text gradient, no mobile overflow, `tabular-nums` |
| Color | `CLR-001` .. `CLR-009` | No clichéd decorative gradient, no excessive neon glow, calm background chroma, `color-scheme` |
| Layout | `LAY-001` .. `LAY-016` | No centered stack, no oversized mobile navbar, no horizontal scroll leak (`100vw`) |
| Components | `CMP-001` .. `CMP-020` | No pill capsule, no neon card border, no fake status theater, concentric radius |
| Motion | `ANI-001` .. `ANI-007` | `transform`/`opacity` only, micro duration `≤250ms`, respect `prefers-reduced-motion` |
| Accessibility | `A11Y-001` .. `A11Y-007` | Accessible name, `<label>` association, `:focus-visible` indicator, semantic heading order |
| Design Locks & Redesign | `SYS-001` .. `SYS-005` | Detect design system locks, delete dull root tokens, open the layout shell, clean cutover |
| Studio Quality & Jury | `JURY-001` .. `JURY-005` | One signature moment, no scroll-jacking, will-change cleanup, inner page consistency |

---

## D. Contextual Evaluation Before Finishing

Before handing over text or interface work, test these three things honestly:
1. **Identity Swap Test**: If the logo and product name are covered, do the structure and language still reflect this product's specific domain, or does it look like a thousand other AI templates?
2. **Subtraction Test**: Is there a card, badge, `<div>` wrapper, or introductory sentence whose removal would make the user's primary task clearer?
3. **Functional Honesty Test**: Does every button, empty/failure state, and number shown on screen actually work and tell the truth?
