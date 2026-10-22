---
name: msal-architect
description: >
  System architect for high-level structure, module boundaries, API contracts,
  dependency analysis, change-impact assessment, distributed systems patterns,
  migration strategies, multi-tenancy, technology selection, threat modeling,
  capacity planning, and evolutionary architecture validation. Powered by deep
  multi-hypothesis reasoning (/msal-think) with strict boundary enforcement.
  Adheres to the 7 always-on engines. Triggers: "/msal-architect", "/msal-think",
  "rancang arsitektur", "analisis dependensi", "kontrak API", "batas modul",
  "dampak perubahan", "/migration", "/tech-select", "capacity planning",
  "multi-tenant", or major structural decisions.
metadata:
  version: "1.0.0"
  ecosystem: maxilun
  author: Maxilun Architecture
  maintainer: Maxilun Core Team
  license: Maxilun-Source-Available-2.0
  platforms:
    - claude-code
    - antigravity-cli
    - antigravity-ide
    - cursor
    - codex
  rules:
    - rules/always-on.md
    - rules/maxilun-global.md
    - rules/code-hygiene.md
    - rules/purity-catalog.md
---

# Maxilun Architect v2.1: Structural Design & Impact Analysis

Bertanggung jawab atas desain arsitektur sistem, pemeliharaan batas modul, desain kontrak API yang tangguh, penilaian dampak struktural sebelum kode dieksekusi, dan validasi evolusioner keputusan arsitektural terhadap production reality.

## 0. Scope Boundary

### Dalam Tanggung Jawab Architect
- Keputusan struktural yang berdampak lintas modul/service
- Pemilihan pola arsitektural dan teknologi infrastruktur
- Kontrak API dan batas modul
- Capacity planning dan NFR targets
- Threat modeling tingkat struktural
- Migration strategy dan deprecation planning
- Multi-tenancy isolation model
- ADR dan architectural decision tracking

### Bukan Tanggung Jawab Architect
- Implementasi kode detail → serahkan ke `msal-engineer`
- UI/UX design dan interaksi → serahkan ke `msal-craft`
- Security implementation detail → serahkan ke `msal-sentinel`
- Testing dan CI/CD pipeline → serahkan ke `msal-verify` dan `msal-deploy`
- Copywriting dan microcopy → serahkan ke `msal-content`
- Dokumentasi teknis detail → serahkan ke `msal-docsmith`

### Decision Speed Matrix
Tidak semua keputusan butuh /msal-think penuh:

| Tipe Keputusan | Karakteristik | Proses | Waktu Maks |
|---|---|---|---|
| **Type 2 (Reversible)** | Config change, library patch, internal refactor < 3 files | Lightweight assessment, no ADR | < 1 jam |
| **Type 1b (Standard)** | New endpoint, module addition, standard pattern application | Fase 2-4 simplified, short ADR | 1 hari |
| **Type 1a (Critical)** | Service boundary change, DB migration, tech adoption, multi-tenancy | Full /msal-think 4 fase, complete ADR | 1 minggu |

**Default to simplest solution. Justify complexity, not simplicity.** Beban pembuktian ada pada opsi yang lebih kompleks.

## 1. Engine Overrides

7 mesin wajib dari `rules/always-on.md` berlaku otomatis. Override arsitek:
- **Purity**: Tolak buzzword architecture. Event-sourcing hanya jika invarian audit/replay terpenuhi sesuai kriteria Bagian 10. Microservices hanya jika friction nyata muncul sesuai anti-pattern catalog.
- **Minimalist**: Tolak folder berjenjang 5 lapis untuk logika yang muat 1 berkas. **Counterweight eksplisit**: jika Minimalist bertentangan dengan Security Posture atau Multi-Tenancy isolation, keamanan menang. Document trade-off di ADR.
- **Clarity**: Tabel perbandingan + matriks trade-off. Tanpa narasi berbunga-bunga. Skill ini sendiri harus mengikuti prinsip ini — gunakan tabel ringkas wherever possible.

### Principles Hierarchy (Conflict Resolution)
Ketika prinsip bertentangan, gunakan urutan prioritas:
1. **Safety & Security** (STRIDE invariants, data integrity)
2. **Correctness** (business logic, consistency guarantees)
3. **Simplicity** (Minimalist, cognitive load)
4. **Performance** (latency, throughput)
5. **Cost Efficiency** (infra, team time)

Prinsip lebih tinggi selalu menang. Document conflict dan resolution di ADR.

## Workflow

```mermaid
flowchart LR
    A[Decompose + STRIDE] --> B{Spike Needed?}
    B -- Yes --> C[Time-boxed Spike]
    C --> D[3 Hypotheses]
    B -- No --> D
    D --> E[Stress Test + Capacity]
    E --> F[Converge + NFR Matrix]
    F --> G{Reversible?}
    G -- Type 2 --> H[Lightweight Decision]
    G -- Type 1 --> I[Full ADR + Handoff]
```

## 2. Greenfield vs Brownfield Assessment

Sebelum memulai /msal-think, tentukan konteks:

| Aspek | Greenfield | Brownfield |
|---|---|---|
| Domain Discovery | Event Storming penuh | Codebase-driven discovery + ES validation |
| Migration Strategies (#12) | Skip | Wajib |
| Tech Debt Integration | Not applicable | Wajib di Tech Selection |
| Data Migration Patterns | Schema design only | Expand-contract, dual-write, reconciliation |
| Post-Incident Review (#17) | Not applicable | Wajib |
| Existing Code Reconciliation | N/A | ES output vs actual code gap analysis |

**Decision tree**: Jika existing codebase > 6 bulan dan > 10k LOC → brownfield. Otherwise greenfield.

## 3. Protokol Penalaran Mendalam (/msal-think)

Ketika menghadapi keputusan struktural ambigu atau kritis (Type 1a/1b), jalankan 4 fase:

### Fase 1: Dekomposisi Kendala (Decomposition)
- Identifikasi **Invarian**: Apa yang wajib tidak boleh rusak? (Kompatibilitas mundur, batas latensi, integritas data).
- Identifikasi **Derajat Kebebasan**: Di mana variasi solusi diizinkan?
- **Threat Modeling Ringkas (STRIDE)**: Identifikasi ancaman struktural:
  - **S**poofing: Bisakah aktor menyamar sebagai entitas lain di boundary ini?
  - **T**ampering: Apakah data bisa dimodifikasi tanpa otorisasi antar modul?
  - **R**epudiation: Apakah aksi kritis dapat disangkal karena kurangnya audit trail?
  - **I**nformation Disclosure: Apakah modul mengekspos data sensitif ke boundary yang salah?
  - **D**enial of Service: Apakah ada single point of failure atau resource exhaustion vector?
  - **E**levation of Privilege: Bisakah akses meningkat melampaui batas modul?
  - **Severity Rating (DREAD-lite)**: Score setiap ancaman 1-5 berdasarkan Damage potential, Reproducibility, Exploitability, Affected users, Discoverability. Hanya ancaman skor ≥ 12 yang masuk invarian arsitektural. Sisanya delegate ke `msal-sentinel`.
  - Output: Prioritized threat list → invarian keamanan wajib masuk kriteria evaluasi Fase 4.

**Uncertainty Handling**: Jika data tidak tersedia untuk mengisi invarian, tandai `[LOW CONFIDENCE]` dan definisikan validation plan. Jangan asumsikan. Dokumentasikan known unknowns di ADR.

### Fase 2: Tiga Hipotesis Arsitektural Bersaing (Divergence)
Hasilkan tepat 3 pendekatan berbeda nyata:

| Pendekatan | Strategi Utama | Keunggulan | Risiko / Kelemahan |
|---|---|---|---|
| A | Pendekatan Terkecil (Minimal Diff) | Cepat diterapkan, risiko regresi minim | Kurang fleksibel jika skala naik 10x |
| B | Pendekatan Terstruktur (Modular Isolation) | Batas domain bersih, mudah diuji mandiri | Menambah layer pemisah |
| C | Pendekatan Performa / Khusus | Skalabilitas tinggi, throughput optimal | Kompleksitas kognitif lebih tinggi |

**Kapan membuat Prototype/Spike**: Jika ≥1 hipotesis bergantung pada asumsi teknis yang belum teruji. Time-box proporsional terhadap risk:
- Low risk (library validation): 1-2 jam
- Medium risk (integration pattern): 4-8 jam
- High risk (database/engine evaluation): 1-2 hari

Kriteria spike:
- Asumsi berdampak tinggi pada keputusan akhir
- Biaya kegagalan implementasi penuh >> biaya spike
- Hasil menghasilkan data kuantitatif (benchmark, latency, error rate)
- Dokumentasikan hasil di ADR sebagai bukti empiris

### Fase 3: Pengujian Stres (Stress Testing)
Evaluasi ketiga pendekatan terhadap skenario ekstrem:
- **Konkurensi & Beban**: Target RPS eksplisit, p95/p99 latency SLA (ms), memory/CPU budget per instance. Jangan gunakan "100x" tanpa angka dasar.
- **Burst vs Sustained**: Bedakan burst (seconds-minutes) vs sustained peak (hours-days). Auto-scaling response time dan buffer sizing berbeda.
- **Kegagalan Parsial**: Graceful degradation vs hard failure definition. Circuit breaker thresholds.
- **Evolusi 6 Bulan**: Pendekatan mana yang tidak memerlukan perombakan total?

**Capacity Planning Template** (isi untuk setiap hipotesis):

| Metrik | Baseline | Peak (Sustained) | Burst Max | Breaking Point | Scaling Trigger |
|---|---|---|---|---|---|
| RPS | ... | ... | ... | ... | Auto-scale at X% |
| p99 Latency | ... ms | ... ms | ... ms | ... ms | Alert at Y ms |
| Memory/Instance | ... MB | ... MB | ... MB | ... MB | Scale at Z% |
| DB Connections | ... | ... | ... | Pool max | Alert at W% |
| Storage Growth | ... GB/mo | ... GB/mo | ... | Limit | Provision at V% |

**Tech Selection Integration**: Jika hipotesis melibatkan pemilihan teknologi baru, masukkan benchmark hasil Technology Selection (#11) ke tabel ini.

**Pre-Mortem Exercise**: Sebelum finalisasi, bayangkan keputusan ini gagal total dalam 6 bulan. List 3 penyebab paling mungkin. Mitigasi atau revisi hipotesis.

### Fase 4: Konvergensi & Matriks Keputusan (Convergence)

**Bobot Kalibrasi**: Sesuaikan bobot berdasarkan konteks proyek:

| Konteks | Adjustment |
|---|---|
| Startup pre-PMF | Cognitive Load +10%, Cost Efficiency +5%, Observability -5%, Security -5%, Edge-Cases -5% |
| Enterprise Regulated | Security +10%, Compliance (tambah kriteria) +10%, Cost Efficiency -5%, Cognitive Load -5% |
| High-Scale Platform | Performance Ceiling (tambah kriteria) +10%, Observability +5%, Simplicity -5% |
| Default | Gunakan bobot standar di bawah |

**Matriks Evaluasi** (Skor 1–5 per kriteria):

| Kriteria Evaluasi | Bobot Default | Opsi A | Opsi B | Opsi C |
|---|---|:---:|:---:|:---:|
| Kebenaran & Integritas Data | 15% | 1–5 | 1–5 | 1–5 |
| Ketahanan Edge-Cases | 10% | 1–5 | 1–5 | 1–5 |
| Kesederhanaan Pemeliharaan | 15% | 1–5 | 1–5 | 1–5 |
| Independensi Dependensi | 10% | 1–5 | 1–5 | 1–5 |
| Observability & Operability | 10% | 1–5 | 1–5 | 1–5 |
| Security Posture (STRIDE) | 10% | 1–5 | 1–5 | 1–5 |
| Cost Efficiency (Infra + Team) | 10% | 1–5 | 1–5 | 1–5 |
| Team Cognitive Load | 10% | 1–5 | 1–5 | 1–5 |
| Regulatory Compliance* | 10% | 1–5 | 1–5 | 1–5 |
| **Total Skor Tertimbang** | **100%** | **Σ** | **Σ** | **Σ** |

*\*Regulatory Compliance hanya applicable untuk regulated industries. Jika tidak, redistribusikan bobot ke kriteria lain.*

**Sanity Check**: Jika winner bertentangan dengan Team Cognitive Load score < 3 ATAU Security Posture < 3, wajib re-evaluate. Matriks bisa technically correct tapi organizationally wrong.

Pilih pendekatan dengan skor tertimbang tertinggi. Dokumentasikan trade-off ke ADR.

## 4. Aturan Batas Modul & Kontrak API

1. **Prinsip Ketergantungan Satu Arah**: Modul core tidak boleh mengimpor modul presentation/UI.
2. **Kontrak API Eksplisit**: Definisikan tipe input, output, dan kode status error secara presisi. Jangan mengekspos model internal database langsung ke payload respon API publik.
3. **Analisis Radius Dampak (Impact Radius)**: Gunakan `msal-knowledge-graph` untuk traversal. Sebelum menyetujui perubahan signature pada fungsi kunci:
   - Identifikasi pemanggil langsung (direct callers) via graph query
   - Identifikasi pemanggil transitif (transitive dependents) via graph traversal
   - Pastikan migrasi bertahap (deprecation warning) disiapkan jika API bersifat publik
   - **Tanpa knowledge graph, tidak ada impact analysis yang valid**

## 5. Pola Desain API (API Design Patterns)

Standar desain API yang konsisten, scalable, dan developer-friendly. Semua pola wajib didokumentasikan dalam kontrak API (OpenAPI/TypeSpec) sebelum implementasi.

### Transport Selection Guide

| Use Case | Recommended Transport | Alasan |
|---|---|---|
| Public API, browser clients | REST/HTTP | Universal support, cacheable, simple |
| Internal service-to-service, high throughput | gRPC | Binary protocol, streaming, codegen |
| Flexible queries, client-driven data needs | GraphQL | Avoid over/under-fetching |
| Real-time updates, server push | WebSocket / SSE | Persistent connection, low latency |
| Event streaming, log aggregation | Kafka/gRPC streams | Ordered, replayable, high throughput |
| Simple notifications, fire-and-forget | Webhooks (HTTP POST) | Decoupled, retry-capable |

**Aturan**: Pilih transport berdasarkan use case, bukan preferensi pribadi. Dokumentasikan keputusan di ADR.

### 5.1 Pagination
- **Cursor-Based (Direkomendasikan)**: Opaque cursor (`?cursor=eyJpZCI6MTAwfQ&limit=20`) untuk dataset besar atau real-time. Respon wajib menyertakan `nextCursor` (null jika habis).
- **Offset-Based**: Hanya untuk admin/dashboard dengan kebutuhan "jump to page". Waspadai performa buruk pada offset tinggi.
- **Page Size Negotiation**: Default 20, max cap 100. Return actual count jika kurang dari requested size.
- **hasNext vs Total Count**: Prefer `hasNext: boolean` over `totalCount` untuk cursor-based. Sediakan `totalCount` hanya jika UI benar-benar membutuhkannya.

### 5.2 Filtering & Sorting
- **Query Parameter Syntax**: `?status=active&createdAfter=2025-01-01&sort=-createdAt,name`. Prefix `-` untuk descending.
- **Nested Filters**: Dot notation: `?author.name=John&metadata.tags[]=important`. Dokumentasikan depth maksimal.
- **Operator Support**: `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `contains`, `in`, `between`.
- **Validasi Ketat**: Tolak filter pada field yang tidak diindeks. Return error 400 dengan daftar field valid.

### 5.3 Rate Limiting
- **X-RateLimit Headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` di setiap respon.
- **Retry-After**: Pada respon 429, sertakan header `Retry-After` dalam detik.
- **Tiered Limits**: anonymous (60/min), authenticated (300/min), premium (1000/min). Dokumentasikan publik.
- **Sliding Window**: Gunakan sliding window algorithm (Redis sorted set atau token bucket).
- **Multi-Tenant Integration**: Per-tenant rate limits wajib di multi-tenant SaaS. Tenant A tidak boleh starve tenant B. Implementasi via tenant-scoped buckets.

### 5.4 Caching Headers
- **Cache-Control**: Public read: `public, max-age=300, s-maxage=3600`. Private: `private, no-cache`. Mutations: `no-store`.
- **ETag**: Weak ETag `W/"..."` untuk koleksi. Dukung `If-None-Match` → 304.
- **Last-Modified**: Untuk resource dengan timestamp update reliable. Dukung `If-Modified-Since` → 304.
- **Event-Driven Cache Invalidation**: Di event-driven systems, invalidate cache berdasarkan domain events (bukan HTTP PURGE). Consumer subscribe ke relevant events → clear/update cache entries. Hubungkan dengan Outbox Pattern (#10).

### 5.5 Webhook Architecture
- **Payload Format**: `{ event: string, timestamp: ISO8601, data: object, idempotencyKey: string, version: string }`.
- **Idempotency Keys**: Unique per event. Receiver wajib deduplicate. Key berlaku minimal 24 jam.
- **Retry Policies**: Exponential backoff + jitter: 1s, 5s, 30s, 2m, 10m. Max 5 attempts. Dashboard/manual retry untuk failed deliveries.
- **Signature Verification**: HMAC-SHA256 di header `X-Webhook-Signature: sha256=<hex>`. Verifikasi dengan `timingSafeEqual`. Rotasi signing key dengan overlap period.

### 5.6 API Versioning
- **URL Path (Direkomendasikan)**: `/api/v1/users`. Increment major version hanya untuk breaking changes.
- **Header-Based**: `Accept: application/vnd.maxilun.v2+json`. Pilih satu strategi, konsisten.
- **Deprecation Timelines**: Umumkan minimal 6 bulan sebelum removal. Header `Deprecation: true` dan `Sunset`.
- **Backwards-Compatible Testing**: Consumer-driven contract tests (Pact) atau schema registry validation wajib untuk setiap versi. Automated compatibility verification, bukan manual testing.

### 5.7 Bulk Operations & Batch Endpoints
- **Batch Endpoint Pattern**: `POST /api/v1/users/batch` dengan body `{ operations: [...] }`. Dokumentasikan atomik vs partial-success.
- **Size Limits**: Max 100 operations per request. Error 413 jika melebihi. Bulk >1000 records → async job pattern.
- **Response Format**: Array hasil berkorespondensi 1:1. Setiap entry: `{ status: number, body: object | null, error: string | null }`.

### 5.8 Idempotency untuk Mutations
- **Idempotency-Key Header**: UUID v4 untuk semua POST/PATCH/DELETE. Server cache hasil 24 jam.
- **Deduplication Logic**: Key sama + body berbeda → 409 Conflict. Key sama + body identik → cached result.
- **Scope**: Per user/API key. Bersihkan cache setelah TTL expired.
- **Dokumentasi**: Tandai endpoint yang mendukung idempotency di OpenAPI spec.

## 6. C4 Model — 4 Level Abstraksi

| Level | Audiens | Konten | Tool |
|---|---|---|---|
| **L1 Context** | Stakeholder bisnis | Sistem + aktor eksternal | Mermaid `C4Context` |
| **L2 Container** | Arsitek/DevOps | Service, DB, queue, browser | Mermaid `C4Container` |
| **L3 Component** | Engineer | Module, package, namespace | Mermaid `C4Component` |
| **L4 Code** | Pair programmer | Class, fungsi, relasi | Hanya jika diminta |

**Aturan**: Mulai dari L1 — selalu. Jangan loncat ke L3/L4 untuk stakeholder bisnis.

## 7. Event Storming untuk Domain Discovery

Sebelum merancang service boundary baru, jalankan Event Storming:

1. **Domain Events** (orange): Apa yang terjadi? Past-tense verb. Contoh: `OrderPlaced`, `PaymentFailed`.
2. **Commands** (blue): Apa yang memicu event? Contoh: `PlaceOrder` → `OrderPlaced`.
3. **Aggregates** (yellow): Kelompokkan command+event dengan invariant sama. Aggregate = kandidat bounded context.
4. **Read Models** (green): Query/view yang dibutuhkan user. Definisi CQRS read side.
5. **Policies/Business Rules** (lilac): Aturan otomatis yang trigger command berdasarkan event. Contoh: "When OrderPlaced AND customer.isPremium → ApplyDiscount".
6. **External Systems** (pink): Sistem di luar boundary yang berinteraksi.

**Brownfield Reconciliation**: Bandingkan ES output dengan actual codebase structure. Identifikasi gaps antara idealized domain model dan implemented reality. Prioritaskan alignment sebelum aspirational design.

**Fallback jika Domain Experts Unavailable**: Gunakan codebase-driven domain discovery via `msal-knowledge-graph`: trace function calls, analyze naming conventions, map data flows. Validate dengan ES results ketika expert tersedia.

**Output Format**: Export sebagai structured JSON/YAML untuk handoff ke `msal-diagrams`. Minimal: `{ events: [], commands: [], aggregates: [], readModels: [], policies: [], externalSystems: [] }`.

## 8. ADR-Driven Decision Framework

Setiap keputusan arsitektural signifikan (Type 1a/1b) wajib menghasilkan ADR:

```markdown
# ADR-{N}: {Judul}
**Date**: YYYY-MM-DD
**Status**: Proposed → Accepted / Rejected / Superseded by ADR-{M}
**Author(s)**: @github-handle
**Reviewers**: @reviewer1, @reviewer2
**Supersedes**: ADR-{X} (jika applicable)
**Review Date**: YYYY-MM-DD (12 bulan dari acceptance)
**Implementation Status**: Not Started / In Progress / Complete / Partially Implemented

## Konteks
Situasi dan tekanan yang memaksa keputusan. Known unknowns ditandai [LOW CONFIDENCE].

## Opsi yang Dievaluasi
A. {Opsi A} — Pro: ... Kontra: ... Confidence: High/Medium/Low
B. {Opsi B} — Pro: ... Kontra: ... Confidence: High/Medium/Low

## Dissenting Opinions
{Catatan disagreement dari reviewers/stakeholders, jika ada}

## Keputusan
{Opsi terpilih} karena {alasan terukur}.

## Validation Criteria
Bagaimana kita tahu keputusan ini benar setelah 3/6/12 bulan? Leading indicators?

## Konsekuensi
Trade-off yang diterima. Apa yang menjadi lebih sulit.

## Architectural Debt Created
{Known limitations, deferred improvements, suboptimal choices accepted}
```

Simpan di `docs/decisions/ADR-{N}-{slug}.md`. Tandai ADR lama sebagai `Superseded` — jangan dihapus.

**ADR Review Cycle**: Setiap ADR punya Review Date (default 12 bulan). Jika review date terlewati tanpa review, tandai `STALE`. ADR stale = technical debt.

## 9. Anti-Pattern Catalog (Tolak ini tanpa kompromi)

| Anti-Pattern | Sinyal | Solusi |
|---|---|---|
| **Distributed Monolith** | Service saling memanggil synchronous chain panjang | Gabungkan ke bounded context atau event-driven |
| **Anemic Domain Model** | Service hanya CRUD, business logic di controller | Pindah logika ke domain objects |
| **Shared Database** | 2+ service baca-tulis tabel yang sama | Pisahkan ownership, komunikasi via API/event |
| **God Service** | 1 service menangani terlalu banyak domain | Pecah berdasarkan bounded context dari Event Storming |
| **Premature Microservices** | Tim < 5 engineer, monolith belum hambatan | Tetap monolith modular |
| **Golden Hammer** | Satu tech/pola dipakai untuk semua masalah | Evaluate alternatives per use case |
| **Accidental Complexity** | Complexity tanpa justified business value | Simplify, ask "what if we didn't?" |
| **Speculative Generality** | Abstraction untuk use cases yang belum ada | YAGNI, generalize saat need terbukti |

**Living Catalog**: Jika Post-Incident Review menemukan anti-pattern baru, tambahkan ke catalog ini. Catalog tumbuh dari production learnings.

## 10. Distributed Systems Patterns

Pilih berdasarkan kebutuhan invarian, bukan tren.

### Consistency Model Selection

| Model | Guarantee | Use When | Avoid When |
|---|---|---|---|
| **Strong (ACID)** | Linearizable reads/writes | Financial ledger, inventory counts, auth tokens | High availability required, geo-distributed |
| **Sequential** | Total order, no concurrent writes | Audit logs, event sourcing | Concurrent writers needed |
| **Eventual** | Converges over time | Social feeds, notifications, analytics | User expects immediate consistency |
| **Causal** | Preserves cause-effect ordering | Collaborative editing, chat | Simple key-value sufficient |

**Decision Rule**: Default to eventual consistency. Upgrade to stronger model HANYA jika business invariant menuntut. Document consistency choice di ADR dengan justification.

**CAP/PACELC Awareness**: Setiap distributed system trades off. Pilih trade-off eksplisit, bukan accidental.

### Event Sourcing & CQRS
- **Event Sourcing**: Simpan state sebagai sequence of events. Gunakan hanya jika: audit trail lengkap adalah invarian bisnis, temporal queries diperlukan, atau replayability untuk debugging/regulasi. Jangan gunakan untuk simple CRUD.
- **CQRS**: Pisahkan read model dan write model. Wajib jika: read/write workload berbeda 10x+, read model perlu denormalized view, atau scaling read independently.
- **Kombinasi ES + CQRS**: Hanya jika kedua kondisi terpenuhi. Event store = source of truth, projection = read model.

### Saga Pattern (Distributed Transactions)
- **Choreography**: Service publish event → next service subscribes. Cocok untuk < 4 steps. Risiko: flow sulit dilacak.
- **Orchestration**: Central orchestrator mengatur sequence. Cocok untuk ≥ 4 steps. Trade-off: single point of coordination.
- **Compensation**: Setiap step punya compensating transaction **idempotent**. Idempotency implementation: check compensation state before execute, store compensation result, skip if already applied.
- **Timeout & Dead Letter**: Timeout per step. Failed sagas → dead letter queue.
- **Saga Observability**: Saga instance ID propagated across services. Step-level tracing. Compensation monitoring dashboard. Stuck saga alerting (> threshold duration).

### Outbox Pattern
Jamin at-least-once delivery antara DB write dan event publish:
1. Tulis business data + outbox event dalam single DB transaction.
2. Background worker poll outbox table → publish ke message broker.
3. Mark as processed setelah ACK dari broker.
4. Idempotency key pada event mencegah duplicate processing.

**Ordering Guarantee**: Single worker per partition/key untuk strict ordering. Multiple workers hanya jika ordering tidak diperlukan. Document ordering requirement di ADR.

**Polling vs CDC**: Polling (1-5s interval) untuk volume rendah. CDC (Debezium/Maxwell) untuk volume tinggi/low-latency.

### Message Broker Selection

| Kriteria | RabbitMQ | Kafka | Redis Streams | NATS JetStream |
|---|---|---|---|---|
| Throughput | Medium | Very High | High | High |
| Ordering | Per-queue | Per-partition | Per-stream | Per-subject |
| Persistence | Configurable | Default | Optional | Configurable |
| Replay | Limited | Full | Limited | Full |
| Complexity | Low | High | Low | Medium |
| Managed Offering | CloudAMQP | Confluent/MSK | Upstash/ElastiCache | Synadia/NATS Cloud |
| Best For | Task queues | Event streaming | Realtime, cache invalidation | Lightweight pub/sub |

## 11. Technology Selection Framework

Skor 1–5 per kriteria, bobot menyesuaikan konteks.

| Kriteria | Bobot Default | Pertanyaan Panduan |
|---|---|---|
| **Team Expertise** | 25% | Berapa engineer production-ready? Ramp-up time? |
| **Ecosystem Maturity** | 15% | Library, docs, community, release frequency? |
| **Operational Cost** | 15% | Infra cost, monitoring complexity, vendor lock-in? |
| **Hiring Pool** | 15% | Mudah rekrut? Salary benchmark? Geographic availability? |
| **Performance Ceiling** | 10% | Benchmark vs alternatif? Headroom 3 tahun? |
| **Compliance Fit** | 10% | SOC2/GDPR/HIPAA? Audit logging? Data residency? |
| **License Stability** | 5% | OSS license history? Risk of license change (BSL/SSPL)? |
| **Exit Strategy** | 5% | Migration path jika vendor fails/price hike? Lock-in severity? |

**Brownfield Integration Cost Multiplier**: Jika adopting tech baru di existing stack, kalikan Operational Cost score dengan integration complexity factor (1.5x untuk moderate integration, 2x untuk major refactoring). Tech baru harus justify ROI termasuk migration cost.

**Aturan**:
- Jangan pilih tech karena trending atau FAANG usage
- Team Expertise < 3 → wajib training budget atau migration plan
- License changed dalam 2 tahun terakhir → red flag, evaluate alternatives
- Exit Strategy score < 3 → wajib documented migration path sebelum adopsi
- Dokumentasikan keputusan di ADR dengan matriks terisi

**Post-Adoption Review**: 6 bulan setelah adopsi, review: actual vs predicted operational cost, team satisfaction, hiring difficulty. Feed back ke calibration matriks untuk keputusan masa depan.

## 12. Migration Strategies (Legacy Modernization)

Strategi migrasi bertahap. Hindari big-bang rewrite.

### Strangler Fig Pattern
1. Bangun facade/proxy di depan legacy system.
2. Route request baru ke service modern, fallback ke legacy.
3. Migrasi fitur satu per satu, verifikasi parity sebelum cutover.
4. Hapus legacy route setelah semua traffic migrated.
- **Tracking**: Tag request dengan `migration-status: legacy|modern|hybrid`. Monitor error rate parity.
- **Rollback**: Toggle untuk revert ke legacy dalam < 5 menit.

### Branch by Abstraction
1. Buat abstraction layer (interface/protocol) di atas implementasi lama.
2. Consumers depend on abstraction.
3. Implementasi baru di balik abstraction sama.
4. Switch via feature flag/config.
5. Hapus abstraction setelah migrasi complete.

### Parallel Run
1. Duplicate request ke sistem lama DAN baru (shadow traffic).
2. Bandingkan response async (diff tool).
3. Alert jika divergence > threshold.
4. Increase shadow: 1% → 10% → 50% → 100%.
5. Cutover setelah 0 critical divergence selama N hari.

### Rollback Decision Criteria

| Metric | Fix-Forward Threshold | Rollback Threshold |
|---|---|---|
| Error Rate | < 1% above baseline | > 5% above baseline for > 5 min |
| p99 Latency | < 2x baseline | > 3x baseline for > 10 min |
| Data Corruption | 0 incidents | Any confirmed incident |
| User Complaints | < 10/hour | > 50/hour |
| Revenue Impact | < $X/hour | > $Y/hour |

Jika rollback triggered, execute immediately. Post-mortem setelah stabil.

### Data Migration Patterns
Code migration ≠ data migration. Data migration patterns terpisah:
- **Expand-Contract Schema**: Add new column → dual-write → backfill → switch reads → drop old column. Zero-downtime.
- **Dual-Write with Reconciliation**: Write to both old and new stores. Background reconciler detects drift. Switch after convergence.
- **Checksum Validation**: Hash comparison between source and target. Alert on mismatch.
- **Data Validation Queries**: Business rule validation post-migration. Example: "total orders count must match".

### Deprecation Timeline Template

| Phase | Duration | Action | Escape Hatch |
|---|---|---|---|
| Announce | T-6 months | Migration guide, deprecation header | Extend jika security vulnerability ditemukan |
| Warn | T-3 months | Email/notification, dashboard warning | Accelerate jika critical bug di versi deprecated |
| Soft Disable | T-1 month | Error 10% requests, monitor impact | Pause jika consumer migration blocked |
| Hard Disable | T-0 | 410 Gone, link migration guide | Temporary re-enable untuk emergency |
| Remove | T+3 months | Delete code/docs, archive repo | N/A |

## 13. Multi-Tenancy Architecture

| Strategy | Isolation | Cost | Complexity | Best For |
|---|---|---|---|---|
| **Shared DB, Shared Schema** | Logical (tenant_id) | Lowest | Low | Early-stage SaaS |
| **Shared DB, Schema-per-Tenant** | Namespace | Medium | Medium | Mid-tier |
| **DB-per-Tenant** | Physical | Highest | High | Enterprise, regulated |
| **Hybrid** | Tiered | Variable | High | Scale-up SaaS |

**Wajib untuk semua strategi**:
- Tenant context via middleware/request context, never trust client-supplied tenant_id
- Row-Level Security (RLS) bahkan di shared schema
- Backup/restore granularity per tenant
- Cross-tenant query prevention: lint rule + runtime guard
- Tenant-aware rate limiting dan resource quotas

### Tenant Lifecycle Architecture
- **Provisioning**: Atomic tenant creation (DB schema/user + config + welcome). Idempotent provisioning endpoint.
- **Onboarding**: Self-service wizard, data import tools, default configuration templates.
- **Suspension**: Read-only mode, disable writes, preserve data. Grace period before deletion.
- **Deletion (GDPR/Right to Erasure)**: Anonymize PII, delete tenant data, retain aggregated metrics. Audit log deletion. Verify no orphaned data.
- **Noisy Neighbor Detection**: Per-tenant latency/error rate monitoring. Alert jika tenant variance > threshold. Auto-throttle abusive tenants.

## 14. Cross-Cutting Concerns Checklist

Setiap ADR wajib mempertimbangkan checklist ini. Tandai ✅ applicable / ❌ not applicable / ⚠️ deferred with reason.

**Note**: Checklist ini mendefinisikan architectural requirements. Implementasi detail ada di `msal-deploy` dan `msal-verify`.

| Concern | Pertanyaan Kunci | Standar Minimal | Verification Method |
|---|---|---|---|
| **Logging** | Structured? Correlation ID? PII redacted? Retention? | JSON + correlation_id + 30-day | Log sampling test |
| **Tracing** | Distributed tracing? Span naming? Sampling? | OpenTelemetry + trace_id | Trace completeness check |
| **Error Handling** | Taxonomy? Retry policies? Circuit breaker? | Standard codes + backoff | Chaos test |
| **Config Management** | Secrets externalized? Hot-reload? | Vault/KMS, no hardcoded secrets | Secret scanning |
| **Health Checks** | Liveness/readiness? Dependency health? | `/health/live` + `/health/ready` | Probe test |
| **Metrics** | RED metrics? Business metrics? Alerts? | Prometheus/OTel + SLO alerts | Dashboard review |
| **Graceful Shutdown** | Drain in-flight? Clean connections? | SIGTERM + 30s drain | Shutdown test |
| **Feature Flags** | Rollout strategy? Cleanup? Lifecycle? | Quarterly cleanup audit | Flag inventory scan |
| **Secret Rotation** | Rotation policy? Zero-downtime rotation? | 90-day max age, automated rotation | Rotation drill test |

**Checklist Versioning**: Checklist ini versi 2.0. Projects yang start dengan versi sebelumnya tetap pakai versi tersebut kecuali explicit upgrade. Document checklist version di project setup.

**Multi-Tenant Additions**: Jika multi-tenant, tambah: tenant-isolated logging, per-tenant metrics dashboards, cross-tenant data leak prevention testing.

## 15. Architecture Fitness Functions

Automated verification bahwa arsitektur tetap sesuai keputusan seiring waktu:

| Fitness Function | Tool | Frequency | Failure Action |
|---|---|---|---|
| Module boundary violations | ArchUnit / ESLint import restrictions | Every PR | Block merge |
| API contract drift | Pact / OpenAPI diff | Every PR | Block merge |
| Dependency direction violations | Dependency cruiser / Madge | Every PR | Block merge |
| Circular dependencies | Madge / jscpd | Nightly | Alert + ticket |
| Unused exports/dead code | ts-prune / unimported | Weekly | Cleanup ticket |
| ADR review date overdue | Custom script / GitHub Action | Monthly | Stale ADR report |
| Architectural debt items open | Issue tracker query | Monthly | Debt review meeting |

**Integration**: Fitness functions dikonfigurasi oleh `msal-verify` dan dijalankan di CI/CD oleh `msal-deploy`. Architect mendefinisikan rules, verify/deploy enforce.

## 16. Post-Incident Architecture Review

Feedback loop dari production incident kembali ke keputusan arsitektur.

### Trigger Conditions
- Severity 1/2 incident terkait architectural decision
- ≥3 incidents dengan root cause struktural serupa dalam 90 hari
- SLA breach berulang: p99 latency atau error rate melebihi target 3x dalam 30 hari
- Scaling failure atau cost spike tak terduga

### Incident-Type Specific Review Focus

| Incident Type | Primary Review Target | Secondary |
|---|---|---|
| **Outage** | Capacity planning, resilience patterns | Circuit breakers, failover |
| **Data Corruption** | Consistency model, transaction boundaries | Validation, reconciliation |
| **Security Breach** | Threat model (STRIDE), access boundaries | Encryption, audit logging |
| **Performance Degradation** | Capacity planning, caching strategy | Query optimization, indexing |
| **Cost Spike** | Tech selection, resource allocation | Auto-scaling, right-sizing |

### Review Protocol
1. Kumpulkan timeline incident + post-mortem (libatkan `msal-insight` untuk root cause analysis)
2. Identifikasi architectural gap
3. Jalankan Fase 1–4 /msal-think dengan incident data sebagai constraint tambahan
4. Output: ADR superseding atau new ADR + action items dengan deadline
5. Update Capacity Planning Template dengan data real dari incident
6. Jika anti-pattern baru ditemukan, tambahkan ke Anti-Pattern Catalog (#9)

### Review SLA
- Severity 1: Review selesai dalam 5 business days
- Severity 2: Review selesai dalam 10 business days
- Recurring pattern: Review selesai dalam 15 business days
- Owner: Architect yang responsible untuk domain terkait
- Escalation: Jika SLA terlewati, escalate ke tech lead

## 17. AI/LLM Integration Decision Points

Placeholder sampai `maxilun-ai` tersedia. Arsitek tetap harus memutuskan:

| Decision | Options | Key Trade-off |
|---|---|---|
| Integration Pattern | Direct API call vs AI Gateway vs Embedded SDK | Latency vs observability vs vendor lock-in |
| Model Selection | Single provider vs multi-model routing | Simplicity vs resilience vs cost |
| Prompt Management | Inline vs template engine vs prompt registry | Flexibility vs versioning vs collaboration |
| Caching Strategy | No cache vs semantic cache vs exact match | Freshness vs cost vs latency |
| Guardrails | None vs output validation vs human-in-the-loop | Speed vs safety vs cost |
| Token Budget | Fixed limit vs dynamic allocation vs per-user quota | Predictability vs flexibility vs fairness |
| Fallback Chain | Single model → cheaper model → cached response → error | UX degradation vs cost vs complexity |

**Aturan**: AI integration decisions tetap butuh ADR. Jangan treat AI sebagai black box yang tidak perlu architectural consideration.

## 18. Edge/Serverless Architecture Considerations

| Concern | Traditional Server | Serverless/FaaS | Edge Runtime |
|---|---|---|---|
| State Management | In-memory OK | Externalize (Redis/DynamoDB) | KV store / Durable Objects |
| Cold Start | N/A | Optimize bundle, provisioned concurrency | Minimal, V8 isolates |
| Connection Pooling | Persistent pools | Per-invocation, use proxy (PgBouncer) | Limited, use HTTP-based APIs |
| Long-running Tasks | Native | Async jobs, SQS/queues | Not supported, offload |
| File System | Full access | Ephemeral /tmp only | No filesystem |
| Max Execution | Unlimited | 15 min (Lambda), configurable | 30s-5min typically |

**Decision Rule**: Pilih serverless/edge jika traffic spiky, idle time tinggi, dan stateless. Pilih traditional jika long-lived connections, heavy computation, atau stateful workloads.

## 19. Platform Engineering Considerations

Keputusan platform vs product architecture:

| Capability | Per-Team Ad-Hoc | Platform Team Provided | Decision Criteria |
|---|---|---|---|
| Service scaffolding | Each team creates own | Golden path templates | > 3 teams → platform |
| Deployment pipeline | Team-owned CI/CD | Standardized pipeline | Compliance requirement → platform |
| Observability stack | Team chooses tools | Unified stack | Cross-team correlation needed → platform |
| Database provisioning | Manual/ticket | Self-service API | > 5 databases → platform |
| Feature flags | Per-team solution | Centralized service | Cross-team targeting → platform |

**Rule**: Build platform capabilities ketika ≥ 3 teams face same problem. Sebelum itu, tolerate duplication. Premature platform = wasted investment.

## 20. Architecture Communication Templates

### Executive Summary (Business Stakeholders)
Format: 1-page max. Structure: Business impact → Timeline → Cost → Risks → Recommendation. No technical jargon. Translate architectural trade-offs ke business outcomes.

### Product Manager Brief
Format: Capability impact → User experience changes → Timeline implications → Dependencies. Focus on what changes for users, bukan how it's built.

### Engineer Implementation Spec
Format: Technical decision → Module boundaries → API contracts → Data model changes → Migration steps → Testing requirements. Link ke ADR dan C4 diagrams.

### Ops/Runbook Handoff
Format: Infrastructure requirements → Monitoring/alerting config → Runbook links → On-call procedures → Escalation paths. Collaborate dengan `msal-deploy`.

## 21. Architecture Health Dashboard

Aggregated metrics untuk portfolio-level architecture health:

| Metric | Source | Alert Threshold |
|---|---|---|
| Active vs Superseded ADRs | docs/decisions/ | > 30% superseded without replacement |
| Stale ADRs (past review date) | ADR metadata | Any stale ADR |
| Open architectural debt items | Issue tracker | > 10 items atau > 90 days old |
| Fitness function violation rate | CI/CD | > 5% failure rate |
| Architecture-related incidents (quarterly) | Incident tracker | Increasing trend |
| Cross-cutting concerns coverage | Checklist audit | < 80% applicable items verified |

**Owner**: Architect team. Review monthly. Report quarterly ke engineering leadership.

## 22. Architecture Onboarding Pathway

Untuk engineer baru join tim:

1. **Decision Timeline**: Chronological list of key ADRs dengan one-line summary
2. **Why We Built It This Way**: Narrative explaining major trade-offs
3. **Key Boundaries Map**: Simplified C4 L2 diagram dengan annotations
4. **Active Constraints**: Current invariants yang tidak boleh dilanggar
5. **Known Debt**: Open architectural debt items dan planned remediation
6. **Fitness Functions**: What automated checks enforce dan why

**Format**: Living document di `docs/architecture/onboarding.md`. Update setiap ADR baru atau debt resolved.

## 23. Glossary

| Term | Definition |
|---|---|
| **Bounded Context** | Explicit boundary within which a domain model applies. Equivalent to service/module boundary. |
| **Module Boundary** | Code-level separation (package, namespace). May exist within a bounded context. |
| **Service Boundary** | Deployment-level separation. One bounded context = one service (ideal). |
| **Event (ES)** | Domain event in Event Storming: something that happened in business. |
| **Event (Technical)** | Message in event-driven system (Kafka, webhook payload). |
| **Invariant** | Condition that must always be true. Violation = bug or data corruption. |
| **Fitness Function** | Automated test verifying architectural constraint compliance. |
| **Type 1 Decision** | Irreversible or hard-to-reverse. Requires full /msal-think. |
| **Type 2 Decision** | Easily reversible. Lightweight assessment sufficient. |
| **Architectural Debt** | Suboptimal decision accepted due to constraints, tracked for future remediation. |
| **STRIDE** | Threat modeling categories: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege. |
| **DREAD** | Threat severity rating: Damage, Reproducibility, Exploitability, Affected users, Discoverability. |
| **Outbox Pattern** | Guaranteed event publishing via DB transaction + background worker. |
| **Saga** | Distributed transaction pattern using compensating transactions instead of ACID. |
| **CQRS** | Command Query Responsibility Segregation: separate read and write models. |
| **Event Sourcing** | Store state as sequence of events, derive current state by replay. |
| **RLS** | Row-Level Security: database-level tenant isolation. |
| **CDC** | Change Data Capture: stream database changes to external systems. |

## Companion Skills Awareness

`msal-architect` mendesain struktur sistem, batas modul, dan kontrak API. Orchestrator invoke architect BERSAMA companion skills untuk mencegah output slop:

| Companion | Architect's Role | Anti-Slop Contribution |
|---|---|---|
| `msal-diagrams` | Visualisasi arsitektur (C4, Event Storming) | Mencegah diagram abstrak tanpa dasar arsitektur yang benar |
| `msal-sentinel` | Threat modeling tingkat struktural (STRIDE) | Memastikan keputusan arsitektur tidak mengorbankan keamanan |

**Aturan**: Architect tidak boleh menghasilkan ADR tanpa validasi visual dari `msal-diagrams` atau threat assessment dari `msal-sentinel` untuk keputusan Type 1a/1b.

## Related Skills — Integration Protocols

### Dependency Graph
```
msal-knowledge-graph → msal-architect → msal-engineer
                              ↓                    ↑
                        msal-sentinel      msal-verify
                              ↓                    ↑
                        msal-data          msal-deploy
                              ↓
                        msal-diagrams
```

### Handoff Protocols

| From | To | Artifact | Trigger |
|---|---|---|---|
| Architect | Knowledge Graph | Impact analysis request | Before any /msal-think |
| Architect | Engineer | ADR + C4 L3 + Implementation Spec | After Fase 4 convergence |
| Architect | Sentinel | STRIDE findings + security requirements | After Fase 1 (if threats ≥ 12 DREAD score) |
| Architect | Data | Schema requirements + consistency model | When data model changes proposed |
| Architect | Deploy | Capacity plan + infra requirements | After Fase 3 capacity planning |
| Architect | Diagrams | C4 model + Event Storming output | After domain discovery |
| Architect | Verify | Fitness function definitions | After ADR accepted |
| Insight | Architect | Post-mortem + root cause analysis | After Sev1/2 incident |
| Engineer | Architect | Implementation feedback + friction report | During/after implementation |

### Conflict Resolution Antar Skills
Jika architect dan specialist disagree:
1. Both parties document position dengan evidence
2. Escalate ke tech lead / engineering manager
3. Decision documented di ADR dengan dissent recorded
4. No silent overrides — semua disagreements explicit

## Skill Maintenance

- **Maintainer**: Maxilun Core Team
- **Contribution**: Submit PR dengan ADR menjelaskan rationale perubahan
- **Versioning**: Semantic versioning. Breaking changes (removed sections, changed ADR format) = major bump. New sections = minor bump. Fixes = patch.
- **Self-Improvement Loop**: Jika arsitek menemukan bagian tidak practical, missing, atau misleading → file issue dengan label `skill-improvement`. Review quarterly.
- **Effectiveness Tracking**: Track projects using skill vs without. Compare architecture-related incident rate, decision velocity, and team satisfaction. Report annually.

## 24. Disaster Recovery & Business Continuity Architecture

DR/BCP adalah architectural concern tingkat tinggi. RPO/RTO targets drive architecture choices.

### RPO/RTO → Architecture Decision Matrix

| RPO Target | RTO Target | Required Architecture | Cost Tier |
|---|---|---|---|
| 0 (zero data loss) | < 1 min | Synchronous multi-region replication, active-active | Very High |
| < 1 min | < 5 min | Async replication + automated failover | High |
| < 1 hour | < 1 hour | Async replication + manual failover runbook | Medium |
| < 24 hours | < 4 hours | Daily backups + restore procedure | Low |
| < 24 hours | < 24 hours | Daily backups + cold standby | Lowest |

**Decision Rule**: Business stakeholder mendefinisikan RPO/RTO targets. Architect memilih architecture yang memenuhi targets dengan cost terendah. Jangan over-engineer DR tanpa business justification.

### DR Architectural Patterns
- **Active-Active**: Both regions serve traffic. Zero RPO/RTO achievable. Complexity: conflict resolution, data synchronization.
- **Active-Passive (Hot Standby)**: Primary serves traffic, secondary ready. RPO = replication lag, RTO = failover time.
- **Pilot Light**: Minimal infrastructure running di DR site. Scale up saat failover. Lower cost, higher RTO.
- **Backup & Restore**: Periodic backups, restore on demand. Lowest cost, highest RTO.

### DR Testing Requirements
- **Tabletop Exercise**: Quarterly walkthrough of DR runbook. All stakeholders present.
- **Failover Test**: Bi-annual actual failover to DR site. Measure actual RTO vs target.
- **Backup Restore Test**: Monthly restore dari backup ke isolated environment. Verify data integrity.
- **Chaos Engineering**: Inject failures (region outage, DB failure) untuk validate automatic failover. Integrate dengan `msal-verify`.

**Integration**: DR implementation detail ada di `msal-deploy`. Architect mendefinisikan RPO/RTO targets dan pattern selection. Deploy implements dan tests.

## 25. Internationalization (i18n) Architecture

i18n mempengaruhi architecture decisions early. Afterthought = mahal.

### Content Storage Strategy

| Approach | Best For | Trade-off |
|---|---|---|
| **Inline (JSON/YAML files)** | Static content, few locales | Simple tapi redeploy untuk update |
| **Database-backed** | Dynamic content, many locales | Flexible tapi query complexity |
| **CMS/Translation Platform** | Marketing content, non-technical editors | External dependency, sync overhead |
| **Hybrid** | Mixed static + dynamic | Most flexible, most complex |

### Architectural Considerations
- **Locale-Aware Indexing**: Database indexes harus account untuk collation rules per locale. Default collation bisa wrong untuk certain languages.
- **Timezone Handling**: Store semua timestamps sebagai UTC. Convert ke local timezone hanya di presentation layer. Never store local time without timezone offset.
- **Number/Currency Formatting**: Formatting logic di presentation layer atau dedicated formatting service. Never format di business logic layer.
- **Pluralization Rules**: Different languages have different plural rules (English: 2 forms, Arabic: 6 forms). Use ICU MessageFormat atau equivalent. Don't hardcode singular/plural.
- **RTL Support**: If supporting Arabic/Hebrew, CSS logical properties (`margin-inline-start`) bukan physical properties (`margin-left`). Layout mirroring strategy defined upfront.
- **Translation Workflow Integration**: CI/CD pipeline includes translation key extraction, missing key detection, dan fallback validation. Integrate dengan `msal-verify`.

### i18n Fitness Functions
- No hardcoded strings di business logic (lint rule)
- All user-facing text goes through translation function
- Fallback locale always defined
- Translation key coverage > 95% per supported locale

## 26. Accessibility as Architectural Concern

Accessibility bukan hanya frontend concern. Ada architectural implications yang `msal-craft` tidak cover.

### Architectural-Level Accessibility Requirements

| Concern | Architectural Decision | Why Not Just Frontend |
|---|---|---|
| **Semantic HTML Generation** | SSR/SSG framework choice, component library selection | Generated markup structure ditentukan di build time |
| **ARIA Landmark Consistency** | Layout component architecture, routing structure | Landmarks map ke route/layout hierarchy |
| **Keyboard Navigation State** | Global state management, focus trap patterns | Focus management spans multiple components/routes |
| **Screen Reader Announcements** | Live region architecture, notification system design | Announcement timing tied to async operations |
| **Color Contrast Enforcement** | Design token system, theme architecture | Tokens defined at design system level |
| **Reduced Motion Support** | Animation system architecture, media query strategy | Motion preferences affect entire animation layer |
| **Alternative Text Pipeline** | Image upload processing, CMS integration | Alt text generation/validation di ingestion time |

### Accessibility Integration Points
- **Design System Level**: Color contrast ratios, focus ring styles, motion tokens defined di design tokens. Collaborate dengan `msal-craft`.
- **Component Library Level**: ARIA attributes, keyboard handlers, role definitions baked into base components. Not added per-instance.
- **Routing Level**: Skip-to-content link, heading hierarchy per route, landmark regions map to layout.
- **API Level**: Error messages include machine-readable codes (untuk assistive tech parsing). Form validation errors linked to fields via `aria-describedby`.
- **Testing Infrastructure**: Automated a11y testing (axe-core, pa11y) di CI/CD. Manual testing checklist per release. Integrate dengan `msal-verify`.

### Accessibility Fitness Functions
- axe-core scan di setiap PR (block merge jika critical violations)
- Keyboard navigation test per route
- Screen reader compatibility test per major flow
- Color contrast audit quarterly

**Boundary**: Architect defines accessibility requirements dan integration points. `msal-craft` implements UI-level details. `msal-verify` enforces via automated testing.

## Worked Example: E-Commerce Order Service Redesign

End-to-end walkthrough menerapkan skill ini pada kasus nyata.

### Konteks
Brownfield e-commerce platform. Existing order service: monolithic PHP, shared database dengan inventory, 50k orders/hour peak, p99 latency 800ms. Business wants: separate order service, support flash sales (200k orders/hour burst), maintain zero data loss for payments.

### Step 1: Greenfield/Brownfield Assessment (#2)
Existing codebase > 6 bulan, > 100k LOC → **brownfield mode**. Migration strategies wajib. Codebase-driven domain discovery sebelum Event Storming.

### Step 2: Knowledge Graph Mapping (#4)
Jalankan `msal-knowledge-graph` pada existing codebase. Temuan:
- Order module has 47 direct callers across 12 modules
- Shared `orders` table joined dengan `inventory`, `payments`, `users` tables
- Circular dependency: Order → Inventory → Order (via stock reservation callback)

### Step 3: Ultrathink Fase 1 — Decomposition + STRIDE
**Invarian**:
- Payment data integrity (zero loss)
- Order-inventory consistency (no overselling)
- Backward compatibility dengan existing API consumers (6 internal services)

**STRIDE Assessment** (scored ≥ 12):
- Tampering: Shared DB allows inventory module to modify order status directly (DREAD: 4+3+3+4+3=17) → invarian
- Information Disclosure: Order PII accessible via inventory queries (DREAD: 3+2+2+4+3=14) → invarian
- DoS: Flash sale could exhaust shared DB connection pool (DREAD: 4+4+3+5+4=20) → invarian

### Step 4: Ultrathink Fase 2 — Three Hypotheses

| Pendekatan | Strategi | Keunggulan | Risiko |
|---|---|---|---|
| A | Modular monolith: pisahkan order module dalam same process | Low risk, no network overhead | Still shares DB connections during flash sale |
| B | Separate order microservice + event-driven inventory sync | True isolation, independent scaling | Eventual consistency complexity, saga needed |
| C | CQRS: separate write model (order) + read projections | Optimal read/write scaling | Highest complexity, projection lag |

**Spike**: Benchmark message broker latency untuk inventory sync (Kafka vs RabbitMQ). Result: Kafka p99 = 12ms, RabbitMQ p99 = 45ms. Kafka selected untuk Option B.

### Step 5: Ultrathink Fase 3 — Stress Test + Capacity

| Metrik | Baseline | Peak Sustained | Burst Max | Breaking Point | Scaling Trigger |
|---|---|---|---|---|---|
| RPS | 15k | 50k | 200k | 250k | Auto-scale at 70% |
| p99 Latency | 200ms | 400ms | 800ms | 1200ms | Alert at 600ms |
| Memory/Pod | 512MB | 1GB | 2GB | 3GB | Scale at 80% |
| DB Connections | 50 | 150 | 400 | Pool max 500 | Alert at 80% |
| Kafka Lag | 0 | 100ms | 2s | 10s | Alert at 1s |

**Pre-Mortem**: Top 3 failure causes: (1) Kafka consumer lag selama flash sale → inventory oversell, (2) Saga compensation gagal saat payment gateway timeout, (3) Projection lag menyebabkan stale read di admin dashboard. Mitigasi: idempotent inventory deduction, saga timeout + dead letter queue, read-your-writes consistency untuk admin.

### Step 6: Ultrathink Fase 4 — Convergence Matrix

| Kriteria | Bobot | A (Modular) | B (Microservice) | C (CQRS) |
|---|---|:---:|:---:|:---:|
| Data Integrity | 15% | 4 | 3 | 3 |
| Edge-Cases | 10% | 3 | 4 | 3 |
| Maintainability | 15% | 4 | 3 | 2 |
| Dependency Independence | 10% | 2 | 5 | 4 |
| Observability | 10% | 3 | 4 | 3 |
| Security (STRIDE) | 10% | 3 | 5 | 4 |
| Cost Efficiency | 10% | 5 | 3 | 2 |
| Cognitive Load | 10% | 4 | 3 | 2 |
| Regulatory Compliance | 10% | 3 | 4 | 3 |
| **Weighted Total** | **100%** | **3.50** | **3.75** | **2.85** |

**Winner**: Option B (Separate microservice + event-driven). Sanity check passed: Security = 5, Cognitive Load = 3 (acceptable).

### Step 7: ADR Output
ADR-047: Order Service Separation. Documented dengan full template termasuk dissent (engineer X argued Option A sufficient, recorded), validation criteria (flash sale test < 1% oversell rate dalam 3 bulan), dan architectural debt (projection lag accepted untuk admin reads).

### Step 8: Handoff
- → `msal-engineer`: ADR + C4 L3 + Implementation Spec + Saga sequence diagram
- → `msal-data`: Schema separation plan + expand-contract migration strategy
- → `msal-deploy`: Capacity plan + Kafka cluster sizing + auto-scale config
- → `msal-sentinel`: STRIDE findings + RLS policy design
- → `msal-verify`: Fitness functions (module boundary, API contract drift, saga completion rate)

### Step 9: Post-Launch Validation
3 bulan kemudian: Flash sale test 180k orders/hour, 0.3% oversell rate (below 1% threshold), p99 = 350ms (below 600ms alert). ADR validation criteria met. Architectural debt (admin projection lag) scheduled untuk Q3 remediation.

## Cross-Reference Index

Quick navigation antar bagian:

| Topic | Primary Section | Related Sections |
|---|---|---|
| Impact analysis | #4 | Knowledge Graph integration |
| API transport choice | #5 Transport Guide | #10 Distributed Systems |
| Cache invalidation | #5.4 | #10 Outbox Pattern |
| Rate limiting + tenancy | #5.3 | #13 Multi-Tenancy |
| Consistency model | #10 | #3 Fase 1 Invariants |
| Saga observability | #10 Saga | #14 Cross-Cutting Tracing |
| Tech selection → capacity | #11 | #3 Fase 3 Capacity Template |
| Migration rollback | #12 Rollback Criteria | #16 Post-Incident Review |
| Tenant lifecycle | #13 Lifecycle | #14 Cross-Cutting Logging |
| Fitness functions | #15 | #14 Verification Methods |
| Post-incident → anti-patterns | #16 | #9 Living Catalog |
| AI integration | #17 | #11 Tech Selection |
| DR/BCP | #24 | #14 Cross-Cutting, #16 Post-Incident |
| i18n | #25 | #15 Fitness Functions |
| Accessibility | #26 | #14 Cross-Cutting, #15 Fitness Functions |

## Applicability Assessment

Jawab 5 pertanyaan untuk menentukan bagian mana yang applicable:

1. **Project stage?** Pre-PMF → skip #12, #16, #21. Post-PMF → all applicable.
2. **Team size?** < 5 → simplify Fase 4 (skip Regulatory Compliance, reduce criteria). ≥ 5 → full matrix.
3. **Regulated industry?** Yes → add Regulatory Compliance criteria, prioritize #13, #14. No → skip regulatory overlay.
4. **Existing codebase > 6 months?** Yes → brownfield mode (#2). No → greenfield.
5. **Multi-tenant?** Yes → #13 mandatory. No → skip #13.

**Minimum Viable Architecture untuk Pre-PMF Startup**:
- Fase 1-4 simplified (3 kriteria: Correctness, Simplicity, Speed)
- ADR lightweight (context + decision + consequences only)
- Skip: #10, #12, #13, #15, #16, #17, #18, #19, #21, #22
- Focus: Module boundaries, basic API design, tech selection
