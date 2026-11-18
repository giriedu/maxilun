# API Design Contracts, Distributed Systems & Technology Selection Reference

Use this reference with `maxilun-architect` when designing API contracts, running *Event Storming*, choosing a distributed consistency model, or evaluating the adoption of a new technology.

---

## 1. API Contract Design Patterns

### 1.1 Transport Selection Matrix
| Use Case | Recommended Transport | Technical Reason |
|---|---|---|
| Public API, browser clients | REST / HTTP (OpenAPI 3.1) | Universal support, native HTTP caching, easy inspection |
| High-throughput internal service-to-service | gRPC (Protobuf) | Fast binary serialization, bidirectional streaming, strictly typed contracts |
| Complex UI aggregation with varying fields | GraphQL | Avoids over/under-fetching on composite screens |
| One-way real-time updates (server to client) | SSE (Server-Sent Events) | Runs over standard HTTP, automatic reconnect, firewall-friendly |
| Low-latency two-way collaboration | WebSocket | Persistent full-duplex connection |
| Event streaming & log pipeline | Kafka / NATS JetStream | Replayable, partitioned, high throughput |
| Cross-organization notifications (B2B) | Webhook (HTTP POST + HMAC) | Decoupled, supports retry with backoff |

### 1.2 Production Endpoint Standards
1. **Pagination**: Prefer **cursor-based** pagination (`?cursor=<opaque>&limit=25`, max cap `100`) with the response `{ data, page_info: { has_next_page, next_cursor } }`. Avoid large `OFFSET` values on production tables.
2. **Filtering & Sorting**: Use indexed queries (`?status=active&sort=-created_at`). Reject a filter on a column without a database index with HTTP `400`.
3. **Multi-Tenant Rate Limiting**: Send `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, and `Retry-After` (on HTTP `429`). Keep a separate bucket per `tenant_id` so one tenant cannot exhaust another tenant's quota (*noisy neighbor*).
4. **Mutation Idempotency**: Require an `Idempotency-Key` header (UUID v4, TTL 24 hours) on every `POST`/`PATCH` operation that triggers a financial mutation or creates a resource. Same key + different payload → return `409 Conflict`.
5. **Webhook Security**: The payload must contain `event_id` and `timestamp` (reject when older than `> 300s`), plus an `HMAC-SHA256` signature header verified with `crypto.timingSafeEqual`.

---

## 2. Event Storming & Bounded Context Discovery

Before setting module boundaries or splitting out a new service:
1. **Domain Events** (*past-tense verb*): `InvoiceCreated`, `PaymentSettled`, `StockReserved`.
2. **Commands** (*imperative*): `CreateInvoice`, `SettlePayment`, `ReserveStock`.
3. **Aggregates & Invariants**: Group commands and events that share one transactional invariant into one *Aggregate* (a strong *Bounded Context* candidate).
4. **Brownfield Reconciliation**: Compare the Event Storming result with the actual map from `maxilun-knowledge-graph` to find module boundary leaks (for example, a table cross-joined by many domains).

---

## 3. Distributed Systems Patterns

### 3.1 Consistency Model Selection
| Model | Guarantee | Use When | Avoid When |
|---|---|---|---|
| **Strong (ACID)** | Linearizable reads/writes within 1 DB | Financial ledger, balances, stock, auth tokens | Cross-region with a very low write-latency requirement |
| **Sequential** | Total order preserved per stream/partition | Audit log, per-entity state machine | Free concurrent writers without a partition key |
| **Causal** | Cause-effect order preserved | Threaded comments, document collaboration | Ordinary independent CRUD operations |
| **Eventual** | Converges over time | Activity feed, notification delivery, aggregate analytics | Users require instant certainty of balance/status |

### 3.2 Transactional Outbox, Saga & CQRS
- **Transactional Outbox**: Write the business table change + the `outbox_events` row in **one local database transaction**. A worker polls with `SELECT ... FOR UPDATE SKIP LOCKED` (or CDC at high scale) and publishes to the broker. Every consumer must be idempotent.
- **Saga Pattern**:
  - *Choreography* (`< 4 steps`): Services react to events.
  - *Orchestration* (`>= 4 steps`): One coordinator drives the forward steps and executes idempotent *compensating actions* on failure.
- **Event Sourcing & CQRS**: Use **only** when historical audit replay is a hard business requirement, or when the read:write ratio is extremely skewed (`> 10:1`) and a denormalized read schema is needed.

### 3.3 Message Broker Selection Matrix
| Criterion | PostgreSQL (`SKIP LOCKED`) | RabbitMQ | Redis Streams | NATS JetStream | Apache Kafka |
|---|---|---|---|---|---|
| **Throughput** | Low–Medium (`< 1k/s`) | Medium (`10k/s`) | High (`50k+/s`) | High (`100k+/s`) | Very High (`500k+/s`) |
| **Operational Load** | Zero (uses the existing DB) | Low | Low | Low–Medium | High |
| **Event Replay** | Yes (until purged) | Limited | Limited | Full | Full (long-term) |
| **When to Choose** | Default for MVP & modular monolith | Complex task routing | Cache invalidation & realtime | Lightweight cloud-native microservices | Large-scale event log & analytics |

---

## 4. Technology Selection Checklist (Unweighted Evaluation)

When evaluating the adoption of a new library, database, or piece of infrastructure, reason through these concrete dimensions instead of computing a pseudo-numeric score:

| Dimension | Evaluation Focus | Key Question |
|---|---|---|
| **Team Expertise** | Operational Reality | How many engineers have operated it in production through an outage? |
| **Ecosystem Maturity** | Maintenance Risk | Documentation quality, release stability, type and tooling support? |
| **Operational Cost** | Brownfield Impact | Infra footprint, observability tooling, and the *Brownfield Multiplier* (`1.5x–2.0x` when refactoring legacy paths)? |
| **Talent Availability** | Long-Term Health | How easy are hiring, onboarding, and long-term maintenance? |
| **Performance Headroom** | Capacity Envelope | Has a *time-boxed spike* proven it meets the target capacity for the next 3 years? |
| **Compliance & Security** | Trust Boundaries | Encryption at rest/transit, audit log generation, and data residency guarantees? |
| **License Stability & Exit** | Vendor Lock-in | License terms (BSL/SSPL risk) and clarity of the rollback/exit migration path? |
---

## 5. Architecture Anti-Pattern Catalog (Always Reject)

| Anti-Pattern | Symptom in the Codebase | Corrective Action |
|---|---|---|
| **Distributed Monolith** | Service A calls B → C → D synchronously (chained HTTP/gRPC) | Merge back into one bounded context or switch to asynchronous events |
| **Shared Database Across Services** | Two different services run `INSERT/UPDATE` against the same physical table | Assign a single table owner; expose access through an API/event contract |
| **Premature Microservices** | A team of `< 5 engineers` splits into 6 micro repos before the domain is stable | Use a **Modular Monolith** with folder import boundaries enforced by a linter |
| **Anemic Domain & Leaky DTO** | Business logic is scattered across HTTP handlers and raw ORM rows are returned publicly | Isolate logic in the `core/` module and separate the DB schema from the API response DTO |

---

## 6. Deep Module Architecture & Seam Discipline

A healthy architecture is built from *deep modules*: large capability behind a slim interface, placed at a clean *seam*, and testable directly through that interface.

### 6.1 Standard Module Design Vocabulary

1. **Module**: Anything that has an interface and an implementation (scale-agnostic: function, class, internal package, or vertical slice).
2. **Interface**: Everything a caller must know to use the module correctly: argument types, state invariants, execution order, error handling, and performance characteristics.
3. **Implementation**: The body of code inside the module, hidden from outside callers.
4. **Depth**: The ratio of capability the caller gains to the cognitive load of the interface the caller must learn.
   - **Deep Module**: A compact interface with a rich internal implementation (example: a file I/O function, or a transaction runner that handles retry, lock, and rollback internally).
   - **Shallow Module**: A wide interface with a thin implementation that only forwards calls (*pass-through*).
5. **Seam**: The place where an interface lives and behavior can change without editing the callers.
6. **Adapter**: A concrete object that satisfies the interface at a seam.

### 6.2 Evaluation Principles & The Deletion Test

1. **The Deletion Test**:
   Simulate deleting the module from the codebase:
   - If the complexity disappears without a trace, the module is only a *shallow wrapper*. Delete it and *inline* its contents.
   - If the same complexity would have to be rewritten across $N$ callers, the module does real work (*deep module*).
2. **Two-Adapter Rule (Seam Reality Check)**:
   - *1 Adapter*: The seam is speculative/hypothetical. Do not create a generic interface when only one real implementation exists (YAGNI violation).
   - *2 Adapters*: The seam is proven real (for example, a Postgres implementation in production and an in-memory fake for unit tests).
3. **Design for Testability**:
   - Accept dependencies from outside (simple *dependency injection*); do not instantiate clients inside core functions.
   - Return explicit computation results; avoid *hidden side-effects*.
   - Shrink the public surface of the interface: fewer public methods mean fewer test scenarios to maintain.
