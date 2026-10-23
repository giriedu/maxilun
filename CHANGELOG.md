# Changelog

All notable changes to Maxilun are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [2.1.0] — 2026-10-23

### Changed
- **Namespace unification**: All 17 specialist skills renamed from `msal-*` to `maxilun-*`. Brand and command namespace are now consistent. Old `/msal-*` commands remain as aliases (documented in orchestrator §2) and will be removed in v3.0.0.
- Orchestrator domain map, alias table, and all cross-references updated to use `maxilun-*` as primary namespace.

### Added
- **Security playbook** (`skills/maxilun-sentinel/references/security-playbook.md`): trust boundary catalog (10 types), security test patterns (4 categories, 20+ patterns), cryptographic implementation reference (4 platforms × 4 use cases), secrets rotation protocol with schedule, extended security headers with CSP templates, supply chain tooling matrix, and STRIDE threat model output template.
- **Verify Tier 5 (Security Validation)**: integrated security testing tier in `maxilun-verify`, triggered for PRs touching auth/input/crypto/data storage. References sentinel security playbook.
- **Design reference corpus** (`skills/maxilun-craft/references/design-md/`): 84 real-world brand design system analyses (Stripe, Vercel, Linear, Figma, Apple, etc.) as anti-slop design references.
- **Alias backward compatibility table** in orchestrator: complete mapping of all 17 old `/msal-*` commands to new `/maxilun-*` primaries.
- **Wave vs workflow hierarchy** clarified in orchestrator §5.
- **Scaffold vs specialist decision matrix** added to orchestrator §3 disambiguation.
- **Discovery protocol example** added to `references/discovery.md` §8.
- **Fallback behavior** for missing references documented in orchestrator §6.

### Fixed
- Insight vs engineer debugging overlap: explicit boundary added to disambiguation table.
- `.gitattributes` added for stable line endings across platforms.

---

## [2.0.0] — 2026-10-23

### Breaking
- Shared rules moved from the repository root into `skills/maxilun/references/`. `npx skills add` copies skill folders only, so the old `rules/` directory was never installed and every skill ran without its engines. The root `rules/` directory is removed.
- Removed the non-standard `metadata.rules` frontmatter field. No harness reads it; it advertised an auto-load that never happened.
- Dropped the bare `/msal` trigger from the orchestrator. It collided with every `/msal-*` command.
- Removed all references to external skills (`antislop`, `antislop-code`, `frontend-design`, `brainstorming`, `superpowers`). Nothing in the ecosystem depends on skills outside the 18.

### Added
- Identical `CORE-RULES` block in all 18 skills, verified byte-for-byte by CI. Engines now travel with the skill instead of being pointed at by path.
- `references/discovery.md`: a Wave 0 protocol for unclear briefs (outcome, constraints, non-goals, done criteria), adopted to replace the removed external brainstorming dependency.
- `references/engines.md`: merged canonical detail for the four engines, three protocols, output contract, and integrity rules.
- Evidence-based delivery gate. Each item requires a command output, `file:line`, or measured value; an item without evidence fails instead of being self-certified.
- Real execution binding per platform, including how a parallel wave is actually dispatched and how skill availability is checked before routing.
- Failure handling table: missing specialist, missing tool, failed gate, conflicting recommendations, two rejected iterations.
- Test suite checks for CORE-RULES drift, unresolved reference paths, external-skill references, legacy `rules/` references, duplicate section numbers, and skill size budget.

### Fixed
- `maxilun-craft`: duplicate section numbers (two `## 4.` and two `## 3.`) renumbered; all internal `§N` references remapped.
- `maxilun-engineer`: duplicate `## 6.` renumbered to `## 7.`.
- `maxilun-motion`: removed a list of ten reference files that did not exist.
- `maxilun-craft`: removed invented catalog IDs `B6.37` and `B4.25`, and corrected `A.5` to `A butir 5`.
- Orchestrator claimed 17 specialists while README, installer, and package metadata claimed 18. Now consistently "18 skills: 1 orchestrator + 17 specialists".
- Platform metadata now matches the platforms the installers actually support.
- Installers no longer copy `rules/`, and strip `__pycache__`/`*.pyc` from installs. Uninstallers still clean up v1 rule files left outside skill folders.

---

## [1.1.0] — 2026-10-23

### Improved
- Replaced phrase-first routing with an ordered, evidence-based protocol for explicit commands, requested outcomes, confidence bands, mixed-domain work, and unsupported prompts.
- Made companion skills conditional on the requested deliverable and availability in the active environment.
- Clarified platform capability boundaries and aligned orchestrator metadata with the release version.
- Separated Motion's interactive animation/assets from CineCode's final video rendering; removed mandatory dual outputs and companion dispatch for both skills.
- Corrected unsafe security/database guidance, made quality gates risk-based, clarified prompt examples versus executable project scripts, and aligned package/skill version validation.
- Updated current skill examples and documentation names, and aligned Knowledge Graph usage with its trivial-task and no-indexer fallbacks.
- Refined Knowledge Graph Visualizer (Lens): added semantic node geometries (circles for functions, hexagons for classes/types, squares for modules/files, diamonds for routes/endpoints), layered ink-blue surfaces, copper focus outlines, adaptive label density, and unified 2D canvas / WebGL visual styling.

---

## [1.0.0] — 2026-10-22

### Initial Stable Release

Maxilun launches as a complete 18-specialist AI engineering co-pilot ecosystem, purpose-built for production-grade software development. Every component — from the mandatory Knowledge Graph foundation and 7 Always-On Quality Engines to the specialist routing matrix and MSAL namespace — has been designed, implemented, tested, and verified as a unified, coherent system.

### Ecosystem Highlights

#### 18 Specialist Skills
| # | Skill | Primary Trigger | Engineering Domain |
|:--:|---|---|---|
| 1 | `maxilun` | `/maxilun` | Master Orchestrator — confidence-based routing & multi-specialist wave coordination |
| 2 | `maxilun-knowledge-graph` | `/msal-graph`, `/msal-trace` | Mandatory Code Discovery — AST parser & WebGL 3D/2D visualizer (Lens) |
| 3 | `maxilun-scaffold` | `/maxilun-scaffold`, `/msal-init` | Project Context Scaffolder — generates 10 AI-readable architecture docs in `docs/` |
| 4 | `maxilun-architect` | `/msal-think`, `/maxilun-architect` | System Architecture — C4 Model, Event Storming, ADRs, deep reasoning |
| 5 | `maxilun-sentinel` | `/maxilun-sentinel`, `/msal-security` | Defensive Security — OWASP Top 10, STRIDE threat modeling, crypto, supply chain audit |
| 6 | `maxilun-engineer` | `/maxilun-engineer` | Code Implementation — Test-Driven Development (TDD), 5-WHY debugging, clean refactoring |
| 7 | `maxilun-data` | `/maxilun-data` | Data & Persistence — schema design, zero-downtime migrations, query optimization, RLS |
| 8 | `maxilun-frontend` | `/maxilun-frontend` | Modern Frontend — React Server Components (RSC), Next.js App Router, Server Actions |
| 9 | `maxilun-verify` | `/maxilun-verify`, `/msal-test` | Quality Assurance — Playwright E2E, visual regression, accessibility (a11y), contract tests |
| 10 | `maxilun-insight` | `/maxilun-insight`, `/msal-audit` | Performance Diagnostics — CPU/memory/DB profiling, distributed tracing, leak detection |
| 11 | `maxilun-deploy` | `/maxilun-deploy` | Cloud & Operations — CI/CD pipelines, multi-stage Docker, zero-downtime rollouts |
| 12 | `maxilun-docsmith` | `/maxilun-docsmith`, `/msal-docs` | Technical Documentation — OpenAPI/AsyncAPI contracts, architecture ADRs, runbooks |
| 13 | `maxilun-craft` | `/maxilun-craft`, `/msal-ui` | Design Systems & UI/UX — OKLCH color palettes, WCAG AAA accessibility, 4px grid |
| 14 | `maxilun-motion` | `/maxilun-motion` | Web Motion Design — physics-based animations, Lottie/SVG, kinetic typography |
| 15 | `maxilun-cinecode` | `/maxilun-cinecode` | Programmatic Video — React components as frames, batch headless MP4/WebM render |
| 16 | `maxilun-diagrams` | `/msal-diagram`, `/maxilun-diagrams` | System Visualization — C4, sequence, Event Storming, data-flow diagrams via Mermaid |
| 17 | `maxilun-content` | `/maxilun-content`, `/msal-copy` | User-Facing Copywriting — landing pages, UI microcopy, error states, brand voice |
| 18 | `maxilun-seo-audit` | `/msal-seo`, `/maxilun-seo-audit` | Technical SEO — Core Web Vitals, JSON-LD structured data, crawler readiness |

#### Unified MSAL Namespace (`/msal-*`)
- Standardized slash command prefix across all specialist skills to prevent namespace conflicts with other skill ecosystems.
- MSAL = Maxilun Skill Abstraction Layer.

#### 7 Always-On Quality Engines
Enforced automatically across all 18 skills, non-overridable:
- **Focus Engine** — Executive HUD, task decomposition, persistent subtask tracking (max 3 concurrent).
- **Purity Engine** — Zero AI slop: automatically purges buzzwords, fabricated claims, and empty placeholders.
- **Minimalist Engineering** — Simplicity ladder, native APIs first, minimal valid changes.
- **Clarity Engine** — Explicit technical signaling (`[CONFIRMED]`, `[INFERRED]`, `[UNCERTAIN]`, `[UNVERIFIED]`).
- **Dependency Decision Framework** — Stdlib-first evaluation, bundle size gating, maintenance viability checks.
- **Cognitive Load Reduction** — Naming as documentation, file size ceilings, nesting depth limits.
- **Proactive Communication Rules** — Blocker reporting, no silent failures, explicit assumptions.

#### Mandatory Knowledge Graph Foundation
- Python AST scanner + TypeScript scanner + Generic polyglot scanner.
- Maxilun Lens: Interactive WebGL 3D/2D visualizer with BFS Path Trace and fuzzy search.
- Pre-edit code mapping guarantees exact `file:line` references before any modification.

#### Multi-Platform Support & Universal Agent Compatibility
- Native support for **Claude Code**, **Antigravity IDE & CLI**, **Cursor**, **OpenCode / Codex**, **Zed Editor** (`-a zed`), and **Termul (`termul.dev`)**.
- Fully installable via universal open-source package manager: `npx skills add giriedu/maxilun`.
- Integrated `skills.sh.json` category schema and live installation counter telemetry on [skills.sh/giriedu/maxilun](https://skills.sh/giriedu/maxilun).

#### License
- Released under **Maxilun Source Available License 2.0 (MSAL-2.0)**. See [LICENSE](./LICENSE) for full terms.
