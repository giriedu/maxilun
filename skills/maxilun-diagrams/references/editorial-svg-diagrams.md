# Editorial SVG Diagrams: Hand-Built Single-File Figures

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun-diagrams/SKILL.md"
  origin: "Maxilun Diagrams Engine"
-->

Rules for drawing a diagram by hand as inline SVG inside one self-contained HTML file: when that beats Mermaid, how to pick the diagram type, how to place nodes on a grid, how to route and label connectors, how to theme with CSS variables, and how to prove the result is readable and accessible before delivery.

---

## 1. Mermaid or Hand-Built SVG

Mermaid stays the default (SKILL.md Section 2). Switch to hand-built SVG only when a row below applies.

| Situation | Choose | Reason |
|---|---|---|
| Diagram lives in a Markdown README, RFC, or ADR that renders Mermaid | Mermaid | Diff-friendly text, reviewers edit it in place |
| Diagram changes every sprint with the code | Mermaid | Auto-layout absorbs churn; hand coordinates rot |
| Published figure: blog post, slide, pitch, docs landing page | Hand-built SVG | Layout, emphasis, and spacing are editorial decisions an auto-layout cannot make |
| Emphasis must fall on one path or one node | Hand-built SVG | Auto-layout gives every node equal weight |
| Must match brand tokens or a docs theme exactly | Hand-built SVG | Full control of type, colour, and stroke via CSS variables |
| Needs light and dark rendering from one file | Hand-built SVG | `prefers-color-scheme` on CSS variables; no re-export |
| Target renderer strips scripts and external CSS (email, some wikis) | Plain `.svg` with presentation attributes | No variables, no `<style>` dependence |
| More than about 15 nodes and the reader needs all of them | Neither as one figure | Split: context figure plus detail figures |

Converting an existing Mermaid or draw.io source: keep the facts (nodes, edges, grouping, direction), discard every coordinate and colour, and redraw. Report what was merged or dropped; never silently lose a node and never invent one to balance a layout.

## 2. Draw-or-Not Gate and Type Selection

Before drawing, answer three questions. Any "no" means write prose or a table instead.

1. Does the reader need spatial reasoning (adjacency, order, containment, flow) that text forces them to reconstruct?
2. Are there at least three things with at least two relationships between them?
3. Is there one sentence the figure proves? Write it down; it becomes the `<desc>`.

Pick the type by the question the reader is asking, not by the data you happen to have.

| Reader's question | Type | Layout axis |
|---|---|---|
| What talks to what, across which boundary? | Architecture / container | Columns by trust zone, rows by tier |
| In what order do calls happen, and who waits? | Sequence | Actors on x, time down y |
| Which path does a decision take? | Flowchart | Main path straight down; branches step right |
| What states can this thing be in, and what moves it? | State machine | Happy path on one line; failure states below |
| What contains what? | Nested / containment | Inset rectangles, no arrows needed |
| Who hands work to whom over time? | Swimlane | One lane per owner, time on x |
| Where does data originate, transform, and land? | Data flow | Sources left, sinks right, transforms between |
| What depends on what, including cycles? | Dependency graph | Ranks by depth; cycle drawn as one back-edge |
| How do layers of abstraction stack? | Layer stack | Horizontal bands, most abstract on top |

If two types seem to fit, keep the one whose layout axis carries the sentence from question 3. Never combine two layout grammars in one figure; split instead.

## 3. Density Budget and Splitting

- Aim for a figure a reader can parse in under ten seconds without a legend lookup.
- Hand-built figures get a tighter budget than Mermaid because every node is placed deliberately: about 10 nodes and 14 connectors. Past that, split into an overview with collapsed groups and one detail figure per group.
- Emphasis colour on at most two elements. If more feel important, the sentence from Section 2 is not decided yet.
- Deletion pass before layout: merge two nodes that always appear together; drop an edge whose relationship is already obvious from position or containment; drop a label that only repeats what shape or colour encodes.

## 4. Layout Grid

Coordinates are computed, never eyeballed.

- **Unit**: 8px structural grid with a 4px half-step for tight spacing. Node x, y, width, height, gaps, and padding are multiples of 4. Font sizes and stroke widths are exempt.
- **Ranks and tracks**: assign every node an integer `(rank, track)` first, then derive pixels: `x = margin + track * (nodeW + gapX)`, `y = margin + rank * (nodeH + gapY)`. Moving a node means changing its rank or track, not its pixels.
- **Uniform node sizes per role**: all services one size, all stores one size. Size variation must encode something (importance, scale); otherwise it reads as noise.
- **Gaps carry labels**: the gap between ranks must fit the longest edge label plus padding. Set `gapY >= labelHeight + 24` when a label sits on a vertical segment between ranks.
- **Text fits the box, not the reverse**: estimate width as `chars * fontSize * 0.6` for a proportional sans stack and `* 0.62` for monospace, add 2 x padding, round up to the grid. Wrap at word boundaries into at most two lines with `<tspan x dy>`; a third line means the name is too long.
- **Pixel-crisp strokes**: odd-width strokes on integer coordinates blur; offset them by 0.5 or use even widths.
- **Containers**: a boundary rectangle extends at least 16px beyond its children on every side and keeps its title inside the top padding, never overlapping a child.
- **viewBox fits the content exactly** plus a uniform outer margin; no content outside it, no large dead margin on one side.

## 5. Tokens via CSS Variables

Name colours by role, never by hue. The SVG references only roles, so a theme swap touches one block.

| Role | Used for |
|---|---|
| `--dg-bg` | Page and figure background |
| `--dg-surface` | Node fill; must differ from `--dg-bg` by a visible step |
| `--dg-ink` | Node names, primary strokes |
| `--dg-muted` | Secondary text, default connectors |
| `--dg-line` | Container borders, grid hairlines |
| `--dg-accent` | The one or two emphasised elements |
| `--dg-external` | Third-party systems, outbound calls |

```css
:root {
  --dg-bg: #fbfaf7; --dg-surface: #ffffff; --dg-ink: #1f2430;
  --dg-muted: #5b6270; --dg-line: #d5d2ca; --dg-accent: #b4441c; --dg-external: #2c5d8f;
  --dg-sans: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --dg-mono: ui-monospace, "Cascadia Mono", Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :root { --dg-bg: #16181d; --dg-surface: #1f2228; --dg-ink: #e8e6e1;
          --dg-muted: #a3a8b3; --dg-line: #3a3e47; --dg-accent: #ec8a5e; --dg-external: #7fb0e0; }
}
.node rect { fill: var(--dg-surface); stroke: var(--dg-ink); stroke-width: 1.5; }
.node text { fill: var(--dg-ink); font: 600 14px var(--dg-sans); }
.edge { fill: none; stroke: var(--dg-muted); stroke-width: 1.5; }
.edge.async { stroke-dasharray: 6 4; }
.edge.hot { stroke: var(--dg-accent); stroke-width: 2; }
```

Rules:

- Re-tune each dark value for contrast; do not invert or reuse light values.
- Typography roles: sans for names and titles, monospace only for literal technical strings (ports, paths, commands, SQL types). Monospace for everything reads as costume, not information.
- Use system font stacks by default. A web font requires the brand to demand it, a self-hosted or inlined file, and a disclosed fallback.
- Shape encodes kind (cylinder-ish store, rounded service, plain external), colour encodes emphasis. Never let colour be the only carrier of kind.
- No drop shadows, gradients, glows, or blur filters; a 1-1.5px border separates surfaces. Corner radius stays small (0-8px).
- Brand alignment comes from `maxilun-craft` tokens when the project has them; do not invent a second palette.

## 6. Connector Routing

- **Orthogonal by default**: connectors between nodes not sharing an x or y become right-angle paths with small rounded corners (radius 6-10px, using arc or quadratic segments). Straight lines only when endpoints align. Diagonals are allowed only in radial or cycle figures where the geometry is the message.
- **Draw order**: containers, then connectors, then nodes, then labels. Nodes paint over connector ends so a line never appears to pierce a box.
- **Attach slots**: when several connectors leave or enter the same side of a box, spread them evenly along that side, each at least 12px from its neighbour and from the corner. Two connectors never share one attach point.
- **No shared strokes**: parallel runs keep at least 12px separation. A crossing is acceptable once per connector pair; mark it with a small gap or hop in the lower-priority line. Two or more crossings on one connector means the track assignment is wrong; reorder tracks first.
- **Never route behind a box that is not an endpoint**; move the route into a gap. If geometry truly forbids it, the hidden segment is dashed and the label sits on the visible part.
- **Direction is consistent**: primary flow goes one way (left-to-right or top-down). Return or reply paths take a parallel lane offset from the request, dashed, not the same line with a second arrowhead.
- **Arrowheads**: one `<marker>` per role colour, `orient="auto-start-reverse"`, sized to stroke width (`markerUnits="strokeWidth"`), so heads scale with emphasis.

```html
<marker id="dg-head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6"
        orient="auto-start-reverse" markerUnits="strokeWidth">
  <path d="M0 0 L10 5 L0 10 z" fill="var(--dg-muted)"/>
</marker>
<!-- elbow: down from gateway, right into worker, 8px corner -->
<path class="edge async" d="M160 96 V156 Q160 164 168 164 H312" marker-end="url(#dg-head)"/>
```

## 7. Labeling

- Every edge in an architecture or flow figure carries a verb or protocol label (SKILL.md Domain Overrides). Keep it to about 18 characters; move detail into the `<desc>` or the text alternative (Section 8).
- Labels sit on the longest straight segment, horizontally, never rotated and never along a vertical text axis.
- Give labels a background-coloured halo so the line breaks cleanly around them without a separate mask rectangle:

```css
.edge-label { font: 500 11px var(--dg-mono); fill: var(--dg-muted);
              paint-order: stroke; stroke: var(--dg-bg); stroke-width: 6px; stroke-linejoin: round; }
```

- Keep at least 6px between a label's glyph box and any stroke other than its own connector, and never let a label overlap a node.
- Node text: a name line in the sans role, an optional one-line qualifier (technology, port) in the mono role, smaller and muted.
- Legend only when shape or dash style encodes something the labels do not. Place it as a single row below the figure, outside the drawing area, listing exactly the encodings used.
- A title above the figure states the subject; the claim sentence from Section 2 can be a caption below.

## 8. Accessibility

| Requirement | Rule |
|---|---|
| Name and summary | `<svg role="img" aria-labelledby="<slug>-title <slug>-desc">`; `<title id="<slug>-title">` is the first child; `<desc>` is one sentence about meaning, not geometry |
| Unique IDs | Prefix every `id` (title, desc, markers, gradients if any) with the figure slug; two figures on one page must not collide |
| Text equivalent | For figures with more than about five edges, add a `<details>` or `<figcaption>` listing edges as "A sends X to B" lines; screen readers cannot traverse SVG geometry |
| Text contrast | At least 4.5:1 for labels under 18px against the colour behind them, in both themes |
| Graphic contrast | Strokes and borders that convey meaning reach at least 3:1 against the background |
| Not colour alone | Emphasis or kind also carried by stroke weight, dash pattern, or shape |
| Forced colours | Under `@media (forced-colors: active)` map strokes to `CanvasText` and fills to `Canvas` so lines do not vanish |
| Minimum size | No text under 11px at the figure's intended display width |
| Decorative SVG | Icons that repeat adjacent text get `aria-hidden="true"` |

## 9. Self-Contained Single-File Output

- One `.html` file: inline `<style>`, inline `<svg>`, no external images, stylesheets, fonts, or scripts. It must render identically from a file share, an air-gapped machine, or an email attachment.
- No JavaScript for a static figure. Zoom or pan (SKILL.md Section 5) is optional, inline, under 40 lines, and the figure must be complete with scripts disabled.
- Responsive without distortion: the SVG gets `viewBox` plus `width="100%"` and a `max-width` equal to the viewBox width; wrap it in a container with `overflow-x: auto` and set a `min-width` on the SVG for dense figures so a phone scrolls the figure, not the page.
- Print: `@media print` forces the light palette and removes interactive controls.
- Standalone `.svg` deliverable: same SVG element, with `xmlns` declared and the `<style>` moved inside the SVG; drop `prefers-color-scheme` if the consumer is an image tag that ignores it, and test it.

```html
<figure class="dg">
  <h2>Checkout request path</h2>
  <div class="dg-scroll">
    <svg viewBox="0 0 640 280" width="100%" style="max-width:640px" role="img"
         aria-labelledby="checkout-title checkout-desc">
      <title id="checkout-title">Checkout request path</title>
      <desc id="checkout-desc">The storefront calls the order API, which writes to the database and queues a payment job.</desc>
      <!-- defs, containers, edges, nodes, labels in that order -->
    </svg>
  </div>
  <figcaption>Payment runs asynchronously; the API never waits on the gateway.</figcaption>
</figure>
```

## 10. Evidence-Gated Review

Delivery requires evidence, not a self-ticked list. Render the file in a headless browser at its intended width (and at the dark scheme), look at the screenshot, and run a geometry probe in the page context:

```js
// Reports overlapping text and labels that collide with node boxes.
const boxes = [...document.querySelectorAll('svg text, svg .node rect')]
  .map(el => ({ el, r: el.getBoundingClientRect() }));
const hit = (a, b) => a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
const clashes = [];
for (let i = 0; i < boxes.length; i++)
  for (let j = i + 1; j < boxes.length; j++) {
    const a = boxes[i], b = boxes[j];
    if (a.el.closest('.node') && a.el.closest('.node') === b.el.closest('.node')) continue;
    if (hit(a.r, b.r)) clashes.push([a.el.textContent || 'rect', b.el.textContent || 'rect']);
  }
clashes;
```

Decision rules for the result:

| Observation | Action |
|---|---|
| Any clash from the probe | Fix spacing or reroute; re-run. Not deliverable. |
| Text clipped by the viewBox | Expand the viewBox or shorten the text. |
| A label visually closer to another connector than its own | Move the label to its own longest segment. |
| A connector passes behind a non-endpoint node | Reroute through a gap (Section 6). |
| More than two accent elements | Remove emphasis until the Section 2 sentence alone is highlighted. |
| A node or edge is unlabeled or has no source fact | Label it from repository evidence or delete it. |
| Contrast below Section 8 thresholds in either theme | Adjust the token, not the single element. |
| The figure could be a three-column table | Replace it with the table. |
| Over budget (Section 3) | Split; do not shrink font size to fit. |

Report what was checked and how (`[CONFIRMED]` for rendered and probed, `[UNVERIFIED]` if no browser was available).

## 11. Patterns Rejected

- **Huge catalogues of diagram types in one skill.** Dozens of type guides inflate the skill and blur ownership; Maxilun keeps a short type table (Section 2) and routes charts and data visualisation to the owning skill.
- **Remote font links in a "self-contained" file.** A font CDN makes the file depend on the network and leaks a request on every open; Maxilun uses system stacks or inlined fonts.
- **Mandatory first-run brand interview.** Blocking on styling questions violates Focus and Agency; read existing tokens from the repository (via `maxilun-craft`) and state the assumption instead.
- **Decorative variants (sketch filters, faux terminal chrome, glow).** They add pixels without information and fight the purity rule.
- **Checklists ticked by the author.** Every review item maps to an observable check (Section 10) or it is not claimed.
