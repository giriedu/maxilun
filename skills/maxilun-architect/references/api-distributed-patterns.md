# API Design Contracts, Distributed Systems & Technology Selection Reference

Gunakan referensi ini bersama `maxilun-architect` saat merancang kontrak API, melakukan *Event Storming*, memilih model konsistensi terdistribusi, atau mengevaluasi adopsi teknologi baru.

---

## 1. Pola Desain Kontrak API (API Design Patterns)

### 1.1 Matriks Pemilihan Transport
| Use Case | Transport Rekomendasi | Alasan Teknis |
|---|---|---|
| Public API, browser clients | REST / HTTP (OpenAPI 3.1) | Dukungan universal, HTTP caching native, inspeksi mudah |
| Internal service-to-service throughput tinggi | gRPC (Protobuf) | Serialisasi biner cepat, streaming dua arah, kontrak ketik ketat |
| Agregasi UI kompleks dengan variasi field | GraphQL | Menghindari over/under-fetching pada layar komposit |
| Update real-time satu arah (server ke client) | SSE (Server-Sent Events) | Berjalan di atas HTTP standar, reconnect otomatis, ramah firewall |
| Kolaborasi dua arah latensi rendah | WebSocket | Koneksi persisten full-duplex |
| Event streaming & log pipeline | Kafka / NATS JetStream | Replayable, terpartisi, throughput tinggi |
| Notifikasi antar-organisasi (B2B) | Webhook (HTTP POST + HMAC) | Terdekopel, mendukung retry dengan backoff |

### 1.2 Standar Endpoint Produksi
1. **Pagination**: Utamakan **Cursor-Based** (`?cursor=<opaque>&limit=25`, max cap `100`) dengan respons `{ data, page_info: { has_next_page, next_cursor } }`. Hindari `OFFSET` besar pada tabel produksi.
2. **Filtering & Sorting**: Gunakan query terindeks (`?status=active&sort=-created_at`). Tolak filter pada kolom yang tidak memiliki indeks database dengan HTTP `400`.
3. **Rate Limiting Multi-Tenant**: Sertakan `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, dan `Retry-After` (pada HTTP `429`). Pisahkan bucket per `tenant_id` agar satu tenant tidak menghabiskan kuota tenant lain (*noisy neighbor*).
4. **Idempotency Mutasi**: Wajibkan header `Idempotency-Key` (UUID v4, TTL 24 jam) untuk semua operasi `POST`/`PATCH` yang memicu mutasi finansial atau pembuatan resource. Key sama + payload berbeda → kembalikan `409 Conflict`.
5. **Webhook Security**: Format payload wajib memuat `event_id`, `timestamp` (tolak jika umur `> 300s`), dan header signature `HMAC-SHA256` yang diverifikasi dengan `crypto.timingSafeEqual`.

---

## 2. Event Storming & Penemuan Bounded Context

Sebelum menetapkan batas modul atau memecah layanan baru:
1. **Domain Events** (*past-tense verb*): `InvoiceCreated`, `PaymentSettled`, `StockReserved`.
2. **Commands** (*imperative*): `CreateInvoice`, `SettlePayment`, `ReserveStock`.
3. **Aggregates & Invariants**: Satukan command dan event yang berbagi satu invarian transaksional ke dalam satu *Aggregate* (kandidat kuat *Bounded Context*).
4. **Brownfield Reconciliation**: Bandingkan hasil Event Storming dengan peta aktual dari `maxilun-knowledge-graph` untuk menemukan kebocoran batas modul (misal: tabel yang di-join silang oleh banyak domain).

---

## 3. Pola Sistem Terdistribusi (Distributed Systems Patterns)

### 3.1 Pemilihan Model Konsistensi
| Model | Jaminan | Gunakan Saat | Hindari Saat |
|---|---|---|---|
| **Strong (ACID)** | Baca/tulis linearizable dalam 1 DB | Buku besar keuangan, saldo, stok barang, token auth | Lintas-region dengan syarat latensi tulis sangat rendah |
| **Sequential** | Urutan total terjaga per stream/partisi | Audit log, state machine per entitas | Penulis konkuren bebas tanpa kunci partisi |
| **Causal** | Urutan sebab-akibat terjaga | Komentar berbalas, kolaborasi dokumen | Operasi CRUD independen biasa |
| **Eventual** | Konvergen seiring waktu | Feed aktivitas, pengiriman notifikasi, analitik agregat | Pengguna menuntut kepastian saldo/status instan |

### 3.2 Transactional Outbox, Saga & CQRS
- **Transactional Outbox**: Tulis perubahan tabel bisnis + baris tabel `outbox_events` dalam **satu transaksi database lokal**. Worker mem-polling dengan `SELECT ... FOR UPDATE SKIP LOCKED` (atau CDC untuk skala tinggi) lalu mem-publish ke broker. Semua konsumen wajib idempoten.
- **Saga Pattern**:
  - *Choreography* (`< 4 langkah`): Layanan bereaksi terhadap event.
  - *Orchestration* (`>= 4 langkah`): Satu koordinator mengatur langkah maju dan mengeksekusi transaksi kompensasi (*compensating action*) yang idempoten saat terjadi kegagalan.
- **Event Sourcing & CQRS**: Gunakan **hanya** jika audit replay historis adalah syarat mutlak bisnis atau rasio baca:tulis timpang ekstrem (`> 10:1`) dengan kebutuhan skema baca terdenormalisasi.

### 3.3 Matriks Pemilihan Message Broker
| Kriteria | PostgreSQL (`SKIP LOCKED`) | RabbitMQ | Redis Streams | NATS JetStream | Apache Kafka |
|---|---|---|---|---|---|
| **Throughput** | Rendah–Menengah (`< 1k/s`) | Menengah (`10k/s`) | Tinggi (`50k+/s`) | Tinggi (`100k+/s`) | Sangat Tinggi (`500k+/s`) |
| **Beban Operasional** | Nol (pakai DB yang ada) | Rendah | Rendah | Rendah–Menengah | Tinggi |
| **Event Replay** | Ya (selama belum di-purge) | Terbatas | Terbatas | Penuh | Penuh (jangka panjang) |
| **Kapan Dipilih** | Default untuk MVP & monolith modular | Task routing kompleks | Cache invalidation & realtime | Microservices cloud-native ringan | Log event skala besar & analitik |

---

## 4. Kerangka Pemilihan Teknologi (Technology Selection Matrix)

Saat mengevaluasi adopsi library, database, atau infrastruktur baru:

| Kriteria | Bobot Default | Pertanyaan Kunci |
|---|---|---|
| **Keahlian Tim (Team Expertise)** | `25%` | Berapa engineer yang sudah pernah mengoperasikannya di produksi? |
| **Kematangan Ekosistem** | `15%` | Kualitas dokumentasi, stabilitas rilis, dukungan tipe/tooling? |
| **Biaya Operasional & Integrasi** | `15%` | Beban infra, observabilitas, dan *Brownfield Multiplier* (`1.5x–2.0x` jika harus refaktor sistem lama)? |
| **Ketersediaan Talenta** | `15%` | Kemudahan rekrutmen dan pemeliharaan jangka panjang? |
| **Batas Performa (Headroom)** | `10%` | Apakah terbukti lewat *time-boxed spike* memenuhi target 3 tahun ke depan? |
| **Kepatuhan & Keamanan** | `10%` | Dukungan enkripsi, audit trail, dan residensi data? |
| **Stabilitas Lisensi & Exit Strategy** | `10%` | Risiko perubahan lisensi (BSL/SSPL) dan kejelasan jalur migrasi keluar? |

---

## 5. Katalog Anti-Pattern Arsitektur (Wajib Ditolak)

| Anti-Pattern | Gejala di Codebase | Tindakan Koreksi |
|---|---|---|
| **Distributed Monolith** | Layanan A memanggil B → C → D secara sinkron (HTTP/gRPC berantai) | Gabungkan kembali ke satu bounded context atau ubah ke event asinkron |
| **Shared Database Lintas-Service** | Dua layanan berbeda melakukan `INSERT/UPDATE` ke tabel fisik yang sama | Tetapkan satu pemilik tabel tunggal; ekspos akses lewat kontrak API/event |
| **Premature Microservices** | Tim `< 5 engineer` memecah 6 repo mikro sebelum domain stabil | Gunakan **Modular Monolith** dengan batas impor folder yang ditegakkan linter |
| **Anemic Domain & Leaky DTO** | Logika bisnis tersebar di handler HTTP dan mengembalikan baris ORM mentah ke publik | Isolasi logika di modul `core/` dan pisahkan skema DB dari DTO respons API |
