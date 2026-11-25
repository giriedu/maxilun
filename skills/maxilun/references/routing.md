# Routing Detail: Agent Personas and Disambiguation

Loaded by `../SKILL.md` §2 when dispatching agents or when two specialists both seem to fit.

## 1. Agent Personas (21)

Skills hold the knowledge; agents (`agents/<name>.md`, installed next to the skills) are the dispatchable workers that load them. Dispatch an agent by name; give it the skills listed here.

| Agent | Loads skills | Edits |
|---|---|---|
| `maxilun-orchestrator` | `maxilun` | No (chairs, dispatches, synthesizes) |
| `maxilun-scout` | `maxilun-knowledge-graph`, `maxilun-insight`, `maxilun-seo-audit` | No |
| `maxilun-planner` | `maxilun-scaffold`, `maxilun-docsmith` | Docs only |
| `maxilun-architect` | `maxilun-architect`, `maxilun-data`, `maxilun-sentinel`, `maxilun-docsmith`, `maxilun-scaffold`, `maxilun-ai` | Contracts, ADRs |
| `maxilun-ui-designer` | `maxilun-craft` | Yes |
| `maxilun-ui-motion` | `maxilun-motion` | Yes |
| `maxilun-studio` | `maxilun-craft`, `maxilun-motion`, `maxilun-cinecode`, `maxilun-diagrams`, `maxilun-content` | Yes |
| `maxilun-coder-frontend` | `maxilun-frontend`, `maxilun-engineer` | Yes |
| `maxilun-coder-backend` | `maxilun-engineer`, `maxilun-data`, `maxilun-ai`, `maxilun-sentinel` | Yes |
| `maxilun-coder-mobile` | `maxilun-mobile`, `maxilun-engineer` | Yes |
| `maxilun-coder-systems` | `maxilun-desktop`, `maxilun-iot`, `maxilun-network` | Yes |
| `maxilun-maker` | `maxilun-engineer`, `maxilun-game`, any surface no coder owns | Yes |
| `maxilun-verifier` | `maxilun-verify`, `maxilun-deploy` | No (runs proof) |
| `maxilun-ui-reviewer` | `maxilun-verify`, `maxilun-craft` scan gate | No |
| `maxilun-security-auditor` | `maxilun-hunt`, `maxilun-sentinel` | No |
| `maxilun-figcraft` | `maxilun-figcraft`, `maxilun-craft` | Yes |
| `maxilun-automator` | `maxilun-n8n` | Yes |
| `maxilun-coder-ai` | `maxilun-ai`, `maxilun-engineer` | Yes |
| `maxilun-data-engineer` | `maxilun-data` | Yes |
| `maxilun-devops` | `maxilun-deploy` | Yes |
| `maxilun-docsmith` | `maxilun-docsmith` | Docs, specs |

## 2. Fast Disambiguation

- `craft` vs `frontend`: anything that produces or changes what a person sees involves `maxilun-craft` for structure, type, colour, and states. `frontend` handles RSC boundaries, caching, and Server Actions only.
- `motion` vs `craft` vs `cinecode`: interactive web experiences and 3D/WebGL are led by `motion`; interface design, component systems, and UI micro-motion by `craft`; rendered MP4/WebM files by `cinecode`.
- `craft` vs `content`: `craft` owns interface words (labels, buttons, empty states); `content` supplies long copy and brand voice.
- `scaffold` vs `docsmith`: `scaffold` initializes a new project's `docs/` foundation; `docsmith` writes deep per-feature specifications (PRD/RFC, OpenAPI 3.1, ADR, runbook, `llms.txt`).
- `frontend` vs `desktop` vs `mobile`: `frontend` owns the web browser (RSC, App Router); `desktop` owns native OS windowing, C++ Qt, and PowerBuilder; `mobile` owns native Android/iOS, touch-screen lifecycle, and offline store sync.
- `iot` vs `network`: `iot` owns microcontroller firmware, peripheral pins, and sensors; `network` owns MikroTik routers, firewalls, BGP/OSPF routing, and VLAN switching.
- `ai` vs `data`: `ai` owns RAG retrieval pipelines, semantic chunking, prompt evals, and context caching; `data` owns relational physical schema, expand-contract migrations, indexing, and RLS.
- `game` vs `motion` vs `craft`: `game` owns gameplay logic, runtime physics simulation, authoritative netcode, engine shaders, and the GDD; `motion` owns interactive web choreography and WebGL scenes; `craft` leads HUD design, interface layout, and visual tokens.
- `sentinel` vs `hunt`: `sentinel` owns application defence, cryptography, auth/DPoP hardening, and defensive OWASP controls; `hunt` owns proving offensive scenarios from the attacker's view, attack-surface mapping, 7-Question Gate validation, and reproducible evidence bundles.
