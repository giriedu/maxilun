# Maxilun Skill Contracts

Maxilun is distributed as independent skills through `skills.sh`. Each skill must work alone and may optionally participate in an orchestrated workflow.

## Required contract

Every skill has one primary owner:

- **Owns**: deliverables the skill is responsible for.
- **Does not own**: adjacent work that must be handed off.
- **Inputs**: evidence, context, or artifacts it consumes.
- **Outputs**: concrete artifacts or findings it returns.
- **Handoff**: the next skill and the condition for invoking it.

The primary skill owns the deliverable. Companion skills advise or validate; they do not silently duplicate ownership.

## Ownership map

| Skill | Owns | Does not own |
|---|---|---|
| `maxilun` | routing, sequencing, synthesis, evidence gates | domain implementation |
| `maxilun-knowledge-graph` | code discovery and dependency mapping | architecture decisions or code edits |
| `maxilun-scaffold` | project-context document bootstrap | detailed architecture decisions |
| `maxilun-architect` | system boundaries, contracts, migrations, ADR decisions | final diagrams or implementation |
| `maxilun-sentinel` | application security and trust boundaries | infrastructure deployment ownership |
| `maxilun-engineer` | general code implementation and refactoring | specialist domain decisions |
| `maxilun-data` | schema, migrations, indexes, ORM and query design | general system diagnosis |
| `maxilun-frontend` | React/Next.js runtime and framework behavior | visual direction and brand system |
| `maxilun-verify` | tests, lint, typecheck, build and regression evidence | root-cause investigation |
| `maxilun-insight` | evidence-based diagnosis and profiling | direct implementation |
| `maxilun-deploy` | CI/CD, containers, runtime operations and recovery | application security decisions |
| `maxilun-docsmith` | engineering and operator documentation | user-facing marketing copy |
| `maxilun-craft` | visual system, layout, typography and interaction design | framework architecture |
| `maxilun-motion` | browser and UI motion | final video rendering |
| `maxilun-cinecode` | rendered video artifacts and video pipelines | browser UI animation |
| `maxilun-diagrams` | diagrams derived from known decisions | architecture decisions |
| `maxilun-content` | user-facing copy and microcopy | engineering documentation |
| `maxilun-seo-audit` | technical SEO findings and remediation priorities | general product copywriting |

## Standalone rule

Never require the orchestrator, a local path, a private tool, or another skill to produce the skill's primary output. If an optional companion is unavailable, use a clearly labeled fallback and preserve evidence quality.

## Routing rule

Choose exactly one primary owner per deliverable. Add a companion only when it contributes a named artifact, decision, or verification step. Do not activate every adjacent skill by default.
