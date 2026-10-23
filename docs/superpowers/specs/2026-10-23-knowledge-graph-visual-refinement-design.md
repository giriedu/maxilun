# Knowledge Graph Viewer — Visual Refinement

Date: 2026-10-23

## Goal

Make the graph nodes and their relationships feel deliberate, polished, and professional in both 2D and 3D, while restoring visual richness without decorative emoji, excessive neon, or label clutter.

## Visual direction

Use an “Atlas at night” palette: deep blue ink background, layered slate panels, and restrained teal, blue, and copper accents. Add a faint technical grid and soft edge shading to establish depth; keep the grid subordinate to graph content. Panels may use a light surface separation and soft shadow, not pervasive blur or glow.

## Node language

- Encode symbol categories with a small, consistent set of node shapes in both render modes (functions, types/classes, files/modules, and routes/components).
- Use size for degree/connectivity and shape/color for type so the same visual channel does not carry multiple meanings.
- Render nodes as solid, faceted or softly shaded forms with a fine outline; no bloom halo.
- Give selection a clear focus ring and keep neighboring nodes and edges legible. Labels prioritize selection, hover, and high-degree nodes, with overlap avoidance.

## Motion and controls

Keep directional edge markers continuously active. Use modest size, opacity, and speed so they clarify direction without competing with labels. Preserve the existing 2D default, 3D view, and fly interaction. Avoid automatic camera rotation and perpetual decorative animation.

## Responsive and accessibility

Maintain readable contrast, visible focus/selection states, keyboard fly controls, and compact layouts at narrow widths. Keep color supplementary to shape and labels.

## Acceptance checks

- Node category is distinguishable in both 2D and 3D without relying on color alone.
- Dense graphs remain readable at default zoom; selection and hover remain obvious.
- The background and panels have depth without obscuring graph content.
- No decorative emoji or unrelated ornamental UI symbols are introduced.
- Direction markers remain on, and the 2D default and fly controls remain functional.
