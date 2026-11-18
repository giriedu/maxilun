# Architect Reference Corpus

This directory is a bundled reference library for `maxilun-architect`. It contains deep-dive engineering matrices, API design contracts, distributed systems patterns, migration playbooks, multi-tenancy models, fitness functions, and worked brownfield examples.

## Index of Bundled References

| File | Coverage | When to Read |
|---|---|---|
| `references/api-distributed-patterns.md` | API Transport Selection, Cursor Pagination, Filtering, Multi-Tenant Rate Limiting, Webhooks, Idempotency, Event Storming, Consistency Models (ACID/Causal/Eventual), Event Sourcing & CQRS, Saga, Transactional Outbox, Broker Selection, Technology Selection Checklist | Read when designing service boundaries, API/event contracts, distributed data flows, or evaluating technology choices |
| `references/migration-operations-playbook.md` | Strangler Fig, Branch by Abstraction, Parallel Run, Rollback Thresholds, Expand-Contract Data Migration, Multi-Tenancy Isolation, Cross-Cutting Concerns Checklist, Disaster Recovery (RPO/RTO), AI/LLM & Edge Runtimes, Fitness Functions, and E-Commerce Worked Example | Read when modernizing brownfield systems, planning zero-downtime migrations, designing multi-tenant SaaS, or defining operational/DR fitness criteria |
| `references/well-architected-framework.md` | Solution Discovery Protocol & Anti-Premature Design, Resolving Ambiguity & Technical Contradictions, the 6 Maxilun WAF Pillars (Reliability, Security, Performance, Cost, Operations, Simplicity), Pre-Deployment & Runtime Validation | Read when conducting end-to-end architecture discovery, evaluating trade-offs across the 6 pillars, resolving conflicting non-functional requirements, or validating deployment topology |
| `../maxilun-docsmith/references/openapi-contracts.md` | OpenAPI 3.1 + RFC 9457 Problem Details (`application/problem+json`) | Read when formalizing an API decision into an executable contract specification |
| `../maxilun-docsmith/references/runbooks-adr.md` | Canonical ADR & Operational Runbook Templates | Read when recording Type 1a/1b architectural decisions or handing off operational constraints |
