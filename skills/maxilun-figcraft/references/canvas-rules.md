# FigCraft Live Canvas: Partitioned Multi-Writer Rules & Protocol

This reference defines the strict invariants for multi-agent collaboration on a live FigCraft canvas over MCP (`127.0.0.1:7979`).

## 1. Mathematical Canvas Boundaries (`parentId` Partitions)

1. The Coordinator / Product Manager creates the root screen container and top-level empty section frames (e.g. `Section_Nav`, `Section_Hero`, `Section_Bento`, `Section_Footer`).
2. Each section frame is assigned an immutable numeric `parentId`.
3. Each sub-agent or UI designer payload must operate exclusively within its designated `parentId`. Targeting nodes outside this subtree or mutating root document attributes is strictly prohibited.

## 2. Selection Independence (`select: false`)

1. FigCraft desktop maintains a single global selection state visible to human operators.
2. Automated agent mutations must never call `select` or depend on active selection.
3. Every `node.create` command inside a `batch` payload must include `"select": false`.
4. Every `set_properties`, `export`, or deletion call must pass explicit numeric IDs via the `ids` array parameter.

## 3. Atomic Batch Mutations

1. Group all mutations for a coherent layout block into a single `batch` payload.
2. Always specify `"onError": "abort"` to prevent partially applied, broken layer trees.
3. Use the `"as"` assignment and `{"$ref": "<name>"}` reference syntax to establish clean parent-child hierarchy in a single network round-trip.

## 4. Prohibition of Global Undo / Redo

1. Undo and redo stacks in FigCraft are document-global.
2. Invoking `undo` during concurrent multi-agent turns rolls back edits across unrelated partitions.
3. When correcting errors, query the node with `get_node` and issue explicit `set_properties` or remove unwanted nodes by specific ID.

## 5. Relative Geometry & Auto-Layout Rules

1. For child elements in freeform frames, `x` and `y` are relative to the parent frame's top-left corner `(0, 0)`.
2. For structured interfaces, use Auto Layout containers (`layout: "vertical"` or `"horizontal"`) with deterministic `gap`, `padding`, `sizingH: "fill" | "hug" | "fixed"`, and `sizingV`.
3. Never use arbitrary floating coordinates when content length is variable (e.g. headings or dynamic copy).

## 6. Maxilun Purity Gate Enforcement

1. Never use Unicode emoji characters (`CMP-003`) in button labels, badges, or headers.
2. Avoid generic 3-column identical card stacks (`LAY-008`). Prefer an asymmetric 8:4 bento or clear hierarchy.
3. Verify typography contrast meets WCAG AAA standards on both light and dark canvas backgrounds.
