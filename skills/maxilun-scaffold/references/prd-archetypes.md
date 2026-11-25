# Domain Archetypes for PRD, Security, Architecture & Design Bootstrap

Use this archetype matrix when running `maxilun-scaffold` so the 10 documents in `docs/` start with sharp domain invariants and link to the real design systems in `../maxilun-craft/references/design-md/index.md`.

---

## 1. Domain Archetype Map → Context Invariants & UI/UX References

| Product Archetype | Required Invariants in `PRD.md` & `GLOSSARY.md` | `ARCHITECTURE.md` & `TECHSTACK.md` Invariants | `SECURITY.md` Invariants (`maxilun-sentinel`) | `DESIGN.md` UI/UX References (`../maxilun-craft/references/design-md/`) |
|---|---|---|---|---|
| **1. Fintech, Billing, Payment & Ledger** | Smallest monetary unit (`BIGINT` IDR/cents), settlement reconciliation flow, refund/dispute rules, audit trail | Double-entry ledger or transactional outbox, `Idempotency-Key` required on every mutation endpoint | Webhook signature verification (`HMAC-SHA256` + `timingSafeEqual`), PII/account number masking in logs, MFA for fund withdrawal | `stripe.md`, `wise.md`, `mercury.md`, `revolut.md` (focus: `tabular-nums`, high contrast, clear semantic status colors) |
| **2. B2B SaaS, ERP, CRM & Workflow** | Organization hierarchy (`Organization` → `Workspace` → `Member`), per-role RBAC matrix, approval state machine, bulk import/export | Multi-tenancy isolation (`tenant_id` on every table + Row-Level Security / middleware guard), background job queue | Cross-tenant IDOR prevention, session revocation when a role changes, audit log of configuration changes | `linear.app.md`, `notion.md`, `airtable.md`, `cal.md` (focus: high information density, `Cmd+K` keyboard navigation, calm panels) |
| **3. DevTools, Cloud Infra, Observability & AI Apps** | API key/token management, usage quotas & rate limits, streaming latency (SSE/WebSocket), CLI/API documentation | Control plane vs data plane separation, time-series / log storage, async job queue with clear timeout limits | API key hashing in the database (store only prefix + SHA-256/Argon2 hash), prompt injection / SSRF protection on webhooks | `vercel.md`, `sentry.md`, `posthog.md`, `supabase.md`, `cursor.md` (focus: optional dark-first, precise monospace font, code blocks easy to copy) |
| **4. E-Commerce, Marketplace & Booking** | Variant/SKU catalog, temporary stock reservation (inventory hold TTL), order state machine (`CART` → `PAID` → `FULFILLED`), commission | Fast indexed search, race condition prevention during flash sales (`SELECT ... FOR UPDATE`), courier/payment integration | Price validation required on the server (never trust the price from the client cart payload), checkout rate limit | `shopify.md`, `airbnb.md`, `nike.md` (focus: clear price hierarchy, mobile bottom-sheet checkout, tap target `>=44px`) |
| **5. Media, EdTech, Documentation & Content Portals** | Content hierarchy (Course/Article/Module), reader/student progress, instant search, long-form reading accessibility | Static/ISR caching, media asset optimization, full-text search index, serving `/llms.txt` & `/llms-full.txt` | Paid content protection (signed URL with short TTL), rich-text/Markdown input sanitization against Stored XSS | `wired.md`, `theverge.md`, `mintlify.md`, `sanity.md` (focus: reading width `60ch-75ch`, sharp editorial typography scale) |

---

## 2. Procedure for Deriving `DESIGN.md` from `maxilun-craft` References

When `maxilun-scaffold` creates `docs/DESIGN.md`:
1. **Do not leave every color and typography value as `[TBD]`** when the product category is already known from the interview or the repo scan.
2. Pick **at most 2 reference files** from the last column of the table above (for example, for a point-of-sale/finance app: read `../maxilun-craft/references/design-md/wise.md` or `stripe.md`).
3. Convert the visual principles of those reference files into the OKLCH token block, typography scale, and component rules in `docs/DESIGN.md`.
4. Write the **Design Reference Record** block at the top of `docs/DESIGN.md`:

```markdown
## Design Reference Record (`maxilun-craft`)
- **References**: `../maxilun-craft/references/design-md/linear.app.md`, `../maxilun-craft/references/design-md/stripe.md`
- **Applied**: Tight 4px spacing scale for operational tables, `tabular-nums` on every metric/amount column, hairline borders with measured contrast.
- **Rejected**: Complex marketing hero animation that is irrelevant to an internal app.
- **Reason**: The primary users are operations staff who need fast table scanning with minimal visual distraction.
```

---

## 3. `PRD.md` Quality Checklist Before Handoff

Before `maxilun-scaffold` finishes creating `docs/PRD.md`, confirm:
- The **Problem Statement** names a measurable impact (time, risk, or cost), not abstract jargon.
- Every **MVP Feature** has acceptance criteria that `maxilun-verify` can test directly.
- The **UI/UX Requirements** section of `PRD.md` points directly to `docs/DESIGN.md` and lists the required 6 UI states (Idle, Loading, Populated, Empty, Pending, Error).
- The **Out of Scope (Non-Goals)** section has at least 2 items to keep the first sprint focused (YAGNI).
