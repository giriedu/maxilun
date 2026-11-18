# AI-Ready Documentation (`llms.txt`, `llms-full.txt`) & High-Density README Reference

Use this reference when writing `README.md`, `/llms.txt`, and `/llms-full.txt` so a human can absorb them in `< 60 seconds` and an AI/LLM agent spends few tokens reading them.

---

## 1. `llms.txt` & `llms-full.txt` Architecture

These files follow the standard `llms.txt` specification (and are checked by the `maxilun-seo-audit` audit):
- **`/llms.txt` (Context Map Index)**: Contains an H1 with the project name, a one-sentence blockquote stating what the system does, then a list of markdown links grouped by priority. Every link must carry a one-sentence description of **when an agent should read that file**.
- **`/llms-full.txt` (Single Context Bundle)**: Combines the content of the core documents (`PRD.md`, `ARCHITECTURE.md`, `TECHSTACK.md`, the main API contracts) with no duplicated navigation, no decorative badges, and no unnecessary HTML.

### Production `/llms.txt` Template

```markdown
# [Project Name]

> [One dense sentence: what this system does, its main stack, and its domain boundary.]

## Quick Context Rules (Read Before Editing Code)
- Stack: [Example: Next.js 15 App Router, TypeScript strict, PostgreSQL 16 + Drizzle ORM]
- Money & Numbers: Store every monetary amount in the smallest unit (`BIGINT` IDR); never use `float`.
- Validation & Auth: Every mutation passes server-side Zod validation and a tenant ownership check (`tenant_id`).

## Core Project Documents (`docs/`)
- [Product Requirements (PRD)](docs/PRD.md): Product goals, user personas, MVP features, non-goals, and success metrics.
- [System Architecture](docs/ARCHITECTURE.md): C4 diagrams, module boundaries, data flow, and the ADR list.
- [Tech Stack & Env](docs/TECHSTACK.md): Runtime versions, dependency policy, and the table of required environment variables.
- [Design System & Tokens](docs/DESIGN.md): OKLCH color tokens, type scale, 4px grid, and the 4 UI state rules (`maxilun-craft`).
- [Security & Threat Model](docs/SECURITY.md): STRIDE matrix, session/JWT policy, RBAC, and PII protection (`maxilun-sentinel`).
- [Coding Styleguide](docs/STYLEGUIDE.md): Naming conventions, import structure, error handling patterns, and the list of hard prohibitions.

## API & Operations
- [OpenAPI Specification](docs/openapi.yaml): REST endpoint contracts, payload schemas, and the RFC 9457 error structure.
- [Operational Runbook](docs/runbooks/core-service.md): Healthcheck procedure, production alert triage, and safe rollback steps.
- [Onboarding Guide](docs/ONBOARDING.md): Local setup order, database migration, and test suite verification.
```

---

## 2. High-Density `README.md` Standard

The `README.md` at the repository root contains no marketing filler. Required structure:

1. **Title + One Functional Sentence**: What this repository does and for whom.
2. **Architecture & Short Directory Map**: A folder tree that states the responsibility of each main directory.
3. **Quickstart (Copy-Paste Ready)**: Commands in order from clone, install, `.env` setup, and DB migration to a running server in under 60 seconds.
4. **Environment Variables Table**: Variable name, required/optional, a safe example value, and its purpose.
5. **Verification & Build Commands**: The exact commands for `typecheck`, `lint`, `test`, and `build`.
6. **Links to `docs/`**: Point readers and AI agents to `docs/PRD.md`, `docs/ARCHITECTURE.md`, and `/llms.txt`.

### Documentation Quality Checklist (`maxilun-docsmith` Delivery Gate)
- Every CLI command in the document has been matched against the actual `package.json` / `Makefile` / `pyproject.toml` in the repository (`[CONFIRMED]`).
- Every environment variable name in the documentation table matches `.env.example` and the `process.env` / `os.environ` reads in the code.
- No performance or security claim appears without a real number or mechanism.
- When the document contains a feature specification/PRD with UI components, the 4-state UI matrix and the design reference note (`../maxilun-craft/references/design-md/index.md`) are included.
