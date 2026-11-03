# Maxilun Routing Matrix

Use this matrix to assign **one cohesive primary owner** per deliverable and prevent both trigger collisions and over-routing fragmentation. Attach companions **only** when crossing a hard capability boundary — never activate every adjacent skill by default.

| Request | Primary Owner | Conditional Companions (Only When Needed) | Do Not Activate as Primary |
|---|---|---|---|
| Add a login / auth / webhook endpoint | `maxilun-sentinel` | `maxilun-data` (if schema changes), `maxilun-verify` | `maxilun-content`, `maxilun-craft` |
| Add or refactor a Next.js App Router page | `maxilun-frontend` | `maxilun-craft` (only if new visual system needed), `maxilun-data` (if DB query/schema changes) | `maxilun-cinecode` |
| Create a landing page or product UI | `maxilun-craft` | `maxilun-content` (only for dedicated campaign copy), `maxilun-frontend` (if Next.js RSC wiring needed) | `maxilun-docsmith`, `maxilun-engineer` |
| Redesign generic UI/UX ("ganti UI/UX") | `maxilun-craft` | `maxilun-verify` (3-viewport & a11y proof) | `maxilun-engineer` as design owner |
| Define visual identity, SVG logo, or Brand PDF | `maxilun-craft` | `maxilun-motion` (animated SVG), `maxilun-cinecode` (`<LogoReveal>` MP4/WebM) | `maxilun-frontend` |
| Investigate a slow page, leak, or outage | `maxilun-insight` | `maxilun-knowledge-graph` (caller radius), then `maxilun-engineer` or `maxilun-data` for the fix | `maxilun-verify` as diagnosis owner |
| Design system boundaries or migration plan | `maxilun-architect` | `maxilun-knowledge-graph` (blast radius), `maxilun-data` (expand-contract), `maxilun-sentinel` (STRIDE) | `maxilun-diagrams` as decision owner |
| Create an architecture / sequence / ER diagram | `maxilun-diagrams` | `maxilun-architect` only when structural decisions do not exist yet | `maxilun-engineer` |
| Write an OpenAPI spec, ADR, runbook, or Feature RFC | `maxilun-docsmith` | `maxilun-architect` (missing system contract), `maxilun-craft` (only if spec defines UI screens) | `maxilun-content`, `maxilun-scaffold` |
| Bootstrap initial project context in `docs/` | `maxilun-scaffold` | `maxilun-craft` (only when project includes a user interface) | `maxilun-docsmith` as bootstrap owner |
| Build an interactive motion or 3D WebGL experience | `maxilun-motion` | `maxilun-craft` (visual tokens), `maxilun-frontend` (React lifecycle) | `maxilun-cinecode` |
| Render a programmatic MP4, WebM, or GIF | `maxilun-cinecode` | `maxilun-motion` (choreography), `maxilun-content` (beat script, full productions only) | `maxilun-craft` as render owner |

## Handoff Record

Keep cross-skill handoffs factual and free of ceremonial banners:

```text
Owner: <skill>
Artifacts: <changed files:lines, contract, or decision>
Verification: <command + exit code/output, or [UNVERIFIED] + reason>
Next: <companion skill if a hard boundary remains, otherwise done>
Residual risks: <concrete open risks, if any>
```
