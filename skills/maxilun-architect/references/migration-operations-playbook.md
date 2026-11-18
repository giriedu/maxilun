# Migration Strategies, Multi-Tenancy, Fitness Functions & Operational Architecture Playbook

Use this reference to guide legacy (brownfield) modernization, multi-tenant isolation, capacity and Disaster Recovery (DR) planning, and continuous architecture verification.

---

## 1. Brownfield & Zero-Downtime Migration Strategy

### 1.1 Service Migration Patterns
1. **Strangler Fig**: Put a router/proxy in front of the old system → move routes one at a time to the new module → monitor error parity → switch off the old route once stable.
2. **Branch by Abstraction**: Create an abstraction interface in the calling code → build the new implementation behind that interface → switch over with a feature flag → delete the old implementation.
3. **Parallel Run (Shadow Traffic)**: Duplicate read/calculation traffic asynchronously to the new system → compare results (*diff*) without affecting the user response → cut over after `0` critical divergences.

### 1.2 Schema & Data Migration Pattern (*Expand-and-Contract*)
Never ship a destructive schema change in a single release:
1. **Expand**: Add new columns/tables that are nullable or have a safe default (compatible with code version `N-1`).
2. **Dual-Write & Backfill**: Deploy code that writes to both the old and new columns; migrate historical data in small batches (`LIMIT 1000` with a pause) to avoid locking the table.
3. **Switch Reads**: Verify checksum consistency, then point reads at the new column/table.
4. **Contract**: Remove the old writes and drop the old column in the next release.

### 1.3 Instant Rollback Decision Thresholds
| Metric | Fix-Forward Limit | Mandatory Rollback Threshold |
|---|---|---|
| **Error Rate (5xx)** | `< 1%` above baseline | `> 5%` above baseline for `> 5 minutes` |
| **p99 Latency** | `< 2x` baseline | `> 3x` baseline for `> 10 minutes` |
| **Data Integrity / Corruption** | `0` incidents | **1 confirmed incident** (stop and roll back immediately) |

---

## 2. Multi-Tenancy Architecture (SaaS Isolation)

| Isolation Model | Mechanism | Infra Cost | Complexity | When to Use |
|---|---|---|---|---|
| **Shared DB, Shared Schema** | `tenant_id` column + PostgreSQL Row-Level Security (RLS) | Lowest | Low | Early- to mid-stage SaaS |
| **Shared DB, Schema-per-Tenant** | Separate schema namespace per organization | Medium | Medium | B2B SaaS that needs per-tenant customization/backup |
| **Database-per-Tenant** | Separate physical instance / DB | High | High | Heavily regulated enterprise (healthcare, banking, government) |
| **Hybrid Tiered** | Shared schema for the standard tier, dedicated DB for the Enterprise tier | Variable | High | Large-scale SaaS with mixed market segments |

**Mandatory Invariants for Every Multi-Tenant Model**:
- Extract the `tenant_id` context from the authentication session verified on the server. **Never** trust a raw `tenant_id` from the client request body/query.
- Enable **PostgreSQL RLS** (`CREATE POLICY tenant_isolation ON ... USING (tenant_id = current_setting('app.current_tenant')::uuid)`) as a second layer of defense.
- Every cache key (Redis), job queue payload, and log must carry the `tenant_id` prefix.

---

## 3. Cross-Cutting Concerns, DR/BCP, i18n & Architectural Accessibility

### 3.1 Cross-Cutting Checklist Required in Every ADR
| Aspect | Minimum Production Standard | Verification Method (`maxilun-verify` / `maxilun-deploy`) |
|---|---|---|
| **Structured Logging** | JSON with `trace_id`, `tenant_id`, and automatic PII masking | Log sampling test on error scenarios |
| **Distributed Tracing** | OpenTelemetry header propagation (`traceparent`) across services/workers | Trace span completeness check |
| **Health Probes** | `/health/live` (process alive) & `/health/ready` (DB/dependency connections ready) | Container probe test at startup & under high load |
| **Graceful Shutdown** | Catch `SIGTERM`, stop accepting new requests, finish active requests (`<= 30s`), close the DB pool | Rolling restart test with no dropped requests |
| **Secrets & Rotation** | No secrets in code; rotate signing/API keys with an overlap period (dual-key verification) | Secret scanner in CI + key rotation test |

### 3.2 Disaster Recovery Matrix (RPO / RTO)
| RPO Target (Max Data Loss) | RTO Target (Max Recovery Time) | Required Architecture |
|---|---|---|
| `0` (Zero data loss) | `< 1 minute` | Synchronous cross-zone/region replication + automatic active-active failover |
| `< 1 minute` | `< 5 minutes` | Asynchronous streaming replication + automatic replica promotion |
| `< 1 hour` | `< 1 hour` | Point-in-Time Recovery (PITR / WAL archiving) + warm standby |
| `< 24 hours` | `< 4 hours` | Encrypted daily snapshots + restore procedure tested monthly |

### 3.3 AI/LLM, Serverless/Edge, i18n & Accessibility Architecture
- **AI/LLM Integration**: Define a *Token Budget* limit per user/tenant, a *Timeout & Fallback Chain* (Primary Model → Lightweight Model → Measured Degraded Response), strict output schema validation (JSON Schema/Zod), and PII isolation before sending a prompt to a third party.
- **Serverless / Edge Runtime**: Use external connection pooling (for example PgBouncer / an HTTP driver) to prevent database connection exhaustion during *cold-start* concurrency spikes.
- **Internationalization (i18n)**: Store all times in the DB as `UTC` (`TIMESTAMPTZ`), store money as integer minor units + an ISO 4217 currency code (`IDR`, `USD`), and use CSS logical properties (`margin-inline-start`) when RTL languages are supported.
- **Architectural Accessibility**: Make the SSR/routing structure produce a consistent ARIA landmark hierarchy and cross-route focus management; coordinate the visual implementation with `maxilun-craft`.

---

## 4. Architecture Fitness Functions (Automated CI Enforcement)

Architecture that is not tested automatically decays. Define the rules below for `maxilun-verify` and `maxilun-deploy` to enforce:

| Fitness Function | Automated Check | Action on Failure |
|---|---|---|
| **Module Boundary Guard** | `core/` must not import from `ui/`, `components/`, or HTTP framework handlers | Fail the PR (`Block Merge`) |
| **Circular Dependency Check** | The import graph in `maxilun-knowledge-graph` / the linter is cycle-free (`A -> B -> A`) | Fail the PR (`Block Merge`) |
| **API Contract Drift** | The OpenAPI specification/schema matches the actual handler DTO types | Fail the PR (`Block Merge`) |
| **Tenant Guard Coverage** | Every query on a multi-tenant table passes through the `tenant_id` guard / RLS | Fail the PR (`Block Merge`) |

---

## 5. Short Worked Example: Splitting the E-Commerce Order Service (50k → 200k Orders/Hour)

1. **Mapping (`maxilun-knowledge-graph`)**: The `Order` module has 47 direct callers and joins directly to the `inventory` and `payments` tables (a dependency cycle on stock reservation).
2. **Decomposition & STRIDE (Phase 1 of `/msal-think`)**:
   - *Invariants*: Zero payment data loss; zero *overselling* during a flash sale; backward compatibility for 6 internal services.
   - *Critical Threats*: DB connection pool exhaustion during a flash sale (DoS on checkout) and direct order status manipulation through the shared table (Elevation of Privilege).
3. **Evaluation of 3 Hypotheses & Convergence (Phases 2–4)**:
   - *Option A (Modular Monolith with shared DB)*: Rejected — connection pool shared during the 200k/hour spike causes cascading saturation across checkout and search.
   - *Option B (Separate Order Service + Transactional Outbox + Event-Driven Inventory)*: **Selected** — full connection pool and failure isolation; independent horizontal scaling for order ingress.
   - *Option C (Full Event Sourcing + CQRS)*: Rejected — operational complexity and team cognitive load disproportionate to the 200k/hour scale.
4. **Execution & Handoff**:
   - Record the decision in `docs/decisions/ADR-047-order-service-separation.md` (`maxilun-docsmith`).
   - Run the *Expand-Contract* schema migration (`maxilun-data`), implement the idempotent Saga (`maxilun-engineer`), and install the module boundary fitness function (`maxilun-verify`).
