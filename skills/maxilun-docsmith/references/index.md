# Docsmith Reference Corpus

This directory is a bundled reference library for `maxilun-docsmith`. It contains production-grade reference specifications, engineering RFCs/PRDs, OpenAPI 3.1 contracts, operational runbooks, ADRs, and AI-ready `llms.txt` architectures.

## Index of Bundled References

| File | Domain & Deliverable | When to Use |
|---|---|---|
| `references/prd-rfc-specs.md` | Feature PRD, Engineering RFC, Technical Design Document (TDD), UI/UX State & API Spec binding | User asks to write a `PRD.md`, feature specification, RFC, or technical spec that bridges product goals, UI states (`maxilun-craft`), and API/data contracts |
| `references/openapi-contracts.md` | OpenAPI 3.1, RFC 9457 Problem Details (`application/problem+json`), Cursor Pagination, Idempotency, Webhooks, AsyncAPI 3.0, TypeSpec | Documenting REST APIs, event-driven topics, error catalogs, or webhook contracts |
| `references/runbooks-adr.md` | Architecture Decision Records (ADR), Production Service Runbooks, Incident Playbooks, Zero-Downtime Migration Guides | Writing `docs/decisions/ADR-*.md`, `docs/runbooks/*.md`, or major version migration guides |
| `references/llms-txt-spec.md` | `llms.txt`, `llms-full.txt`, High-Density READMEs, Context-Window-Optimized AI Documentation | Creating or auditing repository `README.md`, `/llms.txt`, or developer onboarding docs for humans and AI agents |
| `../maxilun-craft/references/design-md/index.md` | 100 Production UI/UX Design Systems (Stripe, Linear, Vercel, GitHub, Wise, Figma, etc.) | Specifying UI components, interaction states, visual hierarchy, or design tokens inside a Feature PRD or Technical Spec |

## Selection & Application Contract

1. Identify the requested document type (Feature PRD, RFC, API Spec, Runbook, ADR, README, or `llms.txt`).
2. Read the matching reference file from the table above before drafting.
3. If the document specifies user-facing screens, flows, or UI states, also consult `../maxilun-craft/references/design-md/index.md` and select at most two comparable product references to ground component density, interaction states, and layout tokens.
4. Translate structural patterns into concrete facts from the user's repository (`package.json`, schema, routes, tests). Never emit ungrounded boilerplate.
5. Record the evidence note in the generated document or handoff:

```text
References: <docsmith and/or craft reference files>
Applied: <structural patterns, schemas, state tables, or UI principles applied>
Rejected: <sections omitted under YAGNI because not applicable to this repo>
Reason: <product domain, audience, or architecture constraint>
```
