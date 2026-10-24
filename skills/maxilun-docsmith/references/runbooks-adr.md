# ADR, Operational Runbooks & Migration Guide Reference

Gunakan referensi ini saat menulis Architecture Decision Records (`docs/decisions/ADR-*.md`), runbook produksi (`docs/runbooks/*.md`), atau panduan migrasi antar-versi.

---

## 1. Standar Architecture Decision Record (ADR)

ADR yang baik mencatat **keputusan beserta opsi yang ditolak dan konsekuensi negatifnya**, bukan sekadar memuji pilihan yang diambil.

```markdown
# ADR-004: Gunakan Transactional Outbox di PostgreSQL untuk Pengiriman Event Pembayaran

- **Date**: 2026-10-24
- **Status**: Accepted
- **Deciders**: Backend Lead, Staff Engineer
- **Related PRD / Issue**: PRD-2026-001

## 1. Konteks & Masalah
Saat transaksi pembayaran berubah status menjadi `PAID`, layanan harus:
1. Mengubah baris di tabel `invoices` PostgreSQL.
2. Mengirim event `invoice.paid` ke worker pengiriman webhook dan email.

Jika layanan melakukan `COMMIT` ke PostgreSQL lalu langsung memanggil message broker secara sinkron, proses yang crash di antara dua langkah tersebut menyebabkan *dual-write inconsistency*: database mencatat `PAID`, tetapi event tidak pernah terkirim.

## 2. Opsi yang Dipertimbangkan

| Opsi | Kelebihan | Kekurangan / Risiko | Keputusan |
|---|---|---|---|
| **A. Dual-write langsung (DB commit lalu publish broker)** | Implementasi paling pendek (5 baris kode) | Kehilangan event saat broker timeout atau pod restart tepat setelah DB commit | ❌ Ditolak (melanggar invarian integritas finansial) |
| **B. Transactional Outbox table di PostgreSQL + Polling Worker (`FOR UPDATE SKIP LOCKED`)** | Atomik dalam 1 transaksi DB lokal; tidak butuh infrastruktur tambahan di luar PostgreSQL | Latensi pengiriman event bertambah `100ms - 500ms` sesuai interval polling; menambah beban tulis di tabel `outbox_events` | ✅ **Dipilih** |
| **C. Debezium CDC (Change Data Capture) + Kafka** | Latensi sangat rendah, tidak membebani aplikasi dengan polling | Kompleksitas operasional tinggi (Kafka Connect + Debezium cluster) untuk volume saat ini (`< 50 RPS`) | ❌ Ditolak (over-engineering untuk skala saat ini) |

## 3. Keputusan Detail
- Buat tabel `outbox_events` di database yang sama dengan `invoices`.
- Setiap mutasi status invoice wajib menulis ke `invoices` dan `outbox_events` di dalam **satu transaksi database (`BEGIN ... COMMIT`)**.
- Worker background menarik maksimal 50 baris per batch dengan query:
  ```sql
  SELECT id, payload FROM outbox_events
  WHERE status = 'PENDING' AND next_attempt_at <= NOW()
  ORDER BY created_at ASC
  LIMIT 50
  FOR UPDATE SKIP LOCKED;
  ```
- Partisi atau hapus baris `PROCESSED` yang lebih tua dari 7 hari melalui cron harian.

## 4. Konsekuensi & Trade-off
- **Positif**: Jaminan *at-least-once delivery* tanpa tambahan infrastruktur baru.
- **Negatif / Kewajiban**: Karena jaminan bersifat *at-least-once*, semua konsumen event wajib idempoten (deduplikasi via `event_id`).
- **Trigger Evaluasi Ulang**: Jika throughput tulis tabel `outbox_events` melampaui `1.500 TPS` atau utilisasi CPU PostgreSQL melewati `70%`, evaluasi migrasi ke `pg_logical` / CDC.
```

---

## 2. Standar Runbook Operasional & Incident Playbook (`docs/runbooks/*.md`)

Runbook ditulis untuk engineer yang sedang *on-call* pukul 03.00 pagi: perintah diagnostik harus **read-only terlebih dahulu**, langkah mitigasi harus jelas batas amannya, dan kriteria rollback harus terukur.

```markdown
# Runbook: Payment & Outbox Worker (`payment-service`)

## 1. Profil Layanan &SLO
| Atribut | Nilai |
|---|---|
| **Service Owner** | Tim Core Billing (`#oncall-billing`) |
| **Repo & Deploy** | `github.com/org/payment-service` (Kubernetes namespace: `prod-billing`) |
| **SLO Latency** | `POST /v1/invoices/{id}/qris` p95 < `300ms`, p99 < `800ms` |
| **SLO Availability** | `99.95%` (non-5xx responses) |
| **Outbox Lag Budget** | Usia event `PENDING` tertua < `30 detik` |

## 2. Pemeriksaan Cepat (Read-Only Triage — 60 Detik Pertama)

```bash
# 1. Cek status pod dan restart count terbaru
kubectl -n prod-billing get pods -l app=payment-service

# 2. Cek healthcheck endpoint dan koneksi DB
kubectl -n prod-billing exec deploy/payment-service -- curl -fsS http://localhost:8080/healthz

# 3. Cek error log 5 menit terakhir (tanpa mencetak secret/PII)
kubectl -n prod-billing logs deploy/payment-service --since=5m | grep -E '"level":"(error|fatal)"'
```

## 3. Playbook per Alert

### Alert A: `OutboxQueueLagHigh` (Event PENDING > 60 detik)
- **Dampak Bisnis**: Pembayaran sudah sukses di DB, tetapi webhook merchant dan notifikasi pelanggan tertunda.
- **Langkah Diagnostik (Read-Only)**:
  ```sql
  -- Cek distribusi status dan error terakhir di outbox
  SELECT status, count(*), min(created_at) AS oldest_event, max(retry_count) AS max_retries
  FROM outbox_events
  WHERE status IN ('PENDING', 'FAILED')
  GROUP BY status;
  ```
- **Langkah Mitigasi**:
  1. Jika `max_retries` meningkat karena satu endpoint merchant mati (HTTP 502/504), worker lain tidak boleh terblokir. Pastikan circuit breaker per-merchant aktif.
  2. Jika backlog murni karena lonjakan volume sah, naikkan replika worker sementara:
     ```bash
     kubectl -n prod-billing scale deployment/payment-outbox-worker --replicas=6
     ```
  3. **DILARANG** menjalankan `DELETE` atau `UPDATE status = 'PROCESSED'` secara manual tanpa memverifikasi apakah event sudah diterima oleh merchant.

### Alert B: `DatabaseLockContention` pada Tabel `invoices`
- **Langkah Diagnostik (Read-Only)**:
  ```sql
  SELECT blocked_locks.pid AS blocked_pid,
         blocking_locks.pid AS blocking_pid,
         now() - blocking_activity.query_start AS blocking_duration,
         blocking_activity.query AS blocking_query
  FROM pg_catalog.pg_locks blocked_locks
  JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
  JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
   AND blocking_locks.relation = blocked_locks.relation
   AND blocking_locks.pid != blocked_locks.pid
  JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
  WHERE NOT blocked_locks.granted;
  ```
- **Langkah Mitigasi**:
  1. Konfirmasi `blocking_pid` dan pastikan bukan proses migrasi skema yang sedang di akhir fase commit.
  2. Batalkan query penghambat secara halus terlebih dahulu: `SELECT pg_cancel_backend(<blocking_pid>);`.

## 4. Prosedur Rollback Rilis
Jika lonjakan error 5xx dimulai tepat setelah deployment baru:
```bash
# 1. Rollback instan ke revisi stabil sebelumnya
kubectl -n prod-billing rollout undo deployment/payment-service

# 2. Pantau hingga seluruh pod baru Ready
kubectl -n prod-billing rollout status deployment/payment-service --timeout=120s
```
> **Peringatan Migrasi DB**: Sesuai aturan zero-downtime `maxilun-data` (Expand-and-Contract), kode versi `N-1` wajib tetap kompatibel dengan skema database versi `N`. Jangan pernah menjalankan `down` migration yang menghapus kolom di produksi saat rollback aplikasi.
```

---

## 3. Standar Panduan Migrasi (Zero-Downtime & Breaking Changes)

Setiap panduan migrasi wajib memuat:
1. **Tabel Ringkasan Breaking Changes** (Apa yang berubah, siapa yang terdampak, batas waktu penghapusan).
2. **Perbandingan Kode Sebelum vs Sesudah** yang bisa langsung di-copy oleh engineer.
3. **Verifikasi Kompatibilitas** (perintah lint/test/codemod untuk memastikan migrasi tuntas).
