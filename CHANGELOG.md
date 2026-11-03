# Changelog

All notable changes to Maxilun are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Enhanced
- **Decision Architecture, Anti-Monoculture & Zero-Ceremony Overhaul**:
  - Replaced passive multi-turn interview loops and ceremonial emoji HUD/gate templates (`FOKUS`/`TINDAKAN`/`DELIVERY GATE`/`Parking Lot` and self-checked `- [ ]` blocks) across all 18 skills with **Repo-First Agency** and **Reversibility-Gated Decision Triage** (execute Type 2 reversible work directly from repo evidence; limit Type 1 irreversible clarification to at most 1 batched turn).
  - Eliminated pseudo-quantitative decision theater in `maxilun-architect` (removed LLM-invented `1–5` weighted score matrices and forced strawman options) in favor of invariant verification, failure-mode stress testing, Deep Modules seam checks, and falsifiable revisit triggers.
  - Eliminated single-style SaaS anchoring bias in `maxilun-craft`, `purity-catalog.md`, and `component-mobile-patterns.md`: removed hardcoded slate-indigo `oklch(... 250)` snippets and universal Asymmetric Bento / `Cmd+K` mandates, introduced `LAY-013` (misplaced SaaS Bento monoculture ban), and established domain-authentic layout/navigation mapping across editorial, clinical/consumer, financial ledger, creative, and developer surfaces.
  - Enforced Single-Owner Cohesion in `maxilun` and `docs/ROUTING-MATRIX.md` so single pages/endpoints are owned end-to-end without unnecessary 4–5 specialist fragmentation.
  - Resolved cross-skill and intra-skill rule contradictions (`maxilun-engineer` dead-code & Tailwind rules, `purity-catalog.md` `TYPO-001`/`TYPO-003` vs `design-md` corpus, `maxilun-sentinel` TOTP SHA-1 & HSTS preload caveats, `maxilun-frontend` Next.js 15 / React 19 async request & Flight serialization semantics, `maxilun-diagrams` labeled-edge consistency) and trimmed every `SKILL.md` strictly below the `≤ 300` line cognitive ceiling.
- **Interface Engineering & Anti-Slop Hardening (Jakub Krehel Synthesis)**:
  - Bundled `skills/maxilun-craft/references/interface-engineering.md` establishing exact mathematical UI tolerances: concentric radius formula ($R_{outer} = R_{inner} + padding + border$), layered shadows over borders for elevation, 1px pure black/white image inset outlines, 0.96 active button press scale over 150ms, hover gating `@media (hover: hover)`, and `overscroll-behavior: contain`.
  - Codified 5 explicit AI-slop visual anti-patterns in `skills/maxilun/references/purity-catalog.md`: `CMP-015` (floating hero pill tagline capsule `• BADGE •`), `LAY-011` (monotonous center-everything cascade), `CMP-016` (pseudo-sci-fi hallucinated gimmicks vs authentic developer tooling), `CMP-017` (dual competing rounded-full pill buttons), and `LAY-012` (symmetrical 4-metric floating KPI strip over radial glow).
  - Integrated Cross-Discipline Review Protocol & 13 Escalation Triggers (HIGH on sight with binary BLOCK/APPROVE verdict) into `maxilun-verify` and `maxilun-craft`.
  - Fortified `maxilun-content` UX writing rules: object/verb terminology inventory, verb-first button labels (`[Action] + [Object]`), contextual error recovery beside the field, and undo-over-modal confirmation for reversible actions.
- **Craft & UI/UX Standards**: Added concentric inner radius formula (`radius_inner = max(0, radius_outer - padding)`), 8-state interactive feedback system, Web Interface Guidelines (WIG) compliance (paste unblocking, spellcheck discipline, flex truncation `min-w-0`, `overscroll-behavior: contain`), and "One Live Thing" subject inventory protocol.
- **Motion & Micro-interactions**: Codified Emil Kowalski action frequency matrix (0ms instant for high-frequency actions) and Disney animation principles adapted for web micro-interactions.
- **Architecture & Deep Modules**: Integrated Deep Modules vocabulary (Module, Interface, Depth, Seam, Adapter), The Deletion Test, and Two-Adapter Seam rule into `maxilun-architect`.
- **Diagnostic & Audit**: Codified Senior On-Call review protocol in `maxilun-insight`, ranked cut-list for pruning dead weight, and mandatory residual risk disclosure.
- **Code Hygiene**: Synchronized form, scroll containment, and micro-typography standards across the ecosystem.

### Fixed
- **Packaging, Installer & Knowledge Graph Cache Hygiene**: Explicitly whitelisted public scripts and excluded `__pycache__`, `.pyc`, `.maxilun`, `maxilun-out`, and `graphify-out` caches in `package.json`, hardened `scripts/install.ps1` and `scripts/install.sh` to strip local scan caches and support `~/.opencode/skills` without creating empty backup folders, and isolated `cli.py scan -o` so custom output paths no longer write `maxilun-out/` into the scanned directory.
- **Generic Scanner AST Patterns**: Added Go method receiver extraction (`func (r *Repo) ...`), Go interface/struct type extraction, and C++ scoped method resolution (`void Class::method(...)`) in `GenericScanner`, verified via functional test suite.
- **Installer & Uninstaller Parity**: Synchronized `scripts/install.sh` to support `--project`/`-p` mode, fixed macOS BSD `date` non-portable `%N` format with portable timestamps, restricted backup creation strictly to existing Maxilun skills, and added `--project`/`-Project` support and full multi-IDE target coverage (Trae, Windsurf, CodeBuddy) across both `scripts/uninstall.sh` and `scripts/uninstall.ps1`.

## [1.0.0] — 2026-10-24

### Initial Release — Production-Grade AI Engineering Skills Ecosystem

Maxilun launches as a complete 18-specialist AI engineering co-pilot ecosystem, purpose-built for production-grade software development. Every component — from the mandatory Knowledge Graph foundation and 7 Always-On Quality Engines to the specialist routing matrix, 100-brand UI design reference corpus, and programmatic motion video studio — has been designed, implemented, tested, and verified as a unified, coherent system.

### Ecosystem Highlights

#### 18 Specialist Skills
| # | Skill | Primary Trigger | Engineering Domain |
|:--:|---|---|---|
| 1 | `maxilun` | `/maxilun` | Master Orchestrator — confidence-based routing & multi-specialist wave coordination |
| 2 | `maxilun-knowledge-graph` | `/maxilun-graph`, `/msal-trace` | Mandatory Code Discovery — AST parser & WebGL 3D/2D visualizer (Lens) |
| 3 | `maxilun-scaffold` | `/maxilun-scaffold`, `/msal-init` | Project Context Scaffolder — 5 domain archetypes & 10 AI-readable architecture docs in `docs/` |
| 4 | `maxilun-architect` | `/maxilun-architect`, `/msal-think` | System Architecture — C4 Model, Event Storming, Transactional Outbox, Saga, PostgreSQL RLS |
| 5 | `maxilun-sentinel` | `/maxilun-sentinel`, `/msal-security` | Defensive Security — OWASP Top 10, STRIDE threat modeling, crypto, 10 trust boundaries |
| 6 | `maxilun-engineer` | `/maxilun-engineer` | Code Implementation — Test-Driven Development (TDD), 5-WHY debugging, clean refactoring |
| 7 | `maxilun-data` | `/maxilun-data` | Data & Persistence — schema design, zero-downtime expand-contract migrations, RLS |
| 8 | `maxilun-frontend` | `/maxilun-frontend` | Modern Frontend — React Server Components (RSC), Next.js App Router, Server Actions |
| 9 | `maxilun-verify` | `/maxilun-verify`, `/msal-test` | Quality Assurance — Playwright E2E, visual regression, accessibility (a11y), contract tests |
| 10 | `maxilun-insight` | `/maxilun-insight`, `/msal-audit` | Performance Diagnostics — CPU/memory/DB profiling, distributed tracing, leak detection |
| 11 | `maxilun-deploy` | `/maxilun-deploy` | Cloud & Operations — CI/CD pipelines, multi-stage Docker, zero-downtime rollouts |
| 12 | `maxilun-docsmith` | `/maxilun-docsmith`, `/msal-docs` | Technical Documentation — OpenAPI 3.1 (RFC 9457), Feature PRD/RFC, runbooks, ADRs |
| 13 | `maxilun-craft` | `/maxilun-craft`, `/msal-ui` | Design Systems & UI/UX — 100 brand design corpus, OKLCH color palettes, WCAG AAA |
| 14 | `maxilun-motion` | `/maxilun-motion` | Web Motion Design — physics-based harmonic springs, Lottie/SVG, 14 motion style signatures |
| 15 | `maxilun-cinecode` | `/maxilun-cinecode` | Programmatic Video Studio — React frame compiler, 22 promo/opener hooks, FFmpeg rendering |
| 16 | `maxilun-diagrams` | `/maxilun-diagrams`, `/msal-diagram` | System Visualization — C4, sequence, Event Storming, data-flow diagrams via Mermaid |
| 17 | `maxilun-content` | `/maxilun-content`, `/msal-copy` | User-Facing Copywriting — landing pages, UI microcopy, error states, brand voice |
| 18 | `maxilun-seo-audit` | `/maxilun-seo-audit`, `/msal-seo` | Technical SEO — Core Web Vitals, JSON-LD structured data, crawler readiness |

#### Multi-Specialist Motion Video Studio Pipeline
- Unified 5-skill pipeline (`craft` + `motion` + `content` + `cinecode` + `verify`) for studio-grade programmatic video generation.
- Brand DNA-to-Motion DNA translation, 14 motion style signatures, 22 opener/explainer hooks, beat-grid synchronization math, and deterministic React frame rendering (`<AbsoluteFill>`, `<Sequence>`, `<Spring>`).
- Direct headless rendering to MP4/WebM via FFmpeg `yuv420p` pipeline.

#### 100 Real-World Brand Design System Corpus
- Curated analyses of 100 production design systems (Stripe, Linear, Vercel, GitHub, Apple, Wise, Tailscale, Cloudflare, Perplexity, Discord, etc.) embedded inside `skills/maxilun-craft/references/design-md/`.
- Concrete token scales, 4 mandatory UI states (Loading/Skeleton, Empty+CTA, Populated `tabular-nums`, Error+Recovery), and strict ban on generic breadcrumb trails (`CMP-001` / `CMP-011`) and cliché purple-blue gradients.

#### 7 Always-On Quality Engines & Purity Gate
- **Focus Engine** — Executive HUD, task decomposition, persistent subtask tracking (max 3 concurrent).
- **Purity Engine** — Zero generic clichés: automatically purges buzzwords, fabricated claims, and empty placeholders.
- **Minimalist Engineering** — Simplicity ladder, native APIs first, minimal valid changes.
- **Clarity Engine** — Explicit technical signaling (`[CONFIRMED]`, `[INFERRED]`, `[UNCERTAIN]`, `[UNVERIFIED]`).
- **Dependency Decision Framework** — Stdlib-first evaluation, bundle size gating, maintenance viability checks.
- **Cognitive Load Reduction** — Naming as documentation, `< 400 line` ceiling per `SKILL.md`.
- **Proactive Communication Rules** — Blocker reporting, no silent failures, explicit assumptions.

#### Mandatory Knowledge Graph Foundation
- Zero-dependency AST scanner for Python, TypeScript, and generic languages (`skills/maxilun-knowledge-graph/`).
- Maxilun Lens: Interactive WebGL 3D and 2D Canvas dependency visualizer with BFS Path Trace and fuzzy search.
- Pre-edit code mapping guarantees exact `file:line` references before any modification.

#### Multi-Platform Support & Universal Agent Compatibility
- Native support for **Claude Code**, **Antigravity IDE & CLI**, **Cursor**, **Codex / OpenCode**, **Zed Editor**, and **Termul**.
- Universal installation: `npx skills add giriedu/maxilun`.
- Integrated `skills.sh.json` schema and live telemetry on [skills.sh/giriedu/maxilun](https://skills.sh/giriedu/maxilun).

#### License
- Released under the **Maxilun Free-to-Use License** (Free to use for personal & commercial projects; modification strictly prohibited). See [LICENSE](./LICENSE) for full terms.
