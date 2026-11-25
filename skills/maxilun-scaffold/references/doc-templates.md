# Canonical Templates for the 10 Project Context Documents (`docs/`)

Use the templates below when generating or updating `docs/`. Fill each section with facts from the repository (`[CONFIRMED]`), domain inferences (`[INFERRED]`), unverified checks (`[UNVERIFIED]`), or open questions labeled with a reason (`[UNCERTAIN: reason]`).

---

## 1. `docs/PRD.md`

```markdown
# PRD — [Project Name]

> **Status**: [Draft | Active | Frozen]  
> **Last Updated**: YYYY-MM-DD  
> **Owner**: [name/role]  
> **Domain Archetype**: [Fintech | B2B SaaS | DevTools/AI | Commerce/Booking | Media/Content]

## One-Paragraph Summary
[Explain WHAT is being built, FOR WHOM, and WHY — max 3 concrete sentences with no buzzwords]

## Problem Statement & Evidence
[The concrete problem solved: how often it occurs, time lost, or current business risk]

## Target Users
| Persona | Work / Usage Context | Primary Need | Current Pain Point |
|---|---|---|---|
| [Persona A] | [When & on which device it is used] | ... | ... |
| [Persona B] | ... | ... | ... |

## Features — MVP (Must Have)
- [ ] **[MVP-01] [Feature Name]**: [Functional description]
  - *Acceptance Criteria*: Given [context], When [action], Then [measurable result + time limit/validation].
  - *UI States (`DESIGN.md`)*: Idle state, Loading skeleton, Populated state (`tabular-nums`), Empty state + first CTA, Pending/optimistic state, Error state + recovery step.
- [ ] **[MVP-02] [Feature Name]**: [Description + acceptance criteria]

## Features — Phase 2 (Should Have)
- [ ] **[P2-01] [Follow-up feature]**

## Out of Scope / Non-Goals (Deliberately Not Built)
- [x] **[Feature X]**: [Clear reason why it is not built in this phase]
- [x] **[Feature Y]**: [Clear reason]

## Success Metrics
| Metric | Baseline | Target | How Measured / Data Source |
|---|---|---|---|
| [KPI 1] | [Current number / manual] | [Target number] | [Event / DB query / log] |

## Constraints & Compliance
- **Timeline**: [CONFIRMED / TBD: reason]
- **Budget / Infra**: [CONFIRMED / TBD: reason]
- **Compliance & Privacy**: [UU PDP / GDPR / PCI-DSS / None]
- **Target Platform**: [Web Responsive / Mobile-First / Desktop-Heavy / API-Only]
```

---

## 2. `docs/TECHSTACK.md`

```markdown
# TECHSTACK — [Project Name]

> **Status**: [Proposed | Confirmed | Locked]  
> **Last Updated**: YYYY-MM-DD

## Stack Decisions

| Layer | Technology | Version | Reason Chosen | Rejected Alternatives |
|---|---|---|---|---|
| **Frontend** | [Next.js / Vite / Astro / etc.] | [x.x] | [Concrete reason] | [What was rejected + why] |
| **Backend** | [Node.js / Go / Python / Rust] | [x.x] | [Concrete reason] | ... |
| **Database** | [PostgreSQL / SQLite / MySQL] | [x.x] | [Concrete reason] | ... |
| **Auth** | [Session HttpOnly / Auth.js / Custom] | [x.x] | [Concrete reason] | ... |
| **ORM / Query** | [Drizzle / Prisma / SQLc / SQLAlchemy] | [x.x] | [Concrete reason] | ... |
| **Styling** | [Native CSS OKLCH / Tailwind / CSS Modules] | [x.x] | [Concrete reason] | ... |
| **Testing** | [Vitest / Playwright / Pytest] | [x.x] | [Concrete reason] | ... |
| **Deployment** | [Docker / VPS / Cloud Run / Vercel] | - | [Concrete reason] | ... |

## Dependency Policy
- Runtime version minimum: `[x.x.x]`
- Package manager: `[pnpm | npm | bun | uv | cargo]`
- Banned packages: [List of packages prohibited in this project, with reasons]

## Environment Variables
| Variable | Scope | Required | Description | ExampleFormat |
|---|---|---|---|---|
| `DATABASE_URL` | server | Yes | Primary database connection string | `postgresql://user:pass@localhost:5432/db` |
| `AUTH_SECRET` | server | Yes | Session/token cryptographic key (min 32 bytes) | `openssl rand -base64 32` |
| `PUBLIC_APP_URL` | client/server | Yes | Application base URL | `https://app.example.com` |
```

---

## 3. `docs/DESIGN.md`

```markdown
# DESIGN — [Project Name]

> **Status**: [Draft | Active]  
> **Last Updated**: YYYY-MM-DD  
> **Skill**: `maxilun-craft` (`/maxilun-craft`)

## Design Reference Record (`maxilun-craft`)
- **References**: `[Pick 1-2 files from ../maxilun-craft/references/design-md/index.md]`
- **Applied**: `[Hierarchy, component density, typography, and contrast principles adapted]`
- **Rejected**: `[Elements of the reference deliberately not used in this product]`
- **Reason**: `[Fit with the user persona and primary task in PRD.md]`
- **Design Read**: `Reading this as: <page kind> for <audience>, in a <visual language> style, dial ENERGY X / RHYTHM Y / MOTION Z.`

## Brand & Visual Identity
- **Name**: [Project/Brand Name]
- **Personality**: [Calm Operational / High-Craft Dark UI / Editorial Crisp / etc.]
- **Anti-vibe**: [What this product does NOT look like — e.g. not neon cyber, not stacked glassmorphism]

## Color System (Semantic OKLCH)
```css
:root {
  /* Surface & Contrast */
  --surface-base:    oklch(98.5% 0.004 250);
  --surface-card:    oklch(100% 0 0);
  --surface-subtle:  oklch(95.5% 0.006 250);
  --border-hairline: oklch(89% 0.008 250);

  /* Text (WCAG AA/AAA Verified) */
  --text-main:       oklch(18% 0.012 250);
  --text-muted:      oklch(46% 0.012 250);

  /* Brand & Interactive */
  --brand-primary:   oklch(50% 0.17 255);
  --brand-hover:     oklch(43% 0.17 255);

  /* Semantic Status */
  --status-success:  oklch(58% 0.16 145);
  --status-warning:  oklch(72% 0.17 75);
  --status-danger:   oklch(56% 0.21 25);
  --status-info:     oklch(56% 0.17 250);
}
```

## Typography & Numeric Discipline
- **Font Sans**: [Plus Jakarta Sans / Geist / specific system font stack]
- **Font Mono**: [JetBrains Mono / Geist Mono]
- **Scale**: `12px (xs) → 14px (sm) → 16px (md/body) → 20px (lg) → 28px (xl) → 40px (2xl)`
- **Line Height**: Heading `1.2`, Body `1.55`, Max reading width `65ch`
- **Tabular Numerals**: Required `font-variant-numeric: tabular-nums` on every table of prices, metrics, times, and IDs.

## Spacing & Layout (4px Grid)
- **Scale**: `4px → 8px → 12px → 16px → 24px → 32px → 48px → 64px`
- **Radius Hierarchy**: Child radius `<=` Parent radius (example: Card `12px`, Inner button/input `8px`, Badge `4px`).
- **Touch Targets**: Minimum `44x44px` on mobile viewports, minimum input font size `16px`.

## Mandatory 6 UI States Contract
Every screen and data component must specify:
0. **Idle**: Initial resting state before user action or filter triggers async loading.
1. **Loading**: A skeleton that mirrors the final layout proportions (`CLS = 0`), not a single spinner in the middle of the screen.
2. **Empty**: A short explanation of why there is no data + a concrete first action button.
3. **Populated**: The normal data view with long-text handling (`truncate` / `wrap`) and tabular numbers.
4. **Pending / Mutating**: Non-janky inflight indicator (`aria-busy`, optimistic lock) during submit/refresh.
5. **Error**: A specific cause message the user understands + a recovery button (*retry* / alternative).
```

---

## 4. `docs/SECURITY.md`

```markdown
# SECURITY — [Project Name]

> **Status**: [Draft | Review | Approved]  
> **Last Updated**: YYYY-MM-DD  
> **Skill**: `maxilun-sentinel` (`/maxilun-sentinel`)

## Threat Model (STRIDE)
| Threat | Vector Specific to This Project | Required Mitigation | Status |
|---|---|---|---|
| **Spoofing** | Session theft / forged token | `HttpOnly`, `Secure`, `SameSite=Lax/Strict` cookie + refresh token rotation | [TBD/Active] |
| **Tampering** | Manipulated amount/status in the client payload | Strict schema validation on the server + recompute price/state on the server | [TBD/Active] |
| **Information Disclosure** | PII leak in logs or error messages | Log sanitization + standardized error responses (RFC 9457) with no production stack trace | [TBD/Active] |
| **Denial of Service** | Flood on login, checkout, or upload | Rate limiting per IP & user + request body size limit | [TBD/Active] |
| **Elevation of Privilege** | Access to another user's/tenant's resource (IDOR) | Ownership check (`resource.tenantId === session.tenantId`) in every query | [TBD/Active] |

## Authentication & Authorization
- **Auth Method**: [Session Cookie / JWT + Refresh Rotation / OAuth2 / Passkeys]
- **Password Hashing**: Argon2id (memory & iteration configuration per OWASP)
- **Authorization Model**: [RBAC / ABAC / Tenant Ownership Guard]
- **Role List**: `[owner, admin, member, ...]`

## Cryptographic & Webhook Rules
- Primitives: native Web Crypto API / `node:crypto`; never build a custom encryption scheme.
- Sensitive data encryption at rest: `AES-256-GCM` with a unique 12-byte IV from a CSPRNG.
- Webhook/token signature verification: must use constant-time comparison (`crypto.timingSafeEqual`).

## Data Privacy & Secrets
- All secrets come from environment variables; `.env` must be in `.gitignore`.
- List of PII stored: [Email, Name, Phone Number, ...] + retention & deletion policy.
```

---

## 5. `docs/STYLEGUIDE.md`

```markdown
# STYLEGUIDE — [Project Name]

> **Last Updated**: YYYY-MM-DD  
> **Skill**: `maxilun-engineer` (`/maxilun-engineer`)

## Naming Conventions
- **UI Components**: `PascalCase` (`InvoiceTable.tsx`)
- **Functions & Variables**: `camelCase` with a verb + specific object (`calculateInvoiceTax`, not `handleData`)
- **Domain Constants**: `UPPER_SNAKE_CASE` (`MAX_UPLOAD_BYTES = 5_242_880`)
- **DB Tables & Columns**: `snake_case` (`payment_intents`, `created_at`, index `idx_<table>_<column>`)

## Code Hygiene & Structure
- Maximum file length `300 lines`; maximum nesting depth `3 levels` (use early return / guard clause).
- One function carries one responsibility at one level of abstraction.
- Comments explain only **WHY** (business reason, third-party bug workaround, or invariant), not WHAT the code already says.

## Error Handling & Validation
- Validate all external input at the entry boundary (*trust boundary*) with an explicit schema (e.g. Zod/TypeBox/Pydantic).
- Never swallow an error with an empty `catch {}` block.

## Git & PR Conventions
- Branch: `feat/<topic>`, `fix/<topic>`, `refactor/<topic>`, `docs/<topic>`.
- Commit: Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`).

## Non-Negotiable Prohibitions
- [ ] No `any` without written justification.
- [ ] No `console.log` / debug print left in a production path.
- [ ] No hardcoded secret, staging/production URL, or magic number without a named constant.
- [ ] No `float` / fractional `number` for money calculations.
```

---

## 6. `docs/TASK.md`

```markdown
# TASK — [Project Name]

> **Sprint / Milestone**: [Milestone 1 — MVP Core]  
> **Last Updated**: YYYY-MM-DD

## Active Milestone Goal
[One sentence describing the end result that must work end-to-end in this milestone]

## In Progress (Maximum 3 Active Items)
- [ ] **[TASK-001]** [Concrete description + target file/module]
  - Verification: [Test or scenario that proves this task is done]

## Prioritized Backlog
- [ ] **[TASK-002]** [Description] — *Priority: High*
- [ ] **[TASK-003]** [Description] — *Priority: Medium*

## Blocked
- **[TASK-00X]**: [Cause of the blocker] → [Concrete step to unblock]

## Done
- [x] **[TASK-000]** Bootstrap the 10 project context documents in `docs/` (`YYYY-MM-DD`)
```

---

## 7. `docs/ARCHITECTURE.md`

```markdown
# ARCHITECTURE — [Project Name]

> **Last Updated**: YYYY-MM-DD  
> **Skill**: `maxilun-architect` (`/maxilun-architect`) & `maxilun-diagrams` (`/maxilun-diagrams`)

## C4 Level 1 & 2 — System & Container Diagram

```mermaid
flowchart TB
    User["Primary User"] -->|HTTPS| Web["Web / App Layer"]
    Web -->|Internal Call / API| Core["Domain & Service Layer"]
    Core -->|SQL / Transaction| DB[("Primary Database")]
    Core -->|HTTPS + HMAC| Ext["External Services"]
```

## Module Boundaries & Dependency Rules
| Module / Folder | Responsibility | May Import | Must Not Import |
|---|---|---|---|
| `core/` / `domain/` | Pure business rules & calculations | Standard library & internal types only | HTTP framework, ORM directly, UI components |
| `api/` / `server/` | Request handlers, auth guard, transactions | `core/`, `db/`, `lib/` | Client/UI components |
| `ui/` / `components/` | Interface rendering & the 6 UI states | `lib/`, DTO type contracts | DB connection or server secrets |

## Data Flow & Trust Boundaries
1. Request arrives → Authentication & Rate Limit middleware.
2. The handler validates the payload schema before touching the service layer.
3. Multi-table mutations must run inside an atomic database transaction.

## Architecture Decision Records (ADR Summary)
- **ADR-001**: [Title of the first structural decision] — *Status: Accepted* (see details in `docs/decisions/` when using separate ADRs).
```

---

## 8. `docs/SKILLS.md`

```markdown
# SKILLS — [Project Name]

> Map of Maxilun specialist usage in this repository.

## Primary Specialists for This Project
| Specialist | Command | When Used in This Project |
|---|---|---|
| `maxilun` | `/maxilun` | Cross-domain task orchestration & evidence gate |
| `maxilun-knowledge-graph` | `/maxilun-knowledge-graph` | Symbol dependency mapping before a refactor or cross-file change |
| `maxilun-scaffold` | `/maxilun-scaffold` | Updating the 10 context documents in `docs/` each milestone |
| `maxilun-docsmith` | `/maxilun-docsmith` | Follow-up feature specs/PRDs, OpenAPI contracts, ADRs, runbooks, `llms.txt` |
| `maxilun-architect` | `/maxilun-architect` | Module boundary decisions, API contracts, migration strategy |
| `maxilun-craft` | `/maxilun-craft` | UI/UX implementation, OKLCH tokens, 6-state & accessibility audit |
| `maxilun-frontend` | `/maxilun-frontend` | Server/client component architecture, state, and bundle performance |
| `maxilun-data` | `/maxilun-data` | DB schema design, indexes, and zero-downtime migrations |
| `maxilun-sentinel` | `/maxilun-sentinel` | Security, authentication, authorization, and cryptography audits |
| `maxilun-engineer` | `/maxilun-engineer` | Writing feature code, bug fixes, and unit tests |
| `maxilun-verify` | `/maxilun-verify` | Verifying the test suite, typecheck, lint, and E2E |
| `maxilun-deploy` | `/maxilun-deploy` | CI/CD pipeline, containerization, and release readiness |

## Quick Summary for AI Agents
- **Product Goal**: [1-sentence summary from `PRD.md`]
- **Core Stack**: [1-sentence summary from `TECHSTACK.md`]
- **Critical Invariants**: [Summary of the security/data rules that must not be violated]
```

---

## 9. `docs/GLOSSARY.md`

```markdown
# GLOSSARY — [Project Name]

> Ubiquitous Language: every developer and AI agent must use the same terms in code, DB schema, and UI.

## Business Domain Terms
| Canonical Term | Precise Definition | Synonyms Prohibited in Code/UI |
|---|---|---|
| **[Entity 1]** | [Exact definition including its lifecycle] | [Ambiguous terms that are prohibited] |
| **[Entity 2]** | [Exact definition] | [Ambiguous terms that are prohibited] |

## Domain Naming Rules
- Use the canonical terms above consistently, from database table names and TypeScript types/structs to API endpoints and UI label text.
```

---

## 10. `docs/ONBOARDING.md`

```markdown
# ONBOARDING — [Project Name]

> Quick orientation guide for new engineers and AI agents.

## Reading Order for AI Agents (Context Loading Order)
1. `docs/PRD.md` → Understand the business problem, MVP features, and non-goals.
2. `docs/ARCHITECTURE.md` & `docs/TECHSTACK.md` → Understand module boundaries and the stack.
3. `docs/DESIGN.md` → Understand the OKLCH tokens, `maxilun-craft` references, and the 6 UI state rule.
4. `docs/SECURITY.md` & `docs/STYLEGUIDE.md` → Understand the hard prohibitions and security boundaries.
5. `docs/TASK.md` → Check the current active work focus.

## Local Setup for Engineers
```bash
# 1. Install dependencies
[install command for the package manager]

# 2. Copy and fill in environment variables
cp .env.example .env

# 3. Run migrations & seed the local database
[DB migration command]

# 4. Run the development server
[dev server command]

# 5. Verify that every check passes
[typecheck && lint && test command]
```
```

---

## 11. The Lean 4-File Root Contract Suite (Fast-Context for Claude & Cursor)

A lean alternative for teams that need an instant *single source of truth* directly at the repository root, so AI agents (Claude Code, Cursor, Codex, Antigravity) stop guessing the schema, auth flow, and conventions:

### A. `Security.md` (Root)
```markdown
# Security.md

## Authentication
- Method: [e.g. Session Cookies HttpOnly / JWT + Refresh Rotation / OAuth2]
- Token expiry: [e.g. Access 15m, Refresh 7d]
- CSRF Protection: [e.g. SameSite=Lax + Double Submit Cookie]

## Secrets Management
- All secrets live in .env (never committed to git)
- Required vars: DATABASE_URL, AUTH_SECRET, API_KEY, ...
- Production secrets: [e.g. AWS Secrets Manager / Vault / Cloudflare Secrets]

## Data Protection & Privacy
- Sensitive fields: [email, phone_number, password_hash, billing_address]
- Encryption at rest: [AES-256-GCM for sensitive fields, CSPRNG 12-byte IV]
- Logging policy: PII redacted from server logs; no secrets in stdout.

## Access Control & Permissions
- Roles: admin, member, viewer, guest
- Multi-tenant rule: All queries MUST include `tenant_id === session.tenantId` (zero IDOR).
- Public routes: `/api/health`, `/api/auth/login`, `/api/webhooks/*`

## External Services & Scopes
- Stripe: payments (restricted webhook signing key)
- Resend: transactional email
```

### B. `Code-Style.md` (Root)
```markdown
# Code-Style.md

## Naming Conventions
- Variables & Functions: camelCase (verb + noun: `calculateInvoiceTax`)
- Components: PascalCase (`InvoiceTable.tsx`)
- Files & Folders: kebab-case (`invoice-table.tsx`, `use-invoice-query.ts`)
- Database tables & columns: snake_case (`payment_intents`, `created_at`)

## Folder Structure
- `/src/components` (reusable UI components)
- `/src/lib` (shared utilities, DB clients, API wrappers)
- `/src/routes` or `/src/app` (routing & pages)
- `/src/types` (TypeScript types & Zod schemas)

## Core Engineering Rules
- No default exports for components (use named exports).
- Imports: external packages first, then internal modules with `@/` alias.
- Prefer early returns & guard clauses over deep nesting (max nesting: 3 levels).
- Maximum file size: 300 lines (split into cohesive submodules if growing).
- Comments explain WHY (business invariant, security limit, workaround), never WHAT.
- Zero-Emoji UI Invariant: Never inject Unicode emojis into UI components or buttons.
```

### C. `Database.md` (Root)
```markdown
# Database.md

## Core Tables & Schema

### users
- id (uuid, primary key)
- email (text, unique, indexed)
- password_hash (text)
- role (text, enum: admin, member, viewer)
- created_at (timestamp with time zone, default now())

### items
- id (uuid, primary key)
- user_id (uuid, foreign key -> users.id on delete cascade)
- title (text, not null)
- status (text, enum: draft, published, archived)
- created_at (timestamp with time zone)

## Relationships
- users 1 -> many items (foreign key: `items.user_id`)

## Indexes & Constraints
- `idx_users_email` UNIQUE on `users(email)`
- `idx_items_user_status` composite index on `items(user_id, status)`

## Migration Invariants
- Zero-Downtime Rule: Never run blocking `ALTER TABLE ... ADD COLUMN ... NOT NULL` without default or multi-step expand-contract.
- All primary keys use UUIDv7 or BigInt identity.
```

### D. `API-Guide.md` (Root)
```markdown
# API-Guide.md

## Standard Response Format
- Success: `{ "data": T, "meta"?: Record<string, unknown> }`
- Error (RFC 9457): `{ "type": string, "title": string, "status": number, "detail": string }`

## Endpoints

### POST /api/auth/login
- Auth: Public
- Body: `{ email: string, password: string }`
- Returns: `{ data: { user: UserDTO }, token: string }`

### GET /api/items
- Auth: Bearer Token / Session Cookie (Required)
- Query: `?page=1&limit=20&status=published`
- Returns: `{ data: Item[], meta: { total: number, page: number } }`

### POST /api/items
- Auth: Required (Roles: admin, member)
- Body: `{ title: string, content: string }`
- Returns: `{ data: Item }` (HTTP 201)

## External Webhooks
- `POST /api/webhooks/stripe`: Verifies `Stripe-Signature` via constant-time HMAC before processing.
```
