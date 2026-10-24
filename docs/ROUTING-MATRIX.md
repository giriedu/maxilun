# Maxilun Routing Matrix

Use this matrix to prevent trigger collisions. The first skill is the primary owner.

| Request | Primary | Companions | Do not activate as primary |
|---|---|---|---|
| Add a login endpoint | `maxilun-sentinel` | `maxilun-engineer`, `maxilun-verify` | `maxilun-content`, `maxilun-craft` |
| Add a Next.js page | `maxilun-frontend` | `maxilun-craft`, `maxilun-engineer`, `maxilun-verify` | `maxilun-cinecode` |
| Define a visual system | `maxilun-craft` | `maxilun-content` when copy is needed | `maxilun-frontend` unless runtime work is requested |
| Investigate a slow page | `maxilun-insight` | `maxilun-data` or `maxilun-frontend`, then `maxilun-engineer` | `maxilun-verify` as diagnosis owner |
| Create an architecture diagram | `maxilun-diagrams` | `maxilun-architect` only when decisions are missing | `maxilun-engineer` |
| Create an API README | `maxilun-docsmith` | `maxilun-architect` when the contract is missing | `maxilun-content` |
| Create a landing page | `maxilun-craft` | `maxilun-content`, `maxilun-frontend`, `maxilun-verify`, `maxilun-seo-audit` | `maxilun-docsmith` |
| Render an MP4 or WebM | `maxilun-cinecode` | `maxilun-motion` for motion direction | `maxilun-craft` as implementation owner |

## Handoff format

Every handoff must state:

```text
Primary: <skill>
Artifact: <file, decision, finding, or test result>
Evidence: <source, command, metric, or explicit user input>
Next: <skill or done>
Open questions: <none or concrete questions>
```
