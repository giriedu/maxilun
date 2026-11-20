# Production Component, Mobile Interaction & Iterative Workflow Reference

Companion reference for `maxilun-craft`. It covers the product context structure (`PRODUCT.md`), cross-domain art direction selection, production component specifications, touch-device ergonomics, and cross-viewport checks.

---

## 1. Product Context & Surface Separation (`PRODUCT.md`)

When building a product from scratch, define its functional identity before choosing an aesthetic:
- **Primary Audience & Anti-Audience**: Who uses it daily in the field, on which device (tablet cashier, field phone, analyst's wide monitor), and who is deliberately not the target.
- **Core Task & Success Metric**: Which primary action must finish fast without a mis-click.
- **Surface Separation**: Public pages (*landing/editorial*) may use bolder typographic expression and whitespace than internal operational work screens (*workspace/ledger*), which prioritize density and scanning speed.

---

## 2. Directed Design Iteration Commands (`/maxilun-craft <action>`)

| Group | Verbs | Target of the Change |
|---|---|---|
| **Structure** | `init`, `shape`, `layout`, `app` | Set the product context, domain information architecture, layout hierarchy, and application workspace flow |
| **Character** | `direction`, `typeset`, `colorize`, `bolder`, `quieter` | Choose the art direction, sharpen the type scale, build the contextual OKLCH color ramp, raise or calm the contrast |
| **Resilience** | `distill`, `harden`, `clarify`, `adapt` | Cut wasteful decoration, complete the 4 data states & long-text edge cases, fix microcopy, and tidy responsiveness |
| **Audit** | `audit`, `critique`, `polish`, `review` | Check WCAG contrast, concentric radius, *Escalation Triggers*, and consistency across the 3 screen widths |

---

## 3. Vocabulary of 20 Art Directions for the Craft Brief

Use these archetypes to inform the **Voice** and **Origin** lines of the craft Brief. They provide vocabulary to articulate a deliberate visual direction grounded in the product domain, not a rigid menu to pick from blindly:
| # | Art Direction | Structural & Surface Traits | Fitting Domains |
|---|---|---|---|
| 1 | **Editorial Magazine** | Display typography with character, asymmetric columns, thin rule dividers | Media, news, research reports, essays |
| 2 | **Swiss International** | Objective mathematical grid, firm sans-serif, measured palette | Finance, legal, B2B corporate, architecture |
| 3 | **Neo-Brutalist** | Firm borders (`1.5–2px`), bold color-block contrast, structurally honest | Creative campaigns, independent studios, cultural events |
| 4 | **Japanese Minimalist** | Meaningful negative space (*Ma*), calm earth tones, single-object focus | Health, boutique hospitality, premium craft |
| 5 | **Retro-Futurism** | Sharp technical geometry, controlled phosphor accents on dark fields | Audio/music, creative hardware, games |
| 6 | **Organic Warmth** | Warm cream/stone surfaces, measured soft corners, eye-friendly contrast | Education, psychology/patient-friendly clinics, culinary, F&B |
| 7 | **Industrial Technical** | Numbered indexes, functional monospaced labels, schematic layout | Cloud infra, IoT, manufacturing, developer CLI |
| 8 | **Art Deco Prestige** | Elegant symmetric proportions, warm metal accents, classic-modern typography | Five-star hospitality, watches, fashion |
| 9 | **Scandinavian Functional** | Clear bright surfaces, soft warm wood/gray, high readability | Household retail, family productivity |
| 10 | **Telemetry Dense** | Data-focused dark surfaces, semantic status indicators + icons, tight charts | Cybersecurity SOC, real-time trading, NOC |
| 11 | **Print Archive** | Sharp reading serif, natural paper background, numbered margin notes | Book publishers, libraries, academic journals |
| 12 | **Layered OS Surface** | One layer of functional translucent panel over a solid work field | Cross-platform desktop/productivity apps |
| 13 | **Bauhaus Functional** | Primary geometric shapes that mark different navigation functions | Design education, visual collaboration tools |
| 14 | **Commerce Showcase** | Sharp product media dominates, factual price/variants, instant purchase flow | Marketplaces, food ordering, direct retail |
| 15 | **Monochrome Type-Led** | Type scale and weight form the main hierarchy without busy color | Design portfolios, photography galleries, writing |
| 16 | **Calm Clinical** | Clean surfaces free of visual noise, clear schedule/action hierarchy | Medical clinics, pharmacies, health records |
| 17 | **Operational Ledger** | Dense tables (`4–8px` cells), right-aligned `tabular-nums`, zero decoration | Accounting, ERP, POS cashier, warehouse management |
| 18 | **Guided Step Flow** | Clear stepwise progress with a live result preview beside the input | Complex onboarding, tax/insurance filing |
| 19 | **Flagship Media** | Dramatic open space, full focus on the engineering of a physical product | Automotive, flagship consumer electronics, property |
| 20 | **Tactile Utility** | Responsive spring controls `<150ms`, instant status without page changes | Technical calculators, converters, daily work tools |

### Example: 3 Contrasting Options When the Visual Direction Is Undecided
If you must offer direction choices to the user, present **3 truly different poles** (not 3 dark twins):
- *Clinic/Reservation Product Example*: **(A) Calm Clinical** (`oura.md` / `cal.md` — clear and bright, focus on time slots) vs **(B) Organic Warmth** (`airbnb.md` — warm, patient-friendly) vs **(C) Swiss Precision** (`wise.md` — firm grid, staff schedule density).
- *SaaS/Data Product Example*: **(A) Crisp Light Ledger** (`stripe.md` / `midday.md`) vs **(B) Editorial Knowledge Workspace** (`claude.md` / `notion.md`) vs **(C) Dark Technical Telemetry** (`tailscale.md` / `linear.app.md`).

---

## 4. Production Component Pattern Specifications

### 4.1 Contextual Navigation Architecture (Choose by Product Depth)
Do not install one header type on every site. Choose the pattern that fits the user's mental model:
1. **Focused Content / Task Header** (Landing, Media, Store, Booking): brand on the left, 3–5 real domain destinations, and exactly one contextual primary action button. Do not place a fake `Cmd+K` badge on a site that is not oriented to keyboard commands.
2. **Operational Sidebar Rail** (ERP, B2B, Admin, Clinic Staff): width `240–260px` (collapsible to icon + tooltip), grouped by real domain workflow (e.g. `Patient Queue`, `Medical Records`, `Billing` — not generic buckets without context), with `aria-current="page"` and `tabular-nums` queue counts when factual.
3. **Command-Driven Workspace** (DevTools, IDE, Keyboard-First Analytics): a compact bar with a command palette trigger (`⌘K` / `Ctrl+K`) that fully works, including arrow-key navigation and `Escape`.
4. **Thumb-Zone Mobile Navigation (`< 768px`)**: use a **Bottom Tab Bar (3–4 core destinations)** `56–64px` tall + `env(safe-area-inset-bottom)` for repeat-use apps, or a **Bottom Sheet Drawer** for secondary menus. Avoid full-screen text lists that break the user's orientation.

### 4.2 Layout Compositions That Replace the Cliché Template
Avoid the pattern *centered hero + 3 identical feature cards + 4 fake KPI boxes*. Derive the hero layout from the craft Brief; these are the 4 production hero archetypes to choose from:
1. **The Interactive Split Engine (Developer Tools, API Gateways, B2B Infrastructure)**:
   - 55/45 or 50/50 ratio with start-aligned text (*text-align: start*).
   - Left: firm solid display typeface + 2 sentences of real value proposition + 1 solid primary action button + an install-command copy block (`$ npx aetherlink@latest` or `$ docker run ...`).
   - Right: **The Living Engine** — a real operational working component (not an illustration, not a 3D particle mesh). Example for a messaging gateway: live WhatsApp QR terminal pairing + live WebSocket JSON event stream (`messages.upsert`, p95 latency `18ms`).
2. **The Task-First Hero (Fintech, Booking, Travel, Work Utilities)**:
   - The task interface itself is the hero of the upper half of the screen (for example: a real currency conversion widget with live rates, or a combined date & room picker, instead of a decorative photo).
3. **The Editorial Masthead (Media, Research, Publications, Narrative AI)**:
   - Proportional reading column (`60–70ch`), sharp serif/sans scale contrast, an executive summary readable at once, and a factual reading-time stamp.
4. **Functional Asymmetric Grid (`2:1` / `1:2`)**:
   - Use it only when the main panel really holds a large working component and the companion panel holds secondary controls.

### 4.3 4-Level Surface & Elevation Ladder
Separate planes through subtle surface tone (`Canvas` → `Surface` with a `1px` line or spacing → `Elevated` with a thin contact shadow → `Overlay` for dialogs/sheets). Do not stack heavy shadows on every box.

### 4.4 Form Validation, Data Tables, Dialogs & Toasts
- **Form UX**: validate on `blur`, then update instantly on `input` once the user corrects the value; link the specific fix message through `aria-describedby`; turn on the busy indicator (`aria-busy="true"`) while submission is in progress.
- **Data Tables**: left-align text, right-align amounts/numbers with `tabular-nums`, set `aria-sort` on sortable columns, debounce filters `250–300ms`, and apply a structured transformation on narrow screens (sticky identity column or label-value pair cards).
- **Dialogs & Toasts**: use `<dialog>` with a *focus trap*, background scroll lock (`overscroll-behavior: contain`), `Escape` to close, and focus return to the trigger. Limit toasts to at most 3 at once (`aria-live="polite"`), pause the timer on hover/focus, and provide an *Undo* button for reversible actions.

---

## 5. Mobile Ergonomics & the 3-Screen-Width Check

1. **Mobile Input & Semantic Keyboard**: `<input>`/`<select>`/`<textarea>` font at least `16px`, touch targets `≥ 44×44px` with a gap `≥ 8px`, plus matching `inputmode` and `autocomplete` (`numeric`, `decimal`, `tel`, `one-time-code`).
2. **Accessible Swipe Actions**: every *swipe* action must have an equivalent button/menu reachable by keyboard and screen reader.
3. **Strict Screen-Width Check (`320px` reflow, `360px`, `768px`, `1440px`) & Zero Canvas Leak**:
   - *320px / 360px Phone Screen Leak Test (`document.documentElement.scrollWidth <= window.innerWidth`)*:
     - `100vw` and `w-screen` are forbidden (the #1 cause of a leaking horizontal scrollbar). Use `w-full`.
     - Excessive horizontal padding is forbidden: use `px-4 sm:px-6` (not `px-12` or `px-20` on mobile).
     - Every flex/grid child must include `min-w-0` so text truncation (`truncate`) and `break-words` work without pushing the container wider.
   - *Mobile Navbar Size (Maximum 64px)*:
     - The mobile header must be compact, `56px–64px` (`h-14 sm:h-16`).
     - Hide desktop text menu links below `768px` (`hidden md:flex`).
     - Hide the desktop navbar CTA button or reduce it to a single icon so it does not collide with the logo on narrow screens.
   - *Fluid Heading Discipline & Anti-Typo Overflow*:
     - Display headings must use a stepped responsive scale (`text-2xl sm:text-4xl lg:text-6xl`) or `clamp()`, and carry `break-words`.
     - Monospace, URLs, tokens, and hashes must use `break-all` or sit inside a bounded wrapper with `overflow-x-auto`.
