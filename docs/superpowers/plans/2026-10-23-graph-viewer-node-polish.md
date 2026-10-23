# Knowledge Graph Viewer Node Polish Implementation Plan

> **For agentic workers:** Execute inline in this thread, one task at a time.

**Goal:** Make graph nodes feel professional and visually distinctive while improving readability in both render modes.

**Architecture:** Keep the single-file viewer architecture. Add one shared semantic node-shape mapping, pass that shape through existing 2D canvas and WebGL buffers, and use matching shape rules in both renderers. Refine background, edge contrast, selected state, and label placement without adding dependencies or changing graph data formats.

**Tech Stack:** HTML, CSS, Canvas 2D, WebGL 2 / GLSL, JavaScript.

---

### Task 1: Add visual depth and controlled contrast

**Files:**
- Modify: `skills/msal-knowledge-graph/graph-viewer/lens.html` palette variables, `BG_FS`, `render2D`, and edge drawing.

- [x] Change the palette to layered ink-blue surfaces with restrained teal, slate, and copper accents.
- [x] Draw a low-contrast technical grid and vignette in the 2D background; match the 3D background to the same palette.
- [x] Replace screen/additive-style 2D edge composition with normal alpha blending; keep selection emphasis semantic and remove unused glow variables.

### Task 2: Encode node types consistently

**Files:**
- Modify: `skills/msal-knowledge-graph/graph-viewer/lens.html` node normalization, `buildGraphBuffers`, `NODE_VS`, `NODE_FS`, and `render2D`.

- [x] Map function-like symbols to circles, class/type/component symbols to hexagons, file/module symbols to squares, and route/endpoint symbols to diamonds.
- [x] Carry the shape code through the WebGL node buffer and use the same geometry in 2D Canvas.
- [x] Use node size only for degree, preserve community color, and give selected nodes a copper focus outline.

### Task 3: Make dense graphs easier to read

**Files:**
- Modify: `skills/msal-knowledge-graph/graph-viewer/lens.html` node drawing and label selection in `render2D` and `updateLabels3D`.

- [x] Prioritize selected and hovered labels, then higher-degree nodes; avoid overlapping label boxes.
- [x] Give labels a restrained dark backing and a readable text contrast.
- [x] Cap moving markers in 2D on large graphs while leaving directional flow continuously active.

### Task 4: Check the finished source

**Files:**
- Review: `skills/msal-knowledge-graph/graph-viewer/lens.html`.

- [x] Extract its inline JavaScript and run `node --check`.
- [x] Run `git diff --check` for whitespace errors.
- [x] Inspect the diff for both render modes, selected-node focus, and preserved 2D default / Fly controls.

## Self-review

The palette and depth are covered by Task 1; type-specific shapes and selection by Task 2; dense labels and always-on flow by Task 3; source validation and preserved behavior by Task 4. No graph format changes, external dependencies, or decorative emoji are part of this plan.
