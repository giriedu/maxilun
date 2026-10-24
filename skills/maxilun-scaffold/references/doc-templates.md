# Canonical Templates for the 10 Project Context Documents (`docs/`)

Gunakan template di bawah ini saat men-generate atau meng-update `docs/`. Isi setiap bagian dengan fakta dari repositori (`[CONFIRMED]`), inferensi domain (`[ASSUMED]`), atau pertanyaan terbuka yang berlabel alasan (`[TBD: alasan]`).

---

## 1. `docs/PRD.md`

```markdown
# PRD — [Nama Project]

> **Status**: [Draft | Active | Frozen]  
> **Last Updated**: YYYY-MM-DD  
> **Owner**: [nama/role]  
> **Domain Archetype**: [Fintech | B2B SaaS | DevTools/AI | Commerce/Booking | Media/Content]

## Ringkasan Satu Paragraf
[Jelaskan APA yang dibangun, UNTUK SIAPA, dan MENGAPA — maks 3 kalimat konkret tanpa buzzword]

## Problem Statement & Bukti
[Masalah konkret yang diselesaikan: frekuensi kejadian, waktu yang hilang, atau risiko bisnis saat ini]

## Target Pengguna
| Persona | Konteks Kerja / Penggunaan | Kebutuhan Utama | Pain Point Saat Ini |
|---|---|---|---|
| [Persona A] | [Kapan & di perangkat apa dipakai] | ... | ... |
| [Persona B] | ... | ... | ... |

## Fitur — MVP (Must Have)
- [ ] **[MVP-01] [Nama Fitur]**: [Deskripsi fungsional]
  - *Acceptance Criteria*: Given [konteks], When [aksi], Then [hasil terukur + batas waktu/validasi].
  - *UI States (`DESIGN.md`)*: Loading skeleton, Empty state + CTA pertama, Populated state, Error state + langkah pemulihan.
- [ ] **[MVP-02] [Nama Fitur]**: [Deskripsi + acceptance criteria]

## Fitur — Phase 2 (Should Have)
- [ ] **[P2-01] [Fitur lanjutan]**

## Out of Scope / Non-Goals (Sengaja Tidak Dibangun)
- [x] **[Fitur X]**: [Alasan tegas mengapa tidak dibangun di fase ini]
- [x] **[Fitur Y]**: [Alasan tegas]

## Success Metrics
| Metrik | Baseline | Target | Cara Ukur / Sumber Data |
|---|---|---|---|
| [KPI 1] | [Angka sekarang / manual] | [Angka target] | [Event / query DB / log] |

## Constraints & Compliance
- **Timeline**: [CONFIRMED / TBD: alasan]
- **Budget / Infra**: [CONFIRMED / TBD: alasan]
- **Compliance & Privasi**: [UU PDP / GDPR / PCI-DSS / Tidak ada]
- **Target Platform**: [Web Responsive / Mobile-First / Desktop-Heavy / API-Only]
```

---

## 2. `docs/TECHSTACK.md`

```markdown
# TECHSTACK — [Nama Project]

> **Status**: [Proposed | Confirmed | Locked]  
> **Last Updated**: YYYY-MM-DD

## Stack Keputusan

| Layer | Teknologi | Versi | Alasan Dipilih | Alternatif Ditolak |
|---|---|---|---|---|
| **Frontend** | [Next.js / Vite / Astro / dll.] | [x.x] | [Alasan konkret] | [Apa yang ditolak + kenapa] |
| **Backend** | [Node.js / Go / Python / Rust] | [x.x] | [Alasan konkret] | ... |
| **Database** | [PostgreSQL / SQLite / MySQL] | [x.x] | [Alasan konkret] | ... |
| **Auth** | [Session HttpOnly / Auth.js / Custom] | [x.x] | [Alasan konkret] | ... |
| **ORM / Query** | [Drizzle / Prisma / SQLc / SQLAlchemy] | [x.x] | [Alasan konkret] | ... |
| **Styling** | [Native CSS OKLCH / Tailwind / CSS Modules] | [x.x] | [Alasan konkret] | ... |
| **Testing** | [Vitest / Playwright / Pytest] | [x.x] | [Alasan konkret] | ... |
| **Deployment** | [Docker / VPS / Cloud Run / Vercel] | - | [Alasan konkret] | ... |

## Dependency Policy
- Runtime version minimum: `[x.x.x]`
- Package manager: `[pnpm | npm | bun | uv | cargo]`
- Banned packages: [Daftar package yang dilarang di project ini beserta alasannya]

## Environment Variables
| Variabel | Scope | Wajib | Deskripsi | ContohFormat |
|---|---|---|---|---|
| `DATABASE_URL` | server | Ya | Connection string database utama | `postgresql://user:pass@localhost:5432/db` |
| `AUTH_SECRET` | server | Ya | Kunci kriptografi sesi/token (min 32 byte) | `openssl rand -base64 32` |
| `PUBLIC_APP_URL` | client/server | Ya | Base URL aplikasi | `https://app.example.com` |
```

---

## 3. `docs/DESIGN.md`

```markdown
# DESIGN — [Nama Project]

> **Status**: [Draft | Active]  
> **Last Updated**: YYYY-MM-DD  
> **Skill**: `maxilun-craft` (`/maxilun-craft`)

## Design Reference Record (`maxilun-craft`)
- **References**: `[Pilih 1-2 file dari ../maxilun-craft/references/design-md/index.md]`
- **Applied**: `[Prinsip hierarki, kepadatan komponen, tipografi, dan kontras yang diadaptasi]`
- **Rejected**: `[Elemen dari referensi yang sengaja tidak dipakai di produk ini]`
- **Reason**: `[Kesesuaian dengan persona pengguna dan tugas utama di PRD.md]`
- **Design Read**: `Reading this as: <page kind> for <audience>, in a <visual language> style, dial ENERGY X / RHYTHM Y / MOTION Z.`

## Brand & Visual Identity
- **Nama**: [Nama Project/Brand]
- **Kepribadian**: [Calm Operational / High-Craft Dark UI / Editorial Crisp / dll.]
- **Anti-vibe**: [Apa yang BUKAN tampilan produk ini — misal: bukan neon cyber, bukan glassmorphism bertumpuk]

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
- **Font Sans**: [Plus Jakarta Sans / Geist / सिस्टम font stack spesifik]
- **Font Mono**: [JetBrains Mono / Geist Mono]
- **Scale**: `12px (xs) → 14px (sm) → 16px (md/body) → 20px (lg) → 28px (xl) → 40px (2xl)`
- **Line Height**: Heading `1.2`, Body `1.55`, Max reading width `65ch`
- **Tabular Numerals**: Wajib `font-variant-numeric: tabular-nums` pada semua tabel harga, metrik, waktu, dan ID.

## Spacing & Layout (4px Grid)
- **Scale**: `4px → 8px → 12px → 16px → 24px → 32px → 48px → 64px`
- **Radius Hierarchy**: Child radius `<=` Parent radius (contoh: Card `12px`, Inner button/input `8px`, Badge `4px`).
- **Touch Targets**: Minimal `44x44px` di viewport mobile, input font size minimal `16px`.

## Mandatory 4 UI States Contract
Setiap layar dan komponen data wajib memiliki spesifikasi untuk:
1. **Loading**: Skeleton yang meniru proporsi layout akhir (`CLS = 0`), bukan spinner tunggal di tengah layar.
2. **Empty**: Penjelasan singkat mengapa data kosong + tombol aksi pertama yang konkret.
3. **Populated**: Tampilan data normal dengan penanganan teks panjang (`truncate` / `wrap`) dan angka tabular.
4. **Error**: Pesan penyebab spesifik yang dimengerti pengguna + tombol pemulihan (*retry* / alternatif).
```

---

## 4. `docs/SECURITY.md`

```markdown
# SECURITY — [Nama Project]

> **Status**: [Draft | Review | Approved]  
> **Last Updated**: YYYY-MM-DD  
> **Skill**: `maxilun-sentinel` (`/maxilun-sentinel`)

## Threat Model (STRIDE)
| Ancaman | Vector Spesifik Project Ini | Mitigasi Wajib | Status |
|---|---|---|---|
| **Spoofing** | Pencurian sesi / token palsu | Cookie `HttpOnly`, `Secure`, `SameSite=Lax/Strict` + rotasi refresh token | [TBD/Active] |
| **Tampering** | Manipulasi nominal/status di payload client | Validasi skema ketat di server + hitung ulang harga/state di server | [TBD/Active] |
| **Information Disclosure** | Kebocoran PII di log atau pesan error | Sanitasi log + respons error terstandar (RFC 9457) tanpa stack trace produksi | [TBD/Active] |
| **Denial of Service** | Flood pada login, checkout, atau upload | Rate limiting per IP & user + batas ukuran body request | [TBD/Active] |
| **Elevation of Privilege** | Akses resource milik user/tenant lain (IDOR) | Pemeriksaan kepemilikan (`resource.tenantId === session.tenantId`) di setiap query | [TBD/Active] |

## Authentication & Authorization
- **Metode Auth**: [Session Cookie / JWT + Refresh Rotation / OAuth2 / Passkeys]
- **Password Hashing**: Argon2id (konfigurasi memori & iterasi sesuai OWASP)
- **Model Otorisasi**: [RBAC / ABAC / Tenant Ownership Guard]
- **Daftar Role**: `[owner, admin, member, ...]`

## Cryptographic & Webhook Rules
- Primitif: Web Crypto API / `node:crypto` native; dilarang membuat skema enkripsi sendiri.
- Enkripsi data sensitif at-rest: `AES-256-GCM` dengan IV 12-byte unik dari CSPRNG.
- Verifikasi signature webhook/token: Wajib menggunakan perbandingan waktu konstan (`crypto.timingSafeEqual`).

## Data Privacy & Secrets
- Semua secret dari environment variable; `.env` wajib masuk `.gitignore`.
- Daftar PII yang disimpan: [Email, Nama, Nomor Telepon, ...] + kebijakan retensi & penghapusan.
```

---

## 5. `docs/STYLEGUIDE.md`

```markdown
# STYLEGUIDE — [Nama Project]

> **Last Updated**: YYYY-MM-DD  
> **Skill**: `maxilun-engineer` (`/maxilun-engineer`)

## Naming Conventions
- **Komponen UI**: `PascalCase` (`InvoiceTable.tsx`)
- **Fungsi & Variabel**: `camelCase` dengan kata kerja + objek spesifik (`calculateInvoiceTax`, bukan `handleData`)
- **Konstanta Domain**: `UPPER_SNAKE_CASE` (`MAX_UPLOAD_BYTES = 5_242_880`)
- **Tabel & Kolom DB**: `snake_case` (`payment_intents`, `created_at`, indeks `idx_<table>_<column>`)

## Code Hygiene & Structure
- Panjang file maksimal `300 baris`; kedalaman blok bersarang (nesting) maksimal `3 level` (gunakan early return / guard clause).
- Satu fungsi melakukan satu tanggung jawab pada satu tingkat abstraksi.
- Komentar hanya menjelaskan **MENGAPA** (alasan bisnis, workaround bug pihak ketiga, atau invarian), bukan menjelaskan APA yang sudah tertulis di kode.

## Error Handling & Validation
- Validasi semua input eksternal di batas masuk (*trust boundary*) menggunakan skema eksplisit (misal Zod/TypeBox/Pydantic).
- Jangan pernah menelan error dengan blok `catch {}` kosong.

## Git & PR Conventions
- Branch: `feat/<topik>`, `fix/<topik>`, `refactor/<topik>`, `docs/<topik>`.
- Commit: Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`).

## Non-Negotiable Prohibitions
- [ ] Dilarang `any` tanpa bukti justifikasi tertulis.
- [ ] Dilarang `console.log` / debug print tertinggal di jalur produksi.
- [ ] Dilarang hardcode secret, URL staging/produksi, atau magic number tanpa konstanta bernama.
- [ ] Dilarang menggunakan `float` / `number` pecahan untuk perhitungan uang.
```

---

## 6. `docs/TASK.md`

```markdown
# TASK — [Nama Project]

> **Sprint / Milestone**: [Milestone 1 — MVP Core]  
> **Last Updated**: YYYY-MM-DD

## Goal Milestone Aktif
[Satu kalimat hasil akhir yang harus berfungsi end-to-end pada milestone ini]

## In Progress (Maksimal 3 Item Aktif)
- [ ] **[TASK-001]** [Deskripsi konkret + file/modul target]
  - Verifikasi: [Tes atau skenario yang membuktikan task ini selesai]

## Backlog Prioritas
- [ ] **[TASK-002]** [Deskripsi] — *Priority: High*
- [ ] **[TASK-003]** [Deskripsi] — *Priority: Medium*

## Blocked
- **[TASK-00X]**: [Penyebab blocker] → [Langkah konkret untuk membuka blocker]

## Done
- [x] **[TASK-000]** Bootstrap 10 dokumen konteks proyek di `docs/` (`YYYY-MM-DD`)
```

---

## 7. `docs/ARCHITECTURE.md`

```markdown
# ARCHITECTURE — [Nama Project]

> **Last Updated**: YYYY-MM-DD  
> **Skill**: `maxilun-architect` (`/maxilun-architect`) & `maxilun-diagrams` (`/maxilun-diagrams`)

## C4 Level 1 & 2 — System & Container Diagram

```mermaid
flowchart TB
    User["Pengguna Utama"] -->|HTTPS| Web["Web / App Layer"]
    Web -->|Internal Call / API| Core["Domain & Service Layer"]
    Core -->|SQL / Transaction| DB[("Primary Database")]
    Core -->|HTTPS + HMAC| Ext["Layanan Eksternal"]
```

## Module Boundaries & Dependency Rules
| Modul / Folder | Tanggung Jawab | Boleh Mengimpor | Dilarang Mengimpor |
|---|---|---|---|
| `core/` / `domain/` | Aturan bisnis murni & kalkulasi | Hanya library standar & tipe internal | Framework HTTP, ORM langsung, komponen UI |
| `api/` / `server/` | Handler request, auth guard, transaksi | `core/`, `db/`, `lib/` | Komponen client/UI |
| `ui/` / `components/` | Rendering antarmuka & 4 state UI | `lib/`, kontrak tipe DTO | Koneksi DB atau secret server |

## Data Flow & Trust Boundaries
1. Request masuk → Middleware Autentikasi & Rate Limit.
2. Handler memvalidasi skema payload sebelum menyentuh service layer.
3. Mutasi multi-tabel wajib berjalan di dalam transaksi database atomik.

## Architecture Decision Records (ADR Summary)
- **ADR-001**: [Judul keputusan struktural pertama] — *Status: Accepted* (lihat detail di `docs/decisions/` bila menggunakan ADR terpisah).
```

---

## 8. `docs/SKILLS.md`

```markdown
# SKILLS — [Nama Project]

> Peta penggunaan spesialis Maxilun pada repositori ini.

## Spesialis Utama Proyek Ini
| Spesialis | Perintah | Kapan Digunakan di Proyek Ini |
|---|---|---|
| `maxilun` | `/maxilun` | Orkestrasi tugas lintas-domain & gate bukti |
| `maxilun-knowledge-graph` | `/maxilun-knowledge-graph` | Pemetaan dependensi simbol sebelum refaktor atau perubahan lintas-file |
| `maxilun-scaffold` | `/maxilun-scaffold` | Pembaruan 10 dokumen konteks di `docs/` tiap milestone |
| `maxilun-docsmith` | `/maxilun-docsmith` | Spesifikasi fitur/PRD lanjutan, kontrak OpenAPI, ADR, runbook, `llms.txt` |
| `maxilun-architect` | `/maxilun-architect` | Keputusan batas modul, kontrak API, strategi migrasi |
| `maxilun-craft` | `/maxilun-craft` | Implementasi UI/UX, token OKLCH, audit 4 state & aksesibilitas |
| `maxilun-frontend` | `/maxilun-frontend` | Arsitektur komponen server/client, state, dan performa bundle |
| `maxilun-data` | `/maxilun-data` | Desain skema DB, indeks, dan migrasi zero-downtime |
| `maxilun-sentinel` | `/maxilun-sentinel` | Audit keamanan, autentikasi, otorisasi, dan kriptografi |
| `maxilun-engineer` | `/maxilun-engineer` | Penulisan kode fitur, perbaikan bug, dan unit test |
| `maxilun-verify` | `/maxilun-verify` | Verifikasi test suite, typecheck, lint, dan E2E |
| `maxilun-deploy` | `/maxilun-deploy` | Pipeline CI/CD, containerization, dan kesiapan rilis |

## Ringkasan Cepat untuk Agen AI
- **Tujuan Produk**: [Ringkasan 1 kalimat dari `PRD.md`]
- **Stack Inti**: [Ringkasan 1 kalimat dari `TECHSTACK.md`]
- **Invarian Kritis**: [Ringkasan aturan keamanan/data yang tidak boleh dilanggar]
```

---

## 9. `docs/GLOSSARY.md`

```markdown
# GLOSSARY — [Nama Project]

> Ubiquitous Language: semua developer dan agen AI wajib memakai istilah yang sama di kode, skema DB, dan UI.

## Istilah Domain Bisnis
| Istilah Kanonik | Definisi Presisi | Sinonim yang Dilarang di Kode/UI |
|---|---|---|
| **[Entitas 1]** | [Definisi tepat beserta siklus hidupnya] | [Istilah ambigu yang dilarang] |
| **[Entitas 2]** | [Definisi tepat] | [Istilah ambigu yang dilarang] |

## Aturan Penamaan Domain
- Gunakan istilah kanonik di atas secara konsisten mulai dari nama tabel database, tipe TypeScript/struct, endpoint API, hingga teks label di UI.
```

---

## 10. `docs/ONBOARDING.md`

```markdown
# ONBOARDING — [Nama Project]

> Panduan orientasi cepat untuk engineer baru dan agen AI.

## Urutan Baca untuk Agen AI (Context Loading Order)
1. `docs/PRD.md` → Pahami masalah bisnis, fitur MVP, dan non-goals.
2. `docs/ARCHITECTURE.md` & `docs/TECHSTACK.md` → Pahami batas modul dan stack.
3. `docs/DESIGN.md` → Pahami token OKLCH, referensi `maxilun-craft`, dan aturan 4 state UI.
4. `docs/SECURITY.md` & `docs/STYLEGUIDE.md` → Pahami larangan keras dan batas keamanan.
5. `docs/TASK.md` → Cek fokus pekerjaan aktif saat ini.

## Setup Lokal untuk Engineer
```bash
# 1. Install dependencies
[perintah install sesuai package manager]

# 2. Salin dan isi environment variables
cp .env.example .env

# 3. Jalankan migrasi & seed database lokal
[perintah migrasi DB]

# 4. Jalankan server development
[perintah dev server]

# 5. Verifikasi seluruh pemeriksaan lulus
[perintah typecheck && lint && test]
```
```
