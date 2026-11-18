# Maxilun Data References Index

Reference catalog for database engineering and query-layer optimization:

- **`references/zero-downtime-migrations.md`**: Safe Expand-Contract migration patterns, DDL changes with no service interruption, safe locking, and backfill handling.
- **`references/query-optimization-explain.md`**: EXPLAIN ANALYZE query plan diagnostics, composite index strategy, partial indexes, Row-Level Security (RLS) optimization, and the 5-Step Systematic Query Optimization Flow (Baseline $\to$ Scan Pruning $\to$ Spill-to-Disk Elimination $\to$ Rewrite $\to$ Comparative Proof).
- **`references/multi-tenant-isolation-rls.md`**: PostgreSQL Row-Level Security (RLS) architecture, PgBouncer transaction-mode pooling with `SET LOCAL`, tenant-leading composite indexes, and cross-tenant leak prevention.
