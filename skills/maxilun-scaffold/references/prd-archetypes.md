# Domain Archetypes for PRD, Security, Architecture & Design Bootstrap

Gunakan matriks archetype ini saat menjalankan `maxilun-scaffold` agar 10 dokumen di `docs/` langsung berisi invarian domain yang tajam dan terhubung ke sistem desain nyata di `../maxilun-craft/references/design-md/index.md`.

---

## 1. Peta Archetype Domain → Invarian Konteks & Referensi UI/UX

| Archetype Produk | Invarian Wajib di `PRD.md` & `GLOSSARY.md` | Invarian `ARCHITECTURE.md` & `TECHSTACK.md` | Invarian `SECURITY.md` (`maxilun-sentinel`) | Referensi UI/UX `DESIGN.md` (`../maxilun-craft/references/design-md/`) |
|---|---|---|---|---|
| **1. Fintech, Billing, Payment & Ledger** | Satuan moneter terkecil (`BIGINT` IDR/cents), alur rekonsiliasi settlement, refund/dispute rules, audit trail | Double-entry ledger atau transactional outbox, `Idempotency-Key` wajib di semua endpoint mutasi | Verifikasi signature webhook (`HMAC-SHA256` + `timingSafeEqual`), masking PII/nomor rekening di log, MFA untuk pencairan dana | `stripe.md`, `wise.md`, `mercury.md`, `revolut.md` (fokus: `tabular-nums`, kontras tinggi, status warna semantik tegas) |
| **2. B2B SaaS, ERP, CRM & Workflow** | Hierarki organisasi (`Organization` → `Workspace` → `Member`), matriks RBAC per role, state machine approval, bulk import/export | Multi-tenancy isolation (`tenant_id` di setiap tabel + Row-Level Security / middleware guard), background job queue | Pencegahan IDOR lintas-tenant, session revocation saat role berubah, audit log perubahan konfigurasi | `linear.app.md`, `notion.md`, `airtable.md`, `cal.md` (fokus: kepadatan informasi tinggi, navigasi keyboard `Cmd+K`, panel tenang) |
| **3. DevTools, Cloud Infra, Observability & AI Apps** | Manajemen API key/token, kuota pemakaian & rate limit, latensi streaming (SSE/WebSocket), dokumentasi CLI/API | Pemisahan control plane vs data plane, time-series / log storage, antrean job asinkron dengan batas timeout jelas | Hashing API key di database (simpan hanya prefix + hash SHA-256/Argon2), proteksi prompt injection / SSRF pada webhook | `vercel.md`, `sentry.md`, `posthog.md`, `supabase.md`, `cursor.md` (fokus: dark-first opsional, font monospace presisi, blok kode mudah di-copy) |
| **4. E-Commerce, Marketplace & Booking** | Katalog varian/SKU, reservasi stok sementara (inventory hold TTL), state machine pesanan (`CART` → `PAID` → `FULFILLED`), komisi | Pencarian berindeks cepat, pencegahan race condition saat flash sale (`SELECT ... FOR UPDATE`), integrasi kurir/payment | Validasi harga wajib di server (jangan pernah percaya harga dari payload keranjang client), rate limit checkout | `shopify.md`, `airbnb.md`, `nike.md` (fokus: hierarki harga jelas, mobile bottom-sheet checkout, tap target `>=44px`) |
| **5. Media, EdTech, Dokumentasi & Portal Konten** | Hierarki konten (Course/Article/Module), progres pembaca/siswa, pencarian instan, aksesibilitas baca panjang | Static/ISR caching, optimasi aset media, indeks pencarian teks penuh, penyediaan `/llms.txt` & `/llms-full.txt` | Proteksi konten berbayar (signed URL dengan TTL pendek), sanitasi input rich-text/Markdown terhadap Stored XSS | `wired.md`, `theverge.md`, `mintlify.md`, `sanity.md` (fokus: lebar baca `60ch-75ch`, skala tipografi editorial tajam) |

---

## 2. Prosedur Menurunkan `DESIGN.md` dari Referensi `maxilun-craft`

Saat `maxilun-scaffold` membuat `docs/DESIGN.md`:
1. **Jangan biarkan nilai warna dan tipografi seluruhnya `[TBD]`** jika kategori produk sudah diketahui dari interview atau scan repo.
2. Pilih **maksimal 2 file referensi** dari kolom terakhir tabel di atas (misal untuk aplikasi kasir/keuangan: baca `../maxilun-craft/references/design-md/wise.md` atau `stripe.md`).
3. Konversi prinsip visual dari file referensi tersebut ke dalam blok token OKLCH, skala tipografi, dan aturan komponen di `docs/DESIGN.md`.
4. Wajib tuliskan blok **Design Reference Record** di bagian atas `docs/DESIGN.md`:

```markdown
## Design Reference Record (`maxilun-craft`)
- **References**: `../maxilun-craft/references/design-md/linear.app.md`, `../maxilun-craft/references/design-md/stripe.md`
- **Applied**: Skala spasi 4px rapat untuk tabel operasional, `tabular-nums` pada seluruh kolom metrik/nominal, border hairline kontras terukur.
- **Rejected**: Hero animasi marketing kompleks yang tidak relevan untuk aplikasi internal.
- **Reason**: Pengguna utama adalah staf operasional yang membutuhkan pemindaian tabel cepat dan minim distraksi visual.
```

---

## 3. Checklist Kualitas `PRD.md` Sebelum Handoff

Sebelum `maxilun-scaffold` menyelesaikan pembuatan `docs/PRD.md`, pastikan:
- [ ] **Problem Statement** menyebut dampak terukur (waktu, risiko, atau biaya), bukan jargon abstrak.
- [ ] Setiap **Fitur MVP** memiliki kriteria penerimaan (*acceptance criteria*) yang dapat diuji langsung oleh `maxilun-verify`.
- [ ] Bagian **UI/UX Requirements** di `PRD.md` merujuk langsung ke `docs/DESIGN.md` dan mencantumkan kewajiban 4 state UI (Loading, Empty, Populated, Error).
- [ ] Bagian **Out of Scope (Non-Goals)** terisi minimal 2 item untuk menjaga fokus sprint pertama (YAGNI).
