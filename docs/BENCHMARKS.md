# Maxilun Engineering Benchmarks & Verifiable Proof

> **No Marketing Claims. Only Reproducible Artifacts.**  
> This document demonstrates the concrete difference between **unconstrained AI output (Raw LLM)** and **Maxilun-governed output** across four real engineering domains, plus the measurable token efficiency of Maxilun v1.0's modular reference architecture.

---

## 1. Context Window & Token Efficiency (`v1.0.0` Architecture)

Most AI skill packs fail in one of two ways:
1. **Empty 40-line prompts** that tell the AI *"write clean code"* without concrete schemas, formulas, or reference tokens.
2. **Bloated 2,000-line monolithic prompts** that flood the context window on every turn and degrade model reasoning.

Maxilun solves this by enforcing a **strict `< 400 line` ceiling on every `SKILL.md`** (`scripts/test-suite.py:test_size_budget`) while bundling **deep, on-demand `references/`** inside each specialist:

| Specialist Skill | Active `SKILL.md` Size | On-Demand Bundled Corpus (`references/` & `scaffold/`) | What Loads Only When Needed |
|---|---:|---|---|
| `maxilun` (Orchestrator) | `343 lines` | `4 files` (`engines.md`, `discovery.md`, `purity-catalog.md`, `code-hygiene.md`) | Wave 0 discovery protocol, 4 engines detail, banned vocabulary catalog |
| `maxilun-craft` | `214 lines` | **`101 files`** (`references/design-md/*.md` + `component-mobile-patterns.md`) | 100 real brand design analyses (Stripe, Linear, Vercel, GitHub, Wise, Apple, etc.), 20 art directions, mobile touch & 4-state UI rules |
| `maxilun-architect` | `202 lines` | `3 files` (`api-distributed-patterns.md`, `migration-operations-playbook.md`) | `/msal-think` 4-phase matrix, Outbox/Saga, Strangler Fig, RLS Multi-Tenancy, DR RPO/RTO, Fitness Functions |
| `maxilun-docsmith` | `177 lines` | `5 files` (`prd-rfc-specs.md`, `openapi-contracts.md`, `runbooks-adr.md`, `llms-txt-spec.md`) | Gherkin PRD/RFC templates, OpenAPI 3.1 + RFC 9457 `ProblemDetails`, production runbooks, `/llms.txt` |
| `maxilun-scaffold` | `219 lines` | `3 files` (`prd-archetypes.md`, `doc-templates.md`, `index.md`) | 5 domain archetypes (Fintech, B2B SaaS, DevTools, Commerce, Media) & 10 canonical `docs/` templates |
| `maxilun-motion` | `176 lines` | `3 files` (`motion-components.md`, `choreography-styles.md`, `index.md`) | Analytical damped harmonic spring evaluator, 14 motion style signatures, 22 opener/promo hooks, beat-grid math |
| `maxilun-cinecode` | `179 lines` | `3 ref files` + **Full React/TS/FFmpeg `scaffold/`** | `<AbsoluteFill>`, `<Sequence>`, `<Spring>`, `interpolate`, headless frame capture, and 5-skill studio video pipeline |
| `maxilun-sentinel` | `310 lines` | `2 files` (`security-playbook.md`, `php2shell-advisory.md`) | 10 trust boundaries, 20+ security test patterns, Web Crypto/Argon2id/AES-256-GCM implementations |
| `maxilun-knowledge-graph` | `178 lines` | **AST Scanners (`python`, `ts`, `generic`) + `cli.py` + `lens.html`** | Zero-dependency AST symbol indexer & 3D WebGL / 2D Canvas dependency visualizer |

---

## 2. Side-by-Side Output Proof: Raw LLM vs. Maxilun

### Case A: Fintech Dashboard UI (`maxilun-craft` + `maxilun-content`)

**Prompt**: *"Build a transaction history table and payout card for a B2B payment dashboard."*

| Dimension | Raw LLM Default (Generic AI Clichés) | Maxilun (`maxilun-craft` + `references/design-md/stripe.md`) |
|---|---|---|
| **Color & Surface** | Decorative purple-to-blue gradient header (`linear-gradient(135deg, #667eea, #764ba2)`), stacked glassmorphism cards | Semantic OKLCH tokens (`--surface-base: oklch(98.5% 0.004 250)`), `1px` high-contrast hairline borders, zero decorative gradients (`CLR-001` enforced) |
| **Typography & Numbers** | Proportional font on currency column (digits jitter horizontally when values change) | `font-variant-numeric: tabular-nums` right-aligned on all monetary, timestamp, and ID columns |
| **UI States** | Only renders the happy path (`transactions.map(...)`) — crashes or shows blank box when empty/loading | Mandatory **4 UI States**: proportional row skeleton (`CLS = 0`), empty state with first-action CTA, populated state, and inline error state with retry |
| **Labels & Copy** | Generic buttons (`"Submit"`, `"Learn More"`), fake badge `"AI-Powered Analytics"` | Action-specific labels (`"Cairkan Dana"`, `"Ekspor CSV"`), factual status badges (`SETTLED`, `PENDING`), zero marketing badges (`CMP-002` enforced) |

---

### Case B: Payment Webhook & Mutation Endpoint (`maxilun-sentinel` + `maxilun-data` + `maxilun-docsmith`)

**Prompt**: *"Create an endpoint to receive payment webhooks and update the invoice balance."*

```typescript
// ❌ RAW LLM OUTPUT (Vulnerable & Non-Idempotent)
app.post('/webhook', async (req, res) => {
  const sig = req.headers['x-signature'];
  const expected = crypto.createHmac('sha256', process.env.SECRET).update(JSON.stringify(req.body)).digest('hex');
  if (sig !== expected) return res.status(401).send('Invalid'); // 1. Timing attack via !== & re-serialized JSON!
  await db.query(`UPDATE invoices SET amount = amount - ${req.body.paid} WHERE id = '${req.body.id}'`); // 2. SQLi + Float drift + No idempotency!
  res.json({ ok: true });
});
```

```typescript
// ✅ MAXILUN OUTPUT (maxilun-sentinel + maxilun-data + maxilun-docsmith)
// Enforces: Raw body HMAC, timingSafeEqual, 300s replay window, BIGINT minor units, and transactional idempotency
import { createHmac, timingSafeEqual } from 'node:crypto';

export function verifyWebhookSignature(rawBody: Buffer, timestampHeader: string, signatureHeader: string, secret: string): boolean {
  const timestamp = Number(timestampHeader);
  const nowSeconds = Math.floor(Date.now() / 1000);
  if (!Number.isInteger(timestamp) || Math.abs(nowSeconds - timestamp) > 300) return false;

  const expected = Buffer.from(`v1=${createHmac('sha256', secret).update(`${timestamp}.${rawBody.toString('utf8')}`).digest('hex')}`, 'utf8');
  const received = Buffer.from(signatureHeader, 'utf8');
  return expected.length === received.length && timingSafeEqual(expected, received);
}
```
- **Schema Invariant (`maxilun-data`)**: Monetary columns use `BIGINT` minor units (`amount_idr BIGINT CHECK (amount_idr >= 0)`), never IEEE-754 floats.
- **Contract Standard (`maxilun-docsmith`)**: Errors return standardized **RFC 9457 Problem Details (`application/problem+json`)** with `trace_id` and field-level codes (`skills/maxilun-docsmith/references/openapi-contracts.md`).

---

### Case C: Multi-File Refactoring (`maxilun-knowledge-graph` + `maxilun-engineer`)

**Prompt**: *"Change `validateSession(token)` to also require `tenantId` across the repository."*

| Step | Without Maxilun | With `maxilun-knowledge-graph` (`cli.py`) |
|---|---|---|
| **1. Discovery** | Blindly greps or reads 15+ full files into context, missing indirect callers | Runs `python cli.py query callsIn: validateToken` → returns exact `file:line` callers and test files in `< 1 second` |
| **2. Impact Radius** | Modifies function signature, breaks 2 transitive route handlers | Maps inbound/outbound edges first, updates all callers atomically, and runs `maxilun-verify` Tier 1–4 |

---

### Case D: Programmatic Motion Video (`maxilun-craft` + `maxilun-motion` + `maxilun-content` + `maxilun-cinecode`)

**Prompt**: *"Create a 12-second product launch video showing our CI build speedup."*

| Layer | Typical AI Video Script | Maxilun 5-Specialist Video Studio Pipeline |
|---|---|---|
| **Visual System (`maxilun-craft`)** | Tiny 14px web text on a 1080p canvas (illegible after MP4 compression), random hex colors | Grounded in `references/design-md/vercel.md`: 1080p canvas typography (`72px` headline, `36px` caption, `tabular-nums` counter) and `96px/80px` safe-area margins |
| **Choreography (`maxilun-motion`)** | CSS `transition: all 0.5s` (causes non-deterministic frame capture drift in headless rendering) | Pure frame-indexed math (`useCurrentFrame()`, analytical damped spring `{ stiffness: 170, damping: 19 }`), 70% overlapping action, and `45-frame` reading hold time |
| **Narrative (`maxilun-content`)** | 30-word marketing paragraph on screen | 4-Beat Script (`<= 8 words/scene`): Hook (`0..90f`) → Mechanism (`90..240f`) → Metric Proof (`240..345f`) → CLI CTA (`345..420f`) |
| **Encoding (`maxilun-cinecode`)** | Browser screen recording with dropped frames | Headless frame-by-frame PNG sequence piped to FFmpeg (`-c:v libx264 -pix_fmt yuv420p`) + `.vtt` subtitle sidecar |

---

## 3. Automated Repository Verification (`scripts/test-suite.py`)

Every commit and pull request in Maxilun is gated by `python scripts/test-suite.py` (16 automated validation suites):
```bash
cd maxilun
python scripts/test-suite.py
```
1. **18-Skill Schema & Version Lock**: Verifies frontmatter, semantic version parity (`1.0.0`), and license across all 18 skills.
2. **Byte-for-Byte `CORE-RULES` Drift Detection**: Guarantees the 4 quality engines are identical in all 18 skills.
3. **Reference Path Resolution**: Parses every `` `references/*.md` `` and `` `../maxilun-*/references/*.md` `` token in all 18 skills and verifies the target file exists on disk.
4. **Cognitive Load Size Budget**: Enforces `< 400 lines` warning / `< 1200 lines` hard limit on every `SKILL.md`.
5. **Security Scanner Compliance (`skills.sh`)**: Blocks any `curl/wget | sh/bash/python/node` pipe-to-interpreter pattern across all markdown files.
6. **Functional AST Knowledge Graph Test**: Executes real Python and TypeScript AST parsing, relative import resolution, and call-graph construction in an isolated temp environment.
