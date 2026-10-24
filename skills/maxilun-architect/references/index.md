# Architect Reference Corpus

This directory is a bundled reference library for `maxilun-architect`. It contains deep-dive engineering matrices, API design contracts, distributed systems patterns, migration playbooks, multi-tenancy models, fitness functions, and worked brownfield examples.

## Index of Bundled References

| File | Coverage | When to Read |
|---|---|---|
| `references/api-distributed-patterns.md` | API Transport Selection, Cursor Pagination, Filtering, Tiered Rate Limiting, Caching, Webhooks, Idempotency, Event Storming, Consistency Models (ACID/Causal/Eventual), Event Sourcing & CQRS, Saga, Transactional Outbox, Broker Selection, Technology Selection Matrix | Read when designing service boundaries, API/event contracts, distributed data flows, or evaluating technology choices |
| `references/migration-operations-playbook.md` | Strangler Fig, Branch by Abstraction, Parallel Run, Rollback Thresholds, Expand-Contract Data Migration, Multi-Tenancy Isolation, Cross-Cutting Concerns Checklist, Fitness Functions, Post-Incident Review, AI/LLM Gateway Patterns, Serverless/Edge, DR/RPO/RTO, i18n, Architectural Accessibility, and E-Commerce Worked Example | Read when modernizing brownfield systems, planning zero-downtime migrations, designing multi-tenant SaaS, or defining operational/DR fitness criteria |
| `../maxilun-docsmith/references/openapi-contracts.md` | OpenAPI 3.1 + RFC 9457 Problem Details (`application/problem+json`) | Read when formalizing an API decision into an executable contract specification |
| `../maxilun-docsmith/references/runbooks-adr.md` | Canonical ADR & Operational Runbook Templates | Read when recording Type 1a/1b architectural decisions or handing off operational constraints |
