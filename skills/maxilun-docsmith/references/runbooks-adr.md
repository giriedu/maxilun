# ADR, Operational Runbooks & Migration Guide Reference

Use this reference when writing Architecture Decision Records (`docs/decisions/ADR-*.md`), production runbooks (`docs/runbooks/*.md`), or version-to-version migration guides.

---

## 1. Architecture Decision Record (ADR) Standard

A good ADR records **the decision together with the rejected options and its negative consequences**. It does not merely praise the option chosen.

```markdown
# ADR-004: Use a Transactional Outbox in PostgreSQL for Payment Event Delivery

- **Date**: 2026-10-24
- **Status**: Accepted
- **Deciders**: Backend Lead, Staff Engineer
- **Related PRD / Issue**: PRD-2026-001

## 1. Context & Problem
When a payment transaction changes status to `PAID`, the service must:
1. Update the row in the PostgreSQL `invoices` table.
2. Send an `invoice.paid` event to the webhook and email delivery workers.

If the service runs `COMMIT` against PostgreSQL and then calls the message broker synchronously, a process that crashes between the two steps causes a *dual-write inconsistency*: the database records `PAID`, but the event is never sent.

## 2. Options Considered

| Option | Advantages | Drawbacks / Risks | Decision |
|---|---|---|---|
| **A. Direct dual-write (DB commit, then publish to broker)** | Shortest implementation (5 lines of code) | Events are lost when the broker times out or the pod restarts right after the DB commit | [REJECTED] (violates financial integrity invariant) |
| **B. Transactional Outbox table in PostgreSQL + Polling Worker (`FOR UPDATE SKIP LOCKED`)** | Atomic within 1 local DB transaction; needs no infrastructure beyond PostgreSQL | Event delivery latency grows by `100ms - 500ms` depending on the polling interval; adds write load on the `outbox_events` table | **[SELECTED]** |
| **C. Debezium CDC (Change Data Capture) + Kafka** | Very low latency, does not burden the application with polling | High operational complexity (Kafka Connect + Debezium cluster) for the current volume (`< 50 RPS`) | [REJECTED] (over-engineering at current scale) |

## 3. Decision Detail
- Create an `outbox_events` table in the same database as `invoices`.
- Every invoice status mutation must write to `invoices` and `outbox_events` inside **one database transaction (`BEGIN ... COMMIT`)**.
- A background worker pulls at most 50 rows per batch with the query:
  ```sql
  SELECT id, payload FROM outbox_events
  WHERE status = 'PENDING' AND next_attempt_at <= NOW()
  ORDER BY created_at ASC
  LIMIT 50
  FOR UPDATE SKIP LOCKED;
  ```
- Partition or delete `PROCESSED` rows older than 7 days with a daily cron job.

## 4. Consequences & Trade-offs
- **Positive**: An *at-least-once delivery* guarantee with no new infrastructure.
- **Negative / Obligation**: Because the guarantee is *at-least-once*, every event consumer must be idempotent (deduplicate on `event_id`).
- **Re-evaluation Trigger**: If write throughput on the `outbox_events` table exceeds `1,500 TPS` or PostgreSQL CPU utilization passes `70%`, evaluate a migration to `pg_logical` / CDC.

## 5. Failure Modes & Mitigations
- **Worker Hang**: Worker process hangs mid-batch -> worker liveness probe restarts pod after 30s; `FOR UPDATE SKIP LOCKED` releases rows on connection drop.
- **Outbox Bloat**: Delivery errors cause pending rows to accumulate -> alert fires when `pending_count > 5,000`; dead-letter table receives records failing > 10 retries.

## 6. Fitness Functions (Automated Verification)
- `test_outbox_transaction_atomicity`: verifies invoice and outbox event are committed or rolled back together.
- `test_consumer_idempotency`: replaying the same `event_id` produces zero duplicate state mutations.
```

---

## 2. Operational Runbook & Incident Playbook Standard (`docs/runbooks/*.md`)

Write the runbook for an engineer who is *on-call* at 03:00: diagnostic commands are **read-only first**, each mitigation step states its safe limit, and rollback criteria are measurable.

```markdown
# Runbook: Payment & Outbox Worker (`payment-service`)

## 1. Service Profile & SLO
| Attribute | Value |
|---|---|
| **Service Owner** | Core Billing Team (`#oncall-billing`) |
| **Repo & Deploy** | `github.com/org/payment-service` (Kubernetes namespace: `prod-billing`) |
| **SLO Latency** | `POST /v1/invoices/{id}/qris` p95 < `300ms`, p99 < `800ms` |
| **SLO Availability** | `99.95%` (non-5xx responses) |
| **Outbox Lag Budget** | Age of the oldest `PENDING` event < `30 seconds` |

## 2. Quick Checks (Read-Only Triage — First 60 Seconds)

```bash
# 1. Check pod status and the latest restart count
kubectl -n prod-billing get pods -l app=payment-service

# 2. Check the healthcheck endpoint and the DB connection
kubectl -n prod-billing exec deploy/payment-service -- curl -fsS http://localhost:8080/healthz

# 3. Check error logs from the last 5 minutes (without printing secrets/PII)
kubectl -n prod-billing logs deploy/payment-service --since=5m | grep -E '"level":"(error|fatal)"'
```

## 3. Playbook per Alert

### Alert A: `OutboxQueueLagHigh` (PENDING Event > 60 seconds)
- **Business Impact**: The payment already succeeded in the DB, but the merchant webhook and customer notification are delayed.
- **Diagnostic Steps (Read-Only)**:
  ```sql
  -- Check the status distribution and the latest errors in the outbox
  SELECT status, count(*), min(created_at) AS oldest_event, max(retry_count) AS max_retries
  FROM outbox_events
  WHERE status IN ('PENDING', 'FAILED')
  GROUP BY status;
  ```
- **Mitigation Steps**:
  1. If `max_retries` rises because one merchant endpoint is down (HTTP 502/504), other workers must not be blocked. Confirm the per-merchant circuit breaker is active.
  2. If the backlog comes purely from a legitimate volume spike, raise the worker replicas temporarily:
     ```bash
     kubectl -n prod-billing scale deployment/payment-outbox-worker --replicas=6
     ```
  3. **NEVER** run `DELETE` or `UPDATE status = 'PROCESSED'` manually without verifying whether the merchant already received the event.

### Alert B: `DatabaseLockContention` on the `invoices` Table
- **Diagnostic Steps (Read-Only)**:
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
- **Mitigation Steps**:
  1. Confirm the `blocking_pid` and make sure it is not a schema migration process in the final part of its commit phase.
  2. Cancel the blocking query gently first: `SELECT pg_cancel_backend(<blocking_pid>);`.

## 4. Release Rollback Procedure
If a spike of 5xx errors starts right after a new deployment:
```bash
# 1. Roll back instantly to the previous stable revision
kubectl -n prod-billing rollout undo deployment/payment-service

# 2. Watch until every new pod is Ready
kubectl -n prod-billing rollout status deployment/payment-service --timeout=120s
```
> **DB Migration Warning**: Under the `maxilun-data` zero-downtime rule (Expand-and-Contract), code version `N-1` must stay compatible with database schema version `N`. Never run a `down` migration that drops a column in production during an application rollback.
```

---

## 3. Migration Guide Standard (Zero-Downtime & Breaking Changes)

Every migration guide must contain:
1. **A Breaking Changes Summary Table** (what changed, who is affected, the removal deadline).
2. **A Before vs After Code Comparison** that an engineer can copy directly.
3. **Compatibility Verification** (lint/test/codemod commands that confirm the migration is complete).
