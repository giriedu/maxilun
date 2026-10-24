# Migration Strategies, Multi-Tenancy, Fitness Functions & Operational Architecture Playbook

Gunakan referensi ini untuk memandu modernisasi sistem legacy (brownfield), isolasi multi-tenant, perencanaan kapasitas & Disaster Recovery (DR), serta verifikasi arsitektur berkelanjutan.

---

## 1. Strategi Migrasi Brownfield & Zero-Downtime

### 1.1 Pola Migrasi Layanan
1. **Strangler Fig**: Pasang router/proxy di depan sistem lama → alihkan rute satu per satu ke modul baru → pantau paritas error → matikan rute lama setelah stabil.
2. **Branch by Abstraction**: Buat antarmuka abstraksi di kode pemanggil → bangun implementasi baru di belakang antarmuka tersebut → alihkan lewat feature flag → hapus implementasi lama.
3. **Parallel Run (Shadow Traffic)**: Gandakan traffic baca/kalkulasi secara asinkron ke sistem baru → bandingkan hasil (*diff*) tanpa memengaruhi respons user → cutover setelah `0` divergensi kritis.

### 1.2 Pola Migrasi Skema & Data (*Expand-and-Contract*)
Jangan pernah melakukan perubahan skema destruktif dalam satu rilis:
1. **Expand**: Tambah kolom/tabel baru yang bersifat nullable atau memiliki default aman (kompatibel dengan kode versi `N-1`).
2. **Dual-Write & Backfill**: Deploy kode yang menulis ke kolom lama dan baru; jalankan migrasi data historis dalam batch kecil (`LIMIT 1000` dengan jeda) agar tidak mengunci tabel.
3. **Switch Reads**: Verifikasi konsistensi checksum, lalu arahkan pembacaan ke kolom/tabel baru.
4. **Contract**: Hapus penulisan lama dan drop kolom lama pada rilis berikutnya.

### 1.3 Ambang Keputusan Rollback Instan
| Metrik | Batas Fix-Forward | Ambang Rollback Wajib |
|---|---|---|
| **Error Rate (5xx)** | `< 1%` di atas baseline | `> 5%` di atas baseline selama `> 5 menit` |
| **Latensi p99** | `< 2x` baseline | `> 3x` baseline selama `> 10 menit` |
| **Integritas / Korupsi Data** | `0` insiden | **1 insiden terkonfirmasi** (hentikan & rollback segera) |

---

## 2. Arsitektur Multi-Tenancy (SaaS Isolation)

| Model Isolasi | Mekanisme | Biaya Infra | Kompleksitas | Kapan Digunakan |
|---|---|---|---|---|
| **Shared DB, Shared Schema** | Kolom `tenant_id` + PostgreSQL Row-Level Security (RLS) | Paling Rendah | Rendah | SaaS tahap awal hingga menengah |
| **Shared DB, Schema-per-Tenant** | Namespace skema terpisah per organisasi | Menengah | Menengah | SaaS B2B dengan kebutuhan kustomisasi/backup per tenant |
| **Database-per-Tenant** | Instance / DB fisik terpisah | Tinggi | Tinggi | Enterprise teregulasi ketat (kesehatan, perbankan, pemerintahan) |
| **Hybrid Tiered** | Shared schema untuk tier standar, dedicated DB untuk tier Enterprise | Variabel | Tinggi | SaaS skala besar dengan segmen pasar campuran |

**Invarian Wajib Seluruh Model Multi-Tenant**:
- Konteks `tenant_id` wajib diekstrak dari sesi autentikasi yang terverifikasi di server; **dilarang** mempercayai `tenant_id` mentah dari body/query request client.
- Aktifkan **PostgreSQL RLS** (`CREATE POLICY tenant_isolation ON ... USING (tenant_id = current_setting('app.current_tenant')::uuid)`) sebagai pertahanan lapis kedua.
- Semua cache key (Redis), job queue payload, dan log wajib menyertakan prefix `tenant_id`.

---

## 3. Cross-Cutting Concerns, DR/BCP, i18n & Architectural Accessibility

### 3.1 Checklist Cross-Cutting Wajib di Setiap ADR
| Aspek | Standar Minimal Produksi | Metode Verifikasi (`maxilun-verify` / `maxilun-deploy`) |
|---|---|---|
| **Structured Logging** | JSON dengan `trace_id`, `tenant_id`, dan masking PII otomatis | Tes sampling log pada skenario error |
| **Distributed Tracing** | Propagasi header OpenTelemetry (`traceparent`) lintas layanan/worker | Pemeriksaan kelengkapan span trace |
| **Health Probes** | `/health/live` (proses hidup) & `/health/ready` (koneksi DB/dependensi siap) | Uji probe container saat startup & beban tinggi |
| **Graceful Shutdown** | Tangkap `SIGTERM`, hentikan terima request baru, selesaikan request aktif (`<= 30s`), tutup pool DB | Uji restart rolling tanpa dropped request |
| **Secrets & Rotation** | Tanpa secret di kode; rotasi kunci signing/API dengan masa overlap (dual-key verification) | Secret scanner di CI + uji rotasi kunci |

### 3.2 Matriks Disaster Recovery (RPO / RTO)
| Target RPO (Kehilangan Data Maks) | Target RTO (Waktu Pulih Maks) | Arsitektur yang Dibutuhkan |
|---|---|---|
| `0` (Zero data loss) | `< 1 menit` | Replikasi sinkron lintas-zona/region + failover otomatis aktif-aktif |
| `< 1 menit` | `< 5 menit` | Streaming replikasi asinkron + promosi replica otomatis |
| `< 1 jam` | `< 1 jam` | Point-in-Time Recovery (PITR / WAL archiving) + warm standby |
| `< 24 jam` | `< 4 jam` | Snapshot harian terenkripsi + prosedur restore teruji bulanan |

### 3.3 Arsitektur AI/LLM, Serverless/Edge, i18n & Aksesibilitas
- **AI/LLM Integration**: Wajib menetapkan batas *Token Budget* per user/tenant, *Timeout & Fallback Chain* (Model Utama → Model Ringan → Respons Degradasi Terukur), validasi skema output ketat (JSON Schema/Zod), dan isolasi PII sebelum mengirim prompt ke pihak ketiga.
- **Serverless / Edge Runtime**: Gunakan connection pooling eksternal (misal PgBouncer / HTTP driver) untuk mencegah habisnya koneksi database saat terjadi lonjakan konkurensi *cold-start*.
- **Internationalization (i18n)**: Simpan seluruh waktu di DB sebagai `UTC` (`TIMESTAMPTZ`), simpan uang sebagai integer minor unit + kode mata uang ISO 4217 (`IDR`, `USD`), dan gunakan properti logis CSS (`margin-inline-start`) bila mendukung bahasa RTL.
- **Architectural Accessibility**: Pastikan struktur SSR/routing menghasilkan hierarki landmark ARIA dan manajemen fokus lintas-rute secara konsisten; koordinasikan implementasi visualnya dengan `maxilun-craft`.

---

## 4. Architecture Fitness Functions (Penegakan Otomatis di CI)

Arsitektur yang tidak diuji secara otomatis akan membusuk. Definisikan aturan berikut untuk ditegakkan oleh `maxilun-verify` dan `maxilun-deploy`:

| Fitness Function | Pemeriksaan Otomatis | Tindakan Jika Gagal |
|---|---|---|
| **Module Boundary Guard** | `core/` dilarang mengimpor dari `ui/`, `components/`, atau handler framework HTTP | Gagalkan PR (`Block Merge`) |
| **Circular Dependency Check** | Graf impor di `maxilun-knowledge-graph` / linter bebas siklus (`A -> B -> A`) | Gagalkan PR (`Block Merge`) |
| **API Contract Drift** | Spesifikasi OpenAPI/skema cocok dengan tipe DTO handler aktual | Gagalkan PR (`Block Merge`) |
| **Tenant Guard Coverage** | Semua query pada tabel multi-tenant melewati guard `tenant_id` / RLS | Gagalkan PR (`Block Merge`) |

---

## 5. Worked Example Ringkas: Pemisahan Layanan Order E-Commerce (50k → 200k Orders/Jam)

1. **Pemetaan (`maxilun-knowledge-graph`)**: Ditemukan modul `Order` memiliki 47 pemanggil langsung dan melakukan join langsung ke tabel `inventory` serta `payments` (siklus ketergantungan pada reservasi stok).
2. **Dekomposisi & STRIDE (Fase 1 `/msal-think`)**:
   - *Invarian*: Nol kehilangan data pembayaran; nol *overselling* saat flash sale; kompatibilitas mundur untuk 6 layanan internal.
   - *Ancaman Kritis*: Habisnya connection pool DB saat flash sale (`DREAD = 20`) dan manipulasi status order langsung via tabel bersama (`DREAD = 17`).
3. **Evaluasi 3 Hipotesis & Konvergensi (Fase 2–4)**:
   - *Opsi A (Modular Monolith)*: Skor `3.50` — cepat, tetapi masih berbagi pool koneksi DB saat lonjakan 200k/jam.
   - *Opsi B (Order Service Terpisah + Transactional Outbox + Event-Driven Inventory)*: Skor **`3.75` (Terpilih)** — isolasi kegagalan penuh dan skala independen.
   - *Opsi C (Full Event Sourcing + CQRS)*: Skor `2.85` — beban kognitif tim terlalu tinggi untuk tenggat waktu saat ini.
4. **Eksekusi & Handoff**:
   - Catat keputusan di `docs/decisions/ADR-047-order-service-separation.md` (`maxilun-docsmith`).
   - Jalankan migrasi skema *Expand-Contract* (`maxilun-data`), implementasi Saga idempoten (`maxilun-engineer`), dan pasang fitness function batas modul (`maxilun-verify`).
