# Project Context Maintenance & Drift Detection Playbook

Operational guide for updating existing project documentation (`docs/`), detecting drift between codebase truth and documentation, and maintaining context freshness.

---

## 1. Documentation Drift Detection Protocol

Documentation drifts when code contracts evolve without corresponding documentation updates:

| Drift Surface | Manifest / Ground Truth | Verification Action |
|---|---|---|
| **Tech Stack & Versions** | `package.json`, `Cargo.toml`, `go.mod`, `requirements.txt` | Compare declared versions in `docs/TECHSTACK.md` against actual dependency tree. |
| **API Endpoints** | Route definitions (`app/api/**/route.ts`, FastAPI routers) | Verify that every active mutation route has an entry in `docs/ARCHITECTURE.md`. |
| **Database Schema** | Migration files (`prisma/migrations`, `migrations/*.sql`) | Reconcile table names, foreign keys, and indexes in `docs/ARCHITECTURE.md` with latest migration. |
| **Environment Variables** | `.env.example`, runtime config validators (`env.mjs`, pydantic) | Confirm all required keys appear in `docs/ONBOARDING.md` with clear validation rules. |

---

## 2. Update Mode (`--update`) Execution Flow

When invoked with `--update` on an existing `docs/` repository:

1. **Non-Destructive Scanning**:
   - Inspect existing `docs/` files before making edits. Preserve custom domain explanations, business invariants, and team-specific notes.
2. **Selective Patching**:
   - Update only drifted sections (e.g. new routes, changed schema columns, added dependencies).
   - Use unified diff-style insertions rather than blowing away existing documentation.
3. **Deprecation Marking**:
   - When an architecture component is removed or refactored in code, mark the corresponding doc section as `[DEPRECATED: superseded by <new-module>]` before eventual pruning.

---

## 3. Lean 4-File Docs Contract

For lightweight microservices, CLI tools, or headless libraries where a full 10-document `docs/` suite is excessive, adopt the lean 4-file `docs/` contract (or 4 standalone root contracts `Security.md`, `Code-Style.md`, `Database.md`, `API-Guide.md` when organizing without a `docs/` folder):

```text
docs/
  ├── PRD.md           <- Business problem, non-goals, and core invariants
  ├── ARCHITECTURE.md  <- System boundaries, data schemas, and API contracts
  ├── TASK.md          <- Current sprint focus, backlog, and active cutovers
  └── ONBOARDING.md    <- Environment setup, required CLI tools, and test commands
```

- When scaling to a full production SaaS, expand from the 4-file root to the 10-document standard (`STYLEGUIDE.md`, `SECURITY.md`, `SKILLS.md`, etc.) using `references/doc-templates.md`.

---

## 4. Documentation Freshness Gate

Run this verification check before declaring context maintenance complete:
1. Every path referenced in `docs/` exists in the repository.
2. Every terminal command in `ONBOARDING.md` and `README.md` runs with exit code `0`.
3. Zero unresolved `TODO` or `FIXME` comments exist in generated documentation without an assigned owner.
