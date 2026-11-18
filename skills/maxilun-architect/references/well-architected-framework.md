# Maxilun Well-Architected Framework (WAF) & Solution Discovery Playbook

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-architect/SKILL.md"
  origin: "Maxilun Architect Engine"
-->

A guide to end-to-end system architecture design: a bias-free requirements discovery protocol, resolution of technical contradictions, and evaluation against the 6 software engineering architecture pillars.

---

## 1. Solution Discovery Protocol & Anti-Premature Design

A leading cause of architecture failure is jumping straight to a *technology stack*, a tool, or a service split before understanding the load characteristics and domain constraints.

### 1.1 Strict Phase Separation

```
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 1: Requirements Discovery & Trade-off Resolution                 │
│ (Functional, Non-Functional, Existing State, Contradiction Resolution) │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Requirements agreed, no contradictions
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 2: System Decomposition & Solution Architecture (6 WAF Pillars)  │
│ (Logical Components, Module Boundaries, API Contracts, Tech Choices)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Architecture plan validated
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 3: Solution Validation (Pre-Deployment Dry-Run & Runtime Checks) │
│ (Static Topology, Policy Check, Canary Routing, Verification Script)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Verification evidence accepted
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 4: Finalize ADR Artifacts & Specialist Handoff                   │
│ (Formal ADR, OpenAPI 3.1, Fitness Functions in CI)                     │
└────────────────────────────────────────────────────────────────────────┘
```

**Golden Rule**: During Phase 1 (Discovery), **never** recommend a product stack, a specific cloud vendor, or a microservice design. Focus entirely on gathering facts:
1. **Functional Requirements**: Critical business flows, core domain entities, stakeholders, and the main data mutations.
2. **Non-Functional Requirements**:
   - *Availability & SLA*: Uptime target (99.9% vs 99.99%), RTO (*Recovery Time Objective*) and RPO (*Recovery Point Objective*) targets.
   - *Latency & Throughput*: Upper-bound $p95$/$p99$ latency, estimated normal RPS, and peak load (*sustained peak*).
   - *Security & Compliance*: Data privacy limits (GDPR/UU PDP, PCI-DSS), tenant model (multi-tenant shared vs isolated).
   - *Cost Envelope*: Budget limits for compute, storage, and operations staff.
3. **Existing State (Brownfield)**: Infrastructure already running, the team's programming languages, and active databases.
4. **External Dependencies**: Third-party services, partner APIs, and their latency/reliability characteristics.

---

## 2. Resolving Ambiguity & Technical Contradictions

When user requirements contain fundamentally conflicting goals (for example: zero-trust network isolation with no public access at all vs a need for real-time webhooks from a public payment gateway; or distributed multi-region ACID consistency vs sub-millisecond write latency):

1. **Identify the Contradiction Explicitly**: Name the two or more requirements that technically conflict.
2. **Explain Why They Cannot Both Hold**: State the physical limit of computing involved (for example the CAP theorem, the network propagation speed limit, or a security trade-off).
3. **Present Measured Trade-off Options**:
   - Give at most 2–3 realistic contrasting options with the risk of each.
   - Include **1 firm recommendation** based on the *Safety* and *Simplicity* principles.
   - Ask for user approval (Type 1 decision) before continuing to structural design.

---

## 3. The Six Pillars of the Maxilun Well-Architected Framework (WAF)

Evaluate every architecture design against these 6 engineering pillars:

### Pillar 1: Reliability & Fault Tolerance
- **Graceful Degradation**: When a downstream dependency (secondary database, cache, broker, or third-party API) slows down or goes dark, the main system keeps serving critical routes in a degraded mode.
- **Circuit Breaker & Retry with Jitter**: Prevent connection storms (*thundering herd*). Apply a strict time limit (*timeout* $\le 2.5\text{s}$), exponential backoff with random jitter, and a circuit breaker.
- **Failover & RPO/RTO**: Give the database read replicas and a PITR recovery procedure, with evidence of periodic restore tests.

### Pillar 2: Security & Trust Boundaries
- **Zero Trust Architecture**: Do not trust a request only because it comes from the internal network. Verify authentication and authorization at every service boundary.
- **Cryptographic Sender-Constraining (DPoP)**: For sensitive high-risk endpoints, use tokens cryptographically bound to the client key pair (RFC 9449) to prevent exfiltration and replay attacks.
- **Least Privilege & RLS**: Restrict data access at the database level with PostgreSQL Row-Level Security (RLS), which mitigates IDOR risk in the application layer.

### Pillar 3: Performance & Capacity Envelope
- **Quantitative Capacity Envelope**: Set explicit numbers for normal RPS, memory capacity per instance, and the database connection pool quota.
- **Asynchronous Processing**: Move heavy I/O work (report generation, email/notification delivery, image resizing) to background queues (*background workers*).
- **Backpressure & Concurrency Limits**: Protect the service from running out of memory (*OOM*) by rejecting or holding requests when the worker queue exceeds its threshold.

### Pillar 4: Cost Optimization & Anti-Waste
- **Modular Monolith Baseline**: Reject premature microservices. One modular monolith application saves 70–90% of network egress cost, cluster orchestration dependencies, and operational complexity.
- **Compute Right-Sizing**: Match instance size to the actual memory profile, use auto-scaling driven by queues/real metrics, and shut down idle staging environments outside working hours.
- **Storage Tiering**: Move rarely accessed logs and historical archives to low-cost object storage with an automatic lifecycle policy.

### Pillar 5: Operational Excellence & Fitness Functions
- **SRE SLO Alerting**: Set error-budget alerts with the *Multi-Window Multi-Burn-Rate* pattern (this avoids alert fatigue from brief CPU spikes).
- **Structured Logs & Distributed Tracing**: Every request carries a consistent `traceId` from the edge to the database.
- **Architecture Fitness Functions**: Turn architecture invariants (module dependency direction, absence of circular imports, module boundary compliance) into automated checks in the CI pipeline.

### Pillar 6: Evolutionary Simplicity & Radical Minimalism
- **The Deletion Test**: Design each component or module so it can be deleted or replaced without reworking the internal logic of its *callers*.
- **Two-Adapter Seam Rule**: Do not create a speculative interface/abstraction when only one concrete implementation exists and no in-memory test fake is needed.
- **Quantitative Revisit Triggers**: Set concrete numeric limits for when the modular monolith should be split into independent services (for example: sustained core-table writes $>2{,}500\text{ TPS}$).

---

## 4. Solution Validation Cycle: Pre-Deployment & Runtime

Before declaring an architecture ready for production release, run two proof stages:

### 4.1 Pre-Deployment Validation (Static & Dry-Run)
1. **Topology & Routing Check**: Verify that the network topology leaves no private endpoint open to the public.
2. **Configuration Dry-Run**: Run the infrastructure syntax validation command (for example `terraform plan` or a manifest dry-run) without modifying live resources.
3. **Security Policy Audit**: Confirm that firewall rules, RLS policies, and secret environment variables are fully defined, with no default placeholder values.

### 4.2 Runtime Validation (Post-Deployment)
1. **Canary & Health Check**: Release traffic in stages ($5\% \to 25\% \to 100\%$) and verify HTTP status code `200` on the `/health` probe.
2. **Synthetic Probing**: Run synthetic tests from outside the network to measure actual round-trip latency and the function of critical routes.
3. **Rollback Readiness**: Test a single rollback command to the previous image digest and prove recovery succeeds within $\le 5$ minutes.
